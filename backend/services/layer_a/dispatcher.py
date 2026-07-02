"""Layer A dispatcher — modality-aware fetch entrypoint.

Cousin: `/reference/akki-legacy/backend/documents_service.py::extract_text`
and its `ACCEPT_EXT` dispatch dict. Same shape, extended to audio /
video / transcript.

This module does NOT perceive. It opens the file at `source_ref`, reads
bytes, and emits the typed Raw artefact. Perception is Layer B.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict

from services.layer_a import handlers
from services.layer_a.types import RawArtifact


class Layer_A_DispatchError(Exception):
    pass


class UnsupportedModality(Layer_A_DispatchError):
    pass


# Cousin ACCEPT_EXT mirrors `documents_service.py::ACCEPT_EXT`.
_AUDIO = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}
_VIDEO = {".mp4", ".mov", ".mkv", ".webm"}
_IMAGE = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
_TEXT = {".pdf", ".docx", ".pptx", ".txt", ".md", ".rtf", ".csv", ".xlsx"}
_TRANSCRIPT = {".vtt", ".srt", ".json"}


def supported_extensions() -> Dict[str, set]:
    return {
        "audio": set(_AUDIO),
        "video": set(_VIDEO),
        "image": set(_IMAGE),
        "text": set(_TEXT),
        "transcript": set(_TRANSCRIPT),
    }


def retrieve(source_ref: str) -> RawArtifact:
    """Branch on extension; delegate to the per-modality handler.

    `source_ref` is treated as a filesystem path. URL-style refs (e.g.
    `s3://...`) will be supported at G2 when the storage substrate is
    wired into the dispatcher. At G0.5 we work off local files (the
    synthetic fixture writes its own bytes under `synthetic_assets/`).
    """
    ext = Path(source_ref).suffix.lower()
    handler: Callable[[str], RawArtifact]
    if ext in _AUDIO:
        handler = handlers.audio.retrieve
    elif ext in _VIDEO:
        handler = handlers.video.retrieve
    elif ext in _IMAGE:
        handler = handlers.image.retrieve
    elif ext in _TEXT:
        handler = handlers.text.retrieve
    elif ext in _TRANSCRIPT:
        handler = handlers.transcript.retrieve
    else:
        raise UnsupportedModality(
            f"no Layer A handler for extension {ext!r} (source_ref={source_ref!r})"
        )
    return handler(source_ref)
