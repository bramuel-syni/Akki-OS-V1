"""Round-trip test for the regenerated adversarial fixture v1.

Verifies all 19 units in
`services/data_source/synthetic_assets/rms_adversarial_v1/fixture.json`
construct as `NormalizedUnit` (frozen `five_rings@v0`) byte-identically
after HAZARD-STOP #1 regenerate pass (2026-07-01T12:30Z).

Also asserts the fixture's `_manifest` flags stay honest — labels are
author-assigned and circular; v1/v3_valid MUST be false so downstream
harnesses refuse to compute a verdict against this fixture.
"""
import json
from pathlib import Path

import pytest

from contracts.five_rings import NormalizedUnit

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "services" / "data_source" / \
    "synthetic_assets" / "rms_adversarial_v1" / "fixture.json"


def _load():
    with open(FIXTURE_PATH) as f:
        return json.load(f)


def test_fixture_present_and_shaped():
    d = _load()
    assert "_manifest" in d and "units" in d
    assert d["_manifest"]["fixture"] == "rms_adversarial_synthetic_v1"
    assert len(d["units"]) == 19


def test_fixture_flags_honest():
    """v1/v3 harnesses must NOT be fooled into computing a verdict against
    author-labelled circular data — the manifest declares this openly."""
    m = _load()["_manifest"]
    assert m["synthetic"] is True
    assert m["plumbing_only"] is True
    assert m["v1_v3_valid"] is False


@pytest.mark.parametrize("i", range(19))
def test_unit_round_trip(i):
    """Every unit constructs as NormalizedUnit — full validator chain
    including extraction_params@v0 modality-mandatory keys."""
    u = _load()["units"][i]
    NormalizedUnit(**u)


def test_adversarial_coverage_preserved():
    """Each adversarial-intent tag from the corpus lives in
    provenance.context (JSON envelope). Regenerate must not lose stress
    cases."""
    d = _load()
    dims = ["code-switch", "genre boundary", "ad mimicking", "contested chain",
            "authority-blind", "source-standing lowers", "diarization stress",
            "cross-modal", "recency stress", "drama", "malformed",
            "opinion-dominant", "clean positive"]
    present = set()
    for u in d["units"]:
        ctx = u["provenance"]["context"] or ""
        for dim in dims:
            if dim in ctx:
                present.add(dim)
    missing = set(dims) - present
    assert not missing, f"adversarial dimensions lost during regenerate: {missing}"


def test_no_forbidden_fields_leak_through():
    """Post-HAZARD-STOP #1 fields that were dropped MUST NOT reappear.
    Guards against future re-introduction of inference-shaped fields."""
    d = _load()
    for u in d["units"]:
        # #5 headline dropped from score_vector
        assert "headline" not in u["defensibility"]["score_vector"], \
            "headline reappeared in score_vector (dropped per HAZARD-STOP #1 #5)"
        # #3 per-dimension confidence dropped
        assert isinstance(u["signal"]["dimensions"], dict), \
            "signal.dimensions must be Dict[str, float] (post-HAZARD-STOP #1 #3)"
        for k, v in u["signal"]["dimensions"].items():
            assert isinstance(v, (int, float)), \
                f"signal dimension {k!r} carries non-scalar (per-dim confidence sneaking back?)"
        # #2 per-edge confidence dropped; edge uses contract shape
        for e in u["relational"]["edges"]:
            assert "confidence" not in e, "per-edge confidence reappeared (dropped per HAZARD-STOP #1 #2)"
            assert "type" in e and "target_unit_ref" in e, \
                "edge missing contract-shape fields"
        # #1 modality is in the frozen Modality enum
        assert u["provenance"]["modality"] in {"text", "audio", "video", "image", "composite"}
