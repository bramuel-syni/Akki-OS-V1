"""Phase 8 Stage B-1 — wizard session→identity binding.

Satisfies Phase 7 B-2 §0.2 "Wizard session-ownership binding" plan-debt
(Owner ruling: "lands with Phase 8 auth/key model — recorded as the
system-wide auth landing, not a wizard-special").

Sidecar table `db.wizard_session_bindings` — one document per bound
wizard session. Grandfathering: sessions initiated before this landing
are NOT in the table; the binding check tolerates missing binding via
a one-time carve-out (see `check_binding`).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from core import db

_COLLECTION = "wizard_session_bindings"


async def ensure_indexes() -> None:
    """Compound unique index on session_id (one binding per session)."""
    await db[_COLLECTION].create_index("session_id", unique=True)


async def bind_session_to_identity(session_id: str, user_id: str) -> None:
    """Record binding at wizard session creation time.

    Idempotent: repeat bind on same session_id updates nothing (unique
    index guards). If a different user_id attempts to rebind, the
    unique index violates; caller MUST NOT attempt cross-user rebind.
    """
    await db[_COLLECTION].update_one(
        {"session_id": session_id},
        {
            "$setOnInsert": {
                "session_id": session_id,
                "user_id": user_id,
                "bound_at": datetime.now(timezone.utc),
            }
        },
        upsert=True,
    )


async def get_bound_identity(session_id: str) -> Optional[str]:
    """Return the bound user_id, or None if session is unbound (grandfathered)."""
    doc = await db[_COLLECTION].find_one({"session_id": session_id})
    if doc is None:
        return None
    return doc.get("user_id")


async def check_binding(session_id: str, caller_user_id: Optional[str]) -> bool:
    """Return True iff the caller may operate on the session.

    Semantics:
      * If session has no binding (grandfathered pre-B-1) → True (permit).
      * If session has a binding and caller matches → True.
      * If session has a binding and caller mismatches → False.
      * If session has a binding and caller is anonymous → False.
    """
    bound = await get_bound_identity(session_id)
    if bound is None:
        return True  # Grandfathered
    if caller_user_id is None:
        return False
    return bound == caller_user_id
