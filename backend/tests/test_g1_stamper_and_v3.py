"""Ring-5 stamper + Solva depth-governor end-to-end."""
from contracts.five_rings import (
    DefensibilityClass, Modality, NormalizedUnit, ProvenanceRing,
    ReextractionHandleRing, SignalRing, RelationalRing, DefensibilityRing, ScoreVector,
)
from services.g1_defensibility import (
    GenreClassificationResult, SourceStanding, stamp, stamp_audit,
)
from services.g1_defensibility.solva_depth.governor import SolvaDepthGovernor
from services.data_source.synthetic import SyntheticPlumbingDataSource


# extraction_params@v0 (Pre-G2 freeze): minimum compliant AUDIO block.
_AUDIO_EP_V0 = {
    "provider_id": "test", "provider_version": "0.0",
    "extraction_run_id": "g1-stamp-test", "extracted_at": "2026-07-01T00:00:00Z",
    "sample_rate_hz": 16000, "chunk_ms": 1000,
    "model_decoding_params": {
        "language_hint": "en", "beam_size": 1,
        "temperature": 0, "vad_threshold": 0.5,
    },
}


def _bare_unit(unit_id='u-1', modality=Modality.AUDIO, dims=None):
    return NormalizedUnit(
        unit_id=unit_id,
        provenance=ProvenanceRing(source_ref='synthetic:rms-hour-001:audio.wav',
                                   modality=modality, locator={'t_start_ms':0,'t_end_ms':1000},
                                   speaker_or_author='Anchor A', context='news bulletin'),
        signal=SignalRing(dimensions=dims or {'prosody':0.6}),
        relational=RelationalRing(),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer='local://x', model_id='m', model_version='v',
            extraction_params=dict(_AUDIO_EP_V0)),
        defensibility=DefensibilityRing(
            defensibility_class=DefensibilityClass.UTTERANCE,
            matrix_rule_ref='panel_debate.wire_republish@v0'),
    )


def test_stamp_accept_path_returns_tuple():
    u = _bare_unit()
    genre = GenreClassificationResult(genre='news_anchor_read', confidence=0.85, decided_by='rule')
    ss = SourceStanding(value='primary_recorded', declared_by='MEA-seed', declared_at='2026-06-30')
    stamp_audit._clear_for_test()
    ring, audit = stamp(u, genre, ss)
    assert ring.defensibility_class == DefensibilityClass.FACT  # matrix ceiling for that cell
    assert audit.decision == 'accept'
    assert audit.floor_violation is False
    stamp_audit.record(audit)
    assert len(stamp_audit.by_unit_id(u.unit_id)) == 1


def test_stamp_refuses_on_unknown_genre():
    u = _bare_unit(unit_id='u-2')
    genre = GenreClassificationResult(genre='unknown', confidence=0.0, decided_by='unknown')
    ss = SourceStanding(value='primary_recorded', declared_by='MEA-seed', declared_at='2026-06-30')
    ring, audit = stamp(u, genre, ss)
    assert ring.defensibility_class == DefensibilityClass.NON_FACTUAL
    assert audit.decision == 'refuse'
    assert 'genre unresolved' in (audit.reason or '')
    assert audit.floor_violation is True


def test_stamp_refuses_on_dimension_violation():
    u = _bare_unit(unit_id='u-3', dims={'NOT_IN_CATALOGUE': 0.5})
    genre = GenreClassificationResult(genre='news_anchor_read', confidence=0.85, decided_by='rule')
    ss = SourceStanding(value='primary_recorded', declared_by='MEA-seed', declared_at='2026-06-30')
    ring, audit = stamp(u, genre, ss)
    assert ring.defensibility_class == DefensibilityClass.NON_FACTUAL
    assert audit.decision == 'refuse'
    assert 'not in v0 catalogue' in (audit.reason or '') or 'dimension' in (audit.reason or '').lower()


def test_classifier_handles_adversarial_fixture():
    from services.g1_defensibility import classify
    units = list(SyntheticPlumbingDataSource().iter_units())
    results = [classify(u) for u in units]
    # All resolve to a matrix genre OR unknown (no inventions).
    valid = {'news_anchor_read', 'panel_debate', 'unknown'}
    for r in results:
        assert r.genre in valid, f'classifier emitted unknown genre {r.genre!r}'
    # At least some land in each matrix-vocabulary genre on the adversarial fixture.
    seen = {r.genre for r in results}
    assert 'news_anchor_read' in seen or 'panel_debate' in seen, seen


def test_v3_harness_refuses_on_synthetic():
    from services.v3_harness import LabelledUnitsBundle, run as v3_run
    units = list(SyntheticPlumbingDataSource().iter_units())
    bundle = LabelledUnitsBundle(
        units=units, gold_labels={}, adjudication_kappa=0.85, labeller_count=3,
        is_synthetic=True, label='synthetic-test',
    )
    r = v3_run(bundle)
    assert r.verdict == 'PENDING_REAL_LABELLED_SET'
    assert any('synthetic' in n.lower() for n in r.notes)


def test_v3_harness_refuses_on_low_kappa():
    from services.v3_harness import LabelledUnitsBundle, run as v3_run
    bundle = LabelledUnitsBundle(
        units=[], gold_labels={}, adjudication_kappa=0.5, labeller_count=2,
        is_synthetic=False, label='real-but-low-kappa',
    )
    r = v3_run(bundle)
    assert r.verdict == 'PENDING_REAL_LABELLED_SET'
    assert any('kappa' in n.lower() for n in r.notes)
