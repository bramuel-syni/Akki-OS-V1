# PHASE_STATE (compact mirror of ORCHESTRATOR_CONTINUITY §2 + §3)

**Last update:** 2026-07-04 (Phase 5 Stage B close — Async delivery §7 landed live at `POST /api/objectives` + `GET /api/objectives/{id}` + `POST /api/objectives/{id}/cancel`; 2 new frozen contracts landed as ADDITIONS: `NorthenaLedgerRow_v1` + `AsyncDeliveryAccepted_v0`; 3 new Standing Owner Dispositions landed at §0.1; parity 18→20 GREEN)

> Any duration / credit / turn number referenced below is a **Provisional planning anchor — not a commitment. Relative weight only.**

## Live State
- **Current gate:** **PHASE 5 STAGE B CLOSED** (2026-07-04) — §7 async delivery live. `POST /api/objectives` returns 202 with `AsyncDeliveryAccepted_v0` (20th frozen contract) OR 422 `AdmissionRefusal_v0` (idempotency-key governed refusals) OR 503 (queue saturated, infra-not-refusal doctrine). `GET /api/objectives/{id}` returns wire-shape polling envelope. `POST /api/objectives/{id}/cancel` returns thin cancelled envelope (4 keys, no claim content). v2 dispatch fresh-fork route ALSO widened to include AsyncDeliveryAccepted_v0 @202 (Owner Q4.d default). 2 NEW frozen contracts: `NorthenaLedgerRow_v1` (contract 19, supersets v0 + adds `terminate_cancelled`; snapshot SHA `0ec71fde...`) + `AsyncDeliveryAccepted_v0` (contract 20, snapshot SHA `d2027c02...`). Mechanical parity 18→20 GREEN. 18 PRIOR frozen contract sources byte-identical pre-5b vs post-5b (verified by parametrised `test_v0_paths_byte_identical_after_5b.py`). Phase 5 Stage A CLOSED. Phase 4b + Phase 4a Stage B CLOSED. Phase 3 CLOSED. Phase 2 CLOSED. Substrate-Drop v2 CLOSED. Phase 0 CLOSED. Phase 1 CLOSED. G5b CLOSED. Backend surface FROZEN except additive-only Phase 5 Stage B landing (2 new frozen contracts + 9 new source files + 5 modified files + 2 new test files + 5 pre-Stage-B test migrations per Condition-5 pattern; zero v0 mutations). Close report on-disk canonical: `/app/docs/close_reports/phase_5_stage_b.md` SHA-256 `49ce2262b1f6f6e244bb7294b165734f6de31a1b176a55f73dd8871e94a2def5`.
- **Counting standard:** post-§0-strict from G6 forward.
- **Standing Owner Dispositions in force** (see ORCHESTRATOR_CONTINUITY §0.1): Ruling 2 (literal-widening HAZARD), Ruling 4 (§10 uniform disposition), Ruling 5 (§6.3/§6.4 confirmed as written), Elevated Doctrine (validation surface IS contract surface), Loose-as-frozen, Ruling 4 shared-derivation, Ruling 3 config-as-versioned-not-frozen, Ruling 1 (Item 4 supersede), Admission-refusal reasons extend via versioned registry, §6.1 payload UNFROZEN by wire-shape gate, License-class Phase 7 seam pre-committed, **Implementation close reports as on-disk canonical + SHA + inline (Phase 4a Stage B, 2026-07-04)**, **Frozen-field-changes-as-new-versions (Phase 5 Stage B, 2026-07-04)**, **Infra-not-refusal (Phase 5 Stage B, 2026-07-04)**, **Cancellation-is-a-state-not-a-refusal (Phase 5 Stage B, 2026-07-04)**.
- **Plan Debts:** ~~§6.1 downgrade~~ RESOLVED at 4a Stage B; ~~Phase 3 model-refusal~~ RESOLVED at Phase 3; ~~Phase 4b transform-variants~~ RESOLVED at Phase 4b; **~~Phase 5 async-delivery debt~~ RESOLVED at Phase 5 Stage B, 2026-07-04**; Phase 6 economics debt REMAINING (§8 `PriceModel@vN`, `FleetPolicy@vN`); Phase 7 wizard-side dispatch debt REMAINING (+ Phase 7 additional receiver debt: wizard-side rendering of `AdmissionRefusal@v0` as REFUSAL-WITH-PATH per UI Spec §3.3 + License-class Phase-7-seam wrap unchanged from pre-commit); Phase 8 frontend rework against UI Spec v1 REMAINING.
- **Phase 5 Stage B CLOSED (2026-07-04):** 9 NEW source files (async_state.py 306L + async_worker.py 197L + webhook.py 106L + idempotency.py 35L + cancellation.py 59L + admission_refusal_reasons.v2.json 38L + service_1_refusal_reasons.v0.json 19L + webhook_registration.py 73L + routers/objectives.py 211L) + 2 NEW frozen contracts (northena_ledger_v1.py 80L + async_delivery_accepted.py 50L) + 5 MODIFIED source files (dispatch.py +80/-13; admission_refusal.py +128 net; routers/service_1.py +48/-27; server.py +21/-3; contracts/__init__.py +3) + 2 NEW test files (Stage-B roster 894L + byte-identity regression 124L) + 5 pre-Stage-B test migrations (Condition-5 pattern: fresh-fork placeholder 501 → async accepted 202/422). Full CI: 446 → 504 (+58 net). Substrate-drop 9/9 GREEN. Mechanical parity 3/3 GREEN at 20. `make ci` PASSED.
- **Awaiting:** Owner acceptance of Phase 5 Stage B close before Phase 6 dispatch.
- **Last green CI:** 504/504 backend at 2026-07-04 (+ 18/18 frontend gate tests unchanged from G5b). Substrate-drop gate 9/9 green. Mechanical parity invariant 3/3 green at 20 entries.
- **Data source posture:** SYNTHETIC v1 = standing test substrate (permanent); real material = operational/benchmark input; no supersede semantics (Ruling 1, 2026-07-03).
- **Canonical specs on-disk:** 7/7 CURRENT.
- **Frozen contracts:** **20** (was 18 at Phase 4b close; +2 at Phase 5 Stage B: `NorthenaLedgerRow_v1` snapshot SHA `0ec71fde...` + `AsyncDeliveryAccepted_v0` snapshot SHA `d2027c02...`). All 20 have canonical `.contract_snapshot.json` files; mechanical parity invariant enforces bijection.
- **Closed seams (5):** `mtafiti_v3_overlay`, `targeta_yield_layer`, `northena_ledger_deletion`, `v2_cumulative_disclosure_arm`, `§6.1_payload_freeze` UNFROZEN by wire-shape gate. Phase 5 Stage B introduced ZERO new seams.
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
| **Phase 4b — §6.2 composed-conclusion path + 18th frozen contract `ComposedConclusion_v0`** | **CLOSED** | **446 (+12)** | ~230 | ~640 (against ~810 band; -21% delta under) | ~2.8× overall / ~0.28× discretionary-only |
| **Phase 5 Stage A — Async Delivery Contract design (design-only)** | **CLOSED** | **446 (unchanged)** | N/A | N/A (Stage B does LoC accounting) | N/A |
| **Phase 5 Stage B — Async delivery §7 implementation (async admission + 5-state machine + webhook + cancellation; 2 new frozen contracts: NorthenaLedgerRow_v1 + AsyncDeliveryAccepted_v0; 3 new Standing Owner Dispositions at §0.1)** | **CLOSED** | **504 (+58)** | ~340 (asyncio.Queue std lib; HMAC-SHA256 signing pattern from trust_receipt.py; Mongo async client pattern; FastAPI APIRouter pattern; Pydantic contract-file scaffolding; ObjectiveRequest_v2 lift; Service1Refusal exception pattern from A2) | ~2274 combined (source ~1256 + test ~1018) against ~1600-2200 band; +3.4% delta above band, within acceptable variance | ~6.7× overall / ~0.68× discretionary-only |
| G2b | BLOCKED (real RMS material) | — | — | — | — |

## Pending Decisions
- [x] ~~Substrate-Drop v2 Part 1?~~ — CLOSED at 2026-07-03.
- [x] ~~Substrate-Drop v2 Part 2 (Phase 0)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 1 (Estate Feasibility Query)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 2 (Shape-Responsive Execution Scaffold)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 3 (Admission-Refusal Envelope — unified §6.5 + future admission reasons via registry)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 4 Stage A (design proposals)?~~ — CLOSED at 2026-07-03.
- [x] ~~Phase 4a Stage B (§6.1 qualified-data path + shared substrates)?~~ — CLOSED at 2026-07-04.
- [x] ~~Phase 4b (§6.2 composed-conclusion path + 18th frozen contract `ComposedConclusion_v0`)?~~ — CLOSED at 2026-07-04.
- [x] ~~Phase 5 Stage A (Async Delivery Contract design)?~~ — CLOSED at 2026-07-04.
- [x] ~~Phase 5 Stage B (Async delivery §7 implementation)?~~ — CLOSED at 2026-07-04.
- [x] ~~Item 4 HAZARD-STOP (fixture-supersede posture)?~~ — RESOLVED at 2026-07-03 per Ruling 1.
- [ ] Owner acceptance of Phase 5 Stage B close report (`/app/docs/close_reports/phase_5_stage_b.md` SHA `49ce2262...`) before Phase 6 dispatch.
- [ ] Owner directive on next phase to dispatch (Phase 6 economics §8 [`PriceModel@vN`, `FleetPolicy@vN`], Phase 7 wizards §3.3, Phase 8 frontend rework against UI Spec v1).
- [ ] Real RMS material for G2b
- [ ] Owner thresholds — Targeta yield seam
- [ ] Owner + DPO thresholds — Mtafiti V3 overlay seam
- [ ] DPO — Northena Ledger retention window
- [ ] DPO — V2 cumulative-disclosure arm env vars
- [ ] MEA — real source-standing table
- [ ] Owner narrowing on `ObjectiveRequest_v2` HAZARD-STOP-NOTE fields (`Reach.depth`, `Envelope.budget`, `Envelope.scope_ceiling`) — future frozen-contract additions when owner rules on scalar types
