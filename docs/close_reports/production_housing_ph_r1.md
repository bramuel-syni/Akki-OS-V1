# §3.4 Production Housing PH-R1 — Close Report

**Close:** 2026-07-10 · atomic execution commit per Owner rulings PH-E1 α + PH-E2 α + PH-E3 α + PH-E4 α + documentation-addition + `/api/system/build_info` enhancement promotion · band `[900, 1,700]` RATIFIED.
**Basis:** Stage A `/app/docs/stage_a_proposals/production_housing_ph_r1.md` · SHA `4c456c29a09b0c20b3920654028e26f23e0aae3aa3af96df9c824f63938d5461`.
**Rulings:** `/app/docs/rulings/production_housing_ph_r1_ph_e1_to_e4.md`.
**Governance:** 3-tier ruling model · §9 metric-verdict-in-raw-LoC · §12 close-ratification-on-own-text · §12.1 remaining-gates enumeration.
**Standing Rule v3:** on-disk canonical.

---

## §1. Ratification posture (§12 self-ratifying · Owner 2026-07-10)

Per governance §12 (Owner 2026-07-10 verbatim): *"A close whose named gates are green and whose rulings are attested as applied ratifies on its own text. Post-close evidence questions are permitted only where a specific Tier-1 gate is alleged defective, with the allegation named. Conditions attach at ruling time, never at close time. No conditional ratifications on meta-evidence."*

Three criteria evaluated at close-landing:

- **(a) Named gates green:** YES — PH-G1..PH-G6 + auxiliary all pass. See §3.
- **(b) Rulings + Owner-addition + enhancement attested as applied:** YES — PH-E1 α + PH-E2 α + PH-E3 α + PH-E4 α + PH-E4 documentation-addition + `/api/system/build_info` all encoded in source + tests + docs. See §2.
- **(c) No new Tier-1 escalation surfaced during execution:** YES — execution stayed within Stage A escalation matrix (PH-E1..E4 + Owner-promoted enhancement).

**Close ratifies on its own text.** Per Owner directive: **mandate-complete lands with it.**

---

## §2. Rulings applied — attest

### §2.1 PH-E1 α · vault-class classification + no-secrets-in-image

Owner verbatim: *"Classification-and-contract is the builder-side promise; the store choice is PH-R4's [OWNER] binding, and β would pre-commit a vault stack that binding may override. The annex contract lands as documentation + no-secrets-in-image; the SDK wiring follows the store choice, not precedes it."*

- Audit report at `/app/docs/production_housing/env_findings_v0.md` classifies every current `.env` var per BCR §3.4 annex verbatim: `MONGO_URL`/`JWT_SECRET`/`EMERGENT_LLM_KEY`/`ADMIN_PASSWORD` → **vault** · `DB_NAME`/`LLM_PROVIDER`/`OBJECT_STORE_ENDPOINT`/`PUBLIC_BASE_URL`/`REACT_APP_BACKEND_URL`/`GIT_SHA`/`BUILD_TIMESTAMP` → **config** · `LLM_API_KEY`/`OBJECT_STORE_CREDS` → **vault (populated at PH-R4/PH-R2)**.
- Zero findings at 2026-07-10 scan (all vars map to annex classifications).
- Injection contract documented: K8s Secret projection / HashiCorp Vault SDK / cloud-native secret manager — [OWNER: store choice] at PH-R4.
- `.dockerignore` excludes `.env` + `.env.*` (attested at PH-G2).
- `Dockerfile` does NOT `COPY .env` (attested at PH-G2).
- Runtime code reads secrets via `os.environ.get(...)` only — no code change.
- Audit file contains zero secret VALUES (attested at PH-G1 grep-negative on MongoDB URI · JWT · sk-* · AKIA* patterns).

Attested at: **PH-G1** (test_env_findings_audit_exists_and_references_bcr_annex + test_env_findings_audit_contains_no_secret_values), **PH-G2** (test_dockerfile_does_not_copy_dotenv + test_dockerignore_excludes_dotenv).

### §2.2 PH-E2 α · multi-stage single-image split

Owner verbatim: *"Multi-stage single image, deploy topology chooses how to serve — the split preserved at the layer boundary without assuming pod-multiplicity nobody has ruled. This is 'destination-agnostic' applied to packaging, same principle as 9.2a's containers. β/γ both pre-commit infrastructure that PH-R2/R3/R4 haven't named."*

- `/app/Dockerfile` — two FROM stages:
  - **Stage 1 · frontend-build:** `node:20-alpine` → `yarn install --frozen-lockfile && yarn build` → `/build/frontend/build/`.
  - **Stage 2 · backend-runtime:** `python:3.11-slim` → `pip install -r backend/requirements.txt` → `COPY --from=frontend-build /build/frontend/build /app/frontend/build` → non-root `app` user → `EXPOSE 8001` → `HEALTHCHECK CMD curl -fsS http://localhost:8001/api/healthz` → `CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8001"]` (preserves supervisor entry verbatim).
- `/app/docker-compose.yml` — dev-parity harness (mongo:6 + backend built).
- `/app/.dockerignore` — excludes `.env*`, `node_modules`, `.venv`, `__pycache__`, `.git`, `test-results/`, `docs/`, `memory/`, `salvage/`.
- Deploy topology choice deferred to PH-R2/PH-R3/PH-R4 [OWNER] bindings (FastAPI-serve vs CDN-serve).
- Frontend/backend split posture documented at `/app/docs/production_housing/frontend_backend_split.md`.

Attested at: **PH-G2** (test_dockerfile_exists_and_is_multistage + test_dockerfile_exposes_8001_and_has_healthcheck).

### §2.3 PH-E3 α · `/readyz` FS-enumeration sharing V1-G7 counter

Owner verbatim: *"FS enumeration sharing V1-G7's authoritative counter — readiness and the parity gate must never disagree about what parity is, and one counting mechanism guarantees that. γ correctly rejected on honesty grounds; β adds production import risk for nothing."*

- Shared counter at `/app/backend/services/health/parity_counter.py`:
  - `count_frozen_contract_snapshots()` returns `len(list(_INVARIANTS_DIR.glob("*.contract_snapshot.json")))`.
  - `EXPECTED_PARITY = 31`. `parity_ok()` returns True iff on-disk == 31.
- `/api/healthz` (routers/health.py) — 200 `{"status": "alive"}` · no auth · no DB.
- `/api/readyz` (routers/health.py):
  - 200 `{"status": "ready", "parity_count": 31, "expected_parity": 31, "db": "ok"}` on both green.
  - 503 `{"status": "not_ready", "reason": "parity_mismatch", "parity_count": <n>, "expected_parity": 31}` on FS drift.
  - 503 `{"status": "not_ready", "reason": "db_ping_failed", ...}` on Mongo unavailable.
  - Refusal taxonomy untouched — 503 is infra readiness signal, NEVER a refusal envelope (AF-E2 amended posture · attested at test_ph_g_readyz_source_never_uses_refusal_envelope AST cell).
- V1-G7 test at `backend/tests/invariants/test_9_2a_real_perception.py::test_v1_g7_attestation_parity_31_at_9_2a_close` refactored to import from `services.health` (uses the shared counter).
- **One authoritative counter across three surfaces:** `/api/readyz` + `/api/system/build_info` + V1-G7 gate — all read from `services.health.count_frozen_contract_snapshots()` (attested at PH-G6).

Attested at: **PH-G3** (healthz + readyz 200 + readyz 503 on DB down + readyz 503 on parity drift), **PH-G6** (shared counter module exists + returns 31 + all three surfaces import from shared module + directory canonical).

### §2.4 PH-E4 α + Owner documentation-addition · LLM swap seam

Owner verbatim: *"α, one addition inside the same ruling: document the seam, defer the rename — correct, 'contained + documented' is the PH-R1 clause and β is a mid-flight refactor with no honesty gain. Addition: the seam doc records the BCR annex shape as the binding migration target with its call-site inventory (the two post-cut call sites named), so the PH-R4 swap executes against a written target rather than rediscovering the seam. Documentation content, zero code, no cell change."*

- Seam doc at `/app/docs/production_housing/llm_swap_seam.md`:
  - **Current shape:** `invoke_with_metering(prompt, model_preference, timeout_seconds, system_msg) -> (text, provider, model, usage)` at `services/synisense/shield/llm_router.py`.
  - **Single-source discipline:** attested by pre-existing `test_no_direct_llm_calls_outside_shield` AST gate.
  - **Owner addition · migration target (verbatim from BCR annex):** `complete(messages: list[dict], temperature: float, model: str) -> str` · provider selection reads `LLM_PROVIDER` env var · call sites never change.
  - **Owner addition · call-site inventory (two post-cut · named):**
    - `backend/services/synisense/shield/fluency_synthesizer.py::L182` (Answer Fluency).
    - `backend/services/synisense/shield/brief_synthesizer.py::L116` (Opportunity Briefs).
- **Zero code change to `llm_router.py` at PH-R1.** Shape rename lands post-PH-R4 owner-side swap.

Attested at: **PH-G4** (test_llm_swap_seam_doc_exists_and_records_target_shape + test_llm_swap_seam_call_site_inventory_matches_repo).

### §2.5 Enhancement promotion · `/api/system/build_info`

Owner verbatim: *"promoted, landing with this execution. Ruled in rather than deferred because it converts PH-R1's own STAKED claim ('promotion-not-rebuild') from asserted to verifiable — a deployed artifact that states its git SHA is the audit made mechanical. Git SHA + build timestamp + parity_count (same counter as PH-E3), no secrets in the payload."*

- Endpoint at `/app/backend/routers/system_info.py` — `GET /api/system/build_info`.
- Payload shape (Owner explicit): `{"git_sha": "<40-char SHA>", "build_timestamp": "<ISO-8601 UTC>", "parity_count": 31}`.
- **Parity count uses the SAME shared counter as `/api/readyz` and V1-G7** — one authoritative source across three surfaces (attested at PH-G6).
- Build-arg injection: `GIT_SHA` + `BUILD_TIMESTAMP` in Dockerfile (`ARG` + `ENV`). Runtime resolution: (1) env var; (2) `git rev-parse HEAD` at container startup; (3) `"dev-unknown"` fallback. Never blocks.
- **No secrets in payload** (Owner explicit) — attested at PH-G5 grep-negative on MongoDB URI · JWT · sk-* patterns.

Attested at: **PH-G5** (test_build_info_returns_git_sha_and_parity + test_build_info_payload_no_secrets), Playwright smoke (`e2e/build_info_smoke.spec.ts` × 3 cells).

### §2.6 Band `[900, 1,700]` ratified — verdict below

See §4.

---

## §3. Gate roster (full attestation)

**Backend Pytest cells — all green (24 cells across PH-G1..G6 + auxiliary):**

| Gate family | Cells | Tier | Location |
|---|---:|---|---|
| **PH-G1** env classification (audit exists · references BCR · no secrets in file) | 2 | Tier-1 (annex environment contract) | `backend/tests/invariants/test_production_housing_ph_g1_to_g6.py` |
| **PH-G2** Dockerfile (multistage · no COPY .env · .dockerignore excludes .env · EXPOSE 8001 + HEALTHCHECK) | 4 | Tier-1 (packaging + secret externalization) | same |
| **PH-G3** healthz + readyz (liveness no-DB · readyz 200 healthy · readyz 503 db-down · readyz 503 parity-drift) | 4 | Tier-1 (annex healthchecks) | same |
| **PH-G4** LLM swap seam doc (doc exists + records target shape · call-site inventory matches repo) | 2 | Tier-1 (annex LLM swap seam) | same |
| **PH-G5** build_info (returns git_sha + parity · payload no secrets) | 2 | Tier-1 (Owner enhancement promotion) | same |
| **PH-G6** one authoritative counter (counter exists · returns 31 · three surfaces share source · directory canonical) | 4 | Tier-1 (PH-E3 α invariant) | same |
| **PH-G-Parity** parity 31 preserved | 1 | Tier-1 (frozen contracts) | same |
| **PH-G-Docs** four production_housing files exist + reference BCR + reference ruling date + rulings record captures all rulings + stage A linked | 4 | Tier-3 (Standing Rule v3) | same |
| **PH-G-Refusal-Closed** /readyz source never uses refusal envelope | 1 | Tier-1 (AF-E2 amended posture) | same |

**Frontend Jest cells:** zero new (PH-R1 lands no UI cells). Regression: 145/145 unchanged.

**Frontend Playwright chromium smokes — all green (3 cells):**

| Cell | Attests |
|---|---|
| `build_info reachable and returns the Owner-approved payload shape` | endpoint reachable through ingress · payload = `{git_sha, build_timestamp, parity_count}` · parity_count=31 |
| `build_info payload carries no secrets (Owner explicit)` | grep-negative on MongoDB URI · JWT · sk-* patterns |
| `healthz reachable · liveness · 200 alive` | liveness endpoint reachable · payload = `{"status": "alive"}` |

Location: `frontend/e2e/build_info_smoke.spec.ts`.

**Total:** 24 backend Pytest + 3 Playwright chromium = **27 cells**. Well under 60 cell threshold.

---

## §4. Rule 2 accounting — §9 metric-verdict-in-raw-LoC

### §4.1 Actual raw LoC (from `wc -l`)

| Bucket | LoC |
|---|---:|
| `backend/routers/health.py` | 84 |
| `backend/routers/system_info.py` | 95 |
| `backend/services/health/__init__.py` | 14 |
| `backend/services/health/parity_counter.py` | 48 |
| `backend/server.py` (mount block delta) | ~15 |
| `backend/tests/invariants/test_9_2a_real_perception.py` (V1-G7 refactor delta) | ~10 |
| **Backend source subtotal** | **266** |
| `backend/tests/invariants/test_production_housing_ph_g1_to_g6.py` | 389 |
| **Backend tests subtotal** | **389** |
| `Dockerfile` | 84 |
| `.dockerignore` | 65 |
| `docker-compose.yml` | 64 |
| **Container artifacts subtotal** | **213** |
| `docs/production_housing/env_findings_v0.md` | 93 |
| `docs/production_housing/frontend_backend_split.md` | 77 |
| `docs/production_housing/llm_swap_seam.md` | 134 |
| `docs/production_housing/promotion_audit_v0.md` | 129 |
| `docs/rulings/production_housing_ph_r1_ph_e1_to_e4.md` | 134 |
| **Docs subtotal** | **567** |
| `frontend/e2e/build_info_smoke.spec.ts` | 63 |
| **Frontend tests subtotal** | **63** |
| **GRAND TOTAL (code + tests + docs · raw LoC per §9)** | **1,498** |

### §4.2 Band verdict (§9 band-relative trichotomy)

- **Ratified band:** `[900, 1,700]` (per rulings §2.6).
- **Actual:** **1,498 raw LoC**.
- **Position in band:** at ~75% of range · WITHIN BAND · **`snapshot_raw_in_band=yes`**.
- **Trichotomy verdict:** in-band. No driver disclosure required beyond snapshot line.

### §4.3 §4.2 threshold disclosure (Tier-2 · never blocking per §12.1)

- **Raw LoC threshold (1,500):** **NOT CROSSED** — 1,498 vs 1,500 = -0.13% (2 LoC under). Effectively at-threshold; disclosure noted for completeness.
- **Cell count threshold (60):** NOT crossed. 24 backend + 3 Playwright = **27 cells**.
- **Disposition:** atomic single commit per §4.1 baseline · dev's judgment per Owner delegation. Split-fallback NOT triggered. Container + code + tests + docs land together (audit narrative cohesion).

### §4.4 CI outcomes

- **Pytest:** 1,202 passed + 1 skipped (baseline 1,178 + 1 → **+24 new PH-R1 cells**).
- **Jest:** 145/145 (baseline 145/145 → zero new; PH-R1 lands no UI).
- **Playwright chromium:** 51/51 (baseline 48/48 → **+3 new PH-R1 build_info smokes**).
- **Parity:** **31/31 byte-identical** (attested at PH-G-Parity).
- **Backend live-endpoint smoke (post supervisor restart):**
  - `curl /api/healthz` → `{"status":"alive"}`
  - `curl /api/readyz` → 200 with parity=31
  - `curl /api/system/build_info` → `{"git_sha":"d5a5d1756a76b4b2dba8ff04e5e9905417c71fac","build_timestamp":"...","parity_count":31}`

---

## §5. §12.1 remaining-gates enumeration (Owner 2026-07-10)

Per governance §12.1 · Tier-1 surfaces named in the mandate covered by execution:

- **BCR §3.4 · containerize from the repository** → PH-E2 α · PH-G2 (green) · `Dockerfile` + `.dockerignore` + `docker-compose.yml` land. **Ratified in effect.**
- **BCR §3.4 · externalize all secrets from .env to a vault-class store** → PH-E1 α · PH-G1 + PH-G2 (green) · classification-and-contract landed via `env_findings_v0.md`; no secret VALUES in image; SDK wiring deferred to PH-R4 owner-side store choice. **Ratified in effect (builder-side half).** PH-R4 owner-side ruling required for store SDK integration.
- **BCR §3.4 · add healthchecks** → PH-E3 α · PH-G3 (green) · `/api/healthz` + `/api/readyz` land per annex verbatim. **Ratified in effect.**
- **BCR §3.4 · split frontend build from backend serve** → PH-E2 α · PH-G2 (green) · multi-stage single image; deploy topology owner-side. **Ratified in effect.**
- **BCR §3.4 · database address stays env-driven** → NOT-A-FINDING at PH-R1 audit · `MONGO_URL` protected variable · zero hardcoded Mongo URIs. **Ratified in effect.**
- **BCR §3.4 · LLM swap seam contained + documented** → PH-E4 α + Owner addition · PH-G4 (green) · single-source discipline attested; seam doc records target shape + call-site inventory. **Ratified in effect.**
- **BCR §3.4 · promotion-not-rebuild audit [STAKED]** → Owner enhancement promotion · PH-G5 + PH-G6 (green) · `/api/system/build_info` makes the audit mechanical (git SHA + build timestamp + parity). **Ratified in effect · audit made mechanical.**

No remaining Tier-1 gates open at PH-R1 builder-side half. Deferred to owner-side:
- **PH-R2 · data plane** ([OWNER] managed replicated DB + artifact store)
- **PH-R3 · Domain + TLS** ([OWNER: domain])
- **PH-R4 · [OWNER] bindings** (production destination · LLM account swap · domain)

---

## §6. Standing constraints preserved

| Constraint | Attest |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | PH-G-Parity (green) · no contract touched · V1-G7 refactored to shared counter · same result |
| 4-code auth-refusal registry closed | GREEN — no auth surface touched |
| No HTTP 409 in PH-R1 new/modified files | GREEN — 503 on not-ready is infra fault, never 409 |
| Standing Rule v3 (on-disk canonical) | GREEN — Stage A + rulings + close + 4 production_housing docs all on-disk |
| AS-H1 retention held-class (no direct DELETE) | GREEN — no DELETE handlers landed |
| Governance §8 data-blind posture | PH-G1 (green) — env findings audit contains zero secret values |
| Governance §9 metric-verdict-in-raw-LoC | GREEN — verdict rendered in raw LoC · WITHIN BAND |
| Governance §10 9.2 split ruling | GREEN — PH-R1 dispatch-independent from 9.2a/9.2b |
| Governance §11 9.2-OWN resolution | N/A (PH-R1 is packaging; not topology) |
| Governance §12 close-ratification-on-own-text | GREEN — three criteria met (see §1) |
| Governance §12.1 remaining-gates enumeration | GREEN — see §5 |
| AF-E2 amended boundary set (Standing Disposition 2026-07-10) | GREEN — /readyz 503 is infra readiness signal, never a refusal envelope (attested at test_ph_g_readyz_source_never_uses_refusal_envelope AST cell) |
| Shield chokepoint (`test_no_direct_llm_calls_outside_shield`) | GREEN — PH-R1 lands no LLM code; documents the existing seam |
| MONGO_URL / DB_NAME protected variables | GREEN — never modified |
| REACT_APP_BACKEND_URL protected variable | GREEN — never modified (used at Dockerfile stage-1 as build ARG) |
| BCR v1.5 §3.4 annex environment contract | PH-G1 (green) · every currently-in-.env var classified per annex verbatim |
| **One authoritative parity counter** (PH-E3 α invariant) | **PH-G6 (green)** · `/api/readyz` + `/api/system/build_info` + V1-G7 test all import from `services.health.count_frozen_contract_snapshots()` |

---

## §7. Tier-3 defaults applied (silent · one-line each per §6.3)

- **[Tier 3]** file names: `Dockerfile`, `.dockerignore`, `docker-compose.yml` (repo root) · `backend/routers/{health,system_info}.py` · `backend/services/health/{__init__,parity_counter}.py` · `docs/production_housing/{env_findings_v0,frontend_backend_split,llm_swap_seam,promotion_audit_v0}.md` · `docs/rulings/production_housing_ph_r1_ph_e1_to_e4.md`.
- **[Tier 3]** base images: `node:20-alpine` (frontend build) · `python:3.11-slim` (backend runtime).
- **[Tier 3]** container user: `app` (non-root · groupadd/useradd system).
- **[Tier 3]** WORKDIR: `/app`.
- **[Tier 3]** healthcheck endpoint prefixes: `/api/healthz` + `/api/readyz` + `/api/system/build_info` (per `/api/*` routing convention).
- **[Tier 3]** healthz payload: `{"status": "alive"}` (200).
- **[Tier 3]** readyz payload success: `{"status": "ready", "parity_count": 31, "expected_parity": 31, "db": "ok"}` (200).
- **[Tier 3]** readyz payload failure: `{"status": "not_ready", "reason": "<db_ping_failed|parity_mismatch>"}` (503).
- **[Tier 3]** readyz mongo-ping timeout: 2.0 seconds.
- **[Tier 3]** build_info payload shape: `{"git_sha", "build_timestamp", "parity_count"}` (Owner explicit).
- **[Tier 3]** build_info fallbacks: env var → `git rev-parse HEAD` → `"dev-unknown"`.
- **[Tier 3]** docker-compose services: `mongo` (mongo:6 + `mongo_data` named volume) + `backend` (built).
- **[Tier 3]** env findings audit format: markdown table with `var_name | location | BCR class | source binding | notes` · NO secret values.
- **[Tier 3]** LLM swap seam doc format: current shape · migration target · call-site inventory with line refs.
- **[Tier 3]** promotion audit format: finding table with `finding_id | description | classification | rationale` · classification enum {NOT-A-FINDING, FIXED-IN-THIS-STAGE-A, DEFERRED-TO-PH-Rx}.
- **[Tier 3]** test file naming: `test_production_housing_ph_g1_to_g6.py` (all gate families in single file per single-file cohesion).
- **[Tier 3]** Playwright smoke file: `e2e/build_info_smoke.spec.ts`.
- **[Tier 3]** build-arg names: `GIT_SHA`, `BUILD_TIMESTAMP`, `REACT_APP_BACKEND_URL`.

---

## §8. §0.1 dispositions + §0.2 debts

**§0.1 dispositions:**
- Zero new §0.1 Standing Owner Dispositions at this close.

**§0.2 debts:**
- Zero new §0.2 Plan Debts at this close.
- **Deferred-to-PH-Rx (not debts · [OWNER]-bound per BCR §3.4):**
  - PH-R2 managed replicated DB + artifact store provisioning ([OWNER])
  - PH-R3 Domain + TLS ([OWNER: domain])
  - PH-R4 [OWNER] LLM account swap + production destination + domain

---

## §9. Provenance + sequence forward

- **Stage A proposal:** `/app/docs/stage_a_proposals/production_housing_ph_r1.md` · SHA `4c456c29a09b0c20b3920654028e26f23e0aae3aa3af96df9c824f63938d5461`.
- **Rulings record:** `/app/docs/rulings/production_housing_ph_r1_ph_e1_to_e4.md`.
- **Close report (this file):** `/app/docs/close_reports/production_housing_ph_r1.md`.
- **Container artifacts:** `/app/Dockerfile` + `/app/.dockerignore` + `/app/docker-compose.yml`.
- **Production housing docs:** `/app/docs/production_housing/{env_findings_v0,frontend_backend_split,llm_swap_seam,promotion_audit_v0}.md`.
- **Backend runtime source:** `/app/backend/routers/{health,system_info}.py` + `/app/backend/services/health/{__init__,parity_counter}.py`.

---

## §10. MANDATE-COMPLETE declaration (Owner-declared)

Per Owner ruling 2026-07-10 verbatim: *"On its close: **mandate-complete** — every BCR §3 item landed or explicitly [OWNER]-bound, and the build's remaining motion is 9.2b on your 'proceed.'"*

**Every BCR v1.5 §3 item landed OR explicitly [OWNER]-bound:**

| BCR §3 item | Status | Close/Ruling doc |
|---|---|---|
| §3.1 Perception (V1-I3 workers) | LANDED | Phase 9.1 close |
| §3.2 Artifact Store (V3 last-mile) | LANDED | 8-EXT close (`test_artifact_store.py`) |
| §3.3 Extraction Console (SM-E1..E3) | LANDED | Phase 9.3 close |
| §3.4 Production Housing **PH-R1** (builder-side dispatchable half) | **LANDED (this close)** | `docs/close_reports/production_housing_ph_r1.md` |
| §3.4 Production Housing PH-R2/R3/R4 | [OWNER]-BOUND | Deferred per BCR verbatim |
| §3.5 Seam 3 authorized deletion | LANDED | Seam 3 close |
| §3.6 B-5a Compliance Console read/prove | LANDED | Phase 8 Stage B-5a close |
| §3.6B B-5b Compliance Console writes | LANDED | Phase 8 Stage B-5b close |
| §3.7 Transform Forms (TF §6.3/§6.4) | LANDED | Transform Forms close |
| §3.8 Answer Fluency | LANDED | `docs/close_reports/answer_fluency.md` |
| §3.9 Auth (JWT + user model) | LANDED | Phase 8 Stage B-1 close |
| §3.10 Operator / Engineer / Master Admin surfaces | LANDED | Phase 8 Stage B-2/B-3/B-4 closes |
| §3.11 Consequence-class checker | LANDED | Seam 3 sub-stage 3 close |
| §3.12 Pricing / Fleet | LANDED | Phase 8 pricing close |
| §3.13 Compliance rule ownership | LANDED | Phase 8 Stage B-5b close |
| §3.14 Census dimensions | LANDED | Census dimensions close (2026-07-10) |
| §3.15 Opportunity Briefs | LANDED | `docs/close_reports/opportunity_briefs.md` (2026-07-10) |

**Mandate-complete gate reached** on the builder-side. Remaining motion: **9.2b on Owner's "proceed"** (RMS agreement + hardware at venue).

---

═══════════════════════════════════════════════════════════════════

*End of §3.4 Production Housing PH-R1 close report. Standing Rule v3: on-disk canonical. Per governance §12: named gates green (§3) · rulings + Owner-addition + enhancement attested as applied (§2) · no new Tier-1 escalation surfaced during execution — close ratifies on its own text. Per Owner directive: **mandate-complete lands with this close**. Sequence forward: idle · 9.2b on Owner "proceed".*
