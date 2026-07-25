"""Composed-conclusion dispatch surface tests — Phase 4b gates 14-17.

Houses:
  * Gate 14 — `test_composed_conclusion_grain_synthesized_whole_only`.
    v3 §6.2.4; non-synthesized_whole grain → AdmissionRefusal_v0(
    reason=grain_form_incompatible) via 4a shared grain-compat matrix.
  * Gate 15 — `test_composed_conclusion_below_floor_returns_service_1_refusal_v0`.
    v3 §6.2.6; response is Service1Refusal_v0(reason=composition_below_floor,
    asked, supported_class, what_would_raise_it) @422.
  * Gate 16 — `test_composed_conclusion_load_bearing_retrievable_by_trace_id`.
    v3 §6.2.3; Northena Ledger lookup by trace_id returns the same
    load_bearing unit ids.
  * Gate 17 — `test_composed_conclusion_live_path_returns_class_inline`.
    v3 §6.2.5 + §12 invariant #7; flat body with `conclusion_class` at
    top level; no separation of claim from class.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import httpx
import pytest
from httpx import ASGITransport

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.composed_conclusion import ComposedConclusion_v0
from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION
from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from contracts.service_1_refusal_v1 import Service1Refusal_v1 as Service1Refusal
from core import db
from server import app


async def _clear() -> None:
    await db[MTAFITI_REGISTRY_COLLECTION].delete_many({})
    await db[NORTHENA_LEDGER_COLLECTION].delete_many({})


async def _seed_row(
    *, source_ref: str, region: str, feed_id: str, klass: str,
) -> None:
    logged = (datetime.now(timezone.utc) - timedelta(days=0)).isoformat()
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


def _body(*, grain: str, scope_refs, minimum_class: str = "utterance",
          commissioner: str = "operator_internal") -> dict:
    return {
        "entry": "external_request",
        "reach": {"scope_refs": scope_refs, "exclusions": [], "depth": "baseline"},
        "output": {
            "form": "composed_conclusion",
            "consumer": "person",
            "grain": grain,
            "standard": {"minimum_class": minimum_class},
        },
        "envelope": {
            "lawful_basis": "test_basis_4b",
            "done_condition": "test",
            "budget": "test",
            "scope_ceiling": "test",
            "commissioner": commissioner,
            "committed_at": "2026-07-04T12:00:00+00:00",
        },
    }


# ---------------------------------------------------------------------------
# Gate 14 — grain synthesized_whole only (v3 §6.2.4)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_composed_conclusion_grain_synthesized_whole_only():
    """composed_conclusion + per_claim (or aggregated) → refused with
    reason=grain_form_incompatible at admission time (reuses 4a shared
    grain-compat matrix).
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        for grain in ("per_claim", "aggregated"):
            resp = await client.post(
                "/api/service_1/v2/dispatch",
                json=_body(grain=grain, scope_refs=["never_reached"]),
            )
            assert resp.status_code == 422, (
                f"({grain}) — expected 422 grain refusal; got {resp.status_code}\n"
                f"body: {resp.text}"
            )
            body = resp.json()
            envelope = AdmissionRefusal_v0.model_validate(body)
            assert envelope.reason == "grain_form_incompatible"
            # Ruling 7 UNIFIED code — same reason string for all grain refusals.
            # 4a fold-in reuse verified.


# ---------------------------------------------------------------------------
# Gate 15 — below-floor → Service1Refusal(composition_below_floor) (v3 §6.2.6)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_composed_conclusion_below_floor_returns_service_1_refusal_v0():
    """Mixed fact + utterance rows, requested floor = fact.

    Warm-fork fires (has fact ≥ floor). package_composed_conclusion
    runs on ALL license-class-filtered survivors (no §6.1.6 hard input
    filter in §6.2 path — dispatch reading 2026-07-04). Solva computes
    conclusion_class = min(fact, utterance) = utterance. utterance <
    fact → Service1Refusal(composition_below_floor) fires @ 422 with
    the frozen envelope.
    """
    await _clear()
    await _seed_row(
        source_ref="s://bf/f.raw", region="bf_region",
        feed_id="feed_a", klass="fact",
    )
    await _seed_row(
        source_ref="s://bf/u.raw", region="bf_region",
        feed_id="feed_a", klass="utterance",
    )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_body(
                grain="synthesized_whole",
                scope_refs=["bf_region"],
                minimum_class="fact",
            ),
        )
    assert resp.status_code == 422, (
        f"expected 422 Service1Refusal(composition_below_floor); "
        f"got {resp.status_code}\nbody: {resp.text}"
    )
    envelope = Service1Refusal.model_validate(resp.json())
    assert envelope.outcome == "refused"
    assert envelope.reason == "composition_below_floor"
    # §6.2.6 fields present + honest content.
    assert envelope.asked and "fact" in envelope.asked
    assert envelope.what_would_raise_it and len(envelope.what_would_raise_it) > 0
    # supported_class = max over load-bearing units' Ring-5 classes.
    # Mix of fact + utterance → max is fact.
    from contracts.five_rings import DefensibilityClass
    assert envelope.supported_class == DefensibilityClass.FACT
    # run_id + trace_id present.
    assert envelope.run_id and envelope.run_id.startswith("cc-run-")
    assert envelope.trace_id and envelope.trace_id.startswith("disp-")


@pytest.mark.asyncio
async def test_composed_conclusion_composition_below_floor_at_fact_floor():
    """Direct-call variant of gate 15 — invokes `package_composed_conclusion`
    with a constructed ObjectiveRequest_v2 and asserts the
    Service1Refusal exception is raised with the correct fields.
    """
    await _clear()
    await _seed_row(
        source_ref="s://cbf/u.raw", region="cbf_region",
        feed_id="feed_a", klass="utterance",
    )
    await _seed_row(
        source_ref="s://cbf/f.raw", region="cbf_region",
        feed_id="feed_a", klass="fact",
    )

    from contracts.objective_request_v2 import ObjectiveRequest_v2
    from services.service_1 import composed_conclusion as cc_module

    request = ObjectiveRequest_v2.model_validate(_body(
        grain="synthesized_whole",
        scope_refs=["cbf_region"],
        minimum_class="fact",
    ))

    with pytest.raises(cc_module.Service1Refusal) as excinfo:
        await cc_module.package_composed_conclusion(request, trace_id="test-cbf")

    exc = excinfo.value
    assert exc.reason == "composition_below_floor"
    assert exc.trace_id == "test-cbf"
    assert exc.asked and "fact" in exc.asked
    assert exc.what_would_raise_it and len(exc.what_would_raise_it) > 0
    from contracts.five_rings import DefensibilityClass
    assert exc.supported_class == DefensibilityClass.FACT


@pytest.mark.asyncio
async def test_composed_conclusion_below_floor_route_serialises_to_service_1_refusal_v0():
    """When Service1Refusal fires from the v2 route, the router catches
    it and serialises to Service1Refusal_v0 @422 with the frozen envelope
    shape (outcome=refused, reason, asked, supported_class,
    what_would_raise_it, run_id, trace_id). Duplicate coverage of the
    router exception-catch surface.
    """
    await _clear()
    await _seed_row(
        source_ref="s://bfr/u.raw", region="bfr_region",
        feed_id="feed_a", klass="utterance",
    )
    await _seed_row(
        source_ref="s://bfr/f.raw", region="bfr_region",
        feed_id="feed_a", klass="fact",
    )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_body(
                grain="synthesized_whole",
                scope_refs=["bfr_region"],
                minimum_class="fact",
            ),
        )
    assert resp.status_code == 422, resp.text
    envelope = Service1Refusal.model_validate(resp.json())
    assert envelope.outcome == "refused"
    assert envelope.reason == "composition_below_floor"
    assert envelope.asked and "fact" in envelope.asked
    assert envelope.what_would_raise_it
    from contracts.five_rings import DefensibilityClass
    assert envelope.supported_class == DefensibilityClass.FACT


# ---------------------------------------------------------------------------
# Gate 16 — load-bearing retrievable by trace_id (v3 §6.2.3)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_composed_conclusion_load_bearing_retrievable_by_trace_id():
    """After a successful composed_conclusion, the Northena Ledger row
    at (trace_id, stage=converge) carries the load_bearing unit_ids in
    its `reason` field per v3 §6.2.3.
    """
    await _clear()
    await _seed_row(
        source_ref="s://lb/f1.raw", region="lb_region",
        feed_id="feed_a", klass="fact",
    )
    await _seed_row(
        source_ref="s://lb/f2.raw", region="lb_region",
        feed_id="feed_a", klass="fact",
    )
    await _seed_row(
        source_ref="s://lb/f3.raw", region="lb_region",
        feed_id="feed_a", klass="fact",
    )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_body(
                grain="synthesized_whole",
                scope_refs=["lb_region"],
                minimum_class="utterance",
            ),
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    envelope = ComposedConclusion_v0.model_validate(body)
    assert len(envelope.load_bearing_unit_ids) == 3
    trace_id = envelope.trace_id

    # Ledger lookup by trace_id.
    rows = [
        r async for r in
        db[NORTHENA_LEDGER_COLLECTION].find({"trace_id": trace_id}, {"_id": 0})
    ]
    assert rows, (
        f"§6.2.3 violation — no Ledger row exists for trace_id={trace_id!r}. "
        f"load-bearing set is unretrievable."
    )
    # At least one row must carry the load_bearing unit_ids in its reason.
    load_bearing_carriers = [
        r for r in rows
        if "composed_conclusion:" in r.get("reason", "")
        and "load_bearing=" in r.get("reason", "")
    ]
    assert load_bearing_carriers, (
        f"§6.2.3 violation — Ledger has {len(rows)} rows for trace_id but "
        f"none carry `composed_conclusion:*:load_bearing=*`.\n"
        f"Rows: {[r.get('reason') for r in rows]}"
    )
    lb_row = load_bearing_carriers[0]
    lb_field = lb_row["reason"].split("load_bearing=", 1)[1]
    ledger_unit_ids = lb_field.split(",")
    # Same unit_ids, same order.
    assert ledger_unit_ids == envelope.load_bearing_unit_ids, (
        f"§6.2.3 violation — Ledger unit_ids do not match envelope "
        f"load_bearing_unit_ids.\n"
        f"  envelope: {envelope.load_bearing_unit_ids}\n"
        f"  ledger:   {ledger_unit_ids}"
    )


# ---------------------------------------------------------------------------
# Gate 17 — conclusion_class inline at top level (v3 §6.2.5 + §12 inv #7)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_composed_conclusion_live_path_returns_class_inline():
    """v3 §12 invariant #7 (line 169): 'no response shape separates
    claim from class'. `answer_text` and `conclusion_class` MUST be
    colocated at top level (not nested in a sub-object).
    """
    await _clear()
    await _seed_row(
        source_ref="s://live/f.raw", region="live_region",
        feed_id="feed_a", klass="fact",
    )
    await _seed_row(
        source_ref="s://live/u.raw", region="live_region",
        feed_id="feed_a", klass="utterance",
    )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_body(
                grain="synthesized_whole",
                scope_refs=["live_region"],
                minimum_class="utterance",
            ),
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    # Top-level keys — §12 invariant #7.
    assert "conclusion_class" in body, (
        f"§12 invariant #7 violation — conclusion_class not at top level: "
        f"{sorted(body.keys())}"
    )
    assert "answer_text" in body, (
        f"§12 invariant #7 violation — answer_text not at top level: "
        f"{sorted(body.keys())}"
    )
    # Colocation confirmed: both present, both top-level.
    assert isinstance(body["conclusion_class"], str)
    assert body["conclusion_class"] in ("fact", "utterance", "non_factual")
    # Solva floor: min over {fact, utterance} == utterance.
    assert body["conclusion_class"] == "utterance"
    # Envelope validates as frozen ComposedConclusion_v0.
    envelope = ComposedConclusion_v0.model_validate(body)
    assert envelope.answer_text
    assert envelope.trace_id
    assert envelope.load_bearing_unit_ids
    assert envelope.objective_ref
    assert envelope.computed_at
