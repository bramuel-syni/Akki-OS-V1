"""G-2 Registry Maintenance · R4 attest cell #8 · PART_II_JOURNEY_STEPS alias canonicalization.

Owner ruling: docs/rulings/g2_rm_e1_to_e3_2026-07-14.md · alias canonicalization
to SHORT forms (S3.prove, S4.verify) per governance-amendment-only clause.
Legacy long-form aliases (S3.prove-end-to-end, S4.verify-receipt) RETIRED.
"""
from __future__ import annotations

import pytest

from backend.services.registry.validator import (
    PART_II_JOURNEY_STEPS,
    _RETIRED_JOURNEY_STEP_ALIASES,
)


def test_canonical_short_forms_present_in_journey_steps():
    """G-2 canonical short forms MUST be in PART_II_JOURNEY_STEPS."""
    assert "S3.prove" in PART_II_JOURNEY_STEPS, "S3.prove missing from PART_II_JOURNEY_STEPS"
    assert "S4.verify" in PART_II_JOURNEY_STEPS, "S4.verify missing from PART_II_JOURNEY_STEPS"


def test_legacy_long_form_aliases_rejected():
    """Legacy long-form aliases MUST NOT be in PART_II_JOURNEY_STEPS."""
    assert "S3.prove-end-to-end" not in PART_II_JOURNEY_STEPS, (
        "S3.prove-end-to-end legacy alias must be retired per G-2 canonicalization ruling"
    )
    assert "S4.verify-receipt" not in PART_II_JOURNEY_STEPS, (
        "S4.verify-receipt legacy alias must be retired per G-2 canonicalization ruling"
    )


def test_retired_aliases_set_carries_both_long_forms():
    """Defensive negative-set enumerates retired aliases for downstream checks."""
    assert "S3.prove-end-to-end" in _RETIRED_JOURNEY_STEP_ALIASES
    assert "S4.verify-receipt" in _RETIRED_JOURNEY_STEP_ALIASES


def test_canonical_forms_do_not_overlap_retired_aliases():
    """Canonical set and retired-alias set are disjoint."""
    overlap = PART_II_JOURNEY_STEPS & _RETIRED_JOURNEY_STEP_ALIASES
    assert not overlap, f"Canonical set overlaps retired aliases: {overlap}"


def test_canonical_forms_present_legacy_aliases_rejected():
    """Composite R4 #8 attest: both directions verified in one cell."""
    # canonical present
    assert {"S3.prove", "S4.verify"}.issubset(PART_II_JOURNEY_STEPS)
    # legacy retired
    assert not ({"S3.prove-end-to-end", "S4.verify-receipt"} & PART_II_JOURNEY_STEPS)
