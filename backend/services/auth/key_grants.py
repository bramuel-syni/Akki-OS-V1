"""Phase 8 Stage B-1 — per-call scope enforcement (Owner E1 scope condition).

Owner condition (verbatim):
    "B-1's auth is not just login — it is the UI Spec §4 key-scope
     enforcement point (class + path + floor + scope, server-side per
     call), and lands as such. The scope check runs inside the router
     handler AND is visible to the response envelope."

`check_scope(identity, required)` returns True iff the identity holds
at least one KeyGrant matching the required tuple exactly. Roles are
NOT scope substitutes — the `admin` role does NOT bypass scope checks;
admin identities carry explicit KeyGrants (see `user_store.seed_admin_if_absent`).

The five-part scope-check tuple is: (key_class, path, floor, scope).
`floor` accepts ordered class comparison via `_floor_meets`.
"""
from __future__ import annotations

from typing import List, Optional

from .identity import Identity, KeyGrant

# Ordered least-restrictive → most-restrictive. A grant with a higher
# floor implicitly satisfies asks with a lower floor (an
# `established_fact` grant satisfies a `recorded_statement` ask).
_FLOOR_ORDER = ["utterance", "recorded_statement", "established_fact"]


def _floor_index(floor: str) -> int:
    try:
        return _FLOOR_ORDER.index(floor)
    except ValueError:
        # Unknown floor → treat as most-restrictive; conservative fail-closed.
        return len(_FLOOR_ORDER)


def _floor_meets(grant_floor: str, required_floor: str) -> bool:
    """Return True iff grant_floor is at least as restrictive as required_floor."""
    return _floor_index(grant_floor) >= _floor_index(required_floor)


class ScopeCheckResult:
    """Envelope-visible scope-check outcome (Owner E1: response envelope visibility)."""

    __slots__ = ("granted", "reason", "matched_grant_id")

    def __init__(
        self,
        granted: bool,
        reason: Optional[str] = None,
        matched_grant_id: Optional[str] = None,
    ):
        self.granted = granted
        self.reason = reason
        self.matched_grant_id = matched_grant_id

    def to_dict(self) -> dict:
        return {
            "granted": self.granted,
            "reason": self.reason,
            "matched_grant_id": self.matched_grant_id,
        }


def check_scope(
    identity: Optional[Identity],
    required_class: str,
    required_path: str,
    required_floor: str,
    required_scope: str,
) -> ScopeCheckResult:
    """Server-side per-call scope enforcement.

    Returns ScopeCheckResult; caller decides whether to short-circuit
    with `auth_refusal.emit("auth_scope_insufficient", ...)` OR to
    include the scope-check outcome in the response envelope
    (envelope-visible per Owner E1 condition).
    """
    if identity is None:
        return ScopeCheckResult(granted=False, reason="auth_missing")
    for grant in identity.key_grants:
        if (
            grant.key_class == required_class
            and grant.path == required_path
            and _floor_meets(grant.floor, required_floor)
            and grant.scope == required_scope
        ):
            return ScopeCheckResult(granted=True, matched_grant_id=grant.grant_id)
    return ScopeCheckResult(granted=False, reason="auth_scope_insufficient")


def list_grants(identity: Identity) -> List[dict]:
    """Serialise identity's grants for envelope surfacing (UI Spec §4.1)."""
    return [g.model_dump() for g in identity.key_grants]
