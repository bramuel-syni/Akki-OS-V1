"""Vision-LM provider — frame perception via Shield perception_router.

A vision-capable LLM (Claude vision via emergentintegrations,
routed through Shield's perception_router so image bytes do not leak
past the Inner Gate). Inputs: keyframe bytes + perception prompt;
outputs: entities + on-screen text (OCR fallback) + scene description.

Cousin: emergentintegrations is the universal LLM SDK already used by
`/reference/akki-legacy/backend/services/synisense/shield/llm_router.py`.
The vision call shape is a *new modality* over the same SDK.
"""
from __future__ import annotations

from typing import Any

from services.layer_a.types import RawImageArtifact
from services.layer_b.contracts import (
    ProviderUnavailable,
    VisionEntity,
    VisionPerception,
)
from services.synisense.shield import perception_router


class EmergentVisionProvider:
    name = "emergent_vision"
    model_id = "claude-vision"
    model_version = "emergent-universal-key"

    def __init__(self) -> None:
        self._params: dict[str, Any] = {"max_tokens": 512}

    def perceive(self, image: RawImageArtifact, *, prompt: str) -> VisionPerception:
        result = perception_router.perceive_image(
            image=image,
            prompt=prompt,
            purpose="akki.layer_b.vision",
            model_id=self.model_id,
            model_version=self.model_version,
            extraction_params=self._params,
        )
        entities = [VisionEntity(**e) for e in result.get("entities", [])]
        return VisionPerception(
            entities=entities,
            on_screen_text=result.get("on_screen_text", ""),
            scene_description=result.get("scene_description", ""),
            model_id=self.model_id,
            model_version=self.model_version,
            extraction_params=self._params,
            synthetic_plumbing_only=result.get("synthetic_plumbing_only", False),
        )
