"""Service 1 v1 invariants — Product v2.1 §2.1 (Day Zero).

Structural + end-to-end tests. Uses MongoDB via `core.db` for the
end-to-end synthetic flow.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from contracts.five_rings import DefensibilityClass, NormalizedUnit
from services.service_1 import service


FIXTURE_PATH = (
    Path(__file__).parent.parent.parent / "services" / "data_source"
    / "synthetic_assets" / "rms_adversarial_v1" / "fixture.json"
)


def _fixture_units(n: int = 4) -> list:
    fx = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return [NormalizedUnit.model_validate(u) for u in fx["units"][:n]]


# ------- Composition-time floor re-assertion (defense-in-depth) --------------
@pytest.mark.asyncio
async def test_service_1_refuses_no_floor():
    units = _fixture_units(1)
    with pytest.raises(service.Service1Refusal) as exc:
        await service.run(
            units, objective_text="test objective",
            artifact_id="test", artifact_version="v0",
            lawful_basis="test-basis", floor=None,  # type: ignore[arg-type]
        )
    assert exc.value.reason == "no_defensibility_floor"


@pytest.mark.asyncio
async def test_service_1_refuses_no_lawful_basis():
    units = _fixture_units(1)
    with pytest.raises(service.Service1Refusal) as exc:
        await service.run(
            units, objective_text="test objective",
            artifact_id="test", artifact_version="v0",
            lawful_basis="", floor=DefensibilityClass.UTTERANCE,
        )
    assert exc.value.reason == "no_lawful_basis"


# ------- End-to-end synthetic ------------------------------------------------
@pytest.mark.asyncio
async def test_service_1_end_to_end_synthetic():
    """Run fixture units through Service 1; assert conclusion + trace + ledger."""
    units = _fixture_units(3)
    result = await service.run(
        units, objective_text="test objective",
        artifact_id="test-day-zero-run",
        artifact_version="v0",
        lawful_basis="dpa-lawful-basis-test",
        floor=DefensibilityClass.NON_FACTUAL,   # accept everything for synthetic run
    )
    assert result["run_id"]
    assert result["trace_id"]
    assert result["mining_plan_id"]
    assert result["mining_plan_id"].startswith("plan_")
    assert result["converged_unit_count"] == 3
    assert result["yield_layer_version"] == "core-only"


# ------- Ledger correlation --------------------------------------------------
@pytest.mark.asyncio
async def test_service_1_ledger_correlation():
    """Ledger rows must correlate to run_id and cover admit + gate + converge."""
    from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
    from core import db

    units = _fixture_units(2)
    result = await service.run(
        units, objective_text="test objective",
        artifact_id="ledger-correlation-test",
        artifact_version="v0",
        lawful_basis="dpa-lawful-basis-test",
        floor=DefensibilityClass.NON_FACTUAL,
    )
    run_id = result["run_id"]
    rows = [
        r async for r in
        db[NORTHENA_LEDGER_COLLECTION].find({"run_id": run_id}, {"_id": 0}).sort("at", 1)
    ]
    stages = [r["stage"] for r in rows]
    assert "admit" in stages
    assert "gate" in stages
    assert "converge" in stages
    # Convergence terminates the run:
    assert rows[-1]["decision"] == "terminate_success"


# ------- Status endpoint (via service method) --------------------------------
@pytest.mark.asyncio
async def test_service_1_status_by_run():
    units = _fixture_units(1)
    result = await service.run(
        units, objective_text="test objective",
        artifact_id="status-test",
        artifact_version="v0",
        lawful_basis="dpa-lawful-basis-test",
        floor=DefensibilityClass.NON_FACTUAL,
    )
    status = await service.status_by_run(result["run_id"])
    assert status["run_id"] == result["run_id"]
    assert status["stage"] == "converge"
    assert status["decision"] == "terminate_success"
    assert status["mining_plan_id"] == result["mining_plan_id"]


# ------- Reproducibility (mining plan is byte-identical for same inputs) -----
@pytest.mark.asyncio
async def test_service_1_reproducible_plan_id():
    """Two runs over identical fixture inputs + governing artifact yield
    identical plan_ids. (§17 #8 for Targeta; end-to-end verification.)"""
    units = _fixture_units(2)
    r1 = await service.run(
        units, objective_text="test objective",
        artifact_id="repro-test", artifact_version="v0",
        lawful_basis="dpa-lawful-basis-test",
        floor=DefensibilityClass.NON_FACTUAL,
    )
    r2 = await service.run(
        units, objective_text="test objective",
        artifact_id="repro-test", artifact_version="v0",
        lawful_basis="dpa-lawful-basis-test",
        floor=DefensibilityClass.NON_FACTUAL,
    )
    assert r1["mining_plan_id"] == r2["mining_plan_id"]


# ------- OpenAPI surface -----------------------------------------------------
def test_service_1_openapi_surface_has_endpoints():
    """/api/openapi.json must expose service_1 endpoints + response models."""
    from server import app
    schema = app.openapi()
    paths = schema.get("paths", {})
    assert "/api/service_1/run" in paths, "POST /api/service_1/run missing from openapi"
    assert "/api/service_1/run/{run_id}" in paths, (
        "GET /api/service_1/run/{run_id} missing from openapi"
    )
    assert "/api/service_1/status" in paths, "GET /api/service_1/status missing"
    components = schema.get("components", {}).get("schemas", {})
    for req in ("Service1RunRequest", "Service1RunSummary", "Service1RunStatus"):
        assert req in components, f"{req} missing from openapi components.schemas"
