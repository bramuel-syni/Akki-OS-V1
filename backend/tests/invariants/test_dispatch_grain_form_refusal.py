"""Grain-form refusal at dispatch — Phase 4a gates 1 + 3.

  * Gate 1 (LOAD-BEARING) — `test_grain_compat_synthesized_whole_refused_at_qualified_data`
    v3 §6.1.4 verbatim: 'synthesized_whole unsupported (that is
    composed_conclusion)'. Dispatch @422 with reason=`grain_form_incompatible`.
  * Gate 3 — `test_grain_compat_per_claim_and_aggregated_pass_at_qualified_data`
    Positive: compatible (form, grain) pairs do NOT emit
    grain_form_incompatible.
"""
from __future__ import annotations

import httpx
import pytest
from httpx import ASGITransport

from contracts.admission_refusal import AdmissionRefusal_v0
from server import app


def _base_body(*, form: str, grain: str, scope_refs=None, idempotency_key: str = "idem-grain-test") -> dict:
    return {
        "entry": "external_request",
        "reach": {
            "scope_refs": scope_refs if scope_refs is not None else [],
            "exclusions": [],
            "depth": "baseline",
        },
        "output": {
            "form": form,
            "consumer": "person",
            "grain": grain,
            "standard": {"minimum_class": "utterance"},
        },
        "envelope": {
            "lawful_basis": "test",
            "done_condition": "test",
            "budget": "test",
            "scope_ceiling": "test",
            "commissioner": "operator_internal",
            "committed_at": "2026-07-03T12:00:00+00:00",
        },
        "idempotency_key": idempotency_key,
    }


# ---------------------------------------------------------------------------
# Gate 1 (LOAD-BEARING) — synthesized_whole × qualified_data → refusal
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_grain_compat_synthesized_whole_refused_at_qualified_data():
    """LOAD-BEARING. v3 §6.1.4 verbatim: 'synthesized_whole unsupported
    (that is composed_conclusion)'. Admission-time refusal fires with
    reason=`grain_form_incompatible` and path_forward names
    composed_conclusion.
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_base_body(form="qualified_data", grain="synthesized_whole"),
        )
    assert resp.status_code == 422, (
        f"expected 422 admission refusal; got {resp.status_code}\nbody: {resp.text}"
    )
    body = resp.json()
    envelope = AdmissionRefusal_v0.model_validate(body)
    assert envelope.reason == "grain_form_incompatible"
    assert envelope.requested_output_form == "qualified_data"
    # path_forward carries the specific fix per Ruling 7 — mentions
    # composed_conclusion as the alternative for synthesized_whole.
    assert "composed_conclusion" in envelope.what_you_can_do
    # Actor-appropriate posture — no owner-side phrasing.
    for phrase in ("await owner", "owner acceptance",
                   "ingredient manifest", "ingredient-manifest"):
        assert phrase not in envelope.what_you_can_do.lower()
        assert phrase not in envelope.off_menu_fact.lower()


# ---------------------------------------------------------------------------
# Gate 1 partner cases — composed_conclusion × per_claim / aggregated
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_grain_compat_composed_conclusion_per_claim_refused():
    """v3 §6.2.4: composed_conclusion grain synthesized_whole only.
    per_claim → grain_form_incompatible with path_forward → qualified_data.
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_base_body(form="composed_conclusion", grain="per_claim"),
        )
    assert resp.status_code == 422
    body = resp.json()
    envelope = AdmissionRefusal_v0.model_validate(body)
    assert envelope.reason == "grain_form_incompatible"
    assert "qualified_data" in envelope.what_you_can_do


# ---------------------------------------------------------------------------
# Gate 3 — positive-path: per_claim & aggregated pass at qualified_data
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_grain_compat_per_claim_and_aggregated_pass_at_qualified_data():
    """Compatible (qualified_data, per_claim) and
    (qualified_data, aggregated) pairs do NOT emit grain_form_incompatible.

    Phase 5 Stage B migration (2026-07-04): With empty reach
    (un-censused), the feasibility fork returns fresh. Fresh-fork now
    ships an AsyncDeliveryAccepted_v0 (§7 §7.1) at HTTP 202; NOT 501
    placeholder. This test verifies the grain gate did NOT fire (no
    422 grain refusal) — the terminal is a governed acceptance.
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        for i, grain in enumerate(("per_claim", "aggregated")):
            resp = await client.post(
                "/api/service_1/v2/dispatch",
                json=_base_body(
                    form="qualified_data",
                    grain=grain,
                    scope_refs=["nowhere_grain_positive"],
                    idempotency_key=f"idem-grain-positive-{i}-{grain}",
                ),
            )
            assert resp.status_code == 202, (
                f"({grain}) — expected 202 async-accepted fresh-fork for "
                f"un-censused reach; got {resp.status_code}\n"
                f"body: {resp.text}"
            )
            body = resp.json()
            # Not a grain refusal — reason field must NOT appear at top level.
            assert "reason" not in body, (
                f"({grain}) — 202 accepted body must not carry top-level "
                f"'reason' field (would signal a grain refusal leaked); got: {body}"
            )
            assert body["status"] == "accepted"


@pytest.mark.asyncio
async def test_grain_compat_composed_conclusion_synthesized_whole_bypasses_grain_gate():
    """(composed_conclusion, synthesized_whole) is compatible — bypasses
    grain refusal. Falls through to admission fork; un-censused reach →
    Phase 5 Stage B fresh-fork async acceptance (202) with
    AsyncDeliveryAccepted_v0.
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_base_body(
                form="composed_conclusion",
                grain="synthesized_whole",
                scope_refs=["nowhere_composed"],
                idempotency_key="idem-cc-sw-bypass",
            ),
        )
    assert resp.status_code == 202, (
        f"Phase 5 Stage B fresh-fork MUST return 202; got {resp.status_code}: {resp.text}"
    )
    body = resp.json()
    assert body["status"] == "accepted"
    # Not a grain refusal — no 'reason' top-level.
    assert "reason" not in body
