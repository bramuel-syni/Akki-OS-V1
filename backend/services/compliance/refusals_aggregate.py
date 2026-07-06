"""Refusals-by-month aggregate service (v2.1 §4.1 substrate; B-5a).

Queries `NorthenaLedgerRow_v1` where `decision == "refused"` within a
month window, classifies each row into a governed-refusal family per
`refusal_family_classifier`, and returns totals grouped by reason AND
by day (dev default ratified at Stage A: both groupings computed in one
Mongo aggregation pipeline).

Auth 403s and validation 422s are STRUCTURALLY excluded — they never
reach the `NorthenaLedgerRow_v1` collection. Exclusion is a property
of the query, not a filter.
"""
from __future__ import annotations

import calendar
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Tuple

from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
from services.compliance.refusals_aggregate_response import (
    RefusalDayCount,
    RefusalReasonCount,
    RefusalsAggregateResponse,
    RefusalsTotals,
)
from core import db
from services.compliance.refusal_family_classifier import (
    FAMILY_DISPLAY_ORDER,
    classify_family,
)


_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


class MalformedMonthError(ValueError):
    """Raised when the `month` query param is not `YYYY-MM`."""


def parse_month(month: str) -> Tuple[datetime, datetime]:
    """Return (start_inclusive, end_exclusive) UTC datetimes for the month.

    Raises MalformedMonthError on bad input — router maps to 400.
    """
    if not month or not _MONTH_RE.match(month):
        raise MalformedMonthError(
            f"Month must be YYYY-MM (got {month!r}). Example: 2026-07."
        )
    year_str, month_str = month.split("-")
    year = int(year_str)
    month_num = int(month_str)
    if month_num < 1 or month_num > 12:
        raise MalformedMonthError(
            f"Month component out of range 01-12 (got {month_str!r})."
        )
    start = datetime(year, month_num, 1, tzinfo=timezone.utc)
    # last day of month → next month's day 1 exclusive
    last_day = calendar.monthrange(year, month_num)[1]
    if month_num == 12:
        end = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(year, month_num + 1, 1, tzinfo=timezone.utc)
    _ = last_day  # documented above; not used numerically
    return start, end


async def aggregate_refusals_by_month(month: str) -> RefusalsAggregateResponse:
    """Read-only aggregate of refused ledger rows in the month window.

    Query filter: `decision == "refused"` (Union of admit-stage +
    gate-stage refusals per `NorthenaLedgerRow_v1` schema).

    Auth 403s + validation 422s excluded structurally: they never
    write to the ledger.
    """
    start, end = parse_month(month)
    cursor = db[NORTHENA_LEDGER_COLLECTION].find(
        {
            "decision": "refused",
            "at": {"$gte": start.isoformat(), "$lt": end.isoformat()},
        },
        {"_id": 0, "reason": 1, "at": 1},
    )
    family_totals: Counter = Counter()
    reason_counts: Counter = Counter()
    day_counts: Counter = Counter()
    async for row in cursor:
        reason = str(row.get("reason") or "")
        family = classify_family(reason)
        family_totals[family] += 1
        reason_counts[(reason, family)] += 1
        at_val = row.get("at")
        if isinstance(at_val, str) and len(at_val) >= 10:
            day_counts[at_val[:10]] += 1
        elif isinstance(at_val, datetime):
            day_counts[at_val.date().isoformat()] += 1
    totals = RefusalsTotals(
        admission_refusals=family_totals.get("admission_refusals", 0),
        composition_below_floor=family_totals.get("composition_below_floor", 0),
        outer_gate_refusals=family_totals.get("outer_gate_refusals", 0),
        unclassified=family_totals.get("unclassified", 0),
        total=sum(family_totals.values()),
    )
    by_reason_sorted = sorted(
        (
            RefusalReasonCount(reason=reason, family=family, count=count)
            for (reason, family), count in reason_counts.items()
        ),
        key=lambda r: (-r.count, r.reason),
    )
    by_day_sorted = sorted(
        (RefusalDayCount(day=day, count=count) for day, count in day_counts.items()),
        key=lambda d: d.day,
    )
    return RefusalsAggregateResponse(
        month=month,
        totals=totals,
        by_reason=by_reason_sorted,
        by_day=by_day_sorted,
    )
