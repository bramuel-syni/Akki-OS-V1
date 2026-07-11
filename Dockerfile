# §3.4 Production Housing PH-R1 — Multi-stage Dockerfile
# Owner ruling PH-E2 α (2026-07-10): multi-stage single-image split · deploy
# topology chooses how to serve (FastAPI serves /frontend/build/* OR CDN
# serves it separately). This is the "destination-agnostic" packaging posture.
#
# BCR v1.5 §3.4 verbatim:
#   "containerize from the repository; ... split frontend build from
#    backend serve; ... the LLM swap seam is contained in the single
#    router module and documented."
#
# Build args (Owner enhancement promotion 2026-07-10 · /api/system/build_info):
#   GIT_SHA          — 40-char full git SHA of the source tree
#   BUILD_TIMESTAMP  — ISO-8601 UTC build wall-clock
# Injected into runtime env so /api/system/build_info can surface them
# without opening the container (mechanical audit of promotion-not-rebuild).

# ─── Stage 1 · Frontend build ────────────────────────────────────────
FROM node:20-alpine AS frontend-build

WORKDIR /build/frontend

# Copy manifest first for layer-cache efficiency; source second.
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install --frozen-lockfile --network-timeout 300000

COPY frontend/ ./
# REACT_APP_BACKEND_URL is a build-time binding; production deploy
# provides it via --build-arg or via a runtime SPA config injection.
ARG REACT_APP_BACKEND_URL=""
ENV REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}
RUN yarn build

# ─── Stage 2 · Backend runtime ───────────────────────────────────────
FROM python:3.11-slim AS backend-runtime

# System deps: curl (HEALTHCHECK) + git (build_info dev-fallback resolver).
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for the runtime process.
RUN groupadd --system app && useradd --system --gid app --home /app app

WORKDIR /app

# Python deps first (layer cache).
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/backend/requirements.txt

# Backend source.
COPY backend/ /app/backend/
# Frozen frontend build (from stage 1). Deploy may serve via FastAPI
# static mount OR a CDN; the artifact is present here either way.
COPY --from=frontend-build /build/frontend/build /app/frontend/build

# Owner enhancement promotion (2026-07-10): build_info envelope.
# `git_sha` + `build_timestamp` in the runtime environment; never a
# secret; enables /api/system/build_info to return a mechanical audit
# of the "promotion-not-rebuild" claim.
ARG GIT_SHA="dev-unknown"
ARG BUILD_TIMESTAMP="dev-unknown"
ENV GIT_SHA=${GIT_SHA} \
    BUILD_TIMESTAMP=${BUILD_TIMESTAMP} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Non-secret runtime defaults: MONGO_URL / JWT_SECRET / EMERGENT_LLM_KEY
# come from the vault-class secret store at deploy time (K8s Secret /
# HashiCorp Vault / cloud-native manager). NEVER copy .env into the image.
# See docs/production_housing/env_findings_v0.md for the full contract.

USER app

EXPOSE 8001

# BCR annex healthcheck: liveness endpoint · no auth · no DB touch.
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
    CMD curl -fsS http://localhost:8001/api/healthz || exit 1

# Preserve the current supervisor entry verbatim (promotion-not-rebuild).
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8001"]
