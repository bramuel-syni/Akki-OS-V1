"""Targeta Plan — MiningPlan assembly + version stamping (mandate §17 #8).

Reproducible: same Registry state + governing artifact + yield-layer
version → byte-identical plan_id.
"""
import hashlib
import json
from datetime import datetime, timezone
from typing import List, Optional, Sequence

from contracts.northena_ledger import LedgerArtifactRef
from contracts.targeta_plan import (
    TARGETA_MINING_PLAN_COLLECTION,
    MiningPlan,
    TargetaFloorSpec,
    TargetLocation,
)
from contracts.five_rings import DefensibilityClass
from core import db
from services.targeta.interface import EligibleCandidate


def _stable_plan_id(
    artifact_ref: LedgerArtifactRef,
    registry_snapshot_ref: str,
    ordered_source_refs: Sequence[str],
    yield_layer_version: str,
) -> str:
    """Deterministic plan id — sha256 over the inputs. Reproducible."""
    payload = json.dumps({
        "artifact": artifact_ref.model_dump(mode="json"),
        "registry_snapshot": registry_snapshot_ref,
        "order": list(ordered_source_refs),
        "yield_version": yield_layer_version,
    }, sort_keys=True)
    return "plan_" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def build_plan(
    *,
    ordered: Sequence[EligibleCandidate],
    core_baseline: Sequence[EligibleCandidate],
    floor: DefensibilityClass,
    mode: str,
    governing_artifact_ref: LedgerArtifactRef,
    registry_snapshot_ref: str,
    yield_layer_version: str = "core-only",
    generated_at: Optional[str] = None,
) -> MiningPlan:
    """Assemble a MiningPlan.

    `core_baseline` is the deterministic ordering (used for
    attribution/audit even when yield is admitted).
    """
    targets = [
        TargetLocation(source_ref=c.source_ref, region=c.region)
        for c in ordered
    ]
    baseline_refs: List[str] = [c.source_ref for c in core_baseline]
    plan_id = _stable_plan_id(
        governing_artifact_ref, registry_snapshot_ref,
        [t.source_ref for t in targets], yield_layer_version,
    )
    return MiningPlan(
        plan_id=plan_id,
        mode=mode,  # type: ignore[arg-type]
        governing_artifact_ref=governing_artifact_ref,
        registry_snapshot_ref=registry_snapshot_ref,
        ordered_targets=targets,
        defensibility_floor=TargetaFloorSpec(minimum_class=floor),
        core_baseline_ranking=baseline_refs,
        yield_layer_version=yield_layer_version,
        generated_at=generated_at or datetime.now(timezone.utc).isoformat(),
    )


async def persist(plan: MiningPlan) -> None:
    """Persist to Mongo (upsert by plan_id)."""
    await db[TARGETA_MINING_PLAN_COLLECTION].update_one(
        {"plan_id": plan.plan_id},
        {"$set": plan.model_dump(mode="json")},
        upsert=True,
    )


async def read(plan_id: str):
    return await db[TARGETA_MINING_PLAN_COLLECTION].find_one(
        {"plan_id": plan_id}, {"_id": 0}
    )
