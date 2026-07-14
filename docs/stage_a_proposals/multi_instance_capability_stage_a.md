# Multi-Instance Capability Stage A · 2026-07-14

**Authorization:** Owner dispatch 2026-07-14 (envelope verbatim §12).
**Predecessor rulings:** IF-1 close · G-10/G-7 PROMOTE 2026-07-14 · Register v1.2 at SHA `b8b45d2424ecfcce5f84593b1f6142104d734fb805c3e6b132b4e9953e72c90b`.
**Sanctioned pre-work:** YES — Owner-dispatched. Not a D7 finding. (Contrast: `sequencing_harness_stage_a.md` line 1 carries the `UNSANCTIONED PRE-WORK · D7 finding` marker; its STRUCTURE is used here as reference precedent, its content is not authorization.)
**Governance:** Standing Rule v3 · on-disk canonical · Registry Doctrine v1.0 R4 + D-10 · Tiered-Ruling §12/§12.1/§12.2/§13/§14/§15/§16 · Defect D-7 (scope) + D-11 (canon-before-ruling) bind.
**Doctrine SHA (in force):** `9dd1cc4bee310ad36780d182377ae8f3e25b7a681430c982dda18d76a408fbcf` (registry_doctrine_v1.md).
**Operating Values SHA (in force):** `a6c4a455175ef37dc71362aea2e41b2ce406baaf9a1c77b3f0f1326e0aa608ee` (operating_values_v1.md).
**Tiered-Ruling SHA (in force):** `187ad8ee6764956a88167b38c6a904c4c43074f6804ee396f627bc2da9a55dbc` (tiered_ruling_model.md).

## §0 · Principle binding (Owner verbatim)

> Principle binding the whole phase: the platform is organization-agnostic; the estate's contents — never the customer's identity — decide which capabilities do work. Instance identity lives in configuration; platform code, contracts, and vocabulary carry no organization.

**Doctrinal consequence:** the four capabilities in §1 are jointly a single split — capability-1..3 add the multi-instance surface; capability-4 discharges the residue where the platform's identity leaked into code/config/copy before the split was named. §5's audit shows the current LoC surface of that leak; §1.4 + §5 land the split in one atomic phase, no successor cleanup deferred.

## §1 · Scope — four capabilities

### §1.1 Structured-source connector class

**Owner dispatch text (verbatim):**
> Structured-source connector class: generic tabular/DB ingestion → NormalizedUnits through the existing intake path — same unit grammar (who/what/when/where/class), provenance-paired, license_class at ingest, census discovering composition. Fixture shapes may be informed by real catalogues on hand; no organization's name, schema, or assumptions enter code, contracts, or vocabulary — per §8, the platform learns each estate at census, never before. Estates with AV route through the existing 9.2a perception path unchanged; no new perception work rides this phase.

**On-disk anchors (D-11 canon):**
- **NormalizedUnit ingest entry point:** `backend/services/data_source/synthetic.py:155` constructs `NormalizedUnit(...)` from a synthetic estate seed; `backend/services/data_source/real_rms.py:15` imports `NormalizedUnit` (module name is itself flagged for §5 class-(b) rename). Additional constructors at `backend/services/perception/asr_worker.py:201` and `diarization_worker.py:153` (AV perception path — preserved unchanged per Owner's D-7 fence).
- **five_rings@v0 contract shape** (`backend/contracts/five_rings.py:276-308`, SHA `5d59da2a077d55f777d88df9ae09bd1ee0f21481fd0d6af3bd5ed9b76fd3c01e`, verbatim excerpt):
  > `NormalizedUnit(unit_id, provenance, signal, relational, reextraction_handle, defensibility)` — "the single modality-neutral unit produced by Layer C. Every Layer-D primitive reads from NormalizedUnits."
  Modality enum at line 44-59 admits `text · audio · video · image · composite`. Tabular ingest maps `text` per unit-row (or defers modality until census discriminates); no enum extension required at G0.
- **Census discovery seam** (`backend/services/mtafiti/census.py:1-46`, SHA `53110a1dd178d5201542d04f2627dbc38f46c00c1aa6d548c72b000fb61d19aa`): consumes `NormalizedUnit`s, classifies sensitivity by `provenance.modality`, feeds `SourceCandidate`. Tabular units enter the same walker with `modality=text` (or composite for mixed sources); no new discovery code required.
- **license_class at ingest:** `NormalizedUnit` has no direct `license_class` field; per Op. Values §7 line 77 (verbatim, SHA `a6c4a455…`): *"License terms machine-attached to every artifact — license_class from the v1 registry rides the receipt."* — license_class rides at the connector-registration layer, attaching to units downstream of the connector, not on the frozen contract. **Zero five_rings@v0 mutation.**

**Operating Values §8 verbatim citation** (SHA `a6c4a455…` lines 85-97):
> **§8 — Org-context onboarding requirements (S2.onboard · completes Q3-02 specification)**
>
> The surface, when dispatched, captures minimally — structured intake, versioned like everything else:
>
> - Estate inventory: sources, systems, custodians.
> - Organizational vocabulary: entities, brands, people-of-record — seeds Targeta targeting and Mtafiti entity resolution.
> - Rights posture per source: what the organization may license onward — feeds license_class at ingest.
> - DPO contact + the five §6 seam values, set per-instance here.
> - Objective priorities — seeds the first opportunity-brief cycle.

**Data-blind posture attest** (Governance §8 SHA `187ad8ee…`): fixture shapes at execution will not encode any organization's schema. Fixture-B (per §1.3) is generic tabular + small synthetic AV; the census discovers composition — the platform makes no pre-build data assumption.

### §1.2 S2.onboard surface — first consumer

**Owner dispatch text (verbatim):**
> S2.onboard surface — first consumer: structured intake per Operating Values §8 verbatim (estate inventory, org vocabulary, rights posture per source, DPO + the five seam values per-instance, objective priorities), versioned, feeding connector registration and the tenant-entity seat the IF-1 stub reserved.

**On-disk write-target anchor:** `backend/services/synisense/shield/tenant_entities.py:25-35` (SHA `27c6fa20dcae4d6256dfee0998bfcc9d9c42070b9f031fa643b3ad8e8fc13ab0`) — the IF-1-era empty-catalogue stub returns `[]` unconditionally; its docstring (line 9-11 verbatim) states: *"When S2.onboard binds (the buyer-onboarding journey seat), estate vocabulary lands here per the OWNER-decision register (OD-1) and Op. Values §8."* This is the write path S2.onboard populates.

**Journey mapping** (per Registry Doctrine v1.0 §S2, SHA `9dd1cc4b…`): S2 journey step "onboard context" — service anchor for the whole surface. Every function this phase lands cites `S2.onboard-context` in `service_trace`.

**Five §6 seam values** (per Op. Values SHA `a6c4a455…` lines 61-71 verbatim):
> - **Deletion consequence classes:** class-C (irreversible, cross-slice) → dual-control always · class-B batch >1,000 units → Owner escalation · class-A (reversible, single-slice) → operator-level.
> - **Rule-tightening delay window:** 72 hours.
> - **Objection escalation window:** 7 days, then auto-annotate-and-proceed.
> - **Suspension re-review:** 30 days, ledgered.
> - **Outer-gate manual-review threshold:** >10,000 units or >1GB per export artifact.

The S2.onboard form persists these per-instance; dual-control adjacency stands where an instance changes an already-set seam value (see MC-E3).

### §1.3 Multi-instance operability v1

**Owner dispatch text (verbatim):**
> Multi-instance operability v1: one codebase, per-instance configuration isolation — instance-scoped seam values, estate inventory, model-registry entries, connector registrations, and (per item 4) instance identity. Proof shape: a second synthetic instance — instance-fixture-B, a generic structured estate (tabular + small AV, synthetic) — stands up beside the existing fixture estate in CI and walks onboard → connect → census → brief → answer end-to-end, with isolation cells proving no cross-instance read on any surface (registry, ledger, keys, census).

**Surfaces requiring per-instance scoping (D-11 enumeration):**
| Surface | Current single-instance location | Instance-scoping mechanism (execution-time proposal) |
|---|---|---|
| Seam values (five §6) | Env-var-configurable per deployment; no in-app instance discrimination | Per-instance config record `instances/{instance_id}/seams.json` (or Mongo collection `instance_seams` keyed by `instance_id`); accessor reads by `instance_id` on request |
| Estate inventory | Not persisted at all today (Op. Values §8 says "when dispatched") | New Mongo collection `instance_estate_inventory`; S2.onboard write path |
| Model-registry entries | `backend/services/perception/models_registry.v0.json` (SHA `291de8ed…`) — global, one file | Instance-scoped copy-on-difference: `instances/{instance_id}/models_registry.v0.json`; default reader falls back to global if instance-level absent (**zero contract mutation** — the JSON shape is unchanged) |
| Connector registrations | Not persisted today (implicit in `backend/services/data_source/synthetic.py:1-30` module import path) | New Mongo collection `instance_connectors` |
| Instance identity | Absent — platform assumes single-instance | New env var `INSTANCE_ID` (or per-request header `X-Instance-Id` where the platform routes multi-instance calls); resolves to `instance-fixture-a` (default, existing state) or `instance-fixture-B` (new proof) |
| Ledger / registry / census reads | Not scoped today | Access-side isolation cells (MC-E2): every read on Northena ledger / Mtafiti census / Function Registry passes `instance_id` filter |

**Proof shape (Owner-dispatched):** instance-fixture-B walks the full onboard → connect → census → brief → answer path in CI; isolation cells assert cross-read denials (fixture-A cannot see fixture-B's rows on any surface).

### §1.4 RMS de-tuning — the platform/instance identity split

**Owner dispatch text (verbatim):**
> RMS de-tuning — the platform/instance identity split. Stage A includes an audit section: enumerate every organization-specific token in live code, config, contracts, fixtures, routes, and UI copy (grep classes: RMS, rms_, Royal Media, broadcaster-specific strings; e.g. the Ask Console's "RMS Intelligence" branding, the rms_adversarial_v1 fixture directory name). Classify each: (a) branding → instance config (display name, product title, headers move to the instance-config surface item 3 creates; instance #1's config carries "RMS Intelligence"); (b) rename (org-token identifiers in live code/fixtures get neutral names); (c) legitimate historical (mandate filenames, close reports, rulings — Standing Rule v3, byte-identical, untouched; list only). Execution applies (a) and (b); the platform ends this phase with zero organization identity outside instance config and historical canon.

**Audit table:** the full grep-driven enumeration lives in §5 below. Summary count: **823 raw hits** across the four grep classes (RMS · rms_ · Royal Media · RMS Intelligence). Class distribution: (a) branding **20 hits** · (b) code/fixture rename **~55 hits** · (c) legitimate historical **~748 hits** (of which ~4 are inside `backend/tests/invariants/*.contract_snapshot.json` — MC-E5 SHA-pinned surface, escalated not renamed). Every hit inside `backend/contracts/*.py` **14 files** — MC-E5 escalated en-bloc; no rename proposed on the frozen contract tier.

## §2 · LoC band per Operating Values §9 · Governance §9 (metric-verdict-in-derivation-unit)

**Operating Values §9 verbatim** (SHA `a6c4a455…` lines 99-105):
> **§9 — PH-R2/R3/R4 acceptance criteria**
>
> - **Data plane (PH-R2):** managed replicated DB · RPO ≤ 1h / RTO ≤ 4h (NORM) · ledger archival append-only to object storage, 7-year retention (NORM · audit-record convention, DPA-compatible) · quarterly restore drill (DEFAULT).
> - **Domain + TLS (PH-R3):** TLS ≥ 1.2 + HSTS (FACT-class floor) · trace ids survive domain moves — receipt URLs stable as config.
> - **LLM swap (PH-R4):** target shape per llm_swap_seam.md · cutover proven by the AF golden set: mechanical arm byte-identical, fluent arm re-validated through the grounding gates · zero call-site changes per BCR.

**D-11 canon note:** Op. Values §9 is the PH-R2/R3/R4 deployment acceptance criteria and does NOT carry the LoC-banding discipline the dispatch's phrase "band in raw LoC per §9" refers to. Per precedent (`fixture_refresh_fr_e1_to_e3.md:6` · `opportunity_briefs_ob_e1_to_e3.md:135` · `answer_fluency_af_e1_to_e4.md:144` · `production_housing_ph_r1_ph_e1_to_e4.md:96` — all Owner-ratified closes), "§9" in that phrase resolves to `docs/governance/tiered_ruling_model.md §9` (the metric-verdict-in-derivation-unit ruling). Op. Values §9 is cited above (verbatim, per dispatch instruction); the LoC verdict itself binds against Governance §9, cited next.

**Governance §9 verbatim** (SHA `187ad8ee…` lines 249-251):
> Metric ruling, binding on all closes (Owner, 2026-07-10): a band's compliance verdict is rendered in the unit the band was derived in — currently raw LoC. LLoC (or any alternate unit) is welcome as a disclosure line, never as the verdict. A builder who believes a different unit is honester proposes it at the next Stage A, where derivation and verdict move together.

**Band derivation** (per Governance §6 rate ledger applied to phase-execution scope; ratified Stage A projection, not the close-time actual):

| Line-item | Rate anchor (Governance §) | LoC estimate |
|---|---|---|
| **Cap. 1 — Structured connector base module** | §6.3 backend service module standalone · 100 LoC/module | **~180** LoC (base class + tabular ingest + provenance-pair helper) |
| **Cap. 1 — Fixture shape module** | §6.3 amortised (fixture module ≠ service module; conservative half-rate) | **~120** LoC |
| **Cap. 1 — Fixture JSON** | Data file, unit-count-driven | **~60** LoC |
| **Cap. 2 — S2.onboard React page + panels** | Frontend Jest structural standalone · §6.4 16 LoC/cell (proxy rate for React page complexity) · ~15 cells | **~240** LoC |
| **Cap. 2 — S2.onboard backend receiver endpoint** | §6.2 backend endpoint impl amortised 3-share · 40 LoC/endpoint | **~40** LoC |
| **Cap. 2 — S2.onboard Jest gates** | §6.4 16 LoC/cell · 5 cells | **~80** LoC |
| **Cap. 2 — tenant_entities write-path implementation** | §6.3 service module partial · ~half-module | **~50** LoC |
| **Cap. 3 — Instance config service module** | §6.3 100 LoC/module · full | **~180** LoC |
| **Cap. 3 — Cross-instance isolation gates** | §6.11 async httpx auth-overhead · 25 LoC/cell · 8 cells | **~200** LoC |
| **Cap. 3 — Instance-fixture-B synthetic estate** | Data file + generator scaffold | **~200** LoC |
| **Cap. 3 — CI wiring for two-fixture parallel run** | §6.1 amortised · 12 LoC/cell · ~5 cells | **~60** LoC |
| **Cap. 3 — E2E onboard→connect→census→brief→answer Playwright** | §6.5 9 LoC/cell · 1 cell | **~9** LoC |
| **Cap. 4 — Instance-config branding surface** | §6.3 partial + Cap. 3 shared | **~90** LoC |
| **Cap. 4 — Class-(b) code renames · fixture dir + refs** | Amortised at ~5 LoC/reference · ~30 refs across ~15 files | **~150** LoC |
| **Cap. 4 — Class-(a) frontend branding move** | ~15 files × ~4 LoC each (extract to instance config accessor) | **~60** LoC |
| **Cap. 4 — Reflection gate: RMS-token-negative on live surface** | §6.10 AST/reflection · 40 LoC/cell · 1 cell | **~40** LoC |
| **Rulings + close report** | §6.9 verbatim-carrier · ~1 carrier | **~130** LoC |
| **R4 v0.5 registry supplement** | §14 pattern · ~20 R4 rows | **~200** LoC |
| **Owner-verbatim carriers (dispatch + rulings) across modules** | §6.9 verbatim-carrier · additional 1 carrier for Stage A trailer | **~100** LoC |
| **Register v1.2 → v1.3 amendment** | Amendment-scope section, additive | **~80** LoC |
| **Raw total (projected phase execution)** | | **~2,269 LoC** |

**Band ratified (Stage A proposal):** `[1,900, 2,700]` raw LoC · verdict rendered in raw LoC per Governance §9.

**Split-threshold check** (Governance §6.10 rate carrier / §4.2 threshold `1,500 raw LoC / 60 cells`): projected raw is above 1,500 → **pre-authorized split** available at execution time; disclosure only per Tier-2. Cell count projected ~40 (below 60). Splits candidate seams: (I) Cap. 1 + Cap. 4 audit-execution as commit A; (II) Cap. 2 + Cap. 3 with proof walkthrough as commit B. Execution-time builder decides; no Owner round-trip.

## §3 · R4 rows per §14 supplement pattern

Landing target: `docs/registry/function_promise_registry_v0.5_supplement.md` (additive supplement · Governance §14 pattern · v0.md + v0.1..v0.5 combined ↔ `registry.yaml` round-trip).

Estimated ~20 R4 reflexive rows across:

| Row group | Rows | Governor | Enforcement class |
|---|---|---|---|
| Structured connector class (§1.1) | 3 · `rms.data_source.structured_connector_base` · `rms.data_source.tabular_ingest_normalizes_units` · `rms.data_source.license_class_pairs_at_ingest` | Named surface (data_source) | pytest end-to-end · runtime check |
| S2.onboard surface (§1.2) | 4 · `rms.frontend.s2_onboard_public_route` · `rms.backend.s2_onboard_receiver_persists_instance_scoped` · `rms.backend.tenant_entities_populates_from_s2_onboard` · `rms.backend.s2_onboard_writes_five_seam_values_dual_control_adjacent` | Named surface (frontend + Synisense) | jest + pytest + playwright |
| Multi-instance operability (§1.3) | 6 · `rms.instance.identity_from_config_only` · `rms.instance.seams_scoped_by_instance_id` · `rms.instance.estate_inventory_scoped_by_instance_id` · `rms.instance.models_registry_scoped_by_instance_id` · `rms.instance.connectors_scoped_by_instance_id` · `rms.instance.no_cross_instance_read_on_any_surface` | Named surface (instance) | async httpx isolation cells |
| RMS de-tuning (§1.4) | 4 · `rms.detune.branding_moved_to_instance_config` · `rms.detune.fixture_dir_renamed_org_agnostic` · `rms.detune.no_rms_token_in_live_code_outside_config` · `rms.detune.contract_tier_rms_tokens_preserved_class_c_historical_by_ruling` | Named surface (Deviation-audit reflexive) | reflection gate (AST) + fs-grep |
| Register + close (§7) | 2 · `rms.register.v1.3_amendment_close_multi_instance_capability` · `rms.close.multi_instance_capability_atomic_commit_close_report` | Named surface (governance) | fs-grep |
| Fixture-B walkthrough (§4) | 1 · `rms.ci.fixture_b_walks_onboard_to_answer_e2e` | Named surface (CI) | playwright + pytest |

**Row schema:** 11-field per Registry Doctrine §3.2 (function_id · governor · mandate · promise · service_trace · surface · enforcement · cost · dependencies · ladder_rung · owner). Every row cites service_trace `S2.onboard-context` or `S1.call` per §1.3 (D-1 reasoning order). Every row targets promise `PROM-S1-frozen-wire-contract` or `PROM-S2-onboard-instance-scope` (new promise? — see §6 MC-E3 escalation) — no new promise minted without Owner ruling per D-4 + D-6 + R2.

## §4 · Isolation-cell shape (Multi-instance proof)

**Cross-instance read denials — 8 isolation cells (async httpx pattern · §6.11 · 25 LoC/cell):**
1. `test_cross_instance_registry_read_denied` — fixture-A auth-token cannot read fixture-B's Function Registry rows via `/api/registry/query`.
2. `test_cross_instance_ledger_read_denied` — fixture-A cannot read fixture-B's Northena ledger rows via `/api/northena/trace/{traceId}` (foreign trace_id) or the ledger-list endpoint.
3. `test_cross_instance_key_custody_denied` — fixture-A cannot access fixture-B's tenant-key material (Shield custody chain SYNISENSE_MASTER_SECRET scoped).
4. `test_cross_instance_census_read_denied` — fixture-A cannot read fixture-B's Mtafiti census outputs.
5. `test_cross_instance_estate_inventory_read_denied` — fixture-A cannot see fixture-B's S2.onboard-written estate inventory.
6. `test_cross_instance_models_registry_read_denied` — fixture-A sees only its own model registry entries (own + global fallback), never fixture-B's instance-specific overrides.
7. `test_cross_instance_seam_values_read_denied` — fixture-A cannot read fixture-B's five §6 seam values.
8. `test_cross_instance_connector_registration_read_denied` — fixture-A cannot see fixture-B's connector registrations.

**Instance-fixture-B end-to-end walkthrough — 1 Playwright cell (§6.5 · 9 LoC/cell):**
- Step 1 · `POST /api/s2/onboard` with fixture-B estate inventory + org vocabulary + rights posture + DPO + seam values + objective priorities.
- Step 2 · `POST /api/connectors/register` with fixture-B's synthetic tabular connector.
- Step 3 · trigger census walk on fixture-B; assert `SourceCandidate` output scoped to fixture-B.
- Step 4 · `POST /api/opportunity_briefs/generate` for fixture-B — brief cites only fixture-B units.
- Step 5 · `POST /v1/objectives` (S1 answer) — answer cites only fixture-B trace ids; Trust Receipt at `/trace/:traceId` renders only fixture-B envelopes.

**Constraint architecture (D-6):** isolation is not gate-only — the persistence layer (Mongo queries) filters by `instance_id` at collection accessor time; the gates verify the constraint holds under adversarial cross-instance requests. Per D-6: "gates are the backstop, not the mechanism."

## §5 · De-tuning audit table

**Grep classes executed:** `RMS` · `rms_` · `Royal Media`/`royal.media` · `RMS Intelligence`/`rms.intelligence` (per Owner-dispatch instruction).

**Total raw hits:** 823 across `backend/` + `frontend/` + `docs/`.

**Aggregation by disposition class:**

| Class | Definition | Count | Execution posture |
|---|---|---|---|
| **(a) branding → instance config** | Display name, product title, HTTP header presentation. Instance-#1's config carries "RMS Intelligence". Zero user-visible change at execution close. | 20 | Move to instance-config accessor at execution |
| **(b) code / fixture identifier rename** | Live code identifiers, fixture dir + refs, function/param names. Neutral names at execution. No wire-contract mutation. | ~55 | Rename at execution (git-mv + reference updates) |
| **(c) legitimate historical — list only, byte-identical** | Mandate filenames, close reports, rulings, archived specs, published spec bundle. Standing Rule v3 preserves. | ~748 | Untouched at execution |
| **MC-E5 SHA-pinned surface** | Hits inside `backend/contracts/*.py` (14 files) OR `backend/tests/invariants/*.contract_snapshot.json` (2 files). Frozen surface — Parity 31 held byte-identical. Cannot rename without contract-schema drift. | ~4 in snapshots + ~35 in contract .py docstrings | **Escalated to Owner via MC-E5 · list-only disposition pending Owner ruling** |
| **MC-E6 live wire surface (builder-identified Tier-1)** | HTTP header names `X-RMS-App-ID` / `X-RMS-Webhook-URL` are public S1 wire; LIVE env var names `RMS_ARTIFACT_STORE_ROOT`, `RMS_G6_*`, `RMS_MTAFITI_*`, `RMS_TARGETA_*`, `RMS_NORTHENA_*`, `RMS_MEA_*`, `RMS_MASTER_ADMIN_TOKEN` etc. Renaming = wire break for integrating apps and deployed environments. | ~30 | **Escalated to Owner via MC-E6 · disposition per Owner ruling** |

### §5.1 Class-(a) branding — 20 hits (execution moves to instance config)

| # | File:line | Token | Move-to accessor |
|---|---|---|---|
| a1 | `frontend/src/pages/AskConsolePage.js:625` | `<h1>RMS Intelligence</h1>` | `instance_config.display_name` (client-hydrated) |
| a2 | `frontend/src/pages/AuthLoginPage.js:46` | "RMS Intelligence" branding text | `instance_config.display_name` |
| a3 | `frontend/src/pages/AuthRegisterPage.js:42` | "RMS Intelligence" branding text | `instance_config.display_name` |
| a4 | `frontend/src/pages/operator/OperatorHomePage.js:163` | "RMS Intelligence" | `instance_config.display_name` |
| a5 | `frontend/src/pages/operator/OperatorHomePage.js:5` | comment "Header: 'RMS Intelligence · operator'" | Comment update (tracks the accessor) |
| a6 | `frontend/src/pages/operator/CommitReviewPage.js:152` | "RMS Intelligence" | `instance_config.display_name` |
| a7 | `frontend/src/pages/operator/CommissionWizardPage.js:193` | "RMS Intelligence" | `instance_config.display_name` |
| a8 | `frontend/src/pages/compliance/ComplianceHomePage.js:112` | "RMS Intelligence · compliance" | `instance_config.display_name` + surface-role suffix |
| a9 | `frontend/src/pages/compliance/ComplianceProveOneRunPage.js:125` | "RMS Intelligence · compliance" | Same accessor |
| a10 | `frontend/src/pages/compliance/ComplianceRetentionRightsPage.js:103` | "RMS Intelligence · compliance" | Same accessor |
| a11 | `frontend/src/pages/engineer/EngineerRegisterAppPage.js:123` | "RMS Intelligence · engineer" | Same accessor |
| a12 | `frontend/src/pages/engineer/EngineerFirstCallPage.js:104` | "RMS Intelligence · engineer" | Same accessor |
| a13 | `frontend/src/pages/engineer/EngineerAdministerPage.js:61` | "RMS Intelligence · engineer" | Same accessor |
| a14 | `frontend/src/pages/master_admin/MasterAdminHomePage.js:87` | "RMS Intelligence · master admin" | Same accessor |
| a15 | `frontend/src/pages/master_admin/ChangeARulePage.js:134` | "RMS Intelligence · master admin" | Same accessor |
| a16 | `frontend/src/pages/master_admin/AuditTrailPage.js:134` | "RMS Intelligence · master admin" | Same accessor |
| a17 | `frontend/public/index.html:7` | `<title>RMS Intelligence System</title>` | `instance_config.product_title` (server-rendered or build-time) |
| a18 | `frontend/public/index.html:13` | noscript "RMS Intelligence System requires JavaScript" | Same accessor |
| a19 | `backend/core.py:28` | `APP_NAME = os.environ.get("APP_NAME", "RMS Intelligence System")` (default only) | Default becomes empty or "Akki Platform"; instance overrides via env |
| a20 | `backend/server.py:47` | FastAPI title description `"RMS Intelligence System. Doctrine names canonical: …"` | Default becomes generic; instance override via env |

Instance-#1's config file (execution artifact) carries: `display_name = "RMS Intelligence"` · `product_title = "RMS Intelligence System"`. Zero user-visible change on instance-#1 at execution close.

### §5.2 Class-(b) rename — ~55 hits

**Fixture directory + all references** (dispatch cited `rms_adversarial_v1` explicitly · SHA of fixture.json `e4d147a8ad83c26502d1b85614f9b32ab427b1103a262546400d940612250b08`):

| # | File:line | Current | Renamed |
|---|---|---|---|
| b1 | `backend/services/data_source/synthetic_assets/rms_adversarial_v1/` (dir) | `rms_adversarial_v1/` | `synthetic_estate_a/` (or `adversarial_estate_v1/` — Tier-3 default at execution) |
| b2 | `backend/services/data_source/synthetic_assets/rms_adversarial_v1/fixture.json:3` | `"fixture": "rms_adversarial_synthetic_v1"` | `"fixture": "synthetic_estate_a_v1"` (or matching Tier-3 default) |
| b3 | `backend/services/data_source/synthetic_assets/rms_adversarial_v1/rejected/fixture.incoming.json:3` | same | same |
| b4-b16 | `backend/tests/**/*.py` references (13 files enumerated in §5 grep output) | Path string `"rms_adversarial_v1"` | Match rename |
| b17 | `backend/services/system_state.py:17` | `def _rms_adversarial_v1_manifest()` | `def _synthetic_estate_a_manifest()` |
| b18 | `backend/services/system_state.py:23,55` | Manifest key `"rms_adversarial_v1"` | Match rename |
| b19 | `backend/services/data_source/real_rms.py` (module filename) | `real_rms.py` | `real_estate_adapter.py` (or Tier-3 default) |
| b20 | `backend/tests/test_rms_adversarial_v1_roundtrip.py` (filename) | same | Match |

**Comment cleanup** (retired-token references in comments · zero runtime impact):
| # | File:line | Current | Change |
|---|---|---|---|
| b21 | `backend/.env:1` | `# RMS Intelligence System — backend env.` | `# Akki Intelligence Platform — backend env.` (or Tier-3 default) |
| b22 | `frontend/.env:1` | `# RMS Intelligence System — frontend env.` | Match |
| b23 | `backend/requirements.txt:1` | `# RMS Intelligence System — backend requirements (G0).` | Match |
| b24 | `backend/tests/conftest.py:1` | `"""Pytest configuration for RMS Intelligence backend."""` | Match |
| b25 | `backend/core.py:1` | `"""RMS Intelligence System — backend core."""` | Match |
| b26 | `backend/server.py:1` | `"""RMS Intelligence System — FastAPI assembler (G0)."""` | Match |
| b27 | `backend/contracts/__init__.py:1` | `"""RMS Intelligence System — contracts package."""` | **MC-E5** — DO NOT rename; escalate |

Additional class-(b) code refs — an execution-time comprehensive grep sweeps residual references. Estimated ~15 additional refs (docstrings, tests, service files); Tier-2 disclosure at close for total actual vs. band.

### §5.3 Class-(c) legitimate historical — list only, byte-identical (~748 hits)

Enumerated top-level buckets (per Standing Rule v3 · frozen archives):
| Bucket | Path root | Approx hits | Posture |
|---|---|---|---|
| Historical mandates archive | `docs/mandates/archive/` | ~450 | Byte-identical · Standing Rule v3 |
| Rulings record | `docs/rulings/` | ~85 | Byte-identical · Standing Rule v3 |
| Close reports | `docs/close_reports/` | ~40 | Byte-identical · Standing Rule v3 |
| Audits | `docs/audits/` | ~35 | Byte-identical · Standing Rule v3 |
| Briefs (registers) | `docs/briefs/` | ~55 | Byte-identical · Standing Rule v3 |
| Governance | `docs/governance/` | ~30 | Byte-identical · Standing Rule v3 |
| Stage A proposals (historical) | `docs/stage_a_proposals/` | ~25 | Byte-identical · Standing Rule v3 |
| Requirements | `docs/requirements/` | ~5 | Byte-identical · Standing Rule v3 |
| Published spec bundle (static download) | `frontend/public/downloads/shield_engine_specs.bundle.md` | ~15 | Published historical artifact · Standing Rule v3 |
| Machine registry (yaml + supplements v0.1..v0.4 references to spec filenames) | `docs/registry/` | ~8 | Cited (not asserted) canon filenames |

**No renames, no touches.** Any drift in this bucket at execution close is a defect.

### §5.4 MC-E5 SHA-pinned surface hits — enumerated, escalated

**Inside `backend/tests/invariants/*.contract_snapshot.json` (Parity 31 seal):**
| # | File:line | Token |
|---|---|---|
| e5-1 | `service_1_refusal.contract_snapshot.json:18` | `"See RMS_Interface_Specification.md §201."` (field description) |
| e5-2 | `service_1_refusal.contract_snapshot.json:52` | `"See RMS_Interface_Specification.md §186-190, §202-203."` (field description) |
| e5-3 | `service_1_refusal.contract_snapshot.json:60` | `"See RMS_Interface_Specification.md §204-205, RMS_UX_Architecture_Specification.md §247."` (field description) |
| e5-4 | `perception_job_v0.contract_snapshot.json:45` | `"description": "Pointers into RMS estate identifying units to perceive."` |

**Inside `backend/contracts/*.py` (frozen source tier · docstrings that materialize into `model_json_schema()` descriptions):**
| # | File:lines | Nature of hit |
|---|---|---|
| e5-5 | `contracts/__init__.py:1` | Package docstring "RMS Intelligence System — contracts package." |
| e5-6 | `contracts/admission_refusal.py:4` | Spec-authority citation "RMS Product & Engineering Spec v3 §6.5" |
| e5-7 | `contracts/feasibility_result.py:4` | Spec-authority "RMS Product & Engineering Spec v3 §5" |
| e5-8 | `contracts/v2_refusal.py:6` | "past extract-for-RMS" (spec citation) |
| e5-9 | `contracts/service_1_refusal.py:8,10,12,14,18,76,86,95,96` | Multiple `RMS_Interface_Specification.md` + `RMS_UX_Architecture_Specification.md` filename citations (materialize into JSON schema field descriptions e5-1..e5-3) |
| e5-10 | `contracts/objective_request_v2.py:1,8` | "RMS Service-2" + "RMS Product & Engineering Spec v3 §3.2" |
| e5-11 | `contracts/signal_ring.py:3` | "RMS Spec §5.3" |
| e5-12 | `contracts/objective_request.py:1,3` | "RMS Service-2" + "RMS Product & Engineering Spec v2.0 §8.1" |
| e5-13 | `contracts/composed_conclusion.py:4` | "RMS Product & Engineering Spec v3 §6.2" |
| e5-14 | `contracts/perception_job_v0.py:16,56` | "Pointers into RMS estate identifying units to perceive" (materializes into e5-4) |
| e5-15 | `contracts/five_rings.py:1,3,5` | "RMS Normalized Tier schema" + "RMS Product & Engineering Spec v2.0 §5" + "the critical seam of the RMS engine" |
| e5-16 | `contracts/qualification_matrix/loader.py:3` | "RMS Product & Engineering Spec v2.0 §3.4" |
| e5-17 | `contracts/extraction_params.py:3` | "RMS Spec §5.5" |

**Disposition (builder analysis · does NOT resolve — Owner rules):** these hits fall into two sub-classes on the frozen tier:
1. **Spec-filename citations** (e5-1..e5-4 in snapshots; e5-6..e5-14, e5-16, e5-17 in contract source) — reference canonical mandate documents at `docs/mandates/archive/` (class-(c) historical, byte-identical). Renaming filenames in citations = pointer break to historical canon. Precedent: class-(c) posture.
2. **Substantive text** (e5-5, e5-8, e5-14 body, e5-15 body, e5-4 body) — "RMS Intelligence System" / "past extract-for-RMS" / "RMS estate" / "RMS engine" — organization-token as substantive prose inside frozen contracts. This IS the platform/instance identity split the dispatch's §1.4 principle targets — but on the frozen surface where Parity 31 seal prohibits mutation.

**MC-E5 escalation content follows in §6.**

### §5.5 MC-E6 live wire surface (builder-identified Tier-1)

Hits that constitute LIVE external-facing wire contracts, whose rename would break integrating applications and/or deployed environments:

| # | File:line | Nature |
|---|---|---|
| e6-1 | `backend/routers/objectives.py:52` | `X-RMS-App-ID` HTTP request header (S1 wire — integrating applications) |
| e6-2 | `backend/routers/objectives.py:53` | `X-RMS-Webhook-URL` HTTP request header (S1 wire) |
| e6-3 | `backend/routers/objectives.py:52,53,115,116,133,134` | Python param names `x_rms_app_id`, `x_rms_webhook_url` bound to those headers |
| e6-4 | `backend/services/artifact_store/adapter.py:27,57` | `RMS_ARTIFACT_STORE_ROOT` env var (LIVE deployment config; changing default = restore-drill breakage per Op. Values §9 PH-R2) |
| e6-5 | `backend/tests/invariants/test_master_admin_pending_seams.py:57-100+` (list) | Env var names `RMS_TARGETA_MIN_EFFICIENCY_GAIN` · `RMS_TARGETA_COVERAGE_ALPHA` · `RMS_TARGETA_HELD_OUT_SET_COMPOSITION` · `RMS_MTAFITI_V3_FACT_PRECISION` · `RMS_MTAFITI_V3_GENRE_ACCURACY` · `RMS_MTAFITI_V3_INTER_ANNOTATOR_FLOOR` · `RMS_NORTHENA_LEDGER_RETENTION_MODE` · `RMS_G6_K_ANONYMITY_THRESHOLD` · `RMS_G6_L_DIVERSITY_THRESHOLD` · `RMS_G6_DP_EPSILON_BUDGET` · `RMS_MEA_SOURCE_STANDING_TABLE_PATH` · `RMS_MASTER_ADMIN_TOKEN` (retired) — pending-seams governance surface tested for un-set posture |
| e6-6 | `backend/core.py:30` | `DB_NAME = os.environ.get("DB_NAME", "rms_intelligence")` — Mongo database name. Renaming = persistent data loss on any live deployment |
| e6-7 | `backend/.env:4` | `DB_NAME=rms_intelligence` — matches e6-6 |
| e6-8 | `backend/routers/master_admin.py:40`, `backend/routers/pricing.py:6` | `RMS_MASTER_ADMIN_TOKEN` / `X-RMS-Master-Admin` — RETIRED per auth-refusal registry closure; comment/grep-negative gate references only (already deprecated) |

**Builder disposition (does NOT resolve):** e6-1..e6-4 and e6-6..e6-7 are LIVE Tier-1 wire; e6-5 are LIVE deployment-config surface; e6-8 is deprecated but grep-negative gates depend on the token remaining greppable.

**MC-E6 escalation content follows in §6.**

## §6 · Tier-1 escalations (MC-E1..MC-E6)

Format precedent: `sequencing_harness_stage_a.md` §3.6 structural. Every block: Class · Options table (α/β/γ) · Builder analysis (does NOT resolve) · Reflexive R4 attest. Owner rules; builder executes on ruling.

### §6.1 MC-E1 · five_rings@v0 contact from tabular mapping · Tier-1 · Owner-anticipated

**Class:** Frozen contract (Parity 31 seal).

**Question:** Does the structured/tabular ingest surface require any mutation to `NormalizedUnit` (five_rings@v0) or its rings, or does it map cleanly onto the existing G0 shape?

**On-disk evidence (D-11 canon · SHA `5d59da2a…`):**
- `NormalizedUnit` (contracts/five_rings.py:276-308) accepts any modality via the `Modality` enum (`text · audio · video · image · composite`, line 44-59).
- `ProvenanceRing.locator` (line 113-119) is a free `Dict[str, Any]` — "text → {page:int, span:[int,int]}"; tabular units can encode `{table:str, row:int, cols:[...]}` in this dict without schema mutation.
- `ReextractionHandleRing.extraction_params` (line 220-224) is a free `Dict[str, Any]` — tabular params (delimiter, encoding, header-mode, primary key) fit here.
- `license_class` is NOT a field on `NormalizedUnit` — Op. Values §7 pairs license_class at the artifact receipt level (`OuterGateReceipt_v1`), not the unit.

**Options:**

| Option | Description | Contract impact | Sequencing cost |
|---|---|---|---|
| **α** (recommended if Owner rules) | **Zero five_rings@v0 mutation.** Tabular ingest maps `modality=text`; row-level locator encoded in `provenance.locator` dict; extraction params in `reextraction_handle.extraction_params`. License_class attaches at connector-registration layer (per §1.1), rides receipts (per Op. Values §7), never touches units directly. | None · Parity 31 held byte-identical. | Low; existing path. |
| **β** | Add a new `Modality.TABULAR` enum value. | Enum extension → JSON schema drift → snapshot re-bless → Parity 31 seal event. | Medium; snapshot bless + all downstream code accepting new modality. |
| **γ** | Add a top-level `license_class` field on `NormalizedUnit`. | Schema mutation → snapshot re-bless → Parity 31 seal event. | High; violates Op. Values §7 which pairs license at receipt level, not unit. |

**Builder analysis (does NOT resolve — options only):**
- α preserves Parity 31 and rides existing G0 flexibility. The `locator` free-dict + Modality union pattern was DESIGNED for exactly this multi-modality extension (five_rings.py:11-31 verbatim: "every field below must be able to carry audio / video / image / text cases without forcing a text-only shape").
- β adds a modality distinction where the existing text modality already carries structured content (tabular rows have text semantics). Adds cost with no clear delta over α's dict-encoded locator.
- γ inverts the layer discipline — license lives at the artifact (per Op. Values §7), not the unit; migrating to unit-level license_class is a strictly-larger scope change and re-opens Op. Values §7.

**Reflexive R4 attest (post-ruling):** New R4 row `rms.data_source.tabular_ingest_normalizes_units_zero_contract_mutation` (or the β/γ analogue) lands in v0.5 supplement §S1; parity 31 attest re-run at close; five_rings.contract_snapshot.json SHA quoted in close report.

### §6.2 MC-E2 · Instance-isolation mechanism · Tier-1 · Owner-anticipated · security boundary

**Class:** Security boundary (raw-never-egresses · own-vs-foreign scope discipline).

**Question:** How does the platform enforce cross-instance read denials on registry, ledger, keys, and census — the mechanism, not just the gate?

**On-disk evidence (D-11 canon):**
- Existing 4-code auth-refusal registry closure per Tiered-Ruling §5 (line 129: "4-code auth-refusal registry closure").
- `require_own_scope_or_deny` pattern cited in Tiered-Ruling §1.1 (line 33: "own-vs-foreign gates (`require_own_scope_or_deny` and equivalents); 4-code auth-refusal registry closure; JWT class/claim discipline").
- No `instance_id` field exists on any current Mongo collection · no current filter · no current header propagation.

**Options:**

| Option | Description | Constraint architecture (D-6) | Cost |
|---|---|---|---|
| **α** | **Constraint architecture — mandatory `instance_id` field on every persistent row + Mongo accessor helper that REFUSES to run a query without `instance_id`.** Every collection gains a compound index `(instance_id, ...)`; every accessor method requires `instance_id` as positional first arg; gates verify the constraint holds under adversarial cross-instance requests. | Persistence layer refuses cross-instance by design; gates verify the refusal. | Higher up-front; higher assurance; the D-6 "path of least resistance" is correct behavior. |
| **β** | Gate-only — accessors take optional `instance_id`; if absent, cross-instance leak; gates check every route filters correctly. | Gates carry the burden alone. | Lower up-front; higher on-going gate maintenance; correct behavior is not the default. |
| **γ** | Per-instance separate Mongo database (each instance = distinct DB name). | Isolation via database boundary; no in-app filter needed. | Instance provisioning becomes DB-provisioning; migration surface increases; PH-R2 restore-drill becomes per-instance. |

**Builder analysis (does NOT resolve):**
- α matches Registry Doctrine D-6 verbatim (SHA `9dd1cc4b…` line 92): "Constraint architecture first. Prefer designs where correct behavior is the path of least resistance; gates are the backstop, not the mechanism." Instance isolation as constraint = D-6 canonical.
- β violates D-6 in spirit (gates as mechanism, not backstop). Higher long-term gate maintenance and false-positive load per Tiered-Ruling §1.1 W1 concern.
- γ introduces DB-name multiplication; the current pattern uses a single `DB_NAME` (e6-6, e6-7 MC-E6) — a rename operation with data-migration semantics. The `instance_id` filter at accessor level (α) achieves the same isolation without DB-name multiplication and preserves single-connection Mongo topology.

**Reflexive R4 attest (post-ruling):** 6 R4 rows land in v0.5 supplement (§S3 instance-scoping enumeration). One row per surface (§3 row group `Multi-instance operability`).

### §6.3 MC-E3 · S2.onboard seam-value write path · Tier-1 · Owner-anticipated · dual-control adjacency

**Class:** Dual-control adjacency (Op. Values §6 · deletion class-C / rule-tightening delay window / etc — the five §6 seam values).

**Question:** The S2.onboard write path lands the five §6 seam values PER-INSTANCE. Op. Values §6 says two of them (class-C deletion, rule-tightening delay) have dual-control adjacency. Does the initial S2.onboard SET operation trigger dual-control, or does it establish the initial values without ceremony?

**On-disk evidence (D-11 canon · SHA `a6c4a455…` Op. Values §6, verbatim already cited §1.2 above):**
- Class-C deletion: "dual-control always" — but this bounds the deletion action, not the initial seam-value set. Ambiguity on which.
- Rule-tightening delay window: "72 hours" — this is a delay window, not a dual-control requirement per se.
- "DPO contact + the five §6 seam values, set per-instance here" (Op. Values §8) — silent on ceremony at set time.

**Options:**

| Option | Description | Precedent | Cost |
|---|---|---|---|
| **α** | **Initial set at onboarding = single-operator (S2 journey step "onboard context" happens under operator role). Subsequent CHANGES to already-set values trigger the dual-control ceremony where §6 requires it.** The onboarding write is the "before-birth" set, not a change. | Analogous to master-admin token seed (once, no dual-control) vs. rotation (dual-control). | Lower ceremony; matches "structured intake" wording of §8. |
| **β** | Initial set requires dual-control from the first act. | Higher assurance; matches "dual-control always" reading of §6 line 63 strictly. | Higher onboarding friction; may block first-day onboarding of new instances. |
| **γ** | Owner-designated seam values (deletion-class + rule-tightening) require dual-control at set; other three (objection escalation window, suspension re-review, outer-gate manual-review) are single-operator. | Mixed ceremony; matches the tiered pattern in §6 itself. | Complexity in the onboarding UX; requires per-seam-value control class. |

**Builder analysis (does NOT resolve):**
- α is the pragmatic reading — initial values are pre-birth defaults for an instance, not a change of policy. Change-detection at the write layer discriminates.
- β is the maximally-conservative reading; matches "dual-control always" strictly but blocks onboarding until two operators exist for a new instance — chicken-and-egg with instance creation.
- γ is the honest split — the tiered pattern already exists in §6 verbatim; the onboarding surface honors it at set-time by tier.

**Reflexive R4 attest (post-ruling):** R4 row `rms.backend.s2_onboard_writes_five_seam_values_dual_control_adjacent` in v0.5 supplement §S2 encodes the Owner's ruling verbatim in its promise field.

### §6.4 MC-E4 · Connector license_class defaults · Tier-1 · Owner-anticipated

**Class:** Rights posture (Op. Values §8 line 93 verbatim: "Rights posture per source: what the organization may license onward — feeds license_class at ingest") · client promise (Op. Values §7 line 77 verbatim: "License terms machine-attached to every artifact — license_class from the v1 registry rides the receipt").

**Question:** When a connector is registered without an explicit license_class (a new instance onboards a source without yet knowing its rights), what license_class default applies? The default determines what units the connector produces are legally permissible to expose in artifacts (S4 tier).

**On-disk evidence (D-11 canon):**
- Op. Values §8 requires "Rights posture per source" at onboarding time — implying the S2.onboard flow SHOULD force explicit rights posture per source.
- Op. Values §7 line 77-78: "License terms machine-attached to every artifact" — silent on default when unset.
- No `license_class` v1 registry exists on disk yet — it's referenced in §7 as "the v1 registry" (future artifact).

**Options:**

| Option | Description | Consequence for S4 surface | Fail-closed posture |
|---|---|---|---|
| **α** | **Default = `internal_only` (most-restrictive class). Any artifact derived from units with default license_class REFUSES to cross the outer gate to S4 until an operator explicitly upgrades the connector's rights posture.** | Fail-closed — no units accidentally leak into S4 without explicit rights. | Matches Shield "raw never egresses" (Tiered-Ruling §1.1). |
| **β** | Default = `unknown` — units are ingestable, but any S4 delivery attempt asks the operator to resolve rights posture before egress. | Deferred decision; operator prompted at S4 time. | Slightly slower onboarding-to-artifact-delivery; each S4 call needs a resolution. |
| **γ** | Default = `public_domain` — assumes commercially clean until proven otherwise. | Fail-open — presumes rights the platform has not verified. | Violates the honesty-grammar surface — presumption without evidence. |

**Builder analysis (does NOT resolve):**
- α is the raw-never-egresses default — a class-C deletion (§6) is dual-control precisely because default-open costs are irreversible; a license_class fail-open has the same asymmetric cost profile.
- β is the resolution-at-egress reading — matches operator ownership of the S2 journey step but shifts friction to S4 time.
- γ inverts the honesty grammar (rights presumed without evidence); no builder path recommends it under the doctrine.

**Reflexive R4 attest (post-ruling):** R4 row `rms.data_source.license_class_pairs_at_ingest` in v0.5 supplement §S1 encodes the Owner's default ruling verbatim.

### §6.5 MC-E5 · De-tuning rename touching frozen contract or SHA-pinned surface · Tier-1 · Owner-anticipated · HALT rather than re-bless silently

**Class:** Frozen wire contract (Parity 31 seal) · Standing Rule v3 mandate-archive pointer discipline.

**Question:** The de-tuning audit (§5.4) surfaces ~4 hits inside `backend/tests/invariants/*.contract_snapshot.json` and ~14 files in `backend/contracts/*.py` (35+ line hits) carrying `RMS`-tokens. Options table below covers the whole set atomically; the Owner rules the whole set with one ruling.

**Options:**

| Option | Description | Parity 31 seal | Historical canon pointers |
|---|---|---|---|
| **α** | **Class-(c) disposition — list only, byte-identical, untouched. All hits inside contracts/ + snapshots are treated as citations to historical canon (mandate filenames at `docs/mandates/archive/`) and substantive spec text that predates the platform/instance identity split. Parity 31 held.** The v0.5 supplement §S4 row `rms.detune.contract_tier_rms_tokens_preserved_class_c_historical_by_ruling` attests the ruling. | Held byte-identical. | Preserved as-cited. |
| **β** | Substantive-text edits only (e5-5, e5-8, e5-14 body, e5-15 body). Filename citations preserved. Snapshot re-bless required — Parity 31 seal event. | Broken → re-bless required · new attest cell for the bless. | Filename citations preserved. |
| **γ** | Full removal of RMS tokens from all contract source + snapshots. Snapshot re-bless required. All spec-filename citations rewritten to `mandate_v2_0_§5.md` (or similar org-agnostic). | Broken → re-bless required. | Filename citations broken — pointer discipline (Standing Rule v3) violated on the source-of-truth-side (contract file cites vs. mandate file it references). |
| **δ** | Rename the archived mandate files themselves (org-agnostic filenames). All contract citations updated in lock-step. All rulings + historical citations of these filenames sweep-updated. Snapshot re-bless. | Broken · massive rebless · historical canon touched (Standing Rule v3 violation candidate — needs explicit Owner exception). | Historical pointers broken across the entire rulings + close-report + audit corpus (~450+ hits per §5.3). |

**Builder analysis (does NOT resolve):**
- α preserves the Owner's principle — the mandates are the platform's own spec authority, cited as historical canon; treating them as class-(c) legitimate-historical extends the existing Standing Rule v3 discipline to the contract tier itself. The contracts' *code shape* is organization-agnostic (five_rings, defensibility ring, etc); only their *docstring citations* reference RMS-tokens, and those citations are the platform's own architectural history, not a customer's identity.
- β removes substantive prose but keeps citations — half-measure; requires re-bless for zero organization-agnosticism gain (the citations still say "RMS_...md").
- γ breaks the source-of-truth pointer discipline — Registry Doctrine v1.0 §3.5 line 76 (verbatim, SHA `9dd1cc4b…`): *"The Registry populates by extraction from what exists: the governor mandate documents, the rulings record, the close reports' gate rosters, and the BCR. Every Tier-1 escalation in the build already carried a 'Promise protected' line — the raw material is on disk."* The mandates ARE the source; citations to them cannot be silently rewritten.
- δ is the maximalist reading — touches Standing Rule v3 archives directly; requires explicit Owner suspension of Standing Rule v3 for the mandate-archive bucket; downstream sweep is massive (~450 historical hits) and likely violates D-7 (scope) by expanding the de-tuning phase into a historical-canon-rewrite phase.

**Reflexive R4 attest (post-ruling):** v0.5 supplement §S4 lands one R4 row per option chosen (α: preserves attest; β/γ/δ: re-bless attest + Parity delta ruling).

### §6.6 MC-E6 · Live wire surface RMS-token rename — builder-identified Tier-1

**Class:** Client-promise wire surface (external HTTP header contract) + Deployment configuration surface (env var identity across live environments).

**Question:** ~30 hits (§5.5) sit on LIVE external wire — HTTP headers `X-RMS-App-ID` / `X-RMS-Webhook-URL` (integrating-application contract) and env var names `RMS_ARTIFACT_STORE_ROOT` · `RMS_G6_*` · `RMS_MTAFITI_*` · `RMS_TARGETA_*` · `RMS_NORTHENA_*` · `RMS_MEA_*` · `RMS_MASTER_ADMIN_TOKEN` (retired) · `DB_NAME=rms_intelligence` · `X-RMS-Master-Admin` (retired grep-negative gate) — LIVE deployment config; rename = wire break for existing integrations + persistent data loss on live deployments (DB_NAME change loses the collection namespace). Options table below covers the whole set.

**Options:**

| Option | HTTP headers | Env var names | DB_NAME | Retired-token grep-negative gates |
|---|---|---|---|---|
| **α** (recommended if Owner rules) | **Dual-alias transition** — accept both `X-RMS-App-ID` AND new `X-Akki-App-ID` (or `X-Instance-App-ID`) at receiver; publish new form; deprecate old form after Owner-set window. | **Dual-alias** — accept both `RMS_*` and new `AKKI_*` (or `INSTANCE_*`) env vars; documented deprecation window. | `DB_NAME` var name unchanged; **value** stays `rms_intelligence` on instance-#1 (data preserved). New instances get new DB_NAME values. | Retired-token grep-negative gates (`test_master_admin_auth_reconciliation.py`) preserved verbatim — they test that RETIRED tokens are NOT emitted; renaming defeats the check semantics. |
| **β** | Rename all headers to organization-agnostic; break existing integrating apps at cutover. | Rename all env vars; break existing deployments at cutover. | Rename DB_NAME value (with migration script). | Update grep-negative gates to check both retired-forms. |
| **γ** | No rename — headers/env vars are class-(c) historical wire (the platform's own historical wire is its identity in this sense; instance identity travels in headers, not header names). List only. | Same. | Same. | Same. |

**Builder analysis (does NOT resolve):**
- α (dual-alias transition) is the standard wire-migration pattern; preserves backward compatibility for integrating applications and deployed environments; deprecation window managed by Owner. Highest cost is documentation + dual-code-path maintenance during the window.
- β is the cleanest end-state (single-name identity per surface) at the cost of a hard cutover; requires an announcement window managed by Owner.
- γ retains the org-token as wire identity — matches the class-(c) posture of §6.5 α option; simplest disposition. Justifies by treating live-wire tokens as historical protocol names (analogous to HTTP `X-Forwarded-For` — organizationally-flavored but industry canon).

**Reflexive R4 attest (post-ruling):** R4 rows land per-surface in v0.5 supplement §S6.

## §7 · Tier-2 disclosures (never-blocking · §12.1)

Tier-2 items surfaced during D-11 reads (disclosure-only per Tiered-Ruling §2.2 line 65: *"a band miss is a line in the close, not a halt"*):

**T2-1 · Band raw LoC projection above §4.2 split threshold** (raw 2,269 > 1,500). Pre-authorized split available at execution; single-commit-baseline (§4.1) may be attempted if execution-time delta stays inside the ratified band. Splits candidate seams named in §2. Owner round-trip NOT required.

**T2-2 · Verbatim-carrier count** (Governance §6.9). This Stage A carries ~5 distinct verbatim blocks (dispatch envelope §12; principle binding §0; capability texts §1.1-§1.4). Amortising per §6.9 within-module discipline: 5 blocks × ~15-40 LoC each = ~100-200 LoC within-module. Falls into the "over-band on the heavy side" bucket if stacked with §6.9's ~100-150 LoC baseline. Disclosure only.

**T2-3 · Rate-composition finding candidate** (Governance §6.4 line 154 precedent). At execution, the S2.onboard React page projects ~240 LoC across ~15 cells (16 LoC/cell §6.4). Given the page composes ~5 minor form-panels + 3 verify-panels + 1 submit + 1 confirmation, empirical may land -20% due to shared-state helper (`useReducer` for the multi-panel form). Watch for rate-composition finding at close; not a rate shift.

**T2-4 · No Tier-1 gate mutation** — the phase does not touch existing frozen contracts (per α options across MC-E1..E5), so pre-flight attestation per Tiered-Ruling §4.2 does not apply.

**T2-5 · D-11 pointer resolution** (already disclosed §2): dispatch's "band in raw LoC per §9" resolves to Governance §9 by precedent (four prior Owner-ratified closes cited). Op. Values §9 cited verbatim per literal dispatch instruction; Governance §9 cited as the binding LoC-verdict authority. This resolution is Tier-2 disclosure only; if Owner intended Op. Values §9 (PH-R2/R3/R4) as the LoC anchor, that is an escalation but there is no plausible reading connecting PH-R2/R3/R4 acceptance criteria to LoC-banding; the disclosure stands.

**T2-6 · rms_adversarial_v1 fixture SHA** (e4d147a8ad83c26502d1b85614f9b32ab427b1103a262546400d940612250b08) — the fixture JSON content is byte-identical across the rename (the file MOVES via `git mv`; the checksum on the JSON body content is unchanged). The `_manifest.fixture` key ("rms_adversarial_synthetic_v1") inside the JSON changes value per §5.2 b2 → fixture-body SHA drifts. Disclosure at close.

## §8 · Tier-3 silent defaults

Format per Tiered-Ruling §3.2 line 88:

- `[Tier 3 default] Fixture dir rename target → 'synthetic_estate_a'` — Owner-agnostic, extensible for future estate labels (b/c/…); avoids "adversarial" as a durable identifier since the fixture role may broaden.
- `[Tier 3 default] Instance identifier for existing single-instance state → 'instance-fixture-a'` — mirrors Owner-dispatched 'instance-fixture-B' naming; keeps CI parity.
- `[Tier 3 default] Instance config storage → Mongo collection 'instance_config' (single collection, keyed by instance_id)` — matches existing Mongo topology (single DB, multiple collections); avoids file-based per-instance JSON that would introduce a new persistence tier.
- `[Tier 3 default] Env var alias prefix for MC-E6-α dual-alias transition → 'AKKI_' (matches company name; organization-agnostic)` — pending Owner rule; may become moot if Owner rules γ (no rename).
- `[Tier 3 default] v0.5 supplement filename → 'function_promise_registry_v0.5_supplement.md'` — Governance §14 pattern per predecessor (v0.4).
- `[Tier 3 default] Close-report filename → 'multi_instance_capability.md'` — under `docs/close_reports/`, matches predecessor naming discipline (e.g. `commercial_cut_2026_07_06.md`).
- `[Tier 3 default] Ruling record filename (if execution issues a Ruling document) → 'multi_instance_capability_mc_e1_to_e6.md'` — under `docs/rulings/`, matches predecessor naming (e.g. `answer_fluency_af_e1_to_e4.md`).

## §9 · D7 fence compliance

Explicit compliance list per Owner-dispatched fences:

| Fence | Compliance mechanism |
|---|---|
| **No real customer data anywhere** | Fixture-B is generic tabular + small AV, SYNTHETIC. Data-blind posture (Governance §8) preserved. Fixture generation code is deterministic + reviewable. |
| **No hosted-shared-tenancy (instances, not tenants-in-one-deployment)** | Instances are configuration boundaries, not tenants sharing a hosted deployment. `INSTANCE_ID` scopes access; each instance's runtime is separable (env vars, config, model overrides). "Multi-instance" does NOT mean "multi-tenant on a single hosted deployment"; it means "the codebase supports being deployed as instance-A OR instance-B with configuration-only difference." Per-DB isolation option (γ under MC-E2) is available; single-DB with `instance_id` filter (α under MC-E2) is a builder recommendation, not a shared-tenancy topology. |
| **No fleet upgrade/rollout machinery beyond config isolation** | No orchestrator, no rolling-deploy tooling, no version-drift-across-instances tracker in scope. Each instance is deployed once by whatever mechanism its host uses; config isolation is the only added surface. |
| **No new perception workers** | The AV perception path (`asr_worker.py`, `diarization_worker.py`, `sample_lifecycle.py`, `job_dispatcher.py`, `stub_worker.py`) is UNTOUCHED. Structured connector produces `NormalizedUnit(modality=text)` (or composite) — the perception workers only fire for AV units, not tabular. Estate-with-AV routing rides the EXISTING perception path unchanged. |
| **Historical docs untouched (Standing Rule v3)** | §5.3 enumerates the ~748 historical hits; §5's disposition-class (c) states "untouched". No `docs/mandates/archive/`, no `docs/rulings/`, no `docs/close_reports/`, no `docs/audits/`, no `docs/briefs/` (v1.0, v1.1 · v1.2 remains), no `docs/governance/` files are proposed for edit. v1.2 → v1.3 amendment (§7) is an ADDITIVE new file, not a mutation of v1.2. |

## §10 · D-11 canon-before-ruling attest

Files read on-disk before drafting this Stage A, with SHA-256:

| File | SHA-256 | Lines cited verbatim in §1..§9 |
|---|---|---|
| `docs/requirements/operating_values_v1.md` | `a6c4a455175ef37dc71362aea2e41b2ce406baaf9a1c77b3f0f1326e0aa608ee` | §8 (lines 85-97) · §9 (lines 99-105) · §6 (lines 61-71) · §7 (line 77) |
| `docs/governance/registry_doctrine_v1.md` | `9dd1cc4bee310ad36780d182377ae8f3e25b7a681430c982dda18d76a408fbcf` | D-6 (line 92) · D-11 (line 97) · §3.5 (line 76) · §3.2 (lines 44-58) · §S2 (line 33) |
| `docs/governance/tiered_ruling_model.md` | `187ad8ee6764956a88167b38c6a904c4c43074f6804ee396f627bc2da9a55dbc` | §9 (lines 249-251) · §1.1 (line 33) · §2.2 (line 65) · §3.2 (line 88) · §6.9 (lines 188-200) · §6.10 (lines 202-213) · §6.11 (lines 215-226) · §8 (line 240) · §14 (line 334) |
| `backend/contracts/five_rings.py` | `5d59da2a077d55f777d88df9ae09bd1ee0f21481fd0d6af3bd5ed9b76fd3c01e` | Lines 11-31 (multimodal discipline) · 44-59 (Modality) · 113-119 (locator) · 220-224 (extraction_params) · 276-308 (NormalizedUnit) |
| `backend/contracts/qualification_matrix/loader.py` | `eef3135e4fc2dcfac8c430e5f13f11d7ac40d5cb627ec75a33ef9264eaf0ab83` | Lines 1-14 (spec authority) |
| `backend/contracts/objective_request.py` | `2588c735356fd096f10726b5a052b8af54172fec0c46f75a62767040aeca1ef1` | Lines 1-14 (spec authority + cousin substrate) |
| `backend/contracts/objective_request_v2.py` | `e20956c5c3751180e9b69fed08a8738c0cdeed3d86aaa0db604f3ef932f2e994` | Lines 1-15 (spec authority) |
| `backend/services/synisense/shield/tenant_entities.py` | `27c6fa20dcae4d6256dfee0998bfcc9d9c42070b9f031fa643b3ad8e8fc13ab0` | Lines 1-36 (IF-1 stub · S2.onboard write target) |
| `backend/services/mtafiti/census.py` | `53110a1dd178d5201542d04f2627dbc38f46c00c1aa6d548c72b000fb61d19aa` | Lines 1-46 (composition discovery seam) |
| `backend/services/mtafiti/registry.py` | `134bfbd05708f74e1a2455e124e78785480adfc81697c9d26dfb9225f57ba919` | Read for scope · not verbatim-cited |
| `backend/services/perception/models_registry.v0.json` | `291de8ed6cdd45951dfe424ad7dac68275f3cec332fa2bc0d68e21b26340513c` | Lines 1-20 (verbatim Owner ruling on empty-registry seed correction) |
| `frontend/src/pages/AskConsolePage.js` | `7704e57b13c6529648d040c10b18fd5509b60e033d6999696e2d56c11eb7c851` | Lines 620-635 (branding location · §5.1 a1) |
| `backend/services/data_source/synthetic_assets/rms_adversarial_v1/fixture.json` | `e4d147a8ad83c26502d1b85614f9b32ab427b1103a262546400d940612250b08` | Fixture header (§5.2 b2) |
| `docs/stage_a_proposals/sequencing_harness_stage_a.md` | `95f9274edad69d3abe7e505aeb1705c5e320638b0d0b6c81d2a9b2a6d81c850f` | Line 1 (D7 UNSANCTIONED PRE-WORK marker · structure reference) |
| `docs/briefs/outstanding_work_and_gap_register_v1.2.md` | `b8b45d2424ecfcce5f84593b1f6142104d734fb805c3e6b132b4e9953e72c90b` | Predecessor register · §6 OD-1 pre-resolution status |
| `docs/rulings/g10_g7_promote_2026-07-14.md` | `03774901a4e56869d50a8551b9987a6fcb302735fbb9aa108768ef3da59031d3` | Predecessor atomic-commit ruling · one-atomic-commit standard |

Grep-audit commands executed (§5 evidence):
```
grep -RIn 'RMS' backend/ frontend/ 2>/dev/null → 823 hits across live tree
grep -RIn 'RMS' docs/ (filtered per dispatch exclusions) → cross-checked
grep -RIn 'rms_' backend/ frontend/ 2>/dev/null → enumerated in §5.2 + §5.5
grep -RIn 'Royal Media\|royal.media' → 6 hits, all class-(c) historical
grep -RIn 'RMS Intelligence\|rms.intelligence' → live-source only; 20 hits enumerated in §5.1
grep -RIn 'RMS' backend/tests/invariants/*.contract_snapshot.json → 4 hits enumerated §5.4 e5-1..e5-4
grep -RIn 'rms_' backend/tests/invariants/*.contract_snapshot.json → 0 hits
```

**D-11 posture attest:** every verbatim excerpt in §1..§9 is quoted from the on-disk file at the SHA listed above at the time of Stage A drafting. Zero content is recalled from LLM memory or summary. Where the dispatch's pointer ("Op. Values §9") did not match on-disk structure (Op. Values §9 = PH-R2/R3/R4, not LoC), the mismatch is disclosed in §2 and Tier-2 §T2-5; the LoC-verdict discipline anchors at Governance §9 per unanimous ratified precedent.

## §11 · Sequencing anchor (Owner verbatim)

> Sequencing after this close: G-2 (Registry maintenance) then G-3 (Operating Values v1.1), folding this phase's rows and the instance-#2 reality in one pass.

**Consequence:** the v0.5 supplement's ~20 R4 rows and the register v1.3 amendment feed the next Owner-dispatched G-2 turn. Op. Values v1.1 (G-3) will fold the instance-#2 reality (per this phase's ratified rulings) into the seam-value + model-registry decisions.

## §12 · Owner dispatch envelope (verbatim)

===== BEGIN OWNER DISPATCH (verbatim) =====

IF-1 reconciliation + G-10/G-7 promote close: ACKNOWLEDGED. Full sweep green (1,241 + 0 failed), triad root-caused and fixed, trace surface public at /trace/:traceId, register at v1.2 — G-7, G-10, G-13 closed; OD-2, OD-6 discharged. Clean.

OD-1 (S2.onboard build timing): RESOLVED BY CONSEQUENCE — the Owner has ordered instance-#2 capability, which cannot onboard without S2.onboard; the surface builds in the phase dispatched below. Record the resolution in the next register touch (v1.2 → v1.3 rides this phase's close).

Dispatch — Multi-Instance Capability Stage A + RMS de-tuning. One phase, standard loop: Stage A → verbatim relay of Tier-1s → rulings → execution → close.

Principle binding the whole phase: the platform is organization-agnostic; the estate's contents — never the customer's identity — decide which capabilities do work. Instance identity lives in configuration; platform code, contracts, and vocabulary carry no organization.

Scope — four capabilities, one platform, zero parallel engines:

Structured-source connector class: generic tabular/DB ingestion → NormalizedUnits through the existing intake path — same unit grammar (who/what/when/where/class), provenance-paired, license_class at ingest, census discovering composition. Fixture shapes may be informed by real catalogues on hand; no organization's name, schema, or assumptions enter code, contracts, or vocabulary — per §8, the platform learns each estate at census, never before. Estates with AV route through the existing 9.2a perception path unchanged; no new perception work rides this phase.

S2.onboard surface — first consumer: structured intake per Operating Values §8 verbatim (estate inventory, org vocabulary, rights posture per source, DPO + the five seam values per-instance, objective priorities), versioned, feeding connector registration and the tenant-entity seat the IF-1 stub reserved.

Multi-instance operability v1: one codebase, per-instance configuration isolation — instance-scoped seam values, estate inventory, model-registry entries, connector registrations, and (per item 4) instance identity. Proof shape: a second synthetic instance — instance-fixture-B, a generic structured estate (tabular + small AV, synthetic) — stands up beside the existing fixture estate in CI and walks onboard → connect → census → brief → answer end-to-end, with isolation cells proving no cross-instance read on any surface (registry, ledger, keys, census).

RMS de-tuning — the platform/instance identity split. Stage A includes an audit section: enumerate every organization-specific token in live code, config, contracts, fixtures, routes, and UI copy (grep classes: RMS, rms_, Royal Media, broadcaster-specific strings; e.g. the Ask Console's "RMS Intelligence" branding, the rms_adversarial_v1 fixture directory name). Classify each: (a) branding → instance config (display name, product title, headers move to the instance-config surface item 3 creates; instance #1's config carries "RMS Intelligence"); (b) rename (org-token identifiers in live code/fixtures get neutral names); (c) legitimate historical (mandate filenames, close reports, rulings — Standing Rule v3, byte-identical, untouched; list only). Execution applies (a) and (b); the platform ends this phase with zero organization identity outside instance config and historical canon.

Expected Tier-1 surfaces (pre-named): any five_rings@v0 contact from tabular mapping (expect additive-sidecar; Tier-1 if touched) · instance-isolation mechanism (security boundary) · S2.onboard seam-value write path (dual-control adjacency) · connector license_class defaults · any de-tuning rename touching a frozen contract or SHA-pinned surface (Tier-1; expect none — HALT rather than re-bless silently).

D7 fences: no real customer data anywhere; no hosted-shared-tenancy work (instances, not tenants-in-one-deployment); no fleet upgrade/rollout machinery beyond config isolation; no new perception workers; historical docs untouched.

Stage A returns: band in raw LoC per §9 · the de-tuning audit table (token → class → disposition) · R4 rows per §14 supplement pattern · escalations pre-tiered · verbatim relay for Tier-1s.

Sequencing after this close: G-2 (Registry maintenance) then G-3 (Operating Values v1.1), folding this phase's rows and the instance-#2 reality in one pass.

===== END OWNER DISPATCH (verbatim) =====

═══════════════════════════════════════════════════════════════════

*End of Multi-Instance Capability Stage A proposal. Six Tier-1 escalations (MC-E1..MC-E6) relayed verbatim in the reply body per Tiered-Ruling §4.4. No execution this turn. Awaiting Owner rulings before atomic-commit dispatch. Standing Rule v3 · on-disk canonical.*
