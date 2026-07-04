# PHASE_STATE (compact mirror of ORCHESTRATOR_CONTINUITY §2 + §3)

**Last update:** 2026-07-03 (Phase 3 close — Admission-Refusal Envelope unified §6.5 + future admission reasons via registry)

> Any duration / credit / turn number referenced below is a **Provisional planning anchor — not a commitment. Relative weight only.**

## Live State
- **Current gate:** **PHASE 3 CLOSED** (2026-07-03) — unified admission-refusal envelope `AdmissionRefusal@v0` landed as 17th frozen contract. Phase 2 CLOSED. Substrate-Drop v2 CLOSED. Phase 0 CLOSED. Phase 1 CLOSED. G5b remains CLOSED. Backend surface FROZEN except additive-only Phase 3 landing (new 17th contract + new service module + v2 dispatch integration + versioned reason registry; no v0 mutations; no `Service1Refusal` mutation; no `ObjectiveRequest_v2` mutation).
- **Counting standard:** post-§0-strict from G6 forward.
- **Standing Owner Dispositions in force** (see ORCHESTRATOR_CONTINUITY §0.1): Ruling 2 (literal-widening HAZARD), Ruling 4 (§10 uniform disposition), Ruling 5 (§6.3/§6.4 confirmed as written), Elevated Doctrine (validation surface IS contract surface), Loose-as-frozen (deliberate under-determination is not a HAZARD), **Ruling 4 shared-derivation (floor_feasibility one function two consumers)**, **Ruling 3 config-as-versioned-not-frozen (feasibility-config@vN control-surface pattern)**, **Ruling 1 (Item 4 supersede)**, **Admission-refusal reasons extend via versioned registry (Phase 3 dispatch, 2026-07-03)**.
- **Plan Debts (see ORCHESTRATOR_CONTINUITY §0.2):** §6.1 downgrade plan-debt; ~~Phase 3 model-refusal debt~~ **RESOLVED at Phase 3 close, 2026-07-03**; **Phase 4 transform-variants debt RESTATED as net-of-refusal-work** (Phase 4 §6.1 hard-input-filter refusal now lands as ADDITIONAL REASON CODE in `AdmissionRefusal@v0` via registry bump, NOT new contract); Phase 5 async-delivery debt; Phase 7 wizard-side dispatch debt (+ Phase 7 additional receiver debt: wizard-side rendering of `AdmissionRefusal@v0` as REFUSAL-WITH-PATH per UI Spec §3.3).
- **Phase 3 CLOSED (2026-07-03):** `contracts/admission_refusal.py` (17th frozen contract) + `services/service_1/admission_refusal_reasons.v0.json` (versioned registry, Ruling 3 pattern) + `services/service_1/admission_refusal.py` (registry validator + form_not_offerable emitter) + dispatch integration (Union[DispatchResult, AdmissionRefusal_v0]) + additive-only router branch (422 for refusal, 501 for placeholder); mechanical parity invariant map bumped 16→17; NEW Standing Owner Disposition landed at §0.1 (admission-refusal reasons extend via versioned registry, never Literal-widening); Phase 2 `form=model` scaffold placeholder REPLACED by `AdmissionRefusal_v0` @422 (Condition 5 migration). Full CI: 402 → 413 (+11 Phase 3 tests + 2 Phase-2 test migrations).
- **Awaiting:** user directive on which post-Phase-3 phase to dispatch (Phase 4 transform variants restated net-of-refusal-work, Phase 5 async delivery, Phase 6 economics, Phase 7 wizards, Phase 8 frontend).
- **Last green CI:** 413/413 backend at 2026-07-03 (+ 18/18 frontend gate tests unchanged from G5b). Substrate-drop gate 9/9 green. Mechanical parity invariant 3/3 green at 17 entries.
- **Data source posture:** SYNTHETIC v1 = standing test substrate (permanent); real material = operational/benchmark input; no supersede semantics between them (Ruling 1, 2026-07-03).
- **Canonical specs on-disk:** 7/7 CURRENT.
- **Frozen contracts:** 17 (was 16 at Phase 2 close; +1 `AdmissionRefusal_v0`). All 17 have canonical `.contract_snapshot.json` files; mechanical parity invariant enforces bijection.
- **Closed seams (4):** unchanged — `mtafiti_v3_overlay`, `targeta_yield_layer`, `northena_ledger_deletion`, `v2_cumulative_disclosure_arm`. All grep-verified intact post-Phase-3.
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
| **Phase 4 Stage A — Transform Layer design proposals (design-only)** | **CLOSED** | **413** (unchanged; docs-only) | N/A | N/A (Stage B does LoC accounting) | N/A |
| G2b | BLOCKED (real RMS material) | — | — | — | — |

## Pending Decisions
- [x] ~~Substrate-Drop v2 Part 1?~~ — CLOSED at 2026-07-03.
- [x] ~~Substrate-Drop v2 Part 2 (Phase 0)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 1 (Estate Feasibility Query)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 2 (Shape-Responsive Execution Scaffold)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 3 (Admission-Refusal Envelope — unified §6.5 + future admission reasons via registry)?~~ — CLOSED at 2026-07-03.
- [x] ~~Item 4 HAZARD-STOP (fixture-supersede posture)?~~ — RESOLVED at 2026-07-03 per Ruling 1.
- [ ] User directive on which post-Phase-3 phase to dispatch (Phase 4 transform variants restated net-of-refusal-work, Phase 5 async delivery, Phase 6 economics, Phase 7 wizards, Phase 8 frontend).
- [ ] Real RMS material for G2b
- [ ] Owner thresholds — Targeta yield seam
- [ ] Owner + DPO thresholds — Mtafiti V3 overlay seam
- [ ] DPO — Northena Ledger retention window
- [ ] DPO — V2 cumulative-disclosure arm env vars
- [ ] MEA — real source-standing table
- [ ] Owner narrowing on `ObjectiveRequest_v2` HAZARD-STOP-NOTE fields (`Reach.depth`, `Envelope.budget`, `Envelope.scope_ceiling`) — future frozen-contract additions when owner rules on scalar types
