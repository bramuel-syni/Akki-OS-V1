"""Solva load-bearing — a reasoning judgment.

Source: `docs/mandates/RMS_Solva_Specification.md` §9.

Identifying which units are load-bearing is a genuine reasoning judgment
and belongs to the reasoning faculty. It is NOT the class computation;
it is the input to it. This separation is what keeps the assertion
boundary mechanical.

Free — no governed artifact dictates this. Returns unit refs only;
carries NO class decision.

Cousin chain (mandate-forced): source §9 declares this net-new; no
in-pod ancestor.
"""
from __future__ import annotations

from typing import List, Sequence

from contracts.five_rings import NormalizedUnit


def load_bearing(conclusion_text: str, candidates: Sequence[NormalizedUnit]) -> List[NormalizedUnit]:
    """Identify units the conclusion actually rests on.

    G3 v0: returns the non-empty candidate set unchanged. When the
    reasoning faculty binds an LLM-based reflection judgment (a
    G3+ implementation choice), this function will consult the
    Reflection-stage output. Meanwhile, an honest default: every
    candidate is treated as load-bearing.

    Contract: NO `DefensibilityClass` construction here; that's the
    boundary's job. See `test_reasoning_faculty_isolation`.
    """
    if not candidates:
        raise ValueError("candidates must be non-empty for a load-bearing judgment")
    # G3 v0 default: all candidates are load-bearing. Not a class
    # decision; a placement decision.
    return list(candidates)
