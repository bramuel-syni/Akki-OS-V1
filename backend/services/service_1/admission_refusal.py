"""Admission-refusal emission service — Phase 3 + Phase 4a.

Responsibilities:
  1. `is_valid_reason(reason: str) -> bool` — reads the versioned
     registry `admission_refusal_reasons.v1.json` (Ruling 3
     control-surface pattern) and returns whether `reason` is a valid
     registered admission-refusal reason code.
  2. `emit_form_not_offerable(...)` — builds an
     `AdmissionRefusal_v0` envelope for the FIRST firing reason
     (v3 §6.5 model form off the offerable menu). Phase 3 landing.
  3. `emit_grain_form_incompatible(...)`, `emit_standard_below_admission_floor(...)`,
     `emit_license_class_unavailable(...)` — Phase 4a §6.1 admission-time
     refusal helpers. Ruling 7 (Phase 4a Stage B, 2026-07-03): all
     grain refusals share the unified `grain_form_incompatible` reason
     code with per-cell `path_forward` discrimination.

Actor-appropriate content discipline (Condition 3, Phase 3 dispatch
ruling 2026-07-03): caller-facing strings state the caller's actionable
move — "choose a different output form" — and NEVER surface owner-side
deliberations ("await owner acceptance of the ingredient-manifest
guarantee" or similar). Enforced by grep-negative gate
`test_admission_refusal_actor_appropriate_string`.

Ruling 3 posture: this file reads the registry; adding a new reason is
a REGISTRY bump (new entry, or `vN.json` file), NEVER modification of
`contracts/admission_refusal.py` or its `.contract_snapshot.json`. The
service-layer `is_valid_reason` check is defense-in-depth against a
code path passing an unregistered reason.

Phase 4a registry-bump landing (2026-07-03): `_REGISTRY_PATH` bumped
from `v0.json` to `v1.json`. v0.json remains byte-identical on disk
(never mutated per Ruling 3); v1.json additively adds three reason
codes (`grain_form_incompatible`, `standard_below_admission_floor`,
`license_class_unavailable`). Extension enforced by
`test_admission_refusal_registry_v1_extends_v0_additively`.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.objective_request_v2 import ObjectiveRequest_v2


_REGISTRY_PATH = Path(__file__).parent / "admission_refusal_reasons.v1.json"


def _load_registry() -> Dict:
    """Read the current-bless admission-refusal reason registry.

    Master Admin bumps to `vN.json` on registry update; this function
    reads the CURRENT bless (`v1.json` post-Phase-4a). No in-place
    mutation.
    """
    return json.loads(_REGISTRY_PATH.read_text(encoding="utf-8"))


def _valid_reasons() -> List[str]:
    reg = _load_registry()
    return [entry["reason"] for entry in reg.get("valid_reasons", [])]


def is_valid_reason(reason: str) -> bool:
    """Return True iff `reason` is a registered admission-refusal reason
    in the current-bless registry."""
    return reason in _valid_reasons()


# ---------------------------------------------------------------------------
# Caller-facing content strings — actor-appropriate per Condition 3.
#
# The following strings are GREP-INSPECTED by
# `test_admission_refusal_actor_appropriate_string`:
#   * MUST NOT contain: "await owner", "owner acceptance",
#     "ingredient manifest", "ingredient-manifest".
#   * MUST contain (in `what_you_can_do`): "output form" — robust
#     invariant word signalling actor-actionable content.
# ---------------------------------------------------------------------------

_OFF_MENU_FACT_FORM_NOT_OFFERABLE = (
    "The 'model' output form is off the offerable menu at this system's "
    "current standing. This is a deliberate, unambiguous state, not an "
    "omission."
)

_WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE = (
    "Choose a different output form. Available forms: qualified_data, "
    "composed_conclusion, knowledge_artifact, callable_skill."
)


def emit_form_not_offerable(
    request: ObjectiveRequest_v2,
    trace_id: str,
) -> AdmissionRefusal_v0:
    """Build the admission-refusal envelope for v3 §6.5 form_not_offerable.

    Fires when `request.output.form == OutputForm.MODEL` at admission
    (Phase 2 v2 dispatch — external_request entry) or when the wizard
    renders it (Phase 7 — work_order entry, not yet built).

    Defense-in-depth: `is_valid_reason("form_not_offerable")` MUST hold
    at construction — the registry governs whether this reason is
    currently live. If a future ops action removes the reason from the
    registry (unlikely — registry is append-only in practice), this
    guard surfaces the mismatch instead of silently building an invalid
    envelope.
    """
    reason = "form_not_offerable"
    if not is_valid_reason(reason):
        raise RuntimeError(
            f"admission_refusal_reasons.vN.json registry does not list "
            f"reason={reason!r} — construction blocked."
        )

    return AdmissionRefusal_v0(
        reason=reason,
        trace_id=trace_id,
        requested_output_form=request.output.form.value,
        off_menu_fact=_OFF_MENU_FACT_FORM_NOT_OFFERABLE,
        what_you_can_do=_WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Phase 4a emit helpers — three §6.1 admission-time refusal cases.
#
# Ruling 7 (Phase 4a Stage B, 2026-07-03): all grain refusals share the
# unified `grain_form_incompatible` reason code; per-cell `path_forward`
# discriminates specific fix (grain-compat matrix owns the strings).
#
# Actor-appropriate discipline preserved — every `off_menu_fact` +
# `what_you_can_do` string is caller-facing, no owner-side deliberations.
# ---------------------------------------------------------------------------


def emit_grain_form_incompatible(
    request: ObjectiveRequest_v2,
    trace_id: str,
    *,
    path_forward: str,
) -> AdmissionRefusal_v0:
    """Build an admission-refusal envelope for v3 §6.1.4/§6.2.4/§6.3.4/
    §6.4.4 (form, grain) incompatibility.

    Fires at admission-time when
    `services/service_1/grain_compatibility.py::evaluate_grain_form(
    request.output.form, request.output.grain).compatible is False`
    with a non-`form_not_offerable` `refusal_reason` (which is the
    `grain_form_incompatible` code per Ruling 7).

    `path_forward` is the actor-appropriate string from
    `GrainCompatResult.path_forward` — passed in so the grain-compat
    matrix stays the single source of truth for per-cell fix advice.

    Defense-in-depth: `is_valid_reason("grain_form_incompatible")` MUST
    hold at construction — the registry governs whether this reason is
    currently live.
    """
    reason = "grain_form_incompatible"
    if not is_valid_reason(reason):
        raise RuntimeError(
            f"admission_refusal_reasons.vN.json registry does not list "
            f"reason={reason!r} — construction blocked."
        )
    off_menu_fact = (
        f"The requested (output.form, output.grain) pair "
        f"('{request.output.form.value}', '{request.output.grain.value}') "
        f"is unsupported at this system's current standing. This is a "
        f"deliberate, unambiguous state per v3 §6.1.4/§6.2.4 grain rules, "
        f"not an omission."
    )
    return AdmissionRefusal_v0(
        reason=reason,
        trace_id=trace_id,
        requested_output_form=request.output.form.value,
        off_menu_fact=off_menu_fact,
        what_you_can_do=path_forward,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )


def emit_standard_below_admission_floor(
    request: ObjectiveRequest_v2,
    trace_id: str,
    *,
    qualifying_volume_after_filter: int,
) -> AdmissionRefusal_v0:
    """Build an admission-refusal envelope for v3 §6.1.6 standard hard
    input filter.

    Fires at admission-time when the requested `output.standard` filter
    removes ALL qualifying units from the reach's Registry rows —
    i.e. zero units survive the standard hard filter. Distinct from
    `Service1Refusal(composition_below_floor)` (§6.2 conclusion-time).

    Actor-appropriate content: names the requested standard + suggests
    two callable moves (lower standard, expand reach).
    """
    reason = "standard_below_admission_floor"
    if not is_valid_reason(reason):
        raise RuntimeError(
            f"admission_refusal_reasons.vN.json registry does not list "
            f"reason={reason!r} — construction blocked."
        )
    requested_standard = request.output.standard.minimum_class.value
    off_menu_fact = (
        f"The requested standard '{requested_standard}' is a hard input "
        f"filter per v3 §6.1.6; zero units in the reach meet or exceed "
        f"this standard. Below-floor units never enter the deliverable."
    )
    what_you_can_do = (
        f"Lower the output.standard.minimum_class below "
        f"'{requested_standard}', or expand output.form-compatible reach "
        f"to admit sources with units meeting this standard "
        f"(qualifying_volume_after_filter={qualifying_volume_after_filter})."
    )
    return AdmissionRefusal_v0(
        reason=reason,
        trace_id=trace_id,
        requested_output_form=request.output.form.value,
        off_menu_fact=off_menu_fact,
        what_you_can_do=what_you_can_do,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )


def emit_license_class_unavailable(
    request: ObjectiveRequest_v2,
    trace_id: str,
    *,
    derived_class: str,
) -> AdmissionRefusal_v0:
    """Build an admission-refusal envelope for v3 §6.1.2 license-class
    axis of the three-way selection intersection.

    Fires at admission-time when the derived (or explicitly-selected
    under future Phase-7 wizard override) license class has zero
    qualifying units in the specified reach.

    Actor-appropriate content: names the derived class + suggests two
    callable moves (change license class via commissioner change, or
    expand reach).
    """
    reason = "license_class_unavailable"
    if not is_valid_reason(reason):
        raise RuntimeError(
            f"admission_refusal_reasons.vN.json registry does not list "
            f"reason={reason!r} — construction blocked."
        )
    off_menu_fact = (
        f"The derived license class '{derived_class}' has zero qualifying "
        f"units in the specified reach at this system's current standing. "
        f"The three-way selection (reach + standard + license class) per "
        f"v3 §6.1.2 requires an INTERSECTION; the license-class axis is "
        f"empty."
    )
    what_you_can_do = (
        f"Change the envelope.commissioner value (or in a future Phase 7 "
        f"wizard flow, override the derived license class), OR expand the "
        f"reach to admit sources whose license class is "
        f"'{derived_class}'."
    )
    return AdmissionRefusal_v0(
        reason=reason,
        trace_id=trace_id,
        requested_output_form=request.output.form.value,
        off_menu_fact=off_menu_fact,
        what_you_can_do=what_you_can_do,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
