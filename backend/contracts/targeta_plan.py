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


class ManifestEntry(BaseModel):
    """CIF §12 line 152 verbatim manifest entry — shared additive substructure.

    Landed at Critic-pass execution atomic under Owner ruling
    `docs/rulings/critic_pass_e1_2026_07_25.md` (SHA
    `42ca9e0f4605b497394772c83572b1e7c5469e17b2c6f7fa39452ec45992c80a`)
    posture (a1): additive fields on existing frozen contracts.

    ManifestEntry is FROZEN on landing; evolution is additive
    (`ManifestEntry_v1` at future seal, same as any contract).

    §0-CAL §23.1 per-line enumeration:
      * `assumption_text: str`         · rung 1 · deterministic
      * `evidence_class: Literal[...]` · rung 1 · deterministic
      * `flip_condition: str`          · rung 1 · deterministic
    """

    model_config = ConfigDict(extra="forbid")

    assumption_text: str = Field(
        ...,
        min_length=1,
        description="The load-bearing assumption text carried on the verdict.",
    )
    evidence_class: Literal["fact", "recalled", "inferred"] = Field(
        ...,
        description="Honesty-grammar source label per PROM-S1-honesty-grammar-source-labels.",
    )
    flip_condition: str = Field(
        ...,
        min_length=1,
        description=(
            "The counterfactual probe per CIF §4 verbatim: 'what, if false, "
            "flips this?'"
        ),
    )


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
    manifest_entries: List[ManifestEntry] = Field(
        default_factory=list,
        description=(
            "CIF §12 schema-required verdict manifest · load-bearing "
            "assumptions evidence-classed · unmanifested verdict rejects at "
            "submission per B-1 (Owner ruling "
            "docs/rulings/critic_pass_e1_2026_07_25.md · additive-versioning "
            "per PROM-S1-additive-versioning)."
        ),
    )
