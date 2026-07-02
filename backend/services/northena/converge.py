"""Northena Converge — Stage 3 (mandate §6).

Threshold check only. Northena owns the halt (N-INV-6). Solva may report
"cannot reason further soundly" — that becomes an input Converge acts on,
but the stop decision + record are Northena's alone.

`absorb_solva_trace` (G3): sibling of `check()` — takes a Solva trace dict
and writes a converge-stage row keyed to the trace's conclusion kind
(assertion → terminate_success; refusal → terminate_budget). Import
boundary preserved: this module takes a plain `Dict` — no Solva import.

No cousin — net-new. Session-shaped substrate does not carry a run-level
threshold check.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.northena.ledger import record as ledger_record


async def check(
    *, run_id: str, trace_id: str, artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: str, done_condition_met: bool, budget_exhausted: bool,
) -> dict:
    """Return `{decision, ledger_row, reason}`. Precedence: done_condition
    beats budget (success is truthful over budget-exhausted when both hit)."""
    if done_condition_met:
        decision, reason = "terminate_success", "done_condition_met"
    elif budget_exhausted:
        decision, reason = "terminate_budget", "budget_exhausted"
    else:
        decision, reason = "continue", "neither_threshold_met"
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id, stage="converge",
        decision=decision, reason=reason,  # type: ignore[arg-type]
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
        stamp_audit=None, at=datetime.now(timezone.utc),
    )
    await ledger_record(row)
    return {"decision": decision, "ledger_row": row, "reason": reason}


async def absorb_solva_trace(
    *,
    run_id: str,
    trace_id: str,
    trace_dict: Dict,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: str,
) -> LedgerRow:
    """G3 seam — Solva SolvaTrace lands in a converge-stage ledger row.

    Solva spec §13: "Solva → Ledger (via stamp-audit): Refusal/decision
    audit; absorbed by Northena." The seam is `LedgerRow.stamp_audit:
    Optional[Dict]` — no frozen-contract mutation. Northena still owns
    the halt (N-INV-6); this helper is the write-side of that ownership
    when Solva provides the convergence-time judgment.

    Decision derives from the trace's conclusion kind:
      * assertion → terminate_success
      * refusal   → terminate_budget (Solva refused below floor; Northena
                    records the halt as a budget-style terminate with the
                    Solva reason preserved in `stamp_audit`).
    """
    conclusion = trace_dict.get("conclusion") or {}
    kind = conclusion.get("kind")
    if kind == "assertion":
        decision = "terminate_success"
        reason = f"solva_assertion_class={conclusion.get('klass')}"
    elif kind == "refusal":
        decision = "terminate_budget"
        reason = f"solva_refusal_{conclusion.get('reason', 'unknown')}"
    else:
        raise ValueError(f"absorb_solva_trace: unrecognised conclusion.kind={kind!r}")
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id,
        stage="converge",
        decision=decision,  # type: ignore[arg-type]
        reason=reason,
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
        stamp_audit=trace_dict,
        at=datetime.now(timezone.utc),
    )
    await ledger_record(row)
    return row


async def absorb_outer_gate_receipt(
    *,
    run_id: str,
    trace_id: str,
    receipt_dict: Dict,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: str,
) -> LedgerRow:
    """G6 seam — outer-gate irreversibility receipt lands in a gate-stage row.

    Product v2.1 §22.1 records "each Gate decision and reason". V2 gates
    the outer-gate file-out (§29.1), so a successful outer-gate transform
    maps to `stage="gate", decision="fresh"` — fresh (anonymised) egress
    was produced. The full receipt lands in `stamp_audit` as a permissive
    Dict; NO NEW FIELD is added to northena_ledger_row@v0.
    """
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id,
        stage="gate",
        decision="fresh",  # type: ignore[arg-type]
        reason=(
            f"outer_gate_transform_applied:"
            f"{receipt_dict.get('transform_version', 'unknown')}"
        ),
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
        stamp_audit={"outer_gate_receipt": receipt_dict},
        at=datetime.now(timezone.utc),
    )
    await ledger_record(row)
    return row


async def absorb_v2_refusal(
    *,
    run_id: str,
    trace_id: str,
    refusal_dict: Dict,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: str,
) -> LedgerRow:
    """G6 seam — V2 refusal envelope lands in a gate-stage row.

    Product v2.1 §29.1 "V2 gates the outer-gate file-out"; §22.1 "every
    refusal" records refusals. V2 refusal maps to `stage="gate",
    decision="refused"`. Full envelope in `stamp_audit` as permissive Dict;
    NO NEW FIELD on northena_ledger_row@v0.
    """
    reason_code = refusal_dict.get("reason_code", "unknown")
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id,
        stage="gate",
        decision="refused",  # type: ignore[arg-type]
        reason=f"v2_refused:{reason_code}",
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
        stamp_audit={"v2_refusal": refusal_dict},
        at=datetime.now(timezone.utc),
    )
    await ledger_record(row)
    return row
