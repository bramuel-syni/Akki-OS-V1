"""Phase 8 Stage B-4 Block 1 — Master Admin surface router (§6 backend).

Endpoints (all under `/api/master_admin`):
  * GET  /api/master_admin/pending_seams  — read-only enumeration of seams
      awaiting owner/DPO/MEA values (§6.1 pending banner data source per
      Owner amendment 2026-07-05: "the seams ARE the data").
  * GET  /api/master_admin/audit_trail    — read-only §6.3 audit-trail
      projection over NorthenaLedgerRow_v1 filtered by
      `stamp_audit.data_class="master_admin_rule_change"`; plain-language
      description rows per §6.3 Rule ("the diff exists in the record; it
      is never the primary display").

Owner E2 taxonomy (B-3 ratified, B-4 upheld):
  * All denials 401/403 `{reason, detail}` — 4-code registry ONLY.
  * NO new codes at B-4. NO outcome key on auth denials.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from core import db
from services.auth import auth_refusal
from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.economics.tier_lock_ledger import DATA_CLASS_MASTER_ADMIN_RULE_CHANGE
from services.master_admin.pending_seams import enumerate_pending_seams


router = APIRouter(prefix="/master_admin", tags=["master_admin"])


def _has_master_admin_authority(identity: Identity) -> bool:
    """A caller may view Master Admin surfaces iff they carry the
    master_admin role (or admin, which is the seeded super-role).
    Post-B-4: this is the SOLE gate on the highest-privilege surface;
    RMS_MASTER_ADMIN_TOKEN retired.
    """
    roles = set(identity.roles)
    return "master_admin" in roles or "admin" in roles


async def _require_master_admin_or_deny(request: Request):
    """Return (identity, None) on permit, (None, JSONResponse) on deny.

    Two-step gate mirroring B-3 engineer authority pattern:
      1. Bearer token → Identity (or 401 auth_missing / auth_expired).
      2. Identity → master_admin/admin role (or 403 auth_scope_insufficient).
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return None, result
    identity: Identity = result
    if not _has_master_admin_authority(identity):
        return None, auth_refusal.emit(
            "auth_scope_insufficient",
            detail=(
                "Master Admin surface requires the `master_admin` role "
                "(or `admin`). The caller identity is authenticated but "
                "lacks master-admin authority."
            ),
        )
    return identity, None


@router.get("/pending_seams")
async def get_pending_seams(request: Request):
    """§6.1 pending banner data source.

    Returns the read-only enumeration of currently-pending governance
    seams (owner/DPO/MEA values awaiting landing). No queue backend,
    no placeholder — the seams ARE the data (Owner amendment,
    2026-07-05). Auth-gated: master_admin role required.
    """
    _, deny = await _require_master_admin_or_deny(request)
    if deny is not None:
        return deny
    seams = enumerate_pending_seams()
    return {
        "pending_seams": seams,
        "count": len(seams),
    }


@router.get("/audit_trail")
async def get_audit_trail(request: Request, limit: int = 50):
    """§6.3 audit-trail data source.

    Returns recent master_admin_rule_change ledger rows rendered as
    plain-language descriptions. The full diff exists in each row's
    stamp_audit payload but is NOT the primary display — the surface
    consumes `plain_description` and links to `full_diff_ref` on demand.

    Ordering: reverse-chronological (most recent first).
    """
    _, deny = await _require_master_admin_or_deny(request)
    if deny is not None:
        return deny
    # Read filtered ledger rows.
    cursor = (
        db[NORTHENA_LEDGER_COLLECTION]
        .find({"stamp_audit.data_class": DATA_CLASS_MASTER_ADMIN_RULE_CHANGE})
        .sort("at", -1)
        .limit(max(1, min(limit, 200)))
    )
    rows: List[dict] = []
    async for doc in cursor:
        stamp = doc.get("stamp_audit") or {}
        rc = stamp.get("rule_change") or {}
        rows.append({
            "run_id": doc.get("run_id"),
            "trace_id": doc.get("trace_id"),
            "at": (doc.get("at").isoformat() if doc.get("at") else None),
            "rule_id": rc.get("rule_id"),
            "grantor_id": rc.get("grantor_id"),
            "plain_description": _plain_description(rc),
            "full_diff_ref": f"/api/northena/ledger/by_run/{doc.get('run_id')}",
        })
    return {"actions": rows, "count": len(rows)}


# ────────────────────────────────────────────────────────────────────
# Phase 8 Seam 3 Sub-stage 3 — Owner-suspend endpoint (Ruling 3)
# ────────────────────────────────────────────────────────────────────


@router.post("/tightening/suspend")
async def post_tightening_suspend(request: Request):
    """§8 owner-suspend endpoint per Owner Ruling 3 (Amendment G, 2026-07-07):
    the ONLY action that halts an in-flight tightening.

    Auth: master_admin/admin role (E2 4-code registry).
    Body: {request_id: str, reason: str}.
    Behavior:
      - Refuses at 403 auth_scope_insufficient if caller lacks master_admin.
      - State-machine `suspend()` transitions pending_delay / pending_counter_sign → suspended.
      - Idempotent on already-suspended (200 returns existing state).
      - `effective` state is a 403 (Standing 409 anti-rule: no 409).
      - Emits `owner_suspended_tightening` ledger row.
    """
    identity, deny = await _require_master_admin_or_deny(request)
    if deny is not None:
        return deny
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_body", "detail": "Body must be JSON."},
        )
    request_id = (payload or {}).get("request_id")
    reason = (payload or {}).get("reason", "")
    if not isinstance(request_id, str) or not request_id:
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_payload", "detail": "request_id required."},
        )
    if not isinstance(reason, str) or not reason.strip():
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_payload", "detail": "reason required."},
        )
    from services.checker import state_machine
    from services.checker.countersign_ledger import emit_owner_suspended_row
    import uuid
    try:
        req = await state_machine.suspend(
            request_id=request_id,
            suspended_by_id=identity.email,
            suspended_by_role="admin",  # capacity role — Ruling 2
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
            detail=f"suspend_refused: {e}",
        )
    ledger = await emit_owner_suspended_row(
        run_id=f"sus-{uuid.uuid4().hex[:12]}",
        trace_id=f"sus-trace-{uuid.uuid4().hex[:12]}",
        rule_class=req.rule_class,
        request_id=req.request_id,
        consequence_class=req.consequence_class,
        suspended_by_id=identity.email,
        suspended_by_role="admin",
        reason=reason,
        suspended_at=req.suspended_at or "",
        prior_state=req.prior_state or "",
    )
    return {
        "state": req.state,
        "suspended_at": req.suspended_at,
        "ledger_row_ref": ledger.run_id,
    }


def _plain_description(rc: dict) -> str:
    """Turn a rule_change payload into a plain-language sentence
    per §6.3 elements verbatim: "plain description of the change
    (from → to in words), who, when".
    """
    rule_id = rc.get("rule_id", "unknown rule")
    from_v = rc.get("from")
    to_v = rc.get("to")
    reason = rc.get("reason_note")
    if rule_id == "tier_lock":
        state = "on" if to_v else "off"
        prior = "off" if not from_v else "on"
        base = f"Pricing tier lock turned {state} (was {prior})"
    else:
        base = f"{rule_id} changed from {from_v!r} to {to_v!r}"
    if reason:
        return f"{base} — {reason}."
    return f"{base}."
