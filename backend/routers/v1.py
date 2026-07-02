"""FastAPI router — /api/v1/status surface.

Returns the harness state: last-run verdict, spike/production hour paths
if any, per-metric values when available. Public (same posture as
/api/health).
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from services.v1_harness import last_report

router = APIRouter(prefix="/v1", tags=["v1"])


class V1StatusResponse(BaseModel):
    verdict: str
    last_run_at: Optional[str]
    spike_hour_path: Optional[str]
    production_hour_path: Optional[str]
    metrics: Dict[str, Any]
    notes: list[str]


@router.get("/status", response_model=V1StatusResponse, summary="V1 measurement harness state.")
async def v1_status() -> V1StatusResponse:
    r = last_report()
    if r is None:
        return V1StatusResponse(
            verdict="PENDING_REAL_MATERIAL",
            last_run_at=None,
            spike_hour_path=None,
            production_hour_path=None,
            metrics={},
            notes=["harness has not run yet; awaiting real RMS Hour A material"],
        )
    d = r.to_dict()
    return V1StatusResponse(
        verdict=d["verdict"],
        last_run_at=d["timestamp"] or None,
        spike_hour_path=d["spike_hour_path"],
        production_hour_path=d["production_hour_path"],
        metrics=d["metrics"],
        notes=d["notes"],
    )
