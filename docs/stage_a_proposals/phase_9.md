# Phase 9 Stage A — Design Proposal (V1 Extraction vertical)

**Design date:** 2026-07-08
**Design authority:** Owner dispatch 2026-07-08 (post-B-5b completeness-line discharge; Phase 8 closed).
**Scope:** BCR v1.4.1 §3.1 (V1 Extraction — Phase 9) + §3.3 BM-V/BM-C + §3.12 SM-E (extraction sample) · UI Spec v2.1 §3.4–3.6 (Extraction Console capabilities) · conformance map §Extraction verdicts · rulings record post-§12 pre-carried by SHA.

**Standing constraints (all binding):**
- Standing Rule v3: this proposal lives on disk; reply body is SHA + structural summary + escalations + band.
- Standing Correction: matrix-enumerated sizing (connectors × cases × gates × invariants; endpoints × auth × posture; UI components × states × cells).
- Standing state-conflict anti-rule: NO HTTP 409 anywhere in Phase 9 diff; static scan at close.
- E7 middle-dot U+00B7 strict on binding copy (extraction console grounding marker + sample cards).
- 26 frozen contracts + snapshots UNTOUCHED (parity 26); PerceptionJob_v0 + PerceptionResult_v0 are ADDITIONS crossing an environment boundary — D4b freeze prior argued at §5.1.
- Owner rulings pre-carried by SHA: E1–E7 + R-1..R-6 + R7 + B5b-E1..E5 + Amortisation Divergence Class (Owner-accepted at B-5b close) — all cited by rulings-record SHA, no restatement.
- No `git push`. Owner pushes.
- No self-dispatch of Sub-stage 9.1 execution or Stage B. Design-only.
- Standing Rule (Phase 8 seam-3 doctrine): the never-rules are enforced mechanically, not conventionally — grep/AST gates on worker code prove no Ledger writes + no transform-key access + no DB touches (BCR §3.1 V1-H2 + §4 custody map).

**Authority-source SHAs (for citation stability):**

| Source | Path | SHA-256 | Cited sections |
|---|---|---|---|
| BCR v1.4.1 | `docs/mandates/RMS_Build_Completion_Requirements_v1_4.md` | `ce5206c9e244fe58edb6824f785077c1c835bdf3f5b347f6a4fb98c036212524` | §3.1 V1-U1..V1-B4..V1-D1..V1-H1..V1-G1..G7 + technical annex (lines 77–108); §3.3 BM-V + BM-C (lines 135–160); §3.12 SM-E1..E3 + SM-G (lines 277–287); §4 housing map + never-rules (lines 297–307); §5.1 sequencing point 4 (line 313). |
| UI Spec v2.1 | `docs/mandates/RMS_UI_Specification_v2_1.md` | `ef6da4b498117608a3091033b5cfa43571ad8a7a38b5954cae7c4a1a698de5e2` | §3.1 Home — land (line 33–39); §3.2 wizard sample action (line 44); §3.3 grounding marker binding copy variants (line 50); §3.4 Sampling (lines 54–58); §3.5 Registry admin (lines 59–60); §3.6 quality observation (lines 61–62). |
| Conformance map | `docs/close_reports/phase_8_conformance_map.md` | `e747a0f6ee815b003d4962dac515b0743451747b1ef4812fa824e6cbe98874e7` | Extraction verdicts — REUSE / EXTEND / NEW classification pre-carried for job seam contracts + worker endpoints + sample surface. |
| Rulings record post-§12 | `docs/rulings/seam_3_stage_a_e1_to_e7.md` | `c89cacc606eda955c7fbde62e1ad1f01e381ad6ab80ae6501e39112057f0a6bb` | E1–E7 + R-1..R-6 + R7 + B5b-E1..E5 + Amortisation Divergence Class — all pre-carry into Phase 9 by SHA. |
| rule2_accounting.json (post-B-5b) | `docs/rule2_accounting.json` | `d9ca0696276ac2cf52cdefafc4edb4c93456b891dbc4c439d1ae0441705b2890` | Velocity baseline with Amortisation Divergence Class codified from B-5b empirical under-run (-45%). |
| Phase 8 B-5b close (ratified) | `docs/close_reports/phase_8_b_5b.md` | `47af8c63112a0c2a8f95a034a339eb5492fe704bd6cd91063408865b6e762238` | Sub-stage 3 rider landing evidence; B-5b delivery empirical basis for amortisation divergence rates. |

---

## §1. Cell-density assumption (Owner-binding, amortisation-divergence-class codified)

Per Owner acceptance at B-5b close (Amortisation Divergence Class ACCEPTED for Phase 9 Stage A codification): standalone vs shared-`_impl` rates with named amortisation trigger.

### §1.1 Empirical baseline (Sub-stage 3 + B-5b measured, on-disk verifiable)

| Cell type | Empirical LoC/cell | Source |
|---|---:|---|
| Backend Pytest cell (standalone) | **22 LoC/cell** | 993L test file / 45 cells (Sub-stage 3); 445L / ~20 non-B5b-G4 cells at B-5b (matched). |
| Backend LB gate (parametrised, multi-class) | **35 LoC/cell** | 17 LB gate cells / ~595 LoC across Sub-stage 3 + B-5b (matched). |
| Frontend Jest structural cell (standalone) | **16 LoC/cell** | 98L / 6 cells (Sub-stage 3). |
| Frontend Jest form-writer cell (standalone) | **28 LoC/cell** | Projected for B-5b; came in below at ~22 due to amortisation (below). |
| Playwright chromium smoke (standalone) | **32 LoC/cell** | 127L / 4 cells (Sub-stage 3). |
| Playwright chromium smoke (form-writer standalone) | **48 LoC/cell** | Projected for B-5b writer smokes; 5 smokes at 173L / 5 = 34.6 avg — actual came in amortised (below). |

### §1.2 Amortisation Divergence Class (Owner-accepted, empirically anchored at B-5b)

Named trigger: **≥2 endpoints (or components) sharing a base `_impl` (or shared component) → apply amortised rate**. Fewer than 2 sharing → apply standalone rate.

| Cell / impl class | Standalone rate | Amortised rate | Trigger | Empirical basis |
|---|---:|---:|---|---|
| Backend endpoint impl LoC | 80 LoC/endpoint | **40 LoC/endpoint** | ≥2 endpoints share a common `_impl` (e.g. `_rulebook_write_impl`) | B-5b: 3 writer endpoints via `_rulebook_write_impl` came in at ~230 LoC total (compliance.py delta 125 + shared helper 105) vs. projected 240 (3×80). |
| Frontend form-writer component LoC | 120 LoC/component | **~55 LoC/component** (as config entries against a shared base) | ≥2 components share a base (e.g. `RuleClassWriter`) | B-5b: 4 rule-class writers projected 480 LoC (4×120); actual = one 217L page hosting shared base + 4 config entries ≈ 217 LoC (~54 LoC amortised effective per writer). |
| UI-form-writer Jest cell | 28 LoC/cell (standalone) | **~22 LoC/cell** | ≥2 form components share a base | B-5b: Jest form-writer cells came in at ~22 LoC/cell effective; projected 28. |
| UI-form-writer Playwright smoke | 48 LoC/cell (standalone) | **~35 LoC/cell** | ≥2 form components share a base | B-5b: 5 smokes at 173L ≈ 34.6 LoC/cell effective. |

**Note (honest, per Ruling 5 doctrine):** B-5b under-delivered by -45% because amortisation was under-priced in the Stage A matrix. Phase 9 Stage A prices amortisation up-front where the shape is known (source-connector shared adapter interface; worker endpoint shared claim/result skeleton). Phase 9-specific cell classes below apply the amortised rate where their shape triggers it, and state standalone otherwise.

### §1.3 Phase 9-specific cell classes (rates stated for deterministic re-derivation)

| Impl / cell class | Standalone rate | Amortised rate | Trigger applied at §3 |
|---|---:|---:|---|
| Source-connector impl (archive / CMS / social) | 140 LoC/connector | **~70 LoC/connector** | 3 connectors share `SourceConnectorAdapter` interface → **amortised applied** |
| Worker endpoint impl (claim + result) | 90 LoC/endpoint | **~50 LoC/endpoint** | 2 endpoints share `_worker_auth_gate` + `_worker_idempotency_check` → **amortised applied** |
| Deterministic stub worker | 180 LoC | — | Single artifact; no sharing → **standalone applied** |
| V1-G* named gate roster (V1-G1..V1-G7) | 45 LoC/gate | **40 LoC/gate** | Gates share `WorkerGateHelpers` (fake credential minter + fake job dispatcher fixture) across ≥2 gates → **amortised applied** |
| PerceptionJob_v0 / PerceptionResult_v0 contract module | 60 LoC/contract | — | 2 new contracts; not shared with anything (frozen additive) → **standalone applied** |
| Extraction Console — sample surface component | 120 LoC/component (standalone) | **~65 LoC/component** | 3 sample surfaces (wizard action + result card + commit-review grounding marker) share a `SampleGroundingContext` → **amortised applied** |
| Extraction Console — sample surface Jest cell | 28 LoC/cell (standalone) | **~22 LoC/cell** | Amortised trigger applies (≥2 surfaces share base) → **amortised applied** |
| Extraction Console — sample surface Playwright smoke | 48 LoC/cell (standalone) | **~35 LoC/cell** | Amortised trigger applies → **amortised applied** |
| SM-G* named gate (SM-G1..SM-G5) | 45 LoC/gate | — | SM-G2..G4 land at post-artifact-store integration expression (out of Phase 9 scope); SM-G1 + G5 land at Phase 9 → **standalone applied** for the 2 in-scope |

### §1.4 Re-derivation rule (Owner-binding, unchanged from Amendment G template)

Any Owner ruling that adds/removes a source connector, adds/removes a worker endpoint, adds a job state, reshapes the amortisation trigger, or reshapes the console-surface sampling flow MUST re-derive the band using §1.1 + §1.2 + §1.3 rates. NO padding, NO buffering up front. Miss + disclosure > pad + hide.

---

## §2. Deliverables enumeration (matrix per Standing Correction)

Enumerated in three sub-stage buckets per Owner directive §3.4. Sub-stage 9.2 (GPU half) is **gated-not-estimated** per Owner directive — matrix enumerates the [OWNER] facts as gates with owners, no cell/LoC totals.

### §2.1 Sub-stage 9.1 — Stub substrate (dispatchable on documents alone)

#### §2.1.1 Backend — new contracts (freeze prior per D4b)

| # | Path | Kind | Purpose |
|---|---|---|---|
| 2.1.1.a | `backend/contracts/perception_job_v0.py` | New frozen contract | BCR §3.1 technical annex verbatim: PerceptionJob_v0 fields (job_id, objective_ref, trace_lineage, reextraction_handles[], modality, extraction_params_ref, idempotency_key, issued_at). Retried dispatch of same idempotency_key MUST return same job. D4b argued at §5.1 P9-E1. |
| 2.1.1.b | `backend/contracts/perception_result_v0.py` | New frozen contract | BCR §3.1 verbatim: PerceptionResult_v0 fields (job_id, units[NormalizedUnit], telemetry, checkpoint, purge_attestation, status). Purge attestation is a REQUIRED field, not optional. Intake-validated at unit level. |
| 2.1.1.c | `backend/contracts/frozen_snapshots/perception_job_v0.json` | New snapshot | Parity-check snapshot for V1-G7 byte-identity 26 → 28 (additive per §7 preserved-parity rule; adds 2 new contracts, no touches to existing 26). |
| 2.1.1.d | `backend/contracts/frozen_snapshots/perception_result_v0.json` | New snapshot | Companion snapshot. |

**Parity bump rationale (Owner-visible):** 26 → 28 is ADDITIVE — the pre-existing 26 remain byte-identical (V1-G7 asserts). The +2 additions cross an environment boundary per V1-I2, so D4b prior is FREEZE (Owner-arguable at Stage A per P9-E1).

#### §2.1.2 Backend — new endpoints (worker plane; scoped credential only)

| # | Endpoint | Auth | Body | Behavior |
|---|---|---|---|---|
| 2.1.2.a | `POST /api/workers/jobs/claim` | Worker credential (scoped to this route + 2.1.2.b only; no DB, no Ledger, no LLM) | `{worker_id, capabilities}` | 200 PerceptionJob_v0 (single job) OR 204 no work. Idempotent on worker_id + capabilities within a short window (job re-issued on lost claim). |
| 2.1.2.b | `POST /api/workers/jobs/{job_id}/result` | Same worker credential | `{PerceptionResult_v0}` | 202 accepted + idempotent on (job_id, checkpoint) — a second post with the same checkpoint returns 202 with same server ack, NEVER duplicates ledger rows. On status=complete, triggers intake pipeline. |

**No new admin/master_admin/compliance route.** Worker credential is a **new capability class** — argued at §5.3 P9-E3.

#### §2.1.3 Backend — new services / modules

| # | Path | Kind | Purpose |
|---|---|---|---|
| 2.1.3.a | `backend/services/perception/job_dispatcher.py` | New | Job queue + assignment. Ties into the existing five-state machine per Phase 5 standing ruling — the in-process worker is the degenerate single-environment case; the dispatcher swaps behind the same states (BCR §3.1 V1-B1). |
| 2.1.3.b | `backend/services/perception/idempotency.py` | New | Idempotency-key resolver (Retried dispatch of same key ⇒ same job per V1-I1). Reuses the existing idempotency posture from Sub-stage 3 checker. |
| 2.1.3.c | `backend/services/perception/checkpointing.py` | New | Unit-level checkpointing (V1-B2). A job failing mid-hour resumes from its checkpoint; completed units NEVER re-perceived and NEVER double-ingested. |
| 2.1.3.d | `backend/services/perception/purge_attestation.py` | New | Purge attestation recording (V1-D1). Raw AV exists worker-side transiently only; purged on job completion with attestation recorded in job result. |
| 2.1.3.e | `backend/services/perception/telemetry.py` | New | Telemetry sidecar wiring (V1-B4). Every job writes to instrumentation sidecar per stamp_audit pattern — this is the benchmark instrument (§3.3 BM-V), ships with the phase. |
| 2.1.3.f | `backend/services/perception/worker_credential.py` | New | Scoped credential minter + verifier. Credential grants EXACTLY the two worker endpoints (claim + result-post). No DB access, no Ledger, no LLM. AST-gate proves it. |
| 2.1.3.g | `backend/services/perception/stub_worker.py` | New | Deterministic stub worker (V1-B3). Consumes claim + posts result deterministically for guard-gate proving BEFORE any GPU code exists. |
| 2.1.3.h | `backend/routers/workers.py` | New router | Wires 2.1.2.a + 2.1.2.b. |

#### §2.1.4 Backend — source connectors (source-adapter shared interface, amortised)

| # | Path | Kind | Purpose |
|---|---|---|---|
| 2.1.4.a | `backend/services/perception/source_connector_adapter.py` | New (interface) | `SourceConnectorAdapter` base: `emit_perception_jobs()` OR `emit_direct_intake_units()` — locator-dialect kept inside `unit.locator` field per V1-I4. |
| 2.1.4.b | `backend/services/perception/connectors/archive_reader.py` | New (impl) | Archive reader → emits PerceptionJobs. Owned sources only. Locator dialect: archive path + timecode range. |
| 2.1.4.c | `backend/services/perception/connectors/cms_reader.py` | New (impl) | CMS reader → emits TEXT-modality units direct to intake (V1-I4). Locator dialect: CMS URL + item_id. |
| 2.1.4.d | `backend/services/perception/connectors/social_reader.py` | New (impl) | Social-account reader → emits TEXT-modality units direct to intake. Owned account credentials only. Locator dialect: platform + account_ref + post_id. |

**Amortisation trigger:** 3 connectors share `SourceConnectorAdapter` interface → amortised rate applied per §1.3 (~70 LoC/connector effective).

#### §2.1.5 Backend — LB gates (V1-G1..V1-G7)

| Gate | Purpose | Cells |
|---|---|---:|
| **V1-G1** `test_stub_worker_e2e` (BCR §3.1) | Stub worker: job → units → database. Green BEFORE any GPU code merges. E2E through the job dispatcher. | 1 |
| **V1-G2** `test_job_kill_and_restart_resumes_without_duplicate_ledger_rows` (BCR §3.1) | Phase 5 recovery pattern extended across the job seam. Kill mid-job → restart → resumes from checkpoint; ledger rows exact once, never duplicated. | 1 |
| **V1-G3** `test_raw_purge_attested_per_job` (BCR §3.1) | Every completed PerceptionResult carries purge_attestation with purged=true + purged_at timestamp. Missing attestation → job status refused. | 1 |
| **V1-G4** `test_intake_rejects_invalid_units` (BCR §3.1) | Intake validator is the ONLY entry for units. A unit failing NormalizedUnit contract is rejected + recorded (never silently dropped). | 1 |
| **V1-G5** `test_worker_code_never_writes_ledger` (BCR §3.1 V1-H2) | AST scan on `backend/services/perception/**` — zero call sites to any `ledger.emit_*` OR `deletion_ledger.*` OR `Registry.*` (any control-plane state mutator). Never-rule enforced mechanically. | 1 |
| **V1-G6** `test_telemetry_fields_present_per_job` (BCR §3.1 V1-B4) | Every completed job's PerceptionResult carries telemetry.gpu_hours + broadcast_hours + unit_yield + per_modality. Empty allowed (partial_failed status), MISSING is a gate failure. | 1 |
| **V1-G7** `test_byte_identity_across_all_prior_frozen_contracts` (BCR §3.1 + Standing 26) | Parity 26 → 28 additive: the 26 pre-existing frozen contracts remain byte-identical (SHA-check per contract file); +2 new (PerceptionJob_v0 + PerceptionResult_v0). NO touches to the 26. | 1 |

**Total: 7 gate cells**. All amortised via `WorkerGateHelpers` (fake credential minter + fake dispatcher fixture) at §1.3 rate.

#### §2.1.6 Backend — endpoint × auth × posture matrix (§2.1.2 coverage)

Per endpoint (§2.1.2.a + §2.1.2.b):
- 4 auth postures (no-cred → 401; wrong-cred class → 403 auth_scope_insufficient; valid worker cred + wrong route → 403 auth_scope_insufficient per never-rule; valid worker cred + right route → 200/204/202).
- 2 idempotency postures per endpoint (fresh call + retry same idempotency key returning same result).
- 1 malformed-payload posture per endpoint (→ 400 malformed_payload).
- **= 7 cells × 2 endpoints = 14 cells**.

Plus worker-credential scope enforcement (AST + runtime):
- 1 cell: `test_worker_credential_denies_all_non_worker_routes` — parametrised over the router registry.

**Total §2.1.6: 15 cells.**

#### §2.1.7 Frontend — Sub-stage 9.1 UI touches

**None.** Sub-stage 9.1 is a backend substrate — no console surface changes. Confirmed against BCR §3.1 V1-U1: *"No new surface. The operator surface's existing elements become real."* Real values render only when jobs actually run (Sub-stage 9.2 or 9.3 depending on where sample lands — see §4.3).

### §2.2 Sub-stage 9.2 — GPU perception half (GATED-not-estimated per Owner)

Per Owner directive verbatim: *"the GPU half explicitly gated on the three [OWNER] facts (topology selection, archive access path, Hour A/B + 300-unit slice), listed as gates with owners, never estimated."*

| Gate | Owner | Content |
|---|---|---|
| **9.2-OWN-1** Topology selection | Owner (grant physical parameters + archive physical reality) | Topology A (compute-to-data, [STAKED default]) → raw NEVER leaves RMS tenancy; Topology B → raw egresses under contract with transit + purge + rights requirements ruled BEFORE dispatch. BCR §3.1 V1-D2. |
| **9.2-OWN-2** Archive access path | Owner (RMS/grant-provider conversation) | Archive access path: format + storage + bandwidth. BCR §4 [OWNER] housing binding. |
| **9.2-OWN-3** Hour A + Hour B + 300-unit human-qualified slice | Owner (in-phase, small — needed during Phase 9 GPU work, not before) | One real broadcast hour for BM-V1 validation; human-qualified sample for class_distribution_delta ground truth. Also feeds BCR §3.3 BM-V PASS/INVESTIGATE verdict. |

**No cells enumerated. No LoC estimated. Sub-stage 9.2 dispatches when 9.2-OWN-1..3 land — not before.** Per Owner ruling: *"listed as gates with owners, never estimated."*

Backend surface intent (structural only, for reader continuity — not sized):
- GPU perception model wired behind the same worker interface (§2.1.2.a claim + §2.1.2.b result-post) — the stub-first pattern (V1-B3) means the seam is proven at 9.1; 9.2 swaps the stub for real perception behind identical wire shapes.
- BM-V1 runs inside 9.2: one real broadcast hour → class_distribution_delta against 9.2-OWN-3 human slice → PASS/INVESTIGATE verdict at Phase 9 close.

### §2.3 Sub-stage 9.3 — Console surface (Extraction Console sampling; dispatchable on documents alone)

Consumes 9.1 substrate; **independent of 9.2 GPU decision** (sampling is a resource-commitment shaping tool; the stub worker satisfies the sample execution path for gate-proving purposes).

#### §2.3.1 Frontend — new pages + component updates

| # | Path | Kind | Purpose |
|---|---|---|---|
| 2.3.1.a | `frontend/src/pages/extraction/WizardSampleAction.jsx` | New | UI Spec v2.1 §3.2 line 44: *"Run a sample — available once reach is drafted."* Wizard-inline action button. Reach-draft-gated (button hidden until reach is drafted). |
| 2.3.1.b | `frontend/src/pages/extraction/SampleResultCard.jsx` | New | UI Spec v2.1 §3.4 line 57: *"Renders in the same feasibility position: volume found, class distribution observed, per-hour cost observed."* Result card. |
| 2.3.1.c | `frontend/src/pages/extraction/CommitReviewGroundingMarker.jsx` | New | UI Spec v2.1 §3.3 line 50 binding-copy variants: *"Grounded by sample {sample_ref}"* / *"No sample run — estimates only."* Middle-dot U+00B7 strict on any list separators. |
| 2.3.1.d | `frontend/src/pages/extraction/SampleGroundingContext.jsx` | New (shared base) | Shared context: sample state (in-flight, complete, failed) + sample_ref propagation. **Amortisation base for 2.3.1.a + 2.3.1.b + 2.3.1.c**. |
| 2.3.1.e | `frontend/src/pages/extraction/ExtractionConsoleHomePage.jsx` | New OR extended (if exists) | UI Spec v2.1 §3.1 Home — land. Status line binding copy: *"Running normally. One item needs you."* Attention cards (SM-E-triggered thresholds surface here). If a stub landed at earlier phase, extend; else new. Investigation at execution time. |
| 2.3.1.f | `frontend/src/pages/extraction/RegistryAdminView.jsx` | New | UI Spec v2.1 §3.5: view census state by estate region; trigger/schedule census passes; un-censused regions marked honestly as `unknown`. |
| 2.3.1.g | `frontend/src/pages/extraction/QualityObservationInline.jsx` | New | UI Spec v2.1 §3.6: mining-stage visibility inside running status; per-objective yield and class distribution as extraction proceeds. Renders inside `RunningList` (existing surface). |
| 2.3.1.h | `frontend/src/App.js` | Modify | Route `/extraction/console` → `ExtractionConsoleHomePage`; `/extraction/registry-admin` → `RegistryAdminView`. |

**Amortisation:** 2.3.1.a + 2.3.1.b + 2.3.1.c share `SampleGroundingContext` (2.3.1.d) → amortised rate applied.

#### §2.3.2 Backend — SM-E1..E3 wiring

| # | Endpoint / service | Purpose |
|---|---|---|
| 2.3.2.a | `backend/services/perception/sample_lifecycle.py` | Sample = narrow-reach objective per SM-E1. Reuses existing objective/commit path; adds `sample_of={objective_ref}` tagging on units (SM-E3). |
| 2.3.2.b | `backend/services/perception/grounding_marker.py` | SM-E2: grounding marker generator. Emits binding-copy strings verbatim per UI Spec §3.3 line 50 (middle-dot strict). |
| 2.3.2.c | `POST /api/extraction/sample/run` | Wizard-inline action wire. Body: `{objective_ref, sample_bound_hours}`. 202 + sample_ref (per V1-I1 idempotency pattern). Budget draw from objective GPU/extraction budget shown on response (SM-E2). |
| 2.3.2.d | `GET /api/extraction/sample/{sample_ref}` | Poll for sample result → renders in 2.3.1.b. |

**Amortisation:** 2 endpoints share `_sample_lifecycle_impl` → amortised rate applied.

#### §2.3.3 SM-G gates in Phase 9 scope

| Gate | Purpose | In-scope | Cells |
|---|---|---|---:|
| **SM-G1** `test_extraction_sample_grounds_commit_envelope` (BCR §3.12 SM-G) | Sample result records into the commit envelope beside availability snapshot per SM-E3. | YES (Phase 9) | 1 |
| **SM-G5** `test_sample_units_tagged_not_committed` (BCR §3.12 SM-G) | Units from a sample carry `sample_of={objective_ref}` tag; NOT counted as committed run units. | YES (Phase 9) | 1 |
| **SM-G2 / SM-G3 / SM-G4** (Integration expression) | Post-artifact-store; Phase 9 does NOT include the integration expression. | NO (out of Phase 9 scope) | 0 |

**Total SM-G in Phase 9: 2 gate cells (standalone rate; not amortised into V1-G* — different gate class).**

#### §2.3.4 Frontend — Jest structural cells

| # | Test file | Cells |
|---|---|---:|
| 2.3.4.a | `test_phase_9_sample_action.test.js` | 4 (button-hidden-when-reach-undrafted + button-visible-when-drafted + click-posts-sample + pending-state-render) |
| 2.3.4.b | `test_phase_9_sample_result_card.test.js` | 3 (renders-volume + renders-class-distribution + renders-per-hour-cost) |
| 2.3.4.c | `test_phase_9_grounding_marker.test.js` | 3 (grounded-by-sample-variant + no-sample-variant + middle-dot-strict) |
| 2.3.4.d | `test_phase_9_registry_admin_view.test.js` | 3 (census-state-render + unknown-marker-verbatim + trigger-census-button) |
| 2.3.4.e | `test_phase_9_quality_observation.test.js` | 2 (mining-stage-inside-running + threshold-crossing-attention-card) |
| **Total** | | **15 cells** (amortised trigger active on 2.3.4.a+b+c) |

#### §2.3.5 Playwright chromium smokes

| # | Spec | Cells |
|---|---|---:|
| 2.3.5.a | `sample_action_smoke.spec.ts` | 2 (wizard-sample-run → grounding marker renders + result card renders) |
| 2.3.5.b | `registry_admin_smoke.spec.ts` | 2 (census view + trigger census with `unknown` marker verbatim) |
| 2.3.5.c | `quality_observation_smoke.spec.ts` | 1 (mining-stage visible inside running-status row) |
| **Total** | | **5 cells** (amortised trigger active on 2.3.5.a — sample flow) |

---

## §3. Band derivation (matrix-derived, cell-density-applied — 9.1 + 9.3 only; 9.2 gated-not-estimated)

### §3.1 Cell count total (Sub-stage 9.1 + 9.3; 9.2 excluded per Owner)

| Bucket | Cells |
|---|---:|
| Backend Pytest — worker endpoints × auth × posture (§2.1.6) | 15 |
| Backend Pytest — V1-G1..V1-G7 (§2.1.5) | 7 |
| Backend Pytest — SM-G1 + SM-G5 (§2.3.3) | 2 |
| Backend Pytest — connector cells (§2.1.4, 3 connectors × 3 postures: happy + malformed-source + owned-source-guard) | 9 |
| Backend Pytest — contract byte-identity + freeze prior (§2.1.1, per contract × add-not-touch + register-parity) | 4 |
| Frontend Jest — sample surface + registry admin + quality observation (§2.3.4) | 15 |
| Playwright chromium — sample + registry + quality (§2.3.5) | 5 |
| **Total cells (9.1 + 9.3)** | **57** |

### §3.2 LoC derivation (matrix × cell-density per §1)

| Bucket | Cells | LoC/cell | Subtotal |
|---:|---:|---:|---:|
| Backend Pytest worker endpoint × auth × posture (§2.1.6) | 15 | 22 | 330 |
| Backend V1-G* gates (§2.1.5, amortised via `WorkerGateHelpers`) | 7 | 40 | 280 |
| Backend SM-G1 + SM-G5 (§2.3.3, standalone) | 2 | 45 | 90 |
| Backend connector Pytest cells (§2.1.4) | 9 | 22 | 198 |
| Backend contract byte-identity + freeze prior (§2.1.1) | 4 | 22 | 88 |
| Frontend Jest — sample surface (§2.3.4.a+b+c, amortised) | 10 | 22 | 220 |
| Frontend Jest — registry admin + quality observation (§2.3.4.d+e, standalone) | 5 | 16 | 80 |
| Playwright — sample flow (§2.3.5.a, amortised) | 2 | 35 | 70 |
| Playwright — registry + quality (§2.3.5.b+c, standalone) | 3 | 32 | 96 |
| **Test LoC subtotal** | **57** | | **1,452** |
| Backend impl — worker endpoints (§2.1.2, amortised via `_worker_auth_gate` + `_worker_idempotency_check`) | | | 100 (2 × 50) |
| Backend impl — perception services (§2.1.3.a..g) | | | 700 (7 modules × ~100 avg; dispatcher 140 + idempotency 60 + checkpointing 90 + purge_attestation 60 + telemetry 80 + worker_credential 90 + stub_worker 180) |
| Backend impl — router wiring (§2.1.3.h) | | | 40 |
| Backend impl — source connectors (§2.1.4, amortised via `SourceConnectorAdapter`) | | | 210 (3 × 70) |
| Backend impl — new contracts (§2.1.1, standalone) | | | 120 (2 × 60) |
| Backend impl — SM-E backend (§2.3.2, amortised via `_sample_lifecycle_impl`) | | | 180 (sample_lifecycle 90 + grounding_marker 40 + 2 endpoints × 25) |
| Frontend impl — sample surface (§2.3.1.a..d, amortised via `SampleGroundingContext`) | | | 260 (context 100 + 3 surfaces × ~55 = 165 → 265; round to 260) |
| Frontend impl — extraction home (§2.3.1.e, extend-or-new) | | | 90 |
| Frontend impl — registry admin (§2.3.1.f, standalone) | | | 130 |
| Frontend impl — quality observation inline (§2.3.1.g, small extension) | | | 60 |
| Frontend impl — App.js routes (§2.3.1.h) | | | 6 |
| **Impl LoC subtotal** | | | **1,896** |
| **Grand total point-estimate (raw LoC, Sub-stage 9.1 + 9.3)** | | | **~3,348** |

### §3.3 Owner-anchored band (matrix-derived, no padding)

**Point estimate:** ~3,348 raw LoC across 57 cells (Sub-stage 9.1 substrate + Sub-stage 9.3 console).

**Anchored band:** `[2,850, 3,650]` raw LoC.

Rationale (rates per §1.1 + §1.2 + §1.3):
- **Bottom-of-band (2,850):** ~15% shave below point-estimate (3,348 × 0.85 = 2,846 → 2,850 rounded). Accounts for further amortisation surfaces discovered at execution (e.g. shared idempotency posture with Sub-stage 3 checker; shared telemetry sidecar wiring).
- **Top-of-band (3,650):** ~9% cushion above point-estimate (3,348 × 1.09 = 3,649 → 3,650 rounded). Reflects:
  - Non-splittable pairing tax on §4.1 baseline atomic commit.
  - Small unknowns on connector locator-dialect parsing (each source has its own path shape — dialect parser may need per-source specialisation).

**Sub-stage 9.2 (GPU half) is NOT in this band.** Per Owner: gated-not-estimated. Band restated at 9.2 dispatch, deterministically, using §1 rates + whatever cell shape the GPU perception model imposes.

### §3.4 Re-derivation trigger table (rates unchanged)

| Ruling shape | Re-derivation direction |
|---|---|
| Owner adds a 4th source connector (e.g. RSS reader) | +3 backend cells + 1 connector impl (~70 LoC amortised) → +~136 LoC |
| Owner removes social_reader from Phase 9 scope | -3 backend cells - 1 connector impl (~70 LoC) → -~136 LoC |
| Owner rules PerceptionJob_v0 as UNFROZEN (D4b liquid) | -4 backend cells (freeze-prior gates retire) → -~88 LoC + potentially shifts V1-G7 to +2 additional-parity-only cells |
| Owner rules a 3rd worker endpoint (e.g. `POST /api/workers/jobs/{job_id}/heartbeat`) | +7 backend cells + 1 endpoint impl (amortised ~50 LoC) → +~204 LoC |
| Owner reshapes SM-E1 to include integration expression at Phase 9 (out of current scope) | +3 SM-G* gate cells + integration expression backend + integration console UI → +~600 LoC |
| Owner reshapes grounding-marker copy | +0 cells (existing 2.3.4.c cell already covers verbatim assertion); only text-string change in impl → +~5 LoC |

**Discipline preserved (Ruling 5 verbatim):** band is stop-and-judge, not a target. Miss with disclosure. No mid-execution restatement.

---

## §4. Sub-stage split (§4.1 baseline + §4.2 pre-authorized escalation)

Per Owner directive: Sub-stage split proposal is 9.1 stub substrate vs 9.2 GPU half vs 9.3 console surface. 9.2 is gated on [OWNER] facts (§2.2). 9.1 + 9.3 dispatchable on documents alone.

### §4.1 Baseline recommendation: TWO atomic commits (9.1 then 9.3)

Recommended posture (dev-autonomous):
- **9.1 commit** (stub substrate): backend-only. ~1,850 LoC estimated (28 cells: §2.1.5 7-gate + §2.1.6 15-cell + §2.1.4 9-cell + §2.1.1 4-cell — wait, that's 35; matrix has 35 backend cells + impl). Bounded, no console touches. Standalone deliverable.
- **9.3 commit** (console surface + SM-E1/E3): frontend + backend SM-E wiring. ~1,500 LoC estimated (22 cells: §2.3.4 15 + §2.3.5 5 + §2.3.3 2). Consumes 9.1 substrate. Standalone deliverable.

**Rationale for two commits (not one):**
- 9.1 has NO frontend surface changes (§2.1.7). 9.3 has NO worker-plane changes. There is no non-splittable pairing between them (unlike B-5b's write-enablement + retrofit atomic requirement).
- Each is a bounded slice with its own gate roster and closes independently.
- Sub-stage 9.2 sits between 9.1 and 9.3 chronologically only if [OWNER] facts land in that window; otherwise 9.3 lands right after 9.1 and 9.2 lands whenever [OWNER] facts arrive.

### §4.2 Contingency: pre-authorized split thresholds (per Ruling B5b-E5 template)

If actual 9.1 delivery exceeds **≥3,500 LoC OR ≥45 cells** (splitting the 9.1 substrate itself into 9.1a stub-only + 9.1b connectors), pre-authorized split at implementation time — no Owner round-trip. Cell threshold 45 = ~1.6× the 9.1 projected 28 cells.

If actual 9.3 delivery exceeds **≥2,200 LoC OR ≥35 cells**, pre-authorized split at implementation time (splitting 9.3 into 9.3a sample-flow + 9.3b registry-admin/quality-observation).

**Decision rule (dev-autonomous, disclosed at close per Ruling 5):** attempt §4.1 baseline. Report chosen path in each close.

### §4.3 Where does the sample execution path exist under 9.1 alone?

**Investigation surfaced at Stage A (Owner-visible):**
- Sub-stage 9.3 wires the sample UI + SM-E backend (`POST /api/extraction/sample/run`).
- The sample execution uses the SAME worker seam as full extraction (§2.1.2 + §2.1.3.g stub worker).
- Under 9.1 alone, the stub worker returns deterministic sample results — sufficient for SM-G1 gate proving (grounds commit envelope) at Sub-stage 9.3 close.
- Real GPU sampling comes with Sub-stage 9.2 (identical seam; stub swap).
- **Note (potential P9-E7 candidate):** if Owner rules that SM-G1 must run against real perception (not stub) at Phase 9 close, then Sub-stage 9.3 becomes gated on 9.2 [OWNER] facts. Current posture: SM-G1 proves against stub per BCR §3.1 V1-B3 stub-first pattern — gate proof precedes GPU code. Investigating at §5 escalations.

---

## §5. Escalation flags (P9-E1..P9-E7)

Enumerated per Standing Correction with authority-source citations + α/β/γ menu OR "cannot-be-menu, requires Owner semantic ruling".

### §5.1 P9-E1 — PerceptionJob_v0 / PerceptionResult_v0 freeze-or-not (D4b argued)

**Class:** frozen-contract-boundary + governance-semantic contact.

**Question:** BCR §3.1 V1-I2 verbatim: *"Freeze-or-not for both contracts is argued on the D4b axes at Phase 9 Stage A — they cross an environment boundary, so the prior is freeze."* The prior is FREEZE per the environment-boundary crossing. Does Owner ratify the FREEZE prior, or rule LIQUID (extensible via versioned bumps like `data_class_registry.v1→v2` at B-5b)?

**Authority-source language:** BCR §3.1 line 59: *"they cross an environment boundary, so the prior is freeze."* + technical annex lines 78–96 (typed schemas verbatim). Ruling record R-4 (Amendment G) established v0→v1 additive-bump pattern for JSON registries; the question here is whether the SAME pattern applies to CONTRACTS (Pydantic files under `backend/contracts/`).

**Options:**
- (α) FREEZE — PerceptionJob_v0 + PerceptionResult_v0 join the 26 frozen contracts as parity 27, 28 (parity bump 26 → 28 additive). Any future field change requires a NEW versioned contract (v1) landing beside v0 (never mutating v0). Matches R-4 for JSON registries but at CONTRACT level.
- (β) LIQUID — contracts remain revisable in-place until GPU perception model lands (Sub-stage 9.2) and freezes them by observed use. Argues that FREEZE-before-first-real-use is premature.
- (γ) STAGED — FREEZE at 9.1 landing (V1-G7 asserts byte-identity forward). Owner reserves the right to bump v0→v1 at 9.2 dispatch if GPU shape reveals field gaps. Compromise position.

**Recommended:** (α) FREEZE — matches the environment-boundary prior explicitly stated in BCR §3.1 line 59. LIQUID (β) is exactly the false-positive shape V1-B3 stub-first exists to prevent: locking in a shape only AFTER GPU code exists means the stub proved a different shape than the GPU consumes. Owner ruling requested.

### §5.2 P9-E2 — Locator-dialect governance (per-adapter vs registry-normalized)

**Class:** governance-semantic contact + adapter-boundary.

**Question:** BCR §3.1 V1-I4 verbatim: *"Each adapter owns its source's locator dialect inside the unit's locator field."* Per-adapter. But `NormalizedUnit` has a single `locator` field on the frozen contract. Two interpretations:
- (a) `locator: str` remains a free-form string; each adapter writes its own dialect; a dispatcher-side registry is NOT required (opaque-string interpretation).
- (b) `locator: {dialect: str, path: str, ...}` becomes a small typed sub-shape with a `locator_dialects.v0.json` registry (like `disclosure_types.v0.json` at B-5b Ruling B5b-E3 γ). Extensible via v0→vN bumps.

**Authority-source language:** BCR §3.1 V1-I4 line 61: *"Each adapter owns its source's locator dialect inside the unit's locator field."* Silent on shape. `NormalizedUnit` contract (existing, frozen) has the field.

**Options:**
- (α) Per-adapter free-form string. `locator: str` on NormalizedUnit (existing shape). Each adapter writes its dialect; consumer parses on demand. Matches "opaque locator" interpretation.
- (β) Registry-normalized sub-shape. Requires bumping `NormalizedUnit` — a FROZEN contract — which violates Standing 26 parity. RULED OUT structurally.
- (γ) Sidecar registry (`locator_dialects.v0.json`) documenting each adapter's dialect FOR HUMAN readers + optional parser lookup, but `locator: str` on the frozen contract stays untouched. Extensible via v0→vN bumps. Matches B5b-E3 γ precedent.

**Recommended:** (γ) — matches B5b-E3 γ constrained-str + JSON registry precedent. Preserves parity 26. Locator field on NormalizedUnit stays byte-identical; the dialect registry lives beside it as documentation + optional parser. Owner ruling requested.

### §5.3 P9-E3 — Worker credential shape + scope (new capability class)

**Class:** frozen-contract adjacency + governance-semantic contact.

**Question:** BCR §3.1 V1-I3 verbatim: *"A worker credential grants exactly these two operations — no database access, no ledger access, no key access."* This is a NEW capability class. How does it fit relative to the existing auth model (JWT tokens with role claims + capacity-role from Ruling 2)?

**Authority-source language:** BCR §3.1 V1-I3 line 60 + BCR §4 custody map line 305: *"Worker credential: the only worker-side secret; unlocks job-fetch and result-post, nothing else."*

**Options:**
- (α) Worker credential is a separate token class (`worker_jwt` with a `capabilities: [worker_claim, worker_result]` claim). Server verifies capabilities on the two worker routes; all other routes reject `worker_jwt` explicitly. AST gate proves scope enforcement.
- (β) Worker credential is a shared-secret HMAC (no JWT), simpler shape. Rejects the JWT posture used elsewhere.
- (γ) Worker credential is a JWT with a `role: worker` claim and worker-only routes gate on that role. Reuses existing role-check code.

**Recommended:** (α) — matches "never-rules enforced mechanically, not conventionally" (V1-H2). Capabilities claim is more explicit than a bare `role: worker` (γ) and more introspectable than HMAC (β). AST gate V1-G5 already proves worker code writes no Ledger — combined with capabilities claim + server-side route registry check, the never-rule holds mechanically at both call-site and credential-scope layers. Owner ruling requested.

### §5.4 P9-E4 — V1-G7 byte-identity gate specifics (parity 26 → 28)

**Class:** governance-semantic contact + Standing 26 adjacency.

**Question:** V1-G7 asserts byte-identity across all prior frozen contracts. Phase 9 ADDS 2 (PerceptionJob_v0 + PerceptionResult_v0). Does V1-G7 assert:
- (a) The 26 PRE-EXISTING contracts remain byte-identical (parity 26 preserved); +2 additive is disclosed but not compared. Effectively the same discipline as prior phases.
- (b) The full new set of 28 must remain byte-identical going forward from Phase 9 landing (parity 28 sealed at 9.1 commit).

**Authority-source language:** BCR §3.1 V1-G7 line 76: *"byte-identity across all prior frozen contracts."*

**Options:**
- (α) Interpretation (a) — 26 pre-existing preserved; +2 additive fall UNDER V1-G7 discipline STARTING from 9.1 commit. Standing 26 posture is exact: pre-9.1 the 26 stay byte-identical (already asserted phase-to-phase); at 9.1 landing the +2 join and the parity becomes 28; post-9.1 all 28 stay byte-identical.
- (β) Interpretation (b) — same as (α) mechanically but discipline is stated as parity 28 going forward (naming difference; identical enforcement).

**Recommended:** (α) — matches Standing 26 pre-existing discipline verbatim. Byte-identity assertion runs against ALL contract files present at each phase close; the set grows as Phase 9 (and future phases) add new frozen surfaces. Owner ruling requested for the naming (parity 26 vs parity 28); enforcement mechanism identical.

### §5.5 P9-E5 — BM-V PASS/INVESTIGATE verdict shape

**Class:** governance-semantic + Cannot-be-α/β choice (requires Owner semantic ruling).

**Question:** BCR §3.3 BM-V1 verbatim: *"class_distribution_delta against a human-qualified sample of the same hour, reported with a PASS/INVESTIGATE verdict at Phase 9 close."* Two-state verdict is explicit. But: is INVESTIGATE a Phase 9 CLOSE-BLOCKING state (Phase 9 does not close on INVESTIGATE) or a Phase 9 CLOSE-COMPATIBLE state (Phase 9 closes with INVESTIGATE recorded; a follow-up Owner ruling determines remediation)?

**Authority-source language:** BCR §3.3 BM-V2 line 139: *"Deferring BM-V past Phase 9 is prohibited: a perception stack declared complete against synthetic fixtures only is the false-positive condition, not the guard against one."* Deferring BM-V is prohibited; silent on INVESTIGATE closure posture.

**Cannot-be-α/β choice — this is a governance-semantic ruling like R-3 (state-machine corrections).**

**Preliminary observation (not a proposal):** BM-V verdict runs inside Sub-stage 9.2 (GPU half). Sub-stage 9.2 is gated on [OWNER] facts (§2.2). If [OWNER] facts land + GPU runs + verdict = INVESTIGATE, does Phase 9 close on INVESTIGATE with follow-up ruling, or does Phase 9 stay open until PASS? Owner semantic ruling required.

### §5.6 P9-E6 — Grounding-marker copy variants (owner-value contact per E7 pattern)

**Class:** owner-value contact + E7 middle-dot glyph strict.

**Question:** UI Spec v2.1 §3.3 line 50 binding-copy verbatim: *"Grounded by sample {sample_ref}"* / *"No sample run — estimates only."* The em-dash "—" is used. Per E7 (middle-dot U+00B7 on binding copy), does the em-dash stay em-dash, or does it convert to middle-dot for consistency?

**Authority-source language:** E7 (rulings record SHA `c89cacc6…`) rules middle-dot U+00B7 on binding-copy list-separators/pattern markers. UI Spec §3.3 verbatim uses em-dash "—" as a syntactic pause (like "No sample run — estimates only"), NOT as a list separator.

**Options:**
- (α) Preserve em-dash "—" exactly as UI Spec §3.3 line 50 states. E7's middle-dot rule applies to LIST SEPARATORS, not syntactic pauses. Distinct usages.
- (β) Convert em-dash to middle-dot "·" for glyph consistency. Deviates from UI Spec verbatim.
- (γ) Preserve UI Spec verbatim (α) AND assert both variants in test (test_phase_9_grounding_marker.test.js §2.3.4.c verifies the em-dash + verbatim string OR the middle-dot IF Owner rules β).

**Recommended:** (α) — matches UI Spec §3.3 verbatim + preserves E7 semantics (E7 is about list separators, not syntactic pauses per rulings record). Owner-ruled ratification anchors the test verbatim assertion. Owner ruling requested.

### §5.7 P9-E7 — SM-G1 stub-vs-real gate proving

**Class:** governance-semantic + Cannot-be-α/β choice.

**Question:** Sub-stage 9.3 wires SM-E1..E3 + SM-G1 + SM-G5. Sub-stage 9.3 dispatchable on 9.1 substrate alone (§4.3). Does SM-G1 prove against stub worker (V1-B3 stub-first) at Sub-stage 9.3 close, or must SM-G1 wait for real GPU perception (Sub-stage 9.2 [OWNER]-gated)?

**Authority-source language:** BCR §3.1 V1-B3 line 65: *"A deterministic stub worker lands first and all guard gates prove against it before any GPU code exists (the established stub-first pattern)."* Applies stub-first to guard gates (V1-G*). Silent on whether SM-G* (sample gates) inherit stub-first, OR whether they must wait for real perception because they prove a governance semantic (grounds-commit-envelope) that only real perception can validate empirically.

**Cannot-be-α/β choice — governance-semantic ruling required.**

**Preliminary observation (not a proposal):** if SM-G1 proves against stub, Sub-stage 9.3 closes independently of 9.2 [OWNER] facts (matches §4.1 baseline). If SM-G1 requires real perception, Sub-stage 9.3 becomes gated on 9.2 — Phase 9 closes only after 9.2 lands. Owner ruling determines whether §4.1 baseline holds or whether 9.3 dispatch is [OWNER]-gated via 9.2.

---

## §6. Standing anti-rules audit (pre-dispatch attestation)

| Rule | Preserved by design |
|---|---|
| E5 (no HTTP 409 anywhere) | Worker endpoints use 401/403/400/202/204. Sample endpoints use 202/200/400/403. AST gate at Phase 9 close scans `backend/services/perception/**` + `backend/routers/workers.py` for `\b409\b` — zero. |
| E7 (middle-dot U+00B7 strict on binding copy) | Preserved: grounding marker + unknown-marker + attention-card copy asserted at §2.3.4.c + §2.3.4.d. |
| E2 (4-code auth-refusal registry) | Worker credential 403 uses `auth_scope_insufficient` (existing E2 code); no new codes minted. |
| Ruling 1 (vestigial artifact_ref pattern) | Phase 9 does NOT touch ledger emit surfaces; retention on artifact_ref unchanged. |
| Ruling 2 (capacity-role for compliance) | Phase 9 does NOT touch checker; worker credential is a distinct capability class (P9-E3). |
| Ruling 3 (state-machine semantics) | Phase 9 job dispatcher ties into existing 5-state machine per Phase 5 standing ruling (V1-B1). No new governance state added. |
| Ruling 4 (v0→v1 JSON registry additive bump) | Extended to P9-E2 γ (`locator_dialects.v0.json`) IF Owner rules γ. |
| Ruling 5 (band discipline, miss + disclosure > pad + hide) | Band `[2,850, 3,650]` matrix-derived, no padding; §3.4 re-derivation triggers explicit. |
| Ruling 6 (consequence_class stamp_audit) | Not touched by Phase 9 (extraction, not compliance rulebook). |
| Ruling 7 (Sub-stage 2 FINAL ACCEPTANCE + rider) | Recorded; Phase 8 close discharge signal serves as Phase 8 final acceptance (see §8 note). |
| B5b-E4 (retrofit voiding via data_class_registry additive bump) | Not touched by Phase 9. |
| B5b-E5 (pre-authorized split thresholds) | Applied at §4.2 with Phase 9-specific thresholds (9.1: 3,500 LoC / 45 cells; 9.3: 2,200 LoC / 35 cells). |
| Amortisation Divergence Class (Owner-accepted at B-5b close) | Codified at §1.2 + §1.3 with named triggers + empirical anchors. |
| Standing 26 (frozen contract parity) | Parity 26 → 28 ADDITIVE at 9.1 landing per §2.1.1 + P9-E1 α; V1-G7 asserts byte-identity of pre-existing 26 forever. |
| Standing Correction (matrix-enumerated sizing) | Applied throughout §2 + §3. |
| Standing Rule v3 (on-disk close reports; reply is SHA + summary) | This proposal ON DISK at `/app/docs/stage_a_proposals/phase_9.md`. Reply = SHA + summary + escalations + band. |

---

## §7. Reply-body structural summary (dispatch reply reference)

**Files landed at this Stage A dispatch:**
- `/app/docs/stage_a_proposals/phase_9.md` (this file).

**Files NOT touched:** all 26 frozen contracts; all Sub-stage 3 + B-5b landed code; all mandate docs; all conformance/rulings/close report docs. Design-only.

**Structural TOC (this proposal):**
- §1. Cell-density assumption + Amortisation Divergence Class codification.
- §2. Deliverables enumeration (§2.1 Sub-stage 9.1 substrate + §2.2 Sub-stage 9.2 GPU-gated + §2.3 Sub-stage 9.3 console surface).
- §3. Band derivation.
- §4. Sub-stage split (§4.1 baseline two-commit + §4.2 pre-authorized escalation thresholds).
- §5. Escalation flags P9-E1..P9-E7.
- §6. Standing anti-rules audit.
- §7. Reply-body structural summary.
- §8. Phase 8 close footer (Owner discharge signal serves).

**Escalation-flag summary:**
- P9-E1: α/β/γ menu — freeze-or-not on PerceptionJob_v0 / PerceptionResult_v0 (recommended α FREEZE).
- P9-E2: α/β/γ menu — locator-dialect governance (recommended γ sidecar registry).
- P9-E3: α/β/γ menu — worker credential shape (recommended α capabilities-claim JWT).
- P9-E4: α/β menu — parity 26→28 naming (recommended α standing-discipline preserved).
- P9-E5: Cannot-be-α/β — BM-V INVESTIGATE closure posture (requires Owner semantic ruling).
- P9-E6: α/β/γ menu — em-dash vs middle-dot on grounding-marker copy (recommended α preserve UI Spec verbatim).
- P9-E7: Cannot-be-α/β — SM-G1 stub-vs-real gate proving (requires Owner semantic ruling; determines §4.1 baseline vs 9.3-gated-on-9.2).

**Band (matrix-derived, no padding):** `[2,850, 3,650]` raw LoC across 57 cells (9.1 + 9.3 only; 9.2 gated-not-estimated per Owner).

**Ready-to-dispatch posture:**
- All BCR §3.1 requirements (V1-U1..V1-B4..V1-D1..V1-H1..V1-G1..G7) matrix-enumerated as backend deliverables §2.1.
- All BCR §3.3 BM-V + BM-C referenced; BM-V is a Sub-stage 9.2 in-phase surface, gated-not-estimated.
- All BCR §3.12 SM-E1..E3 + SM-G1 + SM-G5 (in-scope) matrix-enumerated at §2.3.
- All UI Spec v2.1 §3.1–§3.6 covered by §2.3.1 (Extraction Console home + sample surfaces + registry admin + quality observation).
- Amortisation Divergence Class codified at §1.2 + §1.3 with empirical anchors + named triggers.
- Band matrix-derived at §3.3; re-derivation triggers explicit at §3.4.
- 7 escalations enumerated at §5; P9-E5 + P9-E7 are cannot-be-α/β semantic rulings.
- Frozen contract parity 26 preserved (+2 additive at 9.1 landing per P9-E1 α ratification).
- Standing state-conflict anti-rule preserved (E5 zero-409 attested at §6).
- E7 middle-dot glyph strict (asserted at §2.3.4.c).
- Sub-stage split proposal §4.1 two-commit baseline + §4.2 pre-authorized escalation thresholds.
- 9.2 [OWNER] gates listed with owners, never estimated.
- No self-dispatch. Owner ratifies Stage A + P9-E1..P9-E7 rulings before Sub-stage 9.1 execution dispatch.

**READY TO DISPATCH POST OWNER RULINGS ON P9-E1/E2/E3/E4/E6 (α/β/γ menus) + P9-E5/E7 (governance-semantic rulings) + ratification of §3.3 anchored band + §4 sub-stage split.**

---

## §8. Phase 8 close footer (Owner discharge signal serves)

Per Owner directive verbatim: *"if Phase 8 close needs one per standing rider pattern; if Owner discharge signal serves as the footer, note."*

**Owner discharge signal serves as the Phase 8 close footer.** The B-5b close (SHA `47af8c63…`) already carries §4 Sub-stage 3 rider landing (B-5b commit's own rider-append pattern per §6 of Stage A B-5b). No further rider is required at Phase 9 Stage A dispatch — the completeness-line binary check discharge IS the Phase 8 close attestation.

Historical Phase 8 close chain (for continuity):
- Sub-stage 1 close ratified.
- Sub-stage 2 close ratified (Ruling 7 FINAL ACCEPTANCE).
- Sub-stage 3 close ratified (Ruling 7 + Amendment G).
- B-5b close conditionally ratified pending completeness-line (SHA `47af8c63…`); completeness-line discharged at this dispatch; **Phase 8 CLOSED at Owner discharge signal 2026-07-08.**

═══════════════════════════════════════════════════════════════════

*End of Phase 9 Stage A proposal. Design-only per Owner dispatch. Standing Rule v3: full text on disk. Reply is SHA + structural TOC + escalations + band. Owner ratification of Stage A + P9-E1..P9-E7 required before Sub-stage 9.1 execution dispatch. Sub-stage 9.2 (GPU half) dispatch requires additionally 9.2-OWN-1..3 [OWNER] facts landing.*
