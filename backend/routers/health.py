"""Health router (PH-R1 · BCR v1.5 §3.4 annex verbatim).

Endpoints:
    GET /api/healthz  liveness  · no auth · no DB touch
    GET /api/readyz   readiness · DB ping + frozen-contract parity count

Owner ruling PH-E3 α (2026-07-10):
    "FS enumeration sharing V1-G7's authoritative counter — readiness
    and the parity gate must never disagree about what parity is, and
    one counting mechanism guarantees that."

Refusal taxonomy stays closed: 503 here is an infra readiness signal,
NEVER a refusal envelope (AF-E2 amended posture).
"""
from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from core import db
from services.health import (
    EXPECTED_PARITY,
    count_frozen_contract_snapshots,
)

router = APIRouter(tags=["health"])
log = logging.getLogger("rms.health")

_READY_TIMEOUT_SECONDS: float = 2.0


@router.get("/healthz")
async def healthz() -> dict:
    """Liveness — no auth · no DB touch (BCR annex verbatim)."""
    return {"status": "alive"}


@router.get("/readyz")
async def readyz() -> JSONResponse:
    """Readiness — DB ping + frozen-contract parity count (BCR annex verbatim).

    Returns 200 on both green, 503 on either failure.
    """
    # (1) Frozen-contract parity via shared FS-enumeration counter.
    #     Same source as V1-G7 · same source as /api/system/build_info.
    parity = count_frozen_contract_snapshots()
    if parity != EXPECTED_PARITY:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "reason": "parity_mismatch",
                "parity_count": parity,
                "expected_parity": EXPECTED_PARITY,
            },
        )

    # (2) Mongo ping with short timeout.
    try:
        await asyncio.wait_for(db.command("ping"), timeout=_READY_TIMEOUT_SECONDS)
    except Exception as exc:  # noqa: BLE001 — infra readiness catches all classes
        log.warning("readyz.db_ping_failed reason=%s", type(exc).__name__)
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "reason": "db_ping_failed",
                "parity_count": parity,
                "expected_parity": EXPECTED_PARITY,
            },
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "ready",
            "parity_count": parity,
            "expected_parity": EXPECTED_PARITY,
            "db": "ok",
        },
    )
