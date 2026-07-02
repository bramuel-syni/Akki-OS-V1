"""Solva interfaces — opaque read-only handles.

Source: `docs/mandates/RMS_Solva_Specification.md` §7, §11.

`FloorSpec` and `MatrixHandle` are the two read-only handle types Solva
uses to consult governed values without mutating them. `FloorSpec`
wraps `contracts.objective_request.DefensibilityFloor` at extraction time;
`MatrixHandle` provides deterministic Matrix-rule lookup (Mtafiti's
domain at G4, stubbed to a synchronous local read for G3).

Read-only-ness is a discipline (no setters, no mutation calls in the
consumer modules); enforced structurally by immutable dataclass shape.

Cousin chain (transitive):
  `services/g1_defensibility/solva_depth/governor.py` — uses read-only
    Matrix/Floor lookups internally; same read-only-handle pattern.
  `contracts.qualification_matrix.loader.QualificationMatrix.find` —
    the underlying immutable-lookup surface.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from contracts.five_rings import DefensibilityClass
from contracts.objective_request import DefensibilityFloor
from contracts.qualification_matrix.loader import (
    QualificationMatrix,
    QualificationRule,
    load_qualification_matrix,
)


@dataclass(frozen=True)
class FloorSpec:
    """Read-only floor consumed by Solva enforcement.

    Wraps `DefensibilityFloor` from the frozen Objective Request contract.
    Frozen dataclass — Solva cannot mutate it.
    """

    minimum_class: DefensibilityClass

    @classmethod
    def from_floor(cls, floor: DefensibilityFloor) -> "FloorSpec":
        return cls(minimum_class=floor.minimum_class)


class MatrixHandle(Protocol):
    """Read-only Matrix lookup handle. Solva calls; never sets."""

    def rule_for(self, genre: str, source_standing: str) -> Optional[QualificationRule]:
        ...


@dataclass(frozen=True)
class _DefaultMatrixHandle:
    """Default Matrix handle backed by the frozen v0 loader."""

    _matrix: QualificationMatrix

    def rule_for(self, genre: str, source_standing: str) -> Optional[QualificationRule]:
        return self._matrix.find(genre, source_standing)


def default_matrix_handle() -> MatrixHandle:
    """Return the default v0 Matrix handle (frozen content-snapshot backed)."""
    return _DefaultMatrixHandle(_matrix=load_qualification_matrix("v0"))
