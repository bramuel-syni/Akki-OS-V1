"""CallableSkillProvisioningV0 — additive frozen contract (Transform Forms, TF-E2 α).

BCR §3.7 annex verbatim shape:

    { skill_id, corpus_slice_ref: artifact-store key,
      key_grant_id, floor, scope, endpoint_path,
      provisioned_at, revoked_at?: str }
    Governance: per-call inner gate; every response carries class inline;
    slice bound at freeze and immutable thereafter (new slice = new skill).

Owner ruling TF-E2 α (2026-07-08):

    'α. Internal-vs-external is not the test; promise-load-bearing is.
     The provisioning record carries slice-freeze — "the corpus you
     provisioned is the corpus you're querying" is a buyer-facing
     promise, and the record enforcing it gets the same shape-drift
     protection as any external wire. Parity 31 honest. The ~175 LoC
     saving is Tier-2; the promise is Tier-1.'

Owner ruling TF-E4 (b) β (2026-07-08):

    'β rides along: ConfigDict(frozen=True) on the new contract at
     creation — in-memory hardening, one line, part of the initial
     snapshotted shape.'

Landing:
  * `model_config = ConfigDict(extra="forbid", frozen=True)` — extra fields
    rejected; post-hydration mutation raises TypeError. This is (β)
    in-memory hardening; (α) write-once persistence lives at
    `services/transform_forms/callable_skill_persistence.py`.
  * Parity 30 → 31 (assuming TF-E1 α landed KA at parity 30).
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CallableSkillProvisioningV0(BaseModel):
    """BCR §3.7 annex line 228-233 verbatim shape. TF-E2 α frozen contract.

    Slice-freeze mechanism (TF-E4 (b) α + β):
      * (β) `ConfigDict(frozen=True)` — in-memory hardening; post-load
        mutation raises TypeError.
      * (α) write-once persistence enforced structurally at the
        `callable_skill_persistence` service; grep-negative TF-G9 gate
        asserts NO `update_one({..., "corpus_slice_ref": ...})` in the
        codebase.

    Per-call inner gate (TF-E4 (a) α) reads this record and enforces
    scope + floor at every skill query.
    """

    # (β) TF-E4 (b) β + Owner ruling TF-E2 α precondition: extra=forbid + frozen=True.
    model_config = ConfigDict(extra="forbid", frozen=True)

    skill_id: str = Field(..., min_length=1)
    corpus_slice_ref: str = Field(
        ...,
        min_length=1,
        description="Artifact-store key (`artifacts/{trace_id}/{artifact_id}.{ext}`) "
                    "of the corpus slice this skill is bound to. Immutable "
                    "post-provisioning per TF-E4 (b): 'new slice = new skill_id'. "
                    "Enforced by (β) in-memory frozen + (α) persistence write-once.",
    )
    key_grant_id: str = Field(
        ...,
        min_length=1,
        description="Foreign key into the key-grant registry; drives per-call "
                    "scope check via `services.auth.key_grants.check_scope`.",
    )
    floor: str = Field(
        ...,
        min_length=1,
        description="Defensibility floor label; per-call inner gate refuses "
                    "responses below this floor.",
    )
    scope: str = Field(
        ...,
        min_length=1,
        description="Scope identifier (matches the scope tuple's free-form field). "
                    "Reused by per-call scope check.",
    )
    endpoint_path: str = Field(
        ...,
        min_length=1,
        description="Router path where this skill is exposed "
                    "(e.g., `/api/callable_skill/{skill_id}/query`).",
    )
    provisioned_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp of provisioning.",
    )
    revoked_at: Optional[str] = Field(
        default=None,
        description="ISO-8601 UTC timestamp of revocation; None while active. "
                    "Revocation is the ONLY governed lifecycle change on a "
                    "provisioning record — corpus_slice_ref is never mutated.",
    )
