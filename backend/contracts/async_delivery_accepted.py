"""AsyncDeliveryAccepted@v0 — Phase 5 Stage B freeze (20th frozen contract).

Owner ruling (Phase 5 Stage A close, 2026-07-04): FROZEN, not UNFROZEN
wire-gated. `status` is a bare string carrying lifecycle semantics every
external integrator discriminates on; late-refusal-first-class is §7's
governance innovation; freezing keeps Phase 6 nesting coherent when
`quote` arrives as a frozen `QuoteEnvelope` inside.

Spec authority: v3 §7 bullet 1: `202` with
  `{ objective_id, status: accepted, delivery_estimate, quote? }`.

Snapshot: `tests/invariants/async_delivery_accepted.contract_snapshot.json`.

Fields carry loose-as-frozen scalar types where §7 does not narrow:
  * `delivery_estimate: str` — free-form ISO-8601 duration or human string;
    narrow at Phase 6 economics landing when real numbers arrive.
  * `quote: Optional[Any]` — Phase 6 seam. When QuoteEnvelope@v0 lands,
    this field re-types as Optional[QuoteEnvelope] via superset-validating
    v1 version at Phase 6 (per Standing Owner Disposition
    frozen-field-changes-as-new-versions).
"""
from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class AsyncDeliveryAccepted_v0(BaseModel):
    """202-accepted body — issued at fresh-fork admission per v3 §7."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    objective_id: str = Field(..., min_length=1, description="uuid-like identifier.")
    status: Literal["accepted"] = Field(
        default="accepted",
        description="Terminal Literal — this envelope carries ONLY the accepted state.",
    )
    delivery_estimate: str = Field(
        ..., min_length=1,
        description="Free-form ISO-8601 duration or human string. Loose-as-frozen "
                    "per Standing Owner Disposition; narrow at Phase 6.",
    )
    quote: Optional[Any] = Field(
        default=None,
        description="Phase 6 seam. Will re-type to Optional[QuoteEnvelope] via "
                    "superset-validating v1 at Phase 6 landing.",
    )
    trace_id: str = Field(..., min_length=1, description="Northena/Solva trace correlator.")
    accepted_at: str = Field(..., min_length=1, description="ISO-8601 UTC.")
