"""§8 consequence-class checker state machine.

Per Owner Ruling 3 (Amendment G, 2026-07-07): objection annotates but
NEVER halts a tightening. Only owner-suspend halts. This module implements
the corrected state machine.

Storage: MongoDB collection `checker_requests` — one document per request.
Idempotent `initiate()` uses deterministic request_id derived from
(rule_class, from_value_ref, to_value_ref) if a pending request exists.

Standing state-conflict anti-rule (rulings §8.2 elevated): state
conflicts use 403 access-control class body only.
"""
from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from core import db
from services.checker.consequence_classes import (
    CONSEQUENCE_CLASS_DUAL_CONTROL,
    CONSEQUENCE_CLASS_TIGHTENING_UNILATERAL,
    validate_consequence_class,
)
from services.checker.effective_delay import (
    consequence_class_for,
    effective_delay_seconds,
)
from services.checker.rule_change_request import (
    ALL_STATES,
    RuleChangeRequest,
    STATE_EFFECTIVE,
    STATE_PENDING_COUNTER_SIGN,
    STATE_PENDING_DELAY,
    STATE_SUSPENDED,
    now_iso,
)

log = logging.getLogger(__name__)

CHECKER_COLLECTION = "checker_requests"


class StateMachineError(Exception):
    """Base class for state-machine transition errors."""


class InvalidTransitionError(StateMachineError):
    """Raised when the requested transition is not valid from the
    current state. Router maps to 403 access-control (Standing state-
    conflict anti-rule)."""


class UnknownRequestError(StateMachineError):
    """Raised when a request_id does not exist. Router maps to 404."""


@dataclass
class InitiateResult:
    request_id: str
    state: str
    consequence_class: str
    idempotent_hit: bool  # True if returned existing pending request


def _deterministic_request_id(
    rule_class: str, from_ref: str, to_ref: str
) -> str:
    """Deterministic ID for idempotent initiate() when a matching pending
    request exists. Format: `rc-{first-12-of-sha256}`."""
    h = hashlib.sha256(
        f"{rule_class}|{from_ref}|{to_ref}".encode("utf-8")
    ).hexdigest()
    return f"rc-{h[:12]}"


async def initiate(
    *,
    rule_class: str,
    from_value_ref: str,
    to_value_ref: str,
    initiator_id: str,
    initiator_role: str,  # capacity role per Ruling 2
) -> InitiateResult:
    """Kick off a new rule-change request.

    Ruling 3 semantics:
      - Identical `(rule_class, from_value_ref, to_value_ref)` while a
        matching request is `pending_counter_sign` or `pending_delay`:
        idempotent — returns the existing request_id.
      - Post-`effective` re-initiate on same tuple: new change with own
        window (no memory).
    """
    consequence_class = consequence_class_for(rule_class)
    validate_consequence_class(consequence_class)

    request_id = _deterministic_request_id(
        rule_class, from_value_ref, to_value_ref
    )

    # Idempotency check — any pending (non-terminal) matching request?
    existing = await db[CHECKER_COLLECTION].find_one({
        "request_id": request_id,
        "state": {"$in": [STATE_PENDING_COUNTER_SIGN, STATE_PENDING_DELAY]},
    })
    if existing is not None:
        return InitiateResult(
            request_id=existing["request_id"],
            state=existing["state"],
            consequence_class=existing["consequence_class"],
            idempotent_hit=True,
        )

    # Fresh initiate. If a prior terminal (effective/suspended) row exists
    # with the SAME request_id (from a previous run on the same tuple), we
    # allow a new document with a fresh suffix to distinguish generations.
    prior_terminal = await db[CHECKER_COLLECTION].find_one({
        "request_id": request_id
    })
    if prior_terminal is not None:
        # Append generation suffix (post-effect re-initiate = new change).
        gen = int(datetime.now(timezone.utc).timestamp())
        request_id = f"{request_id}-g{gen}"

    initial_state = (
        STATE_PENDING_COUNTER_SIGN
        if consequence_class == CONSEQUENCE_CLASS_DUAL_CONTROL
        else STATE_PENDING_DELAY
    )
    delay = (
        effective_delay_seconds()
        if consequence_class == CONSEQUENCE_CLASS_TIGHTENING_UNILATERAL
        else None
    )
    initiated_at = now_iso()
    req = RuleChangeRequest(
        request_id=request_id,
        rule_class=rule_class,
        from_value_ref=from_value_ref,
        to_value_ref=to_value_ref,
        consequence_class=consequence_class,
        state=initial_state,
        initiator_id=initiator_id,
        initiator_role=initiator_role,
        initiated_at=initiated_at,
        effective_delay_seconds=delay,
    )
    await db[CHECKER_COLLECTION].insert_one(req.model_dump(mode="python"))
    return InitiateResult(
        request_id=request_id,
        state=initial_state,
        consequence_class=consequence_class,
        idempotent_hit=False,
    )


async def _load(request_id: str) -> RuleChangeRequest:
    doc = await db[CHECKER_COLLECTION].find_one({"request_id": request_id})
    if doc is None:
        raise UnknownRequestError(f"request_id={request_id!r} not found")
    # Drop mongo _id before parsing.
    doc.pop("_id", None)
    return RuleChangeRequest.model_validate(doc)


async def _persist(req: RuleChangeRequest) -> None:
    await db[CHECKER_COLLECTION].update_one(
        {"request_id": req.request_id},
        {"$set": req.model_dump(mode="python")},
        upsert=False,
    )


async def get_request(request_id: str) -> RuleChangeRequest:
    return await _load(request_id)


async def countersign(
    *,
    request_id: str,
    checker_id: str,
    checker_role: str,  # capacity role per Ruling 2
) -> RuleChangeRequest:
    """Dual-control countersign transition. LB gate CK-G1."""
    req = await _load(request_id)
    if req.consequence_class != CONSEQUENCE_CLASS_DUAL_CONTROL:
        raise InvalidTransitionError(
            f"countersign only applies to dual_control; request "
            f"consequence_class={req.consequence_class!r}"
        )
    if req.state != STATE_PENDING_COUNTER_SIGN:
        raise InvalidTransitionError(
            f"cannot countersign a request in state={req.state!r}"
        )
    if checker_id == req.initiator_id:
        raise InvalidTransitionError(
            "same-identity countersign refused (CK-G4 symmetry)"
        )
    req.state = STATE_EFFECTIVE
    req.checker_id = checker_id
    req.checker_role = checker_role
    req.countersigned_at = now_iso()
    req.effective_at = req.countersigned_at
    await _persist(req)
    return req


async def advance_delay(*, request_id: str, now: Optional[datetime] = None) -> RuleChangeRequest:
    """Advance a tightening_unilateral request per delay elapsed.

    Ruling 3: transitions to `effective` at delay expiry UNCONDITIONALLY —
    active objections DO NOT halt. Only `suspend()` halts.
    """
    req = await _load(request_id)
    if req.consequence_class != CONSEQUENCE_CLASS_TIGHTENING_UNILATERAL:
        raise InvalidTransitionError(
            f"advance_delay only applies to tightening_unilateral; got "
            f"consequence_class={req.consequence_class!r}"
        )
    if req.state != STATE_PENDING_DELAY:
        # Terminal states (effective/suspended) don't advance.
        return req
    initiated_at = datetime.fromisoformat(req.initiated_at.replace("Z", "+00:00"))
    reference_now = now if now is not None else datetime.now(timezone.utc)
    if reference_now.tzinfo is None:
        reference_now = reference_now.replace(tzinfo=timezone.utc)
    elapsed = (reference_now - initiated_at).total_seconds()
    if elapsed < (req.effective_delay_seconds or effective_delay_seconds()):
        return req  # still pending
    req.state = STATE_EFFECTIVE
    req.effective_at = reference_now.isoformat().replace("+00:00", "Z")
    await _persist(req)
    return req


async def object_to_tightening(
    *,
    request_id: str,
    objector_id: str,
    objector_role: str,
    reason: str,
) -> RuleChangeRequest:
    """Ruling 3: annotates + escalates. NEVER halts.

    - Only valid on `tightening_unilateral` requests.
    - Only valid while state is `pending_delay` (post-effective is void).
    - Adds objection annotation; does NOT change `state`.
    - Router-layer emits a `tightening_objected` ledger row with
      owner-escalation marker.
    """
    req = await _load(request_id)
    if req.consequence_class != CONSEQUENCE_CLASS_TIGHTENING_UNILATERAL:
        raise InvalidTransitionError(
            "object() only applies to tightening_unilateral requests"
        )
    if req.state != STATE_PENDING_DELAY:
        raise InvalidTransitionError(
            f"cannot object to a request in state={req.state!r}; "
            f"objections are valid only during pending_delay"
        )
    annotation = {
        "objector_id": objector_id,
        "objector_role": objector_role,
        "reason": reason,
        "objected_at": now_iso(),
    }
    req.objections = list(req.objections) + [annotation]
    await _persist(req)
    return req


async def suspend(
    *,
    request_id: str,
    suspended_by_id: str,
    suspended_by_role: str,
    reason: str,
) -> RuleChangeRequest:
    """Ruling 3: the ONLY halt action. Owner-only capability enforced at
    the router layer (master_admin role via E2 4-code registry).

    - Valid on `pending_counter_sign` OR `pending_delay`.
    - Invalid on `effective` (already applied) or `suspended` (idempotent
      no-op is a distinct call at the router; state-machine raises here).
    """
    req = await _load(request_id)
    if req.state == STATE_SUSPENDED:
        # Idempotent no-op: return existing row unchanged. Router encodes
        # this as HTTP 200-with-existing-state (no state-conflict class).
        return req
    if req.state == STATE_EFFECTIVE:
        raise InvalidTransitionError(
            "cannot suspend an already-effective tightening"
        )
    if req.state not in {STATE_PENDING_COUNTER_SIGN, STATE_PENDING_DELAY}:
        raise InvalidTransitionError(
            f"cannot suspend a request in state={req.state!r}"
        )
    req.prior_state = req.state
    req.state = STATE_SUSPENDED
    req.suspended_by_id = suspended_by_id
    req.suspended_by_role = suspended_by_role
    req.suspend_reason = reason
    req.suspended_at = now_iso()
    await _persist(req)
    return req


async def list_pending(role: Optional[str] = None) -> list:
    """Banner-feed. Returns pending (non-terminal) requests, optionally
    filtered by role — but per Ruling 2 the banner renders the CAPACITY
    role, not identity role: the router filters by consequence-class role
    (dpo initiates → admin countersigns and vice versa)."""
    cursor = db[CHECKER_COLLECTION].find({
        "state": {"$in": [STATE_PENDING_COUNTER_SIGN, STATE_PENDING_DELAY]},
    }).sort("initiated_at", 1)
    items = []
    async for doc in cursor:
        doc.pop("_id", None)
        items.append(doc)
    if role is None:
        return items
    # Capacity-role filter: for dual_control the countersigner is the
    # opposite of the initiator; for tightening_unilateral it's
    # observation-only (both consoles see it).
    filtered = []
    for it in items:
        if it["consequence_class"] == CONSEQUENCE_CLASS_DUAL_CONTROL:
            # Countersign capacity role is the opposite of initiator's.
            initiator_capacity = it.get("initiator_role")
            required_countersigner = _opposite_role(initiator_capacity)
            if required_countersigner == role:
                filtered.append(it)
        else:
            # tightening_unilateral: both consoles see the item.
            filtered.append(it)
    return filtered


def _opposite_role(capacity_role: Optional[str]) -> Optional[str]:
    if capacity_role == "compliance":
        return "admin"
    if capacity_role == "admin":
        return "compliance"
    return None
