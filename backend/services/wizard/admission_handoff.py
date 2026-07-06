"""Wizard admission handoff — post-commercial-cut trimmed shim (2026-07-06).

Historical context (kept for BC of pre-existing invariant tests):
  * Phase 7 Stage B-3 landed the composer triad here.
  * Phase 8 Stage B-1 relocated the triad to
    `services/wizard/router_shims.py` (E3 ratified receiver).
  * Commercial cut 2026-07-06 (BCR v1.4 §12) extracted the two
    buyer-only helpers of the triad
    (`summarise_dual_deltas` +
    `compose_objective_request_from_frozen_state_with_proposals`) to
    `/app/salvage/commercial_cut_2026_07_06/backend/wizard/
    router_shims_buyer_helpers.py`.

Post-cut this shim re-exports ONLY the operator-remaining symbol
`compose_objective_request_from_frozen_state`. The BC import path
`services.wizard.admission_handoff.compose_objective_request_from_frozen_state`
still works for any pre-B-1 test that hardcoded it.

Zero behavioural change: pure re-export.
"""
from __future__ import annotations

from services.wizard.router_shims import (  # noqa: F401
    compose_objective_request_from_frozen_state,
)
