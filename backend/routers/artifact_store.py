"""Artifact Store router — GET + HEAD download endpoints (AS-U1, AS-B3).

BCR §3.2 AS-B3 (verbatim):
    'Download is authenticated by the buyer's key scope; a wrong-key
     request returns 403 access-control class ({reason, detail}, never
     outcome=refused).'

Landing:
  * `GET /api/artifacts/{trace_id}/{artifact_id_dot_ext}` — authz + bytes.
  * `HEAD /api/artifacts/{trace_id}/{artifact_id_dot_ext}` — authz + metadata.

Authz via `adapter.get(key, caller_scope)` per AS-E4 γ + Condition-2.
Domain exception `ScopeInsufficientError` → 403 via `auth_refusal.emit`.
4-code registry closed (P9-E3 / P8E-E4 α pre-carry).

AS-H1 verbatim: NO DELETE handler. Deletion via Seam 3 authorized-
deletion path only.
"""
from __future__ import annotations

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from services.artifact_store.adapter import (
    ArtifactStoreAdapter,
    ArtifactNotFoundError,
    ScopeInsufficientError,
)
from services.auth import auth_refusal
from services.auth.dependencies import require_identity_or_deny
from services.auth.identity import Identity


router = APIRouter(prefix="/artifacts", tags=["artifact_store"])


def _validate_path(trace_id: str, artifact_id_dot_ext: str):
    if "/" in trace_id or "/" in artifact_id_dot_ext:
        return None, JSONResponse(status_code=400, content={"detail": "malformed path"})
    if "." not in artifact_id_dot_ext:
        return None, JSONResponse(
            status_code=400,
            content={"detail": "artifact segment must be `{artifact_id}.{ext}`"},
        )
    return f"artifacts/{trace_id}/{artifact_id_dot_ext}", None


@router.get("/{trace_id}/{artifact_id_dot_ext}")
async def get_artifact(
    trace_id: str,
    artifact_id_dot_ext: str,
    request: Request,
):
    """AS-U1 durable download.

    AS-B3 authz posture: wrong-key request → 403
    `{"reason": "auth_scope_insufficient", "detail": ...}`.
    NEVER `outcome=refused` (auth is a 4th class per B-1 E2 ratification).
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result

    key, err = _validate_path(trace_id, artifact_id_dot_ext)
    if err is not None:
        return err

    adapter = ArtifactStoreAdapter()
    try:
        data = adapter.get(key, caller_scope=identity)
    except ScopeInsufficientError as exc:
        return auth_refusal.emit("auth_scope_insufficient", detail=str(exc))
    except ArtifactNotFoundError:
        return JSONResponse(
            status_code=404,
            content={"reason": "artifact_not_found", "detail": key},
        )

    return Response(content=data, media_type="application/octet-stream")


@router.head("/{trace_id}/{artifact_id_dot_ext}")
async def head_artifact(
    trace_id: str,
    artifact_id_dot_ext: str,
    request: Request,
):
    """AS-I1 head — {exists, sha256, size} via response headers.

    Authz posture mirrors GET (mechanism-preserved at the wire boundary):
    wrong-key → 403 with `auth_scope_insufficient`. HEAD existence itself
    is material information; wrong-scope is denied before metadata leaks.
    """
    result = await require_identity_or_deny(request)
    if isinstance(result, JSONResponse):
        return result
    identity: Identity = result

    key, err = _validate_path(trace_id, artifact_id_dot_ext)
    if err is not None:
        return err

    adapter = ArtifactStoreAdapter()
    # Enforce authz via the same path as GET: adapter.get raises
    # ScopeInsufficientError before reading bytes; we discard the bytes
    # after the check because HEAD is metadata-only.
    try:
        _ = adapter.get(key, caller_scope=identity)
    except ScopeInsufficientError as exc:
        return auth_refusal.emit("auth_scope_insufficient", detail=str(exc))
    except ArtifactNotFoundError:
        return Response(status_code=404)

    head = adapter.head(key)
    if not head.exists:
        return Response(status_code=404)

    return Response(
        status_code=200,
        headers={
            "X-Artifact-Sha256": head.sha256 or "",
            "X-Artifact-Size": str(head.size or 0),
        },
    )
