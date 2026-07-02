"""Solva trace — every extraction-time judgment auditable.

Source: `docs/mandates/RMS_Solva_Specification.md` §13.

`SolvaTrace` is a `@dataclass(frozen=True)` — Python-frozen, NOT a
Pydantic contract-grade schema-freeze. Distinction: it is code-frozen
but not schema-registered in the six frozen contracts (per Solva
reconciliation §10). Serializable to dict via `to_dict()` for
Northena Ledger `stamp_audit` absorption.

Cousin chain:
  `contracts.northena_ledger.LedgerRow.stamp_audit` — Optional[Dict]
    field that already accepts free-form audit blobs; the seam Solva
    absorbs into is already present at G2a.
  `services/g1_defensibility/ring5_stamper.py::StampAuditRingBuffer`
    — canonical audit blob writer pattern.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence, Union

from services.solva_depth.assertion import Assertion
from services.solva_depth.enforce import Refusal


@dataclass(frozen=True)
class StageRecord:
    """One reasoning-stage entry."""

    stage_name: str
    input_summary: str
    output_summary: str
    at: str  # ISO-8601 UTC


@dataclass(frozen=True)
class SolvaTrace:
    """Full extraction-time judgment trace."""

    trace_id: str
    run_id: str
    stages: Sequence[StageRecord]
    load_bearing_unit_ids: Sequence[str]
    computed_class: str  # DefensibilityClass value; str for JSON stability
    conclusion: Optional[Dict]  # Assertion.to_dict() or Refusal.to_dict()

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["stages"] = [asdict(s) for s in self.stages]
        d["load_bearing_unit_ids"] = list(self.load_bearing_unit_ids)
        return d


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def conclusion_to_dict(result: Union[Assertion, Refusal]) -> Dict:
    """Serialize an Assertion or Refusal into a JSON-safe dict."""
    if isinstance(result, Refusal):
        return {
            "kind": "refusal",
            "reason": result.reason,
            "computed_class": result.computed_class.value,
            "floor_class": result.floor_class.value,
        }
    return {
        "kind": "assertion",
        "klass": result.klass.value,
        "claim": result.claim,
        "context_only": result.context_only,
    }
