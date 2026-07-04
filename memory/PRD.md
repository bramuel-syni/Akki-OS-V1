# RMS Intelligence System — PRD

## Original problem statement
Stakeholder-directed "Read-First, Reuse-Always" build of the RMS Intelligence System on top of the `Akki-Executive-New-Arch` legacy substrate (now `/reference/akki-legacy/`). Phases G0 → G6 with strict doctrine: frozen contracts via Pydantic + JSON snapshots, all LLM calls through the SyniSense Shield chokepoint, spike vs production hours kept distinct, Rule-2 STOP if net-new code outgrows lifted-substrate lines.

## Current gate status (2026-07-04)
- **G0 — Foundation & Contracts**: CLOSED.
- **G0.5 — V1 Spike Harness Construction**: CLOSED.
- **G1 — Defensibility Detection Substrate**: CLOSED.
- **Pre-G2 hardening**: CLOSED.
- **G2a — Northena Reshape**: CLOSED (2026-07-01).
- **Substrate-Drop v1** (2026-07-01T15:39Z): CLOSED.
- **G3 — Solva Reshape + Layer C** (2026-07-01T17:15Z): CLOSED.
- **G4 — Mtafiti + Targeta + Service 1 v1 (Day-Zero composed)** (2026-07-01T18:55Z): CLOSED.
- **G5a — Backend routes + Trace-lens** (2026-07-02T00:00Z): CLOSED.
- **G6 — Outer Gate + V2 gate** (2026-07-02T00:45Z): CLOSED.
- **Freeze-and-Handoff artifact** (2026-07-02T01:00Z): SHIPPED.
- **Handoff-Download Route** (2026-07-02T01:30Z): SHIPPED.
- **A2 — Service1Refusal envelope + composition_below_floor branch** (2026-07-02T02:15Z): CLOSED.
- **G5b — Frontend Operator Console + Consumer Terminal** (2026-07-02T10:00Z): CLOSED.
- **Docs-Pass (Source-Spec Corrections)** (2026-07-02): CLOSED.
- **Substrate-Drop v2 (Part 1 — backfill + parity invariant + Part 2 Phase 0 `ObjectiveRequest_v2`)** (2026-07-03): CLOSED.
- **Phase 1 — Estate Feasibility Query** (2026-07-03): CLOSED. `FeasibilityResult_v0` 16th frozen contract; `POST /api/mtafiti/feasibility` live.
- **Phase 2 — Shape-Responsive Execution Scaffold** (2026-07-03): CLOSED. `services/service_1/dispatch.py` + `POST /api/service_1/v2/dispatch` (501 + placeholder) live. No new frozen contracts (DispatchResult UNFROZEN per Ruling 3).
- **Phase 3 — Admission-Refusal Envelope (unified §6.5 + future admission reasons via registry)** (2026-07-03): CLOSED. 17th frozen contract `AdmissionRefusal_v0` + versioned reason registry + service module + dispatch integration. Family-consistent with `Service1Refusal@v0`. Doctrinal-tension resolution: `reason` is constrained `str` (not `Literal`); adding a reason = registry bump, never contract modification.
- **Phase 4 Stage A — Transform Layer design proposals (design-only)** (2026-07-03): CLOSED. Delivered full-text artifacts on the second close (first vacated). Verdicts: 4a/4b split, ComposedConclusion@v0 freeze at 4b, §6.1 payload UNFROZEN at 4a.
- **Phase 4a Stage B — §6.1 qualified-data path + shared substrates** (2026-07-04): CLOSED. Live route: `POST /api/service_1/v2/dispatch` returns `Union[DispatchResult @501, AdmissionRefusal_v0 @422, QualifiedDataPayload @200]`. Zero new freezes (parity stays 17); three additive reason codes via v1 registry bump. Three Owner rulings landed inline. CI 434/434 green.
- **Phase 4b — §6.2 composed-conclusion path + 18th frozen contract** (2026-07-04): CLOSED. 18th frozen contract `ComposedConclusion_v0` landed (snapshot SHA `a85eaf95...`). Wire Union widened: 5 arms (adds `ComposedConclusion_v0 @200` and `Service1Refusal_v0 @422` for `composition_below_floor` per §6.2.6). Condition B1 LOAD-BEARING: `conclusion_class` threaded from Solva boundary; no local recomputation (AST + grep-negative verified). §6.1.6-vs-§6.2.6 reading documented in-module: §6.1.6 hard input filter applies to §6.1 only; §6.2 enforces standard at conclusion class. CI 446/446 green. On-disk canonical `/app/docs/close_reports/phase_4b.md` SHA-256 `2781313b28e152277e41f135801e4f5e3f0a3b083aa50a53ef3ab634c9cfb6c7`.
- **Phase 5 Stage A — Async Delivery Contract design** (2026-07-04): CLOSED. Design-only proposal at `/app/docs/stage_a_proposals/phase_5_stage_a.md`. Owner returned 4 rulings + 3 Standing Owner Dispositions verbatim at Stage B open.
- **Phase 5 Stage B — Async delivery §7 implementation** (2026-07-04): CLOSED. 2 new frozen contracts: `NorthenaLedgerRow_v1` (contract 19, supersets v0 + adds `terminate_cancelled` decision axis; snapshot SHA `0ec71fde...`) + `AsyncDeliveryAccepted_v0` (contract 20, snapshot SHA `d2027c02...`). Live routes: `POST /api/objectives` (202 AsyncDeliveryAccepted_v0 | 422 AdmissionRefusal_v0 | 503 infra-not-refusal) + `GET /api/objectives/{id}` (wire-shape polling) + `POST /api/objectives/{id}/cancel` (thin 4-key cancelled envelope). v2 dispatch fresh-fork Union widened to include `AsyncDeliveryAccepted_v0 @202`. 5-state machine on `objectives_async_state` Mongo collection with asyncio.Queue worker substrate (4 workers, maxsize 1024) + kill-and-restart recovery + HMAC-SHA256 webhook signing + 5-retry bounded backoff. 18 PRIOR frozen contract sources byte-identical verified. Three new Standing Owner Dispositions landed at §0.1: frozen-field-changes-as-new-versions + infra-not-refusal + cancellation-is-a-state-not-a-refusal. CI 504/504 green; `make ci` PASSED. On-disk canonical `/app/docs/close_reports/phase_5_stage_b.md` SHA-256 `49ce2262b1f6f6e244bb7294b165734f6de31a1b176a55f73dd8871e94a2def5`.
- **Item 4 HAZARD-STOP (fixture-supersede posture)**: RESOLVED at 2026-07-03 per Ruling 1 — SYNTHETIC v1 = standing test substrate; real material = operational/benchmark input; no supersede semantics.
- **G2b — Convergence Quality on Real Hour**: UNBLOCKED but parked on real RMS material.

## Frozen contracts (17)
1. `five_rings@v0`
2. `objective_request@v0`
3. `qualification_matrix@v0`
4. `signal_ring_dimensions@v0`
5. `extraction_params@v0`
6. `northena_ledger_row@v0`
7. `mtafiti_registry_record@v0` (G4)
8. `targeta_mining_plan@v0` (G4)
9. `trace_lens_envelope@v0` (G5a)
10. `lift_manifest_envelope@v0` (G5a)
11. `outer_gate_receipt@v0` (G6)

## Frozen contracts (20)
1. `five_rings@v0`
2. `objective_request@v0`
3. `qualification_matrix@v0`
4. `signal_ring_dimensions@v0`
5. `extraction_params@v0`
6. `northena_ledger_row@v0`
7. `mtafiti_registry_record@v0` (G4)
8. `targeta_mining_plan@v0` (G4)
9. `trace_lens_envelope@v0` (G5a)
10. `lift_manifest_envelope@v0` (G5a)
11. `outer_gate_receipt@v0` (G6)
12. `v2_refusal_envelope@v0` (G6)
13. `cumulative_disclosure_ledger@v0` (G6)
14. `service_1_refusal@v0` (A2)
15. `objective_request_v2@v0` (Substrate-Drop v2, Part 2 / Phase 0)
16. `feasibility_result@v0` (Phase 1)
17. **`admission_refusal@v0` (Phase 3)** — unified admission-time refusal envelope; `form_not_offerable` (§6.5) is first firing reason; future admission reasons extend via `admission_refusal_reasons.vN.json` registry (never Literal-widening, never new contract).
18. **`composed_conclusion@v0` (Phase 4b, 2026-07-04)** — governed composed-conclusion envelope for §6.2; `conclusion_class` threaded from Solva boundary (Condition B1 LOAD-BEARING); pairs with `Service1Refusal@v0(reason=composition_below_floor)` for below-floor at conclusion class per §6.2.6.
19. **`northena_ledger_row@v1` (Phase 5 Stage B, 2026-07-04)** — first application of Standing Owner Disposition `frozen-field-changes-as-new-versions`; supersets v0 validation set + adds `terminate_cancelled` to Literal decision axis; v0 file preserved byte-identical at SHA `68349bb0...`.
20. **`async_delivery_accepted@v0` (Phase 5 Stage B, 2026-07-04)** — v3 §7 §7.1 acceptance envelope for `POST /api/objectives` @202; 5-field wire shape (`objective_id`, `status="accepted"`, `delivery_estimate`, `trace_id`, `accepted_at`, optional `quote`).

All 20 mapped 1:1 to `.contract_snapshot.json` files under `tests/invariants/`; bijection enforced by `test_frozen_contract_snapshot_parity.py`.

## Backlog (prioritised)
- **P0 — G5b Frontend Operator Console + Consumer Terminal** (awaits user go): 4 operator surfaces (Portfolio, Runs, Sources, Discipline) + Consumer Terminal v0. Backend routes shipped at G5a + G6 + A2; G5b is the surface that renders them.
  - Now backed by `Service1Refusal@v0` for the "asked / supported class / what would raise it" §5.4 render obligation on Service-1 refusals — frontend keys on `body.outcome === "refused"`, NOT status code.
- **P1 — G2b Convergence Quality on Real Hour** (gated on real RMS material from stakeholder).
- **P2 — X1 discipline observation** (parked): consolidate `services/solva_depth/pipeline.py:75-76` redundant `conclusion_class(lb)` recompute into `Refusal.computed_class` read. Non-blocking.
- **Governance-pending (config-only)**:
  - Owner thresholds — Targeta yield seam.
  - Owner + DPO thresholds — Mtafiti V3 overlay seam.
  - DPO — Northena Ledger retention window.
  - DPO — V2 cumulative-disclosure arm env vars.
  - MEA — real source-standing table.

## Hard rules (carry forward)
1. **Held-out hour**: V1 harness `spike_hour` and `production_hour` must be distinct.
2. **Reshape→Rewrite STOP** (Rule 2 v2) + **§0-strict inline discretionary enumeration** (from G6 forward).
3. **G3 before G4** (build time); runtime order is G4 → G3.
4. **V3 re-run at G4** against real source-standing.
5. **Read the cousin before writing the reshape**.
6. **Contract immutability**: any field change requires stakeholder bless. Class docstrings on Pydantic models leak into JSON-Schema.
7. **Timestamps record when, not what.**
8. **Stochastic extraction is non-reproducible-by-construction.**
9. **Governors orthogonal** (mandate §13.11).
10. **Read-only route invariant** (G5a) + **Handoff route read-only invariant** (post-G6).
11. **Outer-gate irreversibility** (G6): egress carries no plaintext identifiers.
12. **V2 refusal terminality** (G6): V2 refusal envelope IS the record; no partial-egress ever.
13. **Service 1 refusal is first-class** (A2): `outcome="refused"` at top level, HTTP 422; distinct from validation-422 by presence of `outcome` field (NOT by status code); infrastructure faults (500) must never carry `outcome === "refused"`.

## Tech stack
- Backend: FastAPI, Python 3.11, Pydantic v2, MongoDB (Motor).
- Frontend: React 18 + CRACO + Tailwind + Radix.
- LLM: Emergent Universal Key via `emergentintegrations` — all calls through Shield chokepoint.
- Test transport: `httpx.AsyncClient(ASGITransport(app))`.

## Key endpoints (21 registered `/api/*`)
- `GET /api/health`
- `GET /api/system/state`
- `GET /api/contracts/{five_rings,objective_request,qualification_matrix}`
- `GET /api/northena/status`, `/api/northena/ledger/open_runs`, `/api/northena/ledger/by_run/{run_id}`, `/api/northena/trace/{trace_id}`
- `GET /api/discipline/lift_manifest`
- `GET /api/handoff/backend_contract_surface_v1` (post-G6)
- `POST /api/service_1/run` (200 → `Service1RunSummary`; 422 → `Service1Refusal@v0` with `outcome="refused"`) / `GET /api/service_1/run/{run_id}`
- **`POST /api/service_1/v2/dispatch`** (Phase 2, 501 + dispatch envelope + governed placeholder) — accepts `ObjectiveRequest_v2`, returns `DispatchResult` (unfrozen)
- `POST /api/mtafiti/feasibility` (Phase 1) — accepts `Reach`, returns `FeasibilityResult_v0`
- `GET /api/solva/status`
- `GET /api/v1/status` / `GET /api/v3/status`
- `GET /api/openapi.json`, `/api/docs`, `/api/redoc`

## CI
`make ci` = **402/402** green at 2026-07-03 (Phase 2 close). Delta from Phase 1 (387): +15 Phase 2 tests (4 named gates + 5 positive-path + 2 wire-shape + 3 v0-untouched + 1 malformed-body).
