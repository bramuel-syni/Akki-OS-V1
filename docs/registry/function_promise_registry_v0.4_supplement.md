# Function & Promise Registry — v0.4 Supplement (G-10/G-7 PROMOTE)

**Purpose:** carries this ruling's (G-10/G-7 PROMOTE · docs/rulings/g10_g7_promote_2026-07-14.md · atomic commit alongside IF-1 reconciliation) own R4 reflexive Registry rows, landed per Owner and **governance §14** (additive-supplement discipline).

**Source lock:** primary source-of-truth `/app/docs/registry/function_promise_registry_v0.md` remains byte-identical at SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0`. Prior supplements byte-identical: `v0.1_supplement` `2822f99e0c20da6f8d02c1f33233965c90df37aeb6939e711da8df2ebd991092` · `v0.2_supplement` `25c5dd5ac515b34a41584dd2b4ba4eab20eb0ae5d40d9022320761056555b79a` · `v0.3_supplement` `8d4cd2ed9c4e802944517908424ba2297ac3b4dd5e0d2a8e6d54f6042e64a8e4`.

**Combined source per §14:** `(v0.md + v0.1_supplement + v0.2_supplement + v0.3_supplement + v0.4_supplement)` ↔ `registry.yaml` — one set. MRR-G3 round-trip attests transparent extension to N supplements (path-list drives the check).

**Doctrine reference:** Registry Doctrine v1.0 §3.2 schema (11 mandatory fields) · §3.3 R4 · §14 additive-supplement pattern.

**Landed:** 2026-07-14 (atomic G-10/G-7 PROMOTE commit alongside IF-1 reconciliation).

---

## §S1. R4 reflexive rows — Trace surface promotion (2 rows · §3.2 schema)

Closes G-7 (SolvaTrace three-lens rendering surface commitment) and G-10 (frontend /legacy/* disposition) simultaneously: the three-lens Trust Receipt lifts out of the archived `/legacy/*` tree and mounts at public `/trace` + `/trace/:traceId`; the AppShell chrome and the seven other legacy pages retire whole at the same ruling.

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `rms.frontend.trace_receipt_page_promoted_public_route` (G-7 close) | Named surfaces (Frontend UI · reflexive) | Built to attest the SolvaTrace three-lens rendering surface (§5 Spec) is a live-visible public route: `src/pages/trace/TraceReceiptPage.js` exists on-disk AND `src/App.js` imports it from `./pages/trace/TraceReceiptPage` AND declares both `<Route path="trace">` and `<Route path="trace/:traceId">`. The three-lens sections (`trace-ledger-section` · `trace-solva-section` · `trace-plans-section` · `trace-registry-section`) render the envelope returned by `GET /api/northena/trace/{traceId}`; back-link resolves to Ask Console at `/` (single-ingress per UI Spec §3.1). | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` + `frontend/e2e/trace_smoke.spec.ts::trace_receipt_page_renders_three_lens_at_promoted_public_route` | jest static-grep + playwright DOM assertion | 1 cell · ms class | apiClient.traceLens + useApi hook + LedgerTable/ClassBadge/StatusBadge components | 1 · Deterministic | Owner |
| `rms.frontend.legacy_shell_retired` (G-10 close) | Named surfaces (Frontend UI · reflexive) | Built to attest the archived `/legacy/*` tree and its AppShell chrome are gone: `src/legacy/` directory does NOT exist AND `src/components/AppShell.js` does NOT exist AND `src/App.js` no longer declares `<Route path="legacy">` block AND no in-tree import references either `./legacy/pages/` or `./components/AppShell`. The G-10 disposition ("evidence at IF-1 close → OWNER decision") is discharged by this ruling. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` | jest static-grep (fs-negative + import-negative + Route-block-negative) | 1 cell · µs class | frontend build clean · yarn build passes · legacy tree fully removed | 1 · Deterministic | Owner |

**Row count:** 2 promote/retire reflexive rows.

---

## §S2. R4 reflexive rows — Legacy page shave attestations (7 rows · §3.2 schema)

Per Owner G-10 close: for each of the seven retired legacy pages, an fs-negative test attests the module no longer exists AND no live consuming route references it. All seven are covered by a single mechanical gate that iterates the `LEGACY_PAGE_NAMES` set (`test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js`); rows enumerate the individual files per §3.2 schema granularity.

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `deviation.shave.frontend_landing_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/LandingPage.js` no longer exists AND `src/App.js` no longer imports it; nested `<Route index element={<LandingPage/>}>` under `/legacy/*` retired at G-10 close. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 1) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_operator_dashboard` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/OperatorDashboard.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 2) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_runs_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/RunsPage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/runs` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 3) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_run_detail_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/RunDetailPage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/runs/:runId` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 4) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_discipline_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/DisciplinePage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/discipline` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 5) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_engines_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/EnginesPage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/engines` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 6) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_compose_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/ComposePage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/compose` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 7) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |

**Row count:** 7 legacy-page shave-attestation rows.

**Note on AppShell chrome:** the retirement of `src/components/AppShell.js` (only-consumer-was-legacy) is folded into row `rms.frontend.legacy_shell_retired` (§S1) rather than minted as a separate row, since the AppShell has no distinct governor promise beyond "carry the /legacy/* nested outlet"; §S1 row's fs-negative already covers it explicitly.

---

## §S3. Promise attribution notes

Zero new promises introduced (Owner-explicit conservation posture held; G-10/G-7 PROMOTE does not mint promises, it discharges G-7 by making the three-lens rendering surface live-visible AND discharges G-10 by shaving the archived tree).

- **PROM-S1-frozen-wire-contract** (v0.md §2) — G-7 close (three-lens public route wire-contract) + G-10 close (retired shell wire-contract negative) + 7 shave rows (dead-surface fs-negatives are wire-contract integrity checks) = 9 rows.

D7 respected · zero candidate promises minted · conservation-not-authorship posture held.

---

## §S4. Standing consequence attest (governance §14 · MRR-E4 β)

This supplement instantiates the pattern ruled in **governance §14** applied to G-10/G-7 PROMOTE: additive supplement beside locked source. v0.md byte-identical at SHA `598a7ad4…` · v0.1_supplement byte-identical at SHA `2822f99e…` · v0.2_supplement byte-identical at SHA `25c5dd5a…` · v0.3_supplement byte-identical at SHA `8d4cd2ed…`. v0.4_supplement is new sibling. MRR-G3's round-trip operates over `(v0.md + v0.1_supplement + v0.2_supplement + v0.3_supplement + v0.4_supplement)` ↔ machine form as one set.

═══════════════════════════════════════════════════════════════════

*End of v0.4 supplement. 2 G-10/G-7 promote/retire rows + 7 legacy-page shave-attestation rows = 9 R4 reflexive rows. Prior source-of-truth files byte-identical. Standing Rule v3 · on-disk canonical.*
