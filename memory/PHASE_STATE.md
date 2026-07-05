# PHASE_STATE (compact mirror of ORCHESTRATOR_CONTINUITY §2 + §3)

**Last update:** 2026-07-05 (Phase 8 Stage B-1 close — auth/key model + envelope-shim triad extraction + shared UI-Spec-v1 §8 barrel + Ask Console-full auth wiring + Playwright chromium smoke.)

> Any duration / credit / turn number referenced below is a **Provisional planning anchor — not a commitment. Relative weight only.**

## Live State
- **Current gate:** **PHASE 8 STAGE B-1 CLOSED — AUTH/KEY MODEL + ENVELOPE-SHIM TRIAD EXTRACTION + SHARED UI-SPEC-V1 §8 BARREL + ASK CONSOLE-FULL AUTH WIRING + PLAYWRIGHT CHROMIUM SMOKE** (2026-07-05). Auth/key model per Owner E1 ratified (custom JWT via PyJWT 2.13.0 + bcrypt 4.1.3, no hand-rolled crypto). Endpoints at `/api/auth/*`: POST /register + POST /login + POST /refresh + GET /me. 4-code auth-refusal bounded set at `services/auth/auth_refusal_reasons.v0.json` (Ruling 3 versioned config): auth_missing (401) / auth_expired (401) / auth_scope_insufficient (403) / auth_identity_mismatch_for_wizard_session (403). Body shape verbatim per Owner E2 non-negotiable: `{"reason", "detail"}` — NO `outcome` key, NO `outcome=refused`, NO AdmissionRefusal_v0 discriminator. Registry-exclusion + console render-path gates GREEN (fourth-not-wearing-first's-clothes preserved). Envelope-shim triad extraction (Owner E3) — `services/wizard/router_shims.py` (159L) canonical; `admission_handoff.py` reduced 212→38L pure re-export shim; grep-negative gate × 3 symbols × 2 routers GREEN. Shared UI-Spec-v1 §8 component barrel at `components/ui_spec_v1/index.js` (re-exports 6 v1 §8 shared components + AuthDeniedNotice). Ask Console-full auth wiring: apiClient +67L tokenStore + Bearer interceptor + auth endpoints + formatApiErrorDetail helper; hooks/useAuth 88L; AuthLoginPage 131L; AuthRegisterPage 132L; App.js +5L AuthProvider wrap + /auth/login + /auth/register routes. Playwright chromium-only config + 1 authenticated smoke scenario. Zero new frozen contracts (parity 26 unchanged); zero new §0.1 dispositions (§0.1 FROZEN). §0.2 updates: 2 debts RESOLVED at B-1 (wizard session-ownership binding + envelope-shim helper triad extraction). All prior phases CLOSED.
- **Plan Debts:** ~~§6.1 downgrade~~ RESOLVED at 4a Stage B; ~~Phase 3 model-refusal~~ RESOLVED at Phase 3; ~~Phase 4b transform-variants~~ RESOLVED at Phase 4b; ~~Phase 5 async-delivery~~ RESOLVED at Phase 5 Stage B; ~~Phase 6 economics~~ RESOLVED at Phase 6 Stage B; ~~Phase 7 wizard-side dispatch (all)~~ RESOLVED at Phase 7 Stage B-3; ~~Phase 8 Stage A trajectory restatement~~ RESOLVED at Phase 8 Stage A; ~~Wizard session-ownership binding~~ RESOLVED at Phase 8 B-1 (services/auth/session_binding.py); ~~Envelope-shim helper triad extraction~~ RESOLVED at Phase 8 B-1 (services/wizard/router_shims.py). **Phase 8c DPO `wizard_transcript` separately-addressable held-class enumeration** REMAINING (targeting Phase 8 B-5). Phase 8 B-2/B-3/B-4/B-5 surfaces REMAINING (Operator/Engineer/Buyer/Master Admin/DPO).
- **Phase 8 Stage B-1 CLOSED (2026-07-05) — deliverables:** 12 NEW backend source files (services/auth/*.py + auth_refusal_reasons.v0.json + routers/auth.py + services/wizard/router_shims.py) + 1 NEW backend test file (test_phase_8_b_1_auth_and_shims.py 393L, 37 gates) + 3 MODIFIED backend files (admission_handoff.py 212→38L pure re-export shim / server.py +9L / .env +3 vars / requirements.txt +2 deps) + 7 NEW frontend source files (AuthDeniedNotice + ui_spec_v1/index barrel + useAuth hook + AuthLoginPage + AuthRegisterPage) + 2 NEW frontend test files (auth_denied_notice_not_refusal_card + shared_components_single_source) + 2 NEW frontend e2e files (playwright.config.js + ask_console_smoke.spec.js) + 2 MODIFIED frontend files (apiClient.js +67L / App.js +5L) + 1 close report at `/app/docs/close_reports/phase_8_b_1.md` SHA `b6d5c7a1ea0aaffa7b2a27dc31d96fd8c64f1ff071caf75913ffe6dde6c3f1fe`. Rule 2 accounting JSON extended 30→31 phases (snapshot_lloc_in_band=no; transcription-only per Owner cap). Zero new §0.1 dispositions. 2 §0.2 Plan Debts RESOLVED at B-1.
- **Awaiting:** Owner acceptance of Phase 8 Stage B-1 close report at `/app/docs/close_reports/phase_8_b_1.md` SHA `b6d5c7a1ea0aaffa7b2a27dc31d96fd8c64f1ff071caf75913ffe6dde6c3f1fe`. Ready for Phase 8 Stage B-2 (Operator surface per UI Spec §2) dispatch.
- **Last green CI:** backend **777 / 777** at 2026-07-05 (baseline 740 → +37 net at Phase 8 Stage B-1). Frontend **47 / 47** across 7 UI-Spec-v1 suites at 2026-07-05 (baseline 27 → +20 net at B-1). Webpack GREEN. Substrate-drop gate 9/9 green. Mechanical parity invariant 3/3 green at **26** entries.
- **Counting standard:** post-§0-strict from G6 forward.
- **Standing Owner Dispositions in force** (see ORCHESTRATOR_CONTINUITY §0.1): 9 total. §0.1 FROZEN. Zero new dispositions at B-3.
- **Plan Debts:** ~~§6.1 downgrade~~ RESOLVED at 4a Stage B; ~~Phase 3 model-refusal~~ RESOLVED at Phase 3; ~~Phase 4b transform-variants~~ RESOLVED at Phase 4b; ~~Phase 5 async-delivery~~ RESOLVED at Phase 5 Stage B; ~~Phase 6 economics~~ RESOLVED at Phase 6 Stage B; ~~Phase 7 wizard-side dispatch (all)~~ RESOLVED at Phase 7 Stage B-3 (wizard trilogy complete). **Wizard session-ownership binding lands with Phase 8 auth/key model** (from B-2). **Phase 8 Stage A frozen-contract trajectory restatement** REMAINING (from B-1). **Phase 8c DPO `wizard_transcript` held-class enumeration** REMAINING (from B-1). Phase 8 full frontend rework REMAINING.
- **Phase 7 Stage B-3 CLOSED (2026-07-04) — deliverables:** 1 NEW source module (admission_handoff.py 211L) + 1 NEW test file (test_phase_7_stage_b_3_wizard.py 574L; 30 named gates + parametrised expansions = ~55 collected cases) + 1 NEW Stage A doc (232L; SHA `040c4099...`) + 2 MODIFIED routers (wizard_buyer.py +176L; wizard_operator.py +101L) + 2 MODIFIED support files (test_phase_7_stage_b_2_wizard.py ±32L point-in-time gate adjustments; docs/lift_manifest.json ±60L 8a-lite copy-forward). Zero new frozen contracts. Zero new §0.1 dispositions. Zero new §0.2 Plan Debts. Rule 2 accounting JSON extended 28 → 30 phases (transcription-only per Owner cap; served through /api/discipline/lift_manifest — verified 30 keys live). Close report SHA `ea12517cec7deee48818a097e942d08601fda5a0f381e215a7df2c508c801c30`.
- **Awaiting:** Owner acceptance of Phase 7 Stage B-3 close report at `/app/docs/close_reports/phase_7_stage_b_3.md` SHA `ea12517cec7deee48818a097e942d08601fda5a0f381e215a7df2c508c801c30`. Hold before Phase 8 full dispatch.
- **Last green CI:** backend **740 / 740** at 2026-07-04 (baseline 685 → +55 net at Phase 7 Stage B-3). Frontend **27 / 27** across 5 UI-Spec-v1 suites at 2026-07-04. Production `yarn build` GREEN. Substrate-drop gate 9/9 green. Mechanical parity invariant 3/3 green at **26** entries.
- **Data source posture:** SYNTHETIC v1 = standing test substrate (permanent); real material = operational/benchmark input; no supersede semantics (Ruling 1, 2026-07-03).
- **Canonical specs on-disk:** 7/7 CURRENT.
- **Frozen contracts:** **26** (unchanged; B-3 introduced ZERO new frozen contracts).
- **Closed seams (5):** unchanged. Phase 7 Stage B-3 introduced ZERO new seams.
- **Rule 2 accounting version:** v2 + §0 discretionary-enumeration-inline discipline. B-3 ratio ~2.24× overall / ~1.6× discretionary; anchored band 800-1100 (mid ~950) → 1094 actual → WITHIN BAND.
- **Discipline observations tracked separately:** X1 — `solva_depth/pipeline.py` code fix is LIVE + test-defended.
- **Open HAZARD-STOP flags:** 0. **Wizard trilogy complete.**

## Phase Ledger
| Phase | Status | Green @ close | Lifted (verifiable) | Net-new | Ratio (v2) |
|---|---|---|---|---|---|
| G0 | CLOSED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| G0.5 | CLOSED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| G1 | CLOSED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Pre-G2 | CLOSED | 61 | UNKNOWN | UNKNOWN | UNKNOWN |
| G2a | CLOSED | 73 initial → 149 rolling | 127 | 344 | 2.71× / 1.34× discretionary |
| Substrate-Drop v1 | CLOSED | 158 | 0 | 0 | N/A |
| G3 | CLOSED | 211 | 98 | 437 | 4.46× / ~0.02× discretionary |
| G4 | CLOSED | 271 | 268 | 785 | 2.93× / 0.00× discretionary |
| G5a | CLOSED | 301 | 159 | 715 | 4.50× / 0.11× discretionary |
| G6 | CLOSED | 340 | 80 | 1176 | 14.70× / 0.80× discretionary |
| Handoff-Download Route | CLOSED | 347 | 12 | 30 | 1.00× discretionary-only |
| A2 | CLOSED | 355 | 20 | ~50 | ~1.27× discretionary-only |
| G5b | CLOSED | 359 backend + 12/12 frontend | 0 | 1848 | N/A |
| Docs-Pass | CLOSED | 367 | 0 | 0 | N/A |
| Substrate-Drop v2 (Part 1) | CLOSED | 373 (+6) | 0 | 0 | N/A |
| Substrate-Drop v2 (Part 2 / Phase 0) | CLOSED | 374 (+1) | 0 | ~180 | ~12× / ~0.08× discretionary-only |
| Phase 1 | CLOSED | 387 (+13) | ~30 | ~490 | ~5.7× / ~0.30× discretionary-only |
| Phase 2 | CLOSED | 402 (+15) | ~40 | ~460 | ~4.2× / ~0.24× discretionary-only |
| Phase 3 | CLOSED | 413 (+11) | ~35 | ~470 | ~13.4× / ~0.19× discretionary-only |
| Phase 4 Stage A | CLOSED | 413 | N/A | N/A | N/A |
| Phase 4a Stage B | CLOSED | 434 (+21) | ~120 | ~840 | ~7× / ~0.30× discretionary-only |
| Phase 4b | CLOSED | 446 (+12) | ~230 | ~640 | ~2.8× / ~0.28× discretionary-only |
| Phase 5 Stage A | CLOSED | 446 | N/A | N/A | N/A |
| Phase 5 Stage B | CLOSED | 504 (+58) | ~340 | ~2274 | ~6.7× / ~0.68× discretionary-only |
| Phase 6 Stage A | CLOSED | 504 | N/A | N/A | N/A |
| Phase 6 Stage B | CLOSED | 550 (+46 net) | ~180 | ~2812 | ~15.6× / ~1.28× discretionary-only |
| Phase 7 Stage A | CLOSED | 550 | N/A | N/A | N/A |
| Phase 7 Stage B-1 | CLOSED | 613 (+63 net) | ~120 | ~2754 | ~23× / ~2.08× discretionary-only |
| Phase 7 Stage B-2 | CLOSED | 685 (+72 net) | ~500 | ~1757 | ~3.5× / ~1.4× discretionary (WITHIN BAND -2.4% below mid ~1800 of 1600-2000) |
| Phase 8a-lite | CLOSED | Frontend 27/27 across 5 UI-Spec-v1 suites; backend 685/685 unchanged | 0 backend (frontend reuses shared components) | ~1173 frontend LoC | N/A (frontend phase) |
| **Phase 7 Stage B-3 — Wizard trilogy COMPLETE (commit-review extensions + buyer freeze ledger parity + admission handoff endpoints on both variants)** | **CLOSED** | **740 (+55 net; Block A 7 gates → Block B 13 gates → Block C 10 gates + parametrised expansions = ~55 collected cases)** | ~275 (ObjectiveRequest_v2 model_validate + WizardCommitState_v0 model_copy + derive_license_class from B-1 + record_wizard_freeze from B-1 + session_persistence.load_session + evaluate_dual_delta from B-2 + httpx.AsyncClient(ASGITransport) pattern from tests + declarative-table pattern from B-2/B-1) | ~1094 (1 NEW module admission_handoff.py 211L + 1 NEW test file 574L + 1 NEW Stage A doc 232L + 2 MODIFIED routers wizard_buyer.py +176 / wizard_operator.py +101 + 2 MODIFIED support files test_phase_7_stage_b_2_wizard.py ±32 / lift_manifest.json ±60) | ~2.24× overall / ~1.6× discretionary-only (v2 accounting, post-§0-strict). **Anchored band 800-1100 (mid ~950) → 1094 actual → WITHIN BAND (+15% of mid; -0.5% within top-of-band). No Rule-2 stop-and-judge triggered.** |
| G2b | BLOCKED (real RMS material) | — | — | — | — |

## Pending Decisions
- [x] ~~Phase 6 Stage B~~ — CLOSED 2026-07-04.
- [x] ~~Phase 7 Stage A (design-only)~~ — CLOSED 2026-07-04.
- [x] ~~Phase 7 Stage B-1 (operator variant + 4 net-new contracts)~~ — CLOSED 2026-07-04.
- [x] ~~Phase 7 Stage B-2 (buyer variant + Sonnet 4.6 LLM)~~ — CLOSED 2026-07-04.
- [x] ~~Phase 8a-lite (Ask Console UI Spec v1 §3 landing)~~ — CLOSED 2026-07-04.
- [x] ~~Phase 7 Stage B-3 (commit-review + buyer freeze + admission handoff)~~ — CLOSED 2026-07-04. Wizard trilogy COMPLETE.
- [ ] Owner acceptance of Phase 7 Stage B-3 close report (`/app/docs/close_reports/phase_7_stage_b_3.md` SHA `ea12517cec7deee48818a097e942d08601fda5a0f381e215a7df2c508c801c30`) before Phase 8 full dispatch.
- [ ] Owner directive on Phase 8 FULL dispatch (Operator / Engineer / Buyer / Master Admin / DPO surfaces per UI Spec §2).
- [ ] Real RMS material for G2b.
- [ ] Owner thresholds — Targeta yield seam.
- [ ] Owner + DPO thresholds — Mtafiti V3 overlay seam.
- [ ] DPO — Northena Ledger retention window.
- [ ] DPO — wizard_transcript retention class (per Owner E5 ruling; at Seam-3 unlock).
- [ ] DPO — V2 cumulative-disclosure arm env vars.
- [ ] MEA — real source-standing table.
- [ ] Owner narrowing on `ObjectiveRequest_v2` HAZARD-STOP-NOTE fields.
- [ ] **NEW at 7b-2:** Wizard session-ownership binding — lands with Phase 8 auth/key model (system-wide auth landing, not wizard-special).
