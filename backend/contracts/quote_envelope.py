"""QuoteEnvelope@v0 — Phase 6 Stage B freeze (21st frozen contract).

Owner ruling Axis 1 (Phase 6 Stage A close, 2026-07-04): FROZEN.
Verbatim: *"The D4b case is stronger than the mirror argument:
price_model_version is the stamp invariant #9 exists on, and pricing_tier
is the structural non-precedent marker — both are governance values
integrators and audit branch on, neither self-carried by a frozen inner.
Real-number narrowing post-G2b lands as v1 per the frozen-field rule."*

Owner ruling Axis 4 (Phase 6 Stage A close, 2026-07-04): TWO bands only.
Verbatim: *"The fresh sub-bands (short/medium/long) fabricate granularity
from zero data — G2b hasn't run; nobody knows the real distribution of
fresh-extraction times, so three invented sub-bands are illustrative
figures wearing an enum. That's Ruling 5's scheduled hazard-stop... plus
the invented-numbers prohibition in one. Buyer legibility doesn't need
bands: the estimate value carries legibility; the band is the cost-class
discriminator, and the spec names exactly two cost classes. Sub-banding
arrives post-G2b as a registry bump when measured data defines the cut
points."*

Spec authority:
  * v3 §8 bullet 2 — every quote stamps its price-model version.
  * v3 §8 bullet 3 — quote instrumentation: shape, model_version, outcome,
    stall_dimension, first_lever_pulled (inner QuoteInstrumentationSeed_v0).
  * v3 §8 bullet 4 — two cost classes: served_from_qualified (warm) vs
    requires_fresh_extraction (fresh).
  * v3 §12 invariant #9 — cost measured before price modelled; every
    quote stamps its price-model version; exploratory pricing non-precedent.
  * UI Spec v1 §5.1 — buyer-surface renders Estimated price + delivery
    estimate + feasible-and-offerable line.

Ruling 5 applied: `pricing_tier` is constrained-str + external registry
(`pricing_tiers.vN.json`), NOT `Literal`. A Literal-you-know-will-widen
is a scheduled HAZARD-STOP.

Loose-as-frozen applied: `figure`, `qualifying_volume`, `delivery_estimate`
scalars are free-form strings. Post-G2b narrowing lands as `QuoteEnvelope_v1`
per Standing Disposition frozen-field-changes-as-new-versions.

Snapshot: `tests/invariants/quote_envelope.contract_snapshot.json`.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from typing_extensions import Annotated


# Constrained-str types per Ruling 5 (external registry, no Literal).
PriceModelVersionStr = Annotated[
    str,
    StringConstraints(min_length=1, max_length=64, pattern=r"^price-model@v[0-9]+(-[a-z0-9_-]+)?$"),
]
PricingTierStr = Annotated[
    str,
    StringConstraints(min_length=1, max_length=32, pattern=r"^[a-z][a-z0-9_]{0,31}$"),
]


class QuoteInstrumentationSeed_v0(BaseModel):
    """Inner frozen shape — 5 keys per v3 §8 bullet 3.

    Instrumentation surface carried INSIDE the quote envelope so late-
    refused/rejected/negotiated-to quotes can be reconstructed from the
    wire object alone (no dead-reference risk). A separate Northena
    Ledger row records outcome/stall/first-lever events as they occur
    (Return 4 / stamp_audit sidecar per Standing Disposition
    frozen-field-changes-as-new-versions §7.3 note).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    shape_ref: str = Field(
        ..., min_length=1,
        description="Reference to shape signature — reach + output + envelope hash.",
    )
    price_model_version: PriceModelVersionStr = Field(
        ...,
        description="Belt-and-suspenders with outer envelope. Same value; both places.",
    )
    outcome: Literal["accepted", "rejected", "negotiated_to", "pending"] = Field(
        default="pending",
        description="Buyer disposition at capture-time. `pending` at mint; updates via instrumentation sidecar.",
    )
    stall_dimension: Optional[str] = Field(
        default=None,
        description="Which shape axis the negotiation stalled on. None if not stalled.",
    )
    first_lever_pulled: Optional[str] = Field(
        default=None,
        description="First axis the buyer moved. None until they move.",
    )


class QuoteEnvelope_v0(BaseModel):
    """v3 §8 quote envelope — 21st frozen contract.

    Freeze posture: FROZEN (Owner ruling Axis 1, Phase 6 Stage A close,
    2026-07-04). Buyer-surface integrators + late-refusal-first-class
    (§7) + governance-carrying strings (price_model_version, pricing_tier)
    all bind on this shape.

    Delivery_class Literal (TWO values only per Axis 4 override):
      - `warm_qualified`      → served from qualified estate; fast band.
      - `fresh_extraction`    → requires fresh extraction; queued/priced-higher.
    Sub-banding by measured duration arrives post-G2b as REGISTRY bump.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # ── Identity + provenance (governance-carrying) ──
    quote_id: str = Field(..., min_length=1, description="uuid-like — one quote, one id.")
    trace_id: str = Field(..., min_length=1, description="Northena/Solva trace correlator.")
    quoted_at: str = Field(..., min_length=1, description="ISO-8601 UTC timestamp of mint.")

    # ── Model-version stamp (§8 bullet 2 + §12 invariant #9) ──
    price_model_version: PriceModelVersionStr = Field(
        ...,
        description="Refs price-model@vN.json version. Constrained-str, NOT Literal (Ruling 5). "
                    "Pattern: `price-model@v<N>[-<tag>]`.",
    )

    # ── Pricing tier (Ruling 5 explicit: constrained-str + external registry) ──
    pricing_tier: PricingTierStr = Field(
        ...,
        description="Refs pricing_tiers.vN.json registry. Constrained-str, NOT Literal (Ruling 5). "
                    "Extension via registry-bump; unknown tiers rejected by validator at issuance.",
    )

    # ── Buyer-surface payload (UI Spec v1 §5.1) ──
    figure: str = Field(
        ..., min_length=1,
        description="Free-form price figure. Loose-as-frozen; narrow at v1 post-G2b.",
    )
    qualifying_volume: str = Field(
        ..., min_length=1,
        description="Free-form volume estimate. Loose-as-frozen.",
    )
    delivery_estimate: str = Field(
        ..., min_length=1,
        description="ISO-8601 duration or human string per §8 bullet 4. Loose-as-frozen.",
    )
    delivery_class: Literal["warm_qualified", "fresh_extraction"] = Field(
        ...,
        description="§8 bullet 4 two-cost-class discriminator. TWO bands only per Owner ruling Axis 4 "
                    "(Phase 6 Stage A close, 2026-07-04). Sub-banding post-G2b via registry bump.",
    )
    feasible_and_offerable: bool = Field(
        ...,
        description="UI Spec §5.1 'feasible-and-offerable line' — carries as bool at the wire.",
    )

    # ── Instrumentation carry-through (§8 bullet 3) ──
    instrumentation_seed: QuoteInstrumentationSeed_v0 = Field(
        ...,
        description="Inner frozen 5-key shape per §8 bullet 3.",
    )
