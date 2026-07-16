"""OnboardContext_v0 — S2.onboard structured intake envelope.

Owner ruling MC-E3 α (2026-07-14) + Op. Values §8 verbatim.

Structured intake per Operating Values §8:
    * Estate inventory: sources, systems, custodians.
    * Organizational vocabulary: entities, brands, people-of-record.
    * Rights posture per source: what the organization may license onward.
    * DPO contact + the five §6 seam values, set per-instance.
    * Objective priorities.

Versioned surface (`v0`) per governance — future v1 lands additively.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class EstateSource(BaseModel):
    """One source entry in the estate inventory."""

    model_config = ConfigDict(extra="forbid")

    source_ref: str = Field(..., description="Stable source identifier.")
    kind: str = Field(..., description="Source kind: 'tabular', 'db', 'audio_feed', 'video_feed', 'text_corpus'.")
    custodian: str = Field(..., description="Custodian contact (email or role).")
    rights_posture: str = Field(
        default="internal_only",
        description="License class for this source (feeds license_class at ingest). Default: internal_only (MC-E4 α fail-closed).",
    )


class SeamValues(BaseModel):
    """The §6 seam values, per-instance.

    G-3 (2026-07-15 · Owner ruling `docs/rulings/g3_operating_values_v1_1_2026-07-15.md`):
    additive extension to a SIXTH field per G3-E1 α (non-breaking, no new contract
    version, no Parity 31 contact — class NOT in `backend/contracts/`).
    Sixth field: `quarantine_systemic_halt_threshold` (F2 · 2% DEFAULT per-instance ·
    S2.onboard-set per MC-E3 α · dual-control on change per §6).
    """

    model_config = ConfigDict(extra="forbid")

    deletion_consequence_classes: str = Field(
        default="class-C=dual_control_always,class-B_over_1000=owner_escalation,class-A=operator",
    )
    rule_tightening_delay_hours: int = Field(default=72)
    objection_escalation_days: int = Field(default=7)
    suspension_re_review_days: int = Field(default=30)
    outer_gate_manual_review_threshold: str = Field(default=">10000_units_or_1gb_per_artifact")

    # G-3 additive · sixth seam value · Op. Values v1.1 §6.6 · EAB v1.1 F2
    # Value stored as fractional rate (0.02 = 2%); range-checked [0,1].
    # DEFAULT = 0.02 per Owner ruling; dual-control-on-change per §6 discipline.
    quarantine_systemic_halt_threshold: float = Field(
        default=0.02,
        ge=0.0,
        le=1.0,
        description=(
            "F2 sixth seam value · 2% DEFAULT · per-instance quarantine-rate "
            "threshold above which run halts systemically (per EAB v1.1 R-A4.2). "
            "Set at S2.onboard per MC-E3 α initial-set/ledger semantics; "
            "dual-control on change per §6."
        ),
    )


class OnboardContextV0(BaseModel):
    """S2.onboard structured intake envelope · Op. Values §8.

    Versioned as `onboard_context_v0` (additive). Persisted per-instance;
    initial set writes an initial-set ledger row (MC-E3 α · Owner ruling).
    """

    model_config = ConfigDict(extra="forbid")

    instance_id: str = Field(..., description="Target instance identifier.")
    estate_inventory: List[EstateSource] = Field(default_factory=list)
    org_vocabulary: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Canonical terms per category: entities, brands, people_of_record, etc.",
    )
    dpo_contact: str = Field(..., description="DPO email or role reference.")
    seam_values: SeamValues = Field(default_factory=SeamValues)
    objective_priorities: List[str] = Field(default_factory=list)
    onboard_version: str = Field(default="v0", frozen=True)
    submitted_by: Optional[str] = Field(default=None, description="Operator identifier at submission.")
