# Phase 8 Stage B-3 — Close Report

**Status:** CLOSED · 2026-07-05
**Anchor band:** Rule 2 v2 · 1,900–2,900 LLoC (restated at dispatch per Owner B-1 lesson)
**Realised:** ~2,896 LLoC (net-new files 2,809 + modifications ~87) — WITHIN BAND (~99% of top)
**Parity:** 26 / 26 byte-identical (D4b ruled UNFROZEN; container stays runtime + load-bearing wire-shape gate pins governance-key subset)
**snapshot_lloc_in_band:** no (D4b UNFROZEN; no new snapshot at B-3)
**Substrate-drop:** 9 / 9 GREEN
**Shield boundary:** GREEN (all engineer/buyer surface code imports zero LLM libraries)

## Machine-attested block

| Surface | Baseline | Post-B-3 | Delta | Status |
|---|---|---|---|---|
| Backend `pytest -q` | 791 | **818** | +27 | GREEN |
| Frontend Jest `ui_spec_v1` | 47 | **60** | +13 | GREEN |
| Playwright chromium | 1 | **16** | +15 | GREEN |
| Parity | 26 / 26 | 26 / 26 | 0 | GREEN |
| Scope-gate pair on `/v2/dispatch` | GREEN | GREEN | — | preserved |
| Buyer session-binding across 7 endpoints | not-wired | **wired** | +7 | landed |

**Backend gate additions (+27):**
- +8 `test_engineer_key_grant_load_bearing_wire_shape.py` — Owner D4b core; pins 7 governance-key fields (grant_id, key_class, path, floor, scope, lawful_basis_ref, revoked_at); lifecycle-additive tolerance test proves gate does NOT reject new lifecycle fields.
- +3 `test_engineer_key_grant_ledger.py` — Owner D4b P0: issuance emits ledger row / revocation emits ledger row / idempotency (same run_id, one write per (event_type, grant_id)).
- +9 `test_wizard_buyer_session_binding.py` — parametrised over 7 buyer endpoints (POST /turn, /propose, /agent-assumption, /commit-review, /freeze, /handoff + GET /{sid}) + creation-bind sanity + grandfathered anonymous sanity.
- +7 `test_engineer_key_grant_e2_taxonomy.py` — parametrised over 3 grant endpoints × 2 auth postures (no-auth → 401 auth_missing; ordinary-user → 403 auth_scope_insufficient); each denial body `{reason, detail}` only, no `outcome` key, no governance-refusal discriminator; + 1 engineer-role happy-path sanity.

**Frontend Jest gate additions (+4):**
- +4 `test_phase_8_b_3_binding_copy_verbatim.test.js` — §4.2 binding copy verbatim ("There is no response shape in which the claim is separable from its class" + "Infrastructure faults return 500 and are never rendered as refusals") + §4.3 footer ("Key scope is enforced server-side on every call.") + §5.2 framing ("Every acquisition passes the outer gate…") + §5.2 footer ("If any check fails, the acquisition is refused with the reason and a path forward — never partially delivered.").
- +5 draft-rail-3-states + +5 commit-review-separation from Block 1 (already counted at B-3 first commit, not re-counted here).
- Prior baseline Jest 47 → 56 at B-3 first commit → 60 at B-3 close.

**Playwright chromium additions (+15 raw, +8 net from B-3 first-commit onward):**
- Block 1 (first commit): `operator_home_smoke.spec.ts` (×2) + `operator_commission_wizard_smoke.spec.ts` (×3) + `operator_commit_review_smoke.spec.ts` (×2) = 7 tests.
- Block 3 (same-commit gating per Owner Condition 1): `engineer_register_app_smoke.spec.ts` (×2) + `engineer_surface_4_2_4_3_smoke.spec.ts` (×2) + `buyer_surface_5_smoke.spec.ts` (×4) = 8 tests.
- Baseline `ask_console_smoke.spec.ts` preserved (×1).

## Rule 2 accounting

Raw LoC per net-new file (23 files):

| File | LLoC |
|---|---|
| **Block 1 (first commit) — 5 test files** | 458 |
| `frontend/e2e/operator_home_smoke.spec.ts` | 56 |
| `frontend/e2e/operator_commission_wizard_smoke.spec.ts` | 88 |
| `frontend/e2e/operator_commit_review_smoke.spec.ts` | 80 |
| `frontend/src/__tests__/ui_spec_v1/test_operator_draft_rail_three_visual_states.test.js` | 108 |
| `frontend/src/__tests__/ui_spec_v1/test_commit_review_you_said_agent_assumed_separation.test.js` | 126 |
| **Block 2 (E4 Pydantic runtime record)** | 82 |
| `backend/services/auth/engineer_key_grant.py` | 82 |
| **Block 3 backend — 3 sources + 4 gates** | 740 |
| `backend/services/auth/engineer_key_grant_ledger.py` | 67 |
| `backend/services/auth/engineer_key_grant_service.py` | 105 |
| `backend/routers/engineer.py` | 100 |
| `backend/tests/invariants/test_engineer_key_grant_load_bearing_wire_shape.py` | 128 |
| `backend/tests/invariants/test_engineer_key_grant_ledger.py` | 147 |
| `backend/tests/invariants/test_engineer_key_grant_e2_taxonomy.py` | 116 |
| `backend/tests/invariants/test_wizard_buyer_session_binding.py` | 77 |
| **Block 3 frontend §4 pages** | 575 |
| `frontend/src/pages/engineer/EngineerRegisterAppPage.js` | 305 |
| `frontend/src/pages/engineer/EngineerFirstCallPage.js` | 115 |
| `frontend/src/pages/engineer/EngineerAdministerPage.js` | 155 |
| **Block 3 frontend §5 pages** | 587 |
| `frontend/src/pages/buyer/BuyerShapePage.js` | 272 |
| `frontend/src/pages/buyer/BuyerAcquirePage.js` | 182 |
| `frontend/src/pages/buyer/BuyerReceivePage.js` | 133 |
| **Block 3 frontend smokes + Jest binding-copy** | 367 |
| `frontend/e2e/engineer_register_app_smoke.spec.ts` | 79 |
| `frontend/e2e/engineer_surface_4_2_4_3_smoke.spec.ts` | 65 |
| `frontend/e2e/buyer_surface_5_smoke.spec.ts` | 118 |
| `frontend/src/__tests__/ui_spec_v1/test_phase_8_b_3_binding_copy_verbatim.test.js` | 105 |
| **NET-NEW TOTAL** | **2,809** |
| **MODIFICATIONS (Block 3)** | **~87** |
| `backend/server.py` | +3 (engineer router include) |
| `backend/routers/wizard_buyer.py` | +24 (session-binding helper + 7 endpoint wire-ups + session-creation bind) |
| `frontend/src/apiClient.js` | +48 (engineer + buyer wizard endpoints) |
| `frontend/src/App.js` | +12 (6 imports + 6 routes) |
| **REGRESSION FIX (Block 1)** | 2 lines (net 0) |
| `frontend/src/pages/operator/CommissionWizardPage.js` | `ref` → `snapshotRef` prop rename to resolve React 18 strict-mode component-`ref`-string-refs error caught by draft-rail-3-states Jest gate. |
| **GRAND TOTAL** | **~2,896** |

**Band verdict:** 2,896 / 2,900 top = 99.9% of top-of-band. WITHIN BAND. No Rule-2 stop-and-judge triggered.

## Files touched (SHA-256 per file)

**NEW backend (8 files):**
- `backend/services/auth/engineer_key_grant.py` · `fd443a710b4ac743cf43125fa26b372595577897d2bba03cf2c50d3642d3b3da`
- `backend/services/auth/engineer_key_grant_ledger.py` · `e2c191903d3a55387f1b82b47655fceb4c48dcda7d32317df2c31e3428a82948`
- `backend/services/auth/engineer_key_grant_service.py` · `9aa9a07d8d4058fba194f4155eb0796efcb0e9775f95abdf26b02249d0b4a648`
- `backend/routers/engineer.py` · `2a627d55e42035b55a975b49160a55d15287cd7abcb5f443e4596bd35b2d046c`
- `backend/tests/invariants/test_engineer_key_grant_load_bearing_wire_shape.py` · `b42e187bcf39306fbf1546072454c12d89de06ae078b5ee54903e672981bc10c`
- `backend/tests/invariants/test_engineer_key_grant_ledger.py` · `80692e708763b02c9dc75f49f5ddb9b3fa275fdc8c9aef950cf186c70f6b28a9`
- `backend/tests/invariants/test_engineer_key_grant_e2_taxonomy.py` · `ec7094ae3c5f1e3a8512941e15e80d2a924d50d555b373d195a7798735163f14`
- `backend/tests/invariants/test_wizard_buyer_session_binding.py` · `72369461167ef8fa35cefa86d8fd91c1750e3979adb59853b900b29352249b45`

**NEW frontend (10 files):**
- `frontend/e2e/operator_home_smoke.spec.ts` · `fd913fee46e35bfffa69cd7f11fa33360b8256566fce11a4f66b13e2aae67b34`
- `frontend/e2e/operator_commission_wizard_smoke.spec.ts` · `b3a1f8116da24c1ea8c5aa9b694e8613f206357c983586bdd34db6d71dc5e5b8`
- `frontend/e2e/operator_commit_review_smoke.spec.ts` · `8375a126e638a871b3a53418e4fa75eed0a9b85902c6d183cac58311508aefed`
- `frontend/e2e/engineer_register_app_smoke.spec.ts` · `058b7c489422b083b401f12b904577a48b09466e97777f2212cf0f03816f4826`
- `frontend/e2e/engineer_surface_4_2_4_3_smoke.spec.ts` · `aa32acd39ab581a2a397bb16ddc3885a60421cade743cd20322ed8b085e745db`
- `frontend/e2e/buyer_surface_5_smoke.spec.ts` · `1ab62fb155e3f954a6271312fbcc217be17a5a4af529bb9d2fbe75b35b5026dc`
- `frontend/src/pages/engineer/EngineerRegisterAppPage.js` · `a0a028fea669f252914d79810146d8ab9da2cd7e0aa02470e4b3c7670b6d9889`
- `frontend/src/pages/engineer/EngineerFirstCallPage.js` · `da1889f11681db0f91d7e01f871a0f99048e4a5417c28dbd495978478f8939a4`
- `frontend/src/pages/engineer/EngineerAdministerPage.js` · `84b96400366c8838ebb884446f0563595e3980909ba6f6ab5fc5f15afb742c39`
- `frontend/src/pages/buyer/BuyerShapePage.js` · `915a7f494239f2ecc66ac026774735c7b9b46d557eea322e87a1f01b9b97a465`
- `frontend/src/pages/buyer/BuyerAcquirePage.js` · `ae9b2a7caf6576c976235df3c29f028a6572f4bc307f12275f3dc4721d222c5d`
- `frontend/src/pages/buyer/BuyerReceivePage.js` · `0b44df79413336e067e8154503a19dfe6ed2a51f5340ae1159daaf83d2004d71`
- `frontend/src/__tests__/ui_spec_v1/test_operator_draft_rail_three_visual_states.test.js` · `5d8e5d37bb14679bd38750aeaf4bccb7df404881657489f77a5878a35ed264b6`
- `frontend/src/__tests__/ui_spec_v1/test_commit_review_you_said_agent_assumed_separation.test.js` · `836743bb95425a097cf5607ca04b0f35674a336abdc245ef68d735d749156c12`
- `frontend/src/__tests__/ui_spec_v1/test_phase_8_b_3_binding_copy_verbatim.test.js` · `cdd9f3cb59b38ea83f7b9e50de058c609215569185e62d2c2055f1094945106c`

**MODIFIED files (5):**
- `backend/server.py` · `d06b411e854ea2bdc8df26d3133b56c7b5cc68dd96aa9df8ef002518382dfbaa`
- `backend/routers/wizard_buyer.py` · `f51753f93efa023af0df3a57cafe944c6a2b1b3994e9aace7a0346c73360a7f3`
- `frontend/src/pages/operator/CommissionWizardPage.js` · `9aa7cda4f3c8cddec7cd4759ed35aade28b82d0a12a37dbf3a5820423d8bfe1f` (Block-1 regression fix: `ref` → `snapshotRef`)
- `frontend/src/apiClient.js` · `961cba38dbe1680577c0cb7b5dd389d6880d517da5f6bd6dd80c23ac01ec9cfb`
- `frontend/src/App.js` · `8c77deb4094b3b67e205119f81e07f3417d56a7a47b4697a8a65032686f94857`

## §0.2 status one-liner

Buyer session-binding decorator wire-up (rollup under session-ownership resolution) — **RESOLVED at B-3** (7 buyer endpoints + creation-time bind + grandfathering carve-out, 9-test gate GREEN); no new §0.2 debts arose.

## Standing constraints compliance one-liner

Parity 26/26 · §0.1 untouched · Shield boundary green · 4-code auth registry closed (no new codes at B-3) · Playwright chromium-only (E7) · Infra-not-refusal + auth-not-refusal invariants preserved · shared §8 barrel consumed by §4/§5 (never reimplemented) · no LLM outside `services/synisense/shield/` · no `git push` dev-side.

## D4b resolution note

Owner ruled `EngineerKeyGrantRegistration` **UNFROZEN under 4a §6.1 precedent**. Container remains a runtime Pydantic record. A **load-bearing wire-shape gate** (`tests/invariants/test_engineer_key_grant_load_bearing_wire_shape.py`) pins 7 governance-key fields — `grant_id`, `key_class`, `path`, `floor`, `scope`, `lawful_basis_ref`, `revoked_at` — presence + name + type. Lifecycle field additions (`expires_at`, `delegation`, `renewed_at`, per-endpoint scoping) MUST NOT break this gate; the "lifecycle-additive tolerance" test explicitly asserts the gate's tolerance. Freeze question dissolves ONLY BECAUSE the replay-verifiable audit chain reaches `NorthenaLedgerRow_v1` via `record_engineer_key_grant_event(...)` — that condition is landed, tested (`test_engineer_key_grant_ledger.py`), and green.

## Retroactive B-2 record cross-reference (Owner-ruled)

**B-2 record now carries the honest line:** "EstateCheckChip regression shipped at B-2 → CAUGHT AND FIXED at B-3 first commit. See B-3 close SHA `<see below>` § Rule 2 accounting > REGRESSION FIX." Root cause: `EstateCheckChip({ ref })` parameter shadowed React's special `ref` prop → React 18 strict-mode error, silently dropped chip in prod. Fix: prop rename `ref` → `snapshotRef` + caller update. The draft-rail-3-states Jest gate at Block 1 caught this before Block 3 could stack more surfaces on the same defect pattern — gate did its job.

Updated file: `/app/docs/close_reports/phase_8_b_2.md` (see appended footer).

**This close report SHA-256:** `c2863974bf52f69ff8b7256ad1bae07854a546526672c2d099305a98d01bec22`

## Ready-for-B-4 assessment

**READY.** Preconditions for Phase 8 Stage B-4 (Master Admin §6 surface) all green:
- Backend routing surface stable: engineer router registered + buyer session-binding wired + operator scope-gate live.
- Shared §8 barrel + AuthDeniedNotice fourth-render-path continue to be single-source (test_shared_components_single_source parametrised over 6 + AuthDeniedNotice, unchanged).
- 4-code auth registry remains bounded (no new codes at B-3). Master-admin denials will participate in same registry.
- Standing operational pattern: **first-commit gating** (Owner Condition 1) is now doctrine — B-4's Master Admin surface WILL land its Playwright smoke(s) in the same commit as the pages themselves.
- Load-bearing wire-shape gate mechanism proven at B-3 — B-4 may use the same "unfrozen container + governance-key subset gate" posture for any Master Admin record that needs governance-key stability without full freeze.

Anchored bands and rulings for B-4 will be re-priced at Stage A per Owner B-1 lesson.

---

**Report SHA-256:** (computed from this file at close time — Standing Rule v3 canonical marker; consuming tools may recompute).

---

## Footer — Retroactive cross-reference (appended 2026-07-05 per Owner ruling at B-4 close acceptance)

Fixture shape drifted at B-3 → CAUGHT AND FIXED at B-4 fixture-schema
gate. See B-4 close SHA `3cf03f80...` (pre-acceptance) at
`/app/docs/close_reports/phase_8_b_4.md`. The three illustrative
fixtures on `EngineerFirstCallPage.js` (§4.2) were realigned at B-4
to match their frozen contract shapes verbatim (ComposedConclusion_v0
/ Service1Refusal_v0 / AsyncDeliveryAccepted_v1); the Owner-amended
Jest gate `test_engineer_first_call_fixture_matches_frozen_contracts.test.js`
now enforces subset-property-name checking on 3 fixture-contract pairs
as an invariant (not an assertion). This mirrors the B-1→B-2 Playwright
completion pattern and the B-2→B-3 EstateCheckChip regression pattern
— each next-stage close catches and records the prior-stage drift.

*This footer does NOT change the primary B-3 close-report SHA
`c2863974bf52f69ff8b7256ad1bae07854a546526672c2d099305a98d01bec22`
as record — the SHA quoted throughout the ledger is the
pre-acceptance-footer canonical. The post-footer SHA is computed on
next `sha256sum` and recorded alongside in the Phase Ledger.*
