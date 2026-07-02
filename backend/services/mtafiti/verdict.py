"""Mtafiti Verdict — Matrix lookup → defensibility_class (mandate §11).

Deterministic. No learned weight assigns the class (invariant #4).

Reads the frozen Qualification Matrix through an opaque handle
(`MatrixHandle`, reused verbatim from `services/solva_depth/interfaces.py`).
Returns a `Verdict` carrying `defensibility_class` and `matrix_rule_ref`
(the auditable rule id per invariant #4).

Mandate §11 note on axes: the spec's `matrix.lookup(claim_genre, context)`
maps onto the frozen `qualification_matrix@v0` axes `(genre, source_standing)`
— per §11 the second axis is contextual (the Ring 5 source-standing
taxonomy `primary_recorded | wire_republish | ...`), NOT the Mtafiti-level
declaration `SourceStanding` enum (`accountable | licensed_wire | ...`).
Composition (measure.py) resolves both axes from the unit before calling
verdict.
"""
from dataclasses import dataclass
from typing import Optional

from services.solva_depth.interfaces import MatrixHandle, default_matrix_handle


@dataclass(frozen=True)
class Verdict:
    """Mandate §11: `defensibility_class + matrix_rule_ref`."""
    defensibility_class: str
    matrix_rule_ref: str


def assign_verdict(claim_genre: str, context: str, matrix: MatrixHandle) -> Verdict:
    """Deterministic Matrix lookup. NEVER a learned weight.

    Mandate §11 verbatim shape. `matrix_rule_ref` carries the id of the
    rule that produced this verdict — auditable (invariant #4).

    Unmapped cell: fails toward caution (mandate §17 #5: "the measure is
    a targeting and flooring prior, not a truth verdict; it fails toward
    caution"). Returns non_factual with matrix_rule_ref='unmapped_cell'.
    """
    rule = matrix.rule_for(claim_genre, context)
    if rule is None:
        return Verdict(
            defensibility_class="non_factual",
            matrix_rule_ref="unmapped_cell",
        )
    return Verdict(
        defensibility_class=rule.asserts_what.value,
        matrix_rule_ref=f"{rule.matrix_rule_id}@v0",
    )


def default_handle() -> MatrixHandle:
    """Convenience re-export of the frozen v0 MatrixHandle."""
    return default_matrix_handle()
