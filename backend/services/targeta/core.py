"""Targeta Core — deterministic eligibility + ranking (mandate §9).

**core.py imports NO ML library.** Enforced by `test_core_has_no_ml_import`.

Reads Registry + governing artifact; applies the floor as a hard filter;
ranks the eligible set by a fixed, inspectable function. Complete
targeter by invariant (§14 #1, §17 #2).
"""
from typing import Dict, List

from contracts.five_rings import DefensibilityClass
from services.targeta.interface import EligibleCandidate

# Class ordering — Solva CLASS_ORDER verbatim (mandate §10 semantics).
_CLASS_ORDER = {"non_factual": 0, "utterance": 1, "fact": 2}


def _class_rank(defensibility_class: str) -> int:
    return _CLASS_ORDER.get(defensibility_class, -1)


def _meets_floor(defensibility_class: str, floor: DefensibilityClass) -> bool:
    """Hard filter: `class_rank >= floor_rank`."""
    return _class_rank(defensibility_class) >= _class_rank(floor.value)


def _relevance(record: Dict, objective_shape: str) -> float:
    """Deterministic relevance score in [0, 1].

    G4 v0: 1.0 if the record's region matches the objective shape key
    (case-insensitive substring), else 0.5 (still eligible; ranking-only).
    Real relevance computation lands post-G4.
    """
    region = str(record.get("region", "")).lower()
    shape = objective_shape.lower()
    return 1.0 if region and shape and (region in shape or shape in region) else 0.5


def eligible_and_rank(
    registry_rows: List[Dict],
    floor: DefensibilityClass,
    objective_shape: str,
) -> List[EligibleCandidate]:
    """Mandate §9 verbatim. Applies floor as hard filter; ranks
    eligible set deterministically.

    Order of tie-break: descending `objective_relevance`, then
    descending `_class_rank`, then ascending `source_ref` for stability.
    """
    out: List[EligibleCandidate] = []
    for r in registry_rows:
        klass = r.get("defensibility_class", "non_factual")
        if not _meets_floor(klass, floor):
            continue  # excluded, full stop
        out.append(EligibleCandidate(
            source_ref=r["source_ref"],
            region=r.get("region", ""),
            objective_relevance=_relevance(r, objective_shape),
            registry_defensibility=float(_class_rank(klass)),
            baseline_rank=-1,
        ))
    # Fixed, inspectable ranking:
    out.sort(
        key=lambda c: (
            -c.objective_relevance,
            -c.registry_defensibility,
            c.source_ref,  # stable tie-break
        )
    )
    return [
        EligibleCandidate(
            source_ref=c.source_ref, region=c.region,
            objective_relevance=c.objective_relevance,
            registry_defensibility=c.registry_defensibility,
            baseline_rank=i,
        )
        for i, c in enumerate(out)
    ]
