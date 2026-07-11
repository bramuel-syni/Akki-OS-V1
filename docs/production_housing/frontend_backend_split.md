# Frontend / Backend split posture (PH-R1 · PH-E2 α)

**Landing:** 2026-07-10 · Owner ruling PH-E2 α (multi-stage single-image split).
**Standing Rule v3:** on-disk canonical.

---

## §1. Owner ruling (verbatim)

> **PH-E2 — α.** Multi-stage single image, deploy topology chooses how to serve — the split preserved at the layer boundary without assuming pod-multiplicity nobody has ruled. This is "destination-agnostic" applied to packaging, same principle as 9.2a's containers. β/γ both pre-commit infrastructure that PH-R2/R3/R4 haven't named.

**BCR v1.5 §3.4 verbatim:**

> containerize from the repository; externalize all secrets from .env to a vault-class store; add healthchecks; **split frontend build from backend serve;** database address stays env-driven; the LLM swap seam is contained in the single router module and documented.

---

## §2. The split — at the layer boundary

**Frontend:**
- **Kind:** Static SPA (React 18 · Create React App / react-scripts).
- **Build:** `yarn build` produces `frontend/build/` (index.html + hashed JS/CSS bundles).
- **Backend binding:** `process.env.REACT_APP_BACKEND_URL` — the ONE binding. Set at build time via Dockerfile `ARG REACT_APP_BACKEND_URL`.

**Backend:**
- **Kind:** FastAPI + uvicorn ASGI service.
- **Path convention:** all endpoints live under `/api/*` (Kubernetes ingress routes `/api` to backend, everything else to the static SPA).
- **Port:** 8001 (fixed by supervisor config in dev; `EXPOSE 8001` in Dockerfile for prod).

**Split boundary:**
- The layer boundary is the Dockerfile stage boundary (frontend-build stage → backend-runtime stage).
- The frontend build artifact is copied INTO the backend runtime image at `/app/frontend/build/` — deploy topology chooses whether FastAPI serves it (single-container deploy) OR a CDN / reverse proxy serves it (split-deploy).

---

## §3. Deploy topologies (owner-side ruling per PH-R2/PH-R3/PH-R4)

**Topology A · Single-container deploy (permitted at demo · builder-side dispatchable):**
- Image contains BOTH artifacts; FastAPI mounts `/app/frontend/build/` as static (via `StaticFiles`) OR sits behind an ingress that serves static files from a shared volume.
- Pod-count = 1. Simplest.

**Topology B · Split-deploy (recommended for production · post-PH-R2):**
- Same image; static assets extracted at deploy time (`docker cp` OR init-container-side extract) → uploaded to a CDN (CloudFront / Fastly / Cloudflare).
- Backend pod serves `/api/*` only.
- Pod-count = ≥1 backend pod + CDN edge; scales independently.

**Topology C · Dual-image (rejected at PH-R1 · β option):**
- Separate `Dockerfile.backend` + `Dockerfile.frontend-nginx`; deploy runs both pods.
- Pre-commits pod-multiplicity that PH-R4 [OWNER] destination has not ruled on. Reject at PH-R1.

---

## §4. `REACT_APP_BACKEND_URL` posture

**Protected variable** per the container environment spec — never modified.

**Build-time binding:**
- Dockerfile stage-1 accepts `ARG REACT_APP_BACKEND_URL` and sets `ENV REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}` before `yarn build`. Create React App bakes it into the static bundle at build time.
- Production deploy pipelines pass the production URL via `--build-arg REACT_APP_BACKEND_URL=https://api.<domain>` (post-PH-R3 [OWNER: domain]).
- Development retains `http://localhost:3000` → `http://localhost:8001` via supervisor + hot-reload.

**Kubernetes ingress:**
- Ingress rule matches `/api/*` → backend service (port 8001).
- Everything else (`/`, `/opportunity-briefs`, `/operator/**`, etc.) → static assets (either a static-file service pod OR the CDN).

---

## §5. Split preserved by structure

The split is **structural**, not just conventional:
- Frontend NEVER imports backend code (Python isolated from JS bundle).
- Backend NEVER references frontend module names (FastAPI serves API only; static SPA config lives in ingress).
- Build stage boundary in the Dockerfile enforces the artifact separation — you can `docker create` an image, `docker cp` the `/app/frontend/build/` directory out, and ship it independently.

═══════════════════════════════════════════════════════════════════

*End of frontend/backend split posture. On-disk canonical per Standing Rule v3. Owner ruling PH-E2 α applied: multi-stage single-image split; deploy topology owner-side per PH-R2/PH-R3/PH-R4.*
