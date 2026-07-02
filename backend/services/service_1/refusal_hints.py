"""Service 1 refusal-hint lookup — A2 D2a static table.

Per-reason `what_would_raise_it` string, keyed on the exception's
`reason` code. Locked by user directive at A2 phase brief:

  * `no_defensibility_floor` and `no_lawful_basis` — input-validation
    refusals, hints are prescriptive fixes for the request.
  * `composition_below_floor` — semantic hint anchored to
    RMS_Interface_Specification.md §204 category `corroboration` and
    the "narrow the objective" alternative per §5.4 of the handoff
    artifact.

A2 HAZARD-STOP (f) check (STEP 0.4) confirmed source specs prescribe
content categories, not verbatim strings; the user's rewrite is
authoritative. Any future addition of a new reason MUST add a row here
or KeyError at raise time — CI catches drift via
`test_service_1_refusal_envelope`.
"""
from __future__ import annotations

from typing import Dict


_HINTS: Dict[str, str] = {
    "no_defensibility_floor": (
        "Provide a defensibility floor on the request "
        "(one of: fact, utterance, non_factual)."
    ),
    "no_lawful_basis": (
        "Provide a non-empty lawful_basis reference on the request."
    ),
    "composition_below_floor": (
        "No corroboration at the required standard was found for the "
        "load-bearing claims. Lower the floor, or narrow the objective "
        "to better-sourced material."
    ),
}


def hint_for(reason: str) -> str:
    """Return the refusal-hint string for the given reason code.

    Raises KeyError if the reason is not registered — intentional; new
    reasons MUST register a hint at introduction time.
    """
    return _HINTS[reason]
