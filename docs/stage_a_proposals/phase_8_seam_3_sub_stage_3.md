# Phase 8 Seam 3 Sub-stage 3 — Stage A Design Proposal (§8 consequence-class checker)

**Design date:** 2026-07-07 (pre-Amendment-G)
**Amendment G applied:** 2026-07-07 (post-Owner-Rulings-1–7 restructure; see rulings record §11).
**Scope authority:** Stage A proposal `/app/docs/stage_a_proposals/phase_8_seam_3_and_checker.md` §6 verbatim (SHA `3fe969c2add52da7f4d80251a8bcb2d1bcf3154c82a10a7fb2241d44bb08500d`).
**Rulings pre-carried:** E1–E7 (§1–§9 rulings record); R-1..R-6 (§10 rulings record); **Rulings 1–7 (§11 rulings record, Amendment G, 2026-07-07)**. Pre-Amendment-G rulings-record SHA: `7c2b61f1e739c3f88689bf7ec235a1f259655d539fe9fc1babd3a1f1d30f6653`.
**Dispatch-A verdict (Owner-ruled, Amendment G, 2026-07-07):** Path 3 confirmed **BUT** the +500 LoC sidecar-key retrofit is REJECTED as redundant (Ruling 1). `stamp_audit["data_class"]` is the pinned canonical governance-event class carrier established at Sub-stage 2; a `governance_artifact_type` key would duplicate it. Retrofit collapses to three items (see §8.4 rewrite). Band B is **VOID**; band re-derives around Band A only (Ruling 5).

**`artifact_ref` field determination (Ruling 1(i) fork):** `NorthenaLedgerRow_v1.artifact_ref: LedgerArtifactRef` is **REQUIRED** (verbatim from `/app/backend/contracts/northena_ledger_v1.py:60`; no `Optional[…]`, no default). Per Ruling 1(i) required-branch: placeholder stands **vestigial-by-ruling** — Sub-stage 2's existing `artifact_type="objective_request"` pragmatic-choice pattern (see `backend/routers/compliance.py:305-314`) is reused for Sub-stage 3 rule-change events. Corrective note in Sub-stage 3 close records: on governance-event rows `artifact_type` is non-authoritative; the honest event class lives at `stamp_audit["data_class"]`.

Standing Rule v3: this proposal lives on disk. Reply body is a header row of SHA + structural summary.
Standing Correction: matrix-enumerated sizing (endpoints × postures × cases × invariants), never LoC lumps.
Standing 409 anti-rule (elevated §8.2 of rulings record): no HTTP 409 anywhere in Sub-stage 3 diff — full-anti-rule enforcement reactivates at Sub-stage 3.
E7 middle-dot strict: Playwright asserts `·` (U+00B7) glyph specifically on banner render.

═══════════════════════════════════════════════════════════════════

## §0. Table of contents

- §1. Substrate reads (Stage A §6 + rulings + Sub-stage 1/2 landings)
- §2. Existing tree reads (checker-adjacent surface baseline)
- §3. Sub-stage 3 deliverables (backend + frontend + tests + retirements)
- §4. Test matrix — cells × postures × cases × invariants (BAND A)
- §5. Retrofit surface (§12 registry retrofit, BAND B additive)
- §6. Test matrix — retrofit deltas (BAND B additive cells)
- §7. Rule 2 anchor bands (BAND A + BAND B)
- §8. Escalations to Owner (S3-E1 through S3-E5)
- §9. Split-proposal candidacy assessment
- §10. Ready-to-dispatch posture per band

═══════════════════════════════════════════════════════════════════

## §1. Substrate reads

**Stage A §6 verbatim scope (SHA `3fe969c2…`, lines 295-368):** Sub-stage 3 = §8 consequence-class checker. Deliverables enumerated below (§3). Anchor band per §9 line 562 = `[2000, 2500]` LoC, `snapshot_lloc_in_band = no` (no new frozen contract). Estimated 49 cells per §6 test matrix table.

**Post-Sub-stage-2 substrate reused:**
- `services/compliance/deletion_ledger.py::emit_deletion_ledger_row` (canonical writer; extended pattern applies to rule-change events).
- `services/compliance/data_class_registry.v0.json` (registry pattern; will extend to countersigned_rule_change / tightening_effective / tightening_objected).
- `services/compliance/retention_config_writes.py::write_retention_config` (consequence-class routing hook lands here).
- `services/retention/authorized_deletion.py` (SINGLE-SOURCE-OF-DELETION module unchanged).

**E2 gate retirement:** `test_retention_endpoint_loosening_disabled_pre_checker` retires at Sub-stage 3 close; replaced by `test_retention_loosening_write_requires_administration_countersign` (CK-B3 symmetry, per Stage A §6.1 line 302).

**R-1 mirror gate retention:** `test_deletion_terminal_row_carries_registry_valid_data_class_in_stamp_audit` (Sub-stage 2 LB) remains active; Sub-stage 3 adds mirror gates for rule-change events under the same data-class registry.

**Frozen contract parity:** 26 unchanged (E1.γ + E1.β both anchored; §7.1 preserves byte-identity across all sub-stages).

**Middle-dot glyph binding:** E7 discipline continues — `CounterSignBanner.jsx` commit-line copy per CK-U1 = `"Signed by {initiator} · counter-signed by {checker} · recorded with both identities."` (verbatim from Stage A §6.1 line 330).

═══════════════════════════════════════════════════════════════════

## §2. Existing tree reads (checker-adjacent surface baseline)

- `services/checker/` — does NOT exist yet; entire subtree created at Sub-stage 3.
- `MasterAdminHomePage.js` — on-disk at `/app/frontend/src/pages/master_admin/MasterAdminHomePage.js` (E6 CLOSED per Stage A §7.6). Sub-stage 3 extends inline.
- `ComplianceHomePage.js` — Sub-stage 1 landed rider hook; Sub-stage 3 adds `<CounterSignBanner />` at page top (per Stage A §6.1 line 328).
- `frontend/src/components/ui_spec_v1/index.js` — barrel exports; `CounterSignBanner` adds here.
- Retention endpoint `POST /api/compliance/retention_config` — Sub-stage 2 landed loosening-disabled 403; Sub-stage 3 wires the checker-countersign routing hook.

═══════════════════════════════════════════════════════════════════

## §3. Sub-stage 3 deliverables (per Stage A §6 verbatim)

### §3.1 Backend — new modules

| # | Module | Role |
|---|---|---|
| 3.1.1 | `services/checker/__init__.py` | Package marker |
| 3.1.2 | `services/checker/consequence_classes.py` | `consequence_class` constrained-str via Pydantic `Field(pattern=r"^(tightening_unilateral\|dual_control)$")`; NEVER Literal per CK-G5 |
| 3.1.3 | `services/checker/rule_change_request.py` | Transient Pydantic model (NOT frozen; NOT in `contracts/__init__.py`). Fields: `request_id, rule_class, from_value_ref, to_value_ref, initiator_id, initiated_at, state, checker_id?, countersigned_at?, effective_at?, objected_at?, objector_id?` |
| 3.1.4 | `services/checker/state_machine.py` | Dual-control path: `initiate() → pending_counter_sign`; `countersign() → effective` (blocks-until-countersigned per CK-G1). Tightening path (per **Ruling 3, Amendment G**): `initiate() → pending_delay`; `advance_delay() → effective` at delay expiry — **UNCONDITIONALLY** (no objection-blocking); `object() → annotates + escalates`, NEVER halts (recorded via `tightening_objected` ledger row + Owner-escalation marker); **`suspend() → suspended`** — Owner-only distinct action, ONLY mechanism to halt an in-flight tightening. Identical `initiate()` while pending is **idempotent** (same-response, no state churn); post-effect `initiate()` is a new change with its own delay window. No objection memory. |
| 3.1.5 | `services/checker/effective_delay.py` | Reads `consequence_class.v0.json` for rule_class→consequence_class mapping + delay config |
| 3.1.6 | `services/checker/countersign_ledger.py` | `emit_countersign_ledger_row()` — CK-B1 pinned sidecar identities; extends the Sub-stage 2 `data_class`-registry LB gate over new rule-change classes (Ruling 1(ii)) |
| 3.1.7 | `services/checker/tightening_effective_ledger.py` (may be same module as 3.1.6 depending on cohesion) | Emits `tightening_effective`, `tightening_objected`, and **`owner_suspended_tightening`** rows (Ruling 3 adds the suspend row class) |
| 3.1.8 | `services/compliance/consequence_class.v0.json` | Registry: `{ rule_class_map: {retention_windows: dual_control, disclosure_thresholds: dual_control, lawful_basis_registry: dual_control, source_standing_table: tightening_unilateral, ...}, effective_delay_seconds: 3600 }` |
| 3.1.9 | Extend `data_class_registry.v0.json` → `v1.json` (Ruling 4) | Append `countersigned_rule_change`, `tightening_effective`, `tightening_objected`, **`owner_suspended_tightening`** as valid_data_classes (append-only version bump; single registry, Sub-stage 2 pattern) |

### §3.2 Backend — new endpoints

| # | Endpoint | Auth | Body | Behavior |
|---|---|---|---|---|
| 3.2.1 | `POST /api/checker/initiate` | DPO OR admin (role-symmetric) | `{rule_class, from_value_ref, to_value_ref}` | Initiator kicks off request. Returns `{request_id, state, consequence_class}`. Identical `(rule_class, from_value_ref, to_value_ref)` while an existing request is pending: **idempotent** — same-request-id returned, no state churn (Ruling 3). |
| 3.2.2 | `POST /api/checker/countersign/{request_id}` | Second-console role (initiator=DPO → countersigner=admin; initiator=admin → countersigner=DPO) — CK-G4 symmetry | (no body) | Countersign transition. LB gate CK-G1: blocks until countersigned. Returns `{state: effective, effective_at, ledger_row_ref}`. |
| 3.2.3 | `POST /api/checker/object/{request_id}` | Countersigner role (tightening_unilateral only) | `{reason}` | Objection path per **Ruling 3**: annotates the active tightening + escalates to Owner (writes `tightening_objected` ledger row + Owner-escalation marker). **NEVER halts** the tightening; tightening proceeds to effective at delay expiry regardless. Returns `{state, objection_recorded_at, owner_escalated: true}`. |
| 3.2.4 | `GET /api/checker/pending` | Any authenticated user | (query param `role`) | Banner-feed for BOTH consoles. Returns per-role pending items. |
| 3.2.5 | **`POST /api/master_admin/tightening/suspend`** (per **Ruling 3** — Owner-only halt action) | `master_admin` role required (E2 4-code registry — `auth_scope_insufficient` on missing role) | `{request_id, reason}` | Suspends an in-flight tightening (either `pending_delay` or already-elapsed but not yet marked effective). Emits `owner_suspended_tightening` ledger row via Sub-stage 3 emitter. The ONLY mechanism that halts a tightening. Returns `{state: suspended, suspended_at, ledger_row_ref}`. Distinct, ledgered, Owner-only. |

### §3.3 Backend — retention endpoint checker-routing hook

- `POST /api/compliance/retention_config` (Sub-stage 2 landed): loosening writes NOW route through `services/checker/state_machine.initiate(rule_class="retention_windows", ...)`. Instead of 403 refusal, the endpoint returns `202 Accepted` with `{state: "pending_counter_sign", request_id, consequence_class: "dual_control"}`.
- Tightening writes stay unilateral-with-delay: enter `pending_delay` state, become effective after `effective_delay_seconds` elapsed (per **Ruling 3**: unconditionally; only `POST /api/master_admin/tightening/suspend` can halt them).
- E2 gate `test_retention_endpoint_loosening_disabled_pre_checker` RETIRES.
- New gate `test_retention_loosening_write_requires_administration_countersign` LANDS (CK-B3 symmetry).
- **New gate per Ruling 6:** `test_every_retention_write_emits_ledger_row_with_consequence_class` — asserts every retention-config write (loosening OR tightening) emits a `NorthenaLedgerRow_v1` whose `stamp_audit["consequence_class"]` is present and registry-valid per `consequence_class.v0.json`. Checker scope, not B-5b's.

### §3.4 Frontend — new component + page extensions

| # | File | Kind | Role |
|---|---|---|---|
| 3.4.1 | `frontend/src/components/ui_spec_v1/CounterSignBanner.jsx` | New component | Top-of-page banner listing pending items per role. Middle-dot binding copy verbatim. Per **Ruling 2 (Amendment G)**: renders the **capacity role** — the role the countersign endpoint's auth required at the time of transition — as the governance fact. Determinism from endpoint requirement; NOT primary-role, NOT bracket-listed roles, NOT identity's role-order. |
| 3.4.2 | `frontend/src/components/ui_spec_v1/index.js` | Barrel extension | Export `CounterSignBanner`. Single-source enforced by CK-G-BARREL. |
| 3.4.3 | `frontend/src/pages/compliance/ComplianceHomePage.js` | Page extension | Render `<CounterSignBanner role="compliance" />` at page top. |
| 3.4.4 | `frontend/src/pages/master_admin/MasterAdminHomePage.js` | Page extension | Render `<CounterSignBanner role="admin" />` at page top. |
| 3.4.5 | `frontend/src/apiClient.js` | Client shim | `checkerInitiate` + `checkerCountersign` + `checkerObject` + `checkerPending` + **`tighteningSuspend`** (Ruling 3 owner-suspend endpoint) |

### §3.5 Rider — Sub-stage 2 §12 retrofit (BAND B ONLY; see §5)

Not part of Band A. If Owner rules Band B (per Dispatch A outcome path 3), §5 additions land in Sub-stage 3's first commit.

═══════════════════════════════════════════════════════════════════

## §4. Test matrix — BAND A (baseline, no §12 retrofit)

Cell × posture × case enumeration:

### §4.1 Backend Pytest — new gates in `tests/invariants/test_phase_8_seam_3_sub_stage_3.py`

| § | Case class | Cell × posture × case | Cell count |
|---|---|---|---|
| §A | `consequence_class` constrained-str validation | valid value × pattern match × pass; invalid value × pattern match × raises; `Literal["dual_control"...]` grep-negative in `services/checker/*.py` (**CK-G5**) | 3 |
| §B | `consequence_class.v0.json` registry shape + non-empty rule_class_map + values ∈ `{tightening_unilateral, dual_control}` | file load × schema × 3 assertions | 3 |
| §C | `RuleChangeRequest` transient model discipline | shape × validation × pass; NOT in `contracts/__init__.py` × grep × asserted; NOT in mechanical-parity map × asserted | 3 |
| §D | Dual-control state machine (**LB CK-G1**) | `initiate` → `pending_counter_sign`; `countersign` → `effective` + ledger row emitted; between-states = blocked-until-countersigned; `object` at pending_counter_sign = disallowed | 4 |
| §E | Tightening-unilateral state machine (**LB CK-G3**) per **Ruling 3** (Amendment G) — objection annotates but NEVER halts; only owner-suspend halts | `initiate` → `pending_delay`; `advance_delay(now < effective_delay)` = still pending; `advance_delay(now >= effective_delay)` = effective **unconditionally** (even with active objection); `object` at pending_delay = annotates + escalates (does NOT halt) + writes `tightening_objected` row; `object` post-effective = disallowed; identical `initiate` while `pending_delay` = **idempotent** (same request_id returned); post-effect (post-`effective`) re-initiate = **new change** with own delay window; NO objection memory across changes | 8 |
| §E-supp | **Owner-suspend action** (**LB CK-G-SUSPEND**, per **Ruling 3**) — the ONLY halt mechanism | `suspend` on `pending_delay` = state → `suspended` + writes `owner_suspended_tightening` row; `suspend` on `pending_counter_sign` (dual-control) = state → `suspended` + writes row; `suspend` on `effective` = disallowed (already applied); `suspend` on `suspended` = idempotent no-op; `suspend` without `master_admin` role = 403 auth_scope_insufficient (E2 4-code); suspended state is terminal (no auto-transition to effective) | 6 |
| §F | Countersign ledger row (**LB CK-G2** `test_countersign_row_carries_both_identities`) | row emitted + stamp_audit carries `{data_class: "countersigned_rule_change", rule_class, consequence_class, initiator, checker, initiated_at, countersigned_at}` pinned keys | 4 |
| §G | Tightening-effective ledger row | row emitted at delay-expiry; stamp_audit carries `initiator + rule_class + effective_at + data_class: "tightening_effective"` | 3 |
| §H | Objection ledger row (per **Ruling 3**: annotation, never a halt) | row emitted at `object()` on active tightening; stamp_audit carries `objector + owner-escalation-marker + data_class: "tightening_objected"`; asserted that the underlying tightening's `state` remains `pending_delay` (NOT halted) post-objection; asserted `advance_delay` still transitions to `effective` at expiry despite the objection | 4 |
| §H-supp | **Owner-suspend ledger row** (per **Ruling 3**) | row emitted at `suspend()`; stamp_audit carries `{data_class: "owner_suspended_tightening", suspended_by, reason, suspended_at, request_id}` pinned keys; membership in v1 data-class registry | 3 |
| §I | Symmetry gates (**LB CK-G4**) | Compliance-initiated loosening needs Admin countersign; Admin-initiated loosening needs Compliance countersign; same-role countersign = refused | 3 |
| §J | Effective-delay is config-driven | change `consequence_class.v0.json` `effective_delay_seconds`; state machine reads new value; `test_effective_delay_is_config_driven_not_hardcoded` | 2 |
| §K | `POST /api/checker/initiate` endpoint × auth × role symmetry × payload | 5 auth postures × 2 payload variants | 6 |
| §L | `POST /api/checker/countersign/{request_id}` endpoint × auth × role symmetry × state | 5 auth postures × 2 state variants (pending → effective / already-effective → 4xx non-409) | 6 |
| §M | `POST /api/checker/object/{request_id}` endpoint (per **Ruling 3** semantics) | 3 auth postures × 2 state variants (`pending_delay` → objection annotated, tightening still proceeds / non-tightening → 4xx non-409); explicit assertion that the endpoint response body does NOT report `state: halted` or equivalent — instead reports `state: <underlying_state>` + `objection_recorded_at` + `owner_escalated: true` | 5 |
| §M-supp | **`POST /api/master_admin/tightening/suspend` endpoint** (**LB per Ruling 3**) | 4 auth postures (master_admin OK / admin denied / dpo denied / anonymous denied) × 3 target-state variants (`pending_delay` → suspended / `pending_counter_sign` → suspended / `effective` → 4xx non-409 already-applied) + idempotent-suspend re-post | 8 |
| §N | `GET /api/checker/pending` endpoint | 5 auth postures × per-role filtering (2 role variants) | 5 |
| §O | `test_retention_loosening_write_requires_administration_countersign` (CK-B3 symmetry) | POST retention_config × loosening × routes to checker × returns 202 pending_counter_sign | 3 |
| §O-supp | **`test_every_retention_write_emits_ledger_row_with_consequence_class`** (per **Ruling 6**) | POST retention_config × loosening + tightening + setting-from-unset × 3 variants × assert emitted ledger row carries `stamp_audit["consequence_class"]` present and registry-valid per `consequence_class.v0.json` | 4 |
| §P | `test_retention_endpoint_loosening_disabled_pre_checker` RETIRES — retirement note preserved | retirement note × asserted × preserved | 1 |
| §Q | 409 self-audit (E5 full-anti-rule reactivation continues) | Sub-stage 3 diff files × static-scan × zero hits | 1 |
| §R | Sub-stage 3 data-class LB mirror gates (per **Ruling 1(ii)** — the existing Sub-stage 2 LB gate `test_deletion_terminal_row_carries_registry_valid_data_class_in_stamp_audit` EXTENDS over new rule-change classes; parametrised over the v1 registry) | 4 new data classes (`countersigned_rule_change`, `tightening_effective`, `tightening_objected`, `owner_suspended_tightening`) — each ledger row asserts pinned `stamp_audit["data_class"]` + registry-valid; parametrised over 4 event classes + 1 aggregate | 5 |
| §S | Commit-line binding-copy verbatim | serialized response carries verbatim string with `·` U+00B7 middle-dot on countersign | 1 |

**Subtotal backend Pytest cells: 91** (post-Amendment-G re-derivation per Ruling 5). Pre-Amendment-G was 64; delta breakdown: +1 (Ruling 1(ii) — existing Sub-stage 2 LB gate extends over 4 new rule-change classes rather than 3), +22 (Ruling 3 — corrected tightening state machine: +3 in §E for idempotent-initiate/post-effect re-initiate/no-objection-memory, +6 new §E-supp for owner-suspend action, +1 in §H for non-halted-tightening assertion, +3 new §H-supp for owner-suspend ledger row, +1 in §M for response-body assertion, +8 new §M-supp for `POST /api/master_admin/tightening/suspend` endpoint auth × state matrix), +4 (Ruling 6 — new §O-supp `test_every_retention_write_emits_ledger_row_with_consequence_class`).

### §4.2 Frontend Jest — `test_phase_8_seam_3_sub_stage_3_counter_sign_banner.test.js`

| § | Case | Count |
|---|---|---|
| §T | `CounterSignBanner` barrel-single-source (grep-negative on `CounterSignBanner` outside barrel) | 1 |
| §U | Component render × empty state × honest empty text | 1 |
| §V | Component render × populated × middle-dot glyph asserted (mirror of Sub-stage 1 pattern) | 1 |
| §W | Component render × per-role variants (compliance vs admin) | 2 |
| §X | Commit-line binding-copy verbatim assertion | 1 |
| §Y | Barrel-reuse across 2 pages (parametrised) | 2 |

**Subtotal Jest cells: 8.**

### §4.3 Playwright chromium — `e2e/checker_countersign_smoke.spec.ts`

| § | Smoke | Count |
|---|---|---|
| §Z1 | Compliance page renders `<CounterSignBanner />` at page top + pending count visible | 1 |
| §Z2 | Master Admin page renders `<CounterSignBanner />` + pending count visible (cross-console visibility) | 1 |
| §Z3 | `test_counter_sign_banner_renders_middle_dot_glyph_verbatim` (mirror of Sub-stage 1 gate) | 1 |
| §Z4 | Countersign happy path E2E (Compliance initiates → banner updates → Master Admin sees pending → countersigns → both consoles show effective) | 1 |

**Subtotal Playwright cells: 4.**

### §4.4 Band A totals (post-Amendment-G, per Ruling 5)

- **Backend cells:** 91 (pre-Amendment-G: 64; delta +27)
- **Frontend Jest cells:** 8 (unchanged; capacity-role Ruling 2 rendered inside existing per-role variant tests)
- **Playwright cells:** 4 (unchanged; middle-dot glyph strict per §8.6-Point-3 discipline)
- **Total Band A cells post-Amendment-G:** **103** (pre: 76; delta +27)

**BAND B IS VOID.** Ruling 1 REJECTS the +500 LoC sidecar-key retrofit as redundant. `stamp_audit["data_class"]` is the pinned canonical carrier since Sub-stage 2; a parallel `governance_artifact_type` key would duplicate it. No `artifact_type_registry.py`, no `artifacts_types.v0.json`, no backfill migration, no sidecar-key LB gate. Only three items land as integral rider (S3-E4a, per Ruling 1): (i) `artifact_ref` vestigial-by-ruling with `artifact_type="objective_request"` reuse + close-report corrective note (see §11.3 rulings record); (ii) existing data-class LB gate EXTENDS over 4 new rule-change classes (already absorbed into §R above); (iii) NO backfill — Sub-stage 2 rows already carry pinned truth; corrective note in close.

═══════════════════════════════════════════════════════════════════

## §5. §12 registry retrofit surface (BAND B — **RULED AGAINST 2026-07-07 Amendment G, Ruling 1**)

> **RULED AGAINST (Ruling 1, Amendment G, 2026-07-07):** the +500 LoC sidecar-key retrofit proposed in Band B is **REJECTED as redundant**. `stamp_audit["data_class"]` is the pinned canonical governance-event class carrier established at Sub-stage 2; a parallel `governance_artifact_type` key would duplicate it. Band B is VOID.
>
> Retrofit collapses to three items (integral rider S3-E4a, absorbed into §3/§4 above): (i) `artifact_ref` vestigial-by-ruling with `artifact_type="objective_request"` reuse + close-report corrective note; (ii) existing Sub-stage 2 data-class LB gate EXTENDS over 4 new rule-change classes (already in §R); (iii) NO backfill migration — Sub-stage 2 rows already carry pinned truth; corrective note only.
>
> Historical Band B analysis preserved verbatim below per §7.1 α/β preservation pattern. Do NOT consume this section as a live specification.

Applied ONLY if Dispatch A outcome selects path 3 (registry retrofit). [**RULED AGAINST**]

### §5.1 Retrofit deliverables

| # | Item | Kind | LoC est. |
|---|---|---|---|
| 5.1.1 | `services/compliance/artifact_type_registry.py` | New file — loader + `valid_artifact_types()` cache + `emit`-adjacent validation helper | ~60 |
| 5.1.2 | `services/compliance/artifact_types.v0.json` | New registry — enumerated valid artifact-type strings for governance events (initial values: `retention_rule`, `rule_change_request`; append-only) | ~25 |
| 5.1.3 | Sidecar key convention: `stamp_audit["governance_artifact_type"]` | Pinned sidecar key on governance-event ledger rows. Frozen contract `LedgerArtifactRef.artifact_type` remains a Literal (byte-identical); the semantic-honest artifact-type identifier moves into the sidecar. | 0 LoC (convention) |
| 5.1.4 | Emitter updates in `services/compliance/deletion_ledger.py::emit_deletion_ledger_row` | Add pinned `stamp_audit["governance_artifact_type"]` argument + registry validation | ~15 |
| 5.1.5 | Emitter updates in `services/checker/countersign_ledger.py::emit_countersign_ledger_row` + tightening-effective + objection emitters | Add pinned sidecar key for the 3 rule-change event classes | ~20 |
| 5.1.6 | Backfill migration `services/compliance/backfill_governance_artifact_type.py` (one-time run) | Rewrites Sub-stage 2 authorized_deletion rows to add the pinned sidecar key (`governance_artifact_type="retention_rule"`). Runs idempotent — skips rows that already carry the key. | ~50 |
| 5.1.7 | Backfill test asserting post-migration completeness | `test_all_governance_events_carry_governance_artifact_type_post_backfill` | LoC per §6 |
| 5.1.8 | Sub-stage 2 close report §12 correction footer | Rider-pattern append note documenting the retrofit landing | ~5 |

**Retrofit LoC estimate: ~175 (excluding tests).**

### §5.2 Retrofit design principle (E1.γ analog on artifact-type field)

**Owner-anchored precedent:** §7.1.γ.1 sidecar+pinned-key+LB-gate pattern applied to `refusal_family` value that was semantically distinct from the frozen Literal `stage` + `decision` enumeration.

**Sub-stage 3 retrofit applies the same three-move discipline to `artifact_type` semantics:**

1. **Sidecar container** — `stamp_audit` (existing `Optional[Dict]` on `NorthenaLedgerRow_v1`, byte-identical).
2. **Pinned key** — `stamp_audit["governance_artifact_type"]` (new key at Sub-stage 3 landing).
3. **LB wire-shape gate** — `test_governance_ledger_row_carries_registry_valid_artifact_type_in_stamp_audit`. Retirement: never.

**Effect:** frozen contract byte-identical; `LedgerArtifactRef.artifact_type="objective_request"` continues to be used for governance events (pragmatic Literal reuse); but the **honest** artifact-type identifier lives in the sidecar-pinned-key under registry-validation. Aggregates read the sidecar key; contract stays byte-identical.

### §5.3 Retrofit does NOT bump frozen contract

`LedgerArtifactRef.artifact_type` Literal remains `["portfolio_mandate", "objective_request"]`. Governance event rows carry the pragmatic Literal value at the top-level field AND the honest artifact-type at the sidecar. The registry-pattern precedent: two truths coexist — the frozen contract Literal (retained for byte-identity) + the honest registry-backed value (in the sidecar). Consumers wanting semantic honesty read the sidecar; consumers relying on the contract shape read the top-level field.

═══════════════════════════════════════════════════════════════════

## §6. Test matrix — BAND B additive cells (retrofit deltas) [**RULED AGAINST 2026-07-07 Amendment G, Ruling 1**]

> **RULED AGAINST (Ruling 1, Amendment G, 2026-07-07):** Band B is VOID (see §5 above). The 15 additive cells in this section were the retrofit's test roster; they do NOT land at Sub-stage 3. Only the LB data-class gate extension survives, and it is absorbed into §R above (parametrised over 4 new rule-change classes, 5 cells total).
>
> Historical §6 matrix preserved verbatim below per §7.1 α/β preservation pattern. Do NOT consume this section as a live specification.

### §6.1 Additional backend Pytest cells (§AA)

| § | Case class | Cell × posture × case | Cell count |
|---|---|---|---|
| §AA1 | `artifact_types.v0.json` registry shape + non-empty + values are snake_case strings | file load × schema × 2 assertions | 2 |
| §AA2 | `artifact_type_registry.py::valid_artifact_types()` returns registry values | unit × happy × asserted | 1 |
| §AA3 | Emitter validation — `emit_deletion_ledger_row` rejects unknown `governance_artifact_type` | unit × unknown × raises | 1 |
| §AA4 | Emitter validation — `emit_countersign_ledger_row` (+ tightening + objection) rejects unknown `governance_artifact_type` | unit × 3 event classes × unknown × raises | 3 |
| §AA5 | **`test_governance_ledger_row_carries_registry_valid_artifact_type_in_stamp_audit`** — LB wire-shape gate; data-shape invariant scan over all governance-event ledger rows (`reason` starts with any of `authorized_deletion:`, `countersigned_rule_change:`, `tightening_effective:`, `tightening_objected:`). Parametrised: 4 exercise fixtures (one per event class) + 1 aggregate regression | LB gate × 5 cases | 5 |
| §AA6 | Backfill migration — `test_all_governance_events_carry_governance_artifact_type_post_backfill` — asserts every pre-existing Sub-stage 2 authorized_deletion row carries the pinned sidecar key post-migration | migration × completeness × asserted | 1 |
| §AA7 | Backfill idempotency — running the migration twice does not double-write or overwrite existing correct values | migration × idempotent × asserted | 1 |
| §AA8 | Registry-append discipline — extending `artifact_types.vN.json` (v0 → v1) does not break existing consumers (frozen-registry-analog gate) | registry × append-only × asserted | 1 |

**Retrofit backend cells added: 15.**

### §6.2 Frontend / Playwright — no additive cells

Retrofit is backend-only. Frontend surfaces do not read `artifact_type` semantics (they consume ledger rows via aggregate + rider components, all of which key off `stamp_audit["data_class"]`, not `artifact_type`).

### §6.3 Band B totals

- **Backend cells:** 64 + 15 = **79**
- **Frontend Jest cells:** 8 (unchanged)
- **Playwright cells:** 4 (unchanged)
- **Total Band B cells:** **91**

═══════════════════════════════════════════════════════════════════

## §7. Rule 2 anchor bands (post-Amendment-G, per Ruling 5)

### §7.1 Band A (post-Amendment-G re-derivation)

**Per-bucket LoC breakdown (re-derived post-Rulings 1/3/6):**

| Bucket | Estimated LoC | Delta vs. pre-Amendment-G |
|---|---|---|
| Backend impl (7 checker modules ~500L + `consequence_class.v0.json` 40L + `data_class_registry.v0.json` v0→v1 bump ~20L + 5 endpoints inc. owner-suspend + retention hook rewire ~270L + owner-suspend ledger emitter ~40L + state machine correction per Ruling 3 ~30L) | ~900 | +125 (Ruling 3 owner-suspend + state-machine + Ruling 4 registry-bump minor) |
| Backend tests (91 cells × ~22 LoC/cell) | ~2,002 | +592 (Ruling 5 re-derivation: +27 cells × ~22 LoC) |
| Frontend impl (`CounterSignBanner` 90L + 2 page deltas 2×40=80L + `apiClient.js` +30L inc. `tighteningSuspend` shim + `MasterAdminHome` extension 60L + barrel +5L) | ~265 | +5 (Ruling 3 owner-suspend apiClient shim) |
| Jest gates (8 cells × ~28 LoC/cell) | ~225 | unchanged |
| Playwright smokes (4 cells × ~55 LoC/cell across 1 spec) | ~220 | unchanged (corrected from typo "120" in pre-Amendment-G) |
| Sub-stage 3 close report §12 corrective note (Ruling 1(iii)) | ~10 | +10 (new; corrective note only, no backfill) |
| **Band A total (post-Amendment-G)** | **~3,622** | **+832 vs. ~2,790 pre-Amendment-G** |

**Owner-anchored band per Stage A §9 line 562:** `[2000, 2500]`.

**Band A LoC ~3,622 vs. anchor top 2,500 → OVERRUN of ~+1,122 LoC (+45%).** Owner-anchored disclosure per **Ruling 5**: *"restate the band at dispatch per the Standing Correction, land one atomic commit, overrun disclosed if any. No split, no band-widening."*

The overrun is composed as:
- +290 LoC vs. anchor top: the same dev-autonomous re-enumeration surprise that pre-Amendment-G accounted for (E2 gate retirement + retention hook rewire + data-class LB mirror gates + auth-posture matrix expansion, matrix-enumerated per Standing Correction).
- +592 LoC: Ruling 3 test cells for the corrected tightening state machine (idempotent initiate + post-effect re-initiate + no-objection-memory + owner-suspend endpoint × auth × state matrix + owner-suspend ledger row).
- +125 LoC: Ruling 3 impl for `POST /api/master_admin/tightening/suspend` endpoint + owner-suspend ledger emitter + state-machine object()-annotates-not-halts semantics.
- +88 LoC: Ruling 6 gate + retention hook consequence-class stamp_audit key emission.
- +10 LoC: Ruling 1(iii) close-report corrective note.
- +17 LoC: Ruling 4 minor (`data_class_registry.v0.json` → `v1.json` bump + 4 new class entries).

**Per Ruling 5: no split, no band-widening. Overrun disclosed here.** Sub-stage 3 lands as ONE atomic commit; the close report §5 (Rule-2 accounting) restates this overrun with honest cost attribution.

### §7.2 Band B (baseline + retrofit) — **RULED AGAINST 2026-07-07 Amendment G, Ruling 1**

> **RULED AGAINST (Ruling 1, Amendment G, 2026-07-07):** Band B is VOID. The +500 LoC retrofit is REJECTED as redundant. `stamp_audit["data_class"]` is the pinned canonical carrier since Sub-stage 2. Historical Band B breakdown preserved below verbatim per §7.1 α/β preservation pattern. Do NOT consume as a live specification.

### §7.3 Both bands — summary (post-Amendment-G)

| Band | Cells | LoC | vs. Anchor [2000, 2500] |
|---|---|---|---|
| A (post-Amendment-G, Rulings 1/3/6 applied) | 103 | ~3,622 | +1,122 (+45%) — dev-autonomous, DISCLOSED per Ruling 5, no split, no band-widening |
| B (baseline + §12 retrofit) — **RULED AGAINST** | 91 (historical) | ~3,290 (historical) | VOID per Ruling 1 |
| B − A (retrofit-only delta) — **RULED AGAINST** | +15 cells (historical) | +500 LoC (historical) | VOID per Ruling 1 |

═══════════════════════════════════════════════════════════════════

## §8. Escalations to Owner (S3-E1 through S3-E5)

### §8.1 S3-E1 — Frozen-contract adjacency: `CounterSignBanner` binding-copy semantics [**RULED by Ruling 2, Amendment G, 2026-07-07**]

> **RULED (Ruling 2, Amendment G, 2026-07-07 — Owner verbatim):**
> *"(d): render the capacity role. The endpoint's required role is deterministic and is the governance fact. (a) can misreport, (b) muddies capacity, (c) breaks single-person operation. Banner renders the role the countersign endpoint required."*
>
> Applied: `CounterSignBanner` renders the **capacity role** — the role the countersign endpoint's auth required at the time of transition — as the governance fact. Determinism from endpoint requirement, not identity's primary/bracket-listed roles. Historical §8.1 a/b/c menu preserved verbatim below per §7.1 α/β preservation pattern. Do NOT consume the (a) recommendation.

**Class:** owner-value contact.

**Question:** the commit-line binding copy per CK-U1 (per Stage A §6.1 line 330) reads: *"Signed by {initiator} · counter-signed by {checker} · recorded with both identities."* The middle-dot glyph U+00B7 is E7-strict. **What if the countersigner has both roles (dpo AND admin) — how does the banner render?** Stage A §6 does not enumerate the two-role case. Options:

- (a) Display the countersigner's PRIMARY role (per identity's roles order). [**RULED AGAINST**]
- (b) Display all roles bracket-listed. [**RULED AGAINST**]
- (c) Refuse the countersign entirely (require single-role countersigners). [**RULED AGAINST**]
- (d) Display the CAPACITY role — the role the countersign endpoint's auth required at the time of transition. [**RULED IN per Ruling 2**]

**Historical pre-Amendment-G recommendation (RULED AGAINST):** (a) — primary role.

### §8.2 S3-E2 — Tightening state machine semantics [**RULED by Ruling 3, Amendment G, 2026-07-07**]

> **RULED (Ruling 3, Amendment G, 2026-07-07 — Owner verbatim):**
> *"State machine corrected before dispatch; the a/b/c menu is void. As proposed, `object()` halts a tightening — an Administration veto over protection-tightening, prohibited by B5b-R3/CK-B2. Correct semantics: **objection annotates and escalates; it never blocks.** Tightening proceeds to effective at delay expiry unless the owner suspends — **owner-suspend is a distinct, ledgered action.** The asked question dissolves: identical `initiate()` while pending is idempotent; post-effect re-initiates are new changes with their own windows; no objection memory."*
>
> **Applied disposition (binding, non-optional):**
> - `object()` on a `pending_delay` tightening: **annotates** the objection + **escalates** to Owner. Writes a `tightening_objected` ledger row + Owner-escalation marker. Does **NOT** halt the tightening. `advance_delay()` continues to transition to `effective` at expiry regardless.
> - `object()` at `pending_counter_sign` (dual-control): disallowed by shape — dual-control tightening isn't the target of objections; only tightening_unilateral tightenings can be objected.
> - `object()` post-`effective`: disallowed (tightening already applied).
> - **`suspend()`** — new action, Owner-only (`master_admin` role via E2 4-code registry). The ONLY mechanism that halts a tightening. Emits `owner_suspended_tightening` ledger row. Distinct, ledgered action.
> - Identical `initiate()` while a matching request is `pending_delay` or `pending_counter_sign`: **idempotent** (same-response, no state churn, same request_id returned).
> - Post-`effective` re-`initiate()` on the same `(rule_class, from_value_ref, to_value_ref)`: **new change** with its own delay window (no memory of prior objections).
> - **No objection memory** — objections annotate the specific tightening they were raised against; they never persist forward.
>
> Historical §8.2 a/b/c menu **PRESERVED VERBATIM BELOW BUT VOID** per §7.1 α/β preservation pattern. Do NOT consume as a live specification.

**Class:** governance-semantic contact.

**Question (RULED VOID):** at `object()` on a `pending_delay` (tightening_unilateral), the request transitions to `objected + owner_escalation`. **Does the objected request block subsequent identical initiate() attempts?** Stage A §6 is silent.

Options (RULED VOID — the state machine is corrected before dispatch; the a/b/c menu is void):
- (a) Objection is one-time — subsequent initiate() with same `(rule_class, from_value_ref, to_value_ref)` proceeds normally (no memory). [**RULED VOID**]
- (b) Objection sticks — subsequent identical initiate() refused until Owner escalation resolves. [**RULED VOID**]
- (c) Cooldown window — subsequent identical initiate() refused within N hours of objection. [**RULED VOID**]

**Historical pre-Amendment-G recommendation (RULED VOID):** (b) — objection sticks pending owner-escalation resolution. Aligns with the "objection triggers owner-escalation" intent.

### §8.3 S3-E3 — `data_class_registry.v0.json` extension mechanism [**RULED by Ruling 4, Amendment G, 2026-07-07**]

> **RULED (Ruling 4, Amendment G, 2026-07-07 — Owner verbatim):**
> *"(a). `data_class_registry` v0→v1, rule-change classes appended. Single registry, Sub-stage 2 pattern."*
>
> Applied: v0→v1 bump of `data_class_registry.v0.json` → `data_class_registry.v1.json`. Append `countersigned_rule_change`, `tightening_effective`, `tightening_objected`, `owner_suspended_tightening`. Single registry, Sub-stage 2 pattern preserved.

**Class:** governance-semantic contact.

**Question:** Stage A §7.1.γ says event classes extend the SAME registry (or a scope-parallel registry per data-class family) as append-only additions. **Does Sub-stage 3 append to `data_class_registry.v0.json` in-place (rename to v1?) or land a new file `rule_change_events.v0.json`?**

Options:
- (a) Append to `data_class_registry.vN.json`, bump v0 → v1 (single-registry per E1.γ discretion "single unified registry vs per-purpose registries settled at those dispatches"). [**RULED IN per Ruling 4**]
- (b) Land per-purpose registry `rule_change_events.v0.json` (scope-parallel). [**RULED AGAINST**]

**Pre-Amendment-G recommendation matched the ruling:** (a) — bump `data_class_registry.v0.json` to v1.

### §8.4 S3-E4 — Retrofit landing pattern (§12) [**RULED by Ruling 1, Amendment G, 2026-07-07**]

> **RULED (Ruling 1, Amendment G, 2026-07-07 — Owner verbatim):**
> *"Path 3 confirmed; the +500 LoC sidecar retrofit is REJECTED as redundant. The truth already exists: `stamp_audit["data_class"]` is pinned, registry-backed, LB-gated since Sub-stage 2. A `governance_artifact_type` key would duplicate it. Actual retrofit:*
> - *(i) If `artifact_ref` is Optional on the ledger row, governance-event rows emit `None` going forward. If required, the placeholder stands vestigial-by-ruling — registry note + close state that on governance-event rows `artifact_type` is non-authoritative and `data_class` is the event class.*
> - *(ii) The existing data-class LB gate extends over the new rule-change classes.*
> - *(iii) No backfill migration — Sub-stage 2 rows already carry the pinned truth; corrective note in the close.*
>
> *Lands as integral rider (S3-E4a). Band B collapses."*
>
> **`artifact_ref` fork applied (per §11.3 rulings record):** `NorthenaLedgerRow_v1.artifact_ref` is **REQUIRED** (verbatim from `/app/backend/contracts/northena_ledger_v1.py:60`). Required-branch applies: placeholder stands **vestigial-by-ruling** — governance-event rows reuse Sub-stage 2's `artifact_type="objective_request"` pragmatic-choice pattern (see `backend/routers/compliance.py:305-314`). Sub-stage 3 close report §12 records: on governance-event rows `artifact_type` is non-authoritative; `data_class` is the event class.
>
> Retrofit collapses to three items:
> - (i) `artifact_ref` vestigial-by-ruling; `artifact_type="objective_request"` Literal reuse; close-report corrective note.
> - (ii) Existing data-class LB gate `test_deletion_terminal_row_carries_registry_valid_data_class_in_stamp_audit` (Sub-stage 2 LB) is **parametrised over the v1 registry** — automatically covers new rule-change classes (see §R above; +1 cell).
> - (iii) **NO backfill migration.** Sub-stage 2 rows already carry pinned truth (`stamp_audit["data_class"]="authorized_deletion"`). No script, no idempotency gate, no completeness gate. Corrective note in close only.
>
> Historical §8.4 a/b menu preserved verbatim below per §7.1 α/β preservation pattern. Do NOT consume as a live specification.

**Class:** governance-semantic contact — applies ONLY if Dispatch A ruling selects path 3. **[Dispatch A ruled: path 3 CONFIRMED, but retrofit collapsed per Ruling 1.]**

**Question (RULED VOID at menu level):** the §12 retrofit lands (a) at Sub-stage 3's first commit as an integral rider, or (b) as a separate pass BEFORE Sub-stage 3 execution.

Options:
- (a) **Integral rider** — retrofit lands in Sub-stage 3's atomic first commit alongside checker impl + tests + frontend. First-commit gating includes retrofit. [**RULED IN as S3-E4a per Ruling 1 (with retrofit collapsed)**]
- (b) **Pre-execution pass** — Sub-stage 3 execution paused; retrofit lands as a dedicated commit first. Two atomic commits. [**RULED AGAINST**]

**Historical pre-Amendment-G recommendation matched the sequencing ruling:** (a) — integral rider.

### §8.5 S3-E5 — Split-proposal candidacy [**RULED by Ruling 5, Amendment G, 2026-07-07**]

> **RULED (Ruling 5, Amendment G, 2026-07-07 — Owner verbatim):**
> *"Re-derive, then (a). Rulings 1 and 3 change the cell count; re-derive the matrix, restate the band at dispatch per the Standing Correction, land one atomic commit, overrun disclosed if any. **No split, no band-widening.**"*
>
> Applied: matrix re-derived (§4 above — 91 backend + 8 Jest + 4 Playwright = 103 cells total); band restated (§7.1 above — ~3,622 LoC vs. anchor top 2,500 → +45% overrun DISCLOSED); one atomic commit; no split; no band-widening. Ruling 6 adds `test_every_retention_write_emits_ledger_row_with_consequence_class` to the roster (§O-supp above).

**Class:** LoC-band overrun (§9 below elaborates).

**Question:** Band A at 2,790 LoC (pre-Amendment-G) exceeds anchor top by 12%; Band B at 3,290 LoC exceeds by 32%. **Does Sub-stage 3 split into two commits (checker impl + tests atomically as commit 1; frontend + Playwright + close as commit 2), or land as one atomic commit?**

Options:
- (a) One atomic commit — first-commit gating discipline preserved; LoC surprise reported in close (dev-autonomous per §7). [**RULED IN per Ruling 5**]
- (b) Two atomic commits — Sub-stage 3.1 backend + tests; Sub-stage 3.2 frontend + Playwright + close. Preserves anchor-band closer to top. [**RULED AGAINST**]
- (c) Widen the anchor band to `[2000, 3000]` for Sub-stage 3 explicitly. [**RULED AGAINST**]

**Historical pre-Amendment-G recommendation matched the ruling:** (a) — one atomic commit with LoC surprise disclosed.

### §8.6 S3-E6 — Retention-write consequence-class emission [**RULED by Ruling 6, Amendment G, 2026-07-07**]

> **RULED (Ruling 6, Amendment G, 2026-07-07 — Owner verbatim):**
> *"Gap confirmed, closes at Sub-stage 3 by named gate. Retention-config writes route through the checker; `test_every_retention_write_emits_ledger_row_with_consequence_class` joins the roster. Checker scope, not B-5b's."*
>
> Applied: retention endpoint `POST /api/compliance/retention_config` — every write (loosening OR tightening OR setting-from-unset) emits a `NorthenaLedgerRow_v1` whose `stamp_audit["consequence_class"]` is present and registry-valid per `consequence_class.v0.json`. Gate `test_every_retention_write_emits_ledger_row_with_consequence_class` lands at §O-supp (4 cells).

═══════════════════════════════════════════════════════════════════

## §9. Split-proposal candidacy assessment (post-Amendment-G, per Ruling 5)

**Owner ruling (Ruling 5, Amendment G, 2026-07-07 — verbatim):** *"No split, no band-widening."* Sub-stage 3 lands as ONE atomic commit with overrun disclosed.

**Prior sub-stage sizing:**

| Sub-stage | Cells | LoC | Split status |
|---|---|---|---|
| Sub-stage 1 | 22 Pytest + 6 Jest + 2 Playwright = 30 | 1,160 | Single-commit atomic |
| Sub-stage 2 | 35 Pytest + 0 Jest + 0 Playwright = 35 | 1,703 | Single-commit atomic |
| Sub-stage 3 Band A (post-Amendment-G) | 91 Pytest + 8 Jest + 4 Playwright = 103 | ~3,622 | Single-commit atomic (Ruling 5 — no split, no band-widening) |
| Sub-stage 3 Band B — **RULED AGAINST** | 91 (historical) | ~3,290 (historical) | VOID per Ruling 1 |

**Historical §9 recommendation (retained for context):** pre-Amendment-G suggested one atomic commit with LoC surprise disclosed; Ruling 5 ratified (a) and rejected the split/widen alternatives explicitly.

═══════════════════════════════════════════════════════════════════

## §10. Ready-to-dispatch posture (post-Amendment-G)

**Band A (post-Amendment-G, Rulings 1–7 pre-carried) posture:**
- All Stage A §6 + Amendment G §3 deliverables enumerated; matrix-enumerated cell roster (103 cells: 91 Pytest + 8 Jest + 4 Playwright) documented.
- All 5 pre-Amendment-G escalations (S3-E1..E5) RULED (per Rulings 2/3/4/1/5 respectively); new S3-E6 (Ruling 6) RULED and gate `test_every_retention_write_emits_ledger_row_with_consequence_class` landed.
- §12 retrofit collapsed per Ruling 1 to (i)+(ii)+(iii); integral rider (S3-E4a).
- Frozen contract parity 26 preserved (no touches). `LedgerArtifactRef.artifact_type` Literal reused via vestigial-by-ruling.
- E2 gate `test_retention_endpoint_loosening_disabled_pre_checker` RETIRES at Sub-stage 3 close; CK-B3 symmetry gate `test_retention_loosening_write_requires_administration_countersign` lands.
- Data-class registry `data_class_registry.v0.json` → `v1.json` bump (Ruling 4): append 4 new rule-change classes (`countersigned_rule_change`, `tightening_effective`, `tightening_objected`, `owner_suspended_tightening`).
- New endpoint `POST /api/master_admin/tightening/suspend` (Ruling 3): Owner-only halt action; only mechanism to halt an in-flight tightening.
- Standing 409 anti-rule (elevated §8.2 of rulings record): full-anti-rule reactivates at Sub-stage 3; static scan at close.
- Middle-dot glyph binding preserved (Jest structural + Playwright chromium byte-strict).
- CounterSignBanner renders capacity role (Ruling 2).
- Sub-stage 2 final acceptance recorded (Ruling 7): close `c17b578b…` FINAL.
- One atomic commit (Ruling 5); overrun ~+45% vs. anchor `[2000, 2500]` top DISCLOSED honestly in Sub-stage 3 close §5 (Rule-2 accounting) with attribution breakdown.
- **BUILD UN-PAUSES ON AMENDMENT G LANDING WITH CONFIRMED SHAs.**

**Band B posture — RULED AGAINST (Ruling 1, Amendment G).** Section retained for historical context; do NOT consume as a live posture.

═══════════════════════════════════════════════════════════════════

*End of Sub-stage 3 Stage A proposal (post-Amendment-G). All seven Owner rulings pre-carried. Sub-stage 3 execution unpauses on Amendment G landing with confirmed SHAs.*
