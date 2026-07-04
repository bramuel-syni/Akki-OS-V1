"""Wizard admission handoff — Phase 7 Stage B-3.

Single-source composer: takes a frozen `WizardCommitState_v0` (both
variants) and mints the `ObjectiveRequest_v2` payload that will be
handed off to the existing async admission surface at
`POST /api/objectives`.

Owner ruling (Phase 7 Stage B-2 close dispatch, 2026-07-04):
    *"The composed ObjectiveRequest_v2 MUST pass all §6.1/§6.2 admission
     gates cleanly OR return AdmissionRefusal_v0 @422 with existing
     refusal codes — NO new refusal codes for handoff. Idempotency:
     handoff request MUST carry the request_body_hash and
     idempotency_key per Phase 5 §7 async doctrine. Dual-delta
     acceptance recording (from B-2) MUST persist through handoff."*

Design constraints binding this module:
  * Pure function; no LLM; no I/O; no network.
  * Single-source (Owner Condition-2 flavored posture): every shared
    symbol used inside is IMPORTED from operator-proven modules — no
    reimplementation. `test_admission_handoff_does_not_reimplement_shared_symbol`
    grep-negatives enforce this.
  * No new §0.1 Standing Dispositions.
  * No new frozen contracts (parity holds at 26).
  * Dual-delta persistence: buyer-variant `proposals` list is summarised
    by `summarise_dual_deltas(...)` and lands on
    `envelope.floor_feasibility["dual_delta_summary"]` — an open-shape
    `Dict[str, Any]` field on the frozen Envelope contract per
    Substrate-Drop v2 Part 2 posture. No frozen-field extension.
  * Deterministic idempotency_key: `f"handoff-{session_id}"`. Repeat
    handoff on same frozen session hits the async admission's
    idempotency guarantee → returns same objective_id (existing Phase 5
    §7 invariant).
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

    Sourced from proposals recorded via
    `services/wizard/buyer_state_machine.py::record_proposal`, which
    itself invokes `services/wizard/dual_delta.py::evaluate_dual_delta`
    (single-source Owner E6 mechanical application from B-2). This
    helper is the ONLY consumer of the proposals structure at handoff
    time — no in-router aggregation.
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
    """Read a committed value from the frozen state; fallback to default.

    Post-Guard-1 the operator-mandatory fields are guaranteed present
    (WizardCommitState_v0._validate_freeze_time_invariants). Buyer
    variant Guard 1 is a no-op — buyer freeze may leave axes agent-set.
    Handoff tolerates absence via `default` (async admission
    validates ObjectiveRequest_v2 shape and refuses with existing
    codes if a required field is missing).
    """
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
      * Deterministic `idempotency_key = f"handoff-{session_id}"` (repeat
        handoff hits async admission idempotency → same objective_id).
      * Buyer variant only: `envelope.floor_feasibility["dual_delta_summary"]`
        carries the aggregated proposal deltas (empty dict when no
        proposals recorded).
      * No mutation of `wizard_state` — pure function.
    """
    if wizard_state.committed_at is None:
        raise ValueError(
            "compose_objective_request_from_frozen_state requires a FROZEN "
            "wizard state (committed_at must be set). Handoff on an unfrozen "
            "session is refused at the router layer with `wizard_not_frozen`."
        )

    # Reach block — v3 §3.2. Frozen wizard commits reach as a dict-shaped
    # value on the `reach` mandatory field.
    reach_value = _get_committed(wizard_state, "reach", {"scope_refs": [], "exclusions": [], "depth": "default"})
    if not isinstance(reach_value, dict):
        # Loose-as-frozen adjacency: normalise scalar reach into dict shape.
        reach_value = {"scope_refs": [str(reach_value)], "exclusions": [], "depth": "default"}
    reach_block = {
        "scope_refs": list(reach_value.get("scope_refs", []) or []),
        "exclusions": list(reach_value.get("exclusions", []) or []),
        "depth": reach_value.get("depth", "default"),
    }

    # Output block — form / consumer / grain / standard.
    output_standard = _get_committed(
        wizard_state, "output.standard",
        {"minimum_class": "utterance", "minimum_scores": {}},
    )
    if not isinstance(output_standard, dict):
        # Loose-as-frozen adjacency: bare class string → wrap.
        output_standard = {"minimum_class": str(output_standard), "minimum_scores": {}}
    output_block = {
        "form": _get_committed(wizard_state, "output.form", "composed_conclusion"),
        "consumer": _get_committed(wizard_state, "output.consumer", "person"),
        "grain": _get_committed(wizard_state, "output.grain", "synthesized_whole"),
        "standard": output_standard,
    }

    # Envelope block — v3 §3.2. Dual-delta summary lands on the open-shape
    # `floor_feasibility` dict (buyer variant only; empty dict on operator).
    floor_feasibility_raw = _get_committed(wizard_state, "envelope.floor_feasibility", {})
    if not isinstance(floor_feasibility_raw, dict):
        floor_feasibility_raw = {}
    floor_feasibility_out: Dict[str, Any] = dict(floor_feasibility_raw)
    if wizard_state.variant == "buyer":
        # Read proposals directly from the frozen wizard state's
        # feasibility_history? No — proposals live on the buyer session
        # in-memory and are consumed at commit-review time. At handoff
        # time (post-freeze), we accept the proposals as an argument via
        # `compose_objective_request_from_frozen_state_with_proposals`
        # to preserve the single-source-of-truth for proposals. The
        # base composer here leaves the summary empty; the extended
        # composer below fills it. Split kept for pure-function purity.
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
    """Variant of `compose_objective_request_from_frozen_state` that
    persists the buyer-variant `dual_delta_summary` (aggregate of
    `proposals`) into `envelope.floor_feasibility["dual_delta_summary"]`.

    The base composer leaves the summary empty (pure fn on
    WizardCommitState_v0 alone). This extended composer accepts the
    proposals list as an argument and populates the summary. Split
    kept for testability + pure-function purity.

    Operator variant: `proposals` MUST be empty (operator has no
    proposals surface); if non-empty, raises ValueError.
    """
    if wizard_state.variant == "operator" and proposals:
        raise ValueError(
            "operator variant handoff must not carry proposals (operator "
            "has no proposals surface; this is a caller bug)."
        )
    base = compose_objective_request_from_frozen_state(wizard_state)
    if wizard_state.variant != "buyer" or not proposals:
        return base
    # Reflow the envelope with the dual_delta_summary populated. The
    # ObjectiveRequest_v2 model is frozen (ConfigDict); we rebuild via
    # model_validate on the mutated payload (single point of validation).
    payload = base.model_dump(mode="python")
    payload["envelope"]["floor_feasibility"]["dual_delta_summary"] = summarise_dual_deltas(proposals)
    return ObjectiveRequest_v2.model_validate(payload)
