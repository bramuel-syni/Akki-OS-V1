# PHASE_STATE (compact mirror of ORCHESTRATOR_CONTINUITY §2 + §3)

**Last update:** 2026-07-04 (Phase 4a Stage B close — §6.1 qualified-data path landed + shared substrates, zero freezes at 4a)

> Any duration / credit / turn number referenced below is a **Provisional planning anchor — not a commitment. Relative weight only.**

## Live State
- **Current gate:** **PHASE 4a STAGE B CLOSED** (2026-07-04) — §6.1 qualified-data path landed live at v2 dispatch (warm+qualified_data → 200 with UNFROZEN `QualifiedDataPayload` container + inner-frozen `OuterGateReceipt_v0`). Shared substrates landed: grain-compat single-source-of-truth (`services/service_1/grain_compatibility.py`, Ruling 4 shared-derivation), license-class Ruling-4 shared-derivation (`services/service_1/license_class_selection.py`, Phase 7 seam pre-committed in docstring per Ruling 4), `license_classes.v0.json` config (Ruling 8 illustrative-taxonomy governance). Admission-refusal reason registry bumped v0→v1 additively (Ruling 3): 3 new reason codes (`grain_form_incompatible`, `standard_below_admission_floor`, `license_class_unavailable`). Ruling 5 MODEL-cell defense-in-depth landed. Ruling 3 wire-shape gate (LOAD-BEARING) landed. **Phase 3 CLOSED. Phase 2 CLOSED. Substrate-Drop v2 CLOSED. Phase 0 CLOSED. Phase 1 CLOSED. G5b CLOSED.** Backend surface FROZEN except additive-only Phase 4a landing (no v0 mutations; no v0 SHA drift on 7 protected files; no `Service1Refusal` mutation; no `AdmissionRefusal_v0` contract snapshot mutation; no `ObjectiveRequest_v2` mutation; zero new freezes — parity stays 17).
- **Counting standard:** post-§0-strict from G6 forward.
- **Standing Owner Dispositions in force** (see ORCHESTRATOR_CONTINUITY §0.1): Ruling 2 (literal-widening HAZARD), Ruling 4 (§10 uniform disposition), Ruling 5 (§6.3/§6.4 confirmed as written), Elevated Doctrine (validation surface IS contract surface), Loose-as-frozen (deliberate under-determination is not a HAZARD), **Ruling 4 shared-derivation (floor_feasibility + grain-compat + license-class-selection — three functions, N consumers each)**, **Ruling 3 config-as-versioned-not-frozen (feasibility-config@vN + admission-refusal-reasons@vN + license-classes@vN control-surface pattern)**, **Ruling 1 (Item 4 supersede)**, **Admission-refusal reasons extend via versioned registry (Phase 3 dispatch, 2026-07-03)**, **§6.1 payload UNFROZEN by named wire-shape gate (Ruling 3, Phase 4a Stage B dispatch, 2026-07-03)**, **License-class Phase 7 seam pre-committed in module docstring (Ruling 4, Phase 4a Stage B dispatch, 2026-07-03)**.
- **Plan Debts (see ORCHESTRATOR_CONTINUITY §0.2):** ~~§6.1 downgrade plan-debt~~ **RESOLVED at Phase 4a Stage B close, 2026-07-04**; ~~Phase 3 model-refusal debt~~ **RESOLVED at Phase 3 close, 2026-07-03**; **Phase 4b transform-variants debt REMAINING** (§6.2 composed_conclusion + 18th frozen contract `ComposedConclusion_v0` — Ruling 2 confirmed); Phase 5 async-delivery debt; Phase 7 wizard-side dispatch debt (+ Phase 7 additional receiver debt: wizard-side rendering of `AdmissionRefusal@v0` as REFUSAL-WITH-PATH per UI Spec §3.3 + License-class Phase-7-seam wrap unchanged from pre-commit).
- **Phase 4a Stage B CLOSED (2026-07-04):** 8 source files (5 NEW + 3 MODIFIED: `services/service_1/grain_compatibility.py`, `services/service_1/license_classes.v0.json`, `services/service_1/license_class_selection.py`, `services/service_1/admission_refusal_reasons.v1.json`, `services/service_1/qualified_data.py`, MODIFIED: `services/service_1/admission_refusal.py` +171/-9, `services/service_1/dispatch.py` +73/-31, `routers/service_1.py` +31/-10) + 6 test files (all NEW, houses 12 gates + 3 Ruling fold-ins) + 1 Phase-2 test migration (`test_dispatch_shape_responsive.py::test_positive_external_request_warm_fork_populated_registry` +30/-17, Condition-5 migration: warm+qualified_data now returns `QualifiedDataPayload`). Full CI: 413 → 434 (+21 tests). Substrate-drop 9/9 GREEN. Mechanical parity 3/3 GREEN at 17 (unchanged).
- **Awaiting:** owner directive on Phase 4b dispatch (§6.2 composed_conclusion + 18th frozen contract) OR Phase 5 async-delivery.
- **Last green CI:** 434/434 backend at 2026-07-04 (+ 18/18 frontend gate tests unchanged from G5b). Substrate-drop gate 9/9 green. Mechanical parity invariant 3/3 green at 17 entries.
- **Data source posture:** SYNTHETIC v1 = standing test substrate (permanent); real material = operational/benchmark input; no supersede semantics between them (Ruling 1, 2026-07-03).
- **Canonical specs on-disk:** 7/7 CURRENT.
- **Frozen contracts:** 17 (unchanged from Phase 3 — Phase 4a Stage B lands ZERO new freezes per Owner dispatch invariant; 18th `ComposedConclusion_v0` deferred to 4b per Ruling 2). All 17 have canonical `.contract_snapshot.json` files; mechanical parity invariant enforces bijection.
- **Closed seams (5):** `mtafiti_v3_overlay`, `targeta_yield_layer`, `northena_ledger_deletion`, `v2_cumulative_disclosure_arm`, **`§6.1_payload_freeze` (Phase 4a Stage B, 2026-07-04 — UNFROZEN by named wire-shape gate per Ruling 3)**. All grep-verified intact post-Phase-4a-Stage-B.
- **Rule 2 accounting version:** v2 + §0 discretionary-enumeration-inline discipline.
- **Discipline observations tracked separately:** X1 — `solva_depth/pipeline.py` code fix is LIVE + test-defended.
- **Open HAZARD-STOP flags:** 0.

## Phase Ledger
| Phase | Status | Green @ close | Lifted (verifiable) | Net-new | Ratio (v2) |
|---|---|---|---|---|---|
| G0 | CLOSED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| G0.5 | CLOSED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| G1 | CLOSED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Pre-G2 | CLOSED | 61 | UNKNOWN | UNKNOWN | UNKNOWN |
| G2a | CLOSED | 73 initial → 149 rolling | 127 (all transitive) | 344 | 2.71× overall / 1.34× discretionary |
| Substrate-Drop v1 | CLOSED | 158 | 0 (docs+CI phase) | 0 | N/A |
| G3 | CLOSED | 211 | 98 | 437 | 4.46× overall / ~0.02× discretionary |
| G4 | CLOSED | 271 | 268 | 785 | 2.93× overall / 0.00× discretionary |
| G5a | CLOSED | 301 | 159 | 715 | 4.50× overall / 0.11× discretionary |
| G6 | CLOSED | 340 | 80 | 1176 | 14.70× overall / 0.80× discretionary |
| Handoff-Download Route | CLOSED | 347 | 12 | 30 | 1.00× discretionary-only |
| A2 (Service1Refusal envelope) | CLOSED | 355 | 20 | ~50 | ~1.27× discretionary-only |
| G5b | CLOSED | 359 backend + 12/12 frontend gate | 0 (API-consumption) | 1848 (all discretionary) | N/A (no source lift) |
| Docs-Pass (Source-Spec Corrections) | CLOSED | 367 | 0 (docs) | 0 | N/A |
| Substrate-Drop v2 (Part 1) | CLOSED | 373 (+6) | 0 (docs+CI; backfill by-copy) | 0 | N/A |
| Substrate-Drop v2 (Part 2 / Phase 0) | CLOSED | 374 (+1) | 0 (net-new contract) | ~180 | ~12× overall / ~0.08× discretionary-only |
| Phase 1 — Estate Feasibility Query | CLOSED | 387 (+13) | ~30 | ~490 | ~5.7× overall / ~0.30× discretionary-only |
| Phase 2 — Shape-Responsive Execution Scaffold | CLOSED | 402 (+15) | ~40 | ~460 | ~4.2× overall / ~0.24× discretionary-only |
| Phase 3 — Admission-Refusal Envelope (unified §6.5 + future admission reasons via registry) | CLOSED | 413 (+11) | ~35 | ~470 | ~13.4× overall / ~0.19× discretionary-only |
| Phase 4 Stage A — Transform Layer design proposals (design-only) | CLOSED | 413 (unchanged; docs-only) — initial verdict-summary close vacated same-day; full-text artifacts delivered 2026-07-03 on owner request | N/A | N/A (Stage B does LoC accounting) | N/A |
| **Phase 4a Stage B — §6.1 qualified-data path + shared substrates (grain-compat, license-class-selection, license-classes.v0.json, admission-refusal-reasons.v1.json, qualified_data.py; zero freezes at 4a; 3 rulings landed: R3 wire-shape gate, R4 Phase-7 seam docstring, R5 MODEL-cell defense-in-depth). Delivery-history note: inline close did not reach owner thread on first attempt (relay-channel content drop); re-emitted on owner request with three specific artifacts + on-disk canonical `/app/docs/close_reports/phase_4a_stage_b.md` SHA-256 `f5bb38e7d25b3e295bb38aec24bf6e46404bb164ab0b9a5cd639c451234eb866`.** | **CLOSED** | **434 (+21)** | ~120 (feasibility read + outer_gate transform/receipt reuse; floor_feasibility import; admission_refusal.emit_form_not_offerable shape lift) | ~840 (against ~950 band; -12% delta under) | ~7× overall / ~0.30× discretionary-only |
| G2b | BLOCKED (real RMS material) | — | — | — | — |

## Pending Decisions
- [x] ~~Substrate-Drop v2 Part 1?~~ — CLOSED at 2026-07-03.
- [x] ~~Substrate-Drop v2 Part 2 (Phase 0)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 1 (Estate Feasibility Query)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 2 (Shape-Responsive Execution Scaffold)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 3 (Admission-Refusal Envelope — unified §6.5 + future admission reasons via registry)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 4 Stage A (design proposals)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 4a Stage B (§6.1 qualified-data path + shared substrates)?~~ — CLOSED at 2026-07-04.
- [x] ~~Item 4 HAZARD-STOP (fixture-supersede posture)?~~ — RESOLVED at 2026-07-03 per Ruling 1.
- [ ] Owner directive on which next phase to dispatch (Phase 4b transform variants §6.2 + 18th frozen contract `ComposedConclusion_v0`, Phase 5 async delivery, Phase 6 economics, Phase 7 wizards, Phase 8 frontend).
- [ ] Real RMS material for G2b
- [ ] Owner thresholds — Targeta yield seam
- [ ] Owner + DPO thresholds — Mtafiti V3 overlay seam
- [ ] DPO — Northena Ledger retention window
- [ ] DPO — V2 cumulative-disclosure arm env vars
- [ ] MEA — real source-standing table
- [ ] Owner narrowing on `ObjectiveRequest_v2` HAZARD-STOP-NOTE fields (`Reach.depth`, `Envelope.budget`, `Envelope.scope_ceiling`) — future frozen-contract additions when owner rules on scalar types
