"""Grain-compat single-source-of-truth invariant — Phase 4a landing.

Mirror of `test_floor_feasibility_shared_derivation.py`. Enforces that
`services/service_1/grain_compatibility.py::evaluate_grain_form` is the
ONLY grain-form compatibility evaluation site in the codebase.
Reimplementation outside this module — even with equal outputs — fails
review on sight (Ruling 4 shared-derivation pattern).

Failure mode this prevents: Phase 7 wizard implementing its own
grain-compat table with different rules or messages, silently diverging
from Phase 4a's admission-time rules. Second computation-path is the
A2 `supported_class` lesson applied at rule-surface level.

Also houses:
  * Matrix exhaustiveness (schema-freeze equivalent for the rule surface).
  * Path-forward actor-appropriate discipline (Condition 3 grep-negative).
  * Ruling 5 fold-in — MODEL cells populated with non-empty path_forward
    tracking `admission_refusal.emit_form_not_offerable`'s string
    (defense-in-depth for unreachable cells).
"""
from __future__ import annotations

import ast
import inspect
from pathlib import Path

from services.service_1 import grain_compatibility as canonical_module
from services.service_1 import admission_refusal as ar_module


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


def test_grain_compatibility_shared_source_of_truth():
    """AST-inspect all .py files under services/ + routers/ (excluding
    the canonical module itself). No file may declare a dict whose keys
    are `(OutputForm.*, OutputGrain.*)` tuples — that pattern is the
    local-rule-table signal."""

    canonical_path = Path(inspect.getfile(canonical_module)).resolve()
    violations = []

    search_roots = [BACKEND_ROOT / "services", BACKEND_ROOT / "routers"]
    for root in search_roots:
        for py in root.rglob("*.py"):
            if py.resolve() == canonical_path:
                continue
            if "__pycache__" in str(py):
                continue

            text = py.read_text(encoding="utf-8")
            if "OutputForm" not in text or "OutputGrain" not in text:
                continue

            try:
                tree = ast.parse(text)
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if not isinstance(node, ast.Dict):
                    continue
                for key in node.keys:
                    if not isinstance(key, ast.Tuple) or len(key.elts) != 2:
                        continue
                    a, b = key.elts
                    if (isinstance(a, ast.Attribute) and isinstance(b, ast.Attribute)
                        and getattr(a.value, "id", "") == "OutputForm"
                        and getattr(b.value, "id", "") == "OutputGrain"):
                        violations.append(
                            f"{py.relative_to(BACKEND_ROOT)}:{key.lineno}: "
                            f"(OutputForm.*, OutputGrain.*) dict-key detected; "
                            f"Ruling 4 shared-derivation violated"
                        )
                        break

    assert not violations, (
        "Grain-compat rule reimplementation detected outside canonical "
        f"module {canonical_path.relative_to(BACKEND_ROOT)}. "
        "Ruling 4 shared-derivation demands single-source-of-truth for "
        "grain-form compatibility evaluation.\n" + "\n".join(violations)
    )


def test_grain_compat_single_source_of_truth():
    """Gate 2 alias — the canonical `evaluate_grain_form` is defined at
    exactly the canonical path and importable."""
    canonical = BACKEND_ROOT / "services" / "service_1" / "grain_compatibility.py"
    assert canonical.exists()
    from services.service_1.grain_compatibility import evaluate_grain_form
    assert evaluate_grain_form.__module__ == "services.service_1.grain_compatibility"


def test_grain_compatibility_matrix_is_exhaustive():
    """Matrix must cover ALL (OutputForm, OutputGrain) combinations."""
    from contracts.objective_request_v2 import OutputForm, OutputGrain
    expected = {(f, g) for f in OutputForm for g in OutputGrain}
    actual = set(canonical_module._MATRIX.keys())
    missing = expected - actual
    extra = actual - expected
    assert not missing, f"Matrix missing combinations: {missing}"
    assert not extra, f"Matrix has extra keys not in enum product: {extra}"


def test_grain_compat_path_forward_actor_appropriate():
    """Condition 3 (Phase 3): path_forward strings NEVER surface owner-side
    deliberations. Grep-negative on 4 forbidden phrases across all
    non-empty path_forward entries in the matrix."""
    forbidden = ["await owner", "owner acceptance", "ingredient manifest", "ingredient-manifest"]
    for (form, grain), result in canonical_module._MATRIX.items():
        pf = result.path_forward or ""
        pf_lower = pf.lower()
        for phrase in forbidden:
            assert phrase not in pf_lower, (
                f"({form.value}, {grain.value}) path_forward contains owner-side "
                f"deliberation phrase {phrase!r}: {pf!r}"
            )


def test_grain_compat_incompatible_cells_have_non_empty_path_forward():
    """Ruling 5 (Phase 4a Stage B, 2026-07-03) fold-in.

    Every cell with `compatible=False` must carry a non-empty
    `path_forward` string. Defense-in-depth: even the UNREACHABLE MODEL
    cells (refused upstream in Phase 3 dispatch by
    `emit_form_not_offerable` before grain-compat is consulted) must
    speak actor-appropriate direction if ever reached.
    """
    from contracts.objective_request_v2 import OutputForm
    for (form, grain), result in canonical_module._MATRIX.items():
        if result.compatible:
            continue
        assert result.path_forward is not None, (
            f"({form.value}, {grain.value}) is compatible=False but "
            f"path_forward is None — Ruling 5 violation."
        )
        assert len(result.path_forward.strip()) > 0, (
            f"({form.value}, {grain.value}) is compatible=False but "
            f"path_forward is empty — Ruling 5 violation."
        )
        # MODEL cells specifically must track admission_refusal.emit_form_not_offerable's
        # actor-appropriate string (Ruling 5 pre-commitment).
        if form == OutputForm.MODEL:
            expected = ar_module._WHAT_YOU_CAN_DO_FORM_NOT_OFFERABLE
            assert result.path_forward == expected, (
                f"({form.value}, {grain.value}) MODEL-cell path_forward does "
                f"not match emit_form_not_offerable's actor string.\n"
                f"  expected: {expected!r}\n"
                f"  actual:   {result.path_forward!r}"
            )
