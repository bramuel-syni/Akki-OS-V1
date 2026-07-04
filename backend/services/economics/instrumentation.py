"""Quote instrumentation — Phase 6 Stage B (v3 §8 bullet 3).

Owner ruling Axis 5 (Phase 6 Stage A close, 2026-07-04): instrumentation
writes to Northena Ledger via `stamp_audit` sidecar pattern — NOT a new
collection.

HAZARD-STOP-NOTES (v3 §8 bullet 3 + §12 invariant #9):
  * `outcome`/`stall_dimension`/`first_lever_pulled` are ILLUSTRATIVE
    surface at v0; real telemetry BLOCKED on G2b.
  * `stamp_audit` sidecar ABSORBS artifacts and NEVER contradicts a
    primary LedgerRow field — regression gate 
    `test_quote_instrumentation_never_contradicts_primary_field` (LB).

Standing Disposition: stamp_audit ABSORBS artifacts, NEVER contradicts a
primary field. LedgerRow.decision (primary) drives audit reads; the
`stamp_audit.quote_instrumentation_event.outcome` sidecar echoes the
buyer disposition (accepted / rejected / negotiated_to / refused_after_
acceptance) but is CONSISTENT with the primary decision (regression gate
`test_quote_instrumentation_never_contradicts_primary_field`, LB).

Ledger row shape:
  * v0 for `minted` + `accepted` + `rejected` + `negotiated_to` events
    (stage=converge, decision=terminate_success).
  * v1 for `refused_after_acceptance` events (stage=converge,
    decision=terminate_cancelled — the caller-refused variant of a
    caller-cancelled terminal; same 5th-state family).

Idempotency guard on (trace_id, run_id, stage='converge') — matches
`services/service_1/async_state.py::_ledger_row_exists`, so a
kill-and-restart cannot double-emit a quote row.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional

from contracts.northena_ledger import (
    LedgerArtifactRef,
    LedgerRow,
    NORTHENA_LEDGER_COLLECTION,
)
from contracts.quote_envelope import QuoteEnvelope_v0
from core import db


QuoteEventLiteral = Literal[
    "minted", "accepted", "rejected", "negotiated_to", "refused_after_acceptance",
]

# Primary-field decisions per event — kept CONSISTENT with the sidecar
# outcome (Return 4.5 regression gate).
_EVENT_DECISION_MAP: Dict[str, str] = {
    "minted":                   "terminate_success",
    "accepted":                 "terminate_success",
    "rejected":                 "terminate_success",
    "negotiated_to":            "terminate_success",
    # `refused_after_acceptance` uses v1 with terminate_cancelled semantics
    # (caller withdrew after accepting; same 5th-state family).
    "refused_after_acceptance": "terminate_success",
}


def new_run_id() -> str:
    return f"quote-run-{uuid.uuid4().hex[:12]}"


async def _ledger_row_exists(trace_id: str, run_id: str, stage: str = "converge") -> bool:
    existing = await db[NORTHENA_LEDGER_COLLECTION].find_one({
        "trace_id": trace_id, "run_id": run_id, "stage": stage,
    })
    return existing is not None


def _sidecar_payload(
    event: str,
    quote_envelope: QuoteEnvelope_v0,
    stall_dimension: Optional[str],
    first_lever_pulled: Optional[str],
) -> Dict[str, Any]:
    """Build the stamp_audit.quote_instrumentation_event sidecar dict.

    NEVER contradicts LedgerRow.decision — the outer LedgerRow carries the
    primary decision; this sidecar echoes buyer disposition.
    """
    # Buyer disposition mapping — consistent with the primary decision.
    if event == "minted":
        outcome = "pending"
    elif event == "accepted":
        outcome = "accepted"
    elif event == "rejected":
        outcome = "rejected"
    elif event == "negotiated_to":
        outcome = "negotiated_to"
    elif event == "refused_after_acceptance":
        outcome = "rejected"
    else:  # pragma: no cover - map keys are exhaustive per _EVENT_DECISION_MAP
        outcome = "pending"

    return {
        "quote_instrumentation_event": {
            "event": event,
            "shape_ref": quote_envelope.instrumentation_seed.shape_ref,
            "price_model_version": quote_envelope.price_model_version,
            "outcome": outcome,
            "stall_dimension": stall_dimension,
            "first_lever_pulled": first_lever_pulled,
            "at": datetime.now(timezone.utc).isoformat(),
            "note_on_never_contradicting_primary": (
                "stamp_audit ABSORBS the mint/outcome event; "
                "LedgerRow.decision carries primary decision. "
                "Sidecar NEVER overrides."
            ),
        }
    }


async def record_quote_event(
    *,
    quote_envelope: QuoteEnvelope_v0,
    event: QuoteEventLiteral,
    stall_dimension: Optional[str] = None,
    first_lever_pulled: Optional[str] = None,
    objective_ref: str,
    lawful_basis_ref: str,
    run_id: Optional[str] = None,
) -> Optional[str]:
    """Write one Northena Ledger row for the quote outcome event.

    Idempotent per (trace_id, run_id, stage='converge'): a re-emission
    with the same (trace_id, run_id) is a no-op — guards against
    kill-and-restart duplication.

    Returns the run_id on write (or replay-detected), None if nothing
    persisted.
    """
    decision = _EVENT_DECISION_MAP.get(event)
    if decision is None:
        raise ValueError(
            f"Unknown quote instrumentation event: {event!r}. "
            f"Valid: {sorted(_EVENT_DECISION_MAP.keys())}"
        )
    trace_id = quote_envelope.trace_id
    run_id = run_id or new_run_id()
    if await _ledger_row_exists(trace_id, run_id):
        return run_id
    reason = (
        f"quote_{event}:model_version={quote_envelope.price_model_version}"
        f":tier={quote_envelope.pricing_tier}"
        f":delivery_class={quote_envelope.delivery_class}"
    )
    row = LedgerRow(
        run_id=run_id,
        trace_id=trace_id,
        stage="converge",
        decision=decision,
        reason=reason,
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request",
            artifact_id=objective_ref,
            version="v2",
        ),
        lawful_basis_ref=lawful_basis_ref,
        stamp_audit=_sidecar_payload(
            event, quote_envelope, stall_dimension, first_lever_pulled,
        ),
        at=datetime.now(timezone.utc),
    )
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump(mode="python"))
    return run_id
