"""Trace-lens read-only invariant (G5a GATE CONDITION 2).

Route: `GET /api/northena/trace/{trace_id}`
Route: `GET /api/discipline/lift_manifest`

Both routes must be GET-only + zero writes to any persistent store.

Enforcement approach:
1. Method enforcement: introspect FastAPI's route table + hit route with
   non-GET methods, assert 405.
2. Write-count enforcement: snapshot Mongo `opcounters` (inserts,
   updates, deletes, findAndModify) BEFORE + AFTER route hits; assert
   deltas are zero across ALL cases (known trace_id, unknown, malformed,
   method-not-allowed).

Async tests use `httpx.AsyncClient(transport=ASGITransport(app))` so the
app runs in the SAME event loop as Motor (session-scoped per conftest).
"""
from __future__ import annotations

import httpx
import pytest
from httpx import ASGITransport

from server import app


async def _opcounters() -> dict:
    """Snapshot Mongo write opcounters via serverStatus."""
    from core import db
    server_status = await db.command("serverStatus")
    op = server_status.get("opcounters", {})
    # Only write-shaped counters
    return {
        "insert": int(op.get("insert", 0)),
        "update": int(op.get("update", 0)),
        "delete": int(op.get("delete", 0)),
        "getmore": int(op.get("getmore", 0)),  # keep as sanity; getmore is a read cursor advance
    }


def _write_delta(before: dict, after: dict) -> int:
    """Return combined write delta (insert + update + delete)."""
    return (
        (after.get("insert", 0) - before.get("insert", 0))
        + (after.get("update", 0) - before.get("update", 0))
        + (after.get("delete", 0) - before.get("delete", 0))
    )


# ------- FastAPI route method enforcement ------------------------------------
def test_trace_lens_route_registered_get_only():
    """`/api/northena/trace/{trace_id}` accepts GET; other methods return 405."""
    trace_paths_in_openapi = [
        p for p in app.openapi()["paths"].keys()
        if p == "/api/northena/trace/{trace_id}"
    ]
    assert trace_paths_in_openapi, "trace-lens path missing from openapi"
    ops = app.openapi()["paths"]["/api/northena/trace/{trace_id}"]
    assert set(ops.keys()) == {"get"}, (
        f"trace-lens route registers other methods: {set(ops.keys())}"
    )


def test_lift_manifest_route_registered_get_only():
    ops = app.openapi()["paths"]["/api/discipline/lift_manifest"]
    assert set(ops.keys()) == {"get"}, (
        f"lift_manifest route registers other methods: {set(ops.keys())}"
    )


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
@pytest.mark.asyncio
async def test_trace_lens_rejects_non_get(method: str):
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await getattr(c, method)("/api/northena/trace/test-id")
    assert resp.status_code == 405, f"{method.upper()} should return 405"


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
@pytest.mark.asyncio
async def test_lift_manifest_rejects_non_get(method: str):
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await getattr(c, method)("/api/discipline/lift_manifest")
    assert resp.status_code == 405, f"{method.upper()} should return 405"


# ------- Read-only write-count enforcement (LOAD-BEARING) --------------------
@pytest.mark.asyncio
async def test_trace_lens_unknown_trace_id_writes_zero():
    before = await _opcounters()
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/northena/trace/known-to-not-exist")
    assert resp.status_code == 404
    after = await _opcounters()
    assert _write_delta(before, after) == 0, (
        f"trace-lens 404 case wrote to DB: {before} -> {after}"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("bad", ["%20", "%20%20", "a" * 200])
async def test_trace_lens_malformed_trace_id_writes_zero(bad: str):
    before = await _opcounters()
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get(f"/api/northena/trace/{bad}")
    assert resp.status_code in (400, 404), (
        f"malformed trace_id should return 400 or 404 (routing); got {resp.status_code}"
    )
    after = await _opcounters()
    assert _write_delta(before, after) == 0


@pytest.mark.asyncio
async def test_trace_lens_known_trace_id_writes_zero():
    """Round-trip: create trace via Service 1 (writes happen HERE),
    then hit the lens (which must NOT write).
    """
    from contracts.five_rings import DefensibilityClass, NormalizedUnit
    from services.service_1 import service
    import json as _json
    from pathlib import Path as _P
    fx = _json.loads((_P(__file__).parent.parent.parent
                      / "services" / "data_source" / "synthetic_assets"
                      / "rms_adversarial_v1" / "fixture.json").read_text(encoding="utf-8"))
    units = [NormalizedUnit.model_validate(u) for u in fx["units"][:2]]
    result = await service.run(
        units, objective_text="trace lens readonly test objective",
        artifact_id="trace-lens-readonly-test", artifact_version="v0",
        lawful_basis="dpa-test", floor=DefensibilityClass.NON_FACTUAL,
    )
    trace_id = result["trace_id"]

    # Now measure — writes from THIS point onward must be zero
    before = await _opcounters()
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get(f"/api/northena/trace/{trace_id}")
    assert resp.status_code == 200, resp.json()
    body = resp.json()
    assert body["trace_id"] == trace_id
    assert body["ledger_rows"], "trace_id should resolve to at least one ledger row"
    after = await _opcounters()
    assert _write_delta(before, after) == 0, (
        f"trace-lens 200 case wrote to DB: {before} -> {after}"
    )


@pytest.mark.asyncio
async def test_lift_manifest_hit_writes_zero():
    before = await _opcounters()
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/discipline/lift_manifest")
    assert resp.status_code == 200
    after = await _opcounters()
    assert _write_delta(before, after) == 0


@pytest.mark.asyncio
async def test_method_not_allowed_writes_zero():
    """Even the 405 path must not write."""
    before = await _opcounters()
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        await c.post("/api/northena/trace/whatever")
        await c.delete("/api/discipline/lift_manifest")
    after = await _opcounters()
    assert _write_delta(before, after) == 0
