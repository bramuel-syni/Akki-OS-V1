"""Execution mode telemetry sidecar (Owner 9.2a-E2 α condition 2 · 2026-07-10).

Owner verbatim carrier (condition 2):

    'execution_mode lands in result telemetry — attribution of GPU-hours
     and yield to a mode the record doesn't carry is the same fabricated-
     attribution gap E1 closes for models. One field, honest attribution.'

Landing: sidecar helper — the frozen `PerceptionResult_v0` contract is NOT
mutated (parity 31 stands). `execution_mode` is attached as an out-of-band
telemetry payload that ships alongside the PerceptionResult via
`services.perception.telemetry` (V1-B4 stamp_audit pattern). Every job
result carries the mode used to produce it.
"""
from __future__ import annotations

from typing import Any, Dict

from services.perception.gpu_execution.cuda_runtime import SELECTED_BACKEND


def execution_mode_payload(job_id: str) -> Dict[str, Any]:
    """Return the telemetry payload attesting the mode used to produce a job."""
    return {
        "job_id": job_id,
        "execution_mode": SELECTED_BACKEND,
        "attribution": (
            "9.2a-E2 α condition 2: execution_mode attribution — GPU-hours "
            "and yield attributed to the mode the record carries."
        ),
    }


def annotate_result(job_id: str, telemetry: Dict[str, Any]) -> Dict[str, Any]:
    """Attach execution_mode + attribution to a telemetry dict in-place-safe.

    Returns a NEW dict (does not mutate the input). Used by workers when
    emitting telemetry to the V1-B4 sidecar.
    """
    out = dict(telemetry)
    out["execution_mode"] = SELECTED_BACKEND
    out["_execution_mode_attribution_job_id"] = job_id
    return out
