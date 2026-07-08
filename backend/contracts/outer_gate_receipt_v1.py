"""OuterGateReceipt_v1 — additive frozen contract (Artifact Store, AS-E1 α).

New at Artifact Store (BCR §3.2). Owner ruling AS-E1 α (2026-07-08):

    'α. OuterGateReceipt_v1 lands as a new frozen contract by addition;
     v0 stays byte-identical; parity 29 at close, V1-G7 assertion set
     bumps with it. Promise basis: buyer-independent verification —
     β routes the buyer's proof through our API being up and truthful;
     on-receipt means the receipt alone suffices. Additive-new-version
     is the settled pattern; 29 is the honest count.'

The v1 receipt extends v0 by ADDITION of two Optional[str] fields:
`artifact_sha256` (the SHA-256 hex of the stored object) and
`artifact_key` (the artifact_store key, `artifacts/{trace_id}/{artifact_id}.{ext}`).

v0 remains byte-identical on disk; call sites that emit v0 (service_1
qualified_data path) continue to do so. Only the Artifact Store atomic-
write step 5 emits v1 (populated with the two new fields).
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.northena_ledger import LedgerArtifactRef


class OuterGateReceiptV1(BaseModel):
    """§21.2 + BCR §3.2:134 — irreversibility receipt for a successful outer-gate egress,
    v1 additive extension binding the artifact SHA-256 + key on-receipt.

    ADDITIVE from v0. Fields inherited from v0 shape (byte-identical to
    contracts/outer_gate_receipt.py). The two NEW fields at v1 land as
    Optional[str] so the buyer verification path (BCR §3.2:134
    'buyer must be able to verify independently') is on-receipt.
    """

    model_config = ConfigDict(extra="forbid")

    # --- v0 fields (byte-identical shape; do NOT rearrange) ---
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

    # --- v1 additive fields (Artifact Store binding, per BCR §3.2:134 + Owner AS-E1 α) ---
    artifact_sha256: Optional[str] = Field(
        default=None,
        description="SHA-256 hex of the stored artifact object. Populated by the "
                    "outer-gate emission at Artifact Store atomic-write step 5. "
                    "Enables buyer-independent verification via the receipt alone "
                    "(BCR §3.2:134 'on-receipt over sidecar').",
        min_length=64, max_length=64,
    )
    artifact_key: Optional[str] = Field(
        default=None,
        description="Artifact Store key: `artifacts/{trace_id}/{artifact_id}.{ext}` "
                    "(BCR §3.2:128). Populated by the outer-gate emission at "
                    "atomic-write step 5.",
    )
