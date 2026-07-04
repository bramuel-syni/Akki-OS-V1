"""Mtafiti router — Estate Feasibility Query endpoint (Phase 1).

Read-only. Objective-blind.

Route: `POST /api/mtafiti/feasibility`
  * Body: `Reach` (scope_refs, exclusions, depth)
  * Returns: `FeasibilityResult_v0` — never fabricates.

Registered in `server.py` alongside existing router includes.
"""
from fastapi import APIRouter

from contracts.feasibility_result import FeasibilityResult_v0
from contracts.objective_request_v2 import Reach
from services.mtafiti.feasibility import compute_feasibility


router = APIRouter(prefix="/mtafiti", tags=["mtafiti"])


@router.post(
    "/feasibility",
    response_model=FeasibilityResult_v0,
    summary="Estate Feasibility Query (v3 §5)",
)
async def feasibility_endpoint(reach: Reach) -> FeasibilityResult_v0:
    """v3 §5 Estate Feasibility Query.

    Consumed by both wizard variants (per-turn grounding) and admission
    (warm/fresh fork). Single query, dual consumers — same body.

    Read-only: no writes to any Mongo collection during handling.
    """
    return await compute_feasibility(reach)
