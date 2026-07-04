"""Phase 7 Stage B-1 — Shaping Wizard §3.3 (operator variant) invariant gates.

Test-surface roster — 27 named gates delivered against Phase 7 Stage A §7.5
scoped to B-1 (buyer-variant gates are B-2 debt).

  # 1  test_committed_value_v0_source_tag_invariant_neither_ref_set_raises        LB
  # 2  test_committed_value_v0_source_tag_invariant_both_refs_set_raises          LB
  # 3  test_committed_value_v0_operator_supplied_requires_operator_turn_ref
  # 4  test_committed_value_v0_agent_assumed_requires_agent_assumption_id
  # 5  test_wizard_commit_state_v0_freeze_refuses_agent_assumed_on_operator_mandatory_field  LB
  # 6  test_wizard_commit_state_v0_freeze_refuses_missing_operator_mandatory_field           LB
  # 7  test_wizard_commit_state_v0_freeze_refuses_orphaned_agent_assumption_ref              LB
  # 8  test_wizard_commit_state_v0_freeze_passes_when_all_guards_satisfied
  # 9  test_wizard_commit_state_v0_mid_session_permits_intermediate_content
  # 10 test_wizard_commit_state_v0_contract_frozen                                LB
  # 11 test_wizard_operator_turn_v0_contract_frozen                               LB
  # 12 test_wizard_agent_assumption_v0_contract_frozen                            LB
  # 13 test_wizard_committed_value_v0_contract_frozen                             LB
  # 14 test_ask_vs_propose_committed_mandatory_fields_all_operator_supplied       LB (parametrised)
  # 15 test_operator_variant_agent_never_proposes_on_mandatory_fields             LB
  # 16 test_wizard_feasibility_grounding_uses_shared_derivation_only              LB (grep-negative)
  # 17 test_every_wizard_turn_carries_feasibility_snapshot_ref                    LB
  # 18 test_no_second_llm_judge_in_wizard_pipeline                                (grep-negative)
  # 19 test_license_class_at_selection_equals_license_class_in_frozen_wizard_state LB
  # 20 test_license_class_mid_session_wizard_state_routes_to_fallback              LB
  # 21 test_license_class_fallback_arm_unchanged_when_no_explicit_value
  # 22 test_license_class_primary_arm_none_license_class_routes_to_fallback
  # 23 test_license_class_docstring_still_documents_phase_7_seam
  # 24 test_provenance_preservation_impossible_refuses_during_shaping             LB (E7)
  # 25 test_provenance_preservation_uses_single_source_derivation                 (grep-negative)
  # 26 test_turn_ledger_stamp_audit_sidecar_carries_wizard_transcript_data_class  LB (E5)
  # 27 test_no_caller_cancelled_or_async_queue_saturated_code_anywhere            (regression from 5b/6b)
  # 28 test_wizard_operator_session_endpoint_returns_ids
  # 29 test_wizard_operator_freeze_endpoint_refuses_on_missing_mandatory          LB
  # 30 test_wizard_operator_turn_endpoint_appends_operator_turn_with_snapshot_ref LB
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import pytest
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from contracts.agent_assumption import AgentAssumption_v0
from contracts.committed_value import CommittedValue_v0
from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from contracts.objective_request_v2 import Envelope
from contracts.operator_turn import OperatorTurn_v0
from contracts.wizard_commit_state import (
    WizardCommitState_v0,
    operator_mandatory_fields,
)
from services.service_1 import license_class_selection
from services.service_1 import provenance_preservation as _pp
from services.wizard import operator_state_machine as osm
from services.wizard.agent_interface import DeterministicStubAgent

from core import db
from server import app


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
CONTRACTS_DIR = BACKEND_ROOT / "contracts"
SERVICES_DIR = BACKEND_ROOT / "services"
INVARIANTS_DIR = Path(__file__).resolve().parent


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# --------------------------------------------------------------------------
# CommittedValue_v0 — anti-laundering XOR invariant (LB)
# --------------------------------------------------------------------------

def test_committed_value_v0_source_tag_invariant_neither_ref_set_raises():
    with pytest.raises(ValidationError) as exc:
        CommittedValue_v0(
            value="whatever",
            source="operator_supplied",
            operator_turn_ref=None,
            agent_assumption_id=None,
            committed_at=_iso_now(),
        )
    msg = str(exc.value)
    assert "exactly one of" in msg or "invariant" in msg.lower()


def test_committed_value_v0_source_tag_invariant_both_refs_set_raises():
    with pytest.raises(ValidationError) as exc:
        CommittedValue_v0(
            value="whatever",
            source="operator_supplied",
            operator_turn_ref="turn-abc",
            agent_assumption_id="asn-def",
            committed_at=_iso_now(),
        )
    msg = str(exc.value)
    assert "exactly one of" in msg or "invariant" in msg.lower()


def test_committed_value_v0_operator_supplied_requires_operator_turn_ref():
    with pytest.raises(ValidationError):
        # source='operator_supplied' but only agent_assumption_id set → refuse.
        CommittedValue_v0(
            value="whatever",
            source="operator_supplied",
            operator_turn_ref=None,
            agent_assumption_id="asn-def",
            committed_at=_iso_now(),
        )


def test_committed_value_v0_agent_assumed_requires_agent_assumption_id():
    with pytest.raises(ValidationError):
        # source='agent_assumed' but only operator_turn_ref set → refuse.
        CommittedValue_v0(
            value="whatever",
            source="agent_assumed",
            operator_turn_ref="turn-abc",
            agent_assumption_id=None,
            committed_at=_iso_now(),
        )


# --------------------------------------------------------------------------
# WizardCommitState_v0 — Guard 1/2/3 freeze-time invariants (LB)
# --------------------------------------------------------------------------

def _valid_full_committed_values(turn_ref: str) -> Dict[str, CommittedValue_v0]:
    """Build a complete committed_values dict — all 8 operator-mandatory
    fields are operator_supplied and reference one turn_ref."""
    out: Dict[str, CommittedValue_v0] = {}
    for field_name in operator_mandatory_fields():
        out[field_name] = CommittedValue_v0(
            value=f"illustrative-value-for-{field_name}",
            source="operator_supplied",
            operator_turn_ref=turn_ref,
            agent_assumption_id=None,
            committed_at=_iso_now(),
        )
    return out


def _mint_turn(turn_ref: str = "turn-abc", snap_ref: str = "feas-trc-xyz-1") -> OperatorTurn_v0:
    return OperatorTurn_v0(
        turn_ref=turn_ref, at=_iso_now(),
        user_content="operator content",
        agent_content="agent content",
        feasibility_snapshot_ref=snap_ref,
    )


def test_wizard_commit_state_v0_freeze_refuses_agent_assumed_on_operator_mandatory_field():
    """Guard 1 LB — an agent_assumed CommittedValue on a mandatory field
    at freeze MUST raise."""
    now = _iso_now()
    turn = _mint_turn()
    cvs = _valid_full_committed_values(turn.turn_ref)
    # Poison one mandatory field with agent_assumed.
    assumption = AgentAssumption_v0(
        assumption_id="asn-poison", at=now, field="output.grain",
        inferred_value="per_claim", evidence_ref="",
    )
    cvs["output.grain"] = CommittedValue_v0(
        value="per_claim",
        source="agent_assumed",
        operator_turn_ref=None,
        agent_assumption_id=assumption.assumption_id,
        committed_at=now,
    )
    with pytest.raises(ValidationError) as exc:
        WizardCommitState_v0(
            session_id="wiz-1", trace_id="trc-1",
            variant="operator", initiated_at=now,
            committed_at=now,
            turns=[turn],
            agent_assumptions=[assumption],
            committed_values=cvs,
            feasibility_history=["feas-trc-xyz-1"],
            license_class=None,
            frozen_objective_ref=None,
        )
    assert "Guard 1" in str(exc.value)


def test_wizard_commit_state_v0_freeze_refuses_missing_operator_mandatory_field():
    """Guard 1 LB — a missing operator-mandatory field at freeze MUST raise."""
    now = _iso_now()
    turn = _mint_turn()
    cvs = _valid_full_committed_values(turn.turn_ref)
    del cvs["envelope.budget"]  # remove one mandatory field
    with pytest.raises(ValidationError) as exc:
        WizardCommitState_v0(
            session_id="wiz-2", trace_id="trc-2",
            variant="operator", initiated_at=now, committed_at=now,
            turns=[turn], agent_assumptions=[], committed_values=cvs,
            feasibility_history=["feas-trc-xyz-1"],
            license_class=None, frozen_objective_ref=None,
        )
    assert "Guard 1" in str(exc.value)
    assert "envelope.budget" in str(exc.value)


def test_wizard_commit_state_v0_freeze_refuses_orphaned_agent_assumption_ref():
    """Guard 2 LB — an agent_assumed CommittedValue that references a
    non-existent assumption_id MUST raise at freeze time."""
    now = _iso_now()
    turn = _mint_turn()
    cvs = _valid_full_committed_values(turn.turn_ref)
    # Add a preference-tier field with agent_assumed pointing at a
    # NON-EXISTENT assumption_id.
    cvs["output.formatting"] = CommittedValue_v0(
        value="json",
        source="agent_assumed",
        operator_turn_ref=None,
        agent_assumption_id="asn-orphan-does-not-exist",
        committed_at=now,
    )
    with pytest.raises(ValidationError) as exc:
        WizardCommitState_v0(
            session_id="wiz-3", trace_id="trc-3",
            variant="operator", initiated_at=now, committed_at=now,
            turns=[turn], agent_assumptions=[],
            committed_values=cvs,
            feasibility_history=["feas-trc-xyz-1"],
            license_class=None, frozen_objective_ref=None,
        )
    assert "Guard 2" in str(exc.value)


def test_wizard_commit_state_v0_freeze_passes_when_all_guards_satisfied():
    now = _iso_now()
    turn = _mint_turn()
    cvs = _valid_full_committed_values(turn.turn_ref)
    frozen = WizardCommitState_v0(
        session_id="wiz-4", trace_id="trc-4",
        variant="operator", initiated_at=now, committed_at=now,
        turns=[turn], agent_assumptions=[], committed_values=cvs,
        feasibility_history=["feas-trc-xyz-1"],
        license_class="standard", frozen_objective_ref=None,
    )
    assert frozen.committed_at == now
    assert frozen.license_class == "standard"


def test_wizard_commit_state_v0_mid_session_permits_intermediate_content():
    """committed_at=None → freeze-time invariants are BYPASSED.
    Mid-session state may hold partial committed_values (Guard 1 fires
    only at freeze, not mid-session)."""
    now = _iso_now()
    turn = _mint_turn()
    partial_cvs = {
        "reach": CommittedValue_v0(
            value="illustrative", source="operator_supplied",
            operator_turn_ref=turn.turn_ref, agent_assumption_id=None,
            committed_at=now,
        )
    }
    # Missing 7 of 8 mandatory fields — mid-session permits this.
    mid = WizardCommitState_v0(
        session_id="wiz-5", trace_id="trc-5",
        variant="operator", initiated_at=now, committed_at=None,
        turns=[turn], agent_assumptions=[], committed_values=partial_cvs,
        feasibility_history=["feas-trc-xyz-1"],
    )
    assert mid.committed_at is None
    assert len(mid.committed_values) == 1


# --------------------------------------------------------------------------
# Contract-frozen snapshot invariants (LB) — the 4 wizard contracts.
# --------------------------------------------------------------------------

def _snapshot(name: str) -> dict:
    return json.loads((INVARIANTS_DIR / name).read_text(encoding="utf-8"))


def test_wizard_commit_state_v0_contract_frozen():
    live = WizardCommitState_v0.model_json_schema()
    assert live == _snapshot("wizard_commit_state.contract_snapshot.json"), (
        "WizardCommitState_v0 schema drift detected."
    )


def test_wizard_operator_turn_v0_contract_frozen():
    live = OperatorTurn_v0.model_json_schema()
    assert live == _snapshot("operator_turn.contract_snapshot.json")


def test_wizard_agent_assumption_v0_contract_frozen():
    live = AgentAssumption_v0.model_json_schema()
    assert live == _snapshot("agent_assumption.contract_snapshot.json")


def test_wizard_committed_value_v0_contract_frozen():
    live = CommittedValue_v0.model_json_schema()
    assert live == _snapshot("committed_value.contract_snapshot.json")


# --------------------------------------------------------------------------
# Ask-vs-propose LB (Guard 1 parametrised over every mandatory field).
# --------------------------------------------------------------------------

@pytest.mark.parametrize("field_name", sorted(operator_mandatory_fields()))
def test_ask_vs_propose_committed_mandatory_fields_all_operator_supplied(field_name):
    """LB — commit refuses on `agent_assumed` for ANY of the 8 mandatory
    fields, parametrised."""
    now = _iso_now()
    turn = _mint_turn()
    cvs = _valid_full_committed_values(turn.turn_ref)
    # Poison the CURRENT parametrised field with agent_assumed.
    assumption = AgentAssumption_v0(
        assumption_id=f"asn-{field_name}", at=now, field=field_name,
        inferred_value="whatever", evidence_ref="",
    )
    cvs[field_name] = CommittedValue_v0(
        value="whatever",
        source="agent_assumed",
        operator_turn_ref=None,
        agent_assumption_id=assumption.assumption_id,
        committed_at=now,
    )
    with pytest.raises(ValidationError):
        WizardCommitState_v0(
            session_id="wiz-p", trace_id="trc-p",
            variant="operator", initiated_at=now, committed_at=now,
            turns=[turn], agent_assumptions=[assumption],
            committed_values=cvs,
            feasibility_history=["feas-trc-xyz-1"],
            license_class=None, frozen_objective_ref=None,
        )


def test_operator_variant_agent_never_proposes_on_mandatory_fields():
    """LB — DeterministicStubAgent's `next_turn` ONLY asks about
    mandatory fields (is_ask=True); never returns is_ask=False with a
    recommendation on a mandatory field."""
    agent = DeterministicStubAgent()
    now = _iso_now()
    empty_state = WizardCommitState_v0(
        session_id="wiz-a", trace_id="trc-a",
        variant="operator", initiated_at=now, committed_at=None,
    )
    resp = agent.next_turn(empty_state)
    assert resp.is_ask is True
    assert resp.field_asked in operator_mandatory_fields()
    assert resp.recommended_value is None


# --------------------------------------------------------------------------
# Guard 3 + Ruling 4 shared-derivation (LB).
# --------------------------------------------------------------------------

def test_every_wizard_turn_carries_feasibility_snapshot_ref():
    """LB — Guard 3: every OperatorTurn_v0 carries a non-empty
    feasibility_snapshot_ref (structural via min_length=1)."""
    with pytest.raises(ValidationError):
        OperatorTurn_v0(
            turn_ref="t-abc", at=_iso_now(),
            user_content="", agent_content="",
            feasibility_snapshot_ref="",  # min_length=1 refuses
        )


def test_wizard_feasibility_grounding_uses_shared_derivation_only():
    """LB grep-negative — NO local re-implementation of
    `derive_floor_feasibility` OR `compute_feasibility` inside
    services/wizard/*. All feasibility grounding routes through
    services/mtafiti/floor_feasibility.py (Ruling 4 shared-derivation).
    """
    wizard_dir = SERVICES_DIR / "wizard"
    offenders = []
    forbidden_defs = re.compile(
        r"^\s*(?:async\s+)?def\s+(derive_floor_feasibility|compute_feasibility)\s*\("
    )
    for py in wizard_dir.rglob("*.py"):
        for line in py.read_text().splitlines():
            if forbidden_defs.match(line):
                offenders.append(f"{py.name}: {line!r}")
    assert not offenders, (
        "Ruling 4 shared-derivation LB — wizard modules MUST NOT re-implement "
        "feasibility derivation. Offenders:\n  " + "\n  ".join(offenders)
    )
    # Positive assertion — the state machine DOES import the shared module.
    sm = (wizard_dir / "operator_state_machine.py").read_text()
    assert "from services.mtafiti import floor_feasibility" in sm, (
        "operator_state_machine.py MUST import floor_feasibility from "
        "services.mtafiti (Ruling 4 shared-derivation)."
    )


# --------------------------------------------------------------------------
# No-second-LLM-judge grep-negative (Owner pre-ruling).
# --------------------------------------------------------------------------

def test_no_second_llm_judge_in_wizard_pipeline():
    """B-1 grep-negative — services/wizard/* MUST NOT import any LLM
    provider client (openai / anthropic / google / emergentintegrations).
    B-2 will plug the LLM behind the WizardAgent Protocol without any
    additional import in the state machine."""
    wizard_dir = SERVICES_DIR / "wizard"
    forbidden = ("openai", "anthropic", "google.generativeai", "emergentintegrations")
    offenders = []
    for py in wizard_dir.rglob("*.py"):
        text = py.read_text()
        for tok in forbidden:
            if re.search(rf"^\s*(?:from|import)\s+{re.escape(tok)}\b", text, re.MULTILINE):
                offenders.append(f"{py.name}: imports {tok!r}")
    assert not offenders, (
        "B-1 no-LLM invariant broken. Offenders:\n  " + "\n  ".join(offenders)
    )


# --------------------------------------------------------------------------
# License-class Option C wrap (Owner E1).
# --------------------------------------------------------------------------

def _make_envelope(commissioner: str = "unknown-commissioner") -> Envelope:
    """Build a minimal Envelope with the given commissioner for license-class tests."""
    return Envelope(
        lawful_basis="illustrative-lb",
        done_condition="illustrative-dc",
        budget="illustrative-budget",
        scope_ceiling="illustrative-scope-ceiling",
        availability_snapshot={},
        floor_feasibility={},
        commissioner=commissioner,
        committed_at="2026-07-04T00:00:00Z",
    )


def test_license_class_at_selection_equals_license_class_in_frozen_wizard_state():
    """LOAD-BEARING (Owner E1 primary-arm gate) — when the wizard state
    is FROZEN and carries an explicit license_class, `derive_license_class`
    MUST return that class verbatim."""
    now = _iso_now()
    turn = _mint_turn()
    cvs = _valid_full_committed_values(turn.turn_ref)
    frozen = WizardCommitState_v0(
        session_id="wiz-lc-1", trace_id="trc-lc-1",
        variant="operator", initiated_at=now, committed_at=now,
        turns=[turn], agent_assumptions=[], committed_values=cvs,
        feasibility_history=["feas-trc-xyz-1"],
        license_class="premium",  # explicit primary-arm value
        frozen_objective_ref=None,
    )
    env = _make_envelope(commissioner="standard-commissioner-would-map-elsewhere")
    result = license_class_selection.derive_license_class(env, wizard_state=frozen)
    assert result == "premium", (
        "Primary arm MUST return the frozen wizard state's license_class."
    )


def test_license_class_mid_session_wizard_state_routes_to_fallback():
    """LOAD-BEARING (Owner clarification — branch discrimination) — a
    wizard_state with committed_at=None (mid-session) MUST route to the
    FALLBACK arm, not primary. Prevents identity-proxy laundering via a
    half-shaped session."""
    now = _iso_now()
    turn = _mint_turn()
    mid_session = WizardCommitState_v0(
        session_id="wiz-lc-2", trace_id="trc-lc-2",
        variant="operator", initiated_at=now, committed_at=None,  # <— mid-session
        turns=[turn], agent_assumptions=[], committed_values={},
        feasibility_history=[],
        license_class="premium",  # would-be primary if state were frozen
    )
    env = _make_envelope(commissioner="unknown-commissioner")
    result = license_class_selection.derive_license_class(env, wizard_state=mid_session)
    fallback = license_class_selection.derive_license_class_from_commissioner(env)
    assert result == fallback, (
        "Mid-session wizard_state (committed_at is None) MUST route to "
        "fallback, NOT primary. Owner E1 branch-discrimination LB."
    )


def test_license_class_fallback_arm_unchanged_when_no_explicit_value():
    """Regression — `derive_license_class(envelope, None)` returns
    identical output to the fallback function."""
    env = _make_envelope(commissioner="illustrative-commissioner-x")
    result = license_class_selection.derive_license_class(env, wizard_state=None)
    fallback = license_class_selection.derive_license_class_from_commissioner(env)
    assert result == fallback


def test_license_class_primary_arm_none_license_class_routes_to_fallback():
    """Defensive — a frozen wizard state whose `license_class` is None
    routes to fallback (the wizard failed to populate — don't invent
    a return value out of the primary arm)."""
    now = _iso_now()
    turn = _mint_turn()
    cvs = _valid_full_committed_values(turn.turn_ref)
    frozen_no_class = WizardCommitState_v0(
        session_id="wiz-lc-3", trace_id="trc-lc-3",
        variant="operator", initiated_at=now, committed_at=now,
        turns=[turn], agent_assumptions=[], committed_values=cvs,
        feasibility_history=["feas-trc-xyz-1"],
        license_class=None,  # explicitly None on the frozen state
    )
    env = _make_envelope(commissioner="illustrative-commissioner-x")
    result = license_class_selection.derive_license_class(env, wizard_state=frozen_no_class)
    fallback = license_class_selection.derive_license_class_from_commissioner(env)
    assert result == fallback


def test_license_class_docstring_still_documents_phase_7_seam():
    """Ruling 4 docstring anchor — the module docstring MUST still
    document the Phase 7 seam wording ('Phase 7 seam pre-committed' +
    'fallback arm'). Survives the Option C wrap addition."""
    text = (SERVICES_DIR / "service_1" / "license_class_selection.py").read_text()
    assert "Phase 7 seam pre-committed" in text
    assert "fallback arm" in text.lower() or "FALLBACK ARM" in text


# --------------------------------------------------------------------------
# Provenance-preservation (Owner E7 — shared-derivation at B-1).
# --------------------------------------------------------------------------

def test_provenance_preservation_impossible_refuses_during_shaping():
    """LB (E7) — provenance-preservation rule refuses at shaping-time
    for a combination the transform layer cannot support (§6 preamble)."""
    # composed_conclusion + per_utterance is impossible per §6 rules.
    result = _pp.evaluate_provenance_preservation(
        output_form="composed_conclusion",
        output_grain="per_utterance",
        output_standard="utterance",
    )
    assert result.preservable is False
    assert result.refusal_reason == "provenance_preservation_impossible"
    assert result.off_menu_fact
    assert result.what_you_can_do

    # And a valid combination MUST pass.
    ok = _pp.evaluate_provenance_preservation(
        output_form="qualified_data",
        output_grain="per_utterance",
        output_standard="utterance",
    )
    assert ok.preservable is True


def test_provenance_preservation_uses_single_source_derivation():
    """Grep-negative — the rule table + evaluator live in ONE module
    (`services/service_1/provenance_preservation.py`). Neither
    services/wizard/* nor services/service_1/* elsewhere may declare a
    second `_PROVENANCE_RULES` table or a second
    `evaluate_provenance_preservation` function."""
    # Grep the codebase for the sentinel identifiers.
    def_pattern = re.compile(r"^\s*def\s+evaluate_provenance_preservation\s*\(")
    dict_pattern = re.compile(r"^\s*_PROVENANCE_RULES\s*[:=]")
    def_hits = 0
    dict_hits = 0
    for base in (SERVICES_DIR,):
        for py in base.rglob("*.py"):
            text = py.read_text()
            for line in text.splitlines():
                if def_pattern.match(line):
                    def_hits += 1
                if dict_pattern.match(line):
                    dict_hits += 1
    assert def_hits == 1, (
        f"provenance-preservation is a shared-derivation module; expected "
        f"EXACTLY 1 `def evaluate_provenance_preservation`, found {def_hits}."
    )
    assert dict_hits == 1, (
        f"provenance-preservation rule table must live in ONE module; "
        f"expected EXACTLY 1 `_PROVENANCE_RULES` definition, found {dict_hits}."
    )


# --------------------------------------------------------------------------
# Owner E5 — turn ledger stamp_audit sidecar carries wizard_transcript marker.
# --------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_turn_ledger_stamp_audit_sidecar_carries_wizard_transcript_data_class():
    """LB (Owner E5) — the stamp_audit sidecar written by
    `turn_ledger.record_wizard_freeze` carries
    `data_class="wizard_transcript"` so DPO can address wizard
    transcripts as a separately-addressable retention class at Seam-3
    unlock."""
    from services.wizard import turn_ledger as _tl
    now = _iso_now()
    turn = _mint_turn()
    cvs = _valid_full_committed_values(turn.turn_ref)
    frozen = WizardCommitState_v0(
        session_id="wiz-tl-1", trace_id="trc-tl-1",
        variant="operator", initiated_at=now, committed_at=now,
        turns=[turn], agent_assumptions=[], committed_values=cvs,
        feasibility_history=["feas-trc-xyz-1"],
        license_class="standard", frozen_objective_ref=None,
    )
    # Clean up any prior test rows on the same (trace_id, run_id).
    run_id = f"wizard-freeze-{frozen.session_id}"
    await db[NORTHENA_LEDGER_COLLECTION].delete_many({
        "trace_id": frozen.trace_id, "run_id": run_id,
    })
    returned_run_id = await _tl.record_wizard_freeze(
        frozen, lawful_basis_ref="wizard-tl-lb",
    )
    assert returned_run_id == run_id
    doc = await db[NORTHENA_LEDGER_COLLECTION].find_one({
        "trace_id": frozen.trace_id, "run_id": run_id,
    })
    assert doc is not None, "wizard-freeze ledger row not written"
    stamp = doc.get("stamp_audit")
    assert stamp is not None, "stamp_audit sidecar missing"
    assert stamp.get("data_class") == "wizard_transcript", (
        "Owner E5: data_class marker MUST equal 'wizard_transcript'"
    )
    # Idempotency — repeated calls MUST NOT write a second row.
    _ = await _tl.record_wizard_freeze(frozen, lawful_basis_ref="wizard-tl-lb")
    n_rows = await db[NORTHENA_LEDGER_COLLECTION].count_documents({
        "trace_id": frozen.trace_id, "run_id": run_id,
    })
    assert n_rows == 1, (
        f"turn_ledger idempotency LB: expected exactly 1 row after 2 calls, "
        f"got {n_rows}."
    )
    # Clean up.
    await db[NORTHENA_LEDGER_COLLECTION].delete_many({
        "trace_id": frozen.trace_id, "run_id": run_id,
    })


# --------------------------------------------------------------------------
# Regression from Phase 5b/6b — no STRUCK reason codes anywhere.
# --------------------------------------------------------------------------

def test_no_caller_cancelled_or_async_queue_saturated_code_anywhere():
    """Regression from 5b/6b — the STRUCK reason codes
    `caller_cancelled` + `async_queue_saturated` MUST NOT appear as a
    REASON CODE (a JSON key in the `valid_reasons` list OR as a
    `reason:` field value) anywhere in the four registries. Explanatory
    docstring mentions of the STRUCK codes inside registry `description`
    or `note` prose are permitted (the doctrine's audit trail lives in
    prose).
    """
    registries = [
        SERVICES_DIR / "service_1" / "admission_refusal_reasons.v0.json",
        SERVICES_DIR / "service_1" / "admission_refusal_reasons.v1.json",
        SERVICES_DIR / "service_1" / "admission_refusal_reasons.v2.json",
        SERVICES_DIR / "service_1" / "admission_refusal_reasons.v3.json",
        SERVICES_DIR / "service_1" / "service_1_refusal_reasons.v0.json",
    ]
    STRUCK = ("caller_cancelled", "async_queue_saturated")
    for reg in registries:
        cfg = json.loads(reg.read_text())
        # Collect all reason-code CODES from the registry structure. The
        # registries carry either `valid_reasons: [{reason: <code>, ...}]`
        # (admission_refusal) or `valid_reasons: [{code: <code>, ...}]`
        # (service_1_refusal). Extract both.
        codes = set()
        for entry in cfg.get("valid_reasons", []):
            if isinstance(entry, dict):
                if "reason" in entry:
                    codes.add(entry["reason"])
                if "code" in entry:
                    codes.add(entry["code"])
        for struck in STRUCK:
            assert struck not in codes, (
                f"STRUCK code {struck!r} found as a reason CODE in "
                f"{reg.name}. Registry code set: {sorted(codes)}"
            )


# --------------------------------------------------------------------------
# Router flow smoke — session + turn + freeze wiring (LB).
# --------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_wizard_operator_session_endpoint_returns_ids():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.post("/api/wizard/operator/session")
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["session_id"].startswith("wiz-")
    assert body["trace_id"].startswith("trc-")
    assert body["variant"] == "operator"
    assert body["initiated_at"]


@pytest.mark.asyncio
async def test_wizard_operator_turn_endpoint_appends_operator_turn_with_snapshot_ref():
    """LB — every turn carries a non-empty feasibility_snapshot_ref (Guard 3)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/operator/session")
        assert r0.status_code == 201
        sid = r0.json()["session_id"]
        r1 = await client.post(f"/api/wizard/operator/{sid}/turn")
    assert r1.status_code == 200, r1.text
    body = r1.json()
    assert body["turn_ref"].startswith("turn-")
    assert body["feasibility_snapshot_ref"], (
        "Guard 3 LB — turn body MUST carry a non-empty feasibility_snapshot_ref"
    )
    assert body["agent_content"], "stub agent MUST supply agent_content"


@pytest.mark.asyncio
async def test_wizard_operator_freeze_endpoint_refuses_on_missing_mandatory():
    """LB — freeze endpoint returns 422 with violations list when Guard 1
    fails (no operator-mandatory fields supplied)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r0 = await client.post("/api/wizard/operator/session")
        sid = r0.json()["session_id"]
        # No turn taken, no mandatory fields supplied — freeze MUST refuse.
        r = await client.post(f"/api/wizard/operator/{sid}/freeze")
    assert r.status_code == 422, r.text
    body = r.json()
    assert body["ready_to_freeze"] is False
    violations = body["violations"]
    assert violations, "MUST enumerate violations on Guard 1 failure"
    joined = "\n".join(violations)
    assert "Guard 1" in joined
