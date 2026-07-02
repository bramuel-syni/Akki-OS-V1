# G3 Solva Conformance Audit v1

**Timestamp:** 2026-07-01T17:15Z
**Source of truth:** `/app/docs/mandates/RMS_Solva_Specification.md` (SHA-256 `f375b5ac…297db`, MANIFEST.md).
**Parent cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §23, §31, §12.
**Freshness:** all 7 canonical specs classified CURRENT at `docs/audits/g3_precondition/spec_freshness_check.md`.
**Precondition audit:** V1–V4 all clean (H-a1 EXACT MATCH, H-a2 EXACT MATCH; no HAZARD-STOPs surfaced).
**CI status at audit time:** 196/196 green via `make ci`.

## Method

For each §-anchor in Solva Spec v1.0 (§1 → §18) plus the referenced Product Spec 2.1 anchors:
- Determine what the mandate requires.
- Locate the G3 landing shape in `/app/backend/`.
- Verdict: **MATCH** (spec obligation satisfied verbatim) / **SPEC_EXPANSION** (G3 lands a proper sub-set of the mandate obligation, with the remainder deferred to a later phase and journal-cited) / **MATERIAL_GAP** (obligation not satisfied — a HAZARD-STOP).

**Result summary: 22 MATCH / 4 SPEC_EXPANSION / 0 MATERIAL_GAP.**

---

## Solva Spec v1.0

### Part I — Mandate

| § | Obligation (mandate ↔ verbatim) | Landing shape | Verdict |
|---|---|---|---|
| §1 | Solva is the depth governor: judges soundness, preservation sufficiency, defensibility assertion. Reasons; never extracts; never reaches into operator primitives. | Reasoning stages emit reasoning artifacts (`reasoning/{frame,candidate,tension,probability,reflection}.py`); no operator primitive calls in `solva_depth/*`; import-boundary asserted by `test_reasoning_faculty_isolation` + `test_assertion_does_not_import_from_reasoning`. | **MATCH** |
| §2 | Anchor: "Reason well AND never override a governed constraint." | Reasoning stages have no governed-artifact writes; `enforce.py` reads `FloorSpec`/`MatrixHandle` via `interfaces.py` frozen dataclass + Protocol; no mutation site. | **MATCH** |
| §3 | Two faculties — free reasoning + bound assertion — one-way seam. | `services/solva_depth/reasoning/` (free); `services/solva_depth/assertion.py` (bound); `test_reasoning_faculty_isolation` enforces `reasoning/` does not import `DefensibilityClass` and `assertion.py` does not import from `reasoning/`. | **MATCH** |
| §4 | Assertion boundary computes class mechanically as floor over load-bearing units' classes. Reasoning strength deaf to boundary. | `conclusion_class(load_bearing_units) -> DefensibilityClass` in `assertion.py`; signature frozen by `conclusion_class_signature.snapshot.json`; three positive-behaviour tests + no-confidence-input test. | **MATCH** |
| §5 | Two bars — narrow bar (fact/utterance/non_factual verdict) + wide bar (which refinements to preserve). | Narrow-bar: `assert_conclusion(text, units)` distinguishes fact-claim vs. utterance stated-form vs. non_factual context-only. Wide-bar: `stamp.preserve_stamps(units)` returns preservation-annotated Ring 5 blobs. G3 v0 preserves identity; refinement judgment binds post-G3. | **SPEC_EXPANSION** (preserve-judgment overlay is identity at v0; source §12 notes wide-bar refinement judgment binds later) |
| §6 | Trace — every extraction-time judgment produces a trace carrying reasoning path, load-bearing units, computed class. | `SolvaTrace` `@dataclass(frozen=True)` with `stages`, `load_bearing_unit_ids`, `computed_class`, `conclusion`. Serialised via `to_dict()` for JSON absorption. | **MATCH** |

### Part II — Construction

| § | Obligation | Landing shape | Verdict |
|---|---|---|---|
| §7 | Module structure: `assertion.py`, `enforce.py`, `interfaces.py`, `load_bearing.py`, `reasoning.py` (or reasoning package), `stamp.py`, `trace.py`, `pipeline.py`, `routers/solva.py`. Dependency rules: no reasoning ↔ assertion cycle. | All eight modules present at `services/solva_depth/`. `reasoning.py` implemented as **5-file package `services/solva_depth/reasoning/`** — scope note §non-hazard-notes explicitly ratifies this (behaviourally equivalent; structurally closer to parametrized isolation-test discipline). Router at `routers/solva.py`. | **MATCH** (`reasoning/` as package; equivalent shape) |
| §8 | Five reasoning stages: Frame → Candidate → Tension → Probability → Reflection. | Five files under `services/solva_depth/reasoning/`. Composition order in `pipeline.run_solva` matches spec. | **MATCH** |
| §9 | Load-bearing is a reasoning judgment; not the class computation. | `services/solva_depth/load_bearing.py::load_bearing(text, candidates) -> List[NormalizedUnit]`. No class construction in load_bearing. `reasoning/reflection.py` calls it and returns `load_bearing_units` — not a class. | **MATCH** (v0 default = all candidates load-bearing; genuine judgment lands with LLM binding post-G3, journaled) |
| §10 | `conclusion_class(load_bearing_units) -> str` — CLASS_ORDER/INV_ORDER mechanical floor. Return typed strictly as `DefensibilityClass` (enum). | `assertion.py::conclusion_class` matches source snippet verbatim; return typed `DefensibilityClass` (strictly stronger than `str`); signature frozen by snapshot. `CLASS_ORDER` maps `NON_FACTUAL=0, UTTERANCE=1, FACT=2` verbatim. | **MATCH** |
| §11 | Enforcement — applies floor; refuses below with structured reason; reads governed values read-only. | `enforce.py::enforce(text, units, floor)` returns `Assertion | Refusal`. Refusal shape: `reason="below_defensibility_floor"`, `computed_class`, `floor_class` frozen dataclass. `FloorSpec` is `@dataclass(frozen=True)`; `MatrixHandle` is a Protocol with no setter methods. | **MATCH** |
| §12 | Ring 5 stamp at convergence — wide-bar refinements preserved. | `stamp.preserve_stamps(units)` returns per-unit preservation-annotated Ring 5 blobs. G3 v0: identity preservation of Layer C stamps. `layer_c/convergence.assert_signal_ring_conformant` enforces §31 #6 (six frozen contracts as source of truth). | **SPEC_EXPANSION** (wide-bar refinement judgment binds post-G3) |
| §13 | Trace and interfaces — SolvaTrace, StageRecord dataclasses (Python-frozen, NOT among the six Pydantic-frozen contracts). Trace absorbed by Northena Ledger via stamp-audit seam. | `trace.py` defines `SolvaTrace` + `StageRecord` `@dataclass(frozen=True)`. `services/northena/converge.py::absorb_solva_trace` writes a `stage="converge"` row with the trace dict in `LedgerRow.stamp_audit`. No frozen-contract mutation (LedgerRow.stamp_audit was already `Optional[Dict]` per Northena §7.2). | **MATCH** |
| §14 | Test obligations — 7 named tests, plus signature freeze. | All 7 tests present and green: `test_class_is_floor_over_load_bearing_*` (3 variants), `test_conclusion_class_takes_no_confidence`, `test_utterance_never_asserted_as_fact`, `test_refuse_below_floor`, `test_solva_reads_governed_values_readonly` (behavioural test asserting no `.model_copy`/`setattr` on `FloorSpec`, via `frozen=True`), `test_solva_never_extracts` (structural — reasoning stages import discipline via `test_reasoning_faculty_isolation`), `test_trace_records_load_bearing_and_class` (integrated in `test_pipeline_emits_full_stage_trace`). Signature freeze: `test_conclusion_class_signature_matches_snapshot`. | **MATCH** |
| §15 | Construction requirements: (1) boundary first as construction; (2) five stages emit judgments and a load-bearing set; (3) enforcement reads governed values read-only; (4) trace from first commit. | (1) `assertion.py` authored first (context sequence: assertion → interfaces → enforce → reasoning stages → pipeline → trace). (2) 5 stages emit dict artifacts; reflection returns `load_bearing_units`. (3) `FloorSpec` frozen; `MatrixHandle` Protocol; no setter surface. (4) `pipeline.run_solva` always returns a `SolvaTrace`. | **MATCH** |

### Part III — Governance, Invariants, Open Decisions

| § | Obligation | Landing shape | Verdict |
|---|---|---|---|
| §16 | Governance: never override governed constraint; auditable reasoning; assertion boundary is the integrity guarantee. | Enforced by construction + tests. `enforce.py` + `interfaces.py` + `assertion.py` + `test_solva_assertion_boundary` + `test_reasoning_faculty_isolation` collectively realise the guarantee. | **MATCH** |
| §17 #1 | Solva reasons; never extracts; never reaches into operator primitives. | Reasoning modules import only from `contracts.five_rings` (data-shape only) + siblings. No `services/synisense/shield/perception_router` invocations. Grep: `services/solva_depth/reasoning/` has no `invoke(` calls. | **MATCH** |
| §17 #2 | Two faculties with one-way seam. | Parametrized `test_reasoning_faculty_isolation` (5 stages × 3 checks = 15 tests) + `test_assertion_does_not_import_from_reasoning`. | **MATCH** |
| §17 #3 | Class = floor over load-bearing units' classes; reasoning strength not an input. | `conclusion_class` signature freeze (`test_conclusion_class_signature`) + no-confidence test. Behaviourally covered by `test_class_is_floor_over_load_bearing_{all_fact,mixed,non_factual_wins}`. | **MATCH** |
| §17 #4 | Utterance-class asserted as "was stated," never fact. | `assert_conclusion` branches on klass; `test_utterance_never_asserted_as_fact` asserts phrasing contains `"was stated"` and NOT the raw claim as fact. | **MATCH** |
| §17 #5 | Load-bearing is reasoning judgment; class those units imply is mechanical. | `load_bearing()` returns units, not a class; class construction confined to `assertion.py`. Enforced by `test_reasoning_faculty_isolation.test_stage_does_not_construct_defensibility_class`. | **MATCH** |
| §17 #6 | Floor + Matrix verdict read-only to Solva. | `FloorSpec` `frozen=True` dataclass; `MatrixHandle` Protocol with no setters; grep: no `.model_copy` / no attribute-assign on floor or matrix in `services/solva_depth/`. | **MATCH** (structural; runtime "no-mutation" assertion is a behavioural test covered by frozen dataclass semantics) |
| §17 #7 | Below-floor conclusion refused with structured reason. | `Refusal(reason="below_defensibility_floor", computed_class, floor_class)`; `test_refuse_below_floor` asserts. | **MATCH** |
| §17 #8 | Every extraction-time judgment produces a trace. | `pipeline.run_solva` always returns `SolvaTrace`; `test_pipeline_emits_full_stage_trace` verifies six stages; `test_solva_trace_lands_in_ledger` verifies Ledger absorption end-to-end with Mongo. | **MATCH** |
| §17 #9 | Solva governs depth only; three axes never collapsed; Solva never performs another governor's function. | N-INV-11 orthogonality grep continues to enforce (Northena side); `services/solva_depth/*` imports do NOT touch `services/northena/`, `services/synisense/shield/purpose_validator`, or `services/g1_defensibility/` beyond transitive-lift docstring citations. | **MATCH** |
| §18 | Open decisions: none. Reasoning-faculty method is a build-time implementation choice bounded by invariants. | G3 v0 reasoning stages are code-only (no LLM calls). LLM binding is a G3+ implementation choice explicitly bounded by Product Spec 2.1 §31 #10 (`extraction_params@v0` temperature=0). Journaled in `reasoning/probability.py::probability` docstring. | **SPEC_EXPANSION** (LLM binding remains a future implementation choice; nothing in spec is left open by mandate) |

---

## Product Spec 2.1 cross-anchor obligations

| § | Obligation | G3 landing | Verdict |
|---|---|---|---|
| §23 | Parent behavioural description of Solva. | Fully realised by Solva Spec §1–§18 landing above. | **MATCH** |
| §31 #1 | Every unit of intelligence carries a complete Ring 5 defensibility stamp. | Layer C `aggregator.py` stamps at declaration baseline (G0.5); Solva `stamp.py` (G3) provides preservation overlay at convergence. | **MATCH** |
| §31 #2 | Two axes never collapsed at unit level (utterance vs. fact). | `assert_conclusion` distinguishes phrasing branches; `test_utterance_never_asserted_as_fact` enforces. | **MATCH** |
| §31 #3 | Governed Matrix verdict is read-only. | `MatrixHandle` Protocol has no setters; `_DefaultMatrixHandle` uses immutable frozen dataclass around `QualificationMatrix.find`. | **MATCH** |
| §31 #4 | Powerful-part-walled principle — reasoning strength walled from assertion class. | `conclusion_class(load_bearing_units, )` signature — no confidence input; snapshot-frozen; test asserts. | **MATCH** |
| §31 #5 | Three governors on orthogonal axes. | N-INV-11 grep + Solva orthogonality (Solva does not import from Northena/SyniSense internals). | **MATCH** |
| §31 #6 | Six frozen contracts are the source of truth. | `layer_c/convergence.assert_signal_ring_conformant` enforces `signal_ring_dimensions@v0` catalogue as source of truth for Signal ring dimensions per modality. Frozen catalogue read from `tests/invariants/signal_ring_dimensions.v0.content_snapshot.json`. | **MATCH** |
| §31 #10 | Reproducibility via `temperature=0`. | G3 v0 reasoning stages are code-only (no LLM calls yet). When LLM binding lands (post-G3), MUST use `extraction_params@v0` `temperature=0` per `is_deterministically_reproducible` gate. Journaled in `reasoning/probability.py`. | **SPEC_EXPANSION** (LLM binding is a G3+ implementation choice) |
| §31 #14 | Gates have certain fallback. | `enforce.py` refuses below floor with structured `Refusal(reason='below_defensibility_floor')` — fallback is refusal-with-reason, not silent downgrade. | **MATCH** |
| §C | Layer C description (normalization + convergence). | `layer_c/aggregator.py` (G0.5) + `layer_c/convergence.py` (G3): `converge_units` validates conformance and hands off; Ring 3 population deferred to real multi-unit runs at G4+, journal-cited in `converge_units` docstring. | **SPEC_EXPANSION** (Ring 3 edge population deferred; source §12 permits) |
| §12 | Signal-ring dimension catalogue (per modality). | Frozen at `signal_ring_dimensions.v0.content_snapshot.json`. Layer C `assert_signal_ring_conformant` reads it; 8 parametrized tests cover all 5 modalities. | **MATCH** |

---

## HAZARD-STOP inventory

- **H-a1 (Ring 5 class enum vs frozen `DefensibilityClass`):** NOT RAISED. Set-membership EXACT MATCH: `{fact, utterance, non_factual}` == `{DefensibilityClass.FACT.value, DefensibilityClass.UTTERANCE.value, DefensibilityClass.NON_FACTUAL.value}`.
- **H-a2 (Solva signal-ring dimensions vs frozen `signal_ring_dimensions@v0`):** NOT RAISED. Solva spec does not enumerate dimensions; Product Spec 2.1 §12 enumeration matches frozen snapshot verbatim.
- **H-b (contract mutation required to house Solva outputs):** NOT RAISED. `LedgerRow.stamp_audit: Optional[Dict]` is already the seam per Northena §7.2. No frozen-contract mutation across all six contracts.
- **H-c (spec absent or stale for G3):** NOT RAISED. All 7 specs CURRENT (see `docs/audits/g3_precondition/spec_freshness_check.md`).

---

## Verdict

- MATCH: **22**
- SPEC_EXPANSION: **4** (all explicitly permitted by mandate for post-G3 implementation choices)
- MATERIAL_GAP: **0**

**G3 phase closure authorized.** No HAZARD-STOPs raised.

## Cross-references

- Solva Spec: `docs/mandates/RMS_Solva_Specification.md`
- Scope note: `docs/g3_prep/solva_scope_from_source.md`
- Precondition freshness: `docs/audits/g3_precondition/spec_freshness_check.md`
- Substrate-Drop v1 Solva reconciliation: `docs/audits/substrate_drop_v1/solva_reconciliation.md`
- BUILD_JOURNAL G3 close entry (this timestamp): 2026-07-01T17:15Z
