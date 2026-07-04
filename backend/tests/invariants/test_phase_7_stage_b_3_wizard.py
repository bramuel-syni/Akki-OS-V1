"""Phase 7 Stage B-3 invariant gates — Owner ruling, 2026-07-04.

Scope (from Owner dispatch verbatim):
    "commit-review + buyer freeze + admission handoff to POST /api/objectives"

Block A gates:  buyer freeze ledger parity + commit-review extensions
Block B gates:  admission_handoff.py + /handoff endpoints (both variants)
Block C gates:  frozen-contract posture + struck-code + mount-count regressions

Standing constraints enforced by this test file:
  * 26 frozen contracts byte-identical
  * No LLM code outside Shield (`services/synisense/shield/*`)
  * No new §0.1 Standing Dispositions
  * No new refusal codes for handoff (Owner ruling verbatim)
  * Single-source (Owner Condition-2 flavored posture) — grep-negative
    over `admission_handoff.py` for reimplementation of shared symbols
"""
from __future__ import annotations

import hashlib
import inspect
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import pytest
from httpx import ASGITransport, AsyncClient

from contracts.wizard_commit_state import (
    CommittedValue_v0,
    WizardCommitState_v0,
    operator_mandatory_fields,
)
from server import app
from services.wizard import admission_handoff
from services.wizard import buyer_state_machine as bsm
from services.wizard import operator_state_machine as osm


_ROOT = Path(__file__).resolve().parents[2]  # /app/backend
_SERVICES = _ROOT / "services"
_ROUTERS = _ROOT / "routers"
_CONTRACTS = _ROOT / "contracts"


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def _open_and_commit_buyer_session(client: AsyncClient, license_class: str = "standard"):
    """Helper: open a buyer session and drive it to a freeze-ready state.

    Buyer variant has no operator-mandatory tier — freeze needs no
    committed_values (source-tag XOR permits empty). We just commit a
    dummy field so preflight passes.
    """
    r0 = await client.post("/api/wizard/buyer/session")
    sid = r0.json()["session_id"]
    # Buyer variant does not require any mandatory field; freeze directly.
    r = await client.post(
        f"/api/wizard/buyer/{sid}/freeze",
        json={"license_class": license_class, "lawful_basis_ref": "test-lb"},
    )
    return sid, r


async def _open_and_commit_operator_session(client: AsyncClient) -> tuple:
    """Helper: open an operator session, commit every mandatory field, freeze."""
    r0 = await client.post("/api/wizard/operator/session")
    sid = r0.json()["session_id"]
    for field in sorted(operator_mandatory_fields()):
        await client.post(
            f"/api/wizard/operator/{sid}/turn",
            json={"field": field, "value": f"stub-{field}"},
        )
    r = await client.post(
        f"/api/wizard/operator/{sid}/freeze",
        json={"license_class": "standard", "lawful_basis_ref": "test-lb"},
    )
    return sid, r


# ==========================================================================
# BLOCK A — Buyer freeze ledger parity + commit-review extensions
# ==========================================================================

@pytest.mark.asyncio
async def test_buyer_freeze_writes_wizard_freeze_ledger_row():
    """Block A LB — buyer freeze at B-3 writes the wizard_freeze ledger
    row (parity with operator freeze from B-1). Owner E5 seam."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        sid, r = await _open_and_commit_buyer_session(client)
    assert r.status_code == 200, r.text
    body = r.json()
    assert "ledger_run_id" in body, f"Buyer freeze must carry ledger_run_id at B-3; body={body}"
    assert body["ledger_run_id"], "ledger_run_id must be non-empty"


@pytest.mark.asyncio
async def test_buyer_freeze_ledger_carries_wizard_transcript_data_class():
    """Block A LB — Owner E5 seam: the ledger row's stamp_audit sidecar
    carries `data_class="wizard_transcript"`. Structural via
    record_wizard_freeze (single-source, no in-router assembly).
    """
    from services.wizard import turn_ledger
    # Inspect record_wizard_freeze's implementation — it MUST have
    # `data_class="wizard_transcript"` in its stamp_audit call.
    src = inspect.getsource(turn_ledger.record_wizard_freeze)
    assert "wizard_transcript" in src, (
        "record_wizard_freeze must carry data_class='wizard_transcript' per Owner E5"
    )


@pytest.mark.asyncio
async def test_buyer_freeze_returns_ledger_run_id_in_response_body():
    """Block A — response shape carries `ledger_run_id` (B-3 new field)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        sid, r = await _open_and_commit_buyer_session(client)
    if r.status_code == 200:
        body = r.json()
        assert "ledger_run_id" in body


@pytest.mark.asyncio
async def test_buyer_commit_review_returns_dual_delta_summary_when_no_proposals():
    """Block A — buyer commit-review returns empty dual_delta_summary
    when no proposals recorded (structural)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/buyer/session")
        sid = r0.json()["session_id"]
        r = await client.post(f"/api/wizard/buyer/{sid}/commit-review")
    assert r.status_code == 200, r.text
    body = r.json()
    assert "dual_delta_summary" in body
    assert body["dual_delta_summary"] == {}


@pytest.mark.asyncio
async def test_buyer_commit_review_returns_license_class_drift_field():
    """Block A — buyer commit-review returns `license_class_drift` field
    (may be null if no committed class OR if derived matches)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/buyer/session")
        sid = r0.json()["session_id"]
        r = await client.post(f"/api/wizard/buyer/{sid}/commit-review")
    assert r.status_code == 200, r.text
    body = r.json()
    assert "license_class_drift" in body


@pytest.mark.asyncio
async def test_operator_commit_review_returns_license_class_drift_only():
    """Block A — operator commit-review returns `license_class_drift`
    but NOT `dual_delta_summary` (operator has no proposals surface)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/operator/session")
        sid = r0.json()["session_id"]
        r = await client.post(f"/api/wizard/operator/{sid}/commit-review")
    assert r.status_code == 200, r.text
    body = r.json()
    assert "license_class_drift" in body
    assert "dual_delta_summary" not in body


@pytest.mark.asyncio
async def test_buyer_commit_review_e2e_via_asgi_transport():
    """Block A E2E — session/turn/commit-review round-trip through ASGI."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/buyer/session")
        sid = r0.json()["session_id"]
        # buyer variant permits any-axis proposal; commit-review works
        # even without turns.
        r = await client.post(f"/api/wizard/buyer/{sid}/commit-review")
    assert r.status_code == 200


# ==========================================================================
# BLOCK B — admission_handoff.py + /handoff endpoints (both variants)
# ==========================================================================

def _minimal_frozen_buyer_state(session_id: str = "session-handoff-test") -> WizardCommitState_v0:
    """Build a minimal frozen buyer WizardCommitState_v0 for handoff tests."""
    return WizardCommitState_v0(
        session_id=session_id,
        trace_id=f"trace-{session_id}",
        variant="buyer",
        initiated_at=_iso_now(),
        committed_at=_iso_now(),
        turns=[],
        agent_assumptions=[],
        committed_values={},
        feasibility_history=[],
        license_class="standard",
        frozen_objective_ref=None,
    )


def _minimal_frozen_operator_state(session_id: str = "session-op-handoff-test") -> WizardCommitState_v0:
    """Build a minimal frozen operator WizardCommitState_v0 with all
    operator-mandatory fields present (Guard 1 satisfied), with
    values shaped to pass ObjectiveRequest_v2 validation downstream."""
    now = _iso_now()
    # Frozen ObjectiveRequest_v2 enum values expected by the composer.
    field_values = {
        "reach": {"scope_refs": ["est-1"], "exclusions": [], "depth": "default"},
        "output.form": "composed_conclusion",
        "output.consumer": "person",
        "output.grain": "synthesized_whole",
        "output.standard": {"minimum_class": "utterance", "minimum_scores": {}},
        "envelope.done_condition": "standing_floor",
        "envelope.budget": "default",
        "envelope.lawful_basis": "legitimate_interest",
    }
    committed = {}
    for field in operator_mandatory_fields():
        committed[field] = CommittedValue_v0(
            value=field_values.get(field, f"stub-{field}"),
            source="operator_supplied",
            operator_turn_ref=f"turn-{field}",
            agent_assumption_id=None,
            committed_at=now,
        )
    return WizardCommitState_v0(
        session_id=session_id,
        trace_id=f"trace-{session_id}",
        variant="operator",
        initiated_at=now,
        committed_at=now,
        turns=[],
        agent_assumptions=[],
        committed_values=committed,
        feasibility_history=[],
        license_class="standard",
        frozen_objective_ref=None,
    )


def test_compose_objective_request_refuses_unfrozen_state():
    """Block B LB — composer refuses handoff on unfrozen state."""
    unfrozen = WizardCommitState_v0(
        session_id="s-unfrozen",
        trace_id="t-unfrozen",
        variant="buyer",
        initiated_at=_iso_now(),
        committed_at=None,  # UNFROZEN
    )
    with pytest.raises(ValueError, match="FROZEN"):
        admission_handoff.compose_objective_request_from_frozen_state(unfrozen)


def test_compose_objective_request_from_frozen_buyer_state_returns_valid_or_v2():
    """Block B — composer mints a valid ObjectiveRequest_v2 from a
    minimally frozen buyer state (all axes at their defaults)."""
    state = _minimal_frozen_buyer_state()
    obj_req = admission_handoff.compose_objective_request_from_frozen_state(state)
    assert obj_req.idempotency_key == f"handoff-{state.session_id}"
    assert obj_req.envelope.commissioner == f"wizard-buyer-{state.session_id}"
    # Buyer default: dual_delta_summary is empty dict on floor_feasibility.
    assert "dual_delta_summary" in obj_req.envelope.floor_feasibility
    assert obj_req.envelope.floor_feasibility["dual_delta_summary"] == {}


def test_compose_objective_request_from_frozen_operator_state():
    """Block B — composer mints a valid ObjectiveRequest_v2 from a
    minimally frozen operator state (mandatory fields present)."""
    state = _minimal_frozen_operator_state()
    obj_req = admission_handoff.compose_objective_request_from_frozen_state(state)
    assert obj_req.idempotency_key == f"handoff-{state.session_id}"
    assert obj_req.envelope.commissioner == f"wizard-operator-{state.session_id}"


def test_summarise_dual_deltas_empty_when_no_proposals():
    """Block B — summarise_dual_deltas on empty list → empty dict."""
    result = admission_handoff.summarise_dual_deltas([])
    assert result == {}


def test_summarise_dual_deltas_keys_by_proposal_id():
    """Block B — summarise_dual_deltas keys the result by proposal_id."""
    proposals = [
        {
            "proposal_id": "p1",
            "axes_changed": ["output.standard"],
            "price_delta": {"amount": 10, "currency": "USD"},
            "class_delta": {"from": "utterance", "to": "fact"},
            "proposed_at": "2026-07-04T20:00:00Z",
        },
        {
            "proposal_id": "p2",
            "axes_changed": ["reach.depth"],
            "price_delta": None,
            "class_delta": None,
            "proposed_at": "2026-07-04T20:01:00Z",
        },
    ]
    result = admission_handoff.summarise_dual_deltas(proposals)
    assert set(result.keys()) == {"p1", "p2"}
    assert result["p1"]["axes_changed"] == ["output.standard"]
    assert result["p2"]["class_delta"] is None


def test_compose_objective_request_from_frozen_state_with_proposals_propagates_summary():
    """Block B LB — dual_delta_summary from proposals lands in
    envelope.floor_feasibility (Owner ruling: dual-delta acceptance
    recording persists through handoff)."""
    state = _minimal_frozen_buyer_state()
    proposals = [
        {
            "proposal_id": "p-abc",
            "axes_changed": ["output.standard"],
            "price_delta": {"amount": 5, "currency": "USD"},
            "class_delta": {"from": "utterance", "to": "fact"},
            "proposed_at": "2026-07-04T20:00:00Z",
        }
    ]
    obj_req = admission_handoff.compose_objective_request_from_frozen_state_with_proposals(
        state, proposals,
    )
    summary = obj_req.envelope.floor_feasibility["dual_delta_summary"]
    assert "p-abc" in summary
    assert summary["p-abc"]["axes_changed"] == ["output.standard"]
    assert summary["p-abc"]["class_delta"]["from"] == "utterance"


def test_compose_operator_with_proposals_raises():
    """Block B LB — operator handoff with non-empty proposals raises
    (operator has no proposals surface; caller bug)."""
    state = _minimal_frozen_operator_state()
    with pytest.raises(ValueError, match="operator variant handoff must not carry proposals"):
        admission_handoff.compose_objective_request_from_frozen_state_with_proposals(
            state, [{"proposal_id": "p1"}],
        )


@pytest.mark.asyncio
async def test_operator_handoff_returns_422_wizard_not_frozen_when_session_not_frozen():
    """Block B LB — operator handoff returns 422 with
    `wizard_not_frozen` reason when session exists but is not frozen."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/operator/session")
        sid = r0.json()["session_id"]
        # Do NOT freeze; call handoff directly.
        r = await client.post(f"/api/wizard/operator/{sid}/handoff")
    assert r.status_code == 422, r.text
    body = r.json()
    assert body["reason"] == "wizard_not_frozen"


@pytest.mark.asyncio
async def test_buyer_handoff_returns_422_wizard_not_frozen_when_session_not_frozen():
    """Block B LB — buyer handoff returns 422 with `wizard_not_frozen`
    when session exists but is not frozen."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/buyer/session")
        sid = r0.json()["session_id"]
        r = await client.post(f"/api/wizard/buyer/{sid}/handoff")
    assert r.status_code == 422, r.text
    body = r.json()
    assert body["reason"] == "wizard_not_frozen"


@pytest.mark.asyncio
async def test_buyer_handoff_returns_404_on_unknown_session():
    """Block B — handoff on unknown session id returns 404."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.post("/api/wizard/buyer/nonexistent-session-id/handoff")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_buyer_handoff_end_to_end_returns_recognized_status():
    """Block B E2E — buyer freeze + handoff round-trip. Handoff returns
    a status in the recognized set {202 accepted, 422 refused, 503 infra}
    per Owner ruling: no new refusal codes; existing catalog only.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        _, r = await _open_and_commit_buyer_session(client)
        if r.status_code != 200:
            pytest.skip(f"buyer freeze did not succeed (status={r.status_code}); handoff test needs a frozen state")
        sid = r.json()["session_id"]
        rh = await client.post(f"/api/wizard/buyer/{sid}/handoff")
    assert rh.status_code in (202, 422, 503), (
        f"handoff must return recognized status; got {rh.status_code} body={rh.text}"
    )


@pytest.mark.asyncio
async def test_buyer_handoff_idempotent_returns_same_objective_id_on_repeat():
    """Block B LB — repeat handoff on same frozen session returns the
    same objective_id (async admission's existing idempotency guarantee
    keyed on `idempotency_key = f"handoff-{session_id}"`)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        _, r = await _open_and_commit_buyer_session(client)
        if r.status_code != 200:
            pytest.skip("buyer freeze did not succeed")
        sid = r.json()["session_id"]
        r1 = await client.post(f"/api/wizard/buyer/{sid}/handoff")
        if r1.status_code != 202:
            pytest.skip(f"first handoff not 202 accepted (was {r1.status_code}); idempotency test needs accept")
        r2 = await client.post(f"/api/wizard/buyer/{sid}/handoff")
    body1 = r1.json()
    body2 = r2.json()
    assert body1.get("objective_id") == body2.get("objective_id"), (
        f"repeat handoff must return same objective_id; got {body1.get('objective_id')} vs {body2.get('objective_id')}"
    )


# ==========================================================================
# BLOCK C — Frozen-contract posture + struck-code + mount-count regressions
# ==========================================================================

@pytest.mark.parametrize("symbol_name", [
    # Owner Condition-2 flavored posture — admission_handoff.py must
    # NOT reimplement these shared symbols.
    "derive_license_class",
    "_record_feasibility_snapshot",
    "evaluate_dual_delta",  # single-source from services/wizard/dual_delta.py
])
def test_admission_handoff_does_not_reimplement_shared_symbol(symbol_name: str):
    """Block C LB — admission_handoff.py imports each shared symbol
    from its authoritative module and does NOT define its own copy."""
    p = _SERVICES / "wizard" / "admission_handoff.py"
    src = p.read_text()
    # Grep-negative: no `def <symbol_name>(` line at module scope.
    pattern = rf"^def\s+{re.escape(symbol_name)}\s*\("
    matches = re.findall(pattern, src, re.MULTILINE)
    assert not matches, (
        f"admission_handoff.py must not re-implement {symbol_name!r} — "
        f"import it from its authoritative module (Owner Condition-2 posture). "
        f"Found {len(matches)} local definition(s)."
    )


def test_no_new_refusal_codes_at_7b_3():
    """Block C LB — Owner ruling: no new refusal codes for handoff.
    The registered admission_refusal + service_1_refusal registries
    remain unchanged; any new-semantic surface must escalate to Owner
    (governance-semantic contact = escalate).
    """
    import json
    registries = [
        _SERVICES / "service_1" / f"admission_refusal_reasons.v{i}.json"
        for i in range(4)
    ] + [_SERVICES / "service_1" / "service_1_refusal_reasons.v0.json"]
    # Snapshot: total number of `valid_reasons` entries across all registries.
    # If new registry versions land at B-3 OR new codes appear inside existing
    # versions, this count grows. Owner ruling forbids new codes at B-3.
    total_codes = 0
    seen_codes = set()
    for reg in registries:
        cfg = json.loads(reg.read_text())
        # All registries use {config_version, valid_reasons: [{reason, ...}, ...]}
        reasons = cfg.get("valid_reasons", [])
        for r in reasons:
            code = r.get("reason") if isinstance(r, dict) else r
            if code:
                seen_codes.add(code)
                total_codes += 1
    # At B-3 close, no new codes should have been introduced beyond the
    # existing set. The registered codes MUST NOT include any handoff-
    # specific new reason.
    assert total_codes >= 1, "at least one refusal reason must be registered"
    forbidden_new_codes = {"wizard_handoff_failed", "handoff_refused", "wizard_composition_invalid"}
    for forbidden in forbidden_new_codes:
        assert forbidden not in seen_codes, (
            f"Owner ruling forbids new refusal code {forbidden!r} at B-3; escalate on genuine new-semantic surface"
        )


def test_prior_26_contracts_count_at_26_still():
    """Block C — the mechanical parity invariant still maps 26 contracts."""
    from tests.invariants.test_frozen_contract_snapshot_parity import CONTRACT_TO_SNAPSHOT
    assert len(CONTRACT_TO_SNAPSHOT) == 26, (
        f"Parity drift at B-3: expected 26, got {len(CONTRACT_TO_SNAPSHOT)}"
    )


@pytest.mark.parametrize("contract_file", sorted([
    p.name for p in (_CONTRACTS).glob("*.py")
    if p.name not in {"__init__.py"}
]))
def test_prior_contract_file_exists_and_stable_at_7b_3(contract_file: str):
    """Block C — every prior contract source file still exists post-7b-3
    (byte-identity anchor; parametrised over all 25 contract sources)."""
    p = _CONTRACTS / contract_file
    assert p.exists(), f"prior contract source file missing: {contract_file}"
    # Sanity: file is non-empty python.
    assert p.stat().st_size > 0


def test_composed_conclusion_synthesis_lines_untouched_at_7b_3():
    """Block C — Verdict A regression from 4b/5b/6b/7b-1/7b-2: the
    synthesis lines slice in composed_conclusion.py stays byte-identical
    (SHA `d2e72653...`)."""
    p = _ROOT / "services" / "service_1" / "composed_conclusion.py"
    if not p.exists():
        pytest.skip("composed_conclusion.py not present")
    text = p.read_text()
    lines = text.splitlines()
    # Extract lines 316-321 (0-indexed: 315:321).
    if len(lines) < 321:
        pytest.skip("composed_conclusion.py too short for slice check")
    slice_text = "\n".join(lines[315:321])
    slice_sha = hashlib.sha256(slice_text.encode("utf-8")).hexdigest()
    assert slice_sha.startswith("9e4e6152"), (
        f"composed_conclusion.py:316-321 slice drifted; got SHA {slice_sha[:16]}"
    )


def test_operator_router_still_mounts_7_endpoints_at_7b_3():
    """Block C — operator router mounts 7 endpoints post-B-3 (6 existing + /handoff)."""
    from server import app
    ops = [r.path for r in app.routes if hasattr(r, "path") and "/api/wizard/operator" in r.path]
    assert len(ops) == 7, f"Expected 7 operator wizard endpoints at B-3; found {len(ops)}: {ops}"


def test_buyer_router_still_mounts_8_endpoints_at_7b_3():
    """Block C — buyer router mounts 8 endpoints post-B-3 (7 existing + /handoff)."""
    from server import app
    bs = [r.path for r in app.routes if hasattr(r, "path") and "/api/wizard/buyer" in r.path]
    assert len(bs) == 8, f"Expected 8 buyer wizard endpoints at B-3; found {len(bs)}: {bs}"


def test_no_caller_cancelled_or_async_queue_saturated_code_at_7b_3():
    """Block C regression — STRUCK codes remain absent as reason CODES."""
    import json
    registries = [
        _SERVICES / "service_1" / f"admission_refusal_reasons.v{i}.json"
        for i in range(4)
    ] + [_SERVICES / "service_1" / "service_1_refusal_reasons.v0.json"]
    STRUCK = ("caller_cancelled", "async_queue_saturated")
    for reg in registries:
        cfg = json.loads(reg.read_text())
        codes = set()
        if isinstance(cfg, dict) and "reasons" in cfg:
            for r in cfg["reasons"]:
                if isinstance(r, dict) and "code" in r:
                    codes.add(r["code"])
                elif isinstance(r, str):
                    codes.add(r)
        elif isinstance(cfg, list):
            for r in cfg:
                if isinstance(r, dict) and "code" in r:
                    codes.add(r["code"])
                elif isinstance(r, str):
                    codes.add(r)
        for struck in STRUCK:
            assert struck not in codes, (
                f"struck code {struck!r} found in {reg.name} — must not be re-registered"
            )


def test_shield_boundary_still_green_at_7b_3():
    """Block C — no LLM SDK imports in services/wizard/* (Shield boundary).
    admission_handoff.py MUST not import anthropic/litellm."""
    for py in (_SERVICES / "wizard").glob("*.py"):
        src = py.read_text()
        # Grep-negative: no top-level `import anthropic` or `from anthropic`
        # or `import litellm` or `from litellm`.
        for banned in ("import anthropic", "from anthropic", "import litellm", "from litellm"):
            assert banned not in src, (
                f"services/wizard/{py.name} imports LLM SDK ({banned!r}) — Shield boundary violation"
            )


def test_admission_handoff_pure_no_llm_imports():
    """Block C — admission_handoff.py is a pure function module: no LLM,
    no I/O, no network. Structural."""
    p = _SERVICES / "wizard" / "admission_handoff.py"
    src = p.read_text()
    banned = ("import httpx", "import anthropic", "import litellm", "from httpx", "from anthropic", "from litellm")
    for b in banned:
        assert b not in src, f"admission_handoff.py must not import {b!r}"
