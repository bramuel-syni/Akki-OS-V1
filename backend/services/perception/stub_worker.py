"""Deterministic stub worker (V1-B3). Green BEFORE any GPU code exists.

Consumes claim + posts result deterministically. Used by V1-G* gates to prove
pipeline mechanism without perception model or GPU runtime.
"""
from __future__ import annotations

from typing import Any, Dict

from contracts.perception_job_v0 import PerceptionJob_v0
from contracts.perception_result_v0 import (
    Checkpoint, PerceptionResult_v0, PurgeAttestation, Telemetry,
)


def process_job_deterministically(job: PerceptionJob_v0) -> PerceptionResult_v0:
    """Produce a deterministic PerceptionResult for the given job.

    Never touches DB, Ledger, or LLM. Never emits ledger rows. Never mutates
    control-plane state. Pure function of the input job.
    """
    # Emit zero units + telemetry + attested purge + complete status.
    return PerceptionResult_v0(
        job_id=job.job_id,
        units=[],
        telemetry=Telemetry(
            gpu_hours=0.0,
            broadcast_hours=float(len(job.reextraction_handles)),
            unit_yield=0,
            per_modality={job.modality: 0},
        ),
        checkpoint=Checkpoint(last_completed_offset_s=3600, completed_unit_ids=[]),
        purge_attestation=PurgeAttestation(purged=True, purged_at=job.issued_at),
        status="complete",
    )


def serialize_result_for_worker(result: PerceptionResult_v0) -> Dict[str, Any]:
    """Serialize PerceptionResult_v0 → wire dict for POST /result."""
    return result.model_dump()
