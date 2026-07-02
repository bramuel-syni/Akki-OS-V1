"""Solva enforcement — apply floor + Matrix verdict, refuse below floor.

Source: `docs/mandates/RMS_Solva_Specification.md` §11.

`enforce` computes the conclusion class via `assertion.conclusion_class`,
compares against the objective's `defensibility_floor` (read-only), and
either returns an `Assertion` (via `assert_conclusion`) or a structured
`Refusal`. The floor and Matrix are read through read-only handles;
enforcement NEVER mutates a governed value.

Cousin chain:
  `services/g1_defensibility/solva_depth/refusal.py` — canonical
    structured-refusal shape; refusal-with-reason discipline.
  `services/solva_depth/assertion.py` — boundary computation.
  `services/solva_depth/interfaces.py` — read-only handle types.

Rule 2: `Refusal` shape + below-floor comparison are mandate-forced net-new
(source §11); `Assertion` composition path is transitive via
`assertion.assert_conclusion`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Union

from contracts.five_rings import DefensibilityClass, NormalizedUnit
from services.solva_depth.assertion import (
    Assertion,
    CLASS_ORDER,
    assert_conclusion,
    conclusion_class,
)
from services.solva_depth.interfaces import FloorSpec


@dataclass(frozen=True)
class Refusal:
    """Structured refusal — never a silent downgrade."""

    reason: str
    computed_class: DefensibilityClass
    floor_class: DefensibilityClass


Result = Union[Assertion, Refusal]


def _below_floor(klass: DefensibilityClass, floor: FloorSpec) -> bool:
    """Read-only comparison. Floor is not mutated; klass is not mutated."""
    return CLASS_ORDER[klass] < CLASS_ORDER[floor.minimum_class]


def enforce(
    conclusion_text: str,
    load_bearing_units: Sequence[NormalizedUnit],
    floor: FloorSpec,
) -> Result:
    """Apply floor read-only; refuse below with structured reason."""
    klass = conclusion_class(load_bearing_units)
    if _below_floor(klass, floor):
        return Refusal(
            reason="below_defensibility_floor",
            computed_class=klass,
            floor_class=floor.minimum_class,
        )
    return assert_conclusion(conclusion_text, load_bearing_units)
