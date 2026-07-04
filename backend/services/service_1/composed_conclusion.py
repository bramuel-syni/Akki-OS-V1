"""Composed-conclusion service — Phase 4b §6.2.

Spec authority: RMS Product & Engineering Spec v3 §6.2 (Composed
conclusion — full). Anchors cited inline.

**Condition B1 — class computed once, at Solva boundary.** This module
NEVER computes conclusion class locally via a floor reduction over
per-unit defensibility. It calls `services.solva_depth.assertion.conclusion_class(units)`
which owns that computation (frozen signature per §10). Grep-negative
enforced by `test_composed_conclusion_class_from_solva_boundary_only`
(gate 13, LOAD-BEARING).

**Condition B2 — grain refusal reuses 4a `grain_form_incompatible`.**
Grain incompatibility for §6.2 (per_claim, aggregated → refused;
synthesized_whole → accepted) is refused UPSTREAM at admission in
`services/service_1/dispatch.py` via the shared grain-compat matrix
(`services/service_1/grain_compatibility.py`). This module is only
reached when grain has already been validated as `synthesized_whole`.

**Condition B3 — outer-gate ride NOT taken.** §6.2's composed
conclusion is a SYNTHESIZED ANSWER, not an egress artifact of raw
Registry material. The conclusion carries a class + trace + load-
bearing set; no unit-level content leaves the system via this path.
Consequently, this module does NOT call `outer_gate.transform_artifact`
or `outer_gate.build_receipt` — those primitives govern egress of
raw-material bundles (per §6.1 qualified_data). The absence of an
outer-gate ride is explicit here, per Stage A ruling B3-clarification
at 4b dispatch.

**Read-only:** this module reads the Mtafiti Registry, then computes.
Persistence: writes ONE row to the Northena Ledger (append-only, per
§7.2 mandate) with `stage=converge / decision=terminate_success` and
`reason` carrying the load-bearing unit_ids for retrieval by trace_id
(v3 §6.2.3). That is the ONLY write on this path.

**Refusal path (Service1Refusal@v0 sibling family):**
  * `composition_below_floor` (v3 §6.2.6): conclusion_class < objective's
    minimum_class. `supported_class` = max over load-bearing units'
    Ring-5 classes (READ, not recomputed). `asked` = plain-language
    rendering of objective. `what_would_raise_it` = shared refusal-hint
    (A2 D2a static table).

**Note (Condition B1 discipline):** the "load-bearing units" passed to
`services.solva_depth.assertion.conclusion_class` are minimal
duck-typed proxies constructed from the Registry rows. They expose ONLY
`u.defensibility.defensibility_class` — the ONE attribute Solva's
signature reads. This is not a NormalizedUnit reconstruction (which
would trigger `extraction_params@v0` model validation); it is the
smallest object shape that satisfies Solva's read pattern. Solva
remains the ONLY site that computes the class.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Union

from contracts.composed_conclusion import ComposedConclusion_v0
from contracts.five_rings import DefensibilityClass
from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from contracts.objective_request_v2 import ObjectiveRequest_v2
from services.mtafiti.floor_feasibility import _CLASS_ORDER
from services.northena import ledger as northena_ledger

# B1 — the ONE conclusion-class computation site imported here.
from services.solva_depth.assertion import conclusion_class as _solva_conclusion_class

# Selection + filter reuse from 4a — Ruling 4 shared-derivation.
from services.service_1.license_class_selection import (
    derive_license_class_from_commissioner,
    select_by_class,
)
from services.service_1.qualified_data import (
    _read_reach_rows,
    _standard_hard_filter,
)
from services.service_1.admission_refusal import (
    emit_license_class_unavailable,
    emit_standard_below_admission_floor,
)
from services.service_1.refusal_hints import hint_for as _refusal_hint_for
from contracts.admission_refusal import AdmissionRefusal_v0


@dataclass(frozen=True)
class _DefensibilityView:
    """Minimal Solva-visible defensibility surface.

    Solva's `conclusion_class` reads only `.defensibility_class`.
    Nothing else — no score_vector, no matrix_rule_ref, no runtime_mode.
    This view exposes ONLY that one attribute, keeping the shape as
    small as the actual read pattern.
    """
    defensibility_class: DefensibilityClass


@dataclass(frozen=True)
class _UnitView:
    """Minimal Solva-visible unit surface — duck-type of NormalizedUnit.

    Solva's `conclusion_class(load_bearing_units)` iterates and reads
    `u.defensibility.defensibility_class` per unit. This view exposes
    exactly that path and nothing else. Registry rows carry
    `defensibility_class` at top level (MtafitiRegistryRecord shape);
    this view lifts it into the ring-nested position Solva expects.

    Not a `NormalizedUnit` — deliberately. Reconstructing a full
    NormalizedUnit from a Registry row would trigger
    `extraction_params@v0` model validation (Ring 4 requires modality-
    specific keys), which the Registry rows don't carry. This view is
    the honest minimal shape.
    """
    unit_id: str
    defensibility: _DefensibilityView


class Service1Refusal(Exception):
    """Composition refusal — mirrors `services/service_1/service.py::Service1Refusal`.

    Fields map 1:1 to the frozen `Service1Refusal@v0` Pydantic envelope
    (contracts/service_1_refusal.py). The router catches this exception
    and serialises the fields into a flat JSONResponse @422.

    Duplicated locally at the v2 dispatch surface to keep the v0
    service.py `run()` byte-identical (Condition B4 SHA-identity gate).
    Same six-field shape; same catch-and-serialise pattern in the
    router.
    """
    def __init__(
        self,
        reason: str,
        run_id: str,
        trace_id: str,
        *,
        asked: str,
        supported_class,
        what_would_raise_it: str,
    ):
        super().__init__(f"Service 1 refused: {reason}")
        self.reason = reason
        self.run_id = run_id
        self.trace_id = trace_id
        self.asked = asked
        self.supported_class = supported_class
        self.what_would_raise_it = what_would_raise_it


def _rows_to_unit_views(rows: List[Dict]) -> List[_UnitView]:
    """Convert Registry rows to Solva-visible unit views.

    Reads `row["defensibility_class"]` per row — the Ring-5-governed
    value stamped upstream by g1_defensibility. Never derives; only
    reads.

    Rows with an invalid/unrecognised defensibility_class value are
    SKIPPED silently — if any such row exists, upstream selection
    should have removed it; this is defense-in-depth.
    """
    out: List[_UnitView] = []
    for i, row in enumerate(rows):
        raw = row.get("defensibility_class", "")
        try:
            kls = DefensibilityClass(raw)
        except ValueError:
            continue
        unit_id = row.get("source_ref") or f"reg-unit-{i}"
        out.append(_UnitView(
            unit_id=f"cc-unit-{unit_id}",
            defensibility=_DefensibilityView(defensibility_class=kls),
        ))
    return out


def _plain_language_asked(request: ObjectiveRequest_v2) -> str:
    """Render the caller-facing 'asked' string for Service1Refusal.

    Mirrors RMS_Interface_Specification.md §201: 'objective + required
    floor, in plain terms'. Since v3's ObjectiveRequest_v2 does not
    carry a natural-language objective string yet (Phase 7 wizard adds
    that), we render structurally from the request shape.
    """
    floor = request.output.standard.minimum_class.value
    form = request.output.form.value
    return (
        f"Composed conclusion at minimum defensibility class "
        f"'{floor}', form '{form}', over reach "
        f"{list(request.reach.scope_refs)}."
    )


def _max_supported_class(unit_views: List[_UnitView]):
    """A2 D6a pattern — ceiling of Ring-5 classes over the input units.

    READ, not recomputed. Empty input → None (defense-in-depth; callers
    should not hit this because upstream selection filters guarantee
    non-empty on the below-floor path).
    """
    if not unit_views:
        return None
    return max(
        (v.defensibility.defensibility_class for v in unit_views),
        key=lambda k: _CLASS_ORDER[k],
    )


async def package_composed_conclusion(
    request: ObjectiveRequest_v2,
    trace_id: str,
) -> Union[ComposedConclusion_v0, AdmissionRefusal_v0, Service1Refusal]:
    """Phase 4b §6.2 entry point.

    Returns:
      * `ComposedConclusion_v0` on success (conclusion at/above floor).
      * `AdmissionRefusal_v0` on standard-hard-filter empty OR
        license-class-axis empty (shared 4a refusal reasons).
      * `Service1Refusal` (exception, raised) on
        `composition_below_floor` (§6.2.6).

    Grain-form incompatibility is refused UPSTREAM in
    `services.service_1.dispatch.dispatch()` — callers rely on grain
    being `synthesized_whole` here.
    """
    # 1. Reach filter — objective-blind Registry read.
    reach_rows = await _read_reach_rows(request)

    # 2. License-class axis filter — v3 §6.1.2 three-way selection.
    # NOTE ON §6.1.6 vs §6.2.6 (2026-07-04 dispatch reading): v3 §6.1.6
    # states 'standard = hard input filter' as a §6.1 QUALIFIED_DATA
    # rule; §6.2.6 states standard 'enforced at conclusion class' as a
    # §6.2 COMPOSED_CONCLUSION rule. These are DIFFERENT enforcement
    # points for the same `output.standard` field. In §6.2, we
    # therefore do NOT apply the input hard filter here — load-bearing
    # units below the floor DO enter the composition, and if the floor
    # over them (Solva's conclusion_class) falls below the requested
    # floor, the sibling Service1Refusal(composition_below_floor) fires
    # at conclusion-class time per §6.2.6.
    #
    # The `emit_standard_below_admission_floor` helper remains
    # registered defense-in-depth for callers that DO want the §6.1.6
    # semantic here (currently unused on the §6.2 path).
    derived_class = derive_license_class_from_commissioner(request.envelope)
    class_survivors = select_by_class(reach_rows, derived_class)
    if not class_survivors:
        return emit_license_class_unavailable(
            request, trace_id,
            derived_class=derived_class,
        )

    # 3. Convert survivors to Solva-visible unit views (Ring-5
    # class read only — no reconstruction of full NormalizedUnit).
    unit_views = _rows_to_unit_views(class_survivors)
    if not unit_views:
        # Every class_survivor had an invalid defensibility_class value —
        # a data-integrity oddity that should never happen post-license-
        # filter. Refuse as license_class_unavailable (closest semantic).
        return emit_license_class_unavailable(
            request, trace_id,
            derived_class=derived_class,
        )

    # 4. Compute conclusion class at the Solva boundary — B1.
    # This is the ONE authoritative computation site (grep-negative
    # enforced elsewhere; recomputation is a review-on-sight failure).
    computed_class = _solva_conclusion_class(unit_views)

    # 5. §6.2.6 — below-floor at conclusion class → Service1Refusal.
    minimum_class_value = request.output.standard.minimum_class.value
    requested_floor = DefensibilityClass(minimum_class_value)
    if _CLASS_ORDER[computed_class] < _CLASS_ORDER[requested_floor]:
        run_id = f"cc-run-{uuid.uuid4().hex[:12]}"
        reason = "composition_below_floor"
        raise Service1Refusal(
            reason=reason,
            run_id=run_id,
            trace_id=trace_id,
            asked=_plain_language_asked(request),
            supported_class=_max_supported_class(unit_views),
            what_would_raise_it=_refusal_hint_for(reason),
        )

    # 7. Success path — persist ONE Northena Ledger row for
    # trace_id → load_bearing correlation (v3 §6.2.3).
    load_bearing_unit_ids = [v.unit_id for v in unit_views]
    objective_ref = f"objreq-{trace_id}"
    run_id = f"cc-run-{uuid.uuid4().hex[:12]}"

    # Ledger's `reason` field carries the retrievable payload — same
    # pattern as service.py's `service_1_converged:units=N:plan=X`.
    # `stage=converge / decision=terminate_success` per the frozen
    # LedgerRow stage/decision enum table.
    ledger_reason = (
        f"composed_conclusion:class={computed_class.value}"
        f":load_bearing={','.join(load_bearing_unit_ids)}"
    )
    await northena_ledger.record(LedgerRow(
        run_id=run_id,
        trace_id=trace_id,
        stage="converge",
        decision="terminate_success",
        reason=ledger_reason,
        artifact_ref=LedgerArtifactRef(
            artifact_type="objective_request",
            artifact_id=objective_ref,
            version="v2",
        ),
        lawful_basis_ref=request.envelope.lawful_basis,
        stamp_audit=None,
        at=datetime.now(timezone.utc),
    ))

    # 8. Build the ComposedConclusion_v0 envelope — Solva-threaded class
    # UNCHANGED. Answer_text is a governance-honest scaffold stub for
    # Phase 4b (real synthesis is downstream; this phase lands the
    # frozen envelope + governance path, not the LLM composition).
    answer_text = (
        f"Composed conclusion over {len(load_bearing_unit_ids)} "
        f"load-bearing unit(s) at defensibility class "
        f"'{computed_class.value}'. Load-bearing set retrievable "
        f"via Northena Ledger by trace_id."
    )
    return ComposedConclusion_v0(
        conclusion_class=computed_class,
        answer_text=answer_text,
        trace_id=trace_id,
        load_bearing_unit_ids=load_bearing_unit_ids,
        objective_ref=objective_ref,
        computed_at=datetime.now(timezone.utc).isoformat(),
    )
