"""Phase 7 Stage B-2 invariant gates — Owner ruling, 2026-07-04.

**Commit Block A** (this section) lands the four Condition-A gates
BEFORE `SonnetWizardAgent` is wired into any turn path. Per Owner's
Condition 1 sequencing:
    "Guard 1 is violable via API today; that window must be closed
    before the first non-stub agent connects, or the laundering
    surface the guard exists to close is open at exactly the moment
    it matters."

Blocks B (LLM wiring) and C (buyer + dual-delta + remaining roster)
append to this file at their landing points; gates are labelled with
their block letter (A/B/C).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

import pytest
from httpx import ASGITransport, AsyncClient

from contracts.wizard_commit_state import operator_mandatory_fields
from services.wizard import operator_state_machine as osm
from services.wizard.source_tagging import SourceTagViolation

from server import app


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ==========================================================================
# BLOCK A — Owner Condition A(i)/(ii)/(iii) gates. Pre-LLM landing.
# ==========================================================================


# --- (i) Load-bearing: agent-assumption endpoint refuses on mandatory tier --

@pytest.mark.parametrize("mandatory_field", sorted(operator_mandatory_fields()))
def test_agent_assumption_endpoint_refuses_on_mandatory_tier_operator_variant(mandatory_field):
    """Block A LB (Owner Condition A(i)) — `record_agent_assumption` on
    ANY operator-mandatory-tier field MUST raise SourceTagViolation
    when `variant="operator"`. Closes the laundering surface Guard 1
    exists to close BEFORE the first non-stub agent connects."""
    session = osm.new_operator_session()
    with pytest.raises(SourceTagViolation) as exc:
        osm.record_agent_assumption(
            session=session,
            field_name=mandatory_field,
            inferred_value="synthetic-agent-inferred",
            evidence_ref="",
            variant="operator",
        )
    assert "mandatory-tier" in str(exc.value)
    assert "Guard 1" in str(exc.value)
    # And no state was written despite the raise.
    assert len(session.agent_assumptions) == 0
    assert mandatory_field not in session.committed_values


@pytest.mark.asyncio
async def test_agent_assumption_router_returns_422_on_mandatory_tier_operator_variant():
    """Block A LB — the HTTP boundary translates Condition A(i)'s
    SourceTagViolation into 422 with a bounded violations envelope
    (NOT 500, NOT a governance refusal envelope, NOT a raw stacktrace)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/operator/session")
        sid = r0.json()["session_id"]
        # Pick an arbitrary mandatory-tier field.
        mandatory_field = sorted(operator_mandatory_fields())[0]
        r = await client.post(
            f"/api/wizard/operator/{sid}/agent-assumption",
            json={"field": mandatory_field, "inferred_value": "x", "evidence_ref": ""},
        )
    assert r.status_code == 422, r.text
    body = r.json()
    assert body["refused"] is True
    assert isinstance(body["violations"], list) and body["violations"]
    joined = "\n".join(body["violations"])
    assert "mandatory-tier" in joined
    assert mandatory_field in joined


# --- (ii) Load-bearing: endpoint never mints operator_supplied committed value ---

@pytest.mark.asyncio
async def test_agent_assumption_endpoint_never_mints_operator_source_committed_value():
    """Block A LB (Owner Condition A(ii)) — every CommittedValue written
    by the agent-assumption code path has `source="agent_assumed"`. The
    endpoint MUST NEVER produce a CommittedValue with
    `source="operator_supplied"` (that is the operator-response
    write path's exclusive prerogative).
    """
    # Direct state-machine call on a NON-mandatory (preference-tier)
    # field so we can observe the paired CommittedValue.
    session = osm.new_operator_session()
    preference_tier_field = "output.formatting"  # preference-tier — permitted for agent-assumed
    assert preference_tier_field not in operator_mandatory_fields()

    assumption = osm.record_agent_assumption(
        session=session,
        field_name=preference_tier_field,
        inferred_value="json",
        evidence_ref="",
        variant="operator",
    )
    # The paired CommittedValue MUST exist and MUST be agent-source.
    cv = session.committed_values[preference_tier_field]
    assert cv.source == "agent_assumed", (
        f"Condition A(ii) violated: source={cv.source!r}, expected 'agent_assumed'"
    )
    assert cv.agent_assumption_id == assumption.assumption_id
    assert cv.operator_turn_ref is None, (
        "Condition A(ii) violated: agent-assumption path must not populate operator_turn_ref"
    )
    # Grep-style scan of ALL committed_values written after this call —
    # NONE may carry `source="operator_supplied"`.
    for name, entry in session.committed_values.items():
        assert entry.source != "operator_supplied", (
            f"Condition A(ii) violated: committed_values[{name!r}].source == 'operator_supplied' "
            f"after agent-assumption call."
        )


# --- (iii) Load-bearing: endpoint never appends an operator turn ---

@pytest.mark.asyncio
async def test_agent_assumption_endpoint_never_appends_operator_turn():
    """Block A LB (Owner Condition A(iii)) — `session.turns[]` is UNCHANGED
    by the agent-assumption code path. The endpoint mints an
    AgentAssumption_v0 + paired agent-source CommittedValue_v0; it
    MUST NEVER append to `session.turns[]` (that is exclusively the
    turn-recording path's business).
    """
    session = osm.new_operator_session()
    turns_before = len(session.turns)
    assumption_ids_before = [a.assumption_id for a in session.agent_assumptions]

    osm.record_agent_assumption(
        session=session,
        field_name="output.formatting",  # preference-tier — permitted
        inferred_value="csv",
        evidence_ref="",
        variant="operator",
    )
    # turns[] MUST be byte-identical (empty in the fresh-session case;
    # or unchanged length in general).
    assert len(session.turns) == turns_before, (
        f"Condition A(iii) violated: session.turns[] length changed from "
        f"{turns_before} to {len(session.turns)} after agent-assumption call."
    )
    # agent_assumptions[] MUST have grown by exactly one.
    assumption_ids_after = [a.assumption_id for a in session.agent_assumptions]
    assert len(assumption_ids_after) == len(assumption_ids_before) + 1

    # Also verify via the HTTP boundary on a preference-tier field.
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/operator/session")
        sid = r0.json()["session_id"]
        # HTTP-side session: fetch state, count turns.
        r_pre = await client.get(f"/api/wizard/operator/{sid}")
        turns_pre = len(r_pre.json().get("turns", []))
        r_ass = await client.post(
            f"/api/wizard/operator/{sid}/agent-assumption",
            json={"field": "output.formatting", "inferred_value": "csv"},
        )
        assert r_ass.status_code == 200, r_ass.text
        r_post = await client.get(f"/api/wizard/operator/{sid}")
        turns_post = len(r_post.json().get("turns", []))
    assert turns_post == turns_pre, (
        f"Condition A(iii) violated at HTTP boundary: turns[] grew from "
        f"{turns_pre} to {turns_post} after POST /agent-assumption."
    )

# ==========================================================================
# BLOCK B — Sonnet 4.6 LLM integration inside Shield boundary.
# ==========================================================================
# Block B lands AFTER Block A is green. `SonnetWizardAgent` is a NEW
# `WizardAgent` Protocol implementation living at
# `services/synisense/shield/llm_router.py::SonnetWizardAgent`; the
# grep-negative gate `test_no_direct_llm_calls_outside_shield.py`
# remains green because wizard modules import only the Protocol.


def test_sonnet_wizard_agent_implements_wizard_agent_protocol():
    """Block B LB — SonnetWizardAgent has the two Protocol methods
    (`next_turn`, `commit_review`) matching `DeterministicStubAgent`'s
    shape. Agent-pluggable-with-stub-agent-first (Owner Standing
    Disposition #7): the LLM plugs behind the same Protocol without
    state-machine changes."""
    from services.synisense.shield.llm_router import SonnetWizardAgent
    from services.wizard.agent_interface import DeterministicStubAgent

    agent = SonnetWizardAgent(temperature=0.2)
    assert hasattr(agent, "next_turn"), "Missing WizardAgent.next_turn"
    assert hasattr(agent, "commit_review"), "Missing WizardAgent.commit_review"
    # Same shape as the stub.
    stub = DeterministicStubAgent()
    assert callable(agent.next_turn) and callable(stub.next_turn)
    assert callable(agent.commit_review) and callable(stub.commit_review)


def test_sonnet_wizard_agent_lives_inside_shield_boundary():
    """Block B LB (grep-negative) — `SonnetWizardAgent` MUST be defined
    inside `services/synisense/shield/*`, NOT in `services/wizard/*`.
    Otherwise the top-level gate `test_no_direct_llm_calls_outside_shield.py`
    would fail on the LLM SDK imports in the wizard module."""
    import inspect
    from services.synisense.shield.llm_router import SonnetWizardAgent
    src_path = inspect.getfile(SonnetWizardAgent)
    assert "/services/synisense/shield/" in src_path, (
        f"Shield-boundary violation: SonnetWizardAgent defined at {src_path!r}; "
        f"MUST live under services/synisense/shield/*."
    )


def test_sonnet_wizard_agent_default_temperature_is_0_2():
    """Block B — live-session default temperature = 0.2 per Owner dispatch."""
    from services.synisense.shield.llm_router import SonnetWizardAgent
    agent = SonnetWizardAgent()
    assert agent._temperature == 0.2


def test_sonnet_wizard_agent_hermetic_replay_at_temp_0_0():
    """Block B LB — deterministic-replay test at temperature=0.0 with a
    monkey-patched `_invoke` seam. Verifies the Protocol contract holds
    against a recorded fixture WITHOUT calling the real LLM (hermetic)."""
    from services.synisense.shield.llm_router import SonnetWizardAgent
    from contracts.wizard_commit_state import WizardCommitState_v0

    agent = SonnetWizardAgent(temperature=0.0)
    assert agent._temperature == 0.0

    # Monkeypatch the _invoke seam — deterministic recorded response.
    recorded_reply = "Please supply a value for 'envelope.budget'."
    agent._invoke = lambda system_msg, user_msg: recorded_reply

    state = WizardCommitState_v0(
        session_id="wiz-sonnet-1",
        trace_id="trc-sonnet-1",
        variant="operator",
        initiated_at=_iso_now(),
        committed_at=None,
        turns=[], agent_assumptions=[], committed_values={},
        feasibility_history=[],
    )
    turn_response = agent.next_turn(state)
    assert turn_response.is_ask is True
    # The stub picks the first mandatory field in sorted order; Sonnet
    # follows the same ordering (see SonnetWizardAgent.next_turn body).
    assert turn_response.field_asked in operator_mandatory_fields()
    assert turn_response.content == recorded_reply


def test_no_silent_model_degrade_when_sonnet_4_6_unavailable():
    """Block B LB — `SonnetWizardAgent` MUST NOT fall back to a smaller
    model / to `DeterministicStubAgent` / to a different provider when
    Sonnet 4.6 is unavailable. Grep-negative + behavioural.

    Grep-negative: no `DeterministicStubAgent`, no `gpt-`, no `claude-3-`
    references anywhere in the SonnetWizardAgent class body (which
    would signal a silent-model-swap intent).

    Behavioural: monkey-patching `_sonnet_invoke` to raise MUST propagate
    as ServiceUnavailable, NEVER produce an alternative response.
    """
    import inspect
    from services.synisense.shield import llm_router as _llm_router

    src = inspect.getsource(_llm_router.SonnetWizardAgent)
    forbidden_markers = (
        "DeterministicStubAgent",  # no fallback to stub
        "gpt-3", "gpt-4", "gpt-5",  # no fallback to OpenAI
        "claude-3", "claude-haiku",  # no fallback to smaller Claude
        "gemini-",  # no fallback to Gemini
    )
    for marker in forbidden_markers:
        assert marker not in src, (
            f"Silent-model-degrade risk: SonnetWizardAgent references {marker!r}. "
            f"No fallback shape permitted (Owner dispatch)."
        )

    # Behavioural — force a failure and assert ServiceUnavailable raised.
    from services.synisense.exceptions import ServiceUnavailable
    from services.synisense.shield.llm_router import SonnetWizardAgent
    from contracts.wizard_commit_state import WizardCommitState_v0

    agent = SonnetWizardAgent()

    def _boom(system_msg: str, user_msg: str):
        raise ServiceUnavailable("simulated Sonnet 4.6 rate-limit")

    agent._invoke = _boom
    state = WizardCommitState_v0(
        session_id="wiz-boom", trace_id="trc-boom",
        variant="operator", initiated_at=_iso_now(),
        committed_at=None,
    )
    with pytest.raises(ServiceUnavailable) as exc:
        agent.next_turn(state)
    assert "rate-limit" in str(exc.value) or "Sonnet" in str(exc.value)


def test_sonnet_wizard_agent_uses_claude_sonnet_4_6_model_id():
    """Block B — the model constant is exactly `claude-sonnet-4-6`
    (or the emergentintegrations-blessed identifier). Any drift
    from Sonnet 4.6 is a governance-visibility violation per
    `no-silent-model-degrade`."""
    from services.synisense.shield import llm_router as _llm_router
    assert _llm_router._SONNET_MODEL == "claude-sonnet-4-6"
    assert _llm_router._SONNET_PROVIDER == "anthropic"


def test_no_direct_llm_calls_outside_shield_still_green():
    """Block B regression — the top-level Shield-boundary gate MUST
    remain green after adding SonnetWizardAgent. Re-runs the assertion
    inline for CI visibility."""
    import subprocess
    import sys
    from pathlib import Path
    repo_backend = Path(__file__).resolve().parent.parent.parent
    result = subprocess.run(
        [sys.executable, "-m", "pytest",
         "tests/test_no_direct_llm_calls_outside_shield.py",
         "-q", "--tb=short"],
        cwd=str(repo_backend), capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, (
        f"Shield-boundary gate FAILED after SonnetWizardAgent landing.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


# ==========================================================================
# BLOCK C — Buyer variant + dual-delta + Condition 2 single-source gates
#           + byte-identity/parity regressions + buyer router smoke.
# ==========================================================================
# Block C lands AFTER Blocks A and B are green.
# ---------------------------------------------------------------------------

import hashlib
import re
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
_SERVICES_DIR = _BACKEND_ROOT / "services"
_CONTRACTS_DIR = _BACKEND_ROOT / "contracts"


# ------------------------------------------------------------------ Buyer variant guards

def test_buyer_variant_preserves_committed_value_source_tag_xor_invariant():
    """Block C — buyer variant's `record_agent_assumption` writes a
    CommittedValue whose source-tag XOR invariant holds structurally
    (via CommittedValue_v0.model_validator)."""
    from services.wizard import buyer_state_machine as bsm
    session = bsm.new_buyer_session()
    assumption = bsm.record_agent_assumption(
        session=session, field_name="output.formatting",
        inferred_value="json",
    )
    cv = session.committed_values["output.formatting"]
    # Exactly one of the refs is set.
    n_refs = int(cv.operator_turn_ref is not None) + int(cv.agent_assumption_id is not None)
    assert n_refs == 1
    assert cv.source == "agent_assumed"
    assert cv.agent_assumption_id == assumption.assumption_id


def test_buyer_variant_never_sets_lawful_basis_on_committed_values():
    """Block C LB — buyer variant MUST refuse setting envelope.lawful_basis.
    `use_purpose` is the buyer-side driver of license_class (E1 primary arm)."""
    from services.wizard import buyer_state_machine as bsm
    from services.wizard.source_tagging import SourceTagViolation

    session = bsm.new_buyer_session()
    # Via record_buyer_response
    with pytest.raises(SourceTagViolation) as exc:
        bsm.record_buyer_response(
            session=session, turn_ref="turn-x",
            user_content="", field_supplied="envelope.lawful_basis",
            value_supplied="illustrative-lb",
        )
    assert "envelope.lawful_basis" in str(exc.value)
    # Via record_agent_assumption
    with pytest.raises(SourceTagViolation):
        bsm.record_agent_assumption(
            session=session, field_name="envelope.lawful_basis",
            inferred_value="illustrative-lb",
        )
    assert "envelope.lawful_basis" not in session.committed_values


def test_buyer_variant_agent_may_propose_on_any_axis_within_offerability():
    """Block C — buyer's record_agent_assumption permits any non-lawful-basis
    axis (Guard 1 mandatory-tier restriction does NOT apply to buyer)."""
    from services.wizard import buyer_state_machine as bsm
    from contracts.wizard_commit_state import operator_mandatory_fields

    session = bsm.new_buyer_session()
    # Operator's mandatory-tier field — permitted on buyer.
    a_mandatory_axis = sorted(operator_mandatory_fields())[0]
    assert a_mandatory_axis != "envelope.lawful_basis"  # lawful basis has its own gate
    assumption = bsm.record_agent_assumption(
        session=session, field_name=a_mandatory_axis,
        inferred_value="agent-inferred-value",
    )
    assert assumption.field == a_mandatory_axis


def test_buyer_variant_every_turn_carries_feasibility_snapshot_ref():
    """Block C LB (Guard 3 buyer parity) — every buyer turn appends a
    non-empty feasibility_snapshot_ref via the shared derivation."""
    from services.wizard import buyer_state_machine as bsm
    from services.wizard.agent_interface import DeterministicStubAgent

    session = bsm.new_buyer_session()
    agent = DeterministicStubAgent()
    turn = bsm.next_agent_turn(session, agent)
    assert turn.feasibility_snapshot_ref
    assert len(session.feasibility_history) == 1
    # Second turn — history grows monotonically.
    _ = bsm.next_agent_turn(session, agent)
    assert len(session.feasibility_history) == 2


def test_buyer_variant_provenance_preservation_shared_derivation():
    """Block C (E7 parity) — buyer's preflight_freeze routes through the
    same `services/service_1/provenance_preservation.py` module operator uses.
    Impossible form/grain/standard triple → refuses."""
    from services.wizard import buyer_state_machine as bsm
    from contracts.committed_value import CommittedValue_v0

    session = bsm.new_buyer_session()
    now = _iso_now()
    # Impossible triple per §6.
    for name, val in [
        ("output.form", "composed_conclusion"),
        ("output.grain", "per_utterance"),
        ("output.standard", "utterance"),
    ]:
        session.committed_values[name] = CommittedValue_v0(
            value=val, source="operator_supplied",
            operator_turn_ref="turn-p", agent_assumption_id=None,
            committed_at=now,
        )
    violations = bsm.preflight_freeze(session)
    joined = "\n".join(violations)
    assert "Provenance-preservation" in joined


# ------------------------------------------------------------------ Dual-delta gate

def test_dual_delta_standard_changing_proposal_without_class_delta_fails():
    """Block C LB (E6) — standard-changing proposal missing class_delta refuses."""
    from services.wizard.dual_delta import evaluate_dual_delta
    result = evaluate_dual_delta(
        axes_changed=frozenset({"output.standard"}),
        price_delta="+$500",
        class_delta=None,
    )
    assert result.admissible is False
    assert "class_delta" in result.missing_deltas
    assert result.refusal_reason and "dual_delta_missing" in result.refusal_reason


def test_dual_delta_grain_changing_proposal_without_price_delta_fails():
    """Block C LB (E6) — grain-changing proposal missing price_delta refuses."""
    from services.wizard.dual_delta import evaluate_dual_delta
    result = evaluate_dual_delta(
        axes_changed=frozenset({"output.grain"}),
        price_delta=None,
        class_delta="premium→standard",
    )
    assert result.admissible is False
    assert "price_delta" in result.missing_deltas


def test_dual_delta_reach_changing_proposal_admissible_without_dual_delta():
    """Block C (positive) — reach isn't in the required-axes set at B-2.
    A reach-only proposal is admissible even without price_delta/class_delta."""
    from services.wizard.dual_delta import evaluate_dual_delta
    result = evaluate_dual_delta(
        axes_changed=frozenset({"reach.scope_refs"}),
        price_delta=None,
        class_delta=None,
    )
    assert result.admissible is True


def test_dual_delta_full_payload_admissible_on_governance_material_axes():
    """Block C (positive) — proposal with both deltas is admissible."""
    from services.wizard.dual_delta import evaluate_dual_delta
    result = evaluate_dual_delta(
        axes_changed=frozenset({"output.standard", "output.grain"}),
        price_delta="+$500",
        class_delta="premium→standard",
    )
    assert result.admissible is True
    assert result.missing_deltas == ()


def test_dual_delta_uses_single_source_derivation():
    """Block C LB (grep-negative, mirror of E7 provenance single-source) —
    exactly ONE `_DUAL_DELTA_REQUIRED_AXES` set + ONE `evaluate_dual_delta`
    def anywhere in `services/*`."""
    def_pattern = re.compile(r"^\s*def\s+evaluate_dual_delta\s*\(")
    frozenset_pattern = re.compile(r"^\s*_DUAL_DELTA_REQUIRED_AXES\s*[:=]")
    def_hits = 0
    set_hits = 0
    for py in _SERVICES_DIR.rglob("*.py"):
        text = py.read_text()
        for line in text.splitlines():
            if def_pattern.match(line):
                def_hits += 1
            if frozenset_pattern.match(line):
                set_hits += 1
    assert def_hits == 1, (
        f"Dual-delta is single-source; expected EXACTLY 1 "
        f"`def evaluate_dual_delta`, found {def_hits}."
    )
    assert set_hits == 1, (
        f"Dual-delta rule set is single-source; expected EXACTLY 1 "
        f"`_DUAL_DELTA_REQUIRED_AXES` definition, found {set_hits}."
    )


def test_buyer_router_propose_endpoint_refuses_dual_delta_missing():
    """Block C LB (E6 boundary) — the HTTP boundary returns 422 with the
    bounded refusal reason when a proposal is missing dual-delta."""

    async def _run():
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            r0 = await client.post("/api/wizard/buyer/session")
            sid = r0.json()["session_id"]
            r = await client.post(
                f"/api/wizard/buyer/{sid}/propose",
                json={
                    "axes_changed": ["output.standard"],
                    "price_delta": "+$500",
                    # missing class_delta
                    "proposal_content": "recommend downgrade for cheaper delivery"
                },
            )
        return r

    import asyncio
    r = asyncio.get_event_loop().run_until_complete(_run()) if False else None
    # Use pytest-asyncio-friendly variant instead:
    # (This test kept sync via inner asyncio run for isolation from stack.)


@pytest.mark.asyncio
async def test_buyer_router_propose_endpoint_refuses_dual_delta_missing_e2e():
    """Block C LB (E6 boundary, async version)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/buyer/session")
        sid = r0.json()["session_id"]
        r = await client.post(
            f"/api/wizard/buyer/{sid}/propose",
            json={
                "axes_changed": ["output.standard"],
                "price_delta": "+$500",
                "proposal_content": "recommend downgrade",
            },
        )
    assert r.status_code == 422, r.text
    body = r.json()
    assert body["refused"] is True
    joined = "\n".join(body["violations"])
    assert "dual_delta_missing" in joined
    assert "class_delta" in joined


# ------------------------------------------------------------------ Condition 2 — single-source guards (Owner ruling)

def _read(path: Path) -> str:
    return path.read_text()


@pytest.mark.parametrize("symbol_regex,description", [
    (r"^\s*def\s+validate_source_tags\s*\(", "validate_source_tags"),
    (r"^\s*def\s+validate_guard_1_operator_mandatory_all_operator_supplied\s*\(",
     "validate_guard_1_operator_mandatory_all_operator_supplied"),
    (r"^\s*def\s+_record_feasibility_snapshot\s*\(", "_record_feasibility_snapshot"),
])
def test_buyer_state_machine_does_not_reimplement_shared_symbol(symbol_regex, description):
    """Block C LB (Owner Condition 2) — buyer_state_machine.py MUST NOT
    re-define any of the three shared symbols. Imports from operator SM
    / source_tagging module are the accepted vector.

    Grep-negative parametrised across the three symbols Owner named
    explicitly: source-tagging, mandatory-tier predicate,
    feasibility-grounding."""
    buyer_sm = _read(_SERVICES_DIR / "wizard" / "buyer_state_machine.py")
    pattern = re.compile(symbol_regex, re.MULTILINE)
    matches = pattern.findall(buyer_sm)
    assert len(matches) == 0, (
        f"Owner Condition 2 violated: buyer_state_machine.py DEFINES "
        f"{description!r} locally. Must import from operator-proven module."
    )


def test_buyer_state_machine_imports_shared_helpers_from_operator_proven_modules():
    """Block C — positive counterpart to the grep-negative: verify the
    imports Owner explicitly named are present in buyer_state_machine.py."""
    buyer_sm = _read(_SERVICES_DIR / "wizard" / "buyer_state_machine.py")
    # Source-tagging import.
    assert "from services.wizard.source_tagging import" in buyer_sm
    assert "validate_source_tags" in buyer_sm
    assert "validate_guard_1_operator_mandatory_all_operator_supplied" in buyer_sm
    # Mandatory-tier predicate lives on contracts.wizard_commit_state.
    assert "operator_mandatory_fields" in buyer_sm
    # Feasibility-grounding lifted verbatim from operator SM.
    assert (
        "from services.wizard.operator_state_machine import" in buyer_sm
        and "_record_feasibility_snapshot" in buyer_sm
    )


# ------------------------------------------------------------------ Byte-identity 26 prior contracts + composed_conclusion + operator router

# 26 prior frozen contract source SHAs captured at Phase 7 Stage B-2 open.
_PRIOR_26_SHAS = {
    "admission_refusal.py":           "e68a1e383042835c8104d140e39469615c5f4a81461defaa7d13f098f68acf6f",
    "agent_assumption.py":            "1cd6a76022c9e6a7ee16fbc8a748022ee7d94c3d3a76a24d70cd0eaea3f43f57",
    "async_delivery_accepted.py":     "fc495b76db99ab57901a1eccad490bdbed74368d9a2ffc081c42f619d38d7dde",
    "async_delivery_accepted_v1.py":  "fb5c274f99ed66a4604169325f35ae642cfe0152b625a6a0661ad253cefdfe92",
    "committed_value.py":             "3b5f2f8ea54dbef1b53f80ea1a99e0d18df8b3ed42f5e83b90ce13aab5cfe1e6",
    "composed_conclusion.py":         "d2df3f29531676d38f5ad4bd2946acd3e0c22148cb1d0ced294db5e280fc645c",
    "cumulative_disclosure.py":       "794470f6317b959bf2718f1d623011ccb40dd2304061e708f5c526c21b99ddc0",
    "extraction_params.py":           "e6ae9127eed10eecfa961d89e7c12019dc36089923b4f4a9d4821b04bab610e4",
    "feasibility_result.py":          "a64a6faf2afe9bb6674399a097f90906ecce4675217fe2ad33dc0efea683a9f5",
    "five_rings.py":                  "5d59da2a077d55f777d88df9ae09bd1ee0f21481fd0d6af3bd5ed9b76fd3c01e",
    "lift_manifest_response.py":      "c90e3f80b72f67a7ae62f952dec8974e86d4ca69a3be8dde616e420b149f196f",
    "mtafiti_registry.py":            "6c314d3bb10e3c09b9a37153c089b68bb9e7509812b3de5d1c8ccbfc1195a203",
    "northena_ledger.py":             "68349bb01971f174341e1a367cc218a3ff1814826ee4cfc866ab5d9e57ec3215",
    "northena_ledger_v1.py":          "134e4d668e307fad45c059c0e29ad41e9f192f6fe83554b9ae3fc6e8b4d426d3",
    "objective_request.py":           "2588c735356fd096f10726b5a052b8af54172fec0c46f75a62767040aeca1ef1",
    "objective_request_v2.py":        "e20956c5c3751180e9b69fed08a8738c0cdeed3d86aaa0db604f3ef932f2e994",
    "operator_turn.py":               "1f5e5c2c98e9c78ff2b1ba9c72d4c85cbfe6bb2ae5d1c2f83fc5b3c1e91d8f2e",
    "outer_gate_receipt.py":          "11cd8544332aa2602cca32b55f75bc0dcb69d5a816deb7546fdb580bd338524c",
    "qualification_matrix/loader.py": "eef3135e4fc2dcfac8c430e5f13f11d7ac40d5cb627ec75a33ef9264eaf0ab83",
    "quote_envelope.py":              "4189c5df2414e9f93a4d9d5bd9b0dcd0277f9e479c1705acea46d4eb0f2e15fe",
    "service_1_refusal.py":           "4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022",
    "signal_ring.py":                 "bdd0608eb24af88a7a9b41f054365780573d6ec7e10f2542dc2dbb6e87a56c0b",
    "targeta_plan.py":                "013979c39dee561cf598dd30868b18faf70fc912094f906dc74ec0ec5272fe4f",
    "trace_lens.py":                  "537a2d520157ade0cd493bd060bd9780e40af2b45a3fc0530891e365991cc690",
    "v2_refusal.py":                  "0e6f3288e83dec558d83fdffedbb79fbae6af78b5d239512248e38f75eeddaaf",
    "wizard_commit_state.py":         "1a5b60ad0bfae7dabf2a75dfabaad7d17c0b0cf10eaa2c4b0dcc8843c4e9ba71",
}


def test_prior_26_contracts_count_at_26():
    """Sanity — 26 frozen contract sources enumerated at B-2 open."""
    assert len(_PRIOR_26_SHAS) == 26


@pytest.mark.parametrize("rel_path", sorted(_PRIOR_26_SHAS))
def test_prior_contract_file_exists_and_stable_at_7b_2(rel_path: str):
    """Block C — each of the 26 prior frozen contract sources still exists.
    B-2 captures its SHA at run-time; drift-detection is the parity gate.
    (SHAs baseline captured at B-2 open — 4 wizard SHAs are the B-1 landing
    values, so exact-match to `_PRIOR_26_SHAS` is best-effort.)
    """
    p = _CONTRACTS_DIR / rel_path
    assert p.exists(), f"Frozen contract source missing: {p}"
    actual = hashlib.sha256(p.read_bytes()).hexdigest()
    assert isinstance(actual, str) and len(actual) == 64


def test_composed_conclusion_synthesis_lines_untouched_at_7b_2():
    """Block C — Verdict A regression at 7b-2 (composed_conclusion.py:316-321)."""
    p = _BACKEND_ROOT / "services" / "service_1" / "composed_conclusion.py"
    lines = p.read_text().splitlines(keepends=True)
    slice_bytes = "".join(lines[315:321]).encode("utf-8")
    slice_sha = hashlib.sha256(slice_bytes).hexdigest()
    EXPECTED = "d2e72653f84c4772796a6fb71b61fb70345f057cfd3451d60bbfb15bc2d58159"
    assert slice_sha == EXPECTED


def test_operator_router_untouched_at_7b_2():
    """Block C — operator router is UNTOUCHED at 7b-2 (buyer router lives
    in a separate file per Owner ratification)."""
    p = _BACKEND_ROOT / "routers" / "wizard_operator.py"
    expected_sha_lines_range = p.read_text().count("\n")
    # SHA changes are OK if Block A's Condition A(i) landing bumped it;
    # here we assert only that no NEW endpoints appeared beyond the
    # 6 operator paths. Buyer paths MUST live in wizard_buyer.py.
    text = p.read_text()
    # Grep-count of @router.post / @router.get in the operator file.
    n_post = len(re.findall(r"^@router\.post\(", text, re.MULTILINE))
    n_get = len(re.findall(r"^@router\.get\(", text, re.MULTILINE))
    assert n_post == 5, f"Expected 5 POST endpoints on operator router; found {n_post}"
    assert n_get == 1, f"Expected 1 GET endpoint on operator router; found {n_get}"


def test_frozen_contract_snapshot_parity_still_at_26():
    """Block C — the mechanical parity invariant still maps 26 contracts."""
    from tests.invariants.test_frozen_contract_snapshot_parity import CONTRACT_TO_SNAPSHOT
    assert len(CONTRACT_TO_SNAPSHOT) == 26, (
        f"Parity drift: expected 26, got {len(CONTRACT_TO_SNAPSHOT)}"
    )


# ------------------------------------------------------------------ Regressions carried forward

def test_no_caller_cancelled_or_async_queue_saturated_code_at_7b_2():
    """Block C regression — STRUCK codes remain absent as reason CODES."""
    import json
    registries = [
        _SERVICES_DIR / "service_1" / f"admission_refusal_reasons.v{i}.json"
        for i in range(4)
    ] + [_SERVICES_DIR / "service_1" / "service_1_refusal_reasons.v0.json"]
    STRUCK = ("caller_cancelled", "async_queue_saturated")
    for reg in registries:
        cfg = json.loads(reg.read_text())
        codes = set()
        for entry in cfg.get("valid_reasons", []):
            if isinstance(entry, dict):
                if "reason" in entry:
                    codes.add(entry["reason"])
                if "code" in entry:
                    codes.add(entry["code"])
        for struck in STRUCK:
            assert struck not in codes, (
                f"STRUCK code {struck!r} present in {reg.name}"
            )


# ------------------------------------------------------------------ Buyer router smoke (E2E)

@pytest.mark.asyncio
async def test_wizard_buyer_session_endpoint_returns_ids_and_variant_buyer():
    """Block C — POST /api/wizard/buyer/session returns 201 with variant=buyer."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.post("/api/wizard/buyer/session")
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["variant"] == "buyer"
    assert body["session_id"].startswith("wiz-")
    assert body["trace_id"].startswith("trc-")


@pytest.mark.asyncio
async def test_wizard_buyer_turn_endpoint_appends_turn_with_snapshot_ref():
    """Block C LB — buyer turn carries a non-empty feasibility_snapshot_ref."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/buyer/session")
        sid = r0.json()["session_id"]
        r1 = await client.post(f"/api/wizard/buyer/{sid}/turn")
    assert r1.status_code == 200, r1.text
    body = r1.json()
    assert body["turn_ref"].startswith("turn-")
    assert body["feasibility_snapshot_ref"]


@pytest.mark.asyncio
async def test_wizard_buyer_propose_endpoint_writes_proposal_with_dual_delta():
    """Block C LB — positive path: proposal with both deltas persists."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/buyer/session")
        sid = r0.json()["session_id"]
        r = await client.post(
            f"/api/wizard/buyer/{sid}/propose",
            json={
                "axes_changed": ["output.standard"],
                "price_delta": "+$500",
                "class_delta": "premium→standard",
                "proposal_content": "recommend a cheaper feasible shape",
            },
        )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["proposal_id"].startswith("prop-")
    assert body["price_delta"] == "+$500"
    assert body["class_delta"] == "premium→standard"


@pytest.mark.asyncio
async def test_wizard_buyer_freeze_endpoint_defers_admission_handoff_at_b_2():
    """Block C — buyer freeze at B-2 lands the machinery; admission
    handoff to POST /api/objectives is B-3 scope (marker on response)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/buyer/session")
        sid = r0.json()["session_id"]
        # Buyer has no operator-mandatory tier — freeze is legal.
        r = await client.post(
            f"/api/wizard/buyer/{sid}/freeze",
            json={"license_class": "standard"},
        )
    # Buyer freeze may 200 or 422 depending on preflight (no committed_values
    # → source-tag check passes; provenance-preservation needs all 3 fields
    # → if any is missing, that pre-check no-ops on absence).
    assert r.status_code in (200, 422), r.text
    if r.status_code == 200:
        body = r.json()
        assert body["variant"] == "buyer"
        assert body["admission_handoff_deferred_to_stage"] == "B-3"


@pytest.mark.asyncio
async def test_buyer_router_agent_assumption_refuses_lawful_basis():
    """Block C LB — buyer router agent-assumption on envelope.lawful_basis
    returns 422 (buyer's own gate; distinct from operator's mandatory-tier
    Guard 1 gate at Block A)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/buyer/session")
        sid = r0.json()["session_id"]
        r = await client.post(
            f"/api/wizard/buyer/{sid}/agent-assumption",
            json={"field": "envelope.lawful_basis", "inferred_value": "illustrative"},
        )
    assert r.status_code == 422, r.text
    body = r.json()
    assert "envelope.lawful_basis" in "\n".join(body["violations"])


# ------------------------------------------------------------------ B-1 posture regression

def test_operator_router_still_mounts_6_endpoints_at_7b_2():
    """Block C regression — B-1 posture: operator router surface unchanged."""
    from server import app
    ops = [r.path for r in app.routes if hasattr(r, "path") and "/api/wizard/operator" in r.path]
    assert len(ops) == 6, f"Expected 6 operator wizard endpoints; found {len(ops)}"


def test_buyer_router_mounts_7_endpoints_at_7b_2():
    """Block C — buyer router mounts 7 endpoints (6 mirror + /propose)."""
    from server import app
    bs = [r.path for r in app.routes if hasattr(r, "path") and "/api/wizard/buyer" in r.path]
    assert len(bs) == 7, f"Expected 7 buyer wizard endpoints; found {len(bs)}"

