"""Targeta Interface types — the one-way set-preserving boundary (§10).

The boundary as a TYPE. `YieldCandidate` is the ONLY view the yield
layer receives — it excludes `defensibility_floor` and
`registry_defensibility` by construction. The bias hazard is
unrepresentable, not policed.

`apply_yield` validates set-equal + permutation before reordering.
Non-permutation raises — it is not caught and corrected, it is rejected
(§10 verbatim).
"""
from dataclasses import dataclass, replace
from typing import Callable, List, Mapping, Sequence


class NonPermutationError(TypeError):
    """Raised when a yield function returns a non-permutation of its
    input. Mandate §10 + §17 #3 verbatim: 'A non-permutation is a
    type error.'"""


@dataclass(frozen=True)
class EligibleCandidate:
    """Core-internal type. Carries `registry_defensibility` and
    `baseline_rank` — NEVER crosses to the yield layer."""
    source_ref: str
    region: str
    objective_relevance: float           # deterministic core computation
    registry_defensibility: float        # from Registry; NEVER crosses to yield
    baseline_rank: int                   # core-assigned deterministic position


@dataclass(frozen=True)
class YieldCandidate:
    """The ONLY view the yield layer receives. Mandate §8 verbatim.
    Excludes floor + registry_defensibility by construction."""
    source_ref: str
    features: Mapping[str, float]
    objective_shape: str                 # conditioning key, NOT the floor value


# Type aliases (mandate §8):
YieldInput = Sequence[YieldCandidate]
Permutation = Sequence[str]              # ordering of source_refs, nothing more


def _safe_features(c: EligibleCandidate) -> Mapping[str, float]:
    """Extract features safe to expose to the yield layer.

    Excludes: `registry_defensibility` (mandate §10 verbatim), the floor
    (never in EligibleCandidate to begin with).

    Includes: `objective_relevance` (deterministic core score),
    `baseline_rank` (as float; ordering-only).
    """
    return {
        "objective_relevance": c.objective_relevance,
        "baseline_rank": float(c.baseline_rank),
    }


def _shape_key(c: EligibleCandidate) -> str:
    """Objective-shape conditioning key (mandate §11). NOT the floor
    value. G4 v0: derive from region (a stable, low-cardinality axis)."""
    return f"region:{c.region}"


def to_yield_input(eligible: Sequence[EligibleCandidate]) -> List[YieldCandidate]:
    """Strip to yield-safe view. Mandate §10 verbatim."""
    return [
        YieldCandidate(
            source_ref=c.source_ref,
            features=_safe_features(c),
            objective_shape=_shape_key(c),
        )
        for c in eligible
    ]


def apply_yield(
    eligible: Sequence[EligibleCandidate],
    yield_fn: Callable[[YieldInput], Permutation],
) -> List[EligibleCandidate]:
    """The one-way boundary. Mandate §10 verbatim.

    Constructs stripped `YieldInput`, invokes yield_fn, validates set-
    equality, then reorders. NonPermutationError is a TYPE error, not a
    runtime warning — no correction, no recovery."""
    order = yield_fn(to_yield_input(eligible))
    src = {c.source_ref for c in eligible}
    if len(order) != len(eligible) or set(order) != src:
        raise NonPermutationError("yield output is not a permutation")
    pos = {ref: i for i, ref in enumerate(order)}
    return [
        replace(c, baseline_rank=pos[c.source_ref])
        for c in sorted(eligible, key=lambda c: pos[c.source_ref])
    ]
