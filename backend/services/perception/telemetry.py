"""Telemetry sidecar (V1-B4). Missing telemetry → V1-G6 gate failure."""
from __future__ import annotations

from typing import Dict

from contracts.perception_result_v0 import Telemetry


def build_telemetry(gpu_hours: float, broadcast_hours: float,
                    unit_yield: int, per_modality: Dict[str, int] | None = None) -> Telemetry:
    """Build a Telemetry record. All four fields REQUIRED per V1-G6."""
    return Telemetry(
        gpu_hours=gpu_hours,
        broadcast_hours=broadcast_hours,
        unit_yield=unit_yield,
        per_modality=per_modality or {},
    )
