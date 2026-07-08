"""Phase 9 Sub-stage 9.3 — SM-E1..E3 sample lifecycle router."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from services.auth.dependencies import require_identity_or_deny
from services.perception import sample_lifecycle

router = APIRouter(prefix="/extraction", tags=["extraction"])


@router.post("/sample/run")
async def run_sample(request: Request) -> JSONResponse:
    """POST /api/extraction/sample/run — wizard-inline sample action."""
    auth = await require_identity_or_deny(request)
    if isinstance(auth, JSONResponse):
        return auth
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400,
                            content={"reason": "malformed_payload",
                                     "detail": "Body must be JSON."})
    if not isinstance(body, dict):
        return JSONResponse(status_code=400,
                            content={"reason": "malformed_payload",
                                     "detail": "Body must be object."})
    objective_ref = body.get("objective_ref")
    sample_bound_hours = body.get("sample_bound_hours", 2.0)
    idempotency_key = body.get("idempotency_key")
    if not objective_ref or not isinstance(objective_ref, str):
        return JSONResponse(status_code=400,
                            content={"reason": "malformed_payload",
                                     "detail": "objective_ref required."})
    try:
        sample_bound_hours = float(sample_bound_hours)
    except (TypeError, ValueError):
        return JSONResponse(status_code=400,
                            content={"reason": "malformed_payload",
                                     "detail": "sample_bound_hours must be numeric."})
    projected = await sample_lifecycle.run_sample(
        objective_ref, sample_bound_hours, idempotency_key)
    # Stub-first per P9-E7 α: advance to complete deterministically at 9.3.
    projected = await sample_lifecycle.stub_complete_sample(projected["sample_ref"])
    return JSONResponse(status_code=202, content=projected)


@router.get("/sample/{sample_ref}")
async def get_sample(sample_ref: str, request: Request) -> JSONResponse:
    auth = await require_identity_or_deny(request)
    if isinstance(auth, JSONResponse):
        return auth
    doc = await sample_lifecycle.get_sample(sample_ref)
    if doc is None:
        return JSONResponse(status_code=404,
                            content={"reason": "sample_not_found",
                                     "detail": f"sample_ref {sample_ref} not found."})
    return JSONResponse(status_code=200, content=doc)
