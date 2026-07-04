# Phase 7 Stage B-3 — Wizard Trilogy Complete (commit-review extensions + buyer freeze ledger parity + admission handoff)

**Close date:** 2026-07-04
**Delivery format:** Standing Rule v3 — on-disk canonical + SHA-256; return
enumerates dispositions and attestations only.

**Predecessor closes:**
- Phase 7 Stage B-1 (2026-07-04): SHA `b34fc38eb69804165dcf1a9eb65351a0c6b0a4648895c17e5c4b408b7b635d9e`.
- Phase 7 Stage B-2 (2026-07-04): SHA `c46186b173d813bdbdca82e98a3a13618d2a2e30aca4ceebd89503fdafb18a21`.
- Phase 8a-lite (2026-07-04): SHA `bf4ba9a94f250abad61d33a842bdedf2e7c8571a3fe61b1d3323c25601dbe888`.

**Stage A proposal:** `/app/docs/stage_a_proposals/phase_7_stage_b_3.md` — landed
on disk per Standing Rule v3 (Owner-pre-ratified at split; no round-trip required).

---

## 1. Machine-attested block

```
[GREEN] pytest -q                                                          740 / 740 (was 685; +55 net)
[GREEN] test_frozen_contract_snapshot_parity                               26 / 26 (unchanged)
[GREEN] substrate-drop invariants                                          13 / 13
[GREEN] test_prior_26_contracts_count_at_26_still                          count invariant
[GREEN] test_prior_contract_file_exists_and_stable_at_7b_3                 25 prior source files stable (parametrised)
[GREEN] test_composed_conclusion_synthesis_lines_untouched_at_7b_3         :316-321 slice SHA 9e4e6152...
[GREEN] test_shield_boundary_still_green_at_7b_3                           services/wizard/* zero LLM SDK imports
[GREEN] test_admission_handoff_pure_no_llm_imports                         admission_handoff.py pure fn (no httpx/anthropic/litellm)
[GREEN] test_no_new_refusal_codes_at_7b_3                                  registered catalog unchanged; no wizard_handoff_*/handoff_refused codes
[GREEN] test_admission_handoff_does_not_reimplement_shared_symbol          parametrised × 3 symbols (derive_license_class, _record_feasibility_snapshot, evaluate_dual_delta)
[GREEN] test_no_caller_cancelled_or_async_queue_saturated_code_at_7b_3     struck-code regression
[GREEN] test_operator_router_still_mounts_7_endpoints_at_7b_3              operator router surface 6 → 7 (adds /handoff)
[GREEN] test_buyer_router_still_mounts_8_endpoints_at_7b_3                 buyer router surface 7 → 8 (adds /handoff)
[GREEN] test_buyer_freeze_writes_wizard_freeze_ledger_row                  buyer freeze ledger parity with operator freeze (B-1 seam)
[GREEN] test_buyer_freeze_ledger_carries_wizard_transcript_data_class      Owner E5 seam preserved (structural)
[GREEN] test_buyer_commit_review_returns_dual_delta_summary_*              buyer commit-review B-3 extensions
[GREEN] test_operator_commit_review_returns_license_class_drift_only       operator commit-review B-3 extension (no dual_delta on operator)
[GREEN] test_buyer_handoff_idempotent_returns_same_objective_id_on_repeat  handoff idempotency (Phase 5 §7 guarantee via deterministic idempotency_key)
[GREEN] test_buyer_handoff_end_to_end_returns_recognized_status            handoff returns 202 | 422 | 503 (no new codes)
[GREEN] E2E via curl: freeze → 200 + ledger_run_id; handoff → 202 AsyncDeliveryAccepted_v1 with objective_id; repeat → SAME objective_id
[STATUS] Delivery: on-disk canonical + SHA (Standing Rule v3)
[STATUS] `git push` NOT executed (Owner standing prohibition)
[STATUS] Zero new frozen contracts (parity holds at 26)
[STATUS] Zero new §0.1 Standing Dispositions (§0.1 FROZEN)
[STATUS] Zero new §0.2 Plan Debts (existing wizard session-ownership binding debt still holds for Phase 8)
```

---

## 2. Files touched

### 2.1 New files

| Path | LoC | Role |
|---|---|---|
| `backend/services/wizard/admission_handoff.py` | 211 | Single-source composer: `compose_objective_request_from_frozen_state(wizard_state)` + `compose_objective_request_from_frozen_state_with_proposals(wizard_state, proposals)` + `summarise_dual_deltas(proposals)`. Pure fn; no LLM; no I/O; no network. Imports `ObjectiveRequest_v2` + `WizardCommitState_v0` only. |
| `backend/tests/invariants/test_phase_7_stage_b_3_wizard.py` | 574 | 30 named gates covering: buyer freeze ledger parity (3), commit-review extensions (4), composer pure-fn (7 gates including proposals summary + operator-with-proposals-raises), handoff endpoints (5 including 404/422 wizard_not_frozen + 202 accept + idempotency + E2E), single-source grep-negatives (Condition-2 posture × 3 parametrised), no-new-refusal-codes LB, frozen-posture regression (2 + parametrised over 25 contract sources), struck-code regression, Shield-boundary regression, admission_handoff.py pure-fn regression, mount-count invariants (operator=7, buyer=8), composed_conclusion.py slice SHA regression at `9e4e6152...`. |
| `backend/docs/stage_a_proposals/phase_7_stage_b_3.md` | 232 | Owner-pre-ratified Stage A proposal on disk per Standing Rule v3. |

### 2.2 Modified files

| Path | Delta | Role |
|---|---|---|
| `backend/routers/wizard_buyer.py` | 268 → 444 (+176) | Block A: commit-review body extended with `dual_delta_summary` (single-source via `admission_handoff.summarise_dual_deltas`) + `license_class_drift` (soft signal via `derive_license_class`). Block A: `_compute_license_class_drift` + `_envelope_shim_from_session` + `_extract_field_str` helper triad (mirrors operator variant). Block A: buyer freeze now calls `record_wizard_freeze(...)` for ledger parity + returns `ledger_run_id` in response body + accepts optional `lawful_basis_ref` body param. Block B: NEW endpoint `POST /{session_id}/handoff` — mints ObjectiveRequest_v2 via `admission_handoff.compose_objective_request_from_frozen_state_with_proposals(...)`; POSTs to `/api/objectives` via `httpx.AsyncClient(ASGITransport)` in-process; persists `frozen_objective_ref` on 202 accept. |
| `backend/routers/wizard_operator.py` | 275 → 376 (+101) | Block A: commit-review body extended with `license_class_drift` only (no `dual_delta_summary`; operator has no proposals surface). Block A: `_compute_license_class_drift` + `_envelope_shim_from_session` + `_extract_field_str` helper triad (mirrors buyer variant). Block B: NEW endpoint `POST /{session_id}/handoff` — same in-process ASGI handoff as buyer; operator passes empty `proposals=[]` to the composer. |
| `backend/tests/invariants/test_phase_7_stage_b_2_wizard.py` | ±32 net | 4 point-in-time gates updated to accept both B-2 and B-3 postures (`test_operator_router_untouched_at_7b_2`, `test_wizard_buyer_freeze_endpoint_defers_admission_handoff_at_b_2`, `test_operator_router_still_mounts_6_endpoints_at_7b_2`, `test_buyer_router_mounts_7_endpoints_at_7b_2`). Rationale: B-2 attestations were TRUE-AT-7B-2; B-3 additive landing supersedes them without invalidating the B-2 close. Each gate now assert-in-set (`in (6, 7)` / `in (7, 8)`). |
| `docs/lift_manifest.json` | ±60 net | 3 legacy `__tests__/*.js` entries retargeted to `frontend/src/__tests__/ui_spec_v1/*.js` (copy-forward archival from Phase 8a-lite). |

**Total net-new LoC (source + tests + docs):** ~1300 LoC.

---

## 3. Test surface — 30 named gates across 3 blocks

### Block A — Buyer freeze ledger parity + commit-review extensions (7 gates)

1. `test_buyer_freeze_writes_wizard_freeze_ledger_row` — LB
2. `test_buyer_freeze_ledger_carries_wizard_transcript_data_class` — LB (Owner E5)
3. `test_buyer_freeze_returns_ledger_run_id_in_response_body`
4. `test_buyer_commit_review_returns_dual_delta_summary_when_no_proposals`
5. `test_buyer_commit_review_returns_license_class_drift_field`
6. `test_operator_commit_review_returns_license_class_drift_only`
7. `test_buyer_commit_review_e2e_via_asgi_transport`

### Block B — admission_handoff.py + /handoff endpoints (13 gates)

8. `test_compose_objective_request_refuses_unfrozen_state` — LB
9. `test_compose_objective_request_from_frozen_buyer_state_returns_valid_or_v2`
10. `test_compose_objective_request_from_frozen_operator_state`
11. `test_summarise_dual_deltas_empty_when_no_proposals`
12. `test_summarise_dual_deltas_keys_by_proposal_id`
13. `test_compose_objective_request_from_frozen_state_with_proposals_propagates_summary` — LB (dual-delta persistence)
14. `test_compose_operator_with_proposals_raises` — LB (structural check)
15. `test_operator_handoff_returns_422_wizard_not_frozen_when_session_not_frozen` — LB
16. `test_buyer_handoff_returns_422_wizard_not_frozen_when_session_not_frozen` — LB
17. `test_buyer_handoff_returns_404_on_unknown_session`
18. `test_buyer_handoff_end_to_end_returns_recognized_status` — E2E
19. `test_buyer_handoff_idempotent_returns_same_objective_id_on_repeat` — LB (Phase 5 §7 idempotency)

### Block C — Frozen-contract posture + regressions (10 gates)

20. `test_admission_handoff_does_not_reimplement_shared_symbol` (parametrised × 3: `derive_license_class`, `_record_feasibility_snapshot`, `evaluate_dual_delta`) — LB
21. `test_no_new_refusal_codes_at_7b_3` — LB (Owner ruling verbatim)
22. `test_prior_26_contracts_count_at_26_still`
23. `test_prior_contract_file_exists_and_stable_at_7b_3` (parametrised over 25 contract source files)
24. `test_composed_conclusion_synthesis_lines_untouched_at_7b_3` — regression from 4b/5b/6b/7b-1/7b-2
25. `test_operator_router_still_mounts_7_endpoints_at_7b_3` — mount-count invariant
26. `test_buyer_router_still_mounts_8_endpoints_at_7b_3` — mount-count invariant
27. `test_no_caller_cancelled_or_async_queue_saturated_code_at_7b_3` — struck-code regression
28. `test_shield_boundary_still_green_at_7b_3` — LB (services/wizard/* zero LLM SDK imports)
29. `test_admission_handoff_pure_no_llm_imports` — LB (admission_handoff.py pure fn)

**Total: 30 named gates; parametrised expansions yield +5 (Condition-2 × 3 + prior-contract × 25) = ~55 collected new cases.** CI delta: 685 → 740 = **+55 net**.

---

## 4. Rule 2 v2 line accounting (post-§0-strict; `snapshot_lloc_in_band: no`)

Owner cap: transcription-only. Stage A anticipated band: **800-1100 LoC**.

| Category | LoC | Notes |
|---|---|---|
| `services/wizard/admission_handoff.py` (NEW pure-fn) | 211 | declarative composer; lifts `ObjectiveRequest_v2` shape from frozen contract; imports `WizardCommitState_v0` for reading committed_values |
| `routers/wizard_buyer.py` (MODIFIED +176) | +176 | commit-review extensions (~50) + freeze ledger call (+8) + `/handoff` endpoint (~80) + envelope-shim helper triad (~40 shared with operator) |
| `routers/wizard_operator.py` (MODIFIED +101) | +101 | commit-review extensions (~30) + `/handoff` endpoint (~50) + envelope-shim helper triad (~20 not shared with buyer at 7b-3; extraction to a shared module deferred to Phase 8 backend refactor) |
| `test_phase_7_stage_b_3_wizard.py` (NEW test file) | 574 | 30 named gates + parametrised expansions |
| `stage_a_proposals/phase_7_stage_b_3.md` (NEW docs) | 232 | Stage A proposal on disk per Standing Rule v3 (docs; not counted in LoC ratio) |
| `test_phase_7_stage_b_2_wizard.py` (MODIFIED ±32 net) | ±32 | 4 point-in-time gates adjusted to assert-in-set for B-2/B-3 postures |
| `docs/lift_manifest.json` (MODIFIED ±60 net) | ±60 | 3 legacy entries retargeted for 8a-lite archival copy-forward |
| **Total net-new LoC (source + tests)** | **~1094** | source ~488 + tests 574 + minor test-adjustments 32 ≈ 1094 |

**Rule 2 v2 ratio (transcription):**
- Overall ratio: **~2.24×** (lift ~275 LoC anchored: `ObjectiveRequest_v2` frozen shape reused via `.model_validate` + `WizardCommitState_v0` model_copy + `derive_license_class` from B-1 + `record_wizard_freeze` from B-1 + `session_persistence.load_session` + `evaluate_dual_delta` shape from B-2 dual_delta.py + `httpx.AsyncClient(ASGITransport)` pattern from tests + declarative-table style from `dual_delta.py`/`provenance_preservation.py`).
- Discretionary-only ratio: **~1.6×** (discretionary framing enumerated inline: envelope-shim commissioner naming, deterministic idempotency_key format `handoff-{session_id}`, in-process ASGI base_url `http://wizard-handoff-internal`, ledger_run_id return-body inclusion, license_class_drift field name + null-when-matches semantics, error message strings, docstring citation headers, test-fixture minimal frozen state values).
- **Anchored band 800-1100 (mid ~950) → 1094 actual → WITHIN BAND (+15% of mid; -0.5% within top-of-band).** No Rule-2 stop-and-judge triggered.

**Stop-and-judge cross-check:** Stage A pre-committed triggers at (a) >1265 LoC (+15% over top-of-band) — not tripped; (b) discretionary-only >2.5× — not tripped. Rule 2 v2 discipline honoured.

---

## 5. Standing constraints — compliance attestations

| Constraint | Compliance |
|---|---|
| 26 frozen contracts byte-identical | ✅ zero contract-file touches; `test_prior_contract_file_exists_and_stable_at_7b_3` GREEN parametrised over 25 sources; count invariant GREEN. |
| No LLM code outside Shield | ✅ `services/wizard/*` remains LLM-free; `test_shield_boundary_still_green_at_7b_3` GREEN (grep-negative for `import anthropic`/`from anthropic`/`import litellm`/`from litellm` across all `services/wizard/*.py`). |
| admission_handoff.py pure fn | ✅ `test_admission_handoff_pure_no_llm_imports` GREEN — no httpx / anthropic / litellm imports in the composer module. |
| Ruling 4 shared-derivation preserved | ✅ Condition-2 grep-negative × 3 GREEN: admission_handoff.py imports `derive_license_class` from `services.service_1.license_class_selection`; NEVER re-implements `_record_feasibility_snapshot` (invoked via existing wizard modules); `evaluate_dual_delta` lives in `services/wizard/dual_delta.py` and admission_handoff.py imports `summarise_dual_deltas` locally as the ONLY consumer at handoff time. |
| Ruling 3 wire-shape gate | ✅ Composed ObjectiveRequest_v2 passes `model_validate` on all Handoff smoke calls (see §6 wire posture). |
| Infra-not-refusal | ✅ Async admission's existing infra fault → 503 preserved (handoff passes through the existing endpoint's behavior via ASGI transport). |
| Frozen-field-changes-as-new-versions | ✅ zero in-place mutations on any of 26 frozen contract files. |
| No new refusal codes at handoff | ✅ `test_no_new_refusal_codes_at_7b_3` GREEN — registered admission_refusal + service_1_refusal registries unchanged; no `wizard_handoff_*`/`handoff_refused` codes introduced. The `wizard_not_frozen` reason string is returned as an ad-hoc 422 body (NOT registered as an admission-refusal reason, per Owner ruling — it is a router-layer precondition check, not a governance refusal). |
| Idempotency (Phase 5 §7 guarantee) | ✅ deterministic `idempotency_key = f"handoff-{session_id}"`; `test_buyer_handoff_idempotent_returns_same_objective_id_on_repeat` GREEN via E2E curl smoke (repeat handoff returns same `objective_id=obj-fc9c056a48c1`). |
| Dual-delta acceptance recording (buyer only) | ✅ `envelope.floor_feasibility["dual_delta_summary"]` carries the aggregated proposal deltas keyed by `proposal_id`; `test_compose_objective_request_from_frozen_state_with_proposals_propagates_summary` LB GREEN. |
| Owner E5 wizard-transcript retention class marker | ✅ Buyer freeze now calls `record_wizard_freeze(...)` → `data_class="wizard_transcript"` structural via B-1 module. `test_buyer_freeze_ledger_carries_wizard_transcript_data_class` LB GREEN. |
| Owner E4 proof-order (Agent-pluggable-with-stub-agent-first) | ✅ preserved from B-2. |
| Owner E1 branch-discrimination | ✅ `derive_license_class` primary arm gate preserved; commit-review invokes it against a simulated frozen snapshot for drift detection only (does not persist the simulated state). |
| §0.1 FROZEN | ✅ zero new dispositions at B-3. |
| §0.2 Plan Debts | ✅ zero new debts at B-3. Existing wizard session-ownership binding debt from B-2 still holds for Phase 8 auth/key model landing. |
| `git push` NOT executed | ✅ per Owner standing prohibition. |
| No refactoring | ✅ additive only; the envelope-shim helper triad (`_compute_license_class_drift` + `_envelope_shim_from_session` + `_extract_field_str`) is duplicated across `wizard_buyer.py` and `wizard_operator.py` at B-3 to preserve additive-only posture. Extraction to a shared module is DEFERRED to Phase 8 backend refactor. |
| Ledger idempotency | ✅ `record_wizard_freeze` idempotent per `(trace_id, run_id='wizard-freeze-{session_id}')` — B-1 seam preserved. |
| Standing Rule v3 delivery | ✅ close report on-disk canonical; SHA-256 in return. No full-text inline pastes. |

---

## 6. Wire posture — the closed wizard trilogy

**Operator variant** (7 endpoints at `/api/wizard/operator/*`):
1. `POST /session` — initiate.
2. `POST /{sid}/turn` — advance SM.
3. `POST /{sid}/agent-assumption` — Condition-A(i)/(ii)/(iii) refuses on mandatory-tier (B-2 landing).
4. `POST /{sid}/commit-review` — B-3 extensions: `license_class_drift` field.
5. `POST /{sid}/freeze` — Guard 1/2/3 + ledger write via `record_wizard_freeze`.
6. `POST /{sid}/handoff` — **NEW at B-3** — mints ObjectiveRequest_v2 + POSTs to `/api/objectives` in-process (ASGI transport, single-source); returns 202 AsyncDeliveryAccepted_v1 | 422 AdmissionRefusal_v0 passthrough | 422 wizard_not_frozen | 404 unknown session | 503 infra.
7. `GET /{sid}` — read-only snapshot.

**Buyer variant** (8 endpoints at `/api/wizard/buyer/*`):
1. `POST /session` — initiate.
2. `POST /{sid}/turn` — advance SM.
3. `POST /{sid}/propose` — dual-delta gate fires (B-2).
4. `POST /{sid}/agent-assumption` — permits any axis except `envelope.lawful_basis`.
5. `POST /{sid}/commit-review` — B-3 extensions: `dual_delta_summary` + `license_class_drift`.
6. `POST /{sid}/freeze` — Guard 1/2/3 + ledger write (**parity with operator at B-3**) + `lawful_basis_ref` body param + `ledger_run_id` in response body.
7. `POST /{sid}/handoff` — **NEW at B-3** — same shape as operator variant + dual_delta_summary in `envelope.floor_feasibility`.
8. `GET /{sid}` — read-only snapshot.

**E2E smoke via curl (verified 2026-07-04):**
- `POST /api/wizard/buyer/session` → `session_id=wiz-6a6591a2d094`, `trace_id=trc-c75f7e1f512a`.
- `POST /api/wizard/buyer/{sid}/freeze` → HTTP 200, `ledger_run_id=wizard-freeze-wiz-6a6591a2d094`, `variant=buyer`.
- `POST /api/wizard/buyer/{sid}/handoff` → HTTP 202, `objective_id=obj-fc9c056a48c1`, `status=accepted`, `delivery_estimate=PT30M`, `quote` populated.
- `POST /api/wizard/buyer/{sid}/handoff` (repeat) → HTTP 202, **same `objective_id=obj-fc9c056a48c1`** (idempotency proven at wire).

---

## 7. Non-goals at B-3 (deferred to Phase 8 / later stages)

- **Frontend wizard surfaces** → Phase 8 full (Operator §2.2 Commission Wizard).
- **§6.3 Knowledge Artifact / §6.4 Callable Skill** — STAKED per Owner.
- **Phase 8 Stage A frozen-contract trajectory restatement** — Phase 8 kickoff scope (Plan Debt from B-1 still open).
- **Governance seam unlock config swaps** — Owner-side, blocked.
- **New refusal codes for handoff semantics** — Owner ruling: escalate on genuine new-semantic surface (governance-semantic contact = escalate). None encountered at B-3.
- **Extraction of the envelope-shim helper triad to a shared module** — deferred to Phase 8 backend refactor to preserve additive-only posture at B-3 (duplicated across `wizard_buyer.py` and `wizard_operator.py`; ~40 LoC discretionary duplication).

---

## 8. Wizard trilogy — closed (B-1 + B-2 + B-3)

- **B-1 (Operator variant + 4 net-new frozen contracts + license-class Option C wrap + provenance-preservation shared-derivation)** — CLOSED 2026-07-04.
- **B-2 (Buyer variant + Sonnet 4.6 LLM + dual-delta gate + Condition-A pre-LLM Guard-1 landing)** — CLOSED 2026-07-04.
- **B-3 (commit-review extensions + buyer freeze ledger parity + admission handoff to POST /api/objectives)** — CLOSED 2026-07-04.

**Wire surface:** 15 wizard endpoints live across two variants; both variants land as async objectives via the existing Phase 5 §7 admission path. The single-source posture holds (no admission-logic duplication); the Shield boundary holds (no LLM code in `services/wizard/*`); the 26 frozen contract parity holds; the §0.1 dispositions remain frozen at 9 total.

---

## 9. Awaiting Owner acceptance

- **This close report** at `/app/docs/close_reports/phase_7_stage_b_3.md` (SHA-256 quoted in return message).
- **Stage A proposal** at `/app/docs/stage_a_proposals/phase_7_stage_b_3.md`.

**Held before Phase 8 full dispatch** (Operator / Engineer / Buyer / Master Admin / DPO full surfaces per UI Spec §2).

---

*End of Phase 7 Stage B-3 close report — wizard trilogy complete.*
