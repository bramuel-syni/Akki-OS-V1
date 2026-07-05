# Phase 8 Stage B-2 — Close Report

**Phase:** 8 Stage B-2 (implementation, DELIVERED)
**Date:** 2026-07-05
**Delivery format:** Standing Rule v3 (Owner ruling, Phase 6 Stage B close, 2026-07-04).
**Doctrine anchors:** UI Spec v1 §2 verbatim + Substrate-Drop v2 §0.1 (frozen) + Standing Rule v3 + Owner Rulings on E1-E8 (Phase 8 Stage A) + Owner B-2 dispatch ratifications (Playwright first-commit + §2 verbatim + session-binding decorator + scope-enforcement gate pair).
**Parity:** 26 frozen contracts byte-identical (unchanged).
**Backend CI:** 777 → 791 (+14 gates: session-binding × 4, operator/status × 2, scope-gate pair × 4, standing-constraint regression × 4).
**Frontend CI:** 47 / 47 unchanged.
**Playwright chromium smoke:** LANDED (was config-only at B-1; deps installed + `test:e2e` script + 1 authenticated smoke scenario now **EXECUTED GREEN**).
**Rule 2 v2 band:** 980-1820 (mid ~1400) → **actual ~1,220 raw LoC → WITHIN BAND** (~67% of top-of-band; `snapshot_lloc_in_band=no`).

---

## §1 — First commit block: Playwright completion (Owner-mandated ordering)

Owner verbatim on ordering: *"(a), as B-2's first commit — deps installed, smoke green, before any surface work. (b) is rejected outright: deferring the regression gate to end-of-phase parks it precisely through the four surface builds it exists to guard."*

**Executed as B-2 first commit (before any surface work):**

1. `yarn add -D @playwright/test` → installed `@playwright/test@1.61.1` + `playwright-core@1.61.1` + `playwright@1.61.1` (devDependency; hoisted).
2. `npx playwright install chromium --with-deps` → chromium browser downloaded to `/pw-browsers`.
3. Renamed `e2e/ask_console_smoke.spec.js` → `e2e/ask_console_smoke.spec.ts` (Owner verbatim filename; Playwright's built-in TS support handles it with zero tsconfig changes).
4. Added `"test:e2e": "playwright test --project=chromium"` script to `package.json`.
5. Ran `PLAYWRIGHT_BROWSERS_PATH=/pw-browsers PLAYWRIGHT_BASE_URL=http://localhost:3000 yarn test:e2e` → **1 passed (chromium, 905 ms)**.

**Retroactive note on B-1's record:** Playwright gate was CONFIG-ONLY at B-1 (deps not installed, spec not executed). At B-2 first commit the gate is LANDED — cross-reference for B-1's record: `/app/docs/close_reports/phase_8_b_1.md` SHA `b6d5c7a1ea0aaffa7b2a27dc31d96fd8c64f1ff071caf75913ffe6dde6c3f1fe` (Playwright config surface only) → **Playwright deps + smoke execution CLOSED at B-2 first commit** (this close report).

**Playwright evidence in this close (Owner condition on B-1 acceptance):**
```
Running 1 test using 1 worker
[1/1] [chromium] › e2e/ask_console_smoke.spec.ts:52:1 › ask_console_smoke_authenticated_flow_end_to_end
  1 passed (905ms)
```

---

## §2 — UI Spec §2 verbatim landing (no partial rendering)

Owner verbatim: *"'§2 verbatim' is the phrase that matters: no partial rendering of the binding spec."*

### §2.1 Operator Home (`/operator/*` → `OperatorHomePage.js` 203L)

- **Calm header** (§1.7): `RMS Intelligence · operator` + **Commission objective** button (`data-testid="operator-commission-objective"`) → routes to `/operator/commission`.
- **Status line** (§2.1 binding-copy pattern): `data-testid="operator-status-line"` renders *"Running normally."* by default; *"One item needs you."* when `status.attention !== null` (§2.1 exception-threshold-crossing rule).
- **Attention card** (§2.1: at most one per exceeded threshold): `data-testid="operator-attention-card"` renders `what_happened` + `number vs threshold` + **Review** action (`data-testid="attention-review"`). Absent at B-2 baseline (no thresholds crossed).
- **Running list** (§2.1: rows of objective name + entry type · stage + budget consumed): `data-testid="operator-running-list"` iterates `status.running`; row `data-testid={`running-row-${objective_id}`}` shows `objective_id`, `entry · stage`, `trace_id` (first 12 chars). Empty state: `data-testid="running-empty"` renders *"Nothing running."*
- **Capacity strip** (§2.1 approved addition, Owner-called-out explicitly): `data-testid="operator-capacity-strip"` reads `GET /api/fleet/policy` (Phase 6b live) + renders three columns (Mining / Transforms / Live path) with `data-testid` each. Version stamp visible per §1 disclosure norms.
- **Rules preserved** (§2.1): no dashboards or charts by default (verified in-code: zero chart libraries imported); exceptions render only through the attention card.

### §2.2 Commission Wizard (`/operator/commission` → `CommissionWizardPage.js` 243L)

- **Layout** (§2.2): two-column responsive grid — chat pane (`data-testid="commission-chat-pane"`) LEFT + Objective draft rail (`data-testid="commission-draft-rail"`) RIGHT.
- **Chat pane** (§2.2):
  - Session initiated on mount via `POST /api/wizard/operator/session` (Bearer wire live; new session binds to caller identity via `services/auth/session_binding.py`).
  - First agent turn advances immediately (turn_ref-less).
  - Each turn rendered as `data-testid={`chat-turn-${turn_ref}`}`; agent content preserved verbatim; `feasibility_snapshot_ref` renders as inline **estate-check chip** (§2.2 verbatim: *"estate-check chip renders inline before a feasibility-dependent question"*).
  - User submits via textarea → `POST /api/wizard/operator/{sid}/turn` with `turn_ref` (Guard 1 pairing).
- **Draft rail** (§2.2):
  - Eight mandatory fields enumerated (`reach`, `output.form`, `output.consumer`, `output.grain`, `output.standard`, `envelope.done_condition`, `envelope.budget`, `envelope.lawful_basis`).
  - Three visual states per field: **filled** (check icon), **open** (muted `— open`), **agent-assumed** (amber chip `data-testid={`draft-agent-assumed-${label}`}`).
  - Envelope line at bottom: *"done-condition: X · budget: Y · lawful basis: Z"* renders committed values or `—` placeholders.
- **Rules preserved** (§2.2):
  - Mandatory fields asked, never pre-filled (draft rail shows `— open` on absent fields).
  - Every turn grounded in a real estate read (feasibility_snapshot_ref rendered — no fabricated availability).

### §2.3 Freeze — commit review (`/operator/commit-review/:sessionId` → `CommitReviewPage.js` 250L)

- **You supplied** rows (§2.3): `data-testid="you-supplied-section"` iterates `review.you_supplied[]`; each row `data-testid={`you-supplied-${field}`}` shows `{field: value}`.
- **Agent assumed — confirm or change** rows (§2.3): `data-testid="agent-assumed-section"` iterates `review.agent_assumed_items[]`; each row `data-testid={`agent-assumed-${field}`}` carries the amber chip `data-testid={`agent-assumed-chip-${field}`}` + `data-testid={`agent-assumed-change-${field}`}` change link.
- **Violations section** (renders only when non-empty): `data-testid="violations-section"` blocks freeze; enumerates each violation.
- **Feasibility verdict card** (§2.3 success treatment): `data-testid="feasibility-verdict-card"` renders when `ready_to_freeze === true`; binding-copy pattern *"Floor feasible — the in-scope estate meets your standard."*
- **License class drift signal** (B-3 extension): `data-testid="license-class-drift"` renders soft-signal chip when `review.license_class_drift !== null` (committed → derived).
- **Envelope line** (§2.3): `data-testid="envelope-line"` renders lawful basis · budget · commissioner · scope ceiling respected.
- **Freeze objective button** (§2.3): `data-testid="freeze-objective-btn"` — disabled unless `ready_to_freeze && !busy`. On click: `POST /api/wizard/operator/{sid}/freeze` → renders `data-testid="frozen-confirmation"` with `trace_id` + `ledger_run_id` on success.
- **Verbatim binding copy** (§2.3): `data-testid="freeze-binding-copy"` renders *"Frozen is immutable — a changed intent is a new objective."* — visible before AND after freeze.

### §8 Shared component reuse (Owner E3 barrel — B-1 landing)

All three operator pages import `AuthDeniedNotice` from `components/ui_spec_v1` barrel. Zero reimplementation of shared components. Barrel single-source gate at B-1 (`test_shared_components_single_source.test.js`) remains GREEN post-B-2 pages landing.

---

## §3 — Backend wiring

### 3.1 Session-binding decorator on operator wizard router (§0.2 debt landing surface)

New module-level helper `_check_session_ownership_or_deny(session_id, request)` at `routers/wizard_operator.py`:
- Reads Bearer token via `get_current_identity_or_none`.
- If session is grandfathered (no binding on disk) → permit (Owner-ratified carve-out).
- If bound + caller identity matches → permit.
- If bound + caller anonymous OR different identity → **403** with `{reason: "auth_identity_mismatch_for_wizard_session", detail: ...}` via `auth_refusal.emit(...)`.

**Wired into 5 operator endpoints (all `POST /{sid}/*` + `GET /{sid}`):**
1. `POST /api/wizard/operator/{sid}/turn`
2. `POST /api/wizard/operator/{sid}/provenance-refusal`
3. `POST /api/wizard/operator/{sid}/commit-review`
4. `POST /api/wizard/operator/{sid}/freeze`
5. `GET  /api/wizard/operator/{sid}`
6. `POST /api/wizard/operator/{sid}/handoff`

`POST /api/wizard/operator/session` (session creation) receives the caller identity via `get_current_identity_or_none`; if authenticated, `session_binding.bind_session_to_identity(session_id, user_id)` records the ownership tuple.

**Buyer router wiring is Phase 8 B-3 scope-scoped** (Owner-ratified: B-2 wires operator only; buyer surface arrives at B-3 with its own decorator wiring).

### 3.2 `GET /api/operator/status` (new read-only route)

New router `routers/operator.py` (78L). Read-only aggregate for UI Spec §2.1 Home:
- Anonymous → `{identity: null, running: [], attention: null, status_line: "Running normally."}` — surface still renders; no per-user projection.
- Authenticated → `{identity: {user_id, email, roles}, running: [...], attention: null, status_line}` — running projection via `async_state_service.list_objectives_in_state("running", limit=10)`.
- **G5a read-only invariant preserved:** the helper degrades to empty list on missing subsystem rather than mutate any store.

### 3.3 Scope-enforcement gate pair on `POST /api/service_1/v2/dispatch` (Owner E1+E2 ratified symmetric-E2 cut)

Owner ruling verbatim: *"The proof is a gate pair, not a wire change: granted key → 200, insufficient key → 403 with the E2 body, both curl-attested. ~30 LoC, zero envelope delta, and the ComposedConclusion_v0 question dissolves — nothing touches it."*

**Implementation (~40L including docstring inside `routers/service_1.py::v2_dispatch_endpoint`):**
- Endpoint signature extended: `v2_dispatch_endpoint(request: ObjectiveRequest_v2, http_request: Request)`.
- Anonymous (no Authorization) → **fall through** (Ask Console B-1 anonymous-friendly posture preserved).
- Authenticated → `key_grants.check_scope(identity, class="external", path="live_query", floor=<from request.output.standard.minimum_class.value>, scope=<from request.envelope.scope_ceiling>)`:
  - Granted → dispatch executes (200 / 202 / 422 / 501 / 503 — full existing wire-table fork preserved).
  - Insufficient → `auth_refusal.emit("auth_scope_insufficient", detail=...)` → 403 with `{reason, detail}` body.

**ZERO envelope delta (Owner symmetric-E2 cut):**
- `ComposedConclusion_v0` UNTOUCHED (parity 26 preserved).
- `AdmissionRefusal_v0` UNTOUCHED.
- Response body for 200/202/422 carries no `granted`, no `matched_grant_id`, no `required` tuple, no `auth_scope`, no `auth_grant`, no `key_grants_used` (`test_b2_v2_dispatch_scope_gate_granted_key_dispatch_executes` asserts absence of all 6 keys).

**Live curl attestation (E2E):**
```
=== HALF 1: GRANTED admin key + estate scope → dispatch executes ===
HTTP 202
{"objective_id":"obj-b81578c13c27","status":"accepted","delivery_estimate":"PT30M","quote":{...}}

=== HALF 2: register new user WITHOUT scope grant → INSUFFICIENT key ===
HTTP 403
{"reason":"auth_scope_insufficient","detail":"Caller identity is authenticated but no granted key matches the required scope tuple (class=external, path=live_query, floor='utterance', scope='estate')."}
```

Half-1 body carries no auth metadata (verified). Half-2 body carries `{reason, detail}` only — no `outcome` key, no `AdmissionRefusal_v0` discriminator (verified).

**Floor-hierarchy honored:** a grant with `floor=established_fact` implicitly satisfies asks with `floor=utterance` (`test_b2_v2_dispatch_scope_gate_floor_hierarchy_higher_floor_grant_permits_lower_floor_ask` GREEN).

---

## §4 — Machine-attested block

```
[GREEN] pytest -q                                              791 / 791 (+14 vs B-1 baseline 777)
[GREEN] parity                                                 26 / 26 frozen contracts byte-identical
[GREEN] shield boundary                                        zero LLM imports outside services/synisense/shield/*
[GREEN] session-binding decorator gate (4 endpoints × identity states)  4 / 4
[GREEN] GET /api/operator/status (anon + authed)               2 / 2
[GREEN] Scope-enforcement gate PAIR on POST /v2/dispatch       4 / 4 (granted / insufficient / anonymous / floor-hierarchy)
[GREEN] Standing constraint regression (parity + imports + route registration)  4 / 4
[GREEN] frontend Jest ui_spec_v1                               47 / 47 unchanged
[GREEN] Playwright chromium smoke                              1 / 1 EXECUTED (was config-only at B-1)
[GREEN] webpack compilation                                    Compiled successfully.

# Live curl-attested scope-gate PAIR (Owner E1+E2 non-negotiable proof):
HALF 1 (granted admin key, estate scope): HTTP 202 with async_delivery_accepted body — NO auth metadata on wire.
HALF 2 (insufficient key, new registered user, no matching grant): HTTP 403 with {"reason":"auth_scope_insufficient","detail":"..."} — NO outcome key.
```

---

## §5 — Files touched at B-2

**Backend NEW (2):**
- `routers/operator.py` (78L)
- `tests/invariants/test_phase_8_b_2_operator_and_scope_gate.py` (~330L, 14 tests)

**Backend MODIFIED (3):**
- `routers/wizard_operator.py` (+41L: `_check_session_ownership_or_deny` helper + wiring across 6 endpoints + session-binding on POST /session)
- `routers/service_1.py` (+40L: scope-enforcement gate + docstring + import lines; endpoint signature extended)
- `server.py` (+3L: operator router registration)

**Frontend NEW (3 source + 1 dep + 0 test = 4):**
- `src/pages/operator/OperatorHomePage.js` (203L)
- `src/pages/operator/CommissionWizardPage.js` (243L)
- `src/pages/operator/CommitReviewPage.js` (250L)
- `package.json` +1 devDependency (`@playwright/test@1.61.1`) + 1 script (`test:e2e`)

**Frontend MODIFIED (2):**
- `src/apiClient.js` (+30L: `operatorStatus`, `fleetPolicy`, 5 wizard operator endpoints)
- `src/App.js` (+5L: 3 operator routes)

**Frontend RENAMED (1):**
- `e2e/ask_console_smoke.spec.js` → `e2e/ask_console_smoke.spec.ts` (Owner verbatim filename)

**Docs / memory MODIFIED (5):**
- `docs/rule2_accounting.json` (+1 phase entry `Phase 8 Stage B-2`)
- `memory/ORCHESTRATOR_CONTINUITY.md` (§2 phase-ledger + §3 current live state)
- `memory/PHASE_STATE.md` (B-2 close)
- `memory/PRD.md` (B-2 dispatch section)

**Docs NEW (1):**
- `docs/close_reports/phase_8_b_2.md` (this file)

**Total LoC:** ~1,220 raw (backend ~495 + frontend ~730 + docs uncounted per Owner cap).

---

## §6 — §0.2 Plan Debt status

No new §0.2 debts arose at B-2. Existing status:
- Wizard session-ownership binding — **RESOLVED at B-1**; ROUTER-DECORATOR WIRING for operator variant landed at B-2 (surface-scoped mechanical follow-up per B-1 close observation). Buyer variant wiring is Phase 8 B-3 sub-stage scope.
- Envelope-shim helper triad extraction — remains **RESOLVED at B-1**.
- Trajectory restatement debt — remains **RESOLVED at Stage A**.
- DPO `wizard_transcript` separately-addressable — remains OPEN (Phase 8 B-5 sub-stage-scoped).

---

## §7 — Standing constraints compliance (all preserved)

- 26 frozen contracts byte-identical ✅
- Shield boundary (LLM only inside `services/synisense/shield/*`) ✅
- §0.1 Standing Dispositions FROZEN (zero additions) ✅
- Standing Rule v3 delivery ✅
- Substrate-drop 9/9 GREEN ✅
- Read-only route invariant (G5a) ✅ (operator/status is read-only; degrades to empty list rather than mutate)
- Outer-gate irreversibility invariant (G6) ✅
- V2 refusal terminality (G6) ✅
- Ruling 3 config-as-versioned-not-frozen ✅
- Ruling 4 shared-derivation ✅
- Frozen-field-changes-as-new-versions ✅ (ObjectiveRequest_v2 signature TOUCHED — new `http_request: Request` parameter — this is an ADDITIVE FastAPI dependency injection, NOT a frozen-contract field change; verified `test_frozen_contract_snapshot_parity` GREEN)
- Infra-not-refusal ✅
- **Auth-not-refusal** (Owner E2 non-negotiable, symmetrically-cut): 403 does not wear governance-refusal clothes (registry-exclusion + no-RefusalCard gates preserved from B-1) AND auth metadata does NOT flow into the intelligence envelope in the 200/422 direction either (Owner E1+E2 gate pair curl-attested, ZERO envelope delta verified) ✅
- Wizard `wizard_transcript` retention marker preserved ✅
- No `git push` ✅
- No refactoring (additive-only, surface builds) ✅
- Disposition-must-cite-owner-ruling ✅
- Sizing-anchor-declares-snapshot-inclusion — B-2 declared `snapshot_lloc_in_band=no` at Stage A + confirmed at close ✅
- E1 federation-forward posture ✅ (session-binding uses identity from JWT; OAuth adapter drop-in later would flow through the same seam)
- E1 scope-enforcement per call (LANDED at B-2 on `POST /v2/dispatch` — first live governed endpoint with scope enforcement) ✅
- E2 4-code bounded set + `{reason, detail}` body + registry-exclusion + console render-path (all preserved) ✅
- E3 grep-negative gate parametrised × 3 triad symbols ✅

---

## §8 — Ready for B-3 (Engineer + Buyer surfaces per §4 + §5)

**YES — ready.**

**Observations for B-3 dispatch consideration:**

1. **E4 posture note (Owner reserved):** *"The B-3 steer stands — schema as Pydantic model, freeze-or-not argued at B-3 against actual wire exposure. Pre-ruling now adds no information; it would be deciding early for comfort."* B-2 preserved this stance and made **zero** engineer-key design choices; B-3 open sees the actual wire exposure and rules D4b (freeze-or-not) then.

2. **Session-binding decorator pattern is available for buyer wiring at B-3:** the operator-side `_check_session_ownership_or_deny(session_id, request)` helper is copy-ready for `routers/wizard_buyer.py`; B-3 mechanical follow-up is 5 minutes.

3. **Scope-enforcement pattern is proven on the live governed endpoint:** `POST /v2/dispatch` scope gate is the reference implementation for the buyer-surface `POST /api/objectives` scope enforcement (if B-3 opens with that scope).

4. **Playwright infrastructure LIVE (Owner-mandated at B-2 first commit):** deps installed, chromium browser downloaded, `test:e2e` script wired, smoke passes GREEN. B-3 can add per-surface smoke scenarios without any config work.

5. **Master-Admin surface at B-4 will exercise the versioned-config bump pattern (Ruling 3):** confirming `pricing_tiers.vN.json` + `fleet_policy.vN.json` write endpoints. Zero new frozen contracts anticipated.

---

## §9 — Escalation Posture summary

No new escalations arose at B-2. E5/E6/E7 remain in their Stage-A-anchored positions (E5 → B-5, E6 → B-5 in-pod route, E7 → chromium-only affirmed by B-2 execution).

E4 remains DEFERRED to B-3 open per Owner (steer verbatim in Stage A §8 as edited at B-1 close).

---

*End of Phase 8 Stage B-2 close report. Awaiting Owner ratification before Phase 8 B-3 (Engineer + Buyer surfaces) dispatch.*
