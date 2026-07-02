"""Solva depth-governor integrity validators — reshaped from cousin.

Cousin shape:
`/reference/akki-legacy/backend/services/solva_v2/integrity_validators.py`
— ValidatorOffender + ValidationResult dataclasses, per-validator function
returning a list of offenders, ValidationResult aggregator with `.ok`.
We lift that shape.

Cousin VALIDATORS (citation_lint, confidence_calibration, refuse_to_decide,
methodological_honesty) are session-shaped — NOT PORTED. They belong to
the cousin's artefact-payload review, not unit-level depth judging.

NET-NEW VALIDATORS at G1:
  * signal_dimensions_in_catalogue_v0
  * defensibility_class_under_matrix_ceiling

LoC ledger for this file: ~30 LoC of lifted shape (ValidatorOffender +
ValidationResult); the rest is net-new content.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from contracts.five_rings import DefensibilityClass, DefensibilityRing, NormalizedUnit, SignalRing
from contracts.qualification_matrix.loader import QualificationMatrix, load_qualification_matrix
from contracts.signal_ring import SIGNAL_RING_DIMENSIONS_V0


@dataclass
class ValidatorOffender:
    """Lifted from cousin integrity_validators.py L46–55."""
    validator: str
    field_path: str
    explanation: str


@dataclass
class ValidationResult:
    """Lifted from cousin integrity_validators.py L56–70 (shape + `.ok`)."""
    offenders: List[ValidatorOffender] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.offenders


def validate_signal_dimensions(unit: NormalizedUnit) -> List[ValidatorOffender]:
    """NET-NEW. Catalogue check at depth-judge time."""
    modality = unit.provenance.modality.value.lower()
    allowed = set(SIGNAL_RING_DIMENSIONS_V0.get(modality, []))
    if modality == "composite":
        if unit.signal.dimensions:
            return [ValidatorOffender(
                validator="signal_dimensions_v0",
                field_path="signal.dimensions",
                explanation=f"COMPOSITE carries no native dimensions; got {sorted(unit.signal.dimensions)}",
            )]
        return []
    bad = [d for d in unit.signal.dimensions if d not in allowed]
    if bad:
        return [ValidatorOffender(
            validator="signal_dimensions_v0",
            field_path="signal.dimensions",
            explanation=f"dimension(s) {bad!r} not in v0 catalogue for {modality!r}",
        )]
    return []


def validate_class_under_ceiling(
    unit: NormalizedUnit, proposed_class: DefensibilityClass,
    matrix: Optional[QualificationMatrix] = None,
) -> List[ValidatorOffender]:
    """NET-NEW. Proposed class must not exceed the matrix row's ceiling."""
    matrix = matrix or load_qualification_matrix("v0")
    # The proposed_class is the class the stamper would emit. The matrix
    # row's `asserts_what` is the ceiling. We reject if proposed > ceiling.
    _RANK = {DefensibilityClass.NON_FACTUAL: 0, DefensibilityClass.UTTERANCE: 1, DefensibilityClass.FACT: 2}
    # Resolve the matrix rule via the *stamper-provided* matrix_rule_ref
    # if available on the unit (synthetic fixture provides it); otherwise
    # this validator is a no-op (stamper hasn't built the candidate yet).
    if not hasattr(unit, "defensibility") or unit.defensibility is None:
        return []
    ref = unit.defensibility.matrix_rule_ref
    if not ref:
        return []
    rule_id = ref.split("@")[0]
    rule = matrix.by_id(rule_id)
    if rule is None:
        return [ValidatorOffender(
            validator="class_under_ceiling",
            field_path="defensibility.matrix_rule_ref",
            explanation=f"unknown matrix rule {rule_id!r}",
        )]
    if _RANK[proposed_class] > _RANK[rule.asserts_what]:
        return [ValidatorOffender(
            validator="class_under_ceiling",
            field_path="defensibility.defensibility_class",
            explanation=(
                f"proposed {proposed_class.value!r} exceeds matrix ceiling "
                f"{rule.asserts_what.value!r} for rule {rule_id!r}"
            ),
        )]
    return []
