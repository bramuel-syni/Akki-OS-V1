"""Mtafiti Source-Standing — MEA-owned per-feed declaration (placeholder at G4).

Post-Fixture-Refresh 2026-07-10 (FR-E2 α): distributed placeholder table
DELETED. Source-of-truth for per-feed source_standing lives in
`services/service_1/license_classes.v1.json` (`feed_entries[*].source_standing`).
This module now READS FROM that central registry via
`services.service_1.license_class_selection.get_source_standing_name`
and `known_feed_ids`. Runtime behavior preserved (every entry still
carries `synthetic_placeholder=True` + `editorial_authority=False`);
authoritative table swap-in remains a config-only ceremony (bump v1.json
to v2.json).

User directive (4) verbatim (pre-refresh): "Minimal synthetic placeholder
covering the on-disk fixture's feed_ids, marked `synthetic_placeholder /
not_editorial_authority`. Real table swaps in by config. NOT empty (would
break plumbing) and NOT a real seed (would usurp MEA editorial authority)."

Every entry carries:
  * standing               — a `SourceStanding` value (the actual value
                             is a synthetic guess from the central v1
                             registry; MEA replaces at real deploy time
                             via config bump)
  * synthetic_placeholder  — always True at G4
  * editorial_authority    — always False at G4

Real table swap-in: bump `services/service_1/license_classes.v1.json`
to `v2.json` with real per-feed source_standing values (MEA authority).
Invariant `test_source_standing_placeholder_flags` will fail naturally,
forcing the deployment ceremony to update the invariant alongside the
real table (correct behaviour).
"""
from dataclasses import dataclass

from contracts.mtafiti_registry import SourceStanding
from services.service_1.license_class_selection import (
    get_source_standing_name,
    known_feed_ids,
)


@dataclass(frozen=True)
class SourceStandingEntry:
    feed_id: str
    standing: SourceStanding
    synthetic_placeholder: bool
    editorial_authority: bool


# Mapping from central-registry name strings → SourceStanding enum.
# Names match the `source_standing` values in
# services/service_1/license_classes.v1.json feed_entries[*].
_NAME_TO_ENUM = {
    "accountable_tier1": SourceStanding.ACCOUNTABLE,
    "licensed_wire":     SourceStanding.LICENSED_WIRE,
    "aggregator":        SourceStanding.AGGREGATOR,
    "ugc":               SourceStanding.UGC,
    "unknown":           SourceStanding.UNKNOWN,
}


def table() -> dict:
    """Return the current declaration table.

    Reads feed_ids + per-feed source_standing from the central v1
    registry (`license_classes.v1.json`); enum-lifts the name strings
    to `SourceStanding` values.

    Every entry is flagged `synthetic_placeholder=True` and
    `editorial_authority=False` — this table has NO editorial authority.
    Real MEA values replace via config bump (v1 → v2).
    """
    return {
        feed_id: SourceStandingEntry(
            feed_id=feed_id,
            standing=_NAME_TO_ENUM[get_source_standing_name(feed_id)],
            synthetic_placeholder=True,
            editorial_authority=False,
        )
        for feed_id in known_feed_ids()
    }


def feed_ids() -> set:
    return set(known_feed_ids())
