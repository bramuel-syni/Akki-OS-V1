"""Sequencing-harness ordering optimizer.

Fold A.SH.3 · Registry Doctrine §5.2 verbatim: *"cheap gates before
expensive, deterministic rungs before model rungs, independent functions
in parallel, fail-fast paths surfaced"*.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple


RUNG_ORDER: Dict[str, int] = {
    "rung-1": 0,  # deterministic first
    "rung-2": 1,
    "rung-3": 2,
    "rung-4": 3,  # model rungs last
}


@dataclass(frozen=True)
class FunctionCostRow:
    """Registry cost + rung + fail-fast marker for one function."""

    function_id: str
    rung: str
    expected_cost: float
    is_fail_fast: bool


def score_ordering(
    ordering: Sequence[str],
    cost_rows: Dict[str, FunctionCostRow],
) -> Tuple[int, int, float]:
    """Score an ordering per Registry Doctrine §5.2 optimization criteria.

    Returns a sort-key tuple where lower is better:
      * (fail_fast_position_penalty, rung_disorder_penalty, cost_before_expensive_penalty)

    Optimization goals (Owner-verbatim):
      1. cheap gates before expensive (cost accumulates left-to-right)
      2. deterministic rungs before model rungs
      3. fail-fast paths surfaced (early)
    """
    fail_fast_penalty = 0
    rung_disorder_penalty = 0
    cost_before_expensive_penalty = 0.0
    prev_rung_num = -1
    prev_cost = 0.0
    for i, fn_id in enumerate(ordering):
        row = cost_rows[fn_id]
        # fail-fast: penalize if fail-fast function is not early
        if row.is_fail_fast:
            fail_fast_penalty += i
        # rung-disorder: penalize if a lower rung follows a higher rung
        rung_num = RUNG_ORDER.get(row.rung, 99)
        if prev_rung_num >= 0 and rung_num < prev_rung_num:
            rung_disorder_penalty += 1
        prev_rung_num = rung_num
        # cost-before-expensive: penalize if a cheap gate follows an expensive one
        if row.expected_cost < prev_cost:
            cost_before_expensive_penalty += prev_cost - row.expected_cost
        prev_cost = max(prev_cost, row.expected_cost)
    return (fail_fast_penalty, rung_disorder_penalty, cost_before_expensive_penalty)


def optimize_orderings(
    orderings: List[Sequence[str]],
    cost_rows: Dict[str, FunctionCostRow],
) -> List[Sequence[str]]:
    """Return orderings sorted from best to worst per §5.2 optimization."""
    return sorted(orderings, key=lambda o: score_ordering(o, cost_rows))
