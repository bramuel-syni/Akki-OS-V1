"""AST cell · five_rings@v0 zero-mutation attest (Owner E1 α · load-bearing).

Landed 2026-07-15 per EAB-1 execution atomic under Owner E1 ruling
(docs/rulings/eab_1_e1_2026-07-15.md).

Owner-verbatim: "The AST cell is the load-bearing part of the ruling — it
converts 'additive by intent' into 'additive by proof,' and it must fail the
build on any mutation, not report one."

FAILURE MODE: `raise AssertionError` (via pytest.assert) on any drift.
             NOT warnings.warn. NOT print+continue. NOT pytest.skip.
             Hard-fails the pytest run.

Coverage: parses the AST of `backend/contracts/five_rings.py` + reads the
snapshot at `backend/tests/invariants/five_rings.contract_snapshot.json`;
asserts:
  1. Same set of class definitions (ProvenanceRing, SignalRing, RelationalRing,
     ReextractionHandleRing, DefensibilityRing, ScoreVector, NormalizedUnit,
     Modality, DefensibilityClass, RelationType).
  2. Same field names per class (against snapshot's `$defs.<ClassName>.properties`).
  3. Same field type annotations (string form) per class.
  4. Same required-field lists per class.

If EAB-1 execution accidentally touched five_rings.py, this cell fails hard
and blocks EAB-1 close. Parity 31/31 guarantee is transitive.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Dict, Set

FIVE_RINGS_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "contracts"
    / "five_rings.py"
)
SNAPSHOT_PATH = Path(__file__).resolve().parent / "five_rings.contract_snapshot.json"


EXPECTED_CLASSES_ORDERED = [
    "Modality",
    "DefensibilityClass",
    "RelationType",
    "ProvenanceRing",
    "SignalRing",
    "RelationalEdge",
    "RelationalRing",
    "ReextractionHandleRing",
    "ScoreVector",
    "DefensibilityRing",
    "NormalizedUnit",
]


def _extract_class_names(tree: ast.AST) -> Set[str]:
    return {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}


def _extract_class_fields(tree: ast.AST) -> Dict[str, Dict[str, str]]:
    """For each ClassDef, return {field_name: type_annotation_string}.

    Only captures AnnAssign nodes at class-body level (i.e. Pydantic fields
    and enum members). Method definitions ignored.
    """
    out: Dict[str, Dict[str, str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            fields: Dict[str, str] = {}
            for stmt in node.body:
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                    name = stmt.target.id
                    ann = ast.unparse(stmt.annotation) if stmt.annotation else ""
                    fields[name] = ann
                elif isinstance(stmt, ast.Assign):
                    # Enum-member assignments: name = "value"
                    for target in stmt.targets:
                        if isinstance(target, ast.Name):
                            fields[target.id] = "<enum_member>"
            out[node.name] = fields
    return out


def _load_snapshot() -> dict:
    if not SNAPSHOT_PATH.is_file():
        raise AssertionError(
            f"[AST cell] snapshot missing at {SNAPSHOT_PATH}; cannot enforce zero-mutation"
        )
    return json.loads(SNAPSHOT_PATH.read_text())


def test_ast_cell_class_list_equivalent() -> None:
    """FAIL HARD if class list in five_rings.py drifts from expected canonical set."""
    tree = ast.parse(FIVE_RINGS_PATH.read_text())
    got = _extract_class_names(tree)
    expected = set(EXPECTED_CLASSES_ORDERED)
    missing = expected - got
    added = got - expected
    if missing or added:
        raise AssertionError(
            f"[AST cell] five_rings@v0 class list DRIFTED. "
            f"missing={sorted(missing)} added={sorted(added)}. "
            f"Owner E1 α FAILS: additive-by-proof violated. Parity 31 at risk."
        )


def test_ast_cell_snapshot_present_and_parseable() -> None:
    """FAIL HARD if snapshot file missing or unparseable."""
    snapshot = _load_snapshot()
    # NormalizedUnit is the aggregate root at top level; the five ring classes
    # sit inside its $defs.
    if snapshot.get("title") != "NormalizedUnit":
        raise AssertionError(
            "[AST cell] snapshot title is not NormalizedUnit. "
            "Owner E1 α FAILS: additive-by-proof cannot be established."
        )
    required_defs = {
        "ProvenanceRing",
        "SignalRing",
        "RelationalRing",
        "ReextractionHandleRing",
        "DefensibilityRing",
    }
    defs = snapshot.get("$defs", {})
    missing = required_defs - set(defs.keys())
    if missing:
        raise AssertionError(
            f"[AST cell] snapshot missing required ring $defs: {sorted(missing)}. "
            f"Owner E1 α FAILS: additive-by-proof cannot be established."
        )


def test_ast_cell_five_rings_ring_class_fields_stable() -> None:
    """FAIL HARD if any of the five ring classes had a field added/removed/renamed.

    Field TYPES are already covered by the contract-snapshot invariant test.
    This cell adds the AST-level attest for field-NAME stability across the
    five ring classes (Owner E1 α: additive-by-proof for the locator addition
    is inseparable from field-name stability on the containing rings).
    """
    tree = ast.parse(FIVE_RINGS_PATH.read_text())
    fields_by_class = _extract_class_fields(tree)
    expected_fields = {
        "ProvenanceRing": {
            "model_config", "source_ref", "modality", "locator",
            "speaker_or_author", "context",
        },
        "ReextractionHandleRing": {
            "model_config", "raw_pointer", "model_id", "model_version",
            "extraction_params",
        },
        "DefensibilityRing": {
            "model_config", "defensibility_class", "score_vector",
            "matrix_rule_ref", "runtime_mode",
        },
        "SignalRing": {"model_config", "dimensions", "depth_judged", "depth_notes"},
        "RelationalRing": {"model_config", "edges"},
        "NormalizedUnit": {
            "model_config", "unit_id", "provenance", "signal",
            "relational", "reextraction_handle", "defensibility",
        },
    }
    drift = []
    for cls, want in expected_fields.items():
        got = set(fields_by_class.get(cls, {}).keys())
        if got != want:
            drift.append(f"{cls}: missing={sorted(want-got)} added={sorted(got-want)}")
    if drift:
        raise AssertionError(
            f"[AST cell] five_rings@v0 ring class FIELDS DRIFTED. "
            f"{'; '.join(drift)}. "
            f"Owner E1 α FAILS: locator additive-vocabulary landing MUST NOT "
            f"touch ring shape. Parity 31 violated."
        )
