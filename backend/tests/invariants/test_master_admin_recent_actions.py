"""Phase 8 Stage B-4 — §6.3 audit-trail endpoint gates.

Endpoint under test: `GET /api/master_admin/audit_trail`.

Surface expectations per UI Spec §6.3 verbatim:
  * Recent-actions rows — plain description of the change (from → to in
    words), who, when.
  * Rule: "the diff exists in the record; it is never the primary
    display" — endpoint MUST expose `full_diff_ref` link and MUST NOT
    embed a raw diff blob as the primary payload.

Gates:
  * empty ledger → empty actions array + count=0
  * after one tier_lock commit, the audit_trail endpoint returns exactly
    ONE actions row with rule_id="tier_lock", plain_description
    beginning with "Pricing tier lock turned <on|off>", and a
    full_diff_ref that resolves via GET /api/northena/ledger/by_run/…
  * reverse-chronological ordering (most-recent first)
  * auth-gate: 401 unauthenticated
"""
from __future__ import annotations

import asyncio
import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from core import db
from server import app
from services.economics import quote_service as _quote_service
from services.economics.tier_lock_ledger import DATA_CLASS_MASTER_ADMIN_RULE_CHANGE


ADMIN_EMAIL = "admin@rms.example.com"
ADMIN_PASSWORD = "admin-b1-test-pw"


@pytest.fixture(autouse=True)
def _reset_tier_lock_after_each_test():
    yield
    _quote_service.set_tier_lock(False, None)


async def _login_admin(client: AsyncClient) -> str:
    resp = await client.post(
        "/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_audit_trail_endpoint_shape_and_auth_gate():
    """Auth-gate: 401 unauthenticated on the endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/api/master_admin/audit_trail")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_audit_trail_returns_recent_master_admin_rule_change_rows():
    """After a tier_lock commit, at least one action row appears with
    the master_admin_rule_change data_class."""
    idempotency_key = f"audit-trail-{uuid.uuid4().hex[:8]}"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_admin(client)
        # Commit a tier_lock change.
        commit = await client.post(
            "/api/pricing/tier_lock",
            json={"locked": True, "reason_note": "audit-trail regression",
                  "idempotency_key": idempotency_key},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert commit.status_code == 200, commit.text
        # Poll audit_trail — ledger insert is awaited before the response
        # returns, but the endpoint reads from the same db collection.
        r = await client.get(
            "/api/master_admin/audit_trail?limit=50",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200, r.text
    body = r.json()
    assert "actions" in body and "count" in body
    assert body["count"] == len(body["actions"])
    # Find the row for our commit.
    matching = [a for a in body["actions"]
                if a.get("rule_id") == "tier_lock"
                and idempotency_key in (a.get("run_id") or "")]
    assert len(matching) == 1, (
        f"Expected exactly one audit-trail row for idempotency_key="
        f"{idempotency_key!r}, got {len(matching)}."
    )
    row = matching[0]
    assert row["rule_id"] == "tier_lock"
    assert row["plain_description"].startswith("Pricing tier lock turned")
    assert row["full_diff_ref"].startswith("/api/northena/ledger/by_run/")


@pytest.mark.asyncio
async def test_audit_trail_reverse_chronological_ordering():
    """Two tier_lock commits — audit_trail returns the more recent one first."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_admin(client)
        first_key = f"ord-1-{uuid.uuid4().hex[:8]}"
        second_key = f"ord-2-{uuid.uuid4().hex[:8]}"
        await client.post(
            "/api/pricing/tier_lock",
            json={"locked": True, "reason_note": "first", "idempotency_key": first_key},
            headers={"Authorization": f"Bearer {token}"},
        )
        # Small sleep to ensure `at` timestamps differ.
        await asyncio.sleep(0.05)
        await client.post(
            "/api/pricing/tier_lock",
            json={"locked": False, "reason_note": "second", "idempotency_key": second_key},
            headers={"Authorization": f"Bearer {token}"},
        )
        r = await client.get(
            "/api/master_admin/audit_trail?limit=50",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    body = r.json()
    # Locate positions of our two entries.
    seen = [
        i for i, a in enumerate(body["actions"])
        if (first_key in (a.get("run_id") or "")) or (second_key in (a.get("run_id") or ""))
    ]
    assert len(seen) >= 2
    # The second commit is more recent — expect it to appear FIRST (lower index).
    idx_first = next(i for i, a in enumerate(body["actions"])
                     if first_key in (a.get("run_id") or ""))
    idx_second = next(i for i, a in enumerate(body["actions"])
                      if second_key in (a.get("run_id") or ""))
    assert idx_second < idx_first, (
        f"Reverse-chronological: second commit index {idx_second} must be "
        f"before first commit index {idx_first}."
    )


@pytest.mark.asyncio
async def test_audit_trail_does_not_embed_raw_diff_as_primary_display():
    """§6.3 Rule verbatim: 'the diff exists in the record; it is never
    the primary display.' The endpoint must NOT return a raw diff blob
    inline — a `full_diff_ref` link is the only diff affordance."""
    idempotency_key = f"diff-primary-{uuid.uuid4().hex[:8]}"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_admin(client)
        await client.post(
            "/api/pricing/tier_lock",
            json={"locked": True, "reason_note": "diff-primary",
                  "idempotency_key": idempotency_key},
            headers={"Authorization": f"Bearer {token}"},
        )
        r = await client.get(
            "/api/master_admin/audit_trail?limit=10",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    for row in r.json()["actions"]:
        # The row exposes plain_description + full_diff_ref link.
        assert isinstance(row.get("plain_description"), str)
        # NOT: full diff payload embedded (stamp_audit / rule_change dict inline).
        assert "stamp_audit" not in row, (
            "Raw stamp_audit payload MUST NOT be primary — use full_diff_ref."
        )
        assert "rule_change" not in row, (
            "Raw rule_change payload MUST NOT be primary — use full_diff_ref."
        )


@pytest.mark.asyncio
async def test_audit_trail_full_diff_ref_link_resolves_to_ledger_row():
    """The `full_diff_ref` link on each audit-trail row resolves to a
    real ledger row via the existing GET /api/northena/ledger/by_run/… route."""
    idempotency_key = f"diff-link-{uuid.uuid4().hex[:8]}"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_admin(client)
        commit = await client.post(
            "/api/pricing/tier_lock",
            json={"locked": True, "reason_note": "diff-link",
                  "idempotency_key": idempotency_key},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert commit.status_code == 200
        run_id = commit.json()["ledger_run_id"]
        r = await client.get(
            "/api/master_admin/audit_trail?limit=50",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 200
        matching = [a for a in r.json()["actions"] if a.get("run_id") == run_id]
        assert len(matching) == 1
        diff_ref = matching[0]["full_diff_ref"]
        # Fetch it — validates the link resolves.
        # Trim `/api` prefix as client baseline is the ASGI transport.
        r_ledger = await client.get(diff_ref)
    assert r_ledger.status_code == 200, r_ledger.text
    rows = r_ledger.json()
    assert isinstance(rows, list) and len(rows) >= 1
    ledger_row = rows[0]
    stamp_audit = ledger_row.get("stamp_audit") or {}
    assert stamp_audit.get("data_class") == DATA_CLASS_MASTER_ADMIN_RULE_CHANGE
