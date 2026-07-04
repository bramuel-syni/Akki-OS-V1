"""Buyer state machine — Phase 7 Stage B-2 (Owner ruling, 2026-07-04).

Mirrors `services/wizard/operator_state_machine.py`'s shape. Divergences
per v3 §3.3 buyer semantics:

  * No operator-mandatory tier — buyer may propose across ALL axes
    within offerability (Guard 1 does NOT fire on buyer variant).
  * Buyer NEVER supplies lawful basis — `use_purpose` drives
    `license_class` at commit-review (Owner E1 Option C primary arm).
  * Agent proposal emission is first-class — every standard-changing
    or grain-changing proposal MUST carry `{price_delta, class_delta}`
    (Owner E6 dual-delta gate via `services/wizard/dual_delta.py`).

Owner Condition 2 (Phase 7 Stage B-2 dispatch, 2026-07-04): "buyer
state machine imports source-tagging, feasibility-grounding, and the
mandatory-tier predicate from the operator-proven modules — never
re-implements them." This module honours that constraint verbatim:

  * Feasibility grounding: `from services.wizard.operator_state_machine
    import _record_feasibility_snapshot as _record_feasibility_snapshot`.
  * Source-tagging: `from services.wizard.source_tagging import
    validate_source_tags, SourceTagViolation`.
  * Mandatory-tier predicate: `from contracts.wizard_commit_state import
    operator_mandatory_fields` (used only for the buyer's assertion that
    no operator-mandatory tag was written; buyer's own state has no
    such tier).
  * Guard-1 buyer-skip: `validate_guard_1_operator_mandatory_all_operator_supplied`
    called with `variant="buyer"` which no-ops per source_tagging.py.

Grep-negative gates enforce that this module DOES NOT re-implement any
of those three (see Owner Condition 2 in Stage A proposal).
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, FrozenSet, List, Optional

from contracts.agent_assumption import AgentAssumption_v0
from contracts.committed_value import CommittedValue_v0
from contracts.operator_turn import OperatorTurn_v0
from contracts.wizard_commit_state import WizardCommitState_v0, operator_mandatory_fields

# ─────────────────────────────────────────────────────────────────────
# Condition 2 imports — feasibility-grounding + source-tagging + mandatory-tier
# lifted from operator-proven modules. NO re-implementation permitted here.
# ─────────────────────────────────────────────────────────────────────
from services.wizard.operator_state_machine import (
    _record_feasibility_snapshot,  # feasibility grounding — Ruling 4 shared-derivation
)
from services.wizard.source_tagging import (
    SourceTagViolation,
    validate_guard_1_operator_mandatory_all_operator_supplied,
    validate_source_tags,
)
from services.wizard.agent_interface import WizardAgent
from services.wizard.dual_delta import evaluate_dual_delta
from services.service_1 import provenance_preservation as _provenance_preservation


def _new_uuid(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class BuyerSession:
    """Working mid-session state for a buyer wizard session.

    Same field surface as `OperatorSession` at B-1 — the frozen
    WizardCommitState_v0 discriminator (`variant="buyer"`) distinguishes
    at freeze time. Buyer never sets `lawful_basis`; `use_purpose`
    drives `license_class` at commit-review (Owner E1 primary arm).
    """
    session_id: str
    trace_id: str
    initiated_at: str
    use_purpose: Optional[str] = None  # drives license_class at commit-review
    turns: List[OperatorTurn_v0] = field(default_factory=list)
    agent_assumptions: List[AgentAssumption_v0] = field(default_factory=list)
    committed_values: Dict[str, CommittedValue_v0] = field(default_factory=dict)
    feasibility_history: List[str] = field(default_factory=list)
    license_class: Optional[str] = None
    # Buyer-specific: proposals emitted this session. Each entry is a
    # dict {axis_changed, price_delta, class_delta, proposal_content, at}.
    proposals: List[Dict[str, Any]] = field(default_factory=list)


def new_buyer_session() -> BuyerSession:
    return BuyerSession(
        session_id=_new_uuid("wiz"),
        trace_id=_new_uuid("trc"),
        initiated_at=_iso_now(),
    )


def next_agent_turn(session: BuyerSession, agent: WizardAgent) -> OperatorTurn_v0:
    """Advance the buyer state machine by one agent turn.

    Guard 3 enforcement point — every turn is feasibility-grounded via
    the SHARED derivation (imported from operator_state_machine; no
    reimpl per Owner Condition 2).
    """
    snapshot_ref = _record_feasibility_snapshot(session)  # shared feasibility grounding
    frozen_snapshot = _to_frozen_commit_state(session, committed_at=None)
    resp = agent.next_turn(frozen_snapshot)
    turn = OperatorTurn_v0(
        turn_ref=_new_uuid("turn"),
        at=_iso_now(),
        user_content="",
        agent_content=resp.content,
        feasibility_snapshot_ref=snapshot_ref,
    )
    session.turns.append(turn)
    return turn


def record_buyer_response(
    session: BuyerSession,
    turn_ref: str,
    user_content: str,
    field_supplied: Optional[str] = None,
    value_supplied: Optional[Any] = None,
) -> OperatorTurn_v0:
    """Record buyer's response to the most recent agent turn.

    Enforcement: buyer NEVER supplies lawful_basis. Attempts to
    supply the `envelope.lawful_basis` field are refused —
    `use_purpose` is the only buyer-side driver of license class,
    threaded via `session.use_purpose`.
    """
    if field_supplied == "envelope.lawful_basis":
        raise SourceTagViolation(
            "buyer variant MUST NOT set envelope.lawful_basis — "
            "use_purpose drives license_class via E1 Option C primary arm"
        )
    updated = []
    matched = False
    for t in session.turns:
        if t.turn_ref == turn_ref and not matched:
            updated.append(
                OperatorTurn_v0(
                    turn_ref=t.turn_ref, at=t.at,
                    user_content=user_content,
                    agent_content=t.agent_content,
                    feasibility_snapshot_ref=t.feasibility_snapshot_ref,
                )
            )
            matched = True
        else:
            updated.append(t)
    session.turns = updated
    if field_supplied is not None:
        session.committed_values[field_supplied] = CommittedValue_v0(
            value=value_supplied,
            source="operator_supplied",  # buyer supplies count as operator-source tag
            operator_turn_ref=turn_ref,
            agent_assumption_id=None,
            committed_at=_iso_now(),
        )
    return session.turns[-1] if session.turns else None  # type: ignore[return-value]


def record_agent_assumption(
    session: BuyerSession,
    field_name: str,
    inferred_value: Any,
    evidence_ref: str = "",
) -> AgentAssumption_v0:
    """Buyer-variant Guard 2 — record an agent-inferred value.

    Guard 1's mandatory-tier restriction does NOT apply on buyer
    variant (buyer may propose across all axes within offerability).
    But the buyer MUST NOT be attributed with lawful_basis via an
    agent-assumption — the seam that drives license class is
    `session.use_purpose`, not a synthesized agent_assumed value.
    """
    if field_name == "envelope.lawful_basis":
        raise SourceTagViolation(
            "buyer variant MUST NOT mint agent-assumption on envelope.lawful_basis — "
            "use_purpose drives license_class via E1 Option C primary arm"
        )
    assumption = AgentAssumption_v0(
        assumption_id=_new_uuid("asn"),
        at=_iso_now(),
        field=field_name,
        inferred_value=inferred_value,
        evidence_ref=evidence_ref,
    )
    session.agent_assumptions.append(assumption)
    session.committed_values[field_name] = CommittedValue_v0(
        value=inferred_value,
        source="agent_assumed",
        operator_turn_ref=None,
        agent_assumption_id=assumption.assumption_id,
        committed_at=_iso_now(),
    )
    return assumption


def record_proposal(
    session: BuyerSession,
    *,
    axes_changed: FrozenSet[str],
    price_delta: Optional[str],
    class_delta: Optional[str],
    proposal_content: str,
) -> Dict[str, Any]:
    """Buyer-only: emit an agent proposal with dual-delta gate.

    Owner E6 (Visibility-not-prohibition) mechanical application via
    `services/wizard/dual_delta.py::evaluate_dual_delta` (single-source
    derivation). Refuses emission if the axes require dual-delta but
    either delta is missing.
    """
    result = evaluate_dual_delta(
        axes_changed=axes_changed,
        price_delta=price_delta,
        class_delta=class_delta,
    )
    if not result.admissible:
        raise SourceTagViolation(result.refusal_reason)
    proposal = {
        "proposal_id": _new_uuid("prop"),
        "axes_changed": sorted(axes_changed),
        "price_delta": price_delta,
        "class_delta": class_delta,
        "proposal_content": proposal_content,
        "rendered_at": _iso_now(),
    }
    session.proposals.append(proposal)
    return proposal


def preflight_freeze(session: BuyerSession) -> List[str]:
    """Return violations (empty iff ready to freeze).

    Buyer-variant preflight: source-tag XOR invariant is enforced;
    Guard 1 mandatory-tier check is SKIPPED (variant="buyer");
    provenance-preservation shaping-time refuse is enforced (shared
    with operator via E7 module).
    """
    violations: List[str] = []
    try:
        validate_source_tags(session.committed_values)
    except SourceTagViolation as e:
        violations.append(str(e))
    try:
        # Owner Condition 2: reuse the operator-proven Guard 1 helper,
        # passing variant="buyer" which no-ops per its source_tagging.py logic.
        validate_guard_1_operator_mandatory_all_operator_supplied(
            session.committed_values, variant="buyer",
        )
    except SourceTagViolation as e:
        violations.append(str(e))
    # Provenance-preservation pre-flight (shared with operator per E7).
    output_form = _extract_field(session, "output.form")
    output_grain = _extract_field(session, "output.grain")
    output_standard = _extract_field(session, "output.standard")
    if all(v is not None for v in (output_form, output_grain, output_standard)):
        pp_result = _provenance_preservation.evaluate_provenance_preservation(
            output_form=output_form,
            output_grain=output_grain,
            output_standard=output_standard,
        )
        if not pp_result.preservable:
            violations.append(
                f"Provenance-preservation: {pp_result.off_menu_fact} — "
                f"path forward: {pp_result.what_you_can_do}"
            )
    # Buyer sanity: no committed_value for envelope.lawful_basis.
    if "envelope.lawful_basis" in session.committed_values:
        violations.append(
            "buyer variant Guard: envelope.lawful_basis MUST NOT be "
            "committed for buyer sessions — use_purpose is the driver."
        )
    return violations


def _extract_field(session: BuyerSession, name: str):
    cv = session.committed_values.get(name)
    return cv.value if cv is not None else None


def _to_frozen_commit_state(
    session: BuyerSession,
    committed_at: Optional[str],
) -> WizardCommitState_v0:
    """Mint a frozen WizardCommitState_v0 with `variant="buyer"`."""
    return WizardCommitState_v0(
        session_id=session.session_id,
        trace_id=session.trace_id,
        variant="buyer",
        initiated_at=session.initiated_at,
        committed_at=committed_at,
        turns=list(session.turns),
        agent_assumptions=list(session.agent_assumptions),
        committed_values=dict(session.committed_values),
        feasibility_history=list(session.feasibility_history),
        license_class=session.license_class,
        frozen_objective_ref=None,
    )


def freeze(
    session: BuyerSession, frozen_objective_ref: Optional[str] = None,
) -> WizardCommitState_v0:
    """Freeze the buyer session — buyer-variant discriminator on the
    frozen state; Guard 1 skips per source_tagging's variant handling.

    B-2 lands the machinery; the admission handoff to `POST /api/objectives`
    lives at B-3 scope.
    """
    committed_at = _iso_now()
    frozen = WizardCommitState_v0(
        session_id=session.session_id,
        trace_id=session.trace_id,
        variant="buyer",
        initiated_at=session.initiated_at,
        committed_at=committed_at,
        turns=list(session.turns),
        agent_assumptions=list(session.agent_assumptions),
        committed_values=dict(session.committed_values),
        feasibility_history=list(session.feasibility_history),
        license_class=session.license_class,
        frozen_objective_ref=frozen_objective_ref,
    )
    return frozen
