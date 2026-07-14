"""Data-source switch — G0 Deliverable 3.

Defines the `DataSource` Protocol with two implementations:
  * SyntheticPlumbingDataSource — emits fake-but-schema-valid units.
  * RealRmsDataSource           — placeholder, NotImplementedError today;
                                  flipped on once real RMS material arrives.

Configurable via `AKKI_DATA_SOURCE=synthetic|real` env var. The system_state
endpoint surfaces the active source so the G5 Engine console can render
"running on synthetic / V-gates pending" when applicable.
"""
from __future__ import annotations

import os
from typing import Iterable, Protocol, runtime_checkable

from contracts.five_rings import NormalizedUnit


@runtime_checkable
class DataSource(Protocol):
    """Source of NormalizedUnits the runtime composes over.

    Layer-D primitives (G3+) read from this. At G0 only the synthetic
    implementation is wired; the real implementation lands when the first
    RMS broadcast hour is delivered.
    """

    name: str
    mode: str  # "synthetic" | "real"

    def iter_units(self) -> Iterable[NormalizedUnit]:
        ...

    def get(self, unit_id: str) -> NormalizedUnit:
        ...


from services.data_source.synthetic import SyntheticPlumbingDataSource  # noqa: E402
from services.data_source.real_estate_adapter import RealRmsDataSource  # noqa: E402


def get_active_data_source() -> DataSource:
    """Read `AKKI_DATA_SOURCE` env (default `synthetic`) and return the source.

    The real source raises NotImplementedError on construction today (it
    has nothing to read), so flipping to `real` before G2 fails loudly
    — that is intentional.
    """
    mode = os.environ.get("AKKI_DATA_SOURCE", "synthetic").strip().lower()
    if mode == "real":
        return RealRmsDataSource()
    return SyntheticPlumbingDataSource()
