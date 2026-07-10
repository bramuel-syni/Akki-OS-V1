"""Callable Skill per-call inner gate (TF-E4 (a) α).

Owner ruling TF-E4 (a) α (2026-07-08):

    '(a) α; decorator composing the P8E-E2 single-source scope check
     + floor check + class-inline mutation — mechanism-not-convention;
     middleware rejected (route-drift leak); γ rejected (call-site
     convention).'

Landing:
  * `require_governed_skill_query(request, skill_id, db)` — FastAPI
    dependency composing (i) identity check (`require_identity_or_deny`),
    (ii) scope check via `check_scope` (P8E-E2 α single-source),
    (iii) floor check against the provisioning record's `floor`,
    (iv) returns the provisioning record for the endpoint to use.
  * Response class-inline mutation is enforced at the endpoint via
    `ensure_response_carries_class(...)` — the endpoint calls this
    on the outgoing response body before returning.
  * Refusal envelope for below-floor uses the standard refusal shape.
  * 403 for scope mismatch uses `auth_refusal.emit('auth_scope_insufficient', ...)`
    (4-code registry closure preserved).
"""
from __future__ import annotations

from typing import Any, Dict, Union

from fastapi import Request
from fastapi.responses import JSONResponse

from contracts.callable_skill_provisioning_v0 import CallableSkillProvisioningV0
from services.auth import auth_refusal
from services.auth.dependencies import require_identity_or_deny
from services.auth.key_grants import check_scope
from services.transform_forms.defensibility_loader import validate_defensibility_class
from services.transform_forms.callable_skill_persistence import load_provisioning

# Defensibility class ordering (from most-permissive to strictest, for the
# floor comparison). Sourced from the live composition path's Enum shape;
# any change to this ordering requires a governance ruling.
_CLASS_RANK = {
    "non_factual": 0,   # weakest defensibility (opinion / rhetorical)
    "utterance": 1,     # someone said it
    "fact": 2,          # matrix-permitted fact
}


class BelowFloorError(Exception):
    """Response class rank is below the provisioning record's floor."""


async def require_governed_skill_query(
    request: Request,
    skill_id: str,
    db: Any,
) -> Union[CallableSkillProvisioningV0, JSONResponse]:
    """Per-call inner gate: identity → scope → floor readiness.

    Composes (mechanism-not-convention):
      1. `require_identity_or_deny(request)` — 401 auth_missing / auth_expired.
      2. `check_scope(identity, ...)` against the provisioning record's
         key_grant_id + scope — 403 auth_scope_insufficient on mismatch.
      3. Returns the provisioning record (endpoint uses `.floor` to
         validate the response and calls `ensure_response_carries_class`).

    Returns:
      * CallableSkillProvisioningV0 on success.
      * JSONResponse (401 / 403 / 404) on failure.
    """
    identity_or_refusal = await require_identity_or_deny(request)
    if isinstance(identity_or_refusal, JSONResponse):
        return identity_or_refusal
    identity = identity_or_refusal

    provisioning = await load_provisioning(db, skill_id=skill_id)
    if provisioning is None:
        return JSONResponse(
            status_code=404,
            content={"reason": "skill_not_found", "detail": skill_id},
        )
    if provisioning.revoked_at is not None:
        return auth_refusal.emit(
            "auth_scope_insufficient",
            detail=f"Skill {skill_id} was revoked at {provisioning.revoked_at}.",
        )

    # Scope check via P8E-E2 α single-source (`check_scope`).
    scope_result = check_scope(
        identity,
        required_class="external",
        required_path="governed_extract",
        required_floor=provisioning.floor,
        required_scope=provisioning.scope,
    )
    if not scope_result.granted:
        return auth_refusal.emit(
            "auth_scope_insufficient",
            detail=f"Caller lacks scope grant for skill {skill_id}.",
        )

    return provisioning


def ensure_response_carries_class(
    response_body: Dict[str, Any],
    *,
    class_label: str,
    floor: str,
) -> Dict[str, Any]:
    """Response class-inline mutation per TF-E4 (a) α.iii + Owner Tier-1 line
    'every response carries class inline'.

    Validates class_label against the canonical registry (TF-E3 α),
    checks below-floor, and injects `defensibility.class` into the
    response body. Raises `BelowFloorError` if class_rank < floor_rank.
    """
    validate_defensibility_class(class_label)
    validate_defensibility_class(floor)

    if _CLASS_RANK[class_label] < _CLASS_RANK[floor]:
        raise BelowFloorError(
            f"Response class {class_label!r} is below the provisioned "
            f"floor {floor!r}. Refusal envelope required."
        )

    return {
        **response_body,
        "defensibility": {
            **response_body.get("defensibility", {}),
            "class": class_label,
        },
    }


def below_floor_refusal_envelope(*, class_label: str, floor: str) -> Dict[str, Any]:
    """Refusal envelope for below-floor responses (Owner Tier-1 line:
    'per-call inner gate refuses below floor')."""
    return {
        "outcome": "refused",
        "reason": "defensibility_below_floor",
        "detail": {
            "class": class_label,
            "floor": floor,
        },
    }
