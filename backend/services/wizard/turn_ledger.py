"""Wizard transcript ledger writer — Phase 7 Stage B-1 (Owner E5 ruling).

Writes wizard transcripts to Northena Ledger via stamp_audit sidecar.

Owner ruling E5 (Phase 7 Stage A close, 2026-07-04) — separately-
addressable retention class. The sidecar payload carries a
`data_class="wizard_transcript"` marker so DPO can rule one retention
window (inheritance from Ledger default) OR split at Seam 3 unlock.

Data classes carried by wizard transcripts (DPO flag):
  * buyer_identity — commissioner + use_purpose (buyer variant)
  * buyer_intent — negotiation lever pulls (buyer variant turns)
  * competitive_signals — buyer ask content that may reveal competitive intent
  * agent_inferred_content — agent_assumed values + evidence_ref
  * feasibility_snapshots — Guard 3 per-turn snapshots
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from contracts.northena_ledger import (
    LedgerArtifactRef,
    LedgerRow,
    NORTHENA_LEDGER_COLLECTION,
)
from contracts.wizard_commit_state import WizardCommitState_v0
from core import db


DATA_CLASS_WIZARD_TRANSCRIPT = "wizard_transcript"


async def _ledger_row_exists(trace_id: str, run_id: str, stage: str = "converge") -> bool:
    existing = await db[NORTHENA_LEDGER_COLLECTION].find_one({
        "trace_id": trace_id, "run_id": run_id, "stage": stage,
    })
    return existing is not None


async def record_wizard_freeze(
    state: WizardCommitState_v0,
    lawful_basis_ref: str,
) -> Optional[str]:
    """Write one ledger row on wizard freeze with the transcript sidecar.

    Idempotent per (trace_id, run_id='wizard-freeze', stage='converge')
    — a re-emission with the same session is a no-op.
    """
    run_id = f"wizard-freeze-{state.session_id}"
    if await _ledger_row_exists(state.trace_id, run_id):
        return run_id
    row = LedgerRow(
        run_id=run_id,
        trace_id=state.trace_id,
        stage="converge",
        decision="terminate_success",
        reason=f"wizard_freeze:variant={state.variant}:turns={len(state.turns)}",
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request",
            artifact_id=state.frozen_objective_ref or f"wizard-{state.session_id}",
            version="v2",
        ),
        lawful_basis_ref=lawful_basis_ref,
        stamp_audit={
            "data_class": DATA_CLASS_WIZARD_TRANSCRIPT,
            "wizard_transcript": {
                "session_id": state.session_id,
                "variant": state.variant,
                "n_turns": len(state.turns),
                "n_agent_assumptions": len(state.agent_assumptions),
                "n_committed_values": len(state.committed_values),
                "license_class": state.license_class,
                "committed_at": state.committed_at,
                "retention_class_note": (
                    "Owner E5 (Phase 7 Stage A close, 2026-07-04): wizard "
                    "transcript is a separately-addressable retention "
                    "class; at Seam 3 unlock DPO may rule one window "
                    "(inheritance) or split."
                ),
            },
        },
        at=datetime.now(timezone.utc),
    )
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump(mode="python"))
    return run_id
