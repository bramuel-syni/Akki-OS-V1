"""Invariant: extraction_params@v0 content frozen.

Mirrors `test_signal_ring_dimensions_v0` pattern exactly. v0 is byte-
frozen; any edit MUST land as a new file (`v1.json`) + new snapshot,
NEVER as silent v0 mutation.
"""
import json
from pathlib import Path

from contracts.extraction_params import (
    EXTRACTION_PARAMS_V0,
    EXTRACTION_PARAMS_REV,
    reproducibility_keys,
)

SNAP = Path(__file__).parent / 'extraction_params.v0.content_snapshot.json'


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, indent=2)


def test_extraction_params_v0_content_frozen():
    expected = json.loads(SNAP.read_text())
    assert _canonical(EXTRACTION_PARAMS_V0) == _canonical(expected), (
        "extraction_params@v0 drift detected. Edit must land as v1.json, not v0 mutation."
    )


def test_extraction_params_v0_rev_label_matches():
    assert EXTRACTION_PARAMS_REV == "v0"
    assert EXTRACTION_PARAMS_V0["rev"] == "v0"


def test_reproducibility_keys_excludes_extracted_at():
    """Stakeholder correction #1: extracted_at is mandatory-yes, anchor-no.

    A timestamp records *when* a run happened — it does not *determine
    the output*. The V1 two-run comparison must use reproducibility
    keys (subset of mandatory) and must NEVER key on extracted_at.
    """
    for modality in ["audio", "video", "image", "text", "transcript", "composite"]:
        anchor_set = reproducibility_keys(modality)
        assert "extracted_at" not in anchor_set, (
            f"modality {modality!r}: extracted_at must NOT be a reproducibility anchor"
        )
        # Anchors must still include the base reproducibility-anchor BASE keys.
        for k in ("provider_id", "provider_version", "extraction_run_id"):
            assert k in anchor_set, f"modality {modality!r}: anchor set missing BASE key {k!r}"
