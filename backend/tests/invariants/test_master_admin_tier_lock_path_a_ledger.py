"""Phase 8 Stage B-4 Block 1 — Master Admin tier_lock Path A ledger gates.

Owner ratification 2026-07-05: tier_lock is the Path A canonical rule.
Path A means: `POST /api/pricing/tier_lock` writes a `tier_lock.vN.json`
versioned marker on disk + emits `NorthenaLedgerRow_v1` with
`stamp_audit.data_class="master_admin_rule_change"` + sets runtime state
via `_quote_service.set_tier_lock(...)`. Repeat POST with the same
`idempotency_key` is a no-op returning the same `ledger_run_id` +
`versioned_file_path` (idempotent-once). Reversibility is IMPLICIT —
opposite POST with a different idempotency_key writes a NEW versioned
file + NEW ledger row.

Three P0 gates (mirror B-3 D4b P0 ledger gates):
  * test_tier_lock_commit_emits_ledger_row
  * test_tier_lock_commit_writes_versioned_file
  * test_tier_lock_commit_idempotent_by_idempotency_key
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from core import db
from server import app
from services.economics import quote_service as _quote_service
from services.economics.tier_lock_ledger import (
    DATA_CLASS_MASTER_ADMIN_RULE_CHANGE,
)


ADMIN_EMAIL = "admin@rms.example.com"
ADMIN_PASSWORD = "admin-b1-test-pw"

ECONOMICS_DIR = (Path(__file__).resolve().parent.parent.parent
                 / "services" / "economics")


@pytest.fixture(autouse=True)
def _reset_tier_lock_after_each_test():
    """Test-cleanliness: ensure `_TIER_LOCK_STATE` is unlocked after
    each test in this module so bleed-over does not refuse the mint
    path in downstream tests (phase_5_stage_b_async, phase_6_stage_b)."""
    yield
    _quote_service.set_tier_lock(False, None)


async def _login_master_admin(client: AsyncClient) -> str:
    """Log in the seeded admin (roles include master_admin) and return
    the bearer access_token."""
    resp = await client.post(
        "/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def _read_current_lock_files() -> list[Path]:
    return sorted(ECONOMICS_DIR.glob("tier_lock.v*.json"))


@pytest.mark.asyncio
async def test_tier_lock_commit_emits_ledger_row():
    """Owner P0 gate #1 — POST /api/pricing/tier_lock as master_admin
    writes a NorthenaLedgerRow_v1 with stamp_audit.data_class=
    "master_admin_rule_change" and rule_change.rule_id="tier_lock".
    """
    idempotency_key = f"tier-lock-emit-{uuid.uuid4().hex[:8]}"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_master_admin(client)
        resp = await client.post(
            "/api/pricing/tier_lock",
            json={
                "locked": True,
                "reason_note": "Path A ledger test — lock.",
                "idempotency_key": idempotency_key,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["locked"] is True
    assert body["reason_note"] == "Path A ledger test — lock."
    assert body["trace_id"].startswith("master-admin-tier-lock-")
    assert body["ledger_run_id"].startswith("master-admin-rule-change-tier_lock-")

    # Verify the ledger row exists.
    cursor = db[NORTHENA_LEDGER_COLLECTION].find({
        "run_id": body["ledger_run_id"],
        "trace_id": body["trace_id"],
    })
    rows = [d async for d in cursor]
    assert len(rows) == 1, (
        f"Path A P0 gate: expected exactly 1 ledger row for "
        f"run_id={body['ledger_run_id']!r}, got {len(rows)}."
    )
    row = rows[0]
    assert row["stage"] == "converge"
    assert row["decision"] == "terminate_success"
    stamp = row.get("stamp_audit") or {}
    assert stamp.get("data_class") == DATA_CLASS_MASTER_ADMIN_RULE_CHANGE
    rc = stamp.get("rule_change") or {}
    assert rc.get("rule_id") == "tier_lock"
    assert rc.get("to") is True
    assert rc.get("reason_note") == "Path A ledger test — lock."
    assert rc.get("idempotency_key") == idempotency_key


@pytest.mark.asyncio
async def test_tier_lock_commit_writes_versioned_file():
    """Owner P0 gate #2 — POST /api/pricing/tier_lock writes a
    `tier_lock.vN.json` versioned marker on disk (N is next serial).
    """
    idempotency_key = f"tier-lock-file-{uuid.uuid4().hex[:8]}"
    files_before = _read_current_lock_files()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_master_admin(client)
        resp = await client.post(
            "/api/pricing/tier_lock",
            json={
                "locked": False,
                "reason_note": "Path A versioned-file test — unlock.",
                "idempotency_key": idempotency_key,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200, resp.text
    files_after = _read_current_lock_files()
    # At least one new file MUST exist (append-only).
    assert len(files_after) > len(files_before), (
        f"Path A P0 gate: no new tier_lock.vN.json file written. "
        f"Before: {[p.name for p in files_before]}. "
        f"After: {[p.name for p in files_after]}."
    )
    # Locate OUR file by idempotency_key (not lex ordering — v10 sorts
    # before v2 in a plain glob sort).
    our_files = []
    for path in files_after:
        try:
            m = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if m.get("idempotency_key") == idempotency_key:
            our_files.append((path, m))
    assert len(our_files) == 1, (
        f"Expected exactly one tier_lock.vN.json for idempotency_key="
        f"{idempotency_key!r}, got {len(our_files)}."
    )
    _, marker = our_files[0]
    assert marker["rule_id"] == "tier_lock"
    assert marker["locked"] is False
    assert marker["reason_note"] == "Path A versioned-file test — unlock."
    assert marker["idempotency_key"] == idempotency_key


@pytest.mark.asyncio
async def test_tier_lock_commit_idempotent_by_idempotency_key():
    """Owner P0 gate #3 — repeat POST with same idempotency_key returns
    the same `ledger_run_id` and does NOT double-write the ledger row.
    """
    idempotency_key = f"tier-lock-idempotent-{uuid.uuid4().hex[:8]}"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_master_admin(client)

        r1 = await client.post(
            "/api/pricing/tier_lock",
            json={"locked": True, "reason_note": "idem-1", "idempotency_key": idempotency_key},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r1.status_code == 200
        run_id_1 = r1.json()["ledger_run_id"]

        r2 = await client.post(
            "/api/pricing/tier_lock",
            json={"locked": True, "reason_note": "idem-2-should-be-noop",
                  "idempotency_key": idempotency_key},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r2.status_code == 200
        run_id_2 = r2.json()["ledger_run_id"]

    assert run_id_1 == run_id_2, (
        f"Path A P0 gate: idempotency violated — repeat POST with same "
        f"idempotency_key yielded different run_ids: "
        f"{run_id_1!r} vs {run_id_2!r}."
    )
    # Mongo has exactly ONE row for this run_id.
    rows = [d async for d in db[NORTHENA_LEDGER_COLLECTION].find({"run_id": run_id_1})]
    assert len(rows) == 1, (
        f"Path A P0 gate: idempotency violated — expected 1 row for "
        f"run_id={run_id_1!r}, got {len(rows)}."
    )
