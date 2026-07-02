# Orchestrator Continuity Protocol (RMS Intelligence System)

> Purpose: after compaction, the orchestrator reads this file FIRST and follows the checklist before saying anything to the user or dispatching work. This file is the single source of truth for "where are we".

## 0. Immutable Ground Rules (never violate)
- Contract-First Hierarchy: `/app/backend/contracts/` schemas are FROZEN. Tests bend to contracts, never the reverse.
- **Rule 2 v2** (Substrate-Drop v1, 2026-07-01): Reshape-to-rewrite STOP applies when net-new LoC exceeds `lifted-verifiable` (kind ∈ {direct, transitive}). `unverifiable-substrate-absent` LoC stays in the manifest for provenance but is EXCLUDED from the lifted total for ratio purposes. Rule 2 is a **stop-and-judge trigger**, not an automatic shrink cap — when a ratio is high, the response is narrow-ratify-with-documentation (like Northena §12 mandate-forced scaffolding at G2a close), not force-the-number-down.
- **Discretionary-enumeration discipline** (added 2026-07-02T00:45Z at G6 close, following G5a ledger-completion pushback): Every phase report must include the full net-new-discretionary LoC enumeration INLINE. Confirming that the audit route serves live numbers is insufficient — the report itself must carry the numbers AND per-line rationale (file:line + one-line description + honest ratify rationale) at close. Aggregation is not allowed; every discretionary line is enumerated. If discretionary LoC == 0 across a phase, prove via §-anchor coverage per module.
- **Substrate-drop gate** (Substrate-Drop v1, 2026-07-01): A phase does not open until `phase_source_requirements` for that phase are all present in `/app/docs/mandates/` with matching SHA-256 in `MANIFEST.md`. The `backend/tests/invariants/test_substrate_drop_gate.py` invariant enforces this at CI time. If a required spec is missing or its hash mismatches, CI fails and the phase is blocked.
- Legacy repo `Akki-Executive-New-Arch` is UNREACHABLE from pod. Do NOT clone/probe. Use transitive-lift-with-manifest via `/app/docs/lift_manifest.json`.
- 4 HAZARD-STOPS (only reasons to break autonomy mid-phase):
  (a) frozen contract must mutate
  (b) governance decision needed (Owner/DPO)
  (c) substrate absent (log as unverifiable-substrate-absent)
  (d) Rule 2 trips
- Solva Boundary (when G3 opens): build `conclusion_class(load_bearing_units)` FIRST, no confidence params, freeze signature via `test_conclusion_class_signature.py`.
- **Read-only route invariant** (G5a): trace-lens + lift-manifest routes write zero rows to any persistent store; enforced by `test_trace_lens_readonly.py`.
- **Outer-gate irreversibility invariant** (G6): egress carries no plaintext identifiers; mint keys purged at end of window; enforced by `test_outer_gate_irreversibility.py`.
- **V2 refusal terminality** (G6): V2 refusal envelope IS the record; no partial-egress ever; enforced by `test_v2_gate_refusal_cumulative.py`.

## 1. Rehydration Checklist (run in order after compaction)
1. Read this file end-to-end.
2. Read `/app/BUILD_JOURNAL.md` — last 300 lines.
3. Read `/app/memory/PHASE_STATE.md` (see §3 below).
4. Read `/app/docs/lift_manifest.json` — get current lifted-vs-net-new LoC totals (v1 accounting).
5. Read `/app/docs/mandates/MANIFEST.md` — confirm canonical specs are on-disk.
6. Read `/app/docs/g4_prep/OPEN_GOVERNANCE.md` — pending Owner/DPO/MEA decisions.
7. Read the latest prep doc for the next phase (e.g. `/app/docs/g3_prep/solva_prep.md`).
8. Read `/app/docs/audits/substrate_drop_v1/` — the four reconciliation docs (Substrate-Drop v1).
9. Run `cd /app && make ci` — confirm current green test count matches PHASE_STATE.md.
10. ONLY THEN respond to the user.

## 2. Phase Ledger (append-only, most recent last)

> Note on estimate framing: any duration / credit / turn number referenced in this ledger or downstream is a **Provisional planning anchor — not a commitment. Relative weight only.** (Norm added at Substrate-Drop v1.)

> Note on LoC columns: only G2a has published per-phase lifted/net-new totals (see BUILD_JOURNAL 2026-07-01T08:30Z "Post-shrink Rule 2 LoC ledger"). Earlier phases froze contracts + reshaped pipeline modules but did not publish per-phase Rule-2 tallies at close; those are marked `UNKNOWN` honestly. Rolling lifted/net-new totals available per-module via `/app/docs/lift_manifest.json` entries.

| Phase | Status | Green tests at close | Lifted LoC | Net-new LoC | Ratio (v1 accounting) | Journal ref |
|---|---|---|---|---|---|---|
| G0 | CLOSED | UNKNOWN (tester 3/3 PASS marker only) | UNKNOWN | UNKNOWN | UNKNOWN | BUILD_JOURNAL 2026-06-30T19:30Z |
| G0.5 | CLOSED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | BUILD_JOURNAL 2026-06-30T19:30Z (opened) → 2026-07-01T00:00Z (pre-G2 handover) |
| G1 | CLOSED | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | BUILD_JOURNAL §G1 (multiple entries pre-2026-07-01T00:00Z) |
| Pre-G2 | CLOSED | 61 | UNKNOWN | UNKNOWN | UNKNOWN | BUILD_JOURNAL 2026-07-01T00:00Z |
| G2a | CLOSED | 73 (at initial close); post-shrink follow-ups added tests to 73→118→146→149 | 127 (all verifiable-transitive; 0 unverifiable) | 344 (170 discretionary + 174 mandate-§12-forced) | **2.71× overall / 1.34× discretionary-only** (v1 == v0 for G2a) | BUILD_JOURNAL 2026-07-01T07:10Z / T08:30Z (post-shrink) — discretionary counted under pre-§0 standard |
| Substrate-Drop v1 | CLOSED | 158 | 0 (no engine code) | 0 | N/A (docs+CI-invariant phase, no LoC change) | BUILD_JOURNAL 2026-07-01T15:39Z |
| G2b | BLOCKED (awaiting real RMS material Hour A/B/300-unit) | — | — | — | — | — |
| G3 | CLOSED | 211 | 98 (all verifiable-transitive, in-pod; 0 unverifiable) | 437 (~2 discretionary + ~435 mandate-forced per Solva Spec §7–§18) | **4.46× overall / ~0.02× discretionary-only** (v2 accounting) | BUILD_JOURNAL 2026-07-01T16:00Z–T17:15Z — discretionary counted under pre-§0 standard |
| G4 | CLOSED | 271 | 268 (all verifiable-transitive, in-pod; 0 unverifiable) | 785 (~0 discretionary + ~785 mandate-forced per Mtafiti §7 + Targeta §7 + Product v2.1 §2.1) | **2.93× overall / 0.00× discretionary-only** (v2 accounting) | BUILD_JOURNAL 2026-07-01T17:30Z–T18:55Z — discretionary counted under pre-§0 standard |
| G5a | CLOSED | 301 | 159 (transitive: Motor cursor pattern + FastAPI APIRouter boilerplate + Pydantic contract scaffolding + _fact_unit fixture-schema mirror + httpx.AsyncClient test transport; in-pod) | 715 (18 discretionary + 697 mandate-forced per Interface Spec §16 invariant #9 + Northena §7.2/§7.3/§12/§14 + Product v2.1 §8) | **4.50× overall / 0.11× discretionary-only** (v2 accounting, honest line-by-line audit; initial close numbers 30/864/0 → 28.80×/0.00× corrected in ledger completion pass) | BUILD_JOURNAL 2026-07-02T00:00Z + 2026-07-02T00:15Z — discretionary counted under pre-§0 standard |
| G5b | NOT STARTED | — | — | — | — | Frontend: Operator Console 4 surfaces + Consumer Terminal v0 |
| G5b | CLOSED | 359 (backend unchanged) + 12/12 frontend gate | 0 (API-consumption, no source lift) | 1848 (all discretionary — frontend-only) | N/A (no source lift) | BUILD_JOURNAL 2026-07-02T10:00Z |
| G6 | CLOSED | 340 | 80 (transitive: Pydantic contract scaffolding + absorb-function shape rhyme with converge.absorb_solva_trace + test infra transitive from G5a test suites; in-pod) | 1176 (64 discretionary + 1112 mandate-forced per Product v2.1 §21.2 + §22.1 + §29.1 + §30 + §31 Sys-Invariant #8 + §32 + Northena §14 stamp-audit side-channel) | **14.70× overall / 0.80× discretionary-only** (v2 accounting; ratify rationale filed inline per new §0 discretionary-enumeration discipline; ratio high because G6 built new crypto primitives with modest transitive lift — cousin_lineage documented in mint.py docstring though manifest lint keeps mint entry mandate-forced) | BUILD_JOURNAL 2026-07-02T00:45Z — discretionary under strict §0 standard (post-§0-strict) |

## 3. Current Live State (rewritten by e1_dev at every phase close)
- Current gate: **G5b CLOSED (2026-07-02T10:00Z)**. React web frontend shipped: Operator Console (4 surfaces — Portfolio, Runs, Discipline, Engines) + Consumer Terminal v0 (trace receipt viewer at `/trace/:traceId`) + Composition surface (objective submission with client-side validation + Service1RunSummary/Service1Refusal rendering). 8 routes, 8 components, 3 gate invariant tests (12/12 passing). Tailwind CSS pipeline fixed via `concurrently` + `tailwindcss --watch`. Backend unchanged — all 14 frozen contracts consumed via API only.
- Awaiting: user directive on next phase or wrap. G2b still blocked (real RMS material). 4 closed seams still pending governance decisions.
- Last green CI: **359/359** backend at **2026-07-02T10:00Z** + **12/12** frontend gate tests. Backend CI unchanged from A2 — G5b is frontend-only.
- Data source posture: **SYNTHETIC** (Layer A/B/C pipeline + adversarial fixture v1). Incoming fixture v2 REJECTED.
- Canonical specs on-disk: 7/7 CURRENT. Substrate-drop gate CI-enforced.
- Frozen contracts: **14** (G5b consumes, doesn't add). No frozen contracts mutated across G0..G5b.
- Frontend surface count: 4 Operator surfaces + 1 Consumer Terminal + 1 Landing + 1 Composition = 7 pages across 8 routes (answer B — "surface" spans multiple routes per UX Arch §7).
- **Closed seams (four)** — unchanged:
  * `mtafiti_v3_overlay` — awaits Owner thresholds.
  * `targeta_yield_layer` — awaits Owner thresholds.
  * `northena_ledger_deletion` — awaits DPO retention window.
  * `v2_cumulative_disclosure_arm` — awaits DPO env-var thresholds.
- Discipline observation carried forward (X1): `pipeline.py:75-76` solva_depth redundant recompute — parked, non-blocking.
- Open HAZARD-STOP flags: **NONE.**

## 4. Frozen Contracts (do not mutate without explicit re-bless)

Fourteen frozen contracts (10 pre-G6 + 3 additions at G6 + 1 at A2). All snapshot tests live in `/app/backend/tests/invariants/`.

| # | Contract file | Snapshot file(s) | Invariant test(s) | Added at |
|---|---|---|---|---|
| 1 | `backend/contracts/five_rings.py` | `five_rings.contract_snapshot.json` | `test_invariant_contract_snapshots.py` | pre-G0 |
| 2 | `backend/contracts/objective_request.py` | `objective_request.contract_snapshot.json` | `test_invariant_contract_snapshots.py` | pre-G0 |
| 3 | `backend/contracts/qualification_matrix/loader.py` | `qualification_matrix.schema_snapshot.json` + `.v0.content_snapshot.json` | `test_invariant_contract_snapshots.py` | pre-G0 |
| 4 | `backend/contracts/signal_ring.py` | `signal_ring_dimensions.v0.content_snapshot.json` | `test_signal_ring_dimensions_v0.py` | pre-G2 |
| 5 | `backend/contracts/extraction_params.py` | `extraction_params.v0.content_snapshot.json` | `test_extraction_params_v0.py` | pre-G2 |
| 6 | `backend/contracts/northena_ledger.py` | `northena_ledger_row.contract_snapshot.json` | `test_northena_ledger_row_v0.py` + `test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit.py::test_northena_ledger_row_contract_snapshot_unchanged_at_g6` (G6 invariant guarding no-mutation) | G2a |
| 7 | `backend/contracts/mtafiti_registry.py` | `mtafiti_registry_record.contract_snapshot.json` | `test_mtafiti_invariants.py::test_registry_record_contract_frozen` | G4 |
| 8 | `backend/contracts/targeta_plan.py` | `targeta_mining_plan.contract_snapshot.json` | `test_targeta_invariants.py::test_mining_plan_contract_frozen` | G4 |
| 9 | `backend/contracts/trace_lens.py` | `trace_lens_envelope.contract_snapshot.json` | `test_trace_lens_cross_engine_correlation.py::test_trace_lens_envelope_contract_frozen` | G5a |
| 10 | `backend/contracts/lift_manifest_response.py` | `lift_manifest_envelope.contract_snapshot.json` | `test_trace_lens_cross_engine_correlation.py::test_lift_manifest_envelope_contract_frozen` | G5a |
| 11 | `backend/contracts/outer_gate_receipt.py` (OuterGateReceipt) | `outer_gate_receipt.contract_snapshot.json` | `test_outer_gate_irreversibility.py::test_outer_gate_receipt_contract_frozen` | **G6** |
| 12 | `backend/contracts/v2_refusal.py` (V2RefusalEnvelope) | `v2_refusal_envelope.contract_snapshot.json` | `test_v2_gate_refusal_cumulative.py::test_v2_refusal_envelope_contract_frozen` | **G6** |
| 13 | `backend/contracts/cumulative_disclosure.py` (CumulativeDisclosureLedger) | `cumulative_disclosure_ledger.contract_snapshot.json` | `test_v2_gate_refusal_cumulative.py::test_cumulative_disclosure_ledger_contract_frozen` | **G6** |
| 14 | `backend/contracts/service_1_refusal.py` (Service1Refusal) | `service_1_refusal.contract_snapshot.json` | `test_service_1_refusal_envelope.py::test_service_1_refusal_schema_frozen` | **A2** |

Additionally: `lift_manifest_schema.snapshot.json` (discipline-freeze) + `outer_gate_transform.snapshot.json` (transform-primitive stability snapshot at G6).

## 5. Communication Contract with Orchestrator
- e1_dev MUST update this file's §2 and §3 at every phase close.
- e1_dev MUST NOT modify §0, §1, §4 unless user explicitly re-blesses.
- Orchestrator will cite section numbers from this file when giving briefs.

## 6. Pending User Decisions (rolling)
- [x] ~~Adoption path for incoming fixture pair~~ — RESOLVED at G3 opening (Path 1 — Reject).
- [x] ~~Open G3?~~ — CLOSED at 2026-07-01T17:15Z.
- [x] ~~Open G4?~~ — CLOSED at 2026-07-01T18:55Z.
- [x] ~~Open G5a?~~ — CLOSED at 2026-07-02T00:00Z.
- [x] ~~Open G6?~~ — CLOSED at 2026-07-02T00:45Z.
- [ ] Open G5b (Frontend Operator Console + Consumer Terminal)?
- [ ] Deliver real RMS material for G2b?
- [ ] **Owner/DPO — unlock Targeta yield seam** (`min_efficiency_gain`, `coverage_alpha`, `held_out_set_composition`). Seam built.
- [ ] **Owner/DPO — unlock Mtafiti V3 overlay seam** (`fact_precision`, `genre_accuracy`, `inter_annotator_floor` + real labelled held-out set). Seam built.
- [ ] **DPO — set Northena Ledger retention window** (currently INDEFINITE default). Deletion invariant re-blessed alongside implementation if window is set.
- [ ] **DPO — unlock V2 cumulative-disclosure arm** (NEW at G6): set `RMS_G6_K_ANONYMITY_THRESHOLD` + `RMS_G6_L_DIVERSITY_THRESHOLD` + `RMS_G6_DP_EPSILON_BUDGET` env vars (Product v2.1 §21.2 primitives; §29.1 "Until V2 passes"; §32 pattern). Seam built + tested LOAD-BEARING when env set.
- [ ] **MEA — deliver real source-standing table**. Currently placeholder covering 8 fixture feed_ids.
- [ ] **Service 2 landing (future track):** when Service 2 (Objective-Extraction with Solva conclusion boundary) is built, seed a run that populates SolvaTrace and verify `/trace/{trace_id}` Consumer Terminal renders the Solva section correctly. Tester's G5b forward-looking suggestion — not blocking, tracked for future.
- [x] ~~Solva/Targeta/Mtafiti spec re-drop~~ — DONE at Substrate-Drop v1.
- [x] ~~Interface + UX Architecture spec landing~~ — DONE at Substrate-Drop v1 addendum.

## 7. Last Orchestrator ⇄ User Exchange (rolling, one paragraph)

User dispatched **A2 — Service1Refusal envelope + composition_below_floor branch** with eight locked decisions (D1b include new branch, D2a static hint table, D3a flat JSONResponse, D4b 14th freeze, D6a Ring-5-upstream-boundary Path A, D7a max reduction, D8a `len(eligible)==0` trigger, X1 discipline observation tracked separately). e1_dev executed the phase autonomously to acceptance gate. STEP 0 preconditions: CI baseline 347/347 green; §204/§247 wording check confirmed source specs prescribe content categories only (`corroboration / accountable source` in `< >` placeholder syntax), NOT verbatim strings — HAZARD-STOP (f) did NOT fire, user's rewrite is authoritative. Shipped: `contracts/service_1_refusal.py` (14th frozen contract, 7 fields: outcome discriminator + reason + run_id + trace_id + asked + supported_class + what_would_raise_it); `service_1_refusal.contract_snapshot.json` (11th snapshot file); `services/service_1/refusal_hints.py` (static per-reason table, three user-locked strings); service layer wired at all three refusal sites via `Service1Refusal(reason, run_id, trace_id, *, asked, supported_class, what_would_raise_it)` exception + `_max_supported_class` helper reading Ring-5-governed per-unit `defensibility_class` with local `_CLASS_ORDER` mirror (D6a doctrine, no `solva_depth` import — service.py docstring L10-11 `"Does NOT invoke Solva"` intact); new `composition_below_floor` raise site fires on `if not eligible:` after Targeta filtering (D8a); router replaced `raise HTTPException(422)` with `return JSONResponse(status_code=422, content=refusal.model_dump())` for flat top-level body (D3a); `responses={200: Service1RunSummary, 422: Service1RefusalContract}` documented on the decorator for OpenAPI; added `objective_text: str` field to `Service1RunRequest` and plumbed through 5 test call-sites (`test_service_1_invariants.py` 4 sites + `test_trace_lens_readonly.py` 1 + `test_trace_lens_cross_engine_correlation.py` 2). Test suite: 7 new HTTP-layer invariant tests + 1 snapshot invariant, all in `test_service_1_refusal_envelope.py`, all green (validation-vs-refusal distinguishability via `body.outcome === "refused"` field-check, NOT status code; infrastructure-fault guard proves 500-not-refusal; D6a governed-not-recomputed via signal-ring mutation test; D7a max-not-min via mixed-class fixture). `.github/workflows/g0-gate.yml` gained `workflow_dispatch`. `docs/handoff/backend_contract_surface_v1.md` realigned across §1 (13→14), §1.14 new subsection, §2 route #17 error cell (fixed self-contradicting "500 (not 500)"), §2.1 request/response examples corrected (previous doc showed `ObjectiveRequest`-shape not `Service1RunRequest`-shape) + three refusal branches enumerated + validation-vs-refusal distinguishability + infrastructure-fault non-conflation, §4 Service 1 row updated with 7-field envelope reference, §5.3 tightened per user brief ("Verified across contracts" → "these payloads carry the class; Gate 1's build-time test enforces completeness"), §5.4 backed by the new envelope, §8 signature bumped to `-v1.1-a2-e1_dev-20260702T021500Z` + CI 340→355. `docs/lift_manifest.json` gained 4 new entries. `BUILD_JOURNAL.md` A2 close entry filed with strict §0 inline discretionary enumeration. **`make ci` = 355/355 green** (delta +15 from G6: +7 handoff route + +7 A2 refusal tests + +1 A2 snapshot invariant). No HAZARD-STOPs raised. Backend surface still FROZEN; A2 was a targeted additive amendment, not a re-open. Parked; G5b dispatch to `e1_web_frontend_dev` still awaits user go with the amended artifact validated.
