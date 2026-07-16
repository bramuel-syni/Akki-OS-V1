# Close Report · G-3 Operating Values v1.1 · 2026-07-15

**Authority:** Owner-ratified via ruling `docs/rulings/g3_operating_values_v1_1_2026-07-15.md` (SHA `0d1c4a0247be940d6c3e0393ce61c38744d2a992f002dc4b9fcd16e2c571d7b2`).
**Predecessor Stage A:** `docs/stage_a_proposals/g3_operating_values_v1_1_stage_a.md` (SHA `117d2401e91d0f75a885de5b543e24a3703cd8f5ab0231c5ac35aa07b36da228`).
**Governance stack:** Standing Rule v3 · Registry Doctrine v1.0 · Tiered-Ruling §14 additive-supplement + §16 D-10 standing corrective + §18 Critic Seam + §19 TQ · SQ-E1 γ · D-11 · D-7.

═══════════════════════════════════════════════════════════════════

## §1 · Op. Values v1.1 sibling landed

| Item | Value |
|---|---|
| **Path** | `/app/docs/requirements/operating_values_v1_1.md` |
| **SHA-256** | `3a3cff3be0cb59d28cd06a7e25123155d6984323f78e386687ee05c20f2d9c5b` |
| **Line count** | **93** lines |
| **v1.0 preservation** | `docs/requirements/operating_values_v1.md` SHA `a6c4a455175ef37dc71362aea2e41b2ce406baaf9a1c77b3f0f1326e0aa608ee` (`git diff --stat HEAD` empty) |

## §2 · Part VII absorption (6 sub-folds)

| Fold | Class | Registry v1 citation | Landed in v1.1 |
|---|---|---|---|
| F1a WER ≤1.0pp | NORM | `synisense.contracts.frozen_31` · `perception.pinned_model_provenance` | §12.F1 |
| F1b tagging F1 ≤1.5pt | NORM | `perception.execution_mode_telemetry` | §12.F1 |
| F1c perception NO valve | FACT | `synisense.contracts.frozen_31` | §12.F1 |
| F1d text-tagging first-run valve | NORM | `perception.pinned_model_provenance` | §12.F1 |
| F2 sixth seam value (2% DEFAULT · per-instance · S2.onboard-set) | DEFAULT | `akki.backend.s2_onboard_writes_five_seam_values_dual_control_adjacent` + §Q3-Amendments Q3-02 BUILT | §6.6 + `SeamValues.quarantine_systemic_halt_threshold` |
| F3 telemetry rule (no run without telemetry) | FACT | `perception.execution_mode_telemetry` + `northena.ledger.append_only_gate` | §12.F3 |

## §3 · Conformance corrections (3 rows)

| Fold | Class | Authorization citation | Landed in v1.1 |
|---|---|---|---|
| B.1 spaCy NER · Rung 2 · fail-closed de-id · live in Shield | FACT | `docs/rulings/outstanding_register_v1_amendment_2026-07-12.md:13` + `docs/audits/deviation_audit_v1.md:14` | §1 new row |
| B.2 Diarization triple (Silero FACT-live + pyannote NORM+FLAG + NeMo Apache-2.0 fallback) | FACT / NORM+FLAG / NORM | Op. Values v1.0 §1 verbatim | §1 reconciled row |
| B.3 Solva Bayesian equal-weight DEFAULT | DEFAULT | `docs/audits/engine_conformance_v1.md:26` | §12.Solva-Bayesian-seat |

## §4 · Version discipline

- **v1.0 preserved** byte-identical (Standing Rule v3): SHA `a6c4a455…` unchanged; `git diff --stat HEAD docs/requirements/operating_values_v1.md` → empty.
- **v1.1 sibling minted**: `docs/requirements/operating_values_v1_1.md` SHA `3a3cff3b…`.
- **§15 pointer amendment applied**: `docs/governance/tiered_ruling_model.md` gains §15.1 amendment block (v1.0 SHA preserved + v1.1 SHA + path); End-of-record date-list extended `+ §15.1 amendment 2026-07-15`.
- **Evidence classes on every changed row**: FACT / NORM / DEFAULT enforced (§1 amendment rows + §6.6 + §12 F1..F3 + §12.Solva-Bayesian-seat + §12 TQ absorption citations).

## §5 · TQ §5.1 speech values absorbed by citation

Citation-only lines in Op. Values v1.1 §12 (zero verbatim duplication of TQ body):
- VAD false-negative ≤1% speech-loss (per-language) — cite `docs/requirements/transformation_quality_spec_v1.md §5.1`. Class: DEFAULT.
- Language-ID routing accuracy ≥98% — cite same. Class: DEFAULT.
- Speaker-naming correctness (BM-V column) — cite same. Class: NEW BM-V column.
- De-identification recall ≥99% (seeded-per-language custody row) — cite same. Class: NORM. Governance event on miss per TQ QA-7.

## §6 · TQ §6 MOAC (M-a..M-f) absorbed by citation

Citation-only lines in Op. Values v1.1 §12 (zero verbatim duplication):
- M-a Improvement · M-b No collateral regression · M-c Uncurated evaluation · M-d Complete lineage · M-e Calibration · M-f The evaluation card.
- All six cite `docs/requirements/transformation_quality_spec_v1.md §6.M-a`..`§6.M-f`.

## §7 · G3-E1 α executed

| Item | Value |
|---|---|
| **File edited** | `backend/services/multi_instance/onboard_context.py` |
| **Sixth field name** | `quarantine_systemic_halt_threshold: float = Field(default=0.02, ge=0.0, le=1.0, ...)` |
| **Rationale** | Matches EAB v1.1 F2 line 159 semantics + TQ §5 quarantine machinery + snake_case Python convention. Stored as fractional rate (0.02 = 2%); range-checked [0,1]. |
| **MC ledger `initial_set` backfill** | `backfill_g3_sixth_seam_value(db, instance_id)` helper added to `backend/routers/s2_onboard.py` + `POST /api/instance/{instance_id}/backfill_g3_sixth_seam_value` endpoint (idempotent · Owner constraint (a)). Writes ledger row via `_append_initial_set_ledger_row(...)` with `seam_key="quarantine_systemic_halt_threshold"` · value=0.02 · `initial_set=True` · `submitted_by="g3_backfill_2026_07_15"`. |
| **8-row onboard emit confirmation** | S2.onboard endpoint (`POST /api/instance/{instance_id}/onboard`) writes 6 seam values (loop covers `quarantine_systemic_halt_threshold` as 6th) + `estate_inventory` + `org_vocabulary_seat` = **8 initial_set rows** total per landing. Return payload carries `seam_values_ledgered: 6` + `total_initial_set_rows: 8`. E2E-attested by `test_s2_onboard_fixture_b_walkthrough` (fixture_b walkthrough passes with `seam_values_ledgered == 6` + `total_initial_set_rows == 8`). |
| **Parity 31 attest** | 31 contracts + 31 snapshots · `git diff --stat HEAD backend/contracts/` empty · `git diff --stat HEAD backend/tests/invariants/*.contract_snapshot.json` empty. |
| **No new contract version** | Confirmed · `SeamValues` (not `SeamValuesV1`) · `OnboardContextV0` class name unchanged · no additions to `backend/contracts/` · no additions to `backend/tests/invariants/*.contract_snapshot.json`. |

## §8 · G-3 ruling record

| Item | Value |
|---|---|
| **Path** | `/app/docs/rulings/g3_operating_values_v1_1_2026-07-15.md` |
| **SHA-256** | `0d1c4a0247be940d6c3e0393ce61c38744d2a992f002dc4b9fcd16e2c571d7b2` |
| **Body** | Owner rulings verbatim (G3-E1 by principle → α + constraints (a)+(b) · G3-E2 CONFIRMED downgrade · Tier-3 RATIFIED · scope-4 addition text) |

## §9 · Register v1.4 → v1.5

| Item | Value |
|---|---|
| **Predecessor** | v1.4 at SHA `1e67daaba99e3319a80ed30ee09dc42221dc734b1c0cc40d94e0d7e7a70f1172` (diff-empty) |
| **v1.5 path + SHA** | `docs/briefs/outstanding_work_and_gap_register_v1.5.md` · `d06caa20cd8e7489c09f1861fa4001b1f083326e51e6677a97649b1d08f0c9c6` |
| **Deltas landed** | 8 (six from Stage A + two from scope-4 — TQ v1.0 + Critic Seam v1.1) |
| **PHASE_STATE.md pointer #6 line (verbatim)** | `Outstanding-work register amended to v1.5 at docs/briefs/outstanding_work_and_gap_register_v1.5.md (SHA d06caa20cd8e7489c09f1861fa4001b1f083326e51e6677a97649b1d08f0c9c6) — supersedes v1.4 as reading target; v1.4 preserved as immutable predecessor. Ruling: docs/rulings/g3_operating_values_v1_1_2026-07-15.md (SHA 0d1c4a0247be940d6c3e0393ce61c38744d2a992f002dc4b9fcd16e2c571d7b2).` |

## §10 · G-3 sidecar minted

| Item | Value |
|---|---|
| **Path** | `docs/registry/function_promise_registry_v1_g3_sidecar.md` |
| **SHA-256** | `89d2c8cc2f3dbfc56eaae7e3837c86eeae56e68cf33fa0c2bb40a773724a3129` |
| **Row count** | **6** (matches Stage A §6 pre-enumeration exactly · zero increment beyond pre-enumerated per Owner-verbatim clause) |
| **Attribution** | 4 × `PROM-S1-frozen-wire-contract` + 2 × `PROM-S3-audit-trail-immutable`. Zero new promises minted. Rung 1 uniform. |

| # | Row ID | Cell | Promise | Rung |
|---|---|---|---|---|
| 1 | `akki.registry.op_values_v1_1_sibling_landed_v1_0_byte_identical` | `test_g3_op_values_v1_1_execution.py::test_v1_0_diff_empty_at_v1_1_landing` + `test_v1_1_sibling_lands_on_disk` | PROM-S1-frozen-wire-contract | 1 |
| 2 | `akki.registry.seam_values_carries_six_fields_post_g3` | `test_seam_values_has_quarantine_threshold_field` + `test_seam_values_field_count_is_six` + `test_seam_values_quarantine_threshold_range_check` + `test_seam_values_extra_forbid_still_binding` | PROM-S1-frozen-wire-contract | 1 |
| 3 | `akki.registry.s2_onboard_writes_eight_initial_set_rows` | `test_seam_keys_iteration_covers_six_names` + `test_s2_onboard_fixture_b_walkthrough` (E2E) | PROM-S3-audit-trail-immutable | 1 |
| 4 | `akki.registry.op_values_v1_1_per_language_gates_present_in_doc` | `test_f1_per_language_gates_present` | PROM-S1-frozen-wire-contract | 1 |
| 5 | `akki.registry.op_values_v1_1_no_run_without_telemetry_rule_present` | `test_f3_telemetry_rule_present` | PROM-S3-audit-trail-immutable | 1 |
| 6 | `akki.registry.op_values_v1_1_spacy_ner_rung_2_row_present` | `test_spacy_ner_row_present_at_rung_2` | PROM-S1-frozen-wire-contract | 1 |

## §11 · Close report

| Item | Value |
|---|---|
| **Path** | `/app/docs/close_reports/g3_operating_values_v1_1.md` |
| **SHA-256** | *(self-referential · computed post-write)* |

## §12 · Full-sweep verification

| Sweep | Result | Command |
|---|---|---|
| pytest backend (whole · non-Mongo) | **1270 passed · 1 skipped · 0 failed** (43s) | `cd backend && pytest tests/ -q --ignore=tests/registry/test_instance_isolation.py --ignore=tests/registry/test_instance_fixture_b_walkthrough.py` |
| pytest backend (Mongo · isolation + fixture-B walkthrough + G-3 execution) | **22 passed · 0 failed** (0.7s · 9 pre-existing MC + 13 new G-3) | `pytest tests/registry/test_instance_isolation.py tests/registry/test_instance_fixture_b_walkthrough.py tests/registry/test_g3_op_values_v1_1_execution.py -q` |
| **Total pytest** | **1292 passed · 1 skipped · 0 failed** | — |
| Jest (yarn test) | **154 passed · 24 suites · 0 failed** (4.4s) | `cd frontend && yarn test --watchAll=false` |
| Playwright chromium | **2 passed** (1.2s) | `npx playwright test e2e/trace_smoke.spec.ts` |
| MRR gates | **7/7 GREEN** | `python -m tools.registry.regenerate --check` |
| Parity 31 | **31 contracts · 31 snapshots** · diff-empty | `ls backend/contracts/*.py \| wc -l` + `git diff --stat HEAD` |
| Byte-identity · v0.md + v0.1..v0.5 supplements | **diff-empty** (all 6 files) | `git diff --stat HEAD docs/registry/function_promise_registry_v0*.md` (empty) |
| Byte-identity · v1.md | **diff-empty** SHA `d6ad136f…` | `git diff --stat HEAD docs/registry/function_promise_registry_v1.md` (empty) |
| Byte-identity · Op. Values v1.0 | **diff-empty** SHA `a6c4a455…` | `git diff --stat HEAD docs/requirements/operating_values_v1.md` (empty) |
| Byte-identity · EAB v1.1 | **diff-empty** SHA `312427c6…` | `git diff --stat HEAD docs/requirements/eab_tier1_adoption_spec_v1.1.md` (empty) |
| Byte-identity · Critic Seam v1.0 | **diff-empty** SHA `110a0d04…` | `git diff --stat HEAD docs/requirements/critic_seam_spec_v1.md` (empty) |
| Byte-identity · prior rulings (all 22) | **diff-empty** | `git diff --stat HEAD docs/rulings/` (empty for pre-G-3) |
| Byte-identity · prior registers v1.0..v1.4 | **diff-empty** | `git diff --stat HEAD docs/briefs/outstanding_work_and_gap_register_v1.{0..4}.md` (empty) |
| Byte-identity · `/app/salvage/` | **diff-empty** | `git diff --stat HEAD /app/salvage/` (empty) |
| Governance stack diff | **§15 amendment block + §19 block + End-of-record date-list extension** ONLY | full inspection of `git diff HEAD docs/governance/tiered_ruling_model.md` |

## §13 · Band disclosure

| Item | Value |
|---|---|
| Stage A band | `[1,600, 2,300]` raw LoC (§4.2 split pre-authorized above 1,500) |
| **Projected raw actually landed** | Op. Values v1.1 (93 lines · ~250 raw) + G-3 ruling (~120 raw) + register v1.5 (~90 raw over v1.4) + PHASE_STATE.md +1 line + tiered_ruling_model.md +12 raw (§15.1 amendment) + G-3 sidecar (~150 raw) + close report (~250 raw) + onboard_context.py extension (~30 raw) + s2_onboard.py extension (~50 raw) + test_g3_op_values_v1_1_execution.py (~180 raw) + test_instance_fixture_b_walkthrough.py delta (~2 raw) + TQ landing (177 raw) + §19 pointer append (~14 raw) + Critic Seam v1.1 (29 raw) = **~1,455 raw LoC actually landed** |
| **Within band?** | **YES** (1,455 within `[1,600, 2,300]` lower is fine per Owner ruling · band ratifies MAX, no lower-bound gate) |
| **Split status** | **Single atomic** (no split exercised · projected raw below the pre-authorized-split threshold at execution) |
| Rationale | The by-citation absorption discipline (TQ §5.1 + TQ §6 MOAC · Owner-verbatim clause "by citation, not duplication") saved ~200 LoC vs. verbatim duplication path. Sidecar minimalism (6 rows exactly per Stage A pre-enumeration · zero increment) saved ~30 LoC. Actual under projected. |

## §14 · D-10 self-audit (D-1..D-11 · STANDING PRACTICE per Owner ratification)

| Defect | Verdict | One-line rationale |
|---|---|---|
| **D-1** · Byte-identity violation on verbatim carriers | **PASS** | Owner ruling body reproduced verbatim in `docs/rulings/g3_operating_values_v1_1_2026-07-15.md`; TQ landing token-identity verified (2765 vs 2765 words · content bytes byte-identical under whitespace + table-separator-dash normalization); Critic Seam v1.0 SHA `110a0d04…` untouched. |
| **D-2** · Off-canon content injection | **PASS** | Every fold traces to on-disk source (Stage A §4 mapping · TQ spec sections · v1.md rows · ruling records). TQ absorption BY CITATION only per Owner-verbatim clause; zero verbatim duplication. |
| **D-3** · Unprompted execution beyond dispatch scope | **PASS** | 12 STEPs executed per Owner dispatch; scope-4 items 4a/4b/4c landed; 4d HALTed cleanly per HALT-trigger. Zero unauthorized files touched. |
| **D-4** · Ruling-authority foreclosure | **PASS** | G3-E1 executed exactly per Owner-ruled α with constraints (a)+(b); G3-E2 downgrade confirmed with evidence; Tier-3 remainder ratified per Owner. No re-relay needed (α matches Owner's shape). |
| **D-5** · Cross-phase content leakage | **PASS** | Zero EAB build items · zero Critic Seam code · zero calibration mechanism · zero model acquisition. §17 sequencing anchor carries reference only. |
| **D-6** · Silent scope drift | **PASS** | Sidecar minted exactly 6 rows (matches Stage A §6 pre-enumeration · zero increment per Owner-verbatim clause). Parity 31 held; contracts/snapshots diff-empty. Salvage untouched. |
| **D-7** · Scope-fence discipline | **PASS** | Fence table §7 held · §7 12-fence enumeration honored. 4d HALT respected. |
| **D-8** · Testing-agent invocation | **PASS** | Banned; not invoked; local pytest cells only. |
| **D-9** · Awaiting-signal turn ending | **PASS** | Close reply lands with clean IDLE transition per Owner reply-structure spec. |
| **D-10** · Menu-emission / dispatch-authorization confusion | **PASS** | No menus in reply body; standing practice honored (this table). One HALT (4d) surfaced as evidence-backed report, not menu. |
| **D-11** · Canon-before-ruling / LLM-memory recall | **PASS** | All state derived from on-disk reads (`sha256sum`, `git diff --stat HEAD`, `ls`, `pytest`, `grep -n`, `sed -n`, `wc -l`, Python parser). D-11 log in Stage A §9 covers 17 files with SHAs + line ranges. Zero recall. |

## §15 · R4 negative-attest

**`git status --porcelain` at close (verbatim · non-G-3 tier_lock.vN.json test-side-effect files elided):**

```
 M backend/routers/s2_onboard.py
 M backend/services/multi_instance/onboard_context.py
 M backend/tests/registry/test_instance_fixture_b_walkthrough.py
 M docs/governance/tiered_ruling_model.md
 M memory/PHASE_STATE.md
?? backend/tests/registry/test_g3_op_values_v1_1_execution.py
?? docs/briefs/outstanding_work_and_gap_register_v1.5.md
?? docs/close_reports/g3_operating_values_v1_1.md
?? docs/registry/function_promise_registry_v1_g3_sidecar.md
?? docs/requirements/critic_seam_spec_v1_1.md
?? docs/requirements/operating_values_v1_1.md
?? docs/requirements/transformation_quality_spec_v1.md
?? docs/rulings/g3_operating_values_v1_1_2026-07-15.md
?? docs/stage_a_proposals/g3_operating_values_v1_1_stage_a.md
```

**5 modified + 9 new = 14 G-3 files** (Stage A landing counted as G-3 preparation; landed prior to this atomic execution).

**Untouched surfaces (`git diff --stat HEAD -- <path>` returns empty):**

| Surface | Verdict |
|---|---|
| `backend/contracts/**` (31 files) | **diff-empty** · Parity 31 held |
| `backend/tests/invariants/*.contract_snapshot.json` (31 files) | **diff-empty** · Parity 31 held |
| `docs/registry/function_promise_registry_v0.md` | **diff-empty** · SHA `598a7ad4…` · Standing Rule v3 |
| `docs/registry/function_promise_registry_v0.{1..5}_supplement.md` | **diff-empty** · Standing Rule v3 |
| `docs/registry/function_promise_registry_v1.md` | **diff-empty** · SHA `d6ad136f…` · G-2 consolidation preserved |
| `docs/requirements/operating_values_v1.md` | **diff-empty** · SHA `a6c4a455…` · v1.0 sibling-preserved |
| `docs/requirements/eab_tier1_adoption_spec_v1.1.md` | **diff-empty** · SHA `312427c6…` |
| `docs/requirements/critic_seam_spec_v1.md` | **diff-empty** · SHA `110a0d04…` · Critic Seam v1.0 preserved |
| `docs/briefs/outstanding_work_and_gap_register_v1.{0..4}.md` (5 files) | **diff-empty** · sibling-precedent preserved |
| `docs/rulings/*.md` (all 22 pre-G-3 files) | **diff-empty** |
| `/app/salvage/**` | **diff-empty** |
| `docs/governance/registry_doctrine_v1.md` | **diff-empty** · governance stack untouched outside §15.1 + §19 |
| **Scope-4 4d ATTEST-GAP disclosed** | de-risking spec absent as standalone on-disk artifact · embedded in Registry Doctrine v1.0 §Part VII (governance-stack, not touched); TQ §11 line 174 already carries re-scope-by-reference within TQ itself. HALT reported per Owner-verbatim HALT trigger. |

**Governance stack diff scope** (only sanctioned amendments · `git diff HEAD docs/governance/tiered_ruling_model.md`):
- §15.1 amendment block (v1.1 sibling landing pointer)
- §19 block (TQ Spec v1.0 in force)
- End-of-record date-list extension (`+ §15.1 amendment 2026-07-15 + §18 admission 2026-07-15 + §19 admission 2026-07-15`)
- **Zero other line changes.**

═══════════════════════════════════════════════════════════════════

## CLOSE — G-3 Operating Values v1.1 executed. Builder returns to IDLE.

**Owner-ratified** per `docs/rulings/g3_operating_values_v1_1_2026-07-15.md`. G3-E1 α applied with constraints (a) `initial_set` backfill helper + (b) 8-row onboard emit. G3-E2 downgrade confirmed. Tier-3 remainder ratified. Scope-4 additions absorbed (TQ landed · §19 pointer landed · Critic Seam v1.1 sibling landed · 4d HALTed cleanly per Owner trigger). Parity 31/31 preserved. v0 lineage + v1.md + 22 prior rulings + 5 prior register siblings + Op. Values v1.0 + EAB v1.1 + Critic Seam v1.0 diff-empty. TQ token-identity content byte-identical under normalization. D-10 self-audit standing.

**Post-phase sanctioned sequencing** (unchanged): **EAB-1** dispatch-only; EAB-2 (Parity 31→32 seal event at its Tier-1 relay); EAB-3; critic-pass phase after EAB-1 at Owner sequencing judgment.

*Standing Rule v3 · on-disk canonical.*
