"""A1.3 · VAD (DEFAULT · PROM-9-2a-real-worker-provenance · Silero registry-pinned).

Silero VAD registry-pinned via existing perception worker infrastructure. No fresh
download; consumer of the model registry pin (models_registry.v0.json).

Parameters (D-12 · known and parameterized · deploy in force):
- silero_threshold: 0.5 (DEFAULT · voice-activity confidence cutoff)
- min_speech_ms: 250 (minimum speech run to retain)
- min_silence_ms: 500 (minimum silence run to split)

Non-speech spans are LOGGED as content-type index entries (music · ad · silence ·
tone · unknown). Never discarded (R-A1.3 honesty grammar).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal

SILERO_THRESHOLD_DEFAULT: float = 0.5
MIN_SPEECH_MS_DEFAULT: int = 250
MIN_SILENCE_MS_DEFAULT: int = 500

ContentType = Literal["speech", "music", "ad", "silence", "tone", "unknown"]


@dataclass(frozen=True)
class VADSegment:
    """VAD-emitted segment: either speech or non-speech (content-type indexed)."""
    batch_id: str
    start_ms: int
    end_ms: int
    is_speech: bool
    content_type: ContentType
    confidence: float


@dataclass(frozen=True)
class VADProbe:
    """Per-frame VAD probe from Silero. Deterministic input to VADSegment reduction."""
    t_ms: int
    speech_probability: float
    content_hint: ContentType = "unknown"


def registry_pin_reference() -> dict:
    """Return the Silero VAD registry-pin reference (no model load)."""
    return {
        "family": "Silero VAD",
        "role": "vad_gate",
        "registry_source": "backend/services/perception/models_registry.v0.json",
        "provenance_discipline": "PROM-9-2a-real-worker-provenance",
        "threshold_default": SILERO_THRESHOLD_DEFAULT,
    }


def reduce_probes_to_segments(
    batch_id: str,
    probes: List[VADProbe],
    threshold: float = SILERO_THRESHOLD_DEFAULT,
    min_speech_ms: int = MIN_SPEECH_MS_DEFAULT,
    min_silence_ms: int = MIN_SILENCE_MS_DEFAULT,
) -> List[VADSegment]:
    """Reduce per-frame probes to run-length speech/non-speech segments.

    Deterministic: same probes + params → same segments. Non-speech spans get
    content-type indexed from the majority hint over the run.
    """
    if not probes:
        return []
    probes_sorted = sorted(probes, key=lambda p: p.t_ms)
    segments: List[VADSegment] = []
    run_start = probes_sorted[0].t_ms
    run_is_speech = probes_sorted[0].speech_probability >= threshold
    run_conf_sum = probes_sorted[0].speech_probability
    run_hint_counts: dict = {probes_sorted[0].content_hint: 1}
    run_count = 1

    for i in range(1, len(probes_sorted)):
        p = probes_sorted[i]
        p_is_speech = p.speech_probability >= threshold
        if p_is_speech != run_is_speech:
            _emit_run(
                segments, batch_id, run_start, p.t_ms, run_is_speech,
                run_conf_sum, run_count, run_hint_counts,
                min_speech_ms, min_silence_ms,
            )
            run_start = p.t_ms
            run_is_speech = p_is_speech
            run_conf_sum = p.speech_probability
            run_hint_counts = {p.content_hint: 1}
            run_count = 1
        else:
            run_conf_sum += p.speech_probability
            run_hint_counts[p.content_hint] = run_hint_counts.get(p.content_hint, 0) + 1
            run_count += 1

    # Emit tail run
    tail_end = probes_sorted[-1].t_ms + 20  # last-frame duration approx
    _emit_run(
        segments, batch_id, run_start, tail_end, run_is_speech,
        run_conf_sum, run_count, run_hint_counts,
        min_speech_ms, min_silence_ms,
    )
    return segments


def _emit_run(
    out: List[VADSegment],
    batch_id: str,
    start_ms: int,
    end_ms: int,
    is_speech: bool,
    conf_sum: float,
    count: int,
    hint_counts: dict,
    min_speech_ms: int,
    min_silence_ms: int,
) -> None:
    duration = end_ms - start_ms
    if is_speech and duration < min_speech_ms:
        return
    if not is_speech and duration < min_silence_ms:
        return
    if is_speech:
        content_type: ContentType = "speech"
    else:
        # Majority-content-hint for non-speech; default unknown.
        content_type = max(hint_counts.items(), key=lambda kv: kv[1])[0]
        if content_type == "speech":  # defensive: never re-emit speech-as-nonspeech
            content_type = "unknown"
    out.append(
        VADSegment(
            batch_id=batch_id,
            start_ms=start_ms,
            end_ms=end_ms,
            is_speech=is_speech,
            content_type=content_type,
            confidence=conf_sum / count if count > 0 else 0.0,
        )
    )
