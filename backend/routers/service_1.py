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

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.five_rings import DefensibilityClass, NormalizedUnit
from contracts.objective_request_v2 import ObjectiveRequest_v2
from contracts.service_1_refusal import Service1Refusal as Service1RefusalContract
from services.service_1 import dispatch as dispatch_module
from services.service_1 import qualified_data as qualified_data_module
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


# ---------------------------------------------------------------------------
# Phase 2 additive-only landing — shape-responsive execution dispatch (v2).
#
# v0 route (`POST /run` above) remains byte-identical. This v2 route accepts
# `ObjectiveRequest_v2` and returns a Phase-2-scaffold `DispatchResult` per
# owner ruling. Response envelope is UNFROZEN at Phase 2 (Ruling 3 pattern
# — mechanism, not values).
#
# Every Phase 2 response carries a governed `placeholder_body` (outcome =
# `not_yet_implemented`) because no downstream receiver is built yet. Status
# is 501 — "known route, receiver not built" — per owner scope declaration.
# Rendering separation from `Service1Refusal@v0` (outcome=refused) is
# enforced by `test_dispatch_placeholder_never_leaks_into_governed_refusal`.
# ---------------------------------------------------------------------------


@router.post(
    "/v2/dispatch",
    responses={
        200: {
            "description": (
                "Phase 4a §6.1 qualified-data warm-fork success. Body is "
                "an UNFROZEN payload (Stage A Section 7 Candidate 2) with "
                "top-level `units`/`receipt`/`unit_count`/`computed_at`; "
                "`receipt` conforms to OuterGateReceipt@v0 (frozen). "
                "Ruling 3 wire-shape gate pins these keys."
            ),
        },
        422: {
            "model": AdmissionRefusal_v0,
            "description": (
                "Governed admission-time refusal (Phase 3 + Phase 4a). "
                "outcome='refused'. Family with Service1Refusal@v0. "
                "Fires for: form_not_offerable (§6.5), "
                "grain_form_incompatible (§6.1.4/§6.2.4/etc), "
                "standard_below_admission_floor (§6.1.6), "
                "license_class_unavailable (§6.1.2). "
                "Frontend keys on body.outcome === 'refused'."
            ),
        },
        501: {
            "model": dispatch_module.DispatchResult,
            "description": (
                "Phase 2 scaffold: dispatch decided + placeholder emitted. "
                "Downstream receiver (Phase 4b/5) not built yet. Distinct "
                "from AdmissionRefusal@v0 by outcome discriminator "
                "(placeholder_body.outcome == 'not_yet_implemented' vs "
                "top-level outcome == 'refused')."
            ),
        },
    },
)
async def v2_dispatch_endpoint(request: ObjectiveRequest_v2) -> JSONResponse:
    """v3 §4 shape-responsive dispatch — Phase 2/3/4a.

    Return path fork (three arms):
      * `QualifiedDataPayload` (§6.1 warm success) → HTTP 200, UNFROZEN
        payload with governance-carrying keys pinned by Ruling 3 gate.
      * `AdmissionRefusal_v0` (governed admission refusal) → HTTP 422,
        flat JSON body per A2 family pattern. Fires for the four
        Phase-3/Phase-4a admission-time refusal reasons.
      * `DispatchResult` (scaffold placeholder) → HTTP 501, envelope
        body with placeholder_body naming the phase-debt receiver.
    """
    result = await dispatch_module.dispatch(request)
    # Isinstance branch — three arms:
    #   200 for §6.1 qualified-data success (Phase 4a landing)
    #   422 for governed refusal (mirrors Service1Refusal@v0 at A2)
    #   501 for scaffold placeholder (Phase 2 receiver-not-built)
    if isinstance(result, qualified_data_module.QualifiedDataPayload):
        return JSONResponse(
            status_code=200,
            content=result.model_dump(mode="json"),
        )
    if isinstance(result, AdmissionRefusal_v0):
        return JSONResponse(
            status_code=422,
            content=result.model_dump(mode="json"),
        )
    return JSONResponse(
        status_code=501,
        content=result.model_dump(mode="json"),
    )
