"""Async worker loop + recovery sweep — Phase 5 Stage B (Owner Ruling 1).

asyncio in-process substrate. Mongo-persisted state is source of truth.
Restart drops workers, not state. Recovery sweep on ASGI boot re-enqueues
non-terminal objectives.

Duplicate-ledger-emission prevention (Return 3.4): idempotency guard on
(trace_id, run_id, stage) — see async_state.emit_ledger_* functions.
"""
from __future__ import annotations

import asyncio
import logging
import os
from typing import Any, Dict, Optional

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.composed_conclusion import ComposedConclusion_v0
from contracts.objective_request_v2 import ObjectiveRequest_v2, OutputForm
from services.service_1 import async_state
from services.service_1.composed_conclusion import (
    Service1Refusal as ComposedService1Refusal,
    package_composed_conclusion,
)
from services.service_1.qualified_data import package_qualified_data
from services.service_1.webhook import fire_webhook


log = logging.getLogger("service_1.async_worker")

# Bounded queue.
_QUEUE_MAX = int(os.environ.get("RMS_ASYNC_QUEUE_MAX", "1000"))
_WORKER_CONCURRENCY = int(os.environ.get("RMS_ASYNC_WORKER_CONCURRENCY", "4"))

_queue: Optional[asyncio.Queue] = None
_workers: list = []


def get_queue() -> asyncio.Queue:
    global _queue
    if _queue is None:
        _queue = asyncio.Queue(maxsize=_QUEUE_MAX)
    return _queue


def reset_queue_for_test() -> None:
    """Test helper — reset the singleton queue between tests."""
    global _queue
    _queue = None


class QueueSaturatedError(RuntimeError):
    """Standing Disposition infra-not-refusal — router surfaces this as HTTP 503."""


async def enqueue_objective(objective_id: str) -> None:
    """Non-blocking put. Raises QueueSaturatedError on overflow (→ 503)."""
    q = get_queue()
    try:
        q.put_nowait(objective_id)
    except asyncio.QueueFull as exc:
        raise QueueSaturatedError(f"async queue at maxsize={_QUEUE_MAX}") from exc


async def _dispatch_objective(request: ObjectiveRequest_v2, trace_id: str):
    """Route the fresh objective through the §6.1 or §6.2 packaging path."""
    form = request.output.form
    if form == OutputForm.COMPOSED_CONCLUSION:
        return await package_composed_conclusion(request, trace_id)
    if form == OutputForm.QUALIFIED_DATA:
        return await package_qualified_data(request, trace_id)
    # Other forms (KNOWLEDGE_ARTIFACT, CALLABLE_SKILL, MODEL) —
    # MODEL is refused at admission upstream; the other two are Phase-2
    # scaffold placeholders still. For Phase 5 async surface, we only
    # exercise the two live forms.
    raise NotImplementedError(
        f"Async dispatch does not yet handle output.form={form.value!r}."
    )


async def _process_one(objective_id: str) -> None:
    """Worker's per-objective loop: claim → dispatch → terminal-transition + webhook."""
    doc = await async_state.atomic_claim_accepted_to_running(objective_id)
    if doc is None:
        return  # Already claimed by another worker or terminal.

    request = ObjectiveRequest_v2.model_validate(doc["request_body"])
    trace_id = doc["trace_id"]
    webhook_url = doc.get("webhook_url")
    webhook_secret_hex = doc.get("webhook_secret_hex")
    webhook_secret = bytes.fromhex(webhook_secret_hex) if webhook_secret_hex else None

    try:
        result = await _dispatch_objective(request, trace_id)
    except ComposedService1Refusal as e:
        envelope = {
            "outcome": "refused",
            "reason": e.reason,
            "run_id": e.run_id,
            "trace_id": e.trace_id,
            "asked": e.asked,
            "supported_class": (e.supported_class.value
                                if e.supported_class is not None else None),
            "what_would_raise_it": e.what_would_raise_it,
        }
        await async_state.transition_to_refused(objective_id, envelope, reason=e.reason)
        await fire_webhook(
            objective_id=objective_id, trace_id=trace_id, status="refused",
            webhook_url=webhook_url, webhook_secret=webhook_secret,
        )
        return
    except NotImplementedError as e:
        log.warning("Async dispatch not-implemented: %s", e)
        # Leave state as running for recovery sweep to observe; test env only.
        return

    # Envelope routing per Union arm.
    if isinstance(result, ComposedConclusion_v0):
        envelope = result.model_dump()
        await async_state.transition_to_delivered(objective_id, envelope)
        await fire_webhook(
            objective_id=objective_id, trace_id=trace_id, status="delivered",
            webhook_url=webhook_url, webhook_secret=webhook_secret,
        )
        return
    if isinstance(result, AdmissionRefusal_v0):
        envelope = result.model_dump()
        await async_state.transition_to_refused(objective_id, envelope, reason=result.reason)
        await fire_webhook(
            objective_id=objective_id, trace_id=trace_id, status="refused",
            webhook_url=webhook_url, webhook_secret=webhook_secret,
        )
        return
    if isinstance(result, dict):
        # QualifiedDataPayload — dict-shaped (UNFROZEN by wire-shape gate per 4a).
        await async_state.transition_to_delivered(objective_id, result)
        await fire_webhook(
            objective_id=objective_id, trace_id=trace_id, status="delivered",
            webhook_url=webhook_url, webhook_secret=webhook_secret,
        )


async def worker_loop() -> None:
    """Consume the queue forever."""
    q = get_queue()
    while True:
        try:
            objective_id = await q.get()
        except asyncio.CancelledError:
            return
        try:
            await _process_one(objective_id)
        except Exception:  # noqa: BLE001 — worker must not crash on any single objective
            log.exception("worker loop error processing objective_id=%s", objective_id)


async def recovery_sweep() -> None:
    """On ASGI startup: reset running rows to accepted and re-enqueue non-terminal."""
    docs = await async_state.find_recovery_candidates()
    for doc in docs:
        if doc["status"] == "running":
            await async_state.reset_running_to_accepted(doc["objective_id"])
        try:
            await enqueue_objective(doc["objective_id"])
        except QueueSaturatedError:
            log.warning("Recovery-sweep enqueue overflowed; leaving objective_id=%s for next boot", doc["objective_id"])


async def start_workers() -> None:
    """Spawn N workers. Idempotent — safe to call multiple times."""
    global _workers
    if _workers:
        return
    for _ in range(_WORKER_CONCURRENCY):
        task = asyncio.create_task(worker_loop())
        _workers.append(task)


async def stop_workers() -> None:
    """Cancel all worker tasks. Called on ASGI shutdown."""
    global _workers
    for task in _workers:
        task.cancel()
    if _workers:
        await asyncio.gather(*_workers, return_exceptions=True)
    _workers = []


async def process_one_from_queue() -> bool:
    """Test helper — dequeue one and process. Returns True if one was processed."""
    q = get_queue()
    try:
        objective_id = q.get_nowait()
    except asyncio.QueueEmpty:
        return False
    await _process_one(objective_id)
    return True
