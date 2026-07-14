"""Diarization provider — pyannote.audio local pipeline.

Construction-time check: pyannote.audio + HuggingFace token are both
required before a real `diarize()` call. Construction without the
library raises ProviderUnavailable. Construction with the library but
without `HUGGINGFACE_HUB_TOKEN` set still succeeds; the token gate is
enforced at `diarize()` time (so the provider is listed but flagged
un-runnable).
"""
from __future__ import annotations

import os
from typing import Any

from services.layer_a.types import RawAudioArtifact
from services.layer_b.contracts import (
    DiarizationPerception,
    DiarizationTurn,
    ProviderUnavailable,
)


class PyannoteProvider:
    name = "pyannote"
    model_id = "pyannote/speaker-diarization-3.1"
    model_version = "pyannote-audio"

    def __init__(self) -> None:
        try:
            from pyannote.audio import Pipeline  # noqa: F401
        except ImportError as e:
            raise ProviderUnavailable(
                "pyannote.audio not installed. "
                "Install with `pip install pyannote.audio` and set HUGGINGFACE_HUB_TOKEN."
            ) from e
        self._params: dict[str, Any] = {
            "min_speakers": int(os.environ.get("AKKI_DIA_MIN_SPEAKERS", "1")),
            "max_speakers": int(os.environ.get("AKKI_DIA_MAX_SPEAKERS", "8")),
        }
        self._pipeline = None

    def _ensure_pipeline(self):
        if self._pipeline is None:
            from pyannote.audio import Pipeline
            token = os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
            if not token:
                raise ProviderUnavailable(
                    "pyannote.audio requires HUGGINGFACE_HUB_TOKEN to download the diarization model."
                )
            self._pipeline = Pipeline.from_pretrained(self.model_id, use_auth_token=token)
        return self._pipeline

    def diarize(self, audio: RawAudioArtifact) -> DiarizationPerception:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=f".{audio.source_format}", delete=False) as tmp:
            tmp.write(audio.bytes_)
            tmp_path = tmp.name
        try:
            pipeline = self._ensure_pipeline()
            diar = pipeline(tmp_path, **self._params)
            turns = [
                DiarizationTurn(
                    speaker=str(spk),
                    t_start_ms=int(seg.start * 1000),
                    t_end_ms=int(seg.end * 1000),
                )
                for seg, _, spk in diar.itertracks(yield_label=True)
            ]
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        return DiarizationPerception(
            turns=turns,
            model_id=self.model_id,
            model_version=self.model_version,
            extraction_params=self._params,
            synthetic_plumbing_only=False,
        )
