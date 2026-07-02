"""Mtafiti Registry — frozen contract (mandate §5, §13).

New at G4. Additions, not mutations. The six existing frozen contracts
(five_rings@v0, objective_request@v0, qualification_matrix@v0,
signal_ring_dimensions@v0, extraction_params@v0, northena_ledger_row@v0)
are UNTOUCHED.

Freeze contract: `MtafitiRegistryRecord.model_json_schema()` and
`FreshnessStamp` + `MtafitiScoreVector` are snapshotted to
`tests/invariants/mtafiti_registry_record.contract_snapshot.json`. Any
drift fails CI.

Naming discipline: `MtafitiScoreVector` (this file) is the Registry-write
composite over baseline + (admitted) detections. It is DISTINCT from
`contracts/five_rings.py::ScoreVector` (Ring 5 signal-strength). CONFIRM
line resolved: five_rings@v0 does NOT require mutation.
"""
from __future__ import annotations

from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


MTAFITI_REGISTRY_COLLECTION = "mtafiti_registry_records"


class SourceStanding(str, Enum):
    """Mandate §9: `accountable | licensed_wire | aggregator | ugc | unknown`."""

    ACCOUNTABLE = "accountable"
    LICENSED_WIRE = "licensed_wire"
    AGGREGATOR = "aggregator"
    UGC = "ugc"
    UNKNOWN = "unknown"


class FreshnessStamp(BaseModel):
    """Mandate §13 — two-level freshness check.

    L1 `logged_date` — LIVE at G4 (ISO-8601 UTC).
    L2 `structural_signature` — Optional at G4; nullable until on-disk
        fixture generator is surgically extended (Substrate-Drop v1
        G4-prep TODO). Absence of L2 is a valid state — L2 is a delta
        detector, not a required signature.
    """

    model_config = ConfigDict(extra="forbid")

    logged_date: str = Field(..., description="ISO-8601 UTC of last measure write.")
    structural_signature: Optional[str] = Field(
        default=None,
        description="16-hex sha256 of source content when fixture emits it; nullable at G4.",
    )


class MtafitiScoreVector(BaseModel):
    """Mandate §11 — composed baseline + (admitted) detections.

    When overlay NOT admitted: attachment=0.0, corroboration=0.0.
    When admitted: attachment/corroboration carry the detection values.

    DISTINCT from `contracts/five_rings.py::ScoreVector` (Ring 5).
    """

    model_config = ConfigDict(extra="forbid")

    source_standing: SourceStanding = Field(..., description="Deterministic per-feed baseline (mandate §9).")
    attachment: float = Field(default=0.0, ge=0.0, le=1.0, description="Detection: attributed/cited markedness (V3-gated).")
    corroboration: float = Field(default=0.0, ge=0.0, le=1.0, description="Detection: cross-estate corroboration (V3-gated).")
    recency_validity: float = Field(default=0.0, ge=0.0, le=1.0, description="Deterministic recency.")
    contested: bool = Field(default=False, description="Deterministic contested status.")


class MtafitiRegistryRecord(BaseModel):
    """Mandate §13 — one record per source. Contract-grade, snapshot + invariant."""

    model_config = ConfigDict(extra="forbid")

    source_ref: str = Field(..., description="Stable pointer (matches ProvenanceRing.source_ref).")
    region: str = Field(..., description="Estate region key.")
    feed_id: str = Field(..., description="Keys the declaration baseline.")
    sensitivity: str = Field(..., description="DPA sensitivity classification (mandate §8).")
    defensibility_measure: MtafitiScoreVector = Field(..., description="Composed measure (mandate §11).")
    defensibility_runtime_mode: Literal["declaration_baseline", "overlay"] = Field(
        default="declaration_baseline",
        description="Which measurement mode produced this record (mandate §12).",
    )
    matrix_rule_ref: str = Field(..., description="Governed Matrix rule id (mandate §17 #4). Auditable.")
    defensibility_class: Literal["fact", "utterance", "non_factual"] = Field(
        ...,
        description="Verdict from Matrix lookup (mandate §11 + §17 #4).",
    )
    freshness_stamp: FreshnessStamp
