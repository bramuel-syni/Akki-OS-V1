"""Targeta Mining Plan — frozen contract (mandate §8).

New at G4. Additions, not mutations.

Freeze contract: `MiningPlan.model_json_schema()` snapshotted to
`tests/invariants/targeta_mining_plan.contract_snapshot.json`. Any drift
fails CI.

CONFIRM (source §8 line): "FloorSpec + TargetLocation against
five_rings@v0, objective_request@v0, and the Registry contract."
- `FloorSpec` reused verbatim from `services/solva_depth/interfaces.py`
  (G3 landed). Wrapper is idempotent — see MiningPlan.defensibility_floor.
- `TargetLocation` — NEW here (Pydantic sub-model).
- `governing_artifact_ref` — reuses `LedgerArtifactRef` from
  `contracts/northena_ledger.py`.
"""
from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

from contracts.five_rings import DefensibilityClass
from contracts.northena_ledger import LedgerArtifactRef


TARGETA_MINING_PLAN_COLLECTION = "targeta_mining_plans"


class TargetLocation(BaseModel):
    """Where Layer A retrieval should begin. Mandate §8 sub-shape."""

    model_config = ConfigDict(extra="forbid")

    source_ref: str = Field(..., description="Registry source_ref key.")
    region: str = Field(..., description="Estate region key.")


class TargetaFloorSpec(BaseModel):
    """Serialisable floor for the Mining Plan. Wraps the same enum shape
    as `services/solva_depth/interfaces.py::FloorSpec` (frozen dataclass);
    Pydantic-serialisable form for the plan contract.
    """

    model_config = ConfigDict(extra="forbid")

    minimum_class: DefensibilityClass = Field(...)


class MiningPlan(BaseModel):
    """Mandate §8 verbatim shape."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(..., description="Deterministic plan id; reproducible per §17 #8.")
    mode: Literal["portfolio", "per_run"]
    governing_artifact_ref: LedgerArtifactRef
    registry_snapshot_ref: str = Field(..., description="Mtafiti Registry snapshot id at plan-build time.")
    ordered_targets: List[TargetLocation]
    defensibility_floor: TargetaFloorSpec
    core_baseline_ranking: List[str] = Field(
        ..., description="Deterministic core ordering, for attribution/audit."
    )
    yield_layer_version: str = Field(
        default="core-only",
        description="'core-only' when yield closed; version string when admitted (mandate §7 + §17 #7).",
    )
    generated_at: str = Field(..., description="ISO-8601 UTC.")
