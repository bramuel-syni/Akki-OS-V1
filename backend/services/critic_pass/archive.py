"""Critic-pass append-only archive ledger.

Owner ruling: `docs/rulings/critic_pass_e1_2026_07_25.md` (2026-07-25 · FINAL).

CIF §12 line 154 verbatim: *"Archive: entries as append-only ledger
rows; a standing query surfaces evaluated-but-unarchived ideas as
findings."*

CIF §14.2 verbatim: *"The archive initializes as a governed file with
CIF as entry #1."*

Discipline anchor: `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable`.
Rides existing Northena ledger machinery pattern — same discipline as
EAB-2 batch-quarantine ledger + EAB-3 partition-promotion ledger.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Literal, Optional
import threading


ArchiveEntryType = Literal[
    "cif_entry_1_seed",       # CIF §14.2 · seed row
    "evaluated_idea",         # Owner-verbatim "evaluated-but-unarchived" → archived
    "critic_verdict",         # Tier-2 rubric verdict archive
    "seeded_defect_verdict",  # Tier-3 seeded-defect audit result
]


@dataclass(frozen=True)
class ArchiveLedgerRow:
    """Append-only archive ledger row.

    IMMUTABLE by construction (frozen dataclass). Once appended, rows
    never mutate — this is the load-bearing discipline of
    `PROM-S3-append-only-ledger`.
    """

    row_id: int
    entry_type: ArchiveEntryType
    subject_ref: str
    appended_at: str  # ISO-8601 UTC
    evaluated_by: Optional[str] = None  # instance_id of the evaluator
    verdict_ref: Optional[str] = None   # verdict artifact SHA / ref


# ---------------------------------------------------------------------------
# In-memory ledger (rides existing Northena ledger machinery pattern; same
# posture as EAB-2 QuarantineEvent + EAB-3 PartitionPromotionLedgerRow).
# ---------------------------------------------------------------------------

_LOCK = threading.Lock()
_LEDGER: List[ArchiveLedgerRow] = []
_NEXT_ROW_ID: int = 1


def _reset_for_tests() -> None:
    """Test hook · reset ledger state for isolated test runs."""
    global _NEXT_ROW_ID
    with _LOCK:
        _LEDGER.clear()
        _NEXT_ROW_ID = 1


def _isoformat_utc() -> str:
    """UTC ISO-8601 timestamp with microsecond precision."""
    return datetime.now(timezone.utc).isoformat()


def initialize_with_cif_seed() -> ArchiveLedgerRow:
    """CIF §14.2 verbatim: 'The archive initializes as a governed file
    with CIF as entry #1.' Seed row landed at Critic-pass execution atomic.

    Idempotent: subsequent calls return the existing seed row (never
    duplicates entry #1).
    """
    global _NEXT_ROW_ID
    with _LOCK:
        for row in _LEDGER:
            if row.entry_type == "cif_entry_1_seed":
                return row
        seed = ArchiveLedgerRow(
            row_id=_NEXT_ROW_ID,
            entry_type="cif_entry_1_seed",
            subject_ref="docs/requirements/cif_spec_v1.md",
            appended_at=_isoformat_utc(),
            evaluated_by=None,
            verdict_ref=None,
        )
        _LEDGER.append(seed)
        _NEXT_ROW_ID += 1
        return seed


def append(
    entry_type: ArchiveEntryType,
    subject_ref: str,
    evaluated_by: Optional[str] = None,
    verdict_ref: Optional[str] = None,
) -> ArchiveLedgerRow:
    """Append a new row to the archive ledger.

    PROM-S3-append-only-ledger discipline: rows are IMMUTABLE post-append.
    """
    global _NEXT_ROW_ID
    if entry_type == "cif_entry_1_seed":
        # Prevent duplicate seed rows; route through initialize_with_cif_seed.
        raise ValueError(
            "cif_entry_1_seed rows are seeded via initialize_with_cif_seed(); "
            "direct append is not allowed."
        )
    with _LOCK:
        row = ArchiveLedgerRow(
            row_id=_NEXT_ROW_ID,
            entry_type=entry_type,
            subject_ref=subject_ref,
            appended_at=_isoformat_utc(),
            evaluated_by=evaluated_by,
            verdict_ref=verdict_ref,
        )
        _LEDGER.append(row)
        _NEXT_ROW_ID += 1
        return row


def get_ledger() -> List[ArchiveLedgerRow]:
    """Return a snapshot of the ledger (immutable view)."""
    with _LOCK:
        return list(_LEDGER)


def evaluated_but_unarchived_query(
    evaluated_refs: List[str],
) -> List[str]:
    """CIF §12 line 154 verbatim: *"a standing query surfaces
    evaluated-but-unarchived ideas as findings."*

    Given a list of `evaluated_refs` (subject_refs that have been
    evaluated), returns the refs that are NOT present in the archive
    ledger. These are surfaced as findings per QA-1 (detect, never
    decide).
    """
    with _LOCK:
        archived = {row.subject_ref for row in _LEDGER}
    return [ref for ref in evaluated_refs if ref not in archived]
