"""License-class taxonomy governance — Phase 4a gate 4.

Enforces that:
  1. The versioned config `license_classes.v0.json` GOVERNS the taxonomy
     — Python `.py` files under services/, routers/, and contracts/
     never carry illustrative class-name string literals (except within
     the canonical selection module's docstring, which documents the
     illustrative names for humans).
  2. `is_valid_class` reads the config; unknown class names return False.
  3. Ruling 4 Phase 7 seam docstring pre-commitment is documented in
     `services/service_1/license_class_selection.py`.

Precedent anchor: `test_admission_refusal_reason_extension_via_registry_bump`.
"""
from __future__ import annotations

import inspect
import re
from pathlib import Path

from services.service_1 import license_class_selection as lc_module


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


# Illustrative class names from license_classes.v0.json — must not appear
# as string literals in any Python file outside the canonical selection
# module's docstring or its exempt sweep locations.
_ILLUSTRATIVE_CLASS_NAMES = ["editorial_use", "syndication", "training_data"]


def test_license_class_config_governs_taxonomy():
    """Gate 4 — grep-negative on illustrative class-name literals in
    services/, routers/, contracts/ Python files (except the canonical
    module's docstring where documentation is legitimate).
    """
    sweep_dirs = [BACKEND_ROOT / d for d in ("services", "routers", "contracts")]

    canonical_module_path = Path(
        inspect.getfile(lc_module)
    ).resolve()

    violations = []
    for base in sweep_dirs:
        if not base.exists():
            continue
        for py in base.rglob("*.py"):
            if "__pycache__" in str(py):
                continue
            # The canonical module legitimately references illustrative
            # names in its module docstring for human reference; skip.
            if py.resolve() == canonical_module_path:
                continue
            text = py.read_text(encoding="utf-8")
            for name in _ILLUSTRATIVE_CLASS_NAMES:
                # Look for the name as a string literal ("editorial_use"
                # or 'editorial_use'), NOT as an identifier. This will
                # miss docstring-embedded prose references — acceptable
                # tolerance since docstrings are not runtime dispatch
                # surface.
                literal_pattern = re.compile(
                    rf'["\']{re.escape(name)}["\']'
                )
                for match in literal_pattern.finditer(text):
                    line_no = text[:match.start()].count("\n") + 1
                    violations.append(
                        f"{py.relative_to(BACKEND_ROOT)}:{line_no}: "
                        f"illustrative class name {name!r} appears as "
                        f"string literal outside canonical module"
                    )
    assert not violations, (
        "Gate 4 violation — illustrative license class names appear as "
        "string literals in .py files. Ruling 8 posture: class NAMES "
        "are config-governed; Python files hold NO name literals.\n"
        + "\n".join(violations)
    )


def test_license_class_config_valid_classes_registered():
    """`is_valid_class` reads config; the three illustrative names all
    validate; unknown class name returns False."""
    for name in _ILLUSTRATIVE_CLASS_NAMES:
        assert lc_module.is_valid_class(name) is True, (
            f"{name!r} not present in valid_classes[]"
        )
    assert lc_module.is_valid_class("no_such_class") is False
    assert lc_module.is_valid_class("") is False


def test_license_class_selection_phase_7_seam_documented():
    """Ruling 4 (Phase 4a Stage B dispatch, 2026-07-03) — Phase 7 seam
    pre-commitment MUST be documented in the module docstring.

    Grep-inspect the module docstring for two invariant phrases:
      * "Phase 7 seam pre-committed"
      * "fallback arm"

    Guards against future silent drift where a subsequent phase forgets
    that the current `derive_license_class_from_commissioner` is bounded
    by Phase 7's landing, or removes the pre-commitment when Phase 7's
    dispatch actually happens.
    """
    doc = inspect.getdoc(lc_module) or ""
    doc_lower = doc.lower()
    assert "phase 7 seam pre-committed" in doc_lower, (
        "license_class_selection.py module docstring MUST document the "
        "Phase 7 seam pre-commitment (Ruling 4, Phase 4a Stage B "
        "dispatch, 2026-07-03). Expected phrase: 'Phase 7 seam pre-committed'."
    )
    assert "fallback arm" in doc_lower, (
        "license_class_selection.py module docstring MUST document that "
        "`derive_license_class_from_commissioner` becomes the FALLBACK "
        "ARM of the unified derivation function under Phase 7. Expected "
        "phrase: 'fallback arm'."
    )
