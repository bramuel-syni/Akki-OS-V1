"""Northena Admit — Stage 1 (mandate §4).

Deterministic-only. Compiles raw intent → frozen governing artifact;
invokes Solva admit-assist for judgement inputs (scope resolution,
preservation depth, defensibility floor); freezes the returned values.
Every path (accept + refuse) writes a Ledger row.

Cousin substrate (LIFT_AND_RESHAPE):

  * `services/synisense/shield/purpose_validator.py` — field-presence +
    completeness validation, structured refusal reasons. Discipline
    ported: refuse deterministically, name what was missing.

  * `services/g1_defensibility/solva_depth/integrity_validators.py`
    (which itself reshapes cousin `solva_v2/integrity_validators.py`
    per its module docstring L1-19). We lift the `ValidatorOffender` +
    `ValidationResult` shape one step further into Northena so admit's
    completeness checks return structured offenders rather than
    ad-hoc reason strings. Cousin note applies transitively: content
    (citation_lint, calibration, etc.) is session-shaped and does NOT
    port; the SHAPE (per-check function returning offenders,
    aggregator with `.ok`) is exactly the discipline admit needs.

Determinism boundary (§9 verbatim): scope resolution, preservation
depth, defensibility floor are Solva's; freezing them is Northena's.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.northena.ledger import record as ledger_record
from services.solva_depth.admit_assist import RegistryStub, get_assist


# Mandate §4 required fields on the raw intent for v0.
_REQUIRED_KEYS = ("artifact_type", "artifact_id", "artifact_version",
                  "lawful_basis", "scope")


# ---------------------------------------------------------------------------
# Structured-offender shape — LIFTED from
# `services/g1_defensibility/solva_depth/integrity_validators.py`
# (which itself lifts from cousin `solva_v2/integrity_validators.py`).
# ---------------------------------------------------------------------------
@dataclass
class AdmitOffender:
    """One deterministic completeness failure. Shape lifted from
    G1 reshape of integrity_validators.ValidatorOffender."""
    validator: str
    field_path: str
    explanation: str


@dataclass
class AdmitValidation:
    """Aggregator with `.ok`. Shape lifted (see G1 ValidationResult)."""
    offenders: List[AdmitOffender] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.offenders

    def refusal_reason(self) -> str:
        # Composite deterministic reason string suitable for LedgerRow.reason.
        return ";".join(f"{o.validator}:{o.field_path}={o.explanation}"
                        for o in self.offenders)


def _validate_completeness(raw_intent: Dict[str, Any]) -> AdmitValidation:
    v = AdmitValidation()
    missing = [k for k in _REQUIRED_KEYS if not raw_intent.get(k)]
    if missing:
        v.offenders.append(AdmitOffender(
            validator="required_fields", field_path=",".join(missing),
            explanation="missing_required_fields",
        ))
    if not str(raw_intent.get("lawful_basis", "")).strip():
        v.offenders.append(AdmitOffender(
            validator="lawful_basis", field_path="lawful_basis",
            explanation="missing_lawful_basis",
        ))
    return v


class FrozenArtifact:
    """Immutable dict wrapper — N-INV-4 immutability at run-time."""
    __slots__ = ("_data",)
    def __init__(self, data: Dict[str, Any]) -> None:
        object.__setattr__(self, "_data", dict(data))
    def __getitem__(self, k): return self._data[k]
    def __setitem__(self, k, v): raise TypeError("FrozenArtifact is immutable (§4/N-INV-4)")
    def __delitem__(self, k): raise TypeError("FrozenArtifact is immutable (§4/N-INV-4)")
    def get(self, k, d=None): return self._data.get(k, d)
    def keys(self): return self._data.keys()
    def to_dict(self) -> Dict[str, Any]: return dict(self._data)
    def artifact_ref(self) -> LedgerArtifactRef:
        return LedgerArtifactRef(
            artifact_type=self._data["artifact_type"],
            artifact_id=self._data["artifact_id"],
            version=self._data["artifact_version"],
        )


async def compile_and_freeze(
    raw_intent: Dict[str, Any], *, run_id: str, trace_id: str,
    registry: Optional[RegistryStub] = None,
) -> Dict[str, Any]:
    """Return `{decision, frozen_artifact?, ledger_row, reason}`."""
    registry = registry or RegistryStub()
    assist = get_assist()

    # Structured completeness (§4) — offender list, not booleans.
    val = _validate_completeness(raw_intent)
    if not val.ok:
        row = await _refuse(run_id, trace_id, raw_intent, reason=val.refusal_reason())
        return {"decision": "refused", "ledger_row": row,
                "reason": row.reason, "frozen_artifact": None}

    # Scope resolves via Solva assist (Northena freezes the returned value).
    resolved = assist.resolve_scope(list(raw_intent.get("scope") or []), registry)
    if not resolved:
        row = await _refuse(run_id, trace_id, raw_intent, reason="scope_unresolved")
        return {"decision": "refused", "ledger_row": row,
                "reason": row.reason, "frozen_artifact": None}

    # Defensibility floor + preservation depth (Solva judges; Northena freezes).
    floor = assist.defensibility_floor(raw_intent.get("defensibility_floor"))
    preservation = assist.preservation_depth(raw_intent.get("preservation_depth"))

    frozen = FrozenArtifact({
        **raw_intent,
        "scope": tuple(resolved),
        "defensibility_floor": floor,
        "preservation_depth": preservation,
    })
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id, stage="admit", decision="admitted",
        reason="admitted",
        artifact_ref=frozen.artifact_ref(),
        lawful_basis_ref=str(raw_intent["lawful_basis"]),
        stamp_audit=None, at=datetime.now(timezone.utc),
    )
    await ledger_record(row)
    return {"decision": "admitted", "frozen_artifact": frozen,
            "ledger_row": row, "reason": "admitted"}


async def _refuse(run_id: str, trace_id: str, raw_intent: Dict[str, Any],
                  *, reason: str) -> LedgerRow:
    # Refusals still need an artifact_ref shape (§7.2). Fall back to
    # objective_request/unresolved when the raw intent doesn't carry one.
    row = LedgerRow(
        run_id=run_id, trace_id=trace_id, stage="admit", decision="refused",
        reason=reason,
        artifact_ref=LedgerArtifactRef(
            artifact_type=raw_intent.get("artifact_type") or "objective_request",
            artifact_id=raw_intent.get("artifact_id") or "unresolved",
            version=raw_intent.get("artifact_version") or "unknown",
        ),
        lawful_basis_ref=str(raw_intent.get("lawful_basis") or ""),
        stamp_audit=None, at=datetime.now(timezone.utc),
    )
    await ledger_record(row)
    return row
