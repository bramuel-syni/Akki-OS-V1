"""Source-standing reader — declaration baseline only (G1).

Reads per-feed declarations from a seed JSON file. NO inference overlay
(V3-gated; lands at G1 V3 pass or later). NEVER invents.

Forward note (G2 swap-in): at G4 this reader's data source is swapped
for Mtafiti's Registry. The function signature does not change; only
the backing store. Document the swap point clearly in the BUILD_JOURNAL
"G2 swap-in points" list.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

_SEED_PATH = Path(__file__).parent / "feed_declarations.seed.json"


@dataclass
class SourceStanding:
    value: str  # e.g. "primary_recorded" / "wire_republish"
    declared_by: str  # who declared it (e.g. "MEA-seed")
    declared_at: str  # ISO timestamp


def _load_table() -> dict:
    if not _SEED_PATH.exists():
        return {}
    return json.loads(_SEED_PATH.read_text(encoding="utf-8"))


def read_declared(source_ref: str) -> Optional[SourceStanding]:
    """Returns the declared SourceStanding for source_ref, or None if
    no declaration exists. Never infers, never guesses."""
    table = _load_table()
    entry = table.get(source_ref)
    if entry is None:
        # Try prefix match (synthetic refs share prefixes with their assets).
        for k, v in table.items():
            if source_ref.startswith(k):
                entry = v; break
    if entry is None:
        return None
    return SourceStanding(
        value=entry["source_standing"],
        declared_by=entry.get("declared_by", "unknown"),
        declared_at=entry.get("declared_at", ""),
    )
