"""Stage 5 — Reflection.

Source: `docs/mandates/RMS_Solva_Specification.md` §8.

Judges soundness and sufficiency; identifies the load-bearing units;
composes the conclusion. Reflection's output includes the set of
load-bearing units — the units the conclusion actually rests on. That
set is the reasoning faculty's product and the only thing the assertion
boundary consumes from it (the units, not the confidence).
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence

from contracts.five_rings import NormalizedUnit
from services.solva_depth.load_bearing import load_bearing


def reflection(
    question: str,
    candidate_artifact: Dict[str, Any],
    probability_artifact: Dict[str, Any],
) -> Dict[str, Any]:
    """Return reflection artifact — a conclusion text + load-bearing units.

    Load-bearing identification is a reasoning judgment (source §9);
    class computation happens elsewhere via `assertion.conclusion_class`.
    """
    candidates: Sequence[NormalizedUnit] = candidate_artifact.get("candidates", [])
    conclusion_text = f"Reflection on: {question}"  # v0 placeholder
    load_bearing_units: List[NormalizedUnit] = load_bearing(conclusion_text, candidates)
    return {
        "stage": "reflection",
        "conclusion_text": conclusion_text,
        "load_bearing_units": load_bearing_units,  # not a class decision
    }
