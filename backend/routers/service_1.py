"""Service 1 v1 — Day-Zero Estate Extraction API surface.

Two endpoints per Interface Spec cross-reference (see
`docs/g4_prep/service_1_v1_scope_from_source.md` §3):

  * POST /api/service_1/run — accepts governing artifact fields + a list
    of NormalizedUnits; returns run summary + trace_id + plan_id.
  * GET  /api/service_1/run/{run_id} — returns Ledger-correlated status.

Response contracts:
  * Service1RunSummary — success 200 (Pydantic response envelope, NOT
    a frozen artifact).
  * Service1RunStatus — status 200 (same).
  * Service1RefusalContract — governed 422 refusal envelope. FROZEN
    contract as of A2 (14th freeze). See contracts/service_1_refusal.py.

Structural note: both models surface via `/api/openapi.json` per
G2a discipline. A2 D3a: refusal is a flat JSONResponse with
outcome=refused at top level, distinct from FastAPI's default
RequestValidationError (which has detail: list, no outcome).
"""
from typing import List, Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from contracts.five_rings import DefensibilityClass, NormalizedUnit
from contracts.service_1_refusal import Service1Refusal as Service1RefusalContract
from services.service_1 import service


router = APIRouter(prefix="/service_1", tags=["service_1"])


class Service1RunRequest(BaseModel):
    """Day-Zero governing artifact + input units."""
    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(..., description="Portfolio Mandate id.")
    artifact_version: str
    lawful_basis: str = Field(..., description="DPA lawful basis ref.")
    floor: DefensibilityClass = Field(..., description="Composition-time floor.")
    scope_key: str = Field(default="portfolio")
    objective_text: str = Field(
        ...,
        min_length=1,
        description=(
            "Plain-language objective — surfaced back into the refusal "
            "envelope's `asked` field per RMS_Interface_Specification.md §201."
        ),
    )
    units: List[NormalizedUnit]


class Service1RunSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    trace_id: str
    mining_plan_id: str
    registry_snapshot_ref: str
    converged_unit_count: int
    defensibility_floor: str
    ledger_correlation_ref: str
    yield_layer_version: str


class Service1RunStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    stage: str
    decision: Optional[str] = None
    mining_plan_id: Optional[str] = None
    converged_unit_count: Optional[int] = None
    ledger_row_count: Optional[int] = None


@router.get("/status")
async def status() -> dict:
    return {
        "gate": "G4",
        "service": "service_1_day_zero",
        "note": "Service 1 v1 — Day-Zero Estate Extraction. Terminates at convergence.",
        "closed_seams": ["mtafiti_v3_overlay", "targeta_yield_layer"],
    }


@router.post(
    "/run",
    responses={
        200: {"model": Service1RunSummary},
        422: {
            "model": Service1RefusalContract,
            "description": (
                "Governed refusal (outcome='refused'). Frontend keys on "
                "body.outcome === 'refused'. Distinct from FastAPI's "
                "validation-422 which has detail: list and no outcome field."
            ),
        },
    },
)
async def run_endpoint(req: Service1RunRequest):
    try:
        result = await service.run(
            req.units,
            objective_text=req.objective_text,
            artifact_id=req.artifact_id,
            artifact_version=req.artifact_version,
            lawful_basis=req.lawful_basis,
            floor=req.floor,
            scope_key=req.scope_key,
        )
    except service.Service1Refusal as e:
        refusal = Service1RefusalContract(
            reason=e.reason,
            run_id=e.run_id,
            trace_id=e.trace_id,
            asked=e.asked,
            supported_class=e.supported_class,
            what_would_raise_it=e.what_would_raise_it,
        )
        return JSONResponse(
            status_code=422,
            content=refusal.model_dump(mode="json"),
        )
    return Service1RunSummary(**result)


@router.get("/run/{run_id}", response_model=Service1RunStatus)
async def run_status(run_id: str) -> Service1RunStatus:
    result = await service.status_by_run(run_id)
    return Service1RunStatus(**result)
