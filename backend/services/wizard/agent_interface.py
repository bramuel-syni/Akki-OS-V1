"""Wizard agent interface — Phase 7 Stage B-1.

Standing Owner Disposition binding this module:
  * `Agent-pluggable-with-stub-agent-first` — [Owner ruling, Phase 7
    Stage A close, 2026-07-04] *"That's not a workaround — it's the
    right proof order: the mechanical guards (source-tagging, ask-slot
    structure) get proven independent of any prompt before an LLM ever
    sits behind the interface. If a guard only works with the LLM
    present, it was prompt discipline wearing a gate."*

Design:
  * `WizardAgent` Protocol — two methods (`next_turn`, `commit_review`).
  * `DeterministicStubAgent` — B-1 implementation; walks operator-mandatory
    field slots in a fixed order; returns deterministic ask content;
    NO LLM. Sufficient for Guard 1/2/3 gates to prove against.
  * B-2 will plug in Sonnet 4.6 behind the same interface without any
    state-machine changes (Owner ruling `Agent-pluggable-with-stub-agent-first`).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol

from contracts.wizard_commit_state import WizardCommitState_v0, operator_mandatory_fields


@dataclass(frozen=True)
class AgentTurnResponse:
    """Structured agent output for a single turn.

    `field_asked` names the operator-mandatory field the agent is
    asking about (Guard 1: agent asks mandatory, never proposes).
    `content` is the agent's rendered ask text.
    `is_ask` distinguishes ask turns from recommend turns (Guard 2:
    agent may recommend on preference-tier only; recommends land as
    agent_assumed).
    """
    field_asked: Optional[str]
    content: str
    is_ask: bool
    recommended_value: Optional[str] = None  # only for is_ask=False recommendations


@dataclass(frozen=True)
class CommitReviewPayload:
    """Marked-draft view for the commit-review UI.

    Painted per UI Spec §2.3 binding copy: `you_supplied` items rendered
    as "You supplied"; `agent_assumed_items` rendered as
    "Agent assumed — confirm or change".
    """
    you_supplied: List[Dict[str, str]] = field(default_factory=list)
    agent_assumed_items: List[Dict[str, str]] = field(default_factory=list)


class WizardAgent(Protocol):
    """Pluggable agent interface. B-1 uses DeterministicStubAgent; B-2
    plugs in Claude Sonnet 4.6 via emergentintegrations. No state-machine
    changes required at B-2."""

    def next_turn(self, state: WizardCommitState_v0) -> AgentTurnResponse:
        """Given the current session state, return the agent's next turn."""
        ...

    def commit_review(self, state: WizardCommitState_v0) -> CommitReviewPayload:
        """Given a state ready for commit-review, return the marked draft view."""
        ...


class DeterministicStubAgent:
    """B-1 stub — no LLM. Walks operator-mandatory field slots in a
    fixed order; returns deterministic ask content. Guard 1/2/3 gates
    are proven against THIS stub before B-2's LLM sits behind the
    interface.
    """

    # Fixed order for deterministic asks. B-2's LLM implementation may
    # reorder; the state machine ONLY relies on `field_asked` being one
    # of the mandatory slots.
    _ORDER = (
        "reach",
        "output.form",
        "output.consumer",
        "output.grain",
        "output.standard",
        "envelope.done_condition",
        "envelope.budget",
        "envelope.lawful_basis",
    )

    def next_turn(self, state: WizardCommitState_v0) -> AgentTurnResponse:
        # Find the first mandatory field the operator has not supplied.
        supplied = {
            name for name, cv in state.committed_values.items()
            if cv.source == "operator_supplied"
        }
        for field_name in self._ORDER:
            if field_name in supplied:
                continue
            return AgentTurnResponse(
                field_asked=field_name,
                content=f"Please supply a value for '{field_name}'.",
                is_ask=True,
            )
        # All mandatory fields supplied — ready for commit-review; a
        # recommendation turn (agent_assumed on any missing preference)
        # would land here in B-2 when preference tier is defined. B-1
        # stub does not recommend.
        return AgentTurnResponse(
            field_asked=None,
            content="All mandatory fields supplied. Ready for commit review.",
            is_ask=False,
        )

    def commit_review(self, state: WizardCommitState_v0) -> CommitReviewPayload:
        payload = CommitReviewPayload()
        for name in sorted(state.committed_values):
            cv = state.committed_values[name]
            entry = {"field": name, "value": str(cv.value)}
            if cv.source == "operator_supplied":
                payload.you_supplied.append(entry)
            else:
                payload.agent_assumed_items.append(entry)
        return payload


# Guard against constructing WizardCommitState_v0 with a variant this
# agent can't drive (buyer variant lands at B-2).
def is_operator_variant(state: WizardCommitState_v0) -> bool:
    return state.variant == "operator"


def operator_mandatory_field_names():
    """Re-export via this module so the state machine can import from
    a single seam."""
    return operator_mandatory_fields()
