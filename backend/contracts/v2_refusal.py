"""V2RefusalEnvelope@v0 — frozen contract for the V2 gate structured refusal (G6).

New at G6. Addition; no mutation.

Realises Product v2.1 §29.1 (V2 gates the outer-gate file-out — confirms rights
past extract-for-RMS, resolves the substrate/rights contract, verifies a sample
file-out cryptographically, and demonstrates the cumulative-disclosure guard
refusing a reconstruction attempt) and §30 purpose-limitation.

**Refusal is structured. No partial-egress ever.** Any V2 refusal halts the
egress with zero content bytes emitted; the envelope is the record.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.northena_ledger import LedgerArtifactRef


class V2RefusalEnvelope(BaseModel):
    """§29.1 — structured refusal at the outer gate."""

    model_config = ConfigDict(extra="forbid")

    reason_code: Literal[
        "lawful_basis_absent",
        "substrate_rights_expired",
        "sample_file_out_crypto_verify_failed",
        "cumulative_disclosure_risk",
    ] = Field(
        ...,
        description="One of the four V2 refusal grounds (§29.1 + §30). "
                    "'cumulative_disclosure_risk' is emitted by the cumulative arm "
                    "(closed-seam at G6 v0 per §29.1 'Until V2 passes').",
    )
    refused_at: str = Field(
        ...,
        description="ISO-8601 UTC timestamp of refusal decision.",
    )
    run_id: str
    trace_id: str
    artifact_ref: LedgerArtifactRef
    lawful_basis_ref: Optional[str] = Field(
        default=None,
        description="What was checked (§30 purpose limitation). None if the refusal "
                    "reason is 'lawful_basis_absent' (nothing to check).",
    )
    substrate_contract_ref: Optional[str] = Field(
        default=None,
        description="What was resolved against for rights (§29.1). "
                    "None if refusal reason is 'lawful_basis_absent'.",
    )
    detail: str = Field(
        default="",
        description="Deterministic reason string with no PII. Human-readable but "
                    "governance-safe (§30 data-protection posture).",
    )
