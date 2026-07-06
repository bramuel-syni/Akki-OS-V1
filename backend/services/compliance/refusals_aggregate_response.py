"""RefusalsAggregateResponse Pydantic model — UNFROZEN wire shape (B-5a).

Data source: `NorthenaLedgerRow_v1` rows where `decision == "refused"`
filtered by month window. Family classification per
`services.compliance.refusal_family_classifier`.

Auth 403s + validation 422s STRUCTURALLY excluded — they do not write
to the ledger at all (exclusion is a property of the source, not a
filter). Enforcement gate:
`test_refusals_by_month_excludes_auth_403_and_validation_422`.
"""
from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class RefusalsTotals(BaseModel):
    model_config = ConfigDict(extra="forbid")

    admission_refusals: int = Field(..., ge=0)
    composition_below_floor: int = Field(..., ge=0)
    outer_gate_refusals: int = Field(..., ge=0)
    unclassified: int = Field(
        ...,
        ge=0,
        description=(
            "Rows whose reason falls outside all governed families. "
            "MUST be surfaced honestly (never silently dropped) — "
            "governance-bites honesty rule."
        ),
    )
    total: int = Field(..., ge=0)


class RefusalReasonCount(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reason: str = Field(...)
    family: Literal[
        "admission_refusals",
        "composition_below_floor",
        "outer_gate_refusals",
        "unclassified",
    ] = Field(...)
    count: int = Field(..., ge=1)


class RefusalDayCount(BaseModel):
    model_config = ConfigDict(extra="forbid")

    day: str = Field(..., description="ISO date YYYY-MM-DD.")
    count: int = Field(..., ge=1)


class RefusalsAggregateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    month: str = Field(..., description="Echo of query param, YYYY-MM.")
    totals: RefusalsTotals = Field(...)
    by_reason: List[RefusalReasonCount] = Field(
        default_factory=list,
        description=(
            "One entry per distinct refusal reason in the month; sorted "
            "by count descending then reason alphabetically for determinism."
        ),
    )
    by_day: List[RefusalDayCount] = Field(
        default_factory=list,
        description=(
            "One entry per day in the month with ≥1 refusal; sorted "
            "chronologically. Empty for zero-refusal months."
        ),
    )
