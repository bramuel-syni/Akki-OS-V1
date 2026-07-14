"""Northena Ledger — append-only write path (mandate §7).

Frozen contract: `northena_ledger_row@v0` in `contracts/northena_ledger.py`.
Frozen collection: `NORTHENA_LEDGER_COLLECTION = "northena_ledger_rows"`.

Cousin substrate — LIFT_AND_RESHAPE:
  `services/synisense/shield/audit_log.py::write_audit`. Same
  "insert-one row per governance event" pattern; adapted to run-level
  Ledger rows rather than per-invocation Shield rows. Session shape
  from cousin explicitly NOT copied per mandate §12.

Public API:
  * `record(row)`             — append a row (mandate §7.2, N-INV-8).
  * `absorb_stamp_audit(...)` — §7.3 G2 swap-in for G1 stamp entries.
  * `retention_mode()`        — read env for §11 (DPO open decision).

Read-side query surfaces (`by_run`, `open_runs`) live in
`routers/northena.py` where the API-shape belongs. Ledger owns writes.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Dict, Optional

from contracts.northena_ledger import (
    NORTHENA_LEDGER_COLLECTION,
    LedgerArtifactRef,
    LedgerRow,
)
from core import db


def retention_mode() -> str:
    """Northena Ledger retention policy — DPO open decision (§11).

    G4 posture (user directive (1)): **indefinite, append-only, configurable.**
    Retention is a parameter defaulting to INDEFINITE. End-of-window
    deletion stays UNIMPLEMENTED until DPO sets a window. Indefinite +
    immutable can be narrowed later without data loss; a default deletion
    window cannot be undone.

    Configuration surface: `AKKI_NORTHENA_LEDGER_RETENTION_MODE` env var.
    Valid values: `'indefinite'` (default) | `'windowed'` (implementation
    LOCKED until DPO decision). If `'windowed'` is set without a matching
    DPO-authorised deletion code path, `record()` continues to append
    normally — the mode label alone does not enable deletion. See
    `test_northena_ledger_no_deletion_path` invariant.
    """
    return os.environ.get("AKKI_NORTHENA_LEDGER_RETENTION_MODE", "indefinite")


def retention_window_days() -> Optional[int]:
    raw = os.environ.get("AKKI_NORTHENA_LEDGER_RETENTION_WINDOW_DAYS")
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


async def record(row: LedgerRow) -> None:
    """Append-only insert. No update, no delete. §7.2 + N-INV-8."""
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump(mode="json"))


async def absorb_stamp_audit(
    *,
    run_id: str,
    trace_id: str,
    stage: str,
    entry: Dict,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: str,
    reason: str = "stamp_audit_absorbed",
) -> LedgerRow:
    """§7.3 — G2 swap-in for G1's in-memory StampAuditEntry buffer.

    `entry` is a dict shaped by
    `services/g1_defensibility/stamp_audit.py::StampAuditEntry.to_dict()`.
    Ledger `decision` derives from entry.decision: 'accept'→'warm'
    (stamp accepted implies unit warm-serves), 'refuse'→'refused'
    (§7.1: refusals recorded, never dropped — N-INV-9).
    """
    entry_decision = str(entry.get("decision", "")).lower()
    if entry_decision == "accept":
        ledger_decision = "warm" if stage == "gate" else "admitted"
    elif entry_decision == "refuse":
        ledger_decision = "refused"
    else:
        raise ValueError(f"absorb_stamp_audit: unrecognised entry.decision={entry_decision!r}")
    if stage not in ("admit", "gate", "converge"):
        raise ValueError(f"absorb_stamp_audit: unknown stage {stage!r}")
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id,
        stage=stage,  # type: ignore[arg-type]
        decision=ledger_decision,  # type: ignore[arg-type]
        reason=reason,
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
        stamp_audit={
            "unit_id": entry.get("unit_id"),
            "decision": entry.get("decision"),
            "reason": entry.get("reason"),
            "judged_signal_dimensions": entry.get("judged_signal_dimensions", []),
            "floor_violation": bool(entry.get("floor_violation", False)),
        },
        at=datetime.now(timezone.utc),
    )
    await record(row)
    return row


# `absorb_solva_trace` (G3) lives in `services/northena/converge.py` — the
# stage owner of the converge-stage row emission per N-INV-6.
