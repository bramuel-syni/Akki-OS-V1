"""Refusals-coverage-marker response model — Sub-stage 1.

UNFROZEN response shape for `GET /api/compliance/refusals_coverage`.
NOT a frozen contract (lives in `services/compliance/`, not `contracts/`).

Rendered by the Compliance Console §4.1 Refusals card as the Owner-supplied
coverage-marker binding-copy (middle-dot per E7):

    "Counts {families_since_system_start} since system start · {families_since_seam_3}
     since {seam_3_earliest_date} — earlier events in those families were
     not recorded."

`{families_since_system_start}` and `{families_since_seam_3}` are family-name
lists composed dynamically per E3.β; `{seam_3_earliest_date}` is the
earliest-among-seam-3 ISO date across families (may differ per family; the
per-family since-date lives inside `per_family_since_date`).
"""
from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class RefusalsCoverageResponse(BaseModel):
    """Coverage-marker response for the Compliance Console §4.1 Refusals card.

    E3.β canonical mechanism (Amendment E, Owner refinement 2026-07-06):
    per-family `since_date` is the ISO-8601 date (`YYYY-MM-DD` UTC) of the
    earliest `NorthenaLedgerRow_v1` whose `stamp_audit["refusal_family"]`
    matches that family. Server-computed at query time; NEVER sourced from
    a config file.
    """

    model_config = ConfigDict(extra="forbid")

    families_since_system_start: List[str] = Field(
        default_factory=list,
        description=(
            "Families with an earliest pinned-key row at or before the "
            "seam-3 wire-up UTC date boundary. Practically empty at Sub-stage 1 "
            "close: pre-wire-up refusal rows do not carry the pinned "
            "stamp_audit['refusal_family'] key and drop out of the "
            "query filter. Populated over time as any historical rows that "
            "carried the key predate the boundary (none expected at Sub-stage 1)."
        ),
    )
    families_since_seam_3: List[str] = Field(
        default_factory=list,
        description=(
            "Families whose earliest pinned-key row lands at Sub-stage 1 "
            "wire-up or later. Family order alphabetical for determinism."
        ),
    )
    per_family_since_date: Dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Map of family name -> ISO-8601 date (YYYY-MM-DD UTC) of the "
            "earliest NorthenaLedgerRow_v1 whose stamp_audit['refusal_family'] "
            "matches. Only present for families with at least one pinned-key "
            "row. Server-computed at query time per E3.β; NEVER from config."
        ),
    )
    seam_3_earliest_date: Optional[str] = Field(
        default=None,
        description=(
            "ISO-8601 date (YYYY-MM-DD UTC) — earliest across `families_since_seam_3` "
            "in `per_family_since_date`. NULL if `families_since_seam_3` is empty. "
            "Rendered into the coverage-marker `{date}` slot on the Compliance "
            "Console §4.1 Refusals card."
        ),
    )
    honest_note_when_no_families_covered: Optional[str] = Field(
        default=None,
        description=(
            "Rendered by the frontend when both family lists are empty — "
            "e.g. immediately post-Sub-stage-1 deploy, before any refusal-terminal "
            "row has fired. Honest empty-state, not fabricated coverage."
        ),
    )
