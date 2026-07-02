"""Layer B provider sanity — contracts implemented; factory honest."""
from __future__ import annotations

import pytest

from services.layer_b.contracts import (
    AsrProvider, DiarizationProvider, VisionProvider, ProviderUnavailable,
)
from services.layer_b.factory import (
    available_providers, get_asr_provider, get_diarization_provider,
    get_vision_provider, list_provider_names,
)


def test_factory_lists_two_asr_one_diarization_one_vision():
    names = list_provider_names()
    assert len(names["asr"]) >= 2, names["asr"]
    assert "whisper" in names["asr"]
    assert "faster_whisper" in names["asr"]
    assert "pyannote" in names["diarization"]
    assert "emergent_vision" in names["vision"]


def test_whisper_provider_constructs_and_satisfies_protocol():
    p = get_asr_provider("whisper")
    assert isinstance(p, AsrProvider)
    assert p.name == "whisper"
    assert p.model_id
    assert p.model_version


def test_vision_provider_constructs_and_satisfies_protocol():
    p = get_vision_provider("emergent_vision")
    assert isinstance(p, VisionProvider)


def test_faster_whisper_or_pyannote_may_be_unavailable_but_factory_is_honest():
    """Heavy deps not installed at G0.5; factory must report False, not crash."""
    av = available_providers()
    assert "asr" in av and "diarization" in av and "vision" in av
    # whisper + emergent_vision construct without heavy deps
    assert av["asr"].get("whisper") is True
    assert av["vision"].get("emergent_vision") is True
    # faster_whisper / pyannote may be either way — the map must contain the key.
    assert "faster_whisper" in av["asr"]
    assert "pyannote" in av["diarization"]


def test_unknown_provider_raises_value_error():
    with pytest.raises(ValueError):
        get_asr_provider("does-not-exist")
