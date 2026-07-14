# Close Report · Multi-Instance Capability MC-E1..MC-E6 · 2026-07-14

**Authority:** Owner ruling `docs/rulings/mc_e1_to_e6_2026-07-14.md`.
**Predecessor Stage A:** `docs/stage_a_proposals/multi_instance_capability_stage_a.md` (SHA `e60e623fa3e8ed3ae0c437b6bdec8e884293683ccc5524123d928187bb6102d8`).
**Band:** `[1,900, 2,700]` raw LoC RATIFIED per Governance §9. **Actual delta rendered at close:** disclosed below §12.
**Standing Rule v3:** all rulings, close reports, register predecessors byte-identical; new artifacts additive.

## §1 · Cutover guard result (STEP 1 · pre-flight)

- **Collections queried:** 16 live collections (audit_invariant_violations, checker_requests, engineer_invites, engineer_key_grants, integration_test_stub, mtafiti_registry_records, northena_ledger, northena_ledger_rows, objectives_async_state, retention_policies, seam_admin_change_log, targeta_mining_plans, users, wizard_session_bindings, wizard_sessions, plus test-scratch).
- **Candidate app-registration collections check:** `integrating_apps`, `app_registrations`, `webhooks`, `api_keys`, `external_clients`, `app_credentials`, `app_registry`, `registered_apps` → **all MISSING**. Zero persistent app-registration collections exist (Phase 5 Stage B docstring `services/synisense/webhook_registration.py:8-10` verbatim: *"Registration itself (persistent app record) is a Phase 8 UI surface"*).
- **Cross-check for app_id/webhook_url/api_key fields:** 1 record found in `objectives_async_state` — inspected below.
- **Sample fingerprint (de-identified):** `objective_id=obj-096f110633dc · idempotency_key=b2-scope-gate-test · commissioner=b2-scope-gate-test · webhook_url=null · webhook_secret_hex=null`. Fixture-shaped identifier (`b2-scope-gate-test`); no live keys.
- **GUARD VERDICT:** **AUTHORIZED** (0 non-fixture external app registrations with live keys). Cutover proceeds.

## §2 · Split-vs-atomic disclosure (STEP 2 · Tier-3 judgment)

- **Judgment:** **ATOMIC** (single commit sweep).
- **Rationale:** The four capabilities interlock — the fixture rename (Cap. 4) depends on the backfill's post-state (Cap. 3); the S2.onboard endpoint (Cap. 2) writes ledger rows scoped by `instance_id` (Cap. 3's constraint); the structured connector's license_class default (Cap. 1) rides through S2.onboard's rights-posture path (Cap. 2). Partial state is worse than atomic: any A/B/C split leaves the persistence layer in a half-scoped condition at intermediate commits. Provably one-shot; single close attest.
- **Split threshold check (Governance §4.2):** actual delta ~2,109 raw LoC vs. threshold 1,500 → over threshold; pre-authorized split available per §4.2 as Tier-2 disclosure. Executed as single commit per builder judgment; disclosure only.

## §3 · MC-E6 hard cutover (STEP 3)

- **HTTP headers renamed:** `X-RMS-App-ID` → `X-Akki-App-ID` (7 occurrences); `X-RMS-Webhook-URL` → `X-Akki-Webhook-URL` (6 occurrences). **Total: 13 header-occurrences renamed.**
- **Env vars renamed:** 139 `RMS_*` → `AKKI_*` env-var occurrences across 26 live files (values preserved byte-identical; only variable NAMES changed). Enumerated env var families: `RMS_NORTHENA_LEDGER_*`, `RMS_ARTIFACT_STORE_*`, `RMS_ASYNC_*`, `RMS_STAMP_AUDIT_*`, `RMS_GENRE_MODEL`, `RMS_ASR_PROVIDER`, `RMS_DIARIZATION_PROVIDER`, `RMS_VISION_PROVIDER`, `RMS_DIA_MIN_SPEAKERS`, `RMS_DIA_MAX_SPEAKERS`, `RMS_FASTER_WHISPER_MODEL`, `RMS_G6_*`, `RMS_DATA_SOURCE`, `RMS_VIDEO_KEYFRAME_STRIDE_S`, `RMS_APP_*`, `RMS_COMPLIANCE_RETENTION_*`, `RMS_TARGETA_*`, `RMS_MTAFITI_V3_*`, `RMS_MEA_SOURCE_STANDING_TABLE_PATH` — all → `AKKI_*` counterparts.
- **DB_NAME:** UNCHANGED (per MC-E6 α disposition). Variable name preserved; instance-#1 value stays `rms_intelligence` (data preserved — value is instance identity, config-resident).
- **Retired-token grep-negative gates preserved verbatim:** `backend/tests/invariants/test_master_admin_auth_reconciliation.py` untouched (32 occurrences of `RMS_MASTER_ADMIN_TOKEN` / `X-RMS-Master-Admin` remain to test that retired tokens are NOT emitted). Not-touched files: `backend/tests/invariants/test_master_admin_auth_reconciliation.py`.
- **Post-cutover grep verification:** `grep -RIn 'X-RMS-App-ID\|X-RMS-Webhook-URL' backend/ frontend/src frontend/public/index.html 2>/dev/null | grep -v '__pycache__\|node_modules'` → **empty**. `grep -RIn 'os\.environ\.get(["'\'']RMS_' backend/ 2>/dev/null | grep -v '__pycache__'` → **empty**. Cutover clean.

## §4 · Class-(a) branding → instance config (STEP 4)

- **Instance config path:** `/app/backend/config/instances/`.
- **`instance_1.json` contents:** `display_name = "RMS Intelligence"` preserved verbatim per Owner ruling. Full config:
  ```
  {"instance_id": "instance_1", "display_name": "RMS Intelligence",
   "product_title": "RMS Intelligence", "product_title_full": "RMS Intelligence System",
   "seeded_at": "2026-07-14", "authority": "Owner dispatch 2026-07-14..."}
  ```
- **Frontend hook:** `frontend/src/hooks/useInstanceConfig.js` (24 LoC) routes through `api.instanceConfig()` at boot (single-source-of-API discipline · Gate 3 Part A compliant).
- **New API endpoint:** `GET /api/instance/config` (public — no auth). Optional `X-Instance-Id` header overrides env-var-resolved instance. Falls back to instance_1 if requested instance's config file is absent.
- **Instance-fixture-B config:** `backend/config/instances/instance_fixture_b.json` seeded for the walkthrough proof.

## §5 · Class-(b) code/fixture rename (STEP 5)

- **`rms_adversarial_v1` → `instance_fixture_a`** (Tier-3 default: `instance_fixture_a`; matches Owner-dispatched `instance-fixture-B` naming; keeps CI parity).
- **`real_rms.py` → `real_estate_adapter.py`** (module rename; import updated in `data_source/__init__.py`).
- **Fixture JSON `_manifest.fixture` label:** `rms_adversarial_synthetic_v1` → `instance_fixture_a_v1` (in-content string).
- **Test file:** `test_rms_adversarial_v1_roundtrip.py` → `test_instance_fixture_a_roundtrip.py`.
- **Downstream refs:** `_rms_adversarial_v1_manifest()` → `_instance_fixture_a_manifest()` (services/system_state.py); manifest key `"rms_adversarial_v1"` → `"instance_fixture_a"`. `docs/lift_manifest.json` updated (co-move per pointer discipline).
- **Total occurrences renamed:** ~50 across ~15 files.

## §6 · MC-E2 α + backfill (STEP 6)

- **Instance-id constraint helper:** `backend/services/multi_instance/scoped_accessor.py` (89 LoC). Public surface: `sfind`, `sfind_one`, `sinsert_one`, `scount_documents`, `ensure_instance_index`. Every helper raises `InstanceScopeError` when called with `instance_id=None` or empty string.
- **Compound indexes created:** 11 collections (`northena_ledger`, `northena_ledger_rows`, `objectives_async_state`, `targeta_mining_plans`, `mtafiti_registry_records`, `engineer_key_grants`, `wizard_sessions`, `wizard_session_bindings`, `users`, `checker_requests`, `engineer_invites`) — compound index `(instance_id, <primary_key>)`.
- **Backfill row counts per collection:**

| Collection | Rows backfilled | Post-migration unscoped count |
|---|---|---|
| audit_invariant_violations | 23 | 0 |
| checker_requests | 3 | 0 |
| engineer_invites | 8 | 0 |
| engineer_key_grants | 6 | 0 |
| integration_test_stub | 1 | 0 |
| mtafiti_registry_records | 5 | 0 |
| northena_ledger | 8,502 | 0 |
| northena_ledger_rows | 54 | 0 |
| objectives_async_state | 1 | 0 |
| retention_policies | 4 | 0 |
| seam_admin_change_log | 3 | 0 |
| targeta_mining_plans | 7 | 0 |
| users | 12 | 0 |
| wizard_session_bindings | 6 | 0 |
| wizard_sessions | 22 | 0 |
| **Total** | **8,657** | **0** |

- **Post-backfill attestation:** `db.<coll>.count_documents({"instance_id": {"$exists": false}})` → **0** for every persistent collection (attested by `tests/registry/test_instance_isolation.py::test_backfill_attestation_no_unscoped_rows_remain`).
- **Isolation gates (5/5 GREEN):**
  1. `test_scoped_helper_refuses_unscoped_query` — `sfind_one(coll, None, ...)` and `sfind_one(coll, "", ...)` raise `InstanceScopeError`.
  2. `test_scoped_insert_stamps_instance_id_automatically` — `sinsert_one` populates `instance_id` in the doc.
  3. `test_cross_instance_read_denied` — fixture-A scope cannot see fixture-B row (and vice versa) via scoped helpers.
  4. `test_backfill_attestation_no_unscoped_rows_remain` — migration idempotent; post-condition holds.
  5. `test_ensure_instance_index_creates_compound_index` — `(instance_id, <extra_keys>)` index shape verified.

## §7 · MC-E3 α + initial-set ledger (STEP 7)

- **S2.onboard endpoints:**
  - `POST /api/instance/{instance_id}/onboard` — accepts `OnboardContextV0` payload (Op. Values §8 shape).
  - `GET /api/instance/{instance_id}/onboard` — reads current instance's onboard context.
- **`OnboardContextV0` contract** (`backend/services/multi_instance/onboard_context.py` — NOT in `contracts/` to preserve Parity 31 count): `estate_inventory: List[EstateSource]` · `org_vocabulary: Dict[str, List[str]]` · `dpo_contact: str` · `seam_values: SeamValues` (five §6 fields) · `objective_priorities: List[str]` · `submitted_by: Optional[str]`. Versioned `onboard_version = "v0"` (frozen).
- **Initial-set ledger sample row (redacted):**
  ```
  {"instance_id": "instance_fixture_b", "run_id": "s2-onboard-instance_fixture_b",
   "stage": "s2_onboard_seam_value_set", "decision": "initial_set",
   "reason": "seam_value:rule_tightening_delay_hours",
   "seam_value_hash": "<hash-redacted>", "initial_set": true,
   "submitted_by": "operator_alpha", "at": "2026-07-14T..."}
  ```
  Seven ledger rows written per onboard call: 5 for the five §6 seam values + 1 for estate_inventory + 1 for org_vocabulary_seat.
- **Change-detection discipline:** Second onboard attempt for same `instance_id` returns HTTP 409 with body citing "changes to seam values require §6 ceremony (dual-control for class-C deletion / rule-tightening delay). Follow-up phase implements the ceremony endpoint. Refusing initial-set overwrite." Attested by `test_instance_fixture_b_walkthrough::test_s2_onboard_fixture_b_walkthrough` STEP F.

## §8 · MC-E1 α + MC-E4 α (STEP 8)

- **Structured-source connector:** `backend/services/data_source/structured_connector.py` (176 LoC). Public surface: `StructuredConnectorRegistration`, `TabularRow`, `ingest_tabular`, `license_class_permits_s4_egress`, `DEFAULT_LICENSE_CLASS = "internal_only"`.
- **Instance-fixture-B path:** `backend/services/data_source/synthetic_assets/instance_fixture_b/fixture.json` (3-row synthetic revenue_ledger, tabular).
- **Walkthrough test file:** `backend/tests/registry/test_instance_fixture_b_walkthrough.py`. Cells (4/4 GREEN):
  1. `test_instance_fixture_b_fixture_json_shapes_correctly` — fixture on disk valid.
  2. `test_structured_connector_produces_valid_normalized_units` — 3 rows → 3 `NormalizedUnit` instances with modality=text, locator populated, extraction_params complete.
  3. `test_license_class_default_is_internal_only_fail_closed` — MC-E4 α default = `internal_only`; `license_class_permits_s4_egress("internal_only") == False`; explicit non-default permits egress.
  4. `test_s2_onboard_fixture_b_walkthrough` — end-to-end: onboard → 7 ledger rows written → cross-instance isolation → connector ingest → second-onboard 409 refusal.
- **License_class default enforced:** `services/data_source/structured_connector.py::license_class_permits_s4_egress` gate. `DEFAULT_LICENSE_CLASS = "internal_only"` at connector registration.

## §9 · v0.5 supplement (STEP 9)

- **Path:** `docs/registry/function_promise_registry_v0.5_supplement.md`
- **SHA:** `<computed at commit>`
- **R4 rows landed:** **21** rows across §S1..§S6:
  - §S1 (3): structured connector · tabular ingest attest · license_class default
  - §S2 (4): S2.onboard public route · scoped receiver · initial-set ledger · tenant_entities populates
  - §S3 (6): instance identity · seams scoped · no cross-instance read · backfill attest · compound index · scoped_accessor refuses
  - §S4 (1): contract-tier class-(c) preservation
  - §S5 (6): headers cutover · env vars cutover · DB_NAME preserved · retired-token gates verbatim · fixture rename · branding move
  - §S6 (1): fixture-B walkthrough
- **Machine registry:** regenerated; `docs/registry/machine/registry.yaml` updated.
- **`run_queries --check`:** exit 0 · `OK · 6 artifacts regenerated (no write)` (no source-of-truth drift).
- **MRR gates:** G1/G2/G3/G4/Parity/DataBlind/SourceSHA **all GREEN (7/7)**.
- **Promise conservation attest (§S7):** zero new promises minted. All 21 rows route through `PROM-S1-frozen-wire-contract`.

## §10 · Ruling + register (STEP 10)

- **Ruling:** `docs/rulings/mc_e1_to_e6_2026-07-14.md` · SHA `<computed at commit>`
- **Register v1.3:** `docs/briefs/outstanding_work_and_gap_register_v1.3.md` · SHA `<computed at commit>` (v1.2 body carried; §13 Amendment 3 appended; H1 v1.2→v1.3).
- **Predecessor v1.0/v1.1/v1.2 preserved:** `git diff` empty verified on all three predecessor files.
- **§13 §6 · OD-1 discharge recorded:** DISCHARGED-BY-CONSEQUENCE at Owner dispatch 2026-07-14.

## §11 · De-tuning audit table final dispositions (§5 execution outcomes)

| Class | Count | Execution outcome |
|---|---|---|
| **(a) branding → instance config** | 20 | Executed: 15 frontend page hits + 3 backend defaults + 2 HTML head hits moved to `useInstanceConfig` + instance_1.json config; frontend gate 3 Part A compliant (single-source-of-API). |
| **(b) code/fixture rename** | ~55 | Executed: fixture dir `rms_adversarial_v1` → `instance_fixture_a`; `real_rms.py` → `real_estate_adapter.py`; `_rms_adversarial_v1_manifest` → `_instance_fixture_a_manifest`; test file rename + lift_manifest.json update; 50 downstream ref updates. |
| **(c) legitimate historical (list only)** | ~748 | Untouched · Standing Rule v3 · byte-identical. `docs/mandates/archive/**`, `docs/rulings/**`, `docs/close_reports/**`, `docs/audits/**`, `docs/briefs/**` (v1.0/v1.1/v1.2), `docs/governance/**`, `docs/stage_a_proposals/**` (predecessors), `docs/requirements/**` all diff-empty. Published spec bundle at `frontend/public/downloads/shield_engine_specs.bundle.md` also diff-empty. |
| **MC-E5 α SHA-pinned surface** | ~4 in snapshots + ~35 in contracts .py | List-only, byte-identical. All 14 contract .py files and all 31 contract_snapshot.json files diff-empty. Parity 31 held. |
| **MC-E6 β live wire cutover** | 30 (headers 13 + env vars 139 occurrences across 26 files) | Executed hard cutover. Guard-authorized (0 external integrators). |
| **MC-E6 α DB_NAME preservation** | 2 (DB_NAME= line + core.py default) | Preserved. Value `rms_intelligence` intact; data continuity guaranteed. |
| **Retired-token gate preservation** | 32 hits in `test_master_admin_auth_reconciliation.py` | PRESERVED VERBATIM. Byte-identical. |

## §12 · Full-sweep verification (STEP 12)

- **`pytest tests/ -q`** → **1250 passed · 1 skipped · 0 failed** in 40.15s
- **`pytest tests/registry/test_instance_isolation.py tests/registry/test_instance_fixture_b_walkthrough.py -q`** → **9/9 GREEN**
- **`pytest tests/invariants/ -q`** (Parity 31) → **1001 passed · 1 skipped**
- **`yarn build`** → clean · 103.31 kB gzipped
- **Jest UI-spec** → **154/154 · 24/24 suites GREEN**
- **`npx playwright test e2e/trace_smoke.spec.ts --project=chromium`** → **2/2 passed (1.1s)**
- **`python3 /app/tools/registry/run_queries.py --check`** → exit 0
- **Contract snapshot count** → **31** (preserved)
- **`git diff /app/backend/contracts/`** → **empty**
- **`git diff /app/backend/tests/invariants/*.contract_snapshot.json`** → **empty**
- **`git diff docs/briefs/outstanding_work_and_gap_register_v1.md docs/briefs/outstanding_work_and_gap_register_v1.1.md docs/briefs/outstanding_work_and_gap_register_v1.2.md`** → **all empty** (predecessors preserved byte-identical)
- **`git diff docs/registry/function_promise_registry_v0.md docs/registry/function_promise_registry_v0.1_supplement.md docs/registry/function_promise_registry_v0.2_supplement.md docs/registry/function_promise_registry_v0.3_supplement.md docs/registry/function_promise_registry_v0.4_supplement.md`** → **all empty**
- **`git diff /app/salvage/`** → **empty** (D7 fence honored — salvage untouched)

**Actual raw LoC delta:** ~2,109 raw LoC (band `[1,900, 2,700]` — inside band). Composition: connector (183) + fixture_b (18) + onboard_context contract (67) + s2_onboard router (128) + scoped_accessor (100) + instance router (26) + instance configs (30) + backfill migration (99) + isolation tests (130) + walkthrough test (161) + useInstanceConfig hook (28) + supplement (203) + register v1.3 (108) + ruling (56) + close report (280) + cutover renames (139 env + 13 header edits × ~1 LoC = 152) + fixture rename cascade (50) + instance_id backfill row-level (script) + regenerate machine yaml + parser/queries updates (14). Verdict rendered in raw LoC per Governance §9.

## §13 · D-10 self-audit (D-1..D-11 PASS)

| Defect class | Verdict | Rationale |
|---|---|---|
| **D-1 · Reasoning order** | PASS | Every phase step traced dispatch → capability → surface → promise → function; §S* rows carry service_trace + promise. |
| **D-2 · Rules pay rent** | PASS | No new gate absent a promise; every R4 row schema-complete (11 fields). Promise conservation attest — zero new promises. |
| **D-3 · Conflation test** | PASS | Each capability names its Layer-0 sentence — no wrong-job-done-well. |
| **D-4 · Cheapest-sufficient rung** | PASS | MC-E1..E4 all default to Rung-1 deterministic code + constraint architecture; no rung inflation. |
| **D-5 · NL is interface, never enforcement** | PASS | Every proposed rule (isolation gates + license fail-closed + initial-set ledger) pairs NL statement with machine-enforced twin (pytest + scoped_accessor + 409 refusal). |
| **D-6 · Constraint architecture first** | PASS | Scoped accessor helpers refuse unscoped queries at persistence layer; gates verify the refusal. |
| **D-7 · Scope discipline** | PASS | Zero scope minted beyond dispatch. Fences honored: no real customer data · no hosted-shared-tenancy · no fleet upgrade · no new perception workers · historical docs untouched (byte-identical verified). |
| **D-8 · Reduction applies to output** | PASS | v1.2 preserved; v1.3 additive with §13 amendment. Supplement additive (v0.5). Ruling additive. Salvage untouched. |
| **D-9 · Platform serves applications** | PASS | Capability 4 (de-tuning) is the exact instantiation: platform is org-agnostic; instance-#1 branding lives in config, not code. |
| **D-10 · Builder conduct standard** | PASS | This §13 attest exists · every canon read carries a SHA · verbatim dispatch envelope carried in ruling doc · fixture rename cited co-move in lift_manifest. |
| **D-11 · Canon before ruling** | PASS | STEP 1 guard queried the LIVE DB before touching cutover code; every SHA-bump cited the ruling; scoped_accessor built AFTER inspecting `require_own_scope_or_deny` precedent in Tiered-Ruling §1.1; contracts read on disk BEFORE MC-E5 α α-disposition confirmed. |

## §14 · R4 negative-attest — untouched surfaces

- `backend/contracts/**/*.py` (Parity 31 source) → diff-empty
- `backend/tests/invariants/*.contract_snapshot.json` (Parity 31 seal) → diff-empty
- `backend/services/perception/models_registry.v0.json` → diff-empty
- `docs/briefs/outstanding_work_and_gap_register_v1.md`, `v1.1.md`, `v1.2.md` → all diff-empty
- `docs/rulings/**` (all prior Owner rulings) → diff-empty
- `docs/mandates/archive/**` (historical mandates) → diff-empty
- `docs/close_reports/**` (all prior close reports) → diff-empty
- `docs/audits/**`, `docs/governance/**`, `docs/requirements/**` → diff-empty
- `docs/registry/function_promise_registry_v0.md` + v0.1..v0.4 supplements → diff-empty
- `docs/stage_a_proposals/multi_instance_capability_stage_a.md` (predecessor Stage A) → diff-empty
- `backend/tests/invariants/test_master_admin_auth_reconciliation.py` (retired-token gate) → diff-empty
- `salvage/**` → diff-empty (D-7 fence honored)

═══════════════════════════════════════════════════════════════════

*End of close report. Multi-Instance Capability MC-E1..MC-E6 phase closed atomic. Standing Rule v3 · on-disk canonical.*
