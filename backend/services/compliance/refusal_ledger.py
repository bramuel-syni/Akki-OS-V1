"""Canonical refusal-family ledger-emission helper — Sub-stage 1 (Seam 3).

E1.γ + E4 rulings (Owner, 2026-07-06):
  * Colocated in `services/compliance/` per E4 (one consumer at Sub-stage 1;
    no shared `_helpers/` extraction until second use).
  * Family value is a constrained-str backed by `refusal_families.v0.json`;
    NEVER a Literal, NEVER a frozen-contract field.
  * Row shape: `NorthenaLedgerRow_v1` byte-identical (parity 26 unchanged).
  * Family carried at pinned `stamp_audit["refusal_family"]` — LB gate
    `test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit`
    asserts presence + registry-validity on every refusal-terminal row.

Cross-reference to dead-stub migration note:
  * `services/service_1/async_state.py:238::emit_ledger_terminate_refused`
    is the pre-Sub-stage-1 stub (zero production callers). Body kept
    byte-identical (BC); migration docstring added. Canonical
    single-source is this module.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, FrozenSet, Optional

from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.northena.ledger import record as ledger_record


_REGISTRY_PATH = Path(__file__).resolve().parent / "refusal_families.v0.json"


def _load_valid_families() -> FrozenSet[str]:
    with _REGISTRY_PATH.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return frozenset(entry["family"] for entry in payload.get("valid_families", []))


# LOAD-BEARING deterministic set — loaded ONCE at import time from the
# on-disk versioned registry. Version bumps land as `refusal_families.vN.json`
# additions (append-only per E1.γ registry precedent).
VALID_REFUSAL_FAMILIES: FrozenSet[str] = _load_valid_families()


class UnknownRefusalFamilyError(ValueError):
    """Raised when the caller passes a family value not in `refusal_families.v0.json`.

    Enforcement point: the LB wire-shape gate at the aggregate/coverage read
    ALSO asserts registry-validity. This constructor-side check is
    defense-in-depth to fail loudly at emission time rather than silently
    write a row that the gate would then flag.
    """


async def emit_refusal_ledger_row(
    *,
    run_id: str,
    trace_id: str,
    family: str,
    reason: str,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: str,
    stage: str,
    at: Optional[datetime] = None,
    extra_stamp_audit: Optional[Dict] = None,
) -> LedgerRow:
    """Emit ONE refusal-terminal `NorthenaLedgerRow_v1` (byte-identical to
    v0 storage shape) carrying `stamp_audit["refusal_family"]` pinned per
    E1.γ ruling.

    Args:
      run_id, trace_id, reason, artifact_ref, lawful_basis_ref: standard
        ledger-row fields.
      family: constrained-str family value; MUST be in
        `refusal_families.v0.json::valid_families`. Raises
        `UnknownRefusalFamilyError` otherwise.
      stage: honest emission-stage per caller context. MUST be one of
        {"admit", "gate"} — the only two stages whose `_ALLOWED_V1` set
        admits `decision="refused"` (converge is refused a "refused"
        decision by the contract v1 validator; α trap rejected).
      at: emission timestamp; defaults to `datetime.now(timezone.utc)`.
      extra_stamp_audit: optional dict merged into the sidecar under
        keys other than `refusal_family` (e.g. `source: sync|async` for
        callers that want to note emission context).

    Returns:
      The `LedgerRow` written (post-`record`).

    Behaviour:
      * `stamp_audit["refusal_family"] = family` — pinned key per §7.1.γ.1.
      * `decision = "refused"` — allowed only under stage in {admit, gate}
        per `_ALLOWED_V1`.
      * Idempotency: NOT enforced here (mirror of `northena.ledger.record`
        which is a raw `insert_one` — append-only per §7.2 mandate). Callers
        that require idempotency add a pre-emission `_ledger_row_exists`
        check (see `services/economics/instrumentation.py:_ledger_row_exists`
        for the precedent shape).
    """
    if family not in VALID_REFUSAL_FAMILIES:
        raise UnknownRefusalFamilyError(
            f"family={family!r} not in refusal_families.v0.json "
            f"valid_families={sorted(VALID_REFUSAL_FAMILIES)}"
        )
    if stage not in ("admit", "gate"):
        raise ValueError(
            f"emit_refusal_ledger_row: stage={stage!r} not in {{'admit', 'gate'}} "
            f"— only stages whose _ALLOWED_V1 admits decision='refused'."
        )

    stamp_audit: Dict = {"refusal_family": family}
    if extra_stamp_audit:
        for key, value in extra_stamp_audit.items():
            if key == "refusal_family":
                # Pinned key wins; caller cannot override family via extra.
                continue
            stamp_audit[key] = value

    row = LedgerRow(
        run_id=run_id,
        trace_id=trace_id,
        stage=stage,  # type: ignore[arg-type]
        decision="refused",  # type: ignore[arg-type]
        reason=reason,
        artifact_ref=artifact_ref,
        lawful_basis_ref=lawful_basis_ref,
        stamp_audit=stamp_audit,
        at=at or datetime.now(timezone.utc),
    )
    await ledger_record(row)
    return row
