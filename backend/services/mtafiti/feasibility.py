"""Mtafiti Feasibility — Estate Feasibility Query compute service.

Spec authority: RMS Product & Engineering Spec v3 §5.

**Objective-blind** (mandate: Mtafiti is objective-blind; §17 #1).
Signature carries no `ObjectiveRequest` — only a `Reach`, which is a
grammar dimension, not an objective.

**Deterministic** — same Registry state + same Reach input → same
`FeasibilityResult_v0` output. `reach_ref` and `snapshot_ref` are
sha256-16 aggregate hashes over sorted inputs so tests can bind
idempotency mechanically.

**Read-only** — no writes to `MTAFITI_REGISTRY_COLLECTION` or any other
Mongo collection during handling. Enforced by
`tests/invariants/test_feasibility_readonly.py`.

**Config-driven freshness threshold** (Ruling 3 disposition — plain
versioned config, NOT snapshotted): `feasibility_config.v0.json`
carries `freshness_threshold_days`. Bumps to `v1.json` on threshold
change; never in-place mutation. Not a frozen contract (Term 2
precedent: shape freezes, values version).
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List

from contracts.feasibility_result import (
    ClassDistribution,
    FeasibilityResult_v0,
    Freshness,
)
from contracts.objective_request_v2 import Reach
from core import db
from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION


_CONFIG_PATH = Path(__file__).parent / "feasibility_config.v0.json"


def _load_config() -> Dict:
    """Load `feasibility-config@v0` — plain versioned config per Ruling 3.

    Master Admin bumps to `v1.json` on threshold update; never in-place
    mutation. This function reads the CURRENT bless (`v0.json`).
    """
    return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))


def _compute_reach_ref(reach: Reach) -> str:
    """Deterministic hash of the input Reach.

    Formula: sha256("|".join(sorted(scope_refs) + sorted(exclusions) + [depth]))[:16]

    Load-bearing for the DPO prove-one-run binding (snapshot↔reach
    correspondence must be mechanical, not assumed — per owner Ruling 2).
    """
    parts = sorted(reach.scope_refs) + sorted(reach.exclusions) + [reach.depth]
    material = "|".join(parts)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _compute_snapshot_ref(rows: List[Dict]) -> str:
    """Deterministic hash of the Registry state producing this response.

    Aggregate over each qualifying row's (source_ref, logged_date,
    structural_signature) — sorted, joined, sha256-16. Same rows → same
    ref. Any change to a row's freshness_stamp → different ref.
    """
    row_keys = []
    for row in rows:
        fs = row.get("freshness_stamp") or {}
        row_keys.append(
            f"{row.get('source_ref', '')}|"
            f"{fs.get('logged_date', '')}|"
            f"{fs.get('structural_signature', '') or ''}"
        )
    row_keys.sort()
    material = "|".join(row_keys)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _row_matches_reach(row: Dict, reach: Reach) -> bool:
    """Deterministic scope match.

    A row matches iff:
      * `row['region']` is in `reach.scope_refs`, AND
      * `row['region']` is NOT in `reach.exclusions`.

    At G4/Phase-1, region == feed_id (see `services/mtafiti/census.py:55-58`).
    Depth is authored authoring on the Reach; it does NOT filter rows at
    Phase 1 — it drives Solva reasoning depth downstream. `reach_ref`
    still binds depth per Ruling 2.
    """
    region = row.get("region", "")
    if region in reach.exclusions:
        return False
    return region in set(reach.scope_refs)


def _classify(rows: List[Dict]) -> ClassDistribution:
    """Bucket qualifying rows by their `defensibility_class` field.

    `MtafitiRegistryRecord.defensibility_class` is `Literal["fact",
    "utterance", "non_factual"]` (see `contracts/mtafiti_registry.py:91`).
    """
    counts = {"fact": 0, "utterance": 0, "non_factual": 0}
    for row in rows:
        klass = row.get("defensibility_class")
        if klass in counts:
            counts[klass] += 1
    return ClassDistribution(**counts)


def _determine_freshness_for_rows(rows: List[Dict]) -> Freshness:
    """v3 §5 honesty semantics.

    * ZERO rows → UNKNOWN (un-censused reach).
    * ANY qualifying row past threshold → STALE.
    * All qualifying rows within threshold → FRESH.
    """
    if not rows:
        return Freshness.UNKNOWN
    cfg = _load_config()
    threshold_days = int(cfg.get("freshness_threshold_days", 7))
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=threshold_days)
    for row in rows:
        fs = row.get("freshness_stamp") or {}
        logged = fs.get("logged_date")
        if not logged:
            # Missing L1 timestamp → conservative: treat as stale
            return Freshness.STALE
        try:
            logged_dt = datetime.fromisoformat(logged.replace("Z", "+00:00"))
        except ValueError:
            return Freshness.STALE
        if logged_dt < cutoff:
            return Freshness.STALE
    return Freshness.FRESH


async def compute_feasibility(reach: Reach) -> FeasibilityResult_v0:
    """Objective-blind, deterministic feasibility read.

    Returns a `FeasibilityResult_v0` per v3 §5 semantics:
      * UNKNOWN when no Registry rows match the reach (honesty-under-absence).
      * FRESH / STALE with real qualifying_volume + class_distribution
        + snapshot_ref otherwise.

    NEVER fabricates. Read-only (no writes).
    """
    reach_ref = _compute_reach_ref(reach)
    computed_at = datetime.now(timezone.utc).isoformat()

    # Read Registry — objective-blind projection over region + defensibility_class + freshness.
    projection = {
        "_id": 0,
        "source_ref": 1,
        "region": 1,
        "defensibility_class": 1,
        "freshness_stamp": 1,
    }
    cursor = db[MTAFITI_REGISTRY_COLLECTION].find({}, projection)
    all_rows = [r async for r in cursor]

    qualifying = [r for r in all_rows if _row_matches_reach(r, reach)]
    freshness = _determine_freshness_for_rows(qualifying)

    if freshness == Freshness.UNKNOWN:
        return FeasibilityResult_v0(
            reach_ref=reach_ref,
            qualifying_volume=None,
            class_distribution=None,
            freshness=Freshness.UNKNOWN,
            snapshot_ref=None,
            computed_at=computed_at,
        )

    return FeasibilityResult_v0(
        reach_ref=reach_ref,
        qualifying_volume=len(qualifying),
        class_distribution=_classify(qualifying),
        freshness=freshness,
        snapshot_ref=_compute_snapshot_ref(qualifying),
        computed_at=computed_at,
    )
