"""Floor-feasibility SINGLE-SOURCE-OF-TRUTH invariant.

Owner Ruling 4 (Substrate-Drop v2 → Phase 1 dispatch, 2026-07-03):
`derive_floor_feasibility` in `services/mtafiti/floor_feasibility.py` is
the ONE shared function both consumers (wizard + admission) import.
Reimplementation per consumer fails review regardless of output equality.

Two guards land here:

  1. **Positive** — `derive_floor_feasibility` is defined at exactly one
     path. Import from anywhere resolves to that one function.

  2. **Regression sweep** — grep the codebase for any pattern that
     recomputes floor-feasibility outside
     `services/mtafiti/floor_feasibility.py`. Fail on any hit under
     `services/service_1/`, `services/northena/`, `services/targeta/`,
     `services/mtafiti/` (excluding floor_feasibility.py itself), or
     `routers/`. Three grep-negative patterns enumerated as constants
     below; violations are flagged with file + line.

Wizard/admission callers do not exist yet (future phases). This test
asserts the SINGLE-SOURCE invariant NOW so future phases cannot silently
drift.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import List, Set, Tuple

BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend
CANONICAL_MODULE = "services/mtafiti/floor_feasibility.py"
CANONICAL_FN_NAME = "derive_floor_feasibility"


# Grep-negative patterns — three regexes that catch known reimplementation shapes.
# If any of these fire OUTSIDE the canonical module, the invariant fails.
REIMPLEMENTATION_PATTERNS: List[Tuple[str, str]] = [
    (
        "class_distribution_and_floor_in_same_function",
        # Reads a `class_distribution` attribute AND a `minimum_class` / `defensibility_floor`
        # reference within the same file. Naive proxy for "recomputes here".
        r"\bclass_distribution\b.*\bminimum_class\b|\bminimum_class\b.*\bclass_distribution\b",
    ),
    (
        "class_ordinal_comparison_with_floor",
        # Comparing an ordinal derived from DefensibilityClass against a floor's minimum_class ordinal.
        # Any file matching this outside the canonical module is doing floor-arithmetic locally.
        r"_CLASS_ORDER\[.*\]\s*[<>=]+.*_CLASS_ORDER\[.*\.minimum_class",
    ),
    (
        "feasibility_boolean_derived_locally",
        # A local variable / assignment named 'feasible' or 'floor_feasibility_*' being computed
        # via a comparison. Catches the "if class_count >= floor_threshold: feasible = True" shape.
        r"\bfeasible\s*=\s*.*[<>=]|\bfloor_feasibility_\w+\s*=\s*.*[<>=]",
    ),
]


# Directories to sweep. Canonical module is EXPLICITLY excluded.
SWEEP_DIRS: List[str] = [
    "services/service_1",
    "services/northena",
    "services/targeta",
    "services/mtafiti",   # excludes floor_feasibility.py itself
    "routers",
]

# Files to explicitly exclude from the sweep (canonical + this test itself + tests).
EXCLUDED_PATHS: Set[str] = {
    "services/mtafiti/floor_feasibility.py",
}


def _iter_py_files() -> List[Path]:
    files: List[Path] = []
    for d in SWEEP_DIRS:
        base = BACKEND_ROOT / d
        if not base.exists():
            continue
        for py in base.rglob("*.py"):
            rel = py.relative_to(BACKEND_ROOT).as_posix()
            if rel in EXCLUDED_PATHS:
                continue
            if "__pycache__" in rel:
                continue
            files.append(py)
    return files


def test_canonical_derive_function_exists():
    """Positive: derive_floor_feasibility is defined at exactly the canonical path."""
    canonical = BACKEND_ROOT / CANONICAL_MODULE
    assert canonical.exists(), f"Canonical module missing at {canonical}"
    text = canonical.read_text(encoding="utf-8")
    assert re.search(rf"^def {CANONICAL_FN_NAME}\b", text, re.MULTILINE), \
        f"Canonical function `{CANONICAL_FN_NAME}` not defined at {CANONICAL_MODULE}"


def test_canonical_derive_function_importable():
    """Positive: importing derive_floor_feasibility works and resolves to canonical module."""
    from services.mtafiti.floor_feasibility import derive_floor_feasibility
    assert derive_floor_feasibility.__module__ == "services.mtafiti.floor_feasibility"


def test_no_reimplementation_of_floor_feasibility_outside_canonical():
    """Regression sweep — no file outside the canonical module recomputes floor-feasibility.

    Enumerates three grep-negative patterns (see REIMPLEMENTATION_PATTERNS)
    and asserts no hit under any of the SWEEP_DIRS.

    Ruling 4 rationale: even if outputs are equal, reimplementing the
    derivation elsewhere fails review. Two consumers computing
    independently is a second-computation-path — the A2 `supported_class`
    lesson exactly.
    """
    violations: List[str] = []
    for f in _iter_py_files():
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(BACKEND_ROOT).as_posix()
        for pattern_name, pattern_re in REIMPLEMENTATION_PATTERNS:
            for match in re.finditer(pattern_re, text):
                # Compute 1-indexed line number of the match
                line_no = text[:match.start()].count("\n") + 1
                violations.append(
                    f"  {rel}:{line_no} — pattern {pattern_name!r} matched: "
                    f"{match.group(0)[:80]!r}"
                )
    assert not violations, (
        "Ruling 4 violation — floor-feasibility recomputation outside "
        "canonical `services/mtafiti/floor_feasibility.py`. Callers "
        "MUST import `derive_floor_feasibility`; reimplementation is a "
        "second-computation-path (the A2 supported_class lesson):\n"
        + "\n".join(violations)
    )


def test_derive_floor_feasibility_is_deterministic_and_pure():
    """Same inputs → same output. No side effects. Objective-blind."""
    from contracts.feasibility_result import ClassDistribution
    from contracts.five_rings import DefensibilityClass
    from contracts.objective_request import DefensibilityFloor
    from services.mtafiti.floor_feasibility import derive_floor_feasibility

    dist = ClassDistribution(fact=3, utterance=5, non_factual=2)
    floor_utterance = DefensibilityFloor(minimum_class=DefensibilityClass.UTTERANCE)

    out1 = derive_floor_feasibility(dist, floor_utterance)
    out2 = derive_floor_feasibility(dist, floor_utterance)
    assert out1 == out2, "derive_floor_feasibility must be deterministic"

    # Feasibility at UTTERANCE floor: fact(3) + utterance(5) = 8 units at or above.
    assert out1["feasible"] is True
    assert out1["qualifying_at_floor"] == 8
    assert out1["qualifying_below_floor"] == 2
    assert out1["requested_minimum_class"] == "utterance"

    # Raise the floor to FACT: only fact(3) qualifies.
    floor_fact = DefensibilityFloor(minimum_class=DefensibilityClass.FACT)
    out3 = derive_floor_feasibility(dist, floor_fact)
    assert out3["feasible"] is True
    assert out3["qualifying_at_floor"] == 3
    assert out3["qualifying_below_floor"] == 7

    # Infeasible case: floor FACT, distribution has zero facts.
    dist2 = ClassDistribution(fact=0, utterance=5, non_factual=2)
    out4 = derive_floor_feasibility(dist2, floor_fact)
    assert out4["feasible"] is False
    assert out4["qualifying_at_floor"] == 0
    assert out4["gap_to_feasibility"] == {"shortfall_units": 1}
    assert out4["minimum_standard_supported"] == "utterance"
