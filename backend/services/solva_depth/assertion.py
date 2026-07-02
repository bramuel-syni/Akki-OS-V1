"""Solva assertion boundary — the mechanical faculty.

Source: `docs/mandates/RMS_Solva_Specification.md` §10.

`conclusion_class(load_bearing_units)` computes the conclusion's
defensibility class as the floor over the load-bearing units' classes.
Reasoning strength is not an input to that computation and cannot raise
the class. The signature IS the guard — no confidence parameter exists,
so laundering is unrepresentable, not runtime-policed.

Distinct from the reasoning faculty. `reasoning/` does NOT import from
this module; this module does NOT import from `reasoning/`. Enforced by
`test_reasoning_faculty_isolation`.

Cousin chain (transitive):
  `contracts.five_rings.DefensibilityClass` — Ring 5 enum (frozen G0).
  `services/g1_defensibility/solva_depth/governor.py` — canonical
    min-floor computation pattern; same read-only-handle discipline.

Rule 2: this module is mandate-forced-net-new per source §10 (the
construction-as-guard property is spec's core deliverable).

Note on `from __future__ import annotations`: intentionally NOT used
here. The signature-invariant test (`test_conclusion_class_signature`)
inspects real annotation objects, not deferred strings; the frozen
snapshot pins `__name__ == 'Sequence'` and `return_annotation is
DefensibilityClass`. Deferred annotations would make both checks fail.
"""

from dataclasses import dataclass
from typing import Optional, Sequence

from contracts.five_rings import DefensibilityClass, NormalizedUnit


CLASS_ORDER = {
    DefensibilityClass.NON_FACTUAL: 0,
    DefensibilityClass.UTTERANCE: 1,
    DefensibilityClass.FACT: 2,
}
INV_ORDER = {v: k for k, v in CLASS_ORDER.items()}


@dataclass(frozen=True)
class Assertion:
    """The bound conclusion output.

    `klass` is a `DefensibilityClass`; `claim` is:
      - the original text if klass == FACT.
      - the stated-form ("X was stated") if klass == UTTERANCE.
      - None if klass == NON_FACTUAL (context_only carries the text).
    """

    klass: DefensibilityClass
    claim: Optional[str]
    context_only: Optional[str] = None


def _stated_form(text: str) -> str:
    """Utterance rendering: mark the text as reported speech."""
    return f'"{text}" was stated'


def conclusion_class(load_bearing_units: Sequence[NormalizedUnit]) -> DefensibilityClass:
    """Compute the conclusion's defensibility class.

    Source §10: floor over the load-bearing units' governed classes.
    Input: `load_bearing_units` ONLY — no confidence, no strength.
    Output: a `DefensibilityClass` (frozen enum).

    Frozen signature — mutation fails `test_conclusion_class_signature`.
    """
    if not load_bearing_units:
        raise ValueError("load_bearing_units must be non-empty")
    floor = min(CLASS_ORDER[u.defensibility.defensibility_class] for u in load_bearing_units)
    return INV_ORDER[floor]


def assert_conclusion(text: str, load_bearing_units: Sequence[NormalizedUnit]) -> Assertion:
    """Compose the final assertion — utterance-class NEVER asserted as fact."""
    klass = conclusion_class(load_bearing_units)
    if klass == DefensibilityClass.FACT:
        return Assertion(klass=klass, claim=text)
    if klass == DefensibilityClass.UTTERANCE:
        return Assertion(klass=klass, claim=_stated_form(text))
    return Assertion(klass=klass, claim=None, context_only=text)
