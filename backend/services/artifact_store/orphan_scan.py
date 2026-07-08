"""Artifact Store orphan-scan — READ-ONLY (AS-E3 α).

Owner ruling AS-E3 α (2026-07-08):

    'α. Report-only. The scan is read-only; disposition of a real
     orphan is an owner-facing decision via the Seam 3 path, per
     AS-H1 verbatim. One interplay line with E2: the scan
     distinguishes in-flight writes (live tmp marker under threshold)
     from orphans — a transaction in progress is not a defect.'

AS-B2 (BCR §3.2:115): 'No artifact exists without its receipt and
ledger row; an orphan-artifact scan MUST return zero.'

Orphan-distinguisher (E2 interplay): a live tmp marker under the
recovery threshold is an in-flight transaction, NOT an orphan.
The scan excludes such keys from the orphan class.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Callable, List, Optional

from .adapter import _root
from .atomic_write import _tmp_threshold_seconds


@dataclass(frozen=True)
class OrphanScanResult:
    """Result of a `scan_orphans` invocation. Read-only — no side effects."""
    scanned: int
    orphans: List[str]
    in_flight: List[str]  # keys with live tmp markers under threshold (excluded from orphans)


def scan_orphans(
    *,
    receipt_exists: Callable[[str], bool],
    ledger_row_exists: Callable[[str], bool],
    now: Optional[float] = None,
) -> OrphanScanResult:
    """Enumerate final-key artifacts + partition by orphan-vs-in-flight.

    Args:
      receipt_exists: (key) -> bool; caller-supplied lookup on the receipt store.
      ledger_row_exists: (key) -> bool; caller-supplied lookup on the ledger.
      now: unix epoch seconds; defaults to time.time() (test injection).

    Returns OrphanScanResult with:
      * `orphans`: keys where final-key exists but (receipt+ledger_row) is missing
                   AND no live tmp under threshold. These are real orphans
                   requiring owner disposition via Seam 3.
      * `in_flight`: keys with a live tmp under threshold. NOT orphans (per E2 interplay).
      * `scanned`: total final-key candidates enumerated.

    NEVER modifies the artifact store. AS-B2 promise: in a well-formed
    system, `orphans == []`.
    """
    now_ts = time.time() if now is None else now
    threshold = _tmp_threshold_seconds()
    scanned = 0
    orphans: List[str] = []
    in_flight: List[str] = []

    root = _root()
    if not root.is_dir():
        return OrphanScanResult(scanned=0, orphans=[], in_flight=[])

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.name.endswith(".tmp"):
            continue  # tmp markers are handled below via companion final-key
        rel = str(path.relative_to(root))
        scanned += 1

        # E2 interplay: check for a companion live tmp under threshold.
        tmp_companion = path.parent / f"{path.name}.tmp"
        if tmp_companion.is_file():
            try:
                tmp_age = now_ts - tmp_companion.stat().st_mtime
                if tmp_age < threshold:
                    # Live in-flight transaction; NOT an orphan.
                    in_flight.append(rel)
                    continue
            except OSError:
                pass

        # AS-B2: orphan iff receipt or ledger row missing.
        if not (receipt_exists(rel) and ledger_row_exists(rel)):
            orphans.append(rel)

    return OrphanScanResult(scanned=scanned, orphans=orphans, in_flight=in_flight)
