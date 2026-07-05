"""Phase 8 Stage B-3 Block 3 — Engineer key-grant event ledger writer.

Owner D4b condition attached to unfrozen ruling (verbatim, 2026-07-04):
    "Grant issuance and revocation emit ledger rows (stamp_audit sidecar
     pattern, idempotent). The FOR-argument #1 dissolves only because
     the replay-verifiable audit chain lives in frozen
     NorthenaLedgerRow_v1 — which is true only if grant events actually
     reach it."

Writes engineer-key-grant lifecycle events (`issued` / `revoked`) to
the Northena Ledger via the stamp_audit sidecar pattern.
`data_class="engineer_key_grant"` marker distinguishes rows from
`wizard_transcript` sibling class (Owner E5 posture: separately-
addressable retention class; DPO ruling deferred).

Idempotent per `(trace_id, run_id)`:
  * issuance run_id = f"engineer-key-grant-issued-{grant_id}"
  * revocation run_id = f"engineer-key-grant-revoked-{grant_id}"
Repeat POST with same grant_id + event_type is a no-op returning the
existing run_id.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal, Optional

from contracts.northena_ledger import (
    LedgerArtifactRef,
    LedgerRow,
    NORTHENA_LEDGER_COLLECTION,
)
from core import db

from .engineer_key_grant import EngineerKeyGrantRegistration


DATA_CLASS_ENGINEER_KEY_GRANT = "engineer_key_grant"


EventType = Literal["issued", "revoked"]


def _run_id_for(event_type: EventType, grant_id: str) -> str:
    return f"engineer-key-grant-{event_type}-{grant_id}"


async def _ledger_row_exists(trace_id: str, run_id: str) -> bool:
    """Idempotency guard — mirrors turn_ledger._ledger_row_exists shape."""
    existing = await db[NORTHENA_LEDGER_COLLECTION].find_one({
        "trace_id": trace_id, "run_id": run_id, "stage": "converge",
    })
    return existing is not None


async def record_engineer_key_grant_event(
    event_type: EventType,
    grant: EngineerKeyGrantRegistration,
    trace_id: str,
    lawful_basis_ref: Optional[str] = None,
) -> str:
    """Write one ledger row per grant lifecycle event, idempotent per
    (trace_id, run_id).

    Returns the ledger `run_id`. Repeat calls with the same
    (event_type, grant_id) return the existing run_id without a
    second write.

    `stage="converge"` + `decision="terminate_success"` — parity with
    `turn_ledger.record_wizard_freeze` (both are governance-terminal
    single-shot events, not per-turn admissions/gates).
    """
    run_id = _run_id_for(event_type, grant.grant_id)
    if await _ledger_row_exists(trace_id, run_id):
        return run_id
    row = LedgerRow(
        run_id=run_id,
        trace_id=trace_id,
        stage="converge",
        decision="terminate_success",
        reason=f"engineer_key_grant:{event_type}:grant_id={grant.grant_id}",
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request",
            artifact_id=f"engineer-key-grant-{grant.grant_id}",
            version="v0",
        ),
        lawful_basis_ref=lawful_basis_ref or grant.lawful_basis_ref,
        stamp_audit={
            "data_class": DATA_CLASS_ENGINEER_KEY_GRANT,
            "engineer_key_grant": {
                "event_type": event_type,
                "grant_id": grant.grant_id,
                "grantee_email": str(grant.grantee_email),
                "grantor_id": grant.grantor_id,
                "key_class": grant.key_class,
                "path": grant.path,
                "floor": grant.floor,
                "scope": grant.scope,
                "lawful_basis_ref": grant.lawful_basis_ref,
                "revoked_at": (
                    grant.revoked_at.isoformat() if grant.revoked_at else None
                ),
                "revocation_reason": grant.revocation_reason,
                "retention_class_note": (
                    "Owner E5 posture: separately-addressable retention "
                    "class; DPO rules one window (inheritance) OR split "
                    "at Seam 3 unlock."
                ),
            },
        },
        at=datetime.now(timezone.utc),
    )
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump(mode="python"))
    return run_id
