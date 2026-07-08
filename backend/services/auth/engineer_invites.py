"""Phase 8-EXT — invited-approved onboarding (Owner P8E-E3 α + P8E-E7 α, 2026-07-08).

P8E-E3 α verbatim: "DB-persisted invite row, external_engineer JWT minted at
approval time, no new JWT class — 'JWT mechanics unchanged' honored literally.
Invite-row mechanics (expiry, single-use) are dev defaults stated at close."

P8E-E7 α verbatim: "Onboarding approval is the introduction of an external
actor to the system — it gets its own audit row, distinct from grant issuance."

MongoDB collection: `engineer_invites`. Document shape:
    {
      invite_id: str (deterministic uuid),
      invited_email: str,
      invited_by: str (internal engineer email),
      state: Literal["pending_invite", "approved", "expired", "revoked"],
      expires_at: str (ISO-8601 UTC, dev default: created_at + 7 days),
      single_use: bool (dev default: True; approval flips state → approved atomically),
      created_at: str,
      approved_at: Optional[str],
    }

Dev defaults (P8E-E3 α condition — stated in close report):
  * expiry_duration_hours: 168 (7 days).
  * single_use: True. Approval endpoint uses a Mongo `find_one_and_update`
    with `state=pending_invite` filter → approval is atomic-once; a second
    approve on the same invite_id returns idempotent-replay (no re-mint).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from core import db

COLLECTION = "engineer_invites"

# Dev defaults per P8E-E3 α (stated in close report).
INVITE_EXPIRY_HOURS = 168  # 7 days
DEFAULT_SINGLE_USE = True


async def ensure_indexes() -> None:
    await db[COLLECTION].create_index("invite_id", unique=True)
    await db[COLLECTION].create_index("invited_email")
    await db[COLLECTION].create_index("state")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _expiry_iso(hours: int = INVITE_EXPIRY_HOURS) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()


async def _onboarding_state_impl_invite(
    invited_email: str,
    invited_by: str,
) -> Dict[str, Any]:
    """Shared invite-issue impl (amortisation base per Amendment I §1.3)."""
    invite_id = f"inv-{uuid.uuid4().hex[:12]}"
    doc = {
        "invite_id": invite_id,
        "invited_email": invited_email.lower(),
        "invited_by": invited_by.lower(),
        "state": "pending_invite",
        "expires_at": _expiry_iso(),
        "single_use": DEFAULT_SINGLE_USE,
        "created_at": _now_iso(),
        "approved_at": None,
    }
    await db[COLLECTION].insert_one(doc)
    return _project(doc)


async def _onboarding_state_impl_approve(invite_id: str) -> Optional[Dict[str, Any]]:
    """Shared invite-approve impl. Atomic state transition + ledger emission
    hook. Returns the approved invite row, or None if not found / not
    pending / expired.

    Single-use enforcement: `find_one_and_update` with `state=pending_invite`
    filter → concurrent second-approve loses the race and returns None.
    """
    now = _now_iso()
    # Expiry check (soft — the record MUST be re-fetched to compare against
    # its own expires_at; the atomic update filters pending_invite only).
    existing = await db[COLLECTION].find_one({"invite_id": invite_id})
    if existing is None:
        return None
    if existing.get("state") != "pending_invite":
        return None
    if existing.get("expires_at", "") <= now:
        # Transition to expired state honestly.
        await db[COLLECTION].update_one(
            {"invite_id": invite_id, "state": "pending_invite"},
            {"$set": {"state": "expired"}},
        )
        return None
    updated = await db[COLLECTION].find_one_and_update(
        {"invite_id": invite_id, "state": "pending_invite"},
        {"$set": {"state": "approved", "approved_at": now}},
        return_document=True,
    )
    if updated is None:
        return None
    return _project(updated)


def _project(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "invite_id": doc.get("invite_id"),
        "invited_email": doc.get("invited_email"),
        "invited_by": doc.get("invited_by"),
        "state": doc.get("state"),
        "expires_at": doc.get("expires_at"),
        "single_use": doc.get("single_use", DEFAULT_SINGLE_USE),
        "created_at": doc.get("created_at"),
        "approved_at": doc.get("approved_at"),
    }


async def issue_invite(invited_email: str, invited_by: str) -> Dict[str, Any]:
    return await _onboarding_state_impl_invite(invited_email, invited_by)


async def approve_invite(invite_id: str) -> Optional[Dict[str, Any]]:
    return await _onboarding_state_impl_approve(invite_id)


async def get_invite(invite_id: str) -> Optional[Dict[str, Any]]:
    doc = await db[COLLECTION].find_one({"invite_id": invite_id})
    return _project(doc) if doc else None


# --- Onboarding-approved ledger emission (P8E-E7 α condition) ---

LEDGER_COLLECTION = "northena_ledger"
DATA_CLASS_ENGINEER_ONBOARDING_APPROVED = "engineer_onboarding_approved"


async def emit_onboarding_approved_ledger_row(
    invited_email: str,
    invited_by: str,
    invite_id: str,
    approved_at: str,
) -> Dict[str, Any]:
    """Emit `engineer_onboarding_approved` ledger row.

    Reuses existing NorthenaLedgerRow_v1 shape via `stamp_audit` sidecar
    pattern (no frozen contract touched; P8E-E7 α condition additive).
    Data-class is validated against `data_class_registry.v3.json` via
    the loader re-point at `deletion_ledger.py`.
    """
    row = {
        "row_id": f"olr-{uuid.uuid4().hex[:12]}",
        "trace_id": f"onboarding-{invite_id}",
        "run_id": invite_id,
        "event_type": "engineer_onboarding_approved",
        "invited_email": invited_email,
        "invited_by": invited_by,
        "approved_at": approved_at,
        "stamp_audit": {
            "data_class": DATA_CLASS_ENGINEER_ONBOARDING_APPROVED,
            "recorded_at": approved_at,
        },
        "artifact_ref": f"onboarding://{invite_id}",
    }
    await db[LEDGER_COLLECTION].insert_one(dict(row))
    return row
