"""Model loader — lazy Whisper model loading with VRAM/memory management.

Loads the CI fixture model (whisper-tiny) via faster-whisper's CTranslate2
backend. Lazy singleton — one model instance per process, released on
worker shutdown. In GPU mode, delegates device='cuda' to CTranslate2's
runtime; in CPU mode, device='cpu' with int8 compute for footprint.
"""
from __future__ import annotations

from typing import Optional

from services.perception.gpu_execution.cuda_runtime import SELECTED_BACKEND
from services.perception.model_registry import attest_model

_model_cache: dict = {}


def get_asr_model(model_id: str = "whisper-tiny"):
    """Return cached faster-whisper WhisperModel for `model_id`.

    Attests the model against `models_registry.v0.json` before load. Raises
    ValueError if model_id is not registered (per 9.2a-E1 α runtime enforce).
    """
    attest_model(model_id)
    cached = _model_cache.get(model_id)
    if cached is not None:
        return cached
    from faster_whisper import WhisperModel

    if SELECTED_BACKEND == "cpu":
        model = WhisperModel(_hf_model_name(model_id), device="cpu", compute_type="int8")
    else:
        model = WhisperModel(_hf_model_name(model_id), device="cuda", compute_type="float16")
    _model_cache[model_id] = model
    return model


def _hf_model_name(model_id: str) -> str:
    """Map registry model_id -> faster-whisper HF hub name."""
    return {"whisper-tiny": "tiny"}.get(model_id, model_id)


def release_all_models() -> None:
    """Release cached models. Called at worker shutdown for VRAM cleanup."""
    _model_cache.clear()
