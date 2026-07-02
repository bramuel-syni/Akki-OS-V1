"""Handoff-download route read-only invariant.

Route: `GET /api/handoff/backend_contract_surface_v1`

Discipline mirrors `test_trace_lens_readonly.py` (G5a Gate Condition 2):

1. Method enforcement — introspect FastAPI's route table, GET only. All
   other verbs return 405.
2. Write-count enforcement — snapshot Mongo `opcounters` (inserts,
   updates, deletes) BEFORE + AFTER every case-class hit; assert deltas
   are zero across 200 / 404 / 405.
3. Response-shape enforcement — 200 returns the markdown body with the
   attachment Content-Disposition header; 404 returns a structured JSON
   envelope, not a 500.

Async tests use `httpx.AsyncClient(transport=ASGITransport(app))` so the
app runs in the SAME event loop as Motor (session-scoped per conftest).
"""
from __future__ import annotations

from pathlib import Path

import httpx
import pytest
from httpx import ASGITransport

from routers import handoff as handoff_router
from server import app


HANDOFF_ROUTE = "/api/handoff/backend_contract_surface_v1"


async def _opcounters() -> dict:
    """Snapshot Mongo write opcounters via serverStatus."""
    from core import db
    server_status = await db.command("serverStatus")
    op = server_status.get("opcounters", {})
    return {
        "insert": int(op.get("insert", 0)),
        "update": int(op.get("update", 0)),
        "delete": int(op.get("delete", 0)),
    }


def _write_delta(before: dict, after: dict) -> int:
    return (
        (after["insert"] - before["insert"])
        + (after["update"] - before["update"])
        + (after["delete"] - before["delete"])
    )


# ------- FastAPI route method enforcement ------------------------------------
def test_handoff_route_registered_get_only():
    """The handoff download path is present in OpenAPI and GET-only."""
    paths = app.openapi()["paths"]
    assert HANDOFF_ROUTE in paths, f"{HANDOFF_ROUTE} missing from openapi"
    ops = paths[HANDOFF_ROUTE]
    assert set(ops.keys()) == {"get"}, (
        f"handoff route registers non-GET methods: {set(ops.keys())}"
    )


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
@pytest.mark.asyncio
async def test_handoff_rejects_non_get(method: str):
    before = await _opcounters()
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        resp = await getattr(c, method)(HANDOFF_ROUTE)
    assert resp.status_code == 405, f"{method.upper()} should return 405"
    after = await _opcounters()
    assert _write_delta(before, after) == 0, (
        f"handoff 405 case wrote to DB: {before} -> {after}"
    )


# ------- 200 case: attachment + markdown body + zero writes ------------------
@pytest.mark.asyncio
async def test_handoff_200_returns_attachment_markdown_writes_zero():
    """The route reads the markdown artifact from disk and returns it as
    an attachment with `Content-Type: text/markdown`. Zero DB writes.
    """
    before = await _opcounters()
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        resp = await c.get(HANDOFF_ROUTE)
    assert resp.status_code == 200, resp.text

    # Header discipline
    ctype = resp.headers.get("content-type", "")
    assert ctype.startswith("text/markdown"), (
        f"expected text/markdown, got {ctype!r}"
    )
    cdisp = resp.headers.get("content-disposition", "")
    assert cdisp.startswith("attachment"), (
        f"expected attachment disposition, got {cdisp!r}"
    )
    assert "backend_contract_surface_v1.md" in cdisp, (
        f"filename missing from disposition: {cdisp!r}"
    )

    # Body discipline: matches the on-disk artifact byte-for-byte (freshness)
    on_disk = Path(
        "/app/docs/handoff/backend_contract_surface_v1.md"
    ).read_text(encoding="utf-8")
    assert resp.text == on_disk, (
        "handoff route body does not match /app/docs/handoff/"
        "backend_contract_surface_v1.md — freshness broken or caching leaked"
    )

    after = await _opcounters()
    assert _write_delta(before, after) == 0, (
        f"handoff 200 case wrote to DB: {before} -> {after}"
    )


# ------- 404 case: structured envelope + zero writes -------------------------
@pytest.mark.asyncio
async def test_handoff_404_when_artifact_missing_writes_zero(monkeypatch):
    """When the on-disk artifact is absent, the route returns a
    structured 404 envelope (not a 500). Zero DB writes.
    """
    fake_path = Path("/tmp/rms-nonexistent-handoff-artifact.md")
    assert not fake_path.exists(), "test precondition: fake path must not exist"
    monkeypatch.setattr(
        handoff_router, "HANDOFF_ARTIFACT_PATH", fake_path
    )

    before = await _opcounters()
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        resp = await c.get(HANDOFF_ROUTE)
    assert resp.status_code == 404, resp.text

    body = resp.json()
    detail = body.get("detail", {})
    assert isinstance(detail, dict), (
        f"expected structured detail dict, got {type(detail).__name__}"
    )
    assert detail.get("reason") == "handoff_artifact_not_found", (
        f"unexpected 404 envelope: {body!r}"
    )
    assert "path" in detail, f"404 envelope missing 'path' key: {body!r}"

    after = await _opcounters()
    assert _write_delta(before, after) == 0, (
        f"handoff 404 case wrote to DB: {before} -> {after}"
    )
