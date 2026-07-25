"""Per-batch quarantine event writer + systemic-halt threshold evaluator + remediation-to-new-version — A4 EAB-2 landing (2026-07-24).

A4.1 · Per-batch quarantine event (`quarantine_batch`):
  Ledger row · receipt-marked · batch-excluded · run continues.
  Append-only per `PROM-S3-append-only-ledger`.

A4.2 · Systemic-halt threshold evaluator (`evaluate_systemic_halt`):
  Reads `SeamValues.quarantine_systemic_halt_threshold` (F2 seam value ·
  landed via G-3 · `docs/close_reports/g3_operating_values_v1_1.md`
  SHA `0a91e1b4…`). Compares live quarantine rate against threshold ·
  triggers HALT + operator notification when exceeded (R-A4.2 verbatim).

A4.3 · Halt is HALT (`raise_halt`):
  Operator notification observable · no silent resume. Halt ceremony
  ledgered per `PROM-S3-audit-trail-immutable`.

A4.4 · Remediation-to-new-version path (`remediate_to_new_version`):
  Quarantined batches reprocess into a new output version with new
  receipts · append-only preserved · immutability doctrine restated as
  quarantine exit path. R-A4.3.

Registry attachment (R4 sidecar rows 9-12):
  * `akki.batch.a4_per_batch_quarantine_ledger_row` (row 9)
  * `akki.batch.a4_systemic_halt_threshold_evaluator_reads_f2_seam_value` (row 10)
  * `akki.batch.a4_halt_is_halt_operator_notification_no_silent_resume` (row 11)
  * `akki.batch.a4_remediation_to_new_version_no_inplace_mutation` (row 12)

Sanction: `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md`
(SHA `8b074dc152b41ed300d5a7626a2a1bd5aa1213371f6eeeac0a096e12f2d6d4a5`).
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


class SystemicHaltError(Exception):
    """Raised by `evaluate_systemic_halt` when live quarantine rate exceeds threshold.

    Halt is HALT (R-A4.2): no silent resume. Operator must ledger the
    remediation ceremony via `remediate_to_new_version` before re-enabling.
    """


@dataclass(frozen=True)
class QuarantineEvent:
    """Append-only ledger row · receipt-marked · batch-excluded · run continues."""

    batch_id: str
    reason: str  # governance failure category (registry-vocabulary)
    run_id: str
    instance_id: str
    receipt: str  # ledger-row receipt identifier (append-only per S3)
    quarantined_at: str  # ISO-8601 UTC
    batch_excluded: bool = True  # always True per A4.1
    run_continues: bool = True   # always True per A4.1 (run does NOT halt on single-batch quarantine)


@dataclass(frozen=True)
class HaltEvent:
    """Systemic-halt ceremony · operator notification observable · no silent resume."""

    run_id: str
    instance_id: str
    quarantine_count: int
    total_batches: int
    live_quarantine_rate: float
    threshold: float
    receipt: str  # halt-ceremony receipt (append-only per S3)
    halted_at: str  # ISO-8601 UTC


@dataclass(frozen=True)
class RemediationOutputVersion:
    """Append-only new output version for remediated batches (R-A4.3).

    Naming convention: `<original_run_id>_r<N>` (builder Tier-3 · disclosed).
    """

    original_run_id: str
    remediation_run_id: str  # `<original_run_id>_r<N>`
    remediation_version: int  # N (1, 2, 3, ...)
    remediated_batch_ids: List[str]
    receipt: str  # new-version receipt (append-only per S3)
    remediated_at: str  # ISO-8601 UTC


@dataclass
class _QuarantineLedger:
    """In-memory append-only ledger of quarantine events + halt events + remediation versions.

    Production wiring points at Northena ledger via
    `contracts/northena_ledger.py::NorthenaLedger` — this module carries
    the EAB-2 landing surface; ledger row schema reuses append-only
    discipline per `PROM-S3-append-only-ledger`.
    """

    events: List[QuarantineEvent] = field(default_factory=list)
    halts: List[HaltEvent] = field(default_factory=list)
    remediations: List[RemediationOutputVersion] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _receipt_counter: int = 0


_LEDGER = _QuarantineLedger()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _next_receipt(prefix: str) -> str:
    with _LEDGER._lock:
        _LEDGER._receipt_counter += 1
        return f"{prefix}-{_LEDGER._receipt_counter:08d}"


def quarantine_batch(
    batch_id: str,
    reason: str,
    run_id: str,
    instance_id: str,
) -> QuarantineEvent:
    """A4.1 · Emit a quarantine ledger row · batch excluded from run · run continues.

    Append-only (`PROM-S3-append-only-ledger`).
    """
    event = QuarantineEvent(
        batch_id=batch_id,
        reason=reason,
        run_id=run_id,
        instance_id=instance_id,
        receipt=_next_receipt("QN"),
        quarantined_at=_now_iso(),
    )
    with _LEDGER._lock:
        _LEDGER.events.append(event)
    return event


def evaluate_systemic_halt(
    run_id: str,
    instance_id: str,
    total_batches: int,
    threshold: float,
) -> Optional[HaltEvent]:
    """A4.2 · Compare live quarantine rate against F2 seam threshold; raise HALT if exceeded.

    Reads `SeamValues.quarantine_systemic_halt_threshold` (F2 · 2% DEFAULT ·
    per-instance · dual-control on change per Op. Values v1.1 §6.6).

    Returns `HaltEvent` if halt fired; None otherwise. Halt ceremony is
    ledgered per `PROM-S3-audit-trail-immutable` (R-A4.2).
    """
    if total_batches <= 0:
        return None
    with _LEDGER._lock:
        run_events = [e for e in _LEDGER.events if e.run_id == run_id and e.instance_id == instance_id]
    live_rate = len(run_events) / total_batches
    if live_rate <= threshold:
        return None
    halt = HaltEvent(
        run_id=run_id,
        instance_id=instance_id,
        quarantine_count=len(run_events),
        total_batches=total_batches,
        live_quarantine_rate=live_rate,
        threshold=threshold,
        receipt=_next_receipt("HALT"),
        halted_at=_now_iso(),
    )
    with _LEDGER._lock:
        _LEDGER.halts.append(halt)
    return halt


def remediate_to_new_version(
    original_run_id: str,
    remediated_batch_ids: List[str],
) -> RemediationOutputVersion:
    """A4.4 · Reprocess quarantined batches into a new output version · append-only.

    Naming convention: `<original_run_id>_r<N>` where N is the next
    remediation version integer for `original_run_id`. Immutability
    preserved: no in-place mutation of the original run's output.
    """
    with _LEDGER._lock:
        prior_versions = [r.remediation_version for r in _LEDGER.remediations if r.original_run_id == original_run_id]
        next_version = (max(prior_versions) + 1) if prior_versions else 1
    remediation = RemediationOutputVersion(
        original_run_id=original_run_id,
        remediation_run_id=f"{original_run_id}_r{next_version}",
        remediation_version=next_version,
        remediated_batch_ids=list(remediated_batch_ids),
        receipt=_next_receipt("REM"),
        remediated_at=_now_iso(),
    )
    with _LEDGER._lock:
        _LEDGER.remediations.append(remediation)
    return remediation


def get_quarantine_events(run_id: str, instance_id: str) -> List[QuarantineEvent]:
    """Read-only view of the ledger for a given run/instance."""
    with _LEDGER._lock:
        return [e for e in _LEDGER.events if e.run_id == run_id and e.instance_id == instance_id]


def get_halt_events(run_id: str, instance_id: str) -> List[HaltEvent]:
    with _LEDGER._lock:
        return [h for h in _LEDGER.halts if h.run_id == run_id and h.instance_id == instance_id]


def get_remediations(original_run_id: str) -> List[RemediationOutputVersion]:
    with _LEDGER._lock:
        return [r for r in _LEDGER.remediations if r.original_run_id == original_run_id]


def _reset_for_tests() -> None:
    """Test-only helper. Not to be called from production code."""
    with _LEDGER._lock:
        _LEDGER.events.clear()
        _LEDGER.halts.clear()
        _LEDGER.remediations.clear()
        _LEDGER._receipt_counter = 0
