"""Layer A audio handler.

Retrieves raw bytes + metadata for `.wav / .mp3 / .m4a / .flac / .ogg`.
Uses `pydub` (which shells out to ffmpeg) for metadata extraction. Pure
WAV via stdlib `wave` works as a fallback when pydub isn't installed.

Cousin: no direct cousin for audio (the cousin is text/image only).
Dispatch-shape kinship: `documents_service.py::extract_text`.
"""
from __future__ import annotations

import wave
from pathlib import Path

from services.layer_a.types import RawAudioArtifact


def retrieve(source_ref: str) -> RawAudioArtifact:
    path = Path(source_ref)
    raw = path.read_bytes()
    ext = path.suffix.lower().lstrip(".")

    # Fast-path for WAV (stdlib only, no pydub/ffmpeg required).
    if ext == "wav":
        with wave.open(str(path), "rb") as wf:
            channels = wf.getnchannels()
            sample_rate = wf.getframerate()
            n_frames = wf.getnframes()
            duration_ms = int(n_frames * 1000 / sample_rate)
        return RawAudioArtifact(
            bytes_=raw,
            sample_rate=sample_rate,
            channels=channels,
            duration_ms=duration_ms,
            source_ref=source_ref,
            source_format=ext,
        )

    # Other formats — use pydub if available.
    try:
        from pydub import AudioSegment
        seg = AudioSegment.from_file(str(path))
        return RawAudioArtifact(
            bytes_=raw,
            sample_rate=seg.frame_rate,
            channels=seg.channels,
            duration_ms=len(seg),
            source_ref=source_ref,
            source_format=ext,
        )
    except ImportError as e:
        raise RuntimeError(
            f"audio handler requires pydub for {ext!r} files (install pydub + ffmpeg)"
        ) from e
