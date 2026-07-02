"""G5a LOAD-BEARING GATE CONDITION 1 — cross-engine trace correlation.

One `trace_id` resolves artifacts from every engine boundary that
participated in a run. This is the acceptance bar for G5a.

Two synthetic flows exercised:
  1. Service 1 v1 Day-Zero run — resolves Northena Ledger + Mtafiti
     Registry + Targeta MiningPlan + Service 1 marker.
  2. Solva pipeline direct run — resolves Northena Converge (absorbed)
     + Solva SolvaTrace.

Combined: an engine-boundary universe of `{northena_ledger, solva,
targeta, mtafiti, service_1}`. The trace-lens must resolve the
appropriate subset for each flow.
"""
from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from httpx import ASGITransport
import uuid

from contracts.five_rings import (
    DefensibilityClass,
    DefensibilityRing,
    Modality,
    NormalizedUnit,
    ProvenanceRing,
    ReextractionHandleRing,
    RelationalRing,
    ScoreVector,
    SignalRing,
)
from contracts.northena_ledger import LedgerArtifactRef
from server import app
from services.northena import converge as northena_converge
from services.service_1 import service as service_1_service
from services.solva_depth.interfaces import FloorSpec
from services.solva_depth.pipeline import run_solva
from tests.invariants._ep_v0_fixtures import ep_v0


FIXTURE_PATH = (
    Path(__file__).parent.parent.parent / "services" / "data_source"
    / "synthetic_assets" / "rms_adversarial_v1" / "fixture.json"
)


def _async_client() -> httpx.AsyncClient:
    """Async client bound to the app in the SAME event loop as Motor (§conftest).

    Using `httpx.AsyncClient(transport=ASGITransport(app))` avoids the
    `TestClient` sync-bridge that owns its own event loop and would collide
    with the session-scoped async Motor fixture.
    """
    return httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


def _fact_unit() -> NormalizedUnit:
    return NormalizedUnit(
        unit_id="corr-fact-1",
        provenance=ProvenanceRing(
            source_ref="synthetic://correlation-test/fact.raw",
            modality=Modality.TEXT,
            locator={}, speaker_or_author="anchor",
            context=json.dumps({
                "feed_id": "citizen_tv_news",
                "logged_date": "2026-07-01T12:00:00Z",
                "structural_signature": "0123456789abcdef",
                "author_labels": {
                    "claim_genre": "news_anchor_read",
                    "source_standing": "primary_recorded",
                    "contested_status": "uncontested",
                },
            }),
        ),
        signal=SignalRing(dimensions={}, depth_judged=False),
        relational=RelationalRing(),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer="synthetic://correlation-test/fact.raw",
            model_id="test-model", model_version="v0",
            extraction_params=ep_v0(Modality.TEXT),
        ),
        defensibility=DefensibilityRing(
            defensibility_class=DefensibilityClass.FACT,
            score_vector=ScoreVector(),
            matrix_rule_ref="news_anchor_read.primary_recorded",
            runtime_mode="declaration_baseline",
        ),
    )


# ----- Flow A: Service 1 run — Northena + Mtafiti + Targeta + Service 1 -----
@pytest.mark.asyncio
async def test_service_1_flow_resolves_all_four_engines():
    """One trace_id from a Service 1 run must resolve to Ledger rows
    (Northena engine) + MiningPlan (Targeta engine) + Registry records
    (Mtafiti engine) + Service 1 marker."""
    fx = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    units = [NormalizedUnit.model_validate(u) for u in fx["units"][:3]]
    result = await service_1_service.run(
        units, objective_text="g5a corr service1 objective",
        artifact_id="g5a-corr-service1", artifact_version="v0",
        lawful_basis="dpa-test", floor=DefensibilityClass.NON_FACTUAL,
    )
    trace_id = result["trace_id"]

    async with _async_client() as c:
        resp = await c.get(f"/api/northena/trace/{trace_id}")
    assert resp.status_code == 200, resp.json()
    body = resp.json()

    assert body["trace_id"] == trace_id
    assert trace_id
    assert body["run_ids"] == [result["run_id"]], (
        f"expected one run_id ({result['run_id']}); got {body['run_ids']}"
    )

    expected_engines = {"northena_ledger", "targeta", "mtafiti", "service_1"}
    actual_engines = set(body["engines_touched"])
    missing = expected_engines - actual_engines
    assert not missing, (
        f"GATE CONDITION 1 — missing engines from correlation: {missing}. "
        f"Got: {sorted(actual_engines)}"
    )

    # Depth checks per engine:
    # Northena: at least 3 rows (admit + gate + converge)
    assert len(body["ledger_rows"]) >= 3, (
        f"expected >=3 ledger rows (admit/gate/converge); got {len(body['ledger_rows'])}"
    )
    stages = [r["stage"] for r in body["ledger_rows"]]
    for expected_stage in ("admit", "gate", "converge"):
        assert expected_stage in stages, f"missing stage row: {expected_stage}"

    # Targeta: MiningPlan resolved and matches the run's plan_id
    assert len(body["mining_plans"]) == 1
    assert body["mining_plans"][0]["plan_id"] == result["mining_plan_id"]

    # Mtafiti: Registry records resolved for each ordered target
    assert len(body["registry_records"]) >= 1, (
        "expected at least one Mtafiti Registry record resolved via plan targets"
    )

    # Temporal ordering: ledger `at` timestamps are non-decreasing (§7.2)
    at_stamps = [r["at"] for r in body["ledger_rows"]]
    assert at_stamps == sorted(at_stamps), (
        "temporal ordering violated in ledger_rows"
    )


# ----- Flow B: Solva direct — Northena Converge + Solva engine artifacts -----
@pytest.mark.asyncio
async def test_solva_flow_resolves_northena_and_solva_engines():
    """Directly invoke Solva pipeline + absorb_solva_trace under a shared
    trace_id; assert the lens resolves both engines.
    """
    unit = _fact_unit()
    unique_trace = f"g5a-corr-solva-{uuid.uuid4().hex[:8]}"
    unique_run = f"g5a-corr-solva-run-{uuid.uuid4().hex[:8]}"
    trace = run_solva(
        trace_id=unique_trace,
        run_id=unique_run,
        question="does the anchor read confirm the outage?",
        units=[unit],
        floor=FloorSpec(minimum_class=DefensibilityClass.NON_FACTUAL),
    )
    row = await northena_converge.absorb_solva_trace(
        run_id=unique_run,
        trace_id=trace.trace_id,
        trace_dict=trace.to_dict(),
        artifact_ref=LedgerArtifactRef(
            artifact_type="portfolio_mandate",
            artifact_id="g5a-corr-solva-artifact", version="v0",
        ),
        lawful_basis_ref="dpa-test",
    )
    assert row.stage == "converge"

    async with _async_client() as c:
        resp = await c.get(f"/api/northena/trace/{trace.trace_id}")
    assert resp.status_code == 200, resp.json()
    body = resp.json()

    assert "northena_ledger" in body["engines_touched"]
    assert "solva" in body["engines_touched"], (
        f"GATE CONDITION 1 — Solva engine artifact missing under trace_id "
        f"that carried a SolvaTrace stamp_audit. Got engines: {body['engines_touched']}"
    )

    # Solva depth check: 5 reasoning stages (Solva §8) resolved by name.
    # Trace also carries a `layer_c_converge` pre-stage → total ≥ 5.
    assert len(body["solva_traces"]) == 1
    solva_trace = body["solva_traces"][0]
    stage_names = [s.get("stage_name") for s in solva_trace.get("stages", [])]
    expected_reasoning_stages = {"frame", "candidate", "tension", "probability", "reflection"}
    missing_stages = expected_reasoning_stages - set(stage_names)
    assert not missing_stages, (
        f"Solva §8 reasoning stages missing from trace: {missing_stages}. "
        f"Got stage_names={stage_names}"
    )
    assert len(solva_trace.get("stages", [])) >= 5, (
        f"expected ≥5 reasoning stages (Solva §8); got {len(solva_trace.get('stages', []))}"
    )
    assert solva_trace.get("computed_class") in ("fact", "utterance", "non_factual")


# ----- Negative case + Northena §7.2 run_id ↔ trace_id semantics -----------
@pytest.mark.asyncio
async def test_trace_lens_404_carries_structured_error():
    async with _async_client() as c:
        resp = await c.get("/api/northena/trace/g5a-does-not-exist")
    assert resp.status_code == 404
    body = resp.json()
    detail = body.get("detail") or {}
    assert detail.get("reason") == "trace_id_not_found"
    assert detail.get("trace_id") == "g5a-does-not-exist"


@pytest.mark.asyncio
async def test_trace_lens_400_carries_structured_error():
    async with _async_client() as c:
        resp = await c.get("/api/northena/trace/%20")
    assert resp.status_code == 400
    body = resp.json()
    detail = body.get("detail") or {}
    assert detail.get("reason") == "malformed_trace_id"


@pytest.mark.asyncio
async def test_run_id_trace_id_semantics_northena_7_2():
    """Northena §7.2: `run_id: str  # one run has one closed Ledger`,
    `trace_id: str  # joins to units + the three trace lenses`.

    Semantics we assert at G4 shipping state:
      * A single run_id yields a set of Ledger rows sharing that run_id.
      * A single trace_id may span multiple stages within one run
        (admit/gate/converge in Service 1). Multiple trace_ids may share
        a run_id (spec-permitted; per-unit traces inside one run).
      * The lens response `run_ids` field surfaces the unique run_ids
        observed for the queried trace_id — for a Service 1 run this
        is exactly one.
    """
    fx = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    units = [NormalizedUnit.model_validate(u) for u in fx["units"][:2]]
    result = await service_1_service.run(
        units, objective_text="g5a corr semantics objective",
        artifact_id="g5a-corr-semantics", artifact_version="v0",
        lawful_basis="dpa-test", floor=DefensibilityClass.NON_FACTUAL,
    )
    resp = None
    async with _async_client() as c:
        resp = await c.get(f"/api/northena/trace/{result['trace_id']}")
    body = resp.json()
    # At G4, Service 1 uses one trace_id across admit/gate/converge — so
    # the lens sees one run_id under the trace_id.
    assert body["run_ids"] == [result["run_id"]]
    # Every row under this trace_id has the same run_id (§7.2 correlation)
    for row in body["ledger_rows"]:
        assert row["run_id"] == result["run_id"]
        assert row["trace_id"] == result["trace_id"]


# ----- Contract snapshot integrity ------------------------------------------
def test_trace_lens_envelope_contract_frozen():
    """Snapshot-freeze the TraceLensEnvelope schema."""
    from contracts.trace_lens import TraceLensEnvelope
    expected = json.loads((Path(__file__).parent
                           / "trace_lens_envelope.contract_snapshot.json"
                           ).read_text(encoding="utf-8"))
    actual = TraceLensEnvelope.model_json_schema()
    assert json.dumps(actual, indent=2, sort_keys=True) == \
           json.dumps(expected, indent=2, sort_keys=True), (
        "TraceLensEnvelope schema drifted; re-bless snapshot in review if intentional."
    )


def test_lift_manifest_envelope_contract_frozen():
    from contracts.lift_manifest_response import LiftManifestEnvelope
    expected = json.loads((Path(__file__).parent
                           / "lift_manifest_envelope.contract_snapshot.json"
                           ).read_text(encoding="utf-8"))
    actual = LiftManifestEnvelope.model_json_schema()
    assert json.dumps(actual, indent=2, sort_keys=True) == \
           json.dumps(expected, indent=2, sort_keys=True), (
        "LiftManifestEnvelope schema drifted; re-bless snapshot in review if intentional."
    )
