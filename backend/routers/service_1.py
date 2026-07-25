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

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.async_delivery_accepted import AsyncDeliveryAccepted_v0
from contracts.composed_conclusion import ComposedConclusion_v0
from contracts.five_rings import DefensibilityClass, NormalizedUnit
from contracts.objective_request_v2 import ObjectiveRequest_v2
from contracts.service_1_refusal import Service1Refusal as Service1RefusalContract
from contracts.service_1_refusal_v1 import Service1Refusal_v1 as Service1RefusalContract_v1
from services.auth import auth_refusal, key_grants
from services.auth.dependencies import get_current_identity_or_none
from services.service_1 import async_worker as async_worker_module
from services.service_1 import composed_conclusion as composed_conclusion_module
from services.service_1 import dispatch as dispatch_module
from services.service_1 import qualified_data as qualified_data_module
from services.service_1 import service
from services.synisense.shield import fluency_synthesizer as fluency_synthesizer_module


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
            "model": Service1RefusalContract_v1,
            "description": (
                "Governed refusal (outcome='refused'). Frontend keys on "
                "body.outcome === 'refused'. Distinct from FastAPI's "
                "validation-422 which has detail: list and no outcome field. "
                "Post-EAB-2 seal (2026-07-24): envelope is Service1Refusal_v1 "
                "(11-field superset · 4-reason enum incl. coverage_gap · "
                "single-writer end-state per Owner ruling ε + α + γ · "
                "docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md)."
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
        # EAB-2 single-writer end-state: v0-emitting call-site transitions
        # to v1 envelope same commit as Parity 31→32 seal. Additive fields
        # (estate_region/period/source_class/filed_candidate_id) default
        # to None on evidential-family refusals per Owner ruling composition
        # ε + α + γ. v0 contract file (contracts/service_1_refusal.py)
        # remains byte-identical (Standing Rule v3 attested this atomic).
        refusal = Service1RefusalContract_v1(
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
                "Phase 4a §6.1 qualified-data warm-fork success OR "
                "Phase 4b §6.2 composed-conclusion warm-fork success."
            ),
        },
        202: {
            "model": AsyncDeliveryAccepted_v0,
            "description": (
                "Phase 5 §7 fresh-fork async admission accepted. "
                "AsyncDeliveryAccepted_v0 (20th frozen contract) body: "
                "`objective_id`, `status='accepted'`, `delivery_estimate`, "
                "`trace_id`, `accepted_at`, `quote?`. Poll "
                "`GET /api/objectives/{id}` for terminal envelope."
            ),
        },
        422: {
            "model": AdmissionRefusal_v0,
            "description": (
                "Governed refusal — AdmissionRefusal@v0 or "
                "Service1Refusal@v0 family. outcome='refused'. "
                "AdmissionRefusal fires for: form_not_offerable (§6.5), "
                "grain_form_incompatible (§6.1.4/§6.2.4), "
                "standard_below_admission_floor (§6.1.6), "
                "license_class_unavailable (§6.1.2), "
                "idempotency_key_missing (§7 bullet 6), "
                "idempotency_key_reused_with_different_body (§7 bullet 6). "
                "Service1Refusal fires for: composition_below_floor "
                "(§6.2.6). Frontend keys on body.outcome === 'refused'."
            ),
        },
        501: {
            "model": dispatch_module.DispatchResult,
            "description": (
                "Phase 2 scaffold: dispatch decided + placeholder emitted. "
                "Distinct from governed refusals by outcome discriminator."
            ),
        },
        503: {
            "description": (
                "Standing Disposition infra-not-refusal — the async delivery "
                "queue is saturated. NOT a governed refusal envelope; retry "
                "later. Clients render this as an infrastructure error, not "
                "a refusal-with-path. Load-bearing per Phase 5 Stage B."
            ),
        },
    },
)
async def v2_dispatch_endpoint(request: ObjectiveRequest_v2, http_request: Request) -> JSONResponse:
    """v3 §4/§7 shape-responsive dispatch — Phase 2/3/4a/4b/5b.

    Phase 8 Stage B-2 (Owner ruling verbatim, symmetric E2 cut):
      Auth is access-control class. Scope enforcement lands as a gate PAIR
      (not a wire change): granted key → dispatch executes (200/202/422/501);
      insufficient key → 403 with the E2 body shape
      `{"reason": "auth_scope_insufficient", "detail": "..."}` —
      NO `outcome` key, NO admission-refusal discriminator, NO governance
      semantics leaking into the auth-denial. Anonymous callers (no
      Authorization header) fall through to dispatch — Ask Console
      anonymous-friendly posture at B-1 is preserved.

    ZERO envelope delta on the 200/202/422 side (Owner ruling: "auth metadata
    off the intelligence envelope in both directions" — a 200 already
    implies scope passed).

    Return path fork (six arms via settled wire table):
      * `QualifiedDataPayload` (§6.1 warm) → 200
      * `ComposedConclusion_v0` (§6.2 warm) → 200
      * `AsyncDeliveryAccepted_v0` (§7 fresh async admission) → 202
      * `AdmissionRefusal_v0` (governed admission refusal) → 422
      * `Service1Refusal` (§6.2.6 composition_below_floor) → 422 via catch
      * `DispatchResult` (scaffold placeholder) → 501
      * QueueSaturatedError → HTTP 503 (infra-not-refusal doctrine).
    """
    # Phase 8 B-2 scope-enforcement gate pair (Owner E1+E2 ratified).
    # Anonymous: fall through (Ask Console B-1 posture).
    # Authenticated: verify {class="external", path="live_query",
    # floor=request.output.standard.minimum_class, scope=request.envelope.scope_ceiling}.
    identity = await get_current_identity_or_none(http_request)
    if identity is not None:
        # Coerce enum to its string value (DefensibilityClass is a str-Enum).
        min_class = request.output.standard.minimum_class
        required_floor = str(getattr(min_class, "value", min_class))
        required_scope = str(request.envelope.scope_ceiling)
        check = key_grants.check_scope(
            identity=identity,
            required_class="external",
            required_path="live_query",
            required_floor=required_floor,
            required_scope=required_scope,
        )
        if not check.granted:
            return auth_refusal.emit(
                "auth_scope_insufficient",
                detail=(
                    "Caller identity is authenticated but no granted key "
                    "matches the required scope tuple "
                    f"(class=external, path=live_query, "
                    f"floor={required_floor!r}, scope={required_scope!r})."
                ),
            )
    try:
        result = await dispatch_module.dispatch(request)
    except composed_conclusion_module.Service1Refusal as e:
        # EAB-2 single-writer end-state: v2/dispatch call-site also
        # transitions to v1 envelope same commit as Parity 31→32 seal.
        refusal = Service1RefusalContract_v1(
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
    except async_worker_module.QueueSaturatedError as exc:
        # Standing Disposition infra-not-refusal — NEVER an admission
        # refusal envelope. Bare 503 with a diagnostic detail.
        raise HTTPException(
            status_code=503,
            detail=f"async delivery queue saturated: {exc}",
        )
    except fluency_synthesizer_module.EmergentKeyMissingError as exc:
        # Answer Fluency AF-E2 amended boundary (Owner 2026-07-10):
        # CONFIG DEFECT → fail loud. Emergent LLM key missing/invalid
        # is a misconfigured deployment, not a runtime transient.
        # Standing Disposition `Infra-not-refusal` — NEVER a refusal
        # envelope. See docs/rulings/answer_fluency_af_e1_to_e4.md §1.2.
        raise HTTPException(
            status_code=503,
            detail=f"answer_fluency: emergent_key_missing: {exc}",
        )
    # Isinstance branch — five arms including the new 202:
    if isinstance(result, qualified_data_module.QualifiedDataPayload):
        return JSONResponse(
            status_code=200,
            content=result.model_dump(mode="json"),
        )
    if isinstance(result, ComposedConclusion_v0):
        return JSONResponse(
            status_code=200,
            content=result.model_dump(mode="json"),
        )
    if isinstance(result, AsyncDeliveryAccepted_v0):
        return JSONResponse(
            status_code=202,
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
