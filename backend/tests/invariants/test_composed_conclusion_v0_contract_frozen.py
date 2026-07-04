"""ComposedConclusion@v0 contract-frozen snapshot invariant — Phase 4b.

18th frozen contract. Snapshot bijection enforced by
`test_frozen_contract_snapshot_parity.py`.

Gate 12 in the Phase 4b close roster.
"""
from __future__ import annotations

import json
from pathlib import Path

from contracts.composed_conclusion import ComposedConclusion_v0


SNAPSHOT_PATH = (
    Path(__file__).parent / "composed_conclusion.contract_snapshot.json"
)


def test_composed_conclusion_v0_contract_frozen():
    """Live schema matches the on-disk canonical snapshot byte-for-byte."""
    live = ComposedConclusion_v0.model_json_schema()
    stored = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    assert live == stored, (
        f"ComposedConclusion@v0 schema drift detected.\n"
        f"Regenerate snapshot ONLY under an explicit owner ruling that "
        f"acknowledges a governed field-shape change.\n"
        f"Live schema keys: {sorted(live.get('properties', {}).keys())}\n"
        f"Stored keys:      {sorted(stored.get('properties', {}).keys())}"
    )


def test_composed_conclusion_snapshot_parity_at_18():
    """Snapshot inventory bumped 17 → 18 at Phase 4b landing.

    Gate 19 of the Phase 4b roster. Complements the three parity tests
    in `test_frozen_contract_snapshot_parity.py` by asserting the
    absolute count invariant at Phase 4b close.
    """
    invariants_dir = Path(__file__).parent
    snapshots = list(invariants_dir.glob("*.contract_snapshot.json"))
    assert len(snapshots) == 18, (
        f"Post-Phase-4b snapshot count must be exactly 18 "
        f"(17 pre-4b + 1 ComposedConclusion_v0). Actual: {len(snapshots)}.\n"
        f"Snapshots: {sorted(p.name for p in snapshots)}"
    )
