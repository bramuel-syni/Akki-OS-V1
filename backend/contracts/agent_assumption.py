"""AgentAssumption_v0 — Phase 7 Stage B-1 (§3.3 agent inference record).

Append-only agent-inference record on WizardCommitState_v0. One entry
per agent-supplied value (Guard 2 marking source). Every CommittedValue
with `source="agent_assumed"` references exactly one AgentAssumption via
`agent_assumption_id`.

FROZEN CONTRACT — additions only. Loose-as-frozen on `inferred_value`
(the agent may infer any lever type; narrow at v1 if type-per-field
narrows).
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AgentAssumption_v0(BaseModel):
    """One agent-supplied value record (append-only)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    assumption_id: str = Field(..., min_length=1, description="uuid; referenced by CommittedValue_v0.agent_assumption_id.")
    at: str = Field(..., min_length=1, description="ISO-8601 UTC.")
    field: str = Field(..., min_length=1, description="Dotted-path field name (e.g. 'output.grain').")
    inferred_value: Any = Field(..., description="Loose-as-frozen; type narrows at v1 post-G2b if lever types narrow.")
    evidence_ref: str = Field(
        default="",
        description="Optional trace pointer to the inference evidence. Loose-as-frozen; empty when not applicable.",
    )
