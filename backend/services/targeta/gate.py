"""Targeta Gate — yield admission (mandate §12). CLOSED SEAM at G4.

Two-arm gate: Arm 1 (Helps) + Arm 2 (Coverage Veto). Veto overrides
helps (mandate §17 #6).

Closed-seam pattern (user directive verbatim):
```python
def yield_admission_gate(measurement) -> bool:
    if self.thresholds is None:
        return False  # closed seam, no threshold configured
    return measurement.efficiency_gain >= thresholds.min_efficiency_gain
```

This is the ONLY module allowed to compare the two orderings
(mandate §7 dependency rule).
"""
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence

from services.targeta.interface import EligibleCandidate, YieldInput, Permutation
from services.targeta.yield_layer import YieldThresholds


@dataclass(frozen=True)
class GateResult:
    """Mandate §12 verbatim shape."""
    admitted: bool
    helps: bool
    veto: bool
    reason: str


def _median(values: List[float]) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def evaluate_gate(
    thresholds: Optional[YieldThresholds],
    held_out: Sequence[dict] = (),
    core_fn: Optional[Callable[[dict], int]] = None,
    yield_fn: Optional[Callable[[dict], int]] = None,
) -> GateResult:
    """Two-arm admission gate. Mandate §12.

    G4 posture: `thresholds is None` → CLOSED. Returns
    `GateResult(admitted=False, helps=False, veto=False,
    reason='thresholds_not_configured')`.

    When thresholds land (Owner directive), the full two-arm computation
    runs:
      * Arm 1 (Helps): median efficiency gain >= min_efficiency_gain
      * Arm 2 (Veto): per-class coverage >= alpha * core-rate
      * admitted = (helps and not veto)
    """
    if thresholds is None:
        return GateResult(
            admitted=False, helps=False, veto=False,
            reason="thresholds_not_configured",
        )
    if not held_out or core_fn is None or yield_fn is None:
        return GateResult(
            admitted=False, helps=False, veto=False,
            reason="no_held_out_set_or_functions",
        )
    # Arm 1 — Helps
    gains: List[float] = []
    for obj in held_out:
        u_core = core_fn(obj)
        u_yield = yield_fn(obj)
        if u_core <= 0:
            continue
        gains.append((u_core - u_yield) / u_core)
    helps = _median(gains) >= thresholds.min_efficiency_gain if gains else False
    # Arm 2 — Coverage veto (simplified for the closed-seam scaffold;
    # real per-class coverage lands with real held-out material)
    veto = False
    admitted = helps and not veto
    return GateResult(
        admitted=admitted, helps=helps, veto=veto,
        reason=("admitted" if admitted else
                ("veto_starves_class" if veto else "insufficient_help")),
    )


def compose_ordering(
    eligible: Sequence[EligibleCandidate],
    thresholds: Optional[YieldThresholds],
    yield_fn: Optional[Callable[[YieldInput], Permutation]] = None,
) -> tuple:
    """Compose the final ordering.

    Returns (ordered_candidates, yield_layer_version). Mandate §17 #7:
    on gate failure → core ordering; `yield_layer_version='core-only'`.

    G4 posture: `thresholds is None` → core ordering; version='core-only'.
    """
    gate = evaluate_gate(thresholds)
    if not gate.admitted:
        return list(eligible), "core-only"
    # Admitted path (post-Owner). Kept lean at G4:
    from services.targeta.interface import apply_yield
    from services.targeta.yield_layer import default_yield_fn
    fn = yield_fn or default_yield_fn
    reordered = apply_yield(eligible, fn)
    return reordered, "yield-v1"
