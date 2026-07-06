"""Coverage-marker service — Sub-stage 1 (E3.β canonical mechanism).

E3.β + honest-cost binding (Owner Amendment E, 2026-07-06):
  Query-time first-timestamp-per-family. Per-family `since_date` = ISO
  of earliest NorthenaLedgerRow_v1 whose stamp_audit["refusal_family"]
  matches. NO config file, NO materialization, NO pre-optimization.
  Honest-cost flagging obligation: if cost surfaces, flag in close report
  with evidence; NEVER route around correctness with a wrong-but-cheap date.

Query filter (per family):
  {decision: "refused", "stamp_audit.refusal_family": <family>}
  sort by `at` ascending, project `_id: 0, at: 1`, limit 1.

Pre-Sub-stage-1 refusal rows lack `stamp_audit["refusal_family"]` (pinned
key wire-up is what Sub-stage 1 lands). Those rows drop out of the query
naturally — β "reports what the ledger contains" (Owner verbatim).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from core import db
from services.compliance.refusals_coverage_response import RefusalsCoverageResponse


# The "seam-3 wire-up boundary" — set to the UTC date the Sub-stage 1
# emission wire-up landed on disk. Rows with `at` timestamp at OR AFTER
# this boundary are categorised under `families_since_seam_3`; rows
# strictly before are categorised under `families_since_system_start`.
# This constant is a DATE, not a coverage claim: families with an earliest
# pinned-key row before this date are surfaced honestly as "since system
# start"; families with only post-boundary pinned rows are surfaced
# as "since {seam_3 date}". E3.β preserved — nothing here fabricates a
# coverage date; the ledger's earliest timestamp per family is the truth.
_SEAM_3_WIRE_UP_DATE = "2026-07-06"


def _families_registry_path() -> Path:
    return Path(__file__).resolve().parent / "refusal_families.v0.json"


def _load_valid_families_ordered() -> Tuple[str, ...]:
    """Return the registry family names in registry order (deterministic)."""
    with _families_registry_path().open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return tuple(entry["family"] for entry in payload.get("valid_families", []))


def _row_at_to_iso_date(at_value) -> Optional[str]:
    """Extract YYYY-MM-DD UTC from a stored `at` value.

    Ledger row `at` is written via `LedgerRow.model_dump(mode="json")`
    which serializes datetime as ISO-8601 string. Fallback: accept native
    datetime for defense-in-depth.
    """
    if isinstance(at_value, str) and len(at_value) >= 10:
        return at_value[:10]
    if isinstance(at_value, datetime):
        if at_value.tzinfo is None:
            at_value = at_value.replace(tzinfo=timezone.utc)
        return at_value.date().isoformat()
    return None


async def compose_coverage_marker() -> RefusalsCoverageResponse:
    """Read per-family earliest pinned-key ledger row; compose the two
    family sets + per-family since-date map + earliest-across-seam-3 date.

    Pure query-time β per E3.β ruling — no cache, no materialization.
    """
    families = _load_valid_families_ordered()

    per_family_since_date: Dict[str, str] = {}
    families_since_system_start: List[str] = []
    families_since_seam_3: List[str] = []

    for family in families:
        # Query: earliest refusal-terminal row per family, matched via the
        # pinned `stamp_audit.refusal_family` key. Pre-wire-up rows without
        # the key are naturally excluded (β honest report).
        cursor = (
            db[NORTHENA_LEDGER_COLLECTION]
            .find(
                {
                    "decision": "refused",
                    "stamp_audit.refusal_family": family,
                },
                {"_id": 0, "at": 1},
            )
            .sort("at", 1)
            .limit(1)
        )
        earliest = None
        async for row in cursor:
            earliest = _row_at_to_iso_date(row.get("at"))
            break
        if earliest is None:
            continue
        per_family_since_date[family] = earliest
        if earliest < _SEAM_3_WIRE_UP_DATE:
            families_since_system_start.append(family)
        else:
            families_since_seam_3.append(family)

    seam_3_earliest_date: Optional[str] = None
    if families_since_seam_3:
        seam_3_earliest_date = min(
            per_family_since_date[f] for f in families_since_seam_3
        )

    honest_note: Optional[str] = None
    if not per_family_since_date:
        honest_note = (
            "No refusal-terminal rows with a registered refusal_family "
            "have been recorded yet · this card will populate as families fire."
        )

    return RefusalsCoverageResponse(
        families_since_system_start=sorted(families_since_system_start),
        families_since_seam_3=sorted(families_since_seam_3),
        per_family_since_date=per_family_since_date,
        seam_3_earliest_date=seam_3_earliest_date,
        honest_note_when_no_families_covered=honest_note,
    )
