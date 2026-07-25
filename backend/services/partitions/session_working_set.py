"""Session working-set service + partition-refresh discipline (EAB-3 A5 landing · 2026-07-24).

Sanction:
  * `docs/rulings/eab_3_e1_2026_07_24.md` — Owner ruled (a1) single-contract landing.
  * `docs/stage_a_proposals/eab_3_stage_a.md` §4.C + §4.D + §4.E.

R-A5.3 verbatim (byte-carried): *"Partition refresh is a cold-path batch job; the
previous version serves until the new version is atomically promoted; promotion
is ledgered."*

R-A5.4 verbatim (byte-carried): *"Iterative surfaces (adjust→re-ask) reuse
session-loaded partitions and intermediate aggregates; only deltas recompute.
Cache entries bind to partition version — promotion invalidates dependents, so
one cited result NEVER mixes evidence versions. Cache stores partition
references + derived arithmetic, never re-materialized raw — no ungoverned data
path; cache reads inherit the session's validated purpose."*

R-A5.5 verbatim (byte-carried): *"Every partition version records the receipt
set it was built from; every answer cites partition versions; the chain
number→partition→receipts→operations is mechanically walkable with zero
additional retrieval at request time."*

Fence: this service imports NOTHING from `backend.services.targeta.gate` or
`backend.services.targeta.yield_layer` (eligibility-computing modules · §1.2
eligibility-wall discipline). AST negative-scan cell at
`tests/invariants/test_partition_schema_v0_envelope.py::
test_session_working_set_no_targeta_eligibility_import` enforces at CI.

Fence: this service does NOT query the raw or qualified estate at request time
(R-A5.2 · ES-1 rule per `docs/rulings/es1_scope_2026-07-14.md` L9-19). Cache
reads only. Companion latency telemetry sidecar per AF-E3 α + AF-E4 α
precedent.

Class E annotation (Owner ITEM 1 forward-binding · Change Order A3.4):
eviction discipline (promotion-invalidation-only), refresh cadence, and
latency-telemetry storage are Class E engine parameters · pinned per engine
version · changed via version bumps with evaluation verdicts · E→O promotion
path per A3.2 for runtime tunability.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from contracts.partition_schema import PartitionSchema_v0


# ---------------------------------------------------------------------------
# Partition-refresh discipline (R-A5.3) — cold-path batch job with atomic
# promotion + ledgered ceremony.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PartitionPromotionLedgerRow:
    """Append-only Northena ledger row for R-A5.3 atomic promotion ceremony.

    Immutable per `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable`
    + `PROM-S3-mechanical-audit-of-promotion` (container-promotion precedent
    extended to partition-promotion).
    """

    promotion_id: str  # unique per promotion event
    partition_id: str
    schema_version: str
    prior_version_receipt_set_ref: Optional[str]  # None on first promotion of a partition
    new_version_receipt_set_ref: str
    promoted_at: str  # ISO-8601 UTC
    instance_id: str


@dataclass
class _PartitionStore:
    """In-memory partition ledger. Production wiring points at Northena via
    contracts/northena_ledger.py::NorthenaLedger — this module carries the
    EAB-3 landing surface; ledger row schema reuses append-only discipline
    per `PROM-S3-append-only-ledger`.
    """

    # Current-authoritative partition per (partition_id, instance_id) tuple.
    current: Dict[Tuple[str, str], PartitionSchema_v0] = field(default_factory=dict)
    # Historical partitions (superseded). Preserved byte-identical per
    # `PROM-S3-append-only-ledger`.
    history: List[PartitionSchema_v0] = field(default_factory=list)
    # Promotion ledger. Append-only.
    promotion_ledger: List[PartitionPromotionLedgerRow] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _promotion_counter: int = 0


_STORE = _PartitionStore()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def promote_partition(
    partition_id: str,
    schema_version: str,
    key_dimensions: List[str],
    receipt_set_ref: str,
    size_bytes: int,
    instance_id: str,
) -> Tuple[PartitionSchema_v0, PartitionPromotionLedgerRow]:
    """R-A5.3 atomic promotion · previous version serves until this call returns.

    Steps (atomic under lock):
      1. Look up current partition for (partition_id, instance_id).
      2. If present, stamp `superseded_at` on prior version and archive to history.
      3. Emit new PartitionSchema@v0 with `promoted_at = now()`.
      4. Emit promotion ledger row (append-only).
      5. Swap current pointer.

    Read-authoritative pointer flips atomically at swap. Callers see either the
    prior version or the new version, never a partial state.
    """
    key = (partition_id, instance_id)
    with _STORE._lock:
        _STORE._promotion_counter += 1
        promotion_id = f"PROM-{_STORE._promotion_counter:08d}"
        now = _now_iso()

        prior = _STORE.current.get(key)
        if prior is not None:
            # Archive prior version with superseded_at stamped (immutable-once-set).
            superseded = PartitionSchema_v0(
                partition_id=prior.partition_id,
                schema_version=prior.schema_version,
                key_dimensions=list(prior.key_dimensions),
                receipt_set_ref=prior.receipt_set_ref,
                promoted_at=prior.promoted_at,
                superseded_at=now,
                partition_shape_kind=prior.partition_shape_kind,
                size_bytes=prior.size_bytes,
                instance_id=prior.instance_id,
            )
            _STORE.history.append(superseded)

        new_partition = PartitionSchema_v0(
            partition_id=partition_id,
            schema_version=schema_version,
            key_dimensions=list(key_dimensions),
            receipt_set_ref=receipt_set_ref,
            promoted_at=now,
            superseded_at=None,
            partition_shape_kind="columnar_memmap",
            size_bytes=size_bytes,
            instance_id=instance_id,
        )

        ledger_row = PartitionPromotionLedgerRow(
            promotion_id=promotion_id,
            partition_id=partition_id,
            schema_version=schema_version,
            prior_version_receipt_set_ref=(prior.receipt_set_ref if prior is not None else None),
            new_version_receipt_set_ref=receipt_set_ref,
            promoted_at=now,
            instance_id=instance_id,
        )
        _STORE.promotion_ledger.append(ledger_row)

        # Atomic swap.
        _STORE.current[key] = new_partition

    return new_partition, ledger_row


def read_current_partition(partition_id: str, instance_id: str) -> Optional[PartitionSchema_v0]:
    """R-A5.3 · previous version serves until the new version is atomically promoted.

    Returns the current-authoritative PartitionSchema@v0 or None if none exists.
    """
    with _STORE._lock:
        return _STORE.current.get((partition_id, instance_id))


def get_partition_history(partition_id: str, instance_id: str) -> List[PartitionSchema_v0]:
    """Read-only view of superseded versions for the given partition · lineage walk."""
    with _STORE._lock:
        return [
            p for p in _STORE.history
            if p.partition_id == partition_id and p.instance_id == instance_id
        ]


def get_promotion_ledger(instance_id: str) -> List[PartitionPromotionLedgerRow]:
    with _STORE._lock:
        return [r for r in _STORE.promotion_ledger if r.instance_id == instance_id]


# ---------------------------------------------------------------------------
# Session working-set (R-A5.4) — cache-references-and-arithmetic-only.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WorkingSetEntry:
    """A cache entry in a session working-set.

    Stores partition reference + derived arithmetic ONLY. Never re-materialized
    raw. Bound to partition version at session-open per R-A5.4 verbatim (*"Cache
    entries bind to partition version — promotion invalidates dependents"*).

    Registry attachments:
      * `PROM-S1-honesty-grammar-source-labels` — cache stores partition
        references + derived arithmetic ONLY.
      * `PROM-S2-slice-freeze-at-commission` (extended) — session-freeze-at-open
        · no silent version-drift.
      * `PROM-S3-audit-trail-immutable` — cache reads inherit session's
        validated purpose.
    """

    partition_ref: str  # `partition_id`
    partition_version_receipt_set_ref: str  # the FK to the receipt set of the bound partition version
    derived_arithmetic_key: str  # cache key (dimension tuple digest)
    derived_arithmetic_value: str  # arithmetic result (registry-vocabulary source-labeled)


class MixedPartitionVersionError(Exception):
    """R-A5.4 · one cited result NEVER mixes evidence versions.

    Raised when a session working-set is asked to serve arithmetic that would
    span two partition versions of the same partition_id. AC-A5.c version-skew
    wire cell asserts this raises.
    """


@dataclass
class SessionWorkingSet:
    """Per-session cache with partition-version binding + purpose inheritance.

    R-A5.4 verbatim discipline:
      * Cache entries bind to partition version.
      * Promotion invalidates dependents.
      * Cache stores partition references + derived arithmetic ONLY.
      * Cache reads inherit session's validated purpose.
    """

    session_id: str
    validated_purpose: str  # inherited from session · R-A5.4 · not bypassable through working-set path
    _entries: List[WorkingSetEntry] = field(default_factory=list)
    _bound_partition_versions: Dict[str, str] = field(default_factory=dict)
    # `partition_id -> receipt_set_ref` binding · locked at first bind ·
    # session cannot mix versions (AC-A5.c version-skew invariant).
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def bind_partition(self, partition: PartitionSchema_v0) -> None:
        """R-A5.4 · session binds to a specific partition version at open time.

        Raises MixedPartitionVersionError if this session has already bound
        to a different version of the same partition_id (one cited result
        NEVER mixes evidence versions per R-A5.4 verbatim).
        """
        with self._lock:
            existing = self._bound_partition_versions.get(partition.partition_id)
            if existing is not None and existing != partition.receipt_set_ref:
                raise MixedPartitionVersionError(
                    f"session {self.session_id} already bound to partition "
                    f"{partition.partition_id} version {existing}; refusing "
                    f"to bind to {partition.receipt_set_ref} (R-A5.4 · one "
                    f"cited result NEVER mixes evidence versions)"
                )
            self._bound_partition_versions[partition.partition_id] = partition.receipt_set_ref

    def add_entry(self, entry: WorkingSetEntry) -> None:
        """R-A5.4 · cache stores partition references + derived arithmetic ONLY.

        Entry is a WorkingSetEntry (frozen dataclass) that carries only a
        partition reference and a derived-arithmetic value; no raw estate
        material is materialized. Registry-vocabulary source-labeled values
        only per `PROM-S1-honesty-grammar-source-labels`.
        """
        with self._lock:
            existing_ref = self._bound_partition_versions.get(entry.partition_ref)
            if existing_ref is None:
                raise ValueError(
                    f"session {self.session_id} not bound to partition "
                    f"{entry.partition_ref}; call bind_partition first"
                )
            if existing_ref != entry.partition_version_receipt_set_ref:
                raise MixedPartitionVersionError(
                    f"session {self.session_id} entry references partition "
                    f"{entry.partition_ref} version "
                    f"{entry.partition_version_receipt_set_ref} but session "
                    f"is bound to version {existing_ref}"
                )
            self._entries.append(entry)

    def read_entries(self, partition_ref: str) -> List[WorkingSetEntry]:
        """R-A5.4 · cache reads inherit session's validated purpose.

        Callers accessing this method must be within a purpose-validated
        session context (validated at session-open · not bypassable through
        the working-set path).
        """
        with self._lock:
            return [e for e in self._entries if e.partition_ref == partition_ref]

    def invalidate_partition(self, partition_id: str) -> int:
        """R-A5.4 · promotion invalidates dependents.

        Called by partition-refresh module when a new version of `partition_id`
        is atomically promoted. Purges all working-set entries bound to the
        prior version. Returns the count of entries invalidated.
        """
        with self._lock:
            before = len(self._entries)
            self._entries = [e for e in self._entries if e.partition_ref != partition_id]
            self._bound_partition_versions.pop(partition_id, None)
            return before - len(self._entries)


# ---------------------------------------------------------------------------
# Test-only helper (not to be called from production code).
# ---------------------------------------------------------------------------


def _reset_for_tests() -> None:
    """Test-only helper. Not to be called from production code."""
    with _STORE._lock:
        _STORE.current.clear()
        _STORE.history.clear()
        _STORE.promotion_ledger.clear()
        _STORE._promotion_counter = 0
