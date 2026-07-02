"""Layer A handler round-trips against the synthetic assets."""
from __future__ import annotations

import pytest

from services.data_source.synthetic_asset_gen import (
    AUDIO_DIR, IMAGE_DIR, TRANSCRIPT_DIR, write_png, write_vtt, write_wav,
)
from services.layer_a import retrieve, supported_extensions
from services.layer_a.types import (
    RawAudioArtifact, RawImageArtifact, RawTranscriptArtifact,
)


def _ensure_assets():
    # Force the synthetic fixture to materialise its bytes if not already.
    from services.data_source.synthetic import SyntheticPlumbingDataSource
    SyntheticPlumbingDataSource()


def test_supported_extensions_cover_all_modalities():
    sup = supported_extensions()
    for k in ("audio", "video", "image", "text", "transcript"):
        assert sup.get(k), f"missing {k}"


def test_audio_handler_roundtrip():
    _ensure_assets()
    wav = next(AUDIO_DIR.glob("*.wav"))
    art = retrieve(str(wav))
    assert isinstance(art, RawAudioArtifact)
    assert art.sample_rate == 16000
    assert art.duration_ms > 0
    assert art.source_format == "wav"


def test_image_handler_roundtrip():
    _ensure_assets()
    png = next(IMAGE_DIR.glob("*.png"))
    art = retrieve(str(png))
    assert isinstance(art, RawImageArtifact)
    assert art.width > 0 and art.height > 0
    assert art.format == "png"


def test_transcript_handler_roundtrip():
    _ensure_assets()
    vtt = next(TRANSCRIPT_DIR.glob("*.vtt"))
    art = retrieve(str(vtt))
    assert isinstance(art, RawTranscriptArtifact)
    assert art.cues, "no cues parsed from VTT"
    assert art.source_format == "vtt"


def test_unsupported_extension_raises():
    from services.layer_a import UnsupportedModality
    with pytest.raises(UnsupportedModality):
        retrieve("/tmp/nope.xyz")
