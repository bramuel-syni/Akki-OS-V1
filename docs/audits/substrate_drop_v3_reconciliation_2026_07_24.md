# Substrate-Drop v3 · Reconciliation Audit · 2026-07-24

**Class:** Reconciliation audit per Owner Configuration Dispatch 2026-07-24 §4.STEP-3 (verbatim: *"Reconciliation audit against the shipped surface with per-artifact CODE_IMPACT enumeration (NET-NEW / PARTIAL-EXTEND / CONFORMS per feature, §-anchored) and CONFLICT rows wherever the drop disagrees with UI Spec v2.2 / Product Spec v3 / SJM v1 — each CONFLICT surfaced for per-conflict Owner ruling. No auto-supersession in either direction."*).
**Authority artifacts:**
- `docs/rulings/owner_configuration_2026-07-24.md` · SHA `ec95a0acec13d81b2fd5f1b1da04c83d2991f3876c795c8266a96eaef1230f52`
- `docs/rulings/owner_step2_surfaces_ruling_2026-07-24.md` · SHA `2e11c7ea864a940d64b1a438b7bf1f0f5fd6e77b12aeb816d9bfad640779d178`

**Prior CODE_IMPACT preview table carries no evidentiary weight** (per §4.STEP-3). This audit is the authoritative record.

**Estimation-discipline attest:** no duration/credit figure emitted (per Owner §3 · module-build bands generated only from STEP 3 reconciliation's enumerated CODE_IMPACT + CONFLICT rows, after §5 closes; those bands land at STEP 5, not here).

**Canonical anchors consulted (D-11 canon-before-attest · live-verified):**
- `docs/mandates/module_specs/*.md` (9 landed 2026-07-24 · SHAs in MANIFEST.md)
- `docs/mandates/RMS_UI_Specification_v2_2.md` · SHA `d681c6cd399dd569…`
- `docs/mandates/RMS_Product_Engineering_Spec_v3.md` · PES v3
- `docs/mandates/surface_journey_map_v1.md` · SJM v1
- `backend/routers/*.py` (28 files · Parity 31 unchanged)
- `backend/services/*/` (31 sub-dirs)
- `backend/contracts/*.py` (31 files · Parity 31 held)
- `frontend/src/App.js` (route map)
- `frontend/src/pages/**` (page + component surfaces)

---

## §A · Per-artifact CODE_IMPACT enumeration

Rows classed **NET-NEW** (no shipped surface) · **PARTIAL-EXTEND** (surface exists · spec depth not carried) · **CONFORMS** (surface implements spec feature).

### §A.1 · `01_connect_module.md` — Connect Module

| Feature (§-anchored) | Class | Shipped-surface anchor (or absence) |
|---|---|---|
| **DPO role** (accountable governance signer) | **NET-NEW** | Roles on-disk: Master Admin · Operator · engineer · buyer-cut · analyst. No DPO role in `services/auth/**` or `routers/auth.py`. No `data_protection_officer` role literal. |
| **Data Engineer role** | **PARTIAL-EXTEND** | `services/auth/engineer_invites.py` + `services/auth/engineer_key_grant_service.py` exist; role literal is `engineer`, not `data_engineer`. Journey 3 Add-Source flow is engineer-adjacent but not landed. |
| **Governance Sponsor + Co-Signer named contacts** | **NET-NEW** | No sponsor / co-signer contact record on-disk. Compliance flows lack Governance Sponsor / Co-Signer nomination. |
| **Journey 1 § Org Setup 5-step wizard** (Org Details · Contacts · Governance Rules · Data Sources · Review + DPO signoff) | **NET-NEW** | Onboarding wizard on-disk (`services/wizard/` + `routers/wizard_operator.py`) is the Operator shaping wizard (Phase 7); NOT the Connect Setup wizard. Setup wizard entirely un-landed. |
| **6 Governance Rules · plain sentence · toggle/numeric** | **NET-NEW** | Rulebook write endpoint at `routers/compliance.py:POST /compliance/lawful_basis_registry` exists but the 6-rule Owner-authored plain-sentence set is not landed with toggle/numeric interaction. |
| **4-value usage-rights enum per data source** | **NET-NEW** | No usage-rights enum on-disk. `services/data_source/**` carries synthetic + source-standing shapes; no usage-rights taxonomy. |
| **DPO signoff · locks configuration** | **NET-NEW** | No DPO-signoff endpoint. Master-admin lock semantics exist at `routers/master_admin.py:POST /master_admin/tightening/suspend` but not DPO-signoff-locks-configuration semantics. |
| **Progress bar · 5 stages · post-signoff screen** (stat cards · source list · invite status · Add Source) | **NET-NEW** | No Connect landing page. `frontend/src/pages/engineer/EngineerRegisterAppPage.js` is dual-actor onboarding-related but a different flow. |
| **Notification Center + email to DPO on Data Engineer submission** | **NET-NEW · rides OD-8** | No Notification Center on-disk. Email fanout not landed anywhere in backend. |
| **Journey 2 § Manage Sources** (view · edit · deactivate) | **NET-NEW** | Data-source registry exists (`services/data_source/**`) but no CRUD surface for source management from Connect UI. |
| **Journey 3 § Add Source** (post-signoff single-source addition · Data Engineer submits · DPO approves) | **NET-NEW** | Not landed. Analogous flow could ride existing `engineer_invites` pattern but is not the same seat. |
| **Journey 4 § Verify Connection** (test connection · mapping resolution) | **NET-NEW** | No connection-test endpoint. Mtafiti census sees data but does not "test connection" as an interactive flow. |
| **Journey 5 § Update Governance Contacts** (change Sponsor / Co-Signer with escalation) | **NET-NEW** | 2-party Co-Signer + 3-party Sponsor succession flows entirely un-landed. |
| **Auto-populate Team Manage Users on Setup completion** | **NET-NEW · cross-module handoff to Team** | `services/auth/user_store.py` supports user creation but no Setup→Team auto-population wiring. |

**Connect Module CODE_IMPACT summary:** NET-NEW **13** · PARTIAL-EXTEND **1** · CONFORMS **0**.

### §A.2 · `02_registry_module.md` — Registry Module

| Feature (§-anchored) | Class | Shipped-surface anchor (or absence) |
|---|---|---|
| **"What You Hold" shared landing** (any authenticated user · same view all roles) | **PARTIAL-EXTEND** | Extraction Console at `frontend/src/pages/extraction/ExtractionConsoleHomePage.jsx` shows census-derived state (measured/unknown badges) but not the Owner-spec "What You Hold" landing depth (8 stat cards · composition breakdown · opportunity preview · item table). |
| **First-Census + auto-trigger on first source Connected** | **NET-NEW · rides OD-10** | Mtafiti census exists as backend service (`services/mtafiti/**` + `routers/mtafiti.py`); no auto-trigger on Connect completion. No scheduler primitive. |
| **Manual Run Census button (Data Engineer / DPO)** | **PARTIAL-EXTEND** | `frontend/src/pages/extraction/RegistryAdminView.jsx` renders trigger-census buttons per row (per Playwright cell `phase_9_registry_admin_smoke.spec.ts:11`); role-gating to Data Engineer / DPO not enforced (current role-gating is engineer-only). |
| **Census State 2** (start time · ETA · progress % · current stage) | **PARTIAL-EXTEND** | `RegistryAdminView.jsx` renders `mining-stage` inline (per Playwright cell `phase_9_quality_observation_smoke.spec.ts:4`) but no full State-2 dashboard with ETA. |
| **State 3 What You Hold · 8 stat cards** (total volume · sources · types · languages · verified share · PII share · licensed for external use · not yet measured) | **NET-NEW** | Not landed on-disk. Extraction Console shows a subset (registry status) but not the 8-card grid. |
| **Composition breakdown by language/era/type/quality with real counts** | **NET-NEW** | Mtafiti backend carries measured counts (`MtafitiRegistryRecord`); frontend renders unknown-marker / measured-marker but not the composition breakdown. |
| **Gaps explicitly marked** (Owner-verbatim: *"marked rather than hidden"*) | **PARTIAL-EXTEND** | `SampleGroundingContext.jsx` renders grounding markers; explicit gap marking as a first-class UI element is not landed. |
| **Debounce logic on multiple sources added quickly** | **NET-NEW · rides OD-10** | No scheduler primitive; no debounce. |
| **Source Profile drill-in per source** | **NET-NEW** | No per-source detail page on-disk. `services/mtafiti/**` has source-standing shape but not a rendered per-source surface. |
| **"How this was measured" methodology popover** (per stat card) | **NET-NEW** | Not landed. |
| **First census date · Last run by · logged** | **PARTIAL-EXTEND** | `MtafitiRegistryRecord` carries `FreshnessStamp`; render not landed. |
| **Opportunity preview inline** | **PARTIAL-EXTEND** | Opportunity Briefs page exists at `frontend/src/pages/opportunity_briefs/OpportunityBriefsPage.jsx` (separate route `/opportunity-briefs`); inline preview inside Registry landing is not landed. |

**Registry Module CODE_IMPACT summary:** NET-NEW **7** · PARTIAL-EXTEND **5** · CONFORMS **0**.

### §A.3 · `03_extract_module.md` — Extract Module

| Feature (§-anchored) | Class | Shipped-surface anchor (or absence) |
|---|---|---|
| **Analyst role** | **CONFORMS** | Analyst role literal exists as one of the on-disk role vocabulary; UI Spec v2.2 §2.1 references. |
| **Run/Commission Approver role** | **NET-NEW** | Role name "provisional" per module spec; no role literal on-disk. Compliance / master-admin flows carry authority patterns but not a Run Approver seat. |
| **Model Acceptor role** | **NET-NEW** | Not landed. |
| **Journey 1 § Shape an Objective wizard** (3 stages: Objective Details · Plan Preview · Sample Results) | **PARTIAL-EXTEND** | Commission Wizard at `frontend/src/pages/operator/CommissionWizardPage.js` + `routers/wizard_operator.py` implements a shaping-wizard-family surface; not the exact Extract 3-stage split (module spec differs from Operator shaping wizard structurally). |
| **Entry from Registry opportunity (prefilled) OR blank** | **PARTIAL-EXTEND** | Opportunity Briefs page has "shape-as-objective" click that stashes reach prefill (per Playwright cell `opportunity_brief_smoke.spec.ts:43`); the prefill routes to `/operator/commission` (existing), not to an Extract-Module-dedicated Shape-an-Objective page. |
| **Stage-2 Plan Preview** (volume range · stock % · coverage · gaps) | **PARTIAL-EXTEND** | Feasibility result contract at `backend/contracts/feasibility_result.py` (`FeasibilityResult_v0` · `ClassDistribution` · `Freshness`) carries the shape; render at `frontend/src/pages/extraction/SampleResultCard.jsx` renders a variant; full 4-field Plan Preview not landed. |
| **Extract-a-Sample flow** (Stage-3 Sample Results · budget ceiling) | **PARTIAL-EXTEND** | `routers/extraction_sample.py:POST /extraction/sample/run` + `GET /extraction/sample/{sample_ref}` exists; `SampleResultCard.jsx` renders result; budget-ceiling UI not landed. |
| **My Objectives listing · Status: Plan generated / Sampled / Commissioned / Running / Complete / Rejected** | **PARTIAL-EXTEND** | Objectives at `routers/objectives.py` (POST/GET/cancel) + Northena ledger; explicit status-taxonomy render not landed as spec'd. |
| **Journey 2 § Commission** (quote + acceptance · Run Approver approval routing) | **PARTIAL-EXTEND** | `contracts/quote_envelope.py` (`QuoteEnvelope_v0` + `QuoteInstrumentationSeed_v0`) carries quote shape; Run Approver routing NET-NEW. |
| **Journey 3 § Run + Model Acceptance** | **PARTIAL-EXTEND** | Async delivery contract at `contracts/async_delivery_accepted.py` + `_v1.py`; Model Acceptance ceremony NET-NEW. |
| **Extracted Intel — completed artifacts list** (datasets · skill files · models) | **PARTIAL-EXTEND** | `services/transform_forms/**` + `routers/transform_forms.py` (produce knowledge_artifact · provision callable_skill · query skill) carries the artifact-emission shape; end-user-facing "Extracted Intel" browse surface not landed. |
| **Rejected model resubmission (new linked version)** | **NET-NEW** | Not landed. |
| **Quarantined batches visible inline** (cross-module handoff to Govern Quarantine) | **NET-NEW** | Per-batch quarantine ledger row is EAB-2 scope (`docs/stage_a_proposals/eab_2_stage_a.md` §4.B); not landed. |
| **Ask Akki drawer available inline** | **NET-NEW · Shared Components** | See §A.7. |

**Extract Module CODE_IMPACT summary:** NET-NEW **5** · PARTIAL-EXTEND **8** · CONFORMS **1**.

### §A.4 · `04_govern_module.md` — Govern Module

| Feature (§-anchored) | Class | Shipped-surface anchor (or absence) |
|---|---|---|
| **DPO's Estate landing page** (8 stat cards + Estate-by-governance-class + Rules record) | **PARTIAL-EXTEND** | Compliance Home at `frontend/src/pages/compliance/ComplianceHomePage.js` renders a compliance-surface variant; not the Owner-spec DPO Estate depth. |
| **8 Estate stat cards** (rules in force · checks enforcing · enforcements 30d · violations · access events 30d · exports blocked · under retention hold · destruction attestations) | **PARTIAL-EXTEND** | `routers/compliance.py:GET /compliance/refusals_coverage` + `GET /compliance/refusals` render backend surface; frontend rendering of 8 cards not landed as spec'd. |
| **Govern side-navigation** (DPO Estate · Change-a-Rule · Destroy-Data · Release Review · Quarantine · Governance Setup) | **NET-NEW** | No Govern-specific side-nav exists. |
| **Change-a-Rule ceremony** (DPO proposes · Co-Signer counter-signs · 72h waiting period · Verify-the-Rules on completion) | **NET-NEW** | `frontend/src/pages/master_admin/ChangeARulePage.js` exists (Master Admin variant); Owner-spec DPO+Co-Signer 72h ceremony NOT landed. |
| **Destroy-Data ceremony** (DPO requests · Co-Signer counter-signs · 24h timer · destruction attestation) | **PARTIAL-EXTEND** | `routers/compliance.py:POST /compliance/authorized_deletion` exists; 24h timer + destruction-attestation ceremony NOT landed. |
| **Release Review** (external memos · deliverables) | **NET-NEW** | Not landed. |
| **Quarantine submodule** (cross-module handoff from Extract) | **NET-NEW · rides EAB-2** | Not landed; part of EAB-2 A4 execution scope. |
| **Governance Setup succession** (2-party Co-Signer / 3-party Sponsor incl. CEO) | **NET-NEW** | Not landed; entirely un-implemented. |
| **Verify-the-Rules flow** (post-Change-a-Rule verification) | **NET-NEW** | Not landed. |
| **Rules record table · Rules in force list** | **PARTIAL-EXTEND** | `routers/compliance.py:POST /compliance/lawful_basis_registry` accepts writes; render not landed. |
| **See-the-Record detail views per stat card** | **NET-NEW** | Not landed. |
| **Access events 30d display · Exports blocked count** | **PARTIAL-EXTEND** | Northena ledger carries the substrate; count/display not landed. |
| **Retention hold posture rendering** | **PARTIAL-EXTEND** | `ComplianceRetentionRightsPage.js` exists (retention rights surface); hold-posture stat card NOT landed. |
| **Destruction attestation surface** | **NET-NEW** | Not landed. |
| **Estate by governance class** (grouped by governance-class enforcement) | **NET-NEW** | Not landed. |
| **Change-a-Rule notification email to Co-Signer** | **NET-NEW · rides OD-8** | See OD-8 rides-list. |
| **Destroy-Data notification email to Co-Signer + 24h timer** | **NET-NEW · rides OD-8** | See OD-8 rides-list. |
| **Sponsor / CEO 3-party succession notification chain** | **NET-NEW · rides OD-8** | See OD-8 rides-list. |

**Govern Module CODE_IMPACT summary:** NET-NEW **13** · PARTIAL-EXTEND **5** · CONFORMS **0**.

### §A.5 · `05_prove_module.md` — Prove Module

| Feature (§-anchored) | Class | Shipped-surface anchor (or absence) |
|---|---|---|
| **Ask a Question landing (any authenticated user)** | **CONFORMS** | `frontend/src/pages/AskConsolePage.js` at route `/` (default landing). Ask surface exists. |
| **Chat history sidebar (past conversations)** | **NET-NEW** | Not landed; AskConsolePage is stateless per invocation. |
| **Answer Card render** (finding · measured/estimated tags · evidence strip with source links) | **PARTIAL-EXTEND** | `TraceReceiptPage.js` renders three-lens SolvaTrace (per Playwright cell `trace_smoke.spec.ts:55`); Answer Card inside Ask is not the full three-tag structure. |
| **Three refusal shapes distinct** (not-extracted-yet + gap-queue + estimated effort · evidence-can't-support · something-broke) | **NET-NEW · HAZARD-STOP surface at STEP 4 EAB-2 refresh** | `contracts/service_1_refusal.py::Service1Refusal_v0` has three reasons (`no_defensibility_floor` · `no_lawful_basis` · `composition_below_floor`) — ALL are evidential-refusal-family. **NONE match the Prove-spec 3 shapes.** See §B.CONFLICT.C-1 below. |
| **Queue-this-gap button** (Not-extracted-yet shape → routes to Extract Shape-an-Objective prefilled) | **NET-NEW** | Not landed. |
| **Estimated effort surfaced on Not-extracted-yet shape** | **NET-NEW** | Not landed. |
| **Break-it-down action** | **NET-NEW** | Not landed. |
| **Draft-a-memo action → Memos submodule** | **NET-NEW** | Not landed. |
| **Walk-the-Proof modal** (Levels 1/2/3 as tabs) | **PARTIAL-EXTEND** | `TraceReceiptPage.js` renders "three-lens" surface at `/trace/:traceId`; modal-based Level 1/2/3 inside Ask NOT landed. |
| **Memos submodule** (draft · save · release for review) | **NET-NEW** | Not landed. |
| **Public Receipts** (DPO-only generation · no-login verify · expiry · revoke · verification log) | **NET-NEW · rides OD-9 + PH-R3** | Not landed. |
| **Public Receipt verification page (no-login)** | **NET-NEW · rides OD-9 + PH-R3** | Not landed. |
| **Public Receipt revocation semantics under caching** | **NET-NEW · rides OD-9** | Not landed. |
| **External memo release** → Govern Release Review (cross-module handoff) | **NET-NEW** | Not landed. |
| **"Honesty strip"** (per module spec — quality/verification indicator on Answer Card) | **PARTIAL-EXTEND** | Compliance markers exist (`RefusalCard.js`, `ClassBadge.js`); dedicated honesty-strip inline in Ask NOT landed. |
| **Cross-module handoff · gap-queue → Extract prefill** | **NET-NEW** | Not landed. |
| **Answer Card evidence-strip source citations link to Registry Source Profile / Extract objective detail** | **PARTIAL-EXTEND** | `TrustReceiptLink.js` component exists; per-source linking NOT landed. |

**Prove Module CODE_IMPACT summary:** NET-NEW **13** · PARTIAL-EXTEND **3** · CONFORMS **1**.

### §A.6 · `06_team_module.md` — Team Module

| Feature (§-anchored) | Class | Shipped-surface anchor (or absence) |
|---|---|---|
| **Master Admin role** | **CONFORMS** | Master Admin role literal exists on-disk (`routers/master_admin.py` + `pages/master_admin/`). |
| **Manage Users landing table** | **NET-NEW** | No Team module page. Master Admin Home exists but not a Manage-Users listing. |
| **Invite User flow** (Name · Email · Role dropdown) | **PARTIAL-EXTEND** | `routers/engineer.py:POST /engineer/onboarding/invite` + `POST /engineer/onboarding/approve` implements a similar-shape flow for engineer role only; multi-role Invite NOT landed. |
| **Master Admin promotion DPO-approval routing** | **NET-NEW** | Not landed. |
| **DPO-approve / return-with-reason on MA promotion request** | **NET-NEW** | Not landed. |
| **Detail view per user** (role · status · date added · deactivate / reassign) | **NET-NEW** | Not landed. |
| **Invitee login flow → status Active** | **PARTIAL-EXTEND** | `routers/auth.py` login flow exists; wiring to Team "Active" status NOT landed. |
| **Governance Co-Signer / Sponsor succession pointer to Govern** | **NET-NEW** | Not landed; part of Govern Module (§A.4). |
| **Team invitation email** | **NET-NEW · rides OD-8** | See OD-8 rides-list. |
| **Master Admin promotion notification email to DPO** | **NET-NEW · rides OD-8** | See OD-8 rides-list. |

**Team Module CODE_IMPACT summary:** NET-NEW **7** · PARTIAL-EXTEND **2** · CONFORMS **1**.

### §A.7 · `07_shared_components.md` — Shared Components

| Feature (§-anchored) | Class | Shipped-surface anchor (or absence) |
|---|---|---|
| **Ask Akki Drawer** (global right-side drawer · header trigger from every module) | **NET-NEW** | No global drawer exists. `AskConsolePage.js` is a full-page route at `/`, not a slide-in drawer. |
| **Suggested questions per context** | **NET-NEW** | Not landed. |
| **Follow-up conversation (running conversation in drawer)** | **NET-NEW** | Not landed. |
| **Walk-the-Proof modal · same Level 1/2/3 as Prove** (single-implementation shared shell) | **NET-NEW** | `TraceReceiptPage.js` is a full-page route; modal variant + shared-shell single-implementation NOT landed. |
| **Answer Card + refusal-shape component family = single shared-shell implementation** (per Owner STEP 5 structural directive) | **NET-NEW** | Currently no shared shell; if built naively as separate implementations, would be a D-class finding per Owner ruling. |
| **Drawer closes → underlying page state preserved** | **NET-NEW** | Not landed. |

**Shared Components CODE_IMPACT summary:** NET-NEW **6** · PARTIAL-EXTEND **0** · CONFORMS **0**.

### §A.8 · `akki_product_system_document.md` — Product & System Document

**Not a code-carrier — descriptive canon per `tiered_ruling_model.md` §22.** Consistency-scan divergences flagged in prior Dispatch 1 reply of 2026-07-15 (5 sub-scans · engine mandates naming · ring-name naming · role-vocabulary drift · surface-vocabulary drift · spec-index gaps · quantitative-claim ambiguities); those remain open findings for Owner ruling. **Zero new CODE_IMPACT rows** from Product Doc content itself — its content is subordinated to engineering canon per §22.

**Product Doc CODE_IMPACT summary:** NET-NEW **0** · PARTIAL-EXTEND **0** · CONFORMS-BY-SUBORDINATION **N/A** (descriptive canon, not code-bearing).

### §A.9 · `08_user_stories.md` — User Stories

**Not a code-carrier — role-anchored story catalog subordinate to module specs.** Every story maps to a module-spec § anchor already enumerated in §A.1–§A.7 above; the story catalog is CODE_IMPACT-neutral (redundant to module-spec features already counted).

**User Stories story-to-feature mapping counts (module-anchored):**

- Connect stories → §A.1 features (14 rows)
- Registry stories → §A.2 features (12 rows)
- Extract stories → §A.3 features (14 rows)
- Govern stories → §A.4 features (18 rows)
- Team stories → §A.6 features (10 rows)
- Prove stories → §A.5 features (17 rows)

**Zero net-new CODE_IMPACT rows.**

---

## §B · CONFLICT rows (per-conflict Owner ruling required · no auto-supersession)

Every divergence from UI Spec v2.2 · PES v3 · SJM v1 surfaces as a discrete row.

### §B.C-1 · **HAZARD-STOP (a) surface for STEP 4 EAB-2 refresh** — Refusal shape taxonomy mismatch

**Conflict source (module spec § verbatim):** `05_prove_module.md § Journey 1 · Ask a Question · Refusal shapes`

> - **Not extracted yet** — shows gap + Queue this gap button
> - **Evidence can't support** — shows reason, no queue option
> - **Something broke** — plain error, distinct styling

**Conflict target (engineering canon):** `backend/contracts/service_1_refusal.py::Service1Refusal_v0` (SHA `4fe38c214dc59260…` · Parity slot 14). Reason enumeration:

```python
reason: Literal[
    "no_defensibility_floor",
    "no_lawful_basis",
    "composition_below_floor",
]
```

**Class:** data shape · refusal-envelope taxonomy · **wire contract**.

**Divergence:** the Prove-spec 3 shapes (not-extracted-yet · evidence-can't-support · something-broke) do NOT map 1:1 to the Service1Refusal@v0 reason enumeration. The v0 envelope's three reasons are all **evidential-refusal-family** (defensibility · lawful basis · composition floor); NONE of the three Prove-spec shapes corresponds. Specifically:

- **"Not-extracted-yet"** ↔ EAB-2 A3 `coverage_gap` class (pre-named for `Service1Refusal@v1` at `docs/stage_a_proposals/eab_2_stage_a.md` §5.1 · Parity 31→32 seal).
- **"Evidence can't support"** ↔ `composition_below_floor` (partial match) + `no_defensibility_floor` (partial match); Prove spec's phrasing may cover both.
- **"Something broke"** ↔ **NOT a refusal class** in engineering canon. Per `Service1Refusal@v1` §5.1 sub-option (a1) recommendation and R-A3.3 (fault-never-dressed rule), infrastructure faults surface as fault-envelopes (HTTP 503 with structured detail per `PROM-S1-config-defect-fail-loud`), NEVER as any refusal class. The Prove-spec "something broke" would need to be rendered as a distinct-styling error, NOT enveloped as a refusal.

**Ruling surface for STEP 4 EAB-2 Stage-A refresh:**

- **(a)** `Service1Refusal@v1` envelope superset lands with 4 wire-classes: `coverage_gap` + 3 evidential-family reasons preserved (per §5.1 sub-option (a1) recommendation); AskConsole renders 3 UI shapes by mapping `coverage_gap`→"not-extracted-yet", any evidential-refusal-family class→"evidence-can't-support" (bucketed at render), and the fault-envelope render path→"something-broke" (distinct styling · not a refusal class at wire).
- **(b)** `Service1Refusal@v1` envelope lands with 3 wire-classes matching Prove-spec 1:1: `coverage_gap` · `evidence_cant_support` · fault-family remains outside the refusal envelope (as per (a)). This collapses `no_defensibility_floor` · `no_lawful_basis` · `composition_below_floor` into a single `evidence_cant_support` class at v1 — lossy for the currently-3-way evidential taxonomy.
- **(c)** Two-envelope posture (§5.1 sub-option (a2)): v0 preserved emitting evidential-family reasons unchanged; v1 emits `coverage_gap` only; AskConsole reads both and maps to Prove-spec 3 shapes at render.
- **(d)** Reject Prove-spec taxonomy and retain engineering-canon 3-reason enumeration (lossy on the Prove UX side).
- **(e)** Other Owner ruling.

**HAZARD-STOP posture:** at STEP 4 EAB-2 Stage-A refresh, this shape-mismatch must be surfaced with byte-level evidence **BEFORE** the Parity 31→32 seal (per Owner Configuration Dispatch §4.STEP-4). Ruling on (a)/(b)/(c)/(d)/(e) is required at that Stage-A refresh, not at this reconciliation audit close.

**HAZARD-STOP surfaced here as pre-EAB-2 signal · not blocking Substrate-Drop v3 close · Owner may address at EAB-2 Stage-A refresh atomic.**

**RESOLVED by `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` · SHA `8b074dc152b41ed300d5a7626a2a1bd5aa1213371f6eeeac0a096e12f2d6d4a5` · Prove Step 4 amended in sibling file · Owner ruled Locus 1 = ε with Owner-authored Prove-spec amendment (ζ-equivalent posture · Owner-authored not builder-authored). Composition ε + α + γ. Service1Refusal@v1 reason enum = exactly 4 members (3 v0 evidential + coverage_gap); `something-broke` routes on fault channel (HTTP 503 + PROM-S1-config-defect-fail-loud). No `estimated_effort` field on envelope (Locus 2 = α · Targeta companion-read). No `queue_action_url` field on envelope (Locus 3 = γ · Prove-side derivation from `filed_candidate_id`). Prove Step 4 sibling amendment at `docs/mandates/module_specs/05_prove_module_step4_amendment_2026_07_24.md` (SHA `2c3526aa739868afebff2a495adc7083eebb3d0023ad59cc62abb394c8ac963d`); original `05_prove_module.md` byte-identical.**

### §B.C-2 · Role taxonomy divergence · Connect Module vs on-disk auth vocabulary

**Conflict source:** `01_connect_module.md § Users Involved` — introduces **DPO**, **Data Engineer**, **Governance Sponsor**, **Governance Co-Signer** as first-class roles.

**Conflict target:**
- `docs/mandates/RMS_UI_Specification_v2_2.md` §2.1 (per prior Dispatch 1 Sub-scan 3): canonical roles are Master Admin · Operator · DPO · Data Buyer · Integrating Application.
- On-disk role vocabulary (`services/auth/**`, `routers/**`): Master Admin · engineer · operator · buyer-cut · analyst.

**Divergences:**

| Role in module spec | UI Spec v2.2 §2.1 canonical | On-disk vocabulary | Ruling required |
|---|---|---|---|
| DPO | DPO (match) | **absent** (not landed on-disk) | Confirm role literal `dpo` for auth + landing paths |
| Data Engineer | (absent · UI Spec has "Integrating Application" as app-actor) | `engineer` (adjacent · human role) | Reconcile: is Data Engineer = engineer literal (rename or alias)? |
| Governance Sponsor | (absent) | absent | Confirm new role literal · succession discipline anchor |
| Governance Co-Signer | (absent) | absent | Confirm new role literal · dual-control anchor |

**Owner ruling required on:** role-literal canonicalization + landing sequence (which role lands at which module dispatch).

**No auto-supersession.**

### §B.C-3 · Console-vs-Module naming taxonomy divergence

**Conflict source:** module specs use **"Connect module · Registry module · Extract module · Govern module · Team module · Prove module"** taxonomy.

**Conflict target:** UI Spec v2.2 §2.1 uses **"Extraction Console · Compliance Console · Integration Console · Administration Console · Ask Console · TraceReceipt public page"** taxonomy.

**Naming divergences:**

| Module spec name | UI Spec v2.2 §2.1 name | Semantic overlap | Ruling required |
|---|---|---|---|
| Connect module | (subsumed under Integration Console · Administration Console) | partial | Which is canonical name for landing? |
| Registry module | Extraction Console (partial · registry is a sub-tab of extraction) | partial | Which is canonical? Is Registry a sub-tab of Extraction or its own module? |
| Extract module | Extraction Console | overlap · differ on scope | Which module boundary is canonical? |
| Govern module | Compliance Console | overlap · Govern spec is broader | Which is canonical name? |
| Team module | Administration Console (partial) | partial | Is Team a sub-tab of Administration or its own module? |
| Prove module | Ask Console + TraceReceipt public page | overlap · Prove spec is broader (Memos · Public Receipts) | Which is canonical? |

**Owner ruling required on:** taxonomy convergence — either (a) module-spec taxonomy supersedes UI Spec v2.2 §2.1, or (b) UI Spec v2.2 taxonomy supersedes module specs, or (c) taxonomies coexist with an explicit mapping table.

**No auto-supersession.**

### §B.C-4 · "Analyst" role usage divergence

**Conflict source:** `03_extract_module.md § Users Involved` — Analyst is a first-class role.

**Conflict target:** Product Doc §21 sub-taxonomy uses "Business user (Analyst, product owner, risk officer, researcher)" — Analyst is sub-taxonomy under Business user. Prior Dispatch 1 Sub-scan 3 flagged this as vocabulary drift.

**Ruling required:** is Analyst a first-class role (Extract Module) or sub-taxonomy under Business user (Product Doc §21)?

**No auto-supersession.**

### §B.C-5 · Waiting-period constants (Change-a-Rule 72h · Destroy-Data 24h) not in engineering canon

**Conflict source:** `04_govern_module.md § Change-a-Rule 72h` + `§ Destroy-Data 24h`.

**Conflict target:** No 72h / 24h constants in engineering canon. `docs/requirements/operating_values_v1_1.md` §6 seam values do not include these two constants.

**Ruling required:** admit as new seam values (F-class fold in Operating Values v1.2)?

**No auto-supersession.**

### §B.C-6 · Public Receipt lifecycle (DPO-only · no-login verify · expiry · revoke · verification log) not in engineering canon

**Conflict source:** `05_prove_module.md § Public Receipts`.

**Conflict target:** No public-receipt contract on-disk. `TraceReceiptPage.js` renders TraceReceipt public page (per Playwright cell); DPO-only generation + revoke + verification-log are not landed.

**Ruling required:** admit as a new contract (`PublicReceipt@v0` or similar frozen contract · Parity additive · rides OD-9 + PH-R3).

**No auto-supersession.**

### §B.C-7 · Usage-rights enum (4-value) not in engineering canon

**Conflict source:** `01_connect_module.md § Journey 1 Step 4 Data Sources · Usage Rights` — 4-value enum.

**Conflict target:** No usage-rights enum in engineering canon. `services/data_source/**` carries source-standing shape without usage-rights taxonomy.

**Ruling required:** admit as a new frozen enum (contract additive · Parity additive). Module spec does not enumerate the 4 values literally; Owner may need to author the 4 literal values.

**No auto-supersession.**

### §B.C-8 · Succession 3-party Sponsor incl. CEO not in engineering canon

**Conflict source:** `04_govern_module.md § Governance Setup succession` + `06_team_module.md § Governance Co-Signer / Sponsor succession pointer`.

**Conflict target:** No 3-party succession primitive on-disk. `services/checker/**` (checker/countersign flow at `routers/checker.py`) supports 2-party countersign patterns but not 3-party attestation with a named CEO seat.

**Ruling required:** admit as extension of checker with 3-party primitive + CEO seat as new role literal.

**No auto-supersession.**

### §B.C-9 · Notification Center + email fanout not in engineering canon

**Conflict source:** module specs across Connect · Govern · Extract · Team · Prove all reference notification-center + email fanout.

**Conflict target:** No Notification Center on-disk. No email fanout backend.

**Ruling required:** rides OD-8 · already surfaced as Owner-decision register row.

**No auto-supersession.**

### §B.C-10 · Ask Akki Drawer + Answer Card single-shell (Owner STEP 5 structural directive)

**Conflict source:** `07_shared_components.md § Ask Akki Drawer` + Owner Configuration Dispatch §4.STEP-5 verbatim structural directive: *"the Answer Card + refusal-shape component family is built once in the shared shell and consumed by both Prove and the Ask Akki drawer — the spec declares them the same structure; two implementations is self-inflicted drift and will be treated as a D-class finding."*

**Conflict target:** Currently `AskConsolePage.js` and `TraceReceiptPage.js` are separate implementations at separate routes. No shared shell exists.

**Class:** D-12 (component-family drift) · UI-1/UI-2 execution scope · Owner-verbatim structural directive.

**Ruling required (at UI-1/UI-2 Stage A per §0-CAL.2 gate-cell roster):** shared-shell factoring must land as a gate-cell-asserted invariant (Ask Akki Drawer + Answer Card + refusal shapes = single component-family shell). Any Stage A that would land two implementations = D-class finding per Owner directive.

**No auto-supersession · gate-cell attest required at UI-1/UI-2 Stage A.**

---

## §C · New Owner-decision register rows minted

Landed at `docs/registers/owner_decisions_v1.md` (mint 2026-07-24 · v1.0 register). SHAs verified live this session.

| OD row | Title | Class | State | Sequence-blocking on |
|---|---|---|---|---|
| **OD-8** | Mail-provider binding · Notification Center email fanout | Owner-decision required · sequence-blocking | open | Connect execution dispatch · Govern Change-a-Rule/Destroy-Data/Release Review/Sponsor succession dispatches · Team invitation flow · Extract commissioned-objective approval · Public Receipts revocation |
| **OD-9** | Public-surface exposure posture · Public Receipts no-login page | Owner-decision required · sequence-blocking | open | Prove Module execution dispatch (Public Receipts subsurface) · PH-R3 finalization · external-facing memo release |
| **OD-10** | Scheduler primitive · census debounce / auto-trigger | Owner-decision required · sequence-blocking | open | Registry Module execution dispatch (auto-trigger + debounce subsurfaces) · Connect execution dispatch (post-signoff first-census kickoff) · Mtafiti backend scheduling additive-surface completion (G-13 §8.1) |

**Zero-loss attest per Owner §4.STEP-3:** every rides-list item preserved intact from module-spec text; no de-scoping performed.

**All 3 rows land as explicit register rows, not buried phase content** (per Owner mandate verbatim).

---

## §D · CODE_IMPACT summary counts (STEP 5 re-band substrate)

**Terminal figures per module. These figures are the STEP 5 re-band substrate. Nothing else may be cited for module-phase bands.**

| Module | NET-NEW | PARTIAL-EXTEND | CONFORMS | Total feature rows |
|---|---:|---:|---:|---:|
| Connect | 13 | 1 | 0 | 14 |
| Registry | 7 | 5 | 0 | 12 |
| Extract | 5 | 8 | 1 | 14 |
| Govern | 13 | 5 | 0 | 18 |
| Prove | 13 | 3 | 1 | 17 |
| Team | 7 | 2 | 1 | 10 |
| Shared Components | 6 | 0 | 0 | 6 |
| Product Doc | (descriptive canon · subordinate per §22) | | | (0 code-bearing rows) |
| User Stories | (story-catalog · no net-new features · already counted in modules above) | | | (0 net-new rows) |
| **TOTAL** | **64** | **24** | **3** | **91** |

**CONFLICT row count:** 10 (§B.C-1 through §B.C-10) · each requires per-conflict Owner ruling · no auto-supersession.

**Owner-decision (OD) row count:** 3 new rows (OD-8/9/10) at `docs/registers/owner_decisions_v1.md`.

---

## §E · Zero-loss attest (per Owner §4.STEP-3 verbatim)

Every one of the following features entered the audit intact — de-scoping is not an audit output:

**Succession attestations:**
- Governance Co-Signer 2-party succession (DPO + outgoing Co-Signer) · `04_govern_module.md § Governance Co-Signer succession` · `06_team_module.md § Governance succession pointer` — **audit § A.4 row 8 · §B.C-8**
- Governance Sponsor 3-party succession (DPO + outgoing Sponsor + CEO) · `04_govern_module.md § Governance Setup succession` — **audit §A.4 row 8 · §B.C-8**

**Waiting periods:**
- Change-a-Rule 72h · `04_govern_module.md § Change-a-Rule` — **audit §A.4 row 4 · §B.C-5**
- Destroy-Data 24h · `04_govern_module.md § Destroy-Data` — **audit §A.4 row 5 · §B.C-5**
- Team promotion DPO-approval (no specific hour · policy-open) · `06_team_module.md § Master Admin promotion` — **audit §A.6 row 4**

**Refusal shapes (3):**
- Not-extracted-yet + gap-queue affordance + estimated effort · `05_prove_module.md` — **audit §A.5 row 4 · §A.5 rows 5-6 · §B.C-1 HAZARD-STOP**
- Evidence-can't-support · `05_prove_module.md` — **audit §A.5 row 4 · §B.C-1 HAZARD-STOP**
- Something-broke · `05_prove_module.md` — **audit §A.5 row 4 · §B.C-1 HAZARD-STOP**

**Receipt behaviors (5):**
- DPO-only generation · `05_prove_module.md § Public Receipts § generation` — **audit §A.5 row 11 · §B.C-6**
- No-login verify · `05_prove_module.md § Public Receipts § verify` — **audit §A.5 row 12 · §B.C-6**
- Expiry lifecycle · `05_prove_module.md § Public Receipts § expiry` — **audit §A.5 row 11 · §B.C-6**
- Revoke · `05_prove_module.md § Public Receipts § revoke` — **audit §A.5 row 13 · §B.C-6**
- Verification log · `05_prove_module.md § Public Receipts § verification-log` — **audit §A.5 row 11 · §B.C-6**

**Notification categories (5+):**
- Connect DPO sign-off email · **audit §A.1 row 9 · OD-8**
- Govern approvals (Change-a-Rule · Destroy-Data · Release Review · Sponsor 3-party) · **audit §A.4 rows 16-18 · OD-8**
- Extract approvals (commissioned-objective approval · Model Acceptance) · **audit §A.3 row 9 · OD-8**
- Team promotion (invitation email · Master Admin promotion DPO-approval) · **audit §A.6 rows 9-10 · OD-8**
- Prove Release Review decision notification · **audit §A.5 row 14 · OD-8**

**Usage-rights enum (4-value):**
- `01_connect_module.md § Journey 1 Step 4` — **audit §A.1 row 6 · §B.C-7**

**Zero features de-scoped. Every intact.**

---

## §F · D-1..D-11 self-audit table (standing practice per Critic Seam Spec v1.0 §5 + Owner §5)

| # | Defect | Verdict | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Every §A row traces to a module-spec § anchor + a shipped-surface anchor (file path) or explicit "not landed" verdict. Every §B row cites both conflict source and conflict target with verbatim quotes. Every §C row traces to Owner §4.STEP-3 mandate. |
| D-2 | NL-only claim | PASS | Every SHA, line-count, file existence, route path, contract class name is disk-verifiable via commands recorded in this atomic (`sha256sum`, `wc -l`, `ls`, `grep`, `git log`). |
| D-3 | Curated verdict | PASS | Full enumeration: 91 CODE_IMPACT rows across 7 code-bearing artifacts + 10 CONFLICT rows + 3 OD rows. Zero cherry-picking. Every module counted; Product Doc and User Stories explicitly no-code-impact-classified with rationale. |
| D-4 | Rung inflation | PASS | No rung claims. Audit body carries only findings + Owner-ruling surfaces + attests. |
| D-5 | Cross-phase content leakage | PASS | Zero EAB-3 · Critic-pass · G-13 (post-Substrate-Drop-v3) · UI-1 · UI-2 execution content. HAZARD-STOP surface (§B.C-1) explicitly pre-named for STEP 4 EAB-2 Stage-A refresh atomic, not enacted here. |
| D-6 | Silent scope drift | PASS | Scope: reconciliation-audit-only per Owner §4.STEP-3. Zero product-code touch. Makefile Tier-3 (build tooling) landed in the same STEP-3 atomic per Owner STEP-2 Surfaces ruling; disclosed inline at close report §5 not here (proper compartmentalization). |
| D-7 | Invented scope | PASS | Every feature row corresponds to a specific module-spec § anchor; zero fabricated. All 3 OD rows have Owner-verbatim mandate excerpts. CONFLICT rows carry both conflict-source and conflict-target verbatim quotes. |
| D-8 | Silent drift | PASS | Standing Rule v3 attest: `backend/contracts/**` zero touch · Parity 31 held · `docs/governance/tiered_ruling_model.md` §§1..22 byte-identical (only §23 additive) · zero contract file created · zero snapshot file created this atomic. |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked. `make ci` green attest recorded via native `pytest` (backend), `yarn test` (Jest), `npx playwright test --project=chromium` (Playwright) — all in close report §5. |
| D-10 | Menu emission | PASS | §B CONFLICT rows and §B.C-1 HAZARD-STOP surface options (a/b/c/d/e) are **Owner-ruling surfaces pre-named per Owner mandate** — structured per §5.1-precedent enumeration pattern (EAB-1/EAB-2 Stage A precedent), NOT builder permission menus. Ruling authority is Owner; disposition is not builder Tier-3. |
| D-11 | Canon-before-ruling / LLM-memory recall | PASS | Every module-spec citation traces to live `sed`/`head`/`grep` on the just-landed `docs/mandates/module_specs/*.md` files (SHAs recorded in MANIFEST.md this atomic). Every shipped-surface citation traces to file-existence check + inspection via `ls`/`grep`/`find`. Every contract reference traces to `sha256sum` verified this atomic. Prior LT-2 forensic-correction lesson applied (BUILD_JOURNAL canon-first for historical claims). Zero memory-recall presented as fact. |

---

*Substrate-Drop v3 · Reconciliation Audit · landed 2026-07-24 · Standing Rule v3 · D-11 canon-before-ruling · D-10 self-audit table attached · Owner-verbatim mandate carried at §§1, 4, and §B.C-10 · 91 CODE_IMPACT rows + 10 CONFLICT rows + 3 OD rows enumerated · zero-loss attest at §E · **HAZARD-STOP surface at §B.C-1 pre-named for STEP 4 EAB-2 Stage-A refresh · NOT blocking Substrate-Drop v3 close** · prior CODE_IMPACT preview carries no evidentiary weight.*
