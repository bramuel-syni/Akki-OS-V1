"""Mtafiti Inference — learned detectors (mandate §10).

**Detect versus decide boundary — enforced by import rule (§17 #3).**

This module emits `Detections` only. It NEVER imports from `verdict.py`.
It NEVER constructs a `DefensibilityClass`. The learned layer cannot
touch the governed decision — the boundary is a dependency rule, not
runtime policing.

At G4 v0: detectors are code-only stubs (return deterministic 0.0).
Real detectors bind post-G4 through V3-gated admission. This module is
part of the V3-DARK closed seam: `overlay_admitted() is False` means
`measure()` zeroes attachment/corroboration regardless of what these
stubs return.
"""
from dataclasses import dataclass, field
from typing import Mapping

from contracts.five_rings import NormalizedUnit


@dataclass(frozen=True)
class Detections:
    """The ONLY thing inference emits (mandate §10 verbatim shape).

    Mandate §10: attachment_markedness, genre_form (label, NOT a
    verdict), corroboration, confidences.
    """

    attachment_markedness: float
    genre_form: str
    corroboration: float
    confidences: Mapping[str, float] = field(default_factory=dict)


def detect(unit: NormalizedUnit, estate_index: object) -> Detections:
    """Learned detectors. Emits signals only.

    G4 v0: deterministic-null detectors (all 0.0). Real learned
    detectors bind post-G4. This module is V3-DARK; the values it
    returns are zeroed at composition time when `overlay_admitted()` is
    False (which it always is at G4).

    MUST NOT import verdict.py; MUST NOT assign defensibility_class.
    """
    _ = unit, estate_index
    return Detections(
        attachment_markedness=0.0,
        genre_form="unknown",
        corroboration=0.0,
        confidences={},
    )
