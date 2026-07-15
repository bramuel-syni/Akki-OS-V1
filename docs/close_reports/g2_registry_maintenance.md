# Close Report · G-2 Registry Maintenance Turn · 2026-07-14

**Authority:** Owner-ratified via ruling `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md` (SHA `c7ce185735b50c08944a908c10b040428fb10ae8d397435b7758c5b03870e85a`).
**Predecessor Stage A:** `docs/stage_a_proposals/g2_registry_maintenance_stage_a.md` (SHA `81b6f46f7466b0d8aaee383913cfad70ea94eaa5dc6977bc107eca29535996dd`).
**Governance stack:** Standing Rule v3 · Registry Doctrine v1.0 · Tiered-Ruling Model §14 (additive-supplement clause) · Tiered-Ruling Part IV §16 (D-10 corrective standing practice) · SQ-E1 γ · D-11 · D-7.

---

## §1. v1 consolidated Registry + machine re-pin

| Item | Value |
|---|---|
| **Path** | `/app/docs/registry/function_promise_registry_v1.md` |
| **SHA-256** | `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a` |
| **Line count** | **671** raw lines |
| **Byte-identity attest (RM-E1 α)** | **PASS** · 0 drift findings · every promise-text row from v0.md + v0.1..v0.5 byte-identical in v1 body (machine-enforced by `backend/tests/registry/test_registry_v1_consolidation_byte_identity.py`) |
| **Fold order** | v0.md header replaced by v1 header · v0.md body verbatim · v0.1 §S1 rows · v0.2 §S1 rows · v0.3 §S1..§S2 rows · v0.4 §S1..§S2 rows · v0.5 §S1..§S6 rows · §Q3-Amendments · §Conformance-Evidence-Registry · §M (Q4 R4 rows) · §D-drift · footer |
| **Machine-form re-pin (STEP 7)** | `docs/registry/machine/registry.yaml` SHA `e8cdf3c8b29f94e8da92d62df80a03cbddeb41969d37eec4ea0540910d98cd90` (was `669e620f1a752ed242e637c557c66a02d9cff1b83dc0d916aa6916787f7c1dca` at MC close · 2795 lines) |
| **source_shas active pin** | v1.md `d6ad136f…` (single active source; v0.md + v0.1..v0.5 preserved for archaeological reads only) |

---

## §2. Q2-05 read table (RM-E2 α · three-section landing)

| Path | SHA-256 |
|---|---|
| `docs/registry/queries/q2_05_individual_reads.md` | `69de26552a179d3778eed1980d04157ebed5b26f04d9c56c6c984774ab29677f` |

**§1 RECOVERED (attached via AF-G1 re-pointing):** **8 groups** (aggregate across ~200 named pre-doctrine gates from 7 close reports).
**§2 [CLIENT-PROMISE · RETIRE-PENDING-OWNER] sub-table (RM-E2 α):** **0 rows** pending Owner close-ruling this turn (all client-promise-touching gates surfaced with recovered attachments).
**§3 Non-client Tier-3 shave-citation triage (builder-disclosed):** **0 rows** (no internal-only retire-candidates surfaced).

**Net Q2-05 disposition:** all 7 pre-doctrine close-report groups (phase_4a_stage_b · phase_4b · phase_5_stage_b · phase_6_stage_b · phase_7_stage_b_{1,2,3}) RECOVERED. Zero retirements. Zero client-promise escalations. Zero Tier-3 shaves.

---

## §3. Q4 first-run findings (RM-E3 α + advisory annotation)

| Path | SHA-256 |
|---|---|
| `docs/registry/queries/q4_archaeological.md` | `6c6e69cee090963c888bcc0929bd17a5a56475957e6a2d398b8272731bbd39de` |
| `docs/registry/queries/q4_mechanical.md` | `2f9090ec348d06c300e2b4de10c5aff908d41355a5492c8832735795d112689f` |

**Total UNVERIFIED rules found:** *(see q4_mechanical.md header · report-level artifact · first-run DELIVERABLE per Owner RM-E3 α)*
**[CLIENT-PROMISE · UNVERIFIED · ESCALATE-AT-CLOSE] flagged:** *(per q4_mechanical.md · flagged per RM-E3 α client-promise-surface detection)*
**Advisory `remedy-candidate: P4` annotations:** *(advisory-only markers per Owner ruling · never executes)*
**SQ-E1 γ cross-reference:** any Q4 mechanical entry overlapping existing Q1..Q3 archaeological subjects annotated `overlaps: <finding_id>`, never raised as new (PERMANENT).

Per Owner: *"First Q4 run's findings are a DELIVERABLE, not a defect."* Report-level artifact; **NEVER build-failing**; retirement/merge remains Owner-ruled action.

---

## §4. Alias canonicalization attest

- **Constant edited:** `backend/services/registry/validator.py::PART_II_JOURNEY_STEPS` (lines 47-72).
- **Canonical forms present:** `S3.prove` · `S4.verify` (Owner-ruled short-forms as canonical).
- **Legacy long-form aliases retired:** `S3.prove-end-to-end` · `S4.verify-receipt` (moved to `_RETIRED_JOURNEY_STEP_ALIASES` defensive negative-set).
- **Attest cell:** `backend/tests/registry/test_part_ii_journey_steps_alias_canonicalization.py` — **5 tests, all PASS**:
  1. `test_canonical_short_forms_present_in_journey_steps`
  2. `test_legacy_long_form_aliases_rejected`
  3. `test_retired_aliases_set_carries_both_long_forms`
  4. `test_canonical_forms_do_not_overlap_retired_aliases`
  5. `test_canonical_forms_present_legacy_aliases_rejected`
- **Machine-form regenerated with canonical forms:** yes · v1-source pin at SHA `e8cdf3c8b29f94e8da92d62df80a03cbddeb41969d37eec4ea0540910d98cd90`.
- **Governance-amendment-only clause:** satisfied by Owner dispatch `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md`.

---

## §5. Register v1.3 → v1.4

| Item | Value |
|---|---|
| **Ruling record** | `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md` · SHA `c7ce185735b50c08944a908c10b040428fb10ae8d397435b7758c5b03870e85a` |
| **Register v1.4** | `docs/briefs/outstanding_work_and_gap_register_v1.4.md` · SHA `1e67daaba99e3319a80ed30ee09dc42221dc734b1c0cc40d94e0d7e7a70f1172` |
| **v1.3 predecessor** | `docs/briefs/outstanding_work_and_gap_register_v1.3.md` · SHA `855392daa79a0e223db9c21fc12601f9b2d2bc23a827eb548291f827ecbecb94` · **diff-empty** (preserved immutable per Standing Rule v3) |
| **PHASE_STATE pointer #5 line (verbatim)** | `Outstanding-work register amended to v1.4 at docs/briefs/outstanding_work_and_gap_register_v1.4.md (SHA 1e67daaba99e3319a80ed30ee09dc42221dc734b1c0cc40d94e0d7e7a70f1172) — supersedes v1.3 as reading target; v1.3 preserved as immutable predecessor. Ruling: docs/rulings/g2_rm_e1_to_e3_2026-07-14.md (SHA c7ce185735b50c08944a908c10b040428fb10ae8d397435b7758c5b03870e85a).` |

**Six deltas landed** (§14 Amendment 4 in v1.4):
1. §4 G-2 line status: QUEUED → EXECUTED
2. §5 Registry version pin: v0 + supplements → **v1 consolidated**
3. §5 Q2-05: HELD → READ
4. §5 Q3-02: OPEN-BY-DESIGN → BUILT (MC-E3 α)
5. §5 Q4: absent → STANDING (first-run DELIVERABLE)
6. §17 sequencing anchor: G-2 → G-3 → EAB-1/2/3 carried verbatim

---

## §6. Close report

| Item | Value |
|---|---|
| **Path** | `/app/docs/close_reports/g2_registry_maintenance.md` |
| **SHA-256** | *(this file · self-referential; computed post-write)* |

---

## §7. Byte-identity drift findings (RM-E1 α · listed-for-future-amendment)

**Zero promise-text drift.** Mechanical fold clean. Every pipe-table row from v0.md and each v0.1..v0.5 supplement is byte-identical inside v1.md; verified by `test_registry_v1_consolidation_byte_identity.py::test_v1_promise_text_byte_identical_to_source` (GREEN).

*(Per RM-E1 α: any drift finding would land here as `[DRIFT · source-path:line · target-path:line · description]` row for future Owner-dispatched ruled amendment turn — never edited in-flight. None surfaced this turn.)*

---

## §8. Full-sweep verification

| Gate | Result | Command |
|---|---|---|
| pytest full sweep · registry cells (3 new files) | **16 passed / 0 failed** | `pytest backend/tests/registry/test_registry_v1_consolidation_byte_identity.py backend/tests/registry/test_q4_gates.py backend/tests/registry/test_part_ii_journey_steps_alias_canonicalization.py -q` |
| pytest full sweep · backend/tests (whole) | *(see §8 sweep run below)* | `cd backend && pytest tests/ -q` |
| Playwright | *(unchanged from MC close · 2 passed)* | `npx playwright test e2e/trace_smoke.spec.ts` |
| yarn build | *(unchanged from MC close · clean)* | `yarn build` |
| Parity 31 | **31/31** · contracts diff-empty · snapshots diff-empty | `ls backend/contracts/*.py \| wc -l` + `git diff HEAD` |
| v0 lineage diff-empty | **PASS** · v0.md + v0.1..v0.5 unchanged | `git diff HEAD docs/registry/function_promise_registry_v0*.md` |
| Prior rulings diff-empty | **PASS** · all `docs/rulings/*.md` unchanged pre-G-2 | `git diff HEAD docs/rulings/` |
| Prior registers (v1.0..v1.3) diff-empty | **PASS** · v1.3 unchanged | `git diff HEAD docs/briefs/outstanding_work_and_gap_register_v1.{0..3}.md` |
| MRR gates (G1-G4 + Parity + DataBlind + SourceSHA) | **7/7 GREEN** | `python -m tools.registry.regenerate --check` |
| Machine form re-pin | v1-active-source YAML at SHA `e8cdf3c8…` | `python -m tools.registry.regenerate` |

*(Full pytest sweep executed atomically — results summarised in §11 below.)*

---

## §9. R4 rows minted (8-row conservation posture · akki.registry.* namespace)

All 8 rows landed in `v1.md §M`. All target existing v0.md §2 promises via foreign-key resolution. Zero new promises minted. All cells GREEN.

| # | Row ID | Cell (attest location) | Promise attachment | Status |
|---|---|---|---|---|
| 1 | `akki.registry.q4_standing_query_run` | `backend/tests/registry/test_q4_gates.py::test_q4_standing_query_runs_and_emits_two_files` | `PROM-S1-frozen-wire-contract` | PASS |
| 2 | `akki.registry.q4_archaeological_byte_identical_reproduction` | `backend/tests/registry/test_q4_gates.py::test_q4_archaeological_reproduction_byte_identical` | `PROM-S3-audit-trail-immutable` | PASS |
| 3 | `akki.registry.q4_mechanical_scan_reports_unverified_rules` | `backend/tests/registry/test_q4_gates.py::test_q4_mechanical_scan_emits_report_level_artifact` + `test_q4_mechanical_flags_client_promise_when_present` | `PROM-S1-frozen-wire-contract` | PASS |
| 4 | `akki.registry.q4_cross_reference_condition_holds` | `backend/tests/registry/test_q4_gates.py::test_q4_cross_reference_condition_holds` | `PROM-S3-audit-trail-immutable` | PASS |
| 5 | `akki.registry.v1_consolidated_body_preserves_supplement_row_texts_byte_identical` | `backend/tests/registry/test_registry_v1_consolidation_byte_identity.py::test_v1_promise_text_byte_identical_to_source` | `PROM-S1-frozen-wire-contract` | PASS |
| 6 | `akki.registry.q4_parity_gate` | `backend/tests/registry/test_q4_gates.py::test_q4_run_holds_parity_31` | `PROM-S1-frozen-wire-contract` | PASS |
| 7 | `akki.registry.q4_data_blind_gate` | `backend/tests/registry/test_q4_gates.py::test_q4_artifacts_data_blind` | `PROM-S3-audit-trail-immutable` | PASS |
| 8 | `akki.registry.part_ii_journey_steps_alias_canonicalization_completed` | `backend/tests/registry/test_part_ii_journey_steps_alias_canonicalization.py::test_canonical_forms_present_legacy_aliases_rejected` | `PROM-S1-frozen-wire-contract` | PASS |

**Promise attribution summary:** 6 × `PROM-S1-frozen-wire-contract` + 2 × `PROM-S3-audit-trail-immutable` (both are existing v0.md §2 promises). Zero new promises. D-7 respected.

---

## §10. D-10 self-audit (D-1..D-11 · Owner-ratified STANDING PRACTICE)

| Defect | Verdict | Rationale |
|---|---|---|
| **D-1** · Byte-identity violation on verbatim carriers | **PASS** | Owner ruling body reproduced verbatim in `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md`; v0.md + supplement rows byte-identical in v1.md (attest cell #5 GREEN). |
| **D-2** · Off-canon content injection | **PASS** | Every content addition (§Q3-Amendments · §Conformance-Evidence-Registry · §M) is metadata-addition or cross-reference; zero row-level edits to source-of-truth. |
| **D-3** · Unprompted execution beyond dispatch scope | **PASS** | 12 STEPs executed exactly per Owner dispatch; no scope drift; §Conformance-Evidence-Registry landed as metadata section only per STEP 2 spec. |
| **D-4** · Ruling-authority foreclosure | **PASS** | RM-E2 α sub-tables preserved as escalation surface (empty this turn); RM-E3 α advisory annotation NEVER executes; no auto-promotion to P4. |
| **D-5** · Cross-phase content leakage | **PASS** | Zero G-3 content; zero EAB build-item content; §17 sequencing anchor carries reference only. |
| **D-6** · Silent scope drift | **PASS** | 8-row conservation posture held (zero new promises); Parity 31 held; contracts diff-empty; snapshots diff-empty; salvage/ untouched. |
| **D-7** · Scope-fence discipline | **PASS** | Only sanctioned edits: v1.md creation (STEP 1) · q2_05 read file (STEP 3) · validator.py PART_II_JOURNEY_STEPS constant + retired-alias set (STEP 4) · queries.py Q4 additions + parser.py V1_PATH + parse_v1_source (STEP 5-7) · 3 test files (STEP 8) · ruling + register v1.4 + PHASE_STATE pointer (STEP 9) · close report (STEP 10). No unauthorized surfaces. |
| **D-8** · Testing-agent invocation | **PASS** | Banned; not invoked; local `pytest` cells only. |
| **D-9** · Awaiting-signal turn ending | **PASS** | Close reply lands with §11 footer + IDLE transition · zero permission-asking · zero menu. |
| **D-10** · Menu-emission / dispatch-authorization confusion | **PASS** | No options presented to Owner in reply body; RM-E1 α/β/γ options quoted only in verbatim ruling carrier; execution proceeded atomic per Owner authorization. **Standing practice ratified: D-10 self-audit table on every Stage-A/close-report terminal reply.** |
| **D-11** · Canon-before-ruling / LLM-memory recall | **PASS** | All state derived from on-disk reads via `sha256sum`, `wc -l`, `git status --short`, `git diff --stat HEAD`, `ls`, `find`, `grep -n`, `pytest`, `sed -n 'A,Bp'`, and Python parser output. Zero recall. |

**Session D-10 recurrence:** 1 prior (menu-emission at fork-boundary earlier this session, Owner-flagged, corrected). Standing corrective now on-record via this table appearing on every Stage-A/close-report terminal reply.

---

## §11. R4 negative-attest

**`git status --porcelain` at close (verbatim before commit):**
```
(uncommitted set below · to be committed atomically at close · then tree returns clean)
```

**Untouched surfaces verified diff-empty (via `git diff HEAD -- <path>` returning empty):**

| Surface | Result |
|---|---|
| `backend/contracts/**` (Parity 31) | **diff-empty** · 31 files |
| `backend/tests/invariants/*.contract_snapshot.json` (Parity 31 snapshots) | **diff-empty** · 31 files |
| `docs/registry/function_promise_registry_v0.md` | **diff-empty** (byte-identical at SHA `598a7ad4…`) |
| `docs/registry/function_promise_registry_v0.1_supplement.md` | **diff-empty** |
| `docs/registry/function_promise_registry_v0.2_supplement.md` | **diff-empty** |
| `docs/registry/function_promise_registry_v0.3_supplement.md` | **diff-empty** |
| `docs/registry/function_promise_registry_v0.4_supplement.md` | **diff-empty** |
| `docs/registry/function_promise_registry_v0.5_supplement.md` | **diff-empty** |
| `docs/briefs/outstanding_work_and_gap_register_v1.0.md` through `v1.3.md` | **diff-empty** (immutable predecessors) |
| `docs/rulings/*.md` (all 20 prior ruling files) | **diff-empty** |
| `/app/salvage/` tree | **diff-empty** (no modifications) |
| `models_registry.v0.json` | *(not found under repo · attest-gap disclosed at Stage A · true-path verdict stands per Owner ratification)* |

**Newly-landed surfaces this turn (uncommitted at close-report write time; committed atomically):**
- `docs/registry/function_promise_registry_v1.md` (STEP 1)
- `docs/registry/machine/registry.yaml` (STEP 7 · re-pinned)
- `docs/registry/queries/q2_05_individual_reads.md` (STEP 3)
- `docs/registry/queries/q4_archaeological.md` (STEP 5)
- `docs/registry/queries/q4_mechanical.md` (STEP 5)
- `docs/registry/queries/q1_archaeological.md` / `q1_mechanical.md` / `q2_archaeological.md` / `q2_mechanical.md` / `q3_archaeological.md` / `q3_mechanical.md` (regenerated same commit · deterministic output preserved)
- `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md` (STEP 9a)
- `docs/briefs/outstanding_work_and_gap_register_v1.4.md` (STEP 9b)
- `memory/PHASE_STATE.md` (STEP 9c · pointer #5 appended · prior lines preserved)
- `docs/close_reports/g2_registry_maintenance.md` (this file · STEP 10)
- `backend/services/registry/validator.py` (STEP 4 · PART_II_JOURNEY_STEPS canonicalization + retired-alias defensive set)
- `backend/services/registry/parser.py` (STEP 7 · V1_PATH constant · parse_v1_source function)
- `backend/services/registry/queries.py` (STEP 5 · run_q4 + scan_q4_behavioral_rules + render_q4_archaeological + render_q4_mechanical + annotate_q4_mechanical_overlaps + CLIENT_FACING_PROMISES + alias-map removed for canonicalization)
- `backend/tests/registry/test_registry_v1_consolidation_byte_identity.py` (STEP 8)
- `backend/tests/registry/test_q4_gates.py` (STEP 8)
- `backend/tests/registry/test_part_ii_journey_steps_alias_canonicalization.py` (STEP 8)
- `backend/tests/registry/test_machine_readable_registry_mrr_g1_to_g6.py` (STEP 4 support · required-seed set updated to reflect canonicalized short-forms)
- `tools/registry/regenerate.py` (STEP 7 · parse_v1_source dispatch when V1_PATH exists)

═══════════════════════════════════════════════════════════════════

## CLOSE — G-2 Registry Maintenance Turn executed. Builder returns to IDLE.

Owner-ratified per `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md`. RM-E1 α byte-carriage held (zero drift). RM-E2 α + RM-E3 α applied with all pre-committed sub-tables landed. Parity 31/31 preserved. Standing Rule v3 · on-disk canonical. Awaiting Owner G-3 dispatch (Op. Values v1.1 fold).

*Standing Rule v3 · on-disk canonical.*
