"""Phase 8 Stage B-3 Block 3 — Engineer key-grant service layer.

Mint grant_id deterministically (SHA-256 short of the scope tuple +
grantor + issued-at); persist to Mongo (`engineer_key_grants`
collection); emit ledger row via
`engineer_key_grant_ledger.record_engineer_key_grant_event`.

Governance-load-bearing under D4b unfrozen ruling: the wire-shape gate
(`tests/invariants/test_engineer_key_grant_load_bearing_wire_shape.py`)
pins the 7 governance-key fields at runtime. This service enforces
that gate at persist time — anything violating the gate FAILS the
mint call before a row is written.
"""
from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from core import db

from .engineer_key_grant import (
    EngineerKeyGrantRegistration,
    EngineerKeyGrantRegistrationRequest,
    EngineerKeyGrantRevocationRequest,
)
from .engineer_key_grant_ledger import record_engineer_key_grant_event


COLLECTION = "engineer_key_grants"


def _mint_grant_id(
    req: EngineerKeyGrantRegistrationRequest,
    grantor_id: str,
    issued_at: datetime,
) -> str:
    """Deterministic 24-char SHA-256 short over the scope tuple + issuer + timestamp."""
    material = "|".join([
        str(req.grantee_email),
        req.key_class,
        req.path,
        req.floor,
        req.scope,
        req.lawful_basis_ref,
        grantor_id,
        issued_at.isoformat(),
    ])
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def _mint_trace_id() -> str:
    """Fresh trace_id per grant lifecycle event — one grant → one audit thread."""
    return f"engineer-key-grant-{uuid.uuid4().hex[:16]}"


async def ensure_indexes() -> None:
    """Compound unique index on grant_id (mints are deterministic + unique)."""
    await db[COLLECTION].create_index("grant_id", unique=True)


async def register_grant(
    req: EngineerKeyGrantRegistrationRequest,
    grantor_id: str,
) -> EngineerKeyGrantRegistration:
    """Mint, persist, and emit-ledger for a new grant.

    Idempotent by grant_id (deterministic mint over the tuple +
    grantor + issued-at). If an identical mint already exists,
    returns the existing row (upsert semantics).
    """
    issued_at = datetime.now(timezone.utc)
    grant_id = _mint_grant_id(req, grantor_id, issued_at)
    existing = await db[COLLECTION].find_one({"grant_id": grant_id})
    if existing is not None:
        existing.pop("_id", None)
        return EngineerKeyGrantRegistration.model_validate(existing)
    grant = EngineerKeyGrantRegistration(
        grant_id=grant_id,
        grantee_email=req.grantee_email,
        grantor_id=grantor_id,
        key_class=req.key_class,
        path=req.path,
        floor=req.floor,
        scope=req.scope,
        justification=req.justification,
        lawful_basis_ref=req.lawful_basis_ref,
        issued_at=issued_at,
        revoked_at=None,
        revocation_reason=None,
    )
    await db[COLLECTION].insert_one(grant.model_dump(mode="python"))
    # Emit ledger row — idempotent by (trace_id, run_id).
    trace_id = _mint_trace_id()
    await record_engineer_key_grant_event(
        event_type="issued", grant=grant, trace_id=trace_id,
    )
    return grant


async def list_grants_for_grantee(grantee_email: str) -> List[EngineerKeyGrantRegistration]:
    """Read all grants for a grantee — Engineer §4.1 grants panel data source."""
    cursor = db[COLLECTION].find({"grantee_email": grantee_email.lower()})
    out: List[EngineerKeyGrantRegistration] = []
    async for doc in cursor:
        doc.pop("_id", None)
        out.append(EngineerKeyGrantRegistration.model_validate(doc))
    return out


async def get_grant(grant_id: str) -> Optional[EngineerKeyGrantRegistration]:
    doc = await db[COLLECTION].find_one({"grant_id": grant_id})
    if doc is None:
        return None
    doc.pop("_id", None)
    return EngineerKeyGrantRegistration.model_validate(doc)


class GrantAlreadyRevoked(Exception):
    """Raised when revoke fires on an already-revoked grant."""


class GrantNotFound(Exception):
    """Raised when revoke fires on a non-existent grant."""


async def revoke_grant(
    grant_id: str,
    req: EngineerKeyGrantRevocationRequest,
    grantor_id: str,
) -> EngineerKeyGrantRegistration:
    """Revoke an active grant.

    Semantics:
      * grant_id not found → GrantNotFound (router surfaces 404).
      * grant already revoked → GrantAlreadyRevoked (router surfaces 409).
      * else → set revoked_at + revocation_reason; emit ledger row
        (event_type='revoked'); return updated Registration.
    """
    grant = await get_grant(grant_id)
    if grant is None:
        raise GrantNotFound(grant_id)
    if grant.revoked_at is not None:
        raise GrantAlreadyRevoked(grant_id)
    revoked_at = datetime.now(timezone.utc)
    updated = grant.model_copy(update={
        "revoked_at": revoked_at,
        "revocation_reason": req.reason,
    })
    await db[COLLECTION].update_one(
        {"grant_id": grant_id},
        {"$set": {
            "revoked_at": revoked_at,
            "revocation_reason": req.reason,
        }},
    )
    # Fresh trace_id for the revocation lifecycle event — a revocation
    # is a distinct audit thread from issuance per Owner D4b posture.
    trace_id = _mint_trace_id()
    await record_engineer_key_grant_event(
        event_type="revoked", grant=updated, trace_id=trace_id,
    )
    return updated
