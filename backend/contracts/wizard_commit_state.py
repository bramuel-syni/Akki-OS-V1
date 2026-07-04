"""WizardCommitState_v0 — Phase 7 Stage B-1 (§3.3 shaping-wizard commit state).

The outer boundary of the operator variant shaping wizard. Persists
across HTTP requests during a multi-turn session, mints an
ObjectiveRequest_v2 at freeze, hands off to the Phase 5 async admission
surface via `frozen_objective_ref`.

FROZEN CONTRACT (23rd). Owner ratified E3 recommendation: FREEZE all
four wizard contracts (this + OperatorTurn_v0 + AgentAssumption_v0 +
CommittedValue_v0). Owner reasoning verbatim (2026-07-04):
  *"CommittedValue's source-tag (operator_turn_ref vs agent_assumed) IS
   the anti-laundering seam itself. Unfrozen inner inside frozen outer
   would let the seam drift silently while the outer snapshot stays
   byte-identical."*

Guards enforced at freeze time by `_validate_freeze_time_invariants`:
  * Guard 1 (Owner ruling §3.3): every operator-mandatory field
    (`reach`, `output.form`, `output.consumer`, `output.grain`,
    `output.standard`, `envelope.done_condition`, `envelope.budget`,
    `envelope.lawful_basis`) MUST have `source == "operator_supplied"`
    at freeze. Commit refuses on any Guard 1 violation.
  * Guard 2 (Owner ruling §3.3): every `agent_assumed` value MUST
    reference an existing entry in `agent_assumptions[]`. Orphan refs
    refuse.
  * Guard 3 (Owner ruling §3.3): every OperatorTurn_v0 has a non-empty
    `feasibility_snapshot_ref` (enforced structurally on OperatorTurn_v0
    via `min_length=1` — no separate freeze-time check needed).

Standing Owner Dispositions binding this shape:
  * Ruling E3 (Phase 7 Stage A close, 2026-07-04) — freeze all four.
  * Ruling E1 Option C (Phase 7 Stage A close, 2026-07-04) — license_class
    lives HERE (on the frozen wizard state), NOT on ObjectiveRequest_v2.
    `derive_license_class` reads it from the FROZEN state only, never
    mid-session working state. Primary arm of the two-arm derivation.
  * Disposition-must-cite-owner-ruling (Phase 6 Stage A close) — every
    ruling above cites the owner ruling verbatim.
"""
from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from contracts.agent_assumption import AgentAssumption_v0
from contracts.committed_value import CommittedValue_v0
from contracts.operator_turn import OperatorTurn_v0


# Operator-mandatory fields per v3 §3.3 verbatim. Frozen at v0; any
# extension lands as `WizardCommitState_v1` per `frozen-field-changes-
# as-new-versions` ruling.
_OPERATOR_MANDATORY_FIELDS = frozenset({
    "reach",
    "output.form",
    "output.consumer",
    "output.grain",
    "output.standard",
    "envelope.done_condition",
    "envelope.budget",
    "envelope.lawful_basis",
})


def operator_mandatory_fields() -> frozenset:
    """Exposed for the source-tagging validator + tests."""
    return _OPERATOR_MANDATORY_FIELDS


class WizardCommitState_v0(BaseModel):
    """Outer boundary of the shaping wizard. See module docstring for
    Guard 1/2/3 discipline and Standing Owner Dispositions binding this
    shape.

    NOTE: `variant: Literal["operator", "buyer"]` is declared at v0 for
    forward-compatibility with the B-2 buyer variant landing. B-1 code
    paths only emit `variant="operator"`; the buyer branch's state
    machine + offerability check land at B-2.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    session_id: str = Field(..., min_length=1, description="uuid-like; unique per wizard session.")
    trace_id: str = Field(..., min_length=1, description="Northena/Solva correlator; shared with downstream admission.")
    variant: Literal["operator", "buyer"] = Field(
        ..., description="Discriminator; immutable within session (enforced at persistence layer, not contract).",
    )
    initiated_at: str = Field(..., min_length=1, description="ISO-8601 UTC.")
    committed_at: Optional[str] = Field(
        default=None,
        description="ISO-8601 UTC. Set at freeze; None while session is open.",
    )
    turns: List[OperatorTurn_v0] = Field(default_factory=list, description="Append-only turn ledger.")
    agent_assumptions: List[AgentAssumption_v0] = Field(
        default_factory=list, description="Append-only agent-inference ledger.",
    )
    committed_values: Dict[str, CommittedValue_v0] = Field(
        default_factory=dict,
        description="Keyed by dotted-path field name; each value carries the source-tag anti-laundering seam.",
    )
    feasibility_history: List[str] = Field(
        default_factory=list,
        description="Per-turn feasibility_snapshot_ref pointers. Guard 3 enforcement point (structural via OperatorTurn_v0 min_length).",
    )
    license_class: Optional[str] = Field(
        default=None,
        description="E1 Option C primary-arm value. Populated at commit-review; only read post-freeze by derive_license_class.",
    )
    frozen_objective_ref: Optional[str] = Field(
        default=None, description="Set at freeze; refs the minted ObjectiveRequest_v2's objective_id.",
    )

    @model_validator(mode="after")
    def _validate_freeze_time_invariants(self):
        """Guard 1 + Guard 2 fire ONLY at freeze (committed_at is not None).

        Mid-session state (committed_at is None) is permitted to hold
        arbitrary intermediate content; the freeze boundary is the
        governance check.
        """
        if self.committed_at is None:
            return self
        # Guard 1 — every operator-mandatory field is operator_supplied at freeze.
        if self.variant == "operator":
            for field_name in _OPERATOR_MANDATORY_FIELDS:
                cv = self.committed_values.get(field_name)
                if cv is None:
                    raise ValueError(
                        f"Guard 1 violation at freeze: operator-mandatory field "
                        f"{field_name!r} is missing from committed_values."
                    )
                if cv.source != "operator_supplied":
                    raise ValueError(
                        f"Guard 1 violation at freeze: operator-mandatory field "
                        f"{field_name!r} has source={cv.source!r}; MUST be "
                        f"'operator_supplied' (per v3 §3.3 + Owner E3 ruling)."
                    )
        # Guard 2 — every agent_assumed CommittedValue references a known assumption_id.
        known_assumption_ids = {a.assumption_id for a in self.agent_assumptions}
        for field_name, cv in self.committed_values.items():
            if cv.source == "agent_assumed":
                if cv.agent_assumption_id not in known_assumption_ids:
                    raise ValueError(
                        f"Guard 2 violation at freeze: committed_values[{field_name!r}] "
                        f"references unknown agent_assumption_id "
                        f"{cv.agent_assumption_id!r}."
                    )
        return self
