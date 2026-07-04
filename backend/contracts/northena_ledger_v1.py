"""northena_ledger_row@v1 — new contract version (Phase 5 Stage B, 2026-07-04).

Owner ruling B (Phase 5 Stage A close, 2026-07-04):
  * `stamp_audit` sidecar precedent absorbs artifacts, NEVER contradicts a
    primary field. A `decision` field reading `terminate_budget` for a
    caller-cancel is a known-false value on an append-only audit record
    annotated in a sidecar — a doctrinally rejected pattern.
  * Frozen field changes land as NEW contract versions, never in-place.

v1 differs from v0 by EXACTLY ONE addition:
  * `_ALLOWED["converge"]` gains the value `"terminate_cancelled"`.
  * `decision` `Literal` extends to include `"terminate_cancelled"`.

Everything else (fields, shape, stage enum, artifact_ref, model_config) is
byte-identical to v0. Superset-validating: `NorthenaLedgerRow_v1.model_validate(row)`
MUST parse every row that `NorthenaLedgerRow.model_validate(row)` (v0) parses.

v0 file `contracts/northena_ledger.py` UNTOUCHED — SHA-identity preserved
from Phase 4b close (`68349bb01971f174…`). Named regression gate
`test_northena_ledger_v0_byte_identical_after_5b`.

Superset-validation named gate: `test_northena_ledger_v1_supersets_v0`.

Standing Owner Disposition landed with this contract:
  frozen-field-changes-as-new-versions (§0.1, 2026-07-04) — audit reads
  accept both versions via superset-validating.
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from contracts.northena_ledger import LedgerArtifactRef, NORTHENA_LEDGER_COLLECTION


_ALLOWED_V1 = {
    "admit":    {"admitted", "refused"},
    "gate":     {"warm", "fresh", "refused"},
    "converge": {"terminate_success", "terminate_budget", "continue", "terminate_cancelled"},
}


class NorthenaLedgerRow_v1(BaseModel):
    """v1 ledger row — superset of v0 by exactly one additional converge decision."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(..., description="uuid — one run has one closed Ledger.")
    trace_id: str = Field(..., description="Joins ledger to unit-level intelligence.")
    stage: Literal["admit", "gate", "converge"]
    decision: Literal[
        "admitted", "refused",
        "warm", "fresh",
        "terminate_success", "terminate_budget", "continue",
        "terminate_cancelled",
    ]
    reason: str = Field(..., description="Deterministic reason string.")
    artifact_ref: LedgerArtifactRef
    lawful_basis_ref: str
    stamp_audit: Optional[Dict] = Field(
        default=None,
        description="Absorbed defensibility stamp-audit entry when present (§7.3).",
    )
    at: datetime

    @model_validator(mode="after")
    def _stage_decision_consistent(self) -> "NorthenaLedgerRow_v1":
        allowed = _ALLOWED_V1[self.stage]
        if self.decision not in allowed:
            raise ValueError(
                f"stage={self.stage!r} does not admit decision={self.decision!r}; "
                f"allowed for this stage: {sorted(allowed)}"
            )
        return self


# Re-export the collection name for consumers.
__all__ = ["NorthenaLedgerRow_v1", "NORTHENA_LEDGER_COLLECTION"]
