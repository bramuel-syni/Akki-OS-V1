# Phase 8 Stage B-5b — Stage A Design Proposal (Compliance rulebook-write UI + B-4 read-only retrofit)

**Design date:** 2026-07-07
**Design authority:** Owner dispatch 2026-07-07 (post-Sub-stage-3 acceptance `994d2b40…`).
**Scope:** UI Spec v2.1 §4.4-4.5 (Compliance Console rulebook writes wiring to Sub-stage 3 checker) + BCR v1.4.1 §3.6B (B5b-R1..R3 + B5b-G1..G4) + BCR v1.4.1 §3.13 / RT-R2 (B-4 retrofit — atomic-with-B-5b) + Owner deferred-UI ruling (x) 2026-07-07 (countersign action button + owner-suspend workflow UI).

**Authority-source SHAs (for citation stability):**
| Source | Path | SHA-256 | Cited sections |
|---|---|---|---|
| UI Spec v2.1 | `docs/mandates/RMS_UI_Specification_v2_1.md` | `ef6da4b498117608a3091033b5cfa43571ad8a7a38b5954cae7c4a1a698de5e2` | §4.4 (line 79-80), §4.5 (line 81-83), §6.4 (line 143) |
| BCR v1.4.1 | `docs/mandates/RMS_Build_Completion_Requirements_v1_4.md` | `ce5206c9e244fe58edb6824f785077c1c835bdf3f5b347f6a4fb98c036212524` | §3.6B (line 209-214), §3.13 (line 288-291), §5.1 (line 310) |
| Sub-stage 3 close | `docs/close_reports/phase_8_seam_3_sub_stage_3.md` | `994d2b40c117f9363495b7442ff1f7309e7b9abe23e248a8ab5ae3d7cc366c12` | FINAL ACCEPTANCE baseline; §8 preconditions surfaced; owner-suspend endpoint contract §7. |
| Sub-stage 3 Stage A (post-Amendment-G) | `docs/stage_a_proposals/phase_8_seam_3_sub_stage_3.md` | `b79469b48e5f39d67fa01a3d096249826b95021250a9effd0a556b6a97a4debe` | Checker endpoint contracts §3.2 (5 endpoints) + Ruling 3 semantics §8.2. |
| Rulings record | `docs/rulings/seam_3_stage_a_e1_to_e7.md` | `30c4af9f9994f0188313d2a2a6de2c68abc16f69deec042c28f38b9bba333f3c` | E7 middle-dot glyph (§8.6 of BCR §3.11); Ruling 2 capacity-role (§11.2); R-3 unclassified (§10). |
| rule2_accounting.json | `docs/rule2_accounting.json` | `b8df5d023a64b9314d824a454476f886714751fe665019d1d9d89c2d965fa89b` | Velocity baseline; cell-density empirical anchors from Sub-stage 3 entry. |

**Standing constraints (all binding):**
- Standing Rule v3: this proposal lives on disk. Reply body is SHA + structural summary.
- Standing Correction: matrix-enumerated sizing (endpoints × postures × cases × invariants).
- Standing state-conflict anti-rule (elevated Amendment G): NO HTTP 409 in B-5b diff; static scan at close.
- E7 middle-dot U+00B7 strict on binding copy.
- 26 frozen contracts + snapshots UNTOUCHED (parity 26).
- No `git push`. Owner pushes.
- Owner deferred-UI ruling (x): countersign button + owner-suspend UI ARE in scope. A checker invocable only by curl does NOT survive Phase 8's close.
- Owner projection-noise ruling: bands stay matrix-derived; misses stay disclosed; band is stop-and-judge, not a target.

---

## §1. Cell-density assumption (Owner-binding per projection-noise ruling)

Stated explicitly per Owner directive so any subsequent ruling that reshapes cells visibly re-derives the band (Amendment G template).

### §1.1 Empirical baseline (Sub-stage 3 measured, on-disk verifiable)

| Cell type | Empirical LoC/cell | Source |
|---|---:|---|
| Backend Pytest cell | **22 LoC/cell** | 993L test file / 45 cells (Sub-stage 3) |
| Frontend Jest structural cell | **16 LoC/cell** | 98L test file / 6 cells (Sub-stage 3) |
| Playwright chromium smoke cell | **32 LoC/cell** | 127L smoke file / 4 cells (Sub-stage 3) |

### §1.2 Divergences applicable to B-5b (stated so re-derivation is deterministic)

| Cell type | Divergent LoC/cell | Rationale |
|---|---:|---|
| **UI-form-writer Jest cell** | **28 LoC/cell** | Higher than baseline (16) because form-writer tests require mock+render+interact+assert per case (versus Sub-stage 3 CounterSignBanner cells, which were mostly render+assert). |
| **UI-form-writer Playwright smoke** | **48 LoC/cell** | Higher than baseline (32) because writer smokes need pre-fill + submit + response-mock + post-state assertion. |
| **Backend endpoint-writer cell (per posture)** | **22 LoC/cell** | Matches Sub-stage 3 baseline; no divergence. |
| **Backend LB gate (B5b-G* named gates)** | **35 LoC/cell** | Higher because parametrised over multiple rule classes with assertions on ledger row shape + registry validity. |
| **Read-only-retrofit invariant (RT-G1)** | **40 LoC/cell** | AST-scan over frontend page files enumerating write-route accessibility per compliance class. |

### §1.3 Backend/frontend impl LoC per feature (stated for re-derivation)

| Impl unit | LoC | Rationale |
|---|---:|---|
| Backend rulebook writer endpoint | **80 LoC/writer** | Route + payload validation + LoosengingRefused-style branch + checker.initiate wiring + ledger emit + registry validation. Matches Sub-stage 3's retention hook complexity. |
| Frontend rule-class writer component | **120 LoC/component** | Reuses §6.2 plain-language pattern from `ChangeARulePage.js` (existing on disk). Form + validation + display of consequence-class + pending state. |
| Frontend admin read-only retrofit (per rule-class read-only tile) | **35 LoC/tile** | Reuses existing `RetentionPostureBadge`-like pattern; adds "owned by Compliance" marker. |
| Frontend banner button augmentation (countersign / suspend) | **45 LoC/button** | Button-render + capacity-role gate + click-handler + feedback. |
| Owner-suspend workflow UI (Master Admin) | **90 LoC** | Reason input + confirmation dialog + wire to `POST /api/master_admin/tightening/suspend` + result render. |

**Re-derivation rule (Owner-binding):** any ruling that adds/removes a rule class, adds/removes an endpoint posture, adds a state to a workflow, or reshapes the compliance-vs-admin ownership split MUST re-derive the band using the rates above. NO padding, NO buffering the estimate up front. Miss + disclosure > pad + hide.

---

## §2. Deliverables enumeration (matrix per Standing Correction)

### §2.1 Backend — new endpoints + LB gates

Sub-stage 3 already landed 5 checker endpoints + rewired `POST /api/compliance/retention_config` to route through the checker. B-5b adds writers for the remaining 3 compliance rule classes (BCR §3.6B B5b-R1).

| # | Endpoint | Auth | Body variant | Behavior |
|---|---|---|---|---|
| 2.1.1 | `POST /api/compliance/disclosure_thresholds` | `dpo` OR `admin` (E2 4-code) | `{class: "k_anonymity"\|"l_diversity"\|"dp_budget", from_value, to_value}` | Loosening → checker.initiate(rule_class="disclosure_thresholds", ...) → 202 pending. Tightening → checker.initiate with tightening_unilateral consequence + 202 pending_delay. Every write emits `stamp_audit["consequence_class"]` (Ruling 6). |
| 2.1.2 | `POST /api/compliance/lawful_basis_registry` | `dpo` OR `admin` | `{basis_key, from_value, to_value}` | Symmetric to 2.1.1 — routes through checker (dual_control per `consequence_class.v0.json`). |
| 2.1.3 | `POST /api/compliance/source_standing_table` | `dpo` OR `admin` | `{source_ref, standing_change}` | Routes through checker as `tightening_unilateral` (per `consequence_class.v0.json` — this is the only compliance class scheduled as unilateral). |

Retention endpoint (`POST /api/compliance/retention_config`) landed at Sub-stage 3 already routes through the checker. **No new endpoint** — regression coverage only.

### §2.2 Backend — LB gates (B5b-G1..G4 + RT-G1)

| Gate | Purpose | Cells |
|---|---|---:|
| **B5b-G1** `test_tightening_change_is_unilateral_and_delayed` (BCR §3.6B line 214) | Every tightening write → 202 pending_delay + effective at delay expiry (verified via advance_delay). Parametrised over 4 rule classes (retention + disclosure + lawful_basis + source_standing). | 4 |
| **B5b-G2** `test_loosening_change_requires_countersign` (BCR §3.6B line 214) | Every loosening write → 202 pending_counter_sign; dual_control classes wait for countersign. Parametrised over 3 rule classes (retention + disclosure + lawful_basis; source_standing has no loosening semantic). | 3 |
| **B5b-G3** `test_compliance_rules_readonly_on_admin_console` (BCR §3.6B line 214) | Backend-side: no `POST /api/master_admin/...` route accepts compliance rule classes. Existing router audit + negative-space assertion. | 1 |
| **B5b-G4** `test_every_rule_write_emits_ledger_row_with_consequence_class` (BCR §3.6B line 214) | Every compliance-rule write emits a ledger row with `stamp_audit["consequence_class"]` present and registry-valid. Parametrised over 4 rule classes × 2 postures (tightening + loosening/setting-from-unset). | 8 |
| **RT-G1** `test_compliance_classes_have_no_write_route_on_admin_console` (BCR §3.13 line 291) | AST-scan or route-registry scan across `routers/master_admin.py` + `routers/pricing.py` — asserts no route accepts `rule_class ∈ {retention_windows, disclosure_thresholds, lawful_basis_registry, source_standing_table}`. Read-only marker rendered on Administration surface (frontend gate at §2.4.4). | 1 |

### §2.3 Backend — endpoint × auth × posture matrix (writer coverage)

Per writer endpoint (§2.1.1–§2.1.3):
- 4 auth postures (no-token → 401, wrong-role → 403, dpo → success, admin → success)
- 2 branch outcomes (tightening → 202 pending_delay, loosening → 202 pending_counter_sign)
- 1 malformed-payload posture (→ 400)
= **7 cells per endpoint × 3 new endpoints = 21 cells**.

Regression on `POST /api/compliance/retention_config` (already landed at Sub-stage 3):
- Existing cells persist unchanged; add 2 new regression cells verifying the ledger row's `stamp_audit["consequence_class"]` field survives B-5b changes.

### §2.4 Frontend — new pages + component updates

| # | File | Kind | Purpose |
|---|---|---|---|
| 2.4.1 | `frontend/src/pages/compliance/ComplianceRulebookWritePage.js` | New page | UI Spec v2.1 §4.4-4.5 hub. Routes at `/compliance/rulebook`. Renders 4 rule-class writer sections (retention + disclosure + lawful_basis + source_standing). Reuses `ChangeARulePage.js` §6.2 plain-language pattern verbatim. |
| 2.4.2 | `frontend/src/pages/compliance/RetentionWindowsWriter.jsx` | New component | Retention writer (already-landed backend). Section 4.5 wire; renders consequence-class banner on submit. |
| 2.4.3 | `frontend/src/pages/compliance/DisclosureThresholdsWriter.jsx` | New component | k-anonymity / l-diversity / DP-budget writer. Sub-class dropdown + numeric input. |
| 2.4.4 | `frontend/src/pages/compliance/LawfulBasisRegistryWriter.jsx` | New component | Basis-key writer with plain-language basis-descriptor input. |
| 2.4.5 | `frontend/src/pages/compliance/SourceStandingTableWriter.jsx` | New component | Source-standing writer; tightening_unilateral only. |
| 2.4.6 | `frontend/src/components/ui_spec_v1/CounterSignBanner.jsx` | **Modify** | Add "Countersign" action button per item where capacity-role matches the current user's capacity. Wires to `POST /api/checker/countersign/{id}` per Ruling 2 capacity-role. |
| 2.4.7 | `frontend/src/pages/master_admin/MasterAdminHomePage.js` | **Modify** | Add "Owner-suspend" action UI per tightening item on the banner. Owner-only capability. |
| 2.4.8 | `frontend/src/pages/master_admin/OwnerSuspendDialog.jsx` | New component | Modal dialog for owner-suspend: reason input + confirmation + wire to `POST /api/master_admin/tightening/suspend`. Distinct visual framing from objection per Ruling 3. |
| 2.4.9 | `frontend/src/pages/master_admin/AdminComplianceReadOnlyView.jsx` | New component | BCR §3.13 RT-R1: read-only render of retention + disclosure + lawful_basis + source_standing with "owned by Compliance" marker verbatim. Renders on `MasterAdminHomePage` OR a dedicated section (see B5b-E1 for escalation). |
| 2.4.10 | `frontend/src/apiClient.js` | Modify | Add: `complianceDisclosureThresholdsWrite`, `complianceLawfulBasisWrite`, `complianceSourceStandingWrite`, `checkerCountersign`. |
| 2.4.11 | `frontend/src/App.js` | Modify | Route `/compliance/rulebook` → `ComplianceRulebookWritePage`. |

### §2.5 Frontend — Jest structural cells

| # | Test file | Cells |
|---|---|---:|
| 2.5.1 | `test_phase_8_b_5b_compliance_rulebook_write.test.js` (writer components) | 5 writer components × 2 render/interact cells = 10 |
| 2.5.2 | `test_phase_8_b_5b_countersign_action_button.test.js` | 4 (render-when-capacity + no-render-otherwise + click-wires-endpoint + feedback) |
| 2.5.3 | `test_phase_8_b_5b_owner_suspend_dialog.test.js` | 4 (opens + reason-required + submit-wires + closes) |
| 2.5.4 | `test_phase_8_b_5b_admin_read_only_view.test.js` | 3 (renders-read-only + owned-by-compliance-marker-verbatim + no-write-button) |
| 2.5.5 | `test_phase_8_b_5b_binding_copy_verbatim.test.js` | 4 (owned-by-Compliance marker text verbatim + §4.4 rule-sentence pattern + §4.5 tightening/loosening copy + middle-dot U+00B7 strict) |
| **Total** | | **25** |

### §2.6 Playwright chromium smokes

| # | Spec | Cells |
|---|---|---:|
| 2.6.1 | `compliance_rulebook_write_smoke.spec.ts` | 4 (page-renders + 3 writer variants POST → 202 pending) |
| 2.6.2 | `countersign_action_button_smoke.spec.ts` | 2 (button-render-when-capacity + click-transitions-to-effective) |
| 2.6.3 | `owner_suspend_workflow_smoke.spec.ts` | 2 (dialog-opens + submit-transitions-to-suspended) |
| 2.6.4 | `admin_compliance_read_only_retrofit_smoke.spec.ts` | 2 (compliance-classes-read-only + owned-by-Compliance-marker-visible) |
| **Total** | | **10** |

---

## §3. Band derivation (matrix-derived, cell-density-applied)

### §3.1 Cell count total

| Bucket | Cells |
|---:|---:|
| Backend Pytest (writers §2.3 + LB gates §2.2 + regression) | 21 + 17 + 2 = **40** |
| Frontend Jest structural (§2.5) | **25** |
| Playwright chromium (§2.6) | **10** |
| **Total cells** | **75** |

### §3.2 LoC derivation (matrix × cell-density per §1)

| Bucket | Cells | LoC/cell | Subtotal |
|---:|---:|---:|---:|
| Backend Pytest endpoint × auth × posture (§2.3) | 21 | 22 | 462 |
| Backend LB gates B5b-G1..G4 + RT-G1 (§2.2) | 17 | 35 | 595 |
| Backend regression (§2.3) | 2 | 22 | 44 |
| Frontend Jest writer-form structural | 10 | 28 | 280 |
| Frontend Jest banner button + suspend dialog + admin retrofit + binding copy | 15 | 16 | 240 |
| Playwright writer smokes | 4 | 48 | 192 |
| Playwright banner/suspend/admin-retrofit smokes | 6 | 32 | 192 |
| **Test LoC subtotal** | **75** | | **2,005** |
| Backend impl (3 writer endpoints × 80) | | | 240 |
| Backend impl (retention regression touches + shared helpers) | | | 40 |
| Frontend impl (5 writer components × 120) | | | 600 |
| Frontend impl (banner button augmentation 45 + owner-suspend UI 90 + admin read-only view 4 tiles × 35 = 140) | | | 275 |
| Frontend impl (ComplianceRulebookWritePage 100 + apiClient 40 + App.js routes 8) | | | 148 |
| **Impl LoC subtotal** | | | **1,303** |
| **Grand total (raw LoC)** | | | **~3,308** |

### §3.3 Owner-anchored band (Standing Correction matrix-enumerated)

**Anchored band at Stage A dispatch: `[2,800, 3,400]` raw LoC.**

Rationale:
- Bottom-of-band (2,800): 15% shave off the point-estimate accounting for reuse from Sub-stage 3 (checker infra is landed) + shared helpers not double-counted.
- Top-of-band (3,400): 3% cushion above point-estimate reflects the non-splittable pairing tax (compliance-write + B-4 retrofit in one commit even if writer variants scale unevenly).
- Point-estimate: 3,308 raw LoC (matrix-derived per §3.2).

### §3.4 Re-derivation trigger table

Per Owner projection-noise ruling: any ruling that reshapes cells RE-DERIVES the band, deterministically, using §1's stated rates. Examples:

| Ruling shape | Re-derivation direction |
|---|---|
| Owner adds a 4th compliance rule class | +7 backend cells + 3 Jest cells + 1 Playwright cell + 1 writer component (120 LoC) → +~350 LoC |
| Owner splits disclosure_thresholds into k_anonymity/l_diversity/DP-budget endpoints (3 separate routes) | +14 backend cells (2 × 7) + 2 writer components (240 LoC) → +~640 LoC |
| Owner removes source_standing from B-5b scope (deferral) | -7 backend cells - 1 writer component (120 LoC) → -~275 LoC |
| Owner adds an "explicit rule-change confirmation" prompt UI | +1 component (~50 LoC) + 2 Jest cells + 1 Playwright cell → +~130 LoC |

**Discipline preserved:** band is stop-and-judge, not a target. Miss with disclosure per Ruling 5.

---

## §4. Non-splittable pairing enforcement (Owner-binding)

Per Owner dispatch §2.3: **compliance-write enablement (§2.4.1–§2.4.5, §2.4.10, §2.4.11 + backend §2.1) + B-4 read-only retrofit (§2.4.9 + backend RT-G1 gate) land in ONE commit regardless of any split.** Write ownership never exists in both consoles or neither.

### §4.1 Baseline recommendation: ONE atomic commit

Recommended per Sub-stage 3 precedent (Ruling 5 verbatim: *"one atomic commit, no split, no band-widening"*). B-5b's ~3,308 LoC / 75 cells is comparable to Sub-stage 3's ~2,582 LoC / 101 cells; one atomic commit remains feasible.

### §4.2 Contingency: 2-sub-stage split proposal (if the matrix demands)

If the matrix is judged to exceed atomic-commit budget:

| Sub-stage | Contents | Non-splittable pairing survives? |
|---|---|---|
| **B-5b.1** (atomic-commit) | Compliance rulebook-write UI (§2.4.1–§2.4.5) + 3 new backend writer endpoints (§2.1) + B-4 read-only retrofit (§2.4.9) + retrofit gate RT-G1 (§2.2) + writer/read-only smokes (§2.6.1, §2.6.4) | ✅ YES — write enablement + admin read-only marker atomic. |
| **B-5b.2** (follow-up commit) | Countersign action button on `CounterSignBanner` (§2.4.6) + Owner-suspend workflow UI (§2.4.7 + §2.4.8) + banner-button/suspend smokes (§2.6.2, §2.6.3) | N/A — deferred-UI ruling (x) items; standalone commit. |

**Sub-stage 1 (B-5b.1) NON-NEGOTIABLES per Owner:**
- Compliance write UI + `POST /api/checker/initiate` wiring MUST include the B-4 retrofit + RT-G1.
- Any proposal violating this pairing is INVALID and gets flagged as a governance-semantic escalation.

**Decision rule (dev-autonomous per §7 discipline, disclosed at Stage A close):** if the point-estimate 3,308 LoC point-estimate is judged manageable in a single atomic commit (based on Sub-stage 3 precedent at 2,582 LoC), recommend **§4.1 baseline (one atomic commit)**. If Owner rules that atomic-commit budget is smaller, execute §4.2 split.

---

## §5. Escalation flags (B5b-E1..E5)

Enumerated per Standing Correction with authority-source citations + α/β/γ menu OR "cannot-be-menu, requires Owner semantic ruling".

### §5.1 B5b-E1 — Owner-suspend UI location on Master Admin surface

**Class:** owner-value contact (visual framing per Ruling 3 distinctness).

**Question:** Owner ruling 3 (Amendment G, Sub-stage 3) says *"owner-suspend is a distinct, ledgered action"*. On the Master Admin surface, where should the suspend action live?

**Authority-source language:** BCR v1.4.1 §3.11 (checker section) + UI Spec v2.1 §6.1 (Master Admin Home: *"Pending banner — Plain language, two backing classes: governance seams awaiting owner/compliance values, and items awaiting counter-signature (Section 8)"*).

**Options:**
- (α) Inline "Suspend" button next to each tightening item on `CounterSignBanner` (data-role="admin"). Matches banner's list pattern; keeps ONE surface for pending-item actions.
- (β) Dedicated Master Admin subsection "Tightenings in-flight" with per-item Suspend button. Physically separates from countersign work; makes the "distinct action" nature per Ruling 3 visually explicit.
- (γ) Separate route `/master-admin/tightening-controls` — full-page workflow. Heavier; matches "distinct, ledgered action" gravitas but adds navigation.

**Recommended:** (α) — matches Sub-stage 3's inline-on-banner posture; still visually distinct via button color/label ("Suspend by Owner" vs. "Countersign"). Owner ruling requested before B-5b dispatch.

### §5.2 B5b-E2 — Rulebook-write validation semantics (client-side vs. server-side)

**Class:** governance-semantic contact (Standing Correction pattern).

**Question:** Compliance-rulebook writers accept `from_value` + `to_value` per rule class. Should the frontend perform pre-check validation (e.g. "k-anonymity ≥ 2", "retention_window > 0") client-side before submit, OR delegate all validation to the server?

**Authority-source language:** UI Spec v2.1 §4.4 says *"Rendering reuses the established plain-language rule pattern (6.2 mechanics)"*. §6.2 says *"Commit paths honor the registry-bump discipline: a committable rule writes a new versioned file server-side, recorded and reversible"*. Silent on client-side pre-check.

**Options:**
- (α) Server-side only. Frontend renders server-returned error verbatim. Matches "the surface is never a bypass" §6.2 discipline; keeps single source of truth.
- (β) Client-side pre-check on numeric ranges + basic string validation, THEN server-side final validation. UX-friendlier; keeps errors immediate.
- (γ) Client-side pre-check only on parseability (is-number, non-empty); all semantics validated server-side. Compromise position.

**Recommended:** (α) — matches the "surface is never a bypass" doctrine. Any client-side check risks becoming stale relative to server registry. Owner ruling requested.

### §5.3 B5b-E3 — disclosure_thresholds sub-class endpoint shape

**Class:** frozen-contract-adjacency + governance-semantic.

**Question:** `disclosure_thresholds` covers k-anonymity + l-diversity + DP-budget per UI Spec v2.1 §4.4 line 80. Are these:
- (α) ONE endpoint `POST /api/compliance/disclosure_thresholds` with `{class: "k_anonymity" | "l_diversity" | "dp_budget", value: ...}` (uses a Literal for `class` param — this is a REQUEST parameter, NOT a frozen contract field, so no §7.1.β trap).
- (β) THREE separate endpoints `POST /api/compliance/disclosure/k_anonymity` + `.../l_diversity` + `.../dp_budget`.
- (γ) ONE endpoint with a `disclosure_type: string` constrained-str + JSON registry (E1.γ pattern from consequence_classes.py).

**Authority-source language:** UI Spec v2.1 §4.4 line 80 groups all three under "disclosure thresholds (k-anonymity, l-diversity, differential-privacy budget)" — treats them as ONE compliance rule class.

**Recommended:** (γ) — matches Sub-stage 3's E1.γ constrained-str pattern + `consequence_class.v0.json` precedent. Extending the disclosure sub-classes then follows the same registry-bump discipline as `data_class_registry v0→v1` (Ruling 4). Owner ruling requested.

### §5.4 B5b-E4 — Pending-checker-request behavior across B-4 retrofit landing

**Class:** governance-semantic + Cannot-be-α/β-choice, requires Owner semantic ruling.

**Question:** At the moment B-4 retrofit lands (compliance rule classes go read-only on Administration), what happens to any in-flight checker request initiated BY an admin (via legacy Admin routes that no longer exist post-retrofit)? Two edge cases:
- (a) An admin-initiated pending_delay tightening on a compliance class. The retrofit removes Admin's write authority; does the pending state stall, cancel, or continue?
- (b) An admin-initiated pending_counter_sign dual_control request on a compliance class. Post-retrofit, the initiator role's authority context has changed.

**Authority-source language:** BCR v1.4.1 §3.13 RT-R2 line 291 says *"Lands with B-5b (the console that receives the write ownership) so the move is atomic - write capability never exists in neither console nor both"*. Silent on in-flight-request behavior.

**Cannot-be-α/β choice** — this is a governance-semantic ruling like R-3 (state-machine corrections). Requires explicit Owner ruling on:
- Do we cancel pending admin-initiated compliance-rule checker requests at retrofit landing?
- Do we let them run through to effective (grandfathering)?
- Do we require Owner-suspend on all admin-initiated compliance-rule pending items?

**Preliminary observation (not a proposal):** at Sub-stage 3 close, ZERO admin-initiated compliance-rule checker requests exist in production (checker just landed; no writes yet). Practically, this is a null population at B-5b landing time. But the doctrine needs explicit ruling.

### §5.5 B5b-E5 — Non-splittable pairing implementation

**Class:** governance-semantic + Cannot-be-α/β-choice, requires Owner semantic ruling if the matrix overrun is severe.

**Question:** Per Owner dispatch §2.3, compliance-write enablement + B-4 read-only retrofit MUST land in one commit. §3.2 point-estimate is 3,308 LoC. Sub-stage 3 landed 2,582 LoC in one atomic commit. B-5b is ~28% larger.

**Options if the matrix at execution-time exceeds atomic-commit budget:**
- (a) Execute per §4.2 (2-sub-stage split): B-5b.1 (write + retrofit atomic) + B-5b.2 (banner button + suspend UI).
- (b) Widen the atomic-commit budget interpretation. NOT recommended (matches Ruling 5's rejection of band-widening).
- (c) Owner ruling to strip a specific feature from B-5b scope (e.g. defer lawful_basis_registry writer to a later mini-phase).

**Preliminary observation:** the split per §4.2 preserves the Owner-binding pairing constraint AND the deferred-UI ruling (x) items are the natural split-off boundary (they were originally deferred anyway). Recommended posture at execution: attempt §4.1 baseline (one atomic commit); if the actual delivery hits ≥ 3,500 LoC or ≥ 90 cells during implementation, escalate to §4.2 split before committing.

**Discipline note:** this escalation is NOT a band-widening request. The band `[2,800, 3,400]` stays fixed; if actual delivery exceeds the top, the discipline is either §4.2 split or Owner-ruled scope strip — NEVER a band restatement mid-execution.

---

## §6. Sub-stage 3 final-acceptance footer (rider draft for B-5b's first execution commit)

Per standing rider pattern: Sub-stage 3 acceptance footer rides B-5b's first execution commit. Draft below; DO NOT append this turn.

### §6.1 Footer text (to append at B-5b execution commit to `/app/docs/close_reports/phase_8_seam_3_sub_stage_3.md`)

```markdown
---

## §10. Sub-stage 3 final-acceptance footer (rider landed at B-5b first execution commit)

**Owner acceptance (2026-07-07, verbatim):**
> Close 994d2b40…: ACCEPTED. Seam 3 complete — all three sub-stages landed, E2 gate retired on evidence, §12.2 closed by named gate, parity 26 byte-identical, +3.3% disclosed per Ruling 5. Final-acceptance footer per standing pattern.

**Landing commit hash (Sub-stage 3 atomic):** (recorded at Sub-stage 3 landing; supplied by Owner post-push).
**Push queue status at acceptance:** Owner pushing six accepted closes plus salvage directory. Owner-side operation; no `e1_dev` action.
**Follow-up surface (Phase 8 completion):** Phase 8 Stage B-5b closes the deferred-UI items surfaced by Sub-stage 3 (countersign action button on `CounterSignBanner`; owner-suspend workflow UI on Master Admin) plus the compliance-rulebook write UI (§4.4-4.5) and the B-4 read-only retrofit (§3.13 / RT-R2). Non-splittable pairing: compliance-write enablement + B-4 retrofit land in one commit.
**Rider landing commit:** B-5b first execution commit (this rider).
**Standing Rule v3 preservation:** footer appended at rider commit per pattern; close report §1–§9 UNTOUCHED.

*Sub-stage 3 recorded as FINAL ACCEPTANCE. Seam 3 (Sub-stages 1 + 2 + 3) complete. Phase 8 completion path: B-5b remains.*
```

### §6.2 Rider landing discipline

- Footer is APPENDED (not rewritten) after §9 of the close report.
- Existing §1–§9 content untouched (byte-identical).
- Close-report SHA CHANGES post-append; the new SHA is recorded in the B-5b close report and in rule2_accounting.json.
- No other close report is modified.

---

## §7. Ready-to-dispatch posture

- All BCR §3.6B requirements (B5b-R1..R3) matrix-enumerated as backend deliverables §2.1–§2.3 + frontend deliverables §2.4.
- All BCR §3.6B gates (B5b-G1..G4) matrix-enumerated at §2.2 (17 cells across 4 gates).
- BCR §3.13 retrofit RT-R1 + RT-R2 + RT-G1 matrix-enumerated at §2.2 (RT-G1: 1 cell) + §2.4.9 (`AdminComplianceReadOnlyView.jsx`).
- Owner deferred-UI ruling (x) items matrix-enumerated: countersign button §2.4.6 + owner-suspend UI §2.4.7-§2.4.8.
- Non-splittable pairing enforced at §4 with contingency §4.2 (survives split).
- Cell-density assumption stated at §1 per Owner projection-noise ruling.
- Band anchored at §3.3 `[2,800, 3,400]` matrix-derived, no padding.
- 5 escalations enumerated at §5 (B5b-E1..E5); E4 + E5 are cannot-be-α/β choices.
- Frozen contract parity 26 preserved (no touches; writer endpoints reuse existing `NorthenaLedgerRow_v1` + vestigial-by-ruling `artifact_type` pattern from Sub-stage 3).
- Standing state-conflict anti-rule preserved (state conflicts use 403; no 409 anywhere).
- E7 middle-dot glyph strict on all binding copy (asserted via Jest + Playwright per Sub-stage 3 template).
- Sub-stage 3 final-acceptance footer drafted at §6 for rider-landing at B-5b execution first commit.

**READY TO DISPATCH POST OWNER RULINGS ON B5b-E1/E2/E3 (α/β/γ menus) + B5b-E4/E5 (governance-semantic rulings) + ratification of §3.3 anchored band + §4 non-splittable pairing implementation.**

═══════════════════════════════════════════════════════════════════

*End of B-5b Stage A proposal. Design-only per Owner dispatch. Standing Rule v3: full text on disk. Reply is SHA + structural TOC + escalations + band + rider draft. Owner ratification of Stage A + B5b-E1..E5 required before B-5b execution dispatch.*
