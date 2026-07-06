# Phase 8 Stage B-5a — Stage A Proposal (2026-07-06)

**Canonical marker (Standing Rule v3).** This on-disk markdown file is the
sole canonical record of the B-5a Stage A design proposal. Its SHA-256
(computed after write, quoted in return) is the immutable pointer. No
implementation code is pasted inline.

- **Dispatch:** Owner Phase 8 Stage B-5a dispatch (2026-07-06) —
  Compliance Console read/prove per UI Spec v2.1 §4.1-4.3 + BCR v1.4
  §3.6.
- **Sequence amendment (binding):** B-5a → Seam 3 + §8 checker → B-5b.
  BCR v1.4 §3.5's "before B-5" posture amended: B-5a runs FIRST; Seam 3
  (authorized deletion path) + §8 consequence-class checker land BETWEEN
  B-5a and B-5b; then B-5b (Compliance Console rulebook writes §4.4-4.5).
- **Escalation-cap wording (original, restored):** defaults everywhere
  except frozen-contract, owner-value, or governance-semantic contact.
- **Standing correction internalized:** test matrix enumerated
  (endpoints × postures × cases; pages × visual states × invariant
  gates), never a test-LoC lump.
- **§0.1 Standing Dispositions FROZEN** at this Stage A (zero new
  dispositions).

═══════════════════════════════════════════════════════════════════

## §1. v2.1 §4 Reading (verbatim)

### §4.1 Home (v2.1 lines 65-70)

- **Lookup** — *"Look up any run, claim, or acquisition by trace…"*
- **Attention** — *"Problems stated honestly."* Pattern: *"One retention
  window has passed — a 2019 call-in set is 14 days beyond its agreed
  hold. It has not been auto-deleted; that rule isn't set."*
- **Cards (three, exact)** —
  1. Runs with lawful basis
  2. Refusals this month with a *See what was refused* link
  3. Retention windows past due
- **RULE** — *"Adversarial to comfort — overruns, unset rules, and
  refusals are surfaced as problems and as evidence the governance
  bites, never hidden behind all-green summaries."*
- **BINDING COPY** — *"This is the same record every user's audit view
  reaches — read-only, nothing reconstructed for display."*

### §4.2 Prove one run (v2.1 lines 71-74)

- **Banner** — *"Lawfulness banner: lawful-basis reference ·
  commissioner · frozen and immutable."*
- **Record rows (five, exact)** —
  1. **Lawful basis** — *"verified present at admission"*
  2. **Scope** — *"nothing mined outside it"*
  3. **Refused** — *"{n} items — below the required standard, recorded
     not dropped"* + *See them* link
  4. **Standard** — *"enforced on every unit, server-side"*
  5. **Ledger** — *"append-only; current retention state stated
     honestly"*
- **BINDING COPY** — *"Read-only. This is the record itself, not a
  summary of it. Export for a regulator on request."*

### §4.3 Retention & rights (v2.1 lines 75-78)

- **Banner** (honest statement while unset) — BINDING COPY: *"No
  deletion rule is set. The system holds everything indefinitely and
  append-only until you set a retention window. This is a decision only
  you can make — the system won't guess a duration."*
- **Holdings rows** —
  1. Within window
  2. Past due (+ *Decide*)
  3. Delivered acquisitions (*"irreversibly transformed · licensed ·
     receipts on file"*)
  4. **Held-classes render separately addressable:** ledger rows,
     wizard transcripts, delivered artifacts — *"the compliance owner
     can scope one window or split per class."*
- **BINDING COPY** — *"Setting a retention window here becomes a
  governed rule — versioned, dated, and recorded like every control
  change."*

**Zero paraphrase.** No partial-rendering; every element above is a
binding element that MUST land at Stage B.

═══════════════════════════════════════════════════════════════════

## §2. Test Matrix — ENUMERATED (per B-4-close-acceptance standing correction)

### §2A. Endpoint × posture × case matrix (BACKEND)

#### §2A.1 `GET /api/compliance/retention_config` (NEW-BUILD)

| Auth posture | Response case | Test name | Verdict |
|---|---|---|---|
| No token | 401 `{reason:"auth_missing", detail:...}` | `test_retention_config_no_token_401_auth_missing` | E2 taxonomy |
| Expired token | 401 `{reason:"auth_expired", detail:...}` | `test_retention_config_expired_token_401_auth_expired` | E2 taxonomy |
| Wrong role (non-dpo, non-admin) | 403 `{reason:"auth_scope_insufficient", detail:...}` | `test_retention_config_wrong_role_403_auth_scope_insufficient` | E2 taxonomy |
| `dpo` role, all-unset (no global default, no class explicit) | 200 with 3 classes all `posture="unset"`, `global_default.days=null` | `test_retention_config_dpo_all_unset_states_honestly` | B5a-G3 substrate |
| `dpo` role, global default set, no class-split | 200 with 3 classes all `posture="inheriting"`, `global_default.days=<int>` | `test_retention_config_dpo_global_default_inheritance` | E5 seam |
| `dpo` role, explicit per-class split (all 3 explicit) | 200 with 3 classes all `posture="explicit"`, each with own `days` | `test_retention_config_dpo_full_split_all_three_classes` | E5 seam |
| `dpo` role, partial split (some explicit, others inheriting) | 200 with mixed postures | `test_retention_config_dpo_partial_split_mixed_postures` | E5 seam |
| `admin` role (equivalent-or-superset scope) | 200 same shape as dpo | `test_retention_config_admin_role_reads` | Role parity |

**Cells: 8.**

#### §2A.2 `GET /api/compliance/refusals?month=YYYY-MM` (NEW-BUILD)

| Auth posture | Response case | Test name | Verdict |
|---|---|---|---|
| No token | 401 `{reason:"auth_missing", detail:...}` | `test_refusals_aggregate_no_token_401_auth_missing` | E2 taxonomy |
| Expired token | 401 `{reason:"auth_expired", detail:...}` | `test_refusals_aggregate_expired_token_401_auth_expired` | E2 taxonomy |
| Wrong role | 403 `{reason:"auth_scope_insufficient", detail:...}` | `test_refusals_aggregate_wrong_role_403_auth_scope_insufficient` | E2 taxonomy |
| `dpo` role, malformed month param | 400 `{reason:"malformed_month", detail:"YYYY-MM required"}` | `test_refusals_aggregate_dpo_malformed_month_400` | Input honesty |
| `dpo` role, month with zero refusals | 200 with `totals.total=0`, empty `by_reason`, empty `by_day` | `test_refusals_aggregate_dpo_empty_month_honest_zero` | §4.1 substrate |
| `dpo` role, month with only admission-refusals | 200 with `totals.admission_refusals>0`, `totals.service_1_refusals=0`, `by_reason` shows admission codes only | `test_refusals_aggregate_dpo_admission_only` | Family isolation |
| `dpo` role, month with only service_1-refusals | 200 with `totals.service_1_refusals>0`, `totals.admission_refusals=0`, `by_reason` shows service_1 codes only | `test_refusals_aggregate_dpo_service_1_only` | Family isolation |
| `dpo` role, mixed month (both families) | 200 with `by_reason` enumerating codes across both families with `family` discriminator | `test_refusals_aggregate_dpo_mixed_families` | Family discriminator |
| `dpo` role, multi-code within admission family | 200 with `by_reason` enumerating distinct admission codes | `test_refusals_aggregate_dpo_multi_code_within_family` | Enumeration correctness |
| `admin` role | 200 same shape as dpo | `test_refusals_aggregate_admin_role_reads` | Role parity |

**Cells: 10.**

#### §2A.3 `GET /api/northena/trace/{trace_id}` (EXISTING; auth-reconciliation posture)

| Auth posture | Response case | Test name | Verdict |
|---|---|---|---|
| No token (regression: anonymous access preserved) | 200 with valid trace_id | `test_trace_endpoint_stays_anonymous_callable_regression` | Endpoint stability |
| `dpo` role | 200 with valid trace_id (positive path for Prove-one-run) | `test_trace_endpoint_dpo_positive_path` | §4.2 substrate |
| Not-found (existing coverage; ensure still green) | 404 `{"reason":"trace_id_not_found","message":...}` | `test_trace_endpoint_not_found_404_regression` | Existing |
| Malformed trace_id (existing coverage) | 400 `{"reason":"malformed_trace_id", ...}` | `test_trace_endpoint_malformed_400_regression` | Existing |

**Cells: 4.**

**Backend endpoint × posture × case grand total: 8 + 10 + 4 = 22 cells.**

### §2B. Page × visual state × invariant gate matrix (FRONTEND)

#### §2B.1 §4.1 Home — `ComplianceHomePage.js` (NEW-BUILD)

| Visual state | Invariant gate | Test name |
|---|---|---|
| Normal — three cards render (runs · refusals-this-month · retention past due) | Cards render binding-copy verbatim | `test_compliance_home_binding_copy_verbatim` |
| Attention — at-most-one attention card (Owner-standing pattern) | Never two attention cards simultaneously | `test_compliance_home_at_most_one_attention_card` |
| No-dashboards invariant (adversarial to comfort) | No "all-green" summary text or count-only-if-zero cheerful strings | `test_compliance_home_no_all_green_summary_string` |
| Auth-denied (non-dpo user) | 403 → AuthDeniedNotice (NOT RefusalCard) | `test_compliance_home_auth_denied_uses_authdeniednotice_not_refusalcard` |
| Backend fault (5xx / network) | InfraFaultView (NOT RefusalCard; infra-not-refusal doctrine) | `test_compliance_home_infra_fault_uses_infrafaultview_not_refusalcard` |
| Refusals card link → §4.2 with month filter | Anchor href includes month query param | `test_compliance_home_refusals_link_carries_month_query` |
| Retention past-due card → §4.3 Decide affordance | Anchor navigates to §4.3 with focus on past-due row | `test_compliance_home_past_due_navigates_to_retention` |

**Cells: 7.**

#### §2B.2 §4.2 Prove one run — `ComplianceProveOneRunPage.js` (NEW-BUILD)

| Visual state | Invariant gate | Test name |
|---|---|---|
| Empty (no trace_id searched) | Search input + placeholder + no card render | `test_compliance_prove_run_empty_state_no_card_render` |
| Loading (trace_id submitted, pending) | Loading indicator; no partial-row render | `test_compliance_prove_run_loading_no_partial_row_render` |
| Loaded (banner + 5 record rows verbatim) | All 5 rows present (Lawful basis · Scope · Refused · Standard · Ledger); binding-copy verbatim | `test_compliance_prove_run_loaded_all_five_rows_verbatim` |
| Refused row — "{n} items … + See them" | Renders count from trace-lens envelope + See-them link | `test_compliance_prove_run_refused_row_renders_count_and_see_them_link` |
| Ledger row — "current retention state stated honestly" | Renders current retention posture (from /api/compliance/retention_config); "unset" state renders honest banner | `test_compliance_prove_run_ledger_row_honest_retention_state` |
| Not-found (404) | 404 rendered honestly ("no record with that trace_id"); NOT via RefusalCard | `test_compliance_prove_run_not_found_honest_render_not_refusalcard` |
| Auth-denied (non-dpo user) | 403 → AuthDeniedNotice | `test_compliance_prove_run_auth_denied_uses_authdeniednotice` |
| Malformed trace_id (400) | Input validation message (client-side) OR 400 rendered honestly | `test_compliance_prove_run_malformed_trace_400_honest_render` |
| Export affordance (§4.2 binding "Export for a regulator on request") | Export button present with data-testid | `test_compliance_prove_run_export_button_present` |
| **B5a-G2 — resolves ANY trace** (not just wizard-frozen) | Test parametrised: wizard-frozen trace / async-delivery-accepted trace / v2-dispatch trace all render | `test_compliance_prove_run_resolves_any_trace` (parametrised × 3) |

**Cells: 10 (10th is parametrised × 3 = 12 collected).**

#### §2B.3 §4.3 Retention & rights — `ComplianceRetentionRightsPage.js` (NEW-BUILD)

| Visual state | Invariant gate | Test name |
|---|---|---|
| No rule set (banner fires with verbatim binding copy) | B5a-G3: honest banner text verbatim; no default hallucinated | `test_compliance_retention_no_rule_banner_verbatim` |
| Global default set, 3 classes inheriting | Inheritance-default badge visible on each class row | `test_compliance_retention_inheriting_default_badge_visible` |
| Explicit per-class split (all 3 explicit) | Each class row shows own window; no inheritance badge | `test_compliance_retention_explicit_split_no_inheritance_badge` |
| Partial split (some explicit, some inheriting) | Mixed badges rendered correctly per class | `test_compliance_retention_partial_split_mixed_badges` |
| Holdings rows (within window / past due + Decide / delivered) | All 3 holdings rows render; Decide affordance on past-due row | `test_compliance_retention_three_holdings_rows_render` |
| **Held-classes separately addressable** (parametrised × 3) | Each of `ledger_row`, `wizard_transcript`, `delivered_artifact` renders in structurally-separate DOM region with distinct semantic label | `test_compliance_retention_held_class_separately_addressable` (parametrised × 3) |
| Setting-a-retention-window binding copy | Verbatim text at bottom of surface: "Setting a retention window here becomes a governed rule …" | `test_compliance_retention_governed_rule_binding_copy_verbatim` |
| Auth-denied | 403 → AuthDeniedNotice | `test_compliance_retention_auth_denied_uses_authdeniednotice` |
| Backend fault | InfraFaultView | `test_compliance_retention_infra_fault_uses_infrafaultview` |
| **§4.3 is READ-ONLY at B-5a** | No write button reachable; Decide affordance is scoped to future B-5b (renders as "record decision — coming in rulebook writes") | `test_compliance_retention_no_write_route_reachable_at_b_5a` |

**Cells: 10 (6th is parametrised × 3 = 12 collected).**

#### §2B.4 Surface-agnostic invariant gates (Jest)

| Gate | Coverage | Test name |
|---|---|---|
| **B5a-G1 (read-only)** — no write route reachable from any of the 3 pages | grep-negative on POST/PUT/PATCH/DELETE call sites in the 3 page files | `test_compliance_surface_read_only` (parametrised × 3 pages) |
| **B5a-G3 (retention-unset states honestly)** — "no rule set" banner uses verbatim v2.1 §4.3 text | Static-string match against on-disk mandate SHA `ef6da4b4…` line 76 | `test_retention_unset_banner_verbatim_from_v2_1` |
| **E2 taxonomy extension** — 403s from `/api/compliance/*` route through AuthDeniedNotice, NOT RefusalCard | AST + testid-namespace-disjoint parametrised over 3 pages | `test_compliance_403_routes_through_authdeniednotice_not_refusalcard` (parametrised × 3) |
| **Held-class enumeration single-source** — the 3-class list `["ledger_row", "wizard_transcript", "delivered_artifact"]` is defined ONCE, consumed by (a) backend retention_config route (b) frontend §4.3 rendering (c) invariant gate | grep for the 3-class Literal — must appear as a NAMED constant in exactly one module; other consumers import | `test_held_class_enumeration_single_source` |
| **Barrel-reuse invariant** — no §4 page reimplements ClassBadge / RefusalCard / AuthDeniedNotice / OuterGateReceiptInline / StatusBadge / LedgerTable / TrustReceiptLink locally | Extend existing `test_shared_components_single_source_ui_spec_v1` to include §4 pages | `test_compliance_pages_consume_ui_spec_v1_barrel_no_reimplementation` (parametrised × 3 pages × 7 components = 21 collected) |
| **Fixture-schema Jest invariant** (extending B-4 pattern) — any illustrative JSON in §4 pages must parse through frozen contracts (TraceLensEnvelope; retention_config response Pydantic-mirror; refusals response Pydantic-mirror) | fs.readFileSync + subset-check against neighbor .contract_snapshot.json OR schema mirror | `test_compliance_page_fixtures_parse_through_frozen_contracts` |

**Gates: 6 (parametrised expansions: 3 + 1 + 3 + 1 + 21 + 1 = 30 collected).**

#### §2B.5 First-commit gating — Playwright chromium smokes

Per Owner Standing Pattern (first-commit gating from B-3 close acceptance): per-surface Playwright chromium smokes MUST land in the same commit block as each surface. No UNGATED holes.

| Smoke | Test file | Flow |
|---|---|---|
| §4.1 Home smoke | `compliance_home_smoke.spec.ts` | Login as dpo → visit `/compliance` → assert 3 cards render + attention posture + refusals-link-with-month + past-due-link-to-retention |
| §4.2 Prove one run smoke | `compliance_prove_one_run_smoke.spec.ts` | Login as dpo → visit `/compliance/prove/:trace_id` → assert banner + 5 record rows + See-them link on refused row + export button |
| §4.3 Retention & rights smoke | `compliance_retention_rights_smoke.spec.ts` | Login as dpo → visit `/compliance/retention` → assert banner-if-unset OR three-classes-separately-addressable rendering + 3 holdings rows + read-only-no-write-button |

**E2E smokes: 3.**

### §2 Grand totals

- Backend endpoint × posture × case cells: **22**
- Frontend page × visual state cells: **7 + 10 + 10 = 27** (raw)
- Frontend Jest invariant gates: **6 gates, 30 collected cases** (with parametrised expansions)
- Playwright chromium smokes: **3** (each ≥ 5 assertions)

**Total collected test cases at B-5a Stage B close: ~22 (backend) + ~27 (page states) + ~30 (invariant gates parametrised) = ~79 collected cases.**

═══════════════════════════════════════════════════════════════════

## §3. Endpoint Shape Proposals (dev defaults)

### §3A. Retention-config read — `GET /api/compliance/retention_config`

**Route:** `GET /api/compliance/retention_config`

**Response body shape (Pydantic model `RetentionConfigResponse` — UNFROZEN, per Owner Ruling 3 wire-shape LOAD-BEARING gate posture at 4a Stage B; docstring cites Ruling 3):**

Fields:
- `global_default: GlobalDefaultRetention` — global-level retention setting
  - `days: Optional[int]` — retention window in days (null = unset)
  - `set_at: Optional[str]` — ISO-8601 timestamp when set (null if unset)
  - `set_by: Optional[str]` — user_id who set it (null if unset)
- `held_classes: List[HeldClassRetention]` — length always exactly 3, ordered `["ledger_row", "wizard_transcript", "delivered_artifact"]`
  - `class_name: Literal["ledger_row", "wizard_transcript", "delivered_artifact"]`
  - `posture: Literal["inheriting", "explicit", "unset"]`
  - `days: Optional[int]` — resolved effective retention days
    - When `posture=="explicit"`: this class's own window
    - When `posture=="inheriting"`: mirrors `global_default.days`
    - When `posture=="unset"`: null
  - `set_at: Optional[str]` — ISO-8601 when explicitly set (null if inheriting or unset)
  - `set_by: Optional[str]` — user_id (null if inheriting or unset)

**Held-class enumeration mechanism:**

The 3-class list is defined as a named constant `HELD_CLASSES` in a
single module (`backend/services/compliance/held_class_registry.py` — a
lightweight registry). Frontend imports the same list via a shared JSON
config (or repeats the list literal with an invariant gate enforcing
single-source across backend + frontend + gate — see §2B.4 gate
"Held-class enumeration single-source").

**"Retention-unset states honestly" semantic distinction:**
- `global_default.days=null` AND all held_classes have `posture=="unset"` → **B5a-G3 substrate: banner fires with verbatim v2.1 §4.3 unset copy.**
- `global_default.days=<int>` AND all held_classes have `posture=="inheriting"` → inheritance-as-default posture per Owner E5 pre-ruling.
- Mixed / partial split → per-class postures rendered independently.

**Auth posture (dev default):**
- Roles allowed: `dpo` OR `admin`.
- Denials: 401 for missing/expired token; 403 `auth_scope_insufficient` for wrong role.
- Uses the existing E2 4-code auth-refusal registry — no new codes.
- Owner-note posture: lesser roles could receive a masked read (e.g. postures without `set_by` user_id); dev default is **NO MASKING at B-5a** — the endpoint is scoped tight (dpo/admin only) to keep the surface simple. If lesser-role read is desired later, it's a follow-on (§8 escalation candidate; see §8 below).

### §3B. Refusals-by-month aggregate — `GET /api/compliance/refusals?month=YYYY-MM`

**Route:** `GET /api/compliance/refusals?month=YYYY-MM`

**Query parameters:**
- `month: str` — required; format `YYYY-MM`; malformed → 400 `{reason:"malformed_month", detail:"Format required: YYYY-MM."}`.

**Response body shape (Pydantic model `RefusalsAggregateResponse` — UNFROZEN):**

Fields:
- `month: str` — echo of query param (normalized `YYYY-MM`)
- `totals: RefusalsTotals` —
  - `admission_refusals: int` — count where family is admission
  - `service_1_refusals: int` — count where family is service_1
  - `total: int` — sum
- `by_reason: List[RefusalReasonCount]` — one entry per distinct refusal code seen in the month; ordered by count descending, then reason alphabetically for determinism
  - `reason: str` — the deterministic reason string from `NorthenaLedgerRow_v1.reason`
  - `family: Literal["admission", "service_1"]`
  - `count: int`
- `by_day: List[RefusalDayCount]` — one entry per day in the month with ≥1 refusal (empty for zero-refusal months)
  - `day: str` — ISO date `YYYY-MM-DD`
  - `count: int`

**Data source:** `NorthenaLedgerRow_v1` collection where `outcome=="refused"`, filtered by `at` field within the month window `[YYYY-MM-01T00:00:00Z, next-month-01T00:00:00Z)`. Family discriminator inferred from the reason-registry name-prefix or from ledger `stage` field (admit-stage vs gate-stage) — implementation detail resolved at Stage B (dev-default: family inferred from the `_ADMISSION_REASONS` vs `_SERVICE_1_REASONS` registry sets — a pure-function classifier).

**Aggregation posture (dev default with justification):**
- **Both** `by_reason` and `by_day` returned in the SAME response.
  - `by_reason` serves the §4.1 Home refusals-this-month card.
  - `by_day` serves potential §4.2 Prove-one-run drill-down + provides future extensibility for §4.4 rulebook-write dashboards without wire-shape rework.
- Single Mongo aggregation pipeline computes both cheaply.

**Auth posture:** same as §3A (`dpo` OR `admin`; existing E2 4-code registry).

### §3C. Trace endpoint auth reconciliation — `GET /api/northena/trace/{trace_id}`

**Current auth check (verified at Stage A):** `backend/routers/northena.py:68-85` — NO auth check. Endpoint is anonymous-callable. Returns:
- 200 `TraceLensEnvelope` on success
- 404 `{"reason":"trace_id_not_found", "message":..., "trace_id":...}`
- 400 `{"reason":"malformed_trace_id", "message":...}`
- 500 (via unhandled) for infra faults

**Proposal (dev default): KEEP ANONYMOUS at endpoint level.**

Justification:
- v2.1 §4.1 binding copy states verbatim: *"This is the same record every user's audit view reaches — read-only, nothing reconstructed for display."* Requiring auth to see the trace-lens envelope contradicts the "every user's audit view" posture.
- G5a design (2026-07-02) landed this as anonymous-read; changing it now would break the Ask console trust-receipt deep-link `/legacy/trace/:trace_id` established at Phase 8a-lite.
- Owner E1/E2 symmetric-cut ratified at B-2: anonymous falls through when scope is not required; scoped callers get gated. Trace-lens is not a scope-gated endpoint per this posture.

**Compliance Console `dpo` role gating:**
- The `/compliance/prove/:trace_id` PAGE requires `dpo` role — auth-context guard at the frontend (mirroring master-admin console pattern from B-4).
- The underlying `GET /api/northena/trace/{trace_id}` API call from that page succeeds anonymously; auth is enforced at the PAGE mount, not at the API.
- Non-dpo users navigating to the Compliance Console see AuthDeniedNotice before the API call is even made (test cell `test_compliance_prove_run_auth_denied_uses_authdeniednotice`).

**Zero change to `TraceLensEnvelope_v0`** (frozen contract 9) — response shape stays byte-identical.

**Reconciliation regression:** one new test cell `test_trace_endpoint_stays_anonymous_callable_regression` explicitly pins the anonymous-callable posture so future auth-additions surface as regressions and require explicit Owner sign-off.

═══════════════════════════════════════════════════════════════════

## §4. Held-Class Rendering Mechanics (dev defaults per Owner E5 pre-ruling)

**Owner E5 pre-ruling (Message dispatch verbatim):**
> *"Three classes separately addressable: `ledger_row`, `wizard_transcript`, `delivered_artifact` — each renders as an independently-configurable entity with its own retention row."*
> *"Inheritance-as-default — retention window inherits from a system-wide default UNLESS DPO explicitly splits per class."*
> *"Mechanics are dev defaults stated at Stage A."*

### §4A. Enumeration mechanism (backend)

- Single named constant `HELD_CLASSES = ("ledger_row", "wizard_transcript", "delivered_artifact")` in `backend/services/compliance/held_class_registry.py`.
- `RetentionConfigResponse.held_classes` list always contains EXACTLY 3 entries in the order above (deterministic; test-verified).
- The registry provides `resolve_effective_retention(class_name: str) -> HeldClassRetention` — pure function.
- Grep-invariant (§2B.4 gate) enforces single-source across backend + frontend + tests.

### §4B. Frontend rendering (§4.3 Retention & rights)

Three structurally-separate DOM regions, each with distinct semantic
label. Not tabs, not a combined table with a "class" column — Owner
"separately addressable" reads as **rendering-independent**:

1. **Ledger rows region** — heading "Ledger rows"; retention row; posture badge (`inheriting` / `explicit` / `unset`); days value or unset copy.
2. **Wizard transcripts region** — heading "Wizard transcripts"; same row structure.
3. **Delivered artifacts region** — heading "Delivered artifacts"; same row structure.

Each region carries a distinct `data-testid` (e.g. `retention-region-ledger_row`, etc.) — the invariant gate `test_compliance_retention_held_class_separately_addressable` parametrises over the 3 class names and asserts each region is present, structurally-independent, and DOM-distinct.

### §4C. Inheritance-as-default indicator

- Each held-class row renders a **posture badge** that reads:
  - `inheriting` → badge: **"inherits from system default"** (subdued styling; distinct data-testid `retention-posture-inheriting`)
  - `explicit` → badge: **"class-specific window"** (prominent styling; data-testid `retention-posture-explicit`)
  - `unset` → badge: **"no rule set"** (adversarial-to-comfort styling; data-testid `retention-posture-unset`; part of B5a-G3 substrate)
- The badge component is a NEW single-source component under `frontend/src/components/ui_spec_v1/RetentionPostureBadge.jsx` and RE-EXPORTED from the barrel `frontend/src/components/ui_spec_v1/index.js` (invariant gate `test_shared_components_single_source_ui_spec_v1` extended).

### §4D. DPO-split-visible state

- When `held_classes[i].posture=="explicit"` for any i, the containing region shows the explicit badge + the class-specific window (days) prominently.
- When all 3 explicit → whole surface is "fully-split" posture; no inheritance banner.
- When mixed → per-region rendering (some inheriting, some explicit) — no summary banner (adversarial to comfort; state each honestly).

### §4E. Copy for "retention-unset states honestly" (B5a-G3)

- When `global_default.days=null` AND all 3 classes `posture=="unset"`:
  - Top-of-surface banner renders v2.1 §4.3 line 76 VERBATIM:
    > *"No deletion rule is set. The system holds everything indefinitely and append-only until you set a retention window. This is a decision only you can make — the system won't guess a duration."*
  - Each held-class region renders the "no rule set" badge.
  - No "unset means default N days" language — verbatim posture.
- Invariant gate `test_retention_unset_banner_verbatim_from_v2_1` compares against the on-disk v2.1 mandate line 76 by SHA to prevent drift.

═══════════════════════════════════════════════════════════════════

## §5. Rule 2 Anchor Via Test-Matrix Enumeration

**Per B-4 close-acceptance standing correction:** *"Stage-A sizing enumerates the test matrix — endpoints × postures × cases — never a test-LoC lump."*

### §5A. Cell counts (from §2)

- Backend endpoint × posture × case cells: **22**
- Frontend page × visual state cells: **27**
- Frontend Jest invariant-gate collected cases: **30** (6 gates with parametrised expansions summing to 30)
- Playwright chromium smokes: **3**

### §5B. LoC per-bucket derived from cells

| Bucket | Count | LoC/cell (from B-3/B-4 pattern) | Bucket LoC |
|---|---|---|---|
| Backend impl: 2 endpoint modules + shared registry + response models | (2 endpoints + 1 registry + 2 Pydantic response modules) | avg ~140L/module | ~350L (~140 + ~90 + ~120) |
| Backend tests: 22 endpoint cells | 22 × avg ~18L/cell | ~18L/cell (parametrised where posture-family repeats) | ~400L |
| Frontend impl: 3 pages + apiClient additions + App.js routing + RetentionPostureBadge | (3 pages @ ~260L avg + apiClient ~40L + App.js ~10L + badge ~40L) | avg ~260L/page | ~870L |
| Frontend Jest gates: 30 collected cases | 30 × avg ~14L/cell (many share files; parametrised expansions cheap) | ~14L/cell | ~420L |
| Playwright chromium smokes: 3 files | 3 × avg ~80L/spec | ~80L/spec | ~240L |

**Total anchor band:** [~2050, ~2450] LoC.

### §5C. Anchor band statement

**Anchor band: `[2050, 2450]` LoC.**

- **Backend implementation:** ~350L
- **Frontend implementation:** ~870L
- **Backend tests:** ~400L (22 cells × ~18L)
- **Frontend Jest gates:** ~420L (30 collected × ~14L)
- **Playwright smokes:** ~240L (3 × ~80L)

Mid-anchor: ~2250L.

**No test-LoC lump.** Test cell counts are the primary driver (22 backend + 30 frontend Jest + 27 page states embedded in page tests + 3 e2e); LoC is derived from cells.

**Rule 2 stop-and-judge posture:** if actual LoC lands above 2450, split-disposition applies per B-4 standing precedent (mandate-forced portion ratified inline; orchestrator-estimation-miss disposed with root-cause). If actual lands below 2050, no restatement needed (under-band is default-accept per Rule 2 v2).

═══════════════════════════════════════════════════════════════════

## §6. §0.2 Debt Resolution Mapping

### §6A. DPO `wizard_transcript` separately-addressable held-class enumeration

- **Debt origin:** *"Wizard transcript retention class is separately addressable — DPO can choose to hold transcripts on a different window than other classes. Held-class enumeration lands at B-5a (Compliance Console read/prove) per Owner E5 seam. [Owner ruling, Phase 7 Stage B-1 close, 2026-07-04; refined at Phase 8 Stage A dispatch, 2026-07-04]"*
- **Resolution surface at B-5a:** §4.3 Retention & rights page renders `wizard_transcript` as one of the 3 separately-addressable held-class regions (per §4B above).
- **Verification gate at close:** `test_compliance_retention_held_class_separately_addressable` parametrised × 3 including `wizard_transcript`. Additionally, the backend gate `test_retention_config_dpo_full_split_all_three_classes` proves the wire-shape supports `wizard_transcript` explicit-split independently.
- **Marked RESOLVED at Stage B close** with citation of these two gate names.

### §6B. Other §0.2 debts

None. All 11 prior debts remain RESOLVED at pre-cut / cut / conformance-map close postures; only the DPO wizard_transcript debt is open and lands here.

═══════════════════════════════════════════════════════════════════

## §7. Standing Constraints Affirmation

| Constraint | Status at Stage A |
|---|---|
| 26 frozen contracts byte-identical | AFFIRMED — B-5a adds ZERO new frozen contracts; `TraceLensEnvelope_v0` UNCHANGED; `NorthenaLedgerRow_v1` UNCHANGED (read-only consumption); `RetentionConfigResponse` + `RefusalsAggregateResponse` are UNFROZEN (Ruling 3 wire-shape gate posture with LOAD-BEARING test at Stage B). Mechanical parity 26/26 stays green. |
| No LLM outside Shield | AFFIRMED — B-5a is a read/prove surface; no LLM code lands. |
| §0.1 Standing Dispositions FROZEN | AFFIRMED — zero new dispositions proposed at Stage A. |
| §0.2 update at close | PLANNED — mark DPO wizard_transcript separately-addressable held-class as RESOLVED with §4.3 evidence (§6A above). |
| No `git push` dev-side | AFFIRMED — Owner pushes at close acceptance. |
| Standing Rule v3 | HONOURED — this proposal is on-disk canonical + SHA; no full-text implementation paste. |
| First-commit gating standing pattern | AFFIRMED — 3 Playwright chromium smokes (§2B.5) land WITH the surfaces in the same commit block. |
| Playwright chromium-only invariant | AFFIRMED — no other browsers. |
| Shared §8 barrel consumed; NO reimplementation | AFFIRMED — new `RetentionPostureBadge` added to barrel; §4 pages consume via barrel; parametrised invariant gate covers all 7 (soon 8) components × 3 §4 pages. |
| 4-code auth registry closed | AFFIRMED — DPO-related 403s use existing `auth_scope_insufficient` / `auth_missing` / `auth_expired`. Zero new codes at B-5a. |
| Escalation cap ORIGINAL wording | AFFIRMED — defaults everywhere except frozen-contract, owner-value, or governance-semantic contact. No scope-specific extensions. |
| Standing correction (test matrix enumeration) | INTERNALIZED AND APPLIED — §2 above enumerates endpoints × postures × cases + pages × visual states × gates; §5 LoC anchor derived from cells, not lumped. |
| Sequence amendment (B-5a → Seam 3 + checker → B-5b) | RECORDED — will be inserted into ORCHESTRATOR_CONTINUITY §2 Phase Ledger at Stage A close per Owner directive. |

═══════════════════════════════════════════════════════════════════

## §8. Escalations to Owner (if any)

**Owner posture:** default everywhere except frozen-contract, owner-value, or governance-semantic contact.

### §8.1 — none required at Stage A. Design surfaces cleared per default posture.

**Candidate items considered but NOT escalated** (dev defaults chosen per posture — flagged here for Owner visibility, not asking for ruling):

1. **Trace endpoint anonymous-callable preservation** (§3C). Default: KEEP ANONYMOUS. Not escalated because: (a) it's the EXISTING G5a design; (b) v2.1 §4.1 binding "every user's audit view" supports it verbatim; (c) Ask console trust-receipt deep-link depends on it. If Owner disagrees, one ruling flip changes the auth-reconciliation cell in §2A.3 and the frontend §4.2 auth path.
2. **Refusals aggregate: both `by_reason` AND `by_day` in same response** (§3B). Default: BOTH. Not escalated because: (a) single Mongo aggregation pipeline computes both cheaply; (b) `by_day` future-proofs §4.2 drill-down and §4.4 rulebook write dashboards without wire-shape rework. If Owner prefers `by_reason` only, a field-set trim is trivial (one Pydantic field removal + one test-cell drop).
3. **Retention config: NO MASKING for lesser roles** (§3A). Default: `dpo` OR `admin` only; other roles get 403. Not escalated because: (a) simplest surface; (b) matches master-admin B-4 pattern; (c) lesser-role masked read is a follow-on decision, not a B-5a blocker.
4. **RetentionPostureBadge as new barrel component** (§4C). Default: NEW single-source component in the shared UI-Spec-v1 barrel. Not escalated because: (a) it's an additive component consumed only within §4.3; (b) barrel-reuse invariant gate ensures no reimplementation. Zero contract impact.
5. **§4.3 "Decide" affordance is READ-ONLY at B-5a** (§2B.3 last row). Default: renders as "record decision — coming in rulebook writes" placeholder (no active write action). Not escalated because: (a) v2.1 §4.4/§4.5 rulebook writes are explicitly B-5b scope; (b) Owner sequence amendment landed Seam 3 + checker BETWEEN B-5a and B-5b, so writes are two dispatches out.

**Zero governance-semantic contact.** Zero frozen-contract mutation. Zero owner-value drift.

═══════════════════════════════════════════════════════════════════

## §9. Ready-for-Stage-B posture

**Stage B implementation, on Owner ratification of this Stage A, proceeds as ONE dispatch (single close):**

1. Backend impl: 2 endpoints + shared held-class registry + Pydantic models — first block.
2. Backend tests (22 cells) — same commit block as impl (first-commit gating).
3. Frontend impl: 3 pages + apiClient additions + App.js routes + RetentionPostureBadge in barrel — second block.
4. Frontend Jest gates (30 collected) + Playwright chromium smokes (3) — same commit block as frontend impl.
5. §0.2 debt marked RESOLVED at close report with dual-gate citation.
6. ORCHESTRATOR_CONTINUITY §2 Phase Ledger new row + PHASE_STATE.md + PRD.md mirror updates.
7. Close report on-disk canonical at `/app/docs/close_reports/phase_8_b_5a.md` (SHA quoted in return).

**No B-5b, Seam 3, or §8 checker scope in this Stage B.** Post-B-5a close, Owner dispatches the next in the amended sequence.

---

*End of Stage A proposal. SHA-256 computed after write and recorded in return message to Owner.*
