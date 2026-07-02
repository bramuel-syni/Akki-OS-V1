"""Layer C convergence surface — G3 addition.

Source: Product Spec 2.1 §C (layer C description) + Solva Spec §12.

Layer C's job at G3:
  * `normalize_and_stamp` — already present in `aggregator.py` (from_asr,
    from_vision). Untouched by G3 reshape.
  * `converge_units` — NEW at G3. Validates every unit's Signal ring
    conformance against `signal_ring_dimensions@v0` (frozen catalogue),
    then hands off to Solva reasoning stage 1 (Frame).
  * `assert_signal_ring_conformant` — a callable guard usable from any
    caller wanting the signal-ring set-membership check.

Cousin chain (transitive):
  `services/layer_c/aggregator.py::from_asr` — the existing `_matrix_lookup`
    + declaration-baseline stamping pattern.
  `contracts.signal_ring.SignalRing` — the frozen shape being validated.
  `backend/tests/invariants/signal_ring_dimensions.v0.content_snapshot.json`
    — the authoritative dimension catalogue.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Sequence, Set

from contracts.five_rings import Modality, NormalizedUnit


class SignalRingConformanceError(ValueError):
    """Signal ring dimensions do not conform to signal_ring_dimensions@v0."""


def _load_frozen_catalogue() -> Dict[str, Set[str]]:
    """Load `signal_ring_dimensions@v0` from the frozen invariant snapshot."""
    here = Path(__file__).resolve().parent.parent.parent  # /app/backend
    snap = here / "tests" / "invariants" / "signal_ring_dimensions.v0.content_snapshot.json"
    with snap.open() as f:
        data = json.load(f)
    return {mod: set(dims) for mod, dims in data["catalogue"].items()}


_CATALOGUE: Dict[str, Set[str]] = _load_frozen_catalogue()


def assert_signal_ring_conformant(unit: NormalizedUnit) -> None:
    """Raise if the unit's Signal ring uses dimensions outside the frozen catalogue.

    Empty dimensions (`{}`) is trivially conformant (subset).
    """
    modality: str = unit.provenance.modality.value if isinstance(unit.provenance.modality, Modality) else str(unit.provenance.modality)
    allowed: Set[str] = _CATALOGUE.get(modality, set())
    got: Set[str] = set(unit.signal.dimensions.keys())
    extra = got - allowed
    if extra:
        raise SignalRingConformanceError(
            f"unit {unit.unit_id} modality={modality} carries non-catalogue "
            f"dimensions {sorted(extra)}; allowed={sorted(allowed)}"
        )


def converge_units(units: Sequence[NormalizedUnit]) -> List[NormalizedUnit]:
    """G3 convergence surface. Validates conformance; returns units unchanged.

    Multi-unit convergence (Ring 3 edge computation for corroboration /
    contradiction / retraction across units) is on the roadmap; at G3
    the shipped path is: verify signal-ring conformance, hand off to
    Solva reasoning stage 1 (Frame). Ring 3 population lands with the
    first real multi-unit run material at G4+.
    """
    for u in units:
        assert_signal_ring_conformant(u)
    return list(units)
