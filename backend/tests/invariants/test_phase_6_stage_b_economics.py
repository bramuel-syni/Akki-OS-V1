"""Phase 6 Stage B economics — 18+ named gate tests.

Test-surface roster per Stage A Return 7.2, Owner-ratified at Stage B open:

  # 1  test_quote_envelope_frozen_at_v0                                    LB
  # 2  test_price_model_version_stamps_every_quote                          LB
  # 3  test_pricing_tier_not_a_literal                                      LB
  # 4  test_pricing_tier_registry_extension_via_bump_not_literal_widening   LB
  # 5  test_fleet_policy_apportionment_sums_to_one
  # 6  test_exploratory_tier_is_time_boxed
  # 7  test_quote_instrumentation_never_contradicts_primary_field           LB
  # 8  test_delivery_time_never_reports_gpu_numbers_on_buyer_surface        LB
  # 9  test_queue_saturation_returns_503_not_refusal
  # 10 test_fleet_capacity_governance_refusal_uses_admission_refusal_v0     LB
  # 11 test_config_expiry_governance_refusal
  # 12 test_async_delivery_accepted_v1_supersets_v0                         LB
  # 13 test_delivery_time_has_exactly_two_bands                             LB
  # 14 test_prior_contracts_byte_identical_after_phase_6_stage_b (in test_v0_paths_byte_identical_after_6b.py) LB
  # 15 test_admission_refusal_v3_extends_v2_additively
  # 16 test_master_admin_gated_pricing_writes
  # 17 test_no_arbitration_beyond_apportionment_in_fleet_policy_json
  # 18 test_hazard_stop_notes_in_all_economics_modules
"""
from __future__ import annotations

import ast
import json
import os
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.async_delivery_accepted import AsyncDeliveryAccepted_v0
from contracts.async_delivery_accepted_v1 import AsyncDeliveryAccepted_v1
from contracts.objective_request_v2 import ObjectiveRequest_v2, OutputForm
from contracts.quote_envelope import QuoteEnvelope_v0, QuoteInstrumentationSeed_v0
from services.economics import (
    delivery_time as _delivery_time,
    expiry as _expiry,
    fleet_policy as _fleet_policy,
    instrumentation as _instrumentation,
    price_model as _price_model,
    quote_service as _quote_service,
)
from services.service_1 import admission_refusal as _admission_refusal
from services.service_1 import async_worker

from server import app


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
CONTRACTS_DIR = BACKEND_ROOT / "contracts"
SERVICES_DIR = BACKEND_ROOT / "services"
INVARIANTS_DIR = Path(__file__).resolve().parent


def _valid_body(
    *, form: str = "qualified_data", grain: str = "per_claim",
    minimum_class: str = "utterance",
    scope_refs=("region:eu",),
    idempotency_key: str = "idem-phase6",
    entry: str = "external_request",
    consumer: str = "person",
):
    return {
        "entry": entry,
        "reach": {"scope_refs": list(scope_refs), "exclusions": [], "depth": "baseline"},
        "output": {
            "form": form,
            "consumer": consumer,
            "grain": grain,
            "standard": {"minimum_class": minimum_class},
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


# ---------------------------------------------------------------------------
# Gate 1 (LB) — QuoteEnvelope_v0 FROZEN at v0.
# ---------------------------------------------------------------------------


def test_quote_envelope_frozen_at_v0():
    """Contract schema matches on-disk snapshot byte-identical."""
    snap = INVARIANTS_DIR / "quote_envelope.contract_snapshot.json"
    expected = json.loads(snap.read_text(encoding="utf-8"))
    live = QuoteEnvelope_v0.model_json_schema()
    assert live == expected, (
        "QuoteEnvelope_v0 schema drift — freeze surface changed. "
        "Update the snapshot ONLY if Owner re-blessed."
    )


# ---------------------------------------------------------------------------
# Gate 2 (LB) — every quote stamps its price-model version (v3 §12 invariant #9).
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_price_model_version_stamps_every_quote():
    request = ObjectiveRequest_v2.model_validate(_valid_body())
    quote_or_ref = await _quote_service.issue_quote(request, "trc-p6-test-2", warm_vs_fresh="fresh")
    assert isinstance(quote_or_ref, QuoteEnvelope_v0), quote_or_ref
    assert quote_or_ref.price_model_version.startswith("price-model@v")
    assert quote_or_ref.instrumentation_seed.price_model_version == quote_or_ref.price_model_version


# ---------------------------------------------------------------------------
# Gate 3 (LB) — `pricing_tier` is a constrained-str, NOT a Literal (Ruling 5).
# ---------------------------------------------------------------------------


def test_pricing_tier_not_a_literal():
    src = (CONTRACTS_DIR / "quote_envelope.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    # Find the QuoteEnvelope_v0 class, then the `pricing_tier` AnnAssign.
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef) or node.name != "QuoteEnvelope_v0":
            continue
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                if item.target.id == "pricing_tier":
                    annotation_src = ast.unparse(item.annotation)
                    assert "Literal" not in annotation_src, (
                        f"HAZARD-STOP — QuoteEnvelope_v0.pricing_tier annotated with "
                        f"`Literal`, violating Ruling 5. Annotation: {annotation_src!r}"
                    )
                    assert "PricingTierStr" in annotation_src or "StringConstraints" in annotation_src, (
                        f"pricing_tier MUST use constrained-str via external registry per Ruling 5. "
                        f"Annotation: {annotation_src!r}"
                    )
                    return
    pytest.fail("QuoteEnvelope_v0.pricing_tier AnnAssign not found in AST scan.")


# ---------------------------------------------------------------------------
# Gate 4 (LB) — Registry extension via bump, never Literal widening.
# ---------------------------------------------------------------------------


def test_pricing_tier_registry_extension_via_bump_not_literal_widening():
    """Adding a new tier ships as a NEW pricing_tiers.vN.json file; never
    a modification of the constrained-str pattern on the frozen contract."""
    src = (CONTRACTS_DIR / "quote_envelope.py").read_text(encoding="utf-8")
    # Any Literal[..] tuple on pricing_tier is a HAZARD-STOP.
    assert "PricingTierStr" in src
    # The pattern regex is the current constrained-str range; unchanged
    # since v0 open — a bump would land a new type alias, not mutate this.
    assert 'pattern=r"^[a-z][a-z0-9_]{0,31}$"' in src


# ---------------------------------------------------------------------------
# Gate 5 — Fleet apportionment sums to 1.0 within tolerance.
# ---------------------------------------------------------------------------


def test_fleet_policy_apportionment_sums_to_one():
    assert _fleet_policy.apportionment_sums_to_one() is True


# ---------------------------------------------------------------------------
# Gate 6 — Exploratory tier is time-boxed (v3 §8 bullet 2).
# ---------------------------------------------------------------------------


def test_exploratory_tier_is_time_boxed():
    cfg = _price_model.load_config()
    assert "expires_at" in cfg, "price_model config MUST carry expires_at (§8 bullet 2 time-boxing)."
    assert cfg["expires_at"], "expires_at MUST be populated for the current-bless tier."


# ---------------------------------------------------------------------------
# Gate 7 (LB) — stamp_audit sidecar NEVER contradicts the primary field.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_quote_instrumentation_never_contradicts_primary_field(monkeypatch):
    """Sidecar `outcome` MUST be consistent with primary decision field."""
    # Build a QuoteEnvelope_v0 fixture.
    inner = QuoteInstrumentationSeed_v0(
        shape_ref="shape:test",
        price_model_version="price-model@v0-exploratory",
    )
    envelope = QuoteEnvelope_v0(
        quote_id="q-consistency-1",
        trace_id="trc-consistency-1",
        quoted_at="2026-07-04T00:00:00+00:00",
        price_model_version="price-model@v0-exploratory",
        pricing_tier="exploratory",
        figure="USD 10.00",
        qualifying_volume="~1 refs",
        delivery_estimate="PT30S",
        delivery_class="warm_qualified",
        feasible_and_offerable=True,
        instrumentation_seed=inner,
    )
    captured = {}

    class _FakeCol:
        async def find_one(self, *a, **kw): return None
        async def insert_one(self, doc):
            captured["doc"] = doc

    monkeypatch.setattr(_instrumentation, "db", {_instrumentation.NORTHENA_LEDGER_COLLECTION: _FakeCol()})

    for event, expected_outcome in [
        ("minted", "pending"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
        ("negotiated_to", "negotiated_to"),
        ("refused_after_acceptance", "rejected"),
    ]:
        captured.clear()
        await _instrumentation.record_quote_event(
            quote_envelope=envelope, event=event,
            objective_ref="objreq-consistency", lawful_basis_ref="lb-consistency",
            run_id=f"run-{event}",
        )
        doc = captured.get("doc")
        assert doc is not None, f"instrumentation write skipped for event={event!r}"
        primary = doc["decision"]
        sidecar_outcome = doc["stamp_audit"]["quote_instrumentation_event"]["outcome"]
        assert sidecar_outcome == expected_outcome
        # Sidecar outcome is NEVER a decision-level term (admitted/refused/warm/fresh/...).
        # This is the "never contradicts primary" guard — sidecar echoes buyer disposition
        # while primary decision (`terminate_success`) records the run outcome shape.
        assert sidecar_outcome not in {"admitted", "refused", "warm", "fresh", "terminate_budget", "continue"}, (
            f"HAZARD-STOP — sidecar outcome {sidecar_outcome!r} would contradict primary "
            f"decision field. See Return 4.5 regression gate."
        )
        assert primary == "terminate_success"


# ---------------------------------------------------------------------------
# Gate 8 (LB) — Buyer surface NEVER exposes GPU numbers (§8 bullet 4).
# ---------------------------------------------------------------------------


def test_delivery_time_never_reports_gpu_numbers_on_buyer_surface():
    """Grep-negative on buyer-surface strings for GPU-adjacent keywords."""
    forbidden = ["gpu", "GPU", "gpu_hours", "gpu_hrs", "cuda", "vram",
                 "throughput_units_per_hour"]
    # Contract layer: QuoteEnvelope_v0 field descriptions.
    schema = QuoteEnvelope_v0.model_json_schema()
    schema_text = json.dumps(schema).lower()
    for word in forbidden:
        assert word.lower() not in schema_text, (
            f"HAZARD-STOP — GPU-adjacent keyword {word!r} appears in "
            f"QuoteEnvelope_v0 schema (buyer surface). Ruling 5 + §8 bullet 4."
        )
    # Delivery config buyer-facing surface.
    price_cfg = _price_model.load_config()
    price_cfg_text = json.dumps(price_cfg).lower()
    for word in forbidden:
        assert word.lower() not in price_cfg_text, (
            f"HAZARD-STOP — GPU-adjacent keyword {word!r} appears in "
            f"price-model config (buyer-facing hazard notes are OK if they warn "
            f"NOT-exposed, but literal exposure is forbidden)."
        )


# ---------------------------------------------------------------------------
# Gate 9 — Queue saturation returns 503 (infra), NOT AdmissionRefusal (governance).
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_queue_saturation_returns_503_not_refusal(monkeypatch):
    """Regression from Phase 5 Stage B — infra-not-refusal doctrine."""
    class _FakeQueue:
        def qsize(self): return 999
        def put_nowait(self, _):
            import asyncio as _a
            raise _a.QueueFull()

    monkeypatch.setattr(async_worker, "_queue", _FakeQueue())

    with pytest.raises(async_worker.QueueSaturatedError):
        await async_worker.enqueue_objective("obj-saturated-1")


# ---------------------------------------------------------------------------
# Gate 10 (LB) — Fleet zero-capacity → AdmissionRefusal_v0 @422 (governance),
# NOT 503 (infra).
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_fleet_capacity_governance_refusal_uses_admission_refusal_v0(monkeypatch):
    """Fleet policy has apportioned zero to a modality — GOVERNANCE decision."""
    original_load = _fleet_policy.load_config
    def zero_transforms():
        cfg = original_load()
        cfg["apportionment"] = {"mining": 0.5, "transforms": 0.0, "live_path": 0.5}
        return cfg
    monkeypatch.setattr(_fleet_policy, "load_config", zero_transforms)

    request = ObjectiveRequest_v2.model_validate(_valid_body(form="qualified_data"))
    # Force _quote_service to pick up the patched config too.
    monkeypatch.setattr(_quote_service, "_fleet_policy", _fleet_policy)
    quote_or_refusal = await _quote_service.issue_quote(request, "trc-fleet-refusal", warm_vs_fresh="fresh")
    assert isinstance(quote_or_refusal, AdmissionRefusal_v0)
    assert quote_or_refusal.reason == "fleet_policy_reserved_zero_capacity"


# ---------------------------------------------------------------------------
# Gate 11 — Config expiry → governance refusal.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_config_expiry_governance_refusal(monkeypatch):
    """Expired price-model config refuses with exploratory_tier_expired."""
    def past_expiry(_cfg, *, now=None):
        return True  # force expired
    monkeypatch.setattr(_expiry, "is_expired", past_expiry)
    monkeypatch.setattr(_quote_service, "_expiry", _expiry)
    request = ObjectiveRequest_v2.model_validate(_valid_body())
    result = await _quote_service.issue_quote(request, "trc-expired", warm_vs_fresh="fresh")
    assert isinstance(result, AdmissionRefusal_v0)
    assert result.reason == "exploratory_tier_expired"


# ---------------------------------------------------------------------------
# Gate 12 (LB) — AsyncDeliveryAccepted_v1 supersets v0.
# ---------------------------------------------------------------------------


def test_async_delivery_accepted_v1_supersets_v0():
    """Every v0 body (with quote=None or dict-shaped quote conforming to
    QuoteEnvelope_v0 shape) parses under v1."""
    # v0 body with quote=None.
    v0_null_body = AsyncDeliveryAccepted_v0(
        objective_id="obj-super-1",
        delivery_estimate="PT5M",
        trace_id="trc-super-1",
        accepted_at="2026-07-04T00:00:00+00:00",
    )
    v1_null = AsyncDeliveryAccepted_v1.model_validate(v0_null_body.model_dump(mode="python"))
    assert v1_null.quote is None

    # v0 body with a conforming quote dict → v1 parses + narrows type.
    inner = QuoteInstrumentationSeed_v0(
        shape_ref="shape:super",
        price_model_version="price-model@v0-exploratory",
    )
    q = QuoteEnvelope_v0(
        quote_id="q-super-1", trace_id="trc-super-1",
        quoted_at="2026-07-04T00:00:00+00:00",
        price_model_version="price-model@v0-exploratory",
        pricing_tier="exploratory",
        figure="USD 10.00", qualifying_volume="~1 refs",
        delivery_estimate="PT30S", delivery_class="warm_qualified",
        feasible_and_offerable=True, instrumentation_seed=inner,
    )
    v0_quoted = AsyncDeliveryAccepted_v0(
        objective_id="obj-super-2", delivery_estimate="PT5M",
        trace_id="trc-super-2", accepted_at="2026-07-04T00:00:00+00:00",
        quote=q.model_dump(mode="python"),
    )
    v1_quoted = AsyncDeliveryAccepted_v1.model_validate(v0_quoted.model_dump(mode="python"))
    assert isinstance(v1_quoted.quote, QuoteEnvelope_v0)


# ---------------------------------------------------------------------------
# Gate 13 (LB) — Delivery time has EXACTLY TWO bands (Axis 4 override).
# ---------------------------------------------------------------------------


def test_delivery_time_has_exactly_two_bands():
    """QuoteEnvelope_v0.delivery_class Literal MUST enumerate exactly two values."""
    schema = QuoteEnvelope_v0.model_json_schema()
    delivery_class_enum = schema["properties"]["delivery_class"]["enum"]
    assert set(delivery_class_enum) == {"warm_qualified", "fresh_extraction"}, (
        f"HAZARD-STOP — delivery_class MUST have exactly two bands "
        f"(Owner ruling Axis 4, 2026-07-04). Got: {delivery_class_enum}"
    )
    assert set(_delivery_time.DELIVERY_CLASSES) == {"warm_qualified", "fresh_extraction"}


# ---------------------------------------------------------------------------
# Gate 15 — admission_refusal_reasons.v3.json extends v2 additively.
# ---------------------------------------------------------------------------


def test_admission_refusal_v3_extends_v2_additively():
    v2 = json.loads((SERVICES_DIR / "service_1" / "admission_refusal_reasons.v2.json").read_text())
    v3 = json.loads((SERVICES_DIR / "service_1" / "admission_refusal_reasons.v3.json").read_text())
    v2_reasons = {e["reason"] for e in v2["valid_reasons"]}
    v3_reasons = {e["reason"] for e in v3["valid_reasons"]}
    assert v2_reasons.issubset(v3_reasons), (
        f"v3 MUST additively extend v2. Missing from v3: {v2_reasons - v3_reasons}"
    )
    new_codes = v3_reasons - v2_reasons
    assert new_codes == {
        "fleet_policy_reserved_zero_capacity",
        "pricing_tier_frozen_by_control_surface",
        "exploratory_tier_expired",
    }, f"Unexpected v3 additions: {new_codes}"


# ---------------------------------------------------------------------------
# Gate 16 — Master Admin gated pricing writes (§6.1 UI Spec surface).
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_master_admin_gated_pricing_writes(monkeypatch):
    """Write endpoints refuse without Master Admin auth header."""
    monkeypatch.delenv("RMS_MASTER_ADMIN_TOKEN", raising=False)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # No env var set → deployment does not carry Master Admin → 403.
        r = await client.post("/api/pricing/tier_lock", params={"locked": True})
        assert r.status_code == 403
        r2 = await client.post("/api/fleet/policy")
        assert r2.status_code == 403

    # With env var set + correct header → passes gate (501 = not-yet-implemented).
    monkeypatch.setenv("RMS_MASTER_ADMIN_TOKEN", "test-master-token")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.post(
            "/api/pricing/tier_lock",
            params={"locked": False, "reason_note": "test"},
            headers={"X-RMS-Master-Admin": "test-master-token"},
        )
        assert r.status_code == 200
        r2 = await client.post(
            "/api/fleet/policy",
            headers={"X-RMS-Master-Admin": "test-master-token"},
        )
        assert r2.status_code == 501


# ---------------------------------------------------------------------------
# Gate 17 — No arbitration beyond apportionment in fleet_policy.v0.json.
# ---------------------------------------------------------------------------


def test_no_arbitration_beyond_apportionment_in_fleet_policy_json():
    """Ruling R4-SD2 — arbitration-under-contention DEFERRED. Config MUST
    NOT carry active arbitration keys beyond the apportionment map."""
    assert _fleet_policy.has_arbitration_beyond_apportionment() is False


# ---------------------------------------------------------------------------
# Gate 18 — HAZARD-STOP-NOTES present in all economics modules.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("module_name", [
    "delivery_time.py",
    "fleet_policy.py",
    "instrumentation.py",
    "price_model.py",
    "quote_service.py",
    "expiry.py",
])
def test_hazard_stop_notes_in_all_economics_modules(module_name: str):
    """Every economics module MUST carry HAZARD-STOP-NOTES referencing
    G2b block or Ruling R4-SD2 deferral."""
    p = SERVICES_DIR / "economics" / module_name
    text = p.read_text(encoding="utf-8")
    assert "HAZARD-STOP-NOTES" in text or "HAZARD-STOP" in text, (
        f"{module_name} MUST carry HAZARD-STOP-NOTES per §8 bullet 1 doctrine."
    )


# ---------------------------------------------------------------------------
# Extra — quote_service returns FormNotOfferable when form has null multiplier.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_form_not_quotable_returns_form_not_offerable():
    """`callable_skill` and `knowledge_artifact` have null multipliers →
    `form_not_offerable` refusal until §6.3/§6.4 lands."""
    request = ObjectiveRequest_v2.model_validate(_valid_body(
        form="callable_skill", grain="synthesized_whole",
    ))
    result = await _quote_service.issue_quote(request, "trc-form-null", warm_vs_fresh="fresh")
    assert isinstance(result, AdmissionRefusal_v0)
    assert result.reason == "form_not_offerable"


# ---------------------------------------------------------------------------
# Extra — pricing router reads.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pricing_read_endpoints_live():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r1 = await client.get("/api/pricing/model_version")
        assert r1.status_code == 200
        body = r1.json()
        assert body["price_model_version"].startswith("price-model@v")
        assert "expires_at" in body

        r2 = await client.get("/api/pricing/tiers")
        assert r2.status_code == 200
        assert r2.json()["valid_tiers"][0]["tier"] == "exploratory"

        r3 = await client.get("/api/fleet/policy")
        assert r3.status_code == 200
        assert "apportionment" in r3.json()
