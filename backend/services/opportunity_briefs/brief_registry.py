"""Brief registry — write-once + refresh-on-census-change (OB-R5).

Sidecar shape (NOT a frozen contract · parity 31 preserved). Own
in-memory table with the option to persist elsewhere later. Governed
purely by:

  * Write-once per (scope, contributing_slices_key, census_ref) — regeneration
    on census change marks the prior row `stale=True` but retains it
    per OB-R5 (Owner-verbatim: *"stale briefs marked, retained"*).
  * Every row carries `brief_id` in the `brief_` namespace (OB-E2 Seam-2 α).
  * Advisory marker attached at write time via `advisory_marker.attach()`
    (OB-E2 Seam-1 α · write-time layer).

`OpportunityBriefRow` = dict shape:
    {
      brief_id: str,                # prefixed `brief_`
      scope: "slice" | "combined" | "estate",
      contributing_slices: List[str],
      brief_text: str,
      quantitative_anchors: List[{value, registry_read_ref}],
      generated_at: ISO8601 str,
      census_ref: str,
      stale: bool,
      _advisory_marker: str,        # attached at write-time
    }
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from services.opportunity_briefs import BRIEF_ID_PREFIX
from services.opportunity_briefs.advisory_marker import attach as _attach_marker


def new_brief_id() -> str:
    """Return a fresh brief id in the OB-E2 Seam-2 α namespace."""
    return f"{BRIEF_ID_PREFIX}{uuid.uuid4().hex[:16]}"


class BriefRegistry:
    """In-memory brief registry (write-once + stale-on-refresh)."""

    def __init__(self) -> None:
        self._rows: Dict[str, Dict[str, Any]] = {}
        self._by_key: Dict[str, str] = {}  # (scope, slices_key, census_ref) -> brief_id

    def _row_key(
        self, scope: str, contributing_slices: List[str], census_ref: str,
    ) -> str:
        slices_key = ",".join(sorted(contributing_slices))
        return f"{scope}|{slices_key}|{census_ref}"

    def write(
        self,
        *,
        scope: str,
        contributing_slices: List[str],
        brief_text: str,
        quantitative_anchors: List[Dict[str, str]],
        census_ref: str,
    ) -> Dict[str, Any]:
        """Write a new brief row. If a prior row exists for the same
        (scope, contributing_slices, census_ref) tuple, mark it stale
        and retain (OB-R5).
        """
        key = self._row_key(scope, contributing_slices, census_ref)
        prior_brief_id = self._by_key.get(key)
        if prior_brief_id is not None:
            self._rows[prior_brief_id]["stale"] = True

        bid = new_brief_id()
        row = {
            "brief_id": bid,
            "scope": scope,
            "contributing_slices": list(contributing_slices),
            "brief_text": brief_text,
            "quantitative_anchors": list(quantitative_anchors),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "census_ref": census_ref,
            "stale": False,
        }
        row = _attach_marker(row)  # OB-E2 Seam-1 α write-time attach
        self._rows[bid] = row
        self._by_key[key] = bid
        return dict(row)

    def read(self, brief_id: str) -> Optional[Dict[str, Any]]:
        row = self._rows.get(brief_id)
        return dict(row) if row is not None else None

    def all_rows(self) -> List[Dict[str, Any]]:
        return [dict(r) for r in self._rows.values()]

    def refresh_on_census_change(self, new_census_ref: str) -> int:
        """Mark all rows with a census_ref != `new_census_ref` as stale.

        Returns the count of rows newly marked stale. Retained rows
        stay in the registry per OB-R5.
        """
        marked = 0
        for row in self._rows.values():
            if row["census_ref"] != new_census_ref and not row["stale"]:
                row["stale"] = True
                marked += 1
        return marked


# Process-wide singleton (import-time construction; fine for the current
# in-memory posture per §3.4 pre-production discipline).
_REGISTRY = BriefRegistry()


def registry() -> BriefRegistry:
    return _REGISTRY
