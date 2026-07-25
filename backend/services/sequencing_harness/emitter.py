"""Sequencing-harness measured-best-path emitter · append-only measurement ledger.

Folds A.SH.7 (append-only measurement ledger · PROM-S3-append-only-ledger) +
Fold A.SH.8 (measured-best-path emitter · Registry cost back-fill).

Registry Doctrine §5.2 verbatim: *"Output: the measured best path of
integration and sequencing per journey — replacing sequencing judgment
with sequencing measurement, and back-filling every 'unknown' cost field
in the Registry."*
"""
from __future__ import annotations

import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class MeasurementLedgerRow:
    """Append-only measurement ledger row · PROM-S3-append-only-ledger discipline."""

    row_id: int
    journey_id: str
    ordering: Tuple[str, ...]
    total_wall_ms: float
    per_function_wall_ms: Tuple[Tuple[str, float], ...]
    ordering_score: Tuple[int, int, float]
    measured_at: str  # ISO-8601 UTC
    engine_version: str


_LOCK = threading.Lock()
_LEDGER: List[MeasurementLedgerRow] = []
_NEXT_ROW_ID: int = 1


def _reset_for_tests() -> None:
    global _NEXT_ROW_ID
    with _LOCK:
        _LEDGER.clear()
        _NEXT_ROW_ID = 1


def _isoformat_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_measurement(
    journey_id: str,
    ordering: Sequence[str],
    total_wall_ms: float,
    per_function_wall_ms: Dict[str, float],
    ordering_score: Tuple[int, int, float],
    engine_version: str,
) -> MeasurementLedgerRow:
    """Append an immutable measurement row."""
    global _NEXT_ROW_ID
    with _LOCK:
        row = MeasurementLedgerRow(
            row_id=_NEXT_ROW_ID,
            journey_id=journey_id,
            ordering=tuple(ordering),
            total_wall_ms=total_wall_ms,
            per_function_wall_ms=tuple(sorted(per_function_wall_ms.items())),
            ordering_score=ordering_score,
            measured_at=_isoformat_utc(),
            engine_version=engine_version,
        )
        _LEDGER.append(row)
        _NEXT_ROW_ID += 1
        return row


def get_ledger() -> List[MeasurementLedgerRow]:
    with _LOCK:
        return list(_LEDGER)


def emit_measured_best_path(journey_id: str) -> Optional[MeasurementLedgerRow]:
    """Return the best-scored ordering for a journey (Registry cost-field back-fill source).

    Ordering scores are minimized (lower is better) per optimizer.py.
    """
    with _LOCK:
        candidates = [r for r in _LEDGER if r.journey_id == journey_id]
    if not candidates:
        return None
    return min(candidates, key=lambda r: r.ordering_score)


def registry_cost_backfill_map() -> Dict[str, float]:
    """Aggregate per-function cost across all measurements (Registry back-fill source).

    Every measured function contributes its mean wall_ms across all
    ledger rows in which it appears. Callers persist to Registry v1.
    """
    accumulator: Dict[str, List[float]] = {}
    with _LOCK:
        rows = list(_LEDGER)
    for row in rows:
        for fn_id, wall_ms in row.per_function_wall_ms:
            accumulator.setdefault(fn_id, []).append(wall_ms)
    return {fn_id: (sum(bag) / len(bag)) for fn_id, bag in accumulator.items()}
