"""Mtafiti Source-Standing — MEA-owned per-feed declaration (placeholder at G4).

User directive (4) verbatim: "Minimal synthetic placeholder covering the
on-disk fixture's feed_ids, marked `synthetic_placeholder /
not_editorial_authority`. Real table swaps in by config. NOT empty (would
break plumbing) and NOT a real seed (would usurp MEA editorial authority)."

Every entry carries:
  * standing               — a `SourceStanding` value (the actual value
                             is a synthetic guess; MEA replaces at real
                             deploy time)
  * synthetic_placeholder  — always True at G4
  * editorial_authority    — always False at G4

Real table swap-in: replace this module's `_PLACEHOLDER_TABLE` with a
loader that reads from `config/source_standing.yaml`. Invariant
`test_source_standing_placeholder_flags` will fail naturally, forcing
the deployment ceremony to update the invariant alongside the real
table (correct behaviour).
"""
from dataclasses import dataclass

from contracts.mtafiti_registry import SourceStanding


@dataclass(frozen=True)
class SourceStandingEntry:
    feed_id: str
    standing: SourceStanding
    synthetic_placeholder: bool
    editorial_authority: bool


# Covers the 8 feed_ids present in the on-disk fixture:
# aggregator_blog, citizen_archive, citizen_drama, citizen_tv_news,
# radio_jambo_callin, unclassified, wire_kna, x_ingest.
_PLACEHOLDER_TABLE = {
    "citizen_tv_news":     SourceStanding.ACCOUNTABLE,
    "citizen_archive":     SourceStanding.ACCOUNTABLE,
    "citizen_drama":       SourceStanding.AGGREGATOR,
    "wire_kna":            SourceStanding.LICENSED_WIRE,
    "radio_jambo_callin":  SourceStanding.UGC,
    "aggregator_blog":     SourceStanding.AGGREGATOR,
    "x_ingest":            SourceStanding.UGC,
    "unclassified":        SourceStanding.UNKNOWN,
}


def table() -> dict:
    """Return the current declaration table.

    Every entry is flagged `synthetic_placeholder=True` and
    `editorial_authority=False` — this table has NO editorial authority.
    Real MEA table replaces via config swap.
    """
    return {
        feed_id: SourceStandingEntry(
            feed_id=feed_id,
            standing=standing,
            synthetic_placeholder=True,
            editorial_authority=False,
        )
        for feed_id, standing in _PLACEHOLDER_TABLE.items()
    }


def feed_ids() -> set:
    return set(_PLACEHOLDER_TABLE.keys())
