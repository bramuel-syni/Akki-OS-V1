"""Session persistence — Phase 7 Stage B-1.

Collection `wizard_sessions` on Mongo. Indexes:
  * Unique on `session_id`.
  * Non-unique on `(variant, initiated_at)` for open-session listing.
  * Sparse unique on `frozen_objective_ref` (post-freeze integrity).
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from core import db
from contracts.wizard_commit_state import WizardCommitState_v0


WIZARD_SESSIONS_COLLECTION = "wizard_sessions"


async def upsert_session(state: WizardCommitState_v0) -> None:
    """Persist a WizardCommitState_v0 snapshot (mid-session or frozen)."""
    doc = state.model_dump(mode="json")
    doc["_id"] = state.session_id
    await db[WIZARD_SESSIONS_COLLECTION].replace_one(
        {"_id": state.session_id}, doc, upsert=True,
    )


async def load_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Read a session document by session_id; returns raw dict or None."""
    return await db[WIZARD_SESSIONS_COLLECTION].find_one({"_id": session_id})


async def load_frozen_wizard_state_by_objective_ref(
    frozen_objective_ref: str,
) -> Optional[WizardCommitState_v0]:
    """Look up the frozen wizard state that minted a given objective.

    Owner E1 Option C: `derive_license_class` reads FROZEN wizard state
    only. Callers pass frozen_objective_ref → this function returns the
    frozen WizardCommitState_v0 whose committed_at is set. Never returns
    a mid-session state (its `committed_at` would be None).
    """
    doc = await db[WIZARD_SESSIONS_COLLECTION].find_one(
        {"frozen_objective_ref": frozen_objective_ref}
    )
    if doc is None:
        return None
    if doc.get("committed_at") is None:
        # Structural check — never return a non-frozen state.
        return None
    doc.pop("_id", None)
    return WizardCommitState_v0.model_validate(doc)


async def ensure_indexes() -> None:
    """Create Mongo indexes at startup."""
    col = db[WIZARD_SESSIONS_COLLECTION]
    await col.create_index("session_id", unique=True)
    await col.create_index([("variant", 1), ("initiated_at", 1)])
    # Partial-filter unique — the index applies only when
    # frozen_objective_ref is a string (post-freeze). Mid-session
    # snapshots carry `frozen_objective_ref: null` which MUST NOT
    # collide across sessions.
    await col.create_index(
        "frozen_objective_ref",
        unique=True,
        partialFilterExpression={"frozen_objective_ref": {"$type": "string"}},
    )
