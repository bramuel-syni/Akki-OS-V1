"""Layer C aggregator emits NormalizedUnits that round-trip through Five Rings."""
from __future__ import annotations

import json

from contracts.five_rings import DefensibilityClass, Modality, NormalizedUnit
from services.layer_b.contracts import (
    AsrCue, AsrPerception, DiarizationPerception, DiarizationTurn,
    VisionEntity, VisionPerception,
)
from services.layer_c.aggregator import from_asr, from_vision, merge_diarization


def _asr_perception() -> AsrPerception:
    return AsrPerception(
        cues=[
            AsrCue(t_start_ms=0, t_end_ms=2500, text="good morning", confidence=0.8),
            AsrCue(t_start_ms=2500, t_end_ms=5000, text="habari za asubuhi", confidence=0.75),
        ],
        language_hint="en",
        model_id="test-asr", model_version="1.0",
        extraction_params={
            "provider_id": "test-asr",
            "provider_version": "1.0",
            "extraction_run_id": "layer-c-test-asr",
            "extracted_at": "2026-07-01T00:00:00Z",
            "sample_rate_hz": 16000,
            "chunk_ms": 1000,
            "model_decoding_params": {
                "language_hint": "en", "beam_size": 1,
                "temperature": 0, "vad_threshold": 0.5,
            },
        },
    )


def _vision_perception() -> VisionPerception:
    return VisionPerception(
        entities=[VisionEntity(label="KBC LOGO", confidence=0.9)],
        on_screen_text="KBC NEWS",
        scene_description="News broadcast graphic",
        model_id="test-vision", model_version="1.0",
        extraction_params={
            "provider_id": "test-vision",
            "provider_version": "1.0",
            "extraction_run_id": "layer-c-test-vision",
            "extracted_at": "2026-07-01T00:00:00Z",
            "target_resolution": [1280, 720],
            "vision_decoding_params": {
                "prompt_template_id": "rms.image.default.v0",
                "max_tokens": 128, "temperature": 0,
            },
        },
    )


def test_from_asr_emits_one_unit_per_cue_and_roundtrips():
    units = from_asr(
        perception=_asr_perception(), source_ref="local://test.wav",
        speaker="Anchor A", context="layer_c test",
        genre="news_anchor_read", source_standing="primary_recorded",
    )
    assert len(units) == 2
    for u in units:
        assert u.provenance.modality == Modality.AUDIO
        assert u.defensibility.defensibility_class == DefensibilityClass.FACT
        assert u.defensibility.runtime_mode == "declaration_baseline"
        # Round-trip
        d = u.model_dump(mode="json")
        assert NormalizedUnit.model_validate(d).model_dump(mode="json") == d


def test_from_vision_emits_unit_with_image_modality():
    u = from_vision(
        perception=_vision_perception(), source_ref="local://test.png",
        context="vision test",
        genre="news_anchor_read", source_standing="primary_recorded",
    )
    assert u.provenance.modality == Modality.IMAGE
    assert u.defensibility.runtime_mode == "declaration_baseline"
    d = u.model_dump(mode="json")
    assert NormalizedUnit.model_validate(d).model_dump(mode="json") == d


def test_merge_diarization_attaches_speaker_by_overlap():
    units = from_asr(
        perception=_asr_perception(), source_ref="local://test.wav",
        speaker=None, context="diarization test",
        genre="news_anchor_read", source_standing="primary_recorded",
    )
    dia = DiarizationPerception(
        turns=[
            DiarizationTurn(speaker="SPK_00", t_start_ms=0, t_end_ms=2500),
            DiarizationTurn(speaker="SPK_01", t_start_ms=2500, t_end_ms=5000),
        ],
        model_id="test-dia", model_version="1.0", extraction_params={},
    )
    merged = merge_diarization(units, dia)
    assert merged[0].provenance.speaker_or_author == "SPK_00"
    assert merged[1].provenance.speaker_or_author == "SPK_01"
