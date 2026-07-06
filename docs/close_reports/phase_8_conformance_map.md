# Phase 8 Conformance Map — Close Report (2026-07-06)

**Canonical marker (Standing Rule v3).** This on-disk markdown file is the
sole canonical record of the post-cut conformance-map dispatch. Its
SHA-256 (computed after write, quoted in return) is the immutable
pointer. No implementation code is pasted inline.

- **Dispatch:** Owner Conformance Map (2026-07-06) — narrow scope, single
  question: *what does B-5a Stage A need to know to dispatch?*
- **Escalation-cap wording (original, restored):** defaults everywhere
  except frozen-contract, owner-value, or governance-semantic contact.
- **Preamble folded:** manifest re-authoring (Part 1) completed in-line
  with this dispatch; §I below.
- **Return-format posture:** 7-point per Standing Rule v3.

---

## §I. Preamble — Manifest re-authoring (Part 1)

### I.1 `/app/docs/mandates/MANIFEST.md`

- **v2.1 UI Specification row ADDED** to `## Specs filed` table with SHA
  `ef6da4b498117608a3091033b5cfa43571ad8a7a38b5954cae7c4a1a698de5e2`,
  first-received 2026-07-05, canonical-status ACTIVE (row states supersedes
  v1 in full; four-consoles taxonomy; §5.5 governed-extract API; §4
  Compliance Console; §7.1 Internal Reference Application; §11 migration
  map; §12 Sales Service stub; 207 LoC).
- **BCR v1.4 row ADDED** with SHA
  `d1f49bc5d7cbf1dea044ca4069a1dc2d45f01876e531b7500d860ae3f48aebdd`,
  first-received 2026-07-05, canonical-status ACTIVE (row states supersedes
  v1.2; §3 engineering per-gap; §5 sequencing; §12 commercial cut with 14
  requirement IDs; 341 LoC).
- **v1 UI Specification row RELOCATED** from `## Specs filed` to `## Archive`
  as a bullet item with SHA
  `9053a4c451954cca1dc2f2b10216bef2058411a1911136581251e395d5bdcbf3` and
  status `SUPERSEDED-BY-v2.1 / NO-LONGER-CONSUMED`. Retained on-disk at
  `/app/docs/mandates/RMS_UI_Specification_v1.md` per Owner Part-1
  directive (SUPERSEDED banner at file top; not moved under `archive/`).
  Archive-block bullets are NOT gate-verified by `test_substrate_drop_gate`
  (per pre-existing MANIFEST.md paragraph on archive-lineage).
- **Zero source-content mutation.** No `.md` file body was edited; only
  MANIFEST rows moved / added.

### I.2 `/app/docs/mandates/phase_source_requirements.yaml`

- **All `RMS_UI_Specification_v1.md` references REDIRECTED to
  `RMS_UI_Specification_v2_1.md`.** Affected phases: G5a, G5b, G6, Phase_5,
  Phase_6, Phase_7, Phase_8 (seven redirects).
- **Per-phase equivalence notes inline** — each redirected phase carries a
  YAML comment naming the v1 § → v2.1 § anchor mapping used (e.g. Phase_7:
  v1 §2.2/§2.3 wizard surfaces → v2.1 §3.2/§3.3; v1 §5.1 buyer wizard →
  v2.1 §11/§12 CUT per commercial-cut ruling).
- **BCR canonical pointer NOT ADDED to any phase** — no phase currently
  references a Build Completion Requirements version in this file; Owner
  directive was conditional ("if `phase_source_requirements.yaml`
  currently references…"), which is false today. Adding BCR as a phase
  dependency is a future dispatch decision (not this one).

### I.3 Gate verification

`python -m pytest tests/invariants/test_substrate_drop_gate.py -q` = **13
passed** post-realignment. All 7 redirected phases resolve their spec
files to SHAs present in the updated `MANIFEST.md`.

### I.4 New SHAs (at preamble close)

- **`MANIFEST.md`** — SHA-256: `46d81b8b37226dcad8c2bf75057337b44248bba4673cc84c6ea89a4de54ab7ef`
- **`phase_source_requirements.yaml`** — SHA-256: `59d43a95028783570546ffeda0e55fd3cfc7d661c2a5303bbca74b668a952927`

---

## §II. Conformance Map — Four Priority Anchors (FULL EVIDENCE)

### Anchor 1 — v2.1 §4.1-4.3 (Compliance Console read/prove; B-5a substrate)

**Anchor citation** (verbatim from `RMS_UI_Specification_v2_1.md` lines 64-78):

*§4.1 Home*  Lookup "Look up any run, claim, or acquisition by trace…";
Attention "Problems stated honestly"; Cards (three: runs with lawful
basis; refusals this month with a See what was refused link; retention
windows past due); RULE adversarial-to-comfort (never all-green
summaries); BINDING COPY *"This is the same record every user's audit
view reaches — read-only, nothing reconstructed for display."*

*§4.2 Prove one run*  Banner "Lawfulness banner: lawful-basis reference ·
commissioner · frozen and immutable"; Record rows (Lawful basis /
Scope / Refused / Standard / Ledger); BINDING COPY *"Read-only. This is
the record itself, not a summary of it. Export for a regulator on
request."*

*§4.3 Retention & rights*  Banner (honest-while-unset) *"No deletion
rule is set. The system holds everything indefinitely and append-only
until you set a retention window. This is a decision only you can make
— the system won't guess a duration."*; Holdings rows (within window /
past due + Decide / delivered acquisitions); held-classes render
**separately addressable**; BINDING COPY *"Setting a retention window
here becomes a governed rule — versioned, dated, and recorded like every
control change."*

**Current-tree artifacts:**
- **Backend seam (EXTENDS material)** — `POST` and `GET` handlers under
  `/app/backend/routers/northena.py`: `@router.get("/status")` line 41;
  `@router.get("/ledger/open_runs")` line 52; `@router.get("/ledger/by_run/{run_id}")`
  line 58; **`@router.get("/trace/{trace_id}", response_model=TraceLensEnvelope)`
  line 68-85** (uses `trace_lens_svc.resolve_trace(trace_id)`; NotFound → 404;
  input-error → 400; unhandled → 500 non-refusal per infra-not-refusal doctrine).
- **Contract shape** — `contracts/trace_lens.py` (frozen contract 9,
  `TraceLensEnvelope@v0`, snapshot `trace_lens_envelope.contract_snapshot.json`
  byte-identical since G5a).
- **Cross-engine correlation** — `services/northena/trace_lens.py` resolves
  `trace_id` across Solva, Mtafiti, Targeta, Service-1, Outer Gate, V2
  gate absorption points (G5a substrate).
- **Northena Ledger v1 stamp_audit sidecar** — `contracts/northena_ledger_v1.py`
  (frozen contract 19) carries `stamp_audit` typed Optional[Dict]; already
  used at B-4 for `data_class="master_admin_rule_change"` + engineer key
  grant events at B-3 for `data_class="engineer_key_grant"`. §4.2 "Ledger
  (append-only; current retention state stated honestly)" row consumes
  the same ledger with `data_class` filter.
- **Frontend surfaces** — **ZERO current-tree Compliance/Regulator/DPO
  pages** in `/app/frontend/src/pages/`. Grep `regulator|dpo|compliance`
  returned only master-admin/operator/ask-console page matches (which
  reference "compliance" in binding copy or footer links). Prior G5b
  Regulator/DPO §7 pages were archived to `src/legacy/pages/` at Phase
  8a-lite close (8 legacy files; routes at `/legacy/*`).

**Current-tree tests:**
- `backend/tests/invariants/test_trace_lens_readonly.py` — LOAD-BEARING
  read-only invariant (G5a); zero writes to persistent store on any
  trace-lens request.
- `backend/tests/invariants/test_trace_lens_cross_engine_correlation.py`
  — cross-engine trace_id resolves across engines.
- `backend/tests/invariants/test_handoff_route_readonly.py` — cousin
  read-only invariant (post-G6).

**Verdict:** **EXTENDS** — the backend seam for §4.2 "Prove one run" is
substantially built (trace-lens read-only route + cross-engine
correlation + append-only ledger with `stamp_audit.data_class` for
governance events). §4.1 "Home" three-card layout and §4.3 "Retention &
rights" honest-while-unset banner + separately-addressable held-classes
render are **NEW-BUILD on the frontend**; backend needs (a) a §4.3
retention-config read endpoint (currently no route exposes retention
window state) and (b) a §4.1 refusals-this-month aggregation endpoint
(currently no route aggregates refusals by month with a `See what was
refused` link surface). The v1 Regulator/DPO §7 pages archived under
`src/legacy/pages/` are NOT a reusable substrate — they were built
against v1's Regulator/DPO framing which v2.1 restructures into the
Compliance Console; treating them as EXTENDS material would import the
v1 information architecture (e.g. G5b Consumer Terminal patterns
crossed with v1 §7) that v2.1 explicitly rearranges.

**What B-5a Stage A needs to know:**
The Compliance Console read/prove half is a **backend-EXTENDS,
frontend-NEW-BUILD dispatch**. `GET /api/northena/trace/{trace_id}` is
the §4.2 substrate; two new backend read endpoints must land (retention
config read + refusals aggregate) alongside three new frontend pages
(§4.1 Home / §4.2 Prove one run / §4.3 Retention & rights). Held-classes
`ledger_row / wizard_transcript / delivered_artifact` must render
**separately addressable** per Owner E5 seam (existing §0.2 debt — see
§V below). First-commit gating (per B-4 close-acceptance standing
correction) requires per-surface Playwright chromium smokes to land in
the same commit as each surface. B5a-G1 test_compliance_surface_read_only
(no write route reachable from this half), B5a-G2
test_prove_run_resolves_any_trace, B5a-G3
test_retention_unset_states_honestly per BCR v1.4 §3.6.

---

### Anchor 2 — v2.1 §5.5 (Governed-extract API — machine boundary, operator-provisioned)

**Anchor citation** (verbatim from `RMS_UI_Specification_v2_1.md` lines 115-120):

*"The Integration Console PROVISIONS access to the extractor's outputs;
it does not itself sell, price, or transact. What it exposes is the
governed-extract API — the single contract every application (internal
or external, RMS-built or third-party) calls to reach extractor output."*

*Provisioned here:* Application registration (name, class internal|external,
path live_query|governed_extract); key issuance and scope (floor, reach
ceiling, license class, disclosure ceiling); offerability bounds for the
key (which estate slices the key may reach); usage and refusal-health
monitoring. All operator-side.

*RULE:* The API enforces, for EVERY caller with no exception for RMS-owned
applications: the inner gate on live_query (per-call class inline) or the
full outer gate on governed_extract (rights, irreversibility,
cumulative-disclosure debit, license issue); server-side key-scope on
every call; the four response classes. An application that appears to
bypass any of these is a defect, not a tier.

*RULE:* No price, quote, offer, catalogue, order, or buyer-account
concept exists on this console or in this API.

**Current-tree artifacts:**
- **The single-contract endpoint** — `POST /api/service_1/v2/dispatch` at
  `backend/routers/service_1.py:214-263`. Accepts `ObjectiveRequest_v2`;
  response Union `[DispatchResult @501 | AdmissionRefusal_v0 @422 |
  ComposedConclusion_v0 @200 | Service1Refusal_v0 @422 |
  QualifiedDataPayload @200 | AsyncDeliveryAccepted_v1 @202]` + `HTTP 503`
  out-of-Union (infra-not-refusal doctrine).
- **Server-side key-scope enforcement** — `backend/routers/service_1.py:250`
  calls `key_grants.check_scope(identity, required)` (from
  `services/auth/key_grants.py:65`). Refusal → HTTP 403
  `{"reason": "auth_scope_insufficient", "detail": ...}` per E2 auth-refusal
  4-code registry. **Owner E1/E2 symmetric-cut ratified at B-2:** anonymous
  falls through (no auth required for grants-not-scoped cases); scoped
  callers get gated; ZERO envelope delta from scope gate (6 forbidden
  auth-metadata keys enumerated absent on 200/202/422 side).
- **Outer gate (full governed-extract path)** — `services/outer_gate/`
  package (transform + mint + receipt); ties into disclosure-budget debit
  via cumulative_disclosure ledger @v0 (frozen contract 13).
  Cumulative-disclosure debit path exists post-G6.
- **Inner gate (live_query path — per-call class inline)** — every
  200-response path (v2 dispatch's ComposedConclusion_v0 branch,
  QualifiedDataPayload container, `POST /api/service_1/run` legacy)
  carries defensibility inline per §5.2 binding copy.
- **Application registration + key issuance** — `POST /api/engineer/key_grants`
  at `backend/routers/engineer.py:89` (issuance); `POST /api/engineer/key_grants/{grant_id}/revoke`
  line 143 (revocation); `GET /api/engineer/key_grants` line 109 (listing).
  Both endpoints emit `NorthenaLedgerRow_v1` via
  `services/auth/engineer_key_grant_ledger.record_engineer_key_grant_event(...)`
  (idempotent per (trace_id, run_id) with `data_class="engineer_key_grant"`).
- **Key-scope tuple shape** — `EngineerKeyGrantRegistration` at
  `backend/services/auth/engineer_key_grant.py:145-` carries the four fields
  v2.1 §5.1 names: `key_class: Literal["internal", "external"]`,
  `path: Literal["live_query", "governed_extract"]`, `floor: FloorClass`,
  `scope: str`. **UNFROZEN at B-3 per D4b ruling** — governance-key wire-shape
  pinned by `test_engineer_key_grant_load_bearing_wire_shape.py`
  (7 governance-key fields presence + name + type).
- **No commercial fields on this surface** — grep `price|quote|offer|catalogue|order|buyer`
  across `backend/routers/service_1.py` + `backend/services/auth/engineer_key_grant.py`
  + `backend/routers/engineer.py` returned zero live-code matches (only
  MAN-G1 test-negative assertions; post-commercial-cut).

**Current-tree tests:**
- `backend/tests/invariants/test_phase_8_b_2_operator_and_scope_gate.py`
  — scope-enforcement gate PAIR on `POST /v2/dispatch`; ZERO envelope delta
  verified; 6 forbidden auth-metadata keys enumerated absent.
- `backend/tests/invariants/test_engineer_key_grant_load_bearing_wire_shape.py`
  — 7 governance-key fields wire-shape pinned; lifecycle-additive tolerance
  explicit (gate does NOT reject new lifecycle fields).
- `backend/tests/invariants/test_engineer_key_grant_e2_taxonomy.py`
  — E2 4-code registry over 3 grant endpoints × 2 auth postures.
- `backend/tests/invariants/test_engineer_key_grant_ledger_integration.py`
  — 3 P0 ledger integration gates (issuance / revocation / idempotency).
- `backend/tests/invariants/test_commercial_cut_man_g1.py`
  — grep-negative over 17 forbidden commercial symbols across extractor
  tree (post-cut zero live commercial code).

**Verdict:** **EXTENDS** — the machine boundary substantially exists.
`POST /api/service_1/v2/dispatch` IS the single-contract endpoint every
application calls; scope-gate enforces server-side per E1/E2; response
Union covers the four response classes (§1 global rule "four response
classes never conflated"); commercial-cut removed price/quote/buyer
paths per BND-1. **Gap for full §5.5 conformance:** (a) the `path`
dichotomy exists on the KEY GRANT schema, but the DISPATCH endpoint does
not currently branch by `path=live_query` vs `path=governed_extract` at
the API layer — the same v2/dispatch endpoint currently serves both
implicitly (governed_extract path becomes async delivery via
AsyncDeliveryAccepted_v1 @202; live_query path becomes ComposedConclusion
@200 or QualifiedDataPayload @200); this is not currently a wire-level
switch, it's a per-request-shape dispatch that happens to align with the
two paths; (b) offerability bounds — the `EngineerKeyGrantRegistration`
carries `floor` and `scope` but does NOT carry `offerability_bounds` /
`reach_ceiling` / `disclosure_ceiling` as explicit fields; §5.5's
"provisioned here" list of `floor, reach ceiling, license class,
disclosure ceiling` names reach ceiling + license class + disclosure
ceiling which are NOT on the current grant schema; (c) usage and
refusal-health monitoring surface (v2.1 §5.3 Administer) exists in
outline at `GET /api/engineer/key_grants` but does not compute usage
counts, refusal rates, or health indicators on the current listing route.

**What B-5a Stage A needs to know:**
§5.5 is **NOT the B-5a Stage A dispatch scope** — Owner's ruling scopes
B-5a to §4.1-4.3 Compliance Console read/prove. However, B-5a Stage A
consumes §5.5 knowledge posture in two places: (a) §4.2 "Prove one run"
Scope row states "nothing mined outside it" — the enforcement point IS
the `check_scope` call at `v2/dispatch:250`; B-5a can point at that call
site as the record-of-enforcement; (b) §4.2 Refused row states
"{n} items — below the required standard, recorded not dropped + See
them" — the enforcement point for standard-below-floor is the
`AdmissionRefusal_v0 @422` branch OR the QualifiedDataPayload hard-input
filter refusal; B-5a's Prove-one-run screen surfaces these via the
Northena Ledger stamp_audit sidecar. **§5.5's build gap (grant schema
field-set + path dichotomy switching + usage/refusal-health monitoring)
is Phase 8 Integration Console follow-on scope, NOT B-5a.**

---

### Anchor 3 — v2.1 §5.4 (Dual-actor scoping — internal_engineer vs external_engineer)

**Anchor citation** (verbatim from `RMS_UI_Specification_v2_1.md` lines 101-114):

*"Two roles, one console, identical screens, different scope —
enforcement server-side, never view-layer filtering alone:"*

| Capability | internal_engineer | external_engineer |
| --- | --- | --- |
| Applications visible | all | own only |
| Grants visible | all | own only |
| Register application | yes | own, via approval |
| Issue / revoke keys | yes (ledgered) | own keys only (ledgered) |
| Usage & refusal view | all applications | own applications only |
| Estate contents | never (not this console's job) | never |
| Fleet / pricing | no (Administration) | no |

*RULE:* External-scope denials are 403 access-control class
({reason, detail}) — never outcome=refused, never the refusal card.
Onboarding [STAKED]: external engineers are invited and approved by an
internal engineer; open self-registration is a commercial decision, out
of scope.

**Current-tree artifacts:**
- **Role model** — `services/auth/identity.py:20-79` defines
  `roles: List[RoleName]`. Grep `internal_engineer|external_engineer`
  across `backend/`: **ZERO matches**. The `engineer` role is a single
  role name; NO split into internal vs external at the identity level.
- **Key grant `key_class` field** — `EngineerKeyGrantRegistration.key_class:
  Literal["internal", "external"]` at `engineer_key_grant.py:184` DOES
  encode the class dichotomy per grant. But this is the class of the KEY
  being issued (which SLICE of the platform the key reaches), not the
  role of the engineer issuing it.
- **Listing route** — `GET /api/engineer/key_grants` at
  `backend/routers/engineer.py:109` currently returns grants visible to
  the caller with no per-caller filtering by `own only` vs `all` — one
  role sees all grants (subject to auth check that caller has engineer
  or admin role).
- **Approval workflow** — the "own, via approval" gate on
  `Register application` for external_engineer does NOT exist as code.
  Currently `POST /api/engineer/key_grants` requires engineer/admin role
  and issues directly.

**Current-tree tests:**
- Grep `internal_engineer|external_engineer|dual_actor|dual-actor` across
  `backend/tests` + `frontend/src`: **ZERO matches**.
- No test enumerates the seven-row capability table's
  internal-vs-external distinction.

**Verdict:** **NEW-BUILD** — the current tree has NO dual-actor role
model. The `key_class` Literal on the grant record encodes a related but
DISTINCT concept (which SLICE the KEY reaches), not the engineer's role.
The v2.1 §5.4 requirement that "internal_engineer sees all applications
and grants; external_engineer sees own only" requires both (a) an
identity-level role split (adding a `role="external_engineer"` alongside
existing `engineer` — or an explicit `engineer_actor_class` field on the
Identity model) and (b) per-caller-scoped listing filters on
`GET /api/engineer/key_grants` and any usage/refusal-health endpoints
(none of which currently do per-caller filtering). Additionally the
approval-workflow gate for external_engineer registration ("own, via
approval") is a fresh backend + frontend build; onboarding pattern is
[STAKED] per anchor citation.

**What B-5a Stage A needs to know:**
§5.4 is Integration Console scope (sequenced as 8-EXT per anchor
citation subheading), not B-5a scope. However, the Compliance Console
§4 must NOT be blocked by §5.4 absence — §4's dual-console rule (§4.4
compliance rulebook / §4.5 checker / §8 counter-sign) is INDEPENDENT of
engineer dual-actor scoping. The one adjacency: Owner's E2 4-code
auth-refusal registry (`auth_missing / auth_expired /
auth_scope_insufficient / auth_identity_mismatch_for_wizard_session`) is
what §5.4's "External-scope denials are 403 access-control class
({reason, detail}) — never outcome=refused" refers to; this shape is
LIVE at B-1 and preserved through B-4 (registry-exclusion gate GREEN;
console render-path gate GREEN AuthDeniedNotice testid-namespace
disjoint from RefusalCard's). B-5a can reference the auth-refusal shape
as "already the pattern" without depending on §5.4 role landing.

---

### Anchor 4 — Operator-agent line post-cut (what serves operator wizard turns; file + test)

**Anchor citation** (self-scoped by dispatch — no verbatim mandate line;
scope is the post-cut agent posture for the operator wizard):

**Current-tree artifacts:**
- **Agent Protocol** — `backend/services/wizard/agent_interface.py`
  defines `WizardAgent(Protocol)` line 56 (methods `next_turn`,
  `commit_review`) and `DeterministicStubAgent` line 70 (B-1
  implementation; no LLM).
- **State machine consumer** — `backend/services/wizard/operator_state_machine.py:35`
  imports `WizardAgent` protocol; line 105 `next_agent_turn(session:
  OperatorSession, agent: WizardAgent) -> OperatorTurn_v0` — the state
  machine calls whichever `WizardAgent` implementation the router
  provides; state machine itself has NO knowledge of LLM vs stub.
- **Router-side agent factory** — `backend/routers/wizard_operator.py:56`
  imports `DeterministicStubAgent`; line 91-96 defines `_new_stub_agent()`
  returning a fresh `DeterministicStubAgent()`. Docstring at line 92-96:
  *"same `WizardAgent` Protocol interface without state-machine changes."*
- **Router endpoint using stub** — every operator wizard endpoint that
  requires an agent (turn, agent-assumption paths) calls `_new_stub_agent()`
  at request time to obtain the agent instance. **The operator wizard is
  running on the DeterministicStubAgent (LLM-free) as its live agent.**
- **Shield-side residue** — `backend/services/synisense/shield/llm_router.py`
  line 224 carries the commercial-cut post-cut comment: *"# Commercial-cut
  2026-07-06 — SonnetWizardAgent extracted to salvage."* Line 227 comments
  document the extraction was of the `SonnetWizardAgent` class + `_sonnet_invoke`
  helper. Grep for live-instantiation `SonnetWizardAgent(...)` or
  `_sonnet_invoke(...)` calls in `services/wizard/*` + `routers/wizard_operator.py`:
  **ZERO matches**. `_LITELLM_AVAILABLE` guard + language-tier routing
  table + main Shield entrypoint remain intact (Shield's OTHER LLM
  functions preserved).
- **Frontend consumption** — `frontend/src/pages/operator/CommissionWizardPage.js`
  calls `apiClient.wizardOperatorTurn(...)` / `wizardOperatorAgentAssumption(...)`;
  these hit the backend router which uses the stub agent. Nothing in the
  frontend touches Sonnet or any LLM directly.

**Current-tree tests:**
- `backend/tests/invariants/test_phase_7_stage_b_1_wizard.py` — 30 wizard
  invariant gates including source-tag XOR + Guard 1/2/3 + license-class
  Option C wrap; parametrised over `DeterministicStubAgent`.
- `backend/tests/invariants/test_phase_7_stage_b_2_wizard.py` (post-cut
  operator-only trim) — parity-count invariant
  `test_prior_26_contracts_count_at_26` + `test_prior_contract_file_exists_and_stable_at_7b_2`.
  Buyer + Sonnet + dual-delta tests salvaged; operator + parity retained.
- `backend/tests/invariants/test_phase_7_stage_b_3_wizard.py` (post-cut
  operator-only trim) — operator commit-review + admission handoff gates
  retained; buyer freeze/commit-review/handoff/mount tests salvaged.
- Grep `SonnetWizardAgent` in `backend/tests/`: matches only in the
  extracted salvage source at
  `/app/salvage/commercial_cut_2026_07_06/backend/wizard/sonnet_wizard_agent_extracted.py`
  and in the commercial-cut MAN-G1 negative-assertion test file (asserts
  the symbol is absent from the extractor tree).

**Verdict:** **CONFORMS** — the operator wizard's live agent post-cut is
`DeterministicStubAgent` (LLM-free); Shield-side has no live wizard-agent
LLM binding; the Owner Standing Disposition
`Agent-pluggable-with-stub-agent-first` [Owner ruling, Phase 7 Stage A
close, 2026-07-04] is preserved — mechanical guards were built against
the stub agent FIRST, and the LLM (SonnetWizardAgent, buyer-only) was
plugged behind the same Protocol interface at Phase 7 B-2, and now
extracted at commercial cut without any change to the operator-side
guard tests. The stub-first posture is the load-bearing invariant that
made the cut trivially non-destructive to operator-side tests.

**What B-5a Stage A needs to know:**
The operator wizard is on stub agent — **no LLM behind any live operator
endpoint post-cut**. B-5a's §4.2 "Prove one run" screen must render
operator-supplied wizard turns and agent-inferred wizard turns
distinctly (per v2.1 §1 global rule "Agent-assumed marking. Any value an
agent supplied carries an amber agent-assumed chip"). Both source
tags are already emitted deterministically by `DeterministicStubAgent`
+ operator turns per B-1's source-tag XOR invariant on
`CommittedValue_v0` (frozen contract 26); B-5a can rely on the
committed-value source-tag as the ground-truth-of-who-said-what for its
Prove-one-run rendering. **No LLM knowledge posture is needed at B-5a
dispatch.** The stub agent's deterministic behavior means B-5a's tests
can seed wizard sessions to reach known committed-value states without
LLM mocking.

---

## §III. Non-priority anchors — ONE-LINE ENTRIES (no evidence packages)

### III.1 Orphan-value rows (4 orphan-in-place points from commercial cut)

- `QuoteEnvelope_v0` (frozen contract 21, snapshot SHA `83679e7d…`) — **ORPHAN-IN-PLACE / CONFORMS-BY-INTENT** (Owner PRES-3: parity stays 26; salvage copy at Sales Service future location).
- `services/economics/pricing_tiers.v0.json` (commercial-tier config, SHA `5dcc9730…`) — **ORPHAN-IN-PLACE / CONFORMS-BY-INTENT** (byte-identical; no live commercial consumer post-cut).
- `AsyncDeliveryAccepted_v1.quote: Optional[QuoteEnvelope_v0]` field (frozen contract 22, snapshot SHA `0cdb911b…`) — **ORPHAN-IN-PLACE / CONFORMS-BY-INTENT** (field byte-identical; live producer emits `None` post-cut).
- `WizardCommitState_v0.variant: Literal["operator", "buyer"]` Literal (frozen contract 23, snapshot SHA `f1551af2…`) — **ORPHAN-IN-PLACE / CONFORMS-BY-INTENT** (Literal byte-identical; `"buyer"` is orphan value with no live producer post-cut).

### III.2 Route archaeology — post-cut endpoint inventory

**Convention:** each row = `METHOD path — brief-scope — VERDICT`. Verdicts:
- CONFORMS = current tree serves the v2.1/v1.4 anchor as-specified
- EXTENDS = current tree partially serves; identifies seam
- NEW-BUILD = fresh scope
- N/A = infra/legacy/pre-v2.1; verdict not applicable at this map depth

**System / infra:**
- `GET /api/health` — liveness probe — CONFORMS
- `GET /api/system/state` — pod state — N/A
- `GET /api/openapi.json` / `GET /api/docs` / `GET /api/redoc` — auto-doc — N/A

**Contracts (read-only):**
- `GET /api/contracts/five_rings` / `GET /api/contracts/objective_request` / `GET /api/contracts/qualification_matrix` — contract JSON schema — CONFORMS

**V1 / G1 harness (historical, closed):**
- `GET /api/v1/status` — V1 harness state — N/A
- `GET /api/v3/status` — V3 harness state — N/A
- `GET /api/v1/stamp_audit/recent` / `GET /api/v1/stamp_audit/by_unit/{unit_id}` — stamp-audit read — CONFORMS (feeds §4.2 Prove-one-run ledger row)

**Solva:**
- `GET /api/solva/status` — Solva engine state — N/A
- `GET /api/solva/trace/{trace_id}` — Solva trace read — EXTENDS (cousin of northena/trace/{id} for §4.2)

**Northena / trace-lens (frozen contract 9):**
- `GET /api/northena/status` — engine state — N/A
- `GET /api/northena/ledger/open_runs` — open runs list — EXTENDS (feeds §4.2 Prove-one-run + §4.3 Retention past-due)
- `GET /api/northena/ledger/by_run/{run_id}` — per-run ledger read — CONFORMS (§4.2 Ledger row substrate)
- `GET /api/northena/trace/{trace_id}` — trace-lens envelope read — **CONFORMS** (§4.2 Prove-one-run direct substrate; LOAD-BEARING for B-5a)

**Discipline / handoff:**
- `GET /api/discipline/lift_manifest` — lift-manifest envelope read — N/A (build-discipline surface)
- `GET /api/handoff/backend_contract_surface_v1` — freeze-and-handoff read — N/A

**Mtafiti (feasibility):**
- `POST /api/mtafiti/feasibility` — feasibility query (v2.1 §3.2 estate-check chip substrate) — CONFORMS

**Service 1 (extraction dispatch — the single-contract §5.5 endpoint):**
- `GET /api/service_1/status` — engine state — N/A
- `POST /api/service_1/run` — V1 dispatch (legacy) — CONFORMS (returns Service1Refusal_v0 with outcome=refused per §1 global rule)
- `GET /api/service_1/run/{run_id}` — V1 dispatch status — CONFORMS
- `POST /api/service_1/v2/dispatch` — **§5.5 single-contract endpoint** — **EXTENDS** (see Anchor 2; path dichotomy + reach/disclosure ceiling + usage/refusal-health remain gap)

**Objectives (async delivery):**
- `POST /api/objectives` — async admission — CONFORMS (§5.2 Async variant; returns AsyncDeliveryAccepted_v1 @202 per §7 async contract)
- `GET /api/objectives/{objective_id}` — async status poll — CONFORMS
- `POST /api/objectives/{objective_id}/cancel` — caller-driven cancel — CONFORMS (5-state machine; thin cancelled envelope)

**Auth (custom JWT + bcrypt, per Owner E1):**
- `POST /api/auth/register` — identity registration — CONFORMS (§1 global rule access-control class)
- `POST /api/auth/login` — login → TokenPair — CONFORMS
- `POST /api/auth/refresh` — refresh access token — CONFORMS
- `GET /api/auth/me` — identity + roles read — CONFORMS

**Pricing (extractor-internal cost/capacity — commercial-tier ORPHAN):**
- `GET /api/pricing/model_version` — read (internal) — CONFORMS (§6.4 operational rulebook)
- `POST /api/pricing/model_version` — Path B honest 501 — CONFORMS (per B-4 close: `{reason: requires_versioned_file_change_by_owner}`)
- `GET /api/pricing/tiers` — read (internal-tier config) — EXTENDS (§6.4 scope-split; commercial tier config is ORPHAN-IN-PLACE)
- `POST /api/pricing/tier_lock` — Path A ledger write (master_admin) — CONFORMS (§6.2 Change-a-rule commit path)
- `POST /api/fleet/policy` — Path B honest 501 — CONFORMS

**Master Admin (Administration Console §6):**
- `GET /api/master_admin/pending_seams` — pending-seams enumeration — CONFORMS (§6.1 pending banner substrate)
- `GET /api/master_admin/audit_trail` — audit-trail read — CONFORMS (§6.3 What-I've-changed substrate)

**Operator (Extraction Console §3):**
- `GET /api/operator/status` — operator home status read — CONFORMS (§3.1 Home status-line substrate)

**Wizard operator (Extraction Console §3.2 + §3.3):**
- `POST /api/wizard/operator/session` — session create — CONFORMS
- `POST /api/wizard/operator/{session_id}/turn` — chat turn — CONFORMS (§3.2 Commission wizard)
- `POST /api/wizard/operator/{session_id}/agent-assumption` — agent-assumed field — CONFORMS (§1 global rule agent-assumed marking)
- `POST /api/wizard/operator/{session_id}/commit-review` — pre-freeze review — CONFORMS (§3.3 Freeze commit review)
- `POST /api/wizard/operator/{session_id}/freeze` — freeze objective — CONFORMS (§3.3 Frozen-is-immutable binding copy)
- `GET /api/wizard/operator/{session_id}` — session read — CONFORMS
- `POST /api/wizard/operator/{session_id}/handoff` — admission handoff — CONFORMS

**Engineer (Integration Console §5 — §5.1 + §5.3 substrate; §5.4 dual-actor NEW-BUILD; §5.5 API §5.2 First-call):**
- `POST /api/engineer/key_grants` — key issuance — EXTENDS (§5.1 register + issue; §5.4 dual-actor gap)
- `GET /api/engineer/key_grants` — key grants list — EXTENDS (§5.3 Administer; §5.4 own-only filter gap)
- `POST /api/engineer/key_grants/{grant_id}/revoke` — key revocation — EXTENDS (§5.1 revocation; §5.4 dual-actor gap)

**Route archaeology summary:** 39 live `/api/*` routes catalogued.
- CONFORMS: 26
- EXTENDS: 8 (northena/ledger/open_runs, solva/trace, service_1/v2/dispatch, pricing/tiers, engineer/key_grants POST+GET+revoke, service_1/run — soft EXTENDS on ledger reads for §4.2 Prove-one-run)
- NEW-BUILD: 0 (no route rooted in v2.1 NEW-BUILD anchor is currently mounted)
- N/A: 5 (infra/openapi/system-state/lift-manifest/handoff)

*Note:* the CONFORMS count is generous on legacy V1/G1 routes because
they existed before v2.1 and pre-exist any conformance-check. The
NEW-BUILD verdicts flow through §III.3 (v2.1 sections) not through
route rows.

### III.3 Non-queue anchors — v2.1 §1 through §12 minus the four priority anchors

- **§1 Global rules — every surface, every application** — CONFORMS (four-response-class rule preserved through 26 frozen contracts; refusal-first-class + class-with-claim + one-trace-thread + plain-language + agent-assumed marking all landed at various phases with dedicated invariants).
- **§2 Surface taxonomy** — CONFORMS-BY-INTENT (four-consoles-plus-applications model reflected in current tree: Ask console at `/`, Extraction/Integration/Administration consoles under `/operator, /engineer, /master_admin`; Compliance Console at §4 is NEW-BUILD).
- **§3.1 Extraction Console Home** — CONFORMS (OperatorHomePage.js + `GET /api/operator/status`; §3.1 status-line + at-most-one-attention-card + running list + capacity strip all landed at B-2).
- **§3.2 Commission wizard** — CONFORMS (CommissionWizardPage.js + wizard_operator endpoints; §3.2 chat + draft-rail + estate-check chip all landed at B-2).
- **§3.3 Freeze — commit review** — CONFORMS (CommitReviewPage.js; §3.3 you-supplied + agent-assumed + feasibility-verdict + Frozen-is-immutable binding copy all landed at B-2; grounding marker present per B-3 dual-delta rendering).
- **§3.4 Sampling — sample-before-commit** — NEW-BUILD (§3.4 lands with Phase 9 per anchor citation; no current-tree code).
- **§3.5 Registry administration** — NEW-BUILD (§3.5 lands with Phase 9 per anchor citation).
- **§3.6 Quality observation** — EXTENDS (mining-stage-visibility exists in existing operator surface; §3.6 named-as-capability posture landed at B-2 attention-card pattern).
- **§4.4 Compliance rulebook** — NEW-BUILD (B-5b scope; depends on §8 checker).
- **§4.5 Write mechanics under the checker** — NEW-BUILD (B-5b scope).
- **§5.1 Register an application** — EXTENDS (engineer key_grants POST landed at B-3; §5.1 UI form + class choice + path choice + async-fields + sandbox-toggle are landed on EngineerRegisterAppPage.js at B-3).
- **§5.2 First call — the contract** — CONFORMS (EngineerFirstCallPage.js at B-3 with 5.2 verbatim binding copy "There is no response shape in which the claim is separable from its class. Infrastructure faults return 500 and are never rendered as refusals."; fixture-schema Jest gate at B-4 pins fixture parses through frozen contracts).
- **§5.3 Administer** — EXTENDS (EngineerAdministerPage.js at B-3; §5.3 attention + applications list landed; §5.4 dual-actor filtering gap remains).
- **§5.6 Dual-actor scoping continues** — NEW-BUILD (external_engineer as integrating partner posture NOT in current tree; conflation-prevention text is documentation-only).
- **§6.1 Administration Console Home** — CONFORMS (MasterAdminHomePage.js at B-4 with pending-banner + prompt + 6 binding-label buttons + footer; §6.1 verbatim landed).
- **§6.2 Change a rule** — CONFORMS (ChangeARulePage.js at B-4; §6.2 verbatim landed with Path A tier_lock ledger integration; Path B honest 501 for model_version + fleet_policy).
- **§6.3 Audit trail** — CONFORMS (AuditTrailPage.js at B-4; §6.3 verbatim landed with inline collapsible pre-block for full diff per Owner ratification).
- **§6.4 Scope split** — EXTENDS (§6.4 mentions operational rulebook only; compliance-rule read-only-on-Administration marker is NEW-BUILD scheduled per BCR v1.4 §3.13 B-4 retrofit).
- **§6.5 Roles and rights** — NEW-BUILD (capability named at v2.1 §6.5; no current-tree screen; role-grant surface NEW-BUILD).
- **§6.6 Counter-sign duties** — NEW-BUILD (depends on §8 checker landing).
- **§7.1 Internal Reference Application — Ask console** — CONFORMS (AskConsolePage.js at Phase 8a-lite with §7.1.1 Ask + §7.1.2 Answer + §7.1.3 Refusal verbatim; five response branches code-covered; NO output picker per §7.1 preset-invisible rule).
- **§7.2 Commercial applications — Sales Service** — N/A (STUB; separately-specified out-of-tree; extractor has no live commercial surface post-cut).
- **§8 Consequence-class checker** — NEW-BUILD (BCR v1.4 §3.11 — cross-console checker; lands per sequencing; §0.2 debt none currently open on this).
- **§9 Sampling — extraction only** — NEW-BUILD (§9 anchors are §3.4 Extraction sample [lands Phase 9] + Pull sample [CUT to Sales Service]).
- **§10 Cross-surface bindings** — CONFORMS (binding-copy set enforced across surfaces via Jest verbatim-copy gates at B-2/B-3/B-4/8a-lite; §10 pattern-carry verified through 12 Jest gates at B-4).
- **§11 Migration map and builder impact** — CONFORMS (commercial-cut close 2026-07-06 executed the §11 subtractive-cut list; salvage manifest verifies preservation).
- **§12 Sales Service — separate product (stub)** — N/A (STUB; boundary preserved by commercial-cut; extractor has no `price/quote/offer/catalogue/order/buyer` symbols post-cut per MAN-G1 gate).

### III.4 BCR v1.4 §3.1-3.14, §5 sequencing, §12 commercial cut

- **§3.1 V1 Extraction — processing layer 1 (Phase 9)** — NEW-BUILD (Phase 9 scope).
- **§3.2 V3 last mile — artifact store** — NEW-BUILD (post-B-5 phase per BCR).
- **§3.3 Benchmark — validation in-phase, calibration as tuning layer** — NEW-BUILD (V-inside-Phase-9 + C-as-continuous).
- **§3.4 Production housing — packaging and data plane** — N/A (deployment/infra; out of build-completion depth here).
- **§3.5 Seam 3 — authorized deletion path (before B-5)** — NEW-BUILD (retention config + deletion event + invariant per BCR technical annex).
- **§3.6 B-5a Compliance Console read/prove half** — priority anchor 1 above (EXTENDS backend / NEW-BUILD frontend).
- **§3.6B B-5b Compliance Console rulebook writes under checker** — NEW-BUILD (depends on §3.11 + follows B-5a).
- **§3.7 Transform forms §6.3/§6.4 (post-B-5 phase)** — NEW-BUILD (knowledge_artifact + callable_skill; §0.1 Ruling 5 confirmed as written).
- **§3.8 Answer fluency — V2 quality completion** — NEW-BUILD.
- **§3.9 Dual-actor engineer surface — internal and external engineers** — priority anchor 3 above (NEW-BUILD).
- **§3.11 The consequence-class checker (cross-console)** — NEW-BUILD.
- **§3.12 The sampling primitive (cross-console)** — NEW-BUILD (extraction expression Phase 9 + integration expression post-artifact-store).
- **§3.13 B-4 retrofit — compliance rules read-only on Administration (scheduled)** — NEW-BUILD (small retrofit at B-4-close; not yet done).
- **§3.14 Recorded open — not specified here** — N/A (explicitly out of scope by BCR itself).
- **§5 Sequencing** — CONFORMS (build has followed §5.1 builder-side order through Phase 8 B-4 close + commercial cut; §5.2 owner-side critical path is owner-owned).
- **§12 Commercial cut** — CONFORMS (executed 2026-07-06; close report SHA `bbf14900…`; MAN-G1/G2/G3 GREEN; salvage MANIFEST SHA `31962579…`; 14 requirement IDs CUT-1..4 / PRES-1..3-ALT / MAN-1 / MAN-G1..G3 / BND-1..2 all satisfied).

---

## §IV. Non-priority anchor verdict counts (for return format point 4)

- **Orphan-value rows** (4 rows): 4 CONFORMS-BY-INTENT / 0 EXTENDS / 0 NEW-BUILD / 0 DIVERGES.
- **Route archaeology** (39 route rows): 26 CONFORMS / 8 EXTENDS / 0 NEW-BUILD / 5 N/A.
- **v2.1 non-queue anchors** (25 anchors — §1-§12 minus 4 priority): 15 CONFORMS / 3 EXTENDS / 7 NEW-BUILD / 0 DIVERGES.
- **BCR v1.4 §3/§5/§12 anchors** (14 items enumerated): 11 NEW-BUILD / 2 CONFORMS / 1 N/A / 0 DIVERGES.

**Overall map surface:** 82 individual verdict assignments. **0 DIVERGES.**

---

## §V. §0.2 Plan Debts — status at conformance-map close

**No new debts arise from the map.** The map is read-only + a bookkeeping
preamble; the only genuinely surfaced divergence is anticipated Phase 9
/ B-5a scope, which is by-design (BCR-anchored) not divergent.

**Existing debt remaining:** **Phase 8c DPO `wizard_transcript`
separately-addressable held-class enumeration** — this is the one debt
that lands with B-5a per v2.1 §4.3 "Held-classes render separately
addressable: ledger rows, wizard transcripts, delivered artifacts".
B-5a Stage A will address this in the retention-and-rights screen
specification. Debt citation preserved at ORCHESTRATOR_CONTINUITY §0.2
[Owner ruling, Phase 7 B-1 close, 2026-07-04; refined at Phase 8 Stage A
dispatch, 2026-07-04].

**All other §0.2 debts remain RESOLVED** at the pre-cut state. Zero new
citations arising from this map.

---

## §VI. Standing constraints compliance

| Constraint | Status |
|---|---|
| 26 frozen contracts byte-identical (read-only map + bookkeeping; zero code changes to backend or frontend source) | PRESERVED — mechanical parity 3/3 GREEN; count-invariant GREEN |
| No LLM outside Shield | PRESERVED — no LLM code added; SonnetWizardAgent extraction already accepted at commercial-cut close |
| §0.1 Standing Dispositions FROZEN | PRESERVED — 0 new dispositions at this map |
| §0.2 Plan Debts updates only if genuine debt surfaced | PRESERVED — 0 new debts; only the pre-existing wizard_transcript debt remains open |
| No `git push` dev-side | HONOURED — Owner pushes at close acceptance |
| Standing Rule v3 (canonical markdown + SHA; no full-text implementation paste) | HONOURED (this file) |
| Playwright chromium-only invariant | PRESERVED — no e2e changes at this map |
| 4-code auth registry closed (auth_missing / auth_expired / auth_scope_insufficient / auth_identity_mismatch_for_wizard_session) | PRESERVED — registry byte-identical |
| Escalation cap ORIGINAL wording (defaults everywhere except frozen-contract, owner-value, or governance-semantic contact) | RESTORED — commercial-cut close scope-specific extension WITHDRAWN per Owner ruling |
| Standing correction (orchestrator-side): test matrix enumeration for Stage-A dispatches | INTERNALIZED — applies to B-5a Stage A next dispatch, NOT this map (this dispatch is read-only + preamble; no test matrix required) |

---

## §VII. HAZARD-STOP log

**Zero HAZARD-STOP events at this dispatch.** The map is a read-only
review of the post-cut tree against v2.1/v1.4 anchors; the preamble
(Part 1) is a bookkeeping realignment of manifest rows already ratified
at commercial-cut close 2026-07-06. Substrate-drop gate re-verified
GREEN post-preamble edits.

**Single mid-dispatch observation** (not HAZARD-STOP; recorded for
transparency): the substrate-drop gate initially failed for G5a/G5b/G6
after v1 was moved to Archive-block (Owner directive: "no-longer-consumed"),
because those historical closed gates still referenced v1 in
`phase_source_requirements.yaml`. Two dispositions were possible: (a)
redirect G5a/G5b/G6 to v2.1 per Owner literal directive; (b) keep v1 as
gated row in Specs-filed table (preserve historical pointer). Chose (a)
per Owner literal directive; v1 marked "no-longer-consumed" in
Archive-block means NO phase should reference it. Per-phase inline
comments in the YAML file preserve the historical-what-was-built context
via v1 → v2.1 anchor-mapping notes.

---

## §VIII. Ready for B-5a Stage A dispatch — YES

**Post-map posture:**
- Preamble complete (v2.1 + BCR v1.4 canonical rows added; v1 archived; phase pointers redirected; substrate-drop 13/13 GREEN).
- Four priority anchors carry full evidence packages; B-5a Stage A has all knowledge points enumerated in §II.
- Non-priority anchors one-line-catalogued; no evidence packages expanded (per Owner scope).
- Zero new frozen contracts. Zero new §0.1 dispositions. Zero new §0.2 debts. Zero HAZARD-STOP events.

**Specific anchor knowledge points forwarded to B-5a Stage A:**

1. **Anchor 1 (v2.1 §4.1-4.3):** Backend seam substrate exists at
   `GET /api/northena/trace/{trace_id}` (LOAD-BEARING for §4.2 Prove-one-run);
   two new backend read endpoints required (retention-config read + refusals-by-month
   aggregation); three frontend pages NEW-BUILD; held-classes must render
   separately addressable per v2.1 §4.3 + Owner E5 seam; BCR v1.4 §3.6
   gates B5a-G1/G2/G3 enumerate the invariant surface.

2. **Anchor 2 (v2.1 §5.5):** `POST /api/service_1/v2/dispatch` IS the
   single-contract endpoint; scope-gate + response-Union + commercial-cut
   compliance preserved; §5.5 is NOT B-5a scope; B-5a Prove-one-run
   screen references this endpoint's `check_scope` call site + the
   AdmissionRefusal_v0 / QualifiedDataPayload / ComposedConclusion_v0
   response branches for §4.2 record rows (Scope / Refused / Standard).

3. **Anchor 3 (v2.1 §5.4):** Dual-actor scoping is NEW-BUILD; B-5a is
   NOT blocked by it; the E2 4-code auth-refusal registry is the correct
   pattern for external-scope denials and is already LIVE / preserved
   at B-4.

4. **Anchor 4 (Operator-agent line):** Live operator agent is
   `DeterministicStubAgent` (LLM-free); Shield-side has no live
   wizard-agent LLM binding post-cut; B-5a can rely on
   `CommittedValue_v0.source_tag` for ground-truth-of-who-said-what on
   Prove-one-run rendering (agent-assumed vs operator-supplied marking);
   no LLM knowledge posture required at B-5a dispatch.

**Not blocked. Not partial. Single-dispatch cap honoured.**

---

*End of conformance-map close report. SHA-256 computed after write and
recorded in the return message to Owner.*
