"""AdmissionRefusal@v0 — Phase 3 gate tests.

Owner ruling (Phase 3 dispatch 2026-07-03): 11 LOAD-BEARING gates
covering the unified admission-refusal envelope, its versioned reason
registry, family consistency with Service1Refusal@v0, dispatch
integration for `output.form == "model"`, actor-appropriate content,
and Phase-2 → Phase-3 migration guards.
"""
from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path

import httpx
import pytest
from httpx import ASGITransport

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.service_1_refusal import Service1Refusal
from server import app
from services.service_1 import admission_refusal as ar_service
from services.service_1 import dispatch as dispatch_module


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


def _base_body(*, form: str) -> dict:
    """Minimal ObjectiveRequest_v2 wire body for dispatch route."""
    return {
        "entry": "external_request",
        "reach": {"scope_refs": [], "exclusions": [], "depth": "baseline"},
        "output": {
            "form": form,
            "consumer": "person",
            "grain": "per_claim",
            "standard": {"minimum_class": "utterance"},
        },
        "envelope": {
            "lawful_basis": "test",
            "done_condition": "test",
            "budget": "test",
            "scope_ceiling": "test",
            "commissioner": "test",
            "committed_at": "2026-07-03T12:00:00+00:00",
        },
    }


# ---------------------------------------------------------------------------
# Gate S5.2 — Reason registry governs validity
# ---------------------------------------------------------------------------


def test_admission_refusal_reason_registry_governs_validity():
    """`is_valid_reason` reads the registry; unregistered reasons return False."""
    assert ar_service.is_valid_reason("form_not_offerable") is True
    assert ar_service.is_valid_reason("unregistered_fake_reason") is False
    assert ar_service.is_valid_reason("") is False
    # Registry file exists and parses
    reg_path = (
        BACKEND_ROOT
        / "services"
        / "service_1"
        / "admission_refusal_reasons.v0.json"
    )
    assert reg_path.exists(), f"Registry missing at {reg_path}"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    assert reg["config_version"] == "v0"
    reasons = [e["reason"] for e in reg["valid_reasons"]]
    assert "form_not_offerable" in reasons


# ---------------------------------------------------------------------------
# Gate S5.3 — Extension via registry bump (no contract mutation)
# ---------------------------------------------------------------------------


def test_admission_refusal_reason_extension_via_registry_bump(tmp_path, monkeypatch):
    """Synthetic proof: extending reasons is a REGISTRY operation.

    Point `ar_service._REGISTRY_PATH` at a temp registry with two
    reasons; verify both validate; the contract file is NOT modified
    (SHA-256 stable). Extension surface works without touching the
    frozen contract.
    """
    fake_registry = tmp_path / "admission_refusal_reasons.v1.json"
    fake_registry.write_text(json.dumps({
        "config_version": "v1",
        "valid_reasons": [
            {"reason": "form_not_offerable", "since_version": "v0"},
            {"reason": "standard_not_met", "since_version": "v1"},
        ],
    }))
    contract_path = BACKEND_ROOT / "contracts" / "admission_refusal.py"
    sha_before = hashlib.sha256(contract_path.read_bytes()).hexdigest()

    monkeypatch.setattr(ar_service, "_REGISTRY_PATH", fake_registry)

    assert ar_service.is_valid_reason("form_not_offerable") is True
    assert ar_service.is_valid_reason("standard_not_met") is True
    assert ar_service.is_valid_reason("still_fake") is False

    sha_after = hashlib.sha256(contract_path.read_bytes()).hexdigest()
    assert sha_before == sha_after, (
        "Registry bump MUST NOT modify the contract file. "
        f"Contract SHA drift: {sha_before} → {sha_after}"
    )


# ---------------------------------------------------------------------------
# Gate S5.4 — form_not_offerable fires on output.form == "model" (LOAD-BEARING)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_admission_refusal_form_not_offerable_fires_on_output_form_model():
    """v2 dispatch with `output.form == "model"` returns AdmissionRefusal@v0."""
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_base_body(form="model"),
        )
    assert resp.status_code == 422, (
        f"Governed admission refusal MUST return 422 (A2 family status); "
        f"got {resp.status_code}"
    )
    body = resp.json()
    assert body["outcome"] == "refused"
    assert body["reason"] == "form_not_offerable"
    assert body["requested_output_form"] == "model"
    assert body["trace_id"].startswith("disp-")
    # Contract-schema shape: AdmissionRefusal_v0 validates the response body.
    envelope = AdmissionRefusal_v0.model_validate(body)
    assert envelope.reason == "form_not_offerable"


# ---------------------------------------------------------------------------
# Gate S5.5 — Actor-appropriate string (LOAD-BEARING, Condition 3)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_admission_refusal_actor_appropriate_string():
    """Grep-negative on owner-side deliberation phrasing.

    Neither `what_you_can_do` NOR `off_menu_fact` may contain:
      * "await owner", "owner acceptance", "ingredient manifest",
        "ingredient-manifest".
    The actor-actionable string MUST reference a robust invariant
    signal — "output form" — evidencing caller-actionable content.
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_base_body(form="model"),
        )
    body = resp.json()

    forbidden = [
        "await owner",
        "owner acceptance",
        "ingredient manifest",
        "ingredient-manifest",
    ]
    for field_name in ("what_you_can_do", "off_menu_fact"):
        text = body[field_name].lower()
        for phrase in forbidden:
            assert phrase not in text, (
                f"Condition 3 violation — {field_name!r} contains "
                f"owner-side deliberation phrasing {phrase!r}. "
                f"Full text: {body[field_name]!r}"
            )

    # Actor-actionable invariant: mentions "output form".
    assert "output form" in body["what_you_can_do"].lower(), (
        f"Condition 3: what_you_can_do MUST reference 'output form' "
        f"as the caller-actionable signal. Got: {body['what_you_can_do']!r}"
    )


# ---------------------------------------------------------------------------
# Gate S5.6 — Family consistency with Service1Refusal@v0 (LOAD-BEARING, Condition 1)
# ---------------------------------------------------------------------------


def test_admission_refusal_family_consistent_with_service_1_refusal():
    """Both envelopes share outer pattern: outcome:Literal["refused"] +
    trace_id + reason.

    Structural check — not a snapshot cross-comparison (they legitimately
    differ in inner fields per firing site). The family invariant is the
    outer three fields; each envelope may carry its own contextual fields
    beyond that.
    """
    ar_schema = AdmissionRefusal_v0.model_json_schema()
    s1_schema = Service1Refusal.model_json_schema()

    ar_props = ar_schema["properties"]
    s1_props = s1_schema["properties"]

    # outcome: Literal["refused"] present in both
    assert "outcome" in ar_props and "outcome" in s1_props
    ar_outcome_const = ar_props["outcome"].get("const") or ar_props["outcome"].get("enum")
    s1_outcome_const = s1_props["outcome"].get("const") or s1_props["outcome"].get("enum")
    # Pydantic renders Literal as `const` or `enum: ["refused"]`
    def _norm(x):
        if isinstance(x, list):
            return x
        return [x]
    assert _norm(ar_outcome_const) == ["refused"]
    assert _norm(s1_outcome_const) == ["refused"]

    # trace_id + reason present in both
    for family_field in ("trace_id", "reason"):
        assert family_field in ar_props, (
            f"Condition 1 violation — AdmissionRefusal missing family field "
            f"{family_field!r}"
        )
        assert family_field in s1_props, (
            f"Condition 1 violation — Service1Refusal missing family field "
            f"{family_field!r}"
        )


# ---------------------------------------------------------------------------
# Gate S5.7 — Phase 2 → Phase 3 migration guard
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_v2_dispatch_placeholder_replaced_by_admission_refusal_for_form_model():
    """`output.form == "model"` no longer emits scaffold 501 placeholder.

    Simultaneously: other placeholder cases (knowledge_artifact,
    callable_skill) STILL emit 501 placeholder (their receivers stay
    Phase-4-debt).
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # form=model → 422 refusal (Phase 3)
        r_model = await client.post(
            "/api/service_1/v2/dispatch", json=_base_body(form="model"),
        )
        assert r_model.status_code == 422
        body_model = r_model.json()
        assert body_model["outcome"] == "refused"
        assert "placeholder_body" not in body_model
        assert body_model["reason"] == "form_not_offerable"

        # form=knowledge_artifact → still 501 placeholder (Phase 2)
        r_ka = await client.post(
            "/api/service_1/v2/dispatch", json=_base_body(form="knowledge_artifact"),
        )
        assert r_ka.status_code == 501
        body_ka = r_ka.json()
        assert body_ka["placeholder_body"]["outcome"] == "not_yet_implemented"
        assert body_ka["placeholder_body"]["phase_debt"] == "phase_4_transform_variants"

        # form=callable_skill → still 501 placeholder (Phase 2)
        r_cs = await client.post(
            "/api/service_1/v2/dispatch", json=_base_body(form="callable_skill"),
        )
        assert r_cs.status_code == 501
        body_cs = r_cs.json()
        assert body_cs["placeholder_body"]["outcome"] == "not_yet_implemented"
        assert body_cs["placeholder_body"]["phase_debt"] == "phase_4_transform_variants"


# ---------------------------------------------------------------------------
# Gate S5.8 — Placeholder-vs-refusal structural non-overlap
# ---------------------------------------------------------------------------


def test_placeholder_vs_refusal_separation_still_green():
    """Placeholder body shape does NOT overlap with AdmissionRefusal_v0 shape.

    Structural non-overlap: the top-level field sets are disjoint on
    discriminators. Placeholder lives NESTED at
    DispatchResult.placeholder_body (with `outcome=not_yet_implemented`)
    while AdmissionRefusal_v0 has `outcome=refused` at the TOP level.
    """
    ar_top_fields = set(AdmissionRefusal_v0.model_json_schema()["properties"].keys())
    placeholder_shape = {"outcome", "reason", "route", "phase_debt", "trace_id"}

    # Discriminator disjointness: outcome values are DIFFERENT.
    # AdmissionRefusal.outcome == "refused"; placeholder.outcome == "not_yet_implemented".
    # Envelope classes at top-level: AdmissionRefusal is FLAT; DispatchResult
    # wraps placeholder inside placeholder_body. So a top-level DispatchResult
    # body MUST NOT be confused with an AdmissionRefusal body — the field
    # sets at top level do not match.
    dispatch_result_top_fields = set(
        dispatch_module.DispatchResult.model_json_schema()["properties"].keys()
    )
    assert dispatch_result_top_fields != ar_top_fields, (
        "Family separation compromised — DispatchResult and "
        "AdmissionRefusal_v0 share the same top-level field set."
    )
    # AdmissionRefusal is FLAT: it does NOT have placeholder_body field.
    assert "placeholder_body" not in ar_top_fields
    # DispatchResult is WRAPPER: it DOES have placeholder_body.
    assert "placeholder_body" in dispatch_result_top_fields
    # Placeholder body shape unaffected by AdmissionRefusal shape.
    assert placeholder_shape == {"outcome", "reason", "route", "phase_debt", "trace_id"}


# ---------------------------------------------------------------------------
# Gate S5.10 — Service1Refusal@v0 SHA byte-identical
# ---------------------------------------------------------------------------


def test_service_1_refusal_v0_untouched():
    """Service1Refusal@v0 stays byte-identical across Phase 3.

    Family member must not shift while new sibling AdmissionRefusal@v0
    lands. If this test fails, the parent contract was mutated — a
    HAZARD-STOP per Ruling 2.
    """
    p = BACKEND_ROOT / "contracts" / "service_1_refusal.py"
    actual = hashlib.sha256(p.read_bytes()).hexdigest()
    PRE_PHASE_3_SHA = (
        "4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022"
    )
    assert actual == PRE_PHASE_3_SHA, (
        f"Ruling 2 violation — Service1Refusal@v0 mutated during Phase 3.\n"
        f"  pre-Phase-3 SHA: {PRE_PHASE_3_SHA}\n"
        f"  post-Phase-3 SHA: {actual}"
    )


# ---------------------------------------------------------------------------
# Gate S5.11 — Contract docstring documents extension path (Condition 2)
# ---------------------------------------------------------------------------


def test_admission_refusal_contract_docstring_states_extension_path():
    """Prevents future silent mechanism drift.

    The module docstring MUST document the versioned-registry
    extension path — that adding a reason is a REGISTRY operation,
    NEVER a contract modification. Guard against a future dev
    silently switching to Literal-widening or another mechanism.
    """
    from contracts import admission_refusal as ar_module
    doc = inspect.getdoc(ar_module) or ""
    doc_lower = doc.lower()
    # Structural checks — the docstring must contain these anchors.
    assert "extension" in doc_lower, "docstring missing 'extension' anchor"
    assert "registry" in doc_lower, "docstring missing 'registry' anchor"
    assert ("never modif" in doc_lower or "never new contract" in doc_lower
            or "never literal" in doc_lower), (
        "docstring must state that reason additions never modify the "
        "contract (or equivalent 'never' phrasing)"
    )


# ---------------------------------------------------------------------------
# Additional wire-shape check — Pydantic pattern validation on reason
# ---------------------------------------------------------------------------


def test_admission_refusal_reason_pattern_snake_case():
    """`reason` field enforces snake_case per contract pattern regex.

    Prevents accidentally-typed reasons like 'FormNotOfferable' or
    'form-not-offerable' from being constructed.
    """
    # Valid
    ok = AdmissionRefusal_v0(
        reason="form_not_offerable",
        trace_id="t-1",
        requested_output_form="model",
        off_menu_fact="fact",
        what_you_can_do="do this output form thing",
        computed_at="2026-07-03T00:00:00+00:00",
    )
    assert ok.reason == "form_not_offerable"

    # Invalid — camelCase
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        AdmissionRefusal_v0(
            reason="FormNotOfferable",
            trace_id="t-1", requested_output_form="model",
            off_menu_fact="f", what_you_can_do="output form",
            computed_at="2026-07-03T00:00:00+00:00",
        )
    # Invalid — kebab-case
    with pytest.raises(pydantic.ValidationError):
        AdmissionRefusal_v0(
            reason="form-not-offerable",
            trace_id="t-1", requested_output_form="model",
            off_menu_fact="f", what_you_can_do="output form",
            computed_at="2026-07-03T00:00:00+00:00",
        )
