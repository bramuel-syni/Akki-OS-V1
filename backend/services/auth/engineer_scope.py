"""Phase 8-EXT — server-side own-scope gate (Owner P8E-E2 α, 2026-07-08).

Owner ruling verbatim:
    "α, one condition. The dedicated helper is not a 'parallel mechanism' —
     EE-R4's prohibition protects B-1's scope-tuple primitive from
     duplication; own-scope is a different check (caller identity vs
     resource owner) and gets its own single source. Condition: the
     helper is provably the single source — grep-negative gate over
     inline owner-comparison patterns in the engineer router."

BCR §3.9 EE-R4 verbatim: *"Every externally reachable endpoint enforces
scope server-side — view-layer filtering alone fails review. Enforcement
rides the existing B-1 scope primitive; no parallel mechanism."*

Own-scope semantics for `external_engineer`: the caller may only interact
with a resource whose owner is themselves. `resource_owner_email` is
compared against `identity.email` (case-insensitive) for the check.

An identity WITHOUT `external_engineer` in `roles` is not subject to
own-scope narrowing here — internal `engineer` / `admin` retain full
scope per BCR §3.9 role-scoping matrix.
"""
from __future__ import annotations

from typing import Optional

from fastapi.responses import JSONResponse

from services.auth import auth_refusal
from services.auth.identity import Identity


def _is_external_engineer(identity: Identity) -> bool:
    """Return True iff the caller is EXCLUSIVELY the external_engineer role.

    An identity that ALSO carries `engineer` / `admin` / `internal-authority`
    roles is not narrowed by own-scope (those roles carry full scope).
    """
    roles = set(identity.roles)
    if "external_engineer" not in roles:
        return False
    # Any internal-authority role short-circuits own-scope narrowing.
    authoritative = {"engineer", "admin", "master_admin", "dpo"}
    return not (roles & authoritative)


def _own_scope_impl(
    identity: Identity,
    resource_owner_email: Optional[str],
) -> Optional[JSONResponse]:
    """Shared own-scope enforcement impl.

    Amortisation base per Amendment I §1.3 (single source for 3+ engineer
    endpoints). Returns None on permit, JSONResponse (403) on deny.

    Denial code is `auth_scope_insufficient` from the closed 4-code
    registry (P9-E3 α condition 1 pre-carried; P8E-E4 α confirmed).
    """
    if not _is_external_engineer(identity):
        return None  # internal authority — full scope
    caller_email = (identity.email or "").lower()
    owner_email = (resource_owner_email or "").lower()
    if owner_email and owner_email == caller_email:
        return None  # own resource
    return auth_refusal.emit(
        "auth_scope_insufficient",
        detail=(
            "External-engineer own-scope: caller may only interact with "
            "resources owned by themselves. Foreign resource-owner "
            "detected — access denied."
        ),
    )


def require_own_scope_or_deny(
    identity: Identity,
    resource_owner_email: Optional[str],
) -> Optional[JSONResponse]:
    """Public API: own-scope gate. Rides B-1 scope primitive; NOT a
    parallel mechanism (per EE-R4 verbatim). Single source across the
    engineer router — the grep-negative gate in the 8-EXT test suite
    attests no inline owner comparison exists in engineer.py.
    """
    return _own_scope_impl(identity, resource_owner_email)
