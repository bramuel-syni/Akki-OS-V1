"""Northena Gate — Stage 2 (mandate §5).

Strict set-membership. NO inference. Ambiguous membership is a
compilation defect Admit should have caught (mandate §5 verbatim).

Cousin: no direct cousin — `synisense/shield/purpose_validator.py`'s
allow-list check is the closest pattern. Net-new state.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable, Optional

from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.northena.ledger import record as ledger_record


async def route(
    *, run_id: str, trace_id: str, sub_objective: str,
    artifact_ref: LedgerArtifactRef, lawful_basis_ref: str,
    scope: Iterable[str], warm_index: Optional[Iterable[str]] = None,
) -> dict:
    """Return `{decision, ledger_row, reason}`.

    decision ∈ {warm, fresh, refused} (§5 verbatim).
    """
    scope_set = set(scope)
    warm_set = set(warm_index or [])

    if sub_objective not in scope_set:
        row = LedgerRow(
            run_id=run_id, trace_id=trace_id, stage="gate", decision="refused",
            reason="out_of_scope",
            artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
            stamp_audit=None, at=datetime.now(timezone.utc),
        )
        await ledger_record(row)
        return {"decision": "refused", "ledger_row": row, "reason": "out_of_scope"}

    if sub_objective in warm_set:
        decision, reason = "warm", "in_scope_warm_serve"
    else:
        decision, reason = "fresh", "in_scope_fresh_extraction"
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id, stage="gate",
        decision=decision, reason=reason,  # type: ignore[arg-type]
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
        stamp_audit=None, at=datetime.now(timezone.utc),
    )
    await ledger_record(row)
    return {"decision": decision, "ledger_row": row, "reason": reason}
