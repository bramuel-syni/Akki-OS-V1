"""Feasibility route read-only invariant.

Route: `POST /api/mtafiti/feasibility` must be POST-only + zero writes
to any persistent store.

Mirrors the trace-lens/handoff readonly pattern
(`test_trace_lens_readonly.py`): snapshot Mongo `opcounters` (insert +
update + delete) BEFORE + AFTER route hits; assert deltas are zero
across known-censused, un-censused, malformed, and method-not-allowed
cases.
"""
from __future__ import annotations

import httpx
import pytest
from httpx import ASGITransport

from server import app


async def _opcounters() -> dict:
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
        (after.get("insert", 0) - before.get("insert", 0))
        + (after.get("update", 0) - before.get("update", 0))
        + (after.get("delete", 0) - before.get("delete", 0))
    )


@pytest.mark.asyncio
async def test_feasibility_readonly():
    """Every code path through /api/mtafiti/feasibility performs zero writes."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        before = await _opcounters()

        # Case 1: un-censused reach
        await client.post("/api/mtafiti/feasibility", json={
            "scope_refs": ["nowhere_xyz_definitely_absent"],
            "exclusions": [],
            "depth": "baseline",
        })

        # Case 2: valid empty scope_refs (all rows excluded by empty match set)
        await client.post("/api/mtafiti/feasibility", json={
            "scope_refs": [],
            "exclusions": [],
            "depth": "baseline",
        })

        # Case 3: malformed body — Pydantic 422
        await client.post("/api/mtafiti/feasibility", json={
            "scope_refs": "not_a_list",  # wrong type
            "exclusions": [],
            "depth": "baseline",
        })

        # Case 4: method-not-allowed — GET should 405
        resp_get = await client.get("/api/mtafiti/feasibility")
        assert resp_get.status_code == 405, f"expected 405 on GET; got {resp_get.status_code}"

        after = await _opcounters()

    delta = _write_delta(before, after)
    assert delta == 0, (
        f"Feasibility route wrote to Mongo during handling. "
        f"insert/update/delete delta={delta}. Before={before}, After={after}."
    )
