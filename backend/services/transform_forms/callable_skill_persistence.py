"""Callable Skill persistence — write-once slice-freeze (TF-E4 (b) α).

Owner ruling TF-E4 (b) α (2026-07-08):

    '(b) α is the load-bearing enforcement — write-once at provisioning,
     no update_one on corpus_slice_ref, grep-negative gate over the
     codebase (Condition-2 pattern) — the persisted record is the
     actual attack surface.'

Landing:
  * `provision_skill(...)` — `insert_one` only. Never `update_one` on
    `corpus_slice_ref`.
  * `revoke_skill(...)` — `update_one` on `revoked_at` field ONLY.
    `corpus_slice_ref` untouched (grep-negative gate TF-G9 attests).
  * `load_provisioning(...)` — read-only fetch.

Slice-freeze structural enforcement:
  * (β) `ConfigDict(frozen=True)` on the contract (in-memory).
  * (α) `insert_one` only for the provisioning record; `update_one`
    limited to `revoked_at` (a non-slice field). Enforced by TF-G9.

MongoDB collection: `callable_skills` with unique index on `skill_id`.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from contracts.callable_skill_provisioning_v0 import CallableSkillProvisioningV0
from core import db as _default_db


COLLECTION = "callable_skills"


async def provision_skill(
    db: AsyncIOMotorDatabase = None,
    *,
    skill_id: str,
    corpus_slice_ref: str,
    key_grant_id: str,
    floor: str,
    scope: str,
    endpoint_path: str,
) -> CallableSkillProvisioningV0:
    """Provision a new callable skill. `insert_one` only — write-once.

    TF-E4 (b) α: `corpus_slice_ref` lands via `insert_one` and NEVER
    changes. New corpus = new skill_id (Owner-verbatim invariant).
    """
    if db is None:
        db = _default_db
    record = CallableSkillProvisioningV0(
        skill_id=skill_id,
        corpus_slice_ref=corpus_slice_ref,
        key_grant_id=key_grant_id,
        floor=floor,
        scope=scope,
        endpoint_path=endpoint_path,
        provisioned_at=datetime.now(timezone.utc).isoformat(),
        revoked_at=None,
    )
    # insert_one only. NEVER update_one on corpus_slice_ref.
    await db[COLLECTION].insert_one(record.model_dump())
    return record


async def revoke_skill(
    db: AsyncIOMotorDatabase = None,
    *,
    skill_id: str,
) -> Optional[CallableSkillProvisioningV0]:
    """Revoke a callable skill by setting `revoked_at` (non-slice field ONLY).

    `corpus_slice_ref` is NEVER touched — the write is scoped to
    `revoked_at` alone. TF-G9 grep-negative gate attests structurally
    that no `update_one` call in the codebase touches `corpus_slice_ref`.
    """
    if db is None:
        db = _default_db
    revoked_at = datetime.now(timezone.utc).isoformat()
    # NOTE: update-set is scoped to `revoked_at` ONLY. TF-G9 attests
    # this line-shape by grep-negative on the full codebase.
    result = await db[COLLECTION].update_one(
        {"skill_id": skill_id, "revoked_at": None},
        {"$set": {"revoked_at": revoked_at}},
    )
    if result.matched_count == 0:
        return None
    doc = await db[COLLECTION].find_one({"skill_id": skill_id})
    if doc is None:
        return None
    doc.pop("_id", None)
    return CallableSkillProvisioningV0.model_validate(doc)


async def load_provisioning(
    db: AsyncIOMotorDatabase = None,
    *,
    skill_id: str,
) -> Optional[CallableSkillProvisioningV0]:
    """Read-only fetch. Returns None if skill_id not found."""
    if db is None:
        db = _default_db
    doc = await db[COLLECTION].find_one({"skill_id": skill_id})
    if doc is None:
        return None
    doc.pop("_id", None)
    return CallableSkillProvisioningV0.model_validate(doc)
