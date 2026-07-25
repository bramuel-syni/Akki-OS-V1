"""Sequencing-harness candidate-ordering enumerator.

Fold A.SH.2 · Registry Doctrine §5.2 verbatim: *"Orderings are optimized
over the Registry's cost and dependency fields"*.
"""
from __future__ import annotations

from itertools import permutations
from typing import Dict, List, Set, Tuple


def enumerate_candidate_orderings(
    function_ids: List[str],
    dependencies: Dict[str, Set[str]],
) -> List[Tuple[str, ...]]:
    """Enumerate all orderings that respect dependency constraints.

    Each entry in `dependencies` maps a function_id to the set of
    function_ids that MUST precede it. Returns orderings that satisfy
    every dependency.

    For large function counts, use topological-batch enumeration
    (out-of-scope this atomic; the naive permutation-filter approach is
    correct for the small counts typical at G-13 landing).
    """
    if not function_ids:
        return [()]
    valid_orderings: List[Tuple[str, ...]] = []
    for perm in permutations(function_ids):
        seen: Set[str] = set()
        ok = True
        for fn_id in perm:
            required = dependencies.get(fn_id, set())
            if not required.issubset(seen):
                ok = False
                break
            seen.add(fn_id)
        if ok:
            valid_orderings.append(perm)
    return valid_orderings
