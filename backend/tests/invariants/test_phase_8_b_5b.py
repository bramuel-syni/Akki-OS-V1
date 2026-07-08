"""Phase 8 Stage B-5b — Compliance rulebook-write UI + B-4 read-only retrofit.

Matrix (Amendment H, 2026-07-07 — Owner Rulings B5b-E1..B5b-E5 pre-carried):

§A. `data_class_registry.v2.json` — v1→v2 additive bump (Ruling B5b-E4).
§B. `disclosure_types.v0.json` — B5b-E3 (γ) constrained-str registry.
§C. Rulebook writer endpoints × auth × posture matrix (B5b-R1 + B5b-G4).
§D. B5b-G1 `test_tightening_change_is_unilateral_and_delayed`.
§E. B5b-G2 `test_loosening_change_requires_countersign`.
§F. B5b-G3 `test_compliance_rules_readonly_on_admin_console`.
§G. B5b-G4 `test_every_rule_write_emits_ledger_row_with_consequence_class`.
§H. B5b-E4 `test_no_admin_initiated_compliance_pending_survives_retrofit`.
§I. 409 anti-rule static scan on B-5b diff.
§J. Retrofit voiding + ledger emit assertion.
"""
from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from core import db
from server import app
from services.auth import jwt_service, user_store
from services.compliance.deletion_ledger import VALID_DATA_CLASSES
from services.compliance.rulebook_writes import (
    RulebookWriteError,
    validate_disclosure_type,
)

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_COMPLIANCE_DIR = _BACKEND_ROOT / "services" / "compliance"


# ────────────────────────────────────────────────────────────────────
# Fixtures
# ────────────────────────────────────────────────────────────────────


async def _make_token(roles):
    email = f"b5b_{uuid.uuid4().hex[:8]}@rms.test"
    identity = await user_store.create_user(
        email=email,
        password_plaintext="Passw0rd!Passw0rd!",
        roles=roles,
        name="b5btester",
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
async def _isolate_b5b_state():
    """Clean checker_requests + ledger rows between tests."""
    await db["checker_requests"].delete_many({})
    marker = {
        "stamp_audit.data_class": {
            "$in": [
                "retrofit_authority_voided",
                "unclassified",
            ]
        }
    }
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(marker)
    yield
    await db["checker_requests"].delete_many({})
    await db[NORTHENA_LEDGER_COLLECTION].delete_many(marker)


# ════════════════════════════════════════════════════════════════════
# §A — data_class_registry v1→v2 additive bump (Ruling B5b-E4)
# ════════════════════════════════════════════════════════════════════


def test_a1_data_class_registry_v2_exists():
    p = _COMPLIANCE_DIR / "data_class_registry.v2.json"
    assert p.exists()


def test_a2_registry_v2_preserves_v0_v1_classes():
    """Append-only bump."""
    for c in [
        "authorized_deletion",
        "unclassified",
        "countersigned_rule_change",
        "tightening_effective",
        "tightening_objected",
        "owner_suspended_tightening",
    ]:
        assert c in VALID_DATA_CLASSES


def test_a3_registry_v2_appends_retrofit_authority_voided():
    """Ruling B5b-E4 new class."""
    assert "retrofit_authority_voided" in VALID_DATA_CLASSES


def test_a4_v2_marks_landed_at_version_v2():
    p = _COMPLIANCE_DIR / "data_class_registry.v2.json"
    doc = json.loads(p.read_text())
    by_name = {e["data_class"]: e for e in doc["valid_data_classes"]}
    assert by_name["retrofit_authority_voided"]["landed_at_version"] == "v2"


# ════════════════════════════════════════════════════════════════════
# §B — disclosure_types.v0.json registry + constrained-str (B5b-E3 γ)
# ════════════════════════════════════════════════════════════════════


def test_b1_disclosure_types_registry_exists():
    p = _COMPLIANCE_DIR / "disclosure_types.v0.json"
    assert p.exists()


def test_b2_disclosure_types_registry_contains_three_v0_entries():
    p = _COMPLIANCE_DIR / "disclosure_types.v0.json"
    doc = json.loads(p.read_text())
    names = {e["disclosure_type"] for e in doc["valid_disclosure_types"]}
    assert names == {"k_anonymity", "l_diversity", "dp_budget"}


def test_b3_validate_disclosure_type_accepts_registered():
    assert validate_disclosure_type("k_anonymity") == "k_anonymity"
    assert validate_disclosure_type("l_diversity") == "l_diversity"
    assert validate_disclosure_type("dp_budget") == "dp_budget"


def test_b4_validate_disclosure_type_rejects_unknown():
    with pytest.raises(RulebookWriteError):
        validate_disclosure_type("differential_privacy_epsilon")


# ════════════════════════════════════════════════════════════════════
# §C — Rulebook writer endpoints × auth × posture matrix
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_c1_disclosure_thresholds_no_token_401():
    async with _client() as c:
        r = await c.post("/api/compliance/disclosure_thresholds", json={})
    assert r.status_code == 401


@pytest.mark.anyio
async def test_c2_disclosure_thresholds_wrong_role_403():
    token, _ = await _make_token(["operator"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/disclosure_thresholds",
            headers={"Authorization": f"Bearer {token}"},
            json={"disclosure_type": "k_anonymity", "from_value": 3, "to_value": 5},
        )
    assert r.status_code == 403


@pytest.mark.anyio
async def test_c3_disclosure_thresholds_dpo_ok_returns_202_pending():
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/disclosure_thresholds",
            headers={"Authorization": f"Bearer {token}"},
            json={"disclosure_type": "k_anonymity", "from_value": 3, "to_value": 5},
        )
    assert r.status_code == 202
    body = r.json()
    assert body["state"] == "pending_counter_sign"
    assert body["consequence_class"] == "dual_control"
    assert body["rule_class"] == "disclosure_thresholds"


@pytest.mark.anyio
async def test_c4_disclosure_thresholds_unknown_type_400():
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/disclosure_thresholds",
            headers={"Authorization": f"Bearer {token}"},
            json={"disclosure_type": "invalid_type", "from_value": 1, "to_value": 2},
        )
    assert r.status_code == 400
    assert r.json()["reason"] == "malformed_payload"


@pytest.mark.anyio
async def test_c5_lawful_basis_registry_dpo_ok_returns_202_pending():
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/lawful_basis_registry",
            headers={"Authorization": f"Bearer {token}"},
            json={"from_value_ref": "consent", "to_value_ref": "legitimate_interest"},
        )
    assert r.status_code == 202
    assert r.json()["consequence_class"] == "dual_control"


@pytest.mark.anyio
async def test_c6_source_standing_table_dpo_ok_returns_202_pending_delay():
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/source_standing_table",
            headers={"Authorization": f"Bearer {token}"},
            json={"from_value_ref": "vetted", "to_value_ref": "provisional"},
        )
    assert r.status_code == 202
    body = r.json()
    assert body["consequence_class"] == "tightening_unilateral"
    assert body["state"] == "pending_delay"


@pytest.mark.anyio
async def test_c7_lawful_basis_registry_no_token_401():
    async with _client() as c:
        r = await c.post("/api/compliance/lawful_basis_registry", json={})
    assert r.status_code == 401


@pytest.mark.anyio
async def test_c8_source_standing_wrong_role_403():
    token, _ = await _make_token(["operator"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/source_standing_table",
            headers={"Authorization": f"Bearer {token}"},
            json={"from_value_ref": "a", "to_value_ref": "b"},
        )
    assert r.status_code == 403


@pytest.mark.anyio
async def test_c9_lawful_basis_malformed_body_400():
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/lawful_basis_registry",
            headers={"Authorization": f"Bearer {token}"},
            json={"missing": "from_and_to"},
        )
    assert r.status_code == 400


# ════════════════════════════════════════════════════════════════════
# §D/E — B5b-G1 / B5b-G2 dual/unilateral behavior
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_b5bg1_tightening_change_is_unilateral_and_delayed():
    """B5b-G1: tightening_unilateral rule classes go pending_delay."""
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/source_standing_table",
            headers={"Authorization": f"Bearer {token}"},
            json={"from_value_ref": "vetted", "to_value_ref": "provisional"},
        )
    assert r.status_code == 202
    assert r.json()["state"] == "pending_delay"
    assert r.json()["consequence_class"] == "tightening_unilateral"


@pytest.mark.anyio
async def test_b5bg2_loosening_change_requires_countersign():
    """B5b-G2: dual_control rule classes go pending_counter_sign."""
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/disclosure_thresholds",
            headers={"Authorization": f"Bearer {token}"},
            json={"disclosure_type": "k_anonymity", "from_value": 5, "to_value": 3},
        )
    assert r.status_code == 202
    assert r.json()["state"] == "pending_counter_sign"


# ════════════════════════════════════════════════════════════════════
# §F — B5b-G3: compliance rules read-only on Admin console (RT-G1)
# ════════════════════════════════════════════════════════════════════


def test_b5bg3_rt_g1_no_write_route_for_compliance_classes_on_master_admin():
    """RT-G1 / B5b-G3: master_admin router does NOT expose any write route
    that accepts a compliance rule_class. Static scan on the file."""
    ma = (_BACKEND_ROOT / "routers" / "master_admin.py").read_text()
    for rc in [
        "retention_windows",
        "disclosure_thresholds",
        "lawful_basis_registry",
        "source_standing_table",
    ]:
        assert f'rule_class="{rc}"' not in ma, (
            f"RT-G1 violation: master_admin router references write for "
            f"compliance rule_class={rc}"
        )


# ════════════════════════════════════════════════════════════════════
# §G — B5b-G4: every rule write emits a ledger row with consequence_class
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_b5bg4_disclosure_write_emits_row_with_consequence_class():
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/disclosure_thresholds",
            headers={"Authorization": f"Bearer {token}"},
            json={"disclosure_type": "k_anonymity", "from_value": 3, "to_value": 5},
        )
    request_id = r.json()["request_id"]
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.request_id": request_id,
         "stamp_audit.rule_class": "disclosure_thresholds"}
    )
    assert row is not None
    assert row["stamp_audit"]["consequence_class"] in {"dual_control", "tightening_unilateral"}
    assert row["stamp_audit"]["data_class"] in VALID_DATA_CLASSES


@pytest.mark.anyio
async def test_b5bg4_source_standing_write_emits_row_with_consequence_class():
    token, _ = await _make_token(["dpo"])
    async with _client() as c:
        r = await c.post(
            "/api/compliance/source_standing_table",
            headers={"Authorization": f"Bearer {token}"},
            json={"from_value_ref": "vetted", "to_value_ref": "provisional"},
        )
    request_id = r.json()["request_id"]
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one(
        {"stamp_audit.request_id": request_id,
         "stamp_audit.rule_class": "source_standing_table"}
    )
    assert row is not None
    assert row["stamp_audit"]["consequence_class"] == "tightening_unilateral"


# ════════════════════════════════════════════════════════════════════
# §H — B5b-E4 named gate + retrofit voiding logic
# ════════════════════════════════════════════════════════════════════


@pytest.mark.anyio
async def test_b5b_e4_no_admin_initiated_compliance_pending_survives_retrofit():
    """Owner Ruling B5b-E4 named gate. Trivially green today (null
    population). Permanent LB thereafter."""
    from services.compliance.retrofit_voiding import void_admin_initiated_compliance_pending
    # Seed one admin-initiated pending compliance-rule request (non-null population).
    from services.checker import state_machine
    await state_machine.initiate(
        rule_class="retention_windows",
        from_value_ref="v0",
        to_value_ref="v1",
        initiator_id="admin@rms.test",
        initiator_role="admin",  # admin capacity — the population that gets voided
    )
    # Verify at least one pending admin-initiated compliance-rule request exists.
    pre = await db["checker_requests"].count_documents({
        "state": {"$in": ["pending_counter_sign", "pending_delay"]},
        "initiator_role": "admin",
        "rule_class": {"$in": [
            "retention_windows", "disclosure_thresholds",
            "lawful_basis_registry", "source_standing_table",
        ]},
    })
    assert pre >= 1
    voided = await void_admin_initiated_compliance_pending()
    assert len(voided) >= 1
    # Post-retrofit: no admin-initiated compliance-rule pending items remain.
    post = await db["checker_requests"].count_documents({
        "state": {"$in": ["pending_counter_sign", "pending_delay"]},
        "initiator_role": "admin",
        "rule_class": {"$in": [
            "retention_windows", "disclosure_thresholds",
            "lawful_basis_registry", "source_standing_table",
        ]},
    })
    assert post == 0


@pytest.mark.anyio
async def test_b5b_e4_retrofit_emits_retrofit_authority_voided_ledger_row():
    """Ruling B5b-E4: each voided item emits a ledger row with data_class=
    retrofit_authority_voided + reason=retrofit_authority_transfer."""
    from services.compliance.retrofit_voiding import void_admin_initiated_compliance_pending
    from services.checker import state_machine
    r = await state_machine.initiate(
        rule_class="disclosure_thresholds",
        from_value_ref="k_anonymity=5",
        to_value_ref="k_anonymity=3",
        initiator_id="legacy_admin@rms.test",
        initiator_role="admin",
    )
    await void_admin_initiated_compliance_pending()
    row = await db[NORTHENA_LEDGER_COLLECTION].find_one({
        "stamp_audit.data_class": "retrofit_authority_voided",
        "stamp_audit.request_id": r.request_id,
    })
    assert row is not None
    assert row["stamp_audit"]["reason"] == "retrofit_authority_transfer"
    assert row["stamp_audit"]["rule_class"] == "disclosure_thresholds"
    assert row["stamp_audit"]["data_class"] in VALID_DATA_CLASSES


@pytest.mark.anyio
async def test_b5b_e4_null_population_trivially_green():
    """Owner-noted: trivially green on today's null population."""
    from services.compliance.retrofit_voiding import void_admin_initiated_compliance_pending
    voided = await void_admin_initiated_compliance_pending()
    assert voided == []


# ════════════════════════════════════════════════════════════════════
# §I — Standing state-conflict anti-rule (409 grep)
# ════════════════════════════════════════════════════════════════════


def test_i1_no_409_in_b_5b_diff():
    diff_paths = [
        _COMPLIANCE_DIR / "rulebook_writes.py",
        _COMPLIANCE_DIR / "retrofit_voiding.py",
    ]
    pattern = re.compile(r"\b409\b")
    for p in diff_paths:
        content = p.read_text()
        assert not pattern.search(content), f"409 in {p}"
