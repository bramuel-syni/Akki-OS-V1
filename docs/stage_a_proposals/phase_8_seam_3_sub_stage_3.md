# Phase 8 Seam 3 Sub-stage 3 — Stage A Design Proposal (§8 consequence-class checker)

**Design date:** 2026-07-07
**Scope authority:** Stage A proposal `/app/docs/stage_a_proposals/phase_8_seam_3_and_checker.md` §6 verbatim (SHA `3fe969c2add52da7f4d80251a8bcb2d1bcf3154c82a10a7fb2241d44bb08500d`).
**Rulings pre-carried:** E1–E7 (§1–§9 rulings record); R-1..R-6 (§10 rulings record). SHA `7c2b61f1e739c3f88689bf7ec235a1f259655d539fe9fc1babd3a1f1d30f6653`.
**Dispatch-A verdict (pending Owner ruling):** `LedgerArtifactRef.artifact_type` is a `Literal["portfolio_mandate", "objective_request"]` (narrow); Stage A §7.1 does NOT explicitly authorize reusing it for deletion events. Per Owner's tightened decision rule (2026-07-07), **path 3 (registry retrofit) applies**. This proposal prices both branches:
- **Band A (no retrofit):** Sub-stage 3 §8 checker scope only. Assumes path 1 selection.
- **Band B (baseline + artifact_type registry retrofit):** Sub-stage 3 §8 checker scope PLUS §12 retrofit lands in Sub-stage 3's first commit.

The §12 read outcome selects; no restatement needed.

Standing Rule v3: this proposal lives on disk. Reply body is a header row of SHA + structural summary.
Standing Correction: matrix-enumerated sizing (endpoints × postures × cases × invariants), never LoC lumps.

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
| 3.1.4 | `services/checker/state_machine.py` | `initiate() → pending_counter_sign\|pending_delay`; `countersign() → effective\|error`; `advance_delay() → effective\|pending_delay`; `object() → objected + owner_escalation` |
| 3.1.5 | `services/checker/effective_delay.py` | Reads `consequence_class.v0.json` for rule_class→consequence_class mapping + delay config |
| 3.1.6 | `services/checker/countersign_ledger.py` | `emit_countersign_ledger_row()` — CK-B1 pinned sidecar identities |
| 3.1.7 | `services/checker/tightening_effective_ledger.py` (may be same module as 3.1.6 depending on cohesion) | Emits tightening-effective + objection rows |
| 3.1.8 | `services/compliance/consequence_class.v0.json` | Registry: `{ rule_class_map: {retention_windows: dual_control, disclosure_thresholds: dual_control, lawful_basis_registry: dual_control, source_standing_table: tightening_unilateral, ...}, effective_delay_seconds: 3600 }` |
| 3.1.9 | Extend `data_class_registry.v0.json` → `v1.json` | Append `countersigned_rule_change`, `tightening_effective`, `tightening_objected` as valid_data_classes (append-only version bump per E1.γ precedent) |

### §3.2 Backend — new endpoints

| # | Endpoint | Auth | Body | Behavior |
|---|---|---|---|---|
| 3.2.1 | `POST /api/checker/initiate` | DPO OR admin (role-symmetric) | `{rule_class, from_value_ref, to_value_ref}` | Initiator kicks off request. Returns `{request_id, state, consequence_class}`. |
| 3.2.2 | `POST /api/checker/countersign/{request_id}` | Second-console role (initiator=DPO → countersigner=admin; initiator=admin → countersigner=DPO) — CK-G4 symmetry | (no body) | Countersign transition. LB gate CK-G1: blocks until countersigned. Returns `{state: effective, effective_at, ledger_row_ref}`. |
| 3.2.3 | `POST /api/checker/object/{request_id}` | Countersigner role (tightening_unilateral only) | `{reason}` | Objection path. Emits owner-escalation marker. |
| 3.2.4 | `GET /api/checker/pending` | Any authenticated user | (query param `role`) | Banner-feed for BOTH consoles. Returns per-role pending items. |

### §3.3 Backend — retention endpoint checker-routing hook

- `POST /api/compliance/retention_config` (Sub-stage 2 landed): loosening writes NOW route through `services/checker/state_machine.initiate(rule_class="retention_windows", ...)`. Instead of 403 refusal, the endpoint returns `202 Accepted` with `{state: "pending_counter_sign", request_id, consequence_class: "dual_control"}`.
- Tightening writes stay unilateral-with-delay: enter `pending_delay` state, become effective after `effective_delay_seconds` elapsed.
- E2 gate `test_retention_endpoint_loosening_disabled_pre_checker` RETIRES.
- New gate `test_retention_loosening_write_requires_administration_countersign` LANDS (CK-B3 symmetry).

### §3.4 Frontend — new component + page extensions

| # | File | Kind | Role |
|---|---|---|---|
| 3.4.1 | `frontend/src/components/ui_spec_v1/CounterSignBanner.jsx` | New component | Top-of-page banner listing pending items per role. Middle-dot binding copy verbatim. |
| 3.4.2 | `frontend/src/components/ui_spec_v1/index.js` | Barrel extension | Export `CounterSignBanner`. Single-source enforced by CK-G-BARREL. |
| 3.4.3 | `frontend/src/pages/compliance/ComplianceHomePage.js` | Page extension | Render `<CounterSignBanner role="compliance" />` at page top. |
| 3.4.4 | `frontend/src/pages/master_admin/MasterAdminHomePage.js` | Page extension | Render `<CounterSignBanner role="admin" />` at page top. |
| 3.4.5 | `frontend/src/apiClient.js` | Client shim | `checkerInitiate` + `checkerCountersign` + `checkerObject` + `checkerPending` |

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
| §E | Tightening-unilateral state machine (**LB CK-G3**) | `initiate` → `pending_delay`; `advance_delay(now < effective_delay)` = still pending; `advance_delay(now >= effective_delay)` = effective; `object` at pending_delay = objected + owner_escalation; `object` post-effective = disallowed | 5 |
| §F | Countersign ledger row (**LB CK-G2** `test_countersign_row_carries_both_identities`) | row emitted + stamp_audit carries `{data_class: "countersigned_rule_change", rule_class, consequence_class, initiator, checker, initiated_at, countersigned_at}` pinned keys | 4 |
| §G | Tightening-effective ledger row | row emitted at delay-expiry; stamp_audit carries `initiator + rule_class + effective_at + data_class: "tightening_effective"` | 3 |
| §H | Objection ledger row | row emitted at `object()`; stamp_audit carries `objector + owner-escalation-marker + data_class: "tightening_objected"` | 3 |
| §I | Symmetry gates (**LB CK-G4**) | Compliance-initiated loosening needs Admin countersign; Admin-initiated loosening needs Compliance countersign; same-role countersign = refused | 3 |
| §J | Effective-delay is config-driven | change `consequence_class.v0.json` `effective_delay_seconds`; state machine reads new value; `test_effective_delay_is_config_driven_not_hardcoded` | 2 |
| §K | `POST /api/checker/initiate` endpoint × auth × role symmetry × payload | 5 auth postures × 2 payload variants | 6 |
| §L | `POST /api/checker/countersign/{request_id}` endpoint × auth × role symmetry × state | 5 auth postures × 2 state variants (pending → effective / already-effective → 4xx non-409) | 6 |
| §M | `POST /api/checker/object/{request_id}` endpoint | 3 auth postures × 2 state variants (pending_delay → objected / non-tightening → 4xx non-409) | 4 |
| §N | `GET /api/checker/pending` endpoint | 5 auth postures × per-role filtering (2 role variants) | 5 |
| §O | `test_retention_loosening_write_requires_administration_countersign` (CK-B3 symmetry) | POST retention_config × loosening × routes to checker × returns 202 pending_counter_sign | 3 |
| §P | `test_retention_endpoint_loosening_disabled_pre_checker` RETIRES — retirement note preserved | retirement note × asserted × preserved | 1 |
| §Q | 409 self-audit (E5 full-anti-rule reactivation continues) | Sub-stage 3 diff files × static-scan × zero hits | 1 |
| §R | Sub-stage 3 data-class LB mirror gates | 3 new data classes (`countersigned_rule_change`, `tightening_effective`, `tightening_objected`) — each ledger row asserts pinned `stamp_audit["data_class"]` + registry-valid; parametrised over 3 event classes + 1 aggregate | 4 |
| §S | Commit-line binding-copy verbatim | serialized response carries verbatim string with `·` U+00B7 middle-dot on countersign | 1 |

**Subtotal backend Pytest cells: 64.**

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

### §4.4 Band A totals

- **Backend cells:** 64
- **Frontend Jest cells:** 8
- **Playwright cells:** 4
- **Total Band A cells:** **76**

═══════════════════════════════════════════════════════════════════

## §5. §12 registry retrofit surface (BAND B ONLY)

Applied ONLY if Dispatch A outcome selects path 3 (registry retrofit).

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

## §6. Test matrix — BAND B additive cells (retrofit deltas)

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

## §7. Rule 2 anchor bands

### §7.1 Band A (no retrofit)

**Per-bucket LoC breakdown:**

| Bucket | Estimated LoC |
|---|---|
| Backend impl (7 checker modules ~500L + `consequence_class.v0.json` 40L + `data_class_registry.v0.json` v1 bump 15L + 4 endpoints + retention hook rewire ~220L) | ~775 |
| Backend tests (64 cells × ~22 LoC/cell) | ~1,410 |
| Frontend impl (`CounterSignBanner` 90L + 2 page deltas 2×40=80L + `apiClient.js` +25L + `MasterAdminHome` extension 60L + barrel +5L) | ~260 |
| Jest gates (8 cells × ~28 LoC/cell) | ~225 |
| Playwright smokes (4 cells × ~55 LoC/cell across 1 spec) | ~120 |
| **Band A total** | **~2,790** |

Compared with Stage A §6 estimate: original was ~2,390 LoC / 49 cells; refined estimate here is ~2,790 LoC / 76 cells. **Overrun of ~+400 LoC vs. Stage A §6 estimate**, driven by more granular cell enumeration (I added E2 gate retirement + retention hook rewire + 409 self-audit + data-class LB mirror gates + auth-posture matrix expansion, all matrix-enumerated per Standing Correction).

**Owner-anchored band per Stage A §9 line 562:** `[2000, 2500]`.

**Band A LoC 2,790 vs. anchor top 2,500 → OVERRUN of +290 LoC (+12%).** This is dev-autonomous LoC surprise per §7 last paragraph, disclosed here for Owner ratification. If Owner prefers Band A stays within anchor `[2000, 2500]`, some cells can defer to a follow-up patch — see §9 split candidacy assessment.

### §7.2 Band B (baseline + retrofit)

**Additional retrofit LoC:**

| Bucket | Estimated LoC |
|---|---|
| `artifact_type_registry.py` + `artifact_types.v0.json` | ~85 |
| Emitter updates (deletion_ledger + countersign_ledger + 2 event-class emitters) | ~35 |
| Backfill migration script | ~50 |
| Sidecar-pinned-key conventions | 0 (convention only) |
| Retrofit tests (15 cells × ~22 LoC/cell) | ~330 |
| **Retrofit subtotal** | **~500** |

**Band B total: 2,790 + 500 = ~3,290 LoC / 91 cells.**

**Band B overrun vs. anchor top 2,500 → +790 LoC (+32%).** Materially over the anchor. Split proposal candidacy triggers (see §9).

### §7.3 Both bands — summary

| Band | Cells | LoC | vs. Anchor [2000, 2500] |
|---|---|---|---|
| A (no retrofit) | 76 | ~2,790 | +290 (+12%) — dev-autonomous surprise |
| B (baseline + §12 retrofit) | 91 | ~3,290 | +790 (+32%) — split candidacy triggers |
| B − A (retrofit cost) | +15 cells | +500 LoC | Retrofit-only delta |

═══════════════════════════════════════════════════════════════════

## §8. Escalations to Owner (S3-E1 through S3-E5)

### §8.1 S3-E1 — Frozen-contract adjacency: `CounterSignBanner` binding-copy semantics

**Class:** owner-value contact.

**Question:** the commit-line binding copy per CK-U1 (per Stage A §6.1 line 330) reads: *"Signed by {initiator} · counter-signed by {checker} · recorded with both identities."* The middle-dot glyph U+00B7 is E7-strict. **What if the countersigner has both roles (dpo AND admin) — how does the banner render?** Stage A §6 does not enumerate the two-role case. Options:

- (a) Display the countersigner's PRIMARY role (per identity's roles order).
- (b) Display all roles bracket-listed.
- (c) Refuse the countersign entirely (require single-role countersigners).

**Recommended:** (a) — primary role. Consistent with existing pattern in `MasterAdminHomePage.js` role display. Owner ruling requested before Sub-stage 3 dispatch.

### §8.2 S3-E2 — Objection rehydration semantics

**Class:** governance-semantic contact.

**Question:** at `object()` on a `pending_delay` (tightening_unilateral), the request transitions to `objected + owner_escalation`. **Does the objected request block subsequent identical initiate() attempts?** Stage A §6 is silent.

Options:
- (a) Objection is one-time — subsequent initiate() with same `(rule_class, from_value_ref, to_value_ref)` proceeds normally (no memory).
- (b) Objection sticks — subsequent identical initiate() refused until Owner escalation resolves.
- (c) Cooldown window — subsequent identical initiate() refused within N hours of objection.

**Recommended:** (b) — objection sticks pending owner-escalation resolution. Aligns with the "objection triggers owner-escalation" intent. Landing includes an owner-escalation resolution endpoint (or Owner-side manual state clear).

### §8.3 S3-E3 — `data_class_registry.v0.json` extension mechanism

**Class:** governance-semantic contact.

**Question:** Stage A §7.1.γ says event classes extend the SAME registry (or a scope-parallel registry per data-class family) as append-only additions. **Does Sub-stage 3 append to `data_class_registry.v0.json` in-place (rename to v1?) or land a new file `rule_change_events.v0.json`?**

Options:
- (a) Append to `data_class_registry.vN.json`, bump v0 → v1 (single-registry per E1.γ discretion "single unified registry vs per-purpose registries settled at those dispatches").
- (b) Land per-purpose registry `rule_change_events.v0.json` (scope-parallel).

**Recommended:** (a) — bump `data_class_registry.v0.json` to v1. Consistent with Sub-stage 2 landing pattern (deletion added to same registry rather than a separate one). Test matrix §R above assumes (a).

### §8.4 S3-E4 — Retrofit landing pattern (Band B only)

**Class:** governance-semantic contact — applies ONLY if Dispatch A ruling selects path 3.

**Question:** the §12 retrofit lands (a) at Sub-stage 3's first commit as an integral rider, or (b) as a separate pass BEFORE Sub-stage 3 execution. Owner directive says both branches priced in same proposal; the SEQUENCING of the retrofit landing is separately ruled.

Options:
- (a) **Integral rider** — retrofit lands in Sub-stage 3's atomic first commit alongside checker impl + tests + frontend. First-commit gating includes retrofit.
- (b) **Pre-execution pass** — Sub-stage 3 execution paused; retrofit lands as a dedicated commit first (Owner ratifies retrofit close report); THEN Sub-stage 3 fires. Two atomic commits.

**Recommended:** (a) — integral rider. Rationale: (i) matches Sub-stage 2's rider pattern (§2.1 R-6 footer + §2.2 stale-line correction all folded into Sub-stage 2's first commit); (ii) Sub-stage 3 emitters (`countersign_ledger.py` etc.) will use the new registry-pattern from the start, so landing them TOGETHER preserves consistency; (iii) backfill migration script runs once at first-commit landing, all consumers converge to the new sidecar-pinned-key convention simultaneously.

Owner ruling required before Sub-stage 3 dispatch.

### §8.5 S3-E5 — Split-proposal candidacy

**Class:** LoC-band overrun (§9 below elaborates).

**Question:** Band A at 2,790 LoC exceeds anchor top by 12%; Band B at 3,290 LoC exceeds by 32%. **Does Sub-stage 3 split into two commits (checker impl + tests atomically as commit 1; frontend + Playwright + close as commit 2), or land as one atomic commit?**

Options:
- (a) One atomic commit — first-commit gating discipline preserved; LoC surprise reported in close (dev-autonomous per §7).
- (b) Two atomic commits — Sub-stage 3.1 backend + tests; Sub-stage 3.2 frontend + Playwright + close. Preserves anchor-band closer to top.
- (c) Widen the anchor band to `[2000, 3000]` for Sub-stage 3 explicitly, reflecting the Standing-Correction cell expansion.

**Recommended:** (a) — one atomic commit with LoC surprise disclosed. First-commit gating is the load-bearing discipline; splitting Sub-stage 3 would break the "wiring + tests + frontend + smoke in ONE commit" invariant that Sub-stages 1 and 2 preserved. Overrun +12% (Band A) is manageable; +32% (Band B) is closer to the split-candidacy threshold but still doable in one commit if honest-cost is preserved. If Owner prefers (b) split at 3.1/3.2, retrofit stays in 3.1.

═══════════════════════════════════════════════════════════════════

## §9. Split-proposal candidacy assessment

**Prior sub-stage sizing:**

| Sub-stage | Cells | LoC | Split status |
|---|---|---|---|
| Sub-stage 1 | 22 Pytest + 6 Jest + 2 Playwright = 30 | 1,160 | Single-commit atomic |
| Sub-stage 2 | 35 Pytest + 0 Jest + 0 Playwright = 35 | 1,703 | Single-commit atomic |
| Sub-stage 3 Band A (proposed) | 64 Pytest + 8 Jest + 4 Playwright = 76 | ~2,790 | Single-commit or split TBD |
| Sub-stage 3 Band B (proposed) | 79 Pytest + 8 Jest + 4 Playwright = 91 | ~3,290 | Single-commit or split TBD |

**Split thresholds observed:**
- Seam 3 originally proposed as one dispatch at 151 cells / 5,900-7,200 LoC — Owner-mandated split into three sub-stages.
- Sub-stage 3 alone at 76-91 cells / 2,790-3,290 LoC is roughly 50% of the original Seam 3 volume. Not egregious relative to Sub-stage 2 (35 cells / 1,703 LoC).

**Split-proposal recommendation for Owner disposition:**

- **Band A + one atomic commit**: recommended default. First-commit gating preserved; LoC surprise disclosed.
- **Band B + one atomic commit**: recommended if Dispatch A selects path 3; retrofit as integral rider (S3-E4 option (a)).
- **Split into Sub-stage 3.1 + 3.2**: NOT recommended unless Owner explicitly rejects the LoC overrun. Split would fragment the checker's landing across two commits, which weakens the "checker state machine + endpoints + banner + gates all-or-nothing" atomic-landing discipline.

═══════════════════════════════════════════════════════════════════

## §10. Ready-to-dispatch posture per band

**Band A (no retrofit) posture:**
- All Stage A §6 deliverables enumerated; matrix-enumerated cell roster (76 cells) documented; escalation flags S3-E1 through S3-E3 + S3-E5 surfaced (S3-E4 does not apply).
- Frozen contract parity 26 preserved (no touches).
- E2 gate retirement + CK-B3 symmetry gate landing.
- E5 full-anti-rule discipline preserved (409 self-audit continues).
- Middle-dot glyph binding preserved (Jest + Playwright).
- **READY TO DISPATCH POST OWNER RULINGS ON S3-E1/E2/E3 + LoC-overrun ratification.**

**Band B (baseline + retrofit) posture:**
- All Band A deliverables PLUS §5 retrofit surface + §6 additional 15 cells.
- Frozen contract parity 26 preserved (retrofit uses sidecar-pinned-key pattern per E1.γ analog; `LedgerArtifactRef.artifact_type` byte-identical).
- Backfill migration lands at first commit; idempotent + post-migration completeness gate.
- Sub-stage 2 close report §12 correction footer appended (small documentation rider inside Sub-stage 3's landing).
- **READY TO DISPATCH POST DISPATCH-A RULING (path 3) + OWNER RULINGS ON S3-E1/E2/E3/E4 + LoC-overrun ratification.**

═══════════════════════════════════════════════════════════════════

*End of Sub-stage 3 Stage A proposal. Owner ruling on Dispatch A + escalations S3-E1..E5 required before Sub-stage 3 dispatch. Both bands priced; §12 read outcome selects.*
