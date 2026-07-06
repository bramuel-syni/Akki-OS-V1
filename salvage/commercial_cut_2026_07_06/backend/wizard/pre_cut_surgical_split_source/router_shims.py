"""Phase 8 Stage B-1 — wizard router shim triad (Owner E3 ratified).

Owner ruling verbatim (Phase 8 Stage B-1 dispatch, E3):
    "Land services/wizard/router_shims.py at B-1. It's the §0.2 debt with
     this slot as named receiver; deferring reschedules it into exactly
     the period (B-2/B-3 router evolution) where duplication drifts.
     Grep-negative gate parametrised over the triad symbols."

Canonical hosting module for the three envelope-shim helpers that both
`routers/wizard_operator.py` and `routers/wizard_buyer.py` invoke at
`POST /api/wizard/{variant}/{sid}/handoff`. Prior to B-1 these lived
inside `services/wizard/admission_handoff.py`; at B-1 they relocate
here and `admission_handoff.py` becomes a thin re-export shim (BC for
existing invariant tests + Owner Condition-2 grep-negative anchors).

Zero behavioural change: the functions are byte-identical to their
B-3 landing (Owner E3 dispatch: "zero behavioural change").

Grep-negative gate: neither router locally defines these symbols
(guarded by `test_phase_8_b_1_router_shims_grep_negative`).
"""
from __future__ import annotations

from typing import Any, Dict, List

from contracts.objective_request_v2 import ObjectiveRequest_v2
from contracts.wizard_commit_state import WizardCommitState_v0


def summarise_dual_deltas(proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate dual-delta payloads from a buyer session's proposals.

    Returns a `{proposal_id: {axes_changed, price_delta, class_delta,
    proposed_at}}` mapping. Empty when `proposals` is empty (operator
    variant OR buyer variant with no proposals).
    """
    summary: Dict[str, Any] = {}
    for proposal in proposals:
        pid = proposal.get("proposal_id")
        if not pid:
            continue
        summary[pid] = {
            "axes_changed": sorted(proposal.get("axes_changed", []) or []),
            "price_delta": proposal.get("price_delta"),
            "class_delta": proposal.get("class_delta"),
            "proposed_at": proposal.get("proposed_at"),
        }
    return summary


def _get_committed(wizard_state: WizardCommitState_v0, field_name: str, default: Any) -> Any:
    """Read a committed value from the frozen state; fallback to default."""
    cv = wizard_state.committed_values.get(field_name)
    if cv is None:
        return default
    return cv.value


def compose_objective_request_from_frozen_state(
    wizard_state: WizardCommitState_v0,
) -> ObjectiveRequest_v2:
    """Mint an `ObjectiveRequest_v2` from a frozen wizard state.

    Preconditions:
      * `wizard_state.committed_at is not None` (state is frozen).
      * `wizard_state.variant in ("operator", "buyer")`.

    Postconditions:
      * Returned envelope carries `commissioner = f"wizard-{variant}-{session_id}"`.
      * Deterministic `idempotency_key = f"handoff-{session_id}"`.
      * Buyer variant only: `envelope.floor_feasibility["dual_delta_summary"]`
        is initialised (empty dict; the extended composer fills it).
      * No mutation of `wizard_state` — pure function.
    """
    if wizard_state.committed_at is None:
        raise ValueError(
            "compose_objective_request_from_frozen_state requires a FROZEN "
            "wizard state (committed_at must be set). Handoff on an unfrozen "
            "session is refused at the router layer with `wizard_not_frozen`."
        )

    reach_value = _get_committed(
        wizard_state, "reach", {"scope_refs": [], "exclusions": [], "depth": "default"}
    )
    if not isinstance(reach_value, dict):
        reach_value = {"scope_refs": [str(reach_value)], "exclusions": [], "depth": "default"}
    reach_block = {
        "scope_refs": list(reach_value.get("scope_refs", []) or []),
        "exclusions": list(reach_value.get("exclusions", []) or []),
        "depth": reach_value.get("depth", "default"),
    }

    output_standard = _get_committed(
        wizard_state, "output.standard",
        {"minimum_class": "utterance", "minimum_scores": {}},
    )
    if not isinstance(output_standard, dict):
        output_standard = {"minimum_class": str(output_standard), "minimum_scores": {}}
    output_block = {
        "form": _get_committed(wizard_state, "output.form", "composed_conclusion"),
        "consumer": _get_committed(wizard_state, "output.consumer", "person"),
        "grain": _get_committed(wizard_state, "output.grain", "synthesized_whole"),
        "standard": output_standard,
    }

    floor_feasibility_raw = _get_committed(wizard_state, "envelope.floor_feasibility", {})
    if not isinstance(floor_feasibility_raw, dict):
        floor_feasibility_raw = {}
    floor_feasibility_out: Dict[str, Any] = dict(floor_feasibility_raw)
    if wizard_state.variant == "buyer":
        floor_feasibility_out.setdefault("dual_delta_summary", {})

    availability_snapshot = _get_committed(wizard_state, "envelope.availability_snapshot", {})
    if not isinstance(availability_snapshot, dict):
        availability_snapshot = {}

    envelope_block = {
        "lawful_basis": _get_committed(wizard_state, "envelope.lawful_basis", "legitimate_interest"),
        "done_condition": _get_committed(wizard_state, "envelope.done_condition", "standing_floor"),
        "budget": _get_committed(wizard_state, "envelope.budget", "default"),
        "scope_ceiling": _get_committed(wizard_state, "envelope.scope_ceiling", "estate"),
        "availability_snapshot": availability_snapshot,
        "floor_feasibility": floor_feasibility_out,
        "commissioner": f"wizard-{wizard_state.variant}-{wizard_state.session_id}",
        "committed_at": wizard_state.committed_at,
    }

    payload = {
        "entry": "external_request",
        "reach": reach_block,
        "output": output_block,
        "envelope": envelope_block,
        "shaping": None,
        "commercial": None,
        "idempotency_key": f"handoff-{wizard_state.session_id}",
    }
    return ObjectiveRequest_v2.model_validate(payload)


def compose_objective_request_from_frozen_state_with_proposals(
    wizard_state: WizardCommitState_v0,
    proposals: List[Dict[str, Any]],
) -> ObjectiveRequest_v2:
    """Variant that persists `dual_delta_summary` (buyer proposals).

    Operator variant with non-empty proposals raises ValueError (caller
    bug: operator has no proposals surface).
    """
    if wizard_state.variant == "operator" and proposals:
        raise ValueError(
            "operator variant handoff must not carry proposals (operator "
            "has no proposals surface; this is a caller bug)."
        )
    base = compose_objective_request_from_frozen_state(wizard_state)
    if wizard_state.variant != "buyer" or not proposals:
        return base
    payload = base.model_dump(mode="python")
    payload["envelope"]["floor_feasibility"]["dual_delta_summary"] = summarise_dual_deltas(proposals)
    return ObjectiveRequest_v2.model_validate(payload)
