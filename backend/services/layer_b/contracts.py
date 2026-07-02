"""Layer B provider contracts — Protocols + artefact dataclasses.

Dataclasses (not Pydantic) deliberately: these are internal engine
types. Frozen contracts at G0 (Five Rings / Objective Request /
Qualification Matrix) stay the only snapshot-locked schemas.

Contract-authoring discipline (Build Kickoff): no spec ambiguity here—
providers carry their own model fingerprint (`model_id`, `model_version`,
`extraction_params`) which feeds Layer C into the Re-extraction Handle
ring at populate time. The Re-extraction Handle ring is fully
unambiguous per Spec §5.5, so we are not freezing anything net-new.

No cousin — net-new contracts. The discipline of "factory-keyed-on-env"
is cousin-shaped (cousin uses env-driven model preference inside
`/reference/akki-legacy/backend/services/synisense/shield/llm_router.py`).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

from services.layer_a.types import (
    RawAudioArtifact,
    RawImageArtifact,
)


class ProviderUnavailable(Exception):
    """Raised on construction when a provider's heavy dep is not installed."""


@dataclass
class AsrCue:
    t_start_ms: int
    t_end_ms: int
    text: str
    confidence: Optional[float] = None


@dataclass
class AsrPerception:
    cues: List[AsrCue]
    language_hint: Optional[str] = None
    model_id: str = ""
    model_version: str = ""
    extraction_params: Dict[str, Any] = field(default_factory=dict)
    synthetic_plumbing_only: bool = False


@dataclass
class DiarizationTurn:
    speaker: str
    t_start_ms: int
    t_end_ms: int


@dataclass
class DiarizationPerception:
    turns: List[DiarizationTurn]
    model_id: str = ""
    model_version: str = ""
    extraction_params: Dict[str, Any] = field(default_factory=dict)
    synthetic_plumbing_only: bool = False


@dataclass
class VisionEntity:
    label: str
    confidence: float
    bbox: Optional[List[int]] = None  # [x, y, w, h]


@dataclass
class VisionPerception:
    entities: List[VisionEntity]
    on_screen_text: str
    scene_description: str
    model_id: str = ""
    model_version: str = ""
    extraction_params: Dict[str, Any] = field(default_factory=dict)
    synthetic_plumbing_only: bool = False


PerceptionArtifact = AsrPerception | DiarizationPerception | VisionPerception


@runtime_checkable
class AsrProvider(Protocol):
    name: str
    model_id: str
    model_version: str

    def transcribe(self, audio: RawAudioArtifact) -> AsrPerception: ...


@runtime_checkable
class DiarizationProvider(Protocol):
    name: str
    model_id: str
    model_version: str

    def diarize(self, audio: RawAudioArtifact) -> DiarizationPerception: ...


@runtime_checkable
class VisionProvider(Protocol):
    name: str
    model_id: str
    model_version: str

    def perceive(self, image: RawImageArtifact, *, prompt: str) -> VisionPerception: ...
