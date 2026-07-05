"""Pricing + Fleet control surface router.

Phase 6 Stage B origin — Master Admin control surface per v3 §8 bullets 2 + 5.

**Phase 8 Stage B-4 auth reconciliation** (Owner ratified, 2026-07-05):
`RMS_MASTER_ADMIN_TOKEN` env-gating and the `X-RMS-Master-Admin` header
are RETIRED. Highest-privilege surface now uses JWT `master_admin` role
check exclusively. Zero production consumers of the retired token
remained pre-retirement (audit at Stage-A close).

**Phase 8 Stage B-4 Path A / Path B disposition** (Owner ratified):
  * `POST /pricing/tier_lock` → **Path A**: writes `tier_lock.vN.json`
    versioned marker + emits `NorthenaLedgerRow_v1` via
    `services/economics/tier_lock_ledger.record_master_admin_rule_change`
    (stamp_audit sidecar, idempotent per (rule_id, idempotency_key)).
  * `POST /pricing/model_version` → **Path B**: honest 501 with
    plain-language `detail` in `{reason, detail}` body — no technical
    hint, no client-side ghosting.
  * `POST /fleet/policy` → **Path B**: same as model_version.

Never Path C (no in-place mutation, no ghosting, no deferred queue).
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from services.auth import auth_refusal
from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity
from services.economics import (
    fleet_policy as _fleet_policy,
    price_model as _price_model,
    quote_service as _quote_service,
)
from services.economics.tier_lock_ledger import (
    _find_existing_row,
    _run_id_for,
    record_master_admin_rule_change,
)


router = APIRouter(prefix="/pricing", tags=["pricing"])
fleet_router = APIRouter(prefix="/fleet", tags=["fleet"])


async def _require_master_admin_or_deny(request: Request):
    """Two-step gate mirroring B-3 engineer authority pattern:
      1. Bearer token → Identity (or 401 auth_missing / auth_expired).
      2. Identity → master_admin/admin role (or 403 auth_scope_insufficient).

    Returns `(identity, None)` on permit; `(None, JSONResponse)` on deny.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return None, result
    identity: Identity = result
    roles = set(identity.roles)
    if not ("master_admin" in roles or "admin" in roles):
        return None, auth_refusal.emit(
            "auth_scope_insufficient",
            detail=(
                "Pricing / Fleet control surface requires the `master_admin` "
                "role (or `admin`). The caller identity is authenticated but "
                "lacks master-admin authority."
            ),
        )
    return identity, None


# ---------------------------------------------------------------------------
# Pricing read surface — model version + tiers (open reads).
# ---------------------------------------------------------------------------


@router.get("/model_version")
async def get_model_version() -> dict:
    """v3 §8 bullet 2: quote-side integrators query current model version."""
    cfg = _price_model.load_config()
    return {
        "price_model_version": cfg["version"],
        "tier": cfg["tier"],
        "expires_at": cfg.get("expires_at"),
        "hazard_stop_notes": cfg.get("hazard_stop_notes", []),
    }


@router.post("/model_version")
async def post_model_version(request: Request) -> JSONResponse:
    """Path B — honest 501 with plain-language detail.

    Changing the price model requires a versioned file update on the
    server. UI cannot safely mutate the disk contract under Ruling
    R3-SD2. The 501 surfaces this fact in plain language; the UI renders
    `detail` verbatim in the "What changes" info box.
    """
    _, deny = await _require_master_admin_or_deny(request)
    if deny is not None:
        return deny
    return JSONResponse(
        status_code=501,
        content={
            "reason": "requires_versioned_file_change_by_owner",
            "detail": (
                "Changing the price model requires a versioned file update on "
                "the server. Contact Owner. No change applied."
            ),
        },
    )


@router.get("/tiers")
async def get_tiers() -> dict:
    """v3 §8 bullet 2 registry read — enumerates known tiers per current bless."""
    registry_path = Path(_price_model._CONFIG_PATH).parent / "pricing_tiers.v0.json"
    return json.loads(registry_path.read_text(encoding="utf-8"))


class TierLockRequest(BaseModel):
    """Path A body per Owner amendment 2026-07-05."""
    model_config = ConfigDict(extra="forbid")
    locked: bool
    reason_note: Optional[str] = None
    idempotency_key: Optional[str] = None


def _next_tier_lock_version_path() -> Path:
    """Return path for the NEXT versioned tier_lock file (append-only)."""
    base = Path(_price_model._CONFIG_PATH).parent
    existing = sorted(base.glob("tier_lock.v*.json"))
    n = len(existing)
    return base / f"tier_lock.v{n}.json"


@router.post("/tier_lock")
async def post_tier_lock(body: TierLockRequest, request: Request) -> JSONResponse:
    """Path A — write versioned file + emit ledger row + set runtime state.

    Idempotent per `(rule_id="tier_lock", idempotency_key)`. Repeat POST
    with the same idempotency_key returns the same `ledger_run_id` +
    `versioned_file_path` without a second file-write or ledger row.

    Reversibility: opposite POST (`locked=<opposite>`) writes a NEW
    versioned file + NEW ledger row — historical record is append-only;
    runtime state moves.
    """
    identity, deny = await _require_master_admin_or_deny(request)
    if deny is not None:
        return deny
    prior_locked = _quote_service.is_tier_locked()
    idempotency_key = body.idempotency_key or uuid.uuid4().hex[:16]
    # Idempotency short-circuit: if the same idempotency_key was used
    # for this rule already, return the SAME response (no new file, no
    # new ledger row, runtime state left as-is).
    prior_run_id = _run_id_for("tier_lock", idempotency_key)
    prior_row = await _find_existing_row(prior_run_id)
    if prior_row is not None:
        prior_stamp = (prior_row.get("stamp_audit") or {}).get("rule_change") or {}
        return JSONResponse(
            status_code=200,
            content={
                "locked": _quote_service.is_tier_locked(),
                "reason_note": prior_stamp.get("reason_note"),
                "trace_id": prior_row.get("trace_id"),
                "ledger_run_id": prior_run_id,
                "versioned_file_path": prior_stamp.get("versioned_file_path"),
                "at": prior_row["at"].isoformat() if prior_row.get("at") else None,
            },
        )
    versioned_path = _next_tier_lock_version_path()
    # Write versioned file (append-only marker).
    marker = {
        "rule_id": "tier_lock",
        "locked": bool(body.locked),
        "reason_note": body.reason_note,
        "grantor_id": identity.user_id,
        "idempotency_key": idempotency_key,
        "at": datetime.now(timezone.utc).isoformat(),
    }
    if not versioned_path.exists():
        versioned_path.write_text(json.dumps(marker, indent=2), encoding="utf-8")
    trace_id = f"master-admin-tier-lock-{uuid.uuid4().hex[:12]}"
    ledger = await record_master_admin_rule_change(
        rule_id="tier_lock",
        from_value=bool(prior_locked),
        to_value=bool(body.locked),
        reason_note=body.reason_note,
        versioned_file_path=str(versioned_path.relative_to(Path("/app").resolve())),
        grantor_id=identity.user_id,
        idempotency_key=idempotency_key,
        trace_id=trace_id,
    )
    # Set runtime state AFTER the audit chain lands.
    _quote_service.set_tier_lock(body.locked, body.reason_note)
    return JSONResponse(
        status_code=200,
        content={
            "locked": _quote_service.is_tier_locked(),
            "reason_note": body.reason_note,
            "trace_id": ledger["trace_id"],
            "ledger_run_id": ledger["run_id"],
            "versioned_file_path": str(
                versioned_path.relative_to(Path("/app").resolve())
            ),
            "at": marker["at"],
        },
    )


# ---------------------------------------------------------------------------
# Fleet policy surface.
# ---------------------------------------------------------------------------


@fleet_router.get("/policy")
async def get_fleet_policy() -> dict:
    return _fleet_policy.load_config()


@fleet_router.post("/policy")
async def post_fleet_policy(request: Request) -> JSONResponse:
    """Path B — honest 501 with plain-language detail.

    Changing GPU capacity apportionment requires a versioned file update
    on the server. UI cannot safely mutate the disk contract under
    Ruling R3-SD2.
    """
    _, deny = await _require_master_admin_or_deny(request)
    if deny is not None:
        return deny
    return JSONResponse(
        status_code=501,
        content={
            "reason": "requires_versioned_file_change_by_owner",
            "detail": (
                "Changing GPU capacity apportionment requires a versioned "
                "file update on the server. Contact Owner. No change applied."
            ),
        },
    )
