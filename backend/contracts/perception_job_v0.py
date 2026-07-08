"""PerceptionJob_v0 — Phase 9 Sub-stage 9.1 (BCR §3.1 technical annex).

FROZEN CONTRACT (27th). Owner P9-E1 α (2026-07-08) verbatim:

    "Parity 26→28 additive at 9.1 landing. The environment-boundary prior
     holds: two codebases must agree on this wire, and a liquid contract
     under a stub-first regime means the stub proves a shape that can
     drift before the GPU consumes it — β is the false-positive
     generator. γ collapses into α: frozen-field-changes-as-new-versions
     already reserves the v0→v1 bump right permanently."

Wire shape per BCR §3.1 technical annex lines 79-87 verbatim:
    job_id: str                      required · server-minted, unique
    objective_ref: str               required
    trace_lineage: str               required · carried, never minted worker-side
    reextraction_handles: List[str]  required · min 1 · pointers into RMS estate
    modality: Literal[AUDIO, VIDEO]  required · TEXT never routes to GPU
    extraction_params_ref: str       required · frozen contract surface
    idempotency_key: str             required · same key => same job, never a second
    issued_at: str                   required · ISO-8601 UTC

D4b freeze prior: environment-boundary crossing (control plane → worker plane).
V1-G7 assertion set grows to 28 at 9.1 landing. Any future field change
requires PerceptionJob_v1 landing beside v0 (never mutating v0).
"""
from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class PerceptionJob_v0(BaseModel):
    """Perception job envelope — control plane → worker plane."""

    model_config = ConfigDict(extra="forbid")

    job_id: str = Field(
        ...,
        min_length=1,
        description="Server-minted unique job identifier. Never worker-provided.",
    )
    objective_ref: str = Field(
        ...,
        min_length=1,
        description="Objective envelope reference (ObjectiveRequest_v2.objective_id).",
    )
    trace_lineage: str = Field(
        ...,
        min_length=1,
        description="Trace lineage identifier; carried, never minted worker-side.",
    )
    reextraction_handles: List[str] = Field(
        ...,
        min_length=1,
        description="Pointers into RMS estate identifying units to perceive.",
    )
    modality: Literal["AUDIO", "VIDEO"] = Field(
        ...,
        description="GPU-perception modality. TEXT never routes to GPU (V1-I1).",
    )
    extraction_params_ref: str = Field(
        ...,
        min_length=1,
        description="Frozen extraction_params contract surface reference.",
    )
    idempotency_key: str = Field(
        ...,
        min_length=1,
        description="Retried dispatch of same key returns the same job, never a second (V1-I1).",
    )
    issued_at: str = Field(
        ...,
        min_length=1,
        description="ISO-8601 UTC timestamp at server-side mint.",
    )
