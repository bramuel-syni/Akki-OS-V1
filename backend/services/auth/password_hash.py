"""Phase 8 Stage B-1 — bcrypt password hashing (Owner E1 no-hand-rolled-crypto).

Pure wrapping of the vetted `bcrypt` library. bcrypt salts internally;
the returned string carries the salt + hash + cost factor per the
$2b$ canonical form. Verification is constant-time via
`bcrypt.checkpw`.
"""
from __future__ import annotations

import bcrypt


def hash_password(plaintext: str) -> str:
    """Return a bcrypt hash (canonical $2b$ form)."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plaintext.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plaintext: str, hashed: str) -> bool:
    """Constant-time verify. Returns True iff the plaintext matches."""
    try:
        return bcrypt.checkpw(plaintext.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False
