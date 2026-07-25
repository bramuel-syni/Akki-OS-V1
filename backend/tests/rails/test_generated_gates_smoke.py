"""G-13 Binding B-3 discharge · generated-gate import-and-invoke smoke cells (rails half).

Owner ruling verbatim (Binding B-3):
    "Every generated gate gets at least an import-and-invoke smoke cell
    inside the far-endpoint rail set, so generated code cannot rot as
    unexecuted text."

Regeneration-diff cells live at
`backend/tests/invariants/test_generated_gates_regeneration_diff.py`.
"""
from __future__ import annotations

import importlib
import pathlib

import pytest

from services.far_endpoint.gate_generator import GENERATED_GATES_DIR


def _generated_gate_modules():
    if not GENERATED_GATES_DIR.exists():
        return []
    return sorted(
        p.stem
        for p in GENERATED_GATES_DIR.glob("*.py")
        if p.name != "__init__.py"
    )


GENERATED_MODULE_STEMS = _generated_gate_modules()


@pytest.mark.parametrize("module_stem", GENERATED_MODULE_STEMS)
def test_b3_import_and_invoke_smoke(module_stem):
    """B-3: every generated gate module imports and every gate function invokes."""
    module_name = f"services.generated_gates.{module_stem}"
    module = importlib.import_module(module_name)
    gates = [
        getattr(module, name)
        for name in dir(module)
        if name.startswith("gate_") and callable(getattr(module, name))
    ]
    for gate in gates:
        result = gate({"smoke_payload": True})
        assert result is None or result is False or result is True, (
            f"B-3 smoke unexpected verdict from {gate.__name__}: {result!r}"
        )
