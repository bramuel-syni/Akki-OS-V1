"""Stage 1 — Frame.

Source: `docs/mandates/RMS_Solva_Specification.md` §8.

Establishes the question and the relevant slice of the Normalized tier.
"""
from __future__ import annotations

from typing import Any, Dict, Sequence

from contracts.five_rings import NormalizedUnit


def frame(question: str, tier_slice: Sequence[NormalizedUnit]) -> Dict[str, Any]:
    """Return frame artifact — question + relevant unit ids only."""
    return {
        "stage": "frame",
        "question": question,
        "candidate_unit_ids": [u.unit_id for u in tier_slice],
    }
