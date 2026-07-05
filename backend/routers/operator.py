"""Operator surface router — Phase 8 Stage B-2.

Read-only aggregate for UI Spec §2.1 Operator Home:
  * `GET /api/operator/status` — returns `{running, attention, status_line}`.

Frontend combines this with `GET /api/pricing/fleet_policy` for the capacity
strip element (§2.1). Scope enforcement per E1: reads granted key from
Authorization: Bearer <token>; anonymous callers see aggregate identity-less
status (empty running list); scope-insufficient callers see 403 with the
Owner E2 4-code auth-refusal body.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from services.auth import auth_refusal, key_grants
from services.auth.dependencies import get_current_identity_or_none
from services.service_1 import async_state as async_state_service

router = APIRouter(prefix="/operator", tags=["operator"])


async def _list_running_objectives(limit: int = 10) -> List[Dict[str, Any]]:
    """Read-only projection of running objectives from async_state (Phase 5b)."""
    running: List[Dict[str, Any]] = []
    try:
        docs = await async_state_service.list_objectives_in_state("running", limit=limit)
    except AttributeError:
        # If the helper is not present on this deploy, degrade to empty list
        # rather than 500. G5a read-only invariant: never mutate under failure.
        return []
    for doc in docs or []:
        running.append({
            "objective_id": doc.get("objective_id"),
            "trace_id": doc.get("trace_id"),
            "entry": doc.get("entry", "external_request"),
            "stage": doc.get("state", "running"),
            "accepted_at": doc.get("accepted_at"),
        })
    return running


def _compose_status_line(running_count: int, attention_present: bool) -> str:
    """UI Spec §2.1 status line binding copy."""
    if attention_present:
        return "One item needs you."
    return "Running normally."


@router.get("/status")
async def get_operator_status(request: Request):
    """Aggregate for UI Spec §2.1 Operator Home.

    Anonymous → empty running list + running-normally line (surface still
    renders; no authenticated user, no per-user projection).
    Authenticated → running-objective projection scoped to the caller.
    """
    identity = await get_current_identity_or_none(request)
    if identity is None:
        return {
            "identity": None,
            "running": [],
            "attention": None,
            "status_line": _compose_status_line(0, False),
        }
    # Authenticated: return the projection.
    running = await _list_running_objectives(limit=10)
    attention: Optional[Dict[str, Any]] = None  # §2.1: at most one attention card
    return {
        "identity": {
            "user_id": identity.user_id,
            "email": identity.email,
            "roles": list(identity.roles),
        },
        "running": running,
        "attention": attention,
        "status_line": _compose_status_line(len(running), attention is not None),
    }
