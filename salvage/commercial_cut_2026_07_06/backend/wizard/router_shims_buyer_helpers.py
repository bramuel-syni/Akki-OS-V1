"""Commercial-cut salvage — buyer wizard shim helpers (2026-07-06).

Extracted from `services/wizard/router_shims.py` at commercial cut per
BCR v1.4 §12. These helpers are BUYER-VARIANT-ONLY:

  * `summarise_dual_deltas` — aggregates buyer session proposals with
    dual-delta payloads (buyer-only surface per Phase 7 B-2 §3).
  * `compose_objective_request_from_frozen_state_with_proposals` —
    variant that persists `dual_delta_summary` from buyer proposals.
    Operator variant with non-empty proposals raises ValueError
    (operator has no proposals surface).

Preserved verbatim per BCR v1.4 §12.2 (code preservation, mandatory).

Not imported by any live consumer post-cut. Frozen contract
`QuoteEnvelope_v0` remains orphan-in-place at
`/app/backend/contracts/quote_envelope.py` byte-identical.
"""
from __future__ import annotations

from typing import Any, Dict, List

# NOTE: the following imports are for verbatim preservation of the
# extracted code. Post-cut this module is not imported anywhere in the
# extractor build tree; the imports reference the operator-remaining
# contract shape which stays byte-identical.
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


def compose_objective_request_from_frozen_state_with_proposals(
    wizard_state: WizardCommitState_v0,
    proposals: List[Dict[str, Any]],
) -> ObjectiveRequest_v2:
    """Variant that persists `dual_delta_summary` (buyer proposals).

    Operator variant with non-empty proposals raises ValueError (caller
    bug: operator has no proposals surface).

    NOTE: at salvage time the base composer
    `compose_objective_request_from_frozen_state` was retained in the
    extractor tree; if resurrecting this helper, re-import from the
    canonical location.
    """
    # Import from the operator-remaining router_shims module.
    from services.wizard.router_shims import (
        compose_objective_request_from_frozen_state,
    )
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
