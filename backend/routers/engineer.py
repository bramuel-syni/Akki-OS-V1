"""Phase 8 Stage B-3 Block 3 — Engineer surface router (§4 backend).

Endpoints (all under `/api/engineer`):
  * POST /api/engineer/key_grants          — mint + persist + ledger-emit
  * GET  /api/engineer/key_grants          — list grants for the caller
      (or for a `?grantee_email=` query when caller is an admin/engineer)
  * POST /api/engineer/key_grants/{gid}/revoke — revoke + ledger-emit

Owner D4b ratification (2026-07-04): grant records are UNFROZEN
runtime shape pinned by the load-bearing wire-shape gate
(`tests/invariants/test_engineer_key_grant_load_bearing_wire_shape.py`);
grant lifecycle events emit `NorthenaLedgerRow_v1` rows via
`engineer_key_grant_ledger.record_engineer_key_grant_event`
(stamp_audit sidecar pattern, idempotent per (trace_id, run_id)).

Owner E2 taxonomy (Condition 2 attached to D4b):
  * Grant-endpoint denials are 403 `{reason, detail}` — 4-code
    registry ONLY (`auth_missing / auth_expired /
    auth_scope_insufficient / auth_identity_mismatch_for_wizard_session`).
  * NO new codes at B-3.
  * NO `outcome` key, NO `outcome=refused`, NO AdmissionRefusal_v0
    discriminator on auth-denial paths.
  * Validation failures (e.g., email invalid, justification too short)
    are 400 (FastAPI RequestValidationError shape) — cleanly OUTSIDE
    the auth taxonomy.
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from services.auth import auth_refusal
from services.auth.dependencies import require_identity_or_deny
from services.auth.engineer_key_grant import (
    EngineerKeyGrantRegistrationRequest,
    EngineerKeyGrantRevocationRequest,
)
from services.auth.engineer_key_grant_service import (
    GrantAlreadyRevoked,
    GrantNotFound,
    list_grants_for_grantee,
    register_grant,
    revoke_grant,
)
from services.auth.identity import Identity


router = APIRouter(prefix="/engineer", tags=["engineer"])


def _has_engineer_authority(identity: Identity) -> bool:
    """A caller may issue/revoke key-grants iff they carry the engineer
    role (or the admin role, which is the seeded super-role).

    NOT a scope-tuple check — engineer surface authority is role-gated
    per Owner intent. Individual GRANTS issued by this endpoint still
    lock down data-plane scope enforcement via `check_scope` on the
    grantee's downstream calls.
    """
    roles = set(identity.roles)
    return "engineer" in roles or "admin" in roles


async def _require_engineer_authority(request: Request):
    """Return (identity, None) on permit, (None, JSONResponse) on deny.

    Two-step gate:
      1. Bearer token → Identity (or 401 auth_missing / auth_expired).
      2. Identity → engineer/admin role (or 403 auth_scope_insufficient).
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return None, result
    identity: Identity = result
    if not _has_engineer_authority(identity):
        return None, auth_refusal.emit(
            "auth_scope_insufficient",
            detail=(
                "Engineer key-grant CRUD requires the `engineer` role "
                "(or `admin`). The caller identity is authenticated but "
                "lacks engineer authority."
            ),
        )
    return identity, None


@router.post("/key_grants", status_code=201)
async def post_key_grants(body: EngineerKeyGrantRegistrationRequest, request: Request):
    """Issue a new key-grant to a grantee.

    Two-step auth: (i) Bearer token → Identity; (ii) engineer/admin
    role required. Denials → 403 `{reason, detail}` per Owner E2.
    Validation failures → 400 (FastAPI default; outside auth taxonomy).

    Response body (201): EngineerKeyGrantRegistration as JSON.
    """
    identity, deny = await _require_engineer_authority(request)
    if deny is not None:
        return deny
    grant = await register_grant(req=body, grantor_id=identity.user_id)
    return JSONResponse(
        status_code=201,
        content=grant.model_dump(mode="json"),
    )


@router.get("/key_grants")
async def get_key_grants(request: Request, grantee_email: Optional[str] = None):
    """List key-grants.

    Two behaviors:
      * If `?grantee_email=<x>` present AND caller has engineer/admin
        authority → return grants for the queried grantee.
      * Otherwise → return grants for the CALLER's own email
        (self-service inspection; no authority required beyond
        authentication).
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    if grantee_email is not None:
        if not _has_engineer_authority(identity):
            return auth_refusal.emit(
                "auth_scope_insufficient",
                detail=(
                    "Listing grants for a different grantee requires "
                    "engineer/admin authority."
                ),
            )
        target_email = grantee_email.lower()
    else:
        target_email = identity.email.lower()
    grants = await list_grants_for_grantee(target_email)
    return {
        "grantee_email": target_email,
        "grants": [g.model_dump(mode="json") for g in grants],
    }


@router.post("/key_grants/{grant_id}/revoke")
async def post_revoke(
    grant_id: str,
    body: EngineerKeyGrantRevocationRequest,
    request: Request,
):
    """Revoke an active key-grant.

    Denials:
      * 401 auth_missing/expired — no valid Bearer token.
      * 403 auth_scope_insufficient — caller lacks engineer/admin role.
      * 404 grant not found (governance-agnostic — not an auth-denial).
      * 409 grant already revoked (governance-agnostic — not an auth-denial).
      * 200 with the updated Registration on success.
    """
    identity, deny = await _require_engineer_authority(request)
    if deny is not None:
        return deny
    try:
        updated = await revoke_grant(
            grant_id=grant_id, req=body, grantor_id=identity.user_id,
        )
    except GrantNotFound:
        return JSONResponse(
            status_code=404,
            content={"reason": "grant_not_found", "detail": f"grant_id={grant_id!r} does not exist."},
        )
    except GrantAlreadyRevoked:
        return JSONResponse(
            status_code=409,
            content={
                "reason": "grant_already_revoked",
                "detail": f"grant_id={grant_id!r} was previously revoked; revocation is idempotent-once.",
            },
        )
    return JSONResponse(
        status_code=200,
        content=updated.model_dump(mode="json"),
    )
