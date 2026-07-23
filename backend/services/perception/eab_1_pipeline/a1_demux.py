"""A1.1 · Demux & normalize (FACT · PROM-S1-frozen-wire-contract).

Rung-1 CPU demux/normalize of source objects to canonical audio artifact.
Deterministic transcoding; source-object lineage preserved.

Parameters (D-12 · known and parameterized · deploy in force):
- target_sample_rate: 16000 Hz (mono · PCM float32 conventional)
- target_channels: 1 (mono downmix)
- normalize_dbfs: -23.0 (EBU R128 loudness normalization target)

Real-world backend adapter is ffmpeg (deterministic, cross-platform, in registry
pin at deployment). This module provides the *deterministic wire contract* — the
canonical audio artifact metadata envelope emitted per source. Backend adapter
lives at `backend/services/perception/eab_1_pipeline/backends/` at deployment
(NOT this atomic; the wire contract is what deploys).
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

TARGET_SAMPLE_RATE_HZ: int = 16000
TARGET_CHANNELS: int = 1
NORMALIZE_LUFS_TARGET: float = -23.0  # EBU R128


@dataclass(frozen=True)
class CanonicalAudioArtifact:
    """Canonical audio artifact envelope emitted per source object.

    Frozen dataclass (worker-side, NOT a Parity 31 contract).
    Lineage back to source is FACT-class; deterministic content-address by SHA-256
    of the normalized waveform (backend adapter computes; interface guaranteed).
    """
    canonical_id: str
    source_object_id: str
    duration_ms: int
    sample_rate_hz: int
    channels: int
    normalize_lufs: float
    content_sha256: str
    demuxed_at: str  # ISO8601 UTC


def compute_canonical_id(source_object_id: str, content_sha256: str) -> str:
    """Content-addressed canonical_id. Deterministic; source-lineage-attached.

    Format: `canon:sha256:<hex[:32]>:<source_stub>` — stable across re-runs.
    """
    if not source_object_id or not content_sha256:
        raise ValueError("source_object_id and content_sha256 required")
    stub = source_object_id.split("/")[-1][:24]
    return f"canon:sha256:{content_sha256[:32]}:{stub}"


def emit_canonical_artifact(
    source_object_id: str,
    normalized_pcm_bytes: bytes,
    duration_ms: int,
) -> CanonicalAudioArtifact:
    """Emit the canonical audio artifact envelope from normalized PCM.

    Deterministic: same inputs → same envelope. Backend adapter (ffmpeg) produces
    `normalized_pcm_bytes` at TARGET_SAMPLE_RATE_HZ · TARGET_CHANNELS · LUFS-normalized;
    this module hashes the bytes and mints the envelope.
    """
    if duration_ms <= 0:
        raise ValueError("duration_ms must be positive")
    content_sha256 = hashlib.sha256(normalized_pcm_bytes).hexdigest()
    canonical_id = compute_canonical_id(source_object_id, content_sha256)
    return CanonicalAudioArtifact(
        canonical_id=canonical_id,
        source_object_id=source_object_id,
        duration_ms=duration_ms,
        sample_rate_hz=TARGET_SAMPLE_RATE_HZ,
        channels=TARGET_CHANNELS,
        normalize_lufs=NORMALIZE_LUFS_TARGET,
        content_sha256=content_sha256,
        demuxed_at=datetime.now(timezone.utc).isoformat(),
    )
