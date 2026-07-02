"""Stage 2 — Candidate.

Source: `docs/mandates/RMS_Solva_Specification.md` §8.

Proposes the units and compositions that could answer the framed question.
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence

from contracts.five_rings import NormalizedUnit


def candidate(frame_artifact: Dict[str, Any], units: Sequence[NormalizedUnit]) -> Dict[str, Any]:
    """Return candidate artifact — every unit in the framed slice is a candidate."""
    ids = set(frame_artifact.get("candidate_unit_ids", []))
    picked: List[NormalizedUnit] = [u for u in units if u.unit_id in ids]
    return {
        "stage": "candidate",
        "candidates": picked,
        "count": len(picked),
    }
