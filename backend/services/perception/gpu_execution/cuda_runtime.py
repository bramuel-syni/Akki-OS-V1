"""GPU execution layer — CPU/GPU backend selection (Owner 9.2a-E2 α · 2026-07-10).

Owner ruling 9.2a-E2 α + two conditions verbatim carrier:

    'α, two conditions. (1) No silent default at deployment: env var unset ->
     explicit import-time failure, never a silent fallback to CPU — a GPU
     deployment quietly running CPU is the silent-swap risk in the other
     direction. CI sets cpu explicitly. (2) execution_mode lands in result
     telemetry — attribution of GPU-hours and yield to a mode the record
     doesn't carry is the same fabricated-attribution gap E1 closes for
     models. One field, honest attribution.'

Landing:
  * `PERCEPTION_EXECUTION_MODE={cpu,gpu}` env var read at module-import time.
  * UNSET -> `ImportError` (explicit; no silent fallback).
  * Invalid value -> `ImportError`.
  * `SELECTED_BACKEND` sentinel exported for downstream workers.
  * `execution_mode` attribution in telemetry sidecar (see
    `services.perception.execution_mode_telemetry`).
"""
from __future__ import annotations

import os
from typing import Final

_ENV_VAR = "PERCEPTION_EXECUTION_MODE"
_VALID_MODES = frozenset({"cpu", "gpu"})

_raw = os.environ.get(_ENV_VAR)
if _raw is None:
    raise ImportError(
        f"{_ENV_VAR} unset — deployment must set explicitly; no silent "
        f"fallback. CI sets '{_ENV_VAR}=cpu'; GPU deployment sets "
        f"'{_ENV_VAR}=gpu'. Owner 9.2a-E2 α condition 1: 'a GPU deployment "
        f"quietly running CPU is the silent-swap risk in the other direction.'"
    )
if _raw not in _VALID_MODES:
    raise ImportError(
        f"{_ENV_VAR}={_raw!r} invalid; must be one of {sorted(_VALID_MODES)}."
    )

SELECTED_BACKEND: Final[str] = _raw
"""Sentinel: 'cpu' or 'gpu' — set at import time from env var. Immutable."""


def is_cpu_mode() -> bool:
    return SELECTED_BACKEND == "cpu"


def is_gpu_mode() -> bool:
    return SELECTED_BACKEND == "gpu"
