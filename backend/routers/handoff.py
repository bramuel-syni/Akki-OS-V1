"""Handoff download surface — `GET /api/handoff/backend_contract_surface_v1`
(post-G6 freeze-and-handoff prep).

GET-only. Reads `/app/docs/handoff/backend_contract_surface_v1.md` from disk
on every hit (freshness: no cache; same discipline as
`/api/discipline/lift_manifest`) and returns the raw markdown as an
attachment for browser download.

Zero writes to any persistent store. Read-only route invariant enforced by
`test_handoff_route_readonly.py`.

Interface Spec anchor: §16 governance-legibility (all disciplines
surface-legible). The handoff artifact is a governance record — the
frozen backend contract surface that G5b binds against — and this route
is the download-scope of that same record.
"""
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response


router = APIRouter(prefix="/handoff", tags=["handoff"])


HANDOFF_ARTIFACT_PATH = Path("/app/docs/handoff/backend_contract_surface_v1.md")
HANDOFF_ARTIFACT_FILENAME = "backend_contract_surface_v1.md"


@router.get("/backend_contract_surface_v1")
async def get_backend_contract_surface_v1() -> Response:
    """Serve the Backend Contract Surface v1 handoff artifact as a
    downloadable markdown attachment.

    Freshness: full file-read on every hit.
    Read-only: zero writes to any persistent store.
    """
    if not HANDOFF_ARTIFACT_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail={
                "reason": "handoff_artifact_not_found",
                "path": str(HANDOFF_ARTIFACT_PATH),
            },
        )
    content = HANDOFF_ARTIFACT_PATH.read_text(encoding="utf-8")
    return Response(
        content=content,
        media_type="text/markdown",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{HANDOFF_ARTIFACT_FILENAME}"'
            ),
        },
    )
