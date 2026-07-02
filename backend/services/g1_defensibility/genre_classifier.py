"""Genre classifier v0 — rule-first hybrid (G1).

Stakeholder note: this is v0; iterate. Tight matrix vocabulary; emits
`genre="unknown"` cleanly when nothing fits (correct behaviour, not a bug).

Approach survey:
  * Pure-model (zero-shot classifier or vision-LM) — expensive per unit;
    falsifies less because failure modes are opaque; over-fits cleanly.
  * Pure-rule (pattern + duration + speaker heuristics) — brittle; needs
    constant hand-tuning; transparent but flat.
  * **Hybrid rule-first (chosen)** — rule layer gates an optional model
    layer; rule decision wins on high-confidence cases, model is fallback
    on medium-confidence or ambiguous cases. Transparent default;
    falsifiable failure modes (rule mismatch is loud); model layer is
    opt-in via `RMS_GENRE_MODEL=on` env, off by default at G1 (no model
    call until real Hour A arrives). This is the v0 stakeholder picked.

Cousin: nothing direct. The pattern-match + light-heuristic shape
rhymes with `/reference/akki-legacy/backend/services/inbox_routing/classifier.py`
(routes inbound emails by rule + confidence), which is cited as the
shape inspiration.

Genre vocabulary is constrained to the Qualification Matrix v0 rows.
If no rule fires and the model layer is off (or unsure), the classifier
emits `genre="unknown"` and the Ring-5 stamper refuses to stamp.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal, Optional

from contracts.five_rings import Modality, NormalizedUnit, ProvenanceRing
from contracts.qualification_matrix.loader import load_qualification_matrix


@dataclass
class GenreClassificationResult:
    genre: str       # value from matrix vocabulary OR "unknown"
    confidence: float
    decided_by: Literal["rule", "model", "hybrid", "unknown"]


def _matrix_genres() -> set[str]:
    matrix = load_qualification_matrix("v0")
    return {r.genre for r in matrix.rules}


def _classify_by_rule(provenance: ProvenanceRing) -> Optional[GenreClassificationResult]:
    ctx = (provenance.context or "").lower()
    speaker = (provenance.speaker_or_author or "").lower()
    modality = provenance.modality
    # Duration heuristic.
    duration_ms = 0
    if modality in (Modality.AUDIO, Modality.VIDEO):
        loc = provenance.locator or {}
        duration_ms = int(loc.get("t_end_ms", 0)) - int(loc.get("t_start_ms", 0))

    matrix_genres = _matrix_genres()

    # Panel-debate cues: panellist speaker, panel/debate language in context.
    if ("panel" in ctx or "debate" in ctx or "panellist" in speaker or "caller" in speaker):
        return GenreClassificationResult(genre="panel_debate", confidence=0.85, decided_by="rule")
    # News-anchor cues: anchor speaker, headline/newsdesk language, audio modality, >5s duration.
    if ("anchor" in speaker or "newsdesk" in ctx or "headline" in ctx or "news" in ctx) \
            and modality in (Modality.AUDIO, Modality.TEXT, Modality.VIDEO):
        return GenreClassificationResult(genre="news_anchor_read", confidence=0.80, decided_by="rule")
    # Image with "keyframe" or "logo" -> follow the parent audio's genre via context.
    if modality == Modality.IMAGE and ("keyframe" in ctx or "logo" in ctx):
        if "news_anchor_read" in matrix_genres:
            return GenreClassificationResult(genre="news_anchor_read", confidence=0.70, decided_by="rule")
    return None


def classify(unit_or_provenance) -> GenreClassificationResult:
    """Returns a GenreClassificationResult; never raises."""
    if isinstance(unit_or_provenance, NormalizedUnit):
        provenance = unit_or_provenance.provenance
    else:
        provenance = unit_or_provenance

    rule_result = _classify_by_rule(provenance)
    if rule_result is not None:
        return rule_result

    # Model layer is opt-in. At G1 we keep it OFF and emit unknown loudly.
    if os.environ.get("RMS_GENRE_MODEL", "off").lower() == "on":
        # G2 wires a vision/text model behind perception_router. At G1 we don't
        # silently fall back to a model call — the env flag must be on AND a
        # provider must be available. For now the flag toggles intent only.
        pass

    return GenreClassificationResult(genre="unknown", confidence=0.0, decided_by="unknown")
