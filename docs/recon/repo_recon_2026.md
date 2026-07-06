# RMS Intelligence System — Repo Recon (2026-07-06)

**Read-only recon. No code modified.** Composed under Standing Rule v3 —
long-form content on-disk; return message carries SHA + short tables +
contradictions.

═══════════════════════════════════════════════════════════════════

## A. Repo topology snapshot

### A.1 Top-level tree summary

| Directory | Files | LoC | Purpose |
|---|---|---|---|
| `/app/backend/` | 497 (.py + .json) | ~36854 (.py) | FastAPI + Pydantic + Motor async Mongo; 26 frozen contracts; ~100 service modules; 17 routers; 64 invariant test files |
| `/app/frontend/` | 65 (.js/.jsx/.ts/.tsx incl. tests) | ~8437 | React SPA (Webpack); 15 pages across 4 consoles + auth; 10 top-level components + 1 barrel; Jest gates + Playwright chromium smokes |
| `/app/docs/` | 80 | ~19610 (.md only) | 8 mandates (7 canonical + 1 superseded v1) + 10 stage-A proposals + 16 close reports + audits/prep/handoff/lift_manifest.json/rule2_accounting.json |
| `/app/memory/` | 5 | (small) | ORCHESTRATOR_CONTINUITY.md + PHASE_STATE.md + PRD.md + test_credentials.md + governance/rulings notes |
| `/app/salvage/` | 18 | ~4489 | Single dated cut `commercial_cut_2026_07_06/` — buyer wizard code + tests + commercial-frontend + salvage MANIFEST + README |

### A.2 Frozen contracts (26/26 parity — verified via directory listing + snapshot listing)

| # | Contract file | Snapshot file (canonical name) | Version |
|---|---|---|---|
| 1 | `admission_refusal.py` | `admission_refusal.contract_snapshot.json` | v0 |
| 2 | `agent_assumption.py` | `agent_assumption.contract_snapshot.json` | v0 |
| 3 | `async_delivery_accepted.py` | `async_delivery_accepted.contract_snapshot.json` | v0 |
| 4 | `async_delivery_accepted_v1.py` | `async_delivery_accepted_v1.contract_snapshot.json` | v1 |
| 5 | `committed_value.py` | `committed_value.contract_snapshot.json` | v0 |
| 6 | `composed_conclusion.py` | `composed_conclusion.contract_snapshot.json` | v0 |
| 7 | `cumulative_disclosure.py` | `cumulative_disclosure_ledger.contract_snapshot.json` | v0 |
| 8 | `extraction_params.py` | `extraction_params.contract_snapshot.json` | v0 |
| 9 | `feasibility_result.py` | `feasibility_result.contract_snapshot.json` | v0 |
| 10 | `five_rings.py` | `five_rings.contract_snapshot.json` | v0 |
| 11 | `lift_manifest_response.py` | `lift_manifest_envelope.contract_snapshot.json` | v0 |
| 12 | `mtafiti_registry.py` | `mtafiti_registry_record.contract_snapshot.json` | v0 |
| 13 | `northena_ledger.py` | `northena_ledger_row.contract_snapshot.json` | v0 |
| 14 | `northena_ledger_v1.py` | `northena_ledger_v1.contract_snapshot.json` | v1 |
| 15 | `objective_request.py` | `objective_request.contract_snapshot.json` | v0 |
| 16 | `objective_request_v2.py` | `objective_request_v2.contract_snapshot.json` | v2 |
| 17 | `operator_turn.py` | `operator_turn.contract_snapshot.json` | v0 |
| 18 | `outer_gate_receipt.py` | `outer_gate_receipt.contract_snapshot.json` | v0 |
| 19 | `qualification_matrix/loader.py` | `qualification_matrix.contract_snapshot.json` | v0 |
| 20 | `quote_envelope.py` | `quote_envelope.contract_snapshot.json` | v0 (ORPHAN-IN-PLACE per §12.3) |
| 21 | `service_1_refusal.py` | `service_1_refusal.contract_snapshot.json` | v0 |
| 22 | `signal_ring.py` | `signal_ring.contract_snapshot.json` | v0 |
| 23 | `targeta_plan.py` | `targeta_mining_plan.contract_snapshot.json` | v0 |
| 24 | `trace_lens.py` | `trace_lens_envelope.contract_snapshot.json` | v0 |
| 25 | `v2_refusal.py` | `v2_refusal_envelope.contract_snapshot.json` | v0 |
| 26 | `wizard_commit_state.py` | `wizard_commit_state.contract_snapshot.json` | v0 |

Count: **26 contracts × 26 snapshots = bijective mapping** confirmed
(matches PHASE_STATE.md parity assertion). QuoteEnvelope_v0 (#20)
carried commercially but retained per PRES-3 orphan-in-place ruling.

### A.3 Routers (17 files under `/app/backend/routers/`)

| Router | One-line purpose |
|---|---|
| `auth.py` | Phase 8 B-1 — /api/auth register/login/me + JWT + refusal codes |
| `compliance.py` | Phase 8 B-5a — /api/compliance retention_config (read) + refusals (aggregate) |
| `contracts.py` | G0 follow-up — surfaces Five Rings + ObjectiveRequest + QualificationMatrix contracts |
| `discipline.py` | G5a — /api/discipline/lift_manifest read-only lift-manifest serving |
| `engineer.py` | Phase 8 B-3 — /api/engineer key_grants + apps management for internal engineers |
| `g1.py` | G1 legacy — /api/v3/status + /api/v1/stamp_audit/* (absorbed into Northena at G2) |
| `handoff.py` | Post-G6 — /api/handoff/backend_contract_surface_v1 dump |
| `master_admin.py` | Phase 8 B-4 — /api/master_admin pending_seams + tier_lock + admin routes |
| `mtafiti.py` | Phase 1 — /api/mtafiti/feasibility Estate Feasibility Query |
| `northena.py` | G2+ — /api/northena/status + ledger read + trace_lens (auth-branch amend at B-5a) |
| `objectives.py` | Phase 5 B — /api/objectives async admission (202) + cancel + poll |
| `operator.py` | Phase 8 B-2 — /api/operator/status Operator Home aggregate |
| `pricing.py` | Phase 6 B / B-4 rewrite — /api/pricing + /api/fleet Master-Admin control surface |
| `service_1.py` | Phase 2/3/4a/4b — /api/service_1/v2/dispatch + v1 dispatch |
| `solva.py` | G3 — Solva enforcement + trace read |
| `v1.py` | G0.5 — /api/v1/status harness state read |
| `wizard_operator.py` | Phase 7 B-1/2/3 — /api/wizard/operator/* full operator wizard trilogy |

### A.4 Service modules (100+ files across 20 subdirs)

| Subdir | Files | Purpose (one-line composite) |
|---|---|---|
| `auth/` | 12 | Phase 8 B-1 identity + JWT + bcrypt + session-binding + engineer key-grants |
| `compliance/` | 8 | Phase 8 B-5a retention_config read + refusals aggregate + trust-receipt allowlist + family classifier + held-class registry |
| `data_source/` | 4 | Synthetic + real-RMS placeholders (real material not yet ingested) |
| `economics/` | 8 | Phase 6 B internal-half only (fleet_policy + delivery_time + tier_lock_ledger; commercial half cut) |
| `g1_defensibility/` | 5 | G1 defensibility ring / genre / source-standing / stamp-audit (Ring 5) |
| `layer_a/` `layer_b/` `layer_c/` | 3 each | G3 3-layer pipeline (dispatcher / provider-factory / aggregator+convergence) |
| `master_admin/` | 2 | Phase 8 B-4 pending_seams read (§6 Admin Home) |
| `mtafiti/` | 11 | Phase 1 estate/feasibility + Ring 4 measurement (census + declaration + inference + measure + registry + source_standing + v3_overlay + verdict + floor_feasibility shared-derivation) |
| `northena/` | 7 | G2+ 3-stage state machine (admit → gate → converge) + ledger + trace_lens |
| `outer_gate/` | 4 | G6 crypto — mint + transform + receipt (irreversibility invariant) |
| `service_1/` | 15 | Phase 2-5 Service_1 v1/v2 dispatch + async worker + refusal families + qualified data + composed conclusion + grain compat + license class |
| `solva_depth/` | 9 | G3 Solva reasoning boundary (depth v1 + trace + stamp + assertion + pipeline + admit_assist) |
| `synisense/` | 4 | Shield boundary (config + exceptions + webhook_registration); LLM router lives here |
| `targeta/` | 6 | G4 Targeta CLOSED SEAM (yield admission + mining plan) |
| `v1_harness/` `v2_gate/` `v3_harness/` | 4 / 3 / 2 | Metric harnesses (G0.5/G6/G1) |
| `wizard/` | 8 | Phase 7 B-1/2/3 operator wizard (state machine + agent interface + admission handoff + session + source-tagging + turn ledger + router_shims) |

**Standalone:** `services/storage_service.py` + `services/system_state.py`.

### A.5 Frontend pages/components

**Pages (15) — grouped by console:**
- **Auth (2):** `AuthLoginPage.js`, `AuthRegisterPage.js`
- **Compliance Console (3):** `ComplianceHomePage.js`, `ComplianceProveOneRunPage.js`, `ComplianceRetentionRightsPage.js` (all NEW at Phase 8 B-5a)
- **Extraction/Operator Console (3):** `OperatorHomePage.js`, `CommissionWizardPage.js`, `CommitReviewPage.js` (Phase 8 B-2)
- **Integration/Engineer Console (3):** `EngineerAdministerPage.js`, `EngineerFirstCallPage.js`, `EngineerRegisterAppPage.js` (Phase 8 B-3)
- **Administration/Master Admin Console (3):** `MasterAdminHomePage.js`, `ChangeARulePage.js`, `AuditTrailPage.js` (Phase 8 B-4)
- **Ask Console reference app (1):** `AskConsolePage.js` (Phase 8a-lite)

**Components (11):**
- `AppShell.js`, `ClassBadge.js`, `EngineCard.js`, `LedgerTable.js`, `OuterGateReceiptInline.js`, `RefusalCard.js`, `StatusBadge.js`, `TrustReceiptLink.js`
- Phase 8 B-1: `AuthDeniedNotice.js`
- Phase 8 B-5a: `RetentionPostureBadge.jsx` (first UI-Spec-v1-barrel-registered new component)
- Barrel: `ui_spec_v1/index.js`

═══════════════════════════════════════════════════════════════════

## B. Spec / mandate inventory

### B.1 Mandates (`/app/docs/mandates/`)

| File | SHA-256 | Status | 1-line summary |
|---|---|---|---|
| `MANIFEST.md` | `46d81b8b37226dcad8c2bf75057337b44248bba4673cc84c6ea89a4de54ab7ef` | canonical | Register of on-disk mandate SHAs + phase_source_requirements pointers |
| `RMS_UI_Specification_v2_1.md` | `ef6da4b498117608a3091033b5cfa43571ad8a7a38b5954cae7c4a1a698de5e2` | canonical, ratified | Four consoles + ref apps (v2.1 supersedes v1; §5.5 governed-extract API; §8 checker; §12 Sales Service stub) |
| `RMS_UI_Specification_v1.md` | `9053a4c451954cca1dc2f2b10216bef2058411a1911136581251e395d5bdcbf3` | SUPERSEDED | Original 8-section UI spec (marker at top); phase_source_requirements repointed |
| `RMS_Build_Completion_Requirements_v1_4.md` | `d1f49bc5d7cbf1dea044ca4069a1dc2d45f01876e531b7500d860ae3f48aebdd` | canonical, ratified | Section 3 covers §3.1 Phase 9 + §3.2 Artifact store + §3.4 Packaging + §3.5 Seam 3 + §3.6/§3.6B B-5a/B-5b + §3.7 TF forms + §3.8 fluency + §3.9 8-EXT + §3.11 checker + §3.12 sampling + §3.13 B-4 retrofit + §12 commercial cut |
| `RMS_Product_Engineering_Spec_v3.md` | `af2e3cb2fccfd92278dedec725732ae1b5b48dff614fd6f7c8fbc805160d915a` | canonical | v3 product spec (§3.3 wizard; §4 extraction; §6 transforms; §7 async; §8 economics) |
| `RMS_Solva_Specification.md` | `e38b0370eed0b065468072a0ab393a66d39760f87c4d12a64f7560b5f0e260b5` | canonical | Solva reasoning boundary spec |
| `RMS_Mtafiti_Specification.md` | `664fb76680cd8b9e62cfeac084a9d7d9410122a26d692f873c0242b59c78a1da` | canonical | Ring 4 measurement engine spec |
| `RMS_Targeta_Specification.md` | `7e0ca7a373684cf30ca39d6a9c98f3a59e57c29f8ce1179eac0cbef9e4086990` | canonical | Yield admission / mining plan spec |
| `RMS_UX_Architecture_v2.md` | `e072fd307e00b207cd2a451791bc3650ad59f5f71b28ac5d4c04b1144b841d59` | canonical | UX architecture v2 |
| `northena.md` | `ab0beeddf23c9530cc54c6ddd4255b4b3d0435df0d4c156d05de478e65af8345` | canonical | Northena 3-stage state machine spec |
| `phase_source_requirements.yaml` | `59d43a95028783570546ffeda0e55fd3cfc7d661c2a5303bbca74b668a952927` | canonical | Per-phase substrate-drop gate config (redirected to v2.1) |
| `archive/*` | — | archived | Predecessor v1.0 northena + v1 UX + Interface Spec + Product Spec v2.1 (superseded by v3) |

### B.2 Stage-A proposals (`/app/docs/stage_a_proposals/`)

| File | SHA-256 | Status |
|---|---|---|
| `phase_4_stage_a.md` | `028bf99c6bcd28779f6f32c5585a13e4feb4950518ef458b3440e1e1b2391504` | ratified (→ 4a+4b closed) |
| `phase_5_stage_a.md` | `8150688e73e2e22f3fbd6e4ea5a78c8bf0020534efca0179921dad1beb97b7df` | ratified (→ 5B closed) |
| `phase_6_stage_a.md` | `62894f2cf4ee40a5d4352b9705c66da6c7fd29f0cafa7f2fe8703a2c37cccf78` | ratified (→ 6B closed) |
| `phase_7_stage_a.md` | `e2bfe36e2e61025fe417d1cd2de3e91cf4c88fdcb745d3c5f0028ef795fa98ce` | ratified (→ B-1/2/3 closed) |
| `phase_7_stage_b_2.md` | `c515a71486abef1ad40e0c44d9f32cbceeb9027f1e7a3e59ae07e809defc3718` | ratified (→ B-2 closed) |
| `phase_7_stage_b_3.md` | `040c4099aa031ddb4b8133ac64f301457e6bdafc13ad12cf5c58fb1ba90f4698` | ratified (→ B-3 closed) |
| `phase_8.md` | `78db65d82e12b62de4198f081cd60c7f1818052d9b88d81077691c2e6c9bc96c` | ratified (→ B-1/2/3/4/5a closed) |
| `phase_8_b_4.md` | `abe7c7c0cd93de1a34d027655c28297ecd1238644478bf69df1682b24d2e255e` | ratified (→ B-4 closed) |
| `phase_8_b_5a.md` | `e031091e5ab0fa42e5369aa83357caa65c561f63370ab970b67a3d13463b28b9` | ratified (→ B-5a closed) |
| `phase_8_seam_3_and_checker.md` | `111b4c43339b7b4db456fcf5c78d38cbbdad959ed419f2808d7ef83374142b89` | **PENDING RATIFICATION** (delivered 2026-07-06) |

### B.3 Close reports (`/app/docs/close_reports/`)

| File | SHA-256 | Status |
|---|---|---|
| `housekeeping_preflight.md` | `8e543ef9e527b691f72ff465f15678b86762ffaec38545733ac9e3ae0ef0a2cb` | closed |
| `phase_4a_stage_b.md` | `f5bb38e7d25b3e295bb38aec24bf6e46404bb164ab0b9a5cd639c451234eb866` | closed, ratified |
| `phase_4b.md` | `2781313b28e152277e41f135801e4f5e3f0a3b083aa50a53ef3ab634c9cfb6c7` | closed, ratified |
| `phase_5_stage_b.md` | `49ce2262b1f6f6e244bb7294b165734f6de31a1b176a55f73dd8871e94a2def5` | closed, ratified |
| `phase_6_stage_b.md` | `79d6e7f4caa865cad09d5eb10ae6ea1fd24e970e96546576ebf9b8ac1ac4cef3` | closed, ratified |
| `phase_7_stage_b_1.md` | `b34fc38eb69804165dcf1a9eb65351a0c6b0a4648895c17e5c4b408b7b635d9e` | closed, ratified |
| `phase_7_stage_b_2.md` | `c46186b173d813bdbdca82e98a3a13618d2a2e30aca4ceebd89503fdafb18a21` | closed, ratified |
| `phase_7_stage_b_3.md` | `ea12517cec7deee48818a097e942d08601fda5a0f381e215a7df2c508c801c30` | closed, ratified |
| `phase_8a_lite.md` | `bf4ba9a94f250abad61d33a842bdedf2e7c8571a3fe61b1d3323c25601dbe888` | closed, ratified |
| `phase_8_b_1.md` | `b6d5c7a1ea0aaffa7b2a27dc31d96fd8c64f1ff071caf75913ffe6dde6c3f1fe` | closed, ratified |
| `phase_8_b_2.md` | `1b4d703d81dad6e80ba1d396ea3668ae29f06180d2eb47e75420e08b383ee580` | closed, ratified |
| `phase_8_b_3.md` | `a31b5a9d43c0563140a73762789f765390187052ebd4e24b47d9bb6a528f7215` | closed, ratified |
| `phase_8_b_4.md` | `21d2f5193cfb53fbb3ec2c35f293e78f7bd535f446a969137b4bad8758fdb3b8` | closed, ratified |
| `commercial_cut_2026_07_06.md` | `bbf14900c7e51514e8be687597a5b046e445dc8fbc7db4f8ec8c853a62f20d90` | closed, ratified (subtractive) |
| `phase_8_conformance_map.md` | `e747a0f6ee815b003d4962dac515b0743451747b1ef4812fa824e6cbe98874e7` | closed, ratified |
| `phase_8_b_5a.md` | `c48672b4562f330129396ef3b90aaffdfb45f6c2714a671e4aaee2953a7c8baf` | closed, ratified |

### B.4 Still-unbuilt UI surfaces (from UI Spec v2.1 + BCR v1.4)

**Compliance Console:**
- §4.4 "The compliance rulebook (NEW)" — write UI for retention windows / disclosure thresholds (k-anonymity, l-diversity, DP budget) / lawful-basis registry / source-standing table
- §4.5 "Write mechanics under the checker (Section 8)"

**Administration Console (§6):**
- §6.4 Scope split: compliance rules render read-only with "owned by Compliance" marker (**B-4 retrofit RT-R1 pending, atomic with B-5b**)
- §6.5 Roles-and-rights capability (unbuilt)
- §6.6 Counter-sign duties (banner surface for pending items — pending §8 checker)

**Extraction Console:**
- §3.4 "Sampling — sample-before-commit (lands with Phase 9)" — narrow-reach objective sample UI
- §3.5 "Registry administration (capability; screens land with Phase 9)"

**Integration Console (Engineer):**
- §5.4 8-EXT dual-actor scoping: external_engineer role additive to identity.roles + view scoping on 3 existing screens (small; unbuilt)
- §5.5 governed-extract API operator provisioning surface (unbuilt — sequenced after B-5b per §5.1 order 5)

**Cross-console:**
- §8 consequence-class checker — pending banners on BOTH Compliance + Administration consoles (unbuilt)

### B.5 Still-open BCR v1.4 completion gates (unbuilt)

| Family | Gates | Phase |
|---|---|---|
| **AS-** Artifact store | AS-B1 AS-B2 AS-B3 AS-G1 AS-G2 AS-G3 AS-G4 AS-H1 AS-I1 AS-R1 AS-U1 AS-U2 | §3.2 — dispatchable soon |
| **BM-** Benchmark | BM-V1 BM-V2 BM-C1 BM-C2 | §3.3 — inside Phase 9 |
| **CK-** §8 Checker | CK-B1 CK-B2 CK-B3 CK-G1 CK-G2 CK-G3 CK-G4 CK-G5 CK-H1 CK-I1 CK-U1 | §3.11 — sub-stage 3 of Seam 3 dispatch |
| **EE-** 8-EXT External Engineer | EE-R1..4 EE-G1..4 | §3.9 — after B-5b, before Phase 9 Stage B |
| **FL-** Answer fluency | FL-R1 FL-R2 | §3.8 — post-B-5b |
| **PH-** Production packaging | PH-R1..4 | §3.4 — destination-agnostic; slot flexible |
| **RT-** B-4 retrofit | RT-R1 RT-R2 RT-G1 | §3.13 — atomic with B-5b |
| **SM-** Sampling | SM-E1..3 SM-G1..5 SM-I1..3 | §3.12 — extraction expression with Phase 9; integration expression post-artifact-store |
| **TF-** Transform forms | TF-R1 TF-R2 TF-R3 | §3.7 — post-B-5b |
| **V1-** Extraction | V1-B1..4 V1-D1 V1-D2 V1-G1..7 V1-H1 V1-H2 V1-I1..4 V1-U1 | §3.1 — Phase 9 Stage A dispatchable now |
| **B5a/B5b/S3** | B5a-G1/G2/G3 GREEN · B5b-G1..4 · S3-R1..3 · B5a-R1..3 · B5b-R1..3 | §3.5 + §3.6B — Seam 3 → B-5a done → B-5b + retrofit |

═══════════════════════════════════════════════════════════════════

## C. Current build-plan digest (verbatim scope per phase)

**Where we are now:** Phase 8 Stage B-5a CLOSED, ACCEPTED 2026-07-06.
Phase 8 Seam 3 + §8 Checker Stage A proposal DELIVERED 2026-07-06,
pending Owner ratification (E1-E6 escalations flagged).

### C.1 Phase 8 Seam 3 + §8 Checker (dispatched Stage A, awaiting rulings)

**Split into 3 sub-stages (per Stage A proposal §3):**

#### Sub-stage 1 — (b) Refusal-family ledger wire-up + first-commit coverage marker

- **Goal:** close B-5a §V.4 governance-bites debt (un-ledgered refusal families) + land Owner-ruled first-commit coverage marker on v2.1 §4.1 Refusals card.
- **In-scope surfaces (backend):** `services/northena/refusal_ledger.py` (NEW canonical single-source `emit_refusal_ledger_row`); `services/compliance/coverage_marker.py` (NEW); `refusal_family_since_dates.v0.json` (NEW versioned config); 4 emission-site instrumentations at `async_worker.py:97-108`, `async_worker.py:129-131`, `service.py:187-192`, `composed_conclusion.py:272-273`; dead-stub migration note at `async_state.py:238`.
- **In-scope endpoints:** `GET /api/compliance/refusals_coverage` (new; auth: same as existing `/api/compliance/refusals`).
- **In-scope frontend:** `RefusalsCoverageMarker.jsx` component (new; barrel-registered); `ComplianceHomePage.js` (extend refusals card to render coverage marker); Playwright chromium smoke.
- **Test matrix cells:** 30 backend + 5 frontend + 1 Playwright spec = **35 cells** (endpoints × auth postures × emission-site combinations enumerated in Stage A §4).
- **LoC budget:** `[1400, 1800]` (per Stage A §4). Per-bucket: backend impl ~365 + backend tests ~770 + frontend impl ~145 + Jest ~150 + Playwright ~55 = **~1485L**.

#### Sub-stage 2 — (a) Authorized deletion path

- **Goal:** land BCR §3.5 Seam 3 — retention-config write endpoint + deletion executor + invariant re-scope from `no_deletion_path` → `no_unauthorized_deletion_path`.
- **In-scope surfaces (backend):** `services/retention/authorized_deletion.py` (NEW single-source-of-deletion); `services/compliance/retention_config_writes.py` (NEW); `retention.v0.json` (NEW versioned config).
- **In-scope endpoints:** `POST /api/compliance/retention_config` (write half; DPO auth); `POST /api/compliance/authorized_deletion` (executor; DPO auth).
- **In-scope invariant:** `test_no_unauthorized_deletion_path` AST gate (whitelist-positive `authorized_deletion.py`; grep-negative elsewhere).
- **In-scope frontend:** **NONE at sub-stage 2** (per proposed E2 disposition; UI lands with B-5b per §3.6B).
- **Test matrix cells:** 67 backend + 0 frontend = **67 cells** (endpoints × auth postures × rule shapes × held-classes enumerated in Stage A §5).
- **LoC budget:** `[2500, 2900]` (E1.α stamp_audit-only) OR `[2500, 3100]` (E1.β adds NorthenaLedgerRow_v2 contract).

#### Sub-stage 3 — (c) §8 Consequence-class checker

- **Goal:** land BCR §3.11 checker per CK-B1/B2/B3 with 5 named gates CK-G1..G5.
- **In-scope surfaces (backend):** `services/checker/{consequence_classes,rule_change_request,state_machine,effective_delay,countersign_ledger}.py` (NEW modules); `consequence_class.v0.json` (NEW versioned config; `rule_class → tightening_unilateral|dual_control` map + `effective_delay_seconds`).
- **In-scope endpoints:** `POST /api/checker/initiate`; `POST /api/checker/countersign/{request_id}`; `POST /api/checker/object/{request_id}`; `GET /api/checker/pending`.
- **In-scope frontend:** `CounterSignBanner.jsx` (NEW; barrel-registered); Compliance + Administration Home page extensions; Playwright chromium smokes × 2 consoles.
- **Test matrix cells:** 36 backend + 11 frontend + 2 Playwright specs = **49 cells** (state transitions × postures × dual-control + tightening + objection + delay paths enumerated in Stage A §6).
- **LoC budget:** `[2000, 2500]` (per Stage A §6). Per-bucket: backend impl ~720 + backend tests ~1080 + frontend impl ~255 + Jest ~225 + Playwright ~110 = **~2390L**.

### C.2 Phase 8 Stage B-5b — Compliance Console rulebook writes (dispatched AFTER Seam 3 + §8 checker)

- **Goal:** BCR §3.6B — Compliance rulebook write UI for retention/disclosure/lawful-basis/source-standing under §8 checker; **atomic with B-4 retrofit RT-R1** (compliance classes render read-only on Admin console).
- **In-scope surfaces:** v2.1 §4.4 + §4.5 Compliance write UI; §6.4 Admin read-only reclassification.
- **In-scope endpoints (proposed):** `POST /api/compliance/rulebook/{class}` (retention / disclosure / lawful_basis / source_standing); each triggers §8 checker rule-change-request emission.
- **In-scope frontend:** New Compliance Console write pages (§4.4 + §4.5); Admin console mutation (read-only markers on 4 compliance classes).
- **Test matrix cells:** not yet estimated (dispatch pending); B5b-G1..G4 named gates enumerated in BCR §3.6B.
- **LoC budget:** not yet estimated (dispatch pending).

### C.3 Phase 9 — V1 Extraction (Stage A dispatchable NOW per BCR §3.1)

- **Goal:** close V1 vertical — raw AV through GPU perception + CMS/social direct intake, both to qualified units.
- **In-scope frozen contracts:** `PerceptionJob_v0` + `PerceptionResult_v0` (2 new; freeze argued at Stage A per D4b priors); **parity 26 → 28 conditional**.
- **In-scope endpoints:** worker-only `POST /api/workers/jobs/claim`, `POST /api/workers/jobs/{job_id}/result` (idempotent on (job_id, checkpoint)).
- **In-scope surfaces:** job dispatcher (extends existing 5-state machine); intake validator; deterministic stub worker; source connectors (archive reader + CMS + social).
- **In-scope UI:** V1-U1 NO NEW SURFACE (operator surface's existing elements become real once telemetry fires).
- **Test matrix cells:** V1-G1..G7 named gates + intake regression parametrised.
- **LoC budget:** not yet estimated (Stage A pending).
- **Owner bindings [OWNER]:** Topology selection; archive access path; Hour A + Hour B + 300-unit human-qualified slice.

### C.4 Post-B-5b sequence per BCR §5.1

Per BCR §5.1 verbatim builder-side order:

3. **Artifact store (§3.2)** — AS-B1..B3, AS-G1..G4, AS-I1, AS-U1..U2, AS-R1. Unblocks V3 done-condition + dependency of §3.7.
4. **Phase 9 Stage B** — GPU half + BM-V benchmark; runs when [OWNER] material lands.
5. **8-EXT dual-actor engineer scoping (§3.9)** — small; after B-5b, before Phase 9 Stage B. EE-R1..4 + EE-G1..G4.
6. **Transform forms (§3.7)** + **fluency (§3.8)** — TF-R1..R3 (knowledge_artifact + callable_skill) + FL-R1 FL-R2 (LLM-behind-composed-conclusion). Both post-B-5b.
7. **Sampling (§3.12) integration expression** — SM-I1..I3 + SM-G1..G5 — post-artifact-store; extraction expression (SM-E1..E3) lands inside Phase 9.
8. **Production packaging (§3.4)** PH-R1..4 — destination-agnostic; slot flexible.
9. **B-4 retrofit (§3.13)** RT-R1 RT-R2 RT-G1 — atomic with B-5b (moves compliance classes to read-only on Admin).

═══════════════════════════════════════════════════════════════════

## D. Reuse vs. new-build assessment

**(See table inline in return message.)**

═══════════════════════════════════════════════════════════════════

## E. Risk register for remaining work

### E.1 Contract-adjacent risks (frozen contracts)

- **E1 escalation (Seam 3 sub-stage 2 + §8 checker sub-stage 3):** `NorthenaLedgerRow_v1.stage: Literal["admit","gate","converge"]` + `decision` Literal do NOT semantically contemplate deletion events (`data_class="authorized_deletion"`) or rule-change events (`data_class="countersigned_rule_change"`). Two options:
  - **E1.α** — stamp_audit-only disambiguation. Parity 26 unchanged. Precedent: Phase 6 Stage B quote-mint. Honesty cost: `stage`/`decision` stretched semantically.
  - **E1.β** — HAZARD-STOP (a): NorthenaLedgerRow_v2 contract addition. Parity 26→27 at sub-stage 2 close. Standing Disposition `frozen-field-changes-as-new-versions` applies.
- **QuoteEnvelope_v0 orphan-in-place (§12.3 PRES-3):** contract file byte-identical, nothing imports live, salvage copy exists. STAKED alternative PRES-3-ALT (vacate) is a HAZARD-STOP against additive-only invariant — untouched at commercial cut close.
- **Phase 9 freezes 2 new contracts:** `PerceptionJob_v0` + `PerceptionResult_v0` cross environment boundary; D4b priors freeze; parity 26→28.
- **Artifact store §3.2:** may need new frozen contract for key-format shape (TBD at Stage A).

### E.2 First-commit gating risks (UI + smoke land together)

- **Seam 3 sub-stage 1** already carries first-commit rider (coverage marker). Cell count 35 / LoC ~1485 — well within budget.
- **§8 checker sub-stage 3** requires banner on BOTH consoles + 2 Playwright specs in same commit. Cell count 49 / LoC ~2390 — mid-band.
- **B-5b** rulebook writes + B-4 retrofit ATOMIC per RT-R2. Not yet sized but 4 write endpoints × new UI × §8 integration + retrofit AST gate likely pushes total cells > B-5a's 55. **Anticipate SPLIT PROPOSAL at B-5b Stage A** (similar to Seam 3).
- **Phase 9 Stage B** GPU half + benchmark + 2 new frozen contracts + intake regression suite = highest cell count of any single dispatch. **Anticipate multi-sub-stage SPLIT at Phase 9 Stage A.**

### E.3 Governance / escalation debt still open (E1-E6 from Stage A)

| # | Class | Blocks | Ruling scope |
|---|---|---|---|
| E1 | governance-semantic (frozen-contract touch) | Seam 3 sub-stage 2 + §8 checker sub-stage 3 | stamp_audit-only vs NorthenaLedgerRow_v2 |
| E2 | governance-semantic (surface ownership) | Seam 3 sub-stage 2 | Retention write UI in Seam 3 or B-5b? |
| E3 | owner-value (config content) | Seam 3 sub-stage 1 | Coverage-marker `{date}` composition method |
| E4 | dev-preference (module placement) | Seam 3 sub-stage 1 | `emit_refusal_ledger_row` home |
| E5 | auth codes (none needed) | — | Confirmatory only |
| E6 | page existence read | §8 checker sub-stage 3 | Master Admin Home page existence — **CONFIRMED EXISTS** at `pages/master_admin/MasterAdminHomePage.js` (this recon) |

### E.4 Real-hour material dependencies (G2b + Phase 9 Stage B)

- **G2b remains BLOCKED** awaiting Hour A / Hour B / 300-unit human-qualified sample. Same substrate feeds Phase 9 Stage B benchmark BM-V.
- **Phase 9 Stage A** (design-only) is dispatchable NOW without any real material.
- **Phase 9 Stage B (GPU half + BM-V)** holds on: (a) topology selection (Topology A/B fork); (b) archive access path facts; (c) 1 real hour + 300-unit slice. Owner-side critical path per BCR §5.2.
- **BM-C calibration** flows post-core continuously; first numbers stay provisional until [OWNER] thresholds.

### E.5 Standing invariants + rules currently under load

- 26 frozen contracts byte-identical (`test_frozen_contract_snapshot_parity.py` bijective; MAN-G1 18/18 GREEN).
- No LLM outside Shield (`services/synisense/` boundary preserved; grep-negative gates).
- §0.1 Standing Owner Dispositions FROZEN (13 total; zero new at B-5a; zero new expected at Seam 3 + §8 checker).
- §0.2 Plan Debts: 1 IN-PROGRESS (Async-worker + Service_1 refusal families un-ledgered — resolves at Seam 3 sub-stage 1 close); 11 prior RESOLVED.
- Substrate-drop gate 13/13; MAN-G1 18/18; first-commit gating (Playwright chromium-only).
- Escalation-cap ORIGINAL wording preserved.
- Standing Rule v3 delivery.

═══════════════════════════════════════════════════════════════════

## F. Rough sizing

**(See table inline in return message.)**

═══════════════════════════════════════════════════════════════════

## G. Spec contradictions noticed (v2.1 UI × v1.4 BCR × current Stage A proposal)

**(See list inline in return message.)**

═══════════════════════════════════════════════════════════════════

*End of recon. Read-only. No code touched.*
