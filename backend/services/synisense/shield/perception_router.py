"""Shield perception_router — extends Shield to ASR / vision modalities.

Mirrors `services/synisense/shield/llm_router.py` (cousin path:
`/reference/akki-legacy/backend/services/synisense/shield/llm_router.py`).
Same discipline: single seam, de-id-aware, audit-logged, trust-receipt
stamped.

RULE 2 BUDGET WATCH (~200 LoC of net-new bridge):
This module aims to stay LEAN. If it grows past ~200 LoC, STOP and
surface to stakeholder. As of G0.5 first draft, the module weighs in
below that floor (see BUILD_JOURNAL entry for the LoC count).

WHY this is doctrinally correct: audio bytes carry voiceprint and image
bytes carry face identity — exactly what the Inner Gate is for. We do
NOT have a text-only Shield with audio/vision running uncovered.

Until emergentintegrations exposes a real ASR / vision SDK seam, calls
fall back to a deterministic `synthetic_plumbing_only=True` stub so the
pipeline exercises end-to-end without leaking bytes to a non-existent
provider.
"""
from __future__ import annotations

import hashlib
import logging
import os
from typing import Any, Dict

from services.layer_a.types import RawAudioArtifact, RawImageArtifact
from services.synisense.exceptions import ServiceUnavailable
from services.synisense.shield import trust_receipt

log = logging.getLogger("synisense.shield.perception_router")

_EMERGENT_KEY = os.environ.get("EMERGENT_LLM_KEY", "").strip()


def _mint_perception_receipt(*, tenant_id: str, purpose: str, audit: Dict[str, Any]) -> Dict[str, Any]:
    """Mint a perception-shaped trust receipt.

    The cousin's `trust_receipt.build_trust_receipt(...)` is shaped for
    text-LLM calls (de_id_summary, llm_provider, request_hash, etc.).
    Perception calls carry different fields; we build a perception-
    flavoured body here and sign it with the same `trust_receipt.sign(...)`
    primitive, so verification stays uniform.
    """
    from datetime import datetime, timezone
    body = {
        "version": "v1-perception",
        "tenant_id": tenant_id,
        "purpose": purpose,
        "modality": audit.get("modality"),
        "byte_count": audit.get("byte_count"),
        "model_id": audit.get("model_id"),
        "content_sha256": audit.get("content_sha256"),
        "prompt_sha256": audit.get("prompt_sha256"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    body["signature"] = trust_receipt.sign(body, tenant_id=tenant_id)
    return body


def _audit_kwargs(*, purpose: str, modality: str, byte_count: int, model_id: str) -> Dict[str, Any]:
    """Build the audit metadata. Mirrors llm_router's audit shape."""
    return {
        "purpose": purpose,
        "modality": modality,
        "byte_count": byte_count,
        "model_id": model_id,
        # NB: bytes themselves never enter the audit log. Only the hash.
        "content_sha256": None,  # filled by caller
    }


def _hash_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _stub_asr(audio: RawAudioArtifact) -> Dict[str, Any]:
    # Plumbing-only stub. Emits a single empty cue covering the duration
    # so downstream Layer C still sees a NormalizedUnit shape.
    return {
        "cues": [{"t_start_ms": 0, "t_end_ms": audio.duration_ms,
                  "text": "", "confidence": None}],
        "language_hint": None,
        "synthetic_plumbing_only": True,
    }


def _stub_vision(image: RawImageArtifact) -> Dict[str, Any]:
    return {
        "entities": [],
        "on_screen_text": "",
        "scene_description": "synthetic plumbing only — no perception",
        "synthetic_plumbing_only": True,
    }


def transcribe(*, audio: RawAudioArtifact, purpose: str, model_preference: str,
               model_id: str, model_version: str,
               extraction_params: Dict[str, Any]) -> Dict[str, Any]:
    """ASR call through the perception gate."""
    audit = _audit_kwargs(
        purpose=purpose, modality="audio",
        byte_count=len(audio.bytes_), model_id=model_id,
    )
    audit["content_sha256"] = _hash_bytes(audio.bytes_)

    if not _EMERGENT_KEY:
        result = _stub_asr(audio)
    else:
        # Real ASR SDK seam: when emergentintegrations exposes ASR, this
        # is where the call lands. Today no such seam exists — we keep
        # the stub path active and journal it.
        result = _stub_asr(audio)
        log.info("perception_router.transcribe: EMERGENT_LLM_KEY set but ASR seam not yet wired; stubbing")

    receipt = _mint_perception_receipt(
        tenant_id="rms",  # G0.5 single-tenant; multi-tenant lands at G5
        purpose=purpose, audit=audit,
    )
    result["trust_receipt"] = receipt
    return result


def perceive_image(*, image: RawImageArtifact, prompt: str, purpose: str,
                   model_id: str, model_version: str,
                   extraction_params: Dict[str, Any]) -> Dict[str, Any]:
    """Vision-LM call through the perception gate."""
    audit = _audit_kwargs(
        purpose=purpose, modality="image",
        byte_count=len(image.bytes_), model_id=model_id,
    )
    audit["content_sha256"] = _hash_bytes(image.bytes_)
    audit["prompt_sha256"] = _hash_bytes(prompt.encode("utf-8"))

    if not _EMERGENT_KEY:
        result = _stub_vision(image)
    else:
        result = _stub_vision(image)
        log.info("perception_router.perceive_image: EMERGENT_LLM_KEY set but vision seam not yet wired; stubbing")

    receipt = _mint_perception_receipt(
        tenant_id="rms", purpose=purpose, audit=audit,
    )
    result["trust_receipt"] = receipt
    return result
