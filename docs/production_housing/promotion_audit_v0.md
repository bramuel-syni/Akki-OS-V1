# Promotion-not-rebuild audit (PH-R1 · STAKED discipline)

**Landing:** 2026-07-10 · Owner-declared STAKED per BCR v1.5 §3.4 PH-R1.
**Standing Rule v3:** on-disk canonical.

---

## §1. BCR v1.5 §3.4 verbatim STAKED clause

> PH-R1 — Packaging (builder-side, destination-agnostic, dispatchable now): ... **This phase is the audit of the promotion-not-rebuild claim [STAKED — expect pod-specific assumptions to surface and be fixed].**

**Owner enhancement promotion 2026-07-10:**

> Enhancement — /api/system/build_info: promoted, landing with this execution. Ruled in rather than deferred because it converts PH-R1's own STAKED claim ("promotion-not-rebuild") from asserted to verifiable — a deployed artifact that states its git SHA is the audit made mechanical.

---

## §2. Promotion-not-rebuild claims audited

The PH-R1 packaging landing makes these six claims. Each is audited below.

### Claim 1 · "Containerize from the repository"

**Audit:** The Dockerfile at repo root builds from the current tree with two stages (node:20-alpine → python:3.11-slim). Zero pod-specific tools/paths compiled into the image. Build is reproducible with `docker build .`.

**Verifiable:** Yes — `/api/system/build_info` returns `git_sha` = 40-char SHA of the source that built the image.

**Finding:** NONE.

### Claim 2 · "Externalize all secrets from .env to a vault-class store"

**Audit:** Dockerfile does NOT `COPY .env`. `.dockerignore` excludes all `.env*` patterns. Runtime code reads secrets via `os.environ.get(...)` only. Injection contract documented at `docs/production_housing/env_findings_v0.md`.

**Verifiable:** Yes — `docker history <image>` shows no `.env` layer; `docker create <image> && docker cp <container>:/app/backend/.env -` fails (file absent).

**Finding:** NONE at PH-R1 (contract landed). Vault-class BINDING lands at production deploy time (owner-side per PH-R4).

### Claim 3 · "Add healthchecks"

**Audit:** Two endpoints landed per BCR annex verbatim:
- `GET /api/healthz` — 200 `{"status": "alive"}` · no auth · no DB touch.
- `GET /api/readyz` — 200 with parity_count on both DB ping + FS-parity green; 503 on either fail.

**Verifiable:** Yes — `curl http://<container>:8001/api/healthz` returns 200 without any header; `curl http://<container>:8001/api/readyz` returns 200 iff Mongo is reachable AND parity=31.

**Finding:** NONE.

### Claim 4 · "Split frontend build from backend serve"

**Audit:** Multi-stage Dockerfile enforces artifact separation at the stage boundary. Frontend build artifact at `/app/frontend/build/` in the runtime image; deploy topology chooses FastAPI-serve vs CDN-serve. Structural split documented at `docs/production_housing/frontend_backend_split.md`.

**Verifiable:** Yes — the build stage boundary in the Dockerfile is a `--from=frontend-build` COPY; layer topology confirms the split.

**Finding:** NONE.

### Claim 5 · "Database address stays env-driven"

**Audit:** `MONGO_URL` is a protected env variable read via `os.environ.get("MONGO_URL")` in `backend/core/__init__.py`. Zero hard-coded Mongo URIs in the codebase (`grep -rn "mongodb://" backend/ | grep -v env` returns empty).

**Verifiable:** Yes — the injection contract at `env_findings_v0.md` names `MONGO_URL` as vault-class; the runtime binding is env-only.

**Finding:** NONE.

### Claim 6 · "The LLM swap seam is contained in the single router module and documented"

**Audit:** Single-router discipline enforced by pre-existing `test_no_direct_llm_calls_outside_shield` AST gate. Documentation landed at `docs/production_housing/llm_swap_seam.md` with call-site inventory (2 post-cut sites: `fluency_synthesizer.py:L182` + `brief_synthesizer.py:L116`) and BCR annex target shape recorded as migration binding for PH-R4.

**Verifiable:** Yes — `grep -rn "invoke_with_metering\|from services.synisense.shield import llm_router" backend/services/` returns exactly the 2 documented call sites plus the router itself.

**Finding:** NONE.

---

## §3. Pod-specific assumptions found (STAKED expected — surfaced + disposed)

Per Owner STAKED clause: *"expect pod-specific assumptions to surface and be fixed"*. Assumptions found + classified per Stage A convention:

| Finding | Description | Classification | Rationale |
|---|---|---|---|
| **F-01** | `/var/log/supervisor/*` log paths in dev tooling | **NOT-A-FINDING** | Supervisor is dev-only; production uses container stdout/stderr per 12-factor. Dockerfile CMD is `uvicorn` (no supervisor). |
| **F-02** | `sudo supervisorctl restart backend` in dev docs | **NOT-A-FINDING** | Dev tooling only; production replicas restart via K8s pod lifecycle. |
| **F-03** | Absolute `/app/*` paths in Python code | **NOT-A-FINDING** | `/app` is the runtime WORKDIR in the Dockerfile; matches K8s + docker-compose deploy convention. |
| **F-04** | Frontend hot-reload via `yarn start` | **NOT-A-FINDING** | Dev-only; production serves the built `frontend/build/` artifact. |
| **F-05** | `ADMIN_EMAIL`/`ADMIN_PASSWORD` idempotent seed at startup (server.py:180-183) | **NOT-A-FINDING** | Optional dev/test convenience; production MUST NOT set these. Documented in `env_findings_v0.md`. |
| **F-06** | `TESTING_LOCAL_MODE` env var references in some tests | **NOT-A-FINDING** | Test-only branch, never triggered in runtime. Not present in production env. |
| **F-07** | `Path(__file__).resolve().parents[N]` throughout backend | **NOT-A-FINDING** | Layout-anchored resolution matches `/app/backend/*` runtime layout; Dockerfile preserves the layout. |
| **F-08** | Test data in `backend/tests/invariants/*.contract_snapshot.json` shipped in the runtime image | **FIXED-IN-THIS-STAGE-A** | Ruling PH-E3 α requires these files present at runtime (readiness parity counter reads them). `.dockerignore` includes `backend/tests/` implicitly via layer selection — REVISED to keep the `invariants/*.contract_snapshot.json` files at `/app/backend/tests/invariants/` in the image. Explicit COPY handles this. |
| **F-09** | `.env` file must NOT reach image | **FIXED-IN-THIS-STAGE-A** | `.dockerignore` excludes `.env*` explicitly (PH-E1 α). |
| **F-10** | GIT_SHA + BUILD_TIMESTAMP resolution when build-args absent | **FIXED-IN-THIS-STAGE-A** | `routers/system_info.py::_resolve_git_sha()` falls back to `git rev-parse HEAD` on the container's source; further fallback to `"dev-unknown"`. Never blocks readiness. |
| **F-11** | Emergent LLM key coupled to platform (`EMERGENT_LLM_KEY`) | **DEFERRED-TO-PH-R4** | Owner-side LLM account swap per PH-R4 [OWNER] binding. Migration target documented at `docs/production_housing/llm_swap_seam.md`. |
| **F-12** | Managed replicated DB not yet provisioned | **DEFERRED-TO-PH-R2** | [OWNER] managed-database provisioning per PH-R2. Local MongoDB works for demo. |
| **F-13** | Public domain + TLS not yet bound | **DEFERRED-TO-PH-R3** | [OWNER: domain] per PH-R3. Trust receipt `/api/trace/{id}` will bind to real URL post-PH-R3. |
| **F-14** | Object store not yet provisioned | **DEFERRED-TO-PH-R2** | [OWNER: store choice] per PH-R2. Artifact store adapter (`routers/artifact_store.py`) already env-driven. |

**Summary:**
- **NOT-A-FINDING:** 7 (dev-only conventions correctly excluded from production posture).
- **FIXED-IN-THIS-STAGE-A:** 3 (F-08 test data preservation · F-09 .env exclusion · F-10 git-fallback resolver).
- **DEFERRED-TO-PH-Rx:** 4 (F-11 through F-14 · all [OWNER]-bound per BCR §3.4).

Zero unresolved-and-blocking findings. STAKED audit passes.

---

## §4. Mechanical audit surface (`/api/system/build_info`)

Per Owner enhancement promotion (2026-07-10), the audit is now mechanical:

```
$ curl https://<domain>/api/system/build_info
{
  "git_sha": "abc123...def",
  "build_timestamp": "2026-07-10T14:30:00Z",
  "parity_count": 31
}
```

**Invariants:**
- `git_sha` matches the source that built the image.
- `parity_count` uses the SAME shared counter as `/api/readyz` and V1-G7 gate (`services/health/parity_counter.py`) — the three surfaces never disagree.
- Payload contains **NO secrets** (attested at PH-G5 grep-negative cell).

**Verification workflow post-deploy:**
1. Owner reads `/api/system/build_info` from the deployed domain.
2. Owner runs `git rev-parse HEAD` against the intended source SHA.
3. If the two match → promotion-not-rebuild attested. If they don't → the deploy is on a different SHA than intended (a finding, not a fault of PH-R1).

═══════════════════════════════════════════════════════════════════

*End of promotion-not-rebuild audit. STAKED discipline honored: findings surfaced (14 total) · 7 NOT-A-FINDING · 3 FIXED-IN-THIS-STAGE-A · 4 DEFERRED-TO-PH-Rx. Zero unresolved-and-blocking. Audit made mechanical via `/api/system/build_info` (Owner enhancement 2026-07-10).*
