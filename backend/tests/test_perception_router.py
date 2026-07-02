"""Shield perception_router — stub paths emit verifiable trust receipts."""
from __future__ import annotations

from services.layer_a.types import RawAudioArtifact, RawImageArtifact
from services.synisense.shield import perception_router, trust_receipt


def test_transcribe_stub_emits_verifiable_receipt():
    audio = RawAudioArtifact(
        bytes_=b"\x00" * 1600, sample_rate=16000, channels=1,
        duration_ms=100, source_ref="test.wav", source_format="wav",
    )
    r = perception_router.transcribe(
        audio=audio, purpose="akki.layer_b.asr", model_preference="whisper-cloud",
        model_id="whisper-1", model_version="openai-cloud", extraction_params={},
    )
    assert r["synthetic_plumbing_only"] is True
    assert trust_receipt.verify(r["trust_receipt"], tenant_id="rms") is True


def test_perceive_image_stub_emits_verifiable_receipt():
    image = RawImageArtifact(
        bytes_=b"\x89PNG\r\n" + b"\x00" * 200, width=10, height=10,
        format="png", source_ref="test.png",
    )
    r = perception_router.perceive_image(
        image=image, prompt="describe", purpose="akki.layer_b.vision",
        model_id="claude-vision", model_version="emergent", extraction_params={},
    )
    assert r["synthetic_plumbing_only"] is True
    assert trust_receipt.verify(r["trust_receipt"], tenant_id="rms") is True
