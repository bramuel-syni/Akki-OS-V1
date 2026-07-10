"""Audio batching — chunk raw audio bytes into GPU-friendly batches.

Reads audio via faster-whisper's underlying decode path (via PyAV). Yields
audio waveform arrays for downstream transcription. In CPU-mode a single
chunk is passed through; in GPU-mode multiple chunks may be batched
depending on model + VRAM budget.
"""
from __future__ import annotations

from typing import Iterator

from services.perception.gpu_execution.cuda_runtime import SELECTED_BACKEND

# Default chunk size aligned with faster-whisper's internal chunk_length_s=30
# for tiny/base models; smaller for CI to keep test time low.
_CI_CHUNK_MS = 30_000  # 30 s (whisper native)
_CPU_MAX_BATCH = 1
_GPU_MAX_BATCH = 8


def target_max_batch() -> int:
    return _CPU_MAX_BATCH if SELECTED_BACKEND == "cpu" else _GPU_MAX_BATCH


def iter_audio_chunks(audio_bytes_or_path) -> Iterator:
    """Yield (chunk_index, waveform_or_path) pairs.

    For 9.2a fixture-mode: single chunk pass-through — faster-whisper's
    internal chunking handles longer audio. This function is a seam for
    9.2b GPU-mode batching.
    """
    yield 0, audio_bytes_or_path
