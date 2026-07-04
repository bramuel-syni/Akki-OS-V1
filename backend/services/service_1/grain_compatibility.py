"""Grain-form compatibility — Ruling 4 shared-derivation pattern.

Single source of truth for the (output.form, output.grain) compatibility
matrix per v3 §6.1.4 + §6.2.4 + §6.3.4 + §6.4.4 + §6.5. Consumed by:
  * Phase 4 dispatch (admission-time refusal for `external_request` entry).
  * Phase 7 wizard (shaping-time refusal in conversation, Phase 7 land).

The rule surface (`evaluate_grain_form`) is imported by BOTH callers.
Reimplementation of this matrix outside this module is grep-negative
enforced by `test_grain_compatibility_shared_source.py`. Mirror of
`services/mtafiti/floor_feasibility.py` structural precedent.

v3 anchors:
  * §6.1.4 (line 91): 'Grains: per_claim, aggregated. synthesized_whole
    unsupported (that is composed_conclusion).'
  * §6.2.4 (line 99): 'Grain: synthesized_whole only.'
  * §6.3.4 (line 107): 'Grains: per_claim, aggregated.'  [STAKED]
  * §6.4.4 (line 115): 'Grains: per_claim and synthesized_whole per query.'  [STAKED]
  * §6.5    (lines 119-121): 'off the offerable menu' — form itself refused
    at Phase 3 (`form_not_offerable`); grain cells present in matrix for
    exhaustiveness but UNREACHABLE from live dispatch.

Ruling 5 (Phase 4a Stage B dispatch, 2026-07-03) — MODEL cells populated
with the SAME actor-appropriate `what_you_can_do` string used by
`services/service_1/admission_refusal.py::emit_form_not_offerable`.
Unreachable cells still speak properly if they are ever reached
(defense-in-depth). Enforced by
`test_grain_compat_incompatible_cells_have_non_empty_path_forward`.

Path forward strings are ACTOR-APPROPRIATE per Condition 3 (Phase 3
disposition): no owner-side deliberation phrasing; caller-actionable
direction only. Enforced by `test_grain_compat_path_forward_actor_appropriate`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from contracts.objective_request_v2 import OutputForm, OutputGrain


@dataclass(frozen=True)
class GrainCompatResult:
    """Grain-form compatibility evaluation result.

    Returned by `evaluate_grain_form(form, grain)`. Consumers branch
    on `compatible`:
      * True  → proceed with dispatch/composition
      * False → emit refusal (Phase 4: AdmissionRefusal@v0 with
                `refusal_reason` as reason code + `path_forward` as
                action string; Phase 7: wizard renders inline
                refusal-with-path)
    """

    compatible: bool
    refusal_reason: Optional[str]     # snake_case; matches admission_refusal_reasons registry entries
    path_forward: Optional[str]       # actor-appropriate; None iff compatible=True


# Ruling 5 — MODEL cells reuse the same actor-appropriate string that
# `admission_refusal.emit_form_not_offerable` surfaces via
# `_WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE`. Defense-in-depth: MODEL grain
# cells are UNREACHABLE from live dispatch (Phase 3 refuses on form
# alone before grain-compat lookup fires), but if a future wiring bug
# ever routes through these cells, refusal fires with actor-actionable
# direction rather than an empty path. String kept literal (not
# imported) to avoid a circular dependency between the two service
# modules; discipline test asserts the two strings track.
_MODEL_CELL_PATH_FORWARD = (
    "Choose a different output form. Available forms: qualified_data, "
    "composed_conclusion, knowledge_artifact, callable_skill."
)


# The (form, grain) compatibility matrix — v3 §6.1–§6.5 anchors inline.
# Keys: (OutputForm, OutputGrain). Values: GrainCompatResult.
# Total combinations: 5 forms × 3 grains = 15 cells (exhaustive).
_MATRIX = {
    # v3 §6.1.4 — qualified_data: per_claim + aggregated only.
    (OutputForm.QUALIFIED_DATA, OutputGrain.PER_CLAIM):        GrainCompatResult(True, None, None),
    (OutputForm.QUALIFIED_DATA, OutputGrain.AGGREGATED):       GrainCompatResult(True, None, None),
    (OutputForm.QUALIFIED_DATA, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'synthesized_whole' grain is unsupported at 'qualified_data' output form. "
        "To use synthesized_whole, change output.form to 'composed_conclusion' (v3 §6.1.4, §6.2)."
    ),
    # v3 §6.2.4 — composed_conclusion: synthesized_whole only.
    (OutputForm.COMPOSED_CONCLUSION, OutputGrain.PER_CLAIM):    GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'per_claim' grain is unsupported at 'composed_conclusion' output form. "
        "To use per_claim, change output.form to 'qualified_data' (v3 §6.1.4, §6.2.4)."
    ),
    (OutputForm.COMPOSED_CONCLUSION, OutputGrain.AGGREGATED):   GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'aggregated' grain is unsupported at 'composed_conclusion' output form. "
        "To use aggregated, change output.form to 'qualified_data' (v3 §6.1.4, §6.2.4)."
    ),
    (OutputForm.COMPOSED_CONCLUSION, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(True, None, None),
    # v3 §6.3.4 [STAKED] — knowledge_artifact: per_claim + aggregated.
    (OutputForm.KNOWLEDGE_ARTIFACT, OutputGrain.PER_CLAIM):     GrainCompatResult(True, None, None),
    (OutputForm.KNOWLEDGE_ARTIFACT, OutputGrain.AGGREGATED):    GrainCompatResult(True, None, None),
    (OutputForm.KNOWLEDGE_ARTIFACT, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'synthesized_whole' grain is unsupported at 'knowledge_artifact' output form (v3 §6.3.4)."
    ),
    # v3 §6.4.4 [STAKED] — callable_skill: per_claim + synthesized_whole per query.
    (OutputForm.CALLABLE_SKILL, OutputGrain.PER_CLAIM):         GrainCompatResult(True, None, None),
    (OutputForm.CALLABLE_SKILL, OutputGrain.AGGREGATED):        GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'aggregated' grain is unsupported at 'callable_skill' output form (v3 §6.4.4)."
    ),
    (OutputForm.CALLABLE_SKILL, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(True, None, None),
    # v3 §6.5 — model form off-menu; refused UPSTREAM by
    # `emit_form_not_offerable(reason='form_not_offerable')`. These
    # cells UNREACHABLE from live dispatch (Ruling 5) but populated
    # with actor-appropriate path-forward for defense-in-depth.
    (OutputForm.MODEL, OutputGrain.PER_CLAIM):         GrainCompatResult(False, "form_not_offerable", _MODEL_CELL_PATH_FORWARD),
    (OutputForm.MODEL, OutputGrain.AGGREGATED):        GrainCompatResult(False, "form_not_offerable", _MODEL_CELL_PATH_FORWARD),
    (OutputForm.MODEL, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(False, "form_not_offerable", _MODEL_CELL_PATH_FORWARD),
}


def evaluate_grain_form(form: OutputForm, grain: OutputGrain) -> GrainCompatResult:
    """Ruling 4 shared-derivation — the ONLY grain-form evaluation site.

    Consumers:
      * `services.service_1.dispatch.dispatch()` — Phase 4a admission-time.
      * Phase 7 wizard state machine — shaping-time (Phase 7 landing).

    Both import THIS function; any local reimplementation elsewhere
    fails `test_grain_compatibility_shared_source.py`.
    """
    return _MATRIX[(form, grain)]
