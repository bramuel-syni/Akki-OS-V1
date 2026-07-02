"""Layer C — Normalize / Converge.

G0.5 Deliverable 4.a. Takes Layer B perception outputs and emits
NormalizedUnit instances against the G0-frozen Five Rings schema.

Discipline at G0.5:
  * Provenance ring populated deterministically from the perception
    artefact + source_ref.
  * Re-extraction Handle ring deterministic from provider artefacts'
    (model_id, model_version, extraction_params).
  * Signal ring populated with whatever the modality affords (cues for
    audio, scene text length for image, etc.). depth_judged stays False
    — Solva stamp lands at G2/G1.
  * Relational ring left empty at G0.5 (corroboration computation
    lands at G2).
  * Defensibility ring stamped DECLARATION BASELINE only:
    feed-level (genre, source_standing) supplied by caller; matrix
    lookup picks the rule; class taken from `asserts_what`. The V3
    inference overlay lands at G1.

Not pulling G1 work forward: no genre classifier, no content inference.
"""
from __future__ import annotations

import uuid
from typing import List, Optional

from contracts.five_rings import (
    DefensibilityClass,
    DefensibilityRing,
    Modality,
    NormalizedUnit,
    ProvenanceRing,
    RelationalRing,
    ReextractionHandleRing,
    ScoreVector,
    SignalRing,
)
from contracts.qualification_matrix.loader import (
    QualificationMatrix,
    load_qualification_matrix,
)
from services.layer_b.contracts import (
    AsrPerception, DiarizationPerception, VisionPerception,
)


def _matrix_lookup(matrix: QualificationMatrix, genre: str, source_standing: str) -> tuple[DefensibilityClass, str]:
    rule = matrix.find(genre, source_standing)
    if rule is None:
        # Conservative default — panel_debate.wire_republish (lowest ceiling cell at v0).
        rule = matrix.find("panel_debate", "wire_republish")
    return rule.asserts_what, matrix.rule_ref(rule)


def from_asr(
    *, perception: AsrPerception, source_ref: str, speaker: Optional[str],
    context: str, genre: str, source_standing: str,
    matrix: Optional[QualificationMatrix] = None,
) -> List[NormalizedUnit]:
    """One NormalizedUnit per ASR cue."""
    matrix = matrix or load_qualification_matrix("v0")
    cls, rule_ref = _matrix_lookup(matrix, genre, source_standing)
    out: List[NormalizedUnit] = []
    for cue in perception.cues:
        out.append(NormalizedUnit(
            unit_id=str(uuid.uuid4()),
            provenance=ProvenanceRing(
                source_ref=source_ref, modality=Modality.AUDIO,
                locator={"t_start_ms": cue.t_start_ms, "t_end_ms": cue.t_end_ms},
                speaker_or_author=speaker, context=context,
            ),
            # Signal Ring left empty at G1: ASR cue text length and
            # confidence are telemetry, NOT depth dimensions per
            # signal_ring_dimensions@v0. G2 perception modules emit real
            # depth signals (prosody / vocal_emphasis / affect_*). Until
            # then, empty is the honest answer.
            signal=SignalRing(dimensions={}, depth_judged=False),
            relational=RelationalRing(),
            reextraction_handle=ReextractionHandleRing(
                raw_pointer=source_ref,
                model_id=perception.model_id,
                model_version=perception.model_version,
                extraction_params=perception.extraction_params,
            ),
            defensibility=DefensibilityRing(
                defensibility_class=cls,
                score_vector=ScoreVector(),  # declaration baseline; scoring is G1
                matrix_rule_ref=rule_ref,
                runtime_mode="declaration_baseline",
            ),
        ))
    return out


def from_vision(
    *, perception: VisionPerception, source_ref: str, context: str,
    genre: str, source_standing: str,
    matrix: Optional[QualificationMatrix] = None,
) -> NormalizedUnit:
    """One NormalizedUnit per vision perception."""
    matrix = matrix or load_qualification_matrix("v0")
    cls, rule_ref = _matrix_lookup(matrix, genre, source_standing)
    return NormalizedUnit(
        unit_id=str(uuid.uuid4()),
        provenance=ProvenanceRing(
            source_ref=source_ref, modality=Modality.IMAGE,
            locator={}, speaker_or_author=None, context=context,
        ),
        # Same discipline as ASR aggregator: entity count + on-screen
        # text length are telemetry, not Signal depth. v0 catalogue
        # for IMAGE is {visual_emphasis, composition_markedness}. Real
        # depth signals come from G2 vision perception.
        signal=SignalRing(dimensions={}, depth_judged=False),
        relational=RelationalRing(),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer=source_ref,
            model_id=perception.model_id,
            model_version=perception.model_version,
            extraction_params=perception.extraction_params,
        ),
        defensibility=DefensibilityRing(
            defensibility_class=cls,
            score_vector=ScoreVector(),
            matrix_rule_ref=rule_ref,
            runtime_mode="declaration_baseline",
        ),
    )


def merge_diarization(
    units: List[NormalizedUnit], diarization: DiarizationPerception
) -> List[NormalizedUnit]:
    """Attach diarization speaker labels to audio units by overlap match.
    Returns NEW unit instances (Pydantic models are immutable-style)."""
    new_units: List[NormalizedUnit] = []
    for u in units:
        if u.provenance.modality != Modality.AUDIO:
            new_units.append(u)
            continue
        loc = u.provenance.locator
        s = int(loc.get("t_start_ms", 0)); e = int(loc.get("t_end_ms", 0))
        best = None; best_overlap = 0
        for turn in diarization.turns:
            overlap = max(0, min(e, turn.t_end_ms) - max(s, turn.t_start_ms))
            if overlap > best_overlap:
                best_overlap = overlap; best = turn
        if best is not None:
            new_units.append(u.model_copy(update={
                "provenance": u.provenance.model_copy(update={"speaker_or_author": best.speaker})
            }))
        else:
            new_units.append(u)
    return new_units
