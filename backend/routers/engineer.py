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
from services.auth.engineer_scope import require_own_scope_or_deny
from services.auth.identity import Identity
from services.auth import engineer_invites


router = APIRouter(prefix="/engineer", tags=["engineer"])


def _has_engineer_authority(identity: Identity) -> bool:
    """A caller may reach the engineer surface iff they carry an engineer
    role (or admin/master_admin).

    Includes `external_engineer` per Owner P8E-E1 α (2026-07-08): the
    external role reaches the engineer surface but is narrowed by
    `require_own_scope_or_deny` per EE-R4 verbatim (server-side own-scope
    enforcement rides B-1 primitive; no parallel mechanism).
    """
    roles = set(identity.roles)
    return bool(roles & {"engineer", "external_engineer", "admin", "master_admin"})


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
    # P8E-E2 α own-scope enforcement — external_engineer may only issue
    # grants naming themselves as grantee. Rides B-1 primitive via
    # `require_own_scope_or_deny`; single source (grep-negative attested).
    scope_deny = require_own_scope_or_deny(identity, body.grantee_email)
    if scope_deny is not None:
        return scope_deny
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
        authority → return grants for the queried grantee (subject to
        P8E-E2 α own-scope narrowing for external_engineer).
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
        # P8E-E2 α own-scope: external_engineer may only query their own email.
        scope_deny = require_own_scope_or_deny(identity, grantee_email)
        if scope_deny is not None:
            return scope_deny
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
      * 403 auth_scope_insufficient — caller lacks engineer/admin role,
        OR external_engineer attempted to revoke a foreign grant
        (P8E-E2 α own-scope).
      * 404 grant not found (governance-agnostic — not an auth-denial).
      * 409 grant already revoked (governance-agnostic — not an auth-denial).
      * 200 with the updated Registration on success.
    """
    identity, deny = await _require_engineer_authority(request)
    if deny is not None:
        return deny
    # P8E-E2 α own-scope enforcement — external_engineer may only revoke
    # grants they own (grantee_email == identity.email).
    # Lookup grant's grantee_email BEFORE revoking to check own-scope.
    from services.auth.engineer_key_grant_service import get_grant as get_grant_by_id
    existing_grant = await get_grant_by_id(grant_id)
    if existing_grant is not None:
        scope_deny = require_own_scope_or_deny(
            identity, existing_grant.grantee_email,
        )
        if scope_deny is not None:
            return scope_deny
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


# ------------------------------------------------------------------------
# Phase 8-EXT — invited-approved onboarding endpoints (P8E-E3 α, P8E-E7 α).
# ------------------------------------------------------------------------


def _require_internal_engineer(identity: Identity) -> bool:
    """Only internal engineer (or admin) may issue / approve invites.

    P8E-E5 α record: `engineer` role IS the internal_engineer identifier;
    external_engineer role is NOT sufficient for onboarding operations.
    """
    roles = set(identity.roles)
    return bool(roles & {"engineer", "admin", "master_admin"})


@router.post("/onboarding/invite", status_code=201)
async def post_onboarding_invite(request: Request):
    """Internal engineer issues an invite for a prospective external engineer.

    Body: {"invited_email": "..."}.
    Response 201: the invite row (P8E-E3 α; DB-persisted).
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    if not _require_internal_engineer(identity):
        return auth_refusal.emit(
            "auth_scope_insufficient",
            detail=(
                "Only internal `engineer` (or `admin`) may issue an "
                "external-engineer onboarding invite."
            ),
        )
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_payload", "detail": "Body must be JSON."},
        )
    invited_email = (body or {}).get("invited_email")
    if not invited_email or not isinstance(invited_email, str):
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_payload", "detail": "invited_email required."},
        )
    invite = await engineer_invites.issue_invite(
        invited_email=invited_email, invited_by=identity.email,
    )
    return JSONResponse(status_code=201, content=invite)


@router.post("/onboarding/approve", status_code=200)
async def post_onboarding_approve(request: Request):
    """Internal engineer approves a pending invite.

    Body: {"invite_id": "..."}.
    On success:
      * The invite row transitions pending_invite → approved atomically.
      * A `stamp_audit.data_class = engineer_onboarding_approved` ledger
        row is emitted per P8E-E7 α (registry v3 additive; data-class
        LB gate auto-extended via `deletion_ledger.py` loader re-point).
      * An access JWT is minted for the invited_email with the
        `external_engineer` role (P8E-E3 α; JWT mechanics unchanged —
        the same `create_access_token()` path used everywhere else).

    Response 200:
      { "invite": {...}, "external_engineer_token": "<jwt>", "ledger": {...} }
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result
    if not _require_internal_engineer(identity):
        return auth_refusal.emit(
            "auth_scope_insufficient",
            detail=(
                "Only internal `engineer` (or `admin`) may approve an "
                "external-engineer onboarding invite."
            ),
        )
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_payload", "detail": "Body must be JSON."},
        )
    invite_id = (body or {}).get("invite_id")
    if not invite_id or not isinstance(invite_id, str):
        return JSONResponse(
            status_code=400,
            content={"reason": "malformed_payload", "detail": "invite_id required."},
        )
    approved = await engineer_invites.approve_invite(invite_id)
    if approved is None:
        return JSONResponse(
            status_code=404,
            content={
                "reason": "invite_not_approvable",
                "detail": f"invite_id={invite_id!r} not found, already used, or expired.",
            },
        )
    # Mint an external_engineer access JWT — no new JWT class per P8E-E3 α.
    from services.auth.jwt_service import create_access_token
    token = create_access_token(
        user_id=f"ext-{approved['invite_id']}",
        email=approved["invited_email"],
        roles=["external_engineer"],
        key_grants=[],
    )
    # Emit engineer_onboarding_approved ledger row per P8E-E7 α.
    ledger_row = await engineer_invites.emit_onboarding_approved_ledger_row(
        invited_email=approved["invited_email"],
        invited_by=approved["invited_by"],
        invite_id=approved["invite_id"],
        approved_at=approved["approved_at"],
    )
    return JSONResponse(
        status_code=200,
        content={
            "invite": approved,
            "external_engineer_token": token,
            "ledger_row_id": ledger_row["row_id"],
        },
    )
