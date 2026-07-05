"""Wizard admission handoff — Phase 7 Stage B-3 landing / Phase 8 Stage B-1 re-export shim.

Owner ruling (Phase 8 Stage B-1 dispatch, E3): the triad
`compose_objective_request_from_frozen_state`,
`compose_objective_request_from_frozen_state_with_proposals`, and
`summarise_dual_deltas` relocate to `services/wizard/router_shims.py`
at B-1 (the §0.2 "envelope-shim helper triad extraction" plan-debt's
named receiver). This module preserves the historical import path
`services.wizard.admission_handoff.<symbol>` for backwards-compat of
existing invariant tests (Phase 7 B-3 test surface at
`tests/invariants/test_phase_7_stage_b_3_wizard.py`) and Owner
Condition-2 grep-negative anchors (single-source posture).

Zero behavioural change: pure re-export.

Owner ruling (Phase 7 Stage B-2 close dispatch, 2026-07-04):
    *"The composed ObjectiveRequest_v2 MUST pass all §6.1/§6.2 admission
     gates cleanly OR return AdmissionRefusal_v0 @422 with existing
     refusal codes — NO new refusal codes for handoff."*

Design constraints binding this module (preserved at B-1):
  * Pure function; no LLM; no I/O; no network.
  * Single-source (Owner Condition-2 flavored posture): every shared
    symbol used inside is IMPORTED from `router_shims` (which itself
    imports proven single-source modules).
  * No new §0.1 Standing Dispositions.
  * No new frozen contracts (parity holds at 26).
"""
from __future__ import annotations

# Re-export the triad from the B-1 canonical location. Historical
# callers (routers + invariant tests) continue to import from this
# module path; the implementation lives in router_shims.
from services.wizard.router_shims import (  # noqa: F401
    compose_objective_request_from_frozen_state,
    compose_objective_request_from_frozen_state_with_proposals,
    summarise_dual_deltas,
)
