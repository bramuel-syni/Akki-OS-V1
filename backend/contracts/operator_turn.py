"""OperatorTurn_v0 — Phase 7 Stage B-1 (§3.3 turn record).

Append-only turn record on WizardCommitState_v0. One entry per
POST /api/wizard/operator/{session_id}/turn. `feasibility_snapshot_ref`
enforcement point for Guard 3 (per-turn feasibility grounding);
present-and-non-empty at commit time OR commit refuses.

FROZEN CONTRACT — additions only. Loose-as-frozen on `user_content` /
`agent_content` (free-form strings; narrow at v1 if turn-shape narrows).
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class OperatorTurn_v0(BaseModel):
    """One turn cycle record (append-only)."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    turn_ref: str = Field(..., min_length=1, description="uuid; identifies this turn across the wizard trace.")
    at: str = Field(..., min_length=1, description="ISO-8601 UTC.")
    user_content: str = Field(default="", description="Empty on agent-first ask turns before the user replies.")
    agent_content: str = Field(default="", description="Empty on user-first turns before the agent replies.")
    feasibility_snapshot_ref: str = Field(
        ...,
        min_length=1,
        description="Reference to WizardCommitState_v0.feasibility_history[] entry (Guard 3 enforcement point).",
    )
