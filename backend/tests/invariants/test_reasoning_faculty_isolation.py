"""Reasoning-faculty isolation — Solva spec §17 invariant #2.

Two faculties (free reasoning + bound assertion) with one-way seam.
`reasoning/` modules do NOT:
  * import `DefensibilityClass` from `contracts.five_rings`,
  * declare `-> DefensibilityClass` return annotations,
  * construct `DefensibilityClass` values via source-inspection (naive but useful).

`assertion.py` MUST NOT import from `reasoning/`.

Parametrized across all 5 stage modules per G3 phase brief step 3.
"""
from __future__ import annotations

import inspect
import re
from pathlib import Path

import pytest

from services.solva_depth.reasoning import (
    candidate as m_candidate,
    frame as m_frame,
    probability as m_probability,
    reflection as m_reflection,
    tension as m_tension,
)

STAGE_MODULES = [
    ("frame", m_frame),
    ("candidate", m_candidate),
    ("tension", m_tension),
    ("probability", m_probability),
    ("reflection", m_reflection),
]


@pytest.mark.parametrize("stage_name,module", STAGE_MODULES)
def test_stage_does_not_import_defensibility_class(stage_name, module):
    """Solva spec §17 #2: reasoning stages do not import the class enum."""
    source = inspect.getsource(module)
    # Allow imports for other names from contracts.five_rings (e.g. NormalizedUnit),
    # forbid importing `DefensibilityClass` specifically.
    bad_import = re.search(
        r"from\s+contracts\.five_rings\s+import\s+[^)\n]*\bDefensibilityClass\b",
        source,
    )
    assert bad_import is None, (
        f"reasoning stage '{stage_name}' MUST NOT import DefensibilityClass "
        f"(source §17 #2)."
    )
    also_bad = re.search(r"\bimport\s+.*DefensibilityClass\b", source)
    assert also_bad is None, (
        f"reasoning stage '{stage_name}' has a suspicious DefensibilityClass import."
    )


@pytest.mark.parametrize("stage_name,module", STAGE_MODULES)
def test_stage_has_no_defensibility_class_return_annotation(stage_name, module):
    """No stage function returns DefensibilityClass."""
    for name, fn in inspect.getmembers(module, inspect.isfunction):
        if fn.__module__ != module.__name__:
            continue  # skip re-exports
        sig = inspect.signature(fn)
        ret = sig.return_annotation
        ret_name = getattr(ret, "__name__", str(ret))
        assert "DefensibilityClass" not in ret_name, (
            f"reasoning stage '{stage_name}' function '{name}' returns "
            f"{ret_name}; class output is the assertion boundary's job."
        )


@pytest.mark.parametrize("stage_name,module", STAGE_MODULES)
def test_stage_does_not_construct_defensibility_class(stage_name, module):
    """Naive source-inspection: no `DefensibilityClass(` construction in stage code."""
    source = inspect.getsource(module)
    assert "DefensibilityClass(" not in source, (
        f"reasoning stage '{stage_name}' constructs DefensibilityClass in source; "
        f"class values are the boundary's."
    )


def test_assertion_does_not_import_from_reasoning():
    """One-way seam — source §17 #2."""
    from services.solva_depth import assertion as m_assertion
    src = inspect.getsource(m_assertion)
    assert "solva_depth.reasoning" not in src, (
        "assertion.py MUST NOT import from services.solva_depth.reasoning "
        "— seam is one-way (source §17 #2)."
    )
