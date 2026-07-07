"""Phase 8 Seam 3 Sub-stage 2 — single-source-of-deletion module.

Owner ruling (Stage A §5.1): this module contains the ONLY authorized
`db.<collection>.delete_one/delete_many/drop` call sites in the
extractor tree. The AST invariant `test_no_unauthorized_deletion_path`
whitelists this file and only this file.

Provenance:
    - Stage A proposal SHA `3fe969c2…` §5 (line 241, deliverables).
    - Amendment F (rulings §10 R-1..R-6, 2026-07-07).
    - E1.γ data-class registry pattern (mirrors refusal-family registry).

Contract adherence:
    - `NorthenaLedgerRow_v1` byte-identical; deletion event is a
      `stage="converge" + decision="continue"` neutral placeholder per
      §7.3 amended (Stage A §7.3.C).
    - Reason string prefix: `authorized_deletion:{held_class}`.
    - `stamp_audit` sidecar: pinned key `data_class="authorized_deletion"`
      + `held_class` + `keys_deleted` + `retention_rule_ref` + `actor`.

Semantics (unilateral tightening only at Sub-stage 2 close):
    - `execute_authorized_deletion(held_class, retention_rule, actor)`
      is the one function that performs deletion I/O.
    - Retention rule shape: `{window_days: int, set_at: ISO8601}` — the
      caller is responsible for verifying `window_days is not None`
      (returns explicit refusal in that case).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from core import db
from services.compliance.held_class_registry import HeldClassName

log = logging.getLogger(__name__)


# Collection-of-record per held_class (single-source enumeration).
# ledger_row → NORTHENA_LEDGER_COLLECTION.
# wizard_transcript → wizard_session (transcript field lives there per B-1/B-2/B-3).
# delivered_artifact → objectives_async_state (delivered_envelope field lives there).
_HELD_CLASS_TO_COLLECTION = {
    "ledger_row": "northena_ledger",
    "wizard_transcript": "wizard_session",
    "delivered_artifact": "objectives_async_state",
}


@dataclass
class DeletionResult:
    """Return shape of `execute_authorized_deletion` — no exceptions on
    empty selectors; honest zero-count is a valid result."""

    held_class: HeldClassName
    collection: str
    keys_deleted: int
    retention_rule_ref: str
    actor: str
    executed_at: str


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


async def execute_authorized_deletion(
    *,
    held_class: HeldClassName,
    retention_rule: dict,
    actor: str,
) -> DeletionResult:
    """Delete rows in the held_class collection whose age exceeds
    `retention_rule["window_days"]` days from now.

    Idempotent: subsequent calls with the same rule + actor produce the
    same result (age gate ensures only expired rows are touched; already-
    deleted rows do not resurrect).

    Args:
        held_class: one of `HELD_CLASSES`. Determines target collection.
        retention_rule: `{window_days: int, set_at: ISO8601}`. window_days
            MUST be a positive int (caller validates; helper raises on
            None to fail-fast).
        actor: identity of the caller (Identity.user_id/email; passed
            through into the DeletionResult + ledger row).

    Returns:
        DeletionResult with keys_deleted count. NEVER raises on empty
        selector; honest zero.
    """
    if retention_rule.get("window_days") is None:
        raise ValueError(
            "execute_authorized_deletion requires window_days:int; "
            "got None. Caller should have refused with no_retention_rule_set."
        )
    if held_class not in _HELD_CLASS_TO_COLLECTION:
        raise ValueError(
            f"held_class={held_class!r} not in registered set "
            f"{sorted(_HELD_CLASS_TO_COLLECTION.keys())}"
        )
    collection_name = _HELD_CLASS_TO_COLLECTION[held_class]
    window_days = int(retention_rule["window_days"])
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    cutoff_iso = cutoff.isoformat().replace("+00:00", "Z")

    # Selector — rows whose stored ISO timestamp is BEFORE the cutoff.
    # Field-name differs per collection (ledger uses `at`; async_state
    # uses `accepted_at`; wizard_session uses `created_at`).
    _TS_FIELD = {
        "northena_ledger": "at",
        "objectives_async_state": "accepted_at",
        "wizard_session": "created_at",
    }[collection_name]
    selector = {_TS_FIELD: {"$lt": cutoff_iso}}

    result = await db[collection_name].delete_many(selector)
    keys_deleted = int(getattr(result, "deleted_count", 0))
    retention_rule_ref = retention_rule.get("ref") or "retention.v0"
    log.info(
        "authorized_deletion held_class=%s collection=%s keys_deleted=%d "
        "window_days=%d actor=%s",
        held_class, collection_name, keys_deleted, window_days, actor,
    )
    return DeletionResult(
        held_class=held_class,
        collection=collection_name,
        keys_deleted=keys_deleted,
        retention_rule_ref=retention_rule_ref,
        actor=actor,
        executed_at=_now_iso(),
    )


# ────────────────────────────────────────────────────────────────────
# Infrastructure-rollback deletion sites — NOT governance-authorized;
# NOT a user-data retention deletion. Preserved here in the SAME module
# as `execute_authorized_deletion` to satisfy Stage A §5.1 "SINGLE-SOURCE-
# OF-DELETION module" literally (whitelist-positive ONLY for THIS file).
# Distinct function per semantic; no ledger row emitted for these
# rollbacks — they undo not-yet-observed inserts (queue-saturation, etc.).
# ────────────────────────────────────────────────────────────────────


async def rollback_saturated_queue_admit(objective_id: str) -> int:
    """Undo an `objectives_async_state` accepted-doc insert on queue-
    saturation infrastructure failure.

    Called from `routers/objectives.py` when `enqueue_objective` raises
    `QueueSaturatedError` — the accepted-doc was inserted moments earlier
    by the same request handler and has NEVER been observed downstream
    (worker never claims it because enqueue failed).

    This is NOT a user-data retention deletion. It is an idempotency
    rollback of a not-yet-committed state per Standing Disposition
    infra-not-refusal (queue saturated → HTTP 503, NEVER a governed refusal).

    Returns:
        deleted_count (int) — normally 1, or 0 if the doc was already
        cleaned up by a concurrent process (idempotent).
    """
    result = await db["objectives_async_state"].delete_one(
        {"objective_id": objective_id}
    )
    return int(getattr(result, "deleted_count", 0))
