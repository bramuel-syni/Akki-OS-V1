"""FastAPI router — /api/v3/status + /api/v1/stamp_audit/*.

G1-only surfaces; absorbed by Northena ledger query routes at G2.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from services.g1_defensibility import stamp_audit
from services.v3_harness import gates, last_report

router = APIRouter(tags=["g1"])


class V3StatusResponse(BaseModel):
    verdict: str
    last_run_at: Optional[str]
    metrics: Dict[str, Any]
    labelled_set_summary: Dict[str, Any]
    gates: Dict[str, float]
    notes: List[str]


class StampAuditEntryDTO(BaseModel):
    unit_id: str
    decision: str
    reason: Optional[str]
    judged_signal_dimensions: List[str]
    floor_violation: bool
    runtime_mode: str
    timestamp: str


@router.get("/v3/status", response_model=V3StatusResponse, summary="V3 measurement harness state.")
async def v3_status() -> V3StatusResponse:
    r = last_report()
    if r is None:
        return V3StatusResponse(
            verdict="PENDING_REAL_LABELLED_SET",
            last_run_at=None,
            metrics={},
            labelled_set_summary={},
            gates=gates(),
            notes=["V3 harness has not run; awaiting real labelled slice (>=300 units, kappa >=0.70, >=2 labellers)."],
        )
    d = r.to_dict()
    return V3StatusResponse(
        verdict=d["verdict"], last_run_at=d["timestamp"] or None,
        metrics=d["metrics"], labelled_set_summary=d["labelled_set_summary"],
        gates=gates(), notes=d["notes"],
    )


@router.get("/v1/stamp_audit/recent", response_model=List[StampAuditEntryDTO],
            summary="Recent stamp-audit entries (ring buffer; G1-only).")
async def stamp_audit_recent(limit: int = 100) -> List[StampAuditEntryDTO]:
    return [StampAuditEntryDTO(**e.to_dict()) for e in stamp_audit.recent(limit=limit)]


@router.get("/v1/stamp_audit/by_unit/{unit_id}", response_model=List[StampAuditEntryDTO])
async def stamp_audit_by_unit(unit_id: str) -> List[StampAuditEntryDTO]:
    return [StampAuditEntryDTO(**e.to_dict()) for e in stamp_audit.by_unit_id(unit_id)]
