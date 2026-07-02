"""Contract-surfacing routes — G0 follow-up.

Closes tester TEST 4: the three frozen Pydantic contracts (Five Rings'
NormalizedUnit, ObjectiveRequest, QualificationMatrix) were snapshot-frozen
on disk and reachable through `backend/tests/invariants/`, but they were
not declared in the live OpenAPI surface's `components.schemas`. That
broke the "machine-discoverable through the live contract" property of
the frozen-contract discipline.

This module mounts three GET endpoints whose `response_model=` argument
forces FastAPI's OpenAPI generator to register the model — and its
transitively-referenced ring / nested models — in `components.schemas`
with non-empty `properties` maps.

Payload shape:
  * five_rings          -> one canonical NormalizedUnit drawn from the
                          synthetic plumbing fixture (first unit).
  * objective_request   -> a canonical example built in code (no fixture
                          for objective requests at G0).
  * qualification_matrix -> the loaded Qualification Matrix v0 rows.

The data itself isn't the point. The point is the schema reaching the
OpenAPI surface. None of these routes are authenticated — same posture
as `/api/health` and `/api/system/state` (G0 acceptance #6).

Cousin pointer: no direct cousin — this is net-new G0-follow-up surface.
The pattern (`response_model` on a GET to surface a contract) is a
standard FastAPI idiom.
"""
from __future__ import annotations

from fastapi import APIRouter

from contracts.five_rings import NormalizedUnit
from contracts.objective_request import (
    DefensibilityFloor,
    EstateRegionSelector,
    ObjectiveMode,
    ObjectiveRequest,
)
from contracts.qualification_matrix.loader import (
    QualificationMatrix,
    load_qualification_matrix,
)
from contracts.five_rings import DefensibilityClass, ScoreVector
from services.data_source.synthetic import SyntheticPlumbingDataSource

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get(
    "/five_rings",
    response_model=NormalizedUnit,
    summary="Five Rings — canonical NormalizedUnit shape (Spec §5).",
)
async def get_five_rings_contract() -> NormalizedUnit:
    """Returns one canonical NormalizedUnit (from the synthetic fixture).

    Surfaces `NormalizedUnit` and its five nested ring models in
    `components.schemas` so machine consumers can read the contract from
    the live OpenAPI spec.
    """
    return next(iter(SyntheticPlumbingDataSource().iter_units()))


@router.get(
    "/objective_request",
    response_model=ObjectiveRequest,
    summary="Objective Request — canonical envelope shape (Spec §8.1).",
)
async def get_objective_request_contract() -> ObjectiveRequest:
    """Returns a canonical ObjectiveRequest example so the schema is
    registered in `components.schemas`.

    G0 has no service that consumes ObjectiveRequest yet (Service 2 lands
    at G3); this route exists purely to surface the contract.
    """
    return ObjectiveRequest(
        objective_text=(
            "Surface every fact-class utterance from primary-recorded "
            "morning-news segments in the last 24 hours."
        ),
        defensibility_floor=DefensibilityFloor(
            minimum_class=DefensibilityClass.UTTERANCE,
            minimum_scores=ScoreVector(
                genre_ceiling=0.5,
                source_standing=0.5,
                corroboration=0.0,
                recency=0.7,
                contested_status=0.0,
            ),
        ),
        provenance_required=True,
        scope=EstateRegionSelector(filters={
            "modalities": ["audio", "video"],
            "date_range": {"from": "2025-09-01", "to": "2025-09-30"},
        }),
        mode=ObjectiveMode.PER_RUN,
        tags=["g0-contract-example"],
    )


@router.get(
    "/qualification_matrix",
    response_model=QualificationMatrix,
    summary="Qualification Matrix v0 — governed taxonomy (Spec §3.4).",
)
async def get_qualification_matrix_contract() -> QualificationMatrix:
    """Returns the loaded v0 matrix.

    Surfaces `QualificationMatrix` and its nested `QualificationRule` in
    `components.schemas`. MEA edits are file-edit-and-bump-rev at G0; the
    MEA editor UI lands at G5.
    """
    return load_qualification_matrix("v0")
