"""Source-tag commit-time invariant checker — Phase 7 Stage B-1.

Structural invariant (also enforced on CommittedValue_v0 model_validator):
  exactly one of `operator_turn_ref` / `agent_assumption_id` is set;
  the other is None.

Additional commit-time Guard 1 check (also enforced on
WizardCommitState_v0._validate_freeze_time_invariants at freeze):
  every operator-mandatory field's CommittedValue MUST have
  `source == "operator_supplied"`.

This module provides a SERVICE-LAYER re-entry point so the state
machine can pre-validate a working-state before attempting to freeze
(cleaner error surface than raising deep inside model_validator).
"""
from __future__ import annotations

from typing import Dict, List

from contracts.committed_value import CommittedValue_v0
from contracts.wizard_commit_state import operator_mandatory_fields


class SourceTagViolation(RuntimeError):
    """Structural violation of the source-tag invariant OR Guard 1."""


def _validate_single_committed_value(name: str, cv: CommittedValue_v0) -> List[str]:
    """Return a list of violation messages (empty iff clean).

    Note: `CommittedValue_v0.__init__` already enforces the XOR
    invariant. This wrapper re-checks to give a service-layer error
    surface when construction happens elsewhere (e.g. deserialised
    from Mongo without re-validation).
    """
    violations = []
    n_refs = int(cv.operator_turn_ref is not None) + int(cv.agent_assumption_id is not None)
    if n_refs != 1:
        violations.append(
            f"committed_values[{name!r}]: source-tag XOR invariant broken "
            f"(operator_turn_ref set: {cv.operator_turn_ref is not None}, "
            f"agent_assumption_id set: {cv.agent_assumption_id is not None})."
        )
    if cv.source == "operator_supplied" and cv.operator_turn_ref is None:
        violations.append(
            f"committed_values[{name!r}]: source='operator_supplied' but "
            f"operator_turn_ref is None."
        )
    if cv.source == "agent_assumed" and cv.agent_assumption_id is None:
        violations.append(
            f"committed_values[{name!r}]: source='agent_assumed' but "
            f"agent_assumption_id is None."
        )
    return violations


def validate_source_tags(committed_values: Dict[str, CommittedValue_v0]) -> None:
    """Raise SourceTagViolation on any structural violation."""
    all_violations: List[str] = []
    for name, cv in committed_values.items():
        all_violations.extend(_validate_single_committed_value(name, cv))
    if all_violations:
        raise SourceTagViolation(
            "Source-tag violations detected:\n  - " + "\n  - ".join(all_violations)
        )


def validate_guard_1_operator_mandatory_all_operator_supplied(
    committed_values: Dict[str, CommittedValue_v0],
    variant: str = "operator",
) -> None:
    """Guard 1 pre-flight — every operator-mandatory field is
    `operator_supplied`. Only fires for `variant == "operator"`;
    buyer variant has different mandatory semantics at B-2."""
    if variant != "operator":
        return
    violations: List[str] = []
    for field_name in operator_mandatory_fields():
        cv = committed_values.get(field_name)
        if cv is None:
            violations.append(
                f"Guard 1: operator-mandatory field {field_name!r} missing at commit."
            )
            continue
        if cv.source != "operator_supplied":
            violations.append(
                f"Guard 1: operator-mandatory field {field_name!r} has "
                f"source={cv.source!r}; MUST be 'operator_supplied'."
            )
    if violations:
        raise SourceTagViolation(
            "Guard 1 violations detected:\n  - " + "\n  - ".join(violations)
        )
