# 8-EXT Stage A — Design Proposal (Dual-actor engineer scoping)

**Design date:** 2026-07-08
**Design authority:** Owner dispatch 2026-07-08 (post-9.1+9.3 close ratification; standing sequence BCR §5.1 point 5).
**Scope:** BCR §3.9 (dual-actor engineer surface, EE-R1..R4, EE-G1..G4) + UI Spec v2.1 §5.4 (Engineer screens own-apps-only surface) — small phase per Owner.

**Sequence position (BCR §5.1 line 314 verbatim):** *"8-EXT dual-actor engineer scoping (3.9) — small; after B-5b, before Phase 9 Stage B."* B-5b is closed; 8-EXT is the next queued builder-side item by the existing ruling. Independent of Sub-stage 9.2 [OWNER] facts.

**Standing constraints (all binding):**
- Standing Rule v3: this proposal lives on disk; reply body is SHA + escalation-ID enumeration + band + line-range map only.
- Standing Correction: matrix-enumerated sizing.
- Standing state-conflict anti-rule: NO HTTP 409 anywhere in 8-EXT diff (E5).
- E7 middle-dot U+00B7 strict on binding copy (list-separators only per P9-E6 informational); em-dash preserved on syntactic pauses.
- 28 frozen contracts + snapshots UNTOUCHED (parity 28 post-9.1). Identity is UNFROZEN service-layer per Ruling 3 (verbatim comment at `backend/services/auth/identity.py:1-11`) — role registry can expand additively without touching frozen surfaces.
- Amortisation Divergence Class codified per B-5b close + Owner P9 ratification.
- Owner rulings pre-carried by SHA: E1–E7, R-1..R-7, B5b-E1..E5, P9-E1..P9-E7 — all cited by SHA at §Authorities.

**Authority-source SHAs (for citation stability):**

| Source | Path | SHA-256 | Cited sections |
|---|---|---|---|
| BCR v1.4.1 | `docs/mandates/RMS_Build_Completion_Requirements_v1_4.md` | `ce5206c9e244fe58edb6824f785077c1c835bdf3f5b347f6a4fb98c036212524` | §3.9 lines 237–253 (EE-R1..R4 + EE-G + role-scoping matrix) verbatim; §5.1 line 314 (sequencing verbatim). |
| UI Spec v2.1 | `docs/mandates/RMS_UI_Specification_v2_1.md` | `ef6da4b498117608a3091033b5cfa43571ad8a7a38b5954cae7c4a1a698de5e2` | §5.4 lines 101–114 (Engineer screens own-apps-only matrix + RULE verbatim); §5.6 lines 121–122 (external_engineer definition). |
| Rulings record post-P9-E7 | `docs/rulings/phase_9_p9_e1_to_e7.md` | `f62c89370b8adbb1392ab7ed5584dc851bca6b521609b268481fcfe593990c83` | P9-E3 α capabilities-claim + 4-code registry closed condition pre-carry. |
| 9.1 close (empirical baseline) | `docs/close_reports/phase_9_sub_stage_9_1.md` | `d8c1abfd6d01640c58987f61ee6a764929c1bae6efa244236c806470824828b1` | Backend Pytest cell effective rate empirical basis. |
| 9.3 close (empirical baseline) | `docs/close_reports/phase_9_sub_stage_9_3.md` | `79dd180debcfc9d42dd1727606a40b3fc4648a2acd4bbc97d6bfa464a5b37329` | Playwright chromium smoke effective rate empirical basis. |
| rule2_accounting.json (post-9.3) | `docs/rule2_accounting.json` | `a98ccbbb8049ea38ffcff0a47f4559b20e8d5f9e5863234fe1121284da758b04` | Velocity baseline with new empirical rates codified. |

## §Substrate already landed (Owner-named — DO NOT re-price)

Per Owner dispatch verbatim: *"Its substrate is fully landed: key_class internal|external, grant CRUD with ledger emission (B-3), scope enforcement (B-1), the three Engineer screens."*

| Substrate item | On-disk file paths + line ranges |
|---|---|
| **key_class internal\|external** (UI Spec §4.1 dichotomy on request/response) | `backend/services/auth/engineer_key_grant.py:27, 164, 179, 243` (Pydantic `Literal["internal", "external"]`) · `backend/services/auth/identity.py:48` (KeyGrant.key_class). |
| **Grant CRUD + ledger emission (B-3)** | Router: `backend/routers/engineer.py:4-7, 50` (`POST /api/engineer/key_grants` + `GET /api/engineer/key_grants` + `POST /api/engineer/key_grants/{gid}/revoke`). Service: `backend/services/auth/engineer_key_grant_service.py:42-83` (mint + persist). Ledger: `backend/services/auth/engineer_key_grant_ledger.py:94` (`record_engineer_key_grant_event`). Contract: `backend/services/auth/engineer_key_grant.py:243` (`EngineerKeyGrant` request/persistence). |
| **Scope enforcement (B-1)** | `backend/services/auth/key_grants.py:65` (`check_scope()` primitive) · `backend/services/auth/identity.py:33-82` (Identity + KeyGrant + role registry — RoleName Literal at line 22-30). B-1 dependency: `backend/services/auth/dependencies.py:require_identity` (post-P9-E3 α: worker_jwt on non-worker → 403 auth_scope_insufficient). |
| **3 Engineer screens** | `frontend/src/pages/engineer/EngineerRegisterAppPage.js` (338 LoC) · `frontend/src/pages/engineer/EngineerFirstCallPage.js` (162 LoC) · `frontend/src/pages/engineer/EngineerAdministerPage.js` (177 LoC). API surface in `frontend/src/apiClient.js:134-149` (`engineerListKeyGrants` + `engineerRegisterKeyGrant` + `engineerRevokeKeyGrant`). |
| **`engineer` role** | `backend/services/auth/identity.py:24` (`"engineer"` in RoleName Literal, alongside operator/buyer/master_admin/dpo/ask_console_user/admin). |

**Boundary of DO-NOT-re-price:** all rows above. 8-EXT builds ON TOP of these — no re-implementation, no duplication.

---

## §1. Cell-density assumption (Owner-binding, empirically anchored)

Per Owner ratification (2026-07-08 dispatch) verbatim: *"codify both rates at next Stage A per §1.4 — backend Pytest 12 LoC/cell when shared helpers cover ≥3 cells; Playwright 9 LoC/cell with data-testid selectors. Same disposition as B-5b's amortisation finding: empirical rate with a named trigger is accuracy, not padding."*

### §1.1 Empirical baseline (Sub-stage 3 + B-5b + 9.1/9.3 measured, on-disk verifiable)

| Cell type | Empirical LoC/cell | Named trigger | Source |
|---|---:|---|---|
| Backend Pytest cell (standalone) | **22 LoC/cell** | none (fallback rate) | Sub-stage 3 993L / 45 cells; B-5b 445L / ~20 non-B5b-G4 cells (matched). |
| Backend Pytest cell (shared-helper amortised) — **NEW, Owner-codified 2026-07-08** | **12 LoC/cell** | ≥3 cells share `_mint_*()` / `_*_token()` / `_access_*()` helpers | Sub-stage 9.1: 47 backend cells / ~564 test LoC = ~12 LoC/cell effective. Cited: 9.1 close SHA `d8c1abfd…` §5 composition bullet (d). |
| Backend LB gate (parametrised, multi-class) | **35 LoC/cell** | none | 17 LB gate cells / ~595 LoC across Sub-stage 3 + B-5b. |
| Frontend Jest structural cell (standalone) | **16 LoC/cell** | none | Sub-stage 3 98L / 6 cells. |
| Frontend Jest form-writer cell (standalone) | **28 LoC/cell** | none | B-5b projected; actual amortised (below). |
| Frontend Jest form-writer cell (amortised) | **~22 LoC/cell** | ≥2 form components share a base | B-5b actual. |
| Playwright chromium smoke (standalone) | **32 LoC/cell** | none (fallback rate) | Sub-stage 3 127L / 4 cells. |
| Playwright chromium smoke (data-testid amortised) — **NEW, Owner-codified 2026-07-08** | **9 LoC/cell** | data-testid selectors on the target components (not text-scrape / role-scrape) | Sub-stage 9.3: 5 smokes / ~45 LoC = ~9 LoC/cell effective. Cited: 9.3 close SHA `79dd180d…` §5 composition bullet (e). |
| Playwright chromium smoke (form-writer standalone) | **48 LoC/cell** | none | B-5b projected. |
| Playwright chromium smoke (form-writer amortised) | **~35 LoC/cell** | ≥2 form components share a base | B-5b actual. |

### §1.2 Amortisation Divergence Class (Owner-accepted at B-5b close + P9 ratification)

Named trigger doctrine: **≥2 endpoints (or components) sharing a base `_impl` (or shared component) → apply amortised rate**. Fewer than 2 sharing → standalone rate. **NEW at P9 close 2026-07-08:** shared-helper triggers extend to test-side cells (backend Pytest ≥3-share; Playwright data-testid) as codified in §1.1.

| Cell / impl class | Standalone rate | Amortised rate | Trigger | Empirical basis |
|---|---:|---:|---|---|
| Backend endpoint impl LoC | 80 LoC/endpoint | **40 LoC/endpoint** | ≥2 endpoints share a common `_impl` | B-5b `_rulebook_write_impl`. |
| Frontend form-writer component LoC | 120 LoC/component | **~55 LoC/component** | ≥2 components share a base | B-5b `RuleClassWriter`. |
| UI-form-writer Jest cell | 28 LoC/cell | **~22 LoC/cell** | ≥2 form components share a base | B-5b. |
| UI-form-writer Playwright smoke | 48 LoC/cell | **~35 LoC/cell** | ≥2 form components share a base | B-5b. |
| **Backend Pytest cell — shared-helper (NEW)** | 22 LoC/cell | **12 LoC/cell** | **≥3 cells share `_mint_*()` / `_*_token()` / `_access_*()` helpers** | **9.1: 47 cells / 564 LoC effective.** |
| **Playwright chromium smoke — data-testid (NEW)** | 32 LoC/cell | **9 LoC/cell** | **data-testid selectors on the target components (not text-scrape / role-scrape)** | **9.3: 5 smokes / 45 LoC effective.** |

**Note (Ruling 5 discipline):** empirical rates with named triggers are ACCURACY, not padding (Owner verbatim 2026-07-08). Miss + disclosure > pad + hide.

### §1.3 8-EXT-specific cell classes (rates stated for deterministic re-derivation)

| Impl / cell class | Standalone rate | Amortised rate | Trigger applied at §3 |
|---|---:|---:|---|
| Role Literal expansion in identity.py | 3 LoC (single-line addition) | — | Not-sharable single-line change → **standalone applied** |
| Scope-enforcement helper (`require_own_scope_or_deny`) | ~35 LoC | — | Single helper (no sharing target) → **standalone applied** |
| Engineer router modification (own-scope enforcement wired into 3 endpoints) | 80 LoC/endpoint | **40 LoC/endpoint** | 3 endpoints share `require_own_scope_or_deny` → **amortised applied** |
| Invited-approved onboarding (EE-R3 [STAKED]) — invite endpoint + approval endpoint | 90 LoC/endpoint (P9 worker-endpoint precedent) | **~50 LoC/endpoint** | 2 endpoints share `_onboarding_state_impl` helper → **amortised applied** |
| Engineer screen scoping (view-level filter alongside server-side gate per EE-R4) | 60 LoC/screen | **~30 LoC/screen** | 3 screens share `useEngineerScope(identity)` React hook → **amortised applied** |
| Backend Pytest cell (EE-G1..EE-G4) | 22 LoC/cell | **12 LoC/cell** | ≥3 cells share `_mint_external_engineer_token()` / `_mint_internal_engineer_token()` / `_seed_foreign_grant()` — trigger fires per §1.2 empirical | **amortised applied** |
| Frontend Jest structural cell | 16 LoC/cell | — | Screen-scoping cells small enough; no amortisation needed | **standalone applied** |
| Playwright chromium smoke (data-testid) | 32 LoC/cell | **9 LoC/cell** | data-testid selectors on Engineer screens (already present per pre-landed screens) | **amortised applied** |

### §1.4 Re-derivation rule (Owner-binding, unchanged from Amendment G/I template)

Any Owner ruling that adds/removes an EE-R requirement, changes the auth-refusal code registry, adds a JWT class, reshapes the amortisation trigger, or reshapes the onboarding flow MUST re-derive the band using §1.1 + §1.2 + §1.3 rates. NO padding, NO buffering up front. Miss + disclosure > pad + hide.

---

## §2. Matrix enumeration (deliverables per Standing Correction)

### §2.1 Backend substrate (EE-R1..R4 enforcement points)

#### §2.1.1 Identity role expansion (EE-R1 verbatim)

BCR §3.9 EE-R1 line 239 verbatim: *"A role external_engineer is added to identity.roles. JWT mechanics unchanged; the 4-code auth registry unchanged — external-scope denials are auth_scope_insufficient, access-control class, never outcome=refused."*

| # | Path | Kind | Purpose |
|---|---|---|---|
| 2.1.1.a | `backend/services/auth/identity.py:22-30` | Modify Literal | Add `"external_engineer"` to `RoleName` Literal (additive; 7 → 8 role names; Identity unfrozen service-layer per Ruling 3). |
| 2.1.1.b | Optional: `internal_engineer` — see P8E-E5 | Modify Literal | If Owner rules add `"internal_engineer"` alongside (naming symmetry) OR retain existing `"engineer"` as internal. Escalation at §5. |

**Parity impact:** none. Identity is unfrozen (comment at line 5: *"Identity is an unfrozen service-layer Pydantic model per Ruling 3"*). Frozen 28 remain byte-identical (V1-G7 GREEN forward).

#### §2.1.2 Server-side own-scope gate (EE-R2 + EE-R4)

BCR §3.9 EE-R2 line 240 verbatim: *"View scoping: an external_engineer sees Register / First call / Administer scoped to their own apps, keys, usage, and refusal health — and NEVER other parties' apps, estate contents, fleet, pricing, or any master-admin control."*

BCR §3.9 EE-R4 line 242 verbatim: *"Every externally reachable endpoint enforces scope server-side — view-layer filtering alone fails review. Enforcement rides the existing B-1 scope primitive; no parallel mechanism."*

| # | Path | Kind | Purpose |
|---|---|---|---|
| 2.1.2.a | `backend/services/auth/engineer_scope.py` | New | `require_own_scope_or_deny(identity, resource_owner_email)` helper. Returns 403 `auth_scope_insufficient` if `identity.roles` contains `external_engineer` (not `internal_engineer`) AND `resource_owner_email != identity.email`. Rides B-1 scope primitive (no parallel mechanism per EE-R4). |
| 2.1.2.b | `backend/routers/engineer.py` (modify) | Modify | Wire `require_own_scope_or_deny` into 3 existing endpoints (list / create / revoke) via shared `_own_scope_impl` helper. Amortised (§1.3 trigger). |

#### §2.1.3 Invited-approved onboarding (EE-R3 [STAKED])

BCR §3.9 EE-R3 line 241 verbatim: *"Onboarding [STAKED]: external engineers are invited and approved by an internal engineer; grant issuance to the external class emits the ledger row exactly as built at Phase 8 B-3. Open self-registration is a commercial decision, out of scope here."*

**Scope:** [STAKED] means minimal skeleton — invited-approved landing shape without the full commercial-decision surface.

| # | Path | Kind | Purpose |
|---|---|---|---|
| 2.1.3.a | `backend/services/auth/onboarding.py` | New | `_onboarding_state_impl` state machine: pending_invite → approved → active. Minimal Mongo persistence. |
| 2.1.3.b | `POST /api/engineer/onboarding/invite` | New endpoint | Internal engineer mints an invite token (email + optional apps allowlist). |
| 2.1.3.c | `POST /api/engineer/onboarding/approve` | New endpoint | Internal engineer approves an invite → mints JWT with `external_engineer` role. |
| 2.1.3.d | `backend/routers/engineer.py` (extension) | Modify | Register 2.1.3.b + 2.1.3.c on existing engineer router. Amortised via `_onboarding_state_impl`. |

Ledger emission on approval: reuses existing `record_engineer_key_grant_event` pattern (no new ledger row class); persisted as `engineer_onboarding_approved` variant via `stamp_audit`.

### §2.2 Frontend surface (Engineer screens own-apps-only scoping)

UI Spec v2.1 §5.4 line 102 verbatim: *"Two roles, one console, identical screens, different scope — enforcement server-side, never view-layer filtering alone."*

Per Owner: extension of existing screens — no new surface built.

| # | Path | Kind | Purpose |
|---|---|---|---|
| 2.2.1 | `frontend/src/hooks/useEngineerScope.js` | New (shared) | Shared hook returning `{ isExternal, ownEmail, scopeFilter(resource) }`. Amortisation base for §1.3 3-screen amortised rate. |
| 2.2.2 | `frontend/src/pages/engineer/EngineerRegisterAppPage.js` (modify) | Modify | Consume `useEngineerScope`; render own-apps-only list; server-side own-scope enforcement is the authority (view-level is defence-in-depth per EE-R4). |
| 2.2.3 | `frontend/src/pages/engineer/EngineerFirstCallPage.js` (modify) | Modify | Same pattern (own keys / grants only). |
| 2.2.4 | `frontend/src/pages/engineer/EngineerAdministerPage.js` (modify) | Modify | Same pattern. |
| 2.2.5 | `frontend/src/pages/engineer/OnboardingInvitePage.jsx` | New | Internal-engineer-only invite page (EE-R3 [STAKED]). Small — invite email input + apps allowlist + issue-invite button. |
| 2.2.6 | `frontend/src/App.js` | Modify | Route `/engineer/onboarding` → `OnboardingInvitePage`. |

**RULE citation** (UI Spec §5.4 line 114 verbatim): *"External-scope denials are 403 access-control class ({reason, detail}) — never outcome=refused, never the refusal card."*

Enforced at 2.1.2.a: response body carries `{reason: "auth_scope_insufficient", detail}`, NEVER `outcome: "refused"`. Attested at EE-G2 + EE-G3.

### §2.3 Named gate roster (EE-G1..EE-G4)

BCR §3.9 EE-G line 243 verbatim: *"Gates: EE-G1 test_external_engineer_sees_only_own_apps; EE-G2 test_external_scope_enforced_server_side (direct API probe, not UI); EE-G3 test_external_cannot_reach_admin_or_fleet_routes (403, access-control body); EE-G4 first-commit per-surface smokes per standing pattern."*

| Gate | Cell(s) | Description |
|---|---:|---|
| **EE-G1** `test_external_engineer_sees_only_own_apps` | 1 | List endpoint (`GET /api/engineer/key_grants`) with `external_engineer` role returns ONLY grants owned by identity.email; foreign grants absent from response body. |
| **EE-G2** `test_external_scope_enforced_server_side` | 1 | Direct API probe (bypass UI): `external_engineer` GETs foreign `grant_id` → 403 `auth_scope_insufficient`. Access-control body shape `{reason, detail}` — never `outcome=refused`. |
| **EE-G3** `test_external_cannot_reach_admin_or_fleet_routes` | **parametrised over N=4 admin/fleet routes** — /api/master_admin/audit_trail + /api/master_admin/tightening/suspend + /api/compliance/disclosure_thresholds + /api/checker/pending. Each returns 403 `auth_scope_insufficient` (existing 4-code registry; P9-E3 α condition 1 pre-carried). | 1 |
| **EE-G4** `first-commit per-surface smokes` — Playwright chromium × 3 screens (Register / First call / Administer) proving own-scope render for external_engineer + full view for internal_engineer. | 3 (data-testid amortised) |

**Total EE-G roster: 3 backend cells + 3 Playwright cells = 6 named-gate cells.**

### §2.4 Onboarding flow (invited-approved, EE-R3 [STAKED])

Skeleton per Owner directive verbatim: *"invited-approved onboarding as staked"*.

| Step | Actor | Endpoint / UI | Persistence |
|---|---|---|---|
| 1. Invite | internal_engineer | `POST /api/engineer/onboarding/invite` OR `OnboardingInvitePage` | `engineer_onboarding_invites` Mongo collection, state=pending_invite. |
| 2. Approve | internal_engineer | `POST /api/engineer/onboarding/approve` | state=approved → JWT with `external_engineer` role minted; ledger emission via existing `engineer_key_grant_ledger` pattern (`stamp_audit.data_class = engineer_onboarding_approved`). |
| 3. Onward key grants | external_engineer | existing `POST /api/engineer/key_grants` | Own-scope enforced per EE-R4 at 2.1.2.a; existing B-3 ledger emission unchanged (BCR §3.9 EE-R3 verbatim: *"grant issuance to the external class emits the ledger row exactly as built at Phase 8 B-3"*). |

Open self-registration REJECTED per BCR §3.9 EE-R3 verbatim: *"Open self-registration is a commercial decision, out of scope here."*

### §2.5 Endpoint × auth × posture matrix (EE-R1..R4 coverage)

Per each engineer endpoint (list / create / revoke × auth × posture):
- 4 role-scope postures (internal_engineer full-view · external_engineer own-only · external_engineer foreign-resource → 403 · anonymous → 401).
- 1 malformed-payload posture per state-changing endpoint.
- **= 5 postures × 3 engineer endpoints = 15 cells** + **4 EE-G3 admin-fleet-403 cells** = **19 backend Pytest cells** total in §2.5.

Amortised @ 12 LoC/cell (shared `_mint_external_engineer_token()` / `_mint_internal_engineer_token()` / `_seed_foreign_grant()` — trigger fires on ≥3-share).

### §2.6 Contract byte-identity + freeze-prior (§2.1.1 informational)

Identity is UNFROZEN per Ruling 3 (verbatim comment at `identity.py:1-11`). RoleName Literal expansion (7 → 8) requires NO contract snapshot bump — the frozen 28 remain byte-identical.

However, **V1-G7 byte-identity assertion at 8-EXT close verifies all 28 pre-existing snapshots stay byte-identical** (assertion-set unchanged; no additive parity bump this phase). 1 cell reserved for this attestation.

---

## §3. Band derivation (matrix-derived, cell-density-applied — no padding)

### §3.1 Cell count total

| Bucket | Cells |
|---|---:|
| Backend Pytest — endpoint × auth × posture + EE-G3 (§2.5) | 19 |
| Backend Pytest — EE-G1 own-apps-only (§2.3) | 1 |
| Backend Pytest — EE-G2 server-side scope enforcement (§2.3) | 1 |
| Backend Pytest — onboarding flow (§2.4, 2 endpoints × 2 postures) | 4 |
| Backend Pytest — role Literal expansion attestation | 1 |
| Backend Pytest — no HTTP 409 standing anti-rule (§P scan) | 1 |
| Backend Pytest — V1-G7 byte-identity 28 (§2.6 attestation) | 1 |
| Frontend Jest — 3 screens × own-scope-render + full-view-render | 6 |
| Frontend Jest — `useEngineerScope` hook | 2 |
| Frontend Jest — `OnboardingInvitePage` | 2 |
| Playwright chromium — EE-G4 first-commit per-surface (3 screens × 2 posture: internal/external) | 3 (per gate roster) |
| Playwright chromium — onboarding invite happy path | 1 |
| **Total cells (8-EXT)** | **42** |

### §3.2 LoC derivation (matrix × cell-density per §1)

| Bucket | Cells | LoC/cell | Subtotal |
|---:|---:|---:|---:|
| Backend Pytest — endpoint × auth × posture (§2.5, amortised via shared token helpers) | 19 | **12** | 228 |
| Backend Pytest — EE-G1 + EE-G2 + role-Literal + no-409 + V1-G7 (5 cells, amortised) | 5 | **12** | 60 |
| Backend Pytest — onboarding flow (§2.4, amortised) | 4 | **12** | 48 |
| Frontend Jest — 3 screens × own-scope + full-view (standalone) | 6 | 16 | 96 |
| Frontend Jest — `useEngineerScope` hook + `OnboardingInvitePage` (standalone) | 4 | 16 | 64 |
| Playwright chromium — EE-G4 3 screens × 2 postures + onboarding smoke (data-testid amortised) | 4 | **9** | 36 |
| **Test LoC subtotal** | **42** | | **532** |
| Backend impl — identity role Literal (§2.1.1, standalone, single-line) | | | 3 |
| Backend impl — `engineer_scope.py` (§2.1.2.a, standalone) | | | 35 |
| Backend impl — engineer router modification (§2.1.2.b, amortised 3 endpoints via `_own_scope_impl`) | | | 120 (3 × 40) |
| Backend impl — onboarding (§2.1.3, amortised via `_onboarding_state_impl`; 2 endpoints @ 50 + shared 90) | | | 190 |
| Backend impl — server.py (no delta; engineer router already registered) | | | 0 |
| Frontend impl — `useEngineerScope.js` (shared hook, §2.2.1) | | | 40 |
| Frontend impl — 3 engineer screens modification (§2.2.2–2.2.4, amortised) | | | 90 (3 × 30) |
| Frontend impl — `OnboardingInvitePage.jsx` (§2.2.5) | | | 55 |
| Frontend impl — `App.js` route (§2.2.6) | | | 2 |
| Frontend impl — `apiClient.js` extension (2 onboarding endpoints) | | | 12 |
| **Impl LoC subtotal** | | | **547** |
| **Grand total point-estimate (raw LoC)** | | | **~1,079** |

### §3.3 Owner-anchored band (matrix-derived, no padding)

**Point estimate:** ~1,079 raw LoC across 42 cells.

**Anchored band:** `[900, 1,180]` raw LoC.

Rationale (rates per §1.1 + §1.2 + §1.3; shave/cushion per Amendment I §3.3 pattern):
- **Bottom-of-band (900):** ~17% shave below point-estimate (1,079 × 0.83 = 895 → 900 rounded). Accounts for further amortisation surfaces discovered at execution (e.g. deeper engineer-router `_own_scope_impl` sharing beyond 3 endpoints if EE-G3 admin-fleet 403 helpers reuse the same posture assertion helpers as EE-G2).
- **Top-of-band (1,180):** ~9% cushion above point-estimate (1,079 × 1.09 = 1,176 → 1,180 rounded). Reflects:
  - Small unknowns on `OnboardingInvitePage` UI copy alignment (UI Spec §5.4 is authoritative but does not specify onboarding-invite-page copy verbatim).
  - Possible extra parametrisation on EE-G3 negative-gate if Owner rules N > 4 admin/fleet routes.

**Small phase per Owner** — band lands well below Phase 9 [2,850, 3,650] and below B-5b [2,940, 3,560].

### §3.4 Re-derivation trigger table (rates unchanged)

| Ruling shape | Re-derivation direction |
|---|---|
| Owner rules `internal_engineer` also joins RoleName Literal (P8E-E5 β) | +1 impl LoC (single-line addition) + 1 test cell attesting both role literals → +~13 LoC |
| Owner rules onboarding EE-R3 [STAKED] beyond invited-approved skeleton | +30–80 LoC per additional endpoint (per §1.3 amortised rate) |
| Owner rules EE-G3 admin/fleet N > 4 routes | +12 LoC/cell × additional N (amortised) |
| Owner rules new 4-code refusal-registry entry (governance ruling required) | +40 LoC contract + registry update; +2 test cells |
| Owner rules onboarding invite-token as new JWT class (P8E-E3 β) | +90 LoC (new class parallel to worker JWT); +5 negative-gate cells |
| Owner rules copy string with middle-dot / em-dash contact | +0 cells (existing cells assert verbatim); +~3 LoC impl |

**Discipline preserved (Ruling 5):** band is stop-and-judge, not a target. Miss + disclosure. No mid-execution restatement.

---

## §4. Dispatch discipline

### §4.1 Baseline atomic commit (single commit, tests + impl + UI + gate roster together)

Per §4.1 baseline pattern (B-5b + 9.1+9.3): 8-EXT lands as ONE atomic commit — Identity role expansion + scope helper + router modifications + Engineer screens + onboarding skeleton + EE-G1..G4 roster + Jest cells + Playwright chromium smokes, all in a single dispatchable slice.

No non-splittable pairing surface adjacent (in contrast to B-5b's write-enablement + retrofit pairing). 8-EXT is a role-scoping extension of pre-landed substrate — one atomic first-commit satisfies §4.1.

### §4.2 Pre-authorized split thresholds (Ruling B5b-E5 template)

Per Ruling B5b-E5 pattern (empirical band-aware thresholds):

**If actual 8-EXT delivery exceeds **≥1,500 LoC OR ≥60 cells** → autonomous split into 8-EXT.a (role + scope + gates, backend-only) + 8-EXT.b (Engineer screens scoping + onboarding UI, frontend-only); disclose in close report; no Owner round-trip.**

- LoC threshold 1,500 = ~1.4× point-estimate 1,079 (matches B5b-E5 threshold-multiplier).
- Cell threshold 60 = ~1.4× projected 42 cells.

**Pairing:** none. 8-EXT.a (backend) is complete standalone; 8-EXT.b (frontend) consumes 8-EXT.a's server-side gates but adds no new server surface.

**Decision rule (dev-autonomous, disclosed at close per Ruling 5):** attempt §4.1 baseline. Report chosen path in close.

### §4.3 Dispatch-independence statement

Per Owner dispatch verbatim: *"[8-EXT] it is not blocked on Phase 9."* Confirmed:
- **8-EXT does NOT depend on Sub-stage 9.2 [OWNER] facts** (Extraction GPU half). 9.2 continues to wait for 9.2-OWN-1..3.
- **8-EXT does NOT depend on artifact store (§3.2, sequenced AFTER 8-EXT per Owner).**
- **8-EXT does NOT depend on transform forms (§3.7, sequenced AFTER artifact store).**
- **8-EXT DOES close-unblock Phase 9 Stage B** per BCR §5.1 line 314: *"after B-5b, before Phase 9 Stage B."* On 8-EXT ratification, Phase 9 Stage B becomes dispatchable (subject to 9.2 [OWNER] facts landing — which remain Owner-side).

**Report cadence (per Owner P9 pattern):** end of STEP B (this proposal); at any §4.2 threshold trigger; end of 8-EXT close (with cell/LoC actuals + gate roster verification); any hard blocker.

---

## §5. Escalations

Enumerated per Standing Correction. Six escalations surfaced from BCR §3.9 + UI Spec §5.4 verbatim + Standing 28 adjacency + P9-E3 precedent chain.

### §5.1 P8E-E1 — `external_engineer` role addition to Identity RoleName Literal

**Class:** governance-semantic contact + Standing 28 adjacency check.

**Question:** BCR §3.9 EE-R1 line 239 verbatim: *"A role external_engineer is added to identity.roles. JWT mechanics unchanged; the 4-code auth registry unchanged."* Identity is UNFROZEN service-layer per Ruling 3 (comment at `identity.py:5`). Additive Literal expansion 7 → 8. Does this trip any parity assertion (V1-G7 or otherwise), or is it a pure service-layer addition?

**Authority-source language:** BCR §3.9 EE-R1 line 239 (quoted above); Ruling 3 (state-machine corrections + service-layer unfrozen-Pydantic policy); `identity.py:5` comment: *"The frozen contracts at parity 26 are UNTOUCHED; Identity is an unfrozen service-layer Pydantic model per Ruling 3."*

**Options:**
- (α) Additive-only Literal expansion — `external_engineer` joins `RoleName` at `identity.py:22-30`; no frozen contract touched; V1-G7 asserts 28 pre-existing byte-identical (unchanged); parity NOT bumped. Matches Ruling 3 unfrozen posture.
- (β) Bump Identity to `Identity_v2` (versioned bump, matching P9-E1 α FREEZE prior on env-boundary crossings). Argues Identity crosses a caller/server boundary. RULED OUT: Identity is JWT-payload-carried and reconstructed server-side; no cross-environment freeze prior applies.
- (γ) Land `external_engineer` as a distinct `capabilities` claim on a new JWT class (like P9-E3 α worker JWT). RULED OUT: BCR §3.9 EE-R1 verbatim states *"JWT mechanics unchanged"* — no new JWT class.

**Recommended:** (α) additive Literal expansion. Matches BCR §3.9 EE-R1 verbatim + Ruling 3 explicit unfrozen posture. Owner ruling requested for the discipline attestation (V1-G7 assertion set stays at 28 with parity count unchanged).

### §5.2 P8E-E2 — Server-side own-scope gate placement (new dependency vs inline check)

**Class:** governance-semantic contact (mechanism choice).

**Question:** EE-R4 verbatim: *"Every externally reachable endpoint enforces scope server-side — view-layer filtering alone fails review. Enforcement rides the existing B-1 scope primitive; no parallel mechanism."* B-1 primitive lives at `backend/services/auth/key_grants.py:65` (`check_scope()`). Own-scope gate is a NEW check (per-caller identity vs per-resource owner) not covered by `check_scope()` (which is class+path+floor+scope). Two placements:
- (a) New `require_own_scope_or_deny(identity, resource_owner)` FastAPI dependency AT the route handler layer, matching P9-E3 α's `require_worker_capability`. Adds explicit checkpoint per route.
- (b) Inline `if identity.roles contains external_engineer and resource.owner != identity.email: return 403` at each route body. Fewer files touched.

**Authority-source language:** BCR §3.9 EE-R4 line 242 (quoted); B-1 scope primitive at `key_grants.py:65`; P9-E3 α mechanism-not-convention doctrine at rulings record SHA `f62c89370b…` §P9-E3.

**Options:**
- (α) New helper `require_own_scope_or_deny` at `backend/services/auth/engineer_scope.py`, wired into engineer router via shared `_own_scope_impl`. Matches P9-E3 α "allowlist" up-from-permitted principle + never-rule-enforced-mechanically doctrine (V1-H2 pattern).
- (β) Inline check per route. Rejects the mechanism-not-convention doctrine.
- (γ) Extend `check_scope()` at `key_grants.py:65` to also accept an `owner_email` parameter. Rejects EE-R4 verbatim *"no parallel mechanism"* — this WOULD be a parallel mechanism (widening B-1 primitive beyond scope-tuple check).

**Recommended:** (α) new dedicated helper. Matches P9-E3 α mechanism-not-convention doctrine + preserves B-1's single-responsibility (class+path+floor+scope). Owner ruling requested.

### §5.3 P8E-E3 — Onboarding invite-token shape (new JWT class vs one-time-token vs email link)

**Class:** frozen-contract adjacency + governance-semantic contact.

**Question:** EE-R3 verbatim: *"external engineers are invited and approved by an internal engineer."* Silent on invite-token shape. Three shapes:
- (a) One-time DB-persisted token (like Sub-stage 3's rule-change ledger). Simple, no JWT class change.
- (b) New capabilities-claim JWT (parallel to P9-E3 α worker JWT with `capabilities: [onboarding_accept]`). Adds a JWT class.
- (c) Simple email + approval endpoint (no token; approval driven purely by `internal_engineer` clicking "approve" against a pending-invite DB row). Least surface.

**Authority-source language:** BCR §3.9 EE-R3 line 241 (quoted); P9-E3 α precedent (capabilities-claim; rulings record SHA `f62c89370b…`).

**Options:**
- (α) DB-persisted invite row (state=pending_invite → approved); approval endpoint is called by `internal_engineer` (authenticated with existing access JWT); JWT with `external_engineer` role minted at approval-time. NO new JWT class. Matches EE-R3 *"JWT mechanics unchanged"* verbatim (from EE-R1).
- (β) Capabilities-claim invite JWT (parallel to worker JWT). Adds JWT class + parity to auth surface.
- (γ) Email-link with signed invite payload (no DB persistence). Rejects idempotency-attested state (fewer guarantees).

**Recommended:** (α) DB-persisted invite row. Matches BCR §3.9 EE-R1 *"JWT mechanics unchanged"* verbatim + fewer moving parts. β is over-engineered for [STAKED] scope. Owner ruling requested.

### §5.4 P8E-E4 — EE-G3 admin/fleet 403 code reuses existing 4-code registry

**Class:** governance-semantic contact + P9-E3 pre-carry.

**Question:** EE-G3 verbatim: *"test_external_cannot_reach_admin_or_fleet_routes (403, access-control body)."* Which of the four existing codes fires: `auth_missing` / `auth_expired` / `auth_scope_insufficient` / `auth_identity_mismatch_for_wizard_session`? P9-E3 α condition 1 pre-carry verbatim: *"worker-auth denials use the existing 4-code registry, no new codes — registry stays closed."*

**Authority-source language:** BCR §3.9 EE-G line 243 + EE-R1 line 239 (*"4-code auth registry unchanged — external-scope denials are auth_scope_insufficient"*); P9-E3 α condition 1 (rulings record SHA `f62c89370b…`).

**Options:**
- (α) All external-scope denials use `auth_scope_insufficient` (per EE-R1 verbatim). Zero new codes. 4-code registry stays closed. Matches P9-E3 α pre-carry.
- (β) Add a 5th code `auth_role_scope_insufficient` distinguishing role-based scope from key-scope. Rejected: EE-R1 verbatim rules this out.
- (γ) Reuse `auth_scope_insufficient` for foreign-resource 403 (EE-G2) but use a different reason for admin/fleet-route 403 (EE-G3). Rejected: same class of denial per BCR §3.9 EE-R1 verbatim (*"access-control class"* covers both).

**Recommended:** (α) — matches EE-R1 verbatim + P9-E3 α condition 1 pre-carry. Not really Owner-ambiguous; asserting for the rulings record. Owner ruling requested (formality).

### §5.5 P8E-E5 — `internal_engineer` role naming (add separately or retain existing `engineer` implicitly)

**Class:** governance-semantic contact + naming.

**Question:** BCR §3.9 role-scoping matrix (line 245) shows `internal_engineer` and `external_engineer` as symmetric columns. `identity.py:24` currently has `"engineer"`. Does 8-EXT:
- (a) Rename `"engineer"` to `"internal_engineer"` (breaking existing JWTs / roles).
- (b) Add `"internal_engineer"` alongside existing `"engineer"` (both valid; internal_engineer is a proper subset of engineer).
- (c) Retain `"engineer"` as the internal-engineer identifier and add `"external_engineer"` only.

**Authority-source language:** BCR §3.9 EE-R1 line 239 (*"A role external_engineer is added"* — only external is named as added); technical annex table line 245 (both role names appear in table).

**Options:**
- (α) Retain `"engineer"` as internal (no breaking change); add `"external_engineer"` only. Interprets EE-R1 literally (*"added"*, singular). Table at line 245 is descriptive matrix, not role registry.
- (β) Add BOTH `"internal_engineer"` and `"external_engineer"`; deprecate `"engineer"` over time. Rejected structurally: breaks existing JWTs mid-flight.
- (γ) Add `"internal_engineer"` alongside `"engineer"` (both valid, symmetric with `"external_engineer"`). Table matches; no breaking change; role registry grows to 9. Attests scope enforcement can treat `engineer` and `internal_engineer` as equivalent for internal-scope reads.

**Recommended:** (α) minimal change matches BCR §3.9 EE-R1 verbatim. If Owner values symmetry with the annex table, (γ) is available. β is off-scope. Owner ruling requested.

### §5.6 P8E-E6 — UI Spec §5.4 binding copy (verbatim + em-dash / middle-dot contact)

**Class:** owner-value contact + E7/P9-E6 pattern.

**Question:** UI Spec §5.4 line 114 verbatim: *"External-scope denials are 403 access-control class ({reason, detail}) — never outcome=refused, never the refusal card."* Em-dash "—" used as syntactic pause (like UI Spec §3.3 line 50 grounding marker). Also UI Spec §5.4 line 102: *"Two roles, one console, identical screens, different scope — enforcement server-side, never view-layer filtering alone."* Similar em-dash syntactic pause pattern. Any binding copy from §5.4 rendered in Engineer screens must preserve the em-dash verbatim (P9-E6 α pre-carry).

**Authority-source language:** UI Spec §5.4 lines 102, 114 (quoted); P9-E6 α rulings record SHA `f62c89370b…` (em-dash preserved verbatim on syntactic pauses).

**Options:**
- (α) Preserve em-dash "—" verbatim on any Engineer-screen binding copy that quotes §5.4 phrasing. Jest cell asserts exact-string match + character-code U+2014 (P9-E6 α anti-slop-gate pattern).
- (β) Convert to middle-dot "·" for E7 uniformity. Rejected: P9-E6 α ruled em-dash is syntactic pause not list separator.
- (γ) Preserve em-dash verbatim OR test asserts two variants. Rejected: P9-E6 α ruled γ as unsatisfiable-spec generator.

**Recommended:** (α). Not really Owner-ambiguous; consistency with P9-E6 α. Owner ruling requested (formality attestation).

### §5.7 P8E-E7 — Ledger emission on onboarding approval (new stamp_audit variant or extend existing)

**Class:** frozen-contract adjacency (NorthenaLedgerRow_v1 stamp_audit) + governance-semantic.

**Question:** EE-R3 verbatim: *"grant issuance to the external class emits the ledger row exactly as built at Phase 8 B-3."* B-3 ledger emits `engineer_key_grant_event` rows. Onboarding APPROVAL is a distinct event from grant-issuance — does it also emit a ledger row? If yes, what shape?

**Authority-source language:** BCR §3.9 EE-R3 line 241 (quoted); B-3 landed at `backend/services/auth/engineer_key_grant_ledger.py:94` verbatim.

**Options:**
- (α) Yes; new `stamp_audit.data_class = "engineer_onboarding_approved"` variant reusing existing `NorthenaLedgerRow_v1` shape (no contract bump; matches B5b-E4 additive-bump-of-registry pattern). Grant-issuance ledger from B-3 continues unchanged (fires when the external engineer subsequently mints their first key grant).
- (β) No; onboarding approval is auth-boundary state (like login), not a governance event. Rejected: onboarding = introducing an external actor to the system; needs an audit trail.
- (γ) Reuse existing `engineer_key_grant_event` shape with `key_class="external_onboarding"` (semantic overload). Rejected: conflates two distinct events.

**Recommended:** (α) — matches BCR §3.9 EE-R3 posture (*"grant issuance ... emits the ledger row"* explicit + implicit that ONBOARDING itself is an event worth attesting). No frozen contract touched. `data_class_registry.v2.json` (landed at B-5b) grows to include `engineer_onboarding_approved` (additive per Ruling 4). Owner ruling requested.

---

## §6. Standing anti-rules audit (pre-dispatch attestation)

| Rule | Preserved by design |
|---|---|
| E5 (no HTTP 409 anywhere) | 8-EXT diff uses 401/403/400/200/201/202/204 exclusively. AST scan at close covers `backend/services/auth/engineer_scope.py` + `backend/services/auth/onboarding.py` + engineer router modifications for `\b409\b` — zero. |
| E7 (middle-dot on list separators) | Preserved. §5.6 (P8E-E6) confirms em-dash preservation on syntactic pauses. |
| E2 (4-code auth-refusal registry closed) | Preserved. §5.4 (P8E-E4) attests. All external-scope denials use `auth_scope_insufficient`. |
| Ruling 1 (artifact_ref vestigial) | 8-EXT does NOT touch ledger emit surfaces beyond §5.7 additive `data_class` variant. |
| Ruling 2 (capacity-role for compliance) | 8-EXT does NOT touch checker/compliance write path. |
| Ruling 3 (state-machine + unfrozen service-layer) | RoleName Literal expansion (§2.1.1 + §5.1) matches Ruling 3 unfrozen posture. |
| Ruling 4 (v0→v1 JSON registry additive bump) | Extended to §5.7 (α) if Owner rules — `data_class_registry.v2→v3` additive bump. |
| Ruling 5 (band discipline, miss + disclosure > pad + hide) | Band [900, 1,180] matrix-derived, no padding. §3.4 re-derivation triggers explicit. |
| Ruling 7 (Sub-stage 2 FINAL ACCEPTANCE) | Not touched. |
| B5b-E5 pre-authorized split | §4.2 thresholds stated: 1,500 LoC OR 60 cells. |
| P9-E1 α parity 28 additive | Preserved. NO parity bump this phase (Identity unfrozen). V1-G7 asserts 28 pre-existing byte-identical (§2.6 attestation cell). |
| P9-E3 α capabilities-claim + 4-code registry closed | Pre-carried (§5.4 P8E-E4 attests). |
| P9-E5 close-report bindings (V1-grid + no production mining) | N/A for 8-EXT (does not touch extraction stack). |
| P9-E6 α em-dash verbatim | Pre-carried (§5.6 P8E-E6 attests). |
| Amortisation Divergence Class | Codified at §1.2 with two NEW empirical rates (backend Pytest 12 LoC/cell shared-helper + Playwright 9 LoC/cell data-testid) per Owner 2026-07-08 dispatch. |
| Standing Correction matrix-enumerated sizing | Applied throughout §2 + §3. |
| Standing Rule v3 (on-disk canonical) | This proposal ON DISK at `/app/docs/stage_a_proposals/8_ext.md`. |

---

## §7. Reply-body structural summary (dispatch reply reference)

**File landed at this Stage A dispatch:**
- `/app/docs/stage_a_proposals/8_ext.md` (this file).

**Files NOT touched:** all 28 frozen contracts; all Sub-stage 3 + B-5b + 9.1/9.3 landed code; all mandate docs; all conformance/rulings/close report docs. Design-only.

**Structural TOC:**
- §Substrate already landed (Owner-named — DO NOT re-price).
- §1. Cell-density assumption + Amortisation Divergence Class codification (2 new empirical rates codified per Owner 2026-07-08).
- §2. Deliverables enumeration (§2.1 backend + §2.2 frontend + §2.3 named gate roster EE-G1..G4 + §2.4 onboarding + §2.5 endpoint × auth × posture matrix + §2.6 contract byte-identity attestation).
- §3. Band derivation.
- §4. Dispatch discipline (§4.1 baseline atomic + §4.2 pre-authorized split thresholds + §4.3 dispatch-independence).
- §5. Escalation flags P8E-E1..P8E-E7.
- §6. Standing anti-rules audit.
- §7. Reply-body structural summary.

**Escalation flags summary (7 total):**
- **P8E-E1** — α/β/γ menu — `external_engineer` role Literal expansion. Recommended: **α additive** (Identity unfrozen per Ruling 3; parity 28 stays).
- **P8E-E2** — α/β/γ menu — server-side own-scope gate placement. Recommended: **α dedicated helper** (`require_own_scope_or_deny`; matches P9-E3 α mechanism-not-convention).
- **P8E-E3** — α/β/γ menu — onboarding invite-token shape. Recommended: **α DB-persisted invite** (JWT mechanics unchanged per EE-R1 verbatim).
- **P8E-E4** — α/β/γ menu — EE-G3 admin/fleet 403 code reuse. Recommended: **α `auth_scope_insufficient`** (P9-E3 α condition 1 pre-carried; 4-code registry closed).
- **P8E-E5** — α/β/γ menu — `internal_engineer` naming. Recommended: **α retain `engineer` as internal** (BCR §3.9 EE-R1 verbatim "added" is singular for external_engineer only).
- **P8E-E6** — α/β/γ menu — UI Spec §5.4 em-dash preservation. Recommended: **α preserve verbatim** (P9-E6 α pattern).
- **P8E-E7** — α/β/γ menu — onboarding-approval ledger emission shape. Recommended: **α new `stamp_audit.data_class = "engineer_onboarding_approved"` variant** (additive; matches Ruling 4 + B5b-E4 pattern).

**Band (matrix-derived, no padding):** `[900, 1,180]` raw LoC across 42 cells.

**§4.2 pre-authorized split thresholds:** 1,500 LoC OR 60 cells → autonomous 8-EXT.a (backend) + 8-EXT.b (frontend) split.

**Ready-to-dispatch posture:**
- BCR §3.9 EE-R1..R4 + EE-G1..G4 matrix-enumerated at §2.
- UI Spec v2.1 §5.4 own-apps-only surface enumerated at §2.2.
- Two new empirical rates (backend Pytest 12 LoC/cell shared-helper + Playwright 9 LoC/cell data-testid) codified at §1.2 with named triggers per Owner 2026-07-08 dispatch verbatim.
- 28 frozen contracts preserved (Identity unfrozen; no parity bump).
- E5 zero-409 attested at §6.
- E7/P9-E6 em-dash preservation attested at §5.6.
- P9-E3 α 4-code registry closed pre-carried and attested at §5.4.
- §4.2 pre-authorized split thresholds stated at §4.2.
- 7 escalations enumerated at §5 (all α/β/γ menu — no cannot-be-α/β semantic rulings this phase).
- Design-only; no code changes; no execution self-dispatch.

**READY TO DISPATCH POST OWNER RULINGS on P8E-E1/E2/E3/E4/E5/E6/E7 (all α/β/γ menus) + ratification of §3.3 band [900, 1,180] + §4 dispatch discipline.**

═══════════════════════════════════════════════════════════════════

*End of 8-EXT Stage A proposal. Design-only per Owner dispatch. Standing Rule v3: full text on disk. Reply body = SHA + escalation IDs + band + line-range map. Owner ratification of Stage A + P8E-E1..P8E-E7 required before 8-EXT execution dispatch. Small phase; independent of Sub-stage 9.2 [OWNER] facts + artifact store + transform forms. On ratification of close, Phase 9 Stage B becomes builder-dispatchable (subject to 9.2-OWN-1..3 landing Owner-side).*
