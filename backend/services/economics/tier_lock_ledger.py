"""Phase 8 Stage B-4 Block 1 — Master-admin rule-change event ledger writer.

Mirror of B-3 `services/auth/engineer_key_grant_ledger.py`, adapted for
master-admin control-surface rule changes (tier lock is the canonical
Path A example; future Path A rules land here).

`stamp_audit.data_class="master_admin_rule_change"` marker
distinguishes rows from sibling data classes (engineer_key_grant,
wizard_transcript). Idempotent per (trace_id, run_id):
  * run_id = f"master-admin-rule-change-{rule_id}-{idempotency_key}"
Repeat POST with same rule_id + idempotency_key is a no-op returning
the existing run_id — the Owner-mandated "reversibility = opposite POST
writes a new row" is preserved (opposite POST carries a different
idempotency_key).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from contracts.northena_ledger import (
    LedgerArtifactRef,
    LedgerRow,
    NORTHENA_LEDGER_COLLECTION,
)
from core import db


DATA_CLASS_MASTER_ADMIN_RULE_CHANGE = "master_admin_rule_change"


def _run_id_for(rule_id: str, idempotency_key: str) -> str:
    return f"master-admin-rule-change-{rule_id}-{idempotency_key}"


async def _ledger_row_exists(trace_id: str, run_id: str) -> bool:
    existing = await db[NORTHENA_LEDGER_COLLECTION].find_one({
        "trace_id": trace_id, "run_id": run_id, "stage": "converge",
    })
    return existing is not None


async def record_master_admin_rule_change(
    rule_id: str,
    from_value: Any,
    to_value: Any,
    reason_note: Optional[str],
    versioned_file_path: str,
    grantor_id: str,
    idempotency_key: str,
    trace_id: str,
    lawful_basis_ref: str = "master-admin-rule-change-lawful-basis-v0",
) -> Dict[str, str]:
    """Write one ledger row per rule-change, idempotent per (trace_id, run_id).

    Returns `{"run_id": ..., "trace_id": ...}`. Repeat calls with the
    same (rule_id, idempotency_key) return the existing run_id without
    a second write.
    """
    run_id = _run_id_for(rule_id, idempotency_key)
    if await _ledger_row_exists(trace_id, run_id):
        return {"run_id": run_id, "trace_id": trace_id}
    row = LedgerRow(
        run_id=run_id,
        trace_id=trace_id,
        stage="converge",
        decision="terminate_success",
        reason=f"master_admin_rule_change:{rule_id}:from={from_value!r}:to={to_value!r}",
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request",
            artifact_id=f"master-admin-rule-{rule_id}",
            version="v0",
        ),
        lawful_basis_ref=lawful_basis_ref,
        stamp_audit={
            "data_class": DATA_CLASS_MASTER_ADMIN_RULE_CHANGE,
            "rule_change": {
                "rule_id": rule_id,
                "from": from_value,
                "to": to_value,
                "reason_note": reason_note,
                "versioned_file_path": versioned_file_path,
                "grantor_id": grantor_id,
                "idempotency_key": idempotency_key,
            },
        },
        at=datetime.now(timezone.utc),
    )
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump(mode="python"))
    return {"run_id": run_id, "trace_id": trace_id}
