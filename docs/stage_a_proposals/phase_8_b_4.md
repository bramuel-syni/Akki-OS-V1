# Phase 8 Stage B-4 — Stage A Proposal (Design-only)

**Status:** DRAFT — awaiting Owner ratification
**Date:** 2026-07-05
**Baseline:** Phase 8 Stage B-3 close SHA `c2863974bf52f69ff8b7256ad1bae07854a546526672c2d099305a98d01bec22`
**Standing Rule v3 in force:** on-disk canonical + SHA, no full-text implementation pastes.

---

## 1 · §6 surface reading (VERBATIM from `RMS_UI_Specification_v1.md` §6.1–§6.3)

### §6.1 Home
- **Elements verbatim:** *"pending banner in plain language ("Two rules are waiting on your decision before they can take effect." + **Review**); prompt "What do you want to do?"; six action buttons (binding labels): **Assign a role** · **Change a rule** · **Manage keys & access** · **Update the taxonomy** · **Set pricing** · **Apportion GPU capacity**; footer link "See everything I've changed — every action is recorded.""*
- **Rules verbatim:** *"buttons and sentences only. No dashboards, no version strings, no config syntax anywhere on this surface."*
- **Enumerated elements** (13):
  1. Pending banner with count of waiting rules (dynamic; plural-aware plain-language).
  2. Verbatim pending copy: "Two rules are waiting on your decision before they can take effect." (with count-substitution).
  3. Verbatim **Review** button on the pending banner.
  4. Verbatim prompt: "What do you want to do?"
  5. Six action buttons with binding labels verbatim:
     - **Assign a role**
     - **Change a rule**
     - **Manage keys & access**
     - **Update the taxonomy**
     - **Set pricing**
     - **Apportion GPU capacity**
  6. Verbatim footer link: "See everything I've changed — every action is recorded."
- **NEGATIVE assertions (Rules-driven):**
  - No dashboards (assert absence of chart/plot/graph testids).
  - No version strings visible (assert absence of `v0` / `vN.json` / semantic-version substrings).
  - No config syntax (assert absence of JSON blobs, YAML fragments, or key=value pairs in visible copy).

### §6.2 Change a rule
- **Elements verbatim:** *"'The rule' — one sentence stating what it does in everyday language; a short paragraph of current behaviour and what turning it on/off means; plain **Off / On** options with natural labels; "What changes" info box — one or two sentences, includes that nothing running now changes (when true) and that it can be switched back; commit button in natural language ("Turn it on")."*
- **Binding copy verbatim:** *"Recorded as your change, with today's date."*
- **Enumerated elements** (6):
  1. "The rule" one-sentence descriptor.
  2. Current-behaviour paragraph explaining on/off semantics.
  3. Plain Off / On radio-like options with natural labels (not `enabled: true/false`).
  4. "What changes" info box with the "nothing running now changes" + "can be switched back" sub-assertions.
  5. Commit button in natural language (e.g., "Turn it on").
  6. Post-commit binding-copy line VERBATIM: "Recorded as your change, with today's date." + today's date rendered.

### §6.3 What I've changed — audit trail
- **Elements verbatim:** *"confirmation line for the latest change (plain: what is now in effect, from when); recent actions rows — plain description of the change (from → to in words), who, when."*
- **Footer binding copy verbatim:** *"Every row carries its full diff. This trail is itself append-only and readable by the regulator surface."*
- **Rule verbatim:** *"the diff exists in the record; it is never the primary display."*
- **Enumerated elements** (4):
  1. Confirmation line for the latest change ("<rule> is now on, from <date>", in plain language).
  2. Recent actions rows — one per row, with plain from→to words + who + when.
  3. Footer binding-copy VERBATIM: "Every row carries its full diff. This trail is itself append-only and readable by the regulator surface."
  4. Diff availability affordance — a "See full diff" link that opens the diff without making it primary (per the Rule).
- **NEGATIVE assertion:** the raw diff (JSON blob / patch text) must NOT appear as primary display; it opens on demand.

---

## 2 · Pre-Rule 1 Path decisions per §6.2 sub-surface

§6.2 is the surface for turning rules on/off. In today's backend, the three "rules" a Master Admin can meaningfully touch are:

| Sub-surface | Endpoint today | Today's shape | Proposed Path | Rationale |
|---|---|---|---|---|
| **Tier lock** | `POST /api/pricing/tier_lock` | Header-gated; writes `_TIER_LOCK_STATE` in-memory; NO ledger write; NO versioned file write | **Path A** | The runtime state is real (quote-issuance already respects it via `pricing_tier_frozen_by_control_surface`); a governance transition IS occurring. Extending it to emit `NorthenaLedgerRow_v1` + write a `tier_lock.vN.json` versioned marker discharges Ruling R3-SD2 without changing runtime semantics. This is exactly the pattern established at B-3 for engineer key-grant lifecycle events (stamp_audit sidecar, idempotent). **Load-bearing:** without ledger emit, §6.3 audit trail has nothing to display for tier-lock changes. |
| **Model version bump** (`POST /api/pricing/model_version`) | Header-gated; already returns 501 with a technical hint ("bump by adding a fresh price_model.vN.json") | **Path B — honest 501** | Registry-bump-via-disk is an ops-side action (Owner-controlled files under `services/economics/`). No UI can safely mutate `price_model.vN.json` under Ruling R3-SD2. Convert the 501 hint from technical language to plain language: "This change requires a versioned file update on the server — contact Owner. No change applied." NO client-side ghosting. |
| **Fleet policy bump** (`POST /api/fleet/policy`) | Header-gated; already 501 with technical hint | **Path B — honest 501** | Same reasoning as model version. Fleet apportionment is Owner-value-adjacent (E1/E5 governance seams still gated). Convert 501 to plain language. NO client-side state mutation. |

**§6.2 "Change a rule" navigation posture** (VERBATIM Owner "buttons and sentences only" applied):
The §6.2 surface presents ONE rule at a time (per UI Spec §6.2 verbatim "The rule" — singular). §6.1's **Change a rule** button routes to a rule-picker or directly to the most-recently-touched rule; for B-4 scope we route to **`/master-admin/change-a-rule/tier-lock`** (Path A path) as the primary Master Admin editable rule at Phase 8. The two Path-B rules (model_version, fleet_policy) are accessible via a small "Other rules" sub-list on the picker so their honest 501 language surfaces if a Master Admin clicks in.

**Path A endpoint spec (VERBATIM proposal):**

`POST /api/pricing/tier_lock` — extended body:
```
{ "locked": bool, "reason_note": str | null, "idempotency_key": str | null }
```
Response body extended:
```
{ "locked": bool, "reason_note": str | null,
  "trace_id": str, "ledger_run_id": str,
  "versioned_file_path": str,      // e.g., "services/economics/tier_lock.v2.json"
  "at": ISO-8601 }
```
Semantics:
- If `idempotency_key` present + prior POST with same key found in ledger → return existing `ledger_run_id` and `versioned_file_path` (idempotent-once).
- Else: write `tier_lock.vN.json` (N = next serial), record the transition into `NorthenaLedgerRow_v1` with `stamp_audit.data_class="master_admin_rule_change"` + `stamp_audit.rule_change={rule_id: "tier_lock", from: bool, to: bool, reason_note: str, versioned_file_path: str}`, then set the in-memory runtime state via `_quote_service.set_tier_lock(...)`.
- Reversibility is IMPLICIT in the pattern: another POST with the opposite `locked` value writes a new versioned file + new ledger row. The historical record is append-only; the runtime state moves.

**Path B "honest 501" plain-language responses:**

`POST /api/pricing/model_version` → 501:
```
{ "outcome": "not_yet_implemented",
  "reason": "requires_versioned_file_change_by_owner",
  "detail": "Changing the price model requires a versioned file update on the server. Contact Owner. No change applied." }
```

`POST /api/fleet/policy` → 501:
```
{ "outcome": "not_yet_implemented",
  "reason": "requires_versioned_file_change_by_owner",
  "detail": "Changing GPU capacity apportionment requires a versioned file update on the server. Contact Owner. No change applied." }
```

Both refuse cleanly with plain-language `detail`. UI surface renders `detail` verbatim in the "What changes" info box.

---

## 3 · Pre-Rule 2 auth reconciliation one-liner

**Proposal (one line):** **RETIRE `RMS_MASTER_ADMIN_TOKEN` env-gating on the pricing + fleet routers — replace with JWT role-based auth requiring `master_admin` in `identity.roles` (already carried by the seeded admin — `user_store.seed_admin_if_absent` line where the admin gets `["admin", "operator", "engineer", "buyer", "master_admin", "dpo"]`). Zero grandfathering required.**

**Justification:**
- **No production consumers of `X-RMS-Master-Admin` header.** Only known consumer in tree: `backend/tests/invariants/test_phase_6_stage_b_economics.py` (test-only) with header value `"test-master-token"`. Test file updates to seed a master-admin user + login (same shape as B-3 test_engineer_key_grant_e2_taxonomy.py's engineer-role seeding). **No operational script / cron / bootstrap depends on the token.**
- **JWT primitive already carries `master_admin`.** The seed admin has the role; `require_identity_or_deny` returns the Identity; a `_has_master_admin_authority(identity)` helper (mirror B-3 engineer authority helper) gates the write endpoints.
- **Owner rationale check:** "Two parallel auth mechanisms on the highest-privilege surface is a standing confusion." Retiring closes the confusion. Layering-beneath keeps the surface confusing for a token whose only current consumer is a test file — Owner would be trading clarity for zero operational continuity.
- **Auth-denial taxonomy applied per Owner E2:** master-admin writes without JWT → 401 `auth_missing`; with JWT but no `master_admin` role → 403 `auth_scope_insufficient`. Body shape `{reason, detail}` — 4-code registry closed, NO new codes.
- **Backward-compatibility posture:** During B-4 implementation, add a deprecation-log entry when the code path detects `X-RMS-Master-Admin` header on a request (informational; no behavior change). At B-4 close, remove the header parameter entirely from the endpoint signatures. Env var `RMS_MASTER_ADMIN_TOKEN` can be removed from `.env` / secrets by operator at their leisure.

**One-line answer (final):** **RETIRE — replace header gate with JWT `master_admin` role check; only test file needs update; audit shows zero production consumers.**

---

## 4 · §4.2 fixture-schema gate design

**Test file (Jest):** `frontend/src/__tests__/ui_spec_v1/test_engineer_first_call_fixture_matches_frozen_contracts.test.js`

**Fixtures under test** (already inline in `frontend/src/pages/engineer/EngineerFirstCallPage.js`):
- `ANSWERED_ILLUSTRATIVE` → maps to `ComposedConclusion_v0` (via `outcome: "answered"` discriminator).
- `REFUSED_ILLUSTRATIVE` → maps to `Service1Refusal_v0` (via `outcome: "refused"` discriminator with `asked`/`supported_class`/`what_would_raise_it`).
- `ASYNC_ACCEPTED_ILLUSTRATIVE` → maps to `AsyncDeliveryAccepted_v1` (via `objective_id`/`accepted`/`delivery_estimate`).

**Refactor step 1** (net-zero-behavior): export the three fixture constants from `EngineerFirstCallPage.js` as named exports so Jest can import them. Zero visible behavior change.

**Source-of-truth for schema:** the frozen `.contract_snapshot.json` files under `backend/tests/invariants/` — one per frozen contract, each carrying the Pydantic-derived JSON-schema `properties` map. The gate reads these snapshots at test runtime via `fs.readFileSync` (Jest runs in Node; filesystem access is available).

**Gate assertions per fixture:**
1. Parse fixture JSON string via `JSON.parse` (structural well-formedness).
2. Extract the top-level field name set from the parsed fixture.
3. Load the corresponding contract snapshot's `properties` object; extract the property name set.
4. **Assert:** every field name in the fixture ALSO exists in the contract's properties. (Drift check: contract dropped a field → fixture becomes stale → fails.)
5. **Recursively check nested objects** for the same subset invariant (fixture's `claim.defensibility.class` must correspond to a field in the nested `defensibility` schema).
6. For discriminated unions (`Service1Refusal_v0` where `outcome` selects the branch), the fixture's discriminator value MUST match a branch that contains the sibling fields.

**On-drift semantics:** if a fixture uses `claim.class` but the frozen contract expects `claim.defensibility.class`, the test fails with a diff message naming both paths — "misdocumentation caught before ship."

**Fixture files referenced:** the three inline exports from `EngineerFirstCallPage.js` (post-refactor).

**Contract-schema-parse approach:** filesystem read of the frozen `.contract_snapshot.json` neighbors, then plain JS property-name comparison. **No shell-out to Python. No JSON-schema library. Zero new dependencies.**

**Coverage extension** (opportunistic, in-block): the same gate framework can be applied to any future illustrative fixtures added elsewhere (e.g., §6 config-syntax examples — but §6.1 rule "no config syntax" makes this unlikely). Not scoped to B-4 unless discovered.

---

## 5 · Rule 2 v2 anchor band (priced at dispatch, all rulings folded)

**LoC estimates (LLoC = non-blank, non-docstring/comment):**

| Component | Estimate (LLoC) |
|---|---|
| **Backend — §6.1/§6.2/§6.3 support** | ~140 |
| `services/economics/tier_lock_persistence.py` (versioned-file write helper) | ~50 |
| `services/economics/tier_lock_ledger.py` (stamp_audit sidecar mirror of B-3 grant_ledger) | ~55 |
| `routers/pricing.py` extensions (Path A tier_lock body + JWT auth + Path B 501 plain-language) | ~35 |
| **Backend — auth reconciliation** | ~40 |
| `routers/pricing.py` — drop `_require_master_admin` header gate, add `_require_master_admin_role_or_deny` JWT gate | ~25 |
| `routers/fleet` refactor to JWT gate | ~15 |
| **Backend — new §6.3 audit-trail endpoint** | ~70 |
| `routers/master_admin.py` — new router `GET /api/master_admin/recent_actions` reads `NorthenaLedgerRow_v1` filtered by `stamp_audit.data_class="master_admin_rule_change"` + returns plain-language descriptions | ~70 |
| **Backend tests** | ~330 |
| `test_master_admin_tier_lock_path_a_ledger.py` (Path A ledger emit + idempotency + versioned file write, mirror B-3 grant ledger) | ~130 |
| `test_master_admin_auth_reconciliation.py` (JWT master_admin gate; retire header gate; taxonomy over write endpoints) | ~90 |
| `test_master_admin_recent_actions.py` (§6.3 audit-trail endpoint tests) | ~60 |
| `test_pricing_paths_b_honest_501.py` (Path B 501 plain-language body assertions) | ~50 |
| **Frontend §6 pages** | ~500 |
| `pages/master_admin/MasterAdminHomePage.js` (§6.1 verbatim + 6 action buttons + pending banner + footer link) | ~160 |
| `pages/master_admin/ChangeARulePage.js` (§6.2 verbatim + Path A tier_lock commit + Path B rule sub-list with honest 501 language) | ~200 |
| `pages/master_admin/AuditTrailPage.js` (§6.3 verbatim + audit-trail data-consuming + "See full diff" affordance) | ~140 |
| **Frontend Playwright first-commit-gated smokes** | ~230 |
| `e2e/master_admin_home_smoke.spec.ts` (§6.1 verbatim elements + no-dashboards/no-version-strings/no-config-syntax NEGATIVE assertions) | ~90 |
| `e2e/master_admin_change_a_rule_smoke.spec.ts` (§6.2 verbatim + Path A commit success + Path B 501 rendering) | ~90 |
| `e2e/master_admin_audit_trail_smoke.spec.ts` (§6.3 verbatim + "See full diff" affordance) | ~50 |
| **Frontend Jest binding-copy verbatim gates** | ~90 |
| `test_master_admin_binding_copy_verbatim.test.js` (4 verbatim strings: 6.1 pending copy + 6.1 footer link + 6.2 "Recorded as your change" + 6.3 footer diff copy) | ~90 |
| **§4.2 fixture-schema gate** | ~80 |
| `test_engineer_first_call_fixture_matches_frozen_contracts.test.js` (imports 3 fixtures + reads 3 contract snapshots + property-subset assertions) | ~80 |
| **App.js + apiClient.js modifications** | ~30 |
| **Modifications to `EngineerFirstCallPage.js`** (export 3 fixture constants) | ~5 |
| **Grand total LLoC** | **~1,515** |

**Owner-priced anchor band proposal:** **1,200–1,700 LLoC** (mid ~1,450).

**Contingency (10%):** included in the band width. If mid-block a §6 element is discovered to require additional wiring (e.g., §6.1 pending banner reads from a not-yet-built endpoint), the total may push toward 1,700; band remains valid.

**Rationale for band shape:** narrower than B-3's 1,900-2,900 because:
- No new frozen contract (D4b-analogue not in scope — see §7 below).
- Auth reconciliation is a delete-and-replace, not additive.
- Path B honest-501s are ~10 lines of copy each.
- §6 surfaces are "buttons and sentences only" — the surface Rules explicitly forbid dashboards + config syntax, keeping visual complexity low.

---

## 6 · `snapshot_lloc_in_band` declaration

**`snapshot_lloc_in_band = no`** for B-4.

**Justification:** UI Spec §6 introduces zero new governed records. Tier-lock persistence uses the existing config-as-versioned-not-frozen posture (Ruling R3-SD2) — versioned JSON files on disk, not Pydantic-frozen contracts. Audit-trail reads existing `NorthenaLedgerRow_v1` (frozen contract 6, snapshot unchanged). No parity 26 → 27 candidate.

**Escalation if my reading of §6 is wrong:** if in-block I discover that §6 mandates a NEW frozen record (e.g., an explicit `MasterAdminRuleChange_v0` audit shape distinct from generic `stamp_audit`), I **STOP** and escalate to Owner before minting the contract. Do NOT extend `snapshot_lloc_in_band` mid-block without ruling.

---

## 7 · New-record wire-shape gate flag

**No new governed records → no wire-shape gate needed → no helper extraction triggered.**

Per Owner "extract on second use" trigger:
- B-3 landed 1 hand-authored wire-shape gate on `EngineerKeyGrantRegistration`.
- B-4 introduces zero governed records requiring wire-shape gates.
- Helper extraction remains DEFERRED until a governed record surfaces that would be the second consumer. B-5 (Regulator/DPO §7) is a candidate if it mints e.g., a `RegulatorAuditRequest_v0` unfrozen container; that is the earliest possible extraction trigger.

**If mid-block §6 reveals a governed record needing a gate:** I halt and escalate to Owner rather than silent-mint the helper.

---

## 8 · Test surface roster (enumerated)

**Playwright chromium (first-commit-gated, in-same-commit-as-surface per standing pattern):**
- `master_admin_home_smoke.spec.ts` — §6.1 verbatim elements (13) + 3 NEGATIVE assertions (no dashboards / no version strings / no config syntax).
- `master_admin_change_a_rule_smoke.spec.ts` — §6.2 verbatim elements (6) + Path A commit happy path + Path B 501-plain-language surfacing.
- `master_admin_audit_trail_smoke.spec.ts` — §6.3 verbatim elements (4) + "See full diff" affordance on-demand.

**Jest binding-copy verbatim (Owner Condition 3-carried):**
- `test_master_admin_binding_copy_verbatim.test.js` — 4 verbatim strings:
  1. §6.1 pending: "Two rules are waiting on your decision before they can take effect." (with count-substitution rendering test).
  2. §6.1 footer link: "See everything I've changed — every action is recorded."
  3. §6.2 post-commit: "Recorded as your change, with today's date." + today's date rendered.
  4. §6.3 footer: "Every row carries its full diff. This trail is itself append-only and readable by the regulator surface."

**Backend Path A ledger integration (mirror B-3 D4b P0):**
- `test_master_admin_tier_lock_path_a_ledger.py` — tier_lock POST emits `NorthenaLedgerRow_v1` with `stamp_audit.data_class="master_admin_rule_change"` + idempotency by `idempotency_key` + versioned file write (`tier_lock.vN.json` where N is next serial).

**Backend Path B honest-501:**
- `test_pricing_paths_b_honest_501.py` — POST /pricing/model_version + POST /fleet/policy return 501 with plain-language `detail` (no technical hint / no `vN.json` string in detail).

**Backend auth reconciliation (Owner E2 registry-closed):**
- `test_master_admin_auth_reconciliation.py` — parametrised over pricing + fleet + master_admin write endpoints × 3 auth postures (no-auth → 401 auth_missing; JWT-authed non-master → 403 auth_scope_insufficient; JWT-authed master_admin → 200/501-as-declared). Body shape `{reason, detail}` only; NO `outcome` key on auth denials.

**Backend §6.3 audit-trail read:**
- `test_master_admin_recent_actions.py` — GET /api/master_admin/recent_actions returns filtered ledger rows (data_class="master_admin_rule_change") rendered as plain-language description objects. No raw JSON diff in primary payload; `full_diff_ref` link only.

**§4.2 fixture-schema gate (Owner B-4 first-commit mandate):**
- `test_engineer_first_call_fixture_matches_frozen_contracts.test.js` — 3 fixture-contract pairs validated against frozen snapshots.

**Total new test files:** 8 (3 Playwright + 5 Jest / pytest).

**Existing test-file updates required:**
- `test_phase_6_stage_b_economics.py` — swap `X-RMS-Master-Admin` header injection for JWT master_admin login (test-only change; net-zero backend semantic).

---

## 9 · Escalations to Owner

**None beyond the Pre-Rules already ratified.**

Enumerated non-blockers (informational; no ruling requested):
- **§6.3 diff-primary-display posture** — my reading is that a "See full diff" collapsed affordance satisfies the rule "the diff exists in the record; it is never the primary display." If Owner prefers a modal/drawer instead of an inline expandable, that's a rendering nit best raised at Stage-B implementation review, not a Stage-A blocker.
- **§6.1 pending-banner data source** — my reading is that "waiting on your decision" refers to rules that have been PROPOSED but not committed. In today's backend, no such "proposal queue" exists (the only mutable rule is tier_lock, which commits directly). The banner surface at B-4 renders count=0 in the initial state and reveals the surface pattern; a real proposal-queue is a future feature. Informational disclosure — no Stage-A ruling requested.
- **Retire timeline for `RMS_MASTER_ADMIN_TOKEN`** — if kept in `.env` for operator convenience after B-4 close, it becomes dead-env. Suggest a Phase-8-close housekeeping item to prune. Not a Stage-A blocker.

---

## Stage-A summary

- **§6 surface reading:** 3 sub-surfaces (§6.1 Home + §6.2 Change-a-rule + §6.3 Audit-trail); 23 total verbatim elements + 3 NEGATIVE-assertions.
- **Pre-Rule 1:** Path A for tier_lock; Path B (honest 501) for model_version + fleet_policy. Path A endpoint spec inlined with ledger integration.
- **Pre-Rule 2:** RETIRE `RMS_MASTER_ADMIN_TOKEN` — replace with JWT `master_admin` role; zero production consumers audited.
- **§4.2 fixture-schema gate:** JS-native filesystem read of `.contract_snapshot.json` neighbors + property-subset assertions across 3 fixture-contract pairs.
- **Rule 2 anchor band:** **1,200–1,700 LLoC** (mid ~1,450); realistic estimate ~1,515 LLoC.
- **`snapshot_lloc_in_band = no`** (no new frozen contracts).
- **No new wire-shape gate** (no new governed records; helper extraction remains deferred to second-use trigger).
- **Test surface:** 8 new gates (3 Playwright + 5 backend/frontend Jest) + 1 existing test file update.
- **Escalations:** none beyond Pre-Rules.

**Ready to proceed to Stage B implementation on Owner ratification.** No ruling-conditioned pause required.
