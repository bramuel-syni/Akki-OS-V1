"""Async objectives router — Phase 5 Stage B (v3 §7).

Endpoints:
  * POST /api/objectives            — accept (202) OR governed refusal (422)
                                       OR infra 503 (queue saturated) OR
                                       idempotent replay (202 byte-identical).
  * GET  /api/objectives/{id}       — status polling + terminal envelope fetch.
  * POST /api/objectives/{id}/cancel — 5th-state terminal transition (200).

Standing Owner Dispositions applied here:
  * infra-not-refusal → queue saturation raises HTTPException(503), NEVER
    an AdmissionRefusal_v0 envelope.
  * cancellation-is-a-state-not-a-refusal → cancel returns the thin
    cancelled terminal envelope (4 keys), NOT a refusal shape.
  * frozen-field-changes-as-new-versions → cancel ledger row uses v1
    (`NorthenaLedgerRow_v1` with `decision="terminate_cancelled"`).

Auth (Phase 5 Stage B posture):
  * `X-Akki-App-ID` header identifies the caller; used for webhook URL +
    sandbox-mode resolution + secret derivation. Full app registration
    surface lands at Phase 8; Stage B keeps the resolution surface thin.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError

from contracts.async_delivery_accepted import AsyncDeliveryAccepted_v0
from contracts.objective_request_v2 import ObjectiveEntry, ObjectiveRequest_v2
from services.economics import quote_service as _quote_service
from contracts.admission_refusal import AdmissionRefusal_v0
from services.service_1 import (
    admission_refusal as admission_refusal_service,
    async_state,
    async_worker,
    cancellation as cancellation_service,
    idempotency as idempotency_service,
)
from services.synisense import webhook_registration


router = APIRouter(prefix="/objectives", tags=["objectives"])


@router.post("")
async def post_objective(
    request: Request,
    x_akki_app_id: Optional[str] = Header(default=None, alias="X-Akki-App-ID"),
    x_akki_webhook_url: Optional[str] = Header(default=None, alias="X-Akki-Webhook-URL"),
):
    """Async admission endpoint — v3 §7 bullet 1.

    Returns:
      * 202 with AsyncDeliveryAccepted_v0 body on accept (or idempotent replay).
      * 422 with AdmissionRefusal_v0 body on governed admission refusal
        (idempotency_key missing / idempotency_key_reused_with_different_body).
      * 503 (empty body per infra-not-refusal doctrine) on queue saturation.
    """
    body = await request.json()
    obj_req = ObjectiveRequest_v2.model_validate(body)

    # v3 §7 bullet 6 — idempotency_key required on external_request.
    if idempotency_service.requires_idempotency_key(obj_req) and not obj_req.idempotency_key:
        refusal = admission_refusal_service.emit_idempotency_key_missing(
            obj_req, async_state.new_id("disp"),
        )
        return JSONResponse(status_code=422, content=refusal.model_dump(mode="json"))

    # Compute canonical hash (excludes idempotency_key from hash input).
    request_body_hash = idempotency_service.canonical_request_hash(obj_req)

    idem_key = obj_req.idempotency_key or ""
    existing = None
    if idem_key:
        existing = await async_state.find_by_idempotency_key(idem_key)

    if existing is not None:
        # Retry-detection: same key + same body → idempotent replay 202.
        if existing["request_body_hash"] == request_body_hash:
            replay = AsyncDeliveryAccepted_v0(
                objective_id=existing["objective_id"],
                delivery_estimate=existing.get("delivery_estimate", "PT5M"),
                trace_id=existing["trace_id"],
                accepted_at=existing["accepted_at"],
            )
            return JSONResponse(status_code=202, content=replay.model_dump(mode="json"))
        # Same key + different body → governed 422.
        refusal = admission_refusal_service.emit_idempotency_key_reused_with_different_body(
            obj_req, async_state.new_id("disp"),
        )
        return JSONResponse(status_code=422, content=refusal.model_dump(mode="json"))

    # New objective — allocate ids + insert.
    objective_id = async_state.new_id("obj")
    trace_id = async_state.new_id("trc")
    accepted_at = async_state.now_iso()
    delivery_estimate = "PT5M"

    # Phase 6 — mint QuoteEnvelope_v0. Governance refusals returned @422.
    quote_or_refusal = await _quote_service.issue_quote(
        obj_req, trace_id, warm_vs_fresh="fresh",
    )
    if isinstance(quote_or_refusal, AdmissionRefusal_v0):
        return JSONResponse(
            status_code=422,
            content=quote_or_refusal.model_dump(mode="json"),
        )
    quote_dict = quote_or_refusal.model_dump(mode="json")
    delivery_estimate = quote_or_refusal.delivery_estimate

    webhook_url = webhook_registration.resolve_webhook_url(x_akki_app_id, x_akki_webhook_url)
    sandbox_mode = webhook_registration.sandbox_mode_default(x_akki_app_id) if x_akki_app_id else False

    doc = {
        "objective_id": objective_id,
        "status": "accepted",
        "state_transitions": [
            {"state": "accepted", "at": accepted_at, "worker_generation_id": None, "reason": None}
        ],
        "enqueue_time": datetime.now(timezone.utc),
        "last_worker_touch": None,
        "worker_generation_id": None,
        "idempotency_key": idem_key or None,
        "request_body_hash": request_body_hash,
        "request_body": obj_req.model_dump(mode="python"),
        "trace_id": trace_id,
        "webhook_url": webhook_url,
        "webhook_secret_hex": (
            webhook_registration.derive_app_webhook_secret(x_akki_app_id).hex()
            if (x_akki_app_id and webhook_url) else None
        ),
        "sandbox_mode": sandbox_mode,
        "delivery_estimate": delivery_estimate,
        "accepted_at": accepted_at,
        "terminal_envelope": None,
        "webhook_undelivered": False,
        "quote": quote_dict,
    }

    try:
        await async_state.db[async_state.ASYNC_STATE_COLLECTION].insert_one(doc)
    except DuplicateKeyError:
        # Race on unique(idempotency_key) — find and treat as replay.
        existing = await async_state.find_by_idempotency_key(idem_key)
        if existing is not None and existing["request_body_hash"] == request_body_hash:
            replay = AsyncDeliveryAccepted_v0(
                objective_id=existing["objective_id"],
                delivery_estimate=existing.get("delivery_estimate", "PT5M"),
                trace_id=existing["trace_id"],
                accepted_at=existing["accepted_at"],
            )
            return JSONResponse(status_code=202, content=replay.model_dump(mode="json"))
        refusal = admission_refusal_service.emit_idempotency_key_reused_with_different_body(
            obj_req, async_state.new_id("disp"),
        )
        return JSONResponse(status_code=422, content=refusal.model_dump(mode="json"))

    # Enqueue for the worker. Standing Disposition infra-not-refusal:
    # queue saturated → HTTP 503, NEVER a governed refusal.
    try:
        await async_worker.enqueue_objective(objective_id)
    except async_worker.QueueSaturatedError as exc:
        # Rollback the accepted doc — infra failure, no state to keep.
        # Sub-stage 2 (2026-07-07): routed through single-source-of-
        # deletion module per `no_unauthorized_deletion_path` invariant.
        # This is an idempotency rollback, NOT a governance deletion;
        # no ledger row emitted.
        from services.retention.authorized_deletion import (
            rollback_saturated_queue_admit,
        )
        await rollback_saturated_queue_admit(objective_id)
        raise HTTPException(
            status_code=503,
            detail=f"async delivery queue saturated: {exc}",
        )

    accepted = AsyncDeliveryAccepted_v0(
        objective_id=objective_id,
        delivery_estimate=delivery_estimate,
        trace_id=trace_id,
        accepted_at=accepted_at,
        quote=quote_dict,
    )
    return JSONResponse(status_code=202, content=accepted.model_dump(mode="json"))


@router.get("/{objective_id}")
async def get_objective(objective_id: str):
    """v3 §7 bullet 4 — status polling + terminal envelope fetch.

    Response body:
      * `objective_id`, `status`, `trace_id` — always present.
      * `terminal_envelope` — populated once status ∈ {delivered, refused, cancelled}.
      * `state_transitions` — full history for lifecycle rendering (Phase 8).
      * `webhook_undelivered` — surfaced so polling remains authoritative
        even if webhook doorbell dropped.

    NOT a frozen response envelope — governed by wire-shape gate
    `test_get_objective_wire_shape` in Phase 5 Stage B tests.
    """
    doc = await async_state.find_by_objective_id(objective_id)
    if doc is None:
        raise HTTPException(status_code=404, detail=f"objective_id={objective_id!r} not found")
    return {
        "objective_id": doc["objective_id"],
        "status": doc["status"],
        "trace_id": doc["trace_id"],
        "accepted_at": doc["accepted_at"],
        "state_transitions": doc.get("state_transitions", []),
        "terminal_envelope": doc.get("terminal_envelope"),
        "webhook_undelivered": bool(doc.get("webhook_undelivered", False)),
    }


@router.post("/{objective_id}/cancel")
async def cancel_objective(objective_id: str):
    """v3 §7 bullet 5 — caller-cancel endpoint. Idempotent: repeated
    cancels on a terminal state return the existing terminal envelope.

    Standing Disposition cancellation-is-a-state-not-a-refusal:
      * cancelled is a 5th terminal state (accepted/running → cancelled).
      * NorthenaLedgerRow_v1(decision="terminate_cancelled") emitted.
      * NO refusal envelope; NO `caller_cancelled` reason code anywhere.
    """
    result = await cancellation_service.cancel_objective(objective_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"objective_id={objective_id!r} not found")
    return result
