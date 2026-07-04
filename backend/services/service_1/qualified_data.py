"""Qualified-data selection + packaging service — Phase 4a §6.1.

Spec authority: RMS Product & Engineering Spec v3 §6.1 (Qualified data —
per-claim units carrying class, contested, provenance, trace).

**§6.1.2 three-way selection (INTERSECTION):** reach + standard filter
+ license class → packaging → outer-gate export.

Read-only: this module reads the Mtafiti Registry (via
`MTAFITI_REGISTRY_COLLECTION`) but writes ZERO rows to any persistent
store. The outer-gate ride is IN-MEMORY only (transform_artifact +
build_receipt); the receipt is returned inline in the response but not
persisted here (Phase 5's async delivery envelope persistence lands in
Phase 5, not 4a).

**Condition B3 preserved (outer-gate extended, not reinvented):** the
export path calls `services.outer_gate.transform.transform_artifact`
and `services.outer_gate.receipt.build_receipt` UNCHANGED. Zero touches
to `services/outer_gate/*.py` (SHA-invariant by
`test_qualified_data_outer_gate_ride_receipt_unchanged` +
`test_v0_paths_byte_identical_after_4a`).

**Section 7 verdict — UNFROZEN plain payload (Candidate 2).** The
`QualifiedDataPayload` container is a Pydantic model with
`extra="forbid"` but WITHOUT `frozen=True` and WITHOUT a
`.contract_snapshot.json`. Governance rides on inner shapes
(`NormalizedUnit` + `OuterGateReceipt_v0`, both already frozen).
Ruling 3 (Owner acceptance 2026-07-03) — pinned by LOAD-BEARING
`test_qualified_data_wire_shape_pins_governance_keys` which asserts:
top-level `units`/`receipt`/`unit_count` present; `receipt` parses as
`OuterGateReceipt_v0.model_validate(...)`; every unit carries its
`defensibility` field.

**Refusal paths (three, all via AdmissionRefusal@v0 registry v1
extension):**
  1. Standard hard input filter empties reach → `emit_standard_below_admission_floor`.
  2. License-class axis empties reach → `emit_license_class_unavailable`.
  3. (Grain-form incompatibility is refused UPSTREAM in dispatch before
     this module is called; kept here as documentation, not enforcement.)
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Union

from pydantic import BaseModel, ConfigDict, Field

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION
from contracts.northena_ledger import LedgerArtifactRef
from contracts.objective_request_v2 import ObjectiveRequest_v2
from contracts.outer_gate_receipt import OuterGateReceipt
from core import db
from services.mtafiti.floor_feasibility import _CLASS_ORDER
from services.outer_gate.mint import MintRegistry
from services.outer_gate.receipt import build_receipt
from services.outer_gate.transform import transform_artifact
from services.service_1.admission_refusal import (
    emit_license_class_unavailable,
    emit_standard_below_admission_floor,
)
from services.service_1.license_class_selection import (
    derive_license_class_from_commissioner,
    select_by_class,
)


class QualifiedDataPayload(BaseModel):
    """Section 7 Candidate 2 UNFROZEN payload — plain wire shape.

    NOT snapshotted. NOT in `test_frozen_contract_snapshot_parity.py`
    map. Governance rides on inner frozen shapes.
    """

    model_config = ConfigDict(extra="forbid")

    units: List[Dict[str, Any]] = Field(
        ...,
        description=(
            "Egress-transformed NormalizedUnit dicts. Each unit's "
            "`defensibility` field is intact (Ruling 3 wire-shape "
            "gate). Identifier fields (unit_id, source_ref, "
            "speaker_or_author) pseudonymised via outer-gate; "
            "feed_id + structural_signature generalised."
        ),
    )
    receipt: OuterGateReceipt = Field(
        ...,
        description=(
            "Governed outer-gate irreversibility receipt (frozen "
            "contract from G6). Ruling 3 wire-shape gate asserts "
            "OuterGateReceipt_v0.model_validate parses this field."
        ),
    )
    unit_count: int = Field(
        ..., ge=1,
        description="Number of units after three-way selection filter.",
    )
    computed_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC. When packaging completed.",
    )


def _standard_hard_filter(
    registry_rows: List[Dict],
    minimum_class_value: str,
) -> List[Dict]:
    """v3 §6.1.6 — standard = hard input filter.

    Removes rows whose `defensibility_class` falls BELOW
    `minimum_class_value` per `_CLASS_ORDER` ordinal.

    NON_FACTUAL(0) < UTTERANCE(1) < FACT(2). Row survives iff its
    class ordinal >= requested standard's ordinal.
    """
    from contracts.five_rings import DefensibilityClass
    threshold = _CLASS_ORDER[DefensibilityClass(minimum_class_value)]
    survivors: List[Dict] = []
    for row in registry_rows:
        row_class = row.get("defensibility_class", "")
        try:
            row_ordinal = _CLASS_ORDER[DefensibilityClass(row_class)]
        except (ValueError, KeyError):
            continue
        if row_ordinal >= threshold:
            survivors.append(row)
    return survivors


async def _read_reach_rows(request: ObjectiveRequest_v2) -> List[Dict]:
    """Objective-blind reach match — mirrors
    `services/mtafiti/feasibility.py::_row_matches_reach`.

    Read-only cursor; zero writes. Projection matches feasibility's
    minimal read shape plus the fields needed for downstream packaging.
    """
    scope_set = set(request.reach.scope_refs)
    exclusion_set = set(request.reach.exclusions)
    cursor = db[MTAFITI_REGISTRY_COLLECTION].find({}, {"_id": 0})
    matched: List[Dict] = []
    async for row in cursor:
        region = row.get("region", "")
        if region in exclusion_set:
            continue
        if region in scope_set:
            matched.append(row)
    return matched


def _row_to_pre_egress(row: Dict, trace_id: str, run_id: str) -> Dict[str, Any]:
    """Convert a Registry row into a per-unit pre-egress artifact for
    the outer-gate transform.

    Fields include identifiers (source_ref, feed_id, run_id, trace_id)
    that the outer-gate transform will pseudonymise or generalise, PLUS
    the `defensibility` sub-dict (untouched by transform — governance
    payload). `unit_id` synthesized from source_ref for pseudonymisation
    surface parity with G6 outer-gate tests.
    """
    return {
        "unit_id": f"reg-unit-{row.get('source_ref', '')}",
        "source_ref": row.get("source_ref", ""),
        "feed_id": row.get("feed_id", ""),
        "region": row.get("region", ""),
        "sensitivity": row.get("sensitivity", ""),
        "run_id": run_id,
        "trace_id": trace_id,
        "defensibility": {
            "defensibility_class": row.get("defensibility_class", ""),
            "defensibility_measure": row.get("defensibility_measure", {}),
            "matrix_rule_ref": row.get("matrix_rule_ref", ""),
            "runtime_mode": row.get("defensibility_runtime_mode", "declaration_baseline"),
        },
        "freshness_stamp": row.get("freshness_stamp", {}),
    }


async def package_qualified_data(
    request: ObjectiveRequest_v2,
    trace_id: str,
) -> Union[QualifiedDataPayload, AdmissionRefusal_v0]:
    """Phase 4a §6.1 selection + packaging entry point.

    Returns:
      * `QualifiedDataPayload` on success (three-way selection non-empty).
      * `AdmissionRefusal_v0` on standard-hard-filter empty OR
        license-class-axis empty.

    Grain-form incompatibility is refused UPSTREAM in
    `services.service_1.dispatch.dispatch()` before this function is
    called; callers can rely on
    `evaluate_grain_form(request.output.form, request.output.grain).compatible`
    being True here.

    Ride discipline (Condition B3): outer-gate transform + receipt run
    UNCHANGED; MintWindow opened per-call (in-memory, purge irrelevant
    at 4a's read-only surface — window key never persisted).
    """
    # 1. Reach filter — objective-blind Registry read.
    reach_rows = await _read_reach_rows(request)

    # 2. Standard hard input filter — v3 §6.1.6.
    minimum_class_value = request.output.standard.minimum_class.value
    standard_survivors = _standard_hard_filter(reach_rows, minimum_class_value)
    if not standard_survivors:
        return emit_standard_below_admission_floor(
            request,
            trace_id,
            qualifying_volume_after_filter=0,
        )

    # 3. License-class axis filter — v3 §6.1.2 three-way selection.
    derived_class = derive_license_class_from_commissioner(request.envelope)
    class_survivors = select_by_class(standard_survivors, derived_class)
    if not class_survivors:
        return emit_license_class_unavailable(
            request,
            trace_id,
            derived_class=derived_class,
        )

    # 4. Outer-gate ride (Condition B3 — extended, not reinvented).
    run_id = f"qd-run-{uuid.uuid4().hex[:12]}"
    mint = MintRegistry()
    window = mint.open_window(
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    egressed_units: List[Dict[str, Any]] = []
    last_egress_artifact: Dict[str, Any] = {}
    for row in class_survivors:
        pre_egress = _row_to_pre_egress(row, trace_id=trace_id, run_id=run_id)
        egress = transform_artifact(pre_egress, window)
        last_egress_artifact = egress
        # Strip transform metadata from the per-unit dict — the receipt
        # captures it at batch level.
        clean_unit = {k: v for k, v in egress.items() if k != "_transform_meta"}
        egressed_units.append(clean_unit)

    # 5. Receipt build (Condition B3 — existing frozen contract).
    artifact_ref = LedgerArtifactRef(
        artifact_type="objective_request",
        artifact_id=f"objreq-{trace_id}",
        version="v2",
    )
    receipt = build_receipt(
        last_egress_artifact,
        run_id=run_id,
        trace_id=trace_id,
        artifact_ref=artifact_ref,
    )

    return QualifiedDataPayload(
        units=egressed_units,
        receipt=receipt,
        unit_count=len(egressed_units),
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
