"""Solva depth-governor composition — single-call judge over a unit.

NET-NEW: composition layer. The cousin's `state_machine.py` is the
composition layer at the session level; we deliberately do NOT port it.
G1's composition is a single function call: run the validators, return
a DepthRefusalResult.

Usage from Ring-5 stamper:
    decision = governor.judge(unit, proposed_ring=candidate_ring)
    if decision.decision == "refuse":
        ...
"""
from __future__ import annotations

from typing import Optional

from contracts.five_rings import DefensibilityRing, NormalizedUnit
from contracts.qualification_matrix.loader import QualificationMatrix
from services.g1_defensibility.solva_depth.integrity_validators import (
    ValidationResult,
    validate_class_under_ceiling,
    validate_signal_dimensions,
)
from services.g1_defensibility.solva_depth.refusal import DepthRefusalResult


class SolvaDepthGovernor:
    name = "solva-depth"
    version = "v1"

    def __init__(self, matrix: Optional[QualificationMatrix] = None) -> None:
        self._matrix = matrix

    def judge(self, unit: NormalizedUnit, proposed_ring: DefensibilityRing) -> DepthRefusalResult:
        # Validator 1: Signal dimensions in v0 catalogue.
        sig_offenders = validate_signal_dimensions(unit)
        if sig_offenders:
            return DepthRefusalResult.refuse(
                category="dimension_violation",
                reason="; ".join(o.explanation for o in sig_offenders),
            )
        # Validator 2: Proposed class within matrix ceiling.
        # Build a transient unit-shape carrying the proposed ring so the
        # validator sees what the stamper would write.
        unit_with_proposed = unit.model_copy(update={"defensibility": proposed_ring})
        ceiling_offenders = validate_class_under_ceiling(
            unit_with_proposed,
            proposed_class=proposed_ring.defensibility_class,
            matrix=self._matrix,
        )
        if ceiling_offenders:
            return DepthRefusalResult.refuse(
                category="floor_violation",
                reason="; ".join(o.explanation for o in ceiling_offenders),
            )
        return DepthRefusalResult.accept()

    def judged_dimensions(self, unit: NormalizedUnit) -> list[str]:
        """Returns the list of Signal dimensions this judge considered.
        At G1 we judge *all* present dimensions for catalogue compliance."""
        return sorted(unit.signal.dimensions.keys())
