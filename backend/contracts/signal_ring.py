"""Signal Ring dimension catalogue — v0 (G1 freeze).

Spec authority: RMS Spec §5.3 (Signal Ring carries modality-native dimensions).
Stakeholder catalogue locked at G1 with three explicit corrections from
the G1 brief:

  1. `on_screen_text_present` REMOVED — it is a Provenance/Relational
     concern, NOT a Signal depth dimension. A perception module that
     observes on-screen text emits a sibling NormalizedUnit (modality
     IMAGE/TEXT) and a Relational edge, not a Signal Boolean coerced
     into a float.
  2. `framing_intent` → `framing_markedness` (VIDEO).
     `composition_intent` → `composition_markedness` (IMAGE).
     **The Signal Ring measures markedness; intent is downstream.**
     Naming a Signal dimension `*_intent` quietly asks Solva to
     depth-judge a conclusion instead of a measured signal. That is
     the truth-vs-defensibility confusion the system exists to avoid.
  3. COMPOSITE carries no native dimensions — aggregation rule only.
     A COMPOSITE unit's `dimensions` reflect merged/averaged values
     drawn from its constituent units.

Freeze pattern lifted from
`/reference/akki-legacy/backend/services/synisense/engine/signal_types.py::_CATALOGUE`
(frozen catalogue + invariant snapshot). Bumping rev means new file
(`v1.json`, `v2.json`...). v0 is byte-frozen.

Forward note (v0 is extensible, not closed): G2 perception modules may
emit signals worth adding (e.g. richer affect dimensions, scene-level
signals). New revs land via snapshot bless. v0 catalogue ≠ final.
"""
from __future__ import annotations

from typing import Dict, Iterable

SIGNAL_RING_DIMENSIONS_V0: Dict[str, list[str]] = {
    "audio": ["prosody", "vocal_emphasis", "affect_valence", "affect_arousal", "speech_rate", "pause_density"],
    "video": ["visual_emphasis", "scene_change_density", "framing_markedness"],
    "image": ["visual_emphasis", "composition_markedness"],
    "text":  ["lexical_intensity", "stance_intensity", "hedging_density"],
    "composite": [],
}

SIGNAL_RING_DIMENSIONS_REV = "v0"


class SignalDimensionViolation(ValueError):
    pass


def validate_signal_dimensions(modality: str, dims: Iterable[str]) -> None:
    """Raise SignalDimensionViolation if any dim key is not in the v0
    catalogue for the given modality. modality is a lowercase string
    matching the Modality enum value."""
    allowed = set(SIGNAL_RING_DIMENSIONS_V0.get(modality.lower(), []))
    dims = list(dims)
    if modality.lower() == "composite":
        if dims:
            raise SignalDimensionViolation(
                f"COMPOSITE Signal Ring carries no native dimensions; got {dims!r}"
            )
        return
    bad = [d for d in dims if d not in allowed]
    if bad:
        raise SignalDimensionViolation(
            f"Signal dimension(s) {bad!r} not in v0 catalogue for modality {modality!r}. "
            f"Allowed: {sorted(allowed)}"
        )
