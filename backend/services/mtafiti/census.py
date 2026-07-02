"""Mtafiti Census — exhaustive, objective-blind estate walk (mandate §8).

`SourceCandidate` is a lightweight in-flight tuple. It is NOT a frozen
contract — it never crosses a service boundary except as an argument to
`declaration.declared_standing()` and `measure.measure()`, both siblings.

Invariant #1 + #9: census consults NO ObjectiveRequest. Signature carries
no such parameter. This is construction-as-guard: the objective is
absent from what the census sees.

Cousin substrate: none. Session-shaped substrates have no
estate-walker analogue.
"""
from dataclasses import dataclass
from typing import Iterator, List

from contracts.five_rings import NormalizedUnit


@dataclass(frozen=True)
class SourceCandidate:
    source_ref: str
    region: str
    feed_id: str
    sensitivity: str


def classify_sensitivity(unit: NormalizedUnit) -> str:
    """Deterministic sensitivity classification for DPA handling (mandate §8).

    G4 v0: single-tier classifier based on `provenance.modality`. Audio /
    video default to `elevated` (voice = personal-data-adjacent under
    Kenya DPA), image `elevated`, text/composite `standard`. Real
    classifier lands with MEA and DPO review post-G4.
    """
    m = unit.provenance.modality.value
    return "elevated" if m in ("audio", "video", "image") else "standard"


def _feed_id_from_unit(unit: NormalizedUnit) -> str:
    """Extract feed_id from `provenance.context` (fixture-carried JSON blob).

    Real feed-id resolution lands with the real estate walker post-G4.
    Fixture-backed at G4 for synthetic-mode runs (per Substrate-Drop v1
    posture). Returns 'unknown' if absent.
    """
    import json
    ctx = unit.provenance.context or ""
    try:
        return json.loads(ctx).get("feed_id", "unknown")
    except (json.JSONDecodeError, TypeError):
        return "unknown"


def _region_from_unit(unit: NormalizedUnit) -> str:
    """Region defaults to feed_id at G4 (feed IS the region seam for
    the on-disk fixture). Real region taxonomy lands post-G4."""
    return _feed_id_from_unit(unit)


def census(units: List[NormalizedUnit]) -> Iterator[SourceCandidate]:
    """Exhaustive, objective-blind walk. Enumerates + classifies; measure
    follows.

    Signature carries NO ObjectiveRequest → invariant #1 + #9 held by
    construction.
    """
    for unit in units:
        yield SourceCandidate(
            source_ref=unit.provenance.source_ref,
            region=_region_from_unit(unit),
            feed_id=_feed_id_from_unit(unit),
            sensitivity=classify_sensitivity(unit),
        )
