"""Outer-gate receipt builder (§21.2).

Constructs `OuterGateReceipt@v0` from a transform outcome. The receipt is the
"each Gate decision and reason" record (Product v2.1 §22.1) for the outer
gate — it records the transform version, key fingerprint, applied
transformations, and correlation identifiers WITHOUT any plaintext values.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from contracts.outer_gate_receipt import OuterGateReceipt
from contracts.northena_ledger import LedgerArtifactRef


def build_receipt(
    egress_artifact: Dict[str, Any],
    *,
    run_id: str,
    trace_id: str,
    artifact_ref: LedgerArtifactRef,
    k_anonymity_bucket_size: int | None = None,
    differential_privacy_epsilon: float | None = None,
) -> OuterGateReceipt:
    """Extract transform metadata from an egress artifact and build the
    receipt. Assumes `egress_artifact` was produced by
    `services.outer_gate.transform.transform_artifact`.
    """
    meta = egress_artifact.get("_transform_meta")
    if not isinstance(meta, dict):
        raise ValueError(
            "egress artifact missing '_transform_meta'; not produced by "
            "outer_gate.transform.transform_artifact."
        )
    return OuterGateReceipt(
        transform_version=meta["transform_version"],
        key_fingerprint=meta["key_fingerprint"],
        mint_window_id=meta["mint_window_id"],
        applied_transformations=list(meta.get("applied_transformations", [])),
        input_identifier_categories=list(meta.get("input_identifier_categories", [])),
        applied_at=datetime.now(timezone.utc).isoformat(),
        run_id=run_id,
        trace_id=trace_id,
        artifact_ref=artifact_ref,
        k_anonymity_bucket_size=k_anonymity_bucket_size,
        differential_privacy_epsilon=differential_privacy_epsilon,
    )
