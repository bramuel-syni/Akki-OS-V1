"""Snapshot test: lift_manifest schema stays frozen.

Same discipline as the six frozen contract snapshots (five_rings@v0,
objective_request@v0, qualification_matrix@v0, signal_ring_dimensions@v0,
extraction_params@v0, northena_ledger_row@v0). Adding a new `lift_kind`
or changing the entry shape requires an explicit re-bless of the schema
snapshot — the manifest itself is treated as a contract.
"""
from __future__ import annotations

import json
from pathlib import Path

SNAPSHOT = Path(__file__).parent / "lift_manifest_schema.snapshot.json"
REPO_ROOT = Path(__file__).resolve().parents[3]  # /app
MANIFEST = REPO_ROOT / "docs" / "lift_manifest.json"


def _load_json(p: Path) -> dict:
    with open(p) as f:
        return json.load(f)


def test_lift_manifest_schema_frozen() -> None:
    """The frozen schema declares four permissible lift_kind values and
    the required entry shape. Any drift requires a re-bless."""
    schema = _load_json(SNAPSHOT)

    # Top-level shape stability.
    assert schema["title"] == "lift_manifest@v0"
    assert schema["properties"]["manifest_version"]["const"] == "v0"

    # The four lift_kinds — this is the enforced discipline surface.
    kinds = schema["properties"]["entries"]["items"]["properties"]["lift_kind"]["enum"]
    assert set(kinds) == {
        "direct",
        "transitive",
        "unverifiable-substrate-absent",
        "mandate-forced-net-new",
    }

    # Entry-level required fields.
    required = set(schema["properties"]["entries"]["items"]["required"])
    assert required == {"module", "shape_signature", "lift_kind", "resolves_by", "notes"}

    # resolves_by must be non-empty (per Condition 1: prose descriptions
    # with no concrete search terms are unresolvable-by-construction).
    resolves_by = schema["properties"]["entries"]["items"]["properties"]["resolves_by"]
    assert resolves_by["minItems"] == 1
    assert resolves_by["items"]["minLength"] == 1

    # notes must be non-empty (per Condition 2: silent gaps are the
    # failure mode the guard exists to catch).
    notes = schema["properties"]["entries"]["items"]["properties"]["notes"]
    assert notes["minLength"] == 1


def test_manifest_conforms_to_schema() -> None:
    """Structural conformance: every entry in the live manifest has the
    keys the frozen schema requires."""
    schema = _load_json(SNAPSHOT)
    manifest = _load_json(MANIFEST)

    required_top = schema["required"]
    for k in required_top:
        assert k in manifest, f"manifest missing top-level {k!r}"

    required_entry = set(schema["properties"]["entries"]["items"]["required"])
    allowed_kinds = set(schema["properties"]["entries"]["items"]["properties"]["lift_kind"]["enum"])
    for e in manifest["entries"]:
        missing = required_entry - set(e.keys())
        assert not missing, f"entry {e.get('module')!r} missing required fields {missing}"
        assert e["lift_kind"] in allowed_kinds, (
            f"entry {e['module']!r} has invalid lift_kind {e['lift_kind']!r}"
        )
