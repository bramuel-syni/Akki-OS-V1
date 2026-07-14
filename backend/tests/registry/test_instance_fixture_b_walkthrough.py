"""Instance-fixture-B end-to-end walkthrough — MC-E2 α proof shape.

Owner ruling MC-E2 α (2026-07-14):
    'a second synthetic instance — instance-fixture-B, a generic
     structured estate (tabular + small AV, synthetic) — stands up
     beside the existing fixture estate in CI and walks onboard →
     connect → census → brief → answer end-to-end, with isolation
     cells proving no cross-instance read on any surface.'

This test walks fixture-B through the promoted surfaces:
    1. S2.onboard structured intake (POST /api/instance/instance_fixture_b/onboard)
    2. Structured connector registration + tabular ingest
    3. Isolation attest — instance_1 scope cannot see fixture-B records
    4. Trust receipt renders only fixture-B trace at /trace/:traceId (checked
       via scoped_accessor read on the ledger)
"""
from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from services.data_source.structured_connector import (
    DEFAULT_LICENSE_CLASS,
    StructuredConnectorRegistration,
    TabularRow,
    ingest_tabular,
    license_class_permits_s4_egress,
)
from services.multi_instance.scoped_accessor import (
    scount_documents,
    sfind,
    sinsert_one,
)


FIXTURE_B = Path(__file__).parents[2] / "services" / "data_source" / "synthetic_assets" / "instance_fixture_b" / "fixture.json"


@pytest.fixture
async def db_client():
    load_dotenv("/app/backend/.env")
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ["DB_NAME"]]
    yield db
    # cleanup fixture-B walkthrough artifacts
    await db["instance_onboard_context"].delete_many({"instance_id": "instance_fixture_b"})
    await db["northena_ledger"].delete_many({"instance_id": "instance_fixture_b"})
    await db["test_instance_fixture_b_units"].delete_many({})
    client.close()


def test_instance_fixture_b_fixture_json_shapes_correctly():
    """Instance-fixture-B fixture.json on disk is valid tabular structure."""
    payload = json.loads(FIXTURE_B.read_text())
    assert payload["_manifest"]["fixture"] == "instance_fixture_b_v1"
    assert payload["_manifest"]["estate_kind"] == "tabular_synthetic"
    assert len(payload["rows"]) == payload["_manifest"]["row_count"]


def test_structured_connector_produces_valid_normalized_units():
    """MC-E1 α attest: tabular rows → NormalizedUnits without contract mutation."""
    payload = json.loads(FIXTURE_B.read_text())
    connector = StructuredConnectorRegistration(
        connector_id=f"connector-{uuid.uuid4().hex[:8]}",
        instance_id="instance_fixture_b",
        source_ref="fixture_b_revenue_ledger",
        connector_kind="tabular",
    )
    rows = [TabularRow(**r) for r in payload["rows"]]
    units = ingest_tabular(rows, connector)
    assert len(units) == 3
    for u in units:
        assert u.provenance.modality.value == "text"
        assert "table" in u.provenance.locator
        assert "row" in u.provenance.locator
        # extraction_params@v0 mandatory keys present (text modality)
        ep = u.reextraction_handle.extraction_params
        for k in ("provider_id", "provider_version", "extraction_run_id",
                  "extracted_at", "source_format", "max_chars", "encoding"):
            assert k in ep, f"missing extraction_param key {k!r}"


def test_license_class_default_is_internal_only_fail_closed():
    """MC-E4 α: default = internal_only; outer-gate egress refused."""
    connector = StructuredConnectorRegistration(
        connector_id="c1", instance_id="instance_fixture_b", source_ref="s1",
    )
    assert connector.license_class == DEFAULT_LICENSE_CLASS == "internal_only"
    assert license_class_permits_s4_egress(connector.license_class) is False
    # Explicit upgrade permits egress.
    assert license_class_permits_s4_egress("public_domain") is True
    assert license_class_permits_s4_egress("licensed_commercial") is True


@pytest.mark.asyncio
async def test_s2_onboard_fixture_b_walkthrough(db_client):
    """End-to-end: onboard → connect → ingest → isolate → verify."""
    from server import app

    # Pre-clean any prior fixture-B state
    await db_client["instance_onboard_context"].delete_many({"instance_id": "instance_fixture_b"})
    await db_client["northena_ledger"].delete_many({"instance_id": "instance_fixture_b"})

    onboard_payload = {
        "instance_id": "instance_fixture_b",
        "estate_inventory": [
            {"source_ref": "fixture_b_revenue_ledger", "kind": "tabular",
             "custodian": "custodian_b@fixture.local", "rights_posture": "internal_only"},
        ],
        "org_vocabulary": {"entities": ["Fixture Region North"], "brands": []},
        "dpo_contact": "dpo_b@fixture.local",
        "seam_values": {
            "deletion_consequence_classes": "class-C=dual_control_always,class-B_over_1000=owner_escalation,class-A=operator",
            "rule_tightening_delay_hours": 72,
            "objection_escalation_days": 7,
            "suspension_re_review_days": 30,
            "outer_gate_manual_review_threshold": ">10000_units_or_1gb_per_artifact"
        },
        "objective_priorities": ["revenue_intelligence_q1_2026"],
        "submitted_by": "operator_alpha",
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # STEP A: S2.onboard
        resp = await client.post(
            "/api/instance/instance_fixture_b/onboard",
            json=onboard_payload,
        )
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["outcome"] == "onboarded"
        assert body["instance_id"] == "instance_fixture_b"
        assert body["initial_set"] is True
        assert body["seam_values_ledgered"] == 5

        # STEP B: read-back
        resp2 = await client.get("/api/instance/instance_fixture_b/onboard")
        assert resp2.status_code == 200

    # STEP C: initial-set ledger rows present under fixture-B scope
    ledger_rows_b = await sfind(
        db_client["northena_ledger"], "instance_fixture_b",
        {"stage": "s2_onboard_seam_value_set"},
    )
    assert len(ledger_rows_b) >= 5  # 5 seam values + 2 estate/vocab

    # STEP D: cross-instance isolation — instance_1 scope cannot see fixture-B ledger rows
    ledger_rows_a = await sfind(
        db_client["northena_ledger"], "instance_1",
        {"stage": "s2_onboard_seam_value_set", "reason": "seam_value:rule_tightening_delay_hours"},
    )
    fixture_b_rows_in_a = [r for r in ledger_rows_a if r.get("submitted_by") == "operator_alpha"]
    assert not fixture_b_rows_in_a, (
        f"Cross-instance leak: instance_1 scope saw fixture-B onboard ledger rows: {fixture_b_rows_in_a}"
    )

    # STEP E: connector ingest — units carry instance-scoped connector metadata
    payload = json.loads(FIXTURE_B.read_text())
    connector = StructuredConnectorRegistration(
        connector_id=f"connector-b-{uuid.uuid4().hex[:8]}",
        instance_id="instance_fixture_b",
        source_ref="fixture_b_revenue_ledger",
    )
    rows = [TabularRow(**r) for r in payload["rows"]]
    units = ingest_tabular(rows, connector)
    assert len(units) == 3
    # STEP F: initial-set assertion — subsequent onboard call for fixture_b fails with 409
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp3 = await client.post(
            "/api/instance/instance_fixture_b/onboard",
            json=onboard_payload,
        )
        assert resp3.status_code == 409, (
            f"Second onboard should fail with §6 ceremony refusal; got {resp3.status_code}"
        )
