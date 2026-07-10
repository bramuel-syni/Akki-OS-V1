"""Honesty-under-absence gate — LOAD-BEARING for v3 §5.

v3 §5 verbatim (RMS_Product_Engineering_Spec_v3.md line 77):
    "a stale or un-censused region returns `unknown`, never a fabricated
     distribution."

Four gates:
  1. Un-censused scope returns `unknown` with all data-fields NULL.
  2. Censused scope returns a real distribution with non-NULL data-fields.
  3. Stale-past-threshold scope returns `stale` with real numbers + provenance.
  4. Regression sweep: no response ever mixes `unknown` freshness with
     non-NULL data (or vice versa).

Uses the existing adversarial fixture v1 (19 units, feed_id=feed_a +
7 other feed_ids) as the censused substrate. Distinct un-censused scope_ref
lives in `feasibility_fixture_augmentation.json` — does NOT modify the
shipping adversarial fixture (Item 4 HAZARD-STOP posture preserved).
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from contracts.feasibility_result import Freshness
from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION
from contracts.objective_request_v2 import Reach
from core import db
from services.mtafiti.feasibility import compute_feasibility


AUG_PATH = Path(__file__).parent / "feasibility_fixture_augmentation.json"
_AUG = json.loads(AUG_PATH.read_text())


async def _clear_registry() -> None:
    await db[MTAFITI_REGISTRY_COLLECTION].delete_many({})


async def _seed_fresh_row(source_ref: str, region: str, klass: str,
                          days_ago: int = 0) -> None:
    """Populate one MtafitiRegistryRecord in Mongo — mirrors the shape from
    contracts/mtafiti_registry.py without going through compose_record."""
    logged = (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()
    await db[MTAFITI_REGISTRY_COLLECTION].insert_one({
        "source_ref": source_ref,
        "region": region,
        "feed_id": region,
        "sensitivity": "standard",
        "defensibility_measure": {
            "source_standing": "accountable",
            "attachment": 0.0,
            "corroboration": 0.0,
            "recency_validity": 0.5,
            "contested": False,
        },
        "defensibility_runtime_mode": "declaration_baseline",
        "matrix_rule_ref": "qm.v0.rule.1",
        "defensibility_class": klass,
        "freshness_stamp": {
            "logged_date": logged,
            "structural_signature": None,
        },
    })


@pytest.mark.asyncio
async def test_feasibility_uncensused_scope_returns_unknown():
    """LOAD-BEARING honesty gate — v3 §5 verbatim."""
    await _clear_registry()
    reach = Reach(
        scope_refs=[_AUG["uncensused_scope_ref"]],
        exclusions=[],
        depth="baseline",
    )
    result = await compute_feasibility(reach)
    assert result.freshness == Freshness.UNKNOWN, \
        f"un-censused reach must return UNKNOWN; got {result.freshness}"
    assert result.qualifying_volume is None
    assert result.class_distribution is None
    assert result.snapshot_ref is None
    assert result.reach_ref  # deterministic hash landed
    assert result.computed_at  # ISO-8601 landed


@pytest.mark.asyncio
async def test_feasibility_censused_scope_returns_real_distribution():
    """Positive path — populated Registry returns real numbers."""
    await _clear_registry()
    await _seed_fresh_row("synthetic://feed_a/a.raw", "feed_a", "fact")
    await _seed_fresh_row("synthetic://feed_a/b.raw", "feed_a", "utterance")
    await _seed_fresh_row("synthetic://feed_a/c.raw", "feed_a", "utterance")
    await _seed_fresh_row("synthetic://feed_a/d.raw", "feed_a", "non_factual")
    reach = Reach(scope_refs=["feed_a"], exclusions=[], depth="baseline")
    result = await compute_feasibility(reach)
    assert result.freshness == Freshness.FRESH
    assert result.qualifying_volume == 4
    assert result.class_distribution is not None
    assert result.class_distribution.fact == 1
    assert result.class_distribution.utterance == 2
    assert result.class_distribution.non_factual == 1
    total = (result.class_distribution.fact + result.class_distribution.utterance
             + result.class_distribution.non_factual)
    assert total == result.qualifying_volume, "class_distribution must sum to qualifying_volume"
    assert result.snapshot_ref is not None


@pytest.mark.asyncio
async def test_feasibility_stale_region_returns_stale_with_provenance():
    """Stale positive path — real numbers, freshness=STALE, snapshot_ref non-null."""
    await _clear_registry()
    # 30 days old — well past the v0-provisional 7-day threshold.
    await _seed_fresh_row("synthetic://feed_d/x.raw", "feed_d", "fact", days_ago=30)
    await _seed_fresh_row("synthetic://feed_d/y.raw", "feed_d", "utterance", days_ago=30)
    reach = Reach(scope_refs=["feed_d"], exclusions=[], depth="baseline")
    result = await compute_feasibility(reach)
    assert result.freshness == Freshness.STALE, \
        f"stale-past-threshold reach must return STALE; got {result.freshness}"
    assert result.qualifying_volume == 2  # staleness is not un-known — numbers ARE real
    assert result.class_distribution is not None
    assert result.snapshot_ref is not None


@pytest.mark.asyncio
async def test_feasibility_never_fabricates():
    """Regression sweep — UNKNOWN never accompanies non-NULL data;
    FRESH/STALE always accompany non-NULL data. v3 §5 hard rule."""
    await _clear_registry()
    # Case 1: empty registry, un-censused scope
    reach1 = Reach(scope_refs=["nowhere_at_all_xyz"], exclusions=[], depth="baseline")
    r1 = await compute_feasibility(reach1)
    if r1.freshness == Freshness.UNKNOWN:
        assert r1.qualifying_volume is None
        assert r1.class_distribution is None
        assert r1.snapshot_ref is None
    else:
        assert r1.qualifying_volume is not None
        assert r1.class_distribution is not None
        assert r1.snapshot_ref is not None

    # Case 2: populated registry, censused scope
    await _seed_fresh_row("synthetic://p/z.raw", "p_region", "fact")
    reach2 = Reach(scope_refs=["p_region"], exclusions=[], depth="baseline")
    r2 = await compute_feasibility(reach2)
    if r2.freshness == Freshness.UNKNOWN:
        assert r2.qualifying_volume is None
        assert r2.class_distribution is None
        assert r2.snapshot_ref is None
    else:
        assert r2.qualifying_volume is not None
        assert r2.class_distribution is not None
        assert r2.snapshot_ref is not None

    # Case 3: registry populated but reach excludes everything
    reach3 = Reach(scope_refs=["p_region"], exclusions=["p_region"], depth="baseline")
    r3 = await compute_feasibility(reach3)
    assert r3.freshness == Freshness.UNKNOWN
    assert r3.qualifying_volume is None
    assert r3.class_distribution is None
    assert r3.snapshot_ref is None
