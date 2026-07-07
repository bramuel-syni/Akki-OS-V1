"""Transient RuleChangeRequest model — NOT frozen; NOT in contracts/.

Sub-stage 3 uses this Pydantic model for in-flight checker requests
(pending_counter_sign / pending_delay / effective / suspended). It is
NOT a frozen contract at v0 per Amendment G scope (parity 26 unchanged).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from services.checker.consequence_classes import validate_consequence_class


# State strings. Kept as module-level constants; not a Literal on the model
# to allow forward-compat extension without breaking test fixtures.
STATE_PENDING_COUNTER_SIGN = "pending_counter_sign"
STATE_PENDING_DELAY = "pending_delay"
STATE_EFFECTIVE = "effective"
STATE_SUSPENDED = "suspended"

ALL_STATES = {
    STATE_PENDING_COUNTER_SIGN,
    STATE_PENDING_DELAY,
    STATE_EFFECTIVE,
    STATE_SUSPENDED,
}


class RuleChangeRequest(BaseModel):
    """In-flight rule-change request — transient, NOT frozen.

    Ruling 3: object() writes to `objections` list without changing `state`.
    suspend() moves state to `suspended`. advance_delay() moves state to
    `effective` at delay expiry unconditionally.
    """

    model_config = ConfigDict(extra="forbid")

    request_id: str
    rule_class: str
    from_value_ref: str
    to_value_ref: str
    consequence_class: str
    state: str
    initiator_id: str
    initiator_role: str  # capacity role per Ruling 2
    initiated_at: str  # ISO-8601 UTC

    # dual-control fields (set on countersign)
    checker_id: Optional[str] = None
    checker_role: Optional[str] = None  # capacity role per Ruling 2
    countersigned_at: Optional[str] = None

    # tightening-effective fields
    effective_at: Optional[str] = None
    effective_delay_seconds: Optional[int] = None

    # objection annotations (Ruling 3: never blocks)
    objections: list = Field(default_factory=list)

    # suspension fields (Ruling 3: only halt action)
    suspended_by_id: Optional[str] = None
    suspended_by_role: Optional[str] = None
    suspended_at: Optional[str] = None
    suspend_reason: Optional[str] = None
    prior_state: Optional[str] = None


def now_iso() -> str:
    """Server-computed ISO-8601 UTC timestamp (E3 precedent)."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
