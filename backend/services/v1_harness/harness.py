"""V1 measurement harness — G0.5 Deliverable 4.b
                          + Pre-G2 hardening (2026-07-01).

Hard Rule 1 enforced: `run(spike_hour, production_hour)` are two
DISTINCT named parameters; identical paths raise immediately.

Until real RMS material lands, every `run(...)` against synthetic
returns `verdict=PENDING_REAL_MATERIAL` and refuses to assign PASS/FAIL.

Pre-G2 hardening added `compare_runs(...)` per the
`extraction_params@v0` stakeholder corrections:
  * Use `reproducibility_keys(modality)` — NOT the full mandatory key
    set. `extracted_at` is mandatory-yes / anchor-no per stakeholder
    correction #1: a timestamp records *when* a run happened, it does
    not *determine the output*.
  * Gate the two-run comparison on
    `is_deterministically_reproducible(params)`. If either run has any
    nested `temperature` != 0 (stakeholder correction #2), the harness
    flags `non_reproducible_by_construction=True` with the failing
    keys listed, and REFUSES to assert "outputs differ → bug". Sampling
    noise is not a bug — the harness must say so explicitly rather
    than chase phantom diffs.

No cousin — net-new harness. Metrics module (`metrics.py`) sketches
standard ASR/diarization scoring — substantive scorer ports happen at
G2 when we have real labelled data to validate against.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from contracts.extraction_params import (
    is_deterministically_reproducible,
    reproducibility_keys,
)
from services.v1_harness.types import HourBundle, V1Metrics, V1Report


class HoursIdenticalError(Exception):
    pass


_LAST_REPORT: Optional[V1Report] = None


def last_report() -> Optional[V1Report]:
    return _LAST_REPORT


def run(*, spike_hour: HourBundle, production_hour: Optional[HourBundle] = None) -> V1Report:
    """Run the harness.

    * `production_hour=None` is the SPIKE-ONLY mode (legitimate at G0.5).
    * `production_hour=spike_hour` (same `audio_path`) raises HoursIdenticalError
      to enforce Hard Rule 1.
    * If any bundle is `is_synthetic=True`, the harness refuses to
      compute PASS/FAIL and returns PENDING_REAL_MATERIAL with the
      synthetic-only metrics for plumbing telemetry.
    """
    global _LAST_REPORT

    if production_hour is not None and production_hour.audio_path == spike_hour.audio_path:
        raise HoursIdenticalError(
            "V1 harness refuses to validate against the hour it was tuned on. "
            f"Provide a held-out production_hour distinct from spike_hour ({spike_hour.audio_path})."
        )

    notes: List[str] = []
    if spike_hour.is_synthetic or (production_hour and production_hour.is_synthetic):
        notes.append(
            "synthetic-fixture bundle present — verdict held at PENDING_REAL_MATERIAL. "
            "V1 metrics are honest only against real RMS material."
        )
        metrics = V1Metrics(
            five_rings_completeness={
                "provenance": 1.0, "re_extraction_handle": 1.0,
                "defensibility": 1.0, "signal": 1.0, "relational": 0.0,
            },
        )
        report = V1Report(
            verdict="PENDING_REAL_MATERIAL",
            metrics=metrics,
            spike_hour_path=spike_hour.audio_path,
            production_hour_path=production_hour.audio_path if production_hour else None,
            notes=notes,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        _LAST_REPORT = report
        return report

    # Real-material path. Metric computation is a placeholder until real
    # Hour A arrives — we explicitly journal that the substantive scorers
    # land at G2.
    notes.append("V1 substantive metric computation pending real Hour A; placeholder runner only.")
    metrics = V1Metrics()
    report = V1Report(
        verdict="PENDING_REAL_MATERIAL",
        metrics=metrics,
        spike_hour_path=spike_hour.audio_path,
        production_hour_path=production_hour.audio_path if production_hour else None,
        notes=notes,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    _LAST_REPORT = report
    return report


def compare_runs(
    *,
    modality: str,
    params_a: Dict[str, Any],
    params_b: Dict[str, Any],
) -> Dict[str, Any]:
    """Two-run extraction_params comparison — Pre-G2 hardening.

    Gates on `is_deterministically_reproducible()` BEFORE comparing —
    if either run has any nested `temperature != 0`, refuse to assert
    "outputs differ → bug" (stakeholder correction #2: sampling noise
    is not a bug).

    Comparison uses `reproducibility_keys(modality)` only — never the
    full mandatory key set (stakeholder correction #1: `extracted_at`
    records *when*, not *what*).

    Returns a dict report shaped for journal / audit consumption.
    """
    det_a, fail_a = is_deterministically_reproducible(params_a)
    det_b, fail_b = is_deterministically_reproducible(params_b)
    if not (det_a and det_b):
        return {
            "non_reproducible_by_construction": True,
            "failing_temperature_keys": sorted(set(fail_a) | set(fail_b)),
            "subset_equal": None,
            "notes": [
                "temperature > 0 on at least one run — non-reproducible-by-construction. "
                "Sampling noise is not a bug; comparison refused."
            ],
        }
    anchor_keys = reproducibility_keys(modality)
    sub_a = {k: params_a.get(k) for k in anchor_keys}
    sub_b = {k: params_b.get(k) for k in anchor_keys}
    return {
        "non_reproducible_by_construction": False,
        "failing_temperature_keys": [],
        "reproducibility_keys_used": sorted(anchor_keys),
        "reproducibility_subset_a": sub_a,
        "reproducibility_subset_b": sub_b,
        "subset_equal": sub_a == sub_b,
        "notes": (
            []
            if sub_a == sub_b
            else ["reproducibility-anchor keys differ across runs — investigate."]
        ),
    }
