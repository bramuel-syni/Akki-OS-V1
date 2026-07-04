"""Cancellation handler — Phase 5 Stage B (Owner Ruling B).

Standing Disposition: cancellation-is-a-state-not-a-refusal.
  * Cancel writes NorthenaLedgerRow_v1(decision="terminate_cancelled").
  * GET at cancelled returns thin terminal envelope (4 keys, no claim content).
  * Repeated cancel on terminal state = no-op returning existing terminal envelope.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from services.service_1 import async_state
from services.service_1.webhook import fire_webhook


async def cancel_objective(objective_id: str) -> Optional[Dict[str, Any]]:
    """Cancel an in-flight (accepted or running) objective.

    Returns the cancelled terminal envelope, or the existing terminal
    envelope if already terminal (idempotent), or None if unknown.
    """
    doc = await async_state.find_by_objective_id(objective_id)
    if doc is None:
        return None

    if doc["status"] in async_state._TERMINAL_STATES:
        # Idempotent: return the existing terminal envelope.
        return doc.get("terminal_envelope")

    cancelled_at_state = doc["status"]
    trace_id = doc["trace_id"]
    envelope = async_state.build_cancelled_terminal(objective_id, trace_id)

    updated = await async_state.transition_to_cancelled(objective_id, envelope)
    if updated is None:
        # Race: another actor cancelled or terminal'd; refetch and return.
        refetched = await async_state.find_by_objective_id(objective_id)
        return (refetched or {}).get("terminal_envelope")

    # Ledger via v1 with terminate_cancelled decision — Owner Ruling B.
    run_id = async_state.new_id("cancel-run")
    request = doc.get("request_body", {})
    lawful_basis_ref = ((request.get("envelope") or {}).get("lawful_basis") or "unspecified")
    await async_state.emit_ledger_terminate_cancelled(
        trace_id=trace_id,
        objective_ref=f"objreq-{trace_id}",
        lawful_basis_ref=lawful_basis_ref,
        run_id=run_id,
        cancelled_at_state=cancelled_at_state,
    )

    webhook_url = doc.get("webhook_url")
    webhook_secret_hex = doc.get("webhook_secret_hex")
    webhook_secret = bytes.fromhex(webhook_secret_hex) if webhook_secret_hex else None
    await fire_webhook(
        objective_id=objective_id, trace_id=trace_id, status="cancelled",
        webhook_url=webhook_url, webhook_secret=webhook_secret,
    )
    return envelope
