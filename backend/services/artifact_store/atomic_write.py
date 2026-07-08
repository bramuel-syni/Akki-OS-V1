"""Artifact Store atomic-write protocol — six-step (AS-E2 γ).

Owner ruling AS-E2 γ + recovery rule (2026-07-08):

    'γ, with the recovery rule explicit. Copy-not-move at step 3,
     dual-copy retention through step 6, GC tmp only after the ledger
     row lands. The tmp object is the in-flight transaction marker.
     Recovery rule: any tmp past threshold → if receipt + ledger row
     complete, GC tmp; else delete the final-key object and GC tmp
     (transaction abort). Clarification so AS-H1 isn't tripped:
     rollback of an incomplete write is transaction mechanics, not
     data deletion — the artifact never existed in the governed
     sense (no receipt, no row).'

Six steps (BCR §3.2:130-133 verbatim):
  1. put to `{key}.tmp`
  2. verify sha256
  3. COPY (not move) to final key       -- AS-E2 γ: copy semantics
  4. head-verify final key
  5. write receipt (OuterGateReceipt_v1 with artifact_sha256 + artifact_key)
  6. emit ledger row
  Failure at any step 1..5 => tmp GC'd + final-key GC'd (transaction abort).
  Failure at step 6 => `reconcile_incomplete_write` (below) sweeps on schedule.

Dev-tier tmp threshold: 300 seconds (env
`RMS_ARTIFACT_STORE_TMP_THRESHOLD_SECONDS`).
"""
from __future__ import annotations

import hashlib
import os
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional

from .adapter import (
    ArtifactStoreAdapter,
    _abs_path,
    _get_raw,  # internal caller — step 4 head-verify
    _root,
)


TMP_THRESHOLD_SECONDS_DEFAULT = 300  # Tier-3 default: 5 minutes.


def _tmp_threshold_seconds() -> int:
    return int(os.environ.get("RMS_ARTIFACT_STORE_TMP_THRESHOLD_SECONDS",
                              str(TMP_THRESHOLD_SECONDS_DEFAULT)))


@dataclass(frozen=True)
class AtomicWriteResult:
    """Result of a successful six-step atomic write."""
    key: str
    sha256: str
    size: int
    receipt: object  # OuterGateReceiptV1; kept as object here to avoid contract-import churn
    ledger_row_id: str


class AtomicWriteError(Exception):
    """Raised on any step 1..5 failure; the transaction is aborted before raise."""


def atomic_put_with_receipt(
    key: str,
    data: bytes,
    content_type: str,
    *,
    build_receipt_v1: Callable[[str, str], object],
    emit_ledger_row: Callable[[object], str],
    adapter: Optional[ArtifactStoreAdapter] = None,
) -> AtomicWriteResult:
    """Six-step atomic write per AS-E2 γ + recovery rule.

    Args:
      key: `artifacts/{trace_id}/{artifact_id}.{ext}`.
      data: bytes to store.
      content_type: MIME hint; not enforced (Tier-3: no MIME sniffing).
      build_receipt_v1: callable (artifact_sha256, artifact_key) -> receipt object.
      emit_ledger_row: callable (receipt) -> ledger_row_id (str).

    On any step 1..5 failure, both tmp AND final-key object are GC'd
    (transaction abort — rollback is mechanics per Owner E2). AS-H1
    is NOT tripped: no receipt, no ledger row ever landed → the
    artifact did not exist in the governed sense.

    Failure at step 6 leaves tmp + final-key + receipt on disk;
    `reconcile_incomplete_write` sweeps such state on schedule.
    """
    adapter = adapter or ArtifactStoreAdapter()
    tmp_path = _abs_path(f"{key}.tmp")
    final_path = _abs_path(key)

    # AS-B1 write-once: fail early if final key already exists.
    if final_path.exists():
        from .adapter import ArtifactKeyExistsError
        raise ArtifactKeyExistsError(key)

    receipt_written = False
    try:
        # Step 1 — put to `{key}.tmp`.
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_bytes(data)

        # Step 2 — verify sha256.
        computed_sha = hashlib.sha256(data).hexdigest()
        tmp_sha = hashlib.sha256(tmp_path.read_bytes()).hexdigest()
        if computed_sha != tmp_sha:
            raise AtomicWriteError(
                f"step 2 sha256 mismatch: computed={computed_sha} tmp={tmp_sha}"
            )

        # Step 3 — COPY (not move) to final key. AS-E2 γ dual-copy semantics.
        final_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tmp_path, final_path)

        # Step 4 — head-verify final key (internal caller of _get_raw).
        final_bytes = _get_raw(key)
        final_sha = hashlib.sha256(final_bytes).hexdigest()
        if final_sha != computed_sha:
            raise AtomicWriteError(
                f"step 4 head-verify mismatch: expected={computed_sha} final={final_sha}"
            )

        # Step 5 — write receipt (OuterGateReceipt_v1 with artifact_sha256 + artifact_key).
        receipt = build_receipt_v1(final_sha, key)
        receipt_written = True

        # Step 6 — emit ledger row.
        ledger_row_id = emit_ledger_row(receipt)

        # SUCCESS — GC tmp (dual-copy no longer needed).
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            # Best-effort GC; reconcile sweep will catch it.
            pass

        return AtomicWriteResult(
            key=key,
            sha256=final_sha,
            size=len(data),
            receipt=receipt,
            ledger_row_id=ledger_row_id,
        )

    except Exception as exc:
        # Rollback: transaction mechanics, NOT AS-H1 authorized deletion.
        # No receipt persisted, no ledger row emitted → artifact never
        # existed in the governed sense. Wipe tmp + final-key.
        # Exception: if step 6 (post-receipt) fails, the receipt is
        # already committed by the caller's build_receipt_v1 side effect
        # (in-memory here; caller decides whether to persist). The
        # reconcile sweep handles that case separately.
        if not receipt_written:
            try:
                tmp_path.unlink(missing_ok=True)
            except OSError:
                pass
            try:
                final_path.unlink(missing_ok=True)
            except OSError:
                pass
        # Re-raise the underlying failure to the caller (AtomicWriteError
        # or any lower-level exception).
        if isinstance(exc, AtomicWriteError):
            raise
        raise AtomicWriteError(str(exc)) from exc


@dataclass(frozen=True)
class ReconcileResult:
    """Result of a `reconcile_incomplete_write` sweep."""
    scanned: int
    gcd_success: List[str]           # tmp GC'd because receipt+ledger row exist (successful writes)
    aborted: List[str]               # final-key deleted + tmp GC'd (transaction aborts)


def reconcile_incomplete_write(
    *,
    receipt_exists: Callable[[str], bool],
    ledger_row_exists: Callable[[str], bool],
    now: Optional[float] = None,
) -> ReconcileResult:
    """Recovery rule (Owner AS-E2 γ verbatim):

        'Recovery rule: any tmp past threshold → if receipt + ledger
         row complete, GC tmp; else delete the final-key object and
         GC tmp (transaction abort). Clarification so AS-H1 isn't
         tripped: rollback of an incomplete write is transaction
         mechanics, not data deletion — the artifact never existed
         in the governed sense (no receipt, no row).'

    Args:
      receipt_exists: (key) -> bool; caller-supplied lookup on the receipt store.
      ledger_row_exists: (key) -> bool; caller-supplied lookup on the ledger.
      now: unix epoch seconds; defaults to time.time() (test injection).

    AS-H1 non-trip: `os.unlink(final_path)` is filesystem transaction
    mechanics; no `NorthenaLedgerRow_v1` emitted on abort.
    """
    now_ts = time.time() if now is None else now
    threshold = _tmp_threshold_seconds()
    scanned = 0
    gcd_success: List[str] = []
    aborted: List[str] = []

    root = _root()
    if not root.is_dir():
        return ReconcileResult(scanned=0, gcd_success=[], aborted=[])

    for tmp_path in root.rglob("*.tmp"):
        scanned += 1
        try:
            age = now_ts - tmp_path.stat().st_mtime
        except OSError:
            continue
        if age < threshold:
            # Live in-flight transaction; not an orphan.
            continue

        # Reconstruct the artifact key from the tmp path (strip `.tmp` suffix).
        rel = tmp_path.relative_to(root)
        key = str(rel)[:-len(".tmp")]
        final_path = root / key

        if receipt_exists(key) and ledger_row_exists(key):
            # Successful write; tmp is stale. GC.
            try:
                tmp_path.unlink(missing_ok=True)
                gcd_success.append(key)
            except OSError:
                continue
        else:
            # Transaction abort. Delete final-key + GC tmp.
            try:
                if final_path.is_file():
                    final_path.unlink()
                tmp_path.unlink(missing_ok=True)
                aborted.append(key)
            except OSError:
                continue

    return ReconcileResult(
        scanned=scanned,
        gcd_success=gcd_success,
        aborted=aborted,
    )
