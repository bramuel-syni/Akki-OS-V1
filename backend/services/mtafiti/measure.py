"""Mtafiti Measure — composes baseline + (admitted) detections (mandate §11).

Verbatim shape from §11:
```python
def measure(cand, standing, detections, v3_admitted) -> ScoreVector:
    return ScoreVector(
        source_standing=standing,                                   # deterministic
        attachment=detections.attachment_markedness if v3_admitted else 0.0,
        corroboration=detections.corroboration if v3_admitted else 0.0,
        recency_validity=recency(cand),                             # deterministic
        contested=contested_status(cand))                           # deterministic
```

When overlay NOT admitted (G4 default — V3 threshold is None), the
composition uses the baseline alone. That is the "baseline stands alone"
guarantee (invariant #2).

Cousin substrate: none. Session-shaped substrates have no defensibility
measure analogue.
"""
import json

from contracts.mtafiti_registry import MtafitiScoreVector, SourceStanding
from services.mtafiti import declaration
from services.mtafiti.census import SourceCandidate
from services.mtafiti.inference import Detections


def measure(
    unit_context: str,
    unit_logged_date: str,
    standing: SourceStanding,
    detections: Detections,
    v3_admitted: bool,
) -> MtafitiScoreVector:
    """Compose the measure. See module docstring for verbatim shape."""
    return MtafitiScoreVector(
        source_standing=standing,
        attachment=detections.attachment_markedness if v3_admitted else 0.0,
        corroboration=detections.corroboration if v3_admitted else 0.0,
        recency_validity=declaration.recency_validity(unit_logged_date),
        contested=declaration.contested_status(unit_context),
    )


def resolve_matrix_axes(unit_context: str) -> tuple:
    """Resolve (claim_genre, source_standing_ring5) from the unit's
    fixture-embedded `author_labels`.

    Mandate §11 verdict uses `(claim_genre, context)` — Ring 5-level
    axes distinct from Mtafiti's declaration `SourceStanding` enum.

    Falls back to ("unknown_genre", "unknown_context") when labels are
    absent — verdict will then return `non_factual` per fail-toward-caution.
    """
    try:
        labels = json.loads(unit_context or "{}").get("author_labels", {})
    except (json.JSONDecodeError, TypeError):
        return ("unknown_genre", "unknown_context")
    # Fixture uses labels like `claim_genre: "report"`,
    # `source_standing: "accountable_tier1"`. Real mapping to Ring-5
    # taxonomy (`news_anchor_read.primary_recorded`, `panel_debate.wire_republish`, ...)
    # lands post-G4 when MEA populates the Ring 5-level taxonomy. At G4 v0 the
    # lookup will typically be unmapped → fail-toward-caution `non_factual`.
    genre = labels.get("claim_genre", "unknown_genre")
    context = labels.get("source_standing", "unknown_context")
    return (genre, context)


__all__ = ["measure", "resolve_matrix_axes", "SourceCandidate"]
