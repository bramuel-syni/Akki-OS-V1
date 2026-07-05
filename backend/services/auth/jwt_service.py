"""Phase 8 Stage B-1 — PyJWT wrapping (Owner E1 standard-library-only).

Two token types:
  * `access` — 15 min expiry; carries user_id + email + roles + key_grants.
  * `refresh` — 7 days expiry; carries user_id + type only. Refresh
    endpoint validates and mints a new access token.

Federation-forward posture: JWT claim shape is the invariant. When
OAuth fronts the session layer later, the OAuth adapter mints the same
claim shape; downstream verification code is byte-identical.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import jwt

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_TTL_MINUTES = 15
REFRESH_TOKEN_TTL_DAYS = 7


def _get_jwt_secret() -> str:
    """Fail-fast if JWT_SECRET is absent."""
    secret = os.environ.get("JWT_SECRET")
    if not secret:
        raise RuntimeError(
            "JWT_SECRET missing from environment. Set via /app/backend/.env; "
            "restart backend service. Fail-fast per Owner E1 no-hand-rolled-crypto."
        )
    return secret


def create_access_token(
    user_id: str,
    email: str,
    roles: List[str],
    key_grants: List[Dict[str, Any]],
) -> str:
    """Mint a 15-minute access token."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "roles": roles,
        "key_grants": key_grants,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TOKEN_TTL_MINUTES)).timestamp()),
        "type": "access",
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Mint a 7-day refresh token."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=REFRESH_TOKEN_TTL_DAYS)).timestamp()),
        "type": "refresh",
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=JWT_ALGORITHM)


class TokenExpired(Exception):
    """JWT has expired (past `exp`)."""


class TokenInvalid(Exception):
    """JWT signature/shape invalid."""


def decode_token(token: str, expected_type: str) -> Dict[str, Any]:
    """Decode + verify a JWT. Raises TokenExpired / TokenInvalid.

    `expected_type` MUST be 'access' or 'refresh'. Type-mismatch → TokenInvalid.
    """
    try:
        payload = jwt.decode(token, _get_jwt_secret(), algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as e:  # noqa: F841
        raise TokenExpired()
    except jwt.InvalidTokenError as e:  # noqa: F841
        raise TokenInvalid()
    if payload.get("type") != expected_type:
        raise TokenInvalid()
    return payload


def extract_bearer_token(authorization_header: Optional[str]) -> Optional[str]:
    """Parse `Authorization: Bearer <token>`. Returns None on missing/malformed."""
    if not authorization_header:
        return None
    parts = authorization_header.split(None, 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip() or None
