"""Sequencing-harness measurement cells (rung-1/rung-2 exact + rung-3/rung-4 statistical).

Fold A.SH.5 (real-cost measurement · rung-1/rung-2 exact) +
Fold A.SH.6 (statistical-cost measurement · rung-3/rung-4).

Registry Doctrine §5.2 verbatim: *"measures real cost — not simulated
approximations. Principle: this system is predominantly deterministic;
you do not simulate a deterministic gate, you run it. [...] rung-3/rung-4
behavior is measured statistically (repeated runs over the harness,
route-level comparisons), never claimed as exact."*

Class E pinned parameters (per Owner G-13 ruling · sequencing-harness-v0):
  * REPETITION_COUNT = 10 · N=10 repetitions for statistical measurement
  * SIGNIFICANCE_ALPHA = 0.05 · α=0.05 threshold for route-level comparisons
"""
from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, field
from typing import Any, Callable, List, Literal

from services.sequencing_harness import (
    ENGINE_VERSION,
    REPETITION_COUNT,
    SIGNIFICANCE_ALPHA,
)


@dataclass(frozen=True)
class ExactMeasurement:
    """Rung-1/rung-2 deterministic measurement · single-run verdict."""

    function_id: str
    rung: Literal["rung-1", "rung-2"]
    wall_ms: float
    verdict: Any
    engine_version: str = ENGINE_VERSION


@dataclass(frozen=True)
class StatisticalMeasurement:
    """Rung-3/rung-4 statistical measurement · N-repetition verdict.

    Owner-verbatim discipline: "never claimed as exact" — statistical
    fields carry provenance labels + variance data.
    """

    function_id: str
    rung: Literal["rung-3", "rung-4"]
    repetitions: int  # matches REPETITION_COUNT unless overridden by engine version bump
    wall_ms_mean: float
    wall_ms_stdev: float
    significance_alpha: float  # matches SIGNIFICANCE_ALPHA
    verdict_bag: List[Any]  # list of per-repetition verdicts (never claimed as exact aggregate)
    engine_version: str = ENGINE_VERSION


def measure_deterministic(
    function_id: str,
    rung: Literal["rung-1", "rung-2"],
    fn: Callable[[Any], Any],
    payload: Any,
) -> ExactMeasurement:
    """Rung-1/rung-2: single-run exact measurement · you do not simulate a deterministic gate."""
    t0 = time.perf_counter()
    verdict = fn(payload)
    wall_ms = (time.perf_counter() - t0) * 1000.0
    return ExactMeasurement(
        function_id=function_id,
        rung=rung,
        wall_ms=wall_ms,
        verdict=verdict,
    )


def measure_statistical(
    function_id: str,
    rung: Literal["rung-3", "rung-4"],
    fn: Callable[[Any], Any],
    payload: Any,
    repetitions: int = REPETITION_COUNT,
) -> StatisticalMeasurement:
    """Rung-3/rung-4: N-repetition statistical measurement · route-level comparisons."""
    wall_ms_bag: List[float] = []
    verdict_bag: List[Any] = []
    for _ in range(repetitions):
        t0 = time.perf_counter()
        verdict = fn(payload)
        wall_ms_bag.append((time.perf_counter() - t0) * 1000.0)
        verdict_bag.append(verdict)
    mean = statistics.mean(wall_ms_bag)
    stdev = statistics.stdev(wall_ms_bag) if len(wall_ms_bag) > 1 else 0.0
    return StatisticalMeasurement(
        function_id=function_id,
        rung=rung,
        repetitions=repetitions,
        wall_ms_mean=mean,
        wall_ms_stdev=stdev,
        significance_alpha=SIGNIFICANCE_ALPHA,
        verdict_bag=verdict_bag,
    )
