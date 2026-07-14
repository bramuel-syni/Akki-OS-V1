"""Stamp-audit ring buffer — G1 placeholder for Northena's per-run ledger.

Approved discipline (stakeholder verbatim record): "Refusal reasons live
in StampAuditEntry (in-memory ring buffer at G1, absorbed by Northena's
ledger at G2). DefensibilityRing stays byte-identical to the G0 freeze.
A unit is the output of a decision; an audit entry is the trace of how
it was made. Different lifecycles — the unit schema is frozen because
everything binds to it; the trace schema is meant to evolve through
G2–G6. Coupling them would chain the stable artifact to the evolving one."

Cousin: `/reference/akki-legacy/backend/services/solva_v2/engines/refusal.py`
— the discipline of structured-refusal records logged OUTSIDE the
artefact they refused on.

Forward note (G2): swap `stamp_audit.record(entry)` → `northena_ledger.
record(entry)`. Single-line change; signature is intentionally identical.
"""
from __future__ import annotations

import os
from collections import deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Deque, List, Literal, Optional

_BUF_SIZE = int(os.environ.get("AKKI_STAMP_AUDIT_BUFFER_SIZE", "1024"))


@dataclass
class StampAuditEntry:
    unit_id: str
    decision: Literal["accept", "refuse"]
    reason: Optional[str] = None
    judged_signal_dimensions: List[str] = field(default_factory=list)
    floor_violation: bool = False
    runtime_mode: str = "declaration_baseline"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return asdict(self)


_RECENT_STAMP_AUDITS: Deque[StampAuditEntry] = deque(maxlen=_BUF_SIZE)


def record(entry: StampAuditEntry) -> None:
    _RECENT_STAMP_AUDITS.append(entry)


def recent(limit: int = 100) -> List[StampAuditEntry]:
    return list(_RECENT_STAMP_AUDITS)[-limit:][::-1]


def by_unit_id(unit_id: str) -> List[StampAuditEntry]:
    return [e for e in _RECENT_STAMP_AUDITS if e.unit_id == unit_id]


def _clear_for_test() -> None:
    _RECENT_STAMP_AUDITS.clear()


def buffer_size() -> int:
    return _BUF_SIZE
