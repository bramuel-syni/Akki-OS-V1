"""Stage 3 — Tension.

Source: `docs/mandates/RMS_Solva_Specification.md` §8.

Surfaces contradiction, corroboration, retraction among candidates
(reads Ring 3 edges). Does not average tensions away.
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence

from contracts.five_rings import NormalizedUnit, RelationType


def tension(candidate_artifact: Dict[str, Any]) -> Dict[str, Any]:
    """Return tension artifact — Ring 3 edges surfaced, not averaged."""
    candidates: Sequence[NormalizedUnit] = candidate_artifact.get("candidates", [])
    surfaced: List[Dict[str, Any]] = []
    for u in candidates:
        for edge in u.relational.edges:
            surfaced.append(
                {
                    "from_unit_id": u.unit_id,
                    "relation": edge.relation.value if hasattr(edge.relation, "value") else str(edge.relation),
                    "to_unit_id": edge.to_unit_id,
                }
            )
    return {
        "stage": "tension",
        "edges": surfaced,
        "has_contradiction": any(e["relation"] == RelationType.CONTRADICTS.value for e in surfaced),
        "has_retraction": any(e["relation"] == RelationType.RETRACTS.value for e in surfaced),
    }
