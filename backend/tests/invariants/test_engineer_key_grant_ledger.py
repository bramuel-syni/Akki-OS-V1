"""Phase 8 Stage B-3 Block 3 — Ledger integration gates for
Engineer key-grant lifecycle events (Owner D4b condition 1).

Owner condition verbatim (attached to unfrozen D4b ruling, 2026-07-04):
    "Grant issuance and revocation emit ledger rows (stamp_audit
     sidecar pattern, idempotent). The FOR-argument #1 dissolves only
     because the replay-verifiable audit chain lives in frozen
     NorthenaLedgerRow_v1 — which is true only if grant events
     actually reach it. Confirm it exists or land it in Block 3;
     without it, the freeze question reopens."

Three P0 gates (verbatim Owner ratification):
  * test_engineer_key_grant_issuance_emits_ledger_row
  * test_engineer_key_grant_revocation_emits_ledger_row
  * test_engineer_key_grant_ledger_idempotent

Failure of ANY of these three reopens D4b for freeze re-ruling.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from httpx import ASGITransport, AsyncClient

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from core import db
from server import app
from services.auth import user_store
from services.auth.engineer_key_grant import EngineerKeyGrantRegistration
from services.auth.engineer_key_grant_ledger import (
    DATA_CLASS_ENGINEER_KEY_GRANT,
    record_engineer_key_grant_event,
)


async def _seed_engineer_user_and_login(client: AsyncClient) -> str:
    """Seed a distinct engineer user (email-unique per-test) and return access token."""
    email = f"engineer-{uuid.uuid4().hex[:8]}@rms.example.com"
    password = "engineer-b3-test-pw"
    # Create user via /api/auth/register (default role: ask_console_user; grant engineer via direct store).
    resp = await client.post(
        "/api/auth/register",
        json={"email": email, "password": password, "name": "Engineer B3 Test"},
    )
    assert resp.status_code == 201
    # Promote to engineer role at the store layer — the register endpoint
    # gives default `ask_console_user`, but this test needs the engineer
    # role for the router's role check.
    await db.users.update_one(
        {"email": email},
        {"$set": {"roles": ["engineer"]}},
    )
    # Re-login to receive a token carrying the new roles claim.
    resp = await client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def _issue_request_body() -> dict:
    return {
        "grantee_email": f"grantee-{uuid.uuid4().hex[:8]}@rms.example.com",
        "key_class": "external",
        "path": "live_query",
        "floor": "utterance",
        "scope": "estate",
        "justification": "Grant issued for automated integration test.",
        "lawful_basis_ref": "engineer-key-grant-lawful-basis-v0",
    }


@pytest.mark.asyncio
async def test_engineer_key_grant_issuance_emits_ledger_row():
    """Owner D4b P0 gate #1 — POST /api/engineer/key_grants → row in
    NorthenaLedgerRow_v1 with `stamp_audit.data_class="engineer_key_grant"`
    and `stamp_audit.engineer_key_grant.event_type="issued"`.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _seed_engineer_user_and_login(client)
        body = _issue_request_body()
        resp = await client.post(
            "/api/engineer/key_grants",
            json=body,
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 201, resp.text
    grant = resp.json()
    assert grant["grantee_email"] == body["grantee_email"]
    grant_id = grant["grant_id"]
    # Read the ledger row(s) with this grant_id.
    cursor = db[NORTHENA_LEDGER_COLLECTION].find({
        "reason": {"$regex": f"engineer_key_grant:issued:grant_id={grant_id}"},
    })
    rows = [d async for d in cursor]
    assert len(rows) >= 1, (
        f"Owner D4b P0 gate: NO ledger row found for grant_id={grant_id!r} issuance. "
        "Without this row the freeze question reopens."
    )
    row = rows[0]
    assert row["stage"] == "converge"
    assert row["decision"] == "terminate_success"
    stamp = row.get("stamp_audit") or {}
    assert stamp.get("data_class") == DATA_CLASS_ENGINEER_KEY_GRANT
    ek = stamp.get("engineer_key_grant") or {}
    assert ek.get("event_type") == "issued"
    assert ek.get("grant_id") == grant_id
    assert ek.get("key_class") == body["key_class"]
    assert ek.get("path") == body["path"]
    assert ek.get("floor") == body["floor"]
    assert ek.get("scope") == body["scope"]
    assert ek.get("lawful_basis_ref") == body["lawful_basis_ref"]


@pytest.mark.asyncio
async def test_engineer_key_grant_revocation_emits_ledger_row():
    """Owner D4b P0 gate #2 — POST /api/engineer/key_grants/{gid}/revoke →
    a SECOND row in NorthenaLedgerRow_v1 with `event_type="revoked"`
    and `revoked_at` populated in the stamp_audit payload.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _seed_engineer_user_and_login(client)
        # Issue.
        issue_body = _issue_request_body()
        r_iss = await client.post(
            "/api/engineer/key_grants",
            json=issue_body,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r_iss.status_code == 201, r_iss.text
        grant_id = r_iss.json()["grant_id"]
        # Revoke.
        r_rev = await client.post(
            f"/api/engineer/key_grants/{grant_id}/revoke",
            json={"reason": "Grant rescinded for automated integration test."},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r_rev.status_code == 200, r_rev.text
    revoked_grant = r_rev.json()
    assert revoked_grant["revoked_at"] is not None
    assert revoked_grant["revocation_reason"] == "Grant rescinded for automated integration test."

    # Find the revocation ledger row.
    cursor = db[NORTHENA_LEDGER_COLLECTION].find({
        "reason": {"$regex": f"engineer_key_grant:revoked:grant_id={grant_id}"},
    })
    rows = [d async for d in cursor]
    assert len(rows) >= 1, (
        f"Owner D4b P0 gate: NO ledger row found for grant_id={grant_id!r} revocation. "
        "Without this row the freeze question reopens."
    )
    row = rows[0]
    stamp = row.get("stamp_audit") or {}
    assert stamp.get("data_class") == DATA_CLASS_ENGINEER_KEY_GRANT
    ek = stamp.get("engineer_key_grant") or {}
    assert ek.get("event_type") == "revoked"
    assert ek.get("revoked_at") is not None
    assert ek.get("revocation_reason") == "Grant rescinded for automated integration test."


@pytest.mark.asyncio
async def test_engineer_key_grant_ledger_idempotent():
    """Owner D4b P0 gate #3 — repeat POST with the same (event_type,
    grant_id) tuple returns the same run_id and does NOT double-write.

    Idempotency is enforced at `record_engineer_key_grant_event` per
    (trace_id, run_id, stage) — a re-emission with the same grant_id
    and event_type produces the same run_id (because run_id =
    f"engineer-key-grant-{event}-{grant_id}") and no second insert.

    We drive this directly against the service — the router mints a
    fresh trace_id per event by design, so idempotency is proved
    through explicit trace_id reuse.
    """
    # Construct a fake grant with a known grant_id — bypass the router
    # to control trace_id determinism.
    grant_id = f"idempotency-test-{uuid.uuid4().hex[:8]}"
    grant = EngineerKeyGrantRegistration(
        grant_id=grant_id,
        grantee_email="idempotency-test@rms.example.com",
        grantor_id="test-engineer-uid",
        key_class="external",
        path="live_query",
        floor="utterance",
        scope="estate",
        justification="Idempotency integration test.",
        lawful_basis_ref="engineer-key-grant-lawful-basis-v0",
        issued_at=datetime.now(timezone.utc),
        revoked_at=None,
        revocation_reason=None,
    )
    trace_id = f"trace-idempotency-{uuid.uuid4().hex[:12]}"

    # First emit.
    run_id_1 = await record_engineer_key_grant_event(
        event_type="issued", grant=grant, trace_id=trace_id,
    )
    # Second emit — same (event_type, grant_id, trace_id).
    run_id_2 = await record_engineer_key_grant_event(
        event_type="issued", grant=grant, trace_id=trace_id,
    )
    assert run_id_1 == run_id_2, "Idempotent returns same run_id."

    # Verify Mongo has exactly ONE row.
    rows = [
        d async for d in db[NORTHENA_LEDGER_COLLECTION].find({
            "run_id": run_id_1, "trace_id": trace_id,
        })
    ]
    assert len(rows) == 1, (
        f"Owner D4b P0 gate: idempotency violated — expected 1 row, got {len(rows)}. "
        "Without idempotency, the audit chain diverges."
    )
