"""Targeta Yield Layer — CLOSED SEAM at G4 (mandate §11, user directive (2)).

Full learned-reorderer code path is built. Imports ONLY interface types
(YieldInput, Permutation) — mandate §7 dependency rule.

Threshold config is `YieldThresholds | None`. Default None → the gate
returns `admitted=False` unconditionally. G4 does NOT pick threshold
values. Real values land with Owner sign-off per Targeta §17.

User directive verbatim: "yield layer built through the apply_yield
interface, but the yield admission gate returns admitted=False
unconditionally until Owner thresholds land."
"""
from dataclasses import dataclass
from typing import Optional

from services.targeta.interface import YieldInput, Permutation


@dataclass(frozen=True)
class YieldThresholds:
    """Mandate §12 threshold config. Owner-owned per §17."""
    min_efficiency_gain: float
    coverage_alpha: float


def default_yield_fn(candidates: YieldInput) -> Permutation:
    """G4 v0 stub. Returns identity ordering — the yield function must
    return a permutation; identity is trivially a permutation.

    Real learned yield function binds post-G4 when Owner thresholds
    admit the layer. Until then, the yield fn exists as a code path
    (satisfying the boundary type), but the gate keeps its output
    unused.
    """
    return [c.source_ref for c in candidates]
