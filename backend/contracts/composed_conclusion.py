"""ComposedConclusion@v0 — governed composed-conclusion envelope
(Phase 4b freeze — 18th frozen contract).

Spec authority: RMS Product & Engineering Spec v3 §6.2 (Composed
conclusion — full). Anchor lines cited inline in field descriptions.

**Condition B1 — Class computed once, threaded from Solva boundary.**

The `conclusion_class` field is populated by threading the output of
`services.solva_depth.assertion.conclusion_class(load_bearing_units)`
into this envelope UNCHANGED. Any recomputation site — anywhere in
`services/`, `routers/`, or the transform layer — is grep-negative
enforced by `test_composed_conclusion_class_from_solva_boundary_only`.
The A2 `supported_class` lesson (composition-time value computed once,
threaded, never recomputed) is applied here at the shape level: this
envelope's `conclusion_class` is Solva's assertion-boundary output,
period. Recomputing it downstream — even to arrive at the same value —
fails review on sight.

**Family posture (not a refusal envelope).**

This is the SUCCESS shape for §6.2 composed-conclusion. The sibling
refusal shape for below-floor conclusions is `Service1Refusal@v0`
(existing frozen contract from A2) with `reason=composition_below_floor`
— v3 §6.2.6 anchor. No new refusal envelope is landed at 4b; the
existing family member handles §6.2's below-floor case exactly per
spec's asked / supported_class / what_would_raise_it fields.

**v3 §6.2 six-point compliance (line-anchored):**

  1. **Definition** (v3 line 96): 'A synthesized answer to a specific
     ask, with class and trace.' → `answer_text` + `objective_ref`
     (specific ask) + `conclusion_class` (class) + `trace_id` (trace).
  2. **Production** (v3 line 97): 'Solva five-stage composition over
     selected units; load-bearing set identified; conclusion class =
     floor over load-bearing units' classes; trace mandatory.' →
     `conclusion_class` threaded from Solva boundary (Condition B1);
     `load_bearing_unit_ids` names the identified set;
     `trace_id` mandatory (min_length=1).
  3. **Provenance** (v3 line 98): 'Floor-over-load-bearing, carried
     as the conclusion's class; load-bearing set retrievable by
     trace_id.' → `load_bearing_unit_ids` retrievable via Northena
     Ledger correlation by `trace_id`.
  4. **Grain** (v3 line 99): 'synthesized_whole only.' → enforced
     UPSTREAM at admission by grain-compat artifact (Phase 4a);
     non-synthesized_whole grains never reach this envelope. This
     envelope therefore carries NO `grain` field (invariant, not
     omission — the shape guarantees synthesized_whole context).
  5. **Delivery** (v3 line 100): 'Hand-over (rendered brief/report)
     or per-response on the live path; both carry class inline.' →
     `conclusion_class` is top-level (not nested); §12 invariant #7
     satisfied structurally. Phase 4b covers the live-path sync
     return; Phase 5 wraps this SAME envelope for async delivery.
  6. **Standard enforcement** (v3 line 101): 'Enforced at conclusion
     class: below the objective's floor → the refusal envelope
     (asked / supported_class / what_would_raise_it).' → the sibling
     `Service1Refusal@v0` (existing) with reason
     `composition_below_floor` handles this case. NOT this envelope.

**Downstream consumers (D4b binding surfaces):**

  * **Phase 4b live-path route** — `POST /api/service_1/v2/dispatch`
    returns this @HTTP 200 for `entry=external_request` + warm-fork
    + `output.form=composed_conclusion` + composition-above-floor.
    Sibling: `Service1Refusal_v0` @HTTP 422 for below-floor at
    conclusion class.
  * **Phase 5 async delivery envelope** — `GET /v1/objectives/{id}`
    on state `delivered` returns this envelope wrapped by the async
    terminal-state envelope. v3 §7 line 131: 'envelopes frozen and
    additive' — Phase 5's wrapper freezes AROUND this frozen shape,
    which requires this shape to be frozen first (Axis 2 argument).
  * **Phase 7 wizard live-answer surface** — renders this envelope
    inline on the wizard's answer surface (UI Spec §3.3 refusal-
    with-path semantics apply only when the sibling refusal fires;
    on the success path the wizard renders this envelope's fields).
  * **Northena Ledger** — records `trace_id` → `run_id` →
    `conclusion_class` correlation. The Ledger's existing frozen
    contract (`NorthenaLedgerRow`) already carries `trace_id`;
    the correlation is by reference, not by contract-mutation.

**Convention anchors:**

  * `conclusion_class: DefensibilityClass` — direct enum reuse from
    `contracts.five_rings.DefensibilityClass` (Ring 5, frozen G0).
    No local literal; type-and-value both governed by the pre-existing
    frozen ring.
  * `computed_at: str` (ISO-8601 UTC) — mirrors
    `contracts.targeta_plan.MiningPlan.generated_at` convention.
  * `trace_id: str` — mirrors `Service1Refusal.trace_id` +
    `AdmissionRefusal_v0.trace_id` family shape; same field name +
    semantic across the response family.

Freeze contract: `ComposedConclusion_v0.model_json_schema()` snapshotted
to `tests/invariants/composed_conclusion.contract_snapshot.json`.
Mechanical parity invariant enforces the source→snapshot bijection
at 18 entries post-Phase-4b.
"""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field

from contracts.five_rings import DefensibilityClass


class ComposedConclusion_v0(BaseModel):
    """Governed composed-conclusion envelope — 18th frozen contract."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    conclusion_class: DefensibilityClass = Field(
        ...,
        description=(
            "Ring 5 defensibility class of the composed conclusion. "
            "Populated by threading "
            "`services.solva_depth.assertion.conclusion_class"
            "(load_bearing_units)` output UNCHANGED (Condition B1). "
            "Below-floor conclusions do NOT populate this envelope — "
            "the sibling `Service1Refusal_v0(reason='composition_below"
            "_floor')` handles that case per v3 §6.2.6."
        ),
    )
    answer_text: str = Field(
        ...,
        min_length=1,
        description=(
            "The synthesized answer to the specific ask (v3 §6.2.1 "
            "at line 96). Renders inline in the live-path response "
            "body per v3 §12 invariant #7 (line 169): 'no response "
            "shape separates claim from class'. answer_text and "
            "conclusion_class are colocated in the same top-level "
            "envelope — the invariant is satisfied structurally."
        ),
    )
    trace_id: str = Field(
        ...,
        min_length=1,
        description=(
            "Correlation ID (v3 §6.2.3 at line 98). Load-bearing set "
            "retrievable via Northena Ledger lookup keyed by this "
            "trace_id. Family field name/semantic — mirrors "
            "Service1Refusal.trace_id and AdmissionRefusal_v0.trace_id."
        ),
    )
    load_bearing_unit_ids: List[str] = Field(
        ...,
        min_length=1,
        description=(
            "Ordered list of `NormalizedUnit.unit_id` values whose "
            "defensibility classes floored to `conclusion_class` "
            "(v3 §6.2.2 at line 97). Non-empty invariant: "
            "`services.solva_depth.assertion.conclusion_class` raises "
            "ValueError on empty input, so the load-bearing set is "
            "always non-empty on success. Ordered: preserves Solva's "
            "identification order for downstream trace-lens "
            "reconstruction."
        ),
    )
    objective_ref: str = Field(
        ...,
        min_length=1,
        description=(
            "Identifier of the ObjectiveRequest (v0 or v2) this "
            "conclusion answers (v3 §6.2.1 'specific ask'). "
            "Correlator into the commissioning record for governance"
            "-side auditability (Regulator/DPO surface per §9)."
        ),
    )
    computed_at: str = Field(
        ...,
        min_length=1,
        description=(
            "ISO-8601 UTC. When Solva's composition boundary emitted "
            "this envelope. Convention-anchored to "
            "`contracts.targeta_plan.MiningPlan.generated_at`."
        ),
    )
