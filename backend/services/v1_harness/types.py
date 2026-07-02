"""V1 measurement harness types.

No cousin. Net-new. Hard Rule 1 enforced by HourBundle + the harness
constructor refusing identical spike/production paths.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional

Verdict = Literal["PASS", "FAIL", "PENDING_REAL_MATERIAL"]


@dataclass
class HourBundle:
    """One RMS broadcast hour + its paired gold data.

    Per the G0.5 brief: real Hour A is the SPIKE hour; held-out Hour B
    is the PRODUCTION hour. The harness refuses to validate against
    the hour it was tuned on.
    """
    audio_path: str
    gold_transcript_path: str
    gold_diarization_path: str
    gold_entities_path: str
    video_path: Optional[str] = None
    label: str = ""  # human-friendly tag, e.g. "hour_a_spike"
    is_synthetic: bool = False  # set True for synthetic-fixture-derived bundles


@dataclass
class V1Metrics:
    wer_vs_clean_gold: Optional[float] = None
    wer_vs_asr_output: Optional[float] = None  # paired telemetry, not a gate
    der_thirty_plus: Optional[float] = None
    ner_recall_vs_clean_gold: Optional[float] = None    # GATE
    ner_recall_vs_asr_output: Optional[float] = None    # telemetry only
    five_rings_completeness: Dict[str, float] = field(default_factory=dict)
    runtime_realtime_x: Optional[float] = None
    cost_per_hour_usd: Optional[float] = None  # report-only
    defensibility_class_distribution: Dict[str, float] = field(default_factory=dict)


@dataclass
class V1Report:
    verdict: Verdict
    metrics: V1Metrics
    spike_hour_path: Optional[str]
    production_hour_path: Optional[str]
    notes: list[str] = field(default_factory=list)
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict,
            "metrics": self.metrics.__dict__,
            "spike_hour_path": self.spike_hour_path,
            "production_hour_path": self.production_hour_path,
            "notes": self.notes,
            "timestamp": self.timestamp,
        }
