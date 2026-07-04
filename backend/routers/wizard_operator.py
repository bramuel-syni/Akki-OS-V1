"""Wizard operator router — Phase 7 Stage B-1 (v3 §3.3 operator variant).

Endpoints:
  * POST /api/wizard/operator/session
      Initiate a fresh operator wizard session; returns
      `{session_id, trace_id, initiated_at}`.
  * POST /api/wizard/operator/{session_id}/turn
      Advance the state machine by one agent turn (Guard 3 fires:
      feasibility snapshot recorded). Body may carry the operator's
      response to the previous turn (`turn_ref`, `user_content`,
      optional `field`, `value`).
  * POST /api/wizard/operator/{session_id}/agent-assumption
      Record an agent-inferred value at preference tier (Guard 2:
      mint an AgentAssumption + paired CommittedValue with
      source="agent_assumed"). B-1 seldom emits this from the stub
      agent; kept as the mechanical entry for tests.
  * POST /api/wizard/operator/{session_id}/commit-review
      Render the marked-draft view (you_supplied / agent_assumed_items);
      Guard 1 pre-flight + provenance-preservation refusal returned as
      a bounded list of violations if any.
  * POST /api/wizard/operator/{session_id}/freeze
      Freeze the session — Guard 1/2/3 fire structurally. Returns
      frozen WizardCommitState_v0 body OR 422 with violations list.
      Writes wizard_freeze ledger row via `turn_ledger.record_wizard_freeze`.
  * GET  /api/wizard/operator/{session_id}
      Read-only snapshot (mid-session working state OR frozen state).

Constraints (LOAD-BEARING at B-1):
  * Uses `DeterministicStubAgent` — NO LLM at B-1.
  * Feasibility grounding via `services/mtafiti/floor_feasibility` (Ruling 4).
  * On freeze, `turn_ledger.record_wizard_freeze` is invoked — the
    stamp_audit sidecar carries `data_class="wizard_transcript"` per
    Owner E5 ruling; gate
    `test_turn_ledger_stamp_audit_sidecar_carries_wizard_transcript_data_class`
    protects the marker.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from contracts.wizard_commit_state import WizardCommitState_v0
from services.wizard import (
    operator_state_machine as osm,
    session_persistence,
    turn_ledger,
)
from services.wizard.agent_interface import DeterministicStubAgent


router = APIRouter(prefix="/wizard/operator", tags=["wizard-operator"])


# In-memory session cache — B-1 keeps working state in-process; Mongo
# holds the frozen snapshots and any mid-session persistence. B-2 will
# lift the cache into a request-scoped read from Mongo when the LLM
# integration lands and the state needs to survive worker restarts.
_SESSIONS: Dict[str, osm.OperatorSession] = {}


def _new_stub_agent() -> DeterministicStubAgent:
    """Agent-pluggable-with-stub-agent-first (Owner ruling, Phase 7 Stage A close):
    B-1 mounts the stub; B-2 will swap in the LLM-backed agent behind the
    same `WizardAgent` Protocol interface without state-machine changes.
    """
    return DeterministicStubAgent()


def _get_session_or_404(session_id: str) -> osm.OperatorSession:
    session = _SESSIONS.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"session_id={session_id!r} not found")
    return session


@router.post("/session")
async def post_session():
    """Initiate a fresh operator wizard session."""
    session = osm.new_operator_session()
    _SESSIONS[session.session_id] = session
    # Persist an initial snapshot to Mongo (mid-session, committed_at=None).
    snapshot = osm._to_frozen_commit_state(session, committed_at=None)
    await session_persistence.upsert_session(snapshot)
    return JSONResponse(
        status_code=201,
        content={
            "session_id": session.session_id,
            "trace_id": session.trace_id,
            "initiated_at": session.initiated_at,
            "variant": "operator",
        },
    )


@router.post("/{session_id}/turn")
async def post_turn(session_id: str, request: Request):
    """Advance the state machine by one agent turn OR record an operator
    response to the previous turn.

    Body shape (all fields optional):
      * `turn_ref`: uuid of the turn being answered by the operator.
      * `user_content`: operator's free-text reply.
      * `field`: dotted-path field being supplied (e.g. "output.grain").
      * `value`: value being supplied for that field.

    If a `turn_ref` is provided → operator response is recorded first
    (Guard 1: paired CommittedValue with source="operator_supplied"),
    then the agent advances one turn. If no `turn_ref` → agent advances
    one turn immediately (first turn or reply-less advance).
    """
    session = _get_session_or_404(session_id)
    body: Dict[str, Any] = await request.json() if await _has_body(request) else {}

    turn_ref: Optional[str] = body.get("turn_ref")
    user_content: str = body.get("user_content", "") or ""
    field_supplied: Optional[str] = body.get("field")
    value_supplied: Any = body.get("value")

    if turn_ref:
        osm.record_operator_response(
            session=session, turn_ref=turn_ref,
            user_content=user_content,
            field_supplied=field_supplied,
            value_supplied=value_supplied,
        )
    agent = _new_stub_agent()
    turn = osm.next_agent_turn(session, agent)
    # Persist mid-session snapshot.
    snapshot = osm._to_frozen_commit_state(session, committed_at=None)
    await session_persistence.upsert_session(snapshot)
    return {
        "session_id": session.session_id,
        "turn_ref": turn.turn_ref,
        "at": turn.at,
        "agent_content": turn.agent_content,
        "feasibility_snapshot_ref": turn.feasibility_snapshot_ref,
    }


@router.post("/{session_id}/agent-assumption")
async def post_agent_assumption(session_id: str, request: Request):
    """Guard 2 seam — record an agent-inferred value at preference tier.

    B-1 keeps this endpoint mechanically callable so the invariant gates
    can prove Guard 2 discipline against the stub agent's outputs.
    Buyer variant (B-2) will exercise this path more heavily via
    live-quote recommendations.

    Body: `{field: str, inferred_value: Any, evidence_ref: str = ""}`.
    """
    session = _get_session_or_404(session_id)
    body = await request.json()
    field_name: str = body["field"]
    inferred_value: Any = body["inferred_value"]
    evidence_ref: str = body.get("evidence_ref", "")
    assumption = osm.record_agent_assumption(
        session=session, field_name=field_name,
        inferred_value=inferred_value, evidence_ref=evidence_ref,
    )
    snapshot = osm._to_frozen_commit_state(session, committed_at=None)
    await session_persistence.upsert_session(snapshot)
    return {
        "assumption_id": assumption.assumption_id,
        "field": assumption.field,
        "at": assumption.at,
    }


@router.post("/{session_id}/commit-review")
async def post_commit_review(session_id: str):
    """Paint the marked-draft view + Guard 1 pre-flight + provenance
    refusal enumeration.

    Response body:
      * `you_supplied`: [{field, value}, ...]
      * `agent_assumed_items`: [{field, value}, ...]
      * `violations`: [str, ...] — empty iff ready to freeze.
    """
    session = _get_session_or_404(session_id)
    agent = _new_stub_agent()
    snapshot = osm._to_frozen_commit_state(session, committed_at=None)
    review = agent.commit_review(snapshot)
    violations = osm.preflight_freeze(session)
    return {
        "session_id": session.session_id,
        "you_supplied": review.you_supplied,
        "agent_assumed_items": review.agent_assumed_items,
        "violations": violations,
        "ready_to_freeze": not violations,
    }


@router.post("/{session_id}/freeze")
async def post_freeze(session_id: str, request: Request):
    """Freeze the session — Guard 1/2 fire structurally on the
    WizardCommitState_v0 model_validator. Guard 3 already enforced
    per-turn via feasibility_snapshot_ref.

    Body (optional): `{license_class: str, lawful_basis_ref: str}`.
    B-1 does NOT mint an ObjectiveRequest_v2 — that lands at B-3 admission
    handoff. B-1 freezes the state and writes the wizard_freeze ledger
    row (with `data_class="wizard_transcript"` marker per Owner E5).
    """
    session = _get_session_or_404(session_id)
    body: Dict[str, Any] = await request.json() if await _has_body(request) else {}
    license_class: Optional[str] = body.get("license_class")
    lawful_basis_ref: str = body.get("lawful_basis_ref", "wizard-lawful-basis-unset")

    if license_class is not None:
        session.license_class = license_class

    # Pre-flight — return violations without raising.
    violations = osm.preflight_freeze(session)
    if violations:
        return JSONResponse(
            status_code=422,
            content={"violations": violations, "ready_to_freeze": False},
        )
    try:
        frozen = osm.freeze(session, frozen_objective_ref=None)
    except Exception as exc:  # pydantic ValidationError etc.
        return JSONResponse(
            status_code=422,
            content={"violations": [str(exc)], "ready_to_freeze": False},
        )
    # Persist frozen snapshot + wizard_freeze ledger row.
    await session_persistence.upsert_session(frozen)
    ledger_run_id = await turn_ledger.record_wizard_freeze(
        frozen, lawful_basis_ref=lawful_basis_ref,
    )
    # Clear the in-memory working session — it's now immutable on disk.
    _SESSIONS.pop(session.session_id, None)
    return {
        "session_id": frozen.session_id,
        "committed_at": frozen.committed_at,
        "trace_id": frozen.trace_id,
        "license_class": frozen.license_class,
        "ledger_run_id": ledger_run_id,
        "frozen_state": frozen.model_dump(mode="json"),
    }


@router.get("/{session_id}")
async def get_session(session_id: str):
    """Read-only snapshot — Mongo is authoritative post-freeze."""
    doc = await session_persistence.load_session(session_id)
    if doc is None:
        # Not persisted yet; check in-memory working state.
        session = _SESSIONS.get(session_id)
        if session is None:
            raise HTTPException(status_code=404, detail=f"session_id={session_id!r} not found")
        snapshot = osm._to_frozen_commit_state(session, committed_at=None)
        return snapshot.model_dump(mode="json")
    doc.pop("_id", None)
    return doc


async def _has_body(request: Request) -> bool:
    """Best-effort body-presence check; POSTs with no JSON body should
    not error on `await request.json()`."""
    body_bytes = await request.body()
    return bool(body_bytes and body_bytes.strip())
