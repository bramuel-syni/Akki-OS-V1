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
- **Phase 3 — Admission-Refusal Envelope (unified §6.5 + future admission reasons via registry)** (2026-07-03): CLOSED. 17th frozen contract `AdmissionRefusal_v0` + versioned reason registry + service module + dispatch integration. Family-consistent with `Service1Refusal@v0`.
- **Phase 4 Stage A — Transform Layer design proposals (design-only)** (2026-07-03): CLOSED.
- **Phase 4a Stage B — §6.1 qualified-data path + shared substrates** (2026-07-04): CLOSED.
- **Phase 4b — §6.2 composed-conclusion path + 18th frozen contract** (2026-07-04): CLOSED.
- **Phase 5 Stage A — Async Delivery Contract design** (2026-07-04): CLOSED.
- **Phase 5 Stage B — Async delivery §7 implementation** (2026-07-04): CLOSED.
- **Phase 6 Stage A — Economics §8 config design (design-only)** (2026-07-04): CLOSED.
- **Phase 6 Stage B — §8 economics implementation** (2026-07-04): CLOSED.
- **Phase 7 Stage A — Shaping Wizard §3.3 design (design-only)** (2026-07-04): CLOSED. Design proposal at `/app/docs/stage_a_proposals/phase_7_stage_a.md`. Owner ruled on 7 escalations (E1-E7).
- **Phase 7 Stage B-1 — Shaping wizard §3.3 operator variant + 4 net-new frozen contracts + license-class Option C wrap + provenance-preservation shared-derivation module** (2026-07-04): CLOSED. Live at `POST /api/wizard/operator/{session, {sid}/turn, {sid}/agent-assumption, {sid}/commit-review, {sid}/freeze}` + `GET /api/wizard/operator/{sid}`. Uses `DeterministicStubAgent` (NO LLM). 4 new frozen contracts: `WizardCommitState_v0` (23) + `OperatorTurn_v0` (24) + `AgentAssumption_v0` (25) + `CommittedValue_v0` (26). Mechanical parity 22→26. 22 prior contracts SHA-identical. License-class Option C wrap additive; fallback body slice byte-identical. Owner E5 wizard-transcript retention class marker LB. Owner E7 provenance-preservation shared-derivation module LB. 2 new Standing Owner Dispositions at §0.1: `Agent-pluggable-with-stub-agent-first` + `Visibility-not-prohibition`. On-disk canonical `/app/docs/close_reports/phase_7_stage_b_1.md` SHA-256 `b34fc38eb69804165dcf1a9eb65351a0c6b0a4648895c17e5c4b408b7b635d9e`.
- **Item 4 HAZARD-STOP (fixture-supersede posture)**: RESOLVED at 2026-07-03 per Ruling 1.
- **G2b — Convergence Quality on Real Hour**: UNBLOCKED but parked on real RMS material.

## Legacy count anchors (historical; superseded by "Frozen contracts (22)" below)
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

## Frozen contracts (26)
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
17. `admission_refusal@v0` (Phase 3)
18. `composed_conclusion@v0` (Phase 4b, 2026-07-04)
19. `northena_ledger_row@v1` (Phase 5 Stage B, 2026-07-04)
20. `async_delivery_accepted@v0` (Phase 5 Stage B, 2026-07-04)
21. `quote_envelope@v0` (Phase 6 Stage B, 2026-07-04)
22. `async_delivery_accepted@v1` (Phase 6 Stage B, 2026-07-04)
23. **`wizard_commit_state@v0` (Phase 7 Stage B-1, 2026-07-04)** — 23rd frozen contract; outer boundary of the operator-variant shaping wizard; Guard 1/2 enforced at freeze-time via `_validate_freeze_time_invariants`; `variant: Literal["operator", "buyer"]` set at v0 for forward-compat with B-2 buyer landing.
24. **`operator_turn@v0` (Phase 7 Stage B-1, 2026-07-04)** — 24th frozen contract; append-only per-turn record; `feasibility_snapshot_ref` structural min_length=1 (Guard 3 enforcement point).
25. **`agent_assumption@v0` (Phase 7 Stage B-1, 2026-07-04)** — 25th frozen contract; append-only agent-inference record; `inferred_value: Any` loose-as-frozen at v0.
26. **`committed_value@v0` (Phase 7 Stage B-1, 2026-07-04)** — 26th frozen contract; anti-laundering source-tag XOR invariant via `model_validator`: exactly one of `operator_turn_ref` / `agent_assumption_id` is set. Per Owner E3 ruling: freezing this shape is what makes the source-tag anti-laundering seam load-bearing.

All 26 mapped 1:1 to `.contract_snapshot.json` files under `tests/invariants/`; bijection enforced by `test_frozen_contract_snapshot_parity.py`.

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
`pytest -q` = **613/613** green at 2026-07-04 (Phase 7 Stage B-1 close). Delta from Phase 6 Stage B (550): +63 (30 wizard invariant gates + 22 parametrised prior-source byte-identity + 3 slice/file gates + 8 parametrised ask-vs-propose expansions + 2 count/sanity gates).
