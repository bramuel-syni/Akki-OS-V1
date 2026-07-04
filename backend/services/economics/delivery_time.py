"""Delivery-time computation — Phase 6 Stage B (v3 §8 bullet 4).

Owner ruling Axis 4 (Phase 6 Stage A close, 2026-07-04) — TWO bands
ONLY: `warm_qualified` + `fresh_extraction`. NO sub-banding until
G2b measured data defines cut points. Verbatim:
  *"Sub-banding by measured duration arrives post-G2b as a registry
    bump when measured data defines the cut points."*

HAZARD-STOP-NOTES (v3 §8 bullet 4 + §12 invariant #9):
  * Fresh-extraction delivery-time ships MECHANISM only.
  * Real queue-depth × throughput × Layer costs BLOCKED on G2b.
  * Buyer surface NEVER sees GPU numbers per §8 bullet 4.

The `delivery_class` Literal at `QuoteEnvelope_v0.delivery_class` has
EXACTLY TWO values (`warm_qualified`, `fresh_extraction`) — enforced by
the contract snapshot AND by
`test_delivery_time_has_exactly_two_bands`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Literal, Optional, Tuple


# The two-band vocabulary — MUST match QuoteEnvelope_v0.delivery_class
# Literal exactly. Any additional band is a HAZARD-STOP (Ruling 5
# scheduled hazard: Literals you-know-will-widen).
DELIVERY_CLASSES: Tuple[str, ...] = ("warm_qualified", "fresh_extraction")

DeliveryClass = Literal["warm_qualified", "fresh_extraction"]


@dataclass(frozen=True)
class FleetStateSnapshot:
    """Runtime data class (NOT a frozen contract) — snapshot of live
    fleet substrate at quote-mint time.

    Never surfaces to the buyer — used internally by
    `compute_delivery_estimate`. Buyer surface NEVER sees GPU numbers
    per §8 bullet 4.
    """
    queue_depth: int
    apportionment: Dict[str, float]
    active_workers: int
    estimated_throughput_units_per_hour: Optional[float] = None  # G2b


def classify_delivery(warm_vs_fresh: str) -> DeliveryClass:
    """Map Phase 5's warm/fresh fork to the §8 bullet 4 delivery class.

    Two-band exhaustive: `warm` → `warm_qualified`; anything else → `fresh_extraction`.
    """
    if warm_vs_fresh == "warm":
        return "warm_qualified"
    return "fresh_extraction"


def compute_delivery_estimate(
    warm_vs_fresh: str,
    config: Dict,
    fleet_state: Optional[FleetStateSnapshot] = None,
) -> Tuple[str, DeliveryClass]:
    """Return `(delivery_estimate_str, delivery_class)`.

    Rules per §8 bullet 4:
      * `warm_qualified` (warm) → "instant-to-seconds" default from config.
      * `fresh_extraction` (fresh) → queued default from config.

    HAZARD-STOP: real math (queue-depth × throughput × Layer costs) is
    BLOCKED on G2b. Until then, delivery estimate returns the config's
    illustrative default per delivery_class — never a GPU-derived number.

    `fleet_state` is accepted so callers can pass it forward for future
    G2b-post logic; this function does NOT use it yet (illustrative
    defaults only). Buyer-surface grep-negative gate:
      test_delivery_time_never_reports_gpu_numbers_on_buyer_surface
    """
    delivery_class = classify_delivery(warm_vs_fresh)
    defaults = config.get("delivery_estimate_defaults", {})
    default_estimate = defaults.get(delivery_class, "PT5M")
    return default_estimate, delivery_class
