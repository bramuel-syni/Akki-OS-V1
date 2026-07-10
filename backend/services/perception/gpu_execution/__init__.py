"""GPU execution package barrel (Owner 9.2a-E2 α · 2026-07-10).

Loads the CPU/GPU backend sentinel at import time. UNSET env var raises
`ImportError` per Owner condition 1.
"""
from .cuda_runtime import SELECTED_BACKEND, is_cpu_mode, is_gpu_mode

__all__ = ["SELECTED_BACKEND", "is_cpu_mode", "is_gpu_mode"]
