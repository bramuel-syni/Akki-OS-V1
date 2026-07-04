# Phase 4 Stage A — Full-text artifacts (design-only)

**Date:** 2026-07-03 (third close pass after two vacates for summary-vs-artifact posture).
**Type:** design-only. Zero code files under `/app/backend/`. Docs-only landing at this path is the canonical-source backup; inline delivery to owner in message body is the primary channel.
**CI status at close:** 413/413 GREEN. `make ci` PASSED. Mechanical parity invariant GREEN at 17. Substrate-drop 9/9 GREEN.

---

## Section 1 — 4a/4b split seam (Artifact 4)

### Phase 4a file-by-file (14 files, ~950 net-new LoC, ~230 lifted)

| # | File | Kind | Net-new LoC | Purpose | Lifted-from |
|---|---|---|---|---|---|
| 4a.1 | `services/service_1/grain_compatibility.py` | NEW pure-function module | ~70 | Single-source (form, grain) compat rules | `services/mtafiti/floor_feasibility.py` module structure |
| 4a.2 | `services/service_1/license_classes.v0.json` | NEW versioned config (NOT snapshotted) | ~35 | Master Admin taxonomy for license classes | `services/service_1/admission_refusal_reasons.v0.json` |
| 4a.3 | `services/service_1/license_class_selection.py` | NEW service module | ~110 | `is_valid_class`, `derive_license_class_from_commissioner`, `select_by_class` | `services/service_1/admission_refusal.py` registry-load pattern |
| 4a.4 | `services/service_1/admission_refusal_reasons.v1.json` | REGISTRY BUMP (additive) | ~25 | Adds 3 reason codes: `grain_form_incompatible`, `standard_below_admission_floor`, `license_class_unavailable` | `admission_refusal_reasons.v0.json` structure |
| 4a.5 | `services/service_1/admission_refusal.py` | MODIFIED (add 3 emit-helpers) | ~90 | `emit_grain_form_incompatible`, `emit_standard_below_admission_floor`, `emit_license_class_unavailable` | Existing `emit_form_not_offerable` pattern |
| 4a.6 | `services/service_1/qualified_data.py` | NEW selection+packaging service | ~140 | `select_units_for_reach`, `package_qualified_data`, ride existing outer-gate | Mtafiti registry read patterns + solva-depth governor floor patterns |
| 4a.7 | `services/service_1/dispatch.py` | MODIFIED | ~60 | Wire grain-compat + license_class + hard-input-filter in front of feasibility fork; wire §6.1 payload production on warm success | Phase 2/3 dispatch pattern |
| 4a.8 | `routers/service_1.py` | MODIFIED | ~15 | Union return widens: add §6.1 payload response (UNFROZEN dict per Section 7 recommendation) | Phase 2/3 router isinstance branch |
| 4a.9 | `tests/invariants/test_grain_compatibility_shared_source.py` | NEW gate | ~50 | Single-source enforcement, exhaustiveness, actor-appropriateness | `test_floor_feasibility_shared_derivation.py` mirror |
| 4a.10 | `tests/invariants/test_license_class_config_governs_taxonomy.py` | NEW gate | ~60 | Config governs; grep-negative on hard-coded class names in .py files | `test_admission_refusal_reason_extension_via_registry_bump` pattern |
| 4a.11 | `tests/invariants/test_qualified_data_selection.py` | NEW gate | ~90 | Standard hard-input-filter + license selection + per-claim provenance | `test_feasibility_honesty_under_absence` seed patterns |
| 4a.12 | `tests/invariants/test_qualified_data_outer_gate_ride.py` | NEW gate | ~40 | Outer-gate files SHA untouched + receipt shape unchanged | `test_dispatch_v0_untouched.py` SHA-invariance |
| 4a.13 | `tests/invariants/test_dispatch_grain_form_refusal.py` | NEW gate | ~50 | Admission-time grain-compat refusal wire shape | `test_admission_refusal_dispatch.py` |
| 4a.14 | `tests/invariants/test_v0_paths_byte_identical_after_4a.py` | NEW regression | ~35 | SHA-invariance on 5 v0 files | `test_dispatch_v0_untouched.py` mirror |
| — | Continuity docs (§0.2 debt update; no new §4 row since 4a adds zero frozen contracts) | MODIFIED | ~40 | Phase Ledger + Live State updates | N/A |
| — | **4a TOTAL** | | **~950 net-new / ~230 lifted** | ~4.1× overall / M-L crossover | |

### Phase 4a gate list (11 gates)

1. `test_grain_compat_synthesized_whole_refused_at_qualified_data` — v3 §6.1.4 verbatim ("synthesized_whole unsupported (that is composed_conclusion)"). LOAD-BEARING.
2. `test_grain_compat_single_source_of_truth` — Ruling 4 pattern. AST grep-negative on `(OutputForm.*, OutputGrain.*)` dict-of-tuples outside canonical module.
3. `test_grain_compat_per_claim_and_aggregated_pass_at_qualified_data` — positive gates for compatible cells.
4. `test_license_class_config_governs_taxonomy` — reads `license_classes.v0.json`; grep-negative for illustrative class-name literals in `.py` files under `services/`, `contracts/`, `routers/`.
5. `test_license_class_selection_filters_registry_reads` — populated Registry with mixed classes; selection with specific class filters correctly.
6. `test_license_class_absence_below_floor_route` — zero units match selected class → `AdmissionRefusal_v0(reason=license_class_unavailable)` @422.
7. `test_qualified_data_standard_hard_input_filter` — v3 §6.1.6. Populated Registry with below-floor units; selection excludes them; output payload has zero below-floor claim classes.
8. `test_qualified_data_outer_gate_ride_receipt_unchanged` — v0 outer_gate/{transform,mint,receipt}.py SHA-untouched; `OuterGateReceipt@v0` shape unchanged (Condition B3).
9. `test_qualified_data_per_claim_provenance_intact` — v3 §6.1.3. Every claim in output has `trace_id`, `defensibility_class`, `contested` set.
10. `test_v0_paths_byte_identical_after_4a` — SHA-identity on `contracts/objective_request.py`, `services/service_1/service.py`, `contracts/service_1_refusal.py`, `contracts/admission_refusal.py`, `services/outer_gate/*.py` (Condition B4).
11. `test_admission_refusal_registry_v1_extends_v0_additively` — v1 bump preserves v0 reasons + adds three new; contract snapshot byte-identical (Condition B2).

### Phase 4b file-by-file (15 files, ~810 net-new LoC, ~55 lifted)

| # | File | Kind | Net-new LoC | Purpose | Lifted-from |
|---|---|---|---|---|---|
| 4b.1 | `contracts/composed_conclusion.py` | NEW 18th frozen contract | ~160 | `ComposedConclusion_v0` schema + module docstring per §6.2 anchors | `contracts/feasibility_result.py` docstring pattern |
| 4b.2 | `tests/invariants/composed_conclusion.contract_snapshot.json` | NEW canonical snapshot (Pydantic-generated) | ~120 | Byte-frozen schema | N/A |
| 4b.3 | `contracts/__init__.py` | MODIFIED | +2 | Export `ComposedConclusion_v0` | Phase 3 pattern |
| 4b.4 | `tests/invariants/test_frozen_contract_snapshot_parity.py` | MODIFIED | +1 | Add `composed_conclusion.py` → snapshot map entry | Phase 3 pattern |
| 4b.5 | `tests/invariants/test_composed_conclusion_v0_contract_frozen.py` | NEW invariant | ~35 | Schema-freeze snapshot test | Phase 3 invariant pattern |
| 4b.6 | `services/service_1/composed_conclusion.py` | NEW service | ~100 | Solva-boundary threading, trace correlation, envelope build | Existing `services/solva_depth/pipeline.py` load-bearing selection |
| 4b.7 | `services/service_1/dispatch.py` | MODIFIED | ~50 | Wire composed_conclusion path on warm success; Solva-boundary invocation | 4a dispatch extension pattern |
| 4b.8 | `routers/service_1.py` | MODIFIED | ~20 | Widen Union: `ComposedConclusion_v0` @200 + `Service1Refusal_v0` @422 for §6.2 below-floor | Phase 3 isinstance branch pattern |
| 4b.9 | `tests/invariants/test_composed_conclusion_class_from_solva_boundary_only.py` | NEW gate (LOAD-BEARING) | ~80 | Condition B1 AST-inspection + grep-negative on floor recomputation | `test_dispatch_uses_shared_feasibility_and_floor_feasibility` |
| 4b.10 | `tests/invariants/test_composed_conclusion_grain_synthesized_whole_only.py` | NEW gate | ~40 | v3 §6.2.4; non-synthesized_whole → admission refusal | grain-compat lookup |
| 4b.11 | `tests/invariants/test_composed_conclusion_below_floor_returns_service_1_refusal.py` | NEW gate | ~50 | v3 §6.2.6; existing envelope reuse | A2 refusal pattern |
| 4b.12 | `tests/invariants/test_composed_conclusion_load_bearing_retrievable_by_trace_id.py` | NEW gate | ~60 | v3 §6.2.3; Ledger correlation | Ledger patterns |
| 4b.13 | `tests/invariants/test_composed_conclusion_live_path_returns_class_inline.py` | NEW gate | ~45 | v3 §12 invariant #7; ASGITransport wire-shape | Phase 3 wire-shape patterns |
| 4b.14 | `tests/invariants/test_v0_paths_byte_identical_after_4b.py` | NEW regression | ~35 | SHA-invariance on 17 prior contracts | 4a mirror |
| — | Continuity docs (17→18 frozen contracts, §0.2 debt update, §4 row 18) | MODIFIED | ~35 | Phase Ledger + Live State + Frozen Contracts table | N/A |
| — | **4b TOTAL** | | **~810 net-new / ~55 lifted** | ~14.7× overall / M-band | |

### Phase 4b gate list (8 gates)

12. `test_composed_conclusion_v0_contract_frozen` — schema-freeze on 18th contract.
13. `test_composed_conclusion_class_from_solva_boundary_only` — **LOAD-BEARING (Condition B1)**. AST-inspects `services/service_1/composed_conclusion.py` to confirm the ONLY class-source is `from services.solva_depth.assertion import conclusion_class`; grep-negative on `min(u.defensibility_class` and `min(u.defensibility.defensibility_class` outside `services/solva_depth/assertion.py`.
14. `test_composed_conclusion_grain_synthesized_whole_only` — v3 §6.2.4. Non-synthesized_whole grain → `AdmissionRefusal_v0(reason=grain_form_incompatible)` at admission.
15. `test_composed_conclusion_below_floor_returns_service_1_refusal_v0` — v3 §6.2.6. Response is `Service1Refusal_v0(reason=composition_below_floor, asked, supported_class, what_would_raise_it)`. No new refusal contract.
16. `test_composed_conclusion_load_bearing_retrievable_by_trace_id` — v3 §6.2.3. Northena Ledger lookup by `trace_id` returns `load_bearing_unit_ids`.
17. `test_composed_conclusion_live_path_returns_class_inline` — v3 §6.2.5 + §12 invariant #7. Route returns flat body with `conclusion_class` at top level.
18. `test_v0_paths_byte_identical_after_4b` — SHA-identity on all 17 prior contracts (Condition B4).
19. `test_composed_conclusion_snapshot_parity_at_18` — mechanical parity invariant map 17→18; three parity tests green.

### 4b → 4a concrete import lines (structural dependency proof)

Three concrete `from X import Y` lines that appear in 4b-created files referencing 4a-created symbols:

```python
# In services/service_1/composed_conclusion.py (4b.6):
from services.service_1.grain_compatibility import evaluate_grain_form, GrainCompatResult
from services.service_1.license_class_selection import select_by_class, derive_license_class_from_commissioner
from services.service_1.qualified_data import select_units_for_reach
```

Reverse-direction grep at 4a-land time: `grep "from services.service_1.composed_conclusion" backend/services/service_1/{grain_compatibility,license_class_selection,qualified_data}.py` → **0 hits.** 4a does not import from 4b. Dependency is asymmetric.

### Sizing verdict — 4a/4b split RECOMMENDED

| Scenario | Net-new | Lifted | Ratio | Band |
|---|---|---|---|---|
| Single Phase 4 (combined) | ~1310 | ~230 | ~5.7× overall | **XL** (twice-flagged risk band) |
| **Phase 4a alone** | ~950 | ~230 | ~4.1× overall | **M-L crossover** |
| **Phase 4b alone (post-4a)** | ~810 | ~55 | ~14.7× overall | **M** (test-heavy, matches Phase 3 profile) |

---

## Section 2 — `ComposedConclusion_v0` full schema + three D4b axes ARGUED

### Full Pydantic model (lands at 4b as `contracts/composed_conclusion.py`)

```python
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
```

**No sub-models.** `LoadBearingClaim`/`ClaimReference` rejected: `load_bearing_unit_ids: List[str]` is sufficient; full unit content is retrievable by Ledger via `trace_id` (v3 §6.2.3). Embedding claims inline duplicates the Ledger's role, bloats the wire, and creates a second freeze surface for claim shape already governed by `NormalizedUnit` frozen contract.

**No enums beyond the pre-existing `DefensibilityClass`.**

### Three D4b axes ARGUED

**Axis 1 — class + trace crosses governance boundary per §12 invariant #7.**

v3 §12 invariant #7 verbatim (`/app/docs/mandates/RMS_Product_Engineering_Spec_v3.md:169`):

> "Governance travels inline everywhere, including async: no response shape separates claim from class; webhooks never carry claims; nothing partial egresses."

**Concrete boundary crossed:** the Solva assertion boundary is a SERVICE-INTERNAL surface — `services/solva_depth/assertion.py::conclusion_class()` computes `DefensibilityClass` from a `Sequence[NormalizedUnit]` in-process. The **user-facing response envelope** is a SERVICE-EXTERNAL surface — the HTTP wire shape returned to callers of `POST /api/service_1/v2/dispatch`. Between these two surfaces sits the governance boundary the invariant governs: the class must travel INLINE with the claim (`answer_text`) across that boundary.

**Field carrying the crossing:** `conclusion_class` (from Solva boundary — producer) colocated with `answer_text` (the claim/answer — consumer's read) in a SINGLE top-level envelope. The colocation IS the mechanism enforcing the invariant.

**What fails silently if the shape drifts:** an unfrozen envelope where a future refactor moves `conclusion_class` into a nested `{metadata: {conclusion_class: ...}}` structure and clients read `answer_text` from the top level. Silent-drift outcome: consumer render paths (mobile client, LLM downstream, API integration) may render `answer_text` WITHOUT the class because it's now buried in metadata. §12 invariant #7 is violated without any test firing. FREEZE closes this silent-drift surface.

**Axis 2 — downstream Phase 5 async wrapper binds it STRUCTURALLY.**

v3 §7 line 125 verbatim:

> "Fork at admission: warm → synchronous full response (existing contract). Fresh → `202` with `{ objective_id, status: accepted, delivery_estimate, quote? }`."

v3 §7 line 126 verbatim:

> "States: `accepted → running → delivered | refused`."

v3 §7 line 128 verbatim (webhook clause):

> "Thin webhook, governed fetch: webhook payload = `{ event, objective_id, trace_id, status }` — never claim content; fetch = `GET /v1/objectives/{id}` returns the shaped output at the delivered state."

v3 §7 line 131 verbatim (versioning clause):

> "Versioning: envelopes frozen and additive (the established A2 pattern); breaking change = new path version."

**Structural binding argument:** Phase 5's async delivery envelope (Stage B for Phase 5) must define what `delivered` state returns when the transform was `composed_conclusion`. Per line 131 that envelope MUST be FROZEN AND ADDITIVE. If the inner `ComposedConclusion_v0` shape is UNFROZEN, Phase 5's frozen wrapper is nesting an unfrozen field — a broken freeze surface.

Concretely: Phase 5's Stage B lands (hypothetically) `AsyncDeliveryTerminal_v0` with `payload: Union[ComposedConclusion_v0, <§6.1 payload>, KnowledgeArtifact, ...]` — for the Union to freeze, each member must freeze. Line 128's governed-fetch return shape IS `ComposedConclusion_v0` in full for the composed_conclusion form.

Merely-referential alternative rejected: Phase 5 could carry only `{objective_ref, trace_id, delivered_at}` and require callers to re-fetch via a separate endpoint. Rejected because line 128's fetch itself must return the composed conclusion (webhook is thin, fetch is full); and v3 §6.2.5 (line 100) requires class inline with the answer — a fetch returning only IDs violates §12 invariant #7 at the async boundary.

**Axis 3 — wire-shape guarantee required; unfrozen cannot deliver.**

v3 §6.2 anchor lines quoted:

- v3 §6.2.1 line 96 verbatim: "A synthesized answer to a specific ask, with class and trace."
- v3 §6.2.2 line 97 verbatim: "Solva five-stage composition over selected units; load-bearing set identified; conclusion class = floor over load-bearing units' classes; trace mandatory."
- v3 §6.2.3 line 98 verbatim: "Floor-over-load-bearing, carried as the conclusion's class; load-bearing set retrievable by trace_id."
- v3 §6.2.4 line 99 verbatim: "Grain: synthesized_whole only."
- v3 §6.2.5 line 100 verbatim: "Hand-over (rendered brief/report) or per-response on the live path; both carry class inline."
- v3 §6.2.6 line 101 verbatim: "Enforced at conclusion class: below the objective's floor → the refusal envelope (asked / supported_class / what_would_raise_it)."

**Callers whose contract-with-the-system depends on wire-shape stability:**

1. **Buyer client integrations** (v3 §3.3 buyer variant, line 62): buyer integration polls `GET /v1/objectives/{id}` (§7 line 128) and expects a stable JSON shape for the delivered composed conclusion. Wire-shape drift silently breaks integrations without a §7-line-131 version bump.

2. **Ask console surface** (v3 §9 line 143: "ask console (ask → answer → refusal)"). First-class UX surface rendering the SUCCESS envelope inline. `conclusion_class` field-migration silently mis-renders or hides class.

3. **Regulator/DPO surface** (v3 §9 line 143: "the record itself, read-only"). Historical persisted envelopes must remain shape-parseable across time; freeze at land time IS the persistence guarantee.

4. **Northena Ledger absorption** (v3 §2 line 18 fold-in). Ledger persists references to composed conclusions; historical shape drift means historical Ledger rows lose their referent shape.

Unfrozen fails all four — Pydantic's `frozen=False` allows in-place field addition/removal/rename without a version-signaled breaking change; callers have no signal that a shape change occurred and cannot defensively code. FREEZE + snapshot invariant is the ONLY mechanism honoring §7 line 131 at the transform-output layer.

**All three axes argue cleanly. Zero HAZARD-STOP. Verdict: FREEZE. 17 → 18 at Phase 4b close.**

### Mechanical parity invariant map entry (lands at 4b Stage B)

```python
CONTRACT_TO_SNAPSHOT: Dict[str, str] = {
    "admission_refusal.py":           "admission_refusal.contract_snapshot.json",
    "composed_conclusion.py":         "composed_conclusion.contract_snapshot.json",   # NEW at 4b
    "cumulative_disclosure.py":       "cumulative_disclosure_ledger.contract_snapshot.json",
    # ... (existing 15 entries unchanged) ...
}
```

---

## Section 3 — Full v3 §6.1/§6.2 scope table (Artifact 5)

### §6.1 scope table

| # | Template point | v3 anchor (line + verbatim quote) | Verdict | Justification |
|---|---|---|---|---|
| 6.1.1 | Per-claim units carrying class + contested + provenance + trace_id | line 88: "Per-claim units, each carrying defensibility class, contested status, provenance, `trace_id`." | **COVERED (4a)** | `services/service_1/qualified_data.py::select_units_for_reach` returns `List[NormalizedUnit]`; frozen contract fields include defensibility, provenance, trace_id per existing schema. |
| 6.1.2 | Selection (reach + standard filter + license class) → packaging → outer-gate export | line 89: "Selection (reach + standard filter + license class) → packaging → outer-gate export (rights check, irreversibility, cumulative-disclosure, license issue, receipt)." | **COVERED (4a)** | Three-filter composition (`Reach`, standard via existing `_max_supported_class` pattern, license via new `select_by_class`); packaging into pre-egress artifact; ride existing `services.outer_gate.transform → mint → receipt` unmodified per Condition B3. |
| 6.1.3 | Per-claim provenance intact end-to-end | line 90: "Per-claim provenance intact end-to-end." | **COVERED (4a)** | Gate 9 (`test_qualified_data_per_claim_provenance_intact`) asserts every output claim carries `trace_id`, `defensibility_class`, `contested` verbatim from source `NormalizedUnit`. |
| 6.1.4 | Grains: per_claim + aggregated; synthesized_whole unsupported | line 91: "Grains: per_claim, aggregated. synthesized_whole unsupported (that is composed_conclusion)." | **REFUSAL-VIA-ADMISSION-REGISTRY (4a)** | Grain-compat artifact returns `(qualified_data, synthesized_whole) → compatible=False, refusal_reason=grain_form_incompatible, path_forward=composed_conclusion`. Admission emits `AdmissionRefusal_v0(reason=grain_form_incompatible)` @422. NEW reason code in `admission_refusal_reasons.v1.json` bump. |
| 6.1.5 | Hand-over; governance enforced once at export via outer gate | line 92: "Hand-over; governance enforced once at export via the outer gate." | **COVERED (4a)** | Outer-gate ride unchanged; Condition B3 preserved; Gate 8 (`test_qualified_data_outer_gate_ride_receipt_unchanged`) SHA-invariants `services/outer_gate/*.py` + `OuterGateReceipt@v0`. |
| 6.1.6 | Standard = hard input filter; below-floor never enters deliverable | line 93: "Standard = hard input filter; below-floor units never enter the deliverable." | **COVERED (4a) + REFUSAL-VIA-ADMISSION-REGISTRY** | Standard filter runs at selection — hard filter excludes below-floor units before packaging. If filter removes ALL units for the reach → `AdmissionRefusal_v0(reason=standard_below_admission_floor)` @422. NEW reason code per Condition B2. Distinct from `Service1Refusal(reason=composition_below_floor)` (§6.2 conclusion-time). |

### §6.2 scope table

| # | Template point | v3 anchor (line + verbatim quote) | Verdict | Justification |
|---|---|---|---|---|
| 6.2.1 | Synthesized answer to a specific ask, with class + trace | line 96: "A synthesized answer to a specific ask, with class and trace." | **COVERED (4b)** | `ComposedConclusion_v0.{answer_text, objective_ref, conclusion_class, trace_id}`. |
| 6.2.2 | Solva five-stage composition; load-bearing set; conclusion class = floor; trace mandatory | line 97: "Solva five-stage composition over selected units; load-bearing set identified; conclusion class = floor over load-bearing units' classes; trace mandatory." | **COVERED (4b)** | `services/service_1/composed_conclusion.py` orchestrates existing `services/solva_depth/pipeline.py` (five-stage) + `services/solva_depth/load_bearing.py::identify_load_bearing_units` + Solva-boundary threading (`conclusion_class` imported UNCHANGED per Condition B1). `trace_id` min_length=1 enforced by contract. |
| 6.2.3 | Floor-over-load-bearing carried as conclusion's class; retrievable by trace_id | line 98: "Floor-over-load-bearing, carried as the conclusion's class; load-bearing set retrievable by trace_id." | **COVERED (4b)** | `load_bearing_unit_ids: List[str]` embedded; retrievability via Northena Ledger's trace_id correlation; Gate 16 (`test_composed_conclusion_load_bearing_retrievable_by_trace_id`) asserts Ledger lookup returns same ids. |
| 6.2.4 | Grain: synthesized_whole only | line 99: "Grain: synthesized_whole only." | **REFUSAL-VIA-ADMISSION-REGISTRY (4a shared)** | Non-synthesized_whole grains at composed_conclusion refused at admission by grain-compat (SAME rule surface as §6.1 grain refusal, SAME reason code `grain_form_incompatible`). Enforced upstream; 4b's envelope never encounters bad grain. |
| 6.2.5 | Hand-over or per-response on live path; both carry class inline | line 100: "Hand-over (rendered brief/report) or per-response on the live path; both carry class inline." | **COVERED (4b — live path); DEFERRED to Phase 5 (async hand-over)** | Live sync return via `POST /api/service_1/v2/dispatch` @200 with `ComposedConclusion_v0`; async hand-over channel is Phase 5's async wrapper around same frozen envelope (§7 line 131 frozen-and-additive). |
| 6.2.6 | Enforced at conclusion class: below floor → refusal (asked / supported_class / what_would_raise_it) | line 101: "Enforced at conclusion class: below the objective's floor → the refusal envelope (asked / supported_class / what_would_raise_it)." | **COVERED (4b) via EXISTING `Service1Refusal@v0`** | NO new contract; existing A2 envelope has exact 7-field shape. Gate 15 asserts fires cleanly with `reason=composition_below_floor` and all named fields present. Family-consistency preserved. |

### Explicit callout — §6.2 live-path serving disposition

v3 anchor (`RMS_Product_Engineering_Spec_v3.md:100` verbatim):

> "Hand-over (rendered brief/report) **or per-response on the live path**; both carry class inline."

**Argument sync is native (not async-only):** v3 §4 line 71 verbatim — "Warm/fresh fork at admission: **an ask servable from qualified intelligence is answered synchronously**; one requiring fresh extraction returns the async contract (§7)." Direct mapping to §6.2.5's "per-response on the live path" — when composed conclusion is servable from already-qualified units (warm-fork branch), response is SYNCHRONOUS. Async only applies to fresh-extraction (Phase 5 territory).

**Wire-shape settlement at 4b:**

```
POST /api/service_1/v2/dispatch returns:
  Union[
    DispatchResult @501,                    # Phase 2 placeholder (still emitted for Phase-4/5-deferred cases)
    AdmissionRefusal_v0 @422,               # Phase 3 admission refusal + 4a §6.1 admission-time refusals
    ComposedConclusion_v0 @200,             # 4b live composed_conclusion warm success (NEW)
    Service1Refusal_v0 @422,                # 4b composition-below-floor per §6.2.6 (NEW invocation of existing envelope)
    <§6.1 payload> @200,                    # 4a live qualified_data warm success — UNFROZEN dict per Section 7
  ]
```

### Explicit callout — Grain-compat firing at BOTH admission (Phase 4) and wizard (Phase 7)

v3 anchor for shaping-time grain-compat (`RMS_Product_Engineering_Spec_v3.md:83` verbatim):

> "Provenance bound (machine-checkable, enforced at shaping time): the transform produces the shaped output only where the declared standard survives it. Each form carries a provenance-preservation rule evaluable by the wizard; a form/grain whose rule cannot satisfy the declared standard is refused during shaping with a path forward — never discovered at execution."

Single-source proof (both callers import THE SAME module):

```python
# Phase 4a caller — services/service_1/dispatch.py (present in 4a landing):
from services.service_1.grain_compatibility import evaluate_grain_form

# Phase 7 caller — services/wizard/shaping.py (future, Phase 7 landing) — DESIGN COMMITMENT:
from services.service_1.grain_compatibility import evaluate_grain_form   # IDENTICAL
```

Guard test `test_grain_compatibility_shared_source.py` (Section 5) enforces grep-negative on any local reimplementation.

### Explicit callout — `synthesized_whole` REFUSED at §6.1

v3 anchor (`RMS_Product_Engineering_Spec_v3.md:91` verbatim):

> "Grains: per_claim, aggregated. **synthesized_whole unsupported (that is composed_conclusion).**"

**Envelope:** `AdmissionRefusal_v0` (from Phase 3, via versioned reason registry — Condition B2 pattern).

**Reason code proposal:** `grain_form_incompatible` (single reason code SHARED across §6.1 and §6.2 non-compatible-grain refusals; the `path_forward` string discriminates between the two contexts).

**Rationale for shared reason code:** the admission-side semantic is identical — "the (form, grain) pair you asked for is not compatible; here's how to reshape". Context-specific advice lives in `path_forward` string per-rule. Unifies wire-level refusal shape while preserving per-rule guidance. Alternative (separate reason codes per cell) rejected as needless proliferation.

### COUNTER-VERDICT #1 — `license_class` Option C sidesteps owner's three field-entry candidates

**What owner's Stage A dispatch (A4) said verbatim:**

> "Selection parameter (code) — where the parameter enters the codebase: `Reach` (Phase 0's `ObjectiveRequest_v2.reach`?) or `Output` or a new additive field? Argue against v3."

Three candidates: (i) `Reach`, (ii) `Output`, (iii) new additive field.

**What Phase 4 Stage A proposes:** Option C — `license_class` is NOT a top-level caller-declared field. Runtime derivation at selection time via `derive_license_class_from_commissioner(objective.envelope) -> str` reads `objective.envelope.commissioner` and maps via `license_classes.v0.json`'s `commissioner_to_default_class`. No frozen-contract mutation; no new additive field on v2.

**Why the counter-verdict is doctrinally required:** v3 §3.3 line 65 verbatim — "use-purpose drives license class". The buyer's use-purpose is INPUT; license_class is OUTPUT of the shaping wizard's offerability negotiation (§3.3 line 63). Landing license_class as caller-declared explicit field encodes the OUTPUT of shaping as caller-declared INPUT — inverting the wizard's role. Option C respects v3 direction of causation.

If owner rules Option B (new frozen contract `SelectionOverlay_v0`) is preferred, that's a viable fallback documented in Section 4.

### COUNTER-VERDICT #2 — §6.1 payload UNFROZEN not owner-scoped

**What owner's Stage A dispatch said:** silence on §6.1 payload freeze status. Dispatch scoped grain-compat + license_class + admission-hard-filter + outer-gate ride, but did not specify whether the §6.1 payload response envelope itself should freeze.

**What Phase 4 Stage A concludes:** UNFROZEN plain dict body at 4a. Shape: `{units: List[NormalizedUnit-as-dict], receipt: OuterGateReceipt_v0.model_dump(), unit_count: int, computed_at: ISO-str}`.

**Why the counter-verdict is doctrinally required:** the §6.1 payload is a CONTAINER of already-frozen inner shapes (`NormalizedUnit` + `OuterGateReceipt_v0`). D4b bar is NOT met — no new governance semantic rides on the container's shape beyond what's already governed by inner frozen shapes. Freezing the container adds a second governance surface without adding a governance guarantee. See Section 7 for full three-axis D4b test applied.

Owner may rule to freeze (creating `QualifiedDataArtifact_v0` at 4a as 18th contract before ComposedConclusion at 4b becomes 19th) — Section 7 documents both paths.

---

## Section 4 — `license_class` Options A/B/C in full (Artifact 2)

### Option A — Additive to `ObjectiveRequest_v2` frozen contract

- **Selection parameter appearance:** `output.license_class: str` OR `commercial.license_class: str` OR `reach.license_class: str` — a new field on the frozen v2 contract.
- **Taxonomy:** either hardcoded `Literal[...]` (frozen enum) OR versioned config `license_classes.v0.json`.
- **What breaks:** modifying `ObjectiveRequest_v2` frozen contract mutates the schema and breaks its byte-identical snapshot. Same class of violation as literal-widening — the snapshot's structural signature changes.
- **Doctrine preserved/violated:**
  - Ruling 2 (no schema mutation of frozen contract): **VIOLATED.**
  - Term 2 (shape freezes, values version): SHAPE would change — VIOLATED.
  - Elevated Doctrine (validation surface = contract surface): **VIOLATED** if taxonomy is enum; PRESERVED if registry.
- **Verdict: REJECTED — HAZARD-STOP-a per Ruling 2.**

### Option B — New frozen contract `SelectionOverlay_v0`

- **Selection parameter appearance:** new frozen contract at `contracts/selection_overlay.py`. Schema (proposed):
  ```python
  from pydantic import BaseModel, ConfigDict, Field

  class SelectionOverlay_v0(BaseModel):
      model_config = ConfigDict(extra="forbid", frozen=True)
      license_class: str = Field(
          ..., min_length=1, pattern=r"^[a-z][a-z_]*[a-z]$",
          description="Selection-time license class. Registry-governed."
      )
      applied_at: str = Field(..., min_length=1)
  ```
  Caller passes as separate query parameter or embedded in wrapper envelope alongside `ObjectiveRequest_v2` (route body becomes `{objective: ObjectiveRequest_v2, selection: SelectionOverlay_v0}`, or new companion endpoint).
- **Taxonomy:** versioned config `license_classes.v0.json` (Ruling 3 pattern); class names governed by config; contract's `license_class` is constrained `str` mirroring `AdmissionRefusal_v0.reason`'s doctrinal-tension resolution.
- **What breaks:** requires ADDITIONAL freeze (17→18 at 4a, before ComposedConclusion pushes 18→19 at 4b) AND route-shape change (widen v2 dispatch route body, or add companion endpoint). Structurally: adds EXPLICIT caller-declared parameter — commits v3 §3.3 line 65 "use-purpose drives license class" direction as caller-input, inverting the shaping semantic.
- **Doctrine preserved/violated:**
  - Ruling 2: **PRESERVED** (v2 unchanged; new contract is additive per Substrate-Drop v2 pattern).
  - Ruling 3 (config-as-versioned-not-frozen): **PRESERVED** (taxonomy in config).
  - Term 2: **PRESERVED** (shape freezes, values version).
  - Elevated Doctrine: **PRESERVED** (registry lives outside contract).
  - v3 §3.3 line 65 semantic direction: **INVERTED** — caller declares the output of shaping.
- **Verdict: VIABLE (fallback).** Clean doctrinally; inverts v3 semantic direction. Land as 18th frozen contract at 4a if owner rules Option C insufficient.

### Option C — Config-driven derivation from `Envelope.commissioner` (RECOMMENDED)

- **Selection parameter appearance:** NO caller-declared field. Runtime derivation at selection time via `derive_license_class_from_commissioner(objective.envelope) -> str` reads `objective.envelope.commissioner` and maps via config's `commissioner_to_default_class`. Derived class then feeds filter step.
- **Taxonomy:** versioned config `license_classes.v0.json` (Ruling 3 pattern; NOT snapshotted). Full schema below.
- **What breaks:** caller CANNOT override the derived class in this pass. If a buyer wants a non-default class for the same commissioner type, Option C requires either (i) new commissioner value in config, or (ii) landing Option B later as an addition. Buyer flexibility bounded by config space.
- **Doctrine preserved/violated:**
  - Ruling 2: **PRESERVED** (no contract change).
  - Ruling 3: **PRESERVED**.
  - Term 2: **PRESERVED**.
  - Elevated Doctrine: **PRESERVED**.
  - v3 §3.3 line 65 direction: **PRESERVED** (class is derived output, not declared input).
- **Verdict: RECOMMENDED.** Owner rules on B vs C.

### Option C concrete — full `license_classes.v0.json` schema

```json
{
  "config_version": "v0",
  "notes": "Master Admin config. Class NAMES in valid_classes are ILLUSTRATIVE — not prescriptive. Owner rules on class naming at 4a Stage B dispatch. Extension: add entry OR bump v0.json -> v1.json per Ruling 3 append-only config policy. Never modifies any frozen contract. Precedent anchor: services/service_1/admission_refusal_reasons.v0.json.",
  "valid_classes": [
    {
      "class_name": "editorial_use",
      "since_version": "v0",
      "description": "ILLUSTRATIVE: Internal editorial + reporting use; no redistribution."
    },
    {
      "class_name": "syndication",
      "since_version": "v0",
      "description": "ILLUSTRATIVE: Redistribution to identified third-party outlets."
    },
    {
      "class_name": "training_data",
      "since_version": "v0",
      "description": "ILLUSTRATIVE: Model training corpus use (ingredient-manifest scope per §6.5)."
    }
  ],
  "commissioner_to_default_class": {
    "operator_internal": "editorial_use",
    "buyer_syndication_partner": "syndication",
    "buyer_ml_partner": "training_data"
  }
}
```

**Class names `editorial_use`, `syndication`, `training_data` are ILLUSTRATIVE placeholders.** Owner rules on actual class taxonomy at 4a Stage B dispatch OR leaves as-is with the illustrative names surfaced as-such.

### Zero-license-values-in-Python grep-plan

Stage A design assurance (not Stage B enforcement). Grep-plan proving no license class name is hardcoded in any `.py` file:

```bash
$ cd /app/backend && grep -rn "editorial_use\|syndication\|training_data" \
    --include="*.py" -- services/ routers/ contracts/ tests/
```

Expected post-4a under Option C:

- **`contracts/`**: **0 hits.** Contracts do not reference class names — no Literal enum, no docstring reference.
- **`services/`**: hits ONLY in
  - `services/service_1/license_class_selection.py` — docstring EXAMPLES referencing class names (documentation, not runtime literal).
  - `services/service_1/admission_refusal.py` — refusal messages BUILT dynamically from config (not hardcoded string literals; substitution from `_load_registry()["commissioner_to_default_class"]`).
- **`routers/`**: **0 hits.**
- **`tests/`**: hits ONLY in test fixture setups seeding config file for testing (test fixtures may reference class names as test data — allowed since tests exercise the config path).

Under Option B (fallback), same result BUT with additional 0-hit under `contracts/selection_overlay.py` — contract holds `license_class: str` constrained by pattern, NOT `Literal[...]`.

Under Option A (rejected), class names bake into `Literal[...]` on frozen contract — the failure mode Option A is rejected for.

### Selection semantics per v3 — HARD FILTER

v3 §6.1.2 verbatim (line 89): "Selection (reach + standard filter + license class) → packaging → outer-gate export".

Three-way selection is INTERSECTION semantics — unit must satisfy `reach AND standard AND license class` to enter deliverable. NOT preference-order. Justification: v3 §6.1.5 (line 92) — "governance enforced once at export" — is a boundary, not preference. Soft-preference interpretation would allow license-mismatched units to leak into aggregated outputs, violating boundary semantic. HARD FILTER is only honest interpretation.

### Refusal path when zero units match selected class

**Envelope:** `AdmissionRefusal@v0` (from Phase 3).
**Reason code proposal:** `license_class_unavailable` — NEW; registered in `admission_refusal_reasons.v1.json` bump per Condition B2.

Registry entry:
```json
{
  "reason": "license_class_unavailable",
  "since_version": "v1",
  "notes": "The derived (or explicitly-selected under Option B) license class has zero qualifying units in the specified reach. Path forward: change license class (Option B) or expand reach."
}
```

Actor-appropriate `path_forward` (Condition 3 grep-negative on 4 forbidden phrases):

> "The requested license class has zero qualifying units in the specified reach. To reshape, either change license class or expand reach."

---

## Section 5 — Grain-compat artifact full text (Artifact 3)

### Artifact type verdict: PURE-FUNCTION MODULE with inline data structure

**Tradeoffs vs alternatives:**

| Option | Tradeoffs |
|---|---|
| **JSON data table only** | Pros: config-swappable. Cons: `path_forward` string is per-rule prose (i18n later); JSON-only forces string literals into JSON. No natural function signature both callers can import identically. |
| **Pure-function module with inline data** ★ | Pros: single import surface; both callers use identical import; data+behavior colocated for grep-atomic single-source-of-truth; mirrors `services/mtafiti/floor_feasibility.py` (Ruling 4). Cons: not runtime-swappable — but grain-compat rules are v3-spec-derived (§6.1.4, §6.2.4), not admin-configurable; this is a feature. |
| **Hybrid (JSON + reader function)** | Pros: both above. Cons: two surfaces to sync; grep for single-source must inspect both; complexity gain without benefit since grain-compat isn't admin-configurable. |

**Verdict: pure-function module only.** Grain-compat rules are STRUCTURAL properties of v3 (spec-derived, not admin-configurable). Matches `floor_feasibility.py` precedent (Ruling 4).

**File location:** `services/service_1/grain_compatibility.py`.

**Location justification:** consumed by service_1 dispatch (Phase 4a) and future Phase 7 wizard; service_1 is the composition-orchestration surface both converge through. Sibling to `admission_refusal.py` and `license_class_selection.py`.

### Full proposed `services/service_1/grain_compatibility.py`

```python
"""Grain-form compatibility — Ruling 4 shared-derivation pattern.

Single source of truth for the (output.form, output.grain) compatibility
matrix per v3 §6.1.4 + §6.2.4 + §6.3.4 + §6.4.4 + §6.5. Consumed by:
  * Phase 4 dispatch (admission-time refusal for `external_request` entry).
  * Phase 7 wizard (shaping-time refusal in conversation, Phase 7 land).

The rule surface (`evaluate_grain_form`) is imported by BOTH callers.
Reimplementation of this matrix outside this module is grep-negative
enforced by `test_grain_compatibility_shared_source.py`. Mirror of
`services/mtafiti/floor_feasibility.py` structural precedent.

v3 anchors:
  * §6.1.4 (line 91): 'Grains: per_claim, aggregated. synthesized_whole
    unsupported (that is composed_conclusion).'
  * §6.2.4 (line 99): 'Grain: synthesized_whole only.'
  * §6.3.4 (line 107): 'Grains: per_claim, aggregated.'  [STAKED]
  * §6.4.4 (line 115): 'Grains: per_claim and synthesized_whole per query.'  [STAKED]
  * §6.5    (lines 119-121): 'off the offerable menu' — form itself refused
    at Phase 3 (`form_not_offerable`); grain cells present in matrix for
    exhaustiveness but UNREACHABLE from live dispatch.

Path forward strings are ACTOR-APPROPRIATE per Condition 3 (Phase 3
disposition): no owner-side deliberation phrasing; caller-actionable
direction only. Enforced by `test_grain_compat_path_forward_actor_appropriate`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from contracts.objective_request_v2 import OutputForm, OutputGrain


@dataclass(frozen=True)
class GrainCompatResult:
    """Grain-form compatibility evaluation result.

    Returned by `evaluate_grain_form(form, grain)`. Consumers branch
    on `compatible`:
      * True  → proceed with dispatch/composition
      * False → emit refusal (Phase 4: AdmissionRefusal@v0 with
                `refusal_reason` as reason code + `path_forward` as
                action string; Phase 7: wizard renders inline
                refusal-with-path)
    """

    compatible: bool
    refusal_reason: Optional[str]     # snake_case; matches admission_refusal_reasons registry entries
    path_forward: Optional[str]       # actor-appropriate; None iff compatible=True


# The (form, grain) compatibility matrix — v3 §6.1–§6.5 anchors inline.
# Keys: (OutputForm, OutputGrain). Values: GrainCompatResult.
# Total combinations: 5 forms × 3 grains = 15 cells (exhaustive).
_MATRIX = {
    # v3 §6.1.4 — qualified_data: per_claim + aggregated only.
    (OutputForm.QUALIFIED_DATA, OutputGrain.PER_CLAIM):        GrainCompatResult(True, None, None),
    (OutputForm.QUALIFIED_DATA, OutputGrain.AGGREGATED):       GrainCompatResult(True, None, None),
    (OutputForm.QUALIFIED_DATA, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'synthesized_whole' grain is unsupported at 'qualified_data' output form. "
        "To use synthesized_whole, change output.form to 'composed_conclusion' (v3 §6.1.4, §6.2)."
    ),
    # v3 §6.2.4 — composed_conclusion: synthesized_whole only.
    (OutputForm.COMPOSED_CONCLUSION, OutputGrain.PER_CLAIM):    GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'per_claim' grain is unsupported at 'composed_conclusion' output form. "
        "To use per_claim, change output.form to 'qualified_data' (v3 §6.1.4, §6.2.4)."
    ),
    (OutputForm.COMPOSED_CONCLUSION, OutputGrain.AGGREGATED):   GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'aggregated' grain is unsupported at 'composed_conclusion' output form. "
        "To use aggregated, change output.form to 'qualified_data' (v3 §6.1.4, §6.2.4)."
    ),
    (OutputForm.COMPOSED_CONCLUSION, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(True, None, None),
    # v3 §6.3.4 [STAKED] — knowledge_artifact: per_claim + aggregated.
    (OutputForm.KNOWLEDGE_ARTIFACT, OutputGrain.PER_CLAIM):     GrainCompatResult(True, None, None),
    (OutputForm.KNOWLEDGE_ARTIFACT, OutputGrain.AGGREGATED):    GrainCompatResult(True, None, None),
    (OutputForm.KNOWLEDGE_ARTIFACT, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'synthesized_whole' grain is unsupported at 'knowledge_artifact' output form (v3 §6.3.4)."
    ),
    # v3 §6.4.4 [STAKED] — callable_skill: per_claim + synthesized_whole per query.
    (OutputForm.CALLABLE_SKILL, OutputGrain.PER_CLAIM):         GrainCompatResult(True, None, None),
    (OutputForm.CALLABLE_SKILL, OutputGrain.AGGREGATED):        GrainCompatResult(
        False,
        "grain_form_incompatible",
        "The 'aggregated' grain is unsupported at 'callable_skill' output form (v3 §6.4.4)."
    ),
    (OutputForm.CALLABLE_SKILL, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(True, None, None),
    # v3 §6.5 — model form off-menu; refused UPSTREAM by
    # `emit_form_not_offerable(reason='form_not_offerable')`. These
    # cells UNREACHABLE from live dispatch but present for matrix
    # exhaustiveness (grep-detectable if reachability invariant
    # is ever violated).
    (OutputForm.MODEL, OutputGrain.PER_CLAIM):         GrainCompatResult(False, "form_not_offerable", ""),
    (OutputForm.MODEL, OutputGrain.AGGREGATED):        GrainCompatResult(False, "form_not_offerable", ""),
    (OutputForm.MODEL, OutputGrain.SYNTHESIZED_WHOLE): GrainCompatResult(False, "form_not_offerable", ""),
}


def evaluate_grain_form(form: OutputForm, grain: OutputGrain) -> GrainCompatResult:
    """Ruling 4 shared-derivation — the ONLY grain-form evaluation site.

    Consumers:
      * `services.service_1.dispatch.dispatch()` — Phase 4a admission-time.
      * Phase 7 wizard state machine — shaping-time (Phase 7 landing).

    Both import THIS function; any local reimplementation elsewhere
    fails `test_grain_compatibility_shared_source.py`.
    """
    return _MATRIX[(form, grain)]
```

### Verbatim import lines

Phase 4a caller (`services/service_1/dispatch.py`):
```python
from services.service_1.grain_compatibility import evaluate_grain_form, GrainCompatResult
```

Phase 7 caller (future `services/wizard/shaping.py`, DESIGN COMMITMENT):
```python
from services.service_1.grain_compatibility import evaluate_grain_form, GrainCompatResult
```

Identical.

### Full proposed `test_grain_compatibility_shared_source.py`

```python
"""Grain-compat single-source-of-truth invariant — Phase 4a landing.

Mirror of `test_floor_feasibility_shared_derivation.py`. Enforces that
`services/service_1/grain_compatibility.py::evaluate_grain_form` is the
ONLY grain-form compatibility evaluation site in the codebase.
Reimplementation outside this module — even with equal outputs — fails
review on sight (Ruling 4 shared-derivation pattern).

Failure mode this prevents: Phase 7 wizard implementing its own
grain-compat table with different rules or messages, silently diverging
from Phase 4a's admission-time rules. Second computation-path is the
A2 `supported_class` lesson applied at rule-surface level.
"""
from __future__ import annotations

import ast
import inspect
from pathlib import Path

from services.service_1 import grain_compatibility as canonical_module


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


def test_grain_compatibility_shared_source_of_truth():
    """AST-inspect all .py files under services/ + routers/ (excluding
    the canonical module itself + test files). No file may declare a
    dict whose keys are `(OutputForm.*, OutputGrain.*)` tuples — that
    pattern is the local-rule-table signal."""

    canonical_path = Path(inspect.getfile(canonical_module)).resolve()
    violations = []

    search_roots = [BACKEND_ROOT / "services", BACKEND_ROOT / "routers"]
    for root in search_roots:
        for py in root.rglob("*.py"):
            if py.resolve() == canonical_path:
                continue
            if "__pycache__" in str(py):
                continue

            text = py.read_text(encoding="utf-8")
            if "OutputForm" not in text or "OutputGrain" not in text:
                continue

            try:
                tree = ast.parse(text)
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if not isinstance(node, ast.Dict):
                    continue
                for key in node.keys:
                    if not isinstance(key, ast.Tuple) or len(key.elts) != 2:
                        continue
                    a, b = key.elts
                    if (isinstance(a, ast.Attribute) and isinstance(b, ast.Attribute)
                        and getattr(a.value, "id", "") == "OutputForm"
                        and getattr(b.value, "id", "") == "OutputGrain"):
                        violations.append(
                            f"{py.relative_to(BACKEND_ROOT)}:{key.lineno}: "
                            f"(OutputForm.*, OutputGrain.*) dict-key detected; "
                            f"Ruling 4 shared-derivation violated"
                        )
                        break

    assert not violations, (
        "Grain-compat rule reimplementation detected outside canonical "
        f"module {canonical_path.relative_to(BACKEND_ROOT)}. "
        "Ruling 4 shared-derivation demands single-source-of-truth for "
        "grain-form compatibility evaluation.\n" + "\n".join(violations)
    )


def test_grain_compatibility_matrix_is_exhaustive():
    """Matrix must cover ALL (OutputForm, OutputGrain) combinations.

    Missing combinations mean `evaluate_grain_form` raises KeyError on
    a valid input — a latent runtime failure. Exhaustiveness at load
    time is a schema-freeze equivalent for the rule surface.
    """
    from contracts.objective_request_v2 import OutputForm, OutputGrain
    expected = {(f, g) for f in OutputForm for g in OutputGrain}
    actual = set(canonical_module._MATRIX.keys())
    missing = expected - actual
    extra = actual - expected
    assert not missing, f"Matrix missing combinations: {missing}"
    assert not extra, f"Matrix has extra keys not in enum product: {extra}"


def test_grain_compat_path_forward_actor_appropriate():
    """Condition 3 (Phase 3): path_forward strings NEVER surface owner-side
    deliberations. Grep-negative on 4 forbidden phrases across all
    non-empty path_forward entries in the matrix."""
    forbidden = ["await owner", "owner acceptance", "ingredient manifest", "ingredient-manifest"]
    for (form, grain), result in canonical_module._MATRIX.items():
        pf = result.path_forward or ""
        pf_lower = pf.lower()
        for phrase in forbidden:
            assert phrase not in pf_lower, (
                f"({form.value}, {grain.value}) path_forward contains owner-side "
                f"deliberation phrase {phrase!r}: {pf!r}"
            )
```

---

## Section 6 — Standing conditions B1/B2/B3/B4 preserved

**B1 (verbatim from Stage A dispatch):** *"Class computed once. `conclusion_class` is Solva's assertion-boundary output. It threads to the envelope from Solva's boundary, unchanged. Any recomputation site — anywhere in `services/`, `routers/`, or the transform layer — fails review on sight. A2 `supported_class` lesson applied literally."*

**Coherence:** `ComposedConclusion_v0.conclusion_class` field description mandates threading from `services.solva_depth.assertion.conclusion_class` UNCHANGED. Module docstring dedicates full block to B1 including A2 lesson. Gate 13 (`test_composed_conclusion_class_from_solva_boundary_only`) LOAD-BEARING — AST-inspection + grep-negative on `min(u.defensibility.defensibility_class` and `min(u.defensibility_class` outside `assertion.py`. **B1 PRESERVED.**

**B2 (verbatim):** *"Standard as hard input filter lands as reason code in AdmissionRefusal@v0. The §6.1 extension surface item 3 from Phase 1's downgrade (admission-time hard-input-filter on `standard`) lands as an ADDITIONAL REASON CODE in the existing `AdmissionRefusal@v0` envelope, via the versioned registry `admission_refusal_reasons.v0.json` (bumped to v1, or appended to v0 per config policy). Zero contract touch. Zero new envelope."*

**Coherence:** Section 3 scope table §6.1.6 verdict = "COVERED (4a) + REFUSAL-VIA-ADMISSION-REGISTRY" with reason code `standard_below_admission_floor`. Section 1 file 4a.4 = `admission_refusal_reasons.v1.json` registry bump (three new reason codes total: `grain_form_incompatible`, `standard_below_admission_floor`, `license_class_unavailable`). Zero contract mutation. Gate 11 asserts snapshot byte-identical. **B2 PRESERVED.**

**B3 (verbatim):** *"Outer gate extended, not reinvented. §6.1 qualified-data export rides the EXISTING outer-gate sequence at `services/outer_gate/{transform,mint,receipt}.py` unchanged. Receipt shape (`OuterGateReceipt@v0`) unchanged. Adaptation happens INSIDE the transform layer, not by mutating gate."*

**Coherence:** Section 1 file list shows `services/outer_gate/*.py` NOT in modification list. New adaptation lives in `services/service_1/qualified_data.py` (file 4a.6) calling existing outer-gate as library. Gate 8 (`test_qualified_data_outer_gate_ride_receipt_unchanged`) SHA-invariants all three outer-gate files + `OuterGateReceipt@v0` schema. **B3 PRESERVED.**

**B4 (verbatim):** *"v0 paths byte-identical. All v0 routes and services stay byte-identical (SHA-proven). Mechanical parity invariant remains green at whatever contract count Stage B lands. Strict Rule 2 v2 §0 counting. Close-report format unchanged."*

**Coherence:** Gates 10 + 18 (`test_v0_paths_byte_identical_after_{4a,4b}`) enforce SHA-identity on `contracts/objective_request.py` (v0), `services/service_1/service.py`, `contracts/service_1_refusal.py`, `contracts/admission_refusal.py`, `services/outer_gate/*.py`. Parity stays 17 at 4a (no new frozen contract), becomes 18 at 4b (+ComposedConclusion_v0). Rule 2 v2 §0 counting inline at each Stage B close report. **B4 PRESERVED.**

**Zero HAZARD-STOP surfaced on full-text inspection.**

---

## Section 7 — §6.1 payload freeze proposal (Artifact 6)

**Payload scope:** the qualified-data export response body returned by v2 dispatch on warm-fork success for `output.form == "qualified_data"`. Specifically: the payload downstream of `services/outer_gate/transform.py::transform_artifact()` + `services/outer_gate/receipt.py::build_receipt()`.

### Candidate 1 — FROZEN `QualifiedDataArtifact_v0`

```python
from typing import List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field
from contracts.outer_gate_receipt import OuterGateReceipt


class QualifiedDataArtifact_v0(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    units: List[Dict[str, Any]] = Field(
        ..., min_length=1,
        description="Egress-transformed NormalizedUnits (pseudonymised per outer-gate)."
    )
    receipt: OuterGateReceipt = Field(
        ...,
        description="Outer-gate receipt from existing frozen contract."
    )
    unit_count: int = Field(..., ge=1)
    computed_at: str = Field(..., min_length=1)
```

Would land at 4a as 18th; parity 17→18→19 (ComposedConclusion becomes 19th at 4b).

### Candidate 2 — UNFROZEN plain dict body (RECOMMENDED)

```python
# Returned as JSONResponse body — no frozen contract:
{
    "units": [<egress_artifact['payload']>...],       # list of egress-transformed unit dicts
    "receipt": <OuterGateReceipt_v0.model_dump()>,    # already-frozen inner shape
    "unit_count": <int>,
    "computed_at": "<ISO-8601 UTC>"
}
```

No new frozen contract. Parity stays 17 at 4a; becomes 18 at 4b for ComposedConclusion only.

### D4b three-axis test applied to Candidate 1

**Axis 1 — class + trace crosses governance boundary per §12 invariant #7:**
Each unit in `units` is an egress-transformed `NormalizedUnit`. `NormalizedUnit` is a frozen contract; Ring 5 defensibility class is already an inline field per its schema; class + trace already travel INLINE within each unit's shape. The container `QualifiedDataArtifact_v0` adds no additional class-carrying field beyond what's already inside `units`. **Axis 1 argument WEAKENS for Candidate 1** — governance semantic rides on inner frozen shape (`NormalizedUnit`), not on container.

**Axis 2 — downstream Phase 5 async wrapper binds it:**
Phase 5's async terminal for `form=qualified_data` returns the export payload. If frozen (Candidate 1), Phase 5's wrapper freezes cleanly around frozen inner. If unfrozen (Candidate 2), Phase 5's wrapper CAN still be frozen if its schema is `payload: Dict[str, Any]` — but then Phase 5 loses structural binding for `form=qualified_data` payloads. **Axis 2 argument MODERATELY-STRONG for Candidate 1** — freezing gives Phase 5 structural binding. Also-defensible under Candidate 2 with `Dict[str, Any]` at async wrapper, at cost of looser binding.

**Axis 3 — wire-shape guarantee required:**
Callers of `POST /api/service_1/v2/dispatch` for `form=qualified_data`: buyer integrations expect stable response body. Under Candidate 2, container shape is stable-by-service-convention (doesn't drift for reasons unrelated to units), and each unit's shape is stable by `NormalizedUnit` freeze. Under Candidate 1, container is stable-by-freeze — one more surface. **Axis 3 argument MODERATE for Candidate 1** — substantive wire-shape (unit content, receipt content) already stable by inner freezes.

**Overall D4b assessment:** the three axes are WEAKER for Candidate 1 than they were for ComposedConclusion_v0. Container is more scaffolding than governance; substantive governance rides on `NormalizedUnit` + `OuterGateReceipt_v0` (already frozen).

### Verdict: Candidate 2 UNFROZEN (RECOMMENDED)

**Doctrinal justification:**

1. **Mechanism-not-values pattern (Ruling 3 precedent):** §6.1 payload container is a MECHANISM (packaging + delivery); VALUES (each unit's class + provenance + trace_id) live in already-frozen inner contracts. Freeze the values, not the mechanism.

2. **D4b bar not met.** Three-axis test above: (i) class+trace crosses AT UNIT LEVEL, not container. (ii) Phase 5 can bind loosely for `form=qualified_data` without losing governance because governance is inside units. (iii) Substantive shape stable via inner freezes; container is scaffolding.

3. **Precedent — `DispatchResult` at Phase 2.** Phase 2 landed `DispatchResult` UNFROZEN under same reasoning — internal-orchestration shape, not governance-critical the way `FeasibilityResult_v0` is. §6.1 payload is analogous: transport-layer container of already-governed inner content.

4. **Snapshot count discipline:** freezing every wire-shape produces ratchet effect — the correct ratchet is at governance-crossing shapes (Phase 3 AdmissionRefusal_v0; Phase 4b ComposedConclusion_v0; Phase 5 async terminal). Adding a fourth freeze at §6.1 container diverges from "freeze governance, not orchestration".

**Doctrinally necessary?** NO. Would-be-cleaner if owner wants wire-shape ratchet at every transform-output — legitimate posture — but not required by D4b bar. Owner rules.

---

## Section 8 — Continuity update

### Corrected `ORCHESTRATOR_CONTINUITY.md §2` phase-ledger entry (verbatim as landed):

| **Phase 4 Stage A — Transform Layer design proposals (design-only, no implementation)** | **CLOSED** | **413** (unchanged; docs-only touch) | N/A (design-only) | N/A (design-only; Stage B does the LoC accounting) | N/A | 2026-07-03 — INITIAL CLOSE VACATED: first close was verdict-summary only, not the artifact-delivery Stage A dispatch required. Second close (same day) delivered Sections 1–8 with full-text artifacts landed at `/app/docs/stage_a_proposals/phase_4_stage_a.md`: §6.1 payload freeze proposal (Artifact 6, NEW Section 7), ComposedConclusion_v0 full schema + three D4b axes argued verbatim (Artifact 1), license_class three-option comparison A/B/C + Option C concrete (Artifact 2), full grain_compatibility.py pure-function module + guard test (Artifact 3), 4a/4b file-by-file split with concrete import lines (Artifact 4), full scope table with v3 line-anchored dispositions + two counter-verdicts (Artifact 5), B1–B4 honesty recheck post-full-text inspection. Verdicts: 4a/4b SPLIT (XL ~1310 net-new); ComposedConclusion@v0 FREEZE (18th, at 4b); §6.1 payload UNFROZEN at 4a (D4b bar not met — container of already-frozen inner shapes). No Standing Owner Disposition changes. Substrate-drop gate 9/9 GREEN. CI 413/413 GREEN. Parity 17 entries. Owner rules on Stage A shape + split before Stage B dispatch. |

### `PHASE_STATE.md` mirror entry (verbatim as landed):

| **Phase 4 Stage A — Transform Layer design proposals (design-only)** | **CLOSED** | **413** (unchanged; docs-only) — initial verdict-summary close vacated same-day; full-text artifacts delivered 2026-07-03 on owner request | N/A | N/A (Stage B does LoC accounting) | N/A |

---

**On-disk landing:** `/app/docs/stage_a_proposals/phase_4_stage_a.md` (this file).
**Substrate:** design-only; zero code files under `/app/backend/`; docs-only.
**CI at close:** 413/413 GREEN; `make ci` PASSED; parity 17; substrate-drop 9/9 GREEN.

Stage B held pending owner rulings on eight items:
1. 4a/4b split acceptance
2. `ComposedConclusion_v0` FREEZE + three D4b axes
3. §6.1 payload freeze verdict (Candidate 1 vs 2)
4. `license_class` Option B vs C
5. Grain-compat artifact form (pure-function vs hybrid)
6. Counter-verdicts (Option C sidestep; §6.1 payload UNFROZEN)
7. Shared vs proliferated grain reason codes (`grain_form_incompatible` unified vs per-cell)
8. Illustrative license class names (accept as-such or replace)
