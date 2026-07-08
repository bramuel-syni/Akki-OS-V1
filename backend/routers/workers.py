"""Phase 9 Sub-stage 9.1 — worker plane router.

Two endpoints — the ONLY two a worker credential unlocks:
  * POST /api/workers/jobs/claim
  * POST /api/workers/jobs/{job_id}/result

Auth: capabilities-claim worker JWT (P9-E3 α). Never touches DB
directly beyond the job dispatcher; never reads Ledger; never reads keys.
Denials use the closed 4-code auth-refusal registry.
"""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from contracts.perception_result_v0 import PerceptionResult_v0
from services.perception import job_dispatcher
from services.perception.worker_credential import (
    CAP_CLAIM, CAP_RESULT, require_worker_capability,
)

router = APIRouter(prefix="/workers", tags=["workers"])


@router.post("/jobs/claim")
async def claim_job(request: Request) -> JSONResponse:
    """POST /api/workers/jobs/claim — claim next queued job.

    Body: {worker_id, capabilities}. 200 PerceptionJob | 204 no work.
    """
    gate = await require_worker_capability(request, CAP_CLAIM)
    if isinstance(gate, JSONResponse):
        return gate
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400,
                            content={"reason": "malformed_payload",
                                     "detail": "Request body must be JSON."})
    worker_id = body.get("worker_id") if isinstance(body, dict) else None
    if not worker_id or not isinstance(worker_id, str):
        return JSONResponse(status_code=400,
                            content={"reason": "malformed_payload",
                                     "detail": "worker_id required."})
    job = await job_dispatcher.claim_next(worker_id)
    if job is None:
        return JSONResponse(status_code=204, content=None)
    return JSONResponse(status_code=200, content=job.model_dump())


@router.post("/jobs/{job_id}/result")
async def post_result(job_id: str, request: Request) -> JSONResponse:
    """POST /api/workers/jobs/{job_id}/result — accept PerceptionResult.

    202 accepted, idempotent on (job_id, checkpoint). Repeat post with
    same checkpoint returns 202 with `result: idempotent_replay`.
    """
    gate = await require_worker_capability(request, CAP_RESULT)
    if isinstance(gate, JSONResponse):
        return gate
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(status_code=400,
                            content={"reason": "malformed_payload",
                                     "detail": "Request body must be JSON."})
    if not isinstance(body, dict):
        return JSONResponse(status_code=400,
                            content={"reason": "malformed_payload",
                                     "detail": "Body must be an object."})
    # Route job_id from URL, ignoring body's job_id if mismatched.
    body["job_id"] = job_id
    try:
        result = PerceptionResult_v0(**body)
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={"reason": "malformed_payload",
                                     "detail": f"PerceptionResult validation failed: {e}"})
    if await job_dispatcher.get_job(job_id) is None:
        return JSONResponse(status_code=404,
                            content={"reason": "job_not_found",
                                     "detail": f"job_id {job_id} not found."})
    outcome: Dict[str, Any] = await job_dispatcher.apply_result(
        job_id, result.model_dump())
    return JSONResponse(status_code=202, content=outcome)
