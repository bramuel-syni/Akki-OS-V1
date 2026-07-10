"""CD-G3 AST/reflection gate — no in-code hard-coded values bypass validators.

Owner ruling CD-E3 α + register-before-validate mechanism (2026-07-10):
CD-G3 stands as belt-and-suspenders alongside the runtime validators.

This gate walks `backend/services/census_dimensions/*.py` + any file that
imports from that package, and asserts that:
  * No string literal is passed directly as `content_surface=` or
    `genre=` keyword argument to `record_census_dimension(...)` from
    non-test code (i.e., no hard-coded fabrication in production paths).
  * No direct Mongo write path bypasses `record_census_dimension(...)`.

Rate class: reflection-gate (§6.10 · ~40 LoC/cell standalone).
"""
from __future__ import annotations

import ast
from pathlib import Path
from typing import List

BACKEND_ROOT = Path(__file__).resolve().parents[2]
CD_SERVICE_DIR = BACKEND_ROOT / "services" / "census_dimensions"
CD_ROUTER = BACKEND_ROOT / "routers" / "census_dimensions.py"

# Whitelist: files allowed to embed content_surface/genre string literals.
# (Test files + registry loader for internal error messages.)
_WHITELIST = {
    "tests/",
    "services/census_dimensions/dimensions_loader.py",  # error strings only
    "services/census_dimensions/dimensions_service.py",  # error strings only
    "services/census_dimensions/__init__.py",
    "routers/census_dimensions.py",  # kind route param, not a value
}


def _is_whitelisted(rel: str) -> bool:
    return any(w in rel for w in _WHITELIST)


def _find_call_kwarg_string_literals(tree: ast.AST) -> List[tuple]:
    """Find `record_census_dimension(...)` calls with string-literal
    content_surface / genre kwargs. Returns [(lineno, kwarg_name, value)]."""
    hits: List[tuple] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        # Match .record_census_dimension(...) OR record_census_dimension(...).
        target_name = None
        if isinstance(node.func, ast.Attribute):
            target_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            target_name = node.func.id
        if target_name != "record_census_dimension":
            continue
        for kw in node.keywords:
            if kw.arg in ("content_surface", "genre"):
                if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    hits.append((node.lineno, kw.arg, kw.value.value))
    return hits


def test_cd_g3_no_hardcoded_dimension_values_in_production_paths() -> None:
    """AST walker: no string-literal content_surface/genre in non-test call sites."""
    violations: List[str] = []
    for py in BACKEND_ROOT.rglob("*.py"):
        if "__pycache__" in py.parts or "site-packages" in py.parts:
            continue
        rel = str(py.relative_to(BACKEND_ROOT))
        if _is_whitelisted(rel):
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for lineno, kw_name, value in _find_call_kwarg_string_literals(tree):
            violations.append(
                f"{rel}:{lineno} — record_census_dimension({kw_name}={value!r}) "
                f"hard-codes a dimension value; must come from census-observed "
                f"input or be validated through validate_{'content_surface' if kw_name == 'content_surface' else 'genre'}(...)."
            )
    assert violations == [], (
        "CD-G3 VIOLATED: hard-coded dimension values in production paths.\n"
        "Owner CD-E3 α belt-and-suspenders: no in-code hard-coded values "
        "may bypass the register-before-validate + validate path.\n"
        "Violations:\n" + "\n".join(violations)
    )


def test_cd_g3_no_direct_mongo_write_bypasses_service() -> None:
    """AST walker: no `census_content_dimensions` collection write outside
    `dimensions_service.record_census_dimension`."""
    violations: List[str] = []
    for py in BACKEND_ROOT.rglob("*.py"):
        if "__pycache__" in py.parts or "site-packages" in py.parts:
            continue
        rel = str(py.relative_to(BACKEND_ROOT))
        # Whitelist: the service itself + server startup index creation + tests.
        if any(w in rel for w in [
            "tests/",
            "services/census_dimensions/dimensions_service.py",
            "server.py",  # startup index only
        ]):
            continue
        try:
            source_text = py.read_text(encoding="utf-8")
            tree = ast.parse(source_text)
        except (SyntaxError, UnicodeDecodeError):
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr not in ("insert_one", "update_one", "delete_one", "delete_many"):
                continue
            try:
                call_src = ast.get_source_segment(source_text, node) or ""
            except Exception:
                call_src = ""
            if "census_content_dimensions" in call_src:
                violations.append(
                    f"{rel}:{node.lineno} — direct Mongo write to "
                    f"census_content_dimensions bypasses record_census_dimension"
                )
    assert violations == [], (
        "CD-G3 VIOLATED: direct Mongo write bypasses census-dimensions service.\n"
        "Violations:\n" + "\n".join(violations)
    )
