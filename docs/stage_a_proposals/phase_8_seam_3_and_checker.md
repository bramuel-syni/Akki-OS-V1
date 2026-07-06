# Phase 8 Seam 3 + §8 Checker — Stage A Proposal (2026-07-06)

**DESIGN-ONLY. No code touches. Matrix-enumerated per B-4-close-acceptance
standing correction. Standing Rule v3 — on-disk canonical + SHA.**

**Dispatch citation:** Owner ruling, Phase 8 Stage B-5a close acceptance +
Seam 3 + §8 checker Stage A dispatch, 2026-07-06.

**Scope classification (binding):** Governance-semantic surface — NOT a
defaults phase. Escalation cap ORIGINAL wording: defaults everywhere
except frozen-contract, owner-value, or governance-semantic contact.

═══════════════════════════════════════════════════════════════════

## §0. Pre-Stage-A one-line resolved

**Line owed at dispatch (third un-ledgered family, file:line evidence):**
The "third family" (`late_refusals`) is **NOT a distinct family** — it
is a TIMING overlay on the same emission sites, per the classifier's
own doctrine at `services/compliance/refusal_family_classifier.py:42-49`
(verbatim: *"the current ledger row shape does not carry a distinct
emission-context marker for async-worker-fired refusals vs
sync-dispatch-fired refusals ... 'late refusals' is a TIMING context
that overlays the four families below, not a distinct family in
itself"*). Honest un-ledgered surface is **2 distinct families × 2
emission-time contexts = 4 un-ledgered emission sites**:

1. `admission_refusals` @ async-worker `async_worker.py:129-131`
   (via `transition_to_refused` → `async_state.py:141-175` no ledger).
2. `composition_below_floor` @ sync `service.py:187-192` (raise without
   ledger).
3. `composition_below_floor` @ sync `composed_conclusion.py:272-273`
   (raise without ledger).
4. `composition_below_floor` @ async-worker `async_worker.py:97-108`
   (via `transition_to_refused` → same ledger gap as #1).

The B-5a close report's "3 families ❌" phrasing conflated the timing
overlay with a family; retracted honestly here and replaced with the
2-families × 2-contexts precise surface. Stage B roster for sub-stage
1 below instruments exactly these 4 sites.

═══════════════════════════════════════════════════════════════════

## §1. Substrate reads (BCR v1.4 verbatim anchors)

### §1.1 §3.5 Seam 3 — authorized deletion path (BCR v1.4:184-202)

- **S3-R1** authorized_deletion path lands: retention configuration
  surface; deletion executes only against a set retention rule; every
  deletion event is itself ledgered (stamp-audited) — deletion is a
  governed act, not an erasure of governance.
- **S3-R2** standing invariant re-scopes from `no_deletion_path` to
  `no_unauthorized_deletion_path`, gate suite updated in the same
  commit.
- **S3-R3** held-classes enumerated and separately addressable:
  `ledger_rows`, `wizard_transcript`, `delivered_artifact`. DPO may set
  one window or split per class. Until set, holds indefinitely
  (honest default; already surfaced at B-5a §4.3 Retention & rights).

**Technical annex verbatim:**
- `retention.v{N}.json` shape: `{ held_classes: { ledger_rows: {window_days: int|null}, wizard_transcript: {window_days: int|null}, delivered_artifact: {window_days: int|null} } }`, `null` = indefinite.
- Deletion event = `NorthenaLedgerRow_v1` with `stamp_audit: { data_class: authorized_deletion, held_class, keys_deleted: int, retention_rule_ref: retention.v{N}, actor }`.
- Invariant re-scope gate: `test_no_unauthorized_deletion_path` — AST
  gate; delete call sites exist only in
  `services/retention/authorized_deletion.py`.

### §1.2 §3.11 Consequence-class checker (BCR v1.4:254-276)

- **CK-I1** No new frozen contract. `consequence_class` is
  **constrained-str** `{ tightening_unilateral | dual_control }` via the
  established versioned-registry pattern — **NEVER a Literal**.
- **CK-B1** dual_control path → `pending_counter_sign` state; effect
  ONLY on second console's signature; both identities + both
  timestamps in ONE `NorthenaLedgerRow_v1` (`stamp_audit: {data_class: countersigned_rule_change, initiator, checker, consequence_class}`).
- **CK-B2** tightening_unilateral path → effective after
  `[config: effective_delay]`; recorded-objection path escalates to
  owner; objection itself ledgered. Delay is config, not code.
- **CK-B3** symmetry: Compliance-loosening ↔ Administration
  countersign; Administration-loosening (e.g. retention-taxonomy
  change) ↔ Compliance countersign. Neither console senior.
- **CK-H1** while one person holds both roles, dual-control is
  ceremony; seam built now because cheap now, expensive to retrofit.
  Gate proves mechanism, not staffing.
- **CK-U1** pending items on BOTH consoles' banners; counter-signing
  console sees full plain-language consequence statement before
  signing. Commit-line binding copy verbatim:
  *"Signed by {initiator} - counter-signed by {checker} - recorded with both identities."*
- **CK-G1..G5** enumerated:
  * CK-G1 `test_dual_control_blocks_until_countersign`
  * CK-G2 `test_countersign_row_carries_both_identities`
  * CK-G3 `test_tightening_effects_after_delay_with_objection_path`
  * CK-G4 `test_symmetry_admin_loosening_needs_compliance_countersign`
  * CK-G5 `test_consequence_class_is_registry_not_literal`

**Transient model (NOT frozen contract):**
```
rule_change_request { request_id, rule_class, from_value_ref, to_value_ref,
                      consequence_class: tightening_unilateral | dual_control,
                      initiator_id, initiated_at,
                      state: pending_counter_sign | pending_delay | effective | objected,
                      effective_at?: str }
```

Config: `consequence_class.v{N}.json` maps `rule_class → class`;
`effective_delay` in same versioned config.

### §1.3 Coverage-marker first-commit rider (Owner ruling, this dispatch)

Owner verbatim binding-copy pattern:
> *"Counts {families} since system start; {families} since {date} — earlier events in those families were not recorded."*

Rendered permanent-surface on v2.1 §4.1 refusals card. Owner rationale:
*"it's how the aggregate stays honest about its own history forever,
since append-only doctrine forbids fabricating historical rows."*

**Named gate first-commit:** `test_refusals_card_states_coverage_by_family`.

Coverage-marker read exposes per-family since-dates via backend surface;
frontend renders binding-copy verbatim with `{families}` sets composed
dynamically from the backend read and `{date}` = Seam 3 wire-up date.

═══════════════════════════════════════════════════════════════════

## §2. Existing tree reads (confirming no doubles)

- `contracts/northena_ledger_v1.py` (contract 19) — `stamp_audit: Optional[Dict]` present; accommodates `data_class="authorized_deletion"` + `data_class="countersigned_rule_change"` sidecar disambiguation **without contract mutation**. `stage: Literal["admit","gate","converge"]` + `decision` Literal — NOT extended to accommodate deletion or rule-change semantics natively. **See §7 Escalation E1.**
- `services/compliance/held_class_registry.py::HELD_CLASSES` (from B-5a) — single-source enumeration `("ledger_rows", "wizard_transcript", "delivered_artifact")`. Seam 3 CONSUMES; does not redefine.
- `services/compliance/retention_config.py` (from B-5a) — READ service. Seam 3 adds WRITE endpoint using same shape; response model `RetentionConfigResponse` (UNFROZEN, from B-5a) already carries all 3 held-class fields.
- `services/compliance/refusal_family_classifier.py` (from B-5a) — deterministic classifier. Seam 3 REUSES for coverage-marker read; does not modify.
- `services/compliance/refusals_aggregate.py` (from B-5a) — aggregate service. Seam 3 extends by adding coverage-marker exposure.
- `services/service_1/async_state.py:238::emit_ledger_terminate_refused` — DEAD STUB today (zero production callers). See §4.4 module-placement disposition.
- Existing `stamp_audit`-disambiguation precedent: Phase 6 Stage B quote-mint instrumentation writes to `stage="converge"` with `stamp_audit={data_class: <domain>}`. Precedent applies. **See §7 Escalation E1.**

═══════════════════════════════════════════════════════════════════

## §3. Split proposal — 3 sub-stages (matrix-enumerated evidence)

Owner ruled: *"Sizing per cell counts; split proposal if the band demands."*
Total cell count across (a) + (b) + (c) + coverage marker: **~129 cells**.
At B-5a's ~56 LoC/cell effective anchor (2805 raw / ~50 collected cells)
× a modest 1.1× complexity multiplier (state machine + cross-console
banner surfaces), a single dispatch derives ~7100 raw LoC, **~2.4× the
empirical ceiling ~[2500, 3000] LoC** from B-5a's razor-thin close.
**SPLIT IS REQUIRED.**

### §3.1 Sub-stage split ordering + justification

| Order | Sub-stage | Cells | LoC band | Justification |
|---|---|---|---|---|
| 1 | (b) Refusal-family ledger wire-up + coverage marker | 31 | [1400, 1800] | Closes B-5a §V.4 governance-bites debt fastest; pure addition (no invariant re-scope); Owner-ruled first-commit rider (coverage marker) requires it lands with the wire-up. Zero frozen-contract touches. Zero governance-semantic escalation needed. |
| 2 | (a) Authorized-deletion path | 54 | [2500, 2900] | Introduces deletion mechanism + invariant re-scope (S3-R2); requires §7 Escalation E1 resolution first. Once resolved, retention writes + deletion executor land together. |
| 3 | (c) §8 consequence-class checker | 44 | [2000, 2500] | Reuses ledger emission patterns from sub-stages 1 & 2 + benefits from stable retention config surface before layering rule-change mechanics on top. Same §7 Escalation E1 resolution reused. |

**Cell-count evidence:** (b)=31 << (c)=44 < (a)=54 by cell count; but
(a) & (c) BOTH require Escalation E1 resolution before Stage B dispatch —
hence (b) first (no escalation) → (a) second (with resolution) →
(c) third (leverages both).

**Cumulative frozen-contract count across all 3 sub-stages:**
- If E1 disposed as stamp_audit-only (option E1.α below): **26 (unchanged).**
- If E1 disposed as NorthenaLedgerRow_v2 (option E1.β below): **27 at
  sub-stage 2 close; unchanged thereafter.**

═══════════════════════════════════════════════════════════════════

## §4. Sub-stage 1 — (b) Refusal-family ledger wire-up + coverage marker

### §4.1 Deliverables

**Backend (new):**
- `services/northena/refusal_ledger.py` — canonical single-source
  `emit_refusal_ledger_row(run_id, trace_id, family, reason, actor, at, extra_stamp_audit=None)` function. Mirrors B-3 `record_wizard_freeze` shape (declarative + idempotent-by-(run_id, trace_id, stage, decision, reason)). Emits `NorthenaLedgerRow_v1` with `stage="admit" | "converge"` per family context + `decision="refused"` + stamp_audit sidecar carrying `{data_class: "governed_refusal", family, source: sync|async}`.
- `services/compliance/coverage_marker.py` — reads per-family
  since-dates from `refusal_family_since_dates.v0.json` config + composes coverage-marker payload for §4.1 refusals card. Two sets: `since_system_start` (families ledgered since G5a) + `since_seam_3_date` (families ledgered since seam-3 wire-up). Response model UNFROZEN.
- `refusal_family_since_dates.v0.json` — versioned config carrying
  `{ system_start_families: [...], seam_3_landing_families: [...], seam_3_landing_date: "YYYY-MM-DD" }`.

**Backend (modified — 4 emission sites):**
- `services/service_1/async_worker.py:97-108` — instrument
  ComposedService1Refusal handler with `emit_refusal_ledger_row(family="composition_below_floor", source="async")` **before** `transition_to_refused` call.
- `services/service_1/async_worker.py:129-131` — instrument
  AdmissionRefusal_v0 handler with `emit_refusal_ledger_row(family="admission_refusals", source="async")` **before** `transition_to_refused` call.
- `services/service_1/service.py:187-192` — instrument
  `Service1Refusal("composition_below_floor")` raise site with `emit_refusal_ledger_row(family="composition_below_floor", source="sync")` **before** raise.
- `services/service_1/composed_conclusion.py:272-273` — instrument same
  pattern.

**Backend (dead-stub migration):**
- `services/service_1/async_state.py:238::emit_ledger_terminate_refused` — module docstring note added; body kept byte-identical (BC) with `# MIGRATED: canonical single-source is services/northena/refusal_ledger.py::emit_refusal_ledger_row`. Callable stays dead (zero callers pre + post).

**Backend (new endpoint):**
- `GET /api/compliance/refusals_coverage` — reads coverage marker. Auth: same as existing `/api/compliance/refusals` (any authenticated role; anonymous 401).

**Frontend (modified — v2.1 §4.1 refusals card):**
- `frontend/src/pages/compliance/ComplianceHomePage.js` — extend refusals card to render coverage marker via new `RefusalsCoverageMarker.jsx` component (added to `ui_spec_v1/index.js` barrel). Binding-copy verbatim from Owner pattern; `{families}` sets composed dynamically from `/api/compliance/refusals_coverage` GET; `{date}` = `seam_3_landing_date` from response.

**Test matrix (sub-stage 1):**

| Cell class | Backend/Frontend | Cases | Count |
|---|---|---|---|
| `emit_refusal_ledger_row` shape gate | Backend | shape + stamp_audit-tag + idempotency-by-key | 3 |
| Sync-path composition_below_floor wire-up | Backend | service.py:187 + composed_conclusion.py:272 = 2 sites × (ledger-row-written + row-classifier-family-correct) = 2 postures | 4 |
| Async-path composition_below_floor wire-up | Backend | async_worker.py:97 × 2 postures | 2 |
| Async-path admission_refusals wire-up | Backend | async_worker.py:129 × 2 postures | 2 |
| Sync-path admission_refusals regression | Backend | service.py:150-155 still ledgers; no double-emit | 2 |
| Idempotency gates | Backend | 4 sites × repeat-emission-same-key = same row | 4 |
| Post-wire-up refusals-aggregate re-verification | Backend | 4 families × counts-nonzero-when-emitted | 4 |
| Coverage-marker read shape | Backend | 2 date-classes (system-start × N families, seam-3 × M families) + dynamic composition | 4 |
| `GET /api/compliance/refusals_coverage` × auth | Backend | 5 postures × 200/401 = 5 cells | 5 |
| Frontend Jest `test_refusals_card_states_coverage_by_family` | Frontend Jest | verbatim binding-copy + dynamic {families}/{date} composition + auth-denied fallback | 3 |
| `RefusalsCoverageMarker` barrel-reuse | Frontend Jest | parametrised over pages consuming it (1) + import-source single-source | 2 |
| Playwright chromium smokes | Frontend e2e | §4.1 Home renders coverage marker + families sets non-empty + date literal present = 3 assertions in 1 smoke | 1 spec (3 assertions) |
| **Sub-total** | | | **~35 cells** |

**Rule 2 estimated band (sub-stage 1):** [1400, 1800] LoC.
`snapshot_lloc_in_band = no` (no frozen contract touches; no snapshot changes).

**Per-bucket LoC breakdown (sub-stage 1):**

| Bucket | Estimated LoC |
|---|---|
| Backend impl (refusal_ledger.py 90L + coverage_marker.py 80L + json config 25L + 4 site instrumentations 4×30=120L + endpoint 50L) | ~365 |
| Backend tests (35 backend cells × ~22 LoC/cell) | ~770 |
| Frontend impl (RefusalsCoverageMarker.jsx 90L + apiClient.js +15L + Home page delta +40L) | ~145 |
| Jest gates (5 cells × ~30 LoC/cell) | ~150 |
| Playwright smoke (1 spec × 3 assertions) | ~55 |
| **Total** | **~1485** |

Falls at ~35% into anchored band [1400, 1800]. Within band.

═══════════════════════════════════════════════════════════════════

## §5. Sub-stage 2 — (a) Authorized-deletion path

### §5.1 Deliverables (pending §7 Escalation E1 resolution)

**Backend (new):**
- `services/retention/authorized_deletion.py` — SINGLE-SOURCE-OF-DELETION module. Contains the ONLY `db.<collection>.delete_one/delete_many/drop` call sites in the extractor tree. Function: `execute_authorized_deletion(held_class, retention_rule, actor) -> DeletionResult`.
- `services/compliance/retention_config_writes.py` — retention-config write service. Loads current config (or defaults to indefinite), validates DPO write payload, persists as `retention.vN.json` (versioned; append-only version bumps).
- `retention.v0.json` — initial config carrying all-null windows (honest indefinite default). Landing at close means "retention config surface is now writable" but the values remain null until DPO writes.

**Backend (new endpoint):**
- `POST /api/compliance/retention_config` — write half. Auth: DPO role required (Amendment 1 pattern). Body: partial config (any subset of 3 held-classes' window_days). Response: new `retention.vN+1.json` version + ledger row emitted.
- `POST /api/compliance/authorized_deletion` — deletion executor. Auth: DPO role. Body: `{held_class, keys_selector}`. Behavior: LOOKUP retention rule for held_class; if `window_days is null` → 422 refusal `no_retention_rule_set`; else if selector matches expired-window keys → `execute_authorized_deletion(...)` + emit ledger row via `emit_refusal_ledger_row`-adjacent helper `emit_deletion_ledger_row`.

**Backend (modified):**
- `backend/server.py` — mount retention router (2 lines).
- `backend/routers/compliance.py` — add 2 write endpoints.

**Backend (invariant re-scope):**
- `backend/tests/invariants/test_no_unauthorized_deletion_path.py` — AST gate. Enumerates all `.py` files under `backend/`; grep-negative on `delete_one`, `delete_many`, `.drop(`; whitelist-positive ONLY for `services/retention/authorized_deletion.py`. Retires old implicit `test_no_deletion_path` (grep-negative on ALL deletion call sites) via retirement note.

**Frontend:**
- NO NEW FRONTEND at sub-stage 2. Retention-config write UI lands with B-5b per §3.6B B5b-R1 (Compliance Console owns write UI). Deletion executor is API-only at this stage. **See §7 Escalation E2.**

**Test matrix (sub-stage 2):**

| Cell class | Backend | Cases | Count |
|---|---|---|---|
| Retention-config write endpoint | Backend | 5 auth postures × 3 rule shapes (per-class × 3 held-classes; inheritance-default; no-rule-set) | 15 |
| Deletion executor endpoint | Backend | 5 auth postures × 6 rule-shape/class-combos (3 held-classes × rule-present + rule-absent) | 30 |
| Deletion event ledger emission | Backend | 3 held-classes × (row-written + stamp_audit.data_class="authorized_deletion" + retention_rule_ref present) | 9 |
| `execute_authorized_deletion` unit | Backend | shape + idempotency + rule-lookup + null-window-refusal | 4 |
| Retention config version bump | Backend | v0→v1 shape + append-only + prior-version-byte-identical | 3 |
| Invariant re-scope AST gate | Backend | grep-negative across tree + whitelist-positive + retirement note preserved | 3 |
| Held-class enumeration single-source | Backend | reuse `HELD_CLASSES` from B-5a; parametrised over 3 classes | 3 |
| **Sub-total** | | | **~67 cells** |

Slightly higher than initial ~54 estimate (re-tabulated); pushes LoC
band accordingly.

**Rule 2 estimated band (sub-stage 2):** [2500, 2900] LoC.
`snapshot_lloc_in_band = conditional` — `no` if E1.α (stamp_audit-only);
`yes` if E1.β (NorthenaLedgerRow_v2 lands at this sub-stage, +216L snapshot).

**Per-bucket LoC breakdown (sub-stage 2):**

| Bucket | Estimated LoC |
|---|---|
| Backend impl (authorized_deletion.py 180L + retention_config_writes.py 140L + retention.v0.json 20L + 2 write endpoints 110L + `emit_deletion_ledger_row` helper 60L) | ~510 |
| Backend tests (67 backend cells × ~25 LoC/cell) | ~1675 |
| Config + snapshot (retention.v0.json + optional v2 contract if E1.β) | conditional 20-280L |
| Invariant re-scope gate (AST + retirement) | ~120 |
| **Total (E1.α)** | **~2325** |
| **Total (E1.β with v2 contract + snapshot)** | **~2605** |

E1.α falls at ~-7% below band mid ~2700. E1.β falls at ~-3% below.
Both within band.

═══════════════════════════════════════════════════════════════════

## §6. Sub-stage 3 — (c) §8 consequence-class checker

### §6.1 Deliverables (pending §7 Escalation E1 resolution)

**Backend (new):**
- `services/checker/consequence_classes.py` — constrained-str `consequence_class` type via Pydantic `Field(pattern=r"^(tightening_unilateral|dual_control)$")`. Explicitly documented in docstring: **NEVER Literal** (per CK-I1 + CK-G5).
- `services/checker/rule_change_request.py` — transient Pydantic model (NOT frozen). Fields per BCR annex.
- `services/checker/state_machine.py` — state transitions per BCR annex. Functions: `initiate(rule_class, from_value_ref, to_value_ref, initiator_id) → rule_change_request`, `countersign(request_id, checker_id) → effective|error`, `advance_delay(request_id, now) → effective|error`, `object(request_id, objector_id) → objected + owner_escalation`.
- `services/checker/effective_delay.py` — reads `consequence_class.v0.json` config for both `rule_class → consequence_class` mapping AND `effective_delay` value.
- `consequence_class.v0.json` — versioned config carrying:
```
{ rule_class_map: { retention_windows: dual_control,
                    disclosure_thresholds: dual_control,
                    lawful_basis_registry: dual_control,
                    source_standing_table: tightening_unilateral,
                    ... },
  effective_delay_seconds: 3600 }
```
- `services/checker/countersign_ledger.py` — emits `NorthenaLedgerRow_v1` with `stamp_audit: {data_class: "countersigned_rule_change", rule_class, consequence_class, initiator, checker, initiated_at, countersigned_at}` per CK-B1 verbatim. Also emits tightening-effective + objection rows.

**Backend (new endpoints):**
- `POST /api/checker/initiate` — initiator kicks off a rule-change request.
- `POST /api/checker/countersign/{request_id}` — second-console signature. LB gate CK-G1: blocks-until-countersign.
- `POST /api/checker/object/{request_id}` — objection path (tightening only).
- `GET /api/checker/pending` — banner-feed for BOTH consoles. Returns per-role pending items.

**Frontend:**
- `frontend/src/components/CounterSignBanner.jsx` — added to `ui_spec_v1/index.js` barrel. Renders on BOTH Compliance and Administration consoles.
- `frontend/src/pages/compliance/ComplianceHomePage.js` — extend to render `CounterSignBanner` (top of page).
- `frontend/src/pages/master_admin/MasterAdminHomePage.js` (extend or NEW; TBD at sub-stage 3 dispatch reading of existing tree) — same banner.
- Commit-line binding copy VERBATIM per CK-U1: `"Signed by {initiator} - counter-signed by {checker} - recorded with both identities."`

**Test matrix (sub-stage 3):**

| Cell class | Backend/Frontend | Cases | Count |
|---|---|---|---|
| `consequence_classes.v0.json` registry × schema | Backend | shape + rule_class_map non-empty + values ∈ {tightening_unilateral, dual_control} | 3 |
| `consequence_class` constrained-str NEVER Literal | Backend | AST gate CK-G5 (grep-negative on `Literal["tightening_unilateral"...` in services/checker/) + positive on `Field(pattern=...)` | 2 |
| Rule-change-request transient model | Backend | shape + NOT in `contracts/__init__.py` exports + NOT in mechanical parity map | 3 |
| Dual-control state machine (LB CK-G1) | Backend | initiate → pending_counter_sign; countersign → effective; between-states = blocked | 4 |
| Tightening state machine (LB CK-G3) | Backend | initiate → pending_delay; advance_delay < effective_delay = still pending; ≥ effective_delay = effective; object() at pending_delay = objected | 5 |
| Countersign ledger row (LB CK-G2) | Backend | row emitted + stamp_audit carries BOTH identities + BOTH timestamps + rule_class + consequence_class | 4 |
| Tightening-effective ledger row | Backend | row emitted at delay-expiry; stamp_audit carries initiator + rule_class + effective_at | 3 |
| Objection ledger row | Backend | row emitted at object() + stamp_audit carries objector + owner-escalation-marker | 3 |
| Symmetry gates (LB CK-G4) | Backend | Compliance-initiated loosening needs Admin countersign; Admin-initiated loosening needs Compliance countersign | 3 |
| Effective-delay is config-driven | Backend | change config value; state machine reads new value | 2 |
| Pending-items banner endpoint | Backend | 5 auth postures × per-role filtering | 6 |
| Commit-line binding-copy verbatim | Backend | serialized response carries verbatim string on countersign | 1 |
| Frontend `CounterSignBanner` barrel-reuse | Frontend Jest | parametrised over 2 pages × barrel-single-source | 3 |
| Verbatim binding-copy render | Frontend Jest | commit-line text matches CK-U1 pattern | 2 |
| Pending banner both-consoles | Frontend Jest | Compliance page renders + MasterAdmin page renders + dynamic per-role composition | 3 |
| Playwright chromium smokes | Frontend e2e | 2 consoles × pending/countersigned states = 2 specs × 2-3 assertions each | 2 specs (~5 assertions) |
| **Sub-total** | | | **~49 cells** |

**Rule 2 estimated band (sub-stage 3):** [2000, 2500] LoC.
`snapshot_lloc_in_band = no` (no new frozen contract per CK-I1).

**Per-bucket LoC breakdown (sub-stage 3):**

| Bucket | Estimated LoC |
|---|---|
| Backend impl (7 checker modules ~500L + consequence_class.v0.json 40L + 4 endpoints ~180L) | ~720 |
| Backend tests (49 backend cells × ~22 LoC/cell) | ~1080 |
| Frontend impl (CounterSignBanner 90L + 2 page deltas 2×40=80L + apiClient.js +25L + MasterAdminHome extension 60L) | ~255 |
| Jest gates (8 cells × ~28 LoC/cell) | ~225 |
| Playwright smokes (2 specs × ~55 LoC/spec) | ~110 |
| **Total** | **~2390** |

Falls at ~-4% below band mid ~2250. Within band.

═══════════════════════════════════════════════════════════════════

## §7. Escalations to Owner

### §7.1 Escalation E1 — governance-semantic (frozen-contract touch question)

**Substrate:** `NorthenaLedgerRow_v1.stage: Literal["admit", "gate", "converge"]` + `decision: Literal[...]` do NOT semantically contemplate:
- deletion events (`data_class="authorized_deletion"` per §3.5 annex);
- rule-change events (`data_class="countersigned_rule_change"` per §3.11 CK-B1; also tightening-effective + objection rows).

Both §3.5 and §3.11 annexes explicitly write "NorthenaLedgerRow_v1" without any note on the stage/decision mismatch. Escalation cap applies.

**Two options for Owner ruling:**

**E1.α — stamp_audit-only disambiguation (proposed default):**
- Reuse `stage="converge"` + `decision="continue"` as neutral placeholders + reason string prefix (e.g. `authorized_deletion:{held_class}`, `countersigned_rule_change:{rule_class}`, `tightening_effective:{rule_class}`, `tightening_objected:{rule_class}`) + `stamp_audit.data_class` carries semantic disambiguation per mandate.
- Precedent: Phase 6 Stage B stamp_audit-disambiguation for quote-mint instrumentation already writes `stage="converge"` + stamp_audit sidecar.
- Frozen contract parity: **26 (unchanged) across all 3 sub-stages.**
- Honesty cost: `stage="converge"` and `decision="continue"` are semantically stretched for events that are neither convergence nor continuation. `reason` string carries the honest label; classifier + regulator surface can key off stamp_audit.data_class or reason prefix.

**E1.β — NorthenaLedgerRow_v2 (frozen-contract addition, HAZARD-STOP path):**
- Lands `contracts/northena_ledger_v2.py` with `stage: Literal["admit","gate","converge","retention","rule_change"]` + `decision` Literal supersetted for the new semantics. Superset-validating (v1 rows also validate under v2 per `frozen-field-changes-as-new-versions` Standing Disposition).
- v0 + v1 files remain byte-identical (guarded by regression gates parametrised over 20 prior contract sources).
- Snapshot map bumps 26→27 at sub-stage 2 close.
- Honesty benefit: `stage` names the event class truthfully; classifier queries + regulator surface read `stage` directly without semantic overloads.
- Cost: HAZARD-STOP (a) at Owner's frozen-field ruling. Substrate-Drop v1 gate re-runs post-freeze.

**Proposed disposition (dev):** E1.α — retains parity 26 unchanged; the mandate annexes explicitly cite `NorthenaLedgerRow_v1` and do not narrow `stage` semantics. But **Owner rules at sub-stage 2 dispatch** — this is the exact governance-semantic contact class the escalation cap protects.

### §7.2 Escalation E2 — governance-semantic (surface ownership)

**Substrate:** BCR §3.5 S3-R1 says "retention CONFIGURATION SURFACE" lands with Seam 3; BCR §3.6B B5b-R1 says Compliance Console owns writes to retention windows.

**Proposed disposition (dev):** Seam 3 = BACKEND ENDPOINT ONLY at sub-stage 2 (`POST /api/compliance/retention_config` + `POST /api/compliance/authorized_deletion`); Compliance Console UI for retention windows lands with B-5b atop the Seam-3 endpoint. Coverage-marker rider (sub-stage 1) is the ONLY frontend touch during Seam 3 sub-stages.

Owner rules if UI should ride Seam 3 sub-stage 2 (retention window write buttons on §4.3 Retention & rights page) OR stay queued for B-5b per §3.6B mandate reading.

### §7.3 Escalation E3 — owner-value (coverage-marker `{date}` composition)

**Substrate:** Owner-supplied binding-copy `"Counts {families} since system start; {families} since {date} — earlier events in those families were not recorded."`

**What does `{date}` literal render as?** Three options:
- **E3.α (proposed default):** Fixed literal in `refusal_family_since_dates.v0.json` config; value set at sub-stage 1 close to the UTC-ISO date of the seam-3 first-commit deploy. Config is versioned, honest, never rewritten. Precedent: `feasibility-config@v0-provisional`.
- **E3.β:** Derived at query time from the earliest `NorthenaLedgerRow_v1` timestamp for each newly-instrumented family. More expensive query; potentially inaccurate if the same family has old rows from a different code path.
- **E3.γ:** Rendered from an env var. Not versioned; violates config-versioned-not-frozen posture.

**Proposed disposition (dev):** E3.α. Owner rules at sub-stage 1 dispatch.

### §7.4 Escalation E4 — module placement (`emit_refusal_ledger_row`)

**Substrate:** Owner's B-5a §7.1 observation named `services/service_1/async_state.py:238::emit_ledger_terminate_refused` as candidate wire-up target (dead stub today).

**Two options:**
- **E4.α (proposed default):** New module `services/northena/refusal_ledger.py` — parallel to `admit.py`, `converge.py`. Serves BOTH sync (`service_1/service.py` + `composed_conclusion.py`) AND async (`async_worker.py`) callers from ONE canonical home. `async_state.py:238` gets migration docstring but body kept byte-identical (BC preserved).
- **E4.β:** Revive `async_state.py:238::emit_ledger_terminate_refused` as canonical. Uses Owner-named function name. But places the callable in an async-worker-scoped module while it must serve sync paths too.

**Proposed disposition (dev):** E4.α. Owner rules at sub-stage 1 dispatch.

### §7.5 Escalation E5 — new named gate registry

No new auth codes needed. `4-code auth registry closed` posture preserved (`auth_scope_insufficient` for DPO-role denials on write endpoints; `auth_missing` / `auth_expired` for JWT plumbing). No new §0.1 dispositions expected across sub-stages 1-3.

### §7.6 Escalation E6 — sub-stage 3 second-console page existence

**Substrate:** BCR CK-U1 requires pending-items banner on BOTH consoles (Compliance + Administration). Need to read Master Admin surface tree at sub-stage 3 open to confirm `MasterAdminHomePage.js` (or equivalent) exists.

**Proposed disposition (dev):** flagged for read at sub-stage 3 dispatch. If page missing: HAZARD-STOP at sub-stage 3 open with a page-creation escalation to Owner. If page exists: extend it inline.

═══════════════════════════════════════════════════════════════════

## §8. Standing constraints compliance one-liner (pre-dispatch)

- 26 frozen contracts byte-identical **UNLESS E1.β ruled at sub-stage 2** (in which case 27 at sub-stage 2 close; frozen-field-changes-as-new-versions Standing Disposition applies).
- No LLM outside Shield.
- §0.1 FROZEN — zero new dispositions expected across sub-stages 1-3.
- §0.2 updates: un-ledgered families debt marked IN-PROGRESS at sub-stage 1 Stage B dispatch; RESOLVED at sub-stage 1 Stage B close with per-family evidence.
- No `git push` dev-side.
- Standing Rule v3 on all deliverables (on-disk canonical + SHA; no inline paste).
- First-commit gating standing pattern applies to all Seam 3 + §8 surfaces (Playwright chromium smokes land in same commit block as pages).
- Playwright chromium-only invariant preserved.
- Shared §8 barrel consumed at all sub-stages (`RefusalsCoverageMarker` at sub-stage 1; `CounterSignBadge` at sub-stage 3); no reimplementation.
- 4-code auth registry closed — Seam 3 write endpoints use existing codes; NO new codes.
- Escalation cap ORIGINAL wording preserved.
- Test matrix enumeration standing correction applied (§4/§5/§6 above).

═══════════════════════════════════════════════════════════════════

## §9. Total cell counts + Rule 2 anchor bands

| Sub-stage | Cells | Anchored LoC band | snapshot_lloc_in_band |
|---|---|---|---|
| 1. Refusal-family ledger wire-up + coverage marker | 35 | [1400, 1800] | no |
| 2. Authorized-deletion path | 67 | [2500, 2900] (E1.α) OR [2500, 3100] (E1.β) | no (E1.α) / yes (E1.β) |
| 3. §8 consequence-class checker | 49 | [2000, 2500] | no |
| **TOTAL** | **151 cells** | **[5900, 7400]** | mixed |

Single-dispatch derives ~5900-7400 LoC — 2×+ ceiling. **Split required
and proposed as sub-stages 1 → 2 → 3.**

═══════════════════════════════════════════════════════════════════

## §10. Ready-to-dispatch posture

**Sub-stage 1 (refusal-family ledger wire-up + coverage marker):**
- E3 (coverage-marker `{date}` composition) + E4 (module placement) resolutions needed BEFORE sub-stage 1 Stage B dispatch. Both default proposals (α) available for owner α-ratify shortcut.
- No frozen-contract escalation.
- No governance-semantic ambiguity.
- **READY TO DISPATCH ON OWNER RULING E3/E4** (or on α-defaults ratification).

**Sub-stage 2 (authorized-deletion path):**
- E1 (frozen-contract touch question) + E2 (surface-ownership question) resolutions needed BEFORE sub-stage 2 Stage B dispatch. Both are governance-semantic surfaces per Owner ruling.
- **RULING-CONDITIONED PAUSE FLAGGED.**

**Sub-stage 3 (§8 consequence-class checker):**
- E1 (reused from sub-stage 2) + E6 (Master Admin page existence read) resolutions needed BEFORE sub-stage 3 Stage B dispatch.
- **RULING-CONDITIONED PAUSE FLAGGED.**

═══════════════════════════════════════════════════════════════════

*End of Stage A proposal.*
