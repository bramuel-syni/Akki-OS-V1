"""PerceptionResult_v0 — Phase 9 Sub-stage 9.1 (BCR §3.1 technical annex).

FROZEN CONTRACT (28th). Owner P9-E1 α (2026-07-08).

Wire shape per BCR §3.1 technical annex lines 89-97 verbatim:
    job_id: str                              required
    units: List[NormalizedUnit]              required · may be empty on failure · intake-validated
    telemetry: {gpu_hours: float, broadcast_hours: float,
                unit_yield: int, per_modality: {…}}     required
    checkpoint: {last_completed_offset_s: int,
                 completed_unit_ids: List[str]}          required
    purge_attestation: {purged: bool, purged_at: str}    required
    status: Literal[complete, partial_failed]            required

D4b freeze prior applies identically. V1-G7 grows to 28 at 9.1 landing.
"""
from __future__ import annotations

from typing import Dict, List, Literal

from pydantic import BaseModel, ConfigDict, Field

from contracts.five_rings import NormalizedUnit


class Telemetry(BaseModel):
    """Per-job telemetry (V1-B4). Missing → gate failure (V1-G6)."""

    model_config = ConfigDict(extra="forbid")

    gpu_hours: float = Field(..., ge=0.0)
    broadcast_hours: float = Field(..., ge=0.0)
    unit_yield: int = Field(..., ge=0)
    per_modality: Dict[str, int] = Field(
        default_factory=dict,
        description="Modality-keyed unit counts (e.g. {AUDIO: 12, VIDEO: 8}).",
    )


class Checkpoint(BaseModel):
    """Unit-level checkpoint (V1-B2). Enables kill-and-restart without duplication."""

    model_config = ConfigDict(extra="forbid")

    last_completed_offset_s: int = Field(..., ge=0)
    completed_unit_ids: List[str] = Field(default_factory=list)


class PurgeAttestation(BaseModel):
    """Purge attestation (V1-D1). REQUIRED field, not optional. Missing → refused."""

    model_config = ConfigDict(extra="forbid")

    purged: bool = Field(..., description="True iff worker-side raw AV was purged.")
    purged_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp of the purge attestation.",
    )


class PerceptionResult_v0(BaseModel):
    """Perception result envelope — worker plane → control plane."""

    model_config = ConfigDict(extra="forbid")

    job_id: str = Field(..., min_length=1)
    units: List[NormalizedUnit] = Field(
        default_factory=list,
        description="May be empty on partial_failed. Intake-validated per unit.",
    )
    telemetry: Telemetry
    checkpoint: Checkpoint
    purge_attestation: PurgeAttestation
    status: Literal["complete", "partial_failed"] = Field(
        ...,
        description="Two-state honest verdict; partial_failed carries whatever units + telemetry landed.",
    )
