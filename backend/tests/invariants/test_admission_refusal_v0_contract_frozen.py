"""AdmissionRefusal@v0 contract-frozen snapshot invariant — Phase 3.

17th frozen contract. Snapshot bijection enforced by
`test_frozen_contract_snapshot_parity.py`.
"""
from __future__ import annotations

import json
from pathlib import Path

from contracts.admission_refusal import AdmissionRefusal_v0


SNAPSHOT_PATH = (
    Path(__file__).parent / "admission_refusal.contract_snapshot.json"
)


def test_admission_refusal_v0_contract_frozen():
    """Live schema matches the on-disk canonical snapshot byte-for-byte."""
    live = AdmissionRefusal_v0.model_json_schema()
    stored = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    assert live == stored, (
        f"AdmissionRefusal@v0 schema drift detected.\n"
        f"Regenerate snapshot ONLY under an explicit owner ruling that "
        f"acknowledges a governed field-shape change.\n"
        f"Live schema keys: {sorted(live.get('properties', {}).keys())}\n"
        f"Stored keys:      {sorted(stored.get('properties', {}).keys())}"
    )
