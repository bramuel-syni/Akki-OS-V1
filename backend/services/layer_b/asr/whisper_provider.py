"""ASR provider — OpenAI-Whisper-API path (via Shield perception_router).

First of the two architecturally-different ASR providers. Path:
remote API, cloud-provider Whisper class, network call brokered
through Shield's perception_router so audio bytes don't escape the
Inner Gate.

The perception_router resolves the actual outbound SDK at call time.
If `emergentintegrations` doesn't expose a whisper ASR seam yet, the
provider's constructor still succeeds; `transcribe()` raises
ProviderUnavailable with an actionable message.
"""
from __future__ import annotations

from typing import Any

from services.layer_a.types import RawAudioArtifact
from services.layer_b.contracts import (
    AsrCue,
    AsrPerception,
    AsrProvider,
    ProviderUnavailable,
)
from services.synisense.shield import perception_router


class WhisperApiProvider:
    name = "whisper"
    model_id = "whisper-1"
    model_version = "openai-cloud"

    def __init__(self) -> None:
        # Construction must not network or download. Capability check
        # lives in `transcribe()` so the factory can probe availability
        # without a real call.
        self._params: dict[str, Any] = {"language_hint": "en"}

    def transcribe(self, audio: RawAudioArtifact) -> AsrPerception:
        result = perception_router.transcribe(
            audio=audio,
            purpose="akki.layer_b.asr",
            model_preference="whisper-cloud",
            model_id=self.model_id,
            model_version=self.model_version,
            extraction_params=self._params,
        )
        # perception_router returns a dict; we wrap into the typed contract.
        cues = [AsrCue(**c) for c in result.get("cues", [])]
        return AsrPerception(
            cues=cues,
            language_hint=result.get("language_hint"),
            model_id=self.model_id,
            model_version=self.model_version,
            extraction_params=self._params,
            synthetic_plumbing_only=result.get("synthetic_plumbing_only", False),
        )
