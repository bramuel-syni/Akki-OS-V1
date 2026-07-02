"""OuterGateReceipt@v0 — frozen contract for the outer-gate irreversibility receipt (G6).

New at G6. Addition to the 10 pre-G6 frozen contracts; no mutation.

Realises Product v2.1 §21.2 (outer gate applies the irreversibility transform;
pseudonymisation with a purged mint, k-anonymity / l-diversity / generalisation)
and §22.1 (Ledger writes each Gate decision and reason, every refusal, the
convergence decision, and the absorbed defensibility stamp-audit).

The receipt is the "each Gate decision and reason" record for the outer gate.
It never contains plaintext identifier values; it records categories transformed,
the transform version, and a fingerprint (hash-of-hash) of the key material.
The mint key itself is destroyed at end of window ("purged mint"); the fingerprint
survives so audit consumers can verify the transform's key-lineage claim without
recovering the key.
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.northena_ledger import LedgerArtifactRef


class OuterGateReceipt(BaseModel):
    """§21.2 — irreversibility receipt for a successful outer-gate egress."""

    model_config = ConfigDict(extra="forbid")

    transform_version: Literal["hmac-sha256-v1"] = Field(
        ...,
        description="Deterministic label for the transform primitive applied (Product v2.1 §21.2 "
                    "'pseudonymisation with a purged mint').",
    )
    key_fingerprint: str = Field(
        ...,
        description="SHA-256 hex of the mint key material. NEVER the key itself. "
                    "Purged mint means the key is destroyed at end of window; the fingerprint "
                    "survives so audit can verify key-lineage without recovering the key.",
        min_length=64, max_length=64,
    )
    mint_window_id: str = Field(
        ...,
        description="uuid of the mint window; the window's key is purged at end (§21.2).",
    )
    applied_transformations: List[str] = Field(
        default_factory=list,
        description="Ordered list of transformation labels applied "
                    "(e.g. ['pseudonymise:unit_id', 'pseudonymise:source_ref', "
                    "'generalise:feed_id', 'pseudonymise:speaker_or_author']). "
                    "Category labels only; no values.",
    )
    input_identifier_categories: List[str] = Field(
        default_factory=list,
        description="Categories present in the pre-egress artifact "
                    "(e.g. ['unit_id', 'source_ref', 'speaker_or_author', 'run_id', 'trace_id']). "
                    "Category labels only; no values.",
    )
    applied_at: str = Field(
        ...,
        description="ISO-8601 UTC timestamp of transform application.",
    )
    run_id: str
    trace_id: str
    artifact_ref: LedgerArtifactRef
    k_anonymity_bucket_size: Optional[int] = Field(
        default=None,
        description="k parameter of the k-anonymity generalisation applied (§21.2). "
                    "None at G6 v0 — closed-seam until DPO policy config lands.",
    )
    differential_privacy_epsilon: Optional[float] = Field(
        default=None,
        description="Optional differential-privacy noise epsilon on numerics (§21.2). "
                    "None at G6 v0 — closed-seam until DPO config lands.",
    )
