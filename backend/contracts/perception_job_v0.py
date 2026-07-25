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


class ManifestEntry(BaseModel):
    """CIF §12 line 152 verbatim manifest entry — shared additive substructure.

    Landed at Critic-pass execution atomic under Owner ruling
    `docs/rulings/critic_pass_e1_2026_07_25.md` (SHA
    `42ca9e0f4605b497394772c83572b1e7c5469e17b2c6f7fa39452ec45992c80a`)
    posture (a1): additive fields on existing frozen contracts.

    ManifestEntry is FROZEN on landing; evolution is additive
    (`ManifestEntry_v1` at future seal, same as any contract).
    """

    model_config = ConfigDict(extra="forbid")

    assumption_text: str = Field(
        ..., min_length=1,
        description="The load-bearing assumption text carried on the verdict.",
    )
    evidence_class: Literal["fact", "recalled", "inferred"] = Field(
        ...,
        description="Honesty-grammar source label per PROM-S1-honesty-grammar-source-labels.",
    )
    flip_condition: str = Field(
        ..., min_length=1,
        description=(
            "The counterfactual probe per CIF §4 verbatim: 'what, if false, "
            "flips this?'"
        ),
    )


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
    manifest_entries: List[ManifestEntry] = Field(
        default_factory=list,
        description=(
            "CIF §12 schema-required verdict manifest · load-bearing "
            "assumptions evidence-classed · unmanifested verdict rejects at "
            "submission per B-1 (Owner ruling "
            "docs/rulings/critic_pass_e1_2026_07_25.md · additive-versioning "
            "per PROM-S1-additive-versioning)."
        ),
    )
