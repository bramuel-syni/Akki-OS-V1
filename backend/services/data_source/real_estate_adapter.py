"""Real RMS data source — placeholder until real material lands.

Flipped on at the G2 V1 timing when the first real RMS broadcast hour
is ingested. Today this class raises on construction so that any
accidental switch to `AKKI_DATA_SOURCE=real` fails loudly.

G0 Deliverable 3.a: "placeholder that raises NotImplementedError today,
switched on later when real RMS material lands. Configuration-switchable,
not code-change-required."
"""
from __future__ import annotations

from typing import Iterable

from contracts.five_rings import NormalizedUnit


class RealRmsDataSource:
    name = "real-rms"
    mode = "real"

    def __init__(self) -> None:
        raise NotImplementedError(
            "RealRmsDataSource is not yet wired. It comes online at G2 when the "
            "first real RMS broadcast hour is ingested. Until then set "
            "AKKI_DATA_SOURCE=synthetic (the default)."
        )

    def iter_units(self) -> Iterable[NormalizedUnit]:  # pragma: no cover
        raise NotImplementedError

    def get(self, unit_id: str) -> NormalizedUnit:  # pragma: no cover
        raise NotImplementedError
