"""License-class selection — Ruling 4 shared-derivation pattern (Phase 4a).

Spec authority: RMS Product & Engineering Spec v3 §6.1.2 verbatim (line 89):
'Selection (reach + standard filter + license class) → packaging → outer-gate
export (rights check, irreversibility, cumulative-disclosure, license issue,
receipt).'

Single-source-of-truth for license-class derivation + selection filter +
per-feed_id source_standing and bucket_category (post-Fixture-Refresh
2026-07-10 · FR-E2 α: centralized single-source registry; distributed
tables in mtafiti/source_standing.py and outer_gate/transform.py DELETED).
Consumed at 4a by:
  * `services.service_1.qualified_data.package_qualified_data` — reach-side
    filter at admission-time selection.
  * `services.mtafiti.source_standing.table()` — MEA source-standing
    declaration table (v1 loader-backed).
  * `services.outer_gate.transform._generalise_feed_id` — k-anonymity
    bucket generalisation (v1 loader-backed).

Taxonomy governance: Ruling 3 config-as-versioned-not-frozen. All class
names + commissioner-mappings + per-feed_id attributes live in
`license_classes.v(N).json` (this directory). Highest-version file wins.
`v0.json` preserved byte-identical for parity attest; runtime reads v1.
No class names in Python literals (grep-negative enforced by
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


_CONFIG_DIR = Path(__file__).parent


def _resolve_highest_version_path() -> Path:
    """Return the highest-version `license_classes.v(N).json` path present.

    Convention matches models_registry.v0.json highest-version discovery
    pattern (Phase 9 Sub-stage 9.2a E1 α). File presence + numeric sort
    on the `v(N)` suffix; missing files fall back gracefully to the
    lowest-known bless.
    """
    candidates = sorted(
        _CONFIG_DIR.glob("license_classes.v*.json"),
        key=lambda p: int(p.stem.split(".v")[1]),
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(
            "no license_classes.v(N).json config present in "
            f"{_CONFIG_DIR}"
        )
    return candidates[0]


_CONFIG_PATH = _resolve_highest_version_path()


def _load_config() -> Dict:
    """Read the current-bless `license_classes.v(N).json` — Ruling 3
    versioned config. Highest-version file wins.

    Master Admin bumps to `v(N+1).json` on taxonomy update; this function
    reads the CURRENT bless (highest version present).
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


def _feed_entries() -> Dict[str, Dict[str, str]]:
    """Return the v1 `feed_entries` map — per-feed_id 3-column attributes
    (`license_class` + `source_standing` + `bucket_category`).

    Data-blind posture (governance §8): keys are neutralized aliases
    (`feed_a..feed_k`). No broadcaster names leak.
    """
    cfg = _load_config()
    return cfg.get("feed_entries", {})


def feed_id_to_license_class_map() -> Dict[str, str]:
    """Projection: {feed_id -> license_class} derived from `feed_entries`.

    Single-source; v0-format `feed_id_to_license_class` field is no
    longer read at runtime (v0.json preserved for parity only).
    """
    return {
        feed_id: entry["license_class"]
        for feed_id, entry in _feed_entries().items()
    }


def get_source_standing_name(feed_id: str) -> str:
    """Return the `source_standing` string for a `feed_id`; unknown
    feeds fall back to the config's `default_source_standing`.

    Callers: `services.mtafiti.source_standing.table()`.
    """
    cfg = _load_config()
    entries = cfg.get("feed_entries", {})
    default = cfg.get("default_source_standing", "unknown")
    entry = entries.get(feed_id)
    if entry is None:
        return default
    return entry.get("source_standing", default)


def get_bucket_category(feed_id: str) -> str:
    """Return the `bucket_category` for a `feed_id`; unknown feeds fall
    back to the config's `default_bucket_category`.

    Callers: `services.outer_gate.transform._generalise_feed_id`.
    """
    cfg = _load_config()
    entries = cfg.get("feed_entries", {})
    default = cfg.get("default_bucket_category", "unknown_broadcast_category")
    entry = entries.get(feed_id)
    if entry is None:
        return default
    return entry.get("bucket_category", default)


def known_feed_ids() -> List[str]:
    """Return the sorted list of known feed_id aliases in the current
    bless. Callers: mtafiti source_standing invariant tests.
    """
    return sorted(_feed_entries().keys())


def select_by_class(
    registry_rows: List[Dict],
    class_name: str,
) -> List[Dict]:
    """Filter registry rows to only those whose `feed_id` maps to
    the selected license class.

    Reads the projection {feed_id -> license_class} from
    `feed_id_to_license_class_map()` (derived from v1 `feed_entries`).
    Rows whose `feed_id` is not in the mapping (or maps to a different
    class) are EXCLUDED — hard filter per v3 §6.1.2 intersection
    semantics.

    Returns a new list; does not mutate input.
    """
    feed_map = feed_id_to_license_class_map()
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
