"""Stage 4 — Probability.

Source: `docs/mandates/RMS_Solva_Specification.md` §8.

Weighs the candidates toward the best-supported conclusion.
"""
from __future__ import annotations

from typing import Any, Dict, Sequence

from contracts.five_rings import NormalizedUnit


def probability(candidate_artifact: Dict[str, Any], tension_artifact: Dict[str, Any]) -> Dict[str, Any]:
    """Return probability artifact — a rank order among candidates.

    G3 v0: honest default — every candidate carries equal weight; the
    reasoning-faculty method (how to weigh) is a build-time implementation
    choice bounded by the invariants (source §18). LLM binding is a
    G3+ implementation choice — MUST use extraction_params@v0
    temperature=0 discipline when it binds (Product Spec 2.1 §31 #10).
    """
    candidates: Sequence[NormalizedUnit] = candidate_artifact.get("candidates", [])
    return {
        "stage": "probability",
        "weighted_unit_ids": [u.unit_id for u in candidates],
        "tension_ack": bool(tension_artifact.get("edges")),
    }
