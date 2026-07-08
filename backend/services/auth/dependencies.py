"""Phase 8 Stage B-1 — FastAPI dependency: current_identity resolver.

Owner E1 ratified: JWT-based auth with server-side scope enforcement.
This module hosts the FastAPI `Depends()` primitives that other
routers reuse:

  * `get_current_identity_or_none(request)` — optional identity resolver;
    returns Identity if authenticated, None otherwise. Used by
    surfaces that permit anonymous access (Ask Console-full at B-1
    permits anonymous per the Owner-ratified E1 posture — auth is the
    scope-enforcement point, not a hard gate on the answer surface).
  * `require_identity(request)` — mandatory identity dependency;
    401s via auth_refusal.emit if no valid token.

Both parse `Authorization: Bearer <token>` (JWT single-source);
future OAuth adapters mint the same JWT claim shape (federation-forward).
"""
from __future__ import annotations

from typing import Optional

from fastapi import Request
from fastapi.responses import JSONResponse

from services.auth import auth_refusal
from services.auth.identity import Identity, KeyGrant
from services.auth.jwt_service import (
    TokenExpired,
    TokenInvalid,
    decode_token,
    extract_bearer_token,
)


class AuthDenied(Exception):
    """Raised by require_identity when no valid identity can be resolved.

    Carries the JSONResponse that the caller should return verbatim.
    """

    def __init__(self, response: JSONResponse):
        self.response = response


def _identity_from_claims(claims: dict) -> Identity:
    """Build an Identity Pydantic model from JWT claims (does NOT touch DB)."""
    return Identity(
        user_id=str(claims.get("sub", "")),
        email=str(claims.get("email", "")),
        roles=list(claims.get("roles", []) or []),
        key_grants=[KeyGrant(**g) for g in (claims.get("key_grants") or [])],
    )


async def get_current_identity_or_none(request: Request) -> Optional[Identity]:
    """Optional identity resolver. Returns None for anonymous callers."""
    token = extract_bearer_token(request.headers.get("Authorization"))
    if token is None:
        return None
    try:
        claims = decode_token(token, expected_type="access")
    except (TokenExpired, TokenInvalid):
        return None
    return _identity_from_claims(claims)


async def require_identity(request: Request) -> Identity:
    """Mandatory identity dependency. Raises AuthDenied with a ready-to-return 401/403 JSONResponse.

    Owner P9-E3 α (2026-07-08): a `worker_jwt` presented against a
    non-worker route returns 403 `auth_scope_insufficient` (existing
    4-code registry). No new codes minted.
    """
    token = extract_bearer_token(request.headers.get("Authorization"))
    if token is None:
        raise AuthDenied(auth_refusal.emit("auth_missing"))
    # Peek at the token type WITHOUT full validation so we can distinguish
    # a wrong-type token (worker_jwt on a non-worker route → 403 scope) from
    # a truly malformed / unknown token (→ 401 missing).
    try:
        import jwt as _jwt
        unverified = _jwt.decode(token, options={"verify_signature": False})
        if unverified.get("type") == "worker":
            raise AuthDenied(auth_refusal.emit("auth_scope_insufficient"))
    except AuthDenied:
        raise
    except Exception:
        pass
    try:
        claims = decode_token(token, expected_type="access")
    except TokenExpired:
        raise AuthDenied(auth_refusal.emit("auth_expired"))
    except TokenInvalid:
        raise AuthDenied(auth_refusal.emit("auth_missing"))
    return _identity_from_claims(claims)


async def require_identity_or_deny(request: Request):
    """Convenience wrapper: returns Identity OR a JSONResponse directly.

    Router handlers use this to short-circuit on auth denial:

        result = await require_identity_or_deny(request)
        if isinstance(result, JSONResponse):
            return result
        identity = result  # typed: Identity
    """
    try:
        return await require_identity(request)
    except AuthDenied as e:
        return e.response
