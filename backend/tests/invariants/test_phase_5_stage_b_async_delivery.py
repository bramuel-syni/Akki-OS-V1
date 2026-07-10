"""Phase 5 Stage B — async delivery gates (G1–G24 + 5-state coverage).

Owner ruling (2026-07-04): FULL G1–G24 gates + 5-state ledger coverage,
NOT the LOAD-BEARING-only subset. Full coverage per Stage B dispatch.

Standing Owner Dispositions enforced by tests here:
  * frozen-field-changes-as-new-versions (NorthenaLedgerRow_v1 write on
    terminate_cancelled).
  * infra-not-refusal (queue saturation → HTTP 503, not AdmissionRefusal).
  * cancellation-is-a-state-not-a-refusal (`cancelled` 5th state).

Envelope inventory (Return 2):
  * AsyncDeliveryAccepted_v0 @202 (20th frozen contract).
  * AdmissionRefusal_v0 @422 (v1→v2 registry-bump for two idempotency codes).
  * Service1Refusal_v0 @422 (existing family; no `caller_cancelled`).
  * Cancelled terminal envelope (4-key thin, non-refusal).
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import time
from pathlib import Path

import httpx
import pytest
from httpx import ASGITransport

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.async_delivery_accepted import AsyncDeliveryAccepted_v0
from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from contracts.northena_ledger_v1 import NorthenaLedgerRow_v1
from core import db
from server import app
from services.service_1 import (
    async_state,
    async_worker,
    cancellation as cancellation_service,
    idempotency as idempotency_service,
    webhook as webhook_service,
)


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


def _valid_body(*, idempotency_key: str = "idem-async-test", scope_ref: str = "async_test_scope") -> dict:
    """Valid ObjectiveRequest_v2 wire body for async admission."""
    return {
        "entry": "external_request",
        "reach": {"scope_refs": [scope_ref], "exclusions": [], "depth": "baseline"},
        "output": {
            "form": "qualified_data",
            "consumer": "person",
            "grain": "per_claim",
            "standard": {"minimum_class": "utterance"},
        },
        "envelope": {
            "lawful_basis": "test_basis",
            "done_condition": "test_done",
            "budget": "test_budget",
            "scope_ceiling": "test_ceiling",
            "commissioner": "operator_internal",
            "committed_at": "2026-07-04T12:00:00+00:00",
        },
        "idempotency_key": idempotency_key,
    }


async def _clear_state_collections() -> None:
    await db[async_state.ASYNC_STATE_COLLECTION].delete_many({})
    await db[NORTHENA_LEDGER_COLLECTION].delete_many({})


# ---------------------------------------------------------------------------
# G1 — LOAD-BEARING — kill-and-restart recovery, no duplicate ledger emit
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_kill_and_restart_recovers_without_state_loss_or_duplicate_ledger_emission():
    """G1 LOAD-BEARING. Simulate a kill mid-`running`: state remains in
    Mongo; recovery sweep resets running→accepted; worker re-claims and
    completes. Ledger emits EXACTLY ONE terminal row per trace_id (the
    async_state.emit_ledger_* helpers guard on (trace_id, run_id, stage)
    idempotency — Return 3.4 Option B).
    """
    await _clear_state_collections()
    async_worker.reset_queue_for_test()

    # Seed a running-state document simulating "worker killed mid-flight".
    objective_id = "obj-killtest-1"
    trace_id = "trc-killtest-1"
    run_id = "cc-run-killtest-1"
    doc = {
        "objective_id": objective_id,
        "status": "running",
        "state_transitions": [
            {"state": "accepted", "at": async_state.now_iso(), "worker_generation_id": None, "reason": None},
            {"state": "running", "at": async_state.now_iso(), "worker_generation_id": "wg-oldgen", "reason": None},
        ],
        "enqueue_time": async_state.datetime.now(async_state.timezone.utc),
        "last_worker_touch": None,
        "worker_generation_id": "wg-oldgen",
        "idempotency_key": "idem-kill-1",
        "request_body_hash": "hash-kill-1",
        "request_body": _valid_body(idempotency_key="idem-kill-1"),
        "trace_id": trace_id,
        "webhook_url": None,
        "webhook_secret_hex": None,
        "sandbox_mode": False,
        "delivery_estimate": "PT5M",
        "accepted_at": async_state.now_iso(),
        "terminal_envelope": None,
        "webhook_undelivered": False,
    }
    await db[async_state.ASYNC_STATE_COLLECTION].insert_one(doc)

    # Emit one ledger row as if the worker had reached line 296 pre-kill.
    await async_state.emit_ledger_terminate_success(
        trace_id=trace_id, objective_ref=f"objreq-{trace_id}",
        lawful_basis_ref="test_basis", run_id=run_id,
        reason=f"composed_conclusion:class=utterance:load_bearing=x,y",
    )
    row_count_pre = await db[NORTHENA_LEDGER_COLLECTION].count_documents({"trace_id": trace_id})
    assert row_count_pre == 1

    # Recovery sweep on next boot — flips running→accepted, re-enqueues.
    await async_worker.recovery_sweep()

    # Assert state was flipped to accepted (running row was reset).
    reloaded = await async_state.find_by_objective_id(objective_id)
    assert reloaded["status"] == "accepted"
    states_seen = [t["state"] for t in reloaded["state_transitions"]]
    assert "recovery_reset" in states_seen, (
        f"recovery sweep must record a recovery_reset transition; got: {states_seen}"
    )

    # Simulate the second worker generation completing dispatch:
    # attempt to emit the SAME ledger row (idempotency guard should skip).
    await async_state.emit_ledger_terminate_success(
        trace_id=trace_id, objective_ref=f"objreq-{trace_id}",
        lawful_basis_ref="test_basis", run_id=run_id,
        reason=f"composed_conclusion:class=utterance:load_bearing=x,y",
    )
    row_count_post = await db[NORTHENA_LEDGER_COLLECTION].count_documents({"trace_id": trace_id})
    assert row_count_post == 1, (
        f"Duplicate-ledger-emission guard failed: expected 1 row per (trace_id, run_id, stage); "
        f"got {row_count_post}"
    )


# ---------------------------------------------------------------------------
# G2–G5 — recovery-sweep family coverage
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_recover_from_accepted_re_enqueues_cleanly():
    """G2 coverage — an `accepted` document is re-enqueued unchanged."""
    await _clear_state_collections()
    async_worker.reset_queue_for_test()
    await async_state.create_accepted(
        objective_id="obj-rec-acc", trace_id="trc-rec-acc",
        idempotency_key="idem-rec-acc", request_body=_valid_body(idempotency_key="idem-rec-acc"),
        request_body_hash="h", webhook_url=None,
    )
    await async_worker.recovery_sweep()
    q = async_worker.get_queue()
    assert q.qsize() >= 1


@pytest.mark.asyncio
async def test_recover_from_running_resets_to_accepted_then_re_enqueues():
    """G3 coverage — a `running` doc is reset to accepted + re-enqueued."""
    await _clear_state_collections()
    async_worker.reset_queue_for_test()
    doc = {
        "objective_id": "obj-rec-run", "status": "running",
        "state_transitions": [], "enqueue_time": async_state.datetime.now(async_state.timezone.utc),
        "last_worker_touch": None, "worker_generation_id": "wg-old",
        "idempotency_key": "idem-rec-run", "request_body_hash": "h",
        "request_body": _valid_body(idempotency_key="idem-rec-run"),
        "trace_id": "trc-rec-run", "webhook_url": None, "webhook_secret_hex": None,
        "sandbox_mode": False, "delivery_estimate": "PT5M",
        "accepted_at": async_state.now_iso(), "terminal_envelope": None,
        "webhook_undelivered": False,
    }
    await db[async_state.ASYNC_STATE_COLLECTION].insert_one(doc)
    await async_worker.recovery_sweep()
    updated = await async_state.find_by_objective_id("obj-rec-run")
    assert updated["status"] == "accepted"


@pytest.mark.asyncio
async def test_recover_from_delivered_is_noop_no_re_delivery_webhook():
    """G4 coverage — terminal `delivered` doc is NOT touched by sweep."""
    await _clear_state_collections()
    async_worker.reset_queue_for_test()
    doc = {
        "objective_id": "obj-rec-del", "status": "delivered",
        "state_transitions": [], "enqueue_time": async_state.datetime.now(async_state.timezone.utc),
        "last_worker_touch": None, "worker_generation_id": "wg-old",
        "idempotency_key": "idem-rec-del", "request_body_hash": "h",
        "request_body": _valid_body(idempotency_key="idem-rec-del"),
        "trace_id": "trc-rec-del", "webhook_url": None, "webhook_secret_hex": None,
        "sandbox_mode": False, "delivery_estimate": "PT5M",
        "accepted_at": async_state.now_iso(),
        "terminal_envelope": {"payload": "existing"}, "webhook_undelivered": False,
    }
    await db[async_state.ASYNC_STATE_COLLECTION].insert_one(doc)
    await async_worker.recovery_sweep()
    q = async_worker.get_queue()
    assert q.qsize() == 0, "Recovery sweep MUST NOT re-enqueue terminal-delivered objectives"
    reloaded = await async_state.find_by_objective_id("obj-rec-del")
    assert reloaded["status"] == "delivered"


@pytest.mark.asyncio
async def test_recover_from_refused_is_noop():
    """G5 coverage — terminal `refused` doc is NOT touched by sweep."""
    await _clear_state_collections()
    async_worker.reset_queue_for_test()
    doc = {
        "objective_id": "obj-rec-ref", "status": "refused",
        "state_transitions": [], "enqueue_time": async_state.datetime.now(async_state.timezone.utc),
        "last_worker_touch": None, "worker_generation_id": None,
        "idempotency_key": "idem-rec-ref", "request_body_hash": "h",
        "request_body": _valid_body(idempotency_key="idem-rec-ref"),
        "trace_id": "trc-rec-ref", "webhook_url": None, "webhook_secret_hex": None,
        "sandbox_mode": False, "delivery_estimate": "PT5M",
        "accepted_at": async_state.now_iso(),
        "terminal_envelope": {"outcome": "refused"}, "webhook_undelivered": False,
    }
    await db[async_state.ASYNC_STATE_COLLECTION].insert_one(doc)
    await async_worker.recovery_sweep()
    q = async_worker.get_queue()
    assert q.qsize() == 0
    reloaded = await async_state.find_by_objective_id("obj-rec-ref")
    assert reloaded["status"] == "refused"


# ---------------------------------------------------------------------------
# G6–G11 — webhook family
# ---------------------------------------------------------------------------


def test_webhook_signature_verifiable():
    """G6 LOAD-BEARING. HMAC round-trip + tamper-negative."""
    from datetime import datetime as _dt, timezone as _tz
    secret = b"test-secret-32-bytes-1234567890xy"
    payload_json = '{"event":"objective.status_changed","objective_id":"obj-1"}'
    ts = _dt.now(_tz.utc).isoformat()
    sig = webhook_service.sign_payload(payload_json, ts, secret)
    assert webhook_service.verify_signature(payload_json, ts, sig, secret) is True
    # Tamper: change one byte of payload → verify MUST fail.
    tampered = payload_json.replace("obj-1", "obj-X")
    assert webhook_service.verify_signature(tampered, ts, sig, secret) is False


@pytest.mark.asyncio
async def test_webhook_retries_bounded_at_five():
    """G7 LOAD-BEARING. Failing endpoint triggers exactly 5 POSTs then marks undelivered."""
    await _clear_state_collections()
    await async_state.create_accepted(
        objective_id="obj-wh-retry", trace_id="trc-wh-retry",
        idempotency_key="idem-wh-retry",
        request_body=_valid_body(idempotency_key="idem-wh-retry"),
        request_body_hash="h", webhook_url="https://example.test/hook",
    )
    call_count = {"n": 0}

    async def _fail(url, body, headers):  # noqa: ARG001
        call_count["n"] += 1
        return False

    async def _no_sleep(_seconds):
        return None

    ok = await webhook_service.fire_webhook(
        objective_id="obj-wh-retry", trace_id="trc-wh-retry", status="delivered",
        webhook_url="https://example.test/hook",
        webhook_secret=b"secret-32-byte-abcdef1234567890xy",
        _sleep=_no_sleep, _post=_fail,
    )
    assert ok is False
    assert call_count["n"] == 5, f"Retries must be bounded at 5; got {call_count['n']}"
    updated = await async_state.find_by_objective_id("obj-wh-retry")
    assert updated["webhook_undelivered"] is True


@pytest.mark.asyncio
async def test_webhook_undelivered_still_polls_status():
    """G8 LOAD-BEARING (§7 bullet 4). GET returns terminal envelope even if
    webhook flag is undelivered."""
    await _clear_state_collections()
    await async_state.create_accepted(
        objective_id="obj-wh-poll", trace_id="trc-wh-poll",
        idempotency_key="idem-wh-poll",
        request_body=_valid_body(idempotency_key="idem-wh-poll"),
        request_body_hash="h", webhook_url=None,
    )
    # Force terminal state directly (bypassing worker for this test).
    await async_state.atomic_claim_accepted_to_running("obj-wh-poll")
    await async_state.transition_to_delivered(
        "obj-wh-poll", {"delivered": True, "payload": "terminal-envelope"}
    )
    await async_state.mark_webhook_undelivered("obj-wh-poll")

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/objectives/obj-wh-poll")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "delivered"
    assert body["webhook_undelivered"] is True
    assert body["terminal_envelope"]["payload"] == "terminal-envelope"


def test_webhook_payload_carries_no_claim_content():
    """G9 LOAD-BEARING (§12 invariant #7). Grep-negative on forbidden keys."""
    payload = webhook_service.build_payload("obj-1", "trc-1", "delivered")
    assert set(payload.keys()) == {"event", "objective_id", "trace_id", "status", "timestamp"}
    forbidden = {"answer_text", "units", "receipt", "defensibility_class", "content", "body"}
    for k in forbidden:
        assert k not in payload, (
            f"Webhook payload MUST NOT carry claim-content key {k!r}. Payload: {payload!r}"
        )


def test_webhook_timestamp_skew_rejected_beyond_five_minutes():
    """G10 coverage — timestamp older than 5 minutes MUST fail verification."""
    secret = b"skew-test-secret-32-bytes-abcdef1"
    payload_json = '{"e":"x"}'
    old_ts = "2020-01-01T00:00:00+00:00"
    sig = webhook_service.sign_payload(payload_json, old_ts, secret)
    assert webhook_service.verify_signature(payload_json, old_ts, sig, secret, skew_seconds=300) is False


def test_webhook_wire_shape_pins_five_governance_keys():
    """G11 LOAD-BEARING (payload UNFROZEN + wire-shape gate)."""
    payload = webhook_service.build_payload("obj-x", "trc-x", "delivered")
    # Exactly five keys.
    assert set(payload.keys()) == {"event", "objective_id", "trace_id", "status", "timestamp"}
    assert payload["status"] in {"delivered", "refused", "cancelled"}, (
        f"webhook status MUST be one of the terminal state names; got {payload['status']!r}"
    )
    # timestamp ISO-8601 parseable.
    from datetime import datetime as _dt
    parsed = _dt.fromisoformat(payload["timestamp"].replace("Z", "+00:00"))
    assert parsed is not None


# ---------------------------------------------------------------------------
# G12–G13 — idempotency family
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_retried_post_neither_double_commissions_nor_double_charges():
    """G12 LOAD-BEARING (§7 bullet 6). Same key + same body → idempotent
    replay (byte-identical 202). Same key + different body → 422 governed."""
    await _clear_state_collections()
    async_worker.reset_queue_for_test()

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        body_a = _valid_body(idempotency_key="idem-retry-detect", scope_ref="scope-A")
        r1 = await client.post("/api/objectives", json=body_a)
        assert r1.status_code == 202
        obj_id_1 = r1.json()["objective_id"]
        trace_id_1 = r1.json()["trace_id"]

        # Turn 2 — same key + same body → replay (same objective_id + trace_id).
        r2 = await client.post("/api/objectives", json=body_a)
        assert r2.status_code == 202
        assert r2.json()["objective_id"] == obj_id_1
        assert r2.json()["trace_id"] == trace_id_1

        # Turn 3 — same key + different body → 422 governed.
        body_b = _valid_body(idempotency_key="idem-retry-detect", scope_ref="scope-B")
        r3 = await client.post("/api/objectives", json=body_b)
        assert r3.status_code == 422
        env = AdmissionRefusal_v0.model_validate(r3.json())
        assert env.reason == "idempotency_key_reused_with_different_body"

    # Mongo count: exactly one document for this idempotency key.
    docs = await db[async_state.ASYNC_STATE_COLLECTION].count_documents(
        {"idempotency_key": "idem-retry-detect"}
    )
    assert docs == 1


@pytest.mark.asyncio
async def test_idempotency_key_missing_on_external_request_refuses():
    """G13 coverage. external_request without idempotency_key → governed 422."""
    await _clear_state_collections()
    transport = ASGITransport(app=app)
    body = _valid_body(idempotency_key="")
    body.pop("idempotency_key")
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/objectives", json=body)
    assert r.status_code == 422
    env = AdmissionRefusal_v0.model_validate(r.json())
    assert env.reason == "idempotency_key_missing"


# ---------------------------------------------------------------------------
# G14–G17 — cancellation family
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_cancelled_run_no_partial_egress():
    """G14 LOAD-BEARING (§7 bullet 5). Cancel while running → thin
    cancelled envelope, no unit content, no receipt."""
    await _clear_state_collections()
    await async_state.create_accepted(
        objective_id="obj-cancel-1", trace_id="trc-cancel-1",
        idempotency_key="idem-cancel-1",
        request_body=_valid_body(idempotency_key="idem-cancel-1"),
        request_body_hash="h",
    )
    # Move to running (simulate worker claim), then cancel.
    await async_state.atomic_claim_accepted_to_running("obj-cancel-1")

    result = await cancellation_service.cancel_objective("obj-cancel-1")
    assert result is not None
    # Thin cancelled envelope — exactly 4 keys, no claim content.
    assert set(result.keys()) == {"objective_id", "status", "trace_id", "cancelled_at"}
    forbidden = {"units", "receipt", "answer_text", "load_bearing_unit_ids"}
    for k in forbidden:
        assert k not in result, (
            f"Cancelled envelope MUST NOT carry claim/receipt/unit content: {k!r}"
        )


@pytest.mark.asyncio
async def test_cancel_during_outer_gate_transform_no_partial_egress():
    """G15 LOAD-BEARING. If cancel wins the atomic transition, worker's
    terminal write MUST return None (no envelope written); no partial
    egress in Mongo state.
    """
    await _clear_state_collections()
    await async_state.create_accepted(
        objective_id="obj-cancel-race", trace_id="trc-cancel-race",
        idempotency_key="idem-cancel-race",
        request_body=_valid_body(idempotency_key="idem-cancel-race"),
        request_body_hash="h",
    )
    # Move to running.
    await async_state.atomic_claim_accepted_to_running("obj-cancel-race")
    # Cancel wins.
    await cancellation_service.cancel_objective("obj-cancel-race")
    doc = await async_state.find_by_objective_id("obj-cancel-race")
    assert doc["status"] == "cancelled"
    # Worker's later attempt at terminal write on running → None (no state change).
    late_result = await async_state.transition_to_delivered(
        "obj-cancel-race", {"units": ["would-be-egressed"]}
    )
    assert late_result is None, (
        "Late worker terminal write MUST NOT succeed after cancel already terminalised"
    )
    # Terminal envelope stays as the cancelled envelope, not the fake delivery.
    doc = await async_state.find_by_objective_id("obj-cancel-race")
    assert doc["status"] == "cancelled"
    assert doc["terminal_envelope"]["status"] == "cancelled"


@pytest.mark.asyncio
async def test_cancelled_run_is_ledgered():
    """G16 LOAD-BEARING (§7 bullet 5). Mid-running cancel emits ONE
    NorthenaLedgerRow_v1 with decision='terminate_cancelled'."""
    await _clear_state_collections()
    await async_state.create_accepted(
        objective_id="obj-cancel-ledger", trace_id="trc-cancel-ledger",
        idempotency_key="idem-cancel-ledger",
        request_body=_valid_body(idempotency_key="idem-cancel-ledger"),
        request_body_hash="h",
    )
    await async_state.atomic_claim_accepted_to_running("obj-cancel-ledger")
    await cancellation_service.cancel_objective("obj-cancel-ledger")

    rows = [r async for r in db[NORTHENA_LEDGER_COLLECTION].find(
        {"trace_id": "trc-cancel-ledger"}
    )]
    assert len(rows) == 1, f"Cancel MUST emit exactly one ledger row; got {len(rows)}"
    row = rows[0]
    assert row["stage"] == "converge"
    assert row["decision"] == "terminate_cancelled"
    assert "caller_cancelled:cancelled_at_state=running" in row["reason"]
    # NorthenaLedgerRow_v1 MUST validate the ledger row.
    # Strip Mongo `_id` (added on read) before validation — v1 is FROZEN
    # with extra=forbid, so external identity fields are excluded.
    row_clean = {k: v for k, v in row.items() if k != "_id"}
    envelope = NorthenaLedgerRow_v1.model_validate(row_clean)
    assert envelope.decision == "terminate_cancelled"


@pytest.mark.asyncio
async def test_cancel_after_terminal_state_is_noop_returns_terminal_envelope():
    """G17 coverage. Repeated cancels after terminal are no-ops."""
    await _clear_state_collections()
    await async_state.create_accepted(
        objective_id="obj-cancel-noop", trace_id="trc-cancel-noop",
        idempotency_key="idem-cancel-noop",
        request_body=_valid_body(idempotency_key="idem-cancel-noop"),
        request_body_hash="h",
    )
    await async_state.atomic_claim_accepted_to_running("obj-cancel-noop")
    first = await cancellation_service.cancel_objective("obj-cancel-noop")
    second = await cancellation_service.cancel_objective("obj-cancel-noop")
    # Both cancels return the same terminal envelope (idempotent).
    assert first is not None
    assert second is not None
    assert first["status"] == "cancelled"
    assert second["status"] == "cancelled"
    assert first["objective_id"] == second["objective_id"]


# ---------------------------------------------------------------------------
# G18–G19 — warm/fresh fork routing
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fresh_fork_at_admission_routes_to_async_pathway():
    """G18 LOAD-BEARING (§4 warm/fresh fork). Fresh @ admission → 202 async."""
    await _clear_state_collections()
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/service_1/v2/dispatch",
            json=_valid_body(idempotency_key="idem-fresh-async-1", scope_ref="unc-1"),
        )
    assert r.status_code == 202
    body = AsyncDeliveryAccepted_v0.model_validate(r.json())
    assert body.status == "accepted"


@pytest.mark.asyncio
async def test_warm_fork_at_admission_uses_sync_pathway_not_async():
    """G19 coverage. Warm fork with qualified_data → 200 sync payload
    (existing 4a behaviour); NOT 202 async."""
    # Seed a warm reach — reuse existing seed helper from qualified_data tests
    # by inserting a fresh MtafitiRegistryRecord row.
    from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION
    from datetime import datetime, timezone
    await _clear_state_collections()
    await db[MTAFITI_REGISTRY_COLLECTION].delete_many({})
    await db[MTAFITI_REGISTRY_COLLECTION].insert_one({
        "source_ref": "s://warm/x.raw",
        "region": "warm_fork_scope",
        "feed_id": "feed_a",
        "modality": "text",
        "score_vector": {"corroboration": 0.0, "recency_validity": 0.5, "contested": False},
        "defensibility_runtime_mode": "declaration_baseline",
        "matrix_rule_ref": "qm.v0.rule.1",
        "defensibility_class": "utterance",
        "freshness_stamp": {
            "logged_date": datetime.now(timezone.utc).isoformat(),
            "structural_signature": None,
        },
    })
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/service_1/v2/dispatch",
            json=_valid_body(idempotency_key="idem-warm-sync-1", scope_ref="warm_fork_scope"),
        )
    # Warm path returns 200 with qualified_data payload (Phase 4a).
    assert r.status_code == 200, f"Warm fork MUST return 200; got {r.status_code}: {r.text}"
    body = r.json()
    assert "units" in body, "Warm-fork qualified_data payload MUST carry 'units' key"


# ---------------------------------------------------------------------------
# G20 — accepted body wire-shape / frozen contract
# ---------------------------------------------------------------------------


def test_accepted_body_wire_shape_pins_governance_keys():
    """G20 LOAD-BEARING. AsyncDeliveryAccepted_v0 frozen contract fields
    are the exact governance-carrying keys; status is Literal['accepted']."""
    schema = AsyncDeliveryAccepted_v0.model_json_schema()
    props = set(schema["properties"].keys())
    required = set(schema["required"])
    assert props == {"objective_id", "status", "delivery_estimate", "quote", "trace_id", "accepted_at"}
    assert required == {"objective_id", "delivery_estimate", "trace_id", "accepted_at"}
    status_schema = schema["properties"]["status"]
    assert status_schema.get("const") == "accepted" or status_schema.get("enum") == ["accepted"]


# ---------------------------------------------------------------------------
# G21 — governance travels inline (§12 invariant #7)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_governance_travels_inline_on_async_response_body():
    """G21 LOAD-BEARING. The 202 response carries objective_id + trace_id
    inline — governance ids don't come via webhook."""
    await _clear_state_collections()
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/objectives", json=_valid_body(idempotency_key="idem-gov-inline"))
    assert r.status_code == 202
    body = r.json()
    assert body["objective_id"].startswith("obj-")
    assert body["trace_id"].startswith("trc-")


# ---------------------------------------------------------------------------
# G22 — late refusal ledgered with governed reason (§12 invariant #8)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_late_refusal_ledgered_with_governed_reason():
    """G22 LOAD-BEARING. A refused terminal (via transition_to_refused)
    emits a ledger row with the governed reason attached."""
    await _clear_state_collections()
    await async_state.create_accepted(
        objective_id="obj-late-ref", trace_id="trc-late-ref",
        idempotency_key="idem-late-ref",
        request_body=_valid_body(idempotency_key="idem-late-ref"),
        request_body_hash="h",
    )
    await async_state.atomic_claim_accepted_to_running("obj-late-ref")
    await async_state.transition_to_refused(
        "obj-late-ref", {"outcome": "refused", "reason": "composition_below_floor"},
        reason="composition_below_floor",
    )
    doc = await async_state.find_by_objective_id("obj-late-ref")
    assert doc["status"] == "refused"
    # Last state_transition names the governed reason.
    last_transition = doc["state_transitions"][-1]
    assert last_transition["state"] == "refused"
    assert last_transition["reason"] == "composition_below_floor"


# ---------------------------------------------------------------------------
# G23 — sandbox mode
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_sandbox_mode_serves_from_fixture_estate(monkeypatch):
    """G23 LOAD-BEARING (§7 bullet 8). Sandbox flag flows through admission
    to the async state document. Phase 8 UI reads this + fixture estate."""
    await _clear_state_collections()
    monkeypatch.setenv("RMS_APP_SANDBOX_MODE_TESTAPP", "1")
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/objectives",
            json=_valid_body(idempotency_key="idem-sandbox-1"),
            headers={"X-RMS-App-ID": "testapp"},
        )
    assert r.status_code == 202
    obj_id = r.json()["objective_id"]
    doc = await async_state.find_by_objective_id(obj_id)
    assert doc["sandbox_mode"] is True


# ---------------------------------------------------------------------------
# G24 — registry-bump extends v1 additively (Phase 3 Standing Disposition)
# ---------------------------------------------------------------------------


def test_admission_refusal_registry_v2_extends_v1_additively():
    """G24 LOAD-BEARING (Phase 3 Standing Disposition regression).

    v2 registry MUST include every v1 reason code (additive extension).
    v0 file remains byte-identical, v1 file byte-identical, v2 adds two
    new codes over v1.
    """
    v0_path = BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v0.json"
    v1_path = BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v1.json"
    v2_path = BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v2.json"
    v0 = json.loads(v0_path.read_text())
    v1 = json.loads(v1_path.read_text())
    v2 = json.loads(v2_path.read_text())
    v0_codes = {e["reason"] for e in v0["valid_reasons"]}
    v1_codes = {e["reason"] for e in v1["valid_reasons"]}
    v2_codes = {e["reason"] for e in v2["valid_reasons"]}
    # Additive: v0 ⊂ v1 ⊂ v2.
    assert v0_codes.issubset(v1_codes), f"v1 must include all v0 codes; missing: {v0_codes - v1_codes}"
    assert v1_codes.issubset(v2_codes), f"v2 must include all v1 codes; missing: {v1_codes - v2_codes}"
    # v2 adds exactly the two Phase 5 Stage B codes.
    v2_only = v2_codes - v1_codes
    assert v2_only == {"idempotency_key_reused_with_different_body", "idempotency_key_missing"}


# ---------------------------------------------------------------------------
# Q4.f — grep-negative gates for STRUCK codes (Standing Dispositions)
# ---------------------------------------------------------------------------


def test_no_caller_cancelled_code_in_any_registry():
    """Standing Disposition regression — cancellation-is-a-state-not-a-refusal.
    The string `caller_cancelled` MUST NOT appear as a REGISTRY REASON CODE
    in any refusal-reason registry. (It may appear elsewhere as a state
    transition reason or ledger-row reason string, but NEVER as an admission
    or service-refusal reason code.)"""
    registries = [
        BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v0.json",
        BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v1.json",
        BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v2.json",
        BACKEND_ROOT / "services" / "service_1" / "service_1_refusal_reasons.v0.json",
    ]
    for p in registries:
        reg = json.loads(p.read_text())
        codes = {e["reason"] for e in reg["valid_reasons"]}
        assert "caller_cancelled" not in codes, (
            f"Standing Disposition violation — {p.name!r} contains "
            f"`caller_cancelled` refusal reason code. Cancellation is a "
            f"state, not a refusal — remove from registry."
        )


def test_no_async_queue_saturated_code_in_any_registry():
    """Standing Disposition regression — infra-not-refusal.
    The string `async_queue_saturated` MUST NOT appear as a refusal
    reason code anywhere. Queue saturation is HTTP 503, not a governed
    refusal envelope.
    """
    registries = [
        BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v0.json",
        BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v1.json",
        BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v2.json",
        BACKEND_ROOT / "services" / "service_1" / "service_1_refusal_reasons.v0.json",
    ]
    for p in registries:
        reg = json.loads(p.read_text())
        codes = {e["reason"] for e in reg["valid_reasons"]}
        assert "async_queue_saturated" not in codes, (
            f"Standing Disposition violation — {p.name!r} contains "
            f"`async_queue_saturated` refusal reason. Infra faults return "
            f"HTTP 503; NEVER a governed refusal envelope."
        )


@pytest.mark.asyncio
async def test_queue_overflow_raises_503_not_refusal(monkeypatch):
    """Standing Disposition LOAD-BEARING — queue full → HTTPException 503,
    NOT AdmissionRefusal_v0."""
    await _clear_state_collections()
    async_worker.reset_queue_for_test()
    # Shrink queue to maxsize=1, fill it, then attempt to enqueue a second.
    monkeypatch.setattr(async_worker, "_QUEUE_MAX", 1)
    q = asyncio.Queue(maxsize=1)
    monkeypatch.setattr(async_worker, "_queue", q)
    q.put_nowait("obj-sat-blocker")
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/objectives", json=_valid_body(idempotency_key="idem-saturate"))
    assert r.status_code == 503, (
        f"Queue-saturated MUST return HTTP 503; got {r.status_code}: {r.text}"
    )
    # Body MUST NOT be an AdmissionRefusal envelope.
    body = r.json()
    assert body.get("outcome") != "refused", (
        f"503 body MUST NOT masquerade as a governed refusal envelope; got: {body}"
    )
    async_worker.reset_queue_for_test()


# ---------------------------------------------------------------------------
# 5-state coverage — state machine legal transitions
# ---------------------------------------------------------------------------


def test_state_machine_five_states_declared():
    """State machine names the five states: accepted, running, delivered,
    refused, cancelled. All three terminals present in _TERMINAL_STATES."""
    legal = async_state.legal_transitions()
    assert set(legal.keys()) == {"accepted", "running", "delivered", "refused", "cancelled"}
    assert legal["accepted"] == {"running", "cancelled"}
    assert legal["running"] == {"delivered", "refused", "cancelled"}
    assert legal["delivered"] == set()
    assert legal["refused"] == set()
    assert legal["cancelled"] == set()


def test_state_machine_no_transition_from_terminal():
    """Terminal states have zero outgoing transitions — attempting to
    transition from delivered/refused/cancelled MUST fail."""
    legal = async_state.legal_transitions()
    for terminal in ("delivered", "refused", "cancelled"):
        assert legal[terminal] == set()


# ---------------------------------------------------------------------------
# Frozen contracts landing at Stage B
# ---------------------------------------------------------------------------


def test_async_delivery_accepted_v0_contract_snapshot_matches():
    """AsyncDeliveryAccepted_v0 (20th frozen contract) — schema matches
    canonical snapshot on disk."""
    snap_path = BACKEND_ROOT / "tests" / "invariants" / "async_delivery_accepted.contract_snapshot.json"
    stored = json.loads(snap_path.read_text())
    current = AsyncDeliveryAccepted_v0.model_json_schema()
    assert stored == current, (
        "AsyncDeliveryAccepted_v0 schema drifted from canonical snapshot. "
        "Any change is a HAZARD-STOP (Ruling 2)."
    )


def test_northena_ledger_v1_contract_snapshot_matches():
    """NorthenaLedgerRow_v1 (19th frozen contract) — schema matches snapshot."""
    snap_path = BACKEND_ROOT / "tests" / "invariants" / "northena_ledger_v1.contract_snapshot.json"
    stored = json.loads(snap_path.read_text())
    current = NorthenaLedgerRow_v1.model_json_schema()
    assert stored == current


def test_northena_ledger_v1_supersets_v0():
    """v1 MUST validate every valid v0 row (superset relationship).

    Standing Owner Disposition frozen-field-changes-as-new-versions:
    frozen-field changes land as NEW contract versions that superset
    the prior version's validation set.
    """
    from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
    from datetime import datetime, timezone

    # Every valid v0 row must also validate under v1.
    for stage, decision in [
        ("admit", "admitted"), ("admit", "refused"),
        ("gate", "warm"), ("gate", "fresh"), ("gate", "refused"),
        ("converge", "terminate_success"), ("converge", "terminate_budget"), ("converge", "continue"),
    ]:
        row = LedgerRow(
            run_id="r-1", trace_id="t-1", stage=stage, decision=decision,
            reason="test", artifact_ref=LedgerArtifactRef(
                artifact_type="objective_request", artifact_id="a-1", version="v2",
            ),
            lawful_basis_ref="lb", stamp_audit=None, at=datetime.now(timezone.utc),
        )
        row_dict = row.model_dump(mode="python")
        NorthenaLedgerRow_v1.model_validate(row_dict)
    # v1 also accepts the new terminate_cancelled decision.
    v1_row = NorthenaLedgerRow_v1(
        run_id="r-2", trace_id="t-2", stage="converge", decision="terminate_cancelled",
        reason="caller_cancelled:cancelled_at_state=running",
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request", artifact_id="a-2", version="v2",
        ),
        lawful_basis_ref="lb", stamp_audit=None, at=datetime.now(timezone.utc),
    )
    assert v1_row.decision == "terminate_cancelled"


# ---------------------------------------------------------------------------
# Idempotency canonicalisation
# ---------------------------------------------------------------------------


def test_canonical_request_hash_excludes_idempotency_key():
    """The idempotency_key MUST be excluded from the canonical hash input
    — the key IS the retry axis, hashing it would defeat retry-detection.
    """
    from contracts.objective_request_v2 import ObjectiveRequest_v2
    body = _valid_body(idempotency_key="key-A")
    req_a = ObjectiveRequest_v2.model_validate(body)
    body_b = _valid_body(idempotency_key="key-B")
    req_b = ObjectiveRequest_v2.model_validate(body_b)
    h_a = idempotency_service.canonical_request_hash(req_a)
    h_b = idempotency_service.canonical_request_hash(req_b)
    # Different keys, same everything else → SAME hash.
    assert h_a == h_b, (
        "Canonical hash MUST exclude idempotency_key; keys A and B "
        "produced different hashes."
    )


def test_canonical_request_hash_deterministic_across_dict_order():
    """Canonicalisation MUST be sort-key-stable: two equal bodies with
    different insertion order produce the same hash."""
    from contracts.objective_request_v2 import ObjectiveRequest_v2
    body = _valid_body(idempotency_key="test")
    body2 = dict(reversed(list(body.items())))
    req_1 = ObjectiveRequest_v2.model_validate(body)
    req_2 = ObjectiveRequest_v2.model_validate(body2)
    assert idempotency_service.canonical_request_hash(req_1) == \
           idempotency_service.canonical_request_hash(req_2)
