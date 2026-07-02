"""Compliant `extraction_params@v0` fixtures per modality.

Frozen contract: `contracts/extraction_params.py`. Used across G3 invariant
tests to construct `NormalizedUnit`s that satisfy the Re-extraction Handle
validator. `temperature=0` everywhere for deterministic-reproducibility.
"""
from typing import Any, Dict

from contracts.five_rings import Modality

_BASE = {
    "provider_id": "test",
    "provider_version": "0.0",
    "extraction_run_id": "g3-test",
    "extracted_at": "2026-07-01T00:00:00Z",
}


def ep_v0(modality: Modality) -> Dict[str, Any]:
    """Return a compliant extraction_params dict for the given modality."""
    if modality is Modality.TEXT:
        return {
            **_BASE,
            "encoding": "utf-8",
            "max_chars": 1000,
            "source_format": "txt",
        }
    if modality is Modality.AUDIO:
        return {
            **_BASE,
            "sample_rate_hz": 16000,
            "chunk_ms": 1000,
            "model_decoding_params": {
                "language_hint": "en",
                "beam_size": 1,
                "temperature": 0,
                "vad_threshold": 0.5,
            },
        }
    if modality is Modality.VIDEO:
        return {
            **_BASE,
            "keyframe_strategy": "scene_change",
            "vision_decoding_params": {
                "prompt_template_id": "v1",
                "max_tokens": 100,
                "temperature": 0,
            },
        }
    if modality is Modality.IMAGE:
        return {
            **_BASE,
            "target_resolution": (1024, 768),
            "vision_decoding_params": {
                "prompt_template_id": "v1",
                "max_tokens": 100,
                "temperature": 0,
            },
        }
    if modality is Modality.COMPOSITE:
        return {
            **_BASE,
            "aggregation_strategy": "union",
            "source_artifact_refs": ["ref-1"],
        }
    raise ValueError(f"unknown modality {modality!r}")
