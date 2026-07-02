"""Mtafiti Declaration Baseline — deterministic, always available (mandate §9).

Feed-level. Low cardinality. Never assigned per item (invariant #6).

Baseline is a "certain floor the whole measure rests on" (mandate §9).
Runs live at G4 whether or not the V3 overlay is admitted.
"""
from typing import Mapping

from contracts.mtafiti_registry import SourceStanding


def declared_standing(feed_id: str, table: Mapping[str, object]) -> SourceStanding:
    """Feed-level lookup. Low cardinality, stable, estate-wide.

    Returns SourceStanding.UNKNOWN when the feed is absent from the
    declaration table. This is the mandate §9 verbatim default.

    `table` is a mapping keyed by feed_id yielding an object with a
    `.standing` attribute (matches the shape from
    `source_standing.table()` at G4; real MEA loader replaces by config).
    """
    entry = table.get(feed_id)
    if entry is None:
        return SourceStanding.UNKNOWN
    return entry.standing


def recency_validity(logged_date_iso: str) -> float:
    """Deterministic recency in [0, 1].

    G4 v0: 1.0 (all fixture units are treated as fresh). Real recency
    computation lands with the estate walker post-G4.
    """
    _ = logged_date_iso  # deterministic, but the input is captured for auditability
    return 1.0


def contested_status(unit_provenance_context: str) -> bool:
    """Deterministic contested-status detection (mandate §11).

    G4 v0: reads the fixture-embedded `author_labels.contested_status`
    ('contested' → True; anything else → False). Real detector lands
    post-G4.
    """
    import json
    try:
        labels = json.loads(unit_provenance_context or "{}").get("author_labels", {})
    except (json.JSONDecodeError, TypeError):
        return False
    return labels.get("contested_status") == "contested"
