"""Content-freeze invariants for the three backfilled canonical
`*.contract_snapshot.json` files landed in Substrate-Drop v2, Part 1.

Landed 2026-07-03 per owner ruling Path B. Term 1 (freeze-as-found) —
each backfill snapshot is byte-identical to the existing legacy-named
snapshot artifact captured at the same time (`.content_snapshot.json`
for the two catalogue-based contracts, `.schema_snapshot.json` for the
qualification_matrix Pydantic-shape).

These tests independently guard the canonical `.contract_snapshot.json`
against source drift. The legacy invariant tests
(`test_extraction_params_v0`, `test_signal_ring_dimensions_v0`, plus the
qualification_matrix schema invariant in `test_invariant_contract_snapshots`)
remain in place and untouched.
"""
import json
from pathlib import Path

from contracts.extraction_params import EXTRACTION_PARAMS_V0
from contracts.signal_ring import SIGNAL_RING_DIMENSIONS_V0
from contracts.qualification_matrix.loader import QualificationMatrix

SNAP_DIR = Path(__file__).parent


def _canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, indent=2)


def test_extraction_params_contract_frozen():
    """Canonical `.contract_snapshot.json` freeze on the v0 catalogue.

    Mirrors `test_extraction_params_v0_content_frozen` in content; guards
    the canonical-name snapshot separately.
    """
    expected = json.loads((SNAP_DIR / "extraction_params.contract_snapshot.json").read_text())
    assert _canonical(EXTRACTION_PARAMS_V0) == _canonical(expected), (
        "extraction_params drift on canonical snapshot. Edit must land as a "
        "new rev (v1.json + fresh snapshot), never as v0 mutation."
    )


def test_signal_ring_contract_frozen():
    """Canonical `.contract_snapshot.json` freeze on the v0 dimension catalogue.

    Term 3 (transitive-protection note): the Pydantic `SignalRing` model
    shape is already embedded in `five_rings.contract_snapshot.json` via
    `$defs.SignalRing`. This snapshot covers the domain-specific
    dimension catalogue (which is not part of the Pydantic shape).
    """
    expected = json.loads((SNAP_DIR / "signal_ring.contract_snapshot.json").read_text())
    actual = {"rev": "v0", "catalogue": SIGNAL_RING_DIMENSIONS_V0}
    assert _canonical(actual) == _canonical(expected), (
        "signal_ring dimension-catalogue drift on canonical snapshot. "
        "Edit must land as a new rev, never as v0 mutation."
    )


def test_qualification_matrix_contract_frozen():
    """Canonical `.contract_snapshot.json` freeze on the Pydantic SHAPE only.

    Term 2 (shape not values): the Qualification Matrix rules live in
    `contracts/qualification_matrix/v0.json` and are ADMINISTRABLE (bump
    to v1.json for a new taxonomy bless). This snapshot freezes the
    Pydantic schema — the CONTRACT SHAPE — not the rule VALUES. Value
    freeze is captured separately in the legacy
    `qualification_matrix.v0.content_snapshot.json` as a v0-rev
    provenance guarantee.
    """
    expected = json.loads((SNAP_DIR / "qualification_matrix.contract_snapshot.json").read_text())
    actual = QualificationMatrix.model_json_schema()
    assert _canonical(actual) == _canonical(expected), (
        "qualification_matrix Pydantic SHAPE drift on canonical snapshot. "
        "Any schema change requires an explicit re-snapshot bless."
    )
