"""Phase 8 Seam 3 Sub-stage 3 — §8 consequence-class checker.

Matrix (Amendment G, 2026-07-07 restructured — Owner Rulings 1-7 pre-carried):

§A. `data_class_registry.v1.json` — v0→v1 bump (Ruling 4).
§B. Consequence-class registry + rule-class map + effective_delay_seconds.
§C. State machine — initiate() for both consequence classes.
§D. State machine — countersign() (dual_control path, CK-G1).
§E. State machine — advance_delay() (tightening_unilateral path).
§E-supp. State machine — suspend() (Ruling 3: the only halt action).
§H. Ruling 3 — object() annotates but NEVER halts.
§K. `POST /api/checker/initiate` endpoint auth × posture.
§L. `POST /api/checker/countersign/{id}` endpoint auth × state.
§M. `POST /api/checker/object/{id}` endpoint auth × state.
§M-supp. `POST /api/master_admin/tightening/suspend` endpoint auth × state.
§N. `GET /api/checker/pending` role filter (Ruling 2 capacity-role).
§O. `test_retention_loosening_write_requires_administration_countersign`.
§O-supp. `test_every_retention_write_emits_ledger_row_with_consequence_class` (Ruling 6).
§P. 409 anti-rule static scan on Sub-stage 3 diff.
§R. Data-class LB gate extension (Ruling 1(ii)) over 4 new rule-change classes.
"""
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from core import db
from server import app
from services.auth import jwt_service, user_store
from services.checker import state_machine
from services.checker.consequence_classes import (
    CONSEQUENCE_CLASS_DUAL_CONTROL,
    CONSEQUENCE_CLASS_TIGHTENING_UNILATERAL,
    InvalidConsequenceClassError,
    validate_consequence_class,
)
from services.checker.effective_delay import (
    consequence_class_for,
    effective_delay_seconds,
    reset_cache_for_tests,
)
from services.checker.rule_change_request import (
    STATE_EFFECTIVE,
    STATE_PENDING_COUNTER_SIGN,
    STATE_PENDING_DELAY,
    STATE_SUSPENDED,
)
from services.compliance.deletion_ledger import VALID_DATA_CLASSES

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_RETENTION_DIR = _BACKEND_ROOT / "services" / "compliance"


# ────────────────────────────────────────────────────────────────────
# Fixtures
# ────────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def _isolate_retention_dir():
    """Wipe retention.vN.json (N>=1) before and after each test to avoid
    cross-test bleed on the file-versioned retention config."""
    def _cleanup():
        for p in _RETENTION_DIR.glob("retention.v*.json"):
            stem = p.stem
            try:
                v = int(stem.split(".v", 1)[1])
            except (IndexError, ValueError):
                continue
            if v >= 1:
                p.unlink(missing_ok=True)
    _cleanup()
    yield
    _cleanup()


async def _make_token(roles):
    email = f"tester_{uuid.uuid4().hex[:8]}@rms.test"
    identity = await user_store.create_user(
        email=email,
        password_plaintext="Passw0rd!Passw0rd!",
        roles=roles,
        name="tester",
    )
    return (
        jwt_service.create_access_token(
            identity.user_id, identity.email, identity.roles, []
        ),
        email,
    )


def _client():
    return AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )


@pytest.fixture(autouse=True)
async def _isolate_checker_state():
    """Clean checker_requests + rule-change ledger rows between tests."""
    reset_cache_for_tests()
    await db["checker_requests"].delete_many({})
    marker = {
        "stamp_audit.data_class": {
            "$in": [
                "countersigned_rule_change",
                "tightening_effective",
                "tightening_objected",
                "owner_suspended_tightening",
            ]
        }
    }
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(marker)
    yield
    await db["checker_requests"].delete_many({})
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(marker)
    reset_cache_for_tests()


# ════════════════════════════════════════════════════════════════════
# §A — data_class_registry v0→v1 bump (Ruling 4)
# ════════════════════════════════════════════════════════════════════


def test_a1_data_class_registry_v1_exists():
    p = _BACKEND_ROOT / "services" / "compliance" / "data_class_registry.v1.json"
    assert p.exists(), "v1 registry file must exist per Ruling 4"


def test_a2_data_class_registry_v1_valid_json_with_version_marker():
    p = _BACKEND_ROOT / "services" / "compliance" / "data_class_registry.v1.json"
    doc = json.loads(p.read_text())
    assert doc["version"] == "v1"
    assert doc["prior_version"] == "v0"


def test_a3_v1_appends_four_new_rule_change_classes():
    """Ruling 4: countersigned_rule_change + tightening_effective +
    tightening_objected + owner_suspended_tightening."""
    expected_new = {
        "countersigned_rule_change",
        "tightening_effective",
        "tightening_objected",
        "owner_suspended_tightening",
    }
    assert expected_new.issubset(VALID_DATA_CLASSES)


def test_a4_v1_preserves_v0_classes():
    """Append-only per Ruling 4."""
    assert "authorized_deletion" in VALID_DATA_CLASSES
    assert "unclassified" in VALID_DATA_CLASSES


def test_a5_v1_new_classes_have_v1_landed_marker():
    p = _BACKEND_ROOT / "services" / "compliance" / "data_class_registry.v1.json"
    doc = json.loads(p.read_text())
    by_name = {e["data_class"]: e for e in doc["valid_data_classes"]}
    for name in [
        "countersigned_rule_change",
        "tightening_effective",
        "tightening_objected",
        "owner_suspended_tightening",
    ]:
        assert by_name[name]["landed_at_version"] == "v1"


# ════════════════════════════════════════════════════════════════════
# §B — consequence_class.v0.json registry
# ════════════════════════════════════════════════════════════════════


def test_b1_consequence_class_registry_exists():
    p = _BACKEND_ROOT / "services" / "compliance" / "consequence_class.v0.json"
    assert p.exists()


def test_b2_rule_class_map_retention_windows_is_dual_control():
    assert consequence_class_for("retention_windows") == CONSEQUENCE_CLASS_DUAL_CONTROL


def test_b3_rule_class_map_source_standing_is_tightening_unilateral():
    assert (
        consequence_class_for("source_standing_table")
        == CONSEQUENCE_CLASS_TIGHTENING_UNILATERAL
    )


def test_b4_effective_delay_positive_int():
    assert effective_delay_seconds() > 0


def test_b5_validate_consequence_class_rejects_unknown():
    with pytest.raises(InvalidConsequenceClassError):
        validate_consequence_class("owner_veto")


def test_b6_validate_consequence_class_accepts_registered():
    assert validate_consequence_class("dual_control") == "dual_control"
    assert (
        validate_consequence_class("tightening_unilateral") == "tightening_unilateral"
    )


# ════════════════════════════════════════════════════════════════════
# §C — state_machine.initiate()
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_c1_initiate_dual_control_returns_pending_counter_sign():
    r = await state_machine.initiate(
        rule_class="retention_windows",
        from_value_ref="v0",
        to_value_ref="v1",
        initiator_id="dpo@rms.test",
        initiator_role="compliance",
    )
    assert r.state == STATE_PENDING_COUNTER_SIGN
    assert r.consequence_class == CONSEQUENCE_CLASS_DUAL_CONTROL
    assert not r.idempotent_hit


@pytest.mark.anyio
async def test_c2_initiate_tightening_unilateral_returns_pending_delay():
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    assert r.state == STATE_PENDING_DELAY
    assert r.consequence_class == CONSEQUENCE_CLASS_TIGHTENING_UNILATERAL


@pytest.mark.anyio
async def test_c3_idempotent_initiate_returns_same_request_id(_isolate_checker_state):
    r1 = await state_machine.initiate(
        rule_class="retention_windows",
        from_value_ref="v0",
        to_value_ref="v1",
        initiator_id="dpo@rms.test",
        initiator_role="compliance",
    )
    r2 = await state_machine.initiate(
        rule_class="retention_windows",
        from_value_ref="v0",
        to_value_ref="v1",
        initiator_id="dpo@rms.test",
        initiator_role="compliance",
    )
    assert r1.request_id == r2.request_id
    assert r2.idempotent_hit


# ════════════════════════════════════════════════════════════════════
# §D — state_machine.countersign() (dual_control, CK-G1 LB)
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_d1_countersign_transitions_to_effective(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="retention_windows",
        from_value_ref="v0",
        to_value_ref="v1",
        initiator_id="dpo@rms.test",
        initiator_role="compliance",
    )
    req = await state_machine.countersign(
        request_id=r.request_id,
        checker_id="admin@rms.test",
        checker_role="admin",
    )
    assert req.state == STATE_EFFECTIVE
    assert req.effective_at is not None


@pytest.mark.anyio
async def test_d2_same_identity_countersign_refused(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="retention_windows",
        from_value_ref="v0",
        to_value_ref="v1",
        initiator_id="dpo@rms.test",
        initiator_role="compliance",
    )
    with pytest.raises(state_machine.InvalidTransitionError):
        await state_machine.countersign(
            request_id=r.request_id,
            checker_id="dpo@rms.test",  # SAME as initiator
            checker_role="compliance",
        )


# ════════════════════════════════════════════════════════════════════
# §E — state_machine.advance_delay() (tightening_unilateral)
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_e1_advance_delay_before_expiry_stays_pending(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    req = await state_machine.advance_delay(
        request_id=r.request_id, now=datetime.now(timezone.utc)
    )
    assert req.state == STATE_PENDING_DELAY


@pytest.mark.anyio
async def test_e2_advance_delay_after_expiry_becomes_effective(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    future = datetime.now(timezone.utc) + timedelta(hours=2)
    req = await state_machine.advance_delay(request_id=r.request_id, now=future)
    assert req.state == STATE_EFFECTIVE


@pytest.mark.anyio
async def test_e3_advance_delay_after_objection_still_becomes_effective(
    _isolate_checker_state,
):
    """Ruling 3: object() annotates but NEVER halts. Tightening proceeds
    to effective at delay expiry UNCONDITIONALLY."""
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    # Object.
    await state_machine.object_to_tightening(
        request_id=r.request_id,
        objector_id="dpo@rms.test",
        objector_role="compliance",
        reason="Concern raised by DPO.",
    )
    # Advance past delay.
    future = datetime.now(timezone.utc) + timedelta(hours=2)
    req = await state_machine.advance_delay(request_id=r.request_id, now=future)
    assert req.state == STATE_EFFECTIVE, (
        "Ruling 3: objection MUST NOT halt tightening; must reach effective."
    )
    assert len(req.objections) == 1


@pytest.mark.anyio
async def test_e4_idempotent_initiate_post_effective_is_new_change(
    _isolate_checker_state,
):
    """Ruling 3: post-effect re-initiate is a NEW change with own window."""
    r1 = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    future = datetime.now(timezone.utc) + timedelta(hours=2)
    await state_machine.advance_delay(request_id=r1.request_id, now=future)
    r2 = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    assert r2.request_id != r1.request_id, (
        "Ruling 3: post-effect re-initiate must be a NEW change."
    )
    assert not r2.idempotent_hit


# ════════════════════════════════════════════════════════════════════
# §E-supp — state_machine.suspend() (Ruling 3 halt action)
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_esup1_suspend_on_pending_delay_halts(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    req = await state_machine.suspend(
        request_id=r.request_id,
        suspended_by_id="owner@rms.test",
        suspended_by_role="admin",
        reason="Owner halt.",
    )
    assert req.state == STATE_SUSPENDED
    assert req.prior_state == STATE_PENDING_DELAY


@pytest.mark.anyio
async def test_esup2_suspend_after_effective_disallowed(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    future = datetime.now(timezone.utc) + timedelta(hours=2)
    await state_machine.advance_delay(request_id=r.request_id, now=future)
    with pytest.raises(state_machine.InvalidTransitionError):
        await state_machine.suspend(
            request_id=r.request_id,
            suspended_by_id="owner@rms.test",
            suspended_by_role="admin",
            reason="too late",
        )


@pytest.mark.anyio
async def test_esup3_suspend_idempotent_no_op_on_suspended(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    await state_machine.suspend(
        request_id=r.request_id,
        suspended_by_id="owner@rms.test",
        suspended_by_role="admin",
        reason="first.",
    )
    req = await state_machine.suspend(
        request_id=r.request_id,
        suspended_by_id="owner@rms.test",
        suspended_by_role="admin",
        reason="second.",
    )
    assert req.state == STATE_SUSPENDED
    # First-suspend reason preserved (idempotent no-op).
    assert req.suspend_reason == "first."


@pytest.mark.anyio
async def test_esup4_suspend_advance_delay_after_suspend_remains_suspended(
    _isolate_checker_state,
):
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    await state_machine.suspend(
        request_id=r.request_id,
        suspended_by_id="owner@rms.test",
        suspended_by_role="admin",
        reason="halt",
    )
    future = datetime.now(timezone.utc) + timedelta(hours=2)
    req = await state_machine.advance_delay(request_id=r.request_id, now=future)
    assert req.state == STATE_SUSPENDED, (
        "Ruling 3: suspend is terminal — no auto-transition to effective."
    )


# ════════════════════════════════════════════════════════════════════
# §H — object() Ruling 3 annotation-not-halt
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_h1_object_annotates_state_unchanged(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    req = await state_machine.object_to_tightening(
        request_id=r.request_id,
        objector_id="dpo@rms.test",
        objector_role="compliance",
        reason="Reason A.",
    )
    assert req.state == STATE_PENDING_DELAY, "Ruling 3: state MUST NOT change on object()"
    assert len(req.objections) == 1


@pytest.mark.anyio
async def test_h2_object_disallowed_on_dual_control(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="retention_windows",
        from_value_ref="v0",
        to_value_ref="v1",
        initiator_id="dpo@rms.test",
        initiator_role="compliance",
    )
    with pytest.raises(state_machine.InvalidTransitionError):
        await state_machine.object_to_tightening(
            request_id=r.request_id,
            objector_id="admin@rms.test",
            objector_role="admin",
            reason="nope",
        )


@pytest.mark.anyio
async def test_h3_multi_objections_accumulate(_isolate_checker_state):
    r = await state_machine.initiate(
        rule_class="source_standing_table",
        from_value_ref="a",
        to_value_ref="b",
        initiator_id="admin@rms.test",
        initiator_role="admin",
    )
    await state_machine.object_to_tightening(
        request_id=r.request_id,
        objector_id="dpo1@rms.test",
        objector_role="compliance",
        reason="1st",
    )
    req = await state_machine.object_to_tightening(
        request_id=r.request_id,
        objector_id="dpo2@rms.test",
        objector_role="compliance",
        reason="2nd",
    )
    assert len(req.objections) == 2
    assert req.state == STATE_PENDING_DELAY


# ════════════════════════════════════════════════════════════════════
# §K — POST /api/checker/initiate endpoint
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_k1_initiate_no_token_401():
    async with _client() as c:
        r = await c.post("/api/checker/initiate", json={})
    assert r.status_code == 401


@pytest.mark.anyio
async def test_k2_initiate_operator_role_403():
    token, _ = await _make_token(["operator"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "rule_class": "retention_windows",
                "from_value_ref": "v0",
                "to_value_ref": "v1",
            },
        )
    assert r.status_code == 403
    assert r.json()["reason"] == "auth_scope_insufficient"


@pytest.mark.anyio
async def test_k3_initiate_dpo_ok_returns_pending_counter_sign():
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "rule_class": "retention_windows",
                "from_value_ref": "v0",
                "to_value_ref": "v1",
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["state"] == "pending_counter_sign"
    assert body["consequence_class"] == "dual_control"


@pytest.mark.anyio
async def test_k4_initiate_unknown_rule_class_400():
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "rule_class": "nonexistent",
                "from_value_ref": "x",
                "to_value_ref": "y",
            },
        )
    assert r.status_code == 400


# ════════════════════════════════════════════════════════════════════
# §L — POST /api/checker/countersign/{id}
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_l1_countersign_by_symmetric_role_effects_and_ledger():
    dpo_token, dpo_email = await _make_token(["dpo"])
    admin_token, admin_email = await _make_token(["admin"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {dpo_token}"},
            json={
                "rule_class": "retention_windows",
                "from_value_ref": "v0",
                "to_value_ref": "v1",
            },
        )
        request_id = r.json()["request_id"]
        r2 = await c.post(
            f"/api/checker/countersign/{request_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
    assert r2.status_code == 200
    body = r2.json()
    assert body["state"] == "effective"
    # CK-U1 middle-dot binding copy (E7 strict).
    assert "\u00b7" in body["commit_line"]
    # Ledger row emitted.
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.request_id": request_id, "stamp_audit.data_class": "countersigned_rule_change"}
    )
    assert row is not None
    # Ruling 2 capacity roles.
    assert row["stamp_audit"]["initiator_role"] == "compliance"
    assert row["stamp_audit"]["checker_role"] == "admin"


@pytest.mark.anyio
async def test_l2_countersign_pending_delay_refused():
    admin_token, _ = await _make_token(["admin"])
    dpo_token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "rule_class": "source_standing_table",
                "from_value_ref": "a",
                "to_value_ref": "b",
            },
        )
        request_id = r.json()["request_id"]
        r2 = await c.post(
            f"/api/checker/countersign/{request_id}",
            headers={"Authorization": f"Bearer {dpo_token}"},
        )
    assert r2.status_code == 403


# ════════════════════════════════════════════════════════════════════
# §M — POST /api/checker/object/{id}
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_m1_object_annotates_state_unchanged_response_body():
    admin_token, _ = await _make_token(["admin"])
    dpo_token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "rule_class": "source_standing_table",
                "from_value_ref": "a",
                "to_value_ref": "b",
            },
        )
        request_id = r.json()["request_id"]
        r2 = await c.post(
            f"/api/checker/object/{request_id}",
            headers={"Authorization": f"Bearer {dpo_token}"},
            json={"reason": "objection reason"},
        )
    assert r2.status_code == 200
    body = r2.json()
    assert body["state"] == "pending_delay"  # UNCHANGED per Ruling 3
    assert body["owner_escalated"] is True


# ════════════════════════════════════════════════════════════════════
# §M-supp — POST /api/master_admin/tightening/suspend endpoint (Ruling 3)
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_msup1_suspend_no_token_401():
    async with _client() as c:
        r = await c.post("/api/master_admin/tightening/suspend", json={})
    assert r.status_code == 401


@pytest.mark.anyio
async def test_msup2_suspend_dpo_role_denied():
    """dpo role does NOT have master_admin authority; admin=super-role
    is accepted. So we test the negative path using dpo."""
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/master_admin/tightening/suspend",
            headers={"Authorization": f"Bearer {token}"},
            json={"request_id": "rc-x", "reason": "y"},
        )
    assert r.status_code == 403


@pytest.mark.anyio
async def test_msup3_suspend_master_admin_ok_halts_pending_delay():
    ma_token, ma_email = await _make_token(["master_admin"])
    admin_token, _ = await _make_token(["admin"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "rule_class": "source_standing_table",
                "from_value_ref": "a",
                "to_value_ref": "b",
            },
        )
        request_id = r.json()["request_id"]
        r2 = await c.post(
            "/api/master_admin/tightening/suspend",
            headers={"Authorization": f"Bearer {ma_token}"},
            json={"request_id": request_id, "reason": "Owner halt."},
        )
    assert r2.status_code == 200
    body = r2.json()
    assert body["state"] == "suspended"
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.data_class": "owner_suspended_tightening",
         "stamp_audit.request_id": request_id}
    )
    assert row is not None


@pytest.mark.anyio
async def test_msup4_suspend_unknown_request_404():
    ma_token, _ = await _make_token(["master_admin"])
    async with _client() as c:
        r = await c.post(
            "/api/master_admin/tightening/suspend",
            headers={"Authorization": f"Bearer {ma_token}"},
            json={"request_id": "rc-nonexistent-99", "reason": "halt"},
        )
    assert r.status_code == 404


# ════════════════════════════════════════════════════════════════════
# §N — GET /api/checker/pending (Ruling 2 capacity-role filter)
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_n1_pending_dual_control_appears_for_countersigner_role_only():
    dpo_token, _ = await _make_token(["dpo"])
    admin_token, _ = await _make_token(["admin"])
    async with _client() as c:
        await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {dpo_token}"},
            json={
                "rule_class": "retention_windows",
                "from_value_ref": "v0",
                "to_value_ref": "v1",
            },
        )
        # Countersigner (admin capacity) sees it.
        r_admin = await c.get(
            "/api/checker/pending?role=admin",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        # Initiator role (compliance) does NOT see it as countersign work.
        r_dpo = await c.get(
            "/api/checker/pending?role=compliance",
            headers={"Authorization": f"Bearer {dpo_token}"},
        )
    assert r_admin.status_code == 200
    assert r_admin.json()["count"] == 1
    assert r_dpo.json()["count"] == 0


# ════════════════════════════════════════════════════════════════════
# §O — retention loosening now requires countersign (CK-B3 symmetry)
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_o1_retention_loosening_write_requires_administration_countersign():
    """Sub-stage 3 CK-B3 gate replacing E2 loosening-disabled."""
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 30}},
        )
        r = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 365}},
        )
    assert r.status_code == 202
    body = r.json()
    assert body["outcome"] == "pending_counter_sign"
    assert body["consequence_class"] == "dual_control"


# ════════════════════════════════════════════════════════════════════
# §O-supp — Ruling 6 new gate: every retention write emits ledger row
# with stamp_audit.consequence_class present and registry-valid.
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_osup1_every_retention_write_emits_ledger_row_with_consequence_class():
    """Ruling 6 named gate."""
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        # Setting-from-unset (null → int).
        r1 = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 90}},
        )
        assert r1.status_code == 200
        # Tightening (int decrease).
        r2 = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 60}},
        )
        assert r2.status_code == 200
        # Loosening — routes to checker (202).
        r3 = await c.post(
            "/api/compliance/retention_config",
            headers={"Authorization": f"Bearer {token}"},
            json={"ledger_row": {"window_days": 180}},
        )
        assert r3.status_code == 202
    # Assert all 3 writes emitted a ledger row with consequence_class.
    rows = await db[NORTHENA_LEDGER_COLLECTION].find(
        {"stamp_audit.consequence_class": {"$exists": True},
         "stamp_audit.held_class": "retention_windows"}
    ).to_list(length=100)
    assert len(rows) >= 3, f"expected >=3 retention writes with consequence_class stamp_audit; got {len(rows)}"
    for row in rows:
        cc = row["stamp_audit"]["consequence_class"]
        # Registry-valid per consequence_class.v0.json values.
        assert cc in {"dual_control", "tightening_unilateral"}


# ════════════════════════════════════════════════════════════════════
# §P — 409 anti-rule static scan (full-anti-rule reactivated per §5.2)
# ════════════════════════════════════════════════════════════════════


def test_p1_no_409_in_sub_stage_3_diff():
    """Sub-stage 3 files must not contain the token 409."""
    diff_paths = [
        _BACKEND_ROOT / "services" / "checker",
        _BACKEND_ROOT / "routers" / "checker.py",
    ]
    pattern = re.compile(r"\b409\b")
    for base in diff_paths:
        if base.is_file():
            content = base.read_text()
            assert not pattern.search(content), f"409 in {base}"
        else:
            for f in base.rglob("*.py"):
                content = f.read_text()
                assert not pattern.search(content), f"409 in {f}"


# ════════════════════════════════════════════════════════════════════
# §R — Data-class LB extension over new rule-change classes (Ruling 1(ii))
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_r1_countersigned_rule_change_row_carries_registry_valid_data_class():
    """The existing Sub-stage 2 LB gate covers this via the shared
    emit_deletion_ledger_row path — Ruling 1(ii)."""
    dpo_token, _ = await _make_token(["dpo"])
    admin_token, _ = await _make_token(["admin"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {dpo_token}"},
            json={
                "rule_class": "retention_windows",
                "from_value_ref": "v0",
                "to_value_ref": "v1",
            },
        )
        req_id = r.json()["request_id"]
        await c.post(
            f"/api/checker/countersign/{req_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.request_id": req_id,
         "stamp_audit.data_class": "countersigned_rule_change"}
    )
    assert row is not None
    assert row["stamp_audit"]["data_class"] in VALID_DATA_CLASSES


@pytest.mark.anyio
async def test_r2_tightening_objected_row_carries_registry_valid_data_class():
    admin_token, _ = await _make_token(["admin"])
    dpo_token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "rule_class": "source_standing_table",
                "from_value_ref": "a",
                "to_value_ref": "b",
            },
        )
        req_id = r.json()["request_id"]
        await c.post(
            f"/api/checker/object/{req_id}",
            headers={"Authorization": f"Bearer {dpo_token}"},
            json={"reason": "test"},
        )
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.request_id": req_id,
         "stamp_audit.data_class": "tightening_objected"}
    )
    assert row is not None
    assert row["stamp_audit"]["data_class"] in VALID_DATA_CLASSES


@pytest.mark.anyio
async def test_r3_owner_suspended_row_carries_registry_valid_data_class():
    admin_token, _ = await _make_token(["admin"])
    ma_token, _ = await _make_token(["master_admin"])
    async with _client() as c:
        r = await c.post(
            "/api/checker/initiate",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "rule_class": "source_standing_table",
                "from_value_ref": "a",
                "to_value_ref": "b",
            },
        )
        req_id = r.json()["request_id"]
        await c.post(
            "/api/master_admin/tightening/suspend",
            headers={"Authorization": f"Bearer {ma_token}"},
            json={"request_id": req_id, "reason": "halt"},
        )
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.request_id": req_id,
         "stamp_audit.data_class": "owner_suspended_tightening"}
    )
    assert row is not None
    assert row["stamp_audit"]["data_class"] in VALID_DATA_CLASSES
