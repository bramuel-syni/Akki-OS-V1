"""extraction_params@v0 validator + V1 harness compare_runs behaviour
   (Pre-G2 hardening, 2026-07-01).
"""
from __future__ import annotations

import pytest

from contracts.extraction_params import (
    ExtractionParamsViolation,
    is_deterministically_reproducible,
    mandatory_keys,
    reproducibility_keys,
    validate_extraction_params,
)
from contracts.five_rings import (
    DefensibilityClass, DefensibilityRing, Modality, NormalizedUnit,
    ProvenanceRing, ReextractionHandleRing, ScoreVector,
)
from services.v1_harness import compare_runs


# ---------------------------------------------------------------------------
# Fixtures — compliant per-modality blocks.
# ---------------------------------------------------------------------------
_BASE = {
    "provider_id": "p", "provider_version": "1.0",
    "extraction_run_id": "r1", "extracted_at": "2026-07-01T00:00:00Z",
}


def _audio(temp: float = 0) -> dict:
    return {
        **_BASE,
        "sample_rate_hz": 16000, "chunk_ms": 1000,
        "model_decoding_params": {
            "language_hint": "en", "beam_size": 1,
            "temperature": temp, "vad_threshold": 0.5,
        },
    }


def _image(temp: float = 0) -> dict:
    return {
        **_BASE,
        "target_resolution": [1024, 768],
        "vision_decoding_params": {
            "prompt_template_id": "rms.image.v0",
            "max_tokens": 128, "temperature": temp,
        },
    }


def _text() -> dict:
    return {**_BASE, "source_format": "txt", "max_chars": 50000, "encoding": "utf-8"}


def _video(temp: float = 0, strategy: str = "every_n_seconds") -> dict:
    block = {
        **_BASE,
        "keyframe_strategy": strategy,
        "vision_decoding_params": {
            "prompt_template_id": "rms.video.v0",
            "max_tokens": 256, "temperature": temp,
        },
    }
    if strategy == "every_n_seconds":
        block["keyframe_interval_ms"] = 1000
    elif strategy == "uniform_n":
        block["keyframe_count"] = 12
    return block


# ---------------------------------------------------------------------------
# Validator — positive + negative cases.
# ---------------------------------------------------------------------------
def test_extraction_params_validator_modality_match_audio_ok():
    validate_extraction_params("audio", _audio())


def test_extraction_params_validator_modality_match_image_ok():
    validate_extraction_params("image", _image())


def test_extraction_params_validator_modality_match_text_ok():
    validate_extraction_params("text", _text())


def test_extraction_params_validator_modality_match_video_ok():
    validate_extraction_params("video", _video())
    validate_extraction_params("video", _video(strategy="uniform_n"))
    validate_extraction_params("video", _video(strategy="scene_change"))


def test_validator_rejects_missing_modality_mandatory_key_audio():
    p = _audio()
    del p["chunk_ms"]
    with pytest.raises(ExtractionParamsViolation):
        validate_extraction_params("audio", p)


def test_validator_rejects_missing_base_key():
    p = _audio()
    del p["provider_id"]
    with pytest.raises(ExtractionParamsViolation):
        validate_extraction_params("audio", p)


def test_validator_rejects_unknown_top_level_key():
    p = _audio()
    p["beam_size"] = 5  # belongs inside model_decoding_params, not top-level
    with pytest.raises(ExtractionParamsViolation):
        validate_extraction_params("audio", p)


def test_validator_rejects_video_when_strategy_keys_inconsistent():
    p = _video(strategy="every_n_seconds")
    del p["keyframe_interval_ms"]
    with pytest.raises(ExtractionParamsViolation):
        validate_extraction_params("video", p)


def test_extraction_params_validator_extras_passthrough():
    p = _audio()
    p["provider_extras"] = {
        "condition_on_previous_text": True,  # whisper-specific exotica
        "weird_provider_flag": [1, 2, 3],
    }
    validate_extraction_params("audio", p)  # must NOT raise


# ---------------------------------------------------------------------------
# Reproducibility helpers.
# ---------------------------------------------------------------------------
def test_mandatory_keys_includes_base_and_modality():
    keys = mandatory_keys("audio")
    assert {"provider_id", "provider_version", "extraction_run_id",
            "extracted_at", "sample_rate_hz", "chunk_ms",
            "model_decoding_params"}.issubset(keys)


def test_is_deterministically_reproducible_temperature_zero():
    ok, fail = is_deterministically_reproducible(_audio(temp=0))
    assert ok is True and fail == []
    ok, fail = is_deterministically_reproducible(_audio(temp=0.7))
    assert ok is False
    assert any("model_decoding_params.temperature" in k for k in fail), fail


def test_is_deterministically_reproducible_image_temperature():
    ok, fail = is_deterministically_reproducible(_image(temp=0.5))
    assert ok is False
    assert any("vision_decoding_params.temperature" in k for k in fail), fail


# ---------------------------------------------------------------------------
# V1 harness compare_runs() — Pre-G2 hardening.
# ---------------------------------------------------------------------------
def test_compare_runs_refuses_when_non_reproducible_by_construction():
    a = _audio(temp=0.7)
    b = _audio(temp=0)
    rpt = compare_runs(modality="audio", params_a=a, params_b=b)
    assert rpt["non_reproducible_by_construction"] is True
    assert "model_decoding_params.temperature" in rpt["failing_temperature_keys"]
    # Crucially: the harness REFUSES the comparison rather than reporting "outputs differ → bug".
    assert rpt["subset_equal"] is None


def test_compare_runs_uses_reproducibility_keys_not_full_mandatory():
    """Two runs identical except for `extracted_at` must NOT differ on
    the reproducibility-anchor subset (stakeholder correction #1)."""
    a = _audio()
    b = _audio()
    b["extracted_at"] = "2099-12-31T23:59:59Z"
    rpt = compare_runs(modality="audio", params_a=a, params_b=b)
    assert rpt["non_reproducible_by_construction"] is False
    assert rpt["subset_equal"] is True, rpt
    assert "extracted_at" not in rpt["reproducibility_keys_used"]


def test_compare_runs_detects_anchor_drift():
    a = _audio()
    b = _audio()
    b["sample_rate_hz"] = 48000  # anchor key drift
    rpt = compare_runs(modality="audio", params_a=a, params_b=b)
    assert rpt["non_reproducible_by_construction"] is False
    assert rpt["subset_equal"] is False


# ---------------------------------------------------------------------------
# NormalizedUnit model_validator wiring.
# ---------------------------------------------------------------------------
def _bare_unit(modality: Modality, params: dict) -> NormalizedUnit:
    return NormalizedUnit(
        unit_id="00000000-0000-0000-0000-aaaaaaaaaaaa",
        provenance=ProvenanceRing(source_ref="x", modality=modality),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer="local://x", model_id="m", model_version="0.0",
            extraction_params=params,
        ),
        defensibility=DefensibilityRing(
            defensibility_class=DefensibilityClass.UTTERANCE,
            score_vector=ScoreVector(),
            matrix_rule_ref="dummy@v0",
        ),
    )


def test_normalized_unit_validator_accepts_compliant_audio():
    _bare_unit(Modality.AUDIO, _audio())


def test_normalized_unit_validator_rejects_incomplete_audio():
    bad = _audio()
    del bad["chunk_ms"]
    with pytest.raises(Exception):  # Pydantic wraps ExtractionParamsViolation
        _bare_unit(Modality.AUDIO, bad)
