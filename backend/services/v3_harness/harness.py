"""V3 measurement harness — G1 Deliverable 4.

Mirrors the V1 harness PENDING-on-synthetic discipline. Refuses to
compute PASS/FAIL unless ALL of the following hold:
  * labelled_slice.units count >= 300
  * adjudication_kappa >= 0.70
  * labeller_count >= 2
  * data source is real (synthetic is author-controlled — scoring against
    it is circular)

Metrics (Spec §5.6 + G1 brief gates):
  * genre_classification_accuracy   (gate >= 0.80)
  * fact_class_precision            (gate >= 0.90)   THE gate
  * fact_class_recall               (gate >= 0.50)
  * utterance_vs_fact_accuracy      (gate >= 0.85)
  * non_factual_precision           (gate >= 0.95)

Per-genre breakdown surfaced alongside aggregates.

No cousin. Pattern rhymes with v1_harness.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from contracts.five_rings import NormalizedUnit

Verdict = Literal["PASS", "FAIL", "PENDING_REAL_LABELLED_SET"]

_GATES = {
    "genre_classification_accuracy": 0.80,
    "fact_class_precision": 0.90,
    "fact_class_recall": 0.50,
    "utterance_vs_fact_accuracy": 0.85,
    "non_factual_precision": 0.95,
}


@dataclass
class LabelledUnitsBundle:
    units: List[NormalizedUnit]
    gold_labels: Dict[str, Dict[str, str]]  # unit_id -> {genre, source_standing, defensibility_class}
    adjudication_kappa: float
    labeller_count: int
    is_synthetic: bool = False
    label: str = ""


@dataclass
class V3Metrics:
    aggregate: Dict[str, Optional[float]] = field(default_factory=dict)
    per_genre: Dict[str, Dict[str, float]] = field(default_factory=dict)


@dataclass
class V3Report:
    verdict: Verdict
    metrics: V3Metrics
    labelled_set_summary: Dict[str, Any]
    notes: List[str] = field(default_factory=list)
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "verdict": self.verdict,
            "metrics": {"aggregate": self.metrics.aggregate, "per_genre": self.metrics.per_genre},
            "labelled_set_summary": self.labelled_set_summary,
            "notes": self.notes,
            "timestamp": self.timestamp,
        }


_LAST_REPORT: Optional[V3Report] = None


def last_report() -> Optional[V3Report]:
    return _LAST_REPORT


def run(labelled_slice: LabelledUnitsBundle) -> V3Report:
    global _LAST_REPORT
    notes: List[str] = []
    summary = {
        "unit_count": len(labelled_slice.units),
        "adjudication_kappa": labelled_slice.adjudication_kappa,
        "labeller_count": labelled_slice.labeller_count,
        "is_synthetic": labelled_slice.is_synthetic,
        "label": labelled_slice.label,
    }

    # Refusal gates.
    refuse = False
    if labelled_slice.is_synthetic:
        notes.append("labelled slice is synthetic; scoring is circular. Verdict PENDING.")
        refuse = True
    if len(labelled_slice.units) < 300:
        notes.append(f"labelled set size {len(labelled_slice.units)} < 300 minimum; PENDING.")
        refuse = True
    if labelled_slice.adjudication_kappa < 0.70:
        notes.append(f"adjudication kappa {labelled_slice.adjudication_kappa} < 0.70; PENDING.")
        refuse = True
    if labelled_slice.labeller_count < 2:
        notes.append(f"labeller_count {labelled_slice.labeller_count} < 2; PENDING.")
        refuse = True

    if refuse:
        report = V3Report(
            verdict="PENDING_REAL_LABELLED_SET",
            metrics=V3Metrics(),
            labelled_set_summary=summary,
            notes=notes,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        _LAST_REPORT = report
        return report

    # Real-material scoring path. Substantive scorers (sklearn-style
    # precision/recall/F1, Cohen-kappa-corrected accuracy) land when the
    # first real labelled slice arrives; at G1 we emit a stub PENDING.
    notes.append("V3 scorers (precision/recall/disambiguation) pending first real labelled slice; placeholder.")
    report = V3Report(
        verdict="PENDING_REAL_LABELLED_SET",
        metrics=V3Metrics(),
        labelled_set_summary=summary,
        notes=notes,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    _LAST_REPORT = report
    return report


def gates() -> Dict[str, float]:
    return dict(_GATES)
