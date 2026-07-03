"""ObjectiveRequest v2 — frozen contract invariant.

Guards the Phase 0 addition landing at Substrate-Drop v2, Part 2.

v0 (`contracts/objective_request.py`) remains byte-identical; its
existing invariant test in `test_invariant_contract_snapshots.py`
continues to guard it independently.

Elevated doctrine (Substrate-Drop v2 Standing Owner Disposition):
validation surface IS contract surface. Any `model_validator`, Config
change, or import-time schema mutation on this contract requires an
explicit re-snapshot bless.
"""
import json
from pathlib import Path

from contracts.objective_request_v2 import ObjectiveRequest_v2

SNAP = Path(__file__).parent / "objective_request_v2.contract_snapshot.json"


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, indent=2)


def test_objective_request_v2_contract_frozen():
    """`ObjectiveRequest_v2.model_json_schema()` matches byte-frozen snapshot."""
    expected = json.loads(SNAP.read_text())
    actual = ObjectiveRequest_v2.model_json_schema()
    assert _canonical(actual) == _canonical(expected), (
        "ObjectiveRequest_v2 schema drift. Any additive change requires a "
        "new contract file (v3) OR an explicit re-snapshot bless of this "
        "one — never a silent snapshot rewrite. See module HAZARD-STOP-NOTES "
        "for owner-owned type-narrowing points."
    )
