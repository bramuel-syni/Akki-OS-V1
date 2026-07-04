"""License-class selection — Ruling 4 shared-derivation pattern (Phase 4a).

Spec authority: RMS Product & Engineering Spec v3 §6.1.2 verbatim (line 89):
'Selection (reach + standard filter + license class) → packaging → outer-gate
export (rights check, irreversibility, cumulative-disclosure, license issue,
receipt).'

Single-source-of-truth for license-class derivation + selection filter.
Consumed at 4a by:
  * `services.service_1.qualified_data.package_qualified_data` — reach-side
    filter at admission-time selection.

Taxonomy governance: Ruling 3 config-as-versioned-not-frozen. All class
names + commissioner-mappings live in `license_classes.v0.json` (this
directory). No class names in Python literals (grep-negative enforced by
`test_license_class_config_governs_taxonomy`).

Ruling 8 (Phase 4a Stage B, 2026-07-03): class names in
`license_classes.v0.json` are illustrative — Master Admin taxonomy on
pricing-model pattern. Real names land as config swap when commercial
reality names them, zero code change.

Phase 7 seam pre-committed 2026-07-03 (Ruling 4, Phase 4a Stage B dispatch):
when the shaping wizard lands (Phase 7), the negotiated `license_class`
arrives on the objective via a versioned frozen-contract addition (form
TBD by Phase 7's dispatch — likely a `WizardCommitState_v0` or similar
sidecar). At that point, `derive_license_class_from_commissioner` becomes
the FALLBACK ARM of a single derivation function
`derive_license_class(objective)` with two arms: explicit-value-if-present
(from wizard commit state) → primary; commissioner-derived fallback →
secondary. ONE site (this module), Ruling 4 shared-derivation unchanged.
The identity-proxy-default posture is bounded by that landing.

Counter-verdict acknowledged (Owner's Ruling 4 note, 2026-07-03): Option C
is an identity-proxy default — honest only because no use-purpose field
exists yet anywhere. Phase 7's landing narrows the identity-proxy posture
by threading explicit use-purpose in front of this fallback. The current
4a implementation ships ONLY the commissioner-derived arm.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from contracts.objective_request_v2 import Envelope
from contracts.wizard_commit_state import WizardCommitState_v0


_CONFIG_PATH = Path(__file__).parent / "license_classes.v0.json"


def _load_config() -> Dict:
    """Read `license_classes.v0.json` — Ruling 3 versioned config.

    Master Admin bumps to `v1.json` on taxonomy update; this function
    reads the CURRENT bless.
    """
    return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))


def _valid_class_names() -> List[str]:
    cfg = _load_config()
    return [entry["class_name"] for entry in cfg.get("valid_classes", [])]


def is_valid_class(class_name: str) -> bool:
    """Return True iff `class_name` is a registered license class in
    the current-bless config."""
    return class_name in _valid_class_names()


def derive_license_class_from_commissioner(envelope: Envelope) -> str:
    """Ruling 4 shared-derivation — commissioner-to-class mapping.

    Reads `envelope.commissioner` and maps via config's
    `commissioner_to_default_class`. Unmapped commissioners resolve to
    the config's `default_class`.

    Phase 7 fallback-arm role: when Phase 7 lands, this function becomes
    the fallback arm of `derive_license_class(objective)`. The wizard
    commit state's explicit value takes precedence; this function fires
    only when the wizard has not committed a class.
    """
    cfg = _load_config()
    mapping: Dict[str, str] = cfg.get("commissioner_to_default_class", {})
    default_class: str = cfg.get("default_class", "")
    return mapping.get(envelope.commissioner, default_class)


def select_by_class(
    registry_rows: List[Dict],
    class_name: str,
) -> List[Dict]:
    """Filter registry rows to only those whose `feed_id` maps to
    the selected license class.

    Reads `feed_id_to_license_class` from config. Rows whose `feed_id`
    is not in the mapping (or maps to a different class) are EXCLUDED
    — hard filter per v3 §6.1.2 intersection semantics.

    Returns a new list; does not mutate input.
    """
    cfg = _load_config()
    feed_map: Dict[str, str] = cfg.get("feed_id_to_license_class", {})
    return [
        row for row in registry_rows
        if feed_map.get(row.get("feed_id", ""), None) == class_name
    ]


def commissioner_default_map() -> Dict[str, str]:
    """Test/observation helper — return the commissioner→class map as
    currently blessed. Callers must not mutate the return value.
    """
    cfg = _load_config()
    return dict(cfg.get("commissioner_to_default_class", {}))


# --------------------------------------------------------------------------
# Phase 7 Stage B-1: Option C wrap (Owner E1 ruling, 2026-07-04) — ADDITIVE.
# --------------------------------------------------------------------------
# Owner ruling E1 (Phase 7 Stage A close, 2026-07-04) verbatim:
#   *"Option C: two-arm derivation on this module. No ObjectiveRequest_v3
#    version bump. Wizard commit state carries `license_class`; the primary
#    arm reads it iff the state is FROZEN; the fallback arm (existing
#    `derive_license_class_from_commissioner`) fires otherwise."*
#
# Primary-arm entry gate (LOAD-BEARING per Owner clarification, Phase 7
# Stage B-1 dispatch): the primary arm fires iff BOTH conditions hold:
#   (1) `wizard_state is not None`, AND
#   (2) `wizard_state.committed_at is not None`  (state is FROZEN).
# A wizard_state where committed_at is None (mid-session) MUST route to
# fallback — this branch-discrimination is enforced by
# `test_license_class_at_selection_equals_license_class_in_frozen_wizard_state`.
#
# The fallback arm's body slice (defined above) MUST remain byte-identical
# at 7b-1 close — enforced by `test_derive_license_class_from_commissioner_untouched_at_7b_1`.
def derive_license_class(
    envelope: Envelope,
    wizard_state: Optional[WizardCommitState_v0] = None,
) -> str:
    """Unified license-class derivation — Option C wrap (Phase 7 Stage B-1).

    Primary arm (frozen wizard state carries an explicit class):
      * Fires iff `wizard_state is not None` AND
        `wizard_state.committed_at is not None` AND
        `wizard_state.license_class is not None`.
      * Returns `wizard_state.license_class` verbatim.

    Fallback arm (no frozen wizard state OR class absent):
      * Delegates to `derive_license_class_from_commissioner(envelope)`.
      * Body is byte-identical to the pre-B-1 implementation.

    Note the mid-session guard: a wizard_state with `committed_at is None`
    (mid-session working state) routes to the FALLBACK. Only the frozen
    committed state is read; never mid-session intermediate content. This
    prevents identity-proxy laundering via a half-shaped wizard session.
    """
    if (
        wizard_state is not None
        and wizard_state.committed_at is not None
        and wizard_state.license_class is not None
    ):
        return wizard_state.license_class
    return derive_license_class_from_commissioner(envelope)
