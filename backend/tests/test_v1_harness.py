"""V1 harness behaviour — Hard Rule 1 + PENDING on synthetic."""
from __future__ import annotations

import pytest

from services.v1_harness import HourBundle, HoursIdenticalError, run
from services.v1_harness.harness import last_report


def _bundle(label: str, audio: str, is_synthetic: bool) -> HourBundle:
    return HourBundle(
        audio_path=audio, gold_transcript_path=f"{audio}.vtt",
        gold_diarization_path=f"{audio}.dia", gold_entities_path=f"{audio}.ner",
        label=label, is_synthetic=is_synthetic,
    )


def test_harness_takes_two_named_parameters():
    """Hard Rule 1: spike_hour and production_hour are distinct named params."""
    import inspect
    sig = inspect.signature(run)
    assert "spike_hour" in sig.parameters
    assert "production_hour" in sig.parameters
    # Both must be keyword-only.
    assert sig.parameters["spike_hour"].kind == inspect.Parameter.KEYWORD_ONLY
    assert sig.parameters["production_hour"].kind == inspect.Parameter.KEYWORD_ONLY


def test_harness_refuses_identical_hours():
    b = _bundle("spike", "/tmp/hour-a.wav", is_synthetic=False)
    with pytest.raises(HoursIdenticalError):
        run(spike_hour=b, production_hour=b)


def test_harness_returns_pending_on_synthetic_only():
    b = _bundle("synthetic-plumbing", "/tmp/synthetic.wav", is_synthetic=True)
    report = run(spike_hour=b)
    assert report.verdict == "PENDING_REAL_MATERIAL"
    assert "synthetic" in " ".join(report.notes).lower()
    # last_report cached.
    cached = last_report()
    assert cached is report


def test_harness_spike_only_mode_works():
    """production_hour=None is the legitimate spike-only mode at G0.5."""
    b = _bundle("hour-a-real", "/tmp/hour-a-real.wav", is_synthetic=False)
    report = run(spike_hour=b, production_hour=None)
    assert report.verdict == "PENDING_REAL_MATERIAL"
    assert report.spike_hour_path == "/tmp/hour-a-real.wav"
    assert report.production_hour_path is None
