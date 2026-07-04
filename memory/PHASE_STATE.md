# PHASE_STATE (compact mirror of ORCHESTRATOR_CONTINUITY §2 + §3)

**Last update:** 2026-07-03 (Phase 2 close — Shape-Responsive Execution Scaffold)

> Any duration / credit / turn number referenced below is a **Provisional planning anchor — not a commitment. Relative weight only.**

## Live State
- **Current gate:** **PHASE 2 CLOSED** (2026-07-03) — shape-responsive execution scaffold landed. Substrate-Drop v2 CLOSED. Phase 0 CLOSED. Phase 1 CLOSED. G5b remains CLOSED (2026-07-02T10:00Z). Docs-Pass 2026-07-02 remains CLOSED. All prior phases CLOSED. Backend surface FROZEN except additive-only Phase 2 landing (new v2 dispatch route, no new frozen contracts, no v0 mutations).
- **Counting standard:** post-§0-strict from G6 forward.
- **Standing Owner Dispositions in force** (see ORCHESTRATOR_CONTINUITY §0.1): Ruling 2 (literal-widening HAZARD), Ruling 4 (§10 uniform disposition), Ruling 5 (§6.3/§6.4 confirmed as written), Elevated Doctrine (validation surface IS contract surface), Loose-as-frozen (deliberate under-determination is not a HAZARD; hardening lands as new contract version), **Ruling 4 shared-derivation (floor_feasibility one function two consumers)**, **Ruling 3 config-as-versioned-not-frozen (feasibility-config@vN control-surface pattern)**, **Ruling 1 (Item 4 supersede) — 2026-07-03: SYNTHETIC v1 = standing test substrate; real material = operational/benchmark input; no supersede semantics between them; fixture-augmentation-file pattern carries forward**.
- **Plan Debts (see ORCHESTRATOR_CONTINUITY §0.2):** §6.1 downgrade plan-debt (whichever phase consumes §6.1 restates LoC band + gate at its own dispatch); **Phase 3 model-refusal debt (v3 §6.5 refusal envelope, NEW frozen contract); Phase 4 transform-variants debt (v3 §6.1+§6.2 + AdmissionRefusal@v0); Phase 5 async-delivery debt (v3 §7); Phase 7 wizard-side dispatch debt (v3 §3.3 per-turn feasibility grounding)** — all named by Phase 2 dispatch placeholders (recorded 2026-07-03).
- **Phase 2 CLOSED (2026-07-03):** `services/service_1/dispatch.py` + additive-only `POST /api/service_1/v2/dispatch` route; shared-import discipline (compute_feasibility + derive_floor_feasibility) statically enforced; UNKNOWN→FRESH honesty gate LOAD-BEARING; placeholder-vs-refusal rendering separation LOAD-BEARING; depth-enum-branch-prohibition LOAD-BEARING; v0 SHA-untouched regression LOAD-BEARING. Full CI: 387 → 402 (+15). Snapshot count 16 → 16 (unchanged; DispatchResult UNFROZEN per Ruling 3 pattern).
- **Awaiting:** user directive on which post-Phase-2 phase to dispatch (Phase 3, 4, 5, 6, 7, 8, or defer).
- **Last green CI:** 402/402 backend at 2026-07-03 (+ 18/18 frontend gate tests unchanged from G5b). Substrate-drop gate 9/9 green. Mechanical parity invariant 3/3 green at 16 entries.
- **Data source posture:** SYNTHETIC v1 = standing test substrate (permanent); real material = operational/benchmark input; no supersede semantics between them (Ruling 1, 2026-07-03).
- **Canonical specs on-disk:** 7/7 CURRENT — post-v2 slate: Solva, Targeta, Mtafiti, Northena, Product v3, UI v1, UX v2. Three predecessors archived with SUPERSEDED headers.
- **Frozen contracts:** 16 (unchanged at Phase 2). All 16 have canonical `.contract_snapshot.json` files; mechanical parity invariant enforces bijection.
- **Closed seams (4):** unchanged — `mtafiti_v3_overlay`, `targeta_yield_layer`, `northena_ledger_deletion`, `v2_cumulative_disclosure_arm`. All grep-verified intact post-Phase-2.
- **Rule 2 accounting version:** v2 + §0 discretionary-enumeration-inline discipline.
- **Discipline observations tracked separately:** X1 — `solva_depth/pipeline.py` code fix is LIVE + test-defended.
- **Open HAZARD-STOP flags:** 0 — Item 4 RESOLVED at Phase 2 close.

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
| **G5b** | **CLOSED** | 359 backend + 12/12 frontend gate | 0 (API-consumption) | 1848 (all discretionary) | N/A (no source lift) |
| Docs-Pass (Source-Spec Corrections) | CLOSED | 367 | 0 (docs) | 0 | N/A |
| **Substrate-Drop v2 (Part 1)** | **CLOSED** | **373** (+6 tests: 3 backfill freeze + 3 parity) | 0 (docs+CI phase; backfill by-copy) | 0 (net-new code) | N/A |
| **Substrate-Drop v2 (Part 2 / Phase 0)** | **CLOSED** | **374** (+1 test: v2 freeze) | 0 (net-new contract) | ~180 (all mandate-forced per v3 §3.2 verbatim; ~15 discretionary flagged as HAZARD-STOP-NOTES for owner narrowing) | ~12× overall / ~0.08× discretionary-only |
| **Phase 1 — Estate Feasibility Query** | **CLOSED** | **387** (+13 tests: 4 honesty + 1 schema-freeze + 1 readonly + 3 dual-consumer + 4 shared-derivation) | ~30 (opcounters pattern, ledger-shape) | ~490 (16th frozen `FeasibilityResult v0` + compute + shared derivation + endpoint + 5 tests; ~85 discretionary framing) | ~5.7× overall / ~0.30× discretionary-only |
| **Phase 2 — Shape-Responsive Execution Scaffold** | **CLOSED** | **402** (+15 tests: 4 named gates + 5 positive-path + 2 wire-shape + 3 v0-untouched + 1 malformed-body) | ~40 (feasibility read-only pattern, ASGITransport pattern, v2 shape lift) | ~460 (dispatch module + additive v2 route + 2 test files; ~110 discretionary framing enumerated inline in close report) | ~4.2× overall / ~0.24× discretionary-only |
| G2b | BLOCKED (real RMS material) | — | — | — | — |

## Pending Decisions
- [x] ~~Substrate-Drop v2 Part 1?~~ — CLOSED at 2026-07-03.
- [x] ~~Substrate-Drop v2 Part 2 (Phase 0 — `ObjectiveRequest v2`)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 1 (Estate Feasibility Query)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 2 (Shape-Responsive Execution Scaffold)?~~ — CLOSED at 2026-07-03.
- [x] ~~Item 4 HAZARD-STOP (fixture-supersede posture)?~~ — RESOLVED at 2026-07-03 per Ruling 1.
- [ ] User directive on which post-Phase-2 phase to dispatch (Phase 3 model refusal, Phase 4 transform variants, Phase 5 async delivery, Phase 6 economics, Phase 7 wizards, Phase 8 frontend).
- [ ] Real RMS material for G2b
- [ ] Owner thresholds — Targeta yield seam
- [ ] Owner + DPO thresholds — Mtafiti V3 overlay seam
- [ ] DPO — Northena Ledger retention window
- [ ] DPO — V2 cumulative-disclosure arm env vars
- [ ] MEA — real source-standing table
- [ ] Owner narrowing on `ObjectiveRequest_v2` HAZARD-STOP-NOTE fields (`Reach.depth`, `Envelope.budget`, `Envelope.scope_ceiling`) — future frozen-contract additions when owner rules on scalar types
