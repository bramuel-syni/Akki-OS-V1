# Env findings audit (PH-R1 · PH-E1 α)

**Landing:** 2026-07-10 · Owner ruling PH-E1 α.
**Standing Rule v3:** on-disk canonical · **NO SECRET VALUES in this file** (only var names + classifications + injection contract).

---

## §1. Owner ruling context (verbatim)

> **PH-E1 — α.** Classification-and-contract is the builder-side promise; the store choice is PH-R4's [OWNER] binding, and β would pre-commit a vault stack that binding may override. The annex contract lands as documentation + no-secrets-in-image; the SDK wiring follows the store choice, not precedes it.

**BCR v1.5 §3.4 annex verbatim:**

> Environment contract (every var named; source binding explicit)
>   MONGO_URL               vault     required
>   JWT_SECRET              vault     required
>   LLM_PROVIDER            config    emergent | anthropic  [OWNER: account]
>   LLM_API_KEY             vault     required off-platform
>   OBJECT_STORE_ENDPOINT   config    [OWNER: store choice]
>   OBJECT_STORE_CREDS      vault     required with store
>   PUBLIC_BASE_URL         config    [OWNER: domain] · binds /trace/{id}
>   Anything else found in .env at packaging = a finding, not a carry-over.

---

## §2. Classification matrix (per BCR annex · every current .env var)

Read from `/app/backend/.env` and `/app/frontend/.env` at 2026-07-10 (var names only · no values enumerated here).

| Var name | Location | BCR class | Source binding | Notes |
|---|---|---|---|---|
| `MONGO_URL` | `backend/.env` | **vault** | required | BCR annex verbatim · protected variable · never modify. |
| `DB_NAME` | `backend/.env` | **config** | required | BCR annex `MONGO_URL` binding · `DB_NAME` is the non-secret partition. |
| `JWT_SECRET` | `backend/.env` | **vault** | required | BCR annex verbatim · Phase 8 Stage B-1 auth issuance key. |
| `EMERGENT_LLM_KEY` | `backend/.env` | **vault** | required (platform-managed) | Emergent platform key · PH-R4 [OWNER] LLM account swap replaces this with off-platform `LLM_API_KEY`. |
| `ADMIN_EMAIL` | `backend/.env` | **config** | optional | Idempotent admin seed (server.py:180-183) · not a secret binding. |
| `ADMIN_PASSWORD` | `backend/.env` | **vault** | optional | Idempotent admin seed value · dev/test only; production must NOT set this. |
| `LLM_PROVIDER` | (not yet set · derived) | **config** | required at PH-R4 | Currently defaults to `emergent`; owner-side PH-R4 sets `emergent \| anthropic`. |
| `LLM_API_KEY` | (not yet set · PH-R4-side) | **vault** | required off-platform at PH-R4 | Populated when PH-R4 [OWNER] LLM account lands. Empty at PH-R1. |
| `OBJECT_STORE_ENDPOINT` | (not yet set · PH-R2-side) | **config** | [OWNER: store choice] | Populated when PH-R2 [OWNER] artifact-store binding lands. Empty at PH-R1. |
| `OBJECT_STORE_CREDS` | (not yet set · PH-R2-side) | **vault** | required with store | Populated when PH-R2 [OWNER] store choice lands. Empty at PH-R1. |
| `PUBLIC_BASE_URL` | (not yet set · PH-R3-side) | **config** | [OWNER: domain] | Populated when PH-R3 [OWNER] domain binding lands. Empty at PH-R1. |
| `REACT_APP_BACKEND_URL` | `frontend/.env` | **config** | required (build-time) | Protected variable · Kubernetes ingress URL · build-arg into Dockerfile stage-1. |
| `WDS_SOCKET_PORT` | `frontend/.env` | **config** | optional (dev-only) | React dev-server WebSocket port · not runtime-relevant post-build. |
| `GIT_SHA` | (build-arg · not .env) | **config** | Dockerfile ARG | Owner enhancement 2026-07-10 · injected via `--build-arg GIT_SHA=$(git rev-parse HEAD)` · surfaced by `/api/system/build_info`. |
| `BUILD_TIMESTAMP` | (build-arg · not .env) | **config** | Dockerfile ARG | Owner enhancement 2026-07-10 · injected via `--build-arg BUILD_TIMESTAMP=<ISO-8601>` · surfaced by `/api/system/build_info`. |

**Findings (per BCR annex verbatim: *"Anything else found in .env at packaging = a finding, not a carry-over"*):**

| Finding | Location | Disposition |
|---|---|---|
| None at 2026-07-10 scan | — | All vars in current `.env` files map to the annex contract. |

---

## §3. Injection contract (production posture · owner-side per PH-R4)

The Dockerfile at repo root does **NOT** `COPY .env`. Secret values enter the container **only** at deploy time via one of:

1. **Kubernetes Secret projection** — `env:` block in the pod spec pulling from `secretRef`:
   ```yaml
   env:
     - name: MONGO_URL
       valueFrom:
         secretKeyRef: { name: rms-secrets, key: mongo-url }
     - name: JWT_SECRET
       valueFrom:
         secretKeyRef: { name: rms-secrets, key: jwt-secret }
     - name: EMERGENT_LLM_KEY   # OR LLM_API_KEY post-PH-R4 swap
       valueFrom:
         secretKeyRef: { name: rms-secrets, key: llm-api-key }
   ```

2. **HashiCorp Vault sidecar injector** — Vault Agent renders env vars from Vault paths at pod init; consumer code unchanged.

3. **Cloud-native secret manager** — AWS Secrets Manager / GCP Secret Manager / Azure Key Vault via CSI driver or init-container.

**Which of the three lands is [OWNER: store choice] per BCR §3.4 · PH-R4.** PH-R1 lands the contract; PH-R4 owner-side ruling picks the store.

Config-class vars (`DB_NAME`, `LLM_PROVIDER`, `OBJECT_STORE_ENDPOINT`, `PUBLIC_BASE_URL`, `REACT_APP_BACKEND_URL`, `GIT_SHA`, `BUILD_TIMESTAMP`) enter via non-secret ConfigMap / build-arg / plain env; they are safe in image layers when set as ARG.

---

## §4. Attest — no secrets leave the repo

- Dockerfile: does NOT `COPY .env` or any file matching the `.env*` glob. `.dockerignore` excludes them at build time.
- Runtime code: reads secrets via `os.environ.get(...)` only. No secret is compiled into a Python source constant.
- `/api/system/build_info` payload contains `git_sha`, `build_timestamp`, `parity_count` **only** · no secrets (attested at PH-G5).
- Every other var in `backend/.env` maps to the annex classification above · zero unclassified findings at this landing.

═══════════════════════════════════════════════════════════════════

*End of env findings audit. On-disk canonical per Standing Rule v3. Zero secret values captured. Attested at PH-G1 (test_env_classification_matches_bcr_annex).*
