"""Composed-conclusion Condition B1 gate — LOAD-BEARING.

Gate 13 of the Phase 4b roster. Owner note (dispatch verbatim):
'AST-inspects `services/service_1/composed_conclusion.py`; only class-source
must be `from services.solva_depth.assertion import conclusion_class`;
grep-negative on `min(u.defensibility.defensibility_class` outside
`services/solva_depth/assertion.py`. Any recomputation site fails the gate.'

Mirrors A2's `supported_class` composition-time discipline applied to
`conclusion_class`: computed ONCE at the Solva boundary, THREADED through
the frozen envelope, NEVER recomputed downstream.

A2 lesson (BUILD_JOURNAL A2 D6a): recomputation is a review-on-sight
failure even if it happens to produce the same value.
"""
from __future__ import annotations

import ast
import inspect
import re
from pathlib import Path

from services.service_1 import composed_conclusion as cc_module
from services.solva_depth import assertion as solva_module


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


# The single-source-of-truth module for `conclusion_class` computation.
SOLVA_ASSERTION_PATH = Path(inspect.getfile(solva_module)).resolve()
COMPOSED_CONCLUSION_PATH = Path(inspect.getfile(cc_module)).resolve()


def test_composed_conclusion_class_from_solva_boundary_only():
    """LOAD-BEARING — Condition B1.

    Two-part inspection:

    Part A — AST inspection of composed_conclusion.py:
      * The module MUST import `conclusion_class` from
        `services.solva_depth.assertion` (as `_solva_conclusion_class`
        or under any name).
      * The module MUST NOT redefine a function or method named
        `conclusion_class` at any scope.

    Part B — Grep-negative across services/ + routers/:
      * The pattern `min(...defensibility_class...)` MUST NOT appear
        anywhere outside `services/solva_depth/assertion.py`.
      * The bare token `conclusion_class` may be REFERENCED anywhere
        (imports, function calls, docstrings) but MUST NOT appear as a
        function definition (`def conclusion_class(`) outside the
        canonical module.
    """
    # --- Part A: AST inspection of composed_conclusion.py ---
    tree = ast.parse(COMPOSED_CONCLUSION_PATH.read_text(encoding="utf-8"))

    # (a) imports `conclusion_class` from Solva.
    imports_solva_conclusion = False
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.module and "solva_depth.assertion" in node.module:
            for alias in node.names:
                if alias.name == "conclusion_class":
                    imports_solva_conclusion = True
                    break
    assert imports_solva_conclusion, (
        "Condition B1 violation — services/service_1/composed_conclusion.py "
        "does NOT import `conclusion_class` from "
        "services.solva_depth.assertion. The Solva boundary is the single "
        "authoritative computation site."
    )

    # (b) does NOT redefine `conclusion_class` locally.
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            assert node.name != "conclusion_class", (
                f"Condition B1 violation — composed_conclusion.py:{node.lineno} "
                f"redefines `conclusion_class` locally. That function may only "
                f"live in services/solva_depth/assertion.py."
            )

    # --- Part B: Grep-negative across services/ + routers/ ---
    forbidden_pattern = re.compile(
        r"min\s*\([^)]*\.defensibility(_class|\.defensibility_class)"
    )

    def_pattern = re.compile(r"^\s*def\s+conclusion_class\s*\(", re.MULTILINE)

    search_roots = [BACKEND_ROOT / "services", BACKEND_ROOT / "routers"]
    violations = []

    for root in search_roots:
        for py in root.rglob("*.py"):
            resolved = py.resolve()
            if resolved == SOLVA_ASSERTION_PATH:
                continue
            if "__pycache__" in str(py):
                continue
            text = py.read_text(encoding="utf-8")

            # min(...defensibility_class...) pattern outside Solva.
            for match in forbidden_pattern.finditer(text):
                line_no = text[:match.start()].count("\n") + 1
                violations.append(
                    f"{py.relative_to(BACKEND_ROOT)}:{line_no}: "
                    f"forbidden pattern `{match.group()!s}` — "
                    f"recomputation of conclusion class outside Solva boundary"
                )

            # `def conclusion_class(` outside Solva.
            for match in def_pattern.finditer(text):
                line_no = text[:match.start()].count("\n") + 1
                violations.append(
                    f"{py.relative_to(BACKEND_ROOT)}:{line_no}: "
                    f"`def conclusion_class(` outside canonical module"
                )

    assert not violations, (
        "Condition B1 LOAD-BEARING gate violation — conclusion-class "
        "recomputation site(s) detected outside "
        f"{SOLVA_ASSERTION_PATH.relative_to(BACKEND_ROOT)}:\n"
        + "\n".join(violations)
    )


def test_composed_conclusion_imports_solva_conclusion_class_by_reference():
    """Complementary AST check — the imported binding is actually used.

    The Ruling 4 shared-derivation pattern demands not just that the
    import exists, but that the imported binding is called somewhere.
    A dead import satisfies the letter of the rule but not its intent.
    """
    text = COMPOSED_CONCLUSION_PATH.read_text(encoding="utf-8")
    # Accept any name the import binds it to (own name or `_solva_...` etc.).
    tree = ast.parse(text)
    bound_name = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and "solva_depth.assertion" in node.module:
            for alias in node.names:
                if alias.name == "conclusion_class":
                    bound_name = alias.asname or "conclusion_class"
                    break
    assert bound_name is not None, "expected import already validated in prior test"

    call_pattern = re.compile(rf"\b{re.escape(bound_name)}\s*\(")
    assert call_pattern.search(text), (
        f"Condition B1 dead-import — `{bound_name}` is imported from Solva "
        f"but never called in composed_conclusion.py. Import must be USED, "
        f"not just present."
    )
