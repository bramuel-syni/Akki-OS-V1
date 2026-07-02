"""Invariant: signal_ring_dimensions@v0 content frozen."""
import json
from pathlib import Path
from contracts.signal_ring import SIGNAL_RING_DIMENSIONS_V0

SNAP = Path(__file__).parent / 'signal_ring_dimensions.v0.content_snapshot.json'


def test_signal_ring_dimensions_v0_content_frozen():
    expected = json.loads(SNAP.read_text())
    actual = {'rev': 'v0', 'catalogue': SIGNAL_RING_DIMENSIONS_V0}
    assert json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True), (
        f'signal_ring_dimensions@v0 drift detected. Edit must land as v1.json, not v0 mutation.'
    )


def test_signal_ring_dimensions_v0_carries_stakeholder_corrections():
    cat = SIGNAL_RING_DIMENSIONS_V0
    # Correction 1: on_screen_text_present absent from VIDEO + IMAGE.
    assert 'on_screen_text_present' not in cat['video']
    assert 'on_screen_text_present' not in cat['image']
    # Correction 2: markedness, not intent.
    assert 'framing_markedness' in cat['video']
    assert 'composition_markedness' in cat['image']
    assert 'framing_intent' not in cat['video']
    assert 'composition_intent' not in cat['image']
    # Correction 3: COMPOSITE empty.
    assert cat['composite'] == []
