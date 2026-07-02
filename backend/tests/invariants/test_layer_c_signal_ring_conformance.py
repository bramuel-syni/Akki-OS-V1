"""Layer C signal-ring conformance — H-a2 discipline landed as test.

Product Spec 2.1 §12 declares the signal_ring_dimensions@v0 catalogue.
Layer C convergence MUST reject any input whose Signal ring uses
dimensions outside the frozen catalogue for its modality.

Enforces §31 invariant #6 (six frozen contracts are the source of truth):
any Layer C emit or consume that widens the dimension set is a
contract-frozenness violation caught here.
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
from services.layer_c.convergence import (
    SignalRingConformanceError,
    assert_signal_ring_conformant,
    converge_units,
)
from tests.invariants._ep_v0_fixtures import ep_v0


def _unit(modality: Modality, dims: dict) -> NormalizedUnit:
    return NormalizedUnit(
        unit_id="u-test-1",
        provenance=ProvenanceRing(
            source_ref="test:src", modality=modality,
            locator={}, speaker_or_author=None, context="test",
        ),
        signal=SignalRing(dimensions=dims, depth_judged=False),
        relational=RelationalRing(),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer="test:src",
            model_id="test-model", model_version="v0",
            extraction_params=ep_v0(modality),
        ),
        defensibility=DefensibilityRing(
            defensibility_class=DefensibilityClass.UTTERANCE,
            score_vector=ScoreVector(),
            matrix_rule_ref="panel_debate.wire_republish",
            runtime_mode="declaration_baseline",
        ),
    )


def test_empty_dimensions_is_conformant():
    """Empty signal-ring dims is trivially subset — must not raise."""
    u = _unit(Modality.AUDIO, {})
    assert_signal_ring_conformant(u)  # no raise


def test_audio_catalogue_dimensions_accepted():
    """Audio dims within the frozen catalogue are accepted."""
    u = _unit(Modality.AUDIO, {"prosody": 0.5, "affect_valence": 0.3})
    assert_signal_ring_conformant(u)  # no raise


def test_audio_out_of_catalogue_dimension_rejected():
    """A modality-inappropriate dim raises SignalRingConformanceError."""
    u = _unit(Modality.AUDIO, {"visual_emphasis": 0.7})
    with pytest.raises(SignalRingConformanceError):
        assert_signal_ring_conformant(u)


def test_converge_units_validates_conformance():
    """`converge_units` MUST reject any non-conformant unit at entry."""
    good = _unit(Modality.TEXT, {"lexical_intensity": 0.4})
    bad = _unit(Modality.TEXT, {"nonexistent_dim": 0.9})
    assert converge_units([good]) == [good]
    with pytest.raises(SignalRingConformanceError):
        converge_units([good, bad])


def test_video_catalogue():
    u = _unit(Modality.VIDEO, {"visual_emphasis": 0.5, "scene_change_density": 0.2, "framing_markedness": 0.1})
    assert_signal_ring_conformant(u)


def test_image_catalogue_rejects_video_dim():
    """Composition_markedness OK for image; scene_change_density is video-only."""
    ok = _unit(Modality.IMAGE, {"visual_emphasis": 0.3, "composition_markedness": 0.6})
    assert_signal_ring_conformant(ok)
    bad = _unit(Modality.IMAGE, {"scene_change_density": 0.5})
    with pytest.raises(SignalRingConformanceError):
        assert_signal_ring_conformant(bad)


def test_composite_modality_empty_only():
    """`composite: []` in the frozen catalogue — no dims allowed."""
    ok = _unit(Modality.COMPOSITE, {})
    assert_signal_ring_conformant(ok)
    bad = _unit(Modality.COMPOSITE, {"prosody": 0.5})
    with pytest.raises(SignalRingConformanceError):
        assert_signal_ring_conformant(bad)
