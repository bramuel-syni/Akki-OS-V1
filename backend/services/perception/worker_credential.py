"""Worker credential — capabilities-claim JWT (Owner P9-E3 α, 2026-07-08).

Owner ruling verbatim:
    "α, capabilities-claim worker JWT, two conditions. The allowlist shape:
     the credential names its exact two operations, rather than a role
     implying operations via route configuration — same up-from-permitted
     principle as the B-5a trace ruling. Conditions: (1) worker-auth
     denials use the existing 4-code registry, no new codes — registry
     stays closed; (2) 'all other routes reject worker_jwt' is proven by
     a parametrised negative gate (worker credential against
     representative non-worker routes → 403 access-class), not
     convention — V1-G5's AST covers the code side; this covers the
     credential side."

Token type: `worker` (distinct from `access`/`refresh`). Claims:
  * sub: worker_id
  * capabilities: List[str] — MUST be a subset of ALLOWED_CAPABILITIES.
  * type: "worker"
  * iat, exp

Two operations only:
  * worker_claim → POST /api/workers/jobs/claim
  * worker_result → POST /api/workers/jobs/{job_id}/result

Denial code on non-worker routes: `auth_scope_insufficient` (existing
4-code registry per Owner condition 1; no new codes).
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import List

import jwt
from fastapi import Request
from fastapi.responses import JSONResponse

from services.auth import auth_refusal
from services.auth.jwt_service import (
    JWT_ALGORITHM,
    TokenExpired,
    TokenInvalid,
    _get_jwt_secret,
    extract_bearer_token,
)

WORKER_TOKEN_TTL_HOURS = 24

CAP_CLAIM = "worker_claim"
CAP_RESULT = "worker_result"

ALLOWED_CAPABILITIES = {CAP_CLAIM, CAP_RESULT}


def mint_worker_token(worker_id: str, capabilities: List[str]) -> str:
    """Mint a worker credential JWT with capabilities allowlist.

    Every capability MUST be in ALLOWED_CAPABILITIES. Attempting to mint
    with a capability outside the allowlist raises ValueError — no
    string outside the closed set ever crosses the wire.
    """
    bad = [c for c in capabilities if c not in ALLOWED_CAPABILITIES]
    if bad:
        raise ValueError(f"Unknown worker capabilities: {bad}")
    now = datetime.now(timezone.utc)
    payload = {
        "sub": worker_id,
        "capabilities": list(capabilities),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=WORKER_TOKEN_TTL_HOURS)).timestamp()),
        "type": "worker",
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=JWT_ALGORITHM)


def decode_worker_token(token: str) -> dict:
    """Decode a worker JWT. Raises TokenExpired / TokenInvalid."""
    try:
        payload = jwt.decode(token, _get_jwt_secret(), algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise TokenExpired()
    except jwt.InvalidTokenError:
        raise TokenInvalid()
    if payload.get("type") != "worker":
        raise TokenInvalid()
    return payload


async def require_worker_capability(request: Request, required: str):
    """FastAPI dependency: assert bearer token is a worker JWT with `required` capability.

    Returns the decoded claims dict on success, OR a JSONResponse ready
    to return verbatim on denial (Owner E2 body shape {reason, detail}
    with existing 4-code registry).

    Denial matrix (Owner P9-E3 α):
      * No bearer token → 401 auth_missing
      * Expired → 401 auth_expired
      * Invalid signature / non-worker type / capability absent → 403 auth_scope_insufficient
    """
    token = extract_bearer_token(request.headers.get("Authorization"))
    if token is None:
        return auth_refusal.emit("auth_missing")
    try:
        claims = decode_worker_token(token)
    except TokenExpired:
        return auth_refusal.emit("auth_expired")
    except TokenInvalid:
        return auth_refusal.emit("auth_scope_insufficient")
    caps = claims.get("capabilities") or []
    if required not in caps:
        return auth_refusal.emit("auth_scope_insufficient")
    return claims
