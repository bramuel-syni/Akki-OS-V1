"""Qualification Matrix loader — G0 freeze.

Spec authority: RMS Product & Engineering Spec v2.0 §3.4. MEA-owned
governed taxonomy: rows of `(genre, source_standing) → asserts_what`.
Solva enforces this at Ring-5 stamp time.

Freeze pattern lifted from
/reference/akki-legacy/backend/services/synisense/engine/signal_types.py
which locks a frozen catalogue with a brief-§-ref and an invariant snapshot.
The matrix content itself is net-new — the cousin has nothing equivalent.

At G0 the matrix is a file-edit-and-bump-rev artefact (v0.json). The MEA
editor UI lands at G5.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.five_rings import DefensibilityClass

_MATRIX_DIR = Path(__file__).parent
_DEFAULT_REV = "v0"


class QualificationRule(BaseModel):
    """One row of the matrix.

    Per Spec §3.4: `(claim-genre × source-standing) → asserts_what`. The
    `asserts_what` here is the *ceiling* the Solva governor will allow
    when stamping the unit's Defensibility ring.
    """

    model_config = ConfigDict(extra="forbid")

    matrix_rule_id: str = Field(
        ..., description="Stable ID; quoted by units' DefensibilityRing.matrix_rule_ref."
    )
    genre: str
    source_standing: str
    asserts_what: DefensibilityClass = Field(
        ..., description="Ceiling: highest defensibility class permitted for this cell."
    )
    notes: Optional[str] = None


class QualificationMatrix(BaseModel):
    """The governed matrix.

    Versioned by `matrix_rev` (e.g. "v0"). Frozen by snapshotting both
    the schema (via Pydantic) and the *content* (the v0.json file).
    Bumping the matrix requires re-blessing both snapshots.
    """

    model_config = ConfigDict(extra="forbid")

    matrix_rev: str
    rules: List[QualificationRule]

    def by_id(self, matrix_rule_id: str) -> Optional[QualificationRule]:
        for r in self.rules:
            if r.matrix_rule_id == matrix_rule_id:
                return r
        return None

    def find(self, genre: str, source_standing: str) -> Optional[QualificationRule]:
        """Lookup by (genre, source_standing). Returns None if no row."""
        for r in self.rules:
            if r.genre == genre and r.source_standing == source_standing:
                return r
        return None

    def rule_ref(self, rule: QualificationRule) -> str:
        """Canonical `matrix_rule_id@rev` string for DefensibilityRing.matrix_rule_ref."""
        return f"{rule.matrix_rule_id}@{self.matrix_rev}"


def _matrix_path(rev: str) -> Path:
    return _MATRIX_DIR / f"{rev}.json"


def load_qualification_matrix(rev: str = _DEFAULT_REV) -> QualificationMatrix:
    """Load + validate the matrix at the given revision.

    Raises FileNotFoundError if the rev's JSON file is missing, and
    pydantic.ValidationError if the file content doesn't match the
    schema (caught by the invariant snapshot test at CI time).
    """
    path = _matrix_path(rev)
    if not path.exists():
        raise FileNotFoundError(f"Qualification Matrix rev {rev} not found at {path}")
    payload: Dict = json.loads(path.read_text(encoding="utf-8"))
    return QualificationMatrix.model_validate(payload)
