"""Admission-refusal emission service — Phase 3.

Two responsibilities:
  1. `is_valid_reason(reason: str) -> bool` — reads the versioned
     registry `admission_refusal_reasons.v0.json` (Ruling 3
     control-surface pattern) and returns whether `reason` is a valid
     registered admission-refusal reason code.
  2. `emit_form_not_offerable(...)` — builds an
     `AdmissionRefusal_v0` envelope for the FIRST firing reason
     (v3 §6.5 model form off the offerable menu).

Actor-appropriate content discipline (Condition 3, Phase 3 dispatch
ruling 2026-07-03): caller-facing strings state the caller's actionable
move — "choose a different output form" — and NEVER surface owner-side
deliberations ("await owner acceptance of the ingredient-manifest
guarantee" or similar). Enforced by grep-negative gate
`test_admission_refusal_actor_appropriate_string`.

Ruling 3 posture: this file reads the registry; adding a new reason is
a REGISTRY bump (new entry, or `v1.json` file), NEVER modification of
`contracts/admission_refusal.py` or its `.contract_snapshot.json`. The
service-layer `is_valid_reason` check is defense-in-depth against a
code path passing an unregistered reason.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.objective_request_v2 import ObjectiveRequest_v2


_REGISTRY_PATH = Path(__file__).parent / "admission_refusal_reasons.v0.json"


def _load_registry() -> Dict:
    """Read the current-bless admission-refusal reason registry.

    Master Admin bumps to `v1.json` on registry update; this function
    reads the CURRENT bless (`v0.json`). No in-place mutation.
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
