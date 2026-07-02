"""Layer A typed artefact dataclasses.

Deliberately dataclasses (not Pydantic). These are internal engine
types, not part of any frozen contract. The frozen contracts at G0
(Five Rings / Objective Request / Qualification Matrix) are the only
Pydantic-snapshot-locked schemas. Layer A/B/V1 types are free to
evolve until they stabilise.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class RawAudioArtifact:
    bytes_: bytes
    sample_rate: int
    channels: int
    duration_ms: int
    source_ref: str
    source_format: str  # e.g. "wav", "mp3"


@dataclass
class RawVideoArtifact:
    audio_track: Optional[RawAudioArtifact]
    keyframes: List[bytes]  # raw JPEG/PNG bytes; one per sampled keyframe
    duration_ms: int
    fps: float
    source_ref: str
    source_format: str  # e.g. "mp4"


@dataclass
class RawImageArtifact:
    bytes_: bytes
    width: int
    height: int
    format: str  # "png" / "jpeg" / …
    source_ref: str


@dataclass
class RawTextArtifact:
    text: str
    source_format: str  # "pdf" / "docx" / "txt" / …
    page_breaks: List[int] = field(default_factory=list)
    source_ref: str = ""


@dataclass
class TranscriptCue:
    t_start_ms: int
    t_end_ms: int
    text: str
    speaker: Optional[str] = None


@dataclass
class RawTranscriptArtifact:
    cues: List[TranscriptCue]
    speaker_labels: List[str]
    source_format: str  # "vtt" / "srt" / "json"
    source_ref: str = ""


RawArtifact = Union[
    RawAudioArtifact,
    RawVideoArtifact,
    RawImageArtifact,
    RawTextArtifact,
    RawTranscriptArtifact,
]
