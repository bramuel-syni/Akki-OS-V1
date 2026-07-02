"""Mtafiti V3 Overlay — admission gate (mandate §12).

**CLOSED SEAM at G4** — user directive (3) verbatim.

The full inference-overlay code path is built. `overlay_admitted()`
returns `False` unconditionally when `V3Thresholds is None`. Threshold
config is a nullable object; default None; Owner-owned per §18.

Closed-seam pattern (from user directive):
```python
def overlay_admitted(thresholds) -> bool:
    if thresholds is None:
        return False  # closed seam, no threshold configured
    return (v3_result.fact_precision >= thresholds.fact_precision
            and v3_result.genre_accuracy >= thresholds.genre_accuracy)
```

Never ship a learned path open on a permissive or invented value.
G4 does NOT pick thresholds. Real thresholds land with Owner + DPO.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class V3Thresholds:
    """Owner-owned thresholds (mandate §18). Nullable at G4."""
    fact_precision: float
    genre_accuracy: float
    inter_annotator_floor: float


@dataclass(frozen=True)
class V3Result:
    """Held-out measurement result. Feeds `overlay_admitted`."""
    fact_precision: float
    genre_accuracy: float
    inter_annotator_kappa: float


def overlay_admitted(
    thresholds: Optional[V3Thresholds],
    v3_result: Optional[V3Result] = None,
) -> bool:
    """Closed-seam admission gate.

    Returns:
      - False when thresholds is None (closed seam; no configuration)
      - False when v3_result is None (nothing to measure)
      - False when inter_annotator kappa below floor (kappa is a
        pre-condition per mandate §12 before accuracy is computed)
      - True iff both accuracy thresholds are met

    Ship deterministic path live; hold governed path behind closed gate.
    """
    if thresholds is None:
        return False
    if v3_result is None:
        return False
    if v3_result.inter_annotator_kappa < thresholds.inter_annotator_floor:
        return False
    return (v3_result.fact_precision >= thresholds.fact_precision
            and v3_result.genre_accuracy >= thresholds.genre_accuracy)


def runtime_mode(thresholds: Optional[V3Thresholds],
                 v3_result: Optional[V3Result] = None) -> str:
    """Mandate §13: `defensibility_runtime_mode` — 'declaration_baseline'
    (closed) or 'overlay' (admitted). Returns the state to record on
    the Registry record.
    """
    return "overlay" if overlay_admitted(thresholds, v3_result) else "declaration_baseline"
