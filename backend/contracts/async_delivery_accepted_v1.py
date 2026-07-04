"""AsyncDeliveryAccepted@v1 — Phase 6 Stage B freeze (22nd frozen contract).

Owner ruling Axis 3 (Phase 6 Stage A close, 2026-07-04): Option α — v1
version file. Verbatim: *"Second application of frozen-field-changes-as-
new-versions; superset-validating, zero break."*

Continuity note (Owner, 2026-07-04): *"v0→v1 one phase apart means the
v0 quote: Optional[Any] freeze was premature on that field — freeze
timing should wait for the nested shape when it's one phase away."*
Landed at ORCHESTRATOR_CONTINUITY.md §0.1 as a continuity note, not
re-litigated.

v1 differs from v0 by EXACTLY ONE narrowing:
  * `quote: Optional[Any]` → `quote: Optional[QuoteEnvelope_v0]`.

Everything else (shape, fields, ConfigDict, docstring content) is
byte-identical to v0. Superset-validating: every valid v0 body (where
`quote` conforms to QuoteEnvelope_v0 shape) MUST parse under v1.

v0 file `contracts/async_delivery_accepted.py` UNTOUCHED — SHA-identity
preserved from Phase 5 Stage B (`fc495b76...`). Named regression gate
`test_async_delivery_accepted_v0_byte_identical_after_6b`.

Superset gate: `test_async_delivery_accepted_v1_supersets_v0`.

Standing Owner Disposition landed with this contract (second application):
  frozen-field-changes-as-new-versions (§0.1, 2026-07-04) — audit reads
  accept both versions via superset-validating.

Snapshot: `tests/invariants/async_delivery_accepted_v1.contract_snapshot.json`.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.quote_envelope import QuoteEnvelope_v0


class AsyncDeliveryAccepted_v1(BaseModel):
    """v1 — 202-accepted body with narrowed `quote` typing.

    Superset of AsyncDeliveryAccepted_v0: every v0 body validates under
    v1 where the v0 `quote: Any` field conforms to QuoteEnvelope_v0.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    objective_id: str = Field(..., min_length=1, description="uuid-like identifier.")
    status: Literal["accepted"] = Field(
        default="accepted",
        description="Terminal Literal — this envelope carries ONLY the accepted state.",
    )
    delivery_estimate: str = Field(
        ..., min_length=1,
        description="Free-form ISO-8601 duration or human string. Loose-as-frozen.",
    )
    quote: Optional[QuoteEnvelope_v0] = Field(
        default=None,
        description="NARROWED from Optional[Any] in v0 to Optional[QuoteEnvelope_v0] at v1. "
                    "Phase 6 seam closure per Option α (Owner ruling Axis 3, Phase 6 Stage A close).",
    )
    trace_id: str = Field(..., min_length=1, description="Northena/Solva trace correlator.")
    accepted_at: str = Field(..., min_length=1, description="ISO-8601 UTC.")
