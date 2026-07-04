"""CommittedValue_v0 — Phase 7 Stage B-1 (§3.3 Guard 1/2 discipline).

Per Owner ruling E3 (Phase 7 Stage A close, 2026-07-04): every committed
field on `WizardCommitState_v0` carries a source tag. `source` is the
anti-laundering seam — a wizard field marked `agent_assumed` on the
outer state but with `operator_turn_ref` set would silently launder an
agent inference as operator-supplied. The `operator_turn_ref XOR
agent_assumption_id` invariant enforcement is STRUCTURAL on this
contract; the outer WizardCommitState_v0's freeze-time model_validator
walks every committed value and rejects Guard 1 violations.

FROZEN CONTRACT — additions only per `frozen-field-changes-as-new-versions`.

Standing Owner Dispositions binding this shape:
  * Ruling E3 (Phase 7 Stage A close, 2026-07-04) — FREEZE all four wizard
    contracts. Inner shapes exist nowhere else; CommittedValue's
    source-tag IS the anti-laundering seam itself; unfrozen inner inside
    frozen outer would let the seam drift silently while the outer
    snapshot stays byte-identical.
  * Disposition-must-cite-owner-ruling (Phase 6 Stage A close) — every
    disposition transcribed here cites its owner ruling verbatim.
"""
from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CommittedValue_v0(BaseModel):
    """Per-field source-tagged committed value on WizardCommitState_v0.

    Structural invariant (enforced at construction time):
      exactly one of `operator_turn_ref` / `agent_assumption_id` is set;
      the other is None. Never both, never neither.

    The `source` field mirrors that split:
      * `operator_supplied` → operator_turn_ref set, agent_assumption_id None
      * `agent_assumed`     → agent_assumption_id set, operator_turn_ref None
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    value: Any = Field(..., description="Loose-as-frozen; type narrows at v1 post-G2b.")
    source: Literal["operator_supplied", "agent_assumed"] = Field(
        ..., description="Anti-laundering seam per Owner E3 ruling; MUST be consistent with the XOR ref pair below.",
    )
    operator_turn_ref: Optional[str] = Field(
        default=None, description="uuid pointing to a WizardCommitState_v0.turns[] entry. Set iff source='operator_supplied'.",
    )
    agent_assumption_id: Optional[str] = Field(
        default=None, description="uuid pointing to a WizardCommitState_v0.agent_assumptions[] entry. Set iff source='agent_assumed'.",
    )
    committed_at: str = Field(..., min_length=1, description="ISO-8601 UTC.")

    @model_validator(mode="after")
    def _validate_source_tag_invariant(self):
        n_refs = int(self.operator_turn_ref is not None) + int(self.agent_assumption_id is not None)
        if n_refs != 1:
            raise ValueError(
                "CommittedValue_v0 invariant: exactly one of operator_turn_ref or "
                f"agent_assumption_id MUST be set; got {n_refs}. This is the "
                "anti-laundering seam per Owner E3 ruling (Phase 7 Stage A close)."
            )
        if self.source == "operator_supplied" and self.operator_turn_ref is None:
            raise ValueError(
                "CommittedValue_v0: source='operator_supplied' requires operator_turn_ref."
            )
        if self.source == "agent_assumed" and self.agent_assumption_id is None:
            raise ValueError(
                "CommittedValue_v0: source='agent_assumed' requires agent_assumption_id."
            )
        return self
