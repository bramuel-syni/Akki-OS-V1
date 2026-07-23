"""A2.1 · Occurrence rows as NormalizedUnits (FACT · MC-E1 α precedent).

Emits occurrence-row NormalizedUnits under Owner E1 ruling:
  - modality: AUDIO (occurrence is not a new modality; it addresses existing audio)
  - locator: DICT ADDITION ONLY — carries {canonical_id, station, timestamp, batch_lineage}
             plus base audio locator keys (t_start_ms, t_end_ms)
  - ZERO contract mutation to backend/contracts/five_rings.py

Enforced by AST cell at backend/tests/invariants/test_five_rings_v0_zero_mutation_ast_cell.py.

Parameters (D-12 · known and parameterized):
- default_chunk_size: 500 occurrences per batch commit (builder Tier-3 default)
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from contracts.five_rings import (
    DefensibilityClass,
    DefensibilityRing,
    Modality,
    NormalizedUnit,
    ProvenanceRing,
    ReextractionHandleRing,
    RelationalRing,
    ScoreVector,
    SignalRing,
)

from services.perception.eab_1_pipeline.a1_dedup import Occurrence


DEFAULT_CHUNK_SIZE: int = 500
EAB1_MODEL_ID: str = "eab_1_pipeline"
EAB1_MODEL_VERSION: str = "v1"


def build_occurrence_locator(
    *,
    canonical_id: str,
    station: str,
    timestamp_ms: int,
    batch_lineage: List[str],
    t_start_ms: int,
    t_end_ms: int,
) -> Dict[str, Any]:
    """Additive locator vocabulary for occurrence rows (Owner E1 α).

    Locator is Dict[str, Any] in the frozen ProvenanceRing; adding new keys is
    dict-content, not contract shape. AST cell enforces contract byte-identity.
    """
    return {
        # base audio locator keys (existing convention):
        "t_start_ms": int(t_start_ms),
        "t_end_ms": int(t_end_ms),
        # additive occurrence keys (Owner E1 α · 2026-07-15):
        "canonical_id": canonical_id,
        "station": station,
        "timestamp_ms": int(timestamp_ms),
        "batch_lineage": list(batch_lineage),
    }


def _eab1_extraction_params() -> Dict[str, Any]:
    """AUDIO modality extraction_params · deterministic pins for occurrence emission."""
    return {
        "provider_id": "eab_1_pipeline",
        "provider_version": "1.0.0",
        "extraction_run_id": "eab-1-occurrence-writer",
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "sample_rate_hz": 16000,
        "chunk_ms": 30000,
        "model_decoding_params": {
            "language_hint": "en",
            "beam_size": 1,
            "temperature": 0,
            "vad_threshold": 0.5,
        },
    }


def build_occurrence_unit(
    *,
    occurrence: Occurrence,
    source_ref: str,
    matrix_rule_ref: str,
    context: Optional[str] = None,
) -> NormalizedUnit:
    """Emit a single occurrence NormalizedUnit.

    FACT-class of container: the occurrence physically appeared at the source
    location; the UTTERANCE/FACT ceiling is inherited from the canonical the
    occurrence matches, per S1 §4.1 "defensibility class capped at the class
    their cited sources support" (S1 spec landed 2026-07-15).
    """
    locator = build_occurrence_locator(
        canonical_id=occurrence.canonical_id,
        station=occurrence.station,
        timestamp_ms=occurrence.timestamp_ms,
        batch_lineage=[occurrence.batch_id],
        t_start_ms=occurrence.start_ms,
        t_end_ms=occurrence.end_ms,
    )
    provenance = ProvenanceRing(
        source_ref=source_ref,
        modality=Modality.AUDIO,  # occurrence is audio-addressed; NOT a new modality
        locator=locator,
        speaker_or_author=None,
        context=context or f"occurrence:{occurrence.occurrence_id}",
    )
    reextraction_handle = ReextractionHandleRing(
        raw_pointer=occurrence.requeue_pointer,
        model_id=EAB1_MODEL_ID,
        model_version=EAB1_MODEL_VERSION,
        extraction_params=_eab1_extraction_params(),
    )
    defensibility = DefensibilityRing(
        defensibility_class=DefensibilityClass.UTTERANCE,
        score_vector=ScoreVector(),
        matrix_rule_ref=matrix_rule_ref,
        runtime_mode="declaration_baseline",
    )
    return NormalizedUnit(
        unit_id=occurrence.occurrence_id,
        provenance=provenance,
        signal=SignalRing(),
        relational=RelationalRing(),
        reextraction_handle=reextraction_handle,
        defensibility=defensibility,
    )


def emit_occurrences_chunked(
    *,
    occurrences: List[Occurrence],
    source_ref: str,
    matrix_rule_ref: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    context: Optional[str] = None,
) -> List[List[NormalizedUnit]]:
    """Emit occurrence NormalizedUnits in deterministic chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    chunks: List[List[NormalizedUnit]] = []
    current: List[NormalizedUnit] = []
    for occurrence in occurrences:
        current.append(
            build_occurrence_unit(
                occurrence=occurrence,
                source_ref=source_ref,
                matrix_rule_ref=matrix_rule_ref,
                context=context,
            )
        )
        if len(current) >= chunk_size:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks
