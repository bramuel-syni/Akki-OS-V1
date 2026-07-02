"""Solva assertion boundary + enforcement — behavioural tests (Solva spec §14).

Covers spec §14 obligations:
  #1 test_class_is_floor_over_load_bearing
  #3 test_utterance_never_asserted_as_fact
  #4 test_refuse_below_floor
  #6 test_solva_never_extracts (structural — see reasoning-faculty isolation)
"""
from __future__ import annotations

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
from services.solva_depth.assertion import (
    Assertion,
    assert_conclusion,
    conclusion_class,
)
from services.solva_depth.enforce import Refusal, enforce
from services.solva_depth.interfaces import FloorSpec
from tests.invariants._ep_v0_fixtures import ep_v0


def _unit(klass: DefensibilityClass, uid: str = "u1") -> NormalizedUnit:
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
            defensibility_class=klass,
            score_vector=ScoreVector(),
            matrix_rule_ref="panel_debate.wire_republish",
            runtime_mode="declaration_baseline",
        ),
    )


# Spec §14 #1
def test_class_is_floor_over_load_bearing_all_fact():
    units = [_unit(DefensibilityClass.FACT, f"u{i}") for i in range(3)]
    assert conclusion_class(units) == DefensibilityClass.FACT


def test_class_is_floor_over_load_bearing_mixed():
    """A single utterance drags the floor to utterance regardless of the rest."""
    units = [
        _unit(DefensibilityClass.FACT, "u1"),
        _unit(DefensibilityClass.UTTERANCE, "u2"),
        _unit(DefensibilityClass.FACT, "u3"),
    ]
    assert conclusion_class(units) == DefensibilityClass.UTTERANCE


def test_class_is_floor_over_load_bearing_non_factual_wins():
    """A single non_factual unit floors the whole conclusion."""
    units = [
        _unit(DefensibilityClass.FACT, "u1"),
        _unit(DefensibilityClass.NON_FACTUAL, "u2"),
    ]
    assert conclusion_class(units) == DefensibilityClass.NON_FACTUAL


# Spec §14 #3
def test_utterance_never_asserted_as_fact():
    """Utterance-class conclusion phrased 'was stated', never as fact."""
    units = [_unit(DefensibilityClass.UTTERANCE)]
    a: Assertion = assert_conclusion("It will rain tomorrow", units)
    assert a.klass == DefensibilityClass.UTTERANCE
    assert a.claim is not None
    assert "was stated" in a.claim.lower()
    assert '"it will rain tomorrow"' in a.claim.lower()


def test_fact_class_assertion_is_raw_claim():
    units = [_unit(DefensibilityClass.FACT)]
    a = assert_conclusion("The sun rose at 06:15 today", units)
    assert a.klass == DefensibilityClass.FACT
    assert a.claim == "The sun rose at 06:15 today"


def test_non_factual_class_carries_context_only():
    units = [_unit(DefensibilityClass.NON_FACTUAL)]
    a = assert_conclusion("Opinion text", units)
    assert a.klass == DefensibilityClass.NON_FACTUAL
    assert a.claim is None
    assert a.context_only == "Opinion text"


# Spec §14 #4
def test_refuse_below_floor():
    """A conclusion below the objective floor is refused with structured reason."""
    units = [_unit(DefensibilityClass.UTTERANCE)]
    floor = FloorSpec(minimum_class=DefensibilityClass.FACT)  # floor demands fact
    result = enforce("Some conclusion", units, floor)
    assert isinstance(result, Refusal)
    assert result.reason == "below_defensibility_floor"
    assert result.computed_class == DefensibilityClass.UTTERANCE
    assert result.floor_class == DefensibilityClass.FACT


def test_enforce_at_floor_passes():
    """Class exactly at floor is not refused."""
    units = [_unit(DefensibilityClass.UTTERANCE)]
    floor = FloorSpec(minimum_class=DefensibilityClass.UTTERANCE)
    result = enforce("It was stated", units, floor)
    assert isinstance(result, Assertion)
    assert result.klass == DefensibilityClass.UTTERANCE


def test_enforce_above_floor_passes():
    units = [_unit(DefensibilityClass.FACT)]
    floor = FloorSpec(minimum_class=DefensibilityClass.UTTERANCE)
    result = enforce("Fact claim", units, floor)
    assert isinstance(result, Assertion)
    assert result.klass == DefensibilityClass.FACT


def test_conclusion_class_rejects_empty():
    """No load-bearing units — no defensible conclusion. Raises."""
    with pytest.raises(ValueError):
        conclusion_class([])
