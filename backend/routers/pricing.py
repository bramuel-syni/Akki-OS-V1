"""Pricing + Fleet control surface router — Phase 6 Stage B.

Master Admin control surface per v3 §8 bullets 2 + 5. Read endpoints are
open; write endpoints are gated by header `X-RMS-Master-Admin` matching
`RMS_MASTER_ADMIN_TOKEN` env (or by config presence of the token
`master_admin_only` sentinel in fleet-policy JSON — thin gate; full
auth surface Phase 8).

Standing Owner Dispositions applied here:
  * Ruling R3-SD2 config-as-versioned-not-frozen — writes bump the vN
    file, not in-place edit. This surface returns 501 on unsupported
    mutations (mutations that would violate versioning), 200 on
    Master-Admin-approved state-only writes (tier lock).
  * infra-not-refusal — capacity-unavailable is 503; governance-lock is
    422 AdmissionRefusal_v0.
"""
from __future__ import annotations

import os
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse

from services.economics import (
    fleet_policy as _fleet_policy,
    price_model as _price_model,
    quote_service as _quote_service,
)


router = APIRouter(prefix="/pricing", tags=["pricing"])
fleet_router = APIRouter(prefix="/fleet", tags=["fleet"])


def _require_master_admin(header_value: Optional[str]) -> None:
    """Master Admin gate — checks header against env var; fails 403 else.

    Phase 8 replaces this with the full app-registration surface + JWT
    scope check. Stage B keeps the surface thin per doctrine.
    """
    expected = os.environ.get("RMS_MASTER_ADMIN_TOKEN", "")
    if not expected:
        # Env-var not set → deployment does not carry a Master Admin;
        # writes are refused (governance decision, not infra).
        raise HTTPException(status_code=403, detail="Master Admin surface not configured.")
    if not header_value or header_value != expected:
        raise HTTPException(status_code=403, detail="Master Admin authorisation required.")


# ---------------------------------------------------------------------------
# Pricing read surface — model version + tiers.
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
async def post_model_version(
    x_rms_master_admin: Optional[str] = Header(default=None, alias="X-RMS-Master-Admin"),
) -> JSONResponse:
    """Master Admin bumps the model version — but ONLY via registry-bump
    (fresh price-model@vN.json file); this endpoint refuses in-place
    edits per Ruling R3-SD2.
    """
    _require_master_admin(x_rms_master_admin)
    return JSONResponse(
        status_code=501,
        content={
            "outcome": "not_yet_implemented",
            "reason": "phase_6_scaffold_registry_bump_via_disk_only",
            "hint": "Master Admin bumps by adding a fresh services/economics/price_model.vN.json file "
                    "and updating the pointer. In-place edit is a Ruling R3-SD2 violation.",
        },
    )


@router.get("/tiers")
async def get_tiers() -> dict:
    """v3 §8 bullet 2 registry read — enumerates known tiers per current bless."""
    import json
    from pathlib import Path
    registry_path = Path(_price_model._CONFIG_PATH).parent / "pricing_tiers.v0.json"
    return json.loads(registry_path.read_text(encoding="utf-8"))


@router.post("/tier_lock")
async def post_tier_lock(
    locked: bool,
    reason_note: Optional[str] = None,
    x_rms_master_admin: Optional[str] = Header(default=None, alias="X-RMS-Master-Admin"),
) -> dict:
    """Master Admin toggles current-bless tier lock. Governance decision;
    quote issuance refuses via `pricing_tier_frozen_by_control_surface` when set.
    """
    _require_master_admin(x_rms_master_admin)
    _quote_service.set_tier_lock(locked, reason_note)
    return {"locked": _quote_service.is_tier_locked(), "reason_note": reason_note}


# ---------------------------------------------------------------------------
# Fleet policy surface.
# ---------------------------------------------------------------------------


@fleet_router.get("/policy")
async def get_fleet_policy() -> dict:
    return _fleet_policy.load_config()


@fleet_router.post("/policy")
async def post_fleet_policy(
    x_rms_master_admin: Optional[str] = Header(default=None, alias="X-RMS-Master-Admin"),
) -> JSONResponse:
    """Master Admin bumps fleet policy via `fleet_policy.vN.json`
    additive-only (Ruling R3-SD2). This endpoint refuses in-place edits.
    """
    _require_master_admin(x_rms_master_admin)
    return JSONResponse(
        status_code=501,
        content={
            "outcome": "not_yet_implemented",
            "reason": "phase_6_scaffold_registry_bump_via_disk_only",
            "hint": "Master Admin bumps by adding a fresh services/economics/fleet_policy.vN.json file "
                    "and updating the pointer. In-place edit is a Ruling R3-SD2 violation.",
        },
    )
