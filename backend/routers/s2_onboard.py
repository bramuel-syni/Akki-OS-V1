"""S2.onboard router — structured intake per Op. Values §8.

Owner ruling MC-E3 α (2026-07-14): initial-set writes = single-operator
(pre-birth defaults); changes to already-set values trigger the §6
ceremony. Every initial set writes an `initial_set: true` ledger row.

Endpoint: `POST /api/instance/{instance_id}/onboard`.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

from services.multi_instance.onboard_context import OnboardContextV0

router = APIRouter(prefix="/instance", tags=["s2-onboard"])

ONBOARD_COLLECTION = "instance_onboard_context"


def _db():
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    return client[os.environ["DB_NAME"]]


async def _append_initial_set_ledger_row(
    db, instance_id: str, seam_key: str, value: Any, submitted_by: str
) -> None:
    """Write an initial-set marker row to northena_ledger.

    Owner ruling MC-E3 α: 'every initial seam-value set writes a ledger row
    marked as initial-set — the ceremony is waived, the audit trail is not.'
    """
    ledger_row = {
        "instance_id": instance_id,
        "run_id": f"s2-onboard-{instance_id}",
        "stage": "s2_onboard_seam_value_set",
        "decision": "initial_set",
        "reason": f"seam_value:{seam_key}",
        "at": datetime.now(timezone.utc).isoformat(),
        "seam_key": seam_key,
        "seam_value_hash": str(hash(str(value)) % (10**16)),
        "initial_set": True,
        "submitted_by": submitted_by,
    }
    await db["northena_ledger"].insert_one(ledger_row)


@router.post("/{instance_id}/onboard")
async def s2_onboard(
    payload: OnboardContextV0,
    instance_id: str = Path(..., description="Target instance identifier."),
) -> Dict[str, Any]:
    """S2.onboard endpoint · structured intake.

    Change-detection at write layer: initial set (no prior context for
    instance_id + seam_key pair) → single-operator (initial_set: true
    ledger row). Subsequent changes trigger §6 ceremony (implemented in
    a follow-up phase; guard raised on second-set attempts).
    """
    if payload.instance_id != instance_id:
        raise HTTPException(
            status_code=400,
            detail=f"path instance_id={instance_id!r} disagrees with payload instance_id={payload.instance_id!r}",
        )
    db = _db()

    # Detect: is this the initial set for this instance?
    prior = await db[ONBOARD_COLLECTION].find_one({"instance_id": instance_id})
    is_initial_set = prior is None
    if not is_initial_set:
        # Subsequent change — §6 ceremony required (deferred to full impl).
        raise HTTPException(
            status_code=409,
            detail=(
                f"onboard_context already exists for instance_id={instance_id!r}; "
                "changes to seam values require §6 ceremony (dual-control for class-C "
                "deletion / rule-tightening delay). Follow-up phase implements the "
                "ceremony endpoint. Refusing initial-set overwrite."
            ),
        )

    doc = payload.model_dump(mode="python")
    doc["at"] = datetime.now(timezone.utc).isoformat()
    await db[ONBOARD_COLLECTION].insert_one(doc)

    # Initial-set ledger rows for each seam value (5 seams).
    submitted_by = payload.submitted_by or "unknown_operator"
    for k in [
        "deletion_consequence_classes",
        "rule_tightening_delay_hours",
        "objection_escalation_days",
        "suspension_re_review_days",
        "outer_gate_manual_review_threshold",
    ]:
        await _append_initial_set_ledger_row(
            db, instance_id, k, getattr(payload.seam_values, k), submitted_by
        )

    # Ledger row for the estate inventory + connector registration seat.
    await _append_initial_set_ledger_row(
        db, instance_id, "estate_inventory",
        [s.source_ref for s in payload.estate_inventory], submitted_by,
    )
    await _append_initial_set_ledger_row(
        db, instance_id, "org_vocabulary_seat", list(payload.org_vocabulary.keys()), submitted_by,
    )

    return {
        "outcome": "onboarded",
        "instance_id": instance_id,
        "initial_set": True,
        "seam_values_ledgered": 5,
        "estate_source_count": len(payload.estate_inventory),
        "org_vocabulary_categories": list(payload.org_vocabulary.keys()),
        "onboard_version": payload.onboard_version,
        "at": doc["at"],
    }


@router.get("/{instance_id}/onboard")
async def s2_onboard_read(instance_id: str) -> Dict[str, Any]:
    """Read the current instance's onboard context (post-set)."""
    db = _db()
    doc = await db[ONBOARD_COLLECTION].find_one({"instance_id": instance_id})
    if not doc:
        raise HTTPException(status_code=404, detail=f"no onboard context for {instance_id!r}")
    doc.pop("_id", None)
    return doc
