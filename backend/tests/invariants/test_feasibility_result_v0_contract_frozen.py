"""FeasibilityResult v0 — frozen contract invariant.

Guards the Phase 1 addition landing at 16th freeze.

Elevated doctrine: validation surface IS contract surface. Any
`model_validator`, `Config` change, or import-time schema mutation on
this contract requires an explicit re-snapshot bless.
"""
import json
from pathlib import Path

from contracts.feasibility_result import FeasibilityResult_v0

SNAP = Path(__file__).parent / "feasibility_result.contract_snapshot.json"


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, indent=2)


def test_feasibility_result_v0_contract_frozen():
    """`FeasibilityResult_v0.model_json_schema()` matches byte-frozen snapshot."""
    expected = json.loads(SNAP.read_text())
    actual = FeasibilityResult_v0.model_json_schema()
    assert _canonical(actual) == _canonical(expected), (
        "FeasibilityResult_v0 schema drift. Any additive change requires "
        "a new contract file (v1) OR an explicit re-snapshot bless of this "
        "one — never a silent snapshot rewrite. See module HAZARD-STOP-NOTES "
        "for owner-owned narrowing points if any land."
    )
