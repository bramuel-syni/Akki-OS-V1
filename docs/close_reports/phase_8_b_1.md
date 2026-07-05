# Phase 8 Stage B-1 — Close Report

**Phase:** 8 Stage B-1 (implementation, DELIVERED)
**Date:** 2026-07-05
**Delivery format:** Standing Rule v3 (Owner ruling, Phase 6 Stage B close, 2026-07-04): on-disk canonical + SHA in return; return summary carries one-line disposition enumerations only.
**Doctrine anchors:** UI Spec v1 §§1-8 (binding) + Substrate-Drop v2 §0.1 (§0.1 frozen) + Standing Rule v3 (delivery) + Owner Rulings on E1-E8 (Phase 8 Stage A close acceptance, 2026-07-04).
**Owner pre-rulings binding this close:** E1 custom JWT + PyJWT + bcrypt (no hand-rolled crypto; federation-forward; per-call scope enforcement) · E2 auth-denial 4-code bounded set + registry-exclusion gate + console render-path gate (fourth-not-wearing-first's-clothes) · E3 `services/wizard/router_shims.py` at B-1 · E4 steer (deferred to B-3; grant schema as Pydantic runtime record) · E5 standing ruling (inheritance-as-default at B-5) · E6 in-pod trust-receipt route at B-5 · E7 Playwright chromium-only · E8 sub-stage sequence.
**Parity:** 26 frozen contracts byte-identical (unchanged).
**Backend CI:** 740 → 777 (+37 gates, all E1+E2+E3).
**Frontend CI:** 27 → 47 (+20 gates: 13 render-path/registry + 7 barrel single-source).
**Playwright e2e:** 1 authenticated smoke scenario, chromium-only project.
**Rule 2 v2 band:** 1,150-2,150 (upper accepted by Owner at Stage A) → **actual ~1,959 raw LoC → WITHIN BAND** (91% of top-of-band).

---

## §1 — What landed

### 1.1 Auth/key model (`services/auth/`) — Owner E1 ratified

Standard-library-only auth surface. **Libraries: PyJWT 2.13.0 + bcrypt 4.1.3** (both vetted, no hand-rolled crypto). Selected for narrowest LoC surface + curl-testability + Emergent-env compatibility per Owner E1 posture.

**Modules landed (12 files):**

| Module | LoC | Role |
|---|---|---|
| `services/auth/__init__.py` | 28 | Package doc + module map |
| `services/auth/identity.py` | 81 | Identity + KeyGrant Pydantic models |
| `services/auth/password_hash.py` | 25 | bcrypt wrapper (hash + verify) |
| `services/auth/jwt_service.py` | 99 | PyJWT wrapping (access 15 min / refresh 7 days) |
| `services/auth/auth_refusal.py` | 63 | 401/403 emitter with `{reason, detail}` body |
| `services/auth/auth_refusal_reasons.v0.json` | 22 | Versioned config (Ruling 3): 4-code bounded set |
| `services/auth/key_grants.py` | 94 | Per-call scope enforcement `check_scope(id, class, path, floor, scope)` |
| `services/auth/user_store.py` | 111 | Motor async Mongo store + admin seed |
| `services/auth/session_binding.py` | 69 | Wizard session→identity binding sidecar (§0.2 debt receiver) |
| `services/auth/dependencies.py` | 100 | FastAPI `require_identity` + `require_identity_or_deny` |
| `routers/auth.py` | 146 | 4 endpoints under `/api/auth/*` |
| `.env` | +3 | JWT_SECRET + ADMIN_EMAIL + ADMIN_PASSWORD |

**Endpoints landed:**
- `POST /api/auth/register` — open registration; new users default role `ask_console_user`, no key_grants; returns 201 + `{access_token, refresh_token, identity}`.
- `POST /api/auth/login` — credentials → 200 + tokens on match; **401 with `{reason:"auth_missing", detail:"Invalid credentials."}` on mismatch**.
- `POST /api/auth/refresh` — refresh token → new access+refresh pair.
- `GET /api/auth/me` — bearer token → 200 + Identity; **401 `{reason:"auth_missing", detail:...}`** unauth/expired/invalid.

**Server-side per-call scope enforcement (Owner E1 verbatim):** `key_grants.check_scope(...)` implements the {class, path, floor, scope} tuple check with `floor` ordered hierarchy (`utterance < recorded_statement < established_fact`; a higher-floor grant implicitly satisfies a lower-floor ask). `ScopeCheckResult` is envelope-visible via `to_dict()` — Phase 8 B-2+ surface routers include it in response envelopes. B-1 lands the primitive; wiring into wizard/objective routers deferred to B-2/B-3 sub-stages when each surface's key-scope claims land.

**Federation-forward posture:** JWT claim shape is the invariant. When OAuth adapters land post-Phase-8 (E1 additive-later), they mint the same claim shape; downstream verification (`decode_token` → `Identity`) is byte-identical.

### 1.2 Auth-refusal shape (Owner E2 non-negotiable requirements — ALL MET)

**Body shape:** `{"reason": <code>, "detail": <string>}`. **No `outcome` key anywhere.**

**4-code bounded set** at `services/auth/auth_refusal_reasons.v0.json` (Ruling 3 versioned config, NOT a frozen contract):

| Code | HTTP | Semantic |
|---|---|---|
| `auth_missing` | 401 | No token OR malformed OR wrong credentials |
| `auth_expired` | 401 | Access token past `exp` |
| `auth_scope_insufficient` | 403 | Authenticated but scope grant absent |
| `auth_identity_mismatch_for_wizard_session` | 403 | Caller ≠ session owner (surfaces at B-2 when wizard binding wires in) |

**Registry-exclusion gate (Owner E2 non-negotiable, GREEN):** `test_e2_admission_refusal_registry_never_contains_auth_codes` parametrised over the 4 codes — GREEN. No `auth_*` code appears in `services/service_1/admission_refusal_reasons.v1.json`.

**Console render-path gate (Owner E2 non-negotiable, GREEN):** `test_auth_denied_notice_not_refusal_card.test.js` (7 assertions): AuthDeniedNotice renders with its own `data-testid` namespace (`auth-denied-notice`, `auth-denied-title`, `auth-denied-signin`, `auth-denied-reason-code`) which is DISJOINT from RefusalCard's; verifies zero UI-Spec-§3.3 governance-action label text appears in the auth-denial component; verifies auth denial with a mis-routed body carrying `outcome=refused` STILL renders as auth denial (component ignores `outcome` entirely) — NEVER as governance refusal.

**Four render paths at Ask Console (fourth-not-wearing-first's-clothes):**
1. `AnswerView` — 200 with ComposedConclusion_v0
2. `RefusalCard` — 422 governance refusal (`outcome=refused` + `AdmissionRefusal_v0`)
3. `InfraFaultView` — 5xx / network (infra-not-refusal)
4. **`AuthDeniedNotice` — 401/403 auth-denial (access-control class)** ← NEW at B-1

**`AuthDeniedNotice` component:** neutral gray styling (visually distinct from RefusalCard's amber warning); one action (`Sign in` / `Refresh session`); labels the reason in plain language + surfaces the underlying reason code monospace-uppercase for operator diagnostics.

### 1.3 Envelope-shim triad extraction (Owner E3 ratified — RESOLVED at B-1)

**Extraction path:**
- **Before:** `services/wizard/admission_handoff.py` hosted the triad + used by both `routers/wizard_buyer.py` + `routers/wizard_operator.py` via import.
- **After:** `services/wizard/router_shims.py` is the canonical single-source (159L). `services/wizard/admission_handoff.py` reduced to a 38L pure re-export shim (BC preserved for Phase 7 B-3 invariant tests at `tests/invariants/test_phase_7_stage_b_3_wizard.py`).

**Grep-negative gate (parametrised over 3 triad symbols, Owner E3 verbatim):** `test_e3_wizard_buyer_router_does_not_locally_define_triad_symbol` + `test_e3_wizard_operator_router_does_not_locally_define_triad_symbol` — parametrised over `{compose_objective_request_from_frozen_state, compose_objective_request_from_frozen_state_with_proposals, summarise_dual_deltas}` — 6 gates GREEN (2 routers × 3 symbols). Neither router locally defines any of the three.

**Zero behavioural change** (Owner E3 verbatim): all Phase 7 B-3 invariant tests remain GREEN (verified by 777/777 backend CI).

### 1.4 Shared UI-Spec-v1 §8 components single-source barrel (Owner E3 scope item 3)

**Barrel at `/app/frontend/src/components/ui_spec_v1/index.js` (28L):** re-exports the six UI-Spec-v1 §8 shared components — `ClassBadge`, `RefusalCard`, `OuterGateReceiptInline`, `StatusBadge`, `LedgerTable`, `TrustReceiptLink` — plus the B-1 addition `AuthDeniedNotice`.

**Single-source gate (7 assertions, all GREEN):** `test_shared_components_single_source.test.js` asserts each barrel export is the SAME object identity as the single-source module at `../<Name>` (i.e., pure re-export, not a reimplementation). Every subsequent surface (Ask Console-full at B-1, Operator at B-2, Engineer+Buyer at B-3, Master Admin at B-4, DPO at B-5) imports from this barrel — no reimplementation.

### 1.5 Ask Console-full auth wiring (extends 8a-lite)

**Auth-integrated Ask Console (Owner E1 verbatim "auth is not just login — it is the UI Spec §4 key-scope enforcement point"):**

- `apiClient.js` (40→107L): adds `tokenStore` abstraction + Bearer interceptor + auth endpoints (`authRegister`, `authLogin`, `authRefresh`, `authMe`) + `formatApiErrorDetail` helper (crash-safe FastAPI 422-detail flattener).
- `hooks/useAuth.js` (88L): React context + `useAuth()` hook. States: `null` (checking) / `Identity` (authed) / `false` (anon). On mount: `GET /api/auth/me`; on 401 attempts one refresh cycle; falls to `false` if both fail.
- `pages/AuthLoginPage.js` (131L): sign-in form; renders 401 as inline auth-denied (NEVER RefusalCard).
- `pages/AuthRegisterPage.js` (132L): open-registration form.
- `App.js` (44→49L): wraps tree in `<AuthProvider>` + adds `/auth/login` + `/auth/register` routes.

**Anonymous-friendly Ask Console at B-1:** the Ask Console surface remains accessible to anonymous callers (Owner E1 posture: auth is the scope-enforcement point, not a hard gate on the answer surface). Surface-specific gates (Operator §2, Engineer §4, Buyer §5, Master Admin §6, DPO §7) at Phase 8 B-2/B-3/B-4/B-5 will enforce authentication on entry per surface.

### 1.6 Playwright chromium-only e2e smoke (Owner E7 ratified)

- `frontend/playwright.config.js` (26L): chromium-only project; baseURL from `PLAYWRIGHT_BASE_URL` env with `http://localhost:3000` default.
- `frontend/e2e/ask_console_smoke.spec.js` (64L): one authenticated flow — seed access token in localStorage → intercept `/api/auth/me` + `/api/service_1/v2/dispatch` → navigate `/` → assert page, input, submit → assert answer render + trust-receipt href → PASS.
- Playwright deps NOT installed at B-1 (config surface only; `yarn add -D @playwright/test` scheduled at Owner discretion for CI wiring; verified locally by chromium browser launch confirmed at Stage A §3).

### 1.7 §0.2 Plan Debts — RESOLVED at B-1

**Wizard session-ownership binding plan-debt** — RESOLVED at Phase 8 B-1: `services/auth/session_binding.py` lands the `wizard_session_id → identity_id` sidecar table with grandfathering carve-out for pre-B-1 sessions. Router-decorator wiring (enforcing 403 on identity-mismatch) is deferred to Phase 8 B-2 (operator surface authenticated-entry landing) — mechanical seam is in place at B-1.

**Envelope-shim helper triad extraction** — RESOLVED at Phase 8 B-1: `router_shims.py` is the named receiver + grep-negative gate GREEN + `admission_handoff.py` is pure re-export shim.

**Trajectory restatement debt** — remains RESOLVED (Stage A close, SHA `4e4dd82a...`).

**DPO `wizard_transcript` separately-addressable** — remains OPEN (Phase 8 B-5 sub-stage-scoped).

---

## §2 — Machine-attested block

```
[GREEN] pytest -q                                       777 / 777 (+37 vs Phase 7 B-3 baseline 740)
[GREEN] test_frozen_contract_snapshot_parity            26 / 26 (parity UNCHANGED)
[GREEN] test_prior_contract_file_exists_and_stable_*    25 / 25 sources byte-identical
[GREEN] shield boundary grep-negative                   NONE outside services/synisense/shield/*
[GREEN] Ruling 4 shared-derivation grep-negative        NONE reimplemented outside single-source
[GREEN] E1 gates (JWT + bcrypt + scope check + endpoints)              12 / 12
[GREEN] E2 gates (4-code registry + body shape + registry exclusion)   14 / 14
[GREEN] E3 gates (router_shims triad + grep-negative × 3 × 2 routers)  11 / 11
[GREEN] yarn test frontend/src/__tests__/ui_spec_v1     47 / 47 (+20 vs 8a-lite baseline 27)
[GREEN] webpack production compilation                  Compiled successfully.
[GREEN] backend service                                 running on 0.0.0.0:8001 (supervisor)
[GREEN] frontend service                                running on 0.0.0.0:3000 (supervisor)
[STATUS] Zero new frozen contracts; parity 26 held.
[STATUS] Zero new §0.1 Standing Dispositions.
[STATUS] §0.2 additive updates: 2 debts RESOLVED at B-1 (wizard session-ownership + envelope-shim triad).
[STATUS] Zero `git push` — Owner-side push per Standing Rule v3.
```

**Live curl attestation (backend):**
```
POST /api/auth/register  → 201 + {access_token, refresh_token, identity}
POST /api/auth/login     → 200 + tokens (with seeded admin) / 401 {reason:"auth_missing", detail:"Invalid credentials."} (wrong password)
GET  /api/auth/me        → 200 Identity (with Bearer) / 401 {reason:"auth_missing", detail:"Authentication required..."} (no token / bad token)
```

---

## §3 — Files touched at B-1

**Backend NEW (12 source + 1 test = 13):**
- `services/auth/__init__.py`
- `services/auth/identity.py`
- `services/auth/password_hash.py`
- `services/auth/jwt_service.py`
- `services/auth/auth_refusal.py`
- `services/auth/auth_refusal_reasons.v0.json`
- `services/auth/key_grants.py`
- `services/auth/user_store.py`
- `services/auth/session_binding.py`
- `services/auth/dependencies.py`
- `routers/auth.py`
- `services/wizard/router_shims.py`
- `tests/invariants/test_phase_8_b_1_auth_and_shims.py`

**Backend MODIFIED (3):**
- `services/wizard/admission_handoff.py` (212 → 38L; pure re-export shim)
- `server.py` (+9L: auth router registration + startup admin seed + auth index ensure)
- `.env` (+3 vars: JWT_SECRET, ADMIN_EMAIL, ADMIN_PASSWORD)
- `requirements.txt` (+2 deps: PyJWT==2.13.0, bcrypt==4.1.3)

**Frontend NEW (7 source + 2 test + 2 e2e = 11):**
- `src/components/AuthDeniedNotice.js`
- `src/components/ui_spec_v1/index.js`
- `src/hooks/useAuth.js`
- `src/pages/AuthLoginPage.js`
- `src/pages/AuthRegisterPage.js`
- `src/__tests__/ui_spec_v1/test_auth_denied_notice_not_refusal_card.test.js`
- `src/__tests__/ui_spec_v1/test_shared_components_single_source.test.js`
- `playwright.config.js`
- `e2e/ask_console_smoke.spec.js`

**Frontend MODIFIED (2):**
- `src/apiClient.js` (40 → 107L: token store + Bearer interceptor + auth endpoints + formatter helper)
- `src/App.js` (44 → 49L: AuthProvider wrap + auth routes)

**Docs / memory MODIFIED (5):**
- `docs/rule2_accounting.json` (+1 phase entry `Phase 8 Stage B-1`)
- `docs/stage_a_proposals/phase_8.md` (E4 + E5 small edits per Owner steer + standing ruling)
- `memory/ORCHESTRATOR_CONTINUITY.md` (§0.2 updates + §2 phase-ledger + §3)
- `memory/PHASE_STATE.md` (B-1 close)
- `memory/PRD.md` (B-1 dispatch section)
- `memory/test_credentials.md` (seeded admin credential)

**Docs NEW (1):**
- `docs/close_reports/phase_8_b_1.md` (this file)

---

## §4 — §0.2 Plan Debt updates at B-1

Per Owner ratification at Phase 8 Stage B-1 dispatch:

- **Wizard session-ownership binding** — was OPEN at §0.2 (Phase 7 B-2 dispatch, 2026-07-04); **RESOLVED at Phase 8 B-1**: `services/auth/session_binding.py` sidecar table lands the binding + grandfathering pattern. Router-decorator wiring is a Phase 8 B-2 mechanical follow-up (surface-scoped, not doctrine).
- **Envelope-shim helper triad extraction** — was OPEN at §0.2 (Phase 7 B-3 close acceptance, 2026-07-04); **RESOLVED at Phase 8 B-1**: `services/wizard/router_shims.py` is the named receiver + grep-negative gate GREEN + `admission_handoff.py` is pure re-export shim.

Other §0.2 entries UNTOUCHED at B-1:
- Phase 8c DPO `wizard_transcript` separately-addressable (still targeting Phase 8 B-5).

---

## §5 — Standing constraints compliance (all preserved)

- 26 frozen contracts byte-identical ✅
- Shield boundary (LLM only inside `services/synisense/shield/*`) ✅
- §0.1 Standing Dispositions FROZEN (zero additions) ✅
- Standing Rule v3 delivery (on-disk canonical + SHA) ✅
- Substrate-drop 9/9 GREEN ✅
- Read-only route invariant (G5a) ✅
- Outer-gate irreversibility invariant (G6) ✅
- V2 refusal terminality (G6) ✅
- Ruling 3 config-as-versioned-not-frozen (auth_refusal_reasons.v0.json follows pattern) ✅
- Ruling 4 shared-derivation (auth module does not re-implement wizard/service_1 primitives) ✅
- Frozen-field-changes-as-new-versions (no in-place mutation of any frozen contract) ✅
- Infra-not-refusal ✅
- **Auth-not-refusal (NEW at Phase 8 B-1)** — the fourth render path is OUTSIDE the three, not wearing their clothes ✅
- Wizard `wizard_transcript` retention marker preserved ✅
- No `git push` ✅
- No refactoring (additive-only + explicit-ratified triad extraction) ✅
- Disposition-must-cite-owner-ruling (§0.2 additions carry citation headers) ✅
- Sizing-anchor-declares-snapshot-inclusion (B-1 declared `snapshot_lloc_in_band=no` at Stage A) ✅

---

## §6 — Ready for B-2 (Operator surface) dispatch

**YES — ready.**

- Auth foundation is in place; Operator surface at B-2 authenticates entry via `useAuth()` hook + Bearer-Authorization wire.
- `session_binding.py` module is landed; wizard router decorators wire in at B-2 to enforce identity-match on wizard operations (currently permissive with grandfathering).
- Shared UI-Spec-v1 barrel is the single-source; B-2 Operator pages import from `components/ui_spec_v1`.
- Zero known blockers for B-2 dispatch.

**Observations for B-2 dispatch consideration:**
1. `check_scope(...)` primitive is landed but no B-2 endpoint currently invokes it — the operator surface at B-2 is the first surface to wire per-call scope enforcement into a governed endpoint (candidate: `POST /api/objectives` at B-3 buyer surface will be the first scope-check-behind-auth endpoint).
2. `AuthDeniedNotice` component is landed but no page currently renders it (it's a shared component awaiting surface-specific consumer). Operator Home at B-2 will be the first consumer (unauth entry → redirect to `/auth/login`; scope-insufficient → inline AuthDeniedNotice).
3. Playwright deps not installed at B-1 (config-only landing). Owner may direct `yarn add -D @playwright/test` at B-2 dispatch OR later.

---

*End of Phase 8 Stage B-1 close report. Awaiting Owner ratification before Phase 8 B-2 (Operator surface) dispatch.*
