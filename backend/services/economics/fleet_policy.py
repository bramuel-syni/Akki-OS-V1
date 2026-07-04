"""Fleet policy loader + governance-refusal helpers — Phase 6 Stage B.

Spec authority: v3 §8 bullet 5 — fleet allocation is config
(`fleet-policy@vN`) apportioning capacity across
mining / transforms / live_path, set at the control surface.

HAZARD-STOP-NOTES (Owner Ruling R4-SD2, Substrate-Drop v2, 2026-07-03):
  * SIMPLE APPORTIONMENT holds until concurrency bites.
  * Arbitration-under-contention DEFERRED — this module REFUSES to make
    arbitration decisions beyond apportionment ratios.
  * When concurrency threshold TBD, escalate to Owner.

HAZARD-STOP-NOTES (v3 §8 bullet 4 + §12 invariant #9):
  * Fleet policy ships MECHANISM only.
  * Real per-capacity-class throughput BLOCKED on G2b.
  * Buyer surface NEVER sees GPU numbers per §8 bullet 4.

Standing Disposition applied:
  * infra-not-refusal — a zero-reserved apportionment is a GOVERNANCE
    decision (Master Admin unwilling) and returns AdmissionRefusal_v0
    with `fleet_policy_reserved_zero_capacity` reason. This is
    distinct from queue saturation (infra unable) which returns 503.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

# Config path — Master Admin bumps to `fleet_policy.vN.json` on update;
# never in-place edit.
_CONFIG_PATH = Path(__file__).parent / "fleet_policy.v0.json"

# Canonical capacity-class vocabulary from v3 §8 bullet 5.
CAPACITY_CLASSES: Tuple[str, ...] = ("mining", "transforms", "live_path")


def load_config() -> Dict:
    """Read the current-bless fleet policy config."""
    return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))


def apportionment() -> Dict[str, float]:
    """Return the current apportionment mapping."""
    return dict(load_config()["apportionment"])


def apportionment_sums_to_one(cfg: Dict = None, *, tolerance: float = None) -> bool:
    """Verify the apportionment fractions sum to 1.0 within tolerance."""
    cfg = cfg or load_config()
    parts = cfg["apportionment"].values()
    tol = tolerance if tolerance is not None else cfg.get("apportionment_sum_tolerance", 0.001)
    return abs(sum(parts) - 1.0) <= tol


def capacity_reserved_zero(capacity_class: str, cfg: Dict = None) -> bool:
    """Return True iff Master Admin has apportioned zero capacity to the class.

    Zero-reserved is a GOVERNANCE decision — the fleet policy explicitly
    denies capacity to this modality. Callers surface this as a
    `fleet_policy_reserved_zero_capacity` refusal @422 (governance),
    NEVER a 503 (infra).
    """
    cfg = cfg or load_config()
    if capacity_class not in cfg["apportionment"]:
        raise ValueError(
            f"Unknown capacity class: {capacity_class!r}. "
            f"Valid classes: {sorted(cfg['apportionment'].keys())}"
        )
    return cfg["apportionment"][capacity_class] <= 0.0


def has_arbitration_beyond_apportionment(cfg: Dict = None) -> bool:
    """R4-SD2 discipline: config MUST NOT carry arbitration fields beyond
    the apportionment map (arbitration-under-contention is DEFERRED)."""
    cfg = cfg or load_config()
    block = cfg.get("arbitration_beyond_apportionment", {})
    # HAZARD-STOP-NOTES documentation block is allowed; any "active"
    # arbitration keys (rules, priority_orders, etc.) are NOT.
    forbidden_keys = ("rules", "priority_order", "contention_policy", "backoff")
    return any(key in block for key in forbidden_keys)


def _read_yaml_or_json_bytes() -> bytes:
    """Return canonical bytes of the current-bless config (for SHA gates)."""
    return _CONFIG_PATH.read_bytes()
