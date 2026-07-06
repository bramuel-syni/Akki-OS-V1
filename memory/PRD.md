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
- **Phase 7 Stage B-2 — Buyer variant + Sonnet 4.6 LLM (SonnetWizardAgent inside Shield) + dual-delta gate + Condition-A pre-LLM Guard-1 landing + Condition-2 grep-negative single-source (× 3 symbols)** (2026-07-04): CLOSED. Live at 7 endpoints `POST /api/wizard/buyer/{session, {sid}/turn, {sid}/propose, {sid}/agent-assumption, {sid}/commit-review, {sid}/freeze}` + `GET /api/wizard/buyer/{sid}`. `SonnetWizardAgent` (Claude Sonnet 4.6 via Emergent LLM Key) lives inside `services/synisense/shield/llm_router.py` — `services/wizard/*` remains LLM-free (Shield boundary preserved). Temp 0.2 live / 0.0 hermetic replay. No silent model degrade — Sonnet-unavailable → HTTP 503 (Standing Disposition `Infra-not-refusal`). Dual-delta gate (`services/wizard/dual_delta.py`, Owner E6 `Visibility-not-prohibition` mechanical application): standard/grain-changing proposals refuse `dual_delta_missing` if `price_delta` or `class_delta` absent; reach-changing proposals admissible. Owner Condition-A pre-LLM Guard-1 mandatory-tier gate on `POST /api/wizard/operator/{sid}/agent-assumption` (3 LB gates). Owner Condition-2 grep-negative single-source × 3 symbols confirms `buyer_state_machine.py` re-implements NONE of {`validate_source_tags`, `validate_guard_1_operator_mandatory_all_operator_supplied`, `_record_feasibility_snapshot`}. Zero new frozen contracts (parity 26 unchanged); zero new §0.1 Standing Dispositions (§0.1 FROZEN per Owner correction); 1 new §0.2 Plan Debt `Wizard session-ownership binding` — [Owner ruling, Phase 7 Stage B-2 dispatch, 2026-07-04]. 26 prior frozen contract sources byte-identical. 685/685 backend GREEN (baseline 613 → +72 net; intermediate block sequence 613 → 624 → 631 → 685). Rule-2 accounting: band 1600-2000 (mid ~1800); actual ~1757; WITHIN BAND (-2.4% delta). On-disk canonical `/app/docs/close_reports/phase_7_stage_b_2.md` SHA `c46186b173d813bdbdca82e98a3a13618d2a2e30aca4ceebd89503fdafb18a21`.
- **Phase 8a-lite — Ask Console (Frontend, UI Spec v1 §3 landing)** (2026-07-04): CLOSED. Live at `/`. Human-visible surface unblocked; production `yarn build` GREEN; 27 / 27 UI-Spec-v1 gate tests across 5 suites GREEN. §3.1 Ask + §3.2 Answer + §3.3 Refusal binding copy verbatim. Consumes `POST /api/service_1/v2/dispatch` via new `apiClient.dispatchV2(...)` (single-ingress preserved). Five response branches code-covered: 200 ComposedConclusion → AnswerView, 202 AsyncDeliveryAccepted → AcceptedView, 422 governed refusal → RefusalView, 422 validation-shape → InfraFaultView, 5xx/network → InfraFaultView (infra-not-refusal doctrine). NO output-form picker on Ask surface (§3.1 verbatim; 6 gates enforce absence). Legacy G5b pages archived under `src/legacy/pages/` (8 files); routes moved to `/legacy/*` (Trust receipt deep-links preserved). 3 G5b invariant gates re-landed under `src/__tests__/ui_spec_v1/` (Gate 1 Class inseparable + Gate 2 Refusal first-class + Gate 3 Single ingress). Component reuse (Owner Condition-2 posture): AskConsolePage reuses `ClassBadge` + `RefusalCard` from `src/components/*` — zero reimplementation. **Zero backend surface delta** — `pytest -q` remains 685 / 685; 26 frozen contracts byte-identical. On-disk canonical `/app/docs/close_reports/phase_8a_lite.md` SHA `bf4ba9a94f250abad61d33a842bdedf2e7c8571a3fe61b1d3323c25601dbe888`.
- **Phase 7 Stage B-3 — Wizard trilogy COMPLETE (commit-review extensions + buyer freeze ledger parity + admission handoff endpoints on both variants)** (2026-07-04): CLOSED. Live at 15 wizard endpoints across both variants (operator 6 → 7, buyer 7 → 8; adds `/handoff` on both). Commit-review body extended (both variants: `license_class_drift` soft signal; buyer only: `dual_delta_summary`). Buyer freeze at B-3 mirrors operator freeze — writes `wizard_freeze` ledger row via `record_wizard_freeze(...)` (Owner E5 seam; `data_class="wizard_transcript"` structural) + accepts optional `lawful_basis_ref` body param + returns `ledger_run_id`. NEW admission handoff endpoint `POST /api/wizard/{variant}/{sid}/handoff` — mints `ObjectiveRequest_v2` via NEW pure-fn composer `services/wizard/admission_handoff.compose_objective_request_from_frozen_state_with_proposals(...)` + POSTs to `/api/objectives` in-process via `httpx.AsyncClient(ASGITransport)` (single-source). Returns HTTP 202 AsyncDeliveryAccepted_v1 | 422 wizard_not_frozen | 422 AdmissionRefusal_v0 passthrough | 404 unknown session | 503 infra. Deterministic idempotency_key `handoff-{session_id}` → repeat handoff returns same objective_id per Phase 5 §7 guarantee (E2E verified: same objective_id=`obj-fc9c056a48c1` across two calls). Dual-delta acceptance recording (buyer only) persists through handoff into `envelope.floor_feasibility["dual_delta_summary"]` (open-shape dict per Substrate-Drop v2 Part 2 posture). Owner Condition-2 grep-negative gates × 3 confirm `admission_handoff.py` imports (does NOT reimplement) `derive_license_class` + `_record_feasibility_snapshot` + `evaluate_dual_delta`. **No new refusal codes at B-3** per Owner ruling verbatim — registered admission_refusal + service_1_refusal registries unchanged; `wizard_not_frozen` returned as an ad-hoc router-layer 422 body (NOT registered as an admission-refusal reason). Zero new frozen contracts (parity 26 unchanged); zero new §0.1 Standing Dispositions (§0.1 FROZEN); zero new §0.2 Plan Debts. 26 prior frozen contract sources byte-identical (verified by `test_prior_contract_file_exists_and_stable_at_7b_3` parametrised over 25 sources + count invariant). Shield boundary preserved (services/wizard/* remains LLM-free). services/service_1/composed_conclusion.py:316-321 UNTOUCHED (Verdict A regression preserved; slice SHA `9e4e6152...`). 740/740 backend GREEN (baseline 685 → +55 net; Block A 7 gates → Block B 13 gates → Block C 10 gates + parametrised = ~55 collected cases). Rule-2 accounting: band 800-1100 (mid ~950); actual ~1094; WITHIN BAND. Rule 2 accounting JSON extended 28 → 30 phases (transcription-only per Owner cap; served through /api/discipline/lift_manifest — verified 30 keys live). Stage A proposal on disk: `/app/docs/stage_a_proposals/phase_7_stage_b_3.md` SHA `040c4099aa031ddb4b8133ac64f301457e6bdafc13ad12cf5c58fb1ba90f4698`. On-disk canonical `/app/docs/close_reports/phase_7_stage_b_3.md` SHA `ea12517cec7deee48818a097e942d08601fda5a0f381e215a7df2c508c801c30`. **Wizard trilogy (B-1 + B-2 + B-3) CLOSED.**
- **Phase 8 Stage B-3 — Engineer §4 + Buyer §5 verbatim + buyer session-binding wire-up + Engineer key-grant CRUD backend + load-bearing wire-shape gate (D4b UNFROZEN) + ledger integration + first-commit gates for §2 coverage** (2026-07-05): CLOSED.
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
`pytest -q` = **855/855** green at 2026-07-05 (Phase 8 Stage B-4 close). Delta from Phase 8 Stage B-3 (818): +37 (tier_lock Path A ledger 3 + auth-reconciliation parametrised 15 + pending-seams enumeration 6 + audit-trail 5 + Path B honest 501 6 + seeded-admin baseline 1 + retired-header zero-effect 1). Frontend Jest ui_spec_v1: 72/72 (+12 vs B-3: 6 fixture-schema + 6 §6 binding-copy verbatim). Playwright chromium: 24/24 (+8 vs B-3: 3 §6.1 Home + 3 §6.2 Change-a-rule + 2 §6.3 Audit-trail).

## Phase 8 Stage B-4 (Implementation dispatch closed, 2026-07-05 · ACCEPTED BY OWNER 2026-07-05)
- **Status:** CLOSED, ACCEPTED (Master Admin §6 surface verbatim + auth reconciliation retiring `RMS_MASTER_ADMIN_TOKEN` + Path A tier_lock ledger integration + Path B honest 501 for model_version and fleet_policy + real seams-pending enumeration + §4.2 fixture-schema Jest invariant). Owner acceptance verbatim: "Step 1 — Accept B-4. Push at this close."
- **On-disk canonical:** `/app/docs/close_reports/phase_8_b_4.md` SHA-256 (pre-acceptance) `3cf03f809a7e19f9d275e2caddc3f1f75d68d29c33190504f4c37377892591b5` → (post-acceptance-footer) `21d2f5193cfb53fbb3ec2c35f293e78f7bd535f446a969137b4bad8758fdb3b8`.
- **Overage split-disposition (Owner-ruled 2026-07-05):** mandate-forced portion (verbatim §6 binding copy + first-commit gates) RATIFIED on record; test-lump underestimate portion (888 actual vs ~330 estimated, 2.7×) is ORCHESTRATOR-OWNED estimation miss. **Standing correction (binding on every future dispatch; internal to orchestrator template, NOT a §0.1 disposition):** Stage-A sizing enumerates the test matrix (endpoints × postures × cases), never a test-LoC lump. B-4 is post-signal where B-1 was pre-signal — same magnitude, different meaning.
- **Retroactive B-3 cross-reference (appended at B-4 close acceptance 2026-07-05):** fixture shape drifted at B-3 → CAUGHT AND FIXED at B-4 fixture-schema gate. B-3 close SHA (pre-acceptance) `c2863974...` → (post-acceptance-footer) `a31b5a9d43c0563140a73762789f765390187052ebd4e24b47d9bb6a528f7215`.
- **Audit-trail rendering:** inline collapsible pre-block RATIFIED (Owner: "modal/drawer is below ruling altitude, no pivot"). Three binding rules verified — never primary display, one click away, full on open.
- **CI (last Phase 8 milestone before commercial cut):** backend 855/855; Jest 72/72; Playwright chromium 24/24. Parity 26/26. Substrate-drop 9/9.
- **New canonical mandates ingested 2026-07-05 (record-only, no code changes):** `/app/docs/mandates/RMS_UI_Specification_v2_1.md` SHA `ef6da4b498117608a3091033b5cfa43571ad8a7a38b5954cae7c4a1a698de5e2` (SUPERSEDES v1); `/app/docs/mandates/RMS_Build_Completion_Requirements_v1_4.md` SHA `d1f49bc5d7cbf1dea044ca4069a1dc2d45f01876e531b7500d860ae3f48aebdd`. `RMS_UI_Specification_v1.md` marked SUPERSEDED at file top (retained for archive per doctrine).
- **Awaiting:** Owner push confirmation at this close. B-5 (Regulator/DPO §7 per UI Spec v1) SUPERSEDED by UI Spec v2.1 mandate. Two Steps queued and NOT begun per Owner Part-1-only dispatch: Step 2 (commercial cut per BCR v1.4 §12) waits for push confirmation; Step 3 (B-5a Compliance Console read/prove per UI Spec v2.1 §4.1-4.3) waits for cut close.

## Phase 8 Stage B-4 (Implementation dispatch closed, 2026-07-05)
- **Status:** CLOSED (Master Admin §6 surface verbatim + auth reconciliation retiring `RMS_MASTER_ADMIN_TOKEN` + Path A tier_lock ledger integration + Path B honest 501 for model_version and fleet_policy + real seams-pending enumeration + §4.2 fixture-schema Jest invariant).
- **On-disk canonical:** `/app/docs/close_reports/phase_8_b_4.md` SHA-256 `3cf03f809a7e19f9d275e2caddc3f1f75d68d29c33190504f4c37377892591b5`.
- **CI:** backend 855/855 (baseline 818 → +37 net); frontend Jest 72/72 (baseline 60 → +12); Playwright chromium 24/24 (baseline 16 → +8); parity 26/26; substrate-drop 9/9.
- **Auth reconciliation (Owner Load-bearing Condition 1):** Highest-privilege surface uses JWT `master_admin` role check exclusively; `RMS_MASTER_ADMIN_TOKEN` and `X-RMS-Master-Admin` header retired. Zero production consumers remaining. Verified by grep-negative gate + `test_retired_master_admin_header_has_zero_runtime_effect` (401 auth_missing when header sent without JWT).
- **Path A ledger integration (`POST /api/pricing/tier_lock`):** Writes `NorthenaLedgerRow_v1` row with `stamp_audit.data_class="master_admin_rule_change"` + versioned marker file `services/economics/tier_lock.vN.json` + idempotent per `(rule_id, idempotency_key)` via deterministic run_id. Three P0 gates GREEN.
- **Path B honest 501 (`POST /api/pricing/model_version`, `POST /api/fleet/policy`):** Both return 501 with `{reason: requires_versioned_file_change_by_owner, detail: <plain language>}`. Detail is plain language — no `vN.json`, no `bump`, no config syntax; ends with "Contact Owner. No change applied.". Six parametrised gates GREEN.
- **Real seams-pending enumeration (`GET /api/master_admin/pending_seams`, Owner amendment):** Reads config-presence for 5 seams — Targeta yield / Mtafiti V3 / Northena retention / V2 cumulative-disclosure / MEA source-standing. Baseline (no env vars) → count=5; setting all env vars for a seam closes it; ordering matches mockup precedent.
- **§4.2 fixture-schema Jest invariant (Owner amendment):** Reads `.contract_snapshot.json` neighbors via `fs.readFileSync`; subset property-name assertion across 3 fixture-contract pairs. Fixtures in `EngineerFirstCallPage.js` refreshed to align with ComposedConclusion_v0 + Service1Refusal_v0 + AsyncDeliveryAccepted_v1. "Marked as illustration" now invariant, not assertion.
- **§6 surface verbatim:** MasterAdminHomePage §6.1 (plural-aware pending banner + prompt "What do you want to do?" + 6 binding-label buttons + footer link "See everything I've changed — every action is recorded."). ChangeARulePage §6.2 (one-sentence rule descriptor + Off/On + What-changes info box + commit button natural-language + post-commit binding copy "Recorded as your change, with today's date."). AuditTrailPage §6.3 (confirmation line + recent actions rows + See full diff collapsed-by-default + footer binding copy "Every row carries its full diff. This trail is itself append-only and readable by the regulator surface.").
- **Files touched:** 5 new backend Pytest gates + 3 new frontend §6 pages + 2 new Jest gates + 3 new Playwright smokes + modified pricing.py (JWT swap + Path A + Path B) + modified test_phase_6_stage_b_economics Gate 16 + modified apiClient.js + App.js + EngineerFirstCallPage.js (fixture export + shape alignment) + updated engineer §4.2 smoke + updated rule2_accounting.json + updated PRD.md + new close report. Total ~2,690 raw LoC.
- **Rule 2 v2 accounting:** Anchored band 1,300-1,800 (Owner amended +100 for seams-pending banner) → 2,690 actual → +49% ABOVE top-of-band → `snapshot_lloc_in_band=no`. Overage composition attested honestly in close report §5 (all mandate-forced by first-commit gate mandate + §6 binding-copy verbatim + Condition-2 auth-taxonomy parametrisation).
- **§0.2 status:** No new debts arose. Owner amendment: seams-pending banner is NOT a plan-debt; the endpoint reads real config-presence for 5 pre-declared seams.
- **Standing constraints preserved:** 26 frozen parity byte-identical; §0.1 unchanged; Shield boundary preserved (services/master_admin imports zero LLM libraries); 4-code auth-refusal registry unchanged (0 new codes at B-4); Playwright chromium-only; shared §8 barrel consumed not reimplemented; first-commit gating ratified as standing operational pattern; Ruling 4 shared-derivation preserved.
- **Next:** Owner ratification of B-4 close → Phase 8 Stage B-5 (Regulator/DPO §7 surface) dispatch.

## Phase 8 Stage B-3 (Implementation dispatch closed, 2026-07-05)
- **Status:** CLOSED (implementation; Engineer §4 + Buyer §5 verbatim + Engineer key-grant CRUD backend + load-bearing wire-shape gate under D4b UNFROZEN + ledger integration + buyer session-binding decorator wire-up + first-commit coverage gates for B-2 §2 surfaces).
- **On-disk canonical:** `/app/docs/close_reports/phase_8_b_3.md` SHA-256 `c2863974bf52f69ff8b7256ad1bae07854a546526672c2d099305a98d01bec22`.
- **CI:** backend 818/818 (baseline 791 → +27 net); frontend Jest ui_spec_v1 60/60 (baseline 47 → +13 net across B-3 first commit + Block 3); Playwright chromium 16/16 (baseline 1 → +15 net across §2 first-commit gates + §4/§5 same-commit gates per Owner Condition 1); parity 26/26; substrate-drop 9/9.
- **Owner D4b ruling ratified (2026-07-05):** `EngineerKeyGrantRegistration` UNFROZEN under 4a §6.1 precedent — container stays runtime Pydantic; NEW `tests/invariants/test_engineer_key_grant_load_bearing_wire_shape.py` pins 7 governance-key fields (grant_id / key_class / path / floor / scope / lawful_basis_ref / revoked_at) presence + name + type; lifecycle-additive tolerance test explicitly asserts gate does NOT reject new lifecycle fields (expires_at, delegation, renewed_at, per-endpoint scoping). Container's unfrozen status is contingent on this gate; without it, freeze would be the ruling.
- **Ledger integration (Owner D4b P0 condition):** `services/auth/engineer_key_grant_ledger.record_engineer_key_grant_event(event_type, grant, trace_id)` writes `NorthenaLedgerRow_v1` rows via `stamp_audit.data_class="engineer_key_grant"` sidecar pattern; idempotent per (trace_id, run_id) with deterministic `run_id = f"engineer-key-grant-{event}-{grant_id}"`. Three P0 gates GREEN: issuance emits ledger row / revocation emits ledger row / repeat calls with same (event_type, grant_id, trace_id) return same run_id and do NOT double-write.
- **Owner Condition 1 (first-commit gating) ratified as standing doctrine:** surfaces do not land ungated with smokes deferred a sub-stage. B-2's hole does not repeat. Engineer §4 + Buyer §5 surfaces landed WITH their Playwright chromium smokes IN THE SAME COMMIT (8 new smokes for §4/§5 in Block 3).
- **Owner Condition 2 (E2 taxonomy over grant endpoints) satisfied:** grant CRUD 403 responses use the closed 4-code registry (`auth_missing / auth_expired / auth_scope_insufficient / auth_identity_mismatch_for_wizard_session`); NO new codes at B-3; body shape `{reason, detail}` only, NO `outcome` key, NO governance-refusal discriminator. Parametrised gate over 3 grant endpoints × 2 auth postures GREEN.
- **Owner Condition 3 (§4/§5 verbatim + dual-delta pair) satisfied:** §4.2 binding copy VERBATIM "There is no response shape in which the claim is separable from its class. Infrastructure faults return 500 and are never rendered as refusals."; §4.3 footer VERBATIM "Key scope is enforced server-side on every call."; §5.2 framing VERBATIM "Every acquisition passes the outer gate. These checks are what make the data lawfully yours to use."; §5.2 footer VERBATIM "If any check fails, the acquisition is refused with the reason and a path forward — never partially delivered."; §5.1 dual-delta pair rendering per E6 Visibility-not-prohibition — {price_delta, class_delta} rendered together on the buyer rail, never one without the other. 4 Jest verbatim-copy gates GREEN + 8 Playwright smokes GREEN.
- **Buyer session-binding wire-up:** `services/auth/session_binding.py` decorator now wired across ALL 7 buyer wizard endpoints (POST /session-create binds identity; POST /{sid}/turn + /propose + /agent-assumption + /commit-review + /freeze + /handoff + GET /{sid} check ownership via `_check_session_ownership_or_deny`; mismatch → 403 auth_identity_mismatch_for_wizard_session). §0.2 Plan Debt "buyer session-binding wire-up" (rollup under session-ownership resolution) — RESOLVED at B-3. 9-test parametrised gate GREEN.
- **Retroactive B-2 record cross-reference:** EstateCheckChip regression shipped at B-2 (component prop named `ref` shadowed React's special `ref` prop, silently dropping the estate-check chip in React 18 dev/strict mode) → CAUGHT AND FIXED at B-3 first commit (prop rename `ref` → `snapshotRef`; 2 lines changed in `CommissionWizardPage.js`). Footer appended to `/app/docs/close_reports/phase_8_b_2.md` per Owner ruling verbatim. Mirror pattern (B-1 Playwright NOT-LANDED → LANDED at B-2) preserved.
- **Files touched:** 3 new backend source (engineer_key_grant_ledger + engineer_key_grant_service + routers/engineer) + 4 new backend test files + 6 new frontend §4/§5 pages + 3 new Playwright smokes + 1 new Jest binding-copy verbatim gate + 5 new Block-1 first-commit gates (3 Playwright + 2 Jest) + 2 modified backend (server + wizard_buyer) + 3 modified frontend (apiClient + App + CommissionWizardPage regression fix) + 3 modified docs/memory + 1 new close report + 1 retroactive footer in phase_8_b_2.md. Total ~2,896 raw LoC (within Owner-anchored band 1,900-2,900, ~99.9% of top-of-band, no Rule-2 stop-and-judge triggered).
- **Next:** Owner ratification of B-3 close → Phase 8 Stage B-4 (Master Admin surface per UI Spec §6) dispatch. First-commit gating pattern applies to all future dispatches.

## CI (superseded by B-3 above)
`pytest -q` = **740/740** green at 2026-07-04 (Phase 7 Stage B-3 close). Delta from Phase 7 Stage B-2 (685): +55 (Block A buyer freeze ledger parity + commit-review extensions 7 gates + Block B admission_handoff.py composer + /handoff endpoints on both variants 13 gates + Block C frozen-contract posture + regressions 10 gates + parametrised expansions: Condition-2 grep-negative × 3 symbols + prior-contract × 25 files = ~55 collected new cases).

## Phase 8 Stage B-2 (Implementation dispatch closed, 2026-07-05)
- **Status:** CLOSED (implementation; Operator surface UI Spec §2 verbatim + session-binding decorator on operator wizard + GET /api/operator/status + scope-enforcement gate PAIR on POST /v2/dispatch + Playwright completion first commit).
- **On-disk canonical:** `/app/docs/close_reports/phase_8_b_2.md` SHA-256 `4a99dbf35cfda8f9207e1b2e0b18a9f4237bc5243c5235bc9056b3e60f04a305`.
- **CI:** backend 791/791 (baseline 777 → +14 net); frontend Jest 47/47 unchanged; Playwright chromium smoke 1/1 EXECUTED (was config-only at B-1); parity 26/26; substrate-drop 9/9.
- **First commit (Owner-mandated before any surface work):** `yarn add -D @playwright/test@1.61.1` + `npx playwright install chromium --with-deps` + renamed e2e spec to `.ts` per Owner verbatim + `test:e2e` script + smoke executed GREEN. Retroactive note: Playwright gate was CONFIG-ONLY at B-1; LANDED at B-2 first commit.
- **UI Spec §2 verbatim (no partial rendering):** §2.1 Operator Home (calm header + Commission-objective button + status-line binding-copy + at-most-one attention card + Running list + capacity strip reading `/api/fleet/policy`); §2.2 Commission Wizard (chat pane left + Objective draft rail right + estate-check chip inline + three visual states filled/open/agent-assumed); §2.3 CommitReview (You-supplied + Agent-assumed-confirm-or-change + Feasibility verdict card + license_class_drift signal + envelope line + Freeze objective button + verbatim binding copy *"Frozen is immutable — a changed intent is a new objective."*).
- **Backend wiring:** session-binding decorator across ALL 6 operator wizard endpoints (mismatch → 403 auth_identity_mismatch_for_wizard_session; buyer wiring is B-3 scope); NEW read-only `GET /api/operator/status` at `routers/operator.py` (78L); scope-enforcement gate PAIR on POST /v2/dispatch (Owner E1+E2 symmetric-cut ratified; granted → dispatch executes; insufficient → 403 with E2 body; anonymous falls through; ZERO envelope delta verified — 6 forbidden auth-metadata keys enumerated absent on 200/202/422 side; ComposedConclusion_v0 UNTOUCHED).
- **Curl-attested gate pair:** HALF 1 admin key + estate scope → HTTP 202 async_delivery_accepted; HALF 2 new-user + no matching grant → HTTP 403 `{reason:"auth_scope_insufficient", detail}`.
- **§0.2 Plan Debts status:** no new debts arose at B-2. Wizard session-ownership binding was RESOLVED at B-1 module landing; router-decorator wiring for operator variant landed at B-2 (surface-scoped mechanical follow-up per B-1 close observation). Buyer variant wiring is Phase 8 B-3 sub-stage scope. Envelope-shim triad remains RESOLVED at B-1. DPO wizard_transcript separately-addressable remains OPEN (Phase 8 B-5 scope).
- **Files touched:** 2 new backend source + 3 modified backend + 3 new frontend source + 2 modified frontend + 1 renamed e2e + 1 devDep + 1 script + 5 modified docs/memory + 1 new close report. Total ~1220 raw LoC (within Owner-anchored band 980-1820, ~67% top-of-band).
- **Next:** Owner ratification of B-2 close → Phase 8 Stage B-3 (Engineer + Buyer surfaces per UI Spec §4 + §5) dispatch. B-3 open sees E4 posture (Pydantic runtime record; D4b freeze-or-not argued against actual wire exposure).

## Phase 8 Stage B-1 (Implementation dispatch closed, 2026-07-05)
- **Status:** CLOSED (implementation; auth/key model + envelope-shim triad extraction + shared UI-Spec-v1 §8 barrel + Ask Console-full auth wiring + Playwright chromium-only smoke).
- **On-disk canonical:** `/app/docs/close_reports/phase_8_b_1.md` SHA-256 `b6d5c7a1ea0aaffa7b2a27dc31d96fd8c64f1ff071caf75913ffe6dde6c3f1fe`.
- **CI:** backend `pytest -q` = 777 / 777 (baseline 740 → +37 net); frontend `yarn test --testPathPattern='ui_spec_v1'` = 47 / 47 across 7 UI-Spec-v1 suites (baseline 27 → +20 net); webpack GREEN; parity 26/26; substrate-drop 9/9.
- **Owner rulings ratified (E1-E8):** E1 custom JWT via PyJWT + bcrypt (no hand-rolled crypto; federation-forward; per-call scope enforcement); E2 4-code auth-refusal bounded set + `{reason, detail}` body shape + registry-exclusion + render-path gates (fourth-not-wearing-first's-clothes); E3 `services/wizard/router_shims.py` at B-1; E4 deferred to B-3 open with steer (grant schema as Pydantic runtime record); E5 deferred to B-5 with standing ruling (inheritance-as-default + wizard_transcript separately-addressable); E6 in-pod trust-receipt route at B-5; E7 Playwright chromium-only at B-1; E8 sub-stage sequence.
- **§0.2 Plan Debts RESOLVED at B-1 (2):** Wizard session-ownership binding (Phase 7 B-2 dispatch, 2026-07-04) — `services/auth/session_binding.py` sidecar table + grandfathering carve-out landed; router-decorator wiring is Phase 8 B-2 surface-scoped follow-up. Envelope-shim helper triad extraction (Phase 7 B-3 close acceptance, 2026-07-04) — `router_shims.py` is named receiver + grep-negative gate GREEN + `admission_handoff.py` is pure re-export shim.
- **Files touched:** 12 new backend source + 1 new backend test + 3 modified backend files + 7 new frontend source + 2 new frontend test + 2 new frontend e2e + 2 modified frontend files + 5 modified docs/memory + 1 new close report. Total ~1959 raw LoC (within Owner-accepted band 1150-2150, ~91% of top-of-band).
- **Next:** Owner ratification of B-1 close → Phase 8 Stage B-2 (Operator surface per UI Spec §2) dispatch. B-2 opens with `session_binding.py` router-decorator wiring in the operator wizard router (enforce identity-match on `POST /api/wizard/operator/{sid}/*`) + Operator Home/Commission/CommitReview pages consuming `useAuth()` + Bearer wire.

## Phase 8 Stage A (Design-only dispatch, 2026-07-04)
- **Status:** CLOSED (design-only; zero code writes; parity stays 26; CI unchanged 740/740).
- **On-disk canonical:** `/app/docs/stage_a_proposals/phase_8.md` SHA-256 `4e4dd82ae2834f7c680429e1b2771221566d2bdc810e04444b722afda7b5c188`.
- **Deliverables:** trajectory restatement through Phase 8 (parity 26 baseline; conditional 27 if Escalation E4 lands `EngineerKeyGrant_v0` at B-3) + `snapshot_lloc_in_band` per sub-stage (B-1/B-2/B-4/B-5 = `no`; B-3 conditional) + Six Surfaces per UI Spec v1 (§§2-7) + §8 shared components + Playwright Ask Console smoke shape (6 scenarios) + Governance seam posture (session-ownership binding + auth-refusal shape + DPO wizard_transcript separately-addressable) + Standing constraints compliance (22 constraints preserved) + 8 escalations (E1-E8; E1/E2/E3 block B-1 dispatch).
- **§0.2 Plan Debts updated:** trajectory restatement MARKED RESOLVED with SHA reference; wizard_transcript entry REFINED with "separately-addressable" qualifier + dual citation header; envelope-shim helper triad extraction debt APPENDED per Owner Decision 3 at B-3 close acceptance.
- **`wizard_not_frozen` 422 body confirmed:** `{"reason": "wizard_not_frozen", "detail": "..."}` — NO `outcome=refused`, NO `AdmissionRefusal_v0` discriminator (router-layer ad-hoc; already documented in B-3 close §5).
- **Next:** Owner rulings on Escalations E1-E3 (P0 blockers for Phase 8 Stage B-1 dispatch) + E4-E8 (sub-stage-scoped).
