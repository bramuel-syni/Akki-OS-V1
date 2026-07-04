# RMS Intelligence System — PRD

## Original problem statement
Stakeholder-directed "Read-First, Reuse-Always" build of the RMS Intelligence System on top of the `Akki-Executive-New-Arch` legacy substrate (now `/reference/akki-legacy/`). Phases G0 → G6 with strict doctrine: frozen contracts via Pydantic + JSON snapshots, all LLM calls through the SyniSense Shield chokepoint, spike vs production hours kept distinct, Rule-2 STOP if net-new code outgrows lifted-substrate lines.

## Current gate status (2026-07-03)
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
- **Phase 3 — Admission-Refusal Envelope (unified §6.5 + future admission reasons via registry)** (2026-07-03): CLOSED. 17th frozen contract `AdmissionRefusal_v0` + versioned reason registry `admission_refusal_reasons.v0.json` (Ruling 3 pattern, NOT snapshotted) + `services/service_1/admission_refusal.py` service module + dispatch integration (Union return type). Phase 2 `form=model` scaffold 501 placeholder REPLACED by `AdmissionRefusal_v0` @422 (Condition 5 migration). Family-consistent with `Service1Refusal@v0` (outcome=refused + trace_id + reason). Doctrinal-tension resolution: `reason` is constrained `str` (not `Literal`); adding a reason = registry bump, never contract modification.
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
12. `v2_refusal_envelope@v0` (G6)
13. `cumulative_disclosure_ledger@v0` (G6)
14. `service_1_refusal@v0` (A2)
15. `objective_request_v2@v0` (Substrate-Drop v2, Part 2 / Phase 0)
16. `feasibility_result@v0` (Phase 1)
17. **`admission_refusal@v0` (Phase 3)** — unified admission-time refusal envelope; `form_not_offerable` (§6.5) is first firing reason; future admission reasons extend via `admission_refusal_reasons.vN.json` registry (never Literal-widening, never new contract).

All 17 mapped 1:1 to `.contract_snapshot.json` files under `tests/invariants/`; bijection enforced by `test_frozen_contract_snapshot_parity.py`.

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
