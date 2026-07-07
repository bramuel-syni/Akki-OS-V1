# Phase 8 Seam 3 Sub-stage 1 — Close Report

**Landing date:** 2026-07-07
**Sub-stage:** Phase 8 Seam 3 Sub-stage 1 — Refusal-family ledger wire-up (I1–I6) + coverage marker (E3.β query-time) + Compliance Console refusals-card rider.
**Authority chain (superseding B-5a close SHA `c48672b4…`):**

- Build brief (post-Amendment-F): `/app/docs/build_briefs/phase_8_seam_3_sub_stage_1.md`
- Rulings record (post-§10 append): `/app/docs/rulings/seam_3_stage_a_e1_to_e7.md`
- Registry (post-R-4 attribution-note fix): `/app/backend/services/compliance/refusal_families.v0.json`
- Grep census (unchanged): `/app/docs/recon/refusal_terminal_emission_site_grep_2026_07_06.md` SHA `a6697d82191500220cf2d56e1787ed979d2e6b9546ee776ca1b3c9f0496029d1`
- BCR v1.4.1 (unchanged): `/app/docs/mandates/RMS_Build_Completion_Requirements_v1_4.md` SHA `ce5206c9e244fe58edb6824f785077c1c835bdf3f5b347f6a4fb98c036212524`
- Conformance map (unchanged): `/app/docs/close_reports/phase_8_conformance_map.md` SHA `e747a0f6ee815b003d4962dac515b0743451747b1ef4812fa824e6cbe98874e7`

Owner rulings pre-carried: E1–E7 from §1–§9 of rulings record; R-1 through R-6 from §10.

Standing Rule v3: reply body is a header row of numbers + one-line disposition per Rule 6; matrix, files, and prose live on disk in this file.

---

## §1. Sub-stage 1 landing SHAs

- **Build brief (Amendment F applied) SHA-256:** `0ca3215d72b65bf91ae549246d36e116a630b8675aa8ae86ec576600e47770c2`
- **Rulings record (§10 appended) SHA-256:** `7c2b61f1e739c3f88689bf7ec235a1f259655d539fe9fc1babd3a1f1d30f6653`
- **`refusal_families.v0.json` (R-4 note-corrected) SHA-256:** `1cad3562d31be878296878c6a67e1643349f71944ced05caada90cc93e2e16ba`
- **This close-report SHA-256:** *(self-referential; recompute after Owner acceptance = `sha256sum /app/docs/close_reports/phase_8_seam_3_sub_stage_1.md` post-amend; recorded in reply header row)*
- **Grep census SHA-256:** `a6697d82191500220cf2d56e1787ed979d2e6b9546ee776ca1b3c9f0496029d1` (unchanged).
- **Landing commit hash:** `b7df53ed1fc1acc2412ae5badfe43803c404a849` (amended to include this SHA-fill; Owner pushes).

## §2. Test-matrix enumerated roster (Standing Correction: cells × postures × cases)

### §2.1 Backend Pytest — `tests/invariants/test_phase_8_seam_3_sub_stage_1.py`

**File total: 22 cases** (per grep-verified §7 disposition + auxiliary units):

| Section | Case name | Kind | Endpoint × posture × case |
|---|---|---|---|
| §A | `test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit[i1_no_defensibility_floor-composition_below_floor-no_defensibility_floor]` | LB gate (R-1) exercise fixture I1 | writer × happy × emits |
| §A | `[i2_no_lawful_basis-composition_below_floor-no_lawful_basis]` | LB gate I2 | writer × happy × emits |
| §A | `[i3_composition_below_floor_sync-composition_below_floor-composition_below_floor]` | LB gate I3 | writer × happy × emits |
| §A | `[i4_composed_conclusion_sync-composition_below_floor-composition_below_floor]` | LB gate I4 | writer × happy × emits |
| §A | `[i5_async_composed_refusal-composition_below_floor-composition_below_floor]` | LB gate I5 | writer × happy × emits |
| §A | `[i6_async_admission_refusal-admission_refusals-unrecognized_reason]` | LB gate I6 | writer × happy × emits |
| §A | `test_refusal_terminal_lb_gate_aggregate_regression` | LB gate aggregate (R-1) | reader × happy × aggregate |
| §B | `test_emit_refusal_ledger_row_rejects_unknown_family` | unit — family validation | writer × unknown-family × raises |
| §B | `test_emit_refusal_ledger_row_rejects_converge_stage` | unit — stage validation | writer × converge-forbidden × raises |
| §B | `test_emit_refusal_ledger_row_pins_family_key_over_extra` | unit — pinned-key discipline (E1.γ.1) | writer × malicious-override × pins registry family |
| §B | `test_emit_refusal_ledger_row_registry_contains_unclassified_per_r_3` | unit — R-3 unclassified family | writer × unclassified × registered + renderable |
| §C | `test_coverage_marker_empty_state_honest_note` | coverage marker | reader × empty × honest-note |
| §C | `test_coverage_marker_populates_from_pinned_key_rows` | coverage marker | reader × populated × surfaces family |
| §C | `test_coverage_marker_uses_query_time_earliest_per_family` | coverage marker (E3.β) | reader × earliest-timestamp × correct |
| §C | `test_coverage_marker_categorises_by_seam_3_boundary` | coverage marker | reader × cross-boundary × correct bucket |
| §D | `test_refusals_coverage_no_token_401_auth_missing` | router auth | GET × no-token × 401 |
| §D | `test_refusals_coverage_wrong_role_403_auth_scope_insufficient` | router auth | GET × operator-role × 403 |
| §D | `test_refusals_coverage_dpo_role_200_shape` | router auth + shape | GET × dpo-role × 200 |
| §D | `test_refusals_coverage_admin_role_200` | router auth | GET × admin-role × 200 |
| §E | `test_r5_no_duplicate_ledger_rows_across_emission_and_transition` | R-5 idempotency | async × retry × dedup |
| §F | `test_r4_registry_admission_refusals_note_matches_classifier` | R-4 registry-note fix | registry × note × classifier-aligned |
| §G | `test_g_no_409_in_sub_stage_1_diff` | 409 self-audit | diff-scan × static × zero-hits |

Backend Pytest totals: **847 → 869 (+22 net; all green)**.

**Byte-identity guardrail updates** (Sub-stage 1 legitimate amend per Owner Amendment F):
- `test_dispatch_v0_untouched.py::test_v0_service_1_service_byte_identical` — SHA constant refreshed to `4a453e30…` (from pre-Phase-2 `05e905ed…`); provenance comment cites R-1..R-6.
- `test_v0_paths_byte_identical_after_4a.py`, `test_v0_paths_byte_identical_after_4b.py` — `service.py` SHA refreshed to `4a453e30…` with provenance comment.
- `test_v0_paths_byte_identical_after_5b/6b/7b_1.py`, `test_phase_7_stage_b_2/3_wizard.py` — synthesis-lines slice index moved [315:321] → [329:335]. Content SHA `d2e72653…` byte-identical (Owner Q4.c protection preserved; only file position shifted after I4 wire-up added ~15 lines).
- `test_service_1_refusal_envelope.py::test_no_lawful_basis_refusal_returns_flat_outcome_refused` — pre-composition-refusal `_write_delta` expectation flipped from 0 → 1 (the pinned refusal-family ledger row is the coverage substrate this sub-stage exists to produce). Provenance comment cites R-1.
- `docs/mandates/MANIFEST.md` — BCR v1.4.1 hash refreshed from `d1f49bc5…` (pre-E7) to `ce5206c9…` (post-E7 middle-dot). **Pre-existing drift from Owner E7 amendment on 2026-07-06; not introduced by Sub-stage 1; landed here as housekeeping per §4.3 "everything else, dev handles autonomously."**

### §2.2 Frontend Jest — `src/__tests__/ui_spec_v1/test_phase_8_seam_3_coverage_marker.test.js`

**File total: 6 cases** (structural contract of `RefusalsCoverageMarker`):

| Case | Kind | Cell × posture × case |
|---|---|---|
| `MIDDLE_DOT export IS the U+00B7 codepoint verbatim (not a hyphen)` | constant | component × exported × equals 0x00B7 |
| `loading state renders coverage-marker-loading with middle-dot` | render | component × loading × middle-dot |
| `load-error state renders coverage-marker-load-error with middle-dot` | render | component × error × middle-dot |
| `empty coverage renders honest empty-state note (not silence)` | render (R-3) | component × empty × honest-note |
| `populated seam-3 families render since-date with middle-dot` | render | component × populated × middle-dot + date |
| `all 4 registry families (incl. R-3 unclassified) render if present` | render (R-3) | component × 4 families × surfaces all |

**Also**: `test_phase_8_b_5a_compliance.test.js` mock updated with `complianceRefusalsCoverage` shim (empty-state body) to keep 22 pre-existing cases green.

Frontend Jest totals: **92 → 98 (+6 net; all green across 14 suites)**.

### §2.3 Playwright chromium — `e2e/compliance_coverage_marker_smoke.spec.ts`

**File total: 2 smokes**:

| Case | Kind | Cell × posture × case |
|---|---|---|
| `test_coverage_marker_renders_middle_dot_glyph_verbatim` (named gate per Amendment F §5) | e2e | rider × populated × asserts `\u00B7` glyph specifically, forbids hyphen substitute in seam-3 line + per-family line |
| `coverage_marker_empty_state_renders_honest_note_with_middle_dot` | e2e | rider × empty × asserts `\u00B7` + no hyphen surrogate |

Playwright chromium totals: **26 → 28 (+2 net; all green)**.

## §3. R-6 WIP-checkpoint documentation

**`a33d9eb = pre-authorization WIP checkpoint, interrupted by compaction; landing commit is b7df53e`** — recorded per R-6 obligation.

## §4. Rule 2 accounting — LoC delta

- **Working-tree modifications** (23 files, backend + frontend + tests + docs + build artifacts): +308 / −28 = **+280 net**.
- **New source files** (untracked, all additions):
  - `backend/tests/invariants/test_phase_8_seam_3_sub_stage_1.py`: 529 LoC (22 Pytest cases).
  - `frontend/e2e/compliance_coverage_marker_smoke.spec.ts`: 110 LoC (2 Playwright smokes).
  - `frontend/src/__tests__/ui_spec_v1/test_phase_8_seam_3_coverage_marker.test.js`: 122 LoC (6 Jest cases).
  - `frontend/src/pages/compliance/RefusalsCoverageMarker.js`: 119 LoC (rider component).
  - Subtotal: 880 LoC.
- **Total Sub-stage 1 landing LoC**: **+1160 net** (+280 modified, +880 new).

**Composition:**
- Backend wire-up (I1–I6 via `emit_refusal_ledger_row` at 4 files): ~90 LoC.
- Backend registry attribution-note fix (R-4): ~2 LoC (docstring content).
- Backend router endpoint (`GET /api/compliance/refusals_coverage`): ~20 LoC.
- Frontend apiClient shim: 7 LoC.
- Frontend ComplianceHomePage rider wire-up: 9 LoC net.
- Frontend `RefusalsCoverageMarker.js` component: 119 LoC.
- Backend Pytest matrix (§A–§G, 22 cases): 529 LoC.
- Frontend Jest structural (6 cases): 122 LoC.
- Playwright chromium (2 smokes): 110 LoC.
- Byte-identity guardrail updates (SHA refresh + slice-index shift + provenance comments): ~30 LoC across 8 test files.
- Doc updates (build brief 7 fold points, rulings §10 append, MANIFEST hash refresh): ~150 LoC.

**Owner-anchored velocity band from B-4 close narrative:** 1,300–1,800 raw LoC (baseline anchor for Phase 8 sub-stages).

**Overage disposition:** Sub-stage 1 raw ≈ **1,160 net LoC** → **INSIDE band** (below top of 1,800). No `LOC-ceiling-breach` escalation. Enumerated composition above shows the four largest cells: Pytest matrix (529L) is honest matrix-enumerated coverage over 6 emission sites × 3 posture classes plus registry + router + R-4 + R-5 + 409 audit; component (119L) + Jest (122L) + Playwright (110L) satisfy first-commit gating in the same landing commit.

## §5. Honest-cost report on query-time β

**Measurement:** `compose_coverage_marker()` latency at Sub-stage 1 landing, against Mongo `NORTHENA_LEDGER_COLLECTION` in the local dev container (dataset size at time of test: **9,893 rows** in NORTHENA_LEDGER_COLLECTION, of which 22 test-source rows were introduced during matrix run and cleared by teardown).

- **compose_coverage_marker() end-to-end latency:** **4.66 ms** (single async call, freshly emitted test row present).
- **Dataset shape at measurement:** live dev-cluster ledger with ~10k rows total; refused-decision subset is a small minority; per-family `find_one(sort=at ASC)` completes in single-digit ms without any index.

**Disposition:** **No cost problem observed.** Honest-cost obligation satisfied without pre-emptive materialization or index (E3.β mandate + Amendment E preserved).

**Standing note for Sub-stage 2/3:** if a future phase raises ledger row count materially, the per-family `find_one(sort=at:1)` query is the honest place to observe stress, and Owner will be surfaced via a fresh honest-cost report — NOT pre-optimized without evidence.

## §6. 409 self-audit

**No HTTP 409 introduced by Sub-stage 1 diff.** Verified via `test_g_no_409_in_sub_stage_1_diff` (§G above) — static scan of the 9 Sub-stage-1 diff files for `\b409\b` literal outside comments and docstrings. Zero hits.

## §7. yarn.lock disposition

**Folded into landing commit.** Rationale: the working-tree `frontend/yarn.lock` +26L delta pre-existed Sub-stage 1's execution (surfaced in the state-verification pass §3.4 as source-not-identified). No dev-side `yarn add` was executed in this sub-stage's execution. Folding it in preserves the lockfile's integrity relative to `package.json`; dropping it would leave a working-tree phantom the next dev run would surface anyway. First-commit gate cleanliness prefers folding.

## §8. Sub-stage 2 preconditions surfaced during Sub-stage 1 build

- **Sub-stage 2 (authorized-deletion path):** requires the same `emit_refusal_ledger_row` canonical writer (already landed) and the `refusal_families.v0.json` registry (already landed). Sub-stage 2's own family attribution (per Stage A §4.2) must be verified against R-3's "unclassified" fallback discipline before Sub-stage 2's LB gate parametrisation is decided.
- **Sub-stage 3 (§8 consequence-class checker):** the checker's data-source is `NORTHENA_LEDGER_COLLECTION` with the pinned `stamp_audit["refusal_family"]` key. Sub-stage 1's landing establishes this key as invariant (R-1). Sub-stage 3 can enumerate consequence classes against the four registry families (admission_refusals / composition_below_floor / outer_gate_refusals / unclassified) without further schema work.
- **Registry `unclassified` family** (R-3): now surfaceable on the Compliance Console rider. If Sub-stage 2 or Sub-stage 3 produces any `unclassified` refusal-terminal row, the honesty banner is already wired.
- **Byte-identity guardrail baseline** (post-Sub-stage-1): `service.py` SHA `4a453e30…`, `composed_conclusion.py` synthesis-slice at `[329:335]`. Sub-stage 2's authorized-deletion path may touch `service.py` again — the guardrails now anchor to Sub-stage 1's landing SHA and will fire on any Sub-stage 2 drift outside Owner-authorised scope.
- **`emit_ledger_terminate_refused` dead stub** at `services/service_1/async_state.py:245-253` remains BC-preserved (E4 migration docstring only). Sub-stage 2 does NOT require touching it. If a future phase ever resurrects that stub, R-1's data-shape invariant will fire on any row produced without a pinned `refusal_family`.

## §9. Standing E-rulings self-audit

- **E2** (retention endpoint): NOT exercised — Sub-stage 2 territory.
- **E5** (409 anti-rule): confirmed — no HTTP 409 introduced (§6 self-audit).
- **E7** (middle-dot glyph): Playwright + Jest gates assert `\u00B7` explicitly.
- **E4** (dead-stub migration): docstring-only on `emit_ledger_terminate_refused`, body byte-identical (grep-verified).
- **R-1** (data-shape LB gate): landed as `test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit` + aggregate = 7 cases + auxiliary units.
- **R-2** (C2/C6 stay un-wired): confirmed — grep of `emit_refusal_ledger_row` call sites shows I1–I6 only.
- **R-3** (`unclassified` registered): confirmed — `VALID_REFUSAL_FAMILIES` contains `unclassified`; frontend rider renders it.
- **R-4** (registry-note corrected): landed at `refusal_families.v0.json` admission_refusals description; classifier untouched; §F test asserts the fix.
- **R-5** (emit before transition, idempotent): landed in `async_worker._process_one` for I5 + I6 with `_refusal_row_exists_for_objective` dedup helper; §E test asserts.
- **R-6** (WIP checkpoint doc): landed above (§3).

## §10. Frozen contracts + snapshots parity

**26 frozen contracts + 26 snapshots** untouched. Parity preserved. Contract-snapshot map at `test_frozen_contract_snapshot_parity.CONTRACT_TO_SNAPSHOT` unchanged.

## §11. Test-file inventory (net-new + modified)

**Net-new** (4 files, 880 LoC):
- `backend/tests/invariants/test_phase_8_seam_3_sub_stage_1.py`
- `frontend/src/__tests__/ui_spec_v1/test_phase_8_seam_3_coverage_marker.test.js`
- `frontend/e2e/compliance_coverage_marker_smoke.spec.ts`
- `frontend/src/pages/compliance/RefusalsCoverageMarker.js`

**Modified backend/routers** (6 files):
- `backend/services/compliance/refusal_families.v0.json` (R-4 attribution-note fix, no version bump)
- `backend/services/service_1/service.py` (I1 + I2 + I3 wire-up)
- `backend/services/service_1/composed_conclusion.py` (I4 wire-up)
- `backend/services/service_1/async_worker.py` (I5 + I6 wire-up + `_refusal_row_exists_for_objective` R-5 dedup helper)
- `backend/services/service_1/async_state.py` (E4 migration docstring only; body byte-identical)
- `backend/routers/compliance.py` (GET /api/compliance/refusals_coverage endpoint)

**Modified frontend** (3 files):
- `frontend/src/apiClient.js` (`complianceRefusalsCoverage` shim; +7 LoC)
- `frontend/src/pages/compliance/ComplianceHomePage.js` (rider wire-up; +9 LoC net)
- `frontend/src/__tests__/ui_spec_v1/test_phase_8_b_5a_compliance.test.js` (mock shim for coverage endpoint)

**Modified byte-identity guardrails** (8 files; provenance comments carry R-1..R-6 citation):
- `backend/tests/invariants/test_dispatch_v0_untouched.py`
- `backend/tests/invariants/test_v0_paths_byte_identical_after_4a.py`
- `backend/tests/invariants/test_v0_paths_byte_identical_after_4b.py`
- `backend/tests/invariants/test_v0_paths_byte_identical_after_5b.py`
- `backend/tests/invariants/test_v0_paths_byte_identical_after_6b.py`
- `backend/tests/invariants/test_v0_paths_byte_identical_after_7b_1.py`
- `backend/tests/invariants/test_phase_7_stage_b_2_wizard.py`
- `backend/tests/invariants/test_phase_7_stage_b_3_wizard.py`

**Modified functional gate** (1 file; provenance comment carries R-1 citation):
- `backend/tests/invariants/test_service_1_refusal_envelope.py` (`_write_delta == 1` per R-1)

**Modified doc/manifest** (5 files):
- `docs/build_briefs/phase_8_seam_3_sub_stage_1.md` (Amendment F 7 fold points)
- `docs/rulings/seam_3_stage_a_e1_to_e7.md` (§10 R-1..R-6 append)
- `docs/mandates/MANIFEST.md` (BCR v1.4.1 hash refresh; pre-existing E7 drift, housekeeping)
- `backend/services/compliance/refusal_families.v0.json` (R-4)
- (this close report is new)

## §12. Standing Rule v3 discipline

- All rulings, briefs, close reports, and rationale live on-disk in this file tree; agent's reply body carries only header numbers + one-line dispositions.
- No inline code paste in reply; no inline verbatim policy text outside authorised verbatim-reads.
- Landing commit hash + all four canonical SHAs (build brief, rulings, registry, close report) populate the reply header row.
