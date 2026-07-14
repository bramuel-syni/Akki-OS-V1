"""ASR provider — faster-whisper local (CTranslate2 inference).

Second of the two architecturally-different ASR providers (Deliverable 3,
bake-off rationale in BUILD_JOURNAL.md):
  * Different VENDOR        — SYSTRAN's CTranslate2 vs OpenAI's API.
  * Different INFERENCE PATH — local CPU/GPU vs remote network call.
  * Different FAILURE MODE   — fails on missing local model file vs
                                fails on network / quota.
  * Different LICENCE        — MIT (faster-whisper) vs vendor terms.

WHY NOT Deepgram / AssemblyAI: same family of remote API (different vendor
but same architectural shape) — falsifies less. The bake-off should
falsify "the approach is wrong" vs "the model is wrong"; that requires
architectural difference, which local-vs-cloud delivers cleanly.

Construction does not download the model — it is downloaded lazily on
first transcribe(). Until real Hour A arrives, the provider runs against
the synthetic TTS audio with `synthetic_plumbing_only=True` set on the
result.
"""
from __future__ import annotations

import os
from typing import Any

from services.layer_a.types import RawAudioArtifact
from services.layer_b.contracts import (
    AsrCue,
    AsrPerception,
    ProviderUnavailable,
)

_MODEL_SIZE = os.environ.get("AKKI_FASTER_WHISPER_MODEL", "tiny")


class FasterWhisperProvider:
    name = "faster_whisper"
    model_id = f"faster-whisper:{_MODEL_SIZE}"
    model_version = "ctranslate2"

    def __init__(self) -> None:
        try:
            from faster_whisper import WhisperModel  # noqa: F401
        except ImportError as e:
            raise ProviderUnavailable(
                "faster-whisper not installed. "
                "Install with `pip install faster-whisper` (CTranslate2 backend)."
            ) from e
        self._params: dict[str, Any] = {
            "model_size": _MODEL_SIZE, "compute_type": "int8", "beam_size": 1,
        }
        self._model = None  # lazy

    def _ensure_model(self):
        if self._model is None:
            from faster_whisper import WhisperModel
            self._model = WhisperModel(_MODEL_SIZE, compute_type="int8")
        return self._model

    def transcribe(self, audio: RawAudioArtifact) -> AsrPerception:
        # Write bytes to a tempfile (faster-whisper consumes a path).
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=f".{audio.source_format}", delete=False) as tmp:
            tmp.write(audio.bytes_)
            tmp_path = tmp.name
        try:
            model = self._ensure_model()
            segments, info = model.transcribe(tmp_path, beam_size=1)
            cues = [
                AsrCue(
                    t_start_ms=int(s.start * 1000),
                    t_end_ms=int(s.end * 1000),
                    text=s.text.strip(),
                    confidence=getattr(s, "avg_logprob", None),
                )
                for s in segments
            ]
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        return AsrPerception(
            cues=cues,
            language_hint=info.language if hasattr(info, "language") else None,
            model_id=self.model_id,
            model_version=self.model_version,
            extraction_params=self._params,
            synthetic_plumbing_only=False,  # provider doesn't know; caller stamps
        )
