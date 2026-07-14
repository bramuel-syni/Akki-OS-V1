"""Layer B provider factory — env-driven selection.

Factory pattern: pick the right provider class by env var, surface
graceful unavailability if its heavy dep isn't installed. Mirrors the
cousin's env-driven LLM model preference in `shield/llm_router.py`.

Env knobs (G0.5):
  * `AKKI_ASR_PROVIDER`           default: "whisper"
  * `AKKI_DIARIZATION_PROVIDER`   default: "pyannote"
  * `AKKI_VISION_PROVIDER`        default: "emergent_vision"
"""
from __future__ import annotations

import os
from typing import Dict, List, Type

from services.layer_b.contracts import (
    AsrProvider,
    DiarizationProvider,
    ProviderUnavailable,
    VisionProvider,
)


_ASR_REGISTRY: Dict[str, str] = {
    # name -> import path of the class
    "whisper":         "services.layer_b.asr.whisper_provider:WhisperApiProvider",
    "faster_whisper":  "services.layer_b.asr.faster_whisper_provider:FasterWhisperProvider",
}
_DIARIZATION_REGISTRY: Dict[str, str] = {
    "pyannote": "services.layer_b.diarization.pyannote_provider:PyannoteProvider",
}
_VISION_REGISTRY: Dict[str, str] = {
    "emergent_vision": "services.layer_b.vision.frame_perception_provider:EmergentVisionProvider",
}


def _resolve(path: str) -> Type:
    mod_path, _, cls_name = path.partition(":")
    import importlib
    mod = importlib.import_module(mod_path)
    return getattr(mod, cls_name)


def get_asr_provider(name: str | None = None) -> AsrProvider:
    name = (name or os.environ.get("AKKI_ASR_PROVIDER", "whisper")).lower()
    if name not in _ASR_REGISTRY:
        raise ValueError(f"unknown ASR provider {name!r}; available: {list(_ASR_REGISTRY)}")
    return _resolve(_ASR_REGISTRY[name])()


def get_diarization_provider(name: str | None = None) -> DiarizationProvider:
    name = (name or os.environ.get("AKKI_DIARIZATION_PROVIDER", "pyannote")).lower()
    if name not in _DIARIZATION_REGISTRY:
        raise ValueError(f"unknown diarization provider {name!r}")
    return _resolve(_DIARIZATION_REGISTRY[name])()


def get_vision_provider(name: str | None = None) -> VisionProvider:
    name = (name or os.environ.get("AKKI_VISION_PROVIDER", "emergent_vision")).lower()
    if name not in _VISION_REGISTRY:
        raise ValueError(f"unknown vision provider {name!r}")
    return _resolve(_VISION_REGISTRY[name])()


def available_providers() -> Dict[str, Dict[str, bool]]:
    """Returns availability map for /api/system/state.

    A provider is "available" iff its class can be constructed without
    raising ProviderUnavailable. This lets the system surface honestly
    flag which providers are wired but un-installed.
    """
    out: Dict[str, Dict[str, bool]] = {"asr": {}, "diarization": {}, "vision": {}}
    for kind, registry, getter in (
        ("asr", _ASR_REGISTRY, get_asr_provider),
        ("diarization", _DIARIZATION_REGISTRY, get_diarization_provider),
        ("vision", _VISION_REGISTRY, get_vision_provider),
    ):
        for name in registry:
            try:
                getter(name)
                out[kind][name] = True
            except (ProviderUnavailable, Exception):
                out[kind][name] = False
    return out


def list_provider_names() -> Dict[str, List[str]]:
    return {
        "asr": list(_ASR_REGISTRY),
        "diarization": list(_DIARIZATION_REGISTRY),
        "vision": list(_VISION_REGISTRY),
    }
