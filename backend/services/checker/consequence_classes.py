"""§8 consequence-class constrained-str per Owner E1.γ registry pattern.

Ruling 4 (Amendment G): consequence_class is a constrained-str backed by
`consequence_class.v0.json` — NEVER a Pydantic Literal (E1.β trap:
widening a frozen Literal is the scheduled hazard-stop).

Values enumerated in the registry:
    * `tightening_unilateral` — Administration-initiated tightening,
      unilateral-with-delay, halted only by owner-suspend (Ruling 3).
    * `dual_control` — Both consoles must sign; blocks until countersign
      (CK-G1 LB).

Gate CK-G5: `services/checker/*.py` MUST NOT contain any
`Literal["tightening_unilateral", "dual_control"]` (or reordering).
Enforced by grep-negative test.
"""
from __future__ import annotations

import re

# Registry-mirrored regex. When the registry appends a new class, extend
# the pattern here in the SAME commit as the registry bump.
_CONSEQUENCE_CLASS_PATTERN = re.compile(
    r"^(tightening_unilateral|dual_control)$"
)


CONSEQUENCE_CLASS_TIGHTENING_UNILATERAL = "tightening_unilateral"
CONSEQUENCE_CLASS_DUAL_CONTROL = "dual_control"


class InvalidConsequenceClassError(ValueError):
    """Raised when a caller supplies a consequence_class value not in the
    registry pattern."""


def validate_consequence_class(value: str) -> str:
    """Constrained-str validation. Returns value on match, raises otherwise."""
    if not isinstance(value, str) or not _CONSEQUENCE_CLASS_PATTERN.match(value):
        raise InvalidConsequenceClassError(
            f"consequence_class={value!r} not in registry-backed pattern; "
            f"expected one of tightening_unilateral | dual_control"
        )
    return value
