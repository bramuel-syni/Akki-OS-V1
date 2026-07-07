"""Phase 8 Stage B-5a Block 1 — Compliance Console read/prove router.

Endpoints (all under `/api/compliance`):
  * GET  /api/compliance/retention_config  — v2.1 §4.3 substrate
      (3 held-classes separately addressable, inheritance-as-default,
       honest-when-unset for B5a-G3).
  * GET  /api/compliance/refusals?month=YYYY-MM  — v2.1 §4.1 refusals
      card substrate (family-classified count over NorthenaLedgerRow_v1).

Owner E2 taxonomy: all denials 401/403 `{reason, detail}` — 4-code
registry only. NO new codes at B-5a.

Auth scope: `dpo` OR `admin` (per Stage A §3A dev default) — mirrored
by `_has_dpo_authority` below. Master_admin role explicitly NOT granted
compliance-read scope by default (Compliance and Administration are
distinct consoles per v2.1 §4 and §6); use `admin` if a caller needs
both (the seeded super-role).
"""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from services.auth import auth_refusal
from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.compliance.coverage_marker import compose_coverage_marker
from services.compliance.refusals_aggregate import (
    MalformedMonthError,
    aggregate_refusals_by_month,
)
from services.compliance.retention_config import read_retention_config


router = APIRouter(prefix="/compliance", tags=["compliance"])


def _has_dpo_authority(identity: Identity) -> bool:
    """A caller may view Compliance Console surfaces iff they carry the
    `dpo` role (or `admin`, the seeded super-role)."""
    roles = set(identity.roles)
    return "dpo" in roles or "admin" in roles


async def _require_dpo_or_deny(request: Request):
    """Return (identity, None) on permit, (None, JSONResponse) on deny.
    Two-step gate mirroring the master_admin router pattern (B-4)."""
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return None, result
    identity: Identity = result
    if not _has_dpo_authority(identity):
        return None, auth_refusal.emit(
            "auth_scope_insufficient",
            detail=(
                "Compliance Console requires the `dpo` role (or `admin`). "
                "The caller identity is authenticated but lacks compliance "
                "authority."
            ),
        )
    return identity, None


@router.get("/refusals_coverage")
async def get_refusals_coverage(request: Request):
    """Sub-stage 1 Seam 3 substrate — refusals coverage marker.

    Returns per-family since-dates (E3.β query-time first-timestamp-per-family
    per Amendment E), the earliest date across seam-3-covered families, and
    an honest empty-state note when no refusal-terminal row carries a
    registered `stamp_audit["refusal_family"]` yet.

    Rendered by the Compliance Console §4.1 Refusals card rider as the
    Owner-supplied coverage-marker binding-copy (middle-dots `·` per E7).
    """
    _, deny = await _require_dpo_or_deny(request)
    if deny is not None:
        return deny
    resp = await compose_coverage_marker()
    return resp.model_dump(mode="json")


@router.get("/retention_config")
async def get_retention_config(request: Request):
    """v2.1 §4.3 substrate — read-only retention posture.

    Returns 3 held-classes with per-class posture (inheriting / explicit
    / unset) plus global_default. B5a-G3 substrate: when nothing set,
    all 3 classes render as unset and the surface fires the honest
    banner from v2.1 §4.3 line 76 verbatim.
    """
    _, deny = await _require_dpo_or_deny(request)
    if deny is not None:
        return deny
    resp = read_retention_config()
    return resp.model_dump(mode="json")


@router.get("/refusals")
async def get_refusals_by_month(request: Request, month: str = ""):
    """v2.1 §4.1 substrate — refusals-this-month aggregate.

    Query param `month=YYYY-MM` required. Returns family-classified
    totals over `NorthenaLedgerRow_v1` where `decision == "refused"`
    within the month window. Auth 403s + validation 422s STRUCTURALLY
    excluded (they don't write to the ledger).
    """
    _, deny = await _require_dpo_or_deny(request)
    if deny is not None:
        return deny
    try:
        resp = await aggregate_refusals_by_month(month)
    except MalformedMonthError as e:
        return JSONResponse(
            status_code=400,
            content={
                "reason": "malformed_month",
                "detail": str(e),
            },
        )
    return resp.model_dump(mode="json")
