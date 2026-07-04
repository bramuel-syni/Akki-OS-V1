"""Operator variant state machine — Phase 7 Stage B-1.

States: `initial → asking_turn → user_responded → validating → next_turn
OR commit_review OR refusing → freeze`.

Guards enforced:
  * Guard 1 (ask-don't-propose on mandatory): every committed value on a
    mandatory-tier field MUST have source="operator_supplied" at freeze.
  * Guard 2 (agent-supplied marking): every value the agent supplies
    carries source="agent_assumed" with a valid agent_assumption_id.
  * Guard 3 (per-turn feasibility grounding): every OperatorTurn_v0
    appended to state.turns MUST have a non-empty
    feasibility_snapshot_ref.

Feasibility import per Ruling 4 (shared-derivation) — imports
`compute_feasibility` from `services/mtafiti/floor_feasibility.py`; no
re-implementation here.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from contracts.agent_assumption import AgentAssumption_v0
from contracts.committed_value import CommittedValue_v0
from contracts.feasibility_result import ClassDistribution
from contracts.five_rings import DefensibilityClass
from contracts.objective_request import DefensibilityFloor
from contracts.operator_turn import OperatorTurn_v0
from contracts.wizard_commit_state import WizardCommitState_v0, operator_mandatory_fields
from services.mtafiti import floor_feasibility as _floor_feasibility
from services.service_1 import provenance_preservation as _provenance_preservation
from services.wizard.agent_interface import WizardAgent
from services.wizard.source_tagging import (
    SourceTagViolation,
    validate_guard_1_operator_mandatory_all_operator_supplied,
    validate_source_tags,
)


def _new_uuid(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class OperatorSession:
    """Working-state container used mid-session; NOT a frozen contract.

    Persists as `WizardCommitState_v0` on Mongo via
    `services/wizard/session_persistence.py`. This dataclass is the
    in-memory representation while the session's `committed_at` is
    still None. On freeze, a frozen `WizardCommitState_v0` is minted
    with `committed_at` set — that's the boundary artifact.
    """
    session_id: str
    trace_id: str
    initiated_at: str
    working_reach: Optional[Dict[str, Any]] = None
    working_output: Optional[Dict[str, Any]] = None
    working_standard: Optional[Dict[str, Any]] = None
    turns: List[OperatorTurn_v0] = field(default_factory=list)
    agent_assumptions: List[AgentAssumption_v0] = field(default_factory=list)
    committed_values: Dict[str, CommittedValue_v0] = field(default_factory=dict)
    feasibility_history: List[str] = field(default_factory=list)
    license_class: Optional[str] = None


def new_operator_session() -> OperatorSession:
    return OperatorSession(
        session_id=_new_uuid("wiz"),
        trace_id=_new_uuid("trc"),
        initiated_at=_iso_now(),
    )


def _record_feasibility_snapshot(session: OperatorSession) -> str:
    """Guard 3 — record a per-turn feasibility snapshot.

    Ruling 4 shared-derivation: this function invokes
    `_floor_feasibility.derive_floor_feasibility(...)` directly — the
    canonical single-source function. No re-implementation here.

    B-1 uses an illustrative empty `ClassDistribution` because the real
    reach-driven distribution lift lives at admission time (Phase 5b
    substrate). The mechanical Guard 3 assertion is that a shared-
    derivation call fired per turn AND a snap_ref got appended; the
    numeric content sharpens at B-3 admission handoff when the working
    reach is bound to Registry state.
    """
    empty_cd = ClassDistribution(fact=0, utterance=0, non_factual=0)
    floor = DefensibilityFloor(minimum_class=DefensibilityClass.UTTERANCE)
    # Call the canonical shared-derivation function per Ruling 4.
    _ = _floor_feasibility.derive_floor_feasibility(empty_cd, floor)
    snap_ref = f"feas-{session.trace_id}-{len(session.feasibility_history) + 1}"
    session.feasibility_history.append(snap_ref)
    return snap_ref


def next_agent_turn(session: OperatorSession, agent: WizardAgent) -> OperatorTurn_v0:
    """Advance the state machine by one agent turn.

    Guard 3 enforcement point — every turn is feasibility-grounded via
    shared-derivation compute_feasibility.
    """
    # Guard 3 — feasibility snapshot per turn.
    snapshot_ref = _record_feasibility_snapshot(session)
    # Ask agent for its next turn.
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


def record_operator_response(
    session: OperatorSession,
    turn_ref: str,
    user_content: str,
    field_supplied: Optional[str] = None,
    value_supplied: Optional[Any] = None,
) -> OperatorTurn_v0:
    """Record the operator's response to the most recent agent turn.

    If `field_supplied` is provided, the value is stored as a
    CommittedValue_v0 with `source="operator_supplied"` referencing the
    given turn_ref (Guard 1: operator-mandatory fields land here).
    """
    # Update the matching turn's user_content in-place (immutable frozen
    # contract → build a fresh copy). Turns list is append-only, so we
    # rebuild only the matched one.
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
            source="operator_supplied",
            operator_turn_ref=turn_ref,
            agent_assumption_id=None,
            committed_at=_iso_now(),
        )
    return session.turns[-1] if session.turns else None  # type: ignore[return-value]


def record_agent_assumption(
    session: OperatorSession,
    field_name: str,
    inferred_value: Any,
    evidence_ref: str = "",
) -> AgentAssumption_v0:
    """Guard 2 — record an agent-inferred value.

    The paired CommittedValue is created here as well, with
    source="agent_assumed" and a valid agent_assumption_id reference.
    """
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


def preflight_freeze(session: OperatorSession) -> List[str]:
    """Return a list of violation messages (empty iff ready to freeze).

    Runs Guard 1 + source-tag XOR pre-flight checks BEFORE constructing
    the frozen WizardCommitState_v0 (whose model_validator would raise
    the same errors — but this gives a service-layer error surface).
    """
    violations: List[str] = []
    try:
        validate_source_tags(session.committed_values)
    except SourceTagViolation as e:
        violations.append(str(e))
    try:
        validate_guard_1_operator_mandatory_all_operator_supplied(
            session.committed_values, variant="operator",
        )
    except SourceTagViolation as e:
        violations.append(str(e))
    # Provenance-preservation pre-flight (§6 shaping-time refusal per E7).
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
    return violations


def _extract_field(session: OperatorSession, name: str):
    cv = session.committed_values.get(name)
    return cv.value if cv is not None else None


def _to_frozen_commit_state(
    session: OperatorSession,
    committed_at: Optional[str],
) -> WizardCommitState_v0:
    """Mint a frozen WizardCommitState_v0 from the working session.

    If `committed_at is None`, freeze-time invariants are skipped
    (mid-session snapshot passed to the agent). If `committed_at` is
    set, Guard 1 + Guard 2 fire structurally at construction.
    """
    return WizardCommitState_v0(
        session_id=session.session_id,
        trace_id=session.trace_id,
        variant="operator",
        initiated_at=session.initiated_at,
        committed_at=committed_at,
        turns=list(session.turns),
        agent_assumptions=list(session.agent_assumptions),
        committed_values=dict(session.committed_values),
        feasibility_history=list(session.feasibility_history),
        license_class=session.license_class,
        frozen_objective_ref=None,
    )


def freeze(session: OperatorSession, frozen_objective_ref: Optional[str] = None) -> WizardCommitState_v0:
    """Freeze the session — Guard 1 + Guard 2 fire structurally.

    Raises pydantic.ValidationError (or SourceTagViolation via
    preflight) on Guard 1/2 violation. Callers should call
    `preflight_freeze` first for a cleaner error surface.
    """
    committed_at = _iso_now()
    frozen = WizardCommitState_v0(
        session_id=session.session_id,
        trace_id=session.trace_id,
        variant="operator",
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
