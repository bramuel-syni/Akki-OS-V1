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

    Phase 5 Stage B (2026-07-04): parity count bumped 18 → 20 (added
    NorthenaLedgerRow_v1 + AsyncDeliveryAccepted_v0). This test's
    assertion updated to 20 to remain compatible; the underlying
    Phase-4b-composed_conclusion snapshot is still present.

    Phase 6 Stage B (2026-07-04): parity count bumped 20 → 22 (added
    QuoteEnvelope_v0 + AsyncDeliveryAccepted_v1). Same additive
    pattern; underlying Phase-4b-composed_conclusion snapshot present.
    """
    invariants_dir = Path(__file__).parent
    snapshots = list(invariants_dir.glob("*.contract_snapshot.json"))
    assert len(snapshots) == 22, (
        f"Post-Phase-6-Stage-B snapshot count must be exactly 22 "
        f"(20 pre-6b + QuoteEnvelope_v0 + AsyncDeliveryAccepted_v1). "
        f"Actual: {len(snapshots)}.\nSnapshots: {sorted(p.name for p in snapshots)}"
    )
