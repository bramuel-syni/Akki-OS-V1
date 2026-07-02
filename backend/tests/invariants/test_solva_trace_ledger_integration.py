"""Solva trace → Northena Ledger integration — Solva spec §17 #8.

Every extraction-time judgment produces a trace. Trace is absorbed into
the Northena Ledger via `absorb_solva_trace` — no frozen-contract mutation.

The test runs a synthetic Solva pipeline end-to-end and asserts:
  * SolvaTrace carries all 6 stages (Layer C converge + 5 reasoning stages).
  * All stages share the same trace_id.
  * Ledger receives exactly one entry per run under stage='converge'.
  * The stamp_audit field carries the full trace dict.
"""
from __future__ import annotations

import asyncio
import uuid
from typing import List

import pytest

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
from contracts.northena_ledger import LedgerArtifactRef
from services.northena.converge import absorb_solva_trace
from services.solva_depth.interfaces import FloorSpec
from services.solva_depth.pipeline import run_solva
from tests.invariants._ep_v0_fixtures import ep_v0


def _fact_unit(uid: str) -> NormalizedUnit:
    return NormalizedUnit(
        unit_id=uid,
        provenance=ProvenanceRing(
            source_ref="test:src", modality=Modality.TEXT,
            locator={}, speaker_or_author=None, context="test",
        ),
        signal=SignalRing(dimensions={}, depth_judged=False),
        relational=RelationalRing(),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer="test:src", model_id="test-model",
            model_version="v0", extraction_params=ep_v0(Modality.TEXT),
        ),
        defensibility=DefensibilityRing(
            defensibility_class=DefensibilityClass.FACT,
            score_vector=ScoreVector(),
            matrix_rule_ref="news_anchor_read.primary_recorded",
            runtime_mode="declaration_baseline",
        ),
    )


def test_pipeline_emits_full_stage_trace():
    """Solva pipeline emits Layer C converge + 5 reasoning stages, all sharing trace_id."""
    trace_id = f"trace-{uuid.uuid4().hex[:8]}"
    run_id = f"run-{uuid.uuid4().hex[:8]}"
    units = [_fact_unit("u-1"), _fact_unit("u-2")]
    floor = FloorSpec(minimum_class=DefensibilityClass.UTTERANCE)
    trace = run_solva(
        trace_id=trace_id, run_id=run_id,
        question="Is this defensible?", units=units, floor=floor,
    )
    # 6 stage records: layer_c_converge + 5 reasoning stages.
    stage_names = [s.stage_name for s in trace.stages]
    assert stage_names == ["layer_c_converge", "frame", "candidate", "tension", "probability", "reflection"]
    assert trace.trace_id == trace_id
    assert trace.run_id == run_id
    # Load-bearing units flow through.
    assert set(trace.load_bearing_unit_ids) == {"u-1", "u-2"}
    # Class is fact (both units are fact-class).
    assert trace.computed_class == "fact"


def _non_factual_unit(uid: str) -> NormalizedUnit:
    """Non-factual fixture — forces refusal under a fact floor."""
    return NormalizedUnit(
        unit_id=uid,
        provenance=ProvenanceRing(
            source_ref="test:src", modality=Modality.TEXT,
            locator={}, speaker_or_author=None, context="test",
        ),
        signal=SignalRing(dimensions={}, depth_judged=False),
        relational=RelationalRing(),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer="test:src", model_id="test-model",
            model_version="v0", extraction_params=ep_v0(Modality.TEXT),
        ),
        defensibility=DefensibilityRing(
            defensibility_class=DefensibilityClass.NON_FACTUAL,
            score_vector=ScoreVector(),
            matrix_rule_ref="opinion.editorial",
            runtime_mode="declaration_baseline",
        ),
    )


def test_pipeline_threads_refusal_computed_class():
    """X1 discipline (post-A2): on a refusal, the pipeline reads
    computed_class from Refusal.computed_class (the boundary's threaded
    value) rather than recomputing it via conclusion_class(lb). Assert
    the trace's computed_class equals what the boundary returned.
    """
    from services.solva_depth.enforce import enforce, Refusal
    trace_id = f"trace-{uuid.uuid4().hex[:8]}"
    run_id = f"run-{uuid.uuid4().hex[:8]}"
    units = [_non_factual_unit("u-x"), _non_factual_unit("u-y")]
    floor = FloorSpec(minimum_class=DefensibilityClass.FACT)  # forces refusal
    trace = run_solva(
        trace_id=trace_id, run_id=run_id,
        question="Below-floor question?", units=units, floor=floor,
    )
    # Precondition: the boundary MUST refuse under this input.
    boundary_result = enforce("Below-floor question?", units, floor)
    assert isinstance(boundary_result, Refusal), (
        "test precondition: enforce() must refuse for this input"
    )
    # X1: threaded value on the refusal object must match the trace's field.
    assert trace.computed_class == boundary_result.computed_class.value
    assert trace.computed_class == "non_factual"


@pytest.mark.asyncio
async def test_solva_trace_lands_in_ledger():
    """Ledger.absorb_solva_trace lands exactly one row per pipeline run.

    Uses MongoDB via the async ledger writer. Isolates by unique trace_id.
    """
    from core import db
    from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION

    trace_id = f"g3-test-trace-{uuid.uuid4().hex[:12]}"
    run_id = f"g3-test-run-{uuid.uuid4().hex[:12]}"
    units = [_fact_unit("u-a"), _fact_unit("u-b")]
    floor = FloorSpec(minimum_class=DefensibilityClass.UTTERANCE)
    trace = run_solva(
        trace_id=trace_id, run_id=run_id,
        question="Is this defensible?", units=units, floor=floor,
    )
    row = await absorb_solva_trace(
        run_id=run_id, trace_id=trace_id, trace_dict=trace.to_dict(),
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request",
            artifact_id="g3-test-artifact",
            version="v0",
        ),
        lawful_basis_ref="g3-test-lawful-basis",
    )
    assert row.stage == "converge"
    assert row.decision == "terminate_success"  # fact-class assertion path
    # Fetch back via cursor + assert single-entry semantics.
    cursor = db[NORTHENA_LEDGER_COLLECTION].find({"trace_id": trace_id}, {"_id": 0})
    found: List[dict] = [r async for r in cursor]
    assert len(found) == 1, f"expected exactly 1 ledger row per run; got {len(found)}"
    sa = found[0]["stamp_audit"]
    # stamp_audit carries the full SolvaTrace dict.
    assert sa["trace_id"] == trace_id
    assert sa["run_id"] == run_id
    stage_names = [s["stage_name"] for s in sa["stages"]]
    assert stage_names == ["layer_c_converge", "frame", "candidate", "tension", "probability", "reflection"]
    assert sa["conclusion"]["kind"] == "assertion"
    # Cleanup — leave no residue in the shared test DB.
    await db[NORTHENA_LEDGER_COLLECTION].delete_many({"trace_id": trace_id})
