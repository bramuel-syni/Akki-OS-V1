"""Registry context · functions-in-scope resolver · fold B.WCH.1.

Determines which Registry v1 rows are "in force on the task" for a given
model worker invocation.

Registry Doctrine §6.2 verbatim: *"the promises in force on its task"* +
*"the functions it touches"*.

Static-declared-list posture: callers pass the explicit list of
function_ids in scope. Dynamic dependency-graph traversal is out of
scope this atomic (Class E parameter surface for a future E→O promotion
per A3.2).
"""
from __future__ import annotations

from typing import List


def resolve_functions_in_scope(declared_function_ids: List[str]) -> List[str]:
    """Return the declared function_ids as the in-scope list (deterministic order preserved).

    Static-declared-list posture at G-13 landing per Owner ruling
    scope discipline. Runtime tunability path: A3.2 E→O promotion
    would enable dependency-graph traversal (not this atomic).
    """
    # Deterministic order: preserve caller order (Owner-verbatim single-writer discipline).
    return list(declared_function_ids)
