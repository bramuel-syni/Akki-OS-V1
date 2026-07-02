"""Service 1 v1 — Day-Zero Estate Extraction (Product v2.1 §2.1).

Composition orchestrator:
  ObjectiveRequest / Portfolio Mandate
  → Mtafiti Registry (census + declaration + measure; V3 dark)
  → Targeta MiningPlan (core arm; yield dark)
  → Layer C convergence (existing G0.5 aggregator + G3 gate)
  → Northena Ledger correlation

Terminates at convergence. Does NOT invoke Solva (Solva is Service 2's
depth boundary at Objective-Extraction time).

Composition-time floor re-assertion (defense-in-depth) — mirrors Solva's
enforce boundary and Northena's admit boundary.
"""
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from contracts.five_rings import DefensibilityClass, NormalizedUnit
from contracts.mtafiti_registry import MtafitiRegistryRecord
from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from contracts.targeta_plan import MiningPlan
from core import db
from services.mtafiti import registry as mtafiti_registry
from services.northena import ledger as northena_ledger
from services.service_1 import refusal_hints
from services.targeta import core as targeta_core
from services.targeta import gate as targeta_gate
from services.targeta import plan as targeta_plan


# A2 D6a: Class ordering — mirrors solva_depth/assertion.py:36-40 CLASS_ORDER
# verbatim (mandate §10 semantics). Duplicated locally rather than imported
# to keep service_1 free of solva_depth dependencies (service.py docstring
# L10-11: "Does NOT invoke Solva"). Same discipline as
# targeta/core.py:15 which duplicates the same mapping.
_CLASS_ORDER = {
    DefensibilityClass.NON_FACTUAL: 0,
    DefensibilityClass.UTTERANCE: 1,
    DefensibilityClass.FACT: 2,
}


def _max_supported_class(
    normalized_units: List[NormalizedUnit],
) -> Optional[DefensibilityClass]:
    """A2 D6a + D7a: ceiling of Ring-5-governed classes over input units.

    Reads `u.defensibility.defensibility_class` per unit — the Ring 5
    governed value stamped upstream by g1_defensibility. Reduction via
    `max` under `_CLASS_ORDER`. NEVER recomputes the class from
    Rings 1-4 signals; that would violate the single-source doctrine.

    Returns None on empty input (edge case; callers should not hit
    this because the two pre-composition refusals fire on other
    conditions before reaching here).
    """
    if not normalized_units:
        return None
    return max(
        (u.defensibility.defensibility_class for u in normalized_units),
        key=lambda k: _CLASS_ORDER[k],
    )


class Service1Refusal(Exception):
    """Composition refusal — structured, at the composition boundary.

    Six fields map 1:1 to the frozen `Service1Refusal@v0` Pydantic
    envelope (contracts/service_1_refusal.py). The router catches this
    exception and serialises the fields into a flat JSONResponse.
    """

    def __init__(
        self,
        reason: str,
        run_id: str,
        trace_id: str,
        *,
        asked: str,
        supported_class: Optional[DefensibilityClass],
        what_would_raise_it: str,
    ):
        super().__init__(f"Service 1 refused: {reason}")
        self.reason = reason
        self.run_id = run_id
        self.trace_id = trace_id
        self.asked = asked
        self.supported_class = supported_class
        self.what_would_raise_it = what_would_raise_it


async def run(
    normalized_units: List[NormalizedUnit],
    *,
    objective_text: str,
    artifact_id: str,
    artifact_version: str,
    lawful_basis: str,
    floor: DefensibilityClass,
    scope_key: str = "portfolio",
    run_id: Optional[str] = None,
    trace_id: Optional[str] = None,
) -> dict:
    """Execute one Service 1 v1 run over the given normalized_units.

    G4 v0 shape: takes the governing artifact fields directly (mirrors
    Northena admit's `raw_intent` pattern). `floor` is the composition-
    time floor re-asserted at the boundary. `objective_text` is the
    plain-language objective for refusal-envelope `asked` rendering
    per RMS_Interface_Specification.md §201.

    Returns:
      { run_id, trace_id, mining_plan_id, registry_snapshot_ref,
        converged_unit_count, defensibility_floor, ledger_correlation_ref,
        yield_layer_version }
    """
    run_id = run_id or f"run-{uuid.uuid4().hex[:12]}"
    trace_id = trace_id or f"trace-{uuid.uuid4().hex[:12]}"

    # 1. Composition-time floor re-assertion (defense-in-depth).
    # A2 D6a: pre-composition refusals — supported_class is None
    # (no aggregate class has been computed yet).
    if floor is None:
        reason = "no_defensibility_floor"
        raise Service1Refusal(
            reason, run_id, trace_id,
            asked=objective_text,
            supported_class=None,
            what_would_raise_it=refusal_hints.hint_for(reason),
        )
    if not lawful_basis or not lawful_basis.strip():
        reason = "no_lawful_basis"
        raise Service1Refusal(
            reason, run_id, trace_id,
            asked=objective_text,
            supported_class=None,
            what_would_raise_it=refusal_hints.hint_for(reason),
        )

    artifact_ref = LedgerArtifactRef(
        artifact_type="portfolio_mandate",
        artifact_id=artifact_id,
        version=artifact_version,
    )

    # 2. Admit row.
    await northena_ledger.record(LedgerRow(
        run_id=run_id, trace_id=trace_id, stage="admit", decision="admitted",
        reason="service_1_run_admitted", artifact_ref=artifact_ref,
        lawful_basis_ref=lawful_basis, stamp_audit=None,
        at=datetime.now(timezone.utc),
    ))

    # 3. Mtafiti — census + declaration + measure (V3 dark).
    registry_records: List[MtafitiRegistryRecord] = []
    for unit in normalized_units:
        record = mtafiti_registry.compose_record(unit)  # v3_thresholds=None
        await mtafiti_registry.upsert(record)
        registry_records.append(record)
    # Registry snapshot ref: content-hash of the records at plan-build time.
    # Deterministic → reproducible plan_id when Registry state is unchanged
    # (Targeta §17 #8).
    import hashlib as _hashlib
    import json as _json
    _snap_payload = _json.dumps(
        [r.model_dump(mode="json") for r in registry_records],
        sort_keys=True,
    )
    registry_snapshot_ref = "snap-" + _hashlib.sha256(
        _snap_payload.encode("utf-8")
    ).hexdigest()[:16]

    # 4. Targeta — core arm; yield dark.
    registry_rows = [r.model_dump(mode="json") for r in registry_records]
    eligible = targeta_core.eligible_and_rank(
        registry_rows, floor, str(scope_key),
    )

    # A2 D1b + D8a: composition-below-floor refusal.
    # Trigger: Targeta filtered every candidate out because none met the
    # requested floor. The pile cannot compose a plan at this floor.
    # D6a: supported_class is the ceiling of Ring-5-governed classes on
    # the INPUT units (read, not recomputed).
    if not eligible:
        reason = "composition_below_floor"
        raise Service1Refusal(
            reason, run_id, trace_id,
            asked=objective_text,
            supported_class=_max_supported_class(normalized_units),
            what_would_raise_it=refusal_hints.hint_for(reason),
        )

    ordered, yield_layer_version = targeta_gate.compose_ordering(
        eligible, thresholds=None,   # closed seam
    )

    # 5. Assemble + persist MiningPlan.
    plan = targeta_plan.build_plan(
        ordered=ordered, core_baseline=eligible,
        floor=floor,
        mode="portfolio", governing_artifact_ref=artifact_ref,
        registry_snapshot_ref=registry_snapshot_ref,
        yield_layer_version=yield_layer_version,
    )
    await targeta_plan.persist(plan)

    # 6. Gate row (Targeta plan accepted).
    await northena_ledger.record(LedgerRow(
        run_id=run_id, trace_id=trace_id, stage="gate", decision="warm",
        reason=f"targeta_plan_built:{plan.plan_id}", artifact_ref=artifact_ref,
        lawful_basis_ref=lawful_basis, stamp_audit=None,
        at=datetime.now(timezone.utc),
    ))

    # 7. Converge terminate row (Service 1 terminates at convergence).
    converged_unit_count = len(registry_records)
    await northena_ledger.record(LedgerRow(
        run_id=run_id, trace_id=trace_id, stage="converge",
        decision="terminate_success",
        reason=(f"service_1_converged:units={converged_unit_count}"
                f":plan={plan.plan_id}"),
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis,
        stamp_audit=None,
        at=datetime.now(timezone.utc),
    ))

    return {
        "run_id": run_id,
        "trace_id": trace_id,
        "mining_plan_id": plan.plan_id,
        "registry_snapshot_ref": registry_snapshot_ref,
        "converged_unit_count": converged_unit_count,
        "defensibility_floor": floor.value,
        "ledger_correlation_ref": run_id,
        "yield_layer_version": yield_layer_version,
    }


async def status_by_run(run_id: str) -> dict:
    """Read run status from Northena Ledger correlation.

    Returns { run_id, stage, mining_plan_id, registry_snapshot_ref,
    converged_unit_count, defensibility_class }. Empty rows → 'unknown'.
    """
    from contracts.northena_ledger import NORTHENA_LEDGER_COLLECTION
    rows_cursor = (
        db[NORTHENA_LEDGER_COLLECTION]
        .find({"run_id": run_id}, {"_id": 0})
        .sort("at", 1)
    )
    rows = [r async for r in rows_cursor]
    if not rows:
        return {"run_id": run_id, "stage": "unknown"}
    last = rows[-1]
    # Extract plan id from the gate row's reason
    mining_plan_id = None
    converged_unit_count = 0
    for r in rows:
        reason = str(r.get("reason", ""))
        if reason.startswith("targeta_plan_built:"):
            mining_plan_id = reason.split(":", 1)[1]
        if reason.startswith("service_1_converged:"):
            parts = reason.split(":")
            for p in parts:
                if p.startswith("units="):
                    try:
                        converged_unit_count = int(p.split("=", 1)[1])
                    except ValueError:
                        pass
    return {
        "run_id": run_id,
        "stage": last["stage"],
        "decision": last["decision"],
        "mining_plan_id": mining_plan_id,
        "converged_unit_count": converged_unit_count,
        "ledger_row_count": len(rows),
    }
