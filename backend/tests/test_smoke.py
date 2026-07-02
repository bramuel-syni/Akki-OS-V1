"""Backend smoke test — G0 acceptance ⌅4.

Verifies the FastAPI app boots, OpenAPI is reachable, and the G0 endpoints
return the documented shape.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from server import app

client = TestClient(app)


def test_openapi_reachable_under_api_prefix():
    r = client.get("/api/openapi.json")
    assert r.status_code == 200
    body = r.json()
    assert body["openapi"].startswith("3.")
    assert "/api/health" in body["paths"]
    assert "/api/system/state" in body["paths"]


def test_openapi_components_schemas_carry_frozen_contracts():
    """G0 follow-up — tester TEST 4. The three frozen Pydantic contracts
    MUST appear in components.schemas with non-empty `properties` maps so
    the frozen-contract discipline is machine-discoverable through the
    live OpenAPI surface.

    G4 note: `NormalizedUnit` is used as both a request body (Service 1)
    and a response model (Layer C etc). Pydantic v2 splits such schemas
    into `NormalizedUnit-Input` and `NormalizedUnit-Output` at the
    OpenAPI level — accept either form (or the un-split legacy form for
    older phases).
    """
    body = client.get("/api/openapi.json").json()
    schemas = body.get("components", {}).get("schemas", {})
    for name, min_props in [
        ("NormalizedUnit", 5),       # 5 rings + unit_id => 6, floor at 5 for safety
        ("ObjectiveRequest", 5),
        ("QualificationMatrix", 2),
        ("QualificationRule", 4),
    ]:
        candidates = [name, f"{name}-Input", f"{name}-Output"]
        found = next((c for c in candidates if c in schemas), None)
        assert found is not None, (
            f"None of {candidates} present in components.schemas"
        )
        props = schemas[found].get("properties", {})
        assert len(props) >= min_props, (
            f"{found} has {len(props)} properties, need >= {min_props}"
        )


def test_contracts_endpoints_return_valid_payloads():
    """The three /api/contracts/* GETs must return 200 + a body that
    validates against the corresponding Pydantic schema (the response_model
    contract). FastAPI does this automatically; we assert here so a
    silent regression on the surfacing routes fails CI."""
    for path in (
        "/api/contracts/five_rings",
        "/api/contracts/objective_request",
        "/api/contracts/qualification_matrix",
    ):
        r = client.get(path)
        assert r.status_code == 200, f"{path} -> {r.status_code}"
        body = r.json()
        assert isinstance(body, dict)
        assert body, f"{path} returned empty body"


def test_health_endpoint():
    r = client.get("/api/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["gate"] == "G0"


def test_system_state_surfaces_data_source_and_v_gates():
    r = client.get("/api/system/state")
    assert r.status_code == 200
    body = r.json()
    assert body["data_source"]["mode"] == "synthetic"
    assert body["data_source"]["running_on_synthetic"] is True
    ids = {g["id"] for g in body["v_gates"]}
    assert ids == {"V1", "V2", "V3"}, ids
    for g in body["v_gates"]:
        assert g["status"] == "pending", g
    assert body["qualification_matrix_rev"] == "v0"
    assert "five_rings@v0" in body["contracts_frozen"]
