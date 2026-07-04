"""Floor-feasibility shared derivation — Ruling 4 (single source of truth).

Spec authority: RMS Product & Engineering Spec v3 §5 + §4.

**One function. Two consumers. Zero re-implementation.**

Feasibility Query returns a `ClassDistribution` per reach (standard-agnostic —
one query serves any floor). But `floor_feasibility` is a governed value
recorded in a frozen envelope, and two consumers (wizard, admission)
computing it independently is a second-computation-path — the A2
`supported_class` lesson exactly.

Owner Ruling 4 (Substrate-Drop v2 → Phase 1 dispatch, 2026-07-03):
Derivation from `class_distribution × requested_standard` lives in ONE
shared function both consumers import. Reimplementation per consumer
fails review regardless of output equality. Enforced by
`tests/invariants/test_floor_feasibility_shared_derivation.py`.

**Deterministic. Objective-blind. No side effects. No Registry read.**

Class ordering follows `services/solva_depth/assertion.py:36-40`
`CLASS_ORDER`:  NON_FACTUAL(0) < UTTERANCE(1) < FACT(2). A floor of X
means units at level >= X meet the floor. So `qualifying_at_floor` is
the SUM of counts at classes >= floor.minimum_class.
"""
from __future__ import annotations

from typing import Any, Dict

from contracts.feasibility_result import ClassDistribution
from contracts.five_rings import DefensibilityClass
from contracts.objective_request import DefensibilityFloor


# Class ordinal — mirrors solva_depth CLASS_ORDER exactly. Load-bearing
# consistency: any drift here breaks the standard-as-hard-input-filter
# semantic in Service 1 (§6.1) too.
_CLASS_ORDER: Dict[DefensibilityClass, int] = {
    DefensibilityClass.NON_FACTUAL: 0,
    DefensibilityClass.UTTERANCE: 1,
    DefensibilityClass.FACT: 2,
}


def derive_floor_feasibility(
    class_distribution: ClassDistribution,
    requested_standard: DefensibilityFloor,
) -> Dict[str, Any]:
    """Single-source-of-truth derivation.

    Returns a dict recorded into `ObjectiveRequest_v2.Envelope.floor_feasibility`
    at shaping-time freeze. Callers (wizard + admission) MUST use this
    function; reimplementation is a Ruling-4 violation caught by
    `test_floor_feasibility_shared_derivation`.

    Return shape:
      * `feasible: bool` — does the qualifying set support the requested floor?
      * `qualifying_at_floor: int` — count of units at class >= floor.minimum_class.
      * `qualifying_below_floor: int` — count of units at class < floor.minimum_class.
      * `requested_minimum_class: str` — echo of input for envelope provenance.
      * `per_class_at_or_above_floor: Dict[str, int]` — the specific classes
        meeting the floor and their counts (helps operators see WHERE the
        support lies).
      * `gap_to_feasibility: Optional[Dict[str, int]]` — when infeasible,
        {`shortfall_units`: N (always at least 1 unit required)}; None otherwise.
      * `minimum_standard_supported: Optional[str]` — the highest floor
        the qualifying set WOULD meet with >= 1 unit; None if distribution
        is completely empty.
    """
    floor_ordinal = _CLASS_ORDER[requested_standard.minimum_class]

    per_class = {
        DefensibilityClass.FACT: class_distribution.fact,
        DefensibilityClass.UTTERANCE: class_distribution.utterance,
        DefensibilityClass.NON_FACTUAL: class_distribution.non_factual,
    }

    at_or_above: Dict[str, int] = {}
    below: int = 0
    for klass, count in per_class.items():
        if _CLASS_ORDER[klass] >= floor_ordinal:
            if count > 0:
                at_or_above[klass.value] = count
        else:
            below += count

    qualifying_at_floor = sum(at_or_above.values())
    feasible = qualifying_at_floor > 0

    gap = None
    if not feasible:
        # At infeasibility, at least one unit at or above the floor is missing.
        gap = {"shortfall_units": 1}

    # Highest floor the distribution supports (with >=1 unit at that ordinal).
    minimum_supported = None
    for klass in (DefensibilityClass.FACT, DefensibilityClass.UTTERANCE,
                  DefensibilityClass.NON_FACTUAL):
        if per_class[klass] > 0:
            minimum_supported = klass.value
            break

    return {
        "feasible": feasible,
        "qualifying_at_floor": qualifying_at_floor,
        "qualifying_below_floor": below,
        "requested_minimum_class": requested_standard.minimum_class.value,
        "per_class_at_or_above_floor": at_or_above,
        "gap_to_feasibility": gap,
        "minimum_standard_supported": minimum_supported,
    }
