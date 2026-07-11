# §3.4 Production Housing PH-R1 — Stage A Proposal

**Dispatch:** Auto-dispatch on §3.15 Opportunity Briefs close-landing (Owner pre-clearance 2026-07-10).
**Basis:** BCR v1.5 §3.4 (lines 161-183) verbatim · PH-R1 packaging (builder-side dispatchable half).
**Governance:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. Metric-verdict in raw LoC per §9 (band-relative trichotomy). Data-blind posture §8. Close-ratification-on-own-text §12 (Owner 2026-07-10) · §12.1 remaining-gates enumeration.
**Standing Rule v3:** on-disk canonical. Reply body carries SHA + tier tags + escalation matrix.
**Precedent:** Rides existing FastAPI/React/Mongo stack; Emergent LLM key already inside Shield at `services/synisense/shield/llm_router.py`; MONGO_URL / DB_NAME already env-driven per protected variable posture.

---

## §1. Owner dispatch — verbatim carrier

> **Dispatch: Production Housing PH-R1 Stage A auto-lands on Opportunity Briefs close-landing (§12 self-ratification permitted).** Land the proposal, tier-1 escalate at the STAKED audit + vault choice, otherwise Tier-3 defaults. Do NOT execute — proposal-only landing. PH-R2/PH-R3/PH-R4 remain scope-annotated and NOT dispatched (they carry [OWNER] bindings that gate full production landing; only PH-R1 is builder-side).

**Mandate reference (BCR v1.5 §3.4 lines 161-183 verbatim · authority-source language):**

> **§3.4 Production housing — packaging and the data plane**
>
> PH-R1 — Packaging (builder-side, destination-agnostic, dispatchable now): containerize from the repository; externalize all secrets from .env to a vault-class store; add healthchecks; split frontend build from backend serve; database address stays env-driven; the LLM swap seam is contained in the single router module and documented. This phase is the audit of the promotion-not-rebuild claim [STAKED — expect pod-specific assumptions to surface and be fixed].
>
> PH-R2 — Data plane: managed, replicated database with backup and append-only ledger archival; the artifact store (3.2) provisioned beside it. Per HS3 this MUST precede the first real mined hour.
>
> PH-R3 — Domain + TLS bind the public trust receipt (/trace/{id}) to its real URL as config [OWNER: domain].
>
> PH-R4 — [OWNER] bindings: production destination; LLM account (the current build is coupled to the platform-managed key; the swap is one module); domain. Demo deployment is permitted any time and carries none of these obligations.
>
> **Technical annex — environment contract, healthchecks, swap seam**
>
> Environment contract (every var named; source binding explicit)
>   MONGO_URL               vault     required
>   JWT_SECRET              vault     required
>   LLM_PROVIDER            config    emergent | anthropic  [OWNER: account]
>   LLM_API_KEY             vault     required off-platform
>   OBJECT_STORE_ENDPOINT   config    [OWNER: store choice]
>   OBJECT_STORE_CREDS      vault     required with store
>   PUBLIC_BASE_URL         config    [OWNER: domain] · binds /trace/{id}
>   Anything else found in .env at packaging = a finding, not a carry-over.
>
> Healthchecks
>   GET /healthz  liveness  · no auth, no DB touch
>   GET /readyz   readiness · DB ping + frozen-contract parity count
>
> LLM swap seam (single module)
>   llm_router.complete(messages, temperature, model) -> text
>   provider selection reads LLM_PROVIDER; call sites never change

**Scope of this Stage A:** PH-R1 builder-side half ONLY. PH-R2 (managed replicated data plane · [OWNER: DB provisioning]), PH-R3 (Domain + TLS · [OWNER: domain]), PH-R4 ([OWNER] bindings) are scope-annotated below in §7 but NOT proposed for dispatch here.

---

## §2. Scope + design

### §2.1 What lands (execution scope · informs Stage A gate roster)

**Containerization (single multi-stage Dockerfile · dev-parity via docker-compose):**

- `Dockerfile` at repository root — multi-stage:
  - **Stage 1 (frontend-build):** `node:20-alpine` base · `yarn install --frozen-lockfile` · `yarn build` → `/app/frontend/build`.
  - **Stage 2 (backend-runtime):** `python:3.11-slim` base · `pip install -r requirements.txt --no-cache-dir` · copies `/app/backend` + frozen frontend build (for the case where a single container serves both; alternative dual-container split disclosed as Tier-3).
  - Non-root user (`app`) · `WORKDIR /app` · exposes 8001 (backend) · CMD `uvicorn server:app --host 0.0.0.0 --port 8001` (production posture; local dev retains supervisor).
- `.dockerignore` — excludes `.env`, `node_modules`, `.venv`, `.pytest_cache`, `.git`, `test-results/`, `salvage/`, `docs/` (docs are on-disk canonical but excluded from packaging image; not runtime artifacts).
- `docker-compose.yml` at repository root — dev-parity harness:
  - `mongo` service (mongo:6 · named volume `mongo_data`).
  - `backend` service (built from Dockerfile · MONGO_URL derived from mongo service · JWT_SECRET/LLM_API_KEY sourced from `.env` symlink in dev).
  - `frontend-dev` service (optional · node:20-alpine · runs `yarn start` against backend at http://backend:8001; alternative is `frontend build` shipped inside backend image).

**Healthchecks (new backend router):**

- `backend/routers/health.py` — 2 endpoints:
  - `GET /api/healthz` — 200 `{"status": "alive"}` · **no auth, no DB touch**. Sync response.
  - `GET /api/readyz` — 200 `{"status": "ready", "parity_count": <int>, "expected_parity": 31}` on success · 503 `{"status": "not_ready", "reason": "<mongo_ping_failed | parity_mismatch>"}` on failure. Performs (a) `db.command("ping")` async, (b) parity count via file-system enumeration of `backend/tests/invariants/*.contract_snapshot.json` (matches V1-G7 pattern; no dev-only reflection dependency).
- Mount `/api/healthz` + `/api/readyz` in `server.py` router chain.
- Note: liveness/readiness routes are stateless from the app perspective — no rate limit, no auth.

**Secret externalization audit (PH-R1 core STAKED discipline):**

- Inventory + audit report at `docs/production_housing/env_findings_v0.md` cataloguing:
  - Every var currently in `backend/.env` and `frontend/.env` classified as: (a) `vault` (required off-platform: MONGO_URL, JWT_SECRET, LLM_API_KEY, EMERGENT_LLM_KEY, OBJECT_STORE_CREDS), (b) `config` (build-time: LLM_PROVIDER, OBJECT_STORE_ENDPOINT, PUBLIC_BASE_URL, DB_NAME, REACT_APP_BACKEND_URL), (c) **`finding`** (unexpected — flagged per BCR verbatim "*Anything else found in .env at packaging = a finding, not a carry-over*").
  - No secret values captured in the audit file — only var names + classifications + source-binding recommendations.
- No code change to secret consumption sites — the audit is documentation-first (PH-R1 STAKED discipline says "expect pod-specific assumptions to surface and be fixed"; the fix is landing the audit + explicit config-vs-vault classification so downstream promotion has a checklist).

**LLM swap seam documentation (single-router discipline):**

- `docs/production_housing/llm_swap_seam.md` — canonical documentation of the `services/synisense/shield/llm_router.py` chokepoint:
  - Confirms the single-source discipline: no call sites outside `services/synisense/shield/**` invoke an LLM (attested by pre-existing `test_no_direct_llm_calls_outside_shield`).
  - Documents the current `_provider_for(...)` dispatcher + `invoke_with_metering(...)` surface + the mandate-target `complete(messages, temperature, model) -> text` shape.
  - Enumerates the provider switch surface: `LLM_PROVIDER=emergent` (current default via Emergent LLM key) vs `LLM_PROVIDER=anthropic` (off-platform swap · owner-side per PH-R4).
  - **Zero code change** — the existing `llm_router.py` already implements the chokepoint; this Stage A only documents the seam per BCR annex requirement.
  - PH-E4 escalation below asks whether to introduce a `complete(messages, temperature, model)` public wrapper NOW (compat helper) or defer to PH-R4 owner-side account swap.

**Frontend/backend split (build/serve separation attestation):**

- `docs/production_housing/frontend_backend_split.md` — attests the split posture:
  - Frontend is a static SPA (React) built via `yarn build` → `frontend/build/` directory.
  - Backend is a FastAPI service serving `/api/*` only.
  - Production posture: static SPA served by CDN or reverse-proxy static handler; backend serves `/api/*` requests. Dev posture (this container): supervisor manages both.
  - `REACT_APP_BACKEND_URL` is the single frontend-to-backend binding; already `process.env.REACT_APP_BACKEND_URL`-driven per protected variable posture.

**Promotion-not-rebuild audit (STAKED per PH-R1):**

- `docs/production_housing/promotion_audit_v0.md` — the honest audit report:
  - Enumerates promotion-not-rebuild claims (containerize from repo · env-driven DB address · vault-source secrets · single-image build).
  - Enumerates pod-specific assumptions found in the current codebase (e.g., hardcoded supervisor commands, absolute paths, dev-only imports, MongoDB local URI dependencies) — the STAKED expected findings.
  - Each finding classified as: (a) `FIXED-IN-THIS-STAGE-A` (the audit surfaces it; the fix lands as part of this landing), (b) `DEFERRED-TO-PH-R2/PH-R3/PH-R4` ([OWNER]-gated · not builder-side), (c) `NOT-A-FINDING` (correctly-designed).
- Owner-verbatim STAKED discipline honored: audit lands the findings; findings are FIXED where builder-side, otherwise scope-annotated.

**Test cells:** PH-G1..PH-G4 backend gate roster per §5 below (all invariant-cell class per §6.1 + §6.10).

### §2.2 What is preserved byte-identical (Tier-1 non-negotiable)

- **All 31 frozen contracts** — untouched. Parity stays at 31 (attested at PH-G-Parity).
- **4-code auth-refusal registry** — untouched.
- **Refusal taxonomy** — untouched. Healthchecks are infra endpoints; 503 on not-ready is infra fault, never a refusal envelope.
- **Shield chokepoint** — untouched. `test_no_direct_llm_calls_outside_shield` remains GREEN.
- **Existing routers** — untouched (only new `routers/health.py` lands).
- **MONGO_URL / DB_NAME protected variables** — never modified.
- **REACT_APP_BACKEND_URL frontend binding** — never modified.
- **Supervisor configuration** — dev-tier only; not modified by this landing. Container Dockerfile CMD is the production posture; dev remains supervisor-managed.
- **Historical close reports** — Standing Rule v3 preserved.
- **AS-U2 fixture-census sample rules** — untouched.

### §2.3 Seam layout (execution guidance)

```
[repo root]              Dockerfile · .dockerignore · docker-compose.yml
    │                     ├─ stage 1 (node:20-alpine) → yarn build → /app/frontend/build
    │                     └─ stage 2 (python:3.11-slim) → pip install → CMD uvicorn
    │
    ▼
[healthchecks]           backend/routers/health.py
    │                     ├─ GET /api/healthz  (no auth · no DB · liveness)
    │                     └─ GET /api/readyz   (DB ping + parity count · readiness)
    │
    ▼
[env audit]              docs/production_housing/env_findings_v0.md
    │                     └─ vault × config × finding classification (no values)
    │
    ▼
[llm swap seam]          docs/production_housing/llm_swap_seam.md
    │                     └─ single-router discipline attestation + shape docs
    │
    ▼
[split docs]             docs/production_housing/frontend_backend_split.md
    │                     └─ SPA + FastAPI split posture attestation
    │
    ▼
[STAKED audit]           docs/production_housing/promotion_audit_v0.md
                          └─ pod-specific assumption findings · FIXED × DEFERRED × NOT-A-FINDING
    │
    ▼
[test cells]             backend/tests/invariants/test_production_housing_ph_g1_to_g4.py
                          ├─ PH-G1 · liveness_endpoint_no_auth_no_db_touch (§6.11 async httpx + §6.10 AST)
                          ├─ PH-G2 · readiness_endpoint_pings_db_and_asserts_parity (§6.11 async httpx)
                          ├─ PH-G3 · llm_swap_seam_single_source (piggybacks on pre-existing test_no_direct_llm_calls_outside_shield)
                          └─ PH-G4 · env_findings_classification_matches_bcr_annex (§6.1 classic; file-attest)
                          + PH-G-Parity · parity_31_preserved_at_ph_r1_landing
                          + PH-G-Docs · promotion_audit_and_env_findings_files_exist_and_reference_bcr (§6.1)
```

### §2.4 Data-blind + honesty-grammar posture attest

- Governance §8 data-blind posture: env findings audit file catalogues var names only · **NO secret values captured** in the on-disk audit. Attested at PH-G4.
- Governance §9: band derived + verdict rendered in RAW LoC (band-relative trichotomy per Owner correction 2026-07-10). LLoC + cell-density disclosure lines only.
- Governance §10: PH-R1 dispatch-independent from 9.2a/9.2b; container packaging is compute-to-data-agnostic.
- Governance §11: N/A (PH-R1 is packaging; 9.2-OWN topology is control-plane · already resolved compute-to-data).
- Governance §12: this Stage A adheres — Tier-1 surfaces enumerated pre-execution; no conditional ratifications.
- Standing Rule v3: this Stage A is on-disk canonical; reply body SHA + tier tags + escalation matrix only.

---

## §3. Band derivation — RAW LoC per governance §9

Rate composition per §6.1-6.11 + §6.9 verbatim-carrier overhead + §6.10 AST/reflection.

### §3.1 Backend source

| Item | Rate class | Est. LoC (α) | Est. LoC (β) | Est. LoC (γ) |
|---|---|---:|---:|---:|
| `backend/routers/health.py` (new · 2 endpoints · async DB ping + fs parity count) | §6.3 route surface | 100 | 130 | 80 |
| `backend/server.py` — mount health router (delta) | §6.4 wire-up | 8 | 10 | 5 |
| **Backend source subtotal** | | **108** | **140** | **85** |

### §3.2 Backend tests

| Gate | Cell class | Cells | Rate | LoC |
|---|---|---:|---:|---:|
| **PH-G1** test_liveness_endpoint_no_auth_no_db_touch | §6.11 async httpx + §6.10 AST no-DB-call check | 3 | 25 | 75 |
| **PH-G2** test_readiness_endpoint_pings_db_and_asserts_parity | §6.11 async httpx (200 success + 503 db-fail + 503 parity-mismatch) | 3 | 25 | 75 |
| **PH-G3** test_llm_swap_seam_single_source | piggyback on pre-existing test (reflection attest only) | 1 | 40 | 40 |
| **PH-G4** test_env_findings_classification_matches_bcr_annex | §6.1 classic file-attest | 2 | 15 | 30 |
| **PH-G-Parity** test_parity_31_preserved_at_ph_r1_landing | §6.1 classic | 1 | 12 | 12 |
| **PH-G-Docs** test_promotion_audit_and_env_findings_files_exist_and_reference_bcr | §6.1 classic | 3 | 15 | 45 |
| **Backend tests subtotal** | | **13** | | **277** |

### §3.3 Frontend tests

**Zero frontend cells at PH-R1.** No new frontend surface lands; PH-R1 is packaging + infra-endpoint scope. Existing 145/145 Jest + 48/48 Playwright chromium baseline preserved (regression-only).

### §3.4 Container + doc artifacts

| Item | Rate class | Est. LoC (α) | Est. LoC (β) | Est. LoC (γ) |
|---|---|---:|---:|---:|
| `Dockerfile` (multi-stage · non-root · exposes 8001) | §6.7 config | 60 | 80 | 40 |
| `.dockerignore` | §6.7 config | 25 | 35 | 15 |
| `docker-compose.yml` (dev-parity: mongo + backend + optional frontend-dev) | §6.7 config | 55 | 80 | 35 |
| `docs/production_housing/env_findings_v0.md` (audit report · classification-only · no secret values) | §6.9 verbatim carrier | 200 | 280 | 140 |
| `docs/production_housing/llm_swap_seam.md` (chokepoint attest + shape docs) | §6.9 verbatim carrier | 150 | 200 | 100 |
| `docs/production_housing/frontend_backend_split.md` (posture attest) | §6.9 verbatim carrier | 80 | 120 | 55 |
| `docs/production_housing/promotion_audit_v0.md` (STAKED audit · pod-specific findings) | §6.9 verbatim carrier | 300 | 450 | 200 |
| **Container + doc subtotal** | | **870** | **1,245** | **585** |

### §3.5 Frozen contract accounting

- **Envelope untouched:** no §6.6 class LoC charged.
- **No new snapshot:** no §6.7 snapshot LoC charged.
- Parity stays at **31**.

Proactive design goal: **zero Tier-1 contract-touches** — PH-R1 is a wrapping-layer landing (containers + healthchecks + doc audits). No contract shape needs mutation.

### §3.6 Band composition

Total per scenario:

| Scenario | Backend source | Backend tests | Container + docs | Total raw LoC |
|---|---:|---:|---:|---:|
| **α** (builder-recommended · dev-parity docker-compose · docs comprehensive) | 108 | 277 | 870 | **1,255** |
| **β** (verbose · findings audit long-form · additional K8s manifests) | 140 | 277 | 1,245 | **1,662** |
| **γ** (minimal · Dockerfile-only · terse audit docs) | 85 | 277 | 585 | **947** |

**Proposed band (raw LoC per §9):** `[900, 1,700]` — brackets all three scenarios with headroom.

Band-relative trichotomy per §9 (Owner correction 2026-07-10):
- below-bottom (< 900) — disclose driver per Tier-2 discipline
- in-band ([900, 1,700]) — no disclosure beyond snapshot line
- above-top (> 1,700) — disclose driver per Tier-2 discipline

### §3.7 §4.2 threshold statement (Tier-2 disclosure · never blocking per §12.1)

- **Raw LoC threshold:** 1,500. Point-estimate: α = 1,255 · β = 1,662 · γ = 947. **§4.2 raw threshold projected-CROSSED under scenario β only** (in-band α · in-band γ · projected-crossed β at +11%).
- **Cell count threshold:** 60. Estimate: 13 backend cells + 0 frontend cells = **13**. Well under.
- **Disposition anticipated: atomic single commit per §4.1 baseline** — dev's judgment at execution per governance §2.2 (no round-trip). Container + docs + tests land together; splitting would fracture the audit narrative.
- Per governance §12.1 (Owner 2026-07-10): §4.2 threshold disclosures are Tier-2, disclosure-only, never blocking.

---

## §4. Standing constraints preserved at close (attested pre-execution)

| Constraint | Attest at execution |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | GREEN — no contract touch; PH-G-Parity attests. |
| 4-code auth-refusal registry closed | GREEN — healthchecks are infra endpoints. |
| No HTTP 409 in new/modified files (E5) | GREEN — 503 on not-ready is infra fault, never 409. |
| Standing Rule v3 (on-disk canonical) | GREEN — Stage A on-disk here; audit + close land separately. |
| AS-H1 retention held-class (no direct DELETE) | GREEN — no DELETE handlers landed. |
| Governance §8 data-blind posture | GREEN — env findings audit catalogues var names only (NO secret values). |
| Governance §9 metric-verdict-in-raw-LoC | GREEN — band + verdict in raw LoC. |
| Governance §10 9.2 split ruling | GREEN — PH-R1 dispatch-independent from 9.2a/9.2b. |
| Governance §11 9.2-OWN resolution | N/A (PH-R1 is packaging; not topology). |
| Governance §12 close-ratification discipline | GREEN — this Stage A adheres; conditions attach at ruling time per §12. |
| AF-E2 amended boundary set precedent | GREEN — 503 on not-ready is infra fault; refusal envelope untouched. |
| Shield chokepoint (`test_no_direct_llm_calls_outside_shield`) | GREEN — PH-R1 lands no LLM code; documents the existing seam. |
| MONGO_URL / DB_NAME protected variables | GREEN — never modified. |
| REACT_APP_BACKEND_URL protected variable | GREEN — never modified. |
| BCR v1.5 §3.4 annex environment contract | GREEN — env findings audit maps every current .env var to vault × config × finding classification per annex. |

---

## §5. Gate roster (PH-G1..PH-G4 mandate + PH-G-Parity / -Docs auxiliary)

**Mandate gates (4 · from BCR v1.5 §3.4 annex verbatim):**

| Gate | Tier | Cell class | Purpose |
|---|---|---|---|
| **PH-G1** `test_liveness_endpoint_no_auth_no_db_touch` | **Tier-1 (annex liveness discipline)** | §6.11 async httpx + §6.10 AST | `/api/healthz` returns 200 without auth header · **no DB call in the code path** (AST attest). |
| **PH-G2** `test_readiness_endpoint_pings_db_and_asserts_parity` | **Tier-1 (annex readiness discipline)** | §6.11 async httpx × 3 | `/api/readyz` returns 200 with parity_count=31 on healthy Mongo · returns 503 when Mongo ping fails · returns 503 when parity count ≠ 31. |
| **PH-G3** `test_llm_swap_seam_single_source` | **Tier-1 (annex LLM swap seam discipline)** | §6.10 reflection | Attests via `test_no_direct_llm_calls_outside_shield` piggyback + doc-file existence at `docs/production_housing/llm_swap_seam.md` that the swap seam is single-source (call sites don't change). |
| **PH-G4** `test_env_findings_classification_matches_bcr_annex` | **Tier-1 (annex environment contract discipline)** | §6.1 classic file-attest | The env findings audit at `docs/production_housing/env_findings_v0.md` classifies every currently-in-.env var as vault/config/finding per BCR annex. No secret values appear in the file. |

**Auxiliary gates (2):**

| Gate | Tier | Cell class | Purpose |
|---|---|---|---|
| **PH-G-Parity** `test_parity_31_preserved_at_ph_r1_landing` | Tier-1 (frozen contracts) | §6.1 classic | 31 frozen contracts + 31 snapshots byte-identical. |
| **PH-G-Docs** `test_promotion_audit_and_env_findings_files_exist_and_reference_bcr` | Tier-3 (Standing Rule v3 file-existence) | §6.1 × 3 | The four production_housing docs exist + each references BCR v1.5 §3.4 verbatim. |

**Total: 6 named gate families · 13 cells · 277 raw LoC backend tests. Zero frontend cells.**

---

## §6. Escalation matrix — PRE-TIERED

Per Owner Message 412 (pre-cleared PH-R1 dispatch on OB close-landing) + BCR v1.5 §3.4 verbatim: Tier-1 surfaces track the annex verbatim (environment contract classification · healthcheck discipline · LLM swap seam · promotion-not-rebuild STAKED audit).

### §6.1 Tier-1 escalations (verbatim relay to Owner · exactly 4 · exactly the surfaces the annex names)

**PH-E1 · Vault-class secret store selection posture (Tier-1)**

> Owner authority-source language (BCR v1.5 §3.4 annex verbatim): *"MONGO_URL vault required · JWT_SECRET vault required · LLM_API_KEY vault required off-platform · OBJECT_STORE_CREDS vault required with store."*
>
> **Promise protected:** vault-class externalization — no secret value in the container image or in a repo-committed `.env` at production time.
>
> **Escalation:** the annex declares the requirement; the STORE CHOICE is the escalation.
>
> **Options (pre-authorised menu):**
> - **α · Documentation-only classification at PH-R1 (builder-recommended · destination-agnostic).** The audit report `docs/production_housing/env_findings_v0.md` classifies each var as `vault`/`config`/`finding` per BCR annex; documents the injection contract expected at production time (env-var interpolation via K8s Secret / HashiCorp Vault / cloud-native manager); the container image itself carries NO secret values (Dockerfile does not `COPY .env`). **No code change** — the runtime already reads env vars via `os.environ.get(...)` per `MONGO_URL`/`JWT_SECRET`/`EMERGENT_LLM_KEY` protected-variable posture. The vault-class binding lands at production deploy time (owner-side per PH-R4).
> - **β · Explicit vault-SDK integration in PH-R1** — introduces a `services/config/vault_reader.py` wrapper with pluggable backends (Kubernetes Secrets projection · HashiCorp Vault SDK · AWS Secrets Manager · local `.env` for dev). Adds ~180 LoC + integration tests. Would require Owner naming of the target vault backend (currently PH-R4 [OWNER]).
> - **γ · Minimum-viable: no audit, no docs, no SDK** — just remove `.env` from image via `.dockerignore` and rely on runtime env var contract. Under-delivers on the STAKED discipline.
>
> **Builder-recommendation: α.** The BCR annex declares the CONTRACT (vault vs config source-binding per var); PH-R4 declares the STORE CHOICE ([OWNER] binding). PH-R1's builder-side role is to LAND the classification-and-contract, not to pick the store. α closes the builder-side promise; the vault-SDK integration lands post-PH-R4 owner-side ruling on store choice. β prematurely commits to a specific vault stack that PH-R4 may override.
>
> **Class:** Tier-1 (annex environment contract discipline · secret externalization audit is STAKED).
> **Ruling required BEFORE execution.**

**PH-E2 · Container image posture — single vs dual-image (Tier-1)**

> Owner authority-source language (BCR v1.5 §3.4 verbatim): *"containerize from the repository; ... split frontend build from backend serve."*
>
> **Promise protected:** frontend build is separable from backend serve at deploy time.
>
> **Escalation:** "split frontend build from backend serve" reads two ways: (a) build-stage separation within one image (multi-stage Dockerfile), or (b) two separate images (backend image + static-SPA image behind a CDN). The mandate does not force one over the other; Owner selection required.
>
> **Options (pre-authorised menu):**
> - **α · Multi-stage single-image split (builder-recommended · destination-agnostic).** One `Dockerfile` with a `node:20-alpine` build stage + a `python:3.11-slim` runtime stage. Frontend build artifact copied into backend image OR left in the build cache (production deploy chooses: FastAPI serves `/frontend/build/*` OR a CDN serves it separately). This is the "promotion-not-rebuild" honest posture — the image contains both artifacts; deploy topology chooses which serves what. Aligns with the current supervisor-managed dev posture (both services present on the same host) while preserving the split at the layer boundary.
> - **β · Two-image split** — separate `Dockerfile.backend` + `Dockerfile.frontend`; frontend image is `nginx:alpine` serving static build. Cleaner separation but pod-multiplicity assumption that a demo deployment may not carry. Requires target deployment to orchestrate the split (K8s pod-multiplicity, docker-compose service pair, etc.).
> - **γ · Backend-only image + build artifact side-channel** — Dockerfile builds backend only; frontend build lands in a released artifact (e.g., S3 tarball); deploy pipeline downloads + mounts. Best for high-scale CDN posture; heaviest on tooling.
>
> **Builder-recommendation: α.** PH-R1 STAKED discipline says "expect pod-specific assumptions to surface and be fixed" — α is the mode that surfaces fewest assumptions (one image, deploy-time chooses how to serve). β pre-commits to pod-multiplicity that PH-R4 destination hasn't decided. γ requires infrastructure (S3 bucket, CDN) that PH-R2/PH-R3 owners have not yet named.
>
> **Class:** Tier-1 (container packaging shape · promotion-not-rebuild audit STAKED).
> **Ruling required BEFORE execution.**

**PH-E3 · `/readyz` parity-count implementation (Tier-1)**

> Owner authority-source language (BCR v1.5 §3.4 annex verbatim): *"GET /readyz readiness · DB ping + frozen-contract parity count."*
>
> **Promise protected:** readiness surface reflects true frozen-contract parity (not a stale constant); readiness fails 503 if parity drifts.
>
> **Escalation:** "frozen-contract parity count" resolution has two viable implementations; Owner selection required.
>
> **Options (pre-authorised menu):**
> - **α · File-system enumeration count (builder-recommended · matches V1-G7 pattern).** `/readyz` handler counts `*.contract_snapshot.json` files under `backend/tests/invariants/` at request time; asserts count == 31. Zero test-suite dependency; production-runtime-safe (fs enumeration is O(31)). Aligned with V1-G7 mechanism (which uses the same enumeration).
> - **β · Reflection-based enumeration via contracts module walk** — walks `backend/contracts/**/*.py` and counts modules with `model_config.frozen=True`. Runtime-heavier (imports every contract module at readiness time · production risk); more brittle to refactors. Not aligned with V1-G7.
> - **γ · Static constant** — hard-code `PARITY_COUNT = 31` in `routers/health.py`; assertion is trivial. Under-delivers on the "reflects true parity" promise — a contract addition without snapshot would not fail readiness. Rejected on honesty grounds.
>
> **Builder-recommendation: α.** V1-G7 already uses fs-enumeration; the readiness surface should share the same authoritative counter. β adds import surface risk. γ fails the honesty promise.
>
> **Class:** Tier-1 (annex readiness discipline · concrete implementation).
> **Ruling required BEFORE execution.**

**PH-E4 · LLM swap seam public shape at PH-R1 (Tier-1)**

> Owner authority-source language (BCR v1.5 §3.4 annex verbatim): *"llm_router.complete(messages, temperature, model) -> text · provider selection reads LLM_PROVIDER; call sites never change."*
>
> **Promise protected:** the LLM swap seam is one module, and its public shape is stable across provider swaps (call sites don't change).
>
> **Escalation:** the current `services/synisense/shield/llm_router.py` exposes `invoke_with_metering(prompt, model_preference, timeout_seconds, system_msg)` and `_provider_for(kind)` (private dispatch). BCR annex names the target shape as `complete(messages, temperature, model) -> text`. Two dispositions available.
>
> **Options (pre-authorised menu):**
> - **α · Document the existing seam · defer the shape rename to PH-R4 owner-side swap (builder-recommended).** `docs/production_housing/llm_swap_seam.md` documents the current `invoke_with_metering` shape + attests to the single-source discipline; declares the BCR annex target shape `complete(messages, temperature, model) -> text` as the migration target for PH-R4 owner-side LLM account swap. Zero code change. Preserves the Emergent LLM key posture (PH-R4 [OWNER] LLM account currently binds to Emergent).
> - **β · Introduce `complete(messages, temperature, model)` public wrapper at PH-R1** — new public function in `llm_router.py` that calls `invoke_with_metering` internally. All existing call sites (fluency_synthesizer, brief_synthesizer, wizard SonnetAgent · post-cut just fluency+brief) migrate to the new shape. Non-trivial refactor; risks breakage. Not required by PH-R1 (BCR §3.4 says "documented", not "renamed").
> - **γ · Leave completely undocumented** — trust the existing chokepoint gate. Under-delivers on BCR annex "LLM swap seam ... documented" verbatim.
>
> **Builder-recommendation: α.** BCR verbatim says "the LLM swap seam is contained in the single router module and documented" — "contained" (already true) + "documented" (α lands the doc). β is a rename that risks the chokepoint discipline mid-flight and adds no honesty at PH-R1; the shape rename is a post-PH-R4 owner-side migration. γ fails the "documented" clause.
>
> **Class:** Tier-1 (annex LLM swap seam discipline · documented single-source).
> **Ruling required BEFORE execution.**

### §6.2 Tier-2 disclosures (cost/rework · no round-trip · lines in close report)

- **T2-D1:** proposed raw-LoC band `[900, 1,700]` per §3 rate ledger + §9 raw-LoC verdict. Band-relative trichotomy per Owner §9 correction.
- **T2-D2:** §4.2 thresholds stated. Raw threshold **1,500 projected-CROSSED under scenario β only** (α + γ in-band). Cell count 13 << 60. Atomic single-commit per §4.1 baseline (per governance §12.1: §4.2 disclosures are never blocking · Tier-2 disclosure-only).
- **T2-D3:** cell-count estimate 13 backend + 0 frontend = 13 cells; density mix ~21 LoC/cell average (§6.11 async httpx × 6 + §6.10 reflection × 1 + §6.1 classic × 6).
- **T2-D4:** verbatim-carrier overhead (§6.9) counted at ~730 LoC across 4 doc files (env findings + LLM swap seam + FE/BE split + promotion audit) — this is the biggest α/β delta and honors Standing Rule v3 on-disk canonical posture.
- **T2-D5:** Dockerfile + docker-compose + .dockerignore land as config artifacts (§6.7 rate) — dev-parity harness is a Tier-3 builder default; if Owner prefers Kubernetes manifests instead of docker-compose, the delta lands at PH-R2 with the data plane.
- **T2-D6:** snapshot in-band verdict rendered post-execution against raw `wc -l`; LLoC + cell density disclosure-only per Owner §9 ruling.
- **T2-D7:** zero frontend cells — PH-R1 is packaging + infra endpoints; Jest 145/145 + Playwright chromium 48/48 baselines regression-preserved.

### §6.3 Tier-3 defaults (silent · one-line notes in close report)

Per Owner Message 412 pre-clearance + BCR v1.5 §3.4: "*all else Tier-3 defaults*" analogous to OB.

- **[Tier 3 default]** file names: `Dockerfile`, `.dockerignore`, `docker-compose.yml` at repository root · `backend/routers/health.py` · `docs/production_housing/{env_findings_v0,llm_swap_seam,frontend_backend_split,promotion_audit_v0}.md`.
- **[Tier 3 default]** base images: `node:20-alpine` (frontend build stage) · `python:3.11-slim` (backend runtime stage) — matches current supervisor-run stack versions.
- **[Tier 3 default]** container user: `app` (non-root) · WORKDIR `/app` · exposes port 8001 (backend).
- **[Tier 3 default]** healthcheck endpoint prefixes: `/api/healthz` + `/api/readyz` (per `/api/*` routing convention).
- **[Tier 3 default]** readiness response shape: `{"status": "ready", "parity_count": <int>, "expected_parity": 31}` (200) OR `{"status": "not_ready", "reason": "<str>"}` (503).
- **[Tier 3 default]** liveness response shape: `{"status": "alive"}` (200).
- **[Tier 3 default]** docker-compose services: `mongo` (mongo:6 + named volume) + `backend` (built) + optional `frontend-dev` (node:20-alpine + `yarn start`).
- **[Tier 3 default]** env findings audit format: markdown table with columns `var_name | source_binding | classification | notes` · NO secret values.
- **[Tier 3 default]** LLM swap seam doc format: markdown attesting the current `services/synisense/shield/llm_router.py` shape + the BCR annex target shape + the migration path.
- **[Tier 3 default]** promotion audit finding format: markdown table with columns `finding_id | description | classification (FIXED-IN-THIS-STAGE-A / DEFERRED-TO-PH-Rx / NOT-A-FINDING) | rationale`.
- **[Tier 3 default]** rulings + close docs on-disk: `docs/rulings/production_housing_ph_r1_e1_to_e4.md` + `docs/close_reports/production_housing_ph_r1.md`.
- **[Tier 3 default]** test file naming: `tests/invariants/test_production_housing_ph_g1_to_g4.py` (mandate + auxiliary gates folded into single file per single-file cohesion convention).

---

## §7. Deferred surfaces (scope-annotated · NOT dispatched at PH-R1)

Per BCR v1.5 §3.4 verbatim + Owner Message 412 pre-clearance:

- **PH-R2 — Data plane:** managed, replicated database with backup and append-only ledger archival + artifact store (§3.2) provisioned beside it. Per HS3 MUST precede first real mined hour. **Gated on** [OWNER] managed-database provisioning (post-9.2b RMS agreement).
- **PH-R3 — Domain + TLS:** binds `/api/trace/{id}` (post-OB rename OB-E2 Seam-2 α) to its real URL as config. **Gated on** [OWNER: domain].
- **PH-R4 — [OWNER] bindings:** production destination · LLM account swap (currently Emergent LLM key → off-platform account · single-module swap) · domain. Demo deployment permitted any time and carries none of these obligations.

PH-R2/PH-R3/PH-R4 are documented here for continuity; **no code, docs, or test changes land under these headers at this Stage A dispatch**.

---

## §8. §DirectionConsistency preview (per Owner §12 dead-tracker · not committed as recurring)

Owner 2026-07-10 struck the direction-consistency check as a recurring per-close section. This Stage A does NOT commit to running a per-close DirectionConsistency section; the check remains available at builder-discretion if a specific direction risk is identified during execution. Not a standing item.

---

## §9. Provenance + sequence forward

- **Stage A (this file):** `/app/docs/stage_a_proposals/production_housing_ph_r1.md`
- **Rulings record (post-Owner-ruling):** `/app/docs/rulings/production_housing_ph_r1_e1_to_e4.md`
- **Close report (post-execution):** `/app/docs/close_reports/production_housing_ph_r1.md`
- **Container artefacts:** `Dockerfile` + `.dockerignore` + `docker-compose.yml` (all at repo root · lifted-once, referenced everywhere).
- **Audit docs:** `/app/docs/production_housing/{env_findings_v0,llm_swap_seam,frontend_backend_split,promotion_audit_v0}.md`.
- **Sequence after:** mandate-complete gate on PH-R1 close. PH-R2/PH-R3/PH-R4 owner-side. 9.2b remains owner-side per §11.

═══════════════════════════════════════════════════════════════════

*End of §3.4 Production Housing PH-R1 Stage A proposal. Standing Rule v3: on-disk canonical. Awaiting Owner rulings on Tier-1 escalations PH-E1..PH-E4 (verbatim relay). Per governance §12 (2026-07-10): band/threshold disclosures are Tier-2, disclosure-only, never blocking; Tier-1 escalations return via verbatim relay before execution.*
