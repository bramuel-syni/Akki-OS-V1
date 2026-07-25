"""G-13 Binding B-3 discharge · generated-gate regeneration-diff (invariants half).

Owner ruling verbatim (Binding B-3):
    "Same regeneration-diff regime as B-2 — generated gates are never
    hand-edited; a needed change lands at the mandate source and flows
    through the emitter."

Smoke-cell family (import-and-invoke) lives at
`backend/tests/rails/test_generated_gates_smoke.py` per Owner-verbatim
placement discipline.
"""
from __future__ import annotations

import pathlib

import pytest

from services.far_endpoint.gate_generator import (
    GENERATED_GATES_DIR,
    render_gate_module,
)
from services.far_endpoint.mandate_reader import list_mandate_paths, parse_mandate
from services.far_endpoint.mandate_spec_emitter import emit_mandate_spec


def test_b3_regeneration_diff_all_gates():
    """B-3 hard-fail: every on-disk generated gate module byte-matches fresh generator output."""
    assert GENERATED_GATES_DIR.exists(), f"B-3: {GENERATED_GATES_DIR} missing"
    for mandate_path in list_mandate_paths():
        parsed = parse_mandate(mandate_path)
        spec = emit_mandate_spec(parsed)
        fresh_module = render_gate_module(spec)
        on_disk_path = GENERATED_GATES_DIR / f"{spec.spec_id}.py"
        assert on_disk_path.exists(), (
            f"B-3 hard-fail: on-disk gate module missing for mandate "
            f"{mandate_path.name}: {on_disk_path}"
        )
        on_disk_text = on_disk_path.read_text()
        assert on_disk_text == fresh_module, (
            f"B-3 hard-fail: regeneration diff at {on_disk_path.name}. "
            f"Generated code hand-edited (never permitted)."
        )


def test_b3_generated_do_not_edit_header_present():
    """B-3: every generated .py carries the do-not-edit header."""
    for py_path in sorted(GENERATED_GATES_DIR.glob("*.py")):
        if py_path.name == "__init__.py":
            continue
        text = py_path.read_text()
        assert text.startswith("# GENERATED · DO NOT EDIT"), (
            f"B-3 hard-fail: {py_path.name} missing generated-do-not-edit header"
        )
        for required in ("# Source:", "# Source SHA-256:", "# Generator:", "# Regenerate:"):
            assert required in text[:400], (
                f"B-3 hard-fail: {py_path.name} missing required header line '{required}'"
            )
