# PHASE_STATE (compact mirror of ORCHESTRATOR_CONTINUITY §2 + §3)

**Last update:** 2026-07-02T02:15Z

> Any duration / credit / turn number referenced below is a **Provisional planning anchor — not a commitment. Relative weight only.**

## Live State
- **Current gate:** **A2 CLOSED** (2026-07-02T02:15Z). `Service1Refusal@v0` shipped as 14th frozen contract. `POST /api/service_1/run` now returns flat JSONResponse-based refusal at HTTP 422 across 3 reason codes. HANDOFF-DOWNLOAD ROUTE shipped earlier in the session (2026-07-02T01:30Z). Awaiting user go on G5b dispatch.
- **Counting standard:** post-§0-strict from G6 forward; G3/G4/G5a annotated as pre-§0 (no retroactive recount).
- **Awaiting:** user validation of the A2-amended handoff artifact → G5b dispatch.
- **Last green CI:** 355/355 at 2026-07-02T02:15Z. Delta from G6: +7 handoff route + +7 A2 refusal tests + +1 A2 snapshot invariant = +15 tests.
- **Data source posture:** SYNTHETIC. Incoming fixture v2 REJECTED.
- **Canonical specs on-disk:** 7/7 CURRENT. Substrate-drop gate CI-enforced.
- **Frozen contracts:** 14 (10 pre-G6 + 3 G6 additions + 1 A2 addition). No frozen contracts mutated across G0..A2.
- **Closed seams (4):** `mtafiti_v3_overlay`, `targeta_yield_layer`, `northena_ledger_deletion`, `v2_cumulative_disclosure_arm`.
- **Rule 2 accounting version:** v2 + §0 discretionary-enumeration-inline discipline.
- **Discipline observations tracked separately:** X1 — `solva_depth/pipeline.py:75-76` redundant `conclusion_class(lb)` recompute after `enforce()` returned `Refusal.computed_class`. Not a doctrine violation; parked for future consolidation phase.
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
| A2 (Service1Refusal envelope) | CLOSED | **355** | 20 | ~50 | ~1.27× discretionary-only |
| G2b | BLOCKED (real RMS material) | — | — | — | — |
| G5b | NOT STARTED | — | — | — | — |

## Pending Decisions
- [x] ~~Open G6?~~ — CLOSED at 2026-07-02T00:45Z.
- [x] ~~Freeze-and-Handoff artifact?~~ — DONE at 2026-07-02T01:00Z.
- [x] ~~Handoff-Download Route?~~ — SHIPPED at 2026-07-02T01:30Z.
- [x] ~~A2 (Service1Refusal envelope + composition_below_floor branch)?~~ — CLOSED at 2026-07-02T02:15Z.
- [ ] Open G5b?
- [ ] Real RMS material for G2b
- [ ] Owner thresholds — Targeta yield seam
- [ ] Owner + DPO thresholds — Mtafiti V3 overlay seam
- [ ] DPO — Northena Ledger retention window
- [ ] DPO — V2 cumulative-disclosure arm env vars
- [ ] MEA — real source-standing table
- [ ] X1 discipline observation — solva_depth/pipeline.py:75-76 redundant recompute (parked, non-blocking)
