"""northena_ledger_row@v0 — the contract-grade Ledger row.

Mandate-binding: `/app/docs/mandates/northena_v1.0.md` §7.2 verbatim.

Nine fields — no more, no less at v0 (stakeholder-restricted; mandate
says "at least" but stakeholder G2a brief locks v0 to the nine below).
Bumping the row shape requires re-blessing the snapshot in code review.

Stage / decision consistency (mandate §7.2 verbatim enum list):
  * admit     ∈ { admitted, refused }
  * gate      ∈ { warm, fresh, refused }
  * converge  ∈ { terminate_success, terminate_budget, continue }
Enforced by a Pydantic `model_validator` and by N-INV-8 test.

Cousin substrate cited: shape of the append-only audit row pattern lifted
from `services/synisense/shield/audit_log.py::AUDIT_COLLECTION` — same
"row is a contract, DPO reads it" discipline; the LedgerRow is the
run-level analogue of the Shield's per-invocation row.
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LedgerArtifactRef(BaseModel):
    """§7.2: { artifact_type, artifact_id, version }."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    artifact_type: Literal["portfolio_mandate", "objective_request"]
    artifact_id: str
    version: str


# Frozen collection name — §12 mandate directive: contract-grade from
# first commit means the collection name is part of the contract.
NORTHENA_LEDGER_COLLECTION = "northena_ledger_rows"


_ALLOWED = {
    "admit":    {"admitted", "refused"},
    "gate":     {"warm", "fresh", "refused"},
    "converge": {"terminate_success", "terminate_budget", "continue"},
}


class LedgerRow(BaseModel):
    """§7.2 — the contract-grade Ledger row. Nine fields."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(..., description="uuid — one run has one closed Ledger.")
    trace_id: str = Field(..., description="Joins ledger to unit-level intelligence and trace lenses.")
    stage: Literal["admit", "gate", "converge"]
    decision: Literal[
        "admitted", "refused",
        "warm", "fresh",
        "terminate_success", "terminate_budget", "continue",
    ]
    reason: str = Field(..., description="Deterministic reason string.")
    artifact_ref: LedgerArtifactRef
    lawful_basis_ref: str
    stamp_audit: Optional[Dict] = Field(
        default=None,
        description="Absorbed defensibility stamp-audit entry when present (§7.3): "
                    "{ unit_id, decision, reason, judged_signal_dimensions, floor_violation }.",
    )
    at: datetime

    @model_validator(mode="after")
    def _stage_decision_consistent(self) -> "LedgerRow":
        allowed = _ALLOWED[self.stage]
        if self.decision not in allowed:
            raise ValueError(
                f"stage={self.stage!r} does not admit decision={self.decision!r}; "
                f"allowed for this stage: {sorted(allowed)}"
            )
        return self
