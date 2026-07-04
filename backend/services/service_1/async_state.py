"""Async state machine + Mongo persistence — Phase 5 Stage B.

Five-state ruling (Owner, Phase 5 Stage A close, 2026-07-04):
  `accepted → running → delivered | refused | cancelled`

Standing Owner Dispositions this module implements:
  * frozen-field-changes-as-new-versions — ledger writes select
    NorthenaLedgerRow_v0 for non-cancel terminals, NorthenaLedgerRow_v1
    for terminate_cancelled.
  * cancellation-is-a-state-not-a-refusal — cancel writes distinct
    ledger row + returns thin terminal envelope (no refusal shape).
  * infra-not-refusal — queue saturation raises HTTPException(503),
    NEVER an AdmissionRefusal.

Duplicate-ledger-emission prevention (Stage A Return 3.4 Option B):
  Ledger.record() calls check an idempotency guard on (trace_id, run_id,
  stage) — if a row already exists for this trio, skip the write.
  Combined with the worker_generation_id fence at accepted→running,
  this ensures kill-and-restart recovery emits exactly one converge row.

Collection: `objectives_async_state`.
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from contracts.northena_ledger import (
    LedgerArtifactRef,
    LedgerRow,
    NORTHENA_LEDGER_COLLECTION,
)
from contracts.northena_ledger_v1 import NorthenaLedgerRow_v1
from core import db


ASYNC_STATE_COLLECTION = "objectives_async_state"

# Legal state transitions — enforced by transition helpers.
_LEGAL_TRANSITIONS: Dict[str, set] = {
    "accepted":  {"running", "cancelled"},
    "running":   {"delivered", "refused", "cancelled"},
    "delivered": set(),   # terminal
    "refused":   set(),   # terminal
    "cancelled": set(),   # terminal
}

_TERMINAL_STATES = {"delivered", "refused", "cancelled"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


async def ensure_indexes() -> None:
    """Idempotent index creation. Called on ASGI startup."""
    col = db[ASYNC_STATE_COLLECTION]
    await col.create_index("idempotency_key", unique=True, sparse=True)
    await col.create_index("objective_id", unique=True)
    await col.create_index("trace_id", unique=True)
    await col.create_index([("status", 1), ("enqueue_time", 1)])


async def create_accepted(
    *,
    objective_id: str,
    trace_id: str,
    idempotency_key: str,
    request_body: Dict[str, Any],
    request_body_hash: str,
    webhook_url: Optional[str] = None,
    sandbox_mode: bool = False,
    delivery_estimate: str = "PT5M",
) -> Dict[str, Any]:
    """Insert a new accepted-state document. Raises DuplicateKeyError on
    idempotency_key collision — caller handles retry-detection."""
    doc = {
        "objective_id": objective_id,
        "status": "accepted",
        "state_transitions": [
            {"state": "accepted", "at": now_iso(), "worker_generation_id": None, "reason": None}
        ],
        "enqueue_time": datetime.now(timezone.utc),
        "last_worker_touch": None,
        "worker_generation_id": None,
        "idempotency_key": idempotency_key,
        "request_body_hash": request_body_hash,
        "request_body": request_body,
        "trace_id": trace_id,
        "webhook_url": webhook_url,
        "sandbox_mode": sandbox_mode,
        "delivery_estimate": delivery_estimate,
        "accepted_at": now_iso(),
        "terminal_envelope": None,
        "webhook_undelivered": False,
    }
    await db[ASYNC_STATE_COLLECTION].insert_one(doc)
    return doc


async def find_by_idempotency_key(key: str) -> Optional[Dict[str, Any]]:
    return await db[ASYNC_STATE_COLLECTION].find_one({"idempotency_key": key})


async def find_by_objective_id(oid: str) -> Optional[Dict[str, Any]]:
    return await db[ASYNC_STATE_COLLECTION].find_one({"objective_id": oid})


async def atomic_claim_accepted_to_running(objective_id: str) -> Optional[Dict[str, Any]]:
    """Atomically transition accepted → running; return the updated doc
    or None if the state was not accepted (already claimed / terminal)."""
    worker_gen = f"wg-{uuid.uuid4().hex[:12]}"
    updated = await db[ASYNC_STATE_COLLECTION].find_one_and_update(
        {"objective_id": objective_id, "status": "accepted"},
        {
            "$set": {
                "status": "running",
                "worker_generation_id": worker_gen,
                "last_worker_touch": datetime.now(timezone.utc),
            },
            "$push": {
                "state_transitions": {
                    "state": "running",
                    "at": now_iso(),
                    "worker_generation_id": worker_gen,
                    "reason": None,
                }
            },
        },
        return_document=True,  # returns updated doc
    )
    return updated


async def _atomic_terminal_transition(
    objective_id: str,
    from_state: str,
    to_state: str,
    terminal_envelope: Dict[str, Any],
    reason: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Atomically flip a live state to a terminal state.
    Returns updated doc or None if the source state didn't match."""
    if to_state not in _TERMINAL_STATES:
        raise ValueError(f"to_state={to_state!r} is not a terminal state.")
    if to_state not in _LEGAL_TRANSITIONS.get(from_state, set()):
        raise ValueError(
            f"Illegal transition {from_state!r} → {to_state!r}. "
            f"Legal from {from_state!r}: {sorted(_LEGAL_TRANSITIONS.get(from_state, set()))}"
        )
    updated = await db[ASYNC_STATE_COLLECTION].find_one_and_update(
        {"objective_id": objective_id, "status": from_state},
        {
            "$set": {
                "status": to_state,
                "terminal_envelope": terminal_envelope,
                "last_worker_touch": datetime.now(timezone.utc),
            },
            "$push": {
                "state_transitions": {
                    "state": to_state,
                    "at": now_iso(),
                    "worker_generation_id": None,
                    "reason": reason,
                }
            },
        },
        return_document=True,
    )
    return updated


async def transition_to_delivered(objective_id: str, envelope: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return await _atomic_terminal_transition(objective_id, "running", "delivered", envelope, reason="dispatch_success")


async def transition_to_refused(objective_id: str, envelope: Dict[str, Any], reason: str) -> Optional[Dict[str, Any]]:
    return await _atomic_terminal_transition(objective_id, "running", "refused", envelope, reason=reason)


async def transition_to_cancelled(objective_id: str, cancelled_envelope: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Cancel can arrive from EITHER accepted or running."""
    # Try running first (most common path), then accepted.
    doc = await _atomic_terminal_transition(
        objective_id, "running", "cancelled", cancelled_envelope, reason="caller_cancelled"
    )
    if doc is None:
        doc = await _atomic_terminal_transition(
            objective_id, "accepted", "cancelled", cancelled_envelope, reason="caller_cancelled"
        )
    return doc


def build_cancelled_terminal(objective_id: str, trace_id: str) -> Dict[str, Any]:
    """Thin cancelled terminal envelope — Owner ruling: no claim content,
    4 keys only per Standing Disposition cancellation-is-a-state-not-a-refusal."""
    return {
        "objective_id": objective_id,
        "status": "cancelled",
        "trace_id": trace_id,
        "cancelled_at": now_iso(),
    }


async def _ledger_row_exists(trace_id: str, run_id: str, stage: str = "converge") -> bool:
    """Idempotency guard for ledger emission — Return 3.4 Option B."""
    existing = await db[NORTHENA_LEDGER_COLLECTION].find_one({
        "trace_id": trace_id, "run_id": run_id, "stage": stage,
    })
    return existing is not None


async def emit_ledger_terminate_success(
    *, trace_id: str, objective_ref: str, lawful_basis_ref: str,
    run_id: str, reason: str,
) -> None:
    """v0 ledger row for successful terminal. Idempotent."""
    if await _ledger_row_exists(trace_id, run_id):
        return
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id, stage="converge",
        decision="terminate_success", reason=reason,
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request", artifact_id=objective_ref, version="v2",
        ),
        lawful_basis_ref=lawful_basis_ref, stamp_audit=None,
        at=datetime.now(timezone.utc),
    )
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump())


async def emit_ledger_terminate_refused(
    *, trace_id: str, objective_ref: str, lawful_basis_ref: str,
    run_id: str, reason: str,
) -> None:
    """v0 ledger row for governance-refused terminal at admit stage. Idempotent."""
    if await _ledger_row_exists(trace_id, run_id, stage="admit"):
        return
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id, stage="admit",
        decision="refused", reason=reason,
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request", artifact_id=objective_ref, version="v2",
        ),
        lawful_basis_ref=lawful_basis_ref, stamp_audit=None,
        at=datetime.now(timezone.utc),
    )
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump())


async def emit_ledger_terminate_cancelled(
    *, trace_id: str, objective_ref: str, lawful_basis_ref: str,
    run_id: str, cancelled_at_state: str,
) -> None:
    """v1 ledger row for caller-cancelled terminal — Owner Ruling B.
    Idempotent per (trace_id, run_id, stage='converge')."""
    if await _ledger_row_exists(trace_id, run_id):
        return
    row = NorthenaLedgerRow_v1(
        run_id=run_id, trace_id=trace_id, stage="converge",
        decision="terminate_cancelled",
        reason=f"caller_cancelled:cancelled_at_state={cancelled_at_state}",
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request", artifact_id=objective_ref, version="v2",
        ),
        lawful_basis_ref=lawful_basis_ref, stamp_audit=None,
        at=datetime.now(timezone.utc),
    )
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump(mode="python"))


async def find_recovery_candidates() -> List[Dict[str, Any]]:
    """Fetch all non-terminal objectives — used by recovery sweep."""
    cursor = db[ASYNC_STATE_COLLECTION].find({"status": {"$in": ["accepted", "running"]}}).sort("enqueue_time", 1)
    return [doc async for doc in cursor]


async def reset_running_to_accepted(objective_id: str) -> None:
    await db[ASYNC_STATE_COLLECTION].update_one(
        {"objective_id": objective_id, "status": "running"},
        {
            "$set": {"status": "accepted"},
            "$push": {"state_transitions": {
                "state": "recovery_reset", "at": now_iso(),
                "worker_generation_id": None,
                "reason": "worker_generation_replaced_on_boot",
            }},
        },
    )


async def mark_webhook_undelivered(objective_id: str) -> None:
    await db[ASYNC_STATE_COLLECTION].update_one(
        {"objective_id": objective_id},
        {"$set": {"webhook_undelivered": True}},
    )


def legal_transitions() -> Dict[str, set]:
    return {k: set(v) for k, v in _LEGAL_TRANSITIONS.items()}
