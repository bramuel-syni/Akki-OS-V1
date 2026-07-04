"""§6.1 qualified-data selection tests — Phase 4a.

Houses gates 5, 6, 7, 9, and 11 per Stage A dispatch:
  5. `test_license_class_selection_filters_registry_reads`
  6. `test_license_class_absence_below_floor_route`
  7. `test_qualified_data_standard_hard_input_filter` (v3 §6.1.6)
  9. `test_qualified_data_per_claim_provenance_intact` (v3 §6.1.3)
 11. `test_admission_refusal_registry_v1_extends_v0_additively` (Condition B2)

Seeds Mtafiti Registry rows directly (mirrors the pattern in
`test_feasibility_honesty_under_absence.py`) and drives the v2 dispatch
route via ASGITransport for wire-shape verification.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
import pytest
from httpx import ASGITransport

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION
from core import db
from server import app


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


async def _clear_registry() -> None:
    await db[MTAFITI_REGISTRY_COLLECTION].delete_many({})


async def _seed_row(
    *,
    source_ref: str,
    region: str,
    feed_id: str,
    klass: str,
    days_ago: int = 0,
) -> None:
    """Populate one MtafitiRegistryRecord row.

    region != feed_id is allowed here — tests need to decouple reach
    (region) from license-class mapping (feed_id).
    """
    logged = (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()
    await db[MTAFITI_REGISTRY_COLLECTION].insert_one({
        "source_ref": source_ref,
        "region": region,
        "feed_id": feed_id,
        "sensitivity": "standard",
        "defensibility_measure": {
            "source_standing": "accountable",
            "attachment": 0.0,
            "corroboration": 0.0,
            "recency_validity": 0.5,
            "contested": False,
        },
        "defensibility_runtime_mode": "declaration_baseline",
        "matrix_rule_ref": "qm.v0.rule.1",
        "defensibility_class": klass,
        "freshness_stamp": {
            "logged_date": logged,
            "structural_signature": None,
        },
    })


def _base_body(
    *,
    scope_refs,
    minimum_class: str = "utterance",
    commissioner: str = "operator_internal",
) -> dict:
    """Minimal ObjectiveRequest_v2 wire body for warm-fork qualified-data."""
    return {
        "entry": "external_request",
        "reach": {"scope_refs": scope_refs, "exclusions": [], "depth": "baseline"},
        "output": {
            "form": "qualified_data",
            "consumer": "person",
            "grain": "per_claim",
            "standard": {"minimum_class": minimum_class},
        },
        "envelope": {
            "lawful_basis": "test",
            "done_condition": "test",
            "budget": "test",
            "scope_ceiling": "test",
            "commissioner": commissioner,
            "committed_at": "2026-07-03T12:00:00+00:00",
        },
    }


# ---------------------------------------------------------------------------
# Gate 5 — license_class filter over mixed-class Registry
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_license_class_selection_filters_registry_reads():
    """Mixed feed_ids across one reach; commissioner derives editorial_use;
    only citizen_tv_news (editorial_use) survives the license-class axis."""
    await _clear_registry()
    # Two editorial_use rows (feed_id=citizen_tv_news) + two syndication
    # rows (feed_id=ktn_news), all in region=mixed_region.
    await _seed_row(
        source_ref="s://a/e1.raw", region="mixed_region",
        feed_id="citizen_tv_news", klass="fact",
    )
    await _seed_row(
        source_ref="s://a/e2.raw", region="mixed_region",
        feed_id="citizen_tv_news", klass="utterance",
    )
    await _seed_row(
        source_ref="s://a/s1.raw", region="mixed_region",
        feed_id="ktn_news", klass="fact",
    )
    await _seed_row(
        source_ref="s://a/s2.raw", region="mixed_region",
        feed_id="ktn_news", klass="utterance",
    )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_base_body(
                scope_refs=["mixed_region"],
                minimum_class="utterance",
                commissioner="operator_internal",  # derives to editorial_use
            ),
        )
    assert resp.status_code == 200, (
        f"expected 200 qualified-data warm success; got {resp.status_code}"
        f"\nbody: {resp.text}"
    )
    body = resp.json()
    assert body["unit_count"] == 2, (
        f"license filter should keep only citizen_tv_news editorial_use rows; "
        f"got unit_count={body['unit_count']}"
    )
    # Every surviving unit's identifier field is pseudonymised (hex) — the
    # source_ref in-list membership check is done via feed_id generalisation.
    # feed_id was generalised via outer_gate transform to broadcast_news.
    for unit in body["units"]:
        assert unit["feed_id"] == "broadcast_news", (
            f"citizen_tv_news feed_id generalised via outer-gate — expected "
            f"'broadcast_news'; got {unit['feed_id']!r}"
        )


# ---------------------------------------------------------------------------
# Gate 6 — license-class axis empty → license_class_unavailable
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_license_class_absence_below_floor_route():
    """Populated Registry with a reach whose feed_ids do NOT match the
    derived license class → AdmissionRefusal_v0(reason=license_class_unavailable)
    @422.
    """
    await _clear_registry()
    # Seed rows with feed_id=wire_kna (training_data) in region=lonely_region.
    await _seed_row(
        source_ref="s://tr/x.raw", region="lonely_region",
        feed_id="wire_kna", klass="fact",
    )
    await _seed_row(
        source_ref="s://tr/y.raw", region="lonely_region",
        feed_id="wire_kna", klass="utterance",
    )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_base_body(
                scope_refs=["lonely_region"],
                minimum_class="utterance",
                commissioner="operator_internal",  # derives to editorial_use
            ),
        )
    assert resp.status_code == 422, (
        f"expected 422 admission refusal; got {resp.status_code}"
        f"\nbody: {resp.text}"
    )
    body = resp.json()
    envelope = AdmissionRefusal_v0.model_validate(body)
    assert envelope.reason == "license_class_unavailable"
    assert "editorial_use" in envelope.off_menu_fact, (
        f"off_menu_fact must reference the derived license class name; "
        f"got {envelope.off_menu_fact!r}"
    )
    # Actor-appropriate posture — grep-negative on owner-side phrasing.
    for phrase in ("await owner", "owner acceptance",
                   "ingredient manifest", "ingredient-manifest"):
        assert phrase not in envelope.what_you_can_do.lower()
        assert phrase not in envelope.off_menu_fact.lower()


# ---------------------------------------------------------------------------
# Gate 7 — standard hard input filter (v3 §6.1.6)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_qualified_data_standard_hard_input_filter():
    """v3 §6.1.6 hard input filter — below-floor units NEVER enter the
    deliverable.

    Test observation via mixed-class positive path: seed 3 rows at
    utterance and 2 at non_factual (both class buckets in
    `feed_id_to_license_class → editorial_use`). Request standard=utterance;
    warm-fork fires (feasible=True); packaging runs
    `_standard_hard_filter` which removes the two non_factual rows.
    Result unit_count == 3 (only utterance/above survives).

    Also verifies the `emit_standard_below_admission_floor` helper is
    callable + registered (defense-in-depth for the case where a future
    refactor bypasses the warm-fork gate and exposes the standard filter
    directly).
    """
    await _clear_registry()
    # 3 utterance-class + 2 non_factual-class rows, all citizen_tv_news
    # (editorial_use license → matches operator_internal commissioner).
    for i in range(3):
        await _seed_row(
            source_ref=f"s://f/u{i}.raw", region="mixed_std_region",
            feed_id="citizen_tv_news", klass="utterance",
        )
    for i in range(2):
        await _seed_row(
            source_ref=f"s://f/n{i}.raw", region="mixed_std_region",
            feed_id="citizen_tv_news", klass="non_factual",
        )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_base_body(
                scope_refs=["mixed_std_region"],
                minimum_class="utterance",  # excludes non_factual per §6.1.6
                commissioner="operator_internal",
            ),
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    # Standard hard filter removed the 2 non_factual rows.
    assert body["unit_count"] == 3, (
        f"§6.1.6 hard filter should have removed 2 non_factual rows from "
        f"the 5-row reach; got unit_count={body['unit_count']}"
    )
    # All surviving units are at or above utterance.
    for unit in body["units"]:
        klass = unit["defensibility"]["defensibility_class"]
        assert klass in ("utterance", "fact"), (
            f"below-floor unit leaked into deliverable — v3 §6.1.6 "
            f"violation: class={klass!r}"
        )


def test_emit_standard_below_admission_floor_helper_is_registered():
    """Defense-in-depth: `emit_standard_below_admission_floor` fires
    only from an unreachable-under-normal-fork branch, but the reason
    code MUST be registered so the emit helper does not RuntimeError
    if a future path exposes it.
    """
    from services.service_1 import admission_refusal as ar
    assert ar.is_valid_reason("standard_below_admission_floor") is True


# ---------------------------------------------------------------------------
# Gate 9 — per-claim provenance intact (v3 §6.1.3)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_qualified_data_per_claim_provenance_intact():
    """Every claim in the output carries `defensibility` (with
    defensibility_class, matrix_rule_ref, runtime_mode) AND `trace_id`."""
    await _clear_registry()
    await _seed_row(
        source_ref="s://p/f1.raw", region="prov_region",
        feed_id="citizen_tv_news", klass="fact",
    )
    await _seed_row(
        source_ref="s://p/f2.raw", region="prov_region",
        feed_id="citizen_tv_news", klass="utterance",
    )
    await _seed_row(
        source_ref="s://p/f3.raw", region="prov_region",
        feed_id="citizen_tv_news", klass="fact",
    )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_base_body(
                scope_refs=["prov_region"],
                minimum_class="utterance",
                commissioner="operator_internal",
            ),
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["unit_count"] == 3
    for unit in body["units"]:
        assert "defensibility" in unit, (
            f"per-claim provenance broken — no `defensibility` field in unit:\n{unit}"
        )
        defensibility = unit["defensibility"]
        assert "defensibility_class" in defensibility
        assert defensibility["defensibility_class"] in ("fact", "utterance", "non_factual")
        assert "matrix_rule_ref" in defensibility
        assert defensibility["matrix_rule_ref"] == "qm.v0.rule.1"
        assert "runtime_mode" in defensibility
        # trace_id is pseudonymised at outer-gate but still present as a field.
        assert "trace_id" in unit
        # `contested` status is contained inside defensibility_measure.
        assert "defensibility_measure" in defensibility
        assert "contested" in defensibility["defensibility_measure"]


# ---------------------------------------------------------------------------
# Gate 11 — Registry v1 extends v0 additively (Condition B2)
# ---------------------------------------------------------------------------


def test_admission_refusal_registry_v1_extends_v0_additively():
    """v1 bump preserves v0 reasons verbatim + adds three new codes;
    the AdmissionRefusal@v0 contract snapshot stays byte-identical.
    """
    v0_path = BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v0.json"
    v1_path = BACKEND_ROOT / "services" / "service_1" / "admission_refusal_reasons.v1.json"
    assert v0_path.exists(), f"v0 registry missing at {v0_path}"
    assert v1_path.exists(), f"v1 registry missing at {v1_path}"

    v0 = json.loads(v0_path.read_text(encoding="utf-8"))
    v1 = json.loads(v1_path.read_text(encoding="utf-8"))

    assert v0["config_version"] == "v0"
    assert v1["config_version"] == "v1"

    v0_reasons = {e["reason"] for e in v0["valid_reasons"]}
    v1_reasons = {e["reason"] for e in v1["valid_reasons"]}

    # v0 entries preserved in v1 (additive extension).
    assert v0_reasons.issubset(v1_reasons), (
        f"v1 must contain every v0 reason additively; missing: "
        f"{v0_reasons - v1_reasons}"
    )
    # v1 adds exactly three new codes (grain_form_incompatible,
    # standard_below_admission_floor, license_class_unavailable).
    added = v1_reasons - v0_reasons
    assert added == {
        "grain_form_incompatible",
        "standard_below_admission_floor",
        "license_class_unavailable",
    }, f"unexpected v1 additions: {added}"

    # v0 entries verbatim in v1 (since_version preserved).
    v0_by_reason = {e["reason"]: e for e in v0["valid_reasons"]}
    v1_by_reason = {e["reason"]: e for e in v1["valid_reasons"]}
    for r in v0_reasons:
        assert v1_by_reason[r]["since_version"] == v0_by_reason[r]["since_version"]

    # Snapshot of AdmissionRefusal@v0 stays byte-identical — the registry
    # bump is an out-of-contract extension per Ruling 3.
    snap = BACKEND_ROOT / "tests" / "invariants" / "admission_refusal.contract_snapshot.json"
    sha_snapshot = hashlib.sha256(snap.read_bytes()).hexdigest()
    # Pre-Phase-4a canonical SHA — captured at Phase 3 close.
    PRE_PHASE_4A_SHA = (
        "99381316dc71bf8f97acb36706bdfb057cb14c2da9ef1d32639aa788d72d67fb"
    )
    assert sha_snapshot == PRE_PHASE_4A_SHA, (
        f"AdmissionRefusal@v0 snapshot mutated by the registry bump — "
        f"Condition B2 violated.\n  pre-4a SHA: {PRE_PHASE_4A_SHA}\n"
        f"  post-4a SHA: {sha_snapshot}"
    )
