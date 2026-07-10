"""Census-dimensions router — read-only endpoints (Owner Message 565 · 2026-07-10).

Endpoints:
  * GET /api/census/dimensions/{feed_id} — read one sidecar record.
  * GET /api/census/dimensions/registry/{kind} — read current registry
    vocabulary for `content_surfaces` or `genres`.

No POST/PUT/DELETE endpoints — writes are census-run-only via
`services.census_dimensions.dimensions_service.record_census_dimension(...)`
called in-process at Phase 9 census. This preserves the invariant that
'the census discovers the estate; nothing pre-describes it' (governance §8).
"""
from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from core import db
from services.census_dimensions.dimensions_loader import RegistryKind
from services.census_dimensions.dimensions_service import (
    list_registry,
    read_census_dimensions_for_feed,
)

router = APIRouter(tags=["census_dimensions"])


@router.get("/census/dimensions/{feed_id}")
async def read_feed_dimensions(feed_id: str):
    record = await read_census_dimensions_for_feed(db, feed_id=feed_id)
    if record is None:
        return JSONResponse(
            status_code=404,
            content={
                "outcome": "not_found",
                "detail": f"no census dimensions recorded for feed_id={feed_id!r}",
            },
        )
    return record.model_dump()


@router.get("/census/dimensions/registry/{kind}")
async def read_registry(kind: str):
    if kind not in ("content_surfaces", "genres"):
        return JSONResponse(
            status_code=404,
            content={
                "outcome": "not_found",
                "detail": (
                    f"unknown registry kind={kind!r}; "
                    f"expected 'content_surfaces' or 'genres'."
                ),
            },
        )
    return list_registry(kind)  # type: ignore[arg-type]
