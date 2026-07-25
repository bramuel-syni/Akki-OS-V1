"""A2 HTTP-layer invariants for `POST /api/service_1/run` refusal envelope.

Verifies:
  1. All three refusal branches (`no_defensibility_floor`,
     `no_lawful_basis`, `composition_below_floor`) return HTTP 422 with a
     flat `outcome=refused` envelope conforming to
     contracts.service_1_refusal.Service1Refusal@v0.
  2. Validation-422 bodies (Pydantic RequestValidationError) are
     structurally distinguishable from refusal-422 (no `outcome` field;
     `detail` is a list).
  3. Infrastructure faults surface as HTTP 500 and NEVER as a
     refusal-shaped body.
  4. `supported_class` on the composition_below_floor branch is the
     max over per-unit Ring-5-governed `defensibility_class` values
     (D6a doctrine: single-source, no recomputation).
  5. Snapshot invariant for the Service1Refusal@v0 contract (14th
     freeze).

Every case-class asserts HTTP status + body shape + (where applicable)
zero DB write-delta on refusal cases.
"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import httpx
import pytest
from httpx import ASGITransport

from contracts.service_1_refusal_v1 import Service1Refusal_v1 as Service1RefusalContract
from server import app


RUN_ROUTE = "/api/service_1/run"
FIXTURE_PATH = (
    Path(__file__).parent.parent.parent / "services" / "data_source"
    / "synthetic_assets" / "instance_fixture_a" / "fixture.json"
)


def _load_fixture_units(n: int) -> list:
    fx = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return fx["units"][:n]


def _units_by_class(target_class: str, n: int) -> list:
    """Return N fixture units whose defensibility_class == target."""
    fx = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    out = []
    for u in fx["units"]:
        if u["defensibility"]["defensibility_class"] == target_class:
            out.append(u)
            if len(out) == n:
                return out
    if len(out) < n:
        raise RuntimeError(
            f"fixture has only {len(out)} units of class {target_class}; "
            f"need {n}"
        )
    return out


def _valid_request_body(*, units: list, floor: str, objective_text: str,
                        lawful_basis: str = "dpa-a2-test") -> dict:
    return {
        "artifact_id": "a2-refusal-envelope-test",
        "artifact_version": "v0",
        "lawful_basis": lawful_basis,
        "floor": floor,
        "scope_key": "portfolio",
        "objective_text": objective_text,
        "units": units,
    }


async def _opcounters() -> dict:
    from core import db
    server_status = await db.command("serverStatus")
    op = server_status.get("opcounters", {})
    return {
        "insert": int(op.get("insert", 0)),
        "update": int(op.get("update", 0)),
        "delete": int(op.get("delete", 0)),
    }


def _write_delta(before: dict, after: dict) -> int:
    return (
        (after["insert"] - before["insert"])
        + (after["update"] - before["update"])
        + (after["delete"] - before["delete"])
    )


REFUSAL_ENVELOPE_KEYS = {
    # v0-preserved keys (7)
    "outcome", "reason", "run_id", "trace_id",
    "asked", "supported_class", "what_would_raise_it",
    # v1 additive keys (4 · EAB-2 seal 2026-07-24 · Owner ruling Locus 2 = α + Locus 3 = γ posture)
    # Populated on `reason == "coverage_gap"` · None on evidential-family refusals per
    # single-writer end-state (Owner ruling composition ε + α + γ).
    "estate_region", "period", "source_class", "filed_candidate_id",
}


# ------- Case 1: no_defensibility_floor --------------------------------------
@pytest.mark.asyncio
async def test_no_floor_refusal_returns_flat_outcome_refused():
    """Missing floor → validation-422 (Pydantic rejects, doesn't reach service).

    Note: the router's `Service1RunRequest.floor` is a required enum, so
    passing `null` triggers Pydantic validation error BEFORE service.run
    runs. That is FastAPI's validation-422 (detail: list). The
    service-layer `no_defensibility_floor` refusal only fires if the
    router bypass is used (direct service call — covered by
    test_service_1_refuses_no_floor in test_service_1_invariants.py).

    This test therefore verifies the boundary: a request with a null
    floor hits validation-422, NOT refusal-422 with outcome=refused.
    """
    body = _valid_request_body(
        units=_load_fixture_units(1),
        floor=None,  # invalid — will trip Pydantic
        objective_text="test objective for missing-floor case",
    )
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        resp = await c.post(RUN_ROUTE, json=body)
    assert resp.status_code == 422, resp.text
    b = resp.json()
    # Validation-422 shape (Pydantic): detail is a list, no outcome
    assert b.get("outcome") is None, (
        f"validation-422 leaked outcome field: {b!r}"
    )
    assert isinstance(b.get("detail"), list), (
        f"expected detail: list for validation-422; got {type(b.get('detail')).__name__}"
    )


# ------- Case 2: no_lawful_basis (empty string) ------------------------------
@pytest.mark.asyncio
async def test_no_lawful_basis_refusal_returns_flat_outcome_refused():
    """Empty lawful_basis passes Pydantic (str min=0) but hits the
    service-layer no_lawful_basis refusal → 422 with outcome=refused.
    """
    body = _valid_request_body(
        units=_load_fixture_units(1),
        floor="non_factual",
        objective_text="test objective for no-lawful-basis case",
        lawful_basis="",   # empty → service-layer refusal
    )
    before = await _opcounters()
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        resp = await c.post(RUN_ROUTE, json=body)
    after = await _opcounters()

    assert resp.status_code == 422, resp.text
    b = resp.json()
    assert set(b.keys()) == REFUSAL_ENVELOPE_KEYS, (
        f"refusal envelope key drift: got {sorted(b.keys())} "
        f"vs expected {sorted(REFUSAL_ENVELOPE_KEYS)}"
    )
    assert b["outcome"] == "refused"
    assert b["reason"] == "no_lawful_basis"
    assert b["asked"], f"empty 'asked': {b!r}"
    assert b["supported_class"] is None
    assert b["what_would_raise_it"] == (
        "Provide a non-empty lawful_basis reference on the request."
    )
    # Round-trip through the frozen contract to prove shape conformance
    parsed = Service1RefusalContract(**b)
    assert parsed.outcome == "refused"
    # Phase 8 Seam 3 Sub-stage 1 (2026-07-07): pre-composition refusals now
    # emit EXACTLY ONE ledger row via emit_refusal_ledger_row per R-1 (LB
    # gate: every decision="refused" row pins refusal_family). Pre-Sub-
    # stage-1 asserted zero writes; post-Sub-stage-1 asserts exactly one
    # insert (the pinned-key ledger row) into NORTHENA_LEDGER_COLLECTION.
    assert _write_delta(before, after) == 1, (
        f"no_lawful_basis refusal expected exactly 1 write (pinned "
        f"refusal-family ledger row): {before} -> {after}"
    )


# ------- Case 3: composition_below_floor (D1b + D8a) -------------------------
@pytest.mark.asyncio
async def test_composition_below_floor_returns_flat_outcome_refused():
    """Feed only utterance+non_factual units under a `fact` floor →
    Targeta filters everything → eligible == [] → composition_below_floor
    refusal fires with supported_class=max(input classes)=utterance.
    """
    utterances = _units_by_class("utterance", 2)
    non_factuals = _units_by_class("non_factual", 1)
    units = utterances + non_factuals   # no fact-class units
    body = _valid_request_body(
        units=units, floor="fact",
        objective_text="composition-below-floor test objective",
    )
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        resp = await c.post(RUN_ROUTE, json=body)
    assert resp.status_code == 422, resp.text
    b = resp.json()
    assert set(b.keys()) == REFUSAL_ENVELOPE_KEYS
    assert b["outcome"] == "refused"
    assert b["reason"] == "composition_below_floor"
    assert b["asked"] == "composition-below-floor test objective"
    # D7a: max over per-unit governed classes = utterance (utterance > non_factual)
    assert b["supported_class"] == "utterance", (
        f"expected supported_class=utterance (max over input classes); "
        f"got {b['supported_class']!r}"
    )
    assert b["what_would_raise_it"].startswith("No corroboration at the required standard")
    # Round-trip the frozen contract
    parsed = Service1RefusalContract(**b)
    assert parsed.reason == "composition_below_floor"


# ------- Case 4: validation-422 distinguishability (D3a load-bearing) --------
@pytest.mark.asyncio
async def test_validation_422_distinguishable_from_refusal_422():
    """POST with missing required artifact_id → FastAPI validation-422.
    Body has detail: list, no outcome field. Structurally distinct from
    a governed refusal envelope.
    """
    bad_body = _valid_request_body(
        units=_load_fixture_units(1),
        floor="non_factual",
        objective_text="validation-422 test",
    )
    del bad_body["artifact_id"]   # trip Pydantic
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        resp = await c.post(RUN_ROUTE, json=bad_body)
    assert resp.status_code == 422, resp.text
    b = resp.json()
    # Structural discriminator: validation body has detail: list, no outcome
    assert b.get("outcome") is None
    assert isinstance(b.get("detail"), list), (
        f"expected list-shaped detail for validation-422; got {b!r}"
    )
    # Confirm this shape is NOT a refusal envelope
    assert set(b.keys()) != REFUSAL_ENVELOPE_KEYS
    # And each detail item carries the Pydantic validation fields
    first = b["detail"][0]
    for k in ("type", "loc", "msg"):
        assert k in first, f"validation entry missing {k}: {first!r}"


# ------- Case 5: infrastructure fault → 500, never refusal-shaped ------------
@pytest.mark.asyncio
async def test_infrastructure_fault_does_not_render_as_refusal(monkeypatch):
    """Simulate a Mongo outage by monkeypatching northena_ledger.record
    to raise RuntimeError. Router MUST propagate 500; body MUST NOT have
    outcome=refused (else infrastructure faults masquerade as governed
    refusals).
    """
    async def _boom(*_a, **_kw):
        raise RuntimeError("simulated Mongo outage for A2 fault-guard test")

    from services.northena import ledger as northena_ledger
    monkeypatch.setattr(northena_ledger, "record", _boom)

    body = _valid_request_body(
        units=_load_fixture_units(1),
        floor="non_factual",
        objective_text="infrastructure-fault test",
    )
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        # httpx raises the underlying exception when the ASGI handler
        # explodes; we assert via the raised type rather than status_code
        try:
            resp = await c.post(RUN_ROUTE, json=body)
            got_status = resp.status_code
            got_body = None
            try:
                got_body = resp.json()
            except Exception:
                got_body = {"raw": resp.text}
        except RuntimeError as e:
            # If ASGITransport surfaces the exception directly, that is a
            # non-refusal path (definitely not outcome=refused). Test
            # passes on this branch.
            assert "simulated Mongo outage" in str(e)
            return
    # If we got a response, it must NOT be refusal-shaped.
    assert got_status == 500, (
        f"expected 500 on infrastructure fault; got {got_status}, body={got_body!r}"
    )
    assert got_body is None or got_body.get("outcome") != "refused", (
        f"infrastructure fault masqueraded as refusal: {got_body!r}"
    )


# ------- Case 6: supported_class is Ring-5-governed, not recomputed (D6a) ---
@pytest.mark.asyncio
async def test_supported_class_is_ring5_governed_not_recomputed():
    """Construct a request with a KNOWN mix of classes and assert the
    refusal envelope's supported_class equals max(input classes) — the
    Ring-5-governed value already stamped on each NormalizedUnit.
    """
    utterance_units = _units_by_class("utterance", 1)
    nf_units = _units_by_class("non_factual", 2)
    input_units = utterance_units + nf_units

    # Mutate a copy: force the SIGNAL ring on the utterance-class unit to
    # look "weak" (all zero score_vector). If supported_class were
    # recomputed from signals, mutation would sway the result. Under
    # D6a doctrine, supported_class reads defensibility_class directly
    # and stays at "utterance" regardless of the signal ring.
    units = deepcopy(input_units)
    units[0]["defensibility"]["score_vector"] = {
        "genre_ceiling": 0.0, "source_standing": 0.0, "corroboration": 0.0,
        "recency": 0.0, "contested_status": 0.0,
    }

    body = _valid_request_body(
        units=units, floor="fact",
        objective_text="D6a governed-not-recomputed test",
    )
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        resp = await c.post(RUN_ROUTE, json=body)
    assert resp.status_code == 422, resp.text
    b = resp.json()
    assert b["reason"] == "composition_below_floor"
    # If signals-based recomputation were happening, the zeroed
    # score_vector would drop the class. D6a: it stays at utterance.
    assert b["supported_class"] == "utterance", (
        f"D6a violation: supported_class changed under signal-ring mutation. "
        f"Got {b['supported_class']!r}, expected 'utterance' (governed value)."
    )


# ------- Case 7: max, not min (D7a) ------------------------------------------
@pytest.mark.asyncio
async def test_composition_below_floor_uses_max_not_min():
    """Mixed input: one utterance + one non_factual, floor=fact.
    Under max reduction (D7a), supported_class == 'utterance'.
    Under min reduction (Solva's conclusion_class semantic, wrong for
    Service 1), supported_class would be 'non_factual'.
    Assert max semantics.
    """
    units = _units_by_class("utterance", 1) + _units_by_class("non_factual", 1)
    body = _valid_request_body(
        units=units, floor="fact",
        objective_text="D7a max-not-min test",
    )
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        resp = await c.post(RUN_ROUTE, json=body)
    assert resp.status_code == 422, resp.text
    b = resp.json()
    assert b["reason"] == "composition_below_floor"
    assert b["supported_class"] == "utterance", (
        f"D7a violation: expected max reduction (utterance); got "
        f"{b['supported_class']!r} — this looks like min semantics."
    )


# ------- Snapshot invariant (14th freeze) ------------------------------------
def test_service_1_refusal_schema_frozen():
    """Snapshot invariant — Service1Refusal@v0 schema is frozen.

    Any drift fails loudly. Re-blessing requires an explicit code
    review artifact (mirrors Operating Protocol §1.7 discipline).
    """
    snapshot_path = (
        Path(__file__).parent / "service_1_refusal_v1.contract_snapshot.json"
    )
    expected = snapshot_path.read_text(encoding="utf-8").rstrip("\n")
    actual = json.dumps(
        Service1RefusalContract.model_json_schema(),
        indent=2, sort_keys=True,
    )
    assert actual == expected, (
        "Service1Refusal@v0 schema drifted; re-bless snapshot in review."
    )
