# Phase 8 Stage A — Frontend Surfaces (DESIGN-ONLY)

**Phase:** 8 Stage A (Design-only, no code writes)
**Date:** 2026-07-04
**Delivery format:** Standing Rule v3 (Owner ruling, Phase 6 Stage B close, 2026-07-04): on-disk canonical + SHA in return; return summary carries one-line disposition enumerations only.
**Doctrine anchors:** UI Spec v1 §§1-8 (binding; canonical mockups) + UX Architecture v2 §4.3 + RMS v3 §3.3 (wizard) + §7 (async) + §8 (economics) + §5 (feasibility) + Standing Dispositions §0.1 (all frozen).
**Owner pre-rulings binding this proposal:** Standing Rule v3 (delivery) + `Sizing-anchor-declares-snapshot-inclusion` + `Agent-pluggable-with-stub-agent-first` + `Visibility-not-prohibition` + `Infra-not-refusal` + `Frozen-field-changes-as-new-versions` + `Wizard session-ownership binding` plan-debt (§0.2) + Phase 8c DPO `wizard_transcript` separately-addressable plan-debt (§0.2, refined this dispatch).
**Status:** DESIGN PROPOSAL. Parity stays 26. Zero code writes. No new frozen contracts landing at Stage A.

---

## Preamble — Mandatory `wizard_not_frozen` 422 body-shape confirmation (Owner condition, Phase 7 Stage B-3 close acceptance)

Investigated `backend/routers/wizard_buyer.py` (lines 390-406) + `backend/routers/wizard_operator.py` (lines 336-352). Both routers emit **identical shape** at both fire sites (in-memory session absent-but-not-persisted AND persisted-but-`committed_at is None`):

```json
{"reason": "wizard_not_frozen",
 "detail": "handoff requires a frozen wizard session; call POST /freeze first."}
```

**Emission mechanics:** `JSONResponse(status_code=422, content={...})`. NOT a Pydantic model. NOT registered in any refusal-reason registry.

**Discriminator check:**
- ❌ Does NOT carry `outcome=refused`.
- ❌ Does NOT carry the `AdmissionRefusal_v0` discriminator (no `asked` / `supported_class` / `what_would_raise_it` / `what_you_can_do` fields; no `outcome` field at all).
- ✅ Carries `reason` (bounded string literal `"wizard_not_frozen"`) + `detail` (human-readable string).

**Doctrinal posture (already documented in the B-3 close report §5 and ORCHESTRATOR §3 line 116 verbatim):** *"`wizard_not_frozen` is an ad-hoc router-layer 422 body, NOT registered as an admission-refusal reason."*

**Frontend consequence (already live at 8a-lite):** `apiClient.dispatchV2(...)` discriminates refusals on `body.outcome === "refused"`. Because `wizard_not_frozen` carries no `outcome` field, the frontend's `RefusalView` renderer will NOT match; it falls through to `InfraFaultView` / precondition-error rendering. This is the correct behavior for a router-layer precondition failure (governance surface reserves refusal semantics for `AdmissionRefusal_v0` / `Service1Refusal_v0`).

**Phase 8 Stage B remediation stance:** the wizard-handoff endpoint is invoked only from the wizard commit-review → freeze → handoff flow (§2 buyer + §5 buyer wizard surfaces). The wizard surface has full session-state locally; it will render `wizard_not_frozen` as a **precondition-not-yet-met** prompt ("Freeze the objective first, then hand off"), NOT as a refusal card and NOT as an infra fault. Named binding gate at Phase 8 Stage B: `test_wizard_surface_renders_wizard_not_frozen_as_precondition_not_refusal_not_infra`. No new contract, no registry bump.

---

## §1. Trajectory Restatement (frozen contracts + `snapshot_lloc_in_band` per anticipated sub-stage)

### 1.1 Current parity anchor

**Parity at Phase 7 Stage B-3 close: 26 frozen contracts.**

Enumeration (byte-identical since respective landing phase; guarded by `test_prior_contract_file_exists_and_stable_at_7b_3` parametrised over 25 sources + `test_composed_conclusion_v0_contract_frozen::test_prior_26_contracts_count_at_26`):

1. Five Rings v0
2. Ask v0
3. Objective Request v0 (legacy)
4. Fact Envelope v0
5. Outer Gate Receipt v0
6. Northena Ledger Row v0 (superseded by v1 at Phase 5b for decision axis; v0 preserved byte-identical)
7. Solva Conclusion Trace v0
8. Trust Receipt v0
9. Mtafiti Fact Unit v0
10. Targeta Query v0
11. Service1Refusal v0 (A2)
12. Objective Request v2 (Substrate-Drop v2 Phase 0)
13. FeasibilityResult v0 (Phase 1)
14. AdmissionRefusal v0 (Phase 3)
15. ComposedConclusion v0 (Phase 4b)
16. NorthenaLedgerRow v1 (Phase 5b)
17. AsyncDeliveryAccepted v0 (Phase 5b)
18. QuoteEnvelope v0 (Phase 6b)
19. AsyncDeliveryAccepted v1 (Phase 6b)
20. WizardCommitState v0 (Phase 7 B-1)
21. OperatorTurn v0 (Phase 7 B-1)
22. AgentAssumption v0 (Phase 7 B-1)
23. CommittedValue v0 (Phase 7 B-1)

Plus 3 pre-G6 contracts already tallied within the 26 (backfilled at Substrate-Drop v2 Part 1). Mechanical parity map `test_frozen_contract_snapshot_parity::CONTRACT_TO_SNAPSHOT` bijective at 26 entries.

### 1.2 Restated trajectory through Phase 8

**Prior PM anchor:** *"~22-23 frozen contracts through Phase 8"* (per §0.2 debt, Phase 7 B-1 close). Already **exceeded** at Phase 7 B-1 close (26). This Stage A **RESTATES** the trajectory.

**Restated Phase 8 trajectory:**

| Anticipated sub-stage | New frozen contracts | Running parity | Rationale |
|---|---|---|---|
| Phase 8 Stage B-1 (Auth/key + shared §8 components + Ask Console-full) | **0** | **26** | Auth/key model uses versioned config (Ruling 3 pattern), NOT frozen contracts. Shared §8 components are frontend renderers (no backend contract). Ask Console-full extends 8a-lite frontend (no backend contract). |
| Phase 8 Stage B-2 (Operator surface — Home/Commission/Freeze per UI Spec §2) | **0** | **26** | Operator surface consumes existing `WizardCommitState_v0` + `OperatorTurn_v0` + `AgentAssumption_v0` + `CommittedValue_v0` (contracts 20-23). No new contract. |
| Phase 8 Stage B-3 (Engineer surface + Buyer surface per UI Spec §4 + §5) | **0** | **26** | Engineer surface = key-issuance UI over auth/key config (versioned config, not frozen). Buyer surface consumes existing `WizardCommitState_v0(variant="buyer")` + `QuoteEnvelope_v0` + `AsyncDeliveryAccepted_v1`. No new contract. **Escalation E4:** if key-issuance boundary demands a governed record (e.g. `EngineerKeyGrant_v0`), lands as NEW frozen contract in this sub-stage; parity 26→27. Owner ratifies at Stage B-3 open. |
| Phase 8 Stage B-4 (Master Admin surface per UI Spec §6) | **0** | **26** | All Master Admin actions land as versioned config bumps (`price-model@vN`, `fleet-policy@vN`, `pricing_tiers@vN`, `admission_refusal_reasons@vN`, `retention_config@vN`) — Term 2 / Ruling 3 pattern. Rule changes are NOT frozen contract additions. |
| Phase 8 Stage B-5 (Regulator / DPO surface per UI Spec §7) | **0** | **26** | DPO surface is READ-ONLY over Northena Ledger + trust receipts + retention config. `wizard_transcript` held-class enumeration lands here (see §6.3 below). No new contract. |

**Restated end-of-Phase-8 parity: 26 (unchanged) OR 27 (only if E4 Engineer key-grant contract lands).**

### 1.3 `snapshot_lloc_in_band` declaration per anticipated sub-stage

Per Standing Disposition `Sizing-anchor-declares-snapshot-inclusion` (Owner ruling, Phase 6 Stage B close, 2026-07-04):

| Sub-stage | `snapshot_lloc_in_band` | Notes |
|---|---|---|
| Phase 8 B-1 (Auth/key + shared §8 + Ask Console-full) | **no** | Zero anticipated new snapshots. If auth boundary demands a governed record contract (unlikely under versioned-config posture), flips to `yes` and band expands by ~200 LoC per snapshot. |
| Phase 8 B-2 (Operator surface) | **no** | Frontend-only surface phase; no backend snapshot generation. |
| Phase 8 B-3 (Engineer + Buyer surface) | **conditional: `no` default; `yes` if E4 lands `EngineerKeyGrant_v0`** | Explicit E4 ratification at Stage B-3 open determines the flag. Band expands by ~200 LoC if `yes`. |
| Phase 8 B-4 (Master Admin surface) | **no** | Config-value bumps only; no snapshot generation. |
| Phase 8 B-5 (DPO surface) | **no** | Read-only surface over existing records; no snapshot generation. |

**Standing convention (Owner ratified G6 + Phase 6b):** when `snapshot_lloc_in_band=yes`, machine-generated snapshot JSON counts against the sizing band. Explicit per-sub-stage declaration lands here satisfying the Standing Disposition forward clause.

---

## §2. Six Surfaces per UI Spec v1 + §8 Shared components

**Scope:** UI Spec v1 §§2-7 enumerate six user surfaces. §8 enumerates cross-surface bindings shared across all six. This section restates each surface's Phase 8 Stage B landing shape.

### 2.1 Ask Console (UI Spec §3) — extends Phase 8a-lite

**Status at Stage A:** Phase 8a-lite CLOSED (2026-07-04) — landed §3.1 Ask + §3.2 Answer + §3.3 Refusal binding copy verbatim.

**Phase 8 Stage B-1 Ask Console-full extensions:**

- (a) **Recent list** (§3.1 element): renders last N Ask Console runs for the authenticated identity, keyed by `trace_id`. Reads Northena Ledger via a new READ-ONLY route `GET /api/ask/recent?limit=N` (single-source; no new ledger writes). Read-only invariant per G5a doctrine.
- (b) **Quiet defaults line** (§3.1): renders `Standard: {frozen_default} · Scope: {frozen_default} · change`. `change` link opens a bounded surface for narrowing scope/standard (delegates to Operator wizard §2.2 in-place if identity has operator role; otherwise inert with copy "Widening intent requires a new objective, made elsewhere" per §3.1 binding).
- (c) **Metric cards** (§3.2, up to three): renders top-three quantitative supports from `ComposedConclusion_v0.metrics` field. Each card carries its per-claim class chip.
- (d) **Actions** (§3.2): **Why this answer** (opens trust-receipt lens via `GET /api/trust/{trace_id}` — read-only per G5a), **Export report** (renders same artifact with class markings intact — never a data download, never a re-shape), **Trust receipt** link (public `rms.intel/trace/{id}` URL per §8 cross-surface binding).

**No output-form picker** anywhere on this surface (§3.1 binding rule; 8a-lite gate `test_no_output_form_picker_present_on_ask_surface` GREEN — regression preserved at B-1).

**Backend surface delta:** 1 NEW read-only route `GET /api/ask/recent?limit=N` (~30 LoC). Zero new frozen contracts. Zero registry bumps.

### 2.2 Operator surface (UI Spec §2)

**Phase 8 Stage B-2 landing scope:**

- **§2.1 Home — land** (frontend page `src/pages/operator/OperatorHomePage.js`):
  - Header (`RMS Intelligence · operator`) + **Commission objective** button routes to `/operator/commission` (wizard surface).
  - Status line binding copy: *"Running normally. One item needs you."* (illustrative; renders exception-count from `GET /api/operator/status`).
  - Attention card renders at most one exceeded-threshold event.
  - **Running** list: rows of objective name, entry type · stage, budget consumed. Reads `GET /api/objectives?state=running` (existing Phase 5b endpoint).
  - **Capacity strip:** fleet apportionment + current consumption. Reads `GET /api/fleet/status` (existing Phase 6b endpoint; env-gated `RMS_MASTER_ADMIN_TOKEN` for write, but read is operator-scope).

- **§2.2 Commission — the shaping wizard** (frontend page `src/pages/operator/CommissionWizardPage.js`):
  - Chat pane (left) + Objective draft rail (right).
  - Chat consumes existing wizard operator router: `POST /api/wizard/operator/session` → `POST /api/wizard/operator/{sid}/turn` → `POST /api/wizard/operator/{sid}/commit-review` → `POST /api/wizard/operator/{sid}/freeze` → `POST /api/wizard/operator/{sid}/handoff`.
  - Draft rail renders `WizardCommitState_v0.committed_values` byte-identically per `CommittedValue_v0.source` tag (§2.2 UI Spec: filled=check, open=muted "— open", agent-assumed=amber chip).
  - Estate-check chip inline before each feasibility-dependent turn: renders `OperatorTurn_v0.feasibility_snapshot_ref` result (Guard 3 grounded).

- **§2.3 Freeze — commit review** (frontend page `src/pages/operator/CommitReviewPage.js`):
  - **"You supplied"** rows: renders `committed_values[field].source === "operator_supplied"`.
  - **"Agent assumed — confirm or change"** rows: renders `committed_values[field].source === "agent_assumed"` + amber chip + `change` link.
  - Feasibility verdict card (success treatment; binding copy pattern *"Floor feasible — {n}% of in-scope estate meets your standard"*).
  - Envelope line: lawful basis ref · budget · commissioner · scope ceiling respected.
  - **Freeze objective** button → `POST /api/wizard/operator/{sid}/freeze` → auto-follow with `POST /api/wizard/operator/{sid}/handoff` (already E2E-verified at B-3).
  - Binding copy verbatim: *"Frozen is immutable — a changed intent is a new objective."*

**Backend surface delta at B-2:** 1 NEW read-only route `GET /api/operator/status` (aggregates running-count + attention-card content; ~40 LoC). Zero new frozen contracts.

### 2.3 Engineer surface (UI Spec §4)

**Phase 8 Stage B-3 landing scope:**

- **§4.1 Register an app** (frontend page `src/pages/engineer/RegisterAppPage.js`):
  - App name input.
  - Class choice: **Internal / External**.
  - Path choice: "Live query — inner gate · per-call governance · answers in responses" / "Governed extract — outer gate · rights-checked · datasets and skills out".
  - Key grants panel: plain-language enumeration of what the key permits.
  - **Issue key** button → `POST /api/engineer/keys` (new endpoint).
  - Async additions (approved): optional webhook URL field + sandbox toggle.

- **§4.2 First call — the contract** (frontend page `src/pages/engineer/FirstCallPage.js`):
  - Request block: `POST /v1/objectives` example with ask/standard/scope.
  - Two response panels: **Answered** (outcome, trace_id, claim, defensibility, provenance) + **Refused** (same envelope, body discriminator `outcome: refused`, asked, supported_class, what_would_raise_it).
  - Async variant: fresh-extraction returns `202 {objective_id, accepted, delivery_estimate}`.
  - Binding copy verbatim: *"There is no response shape in which the claim is separable from its class. Infrastructure faults return 500 and are never rendered as refusals."*

- **§4.3 Administer** (frontend page `src/pages/engineer/AdministerPage.js`):
  - Attention card (at most one; pattern: app name — refusal rate — plain cause — Review).
  - Apps list rows: name + class badge, path + key, calls + refusal rate.
  - Extract-path rows: acquisitions + rights state.
  - Async addition: long-running objectives show lifecycle state (`accepted / running / delivered / refused`).
  - Footer binding copy: *"Key scope is enforced server-side on every call."*

**Backend surface delta at B-3:**
- **NEW routes** at `/api/engineer/*`: `POST /keys` (issue), `GET /keys` (list for identity), `POST /keys/{key_id}/revoke`, `GET /apps` (list registered apps), `GET /apps/{app_id}/calls` (call history + refusal rate). Read-only for status; write endpoints require Master Admin scope OR self-scope per auth/key model.
- **Escalation E4:** if the key-issuance boundary demands a governed record contract (a frozen `EngineerKeyGrant_v0` shape byte-identical across API boundaries — trust-receipt style), lands as NEW frozen contract. Otherwise, key records live as versioned config (`engineer_keys.vN.json`) per Ruling 3.

### 2.4 Buyer surface (UI Spec §5)

**Phase 8 Stage B-3 landing scope:**

- **§5.1 Shape — buyer objective wizard** (frontend page `src/pages/buyer/BuyerShapeWizardPage.js`):
  - Chat pane (left) + Your acquisition rail (right).
  - Chat consumes existing wizard buyer router: `POST /api/wizard/buyer/session` → `POST /api/wizard/buyer/{sid}/turn` → `POST /api/wizard/buyer/{sid}/propose` → `POST /api/wizard/buyer/{sid}/commit-review` → `POST /api/wizard/buyer/{sid}/freeze` → `POST /api/wizard/buyer/{sid}/handoff`.
  - Rail: reach; output (form · grain · standard); license; **price card** ("Estimated price", figure, qualifying volume, binding copy *"moves as you shape"*); **delivery estimate beside price** (served-from-qualified = fast; requires-fresh-extraction = queued, longer); feasible-and-offerable line.
  - Estate-check chip inline (renders feasibility_snapshot_ref result).
  - Buyer never sets lawful basis (`variant="buyer"` state machine already enforces this at B-2).
  - Out-of-bounds shapes → refused with reason (renders `AdmissionRefusal_v0` refusal card per §3.3 binding).

- **§5.2 Acquire — the governed acquisition** (frontend page `src/pages/buyer/AcquirePage.js`):
  - Framing binding copy verbatim: *"Every acquisition passes the outer gate. These checks are what make the data lawfully yours to use."*
  - Four check rows: Rights check · Irreversibility transform · Cumulative disclosure check · License issue. Each with state + plain-language description.
  - Footer binding copy verbatim: *"If any check fails, the acquisition is refused with the reason and a path forward — never partially delivered."*

- **§5.3 Receive — deliverable and receipt** (frontend page `src/pages/buyer/ReceivePage.js`):
  - Delivered header + **Download** button.
  - Artifact sample block: per-claim structure (claim, `defensibility { class, contested }`, `provenance { source_ref, trace_id }`).
  - **Outer-gate receipt** card: transform name, key fingerprint, identity categories transformed, license ref (fact and fingerprint only; nothing that could aid reversal — G6 irreversibility invariant preserved).
  - Public trust-receipt line: `rms.intel/trace/{id}` URL pattern.

**Backend surface delta at B-3:** 1 NEW read-only route `GET /api/buyer/deliverables/{objective_id}` (aggregates delivered artifact + receipt; ~50 LoC). Zero new frozen contracts (all shapes consumed already frozen: `ComposedConclusion_v0`, `OuterGateReceipt_v0`, `QuoteEnvelope_v0`, `AsyncDeliveryAccepted_v1`).

### 2.5 Master Admin surface (UI Spec §6)

**Phase 8 Stage B-4 landing scope:**

- **§6.1 Home** (frontend page `src/pages/masteradmin/MasterAdminHomePage.js`):
  - Pending banner (plain language; illustrative *"Two rules are waiting on your decision before they can take effect."* + Review).
  - Prompt: *"What do you want to do?"*
  - Six action buttons (binding labels verbatim): **Assign a role** · **Change a rule** · **Manage keys & access** · **Update the taxonomy** · **Set pricing** · **Apportion GPU capacity**.
  - Footer link: *"See everything I've changed — every action is recorded."*

- **§6.2 Change a rule** (frontend page `src/pages/masteradmin/ChangeRulePage.js`):
  - "The rule" — one plain-language sentence.
  - Short paragraph of current behaviour + on/off implications.
  - Plain **Off / On** options.
  - "What changes" info box.
  - Commit button in natural language ("Turn it on").
  - Binding copy verbatim: *"Recorded as your change, with today's date."*

- **§6.3 What I've changed — audit trail** (frontend page `src/pages/masteradmin/AuditTrailPage.js`):
  - Confirmation line for latest change.
  - Recent actions rows (plain description from → to in words, who, when).
  - Footer binding copy verbatim: *"Every row carries its full diff. This trail is itself append-only and readable by the regulator surface."*

**Backend surface delta at B-4:**
- **EXTENDED routes** at existing `/api/pricing/*` + `/api/fleet/*` (Phase 6b): add plain-language rule descriptions on GET responses; add `POST /api/pricing/tiers`, `POST /api/fleet/policy` for versioned-config bumps. All writes gated by `RMS_MASTER_ADMIN_TOKEN` (existing env-gate).
- **NEW routes** at `/api/admin/*`: `POST /roles` (assign role), `POST /keys/grant`, `POST /taxonomy/update`, `GET /audit_trail` (read-only over versioned-config change history). All writes gated by Master Admin scope.
- Zero new frozen contracts (all changes land as versioned-config bumps per Ruling 3).

### 2.6 Regulator / DPO surface (UI Spec §7)

**Phase 8 Stage B-5 landing scope:**

- **§7.1 Home** (frontend page `src/pages/dpo/DpoHomePage.js`):
  - Trace lookup input (*"Look up any run, claim, or acquisition by trace…"*).
  - Attention card: honest problems (retention overruns, unset rules, refusals).
  - Three cards: runs with lawful basis · refusals this month + **See what was refused** link · retention windows past due.
  - Footer binding copy verbatim: *"This is the same record every user's audit view reaches — read-only, nothing reconstructed for display."*

- **§7.2 Prove one run** (frontend page `src/pages/dpo/ProveRunPage.js`):
  - Lawfulness banner (LB ref · commissioner · frozen and immutable).
  - Record rows: Lawful basis · Scope · Refused ({n} items — below the required standard, recorded not dropped + **See them**) · Standard · Ledger (append-only; current retention state stated honestly).
  - Footer binding copy verbatim: *"Read-only. This is the record itself, not a summary of it. Export for a regulator on request."*

- **§7.3 Retention & rights** (frontend page `src/pages/dpo/RetentionRightsPage.js`):
  - Honest banner binding copy verbatim: *"No deletion rule is set. The system holds everything indefinitely and append-only until you set a retention window. This is a decision only you can make — the system won't guess a duration."*
  - Holdings rows: within window / past due (+ **Decide**) / delivered acquisitions (irreversibly transformed · licensed · receipts on file).
  - **`wizard_transcript` held-class enumeration** (Phase 7 B-1 debt, refined this dispatch per Owner ruling — see §6.3 below): renders `wizard_transcript` as a **separately-addressable** row, distinct from other held-classes.
  - Footer binding copy verbatim: *"Setting a retention window here becomes a governed rule — versioned, dated, and recorded like every control change."*

**Backend surface delta at B-5:**
- **NEW read-only routes** at `/api/dpo/*`: `GET /trace/{trace_id}` (full run lens — reuses Phase 5b + Phase 6b trace lens), `GET /refusals?month=YYYY-MM` (refusal enumeration), `GET /retention/holdings` (retention window status per held-class INCLUDING `wizard_transcript` separately-addressable), `POST /retention/decide` (versioned-config bump for retention window per held-class; Master Admin scope OR DPO scope).
- Zero new frozen contracts. Read-only invariant per G5a doctrine (`test_trace_lens_readonly` still GREEN — verified at each sub-stage close).

### 2.7 §8 Shared / cross-surface components

**Phase 8 Stage B-1 landing scope** (before any surface-specific page — foundation layer):

- **Shared component: `<ClassBadge>`** (already at `src/components/ClassBadge.jsx` per 8a-lite). Renders defensibility class in plain language ("Established fact", "Recorded statement", etc.) in the headline position. Never renders raw enum value. Byte-identical across all six surfaces. Binding for §1 rule 2 "Class-with-claim".

- **Shared component: `<RefusalCard>`** (already at `src/components/RefusalCard.jsx` per 8a-lite). Renders `AdmissionRefusal_v0` / `Service1Refusal_v0` in the answer position with warning treatment. Names the gap · shows asked vs supported class · offers only actor-appropriate actions. Never rendered as an error. Binding for §1 rule 3.

- **Shared component: `<AgentAssumedChip>`** (NEW at Phase 8 B-1 — `src/components/AgentAssumedChip.jsx`). Amber chip for any value an agent supplied. Reads `CommittedValue_v0.source === "agent_assumed"`. Binding for §1 rule 4.

- **Shared component: `<TraceReceiptLink>`** (already at `src/components/TrustReceiptLink.jsx` per 8a-lite). Renders `rms.intel/trace/{id}` public URL. Binding for §1 rule 5 and §8 cross-surface binding.

- **Shared component: `<QuietDefaultsLine>`** (NEW at Phase 8 B-1 — `src/components/QuietDefaultsLine.jsx`). Renders "Standard: {default} · Scope: {default} · change" line. Reused by Ask Console §3.1 + Buyer §5.1.

- **Shared component: `<AttentionCard>`** (NEW at Phase 8 B-1 — `src/components/AttentionCard.jsx`). Single-attention-card pattern per §1 rule 7. Reused by Operator Home §2.1 + Engineer Administer §4.3 + Master Admin Home §6.1 + DPO Home §7.1.

- **Shared component: `<InfraFaultView>`** (already at `src/pages/AskConsolePage.js` per 8a-lite — refactor to shared `src/components/InfraFaultView.jsx` at B-1). Renders infrastructure faults as system errors, never as refusals. Binding for §1 rule 3 second clause.

- **Shared component: `<CalmHeader>`** (NEW at Phase 8 B-1 — `src/components/CalmHeader.jsx`). `product · role` pattern per §1 rule 7 visual family. Six variants: operator / engineer / buyer / master admin / dpo / ask-console.

**Shared backend module (Phase 8 B-1):**
- **NEW module `services/auth/`** — auth/key model per Wizard session-ownership binding plan-debt (§0.2 line 59). Structure:
  - `services/auth/__init__.py`
  - `services/auth/identity.py` — identity model (auth boundary primitive).
  - `services/auth/key_grants.py` — key-scope resolution (per-call gating).
  - `services/auth/session_binding.py` — binds `wizard_session_id → identity_id`; used by wizard routers to enforce session ownership.
  - `services/auth/keys.vN.json` — versioned key registry (Ruling 3 pattern; N starts at 0 at B-1).
- Auth backend integration TBD at Stage B-1 dispatch — **Escalation E1** below.

---

## §3. Playwright Ask Console Smoke (`/app/frontend/e2e/ask_console_smoke.spec.ts` — SHAPE)

### 3.1 Target directory + file (currently absent)

**Verified at Stage A:** `/app/frontend/e2e/` directory does NOT exist. Phase 8 Stage B-1 creates it.

**Target file:** `/app/frontend/e2e/ask_console_smoke.spec.ts` (~180 LoC anticipated).

### 3.2 Smoke test shape (Playwright TypeScript)

Six named scenarios, each testing one binding rule from UI Spec §3:

1. **`ask_console_home_renders_prompt_and_input`** — navigate to `/`; assert:
   - Centered prompt text = *"What do you need to know?"* (§3.1 binding copy verbatim).
   - Single input visible.
   - **No `<select>` element** anywhere on page (§3.1 no-output-picker rule — regression from 8a-lite gate).
   - Quiet defaults line visible with "Standard:" and "Scope:" prefixes.
   - Recent list container visible (may be empty).

2. **`ask_console_submits_ask_and_renders_answer_on_200_composed_conclusion`** — mock `POST /api/service_1/v2/dispatch` returning `ComposedConclusion_v0(@200)`:
   - Type an ask into the input; click submit.
   - Await answer surface (§3.2).
   - Assert class badge visible in headline position + meta line (`{n} sources examined · answered in {t}`).
   - Assert headline finding (one sentence) rendered.
   - Assert up to three metric cards rendered (each with class chip).
   - Assert three actions visible: **Why this answer** · **Export report** · **Trust receipt** link.

3. **`ask_console_renders_refusal_card_on_422_admission_refusal`** — mock `POST /api/service_1/v2/dispatch` returning `AdmissionRefusal_v0(@422)` with `outcome: "refused"`:
   - Submit ask.
   - Assert refusal warning card visible in ANSWER POSITION (not error position).
   - Assert title text = *"Not to the standard you asked for."* (§3.3 binding copy verbatim).
   - Assert line "Asked: {floor} · Supported: {class}" visible.
   - Assert three action buttons visible with binding labels: **Accept as recorded statement** · **Narrow the objective** · **Lower the standard**.
   - Assert footer text starts with *"A refusal is the system keeping its promise…"*.
   - **Assert page does NOT render infra-error styling** (refusal ≠ error; §3 rule 3 binding).

4. **`ask_console_renders_accepted_view_on_202_async_delivery_accepted`** — mock `POST /api/service_1/v2/dispatch` returning `AsyncDeliveryAccepted_v1(@202)`:
   - Submit ask.
   - Assert accepted view visible with `objective_id` + `delivery_estimate` + `trace_id`.
   - Assert quote card visible (populated `quote` per AsyncDeliveryAccepted_v1 shape from Phase 6b).

5. **`ask_console_renders_infra_fault_view_on_500`** — mock `POST /api/service_1/v2/dispatch` returning HTTP 500:
   - Submit ask.
   - Assert InfraFaultView visible with copy *"infrastructure fault, not a governance decision"* (or equivalent per 8a-lite).
   - **Assert refusal-card styling NOT applied** (§3 rule 3 binding — infra ≠ refusal).

6. **`ask_console_trust_receipt_link_resolves_public_url`** — from any answered state (scenario 2):
   - Click **Trust receipt** link.
   - Assert URL pattern matches `rms.intel/trace/{trace_id}` OR internal `/trace/{trace_id}` route depending on Owner ratification.
   - Assert opened surface is read-only (no submit/edit affordances).

### 3.3 Playwright infrastructure at B-1

- `package.json` adds `@playwright/test` devDependency (yarn install at B-1 dispatch).
- `/app/frontend/playwright.config.ts` NEW (baseURL from `REACT_APP_BACKEND_URL` env; browser projects: chromium only at B-1).
- CI integration: `frontend/e2e/*.spec.ts` runs on webpack production build (`yarn build && yarn preview` OR equivalent static serve).
- Playwright counts against Phase 8 B-1 sizing band (see §5 below).

### 3.4 Sizing anchor for Playwright smoke

- **Playwright config + spec file estimated:** ~180 LoC (spec) + ~40 LoC (config) = **~220 LoC net-new frontend**.
- **`snapshot_lloc_in_band: N/A`** (Playwright is not a Pydantic snapshot).

---

## §4. Plan Debts (references §0.2 in ORCHESTRATOR_CONTINUITY.md)

All Phase 8-relevant plan debts (verbatim from §0.2 post-refresh at this dispatch):

- **Phase 8 Stage A frozen-contract trajectory restatement plan-debt** (Phase 7 B-1 close, 2026-07-04) — **RESOLVED at Phase 8 Stage A dispatch (this proposal), 2026-07-04:** trajectory restated in §1 above; per-sub-stage `snapshot_lloc_in_band` declarations landed in §1.3 above.

- **Phase 8c DPO `wizard_transcript` held-class enumeration** (refined at this dispatch per Owner verbatim clarification) — DPO surface must expose `wizard_transcript` as **separately-addressable** held-class. See §6.3 below for the mechanical seam.

- **Wizard session-ownership binding plan-debt** (Phase 7 B-2 dispatch, 2026-07-04) — landing at Phase 8 B-1 as the auth/key model. See §2.7 "Shared backend module" + §6.1 below.

- **Envelope-shim helper triad extraction** (Phase 7 B-3 close acceptance, 2026-07-04) — the triad in `services/wizard/admission_handoff.py` is duplication-by-design at B-3; extraction to shared module lands with Phase 8 backend-refactor slot. Landing sub-stage: **Phase 8 B-1** (co-located with auth/key model landing since both are backend foundation-layer work). Mechanism: extract `_compose_shim`, `_shim_helper_2`, `_shim_helper_3` (actual names to be resolved at Stage B-1 open) from both `routers/wizard_buyer.py` + `routers/wizard_operator.py` into shared module `services/wizard/router_shims.py` (single-source; each router imports). Guarded by grep-negative parametrised over the triad symbols at B-1 close.

---

## §5. Rule 2 v2 Sizing Anchors per sub-stage

**Note on transcription posture:** Owner cap at Phase 7 B-2 established transcription-only Rule 2 accounting posture (`rule2_accounting.json` at 30 phases post-B-3). This Stage A **projects** sizing anchors; actual close accounting is transcribed at each sub-stage close, not fresh-derived.

### 5.1 Anticipated LoC bands per sub-stage

| Sub-stage | Anticipated net-new LoC | Band (mid ± 30%) | Snapshot LoC in band |
|---|---|---|---|
| Phase 8 B-1 (Auth/key + Shared §8 components + Ask Console-full + Playwright + Envelope-shim extraction) | ~1650 | **1150-2150** | **no** (frontend + auth backend; no new frozen contracts unless E4 lands as B-1 instead of B-3) |
| Phase 8 B-2 (Operator surface pages + Home/Commission/Freeze) | ~1400 | **980-1820** | **no** (frontend + 1 read-only route) |
| Phase 8 B-3 (Engineer surface + Buyer surface) | ~2100 | **1470-2730** | **conditional** (see §1.3 — `no` default; `yes` if E4 `EngineerKeyGrant_v0` lands, band +200) |
| Phase 8 B-4 (Master Admin surface) | ~1200 | **840-1560** | **no** (frontend + versioned-config bumps only) |
| Phase 8 B-5 (Regulator / DPO surface + retention config) | ~1350 | **945-1755** | **no** (frontend + read-only routes + retention config bump) |
| **Total anticipated Phase 8** | **~7700 LoC** | **~5400-10000 LoC** | **no OR conditional yes at B-3 only** |

### 5.2 Anticipated CI delta per sub-stage

| Sub-stage | Backend gate delta | Frontend gate delta | Playwright scenario delta | Anticipated backend CI at close |
|---|---|---|---|---|
| Phase 8 B-1 | +12 (auth boundary + shim extraction + read-only route + regression) | +8 (shared components) | +6 (Ask Console smoke) | 740 → ~752 backend; ~35 frontend + 6 Playwright |
| Phase 8 B-2 | +5 (operator status route + regression) | +12 (operator pages) | +4 (operator surface smoke) | 752 → ~757; ~47 frontend + 10 Playwright |
| Phase 8 B-3 | +10 (engineer keys + buyer deliverables + regression) | +18 (engineer + buyer pages) | +6 (engineer + buyer smoke) | 757 → ~767; ~65 frontend + 16 Playwright |
| Phase 8 B-4 | +8 (admin routes + versioned-config bumps + regression) | +12 (master admin pages) | +4 (master admin smoke) | 767 → ~775; ~77 frontend + 20 Playwright |
| Phase 8 B-5 | +10 (DPO routes + retention config + regression) | +12 (DPO pages) | +5 (DPO surface smoke) | 775 → ~785; ~89 frontend + 25 Playwright |

**Stop-and-judge triggers per sub-stage:**
- (a) `LoC > +15% over top-of-band` → Owner stop-and-judge before landing.
- (b) `discretionary-only ratio > 2.5×` → same.
- (c) any Literal-widening on a frozen contract → HAZARD-STOP (a) immediate.
- (d) any snapshot LoC discovered mid-implementation without band coverage → HAZARD-STOP; restate band OR defer contract to next sub-stage.

### 5.3 Snapshot inclusion declaration (Standing Disposition forward clause)

Explicit per §1.3 above. Standing Disposition `Sizing-anchor-declares-snapshot-inclusion` requirement fully satisfied at Stage A close.

---

## §6. Governance Seam Posture

### 6.1 Wizard session-ownership binding (Phase 7 B-2 plan-debt landing)

**Current posture (post-B-3):** wizard session caches (in-memory `_SESSIONS` dict + Mongo `wizard_sessions` collection) keyed only by `session_id`. Compound index on `variant + session_id` (B-2 addition). **No per-user ownership.**

**Phase 8 B-1 landing shape:**
- NEW module `services/auth/session_binding.py` — table binding `session_id → identity_id`. Populated at `POST /api/wizard/{variant}/session` when authenticated caller identity resolves.
- Wizard endpoint decorators enforce: any subsequent `POST /api/wizard/{variant}/{sid}/*` requires the authenticated caller identity to match the binding, else HTTP 403 (auth boundary refusal — distinct shape from `AdmissionRefusal_v0` per doctrine).
- Existing frozen contracts UNTOUCHED: `WizardCommitState_v0` remains at 26th parity, byte-identical, no `identity_id` field on state (binding lives in a sidecar table, not the state contract).
- Backward compatibility: sessions initiated before auth landing (i.e., existing test-fixture sessions) grandfather with `identity_id=None`; new sessions post-auth-landing require binding. Grandfathering pattern is a one-time carve-out; grep-negative gate ensures new session code paths always bind.

### 6.2 Auth-refusal shape (NEW at Phase 8 B-1 — NOT AdmissionRefusal, NOT Service1Refusal)

- Auth failures (missing key / expired / scope-mismatch / wrong-identity-for-wizard-session) return HTTP 403 with a distinct shape (bounded string reason set):
  ```json
  {"reason": "auth_scope_insufficient", "detail": "..."}
  ```
- **Doctrinal reasoning:** an auth failure is neither a governance refusal (needs `outcome=refused` + `asked` + `supported_class`) nor an infra fault (503). It's a boundary decision on caller identity — HTTP 403 with a plain-language reason.
- Bounded string reason set (proposed at Stage B-1 open; escalation E2 below): `auth_missing`, `auth_expired`, `auth_scope_insufficient`, `auth_identity_mismatch_for_wizard_session`.

### 6.3 DPO `wizard_transcript` separately-addressable (Phase 7 B-1 plan-debt refined this dispatch)

**Mechanical seam:** `services/wizard/turn_ledger.py::record_wizard_freeze` writes Northena Ledger rows with `stamp_audit` sidecar carrying `data_class="wizard_transcript"` (B-1 gate `test_turn_ledger_stamp_audit_sidecar_carries_wizard_transcript_data_class` GREEN + regression preserved at B-2 + B-3).

**Phase 8 B-5 landing shape:**
- DPO surface `/api/dpo/retention/holdings` enumerates held-classes distinctly. `wizard_transcript` renders as its OWN row (separately-addressable per Owner refinement), distinct from `objective_request` / `composed_conclusion` / `outer_gate_receipt` / `northena_ledger` general row.
- DPO can `POST /api/dpo/retention/decide` scoped per held-class: `{"held_class": "wizard_transcript", "retention_window_days": N}` — versioned-config bump on `retention_config.vN.json` per held-class. Ruling 3 pattern preserved.
- DPO may inherit ledger default OR split (Owner E5 seam preserved from B-1) — Phase 8 B-5 surfaces the CHOICE, doesn't pre-decide.

### 6.4 Standing seams preserved (no changes at Phase 8)

- **Ruling 4 shared-derivation** — all Phase 8 backend routes import from proven single-source modules (`floor_feasibility`, `grain_compatibility`, `license_class_selection`, `provenance_preservation`, `dual_delta`, `admission_handoff`). Zero re-implementation.
- **Infra-not-refusal (Standing Disposition, Phase 5 A close)** — all Phase 8 auth failures → HTTP 403 (auth boundary shape); all Phase 8 infra failures → HTTP 5xx; NEITHER shape is a governed 422 refusal.
- **Cancellation-is-a-state-not-a-refusal (Standing Disposition, Phase 5 A close)** — preserved; Phase 8 buyer surface §5.1 offers refusal-with-path (§3.3 pattern), not cancellation on shape refusal.
- **Frozen-field-changes-as-new-versions (Standing Disposition, Phase 5 A close)** — any Phase 8 contract addition (only E4 candidate; otherwise 0) lands as versioned file; no in-place mutation.
- **Visibility-not-prohibition (Standing Disposition, Phase 7 A close)** — buyer surface §5.1 preserves the B-2 dual-delta mechanical gate; agent-may-propose surfaces class_delta + price_delta on-wire.
- **Read-only route invariant (G5a)** — all Phase 8 DPO routes + Ask Console recent + Buyer deliverables write ZERO rows to any persistent store. Guarded by regression of `test_trace_lens_readonly.py` scope extended to Phase 8 read routes.
- **Outer-gate irreversibility invariant (G6)** — Buyer §5.3 renders receipt "fact and fingerprint only, nothing that could aid reversal" verbatim per UI Spec §5.3.
- **V2 refusal terminality (G6)** — preserved; Phase 8 surfaces render refusals as terminal records, never partial-egress.

---

## §7. Standing Constraints Compliance

**Full doctrinal cross-check at this Stage A close:**

| Constraint | Compliance mechanism at Phase 8 | Verification anchor |
|---|---|---|
| 26 frozen contracts byte-identical (parity invariant) | No new contracts anticipated (E4 optional at B-3 → 27). Byte-identity regression gate `test_prior_contract_file_exists_and_stable_at_8_stage_N` parametrised over 25 (or 26 post-E4) sources runs at each sub-stage close. | `test_frozen_contract_snapshot_parity` GREEN at 26 (or 27) |
| Shield boundary (LLM only inside `services/synisense/shield/*`) | No LLM code anywhere on Phase 8 frontend or non-Shield backend. Grep-negative `test_no_direct_llm_calls_outside_shield_still_green` runs at each sub-stage close. | GREEN post-each-sub-stage |
| Ruling 4 shared-derivation | Every Phase 8 endpoint invokes proven single-source modules. Grep-negative parametrised gate enforces. | GREEN post-each-sub-stage |
| §0.1 Standing Dispositions FROZEN | Zero new §0.1 additions at Phase 8. Only §0.2 plan-debt RESOLVED-markings + additive debt entries at B-1 (envelope-shim triad extraction). | Read of §0.1 diff at each close |
| Standing Rule v3 delivery | Every sub-stage close lands as on-disk canonical + SHA in return; NO full-text inline. | This proposal + each future close |
| Substrate-drop gate 9/9 | No new phase-source-requirements introduced at Phase 8; existing 9 remain SHA-matched. | Existing gate GREEN |
| Read-only route invariant (G5a) | All Phase 8 read routes write zero rows. `test_trace_lens_readonly` scope extended. | Scope extension at B-1 |
| Outer-gate irreversibility (G6) | Buyer §5.3 render preserves fact-and-fingerprint-only receipt. | Buyer surface gate at B-3 |
| V2 refusal terminality (G6) | Refusals rendered as terminal, never partial-egress. Regression preserved. | Refusal gate parametrised per surface |
| Loose-as-frozen (Substrate-Drop v2 close) | No frozen field narrowing at Phase 8. All new configs are versioned (Ruling 3). | No-contract-mutation gate |
| Config-as-versioned-not-frozen (Ruling 3) | Auth keys, retention windows, roles, taxonomy updates all land as `<name>.vN.json` versioned configs. Zero snapshot generation. | Standing pattern preserved |
| Admission-refusal reason via registry (Standing Disposition) | Zero new admission-refusal codes at Phase 8 (auth failures are HTTP 403, not 422 refusals). Registry bump ONLY if a genuine new governance refusal arises during Stage B (escalates as governance-semantic contact). | Registry byte-identity |
| Wizard `wizard_transcript` retention marker preserved | Ledger sidecar marker unchanged at Phase 8. B-1 gate `test_turn_ledger_stamp_audit_sidecar_carries_wizard_transcript_data_class` remains GREEN. | Regression at each sub-stage |
| No `git push` | Owner-side push per Standing Rule v3. | Agent never runs `git push` |
| No refactoring | Zero refactors during Phase 8 sub-stages; only additive-only + envelope-shim triad extraction (explicitly ratified). | Diff review at each sub-stage close |
| Disposition-must-cite-owner-ruling meta-doctrine | §0.2 additive entries (envelope-shim triad + refined wizard_transcript enumeration) carry `[Owner ruling, <phase-context>, <date>]` citation headers verbatim. | §0.2 update at this close |
| Inline-delivery-scope-amended-v3 | This proposal lands on-disk canonical + SHA in return; return summary carries one-line enumerations only. | This delivery |
| Sizing-anchor-declares-snapshot-inclusion | Per-sub-stage `snapshot_lloc_in_band` declared in §1.3 + §5.1. | §1.3 + §5.1 above |
| Agent-pluggable-with-stub-agent-first | Zero new agent-driven pipelines at Phase 8 (wizard SonnetWizardAgent already landed at B-2). If any B-N adds a new agent surface, `DeterministicStubAgent`-first proof order applies. | N/A at Phase 8 unless new agent |
| Visibility-not-prohibition | Preserved at buyer surface B-3 (dual-delta already mechanical at B-2). | Buyer surface gate at B-3 |
| Frozen-field-changes-as-new-versions | Any Phase 8 contract addition lands as versioned file. E4 candidate = new `EngineerKeyGrant_v0`, not v1 of any existing shape. | Standing pattern |

**Total: 22 standing constraints; ALL preserved at Phase 8 design shape.**

---

## §8. Escalation Posture

**Open items requiring Owner ruling before Phase 8 Stage B-1 dispatches:**

- **E1 — Auth/key model choice (P0 blocker for B-1).** Two candidate paths, propose Owner picks one:
  - (a) **Custom JWT-based auth** with `services/auth/` module hosting identity + key-grant + session-binding all in-pod. Zero third-party integration. Fits Emergent env constraints (backend-only, MONGO_URL storage).
  - (b) **Emergent-managed Google OAuth** integration (per system-prompt integration option). External auth surface; local `services/auth/` module then only handles session-binding (identity issued externally).
  - Agent recommends: **(a) custom JWT** for Phase 8 B-1 landing — smallest LoC surface, single-source identity, testable via curl without third-party mock, aligns with Emergent-env constraints. Escalate at Owner discretion if buyer/engineer surfaces later demand Google-identity federation.

- **E2 — Auth-refusal reason bounded set (P0 blocker for B-1).** Proposed bounded set (§6.2): `auth_missing`, `auth_expired`, `auth_scope_insufficient`, `auth_identity_mismatch_for_wizard_session`. Owner ratifies set OR narrows/expands.

- **E3 — Envelope-shim triad symbol names (P0 blocker for B-1).** Actual symbol names to be resolved by reading `routers/wizard_buyer.py` + `routers/wizard_operator.py` at implementation time. Landing module: `services/wizard/router_shims.py`. Owner ratifies module name + landing sub-stage (B-1 proposed).

- **E4 — Engineer key-grant governed record shape (P1 conditional at B-3).** Two candidate paths:
  - (a) **`EngineerKeyGrant_v0` as NEW frozen contract** at Phase 8 B-3. Parity 26→27. `snapshot_lloc_in_band=yes` at B-3, band expands by ~200 LoC.
  - (b) **`engineer_keys.vN.json` versioned config** (Ruling 3 pattern). No parity change. Landing config file only.
  - Agent recommends: **(b) versioned config** unless Owner explicitly requires a governed record (i.e., key issuance must trust-receipt through the same wire as objectives). Owner ratifies at Stage B-3 open — sub-stage-scoped decision, does not block B-1 dispatch.

- **E5 — DPO retention-window inheritance vs split (Owner ruling deferred from Phase 7 B-1 close; Phase 8 B-5 surfaces the CHOICE).** Not a blocker for Phase 8 B-1/B-2/B-3/B-4. Owner rules at Phase 8 B-5 open OR when DPO surface goes live.

- **E6 — Trust-receipt public URL** — `rms.intel/trace/{id}` verbatim from UI Spec, but domain not yet resolved in-pod. Two candidate paths:
  - (a) **In-pod internal route** `/trace/{id}` served by `routers/trust.py` at Phase 8 B-5; public URL rendered as `${REACT_APP_BACKEND_URL}/trace/{id}`.
  - (b) **Placeholder external URL** `rms.intel/trace/{id}` rendered as illustrative-only text at Phase 8; actual public routing landed post-Phase-8 with domain provisioning.
  - Agent recommends: **(a) in-pod route** at Phase 8 B-5, honoring the read-only invariant + G5a doctrine. Owner ratifies at Stage B-5 open.

- **E7 — Playwright browser project scope at B-1.** Chromium-only proposed. Owner ratifies OR expands to Firefox/WebKit (adds CI runtime).

- **E8 — Sub-stage sequence.** Proposed: B-1 (Auth + Shared + Ask Console-full + Playwright) → B-2 (Operator) → B-3 (Engineer + Buyer) → B-4 (Master Admin) → B-5 (DPO). Owner ratifies sequence OR re-orders (e.g., DPO earlier for regulator-first posture).

**Standing constraint reminder:** Any escalation resolved at Stage A close is folded into Stage B-1 dispatch verbatim. Escalations remaining open at Stage A close block Stage B-1 dispatch (per doctrine).

---

## Machine-attested block (Stage A close)

```
[GREEN] pytest -q                                                        740 / 740 unchanged
[GREEN] test_frozen_contract_snapshot_parity                             26 / 26 (parity UNCHANGED at Stage A)
[GREEN] substrate-drop invariants                                        9 / 9 (Phase 8 GREEN — no new source requirements at Stage A)
[GREEN] frontend yarn test                                               27 / 27 across 5 UI-Spec-v1 suites unchanged
[STATUS] Stage A design-only: ZERO code files written outside /app/docs/stage_a_proposals/phase_8.md + /app/memory/ORCHESTRATOR_CONTINUITY.md §0.2 (three plan-debt updates per Owner verbatim)
[STATUS] Zero new frozen contracts landing at Stage A
[STATUS] No `git push`
[STATUS] wizard_not_frozen 422 body shape confirmed: {"reason": "wizard_not_frozen", "detail": "..."} — NO outcome=refused, NO AdmissionRefusal_v0 discriminator
[CANONICAL] /app/docs/stage_a_proposals/phase_8.md (SHA quoted in return message)
```

---

## Escalations summary (one-line enumeration for Owner)

- **E1** — Auth/key model: custom JWT (recommended) OR Emergent-managed Google OAuth.
- **E2** — Auth-refusal bounded reason set: 4 codes proposed (`auth_missing` / `auth_expired` / `auth_scope_insufficient` / `auth_identity_mismatch_for_wizard_session`).
- **E3** — Envelope-shim triad extraction module name (`services/wizard/router_shims.py` proposed) + landing sub-stage (B-1 proposed).
- **E4** — Engineer key-grant governed record: versioned config (recommended) OR new frozen contract `EngineerKeyGrant_v0` at B-3 (parity 26→27).
- **E5** — DPO retention-window inheritance vs split (Owner ruling deferred; surfaces at B-5).
- **E6** — Trust-receipt public URL: in-pod route (recommended) OR external domain placeholder.
- **E7** — Playwright browser project scope: chromium-only proposed.
- **E8** — Sub-stage sequence: B-1 Auth+Shared+Ask-full+Playwright → B-2 Operator → B-3 Engineer+Buyer → B-4 Master Admin → B-5 DPO.

---

*End of Phase 8 Stage A design proposal. Awaiting Owner rulings on E1-E8 (E1/E2/E3 block Stage B-1 dispatch; E4-E8 sub-stage-scoped).*
