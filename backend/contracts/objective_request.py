"""Objective Request — RMS Service-2 request envelope (G0 freeze).

Spec authority: RMS Product & Engineering Spec v2.0 §8.1.

Service 2 (Day-to-Day / Objective Extraction) is governed by an
Objective Request: a user-authored objective plus a defensibility
floor. Layer D composes primitives over the Normalized Tier; A→B→C
only as fallback.

Freeze: snapshotted to tests/invariants/objective_request.contract_snapshot.json.
Cousin substrate (shape only): /reference/akki-legacy/backend/routers/signals_ask.py
request body is the closest functional cousin (objective-style question
over signals).
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.five_rings import DefensibilityClass, ScoreVector


class ObjectiveMode(str, Enum):
    """Spec §8.1: per-run or portfolio.

    * per_run   — one-shot objective, narrow scope, returns answer + trace.
    * portfolio — long-running standing objective, re-runs as the
                  Normalized Tier evolves.
    """

    PER_RUN = "per_run"
    PORTFOLIO = "portfolio"


class DefensibilityFloor(BaseModel):
    """Author-set floor below which Solva refuses to compose an answer.

    Spec §8.1 + UX ("set a defensibility floor"). Solva will not
    surface a unit in the answer whose `defensibility` ring fails this
    floor.
    """

    model_config = ConfigDict(extra="forbid")

    minimum_class: DefensibilityClass = Field(
        default=DefensibilityClass.UTTERANCE,
        description="Lowest acceptable defensibility class. Default: utterance.",
    )
    minimum_scores: ScoreVector = Field(
        default_factory=ScoreVector,
        description="Per-dimension lower bounds. Units below any dim are excluded.",
    )


class EstateRegionSelector(BaseModel):
    """Spec §8.1: scope selector against the Normalized Tier.

    Free-form for G0: a dict of filters interpreted by Layer D against
    the tier index. Examples a Layer-D resolver will support at G3:
      * {"source_refs": ["ifeed:sl-2025-q3"]}
      * {"date_range": {"from": "2025-09-01", "to": "2025-09-30"}}
      * {"modalities": ["audio", "video"]}
    Filters are AND-composed.
    """

    model_config = ConfigDict(extra="forbid")

    filters: Dict[str, Any] = Field(default_factory=dict)


class ObjectiveRequest(BaseModel):
    """The Service-2 request envelope. Spec §8.1."""

    model_config = ConfigDict(extra="forbid")

    objective_text: str = Field(
        ..., min_length=1, description="Author's free-form objective statement."
    )
    defensibility_floor: DefensibilityFloor = Field(default_factory=DefensibilityFloor)
    provenance_required: bool = Field(
        default=True,
        description="If true, every cited unit must carry a non-empty Provenance ring.",
    )
    scope: EstateRegionSelector = Field(default_factory=EstateRegionSelector)
    mode: ObjectiveMode = Field(default=ObjectiveMode.PER_RUN)
    tags: List[str] = Field(
        default_factory=list,
        description="Optional author tags; surfaced in the Operator Console (G5).",
    )
