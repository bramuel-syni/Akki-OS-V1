"""Feasibility dual-consumer schema + determinism + reproducibility gates.

Gates:
  8. `test_feasibility_single_consumer_schema` — the response schema
     served on the endpoint is IDENTICAL to what an in-process caller
     gets from `compute_feasibility()`. One shape. Two consumers.
     Structural parity.

  9. `test_feasibility_reach_ref_is_deterministic` — same Reach →
     same `reach_ref`; different Reach → different `reach_ref`. Guards
     idempotency (owner Ruling 2).

  10. `test_feasibility_snapshot_ref_changes_when_registry_updates` —
      after inserting a new Registry row that matches the reach, a
      subsequent query returns a DIFFERENT `snapshot_ref`. Guards
      reproducibility (Registry-state binding).
"""
from __future__ import annotations

from datetime import datetime, timezone

import httpx
import pytest
from httpx import ASGITransport

from contracts.feasibility_result import FeasibilityResult_v0, Freshness
from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION
from contracts.objective_request_v2 import Reach
from core import db
from server import app
from services.mtafiti.feasibility import compute_feasibility


async def _clear_registry() -> None:
    await db[MTAFITI_REGISTRY_COLLECTION].delete_many({})


async def _seed(source_ref: str, region: str, klass: str = "fact") -> None:
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
            "logged_date": datetime.now(timezone.utc).isoformat(),
            "structural_signature": None,
        },
    })


@pytest.mark.asyncio
async def test_feasibility_single_consumer_schema():
    """Endpoint response and in-process response share the SAME schema.
    Both consumers (wizard + admission) will read the identical body.
    """
    await _clear_registry()
    await _seed("s://r/1", "shared_region")
    await _seed("s://r/2", "shared_region", "utterance")

    reach = Reach(scope_refs=["shared_region"], exclusions=[], depth="baseline")

    # In-process (admission caller pattern)
    in_process = await compute_feasibility(reach)

    # Endpoint (wizard caller pattern)
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/mtafiti/feasibility", json={
            "scope_refs": ["shared_region"],
            "exclusions": [],
            "depth": "baseline",
        })
    assert resp.status_code == 200, resp.text
    endpoint = FeasibilityResult_v0.model_validate(resp.json())

    # Same schema. Not necessarily same content (computed_at differs).
    assert set(in_process.model_json_schema()["properties"].keys()) == \
           set(endpoint.model_json_schema()["properties"].keys())
    # Same reach → same reach_ref
    assert in_process.reach_ref == endpoint.reach_ref
    # Same registry state → same snapshot_ref
    assert in_process.snapshot_ref == endpoint.snapshot_ref
    # Same freshness verdict
    assert in_process.freshness == endpoint.freshness
    assert in_process.qualifying_volume == endpoint.qualifying_volume


@pytest.mark.asyncio
async def test_feasibility_reach_ref_is_deterministic():
    """Same Reach → same reach_ref; different Reach → different reach_ref."""
    await _clear_registry()

    r1 = Reach(scope_refs=["a", "b"], exclusions=["x"], depth="baseline")
    r2 = Reach(scope_refs=["b", "a"], exclusions=["x"], depth="baseline")  # order-agnostic
    r3 = Reach(scope_refs=["a"], exclusions=["x"], depth="baseline")

    result1 = await compute_feasibility(r1)
    result2 = await compute_feasibility(r2)
    result3 = await compute_feasibility(r3)

    assert result1.reach_ref == result2.reach_ref, \
        "reach_ref must be order-agnostic on scope_refs (sorted before hashing)"
    assert result1.reach_ref != result3.reach_ref, \
        "different Reach must yield different reach_ref"


@pytest.mark.asyncio
async def test_feasibility_snapshot_ref_changes_when_registry_updates():
    """Insert a new matching row → subsequent query yields different snapshot_ref."""
    await _clear_registry()
    await _seed("s://c/1", "c_region")

    reach = Reach(scope_refs=["c_region"], exclusions=[], depth="baseline")
    r_before = await compute_feasibility(reach)
    assert r_before.freshness == Freshness.FRESH
    assert r_before.snapshot_ref is not None

    # Insert a new matching row
    await _seed("s://c/2", "c_region", "utterance")

    r_after = await compute_feasibility(reach)
    assert r_after.snapshot_ref != r_before.snapshot_ref, \
        "snapshot_ref must change when qualifying rowset changes"
    assert r_after.qualifying_volume == 2
    assert r_before.qualifying_volume == 1
    # reach_ref MUST stay the same — same reach, different registry state
    assert r_after.reach_ref == r_before.reach_ref
