# §3.4 Production Housing PH-R1 — Rulings Record (PH-E1..PH-E4 + enhancement)

**Landing:** 2026-07-10 · Owner rulings on Tier-1 escalations PH-E1..PH-E4 + `/api/system/build_info` enhancement promotion + band `[900, 1,700]` ratification + close-landing note.
**Stage A basis:** `/app/docs/stage_a_proposals/production_housing_ph_r1.md` · SHA `4c456c29a09b0c20b3920654028e26f23e0aae3aa3af96df9c824f63938d5461`.
**Governance:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md` · §12 close-ratification-on-own-text · §12.1 remaining-gates enumeration.
**Standing Rule v3:** on-disk canonical.

---

## §1. Owner rulings — verbatim carrier

**OB close acknowledgement (context):**

> OB close: acknowledged as self-ratified per §12 — criteria met on its own text, within band, zero debts. The §12 mechanism working exactly as intended on first use.

**PH-R1 ruling · PH-E1 · Vault-class secret store selection posture:**

> **PH-E1 — α.** Classification-and-contract is the builder-side promise; the store choice is PH-R4's [OWNER] binding, and β would pre-commit a vault stack that binding may override. The annex contract lands as documentation + no-secrets-in-image; the SDK wiring follows the store choice, not precedes it.

**PH-R1 ruling · PH-E2 · Container image posture — single vs dual-image:**

> **PH-E2 — α.** Multi-stage single image, deploy topology chooses how to serve — the split preserved at the layer boundary without assuming pod-multiplicity nobody has ruled. This is "destination-agnostic" applied to packaging, same principle as 9.2a's containers. β/γ both pre-commit infrastructure that PH-R2/R3/R4 haven't named.

**PH-R1 ruling · PH-E3 · `/readyz` parity-count implementation:**

> **PH-E3 — α.** FS enumeration sharing V1-G7's authoritative counter — readiness and the parity gate must never disagree about what parity is, and one counting mechanism guarantees that. γ correctly rejected on honesty grounds; β adds production import risk for nothing.

**PH-R1 ruling · PH-E4 · LLM swap seam public shape (α + one Owner addition):**

> **PH-E4 — α, one addition inside the same ruling:** document the seam, defer the rename — correct, "contained + documented" is the PH-R1 clause and β is a mid-flight refactor with no honesty gain. **Addition:** the seam doc records the BCR annex shape as the binding migration target with its call-site inventory (the two post-cut call sites named), so the PH-R4 swap executes against a written target rather than rediscovering the seam. Documentation content, zero code, no cell change.

**Enhancement promotion · `/api/system/build_info`:**

> **Enhancement — /api/system/build_info: promoted, landing with this execution.** Ruled in rather than deferred because it converts PH-R1's own STAKED claim ("promotion-not-rebuild") from asserted to verifiable — a deployed artifact that states its git SHA is the audit made mechanical. Git SHA + build timestamp + parity_count (same counter as PH-E3), no secrets in the payload. ~1 LoC insert per your note; disclose in the close.

**Band ratification:**

> **Band `[900, 1,700]`: RATIFIED.** α scenario in-band; §4.2 projections are Tier-2 disclosure per §12.1; split-fallback at dev's judgment.

**Close-landing sequence note:**

> Execute → close per standing format. On its close: **mandate-complete** — every BCR §3 item landed or explicitly [OWNER]-bound, and the build's remaining motion is 9.2b on your "proceed."

**Orchestrator directive (verbatim):**

> Execute PH-R1 atomically per §4.1 baseline. Standing Rule v3 in force. Native pytest/jest/playwright only (no e1_tester). Governance §12 auto-ratification-on-own-text applies at close-landing. On successful close, **mandate-complete gate reached** — update PHASE_STATE + PRD accordingly and idle.

---

## §2. Ruling-derived execution requirements

### §2.1 PH-E1 α (secret externalization audit)

- Land audit report at `/app/docs/production_housing/env_findings_v0.md`. Classification per BCR §3.4 annex verbatim: MONGO_URL / JWT_SECRET → vault · LLM_API_KEY / EMERGENT_LLM_KEY → vault (off-platform when swapped per PH-R4) · OBJECT_STORE_CREDS → vault · non-secret vars → config · misclassified/deprecated/orphaned → finding.
- Injection contract documented: env-var interpolation via K8s Secret projection / HashiCorp Vault SDK / cloud-native manager. Vault-class binding at production deploy time (owner-side per PH-R4).
- `.dockerignore` MUST exclude `.env` and any secret-carrying dotfile.
- Zero code change to runtime env-reading paths.

### §2.2 PH-E2 α (multi-stage single Dockerfile)

- Repo-root `Dockerfile`:
  - Build stage: `node:20-alpine` → `yarn install --frozen-lockfile && yarn build`.
  - Runtime stage: `python:3.11-slim` → `pip install -r backend/requirements.txt` → copies frontend build artifact + backend → EXPOSE 8001 → uvicorn CMD (verbatim to current supervisor entry to preserve promotion-not-rebuild).
- Frontend build artifact left available for FastAPI serve OR CDN serve (deploy-time choice).
- HEALTHCHECK: `curl -f http://localhost:8001/api/healthz` per BCR annex verbatim.

### §2.3 PH-E3 α (`/readyz` FS-enumeration sharing V1-G7 counter)

- `/api/healthz` — 200 `{"status": "alive"}` · no auth · no DB touch.
- `/api/readyz` — 200 `{"status": "ready", "parity_count": 31, "expected_parity": 31, "db": "ok"}` OR 503 `{"status": "not_ready", "reason": "..."}` on either check-fail.
- Shared parity counter at `/app/backend/services/health/parity_counter.py` — one authoritative FS-enumeration source used by BOTH `/api/readyz` AND V1-G7 tests. V1-G7 refactored (minimal edit) to import from this shared counter.
- Refusal taxonomy untouched — 503 is infra readiness signal, never a refusal envelope.

### §2.4 PH-E4 α + Owner addition (LLM swap seam doc + call-site inventory)

- Land seam doc at `/app/docs/production_housing/llm_swap_seam.md`.
- Current shape: `services/synisense/shield/llm_router.py::invoke_with_metering(prompt, model_preference, timeout_seconds, system_msg) -> (text, provider, model, usage)`.
- Single-source discipline attest.
- **Owner addition · binding migration target:** BCR annex target shape `complete(messages, temperature, model) -> text` recorded as binding migration target for PH-R4 owner-side LLM account swap.
- **Owner addition · call-site inventory (two post-cut call sites named):**
  - `backend/services/synisense/shield/fluency_synthesizer.py::L182` — Answer Fluency post-Shield synthesis.
  - `backend/services/synisense/shield/brief_synthesizer.py::L116` — Opportunity Briefs post-Shield synthesis.
- Zero code change to `llm_router.py` at PH-R1. Shape rename lands post-PH-R4.

### §2.5 Enhancement promotion · `/api/system/build_info`

- Endpoint at `/app/backend/routers/system_info.py` — `GET /api/system/build_info`.
- Payload shape (Owner-explicit): `{"git_sha": "<40-char full SHA>", "build_timestamp": "<ISO-8601 UTC>", "parity_count": 31}`.
- Parity count MUST use SAME shared counter as `/api/readyz` (no duplicate counting logic).
- Build args `GIT_SHA` + `BUILD_TIMESTAMP` injected via Dockerfile `ARG` + env at build time; container startup reads from env; falls back to git-tree inspection or a "dev" placeholder if not set.
- **No secrets in the payload** (Owner explicit).
- Test coverage: PH-G5 backend cells (endpoint reachable · payload shape · no-secrets grep-negative on payload keys) + Playwright smoke (endpoint reachable + payload shape client-side).

### §2.6 Band ratification

- Ratified: `[900, 1,700]` raw LoC per §9.
- §9 band-relative trichotomy at close:
  - below-bottom (< 900) — Tier-2 driver disclosure
  - in-band ([900, 1,700]) — no disclosure beyond snapshot line
  - above-top (> 1,700) — Tier-2 driver disclosure
- §4.2 raw threshold (1,500) — Tier-2 disclosure-only per §12.1 (non-blocking).
- Split-fallback at dev's judgment (autonomous per §4.1 baseline).

---

## §3. §12 auto-ratification pre-clearance criteria

Per Owner directive: if close-landing satisfies —
- **(a)** named gates green (PH-G1..PH-G6 all green + auxiliary),
- **(b)** rulings + Owner-addition + enhancement attested as applied,
- **(c)** no new Tier-1 escalation surfaced during execution,

— then close ratifies on its own text and **mandate-complete lands with it**. No further Owner turn required for ratification.

**HALT-for-Owner condition:** only if a new Tier-1 surfaces mid-execution outside the Stage A escalation matrix + Owner enhancement promotion.

---

## §4. Standing Rule v3 posture

This ruling record is on-disk canonical. Reply body at execution close carries SHAs (this file + close report + PHASE_STATE + PRD + Dockerfile + env_findings + llm_swap_seam + build_info endpoint tests) + band actual + parity attest + gate roster green + one-line mandate-complete declaration.

---

## §5. Sequence forward (post-close)

- **Mandate-complete gate lands with the PH-R1 close** (Owner-declared).
- **Idle** — no self-dispatch after mandate-complete.
- **9.2b awaits Owner "proceed"** + RMS agreement + hardware at venue.
- PH-R2 / PH-R3 / PH-R4 remain [OWNER]-bound.

═══════════════════════════════════════════════════════════════════

*End of PH-R1 rulings record. Standing Rule v3 · on-disk canonical. All four escalations ruled α with one PH-E4 documentation addition and one Owner-promoted enhancement (`/api/system/build_info`). Band ratified. Mandate-complete pre-cleared for landing at close.*
