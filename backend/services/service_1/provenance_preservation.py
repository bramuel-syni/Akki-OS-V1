"""Provenance-preservation rule module — Phase 7 Stage B-1 (Owner E7 ruling).

Spec authority: v3 §6 preamble — "the transform produces the shaped
output only where the declared standard survives it."

Owner ruling E7 (Phase 7 Stage A close, 2026-07-04) verbatim:
  *"the provenance-preservation bound (§6 preamble) binds both variants —
   the operator's shaping-time refusal needs it as much as the buyer's
   offerability check. Landing it in B-2 ships an operator machine that
   can freeze objectives the transform layer must later refuse —
   execution-time discovery, the exact thing §6 forbids."*

Design: shared-derivation pattern mirroring `services/service_1/grain_compatibility.py`.
Both variants import from this canonical module — operator state
machine at B-1 (this stage), buyer state machine at B-2. Grep-negative
single-source gate: `test_provenance_preservation_uses_single_source_derivation`.

HAZARD-STOP-NOTES:
  * Provenance-preservation rules are ILLUSTRATIVE at v0; real rules
    lift from v3 §6 form-specific texts and land narrowed post-G2b.
  * The rule table below is DECLARATIVE — each output form declares
    the minimum standard its transform can preserve. Below-floor
    combinations refuse DURING SHAPING (never at execution) per §6.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


# Per v3 §6: each output form declares what standard its transform
# can preserve for each grain. `None` sentinel means "rule cannot
# satisfy any declared standard for this grain" (form/grain
# incompatibility).
#
# Format: {output_form: {output_grain: {"minimum_preservable_standard": str_or_None,
#                                        "notes": str}}}
#
# Standards ordered ascending: "utterance" < "assertion" < "claim" < "verifiable".
#
# HAZARD-STOP-NOTES: values ILLUSTRATIVE per §12 invariant #9 until G2b.
_PROVENANCE_RULES: Dict[str, Dict[str, Dict]] = {
    "qualified_data": {
        "per_utterance":       {"minimum_preservable_standard": "utterance",  "notes": "Direct pass-through."},
        "per_claim":           {"minimum_preservable_standard": "utterance",  "notes": "Per-claim aggregation preserves utterance-level provenance."},
        "synthesized_whole":   {"minimum_preservable_standard": "claim",      "notes": "Synthesis discards utterance-level ties; requires claim-level provenance."},
    },
    "composed_conclusion": {
        "per_utterance":       {"minimum_preservable_standard": None,         "notes": "Composed conclusion cannot preserve utterance-level provenance by construction; refuse."},
        "per_claim":           {"minimum_preservable_standard": "claim",      "notes": "Conclusion carries claim-level provenance via cited-utterance list."},
        "synthesized_whole":   {"minimum_preservable_standard": "claim",      "notes": "Synthesized conclusion preserves claim-level provenance only."},
    },
    "callable_skill":         {
        # v3 §6.3 not yet landed — all combinations refuse until §6.3 defines the rule set.
        "per_utterance":       {"minimum_preservable_standard": None, "notes": "§6.3 not landed; provenance rule TBD."},
        "per_claim":           {"minimum_preservable_standard": None, "notes": "§6.3 not landed; provenance rule TBD."},
        "synthesized_whole":   {"minimum_preservable_standard": None, "notes": "§6.3 not landed; provenance rule TBD."},
    },
    "knowledge_artifact":     {
        "per_utterance":       {"minimum_preservable_standard": None, "notes": "§6.4 not landed; provenance rule TBD."},
        "per_claim":           {"minimum_preservable_standard": None, "notes": "§6.4 not landed; provenance rule TBD."},
        "synthesized_whole":   {"minimum_preservable_standard": None, "notes": "§6.4 not landed; provenance rule TBD."},
    },
}


# Standard rank — ascending. Used for "declared standard ≤ minimum
# preservable standard" comparison.
_STANDARD_RANK: Dict[str, int] = {
    "utterance":  0,
    "assertion":  1,
    "claim":      2,
    "verifiable": 3,
}


@dataclass(frozen=True)
class PreservationResult:
    """Outcome of a provenance-preservation evaluation.

    `preservable`: True iff the form/grain rule can satisfy the
    declared standard.
    `refusal_reason`: populated on refusal; feeds AdmissionRefusal_v0.
    `off_menu_fact`: caller-facing narration.
    `what_you_can_do`: caller-facing path forward.
    """
    preservable: bool
    refusal_reason: str = ""
    off_menu_fact: str = ""
    what_you_can_do: str = ""


def evaluate_provenance_preservation(
    output_form: str,
    output_grain: str,
    output_standard: str,
) -> PreservationResult:
    """Evaluate whether the transform for the given (form, grain) can
    preserve the declared `output_standard`. Refuse DURING SHAPING
    (via the caller's admission-refusal emit) never at execution.
    """
    form_rules = _PROVENANCE_RULES.get(output_form)
    if form_rules is None:
        return PreservationResult(
            preservable=False,
            refusal_reason="provenance_preservation_impossible",
            off_menu_fact=(
                f"Output form '{output_form}' has no provenance-preservation "
                f"rule in the current-bless registry. Per v3 §6, forms without "
                f"a rule cannot be shaped."
            ),
            what_you_can_do=(
                "Choose a form for which v3 §6 defines a provenance-preservation "
                "rule (currently: qualified_data, composed_conclusion)."
            ),
        )
    grain_rule = form_rules.get(output_grain)
    if grain_rule is None:
        return PreservationResult(
            preservable=False,
            refusal_reason="provenance_preservation_impossible",
            off_menu_fact=(
                f"Grain '{output_grain}' is not supported for form '{output_form}' "
                f"per v3 §6 provenance rules."
            ),
            what_you_can_do=(
                f"Choose a grain supported for form '{output_form}': "
                f"{sorted(form_rules.keys())}."
            ),
        )
    min_preservable = grain_rule["minimum_preservable_standard"]
    if min_preservable is None:
        return PreservationResult(
            preservable=False,
            refusal_reason="provenance_preservation_impossible",
            off_menu_fact=(
                f"Form '{output_form}' at grain '{output_grain}' cannot preserve "
                f"provenance per v3 §6. {grain_rule['notes']}"
            ),
            what_you_can_do=(
                f"Choose a different grain OR form. Rule note: {grain_rule['notes']}"
            ),
        )
    declared_rank = _STANDARD_RANK.get(output_standard)
    min_preservable_rank = _STANDARD_RANK.get(min_preservable)
    if declared_rank is None or min_preservable_rank is None:
        return PreservationResult(
            preservable=False,
            refusal_reason="provenance_preservation_impossible",
            off_menu_fact=(
                f"Standard '{output_standard}' or preservable-standard "
                f"'{min_preservable}' is not in the registered rank table."
            ),
            what_you_can_do=(
                f"Choose a standard from {sorted(_STANDARD_RANK.keys())}."
            ),
        )
    if declared_rank < min_preservable_rank:
        return PreservationResult(
            preservable=False,
            refusal_reason="provenance_preservation_impossible",
            off_menu_fact=(
                f"Declared output standard '{output_standard}' is below the minimum "
                f"preservable standard '{min_preservable}' for form '{output_form}' "
                f"at grain '{output_grain}' per v3 §6. {grain_rule['notes']}"
            ),
            what_you_can_do=(
                f"Raise the declared standard to '{min_preservable}' or higher, "
                f"OR pick a form/grain combination with a lower minimum preservable "
                f"standard."
            ),
        )
    return PreservationResult(preservable=True)
