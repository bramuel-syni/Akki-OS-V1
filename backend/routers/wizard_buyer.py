"""Wizard buyer router — Phase 7 Stage B-2 (v3 §3.3 buyer variant).

Endpoints (7):
  * POST /api/wizard/buyer/session — initiate; returns
      {session_id, trace_id, initiated_at, variant="buyer"}.
  * POST /api/wizard/buyer/{sid}/turn — advance state machine one turn.
  * POST /api/wizard/buyer/{sid}/propose — agent proposal emission
      (dual-delta gate fires; refuse on missing price_delta / class_delta
      when the axes are governance-material).
  * POST /api/wizard/buyer/{sid}/agent-assumption — mint an
      AgentAssumption_v0 (buyer variant permits ANY axis except
      envelope.lawful_basis; Condition A(ii)/(iii) structural).
  * POST /api/wizard/buyer/{sid}/commit-review — paint marked draft.
  * POST /api/wizard/buyer/{sid}/freeze — freeze (B-2 landing; B-3
      wires the admission handoff to POST /api/objectives).
  * GET  /api/wizard/buyer/{sid} — read-only snapshot.

Owner Standing Disposition #2 (Infra-not-refusal): if the underlying
LLM agent raises `ServiceUnavailable`, the router returns HTTP 503 —
NEVER an AdmissionRefusal_v0 / Service1Refusal_v0 governance envelope.
"""
from __future__ import annotations

from typing import Any, Dict, FrozenSet, Optional

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from contracts.wizard_commit_state import WizardCommitState_v0
from services.synisense.exceptions import ServiceUnavailable
from services.wizard import (
    buyer_state_machine as bsm,
    session_persistence,
)
from services.wizard.agent_interface import DeterministicStubAgent
from services.wizard.source_tagging import SourceTagViolation


router = APIRouter(prefix="/wizard/buyer", tags=["wizard-buyer"])


# In-memory buyer session cache. Same posture as operator router — B-2
# persists mid-session snapshots to Mongo (`wizard_sessions` with
# `variant="buyer"`), and the frozen state lives on disk post-freeze.
# Ownership binding lands with the system-wide auth model at Phase 8
# per Owner Plan Debt (Phase 7 Stage B-2 dispatch, 2026-07-04).
_SESSIONS: Dict[str, bsm.BuyerSession] = {}


def _new_agent():
    """B-2 default agent: DeterministicStubAgent. Callers may inject a
    SonnetWizardAgent via a request-scoped seam in Stage B-3 UI wiring.
    Keeping the router's default to stub means every buyer router gate
    test runs hermetically without LLM calls.
    """
    return DeterministicStubAgent()


def _get_session_or_404(session_id: str) -> bsm.BuyerSession:
    session = _SESSIONS.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"session_id={session_id!r} not found")
    return session


async def _has_body(request: Request) -> bool:
    body_bytes = await request.body()
    return bool(body_bytes and body_bytes.strip())


@router.post("/session")
async def post_session():
    """Initiate a fresh buyer wizard session (variant='buyer')."""
    session = bsm.new_buyer_session()
    _SESSIONS[session.session_id] = session
    snapshot = bsm._to_frozen_commit_state(session, committed_at=None)
    await session_persistence.upsert_session(snapshot)
    return JSONResponse(
        status_code=201,
        content={
            "session_id": session.session_id,
            "trace_id": session.trace_id,
            "initiated_at": session.initiated_at,
            "variant": "buyer",
        },
    )


@router.post("/{session_id}/turn")
async def post_turn(session_id: str, request: Request):
    session = _get_session_or_404(session_id)
    body: Dict[str, Any] = await request.json() if await _has_body(request) else {}
    turn_ref: Optional[str] = body.get("turn_ref")
    user_content: str = body.get("user_content", "") or ""
    field_supplied: Optional[str] = body.get("field")
    value_supplied: Any = body.get("value")

    if turn_ref:
        try:
            bsm.record_buyer_response(
                session=session, turn_ref=turn_ref,
                user_content=user_content,
                field_supplied=field_supplied,
                value_supplied=value_supplied,
            )
        except SourceTagViolation as exc:
            return JSONResponse(
                status_code=422,
                content={"violations": [str(exc)], "refused": True},
            )
    try:
        turn = bsm.next_agent_turn(session, _new_agent())
    except ServiceUnavailable as exc:
        # Owner Standing Disposition #2 — LLM fault surfaces as 503,
        # NOT as a governance-refusal envelope.
        return JSONResponse(
            status_code=503,
            content={"detail": f"wizard unavailable: {exc!s}"},
        )
    snapshot = bsm._to_frozen_commit_state(session, committed_at=None)
    await session_persistence.upsert_session(snapshot)
    return {
        "session_id": session.session_id,
        "turn_ref": turn.turn_ref,
        "at": turn.at,
        "agent_content": turn.agent_content,
        "feasibility_snapshot_ref": turn.feasibility_snapshot_ref,
    }


@router.post("/{session_id}/propose")
async def post_propose(session_id: str, request: Request):
    """Buyer-only: emit an agent proposal with dual-delta gate.

    Body:
      * `axes_changed`: list[str] — the axes the proposal shifts.
      * `price_delta`: Optional[str] — required when axis in
        {output.standard, output.grain}.
      * `class_delta`: Optional[str] — required when axis in
        {output.standard, output.grain}.
      * `proposal_content`: str — the agent's proposal text.

    On dual-delta refusal → 422 with the bounded refusal reason
    (Owner E6 Visibility-not-prohibition mechanical application).
    """
    session = _get_session_or_404(session_id)
    body = await request.json()
    axes_changed: FrozenSet[str] = frozenset(body.get("axes_changed", []) or [])
    price_delta: Optional[str] = body.get("price_delta")
    class_delta: Optional[str] = body.get("class_delta")
    proposal_content: str = body.get("proposal_content", "") or ""
    try:
        proposal = bsm.record_proposal(
            session=session,
            axes_changed=axes_changed,
            price_delta=price_delta,
            class_delta=class_delta,
            proposal_content=proposal_content,
        )
    except SourceTagViolation as exc:
        return JSONResponse(
            status_code=422,
            content={"violations": [str(exc)], "refused": True},
        )
    snapshot = bsm._to_frozen_commit_state(session, committed_at=None)
    await session_persistence.upsert_session(snapshot)
    return proposal


@router.post("/{session_id}/agent-assumption")
async def post_agent_assumption(session_id: str, request: Request):
    """Buyer variant Guard 2 seam.

    Buyer permits agent-assumption on any axis EXCEPT
    `envelope.lawful_basis` (buyer NEVER attributes lawful basis —
    `use_purpose` drives license_class via E1 Option C primary arm).
    Condition A(ii)/(iii) still apply: this endpoint mints agent-source
    CommittedValue only; never writes operator-turn content.
    """
    session = _get_session_or_404(session_id)
    body = await request.json()
    field_name: str = body["field"]
    inferred_value: Any = body["inferred_value"]
    evidence_ref: str = body.get("evidence_ref", "")
    try:
        assumption = bsm.record_agent_assumption(
            session=session, field_name=field_name,
            inferred_value=inferred_value, evidence_ref=evidence_ref,
        )
    except SourceTagViolation as exc:
        return JSONResponse(
            status_code=422,
            content={"violations": [str(exc)], "refused": True},
        )
    snapshot = bsm._to_frozen_commit_state(session, committed_at=None)
    await session_persistence.upsert_session(snapshot)
    return {
        "assumption_id": assumption.assumption_id,
        "field": assumption.field,
        "at": assumption.at,
    }


@router.post("/{session_id}/commit-review")
async def post_commit_review(session_id: str):
    session = _get_session_or_404(session_id)
    agent = _new_agent()
    snapshot = bsm._to_frozen_commit_state(session, committed_at=None)
    review = agent.commit_review(snapshot)
    violations = bsm.preflight_freeze(session)
    return {
        "session_id": session.session_id,
        "you_supplied": review.you_supplied,
        "agent_assumed_items": review.agent_assumed_items,
        "proposals": session.proposals,
        "violations": violations,
        "ready_to_freeze": not violations,
    }


@router.post("/{session_id}/freeze")
async def post_freeze(session_id: str, request: Request):
    """B-2 buyer freeze — lands the machinery; admission handoff to
    POST /api/objectives is B-3 scope."""
    session = _get_session_or_404(session_id)
    body: Dict[str, Any] = await request.json() if await _has_body(request) else {}
    license_class: Optional[str] = body.get("license_class")
    if license_class is not None:
        session.license_class = license_class

    violations = bsm.preflight_freeze(session)
    if violations:
        return JSONResponse(
            status_code=422,
            content={"violations": violations, "ready_to_freeze": False},
        )
    try:
        frozen = bsm.freeze(session, frozen_objective_ref=None)
    except Exception as exc:  # pydantic ValidationError etc.
        return JSONResponse(
            status_code=422,
            content={"violations": [str(exc)], "ready_to_freeze": False},
        )
    await session_persistence.upsert_session(frozen)
    _SESSIONS.pop(session.session_id, None)
    return {
        "session_id": frozen.session_id,
        "committed_at": frozen.committed_at,
        "trace_id": frozen.trace_id,
        "variant": frozen.variant,
        "license_class": frozen.license_class,
        "admission_handoff_deferred_to_stage": "B-3",
        "frozen_state": frozen.model_dump(mode="json"),
    }


@router.get("/{session_id}")
async def get_session(session_id: str):
    doc = await session_persistence.load_session(session_id)
    if doc is None:
        session = _SESSIONS.get(session_id)
        if session is None:
            raise HTTPException(status_code=404, detail=f"session_id={session_id!r} not found")
        snapshot = bsm._to_frozen_commit_state(session, committed_at=None)
        return snapshot.model_dump(mode="json")
    doc.pop("_id", None)
    return doc
