"""Structured refusal result — ported shape from cousin
`/reference/akki-legacy/backend/services/solva_v2/engines/refusal.py`.

Cousin returns `{block, category, confidence, reason, distress_flag,
extraction_marker_hit}`. We keep the discipline (refusal as a structured
record, not a bool) and reshape the field set to depth-governor concerns:
  * decision      — "accept" | "refuse"
  * category      — the kind of refusal (unknown_genre / floor_violation /
                    dimension_violation / signal_invalid)
  * confidence    — 1.0 for deterministic refusals at G1; reserved for
                    when the model layer activates
  * reason        — human-readable short string

LIFTED LoC from cousin: ~10 (the dataclass shape + the discipline).
NET-NEW LoC in this file: the rest.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional

RefusalCategory = Literal[
    "clean", "unknown_genre", "floor_violation", "dimension_violation", "signal_invalid",
]


@dataclass
class DepthRefusalResult:
    decision: Literal["accept", "refuse"]
    category: RefusalCategory
    confidence: float
    reason: Optional[str] = None

    @classmethod
    def accept(cls) -> "DepthRefusalResult":
        return cls(decision="accept", category="clean", confidence=1.0, reason=None)

    @classmethod
    def refuse(cls, category: RefusalCategory, reason: str) -> "DepthRefusalResult":
        return cls(decision="refuse", category=category, confidence=1.0, reason=reason)
