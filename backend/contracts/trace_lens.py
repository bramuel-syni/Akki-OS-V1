"""TraceLensEnvelope — frozen contract for `/api/northena/trace/{trace_id}` (§G5a).

New at G5a. Addition, not mutation. The eight existing frozen contracts
(six pre-G4 + MtafitiRegistryRecord@v0 + MiningPlan@v0) remain UNTOUCHED.

Realises Interface Spec §16 invariant #9 ("One record, seen at two scopes")
and Northena §12 (Ledger absorbs stamp-audit by unit_id + trace_id).

The envelope is engine-agnostic: it resolves whatever engines have records
under this `trace_id`. `engines_touched` reports the set.
"""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.mtafiti_registry import MtafitiRegistryRecord
from contracts.northena_ledger import LedgerRow
from contracts.targeta_plan import MiningPlan


class ResolvedSolvaTrace(BaseModel):
    """Solva trace resolved from a Northena Ledger stamp_audit blob.

    Mirrors `services/solva_depth/trace.py::SolvaTrace.to_dict()` shape.
    """
    model_config = ConfigDict(extra="allow")

    trace_id: Optional[str] = None
    stages: List[dict] = Field(default_factory=list)
    load_bearing_unit_ids: List[str] = Field(default_factory=list)
    computed_class: Optional[str] = None
    conclusion: Optional[dict] = None


class RegistryFreshnessMarker(BaseModel):
    """Whether the resolved Registry records match the plan's snapshot
    ref or have drifted since. `snapshot_pinned=False` at G5a because
    the Registry is a rolling store (planned enrichment post-G5a)."""
    model_config = ConfigDict(extra="forbid")

    snapshot_pinned: bool = Field(
        default=False,
        description="False at G5a — Registry is a rolling store; records "
                    "resolved are current-state.",
    )
    note: str = Field(
        default="G5a: Registry records resolved from current-state store; "
                "snapshot pinning is a post-G5a enrichment.",
    )


class TraceLensEnvelope(BaseModel):
    """Response envelope for `GET /api/northena/trace/{trace_id}`.

    engines_touched reports which engines had records under this trace_id.
    Empty arrays are correct answers when a particular engine did not
    participate — a Service 1 flow does not touch Solva at G4 shipping
    state; a Solva pipeline flow may not touch Targeta.
    """
    model_config = ConfigDict(extra="forbid")

    trace_id: str
    resolved_at: str = Field(..., description="ISO-8601 UTC of resolution moment.")
    run_ids: List[str] = Field(default_factory=list,
                               description="Unique run_ids observed for this trace_id (Northena §7.2).")
    engines_touched: List[str] = Field(
        default_factory=list,
        description="Set membership: {northena_ledger, solva, targeta, mtafiti, service_1}.",
    )
    ledger_rows: List[LedgerRow] = Field(default_factory=list)
    solva_traces: List[ResolvedSolvaTrace] = Field(default_factory=list)
    mining_plans: List[MiningPlan] = Field(default_factory=list)
    registry_records: List[MtafitiRegistryRecord] = Field(default_factory=list)
    registry_freshness: RegistryFreshnessMarker = Field(
        default_factory=RegistryFreshnessMarker,
    )
