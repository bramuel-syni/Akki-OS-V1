"""V2 gate — structured refusal (§29.1 + §30).

Constructs `V2RefusalEnvelope@v0` for the four V2 refusal grounds.
Refusal is total: no partial-egress ever (§29.1 "delivery is inner-gate-only"
until V2 passes; §30 purpose limitation).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from contracts.northena_ledger import LedgerArtifactRef
from contracts.v2_refusal import V2RefusalEnvelope


def build_refusal(
    *,
    reason_code: str,
    run_id: str,
    trace_id: str,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: Optional[str] = None,
    substrate_contract_ref: Optional[str] = None,
    detail: str = "",
) -> V2RefusalEnvelope:
    """Emit a structured V2 refusal envelope.

    Callers MUST NOT emit content bytes after invoking this. The refusal
    envelope IS the egress record; nothing else crosses.
    """
    return V2RefusalEnvelope(
        reason_code=reason_code,
        refused_at=datetime.now(timezone.utc).isoformat(),
        run_id=run_id,
        trace_id=trace_id,
        artifact_ref=artifact_ref,
        lawful_basis_ref=lawful_basis_ref,
        substrate_contract_ref=substrate_contract_ref,
        detail=detail,
    )
