# PHASE_STATE (compact mirror of ORCHESTRATOR_CONTINUITY §2 + §3)

**Last update:** 2026-07-03 (Substrate-Drop v2 close — Part 1 backfill + Part 2 Phase 0)

> Any duration / credit / turn number referenced below is a **Provisional planning anchor — not a commitment. Relative weight only.**

## Live State
- **Current gate:** **SUBSTRATE-DROP v2 CLOSED** (2026-07-03). Part 1 (backfill + parity invariant) + Part 2 (Phase 0 — `ObjectiveRequest v2`) both green. G5b remains CLOSED (2026-07-02T10:00Z). Docs-Pass 2026-07-02 remains CLOSED. All prior phases CLOSED. Backend surface FROZEN except additive-only Phase 0 landing. §6.1 verdict re-marked EXTENDS per Ruling 3 challenge (grep-negative on `grain`, `license_class`, and `standard`-as-admission-filter).
- **Counting standard:** post-§0-strict from G6 forward.
- **Standing Owner Dispositions in force** (see ORCHESTRATOR_CONTINUITY §0.1): Ruling 2 (literal-widening HAZARD), Ruling 4 (§10 uniform disposition), Ruling 5 (§6.3/§6.4 confirmed as written), Elevated Doctrine (validation surface IS contract surface), Loose-as-frozen (deliberate under-determination is not a HAZARD; hardening lands as new contract version).
- **Plan Debts (see ORCHESTRATOR_CONTINUITY §0.2):** §6.1 downgrade plan-debt — whichever phase consumes §6.1 restates LoC band + gate at its own dispatch (recorded 2026-07-03).
- **Awaiting:** user judgment on Item 4 HAZARD_STOP (v1 adversarial fixture NOT superseded — from Docs-Pass 2026-07-02); user directive on which phase to dispatch next.
- **Last green CI:** 374/374 backend at 2026-07-03 (+ 12/12 frontend gate tests unchanged from G5b). Substrate-drop gate 9/9 green. Mechanical parity invariant 3/3 green.
- **Data source posture:** SYNTHETIC (v1 shipping — NOT superseded per Item 4 HAZARD_STOP).
- **Canonical specs on-disk:** 7/7 CURRENT — post-v2 slate: Solva, Targeta, Mtafiti, Northena, Product v3, UI v1, UX v2. Three predecessors archived with SUPERSEDED headers.
- **Frozen contracts:** 15 (14 + 1 Phase 0 addition `ObjectiveRequest v2`). All 15 have canonical `.contract_snapshot.json` files; mechanical parity invariant enforces bijection.
- **Closed seams (4):** unchanged — `mtafiti_v3_overlay`, `targeta_yield_layer`, `northena_ledger_deletion`, `v2_cumulative_disclosure_arm`.
- **Rule 2 accounting version:** v2 + §0 discretionary-enumeration-inline discipline.
- **Discipline observations tracked separately:** X1 — `solva_depth/pipeline.py` code fix is LIVE + test-defended.
- **Open HAZARD-STOP flags:** 1 — Item 4 (fixture-supersede state question).

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
| G2b | BLOCKED (real RMS material) | — | — | — | — |

## Pending Decisions
- [x] ~~Substrate-Drop v2 Part 1?~~ — CLOSED at 2026-07-03.
- [x] ~~Substrate-Drop v2 Part 2 (Phase 0 — `ObjectiveRequest v2`)?~~ — CLOSED at 2026-07-03.
- [ ] User directive on which post-Phase-0 phase to dispatch (Phase 1 feasibility query, Phase 2 shape-responsive dispatch, or none).
- [ ] Real RMS material for G2b
- [ ] Owner thresholds — Targeta yield seam
- [ ] Owner + DPO thresholds — Mtafiti V3 overlay seam
- [ ] DPO — Northena Ledger retention window
- [ ] DPO — V2 cumulative-disclosure arm env vars
- [ ] MEA — real source-standing table
- [ ] Owner narrowing on `ObjectiveRequest_v2` HAZARD-STOP-NOTE fields (`Reach.depth`, `Envelope.budget`, `Envelope.scope_ceiling`) — future frozen-contract additions when owner rules on scalar types
