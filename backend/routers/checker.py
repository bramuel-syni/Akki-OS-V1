"""§8 consequence-class checker router.

Endpoints (all under /api/checker):
    * POST /api/checker/initiate — kicks off a rule-change request.
    * POST /api/checker/countersign/{request_id} — dual-control countersign.
    * POST /api/checker/object/{request_id} — annotate + escalate (Ruling 3).
    * GET  /api/checker/pending — per-role pending banner feed.

E2 taxonomy (4-code registry): auth denials 401/403 with {reason, detail}.
Standing state-conflict anti-rule (elevated): invalid state transitions
use HTTP 403 access-control class only.
"""
from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from services.auth import auth_refusal
from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.checker import state_machine
from services.checker.countersign_ledger import (
    emit_countersign_ledger_row,
    emit_tightening_objected_row,
)
from services.checker.rule_change_request import now_iso

router = APIRouter(prefix="/checker", tags=["checker"])


def _capacity_role(identity: Identity, roles: set) -> Optional[str]:
    """Returns 'compliance' or 'admin' as the CAPACITY role for a
    checker action, per Ruling 2. The `admin` seeded super-role acts as
    'admin' capacity by default; `dpo` acts as 'compliance' capacity."""
    if "dpo" in roles:
        return "compliance"
    if "master_admin" in roles or "admin" in roles:
        return "admin"
    return None


async def _require_checker_or_deny(request: Request):
    """Require dpo OR admin/master_admin role."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return None, None, result
    identity: Identity = result
    roles = set(identity.roles)
    capacity = _capacity_role(identity, roles)
    if capacity is None:
        return None, None, auth_refusal.emit(
            "auth_scope_insufficient",
            detail=(
                "Checker endpoints require `dpo` (compliance capacity) or "
                "`admin`/`master_admin` (admin capacity)."
            ),
        )
    return identity, capacity, None


@router.post("/initiate")
async def post_initiate(request: Request):
    identity, capacity, deny = await _require_checker_or_deny(request)
    if deny is not None:
        return deny
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_body", "detail": "Body must be JSON."},
        )
    rule_class = payload.get("rule_class")
    from_ref = payload.get("from_value_ref")
    to_ref = payload.get("to_value_ref")
    if not (isinstance(rule_class, str) and isinstance(from_ref, str) and isinstance(to_ref, str)):
        return JSONResponse(
            status_code=400,
            content={
                "reason": "malformed_payload",
                "detail": "Body must include rule_class, from_value_ref, to_value_ref (all strings).",
            },
        )
    try:
        result = await state_machine.initiate(
            rule_class=rule_class,
            from_value_ref=from_ref,
            to_value_ref=to_ref,
            initiator_id=identity.email,
            initiator_role=capacity,
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"reason": "unknown_rule_class", "detail": str(e)},
        )
    return {
        "request_id": result.request_id,
        "state": result.state,
        "consequence_class": result.consequence_class,
        "idempotent_hit": result.idempotent_hit,
    }


@router.post("/countersign/{request_id}")
async def post_countersign(request_id: str, request: Request):
    identity, capacity, deny = await _require_checker_or_deny(request)
    if deny is not None:
        return deny
    try:
        req = await state_machine.countersign(
            request_id=request_id,
            checker_id=identity.email,
            checker_role=capacity,
        )
    except state_machine.UnknownRequestError as e:
        return JSONResponse(
            status_code=404,
            content={"reason": "request_not_found", "detail": str(e)},
        )
    except state_machine.InvalidTransitionError as e:
        # Standing state-conflict anti-rule (elevated): use 403 access-control.
        return auth_refusal.emit(
            "auth_scope_insufficient",
            detail=f"checker_transition_refused: {e}",
        )
    # Emit ledger row (Ruling 1(ii): existing data-class LB gate extends).
    ledger = await emit_countersign_ledger_row(
        run_id=f"cs-{uuid.uuid4().hex[:12]}",
        trace_id=f"cs-trace-{uuid.uuid4().hex[:12]}",
        rule_class=req.rule_class,
        request_id=req.request_id,
        consequence_class=req.consequence_class,
        initiator_id=req.initiator_id,
        initiator_role=req.initiator_role,
        checker_id=req.checker_id,
        checker_role=req.checker_role,
        initiated_at=req.initiated_at,
        countersigned_at=req.countersigned_at,
    )
    # CK-U1 commit-line binding copy with U+00B7 middle-dot (E7 strict).
    commit_line = (
        f"Signed by {req.initiator_role} \u00b7 counter-signed by "
        f"{req.checker_role} \u00b7 recorded with both identities."
    )
    return {
        "state": req.state,
        "effective_at": req.effective_at,
        "ledger_row_ref": ledger.run_id,
        "commit_line": commit_line,
    }


@router.post("/object/{request_id}")
async def post_object(request_id: str, request: Request):
    identity, capacity, deny = await _require_checker_or_deny(request)
    if deny is not None:
        return deny
    try:
        payload = await request.json()
    except Exception:
        payload = {}
    reason = (payload or {}).get("reason", "")
    if not isinstance(reason, str) or not reason.strip():
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_payload", "detail": "reason required."},
        )
    try:
        req = await state_machine.object_to_tightening(
            request_id=request_id,
            objector_id=identity.email,
            objector_role=capacity,
            reason=reason,
        )
    except state_machine.UnknownRequestError as e:
        return JSONResponse(
            status_code=404,
            content={"reason": "request_not_found", "detail": str(e)},
        )
    except state_machine.InvalidTransitionError as e:
        return auth_refusal.emit(
            "auth_scope_insufficient",
            detail=f"checker_transition_refused: {e}",
        )
    objected_at = req.objections[-1]["objected_at"] if req.objections else now_iso()
    await emit_tightening_objected_row(
        run_id=f"obj-{uuid.uuid4().hex[:12]}",
        trace_id=f"obj-trace-{uuid.uuid4().hex[:12]}",
        rule_class=req.rule_class,
        request_id=req.request_id,
        consequence_class=req.consequence_class,
        objector_id=identity.email,
        objector_role=capacity,
        objection_reason=reason,
        objected_at=objected_at,
        underlying_state=req.state,  # unchanged; Ruling 3
    )
    return {
        "state": req.state,  # UNCHANGED per Ruling 3
        "objection_recorded_at": objected_at,
        "owner_escalated": True,
    }


@router.get("/pending")
async def get_pending(request: Request, role: Optional[str] = None):
    _, _, deny = await _require_checker_or_deny(request)
    if deny is not None:
        return deny
    items = await state_machine.list_pending(role=role)
    return {"pending": items, "count": len(items)}
