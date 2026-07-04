"""Shape-responsive execution dispatch — Phase 2 scaffold.

Spec authority: RMS Product & Engineering Spec v3 §4 (Shape-responsive
execution — NEW build item).

**Scaffold, not execution.** This module DECIDES routing per v3 §4 four
bullets — reach-sizing plumbing, warm/fresh fork at admission,
structured-intake entry-point branch, output-form routing — and returns
a `DispatchResult` for a caller (the v2 route) to act on. It does NOT
execute the downstream receiver; downstream receivers (Phase 3 refusal
envelope, Phase 4 transform variants, Phase 5 async delivery) are
un-built at Phase 2 dispatch time. Every dispatch response therefore
carries a governed `placeholder_body` naming the phase-debt receiver.

**Standing owner rulings honoured here:**

  * **Gate 1 (Unknown freshness → FRESH, never warm)** — v3 §5 honesty
    binds the fork decision: UNKNOWN freshness forks FRESH. Warmth is
    an assertion of qualified availability; asserting it from an
    un-censused reach fabricates. Enforced by
    `tests/invariants/test_dispatch_shape_responsive.py`.

  * **Gate 2 (single-consumer feasibility + shared floor-feasibility)** —
    Ruling 4 (Phase 1 close). This module imports
    `compute_feasibility` from `services/mtafiti/feasibility.py` and
    `derive_floor_feasibility` from
    `services/mtafiti/floor_feasibility.py`. Reimplementation fails
    review regardless of output equality.

  * **Gate 3 (v0 untouched)** — no modification to
    `contracts/objective_request.py` or `services/service_1/service.py`.
    The work_order route_target NAMES the v0 path but this module does
    NOT invoke `service_1.service.run` (units aren't in the v2
    envelope; Phase 4 supplies them via the transform layer). The
    existing v0 route (`POST /api/service_1/run`) remains
    byte-identical.

  * **Gate 4 (loose-typed depth passthrough)** — `Reach.depth` is `str`
    per Phase 0 loose-as-frozen ruling. This module reads `depth`
    as-is and threads it forward through the trace but NEVER branches
    on its value. Enforced by grep-negative on
    `if depth ==`, `match depth`, `Depth.` in
    `test_dispatch_never_branches_on_depth_enum`.

**Response envelope (unfrozen at Phase 2, per Ruling 3 pattern — mechanism,
not values):** `DispatchResult` is a Pydantic model with fields
`fork_decision`, `route_target`, `feasibility_result`,
`floor_feasibility`, `placeholder_body`, `trace_id`. Not snapshotted; if
owner later rules this shape needs freezing, that lands as an additive
frozen contract at that phase's dispatch. Rationale: dispatch outcome
shape is internal-orchestration, not governance-critical the way
`FeasibilityResult_v0` is (which feeds a frozen envelope's field).

**Deferred bullets (Phase 2 does NOT cover):**
  * Transform variants proper (§6.1 qualified_data selection+packaging,
    §6.2 Solva composition) → Phase 4.
  * Async delivery envelope (§7) → Phase 5.
  * `model` form refusal (§6.5 off-menu refusal envelope) → Phase 3.
  * Wizard-side dispatch grounding (§3.3) → Phase 7.
  * Admission-time hard-input-filter `AdmissionRefusal@v0` for §6.1
    standard (Phase 1 §6.1 extension-surface item 3) → Phase 4.

Placeholder rendering separation: `placeholder_body["outcome"] ==
"not_yet_implemented"` is scaffold engineering, NOT a product outcome.
Distinct from `Service1Refusal@v0` (outcome=refused, composition-boundary
governed refusal). Enforced by
`test_dispatch_placeholder_never_leaks_into_governed_refusal`.
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from contracts.admission_refusal import AdmissionRefusal_v0
from contracts.feasibility_result import FeasibilityResult_v0, Freshness
from contracts.objective_request_v2 import (
    ObjectiveEntry,
    ObjectiveRequest_v2,
    OutputForm,
)

# Gate 2 imports — shared feasibility + shared floor-feasibility.
# Static-inspection-checked by
# `test_dispatch_uses_shared_feasibility_and_floor_feasibility`.
from services.mtafiti.feasibility import compute_feasibility
from services.mtafiti.floor_feasibility import derive_floor_feasibility

# Phase 3 admission-refusal emission — replaces the scaffold placeholder
# for `output.form == "model"` (Condition 5 migration).
from services.service_1.admission_refusal import (
    emit_form_not_offerable,
    emit_grain_form_incompatible,
)

# Phase 4a — grain-compat single-source-of-truth + §6.1 qualified-data
# packaging path.
from services.service_1.grain_compatibility import evaluate_grain_form
from services.service_1.qualified_data import (
    QualifiedDataPayload,
    package_qualified_data,
)

# Phase 4b — §6.2 composed-conclusion packaging path (18th frozen
# contract landing).
from contracts.composed_conclusion import ComposedConclusion_v0
from services.service_1.composed_conclusion import (
    Service1Refusal as ComposedConclusionRefusal,
    package_composed_conclusion,
)


# Route-target constants — named string constants surfaced in responses.
# Naming discipline: `{receiver_phase}_{receiver_name}` where the
# receiver is described in terms of the phase that will build/wire it.
ROUTE_SERVICE_1_V0_VIA_ADAPTER = "service_1_v0_via_adapter"
ROUTE_ADMISSION_WARM_FORK = "admission_warm_fork_via_northena_admit"
ROUTE_ADMISSION_FRESH_FORK = "admission_fresh_fork_via_northena_admit"
ROUTE_PHASE_3_MODEL_REFUSAL = "phase_3_model_refusal_envelope"
ROUTE_PHASE_4_KNOWLEDGE_ARTIFACT = "phase_4_transform_variant_knowledge_artifact"
ROUTE_PHASE_4_CALLABLE_SKILL = "phase_4_transform_variant_callable_skill"

# Phase-debt names — surfaced in placeholder_body["phase_debt"] for
# operator observability. Match §0.2 Plan Debts entries in
# ORCHESTRATOR_CONTINUITY.md.
DEBT_PHASE_3 = "phase_3_model_refusal_envelope"
DEBT_PHASE_4 = "phase_4_transform_variants"
DEBT_PHASE_5 = "phase_5_async_delivery"

# Placeholder outcome discriminator — distinct from Service1Refusal
# `outcome=refused`. Rendering separation enforced by
# `test_dispatch_placeholder_never_leaks_into_governed_refusal`.
PLACEHOLDER_OUTCOME = "not_yet_implemented"
PLACEHOLDER_REASON = "phase_2_scaffold_downstream_deferred"


class DispatchResult(BaseModel):
    """Phase-2-scaffold dispatch outcome envelope.

    UNFROZEN at Phase 2 (per Ruling 3 pattern — mechanism, not values).
    If owner later rules this shape needs freezing, that lands as an
    additive frozen contract at the freezing phase's dispatch.
    """

    model_config = ConfigDict(extra="forbid")

    fork_decision: Optional[str] = Field(
        default=None,
        description=(
            "'warm' | 'fresh' when entry=='external_request' and "
            "output.form in (qualified_data, composed_conclusion). "
            "None for work_order entry (wizard grounds per-turn; no "
            "admission-time fork) and for output-form-refusal paths."
        ),
    )
    route_target: str = Field(
        ...,
        description=(
            "Named target of the dispatch decision. See "
            "ROUTE_* constants for the vocabulary."
        ),
    )
    feasibility_result: Optional[FeasibilityResult_v0] = Field(
        default=None,
        description=(
            "The v3 §5 Estate Feasibility Query response consumed by "
            "the admission warm/fresh fork. None for work_order entry "
            "and for output-form-refusal paths."
        ),
    )
    floor_feasibility: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "The shared `derive_floor_feasibility` output when a "
            "distribution was available (FRESH/STALE freshness). None "
            "when freshness==UNKNOWN or when the code path does not "
            "compute feasibility (work_order, output-form-refusal)."
        ),
    )
    placeholder_body: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "Governed scaffold placeholder — set on EVERY Phase 2 "
            "dispatch response because no downstream receiver is built "
            "yet. Distinct from Service1Refusal (rendering separation "
            "enforced by test_dispatch_placeholder_never_leaks_into_"
            "governed_refusal)."
        ),
    )
    trace_id: str = Field(
        ...,
        description="Dispatch-generated trace id. Correlation only.",
    )


def _make_placeholder(route: str, phase_debt: str, trace_id: str) -> Dict[str, Any]:
    """Build the governed scaffold placeholder body.

    Fields per owner scope declaration:
      * outcome      — discriminator 'not_yet_implemented' (distinct
                        from Service1Refusal 'refused').
      * reason       — 'phase_2_scaffold_downstream_deferred'.
      * route        — the route the dispatch would have taken.
      * phase_debt   — the phase that will implement this receiver.
      * trace_id     — dispatch-generated correlation id.
    """
    return {
        "outcome": PLACEHOLDER_OUTCOME,
        "reason": PLACEHOLDER_REASON,
        "route": route,
        "phase_debt": phase_debt,
        "trace_id": trace_id,
    }


async def dispatch(
    request: ObjectiveRequest_v2,
) -> Union[
    DispatchResult, AdmissionRefusal_v0, QualifiedDataPayload,
    ComposedConclusion_v0,
]:
    """Shape-responsive dispatch — the single Phase 2/3/4a/4b entrypoint.

    Reads `entry`, `reach`, `output.form`, `output.grain`,
    `output.standard`. Calls `compute_feasibility` and
    `derive_floor_feasibility` from the shared services when the
    admission warm/fresh fork applies. Fires grain-compat admission
    refusal (Phase 4a) UPSTREAM of the fork. Fires §6.1 qualified-data
    packaging (Phase 4a) on WARM + `output.form==qualified_data`.

    Return type union — three arms:
      * `DispatchResult` for the six placeholder-emitting code paths.
      * `AdmissionRefusal_v0` for `form_not_offerable` (§6.5),
        `grain_form_incompatible` (§6.1.4/§6.2.4/etc), or the two
        §6.1 packaging-time refusals (`standard_below_admission_floor`,
        `license_class_unavailable`) surfaced through
        `package_qualified_data`.
      * `QualifiedDataPayload` for §6.1 warm success (Section 7
        Candidate 2 UNFROZEN plain payload).

    The v2 route branches on isinstance and returns different HTTP
    statuses (200 for qualified-data success, 422 for governed refusal,
    501 for scaffold placeholder).

    Does NOT invoke `services.service_1.service.run`. Does NOT write to
    any Mongo collection (`compute_feasibility` and the qualified-data
    packaging path are both read-only per
    `test_feasibility_readonly.py` + Condition B3).
    """
    trace_id = f"disp-{uuid.uuid4().hex[:12]}"

    # ------------------------------------------------------------------
    # Output-form routing — check refusal / deferred variants FIRST.
    # These bypass the admission fork because there is no receiver to
    # dispatch to at Phase 2/3 regardless of feasibility.
    # ------------------------------------------------------------------
    form = request.output.form
    if form == OutputForm.MODEL:
        # v3 §6.5: off the offerable menu. Phase 3 lands the governed
        # AdmissionRefusal@v0 envelope (17th frozen contract) — the
        # scaffold 501 placeholder is REPLACED here per Condition 5.
        # Fires at BOTH entry points (Condition 4): external_request
        # emits it directly at admission; work_order will render it via
        # the wizard (Phase 7 receiver, not yet built).
        return emit_form_not_offerable(request, trace_id)

    # Phase 4a — grain-compat admission-time refusal (§6.1.4 + §6.2.4
    # + §6.3.4 + §6.4.4). Fires UPSTREAM of the form-specific branches
    # so a mismatched (form, grain) pair never enters the deferred /
    # warm packaging code paths. Grain-compat is the single-source-of
    # truth per Ruling 4 (single derivation site, shared with Phase 7
    # wizard). MODEL cells above already refused; this checks the
    # remaining four forms.
    grain_result = evaluate_grain_form(form, request.output.grain)
    if not grain_result.compatible:
        # Under normal control flow, MODEL cells are unreachable here
        # (already returned above). This branch fires for the four
        # non-MODEL forms whose (form, grain) pair is incompatible.
        # `grain_result.refusal_reason` is `grain_form_incompatible`
        # for non-MODEL cells per Ruling 7 unification.
        assert grain_result.path_forward is not None
        return emit_grain_form_incompatible(
            request,
            trace_id,
            path_forward=grain_result.path_forward,
        )

    if form == OutputForm.KNOWLEDGE_ARTIFACT:
        return DispatchResult(
            fork_decision=None,
            route_target=ROUTE_PHASE_4_KNOWLEDGE_ARTIFACT,
            feasibility_result=None,
            floor_feasibility=None,
            placeholder_body=_make_placeholder(
                route=ROUTE_PHASE_4_KNOWLEDGE_ARTIFACT,
                phase_debt=DEBT_PHASE_4,
                trace_id=trace_id,
            ),
            trace_id=trace_id,
        )
    if form == OutputForm.CALLABLE_SKILL:
        return DispatchResult(
            fork_decision=None,
            route_target=ROUTE_PHASE_4_CALLABLE_SKILL,
            feasibility_result=None,
            floor_feasibility=None,
            placeholder_body=_make_placeholder(
                route=ROUTE_PHASE_4_CALLABLE_SKILL,
                phase_debt=DEBT_PHASE_4,
                trace_id=trace_id,
            ),
            trace_id=trace_id,
        )

    # ------------------------------------------------------------------
    # form is QUALIFIED_DATA or COMPOSED_CONCLUSION at this point.
    # QUALIFIED_DATA live-path lands at 4a (this phase);
    # COMPOSED_CONCLUSION live-path lands at 4b (next phase).
    # ------------------------------------------------------------------

    # Entry-point branch — work_order vs external_request.
    if request.entry == ObjectiveEntry.WORK_ORDER:
        # v3 §3.3: the wizard grounds feasibility per-turn (guard 3);
        # by the time a work_order lands here it is already grounded.
        # Phase 2 declares the v0 route target without invoking service_1
        # (Gate 3: no modification to service.py; units aren't in v2).
        return DispatchResult(
            fork_decision=None,
            route_target=ROUTE_SERVICE_1_V0_VIA_ADAPTER,
            feasibility_result=None,
            floor_feasibility=None,
            placeholder_body=_make_placeholder(
                route=ROUTE_SERVICE_1_V0_VIA_ADAPTER,
                phase_debt=DEBT_PHASE_4,
                trace_id=trace_id,
            ),
            trace_id=trace_id,
        )

    # entry == EXTERNAL_REQUEST — admission-time warm/fresh fork.
    feasibility = await compute_feasibility(request.reach)

    # Gate 1: UNKNOWN freshness → FRESH path, never warm.
    if feasibility.freshness == Freshness.UNKNOWN:
        fork = "fresh"
        floor_result: Optional[Dict[str, Any]] = None
    else:
        # class_distribution is non-None for FRESH/STALE per
        # FeasibilityResult_v0 honesty contract.
        assert feasibility.class_distribution is not None
        floor_result = derive_floor_feasibility(
            feasibility.class_distribution,
            request.output.standard,
        )
        # Warm gate: freshness in (FRESH, STALE) AND feasible AND
        # qualifying_volume >= 1. STALE qualifies as "qualified
        # intelligence" per §5 ("staleness is not un-known"). The
        # qualifying_volume >= 1 clause is defensive under the
        # non-UNKNOWN branch (implicit but explicit for clarity).
        qualifying_volume = feasibility.qualifying_volume or 0
        if floor_result["feasible"] and qualifying_volume >= 1:
            fork = "warm"
        else:
            fork = "fresh"

    # Phase 4a §6.1 live-path: WARM + qualified_data → package and
    # return QualifiedDataPayload (or AdmissionRefusal_v0 for the two
    # packaging-time refusal cases). Otherwise fall through to
    # placeholder emission.
    if fork == "warm" and form == OutputForm.QUALIFIED_DATA:
        return await package_qualified_data(request, trace_id)

    # Phase 4b §6.2 live-path: WARM + composed_conclusion → package
    # via Solva-boundary threading and return ComposedConclusion_v0
    # (or AdmissionRefusal_v0 for standard/license refusals, or raise
    # ComposedConclusionRefusal (Service1Refusal family) for
    # composition_below_floor). Otherwise fall through to placeholder.
    if fork == "warm" and form == OutputForm.COMPOSED_CONCLUSION:
        return await package_composed_conclusion(request, trace_id)

    route_target = (
        ROUTE_ADMISSION_WARM_FORK if fork == "warm"
        else ROUTE_ADMISSION_FRESH_FORK
    )
    # The receiver-side (transform layer §6.2 composed_conclusion for warm;
    # async delivery §7 for fresh) is Phase 4b/5 territory. Placeholder
    # marks the phase-debt appropriately.
    receiver_debt = DEBT_PHASE_4 if fork == "warm" else DEBT_PHASE_5

    return DispatchResult(
        fork_decision=fork,
        route_target=route_target,
        feasibility_result=feasibility,
        floor_feasibility=floor_result,
        placeholder_body=_make_placeholder(
            route=route_target,
            phase_debt=receiver_debt,
            trace_id=trace_id,
        ),
        trace_id=trace_id,
    )
