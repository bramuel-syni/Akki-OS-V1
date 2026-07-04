"""Wizard buyer router — Phase 7 Stage B-2 + Phase 7 Stage B-3.

Endpoints (8; B-3 adds `/handoff`):
  * POST /api/wizard/buyer/session — initiate; returns
      {session_id, trace_id, initiated_at, variant="buyer"}.
  * POST /api/wizard/buyer/{sid}/turn — advance state machine one turn.
  * POST /api/wizard/buyer/{sid}/propose — agent proposal emission
      (dual-delta gate fires; refuse on missing price_delta / class_delta
      when the axes are governance-material).
  * POST /api/wizard/buyer/{sid}/agent-assumption — mint an
      AgentAssumption_v0 (buyer variant permits ANY axis except
      envelope.lawful_basis; Condition A(ii)/(iii) structural).
  * POST /api/wizard/buyer/{sid}/commit-review — paint marked draft +
      dual_delta_summary + license_class_drift (B-3 extensions).
  * POST /api/wizard/buyer/{sid}/freeze — freeze + wizard_freeze ledger
      write (B-3 parity with operator).
  * POST /api/wizard/buyer/{sid}/handoff — B-3 admission handoff to
      POST /api/objectives (in-process ASGI transport; single-source).
  * GET  /api/wizard/buyer/{sid} — read-only snapshot.

Owner Standing Disposition #2 (Infra-not-refusal): if the underlying
LLM agent raises `ServiceUnavailable`, the router returns HTTP 503 —
NEVER an AdmissionRefusal_v0 / Service1Refusal_v0 governance envelope.
"""
from __future__ import annotations

from typing import Any, Dict, FrozenSet, Optional

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from httpx import ASGITransport

from contracts.wizard_commit_state import WizardCommitState_v0
from services.service_1.license_class_selection import derive_license_class
from services.synisense.exceptions import ServiceUnavailable
from services.wizard import (
    admission_handoff,
    buyer_state_machine as bsm,
    session_persistence,
    turn_ledger,
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
    """Paint the marked-draft view + dual-delta summary + license-class-drift.

    B-3 extensions (both fields lift from single-source helpers; no
    in-router computation):
      * `dual_delta_summary`: dict keyed by `proposal_id` — buyer only.
        Sourced from `services/wizard/admission_handoff.py::summarise_dual_deltas`.
      * `license_class_drift`: {committed: str, derived: str} | null.
        Sourced from `services/service_1/license_class_selection.py::derive_license_class`
        invoked against the reviewed state. Soft signal — NOT a hard refusal.
    """
    session = _get_session_or_404(session_id)
    agent = _new_agent()
    snapshot = bsm._to_frozen_commit_state(session, committed_at=None)
    review = agent.commit_review(snapshot)
    violations = bsm.preflight_freeze(session)
    dual_delta_summary = admission_handoff.summarise_dual_deltas(session.proposals)
    license_class_drift = _compute_license_class_drift(session, snapshot)
    return {
        "session_id": session.session_id,
        "you_supplied": review.you_supplied,
        "agent_assumed_items": review.agent_assumed_items,
        "proposals": session.proposals,
        "dual_delta_summary": dual_delta_summary,
        "license_class_drift": license_class_drift,
        "violations": violations,
        "ready_to_freeze": not violations,
    }


def _compute_license_class_drift(
    session: bsm.BuyerSession,
    snapshot: WizardCommitState_v0,
) -> Optional[Dict[str, str]]:
    """Compute soft license_class_drift signal.

    `committed` = value the user committed on the session (may be None
    if mid-shape). `derived` = what `derive_license_class` would return
    against a FROZEN wizard state (post-freeze primary arm).

    Returns None when either (a) no committed class OR (b) derived
    matches committed. Otherwise returns `{committed, derived}` for
    surface rendering.

    The primary-arm gate of `derive_license_class` requires
    `wizard_state.committed_at is not None`. At commit-review time
    the state is NOT yet frozen — we simulate the frozen posture by
    minting a snapshot with `committed_at=_iso_now()` for derivation
    purposes ONLY (this simulated snapshot is discarded; nothing
    persists).
    """
    if session.license_class is None:
        return None
    # Simulate frozen posture for derivation.
    from services.wizard.buyer_state_machine import _iso_now  # single-source
    committed_snapshot = snapshot.model_copy(update={"committed_at": _iso_now()})
    # Envelope is not passed here — derive_license_class primary arm
    # returns wizard_state.license_class when the state is frozen. The
    # fallback arm (from Envelope) is not exercised here because the
    # primary arm gate fires.
    # We invoke against a minimal envelope shim: pass the committed
    # snapshot's envelope-shaped values if present, else None.
    envelope_shim = _envelope_shim_from_session(session)
    derived = derive_license_class(envelope_shim, wizard_state=committed_snapshot)
    if derived == session.license_class:
        return None
    return {"committed": session.license_class, "derived": derived}


def _envelope_shim_from_session(session: bsm.BuyerSession):
    """Construct a minimal Envelope for the fallback arm.

    The primary arm fires when the simulated snapshot has committed_at +
    license_class both set; the fallback arm is not exercised. But
    derive_license_class's signature requires a valid Envelope object,
    so we build a minimal one from the session's committed values.
    """
    from contracts.objective_request_v2 import Envelope
    return Envelope(
        lawful_basis=_extract_field_str(session, "envelope.lawful_basis", "legitimate_interest"),
        done_condition=_extract_field_str(session, "envelope.done_condition", "standing_floor"),
        budget=_extract_field_str(session, "envelope.budget", "default"),
        scope_ceiling=_extract_field_str(session, "envelope.scope_ceiling", "estate"),
        availability_snapshot={},
        floor_feasibility={},
        commissioner=f"wizard-buyer-{session.session_id}",
        committed_at=session.initiated_at,
    )


def _extract_field_str(session: bsm.BuyerSession, name: str, default: str) -> str:
    cv = session.committed_values.get(name)
    if cv is None or cv.value is None:
        return default
    return str(cv.value)


@router.post("/{session_id}/freeze")
async def post_freeze(session_id: str, request: Request):
    """B-3 buyer freeze — parity with operator freeze:
      * `record_wizard_freeze(...)` ledger write with
        `data_class="wizard_transcript"` (Owner E5 marker) — this was
        missing at B-2 and lands at B-3.
      * Body accepts optional `lawful_basis_ref` (default matches operator).
      * Response body carries `ledger_run_id`.
    """
    session = _get_session_or_404(session_id)
    body: Dict[str, Any] = await request.json() if await _has_body(request) else {}
    license_class: Optional[str] = body.get("license_class")
    lawful_basis_ref: str = body.get("lawful_basis_ref", "wizard-lawful-basis-unset")
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
    # B-3 ledger parity with operator freeze — record_wizard_freeze is
    # idempotent per (trace_id, run_id='wizard-freeze-{session_id}').
    ledger_run_id = await turn_ledger.record_wizard_freeze(
        frozen, lawful_basis_ref=lawful_basis_ref,
    )
    _SESSIONS.pop(session.session_id, None)
    return {
        "session_id": frozen.session_id,
        "committed_at": frozen.committed_at,
        "trace_id": frozen.trace_id,
        "variant": frozen.variant,
        "license_class": frozen.license_class,
        "ledger_run_id": ledger_run_id,
        "frozen_state": frozen.model_dump(mode="json"),
    }


@router.post("/{session_id}/handoff")
async def post_handoff(session_id: str, request: Request):
    """B-3 admission handoff — mint `ObjectiveRequest_v2` from the frozen
    wizard state and hand off to `POST /api/objectives` (existing async
    admission surface).

    Preconditions:
      * Wizard session MUST be frozen (`committed_at is not None` on the
        persisted state). If not frozen → 422 with
        `{"reason": "wizard_not_frozen", ...}`.

    Return codes:
      * 202 with `AsyncDeliveryAccepted_v1` on admission accept
        (or idempotent replay — repeat handoff on same frozen session
        returns same `objective_id`).
      * 422 with `AdmissionRefusal_v0` (or `Service1Refusal_v0`)
        passthrough on governed admission refuse. **No new refusal
        codes at B-3 per Owner ruling.**
      * 503 on infra fault (async admission's existing infra-not-refusal
        behavior).

    Dual-delta acceptance recording (buyer only): `proposals` from the
    in-memory session are aggregated by
    `admission_handoff.compose_objective_request_from_frozen_state_with_proposals`
    into `envelope.floor_feasibility["dual_delta_summary"]`.
    """
    # Load frozen state — Mongo authoritative post-freeze.
    doc = await session_persistence.load_session(session_id)
    if doc is None:
        # Not persisted → maybe still mid-shape in memory.
        in_mem = _SESSIONS.get(session_id)
        if in_mem is None:
            raise HTTPException(status_code=404, detail=f"session_id={session_id!r} not found")
        return JSONResponse(
            status_code=422,
            content={
                "reason": "wizard_not_frozen",
                "detail": "handoff requires a frozen wizard session; call POST /freeze first.",
            },
        )
    doc.pop("_id", None)
    frozen_state = WizardCommitState_v0.model_validate(doc)
    if frozen_state.committed_at is None:
        return JSONResponse(
            status_code=422,
            content={
                "reason": "wizard_not_frozen",
                "detail": "handoff requires a frozen wizard session; call POST /freeze first.",
            },
        )
    # Buyer variant — carry proposals summary into the composed request.
    in_mem = _SESSIONS.get(session_id)
    proposals = list(in_mem.proposals) if in_mem is not None else []
    obj_req = admission_handoff.compose_objective_request_from_frozen_state_with_proposals(
        frozen_state, proposals,
    )
    # In-process ASGI transport call to POST /api/objectives — single-source
    # (no duplication of admission logic). Preserves idempotency via the
    # deterministic idempotency_key = f"handoff-{session_id}".
    from server import app as _fastapi_app  # local import to avoid circular
    payload = obj_req.model_dump(mode="json")
    async with httpx.AsyncClient(
        transport=ASGITransport(app=_fastapi_app),
        base_url="http://wizard-handoff-internal",
    ) as client:
        resp = await client.post("/api/objectives", json=payload)
    # Persist frozen_objective_ref on the wizard state (mongo update)
    # when handoff was accepted at 202 with an objective_id.
    if resp.status_code == 202:
        body = resp.json()
        objective_id = body.get("objective_id")
        if objective_id and frozen_state.frozen_objective_ref != objective_id:
            updated = frozen_state.model_copy(update={"frozen_objective_ref": objective_id})
            await session_persistence.upsert_session(updated)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


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
