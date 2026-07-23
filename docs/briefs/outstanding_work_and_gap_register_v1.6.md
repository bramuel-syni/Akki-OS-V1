# Outstanding Work & Gap Register · v1.6

**Landed:** 2026-07-15 · EAB-1 execution atomic close · siblings pattern.
**Predecessor:** v1.5 (`docs/briefs/outstanding_work_and_gap_register_v1.5.md` SHA `d06caa20cd8e74891c4b90f38b57de3f36b9f8b8d5ba05f5f5e0a3f9c1c3b60d`) held byte-identical per Standing Rule v3.
**Sequencing anchor:** register v1.5 §15 Delta 8 (per FLAG 4 forward-only re-cite ruling, `docs/rulings/section_17_forward_only_re_cite_2026-07-15.md`).

Deltas since v1.5 landing (2026-07-15):

## Delta 1 · EAB-1 execution atomic CLOSED (2026-07-15)

EAB-1 phase (A1 + A2 · ingestion side · one seam) executed and closed under D-9 auto-proceed from the S1 Memory Model + Five-Flag atomic close. Full close report at `docs/close_reports/eab_1.md`. Registry v1.5 §4 sequencing item "EAB-1" transitions from open (Stage A landed) to CLOSED.

## Delta 2 · A1 pipeline landed (7 folds · rung-1)

- A1.1 · Demux & normalize (`backend/services/perception/eab_1_pipeline/a1_demux.py`)
- A1.2 · Batch segmentation with worker-side batch schema (MC-E3 α placement precedent · not in `contracts/`)
- A1.3 · VAD wrapper with Silero registry-pin reference (no fresh model download)
- A1.4 · Acoustic-fingerprint dedup with canonical/occurrence honesty pointers
- AC-A1.a · rung-1 job-seam gate
- AC-A1.b · monthly reduction-ratio report shape
- AC-A1.d · news programme blocks dedup-exempt

## Delta 3 · A2 folds landed (3 folds · rung-1)

- A2.1 · Occurrence rows as NormalizedUnits (five_rings@v0 shape · **zero contract mutation**)
- A2.2 · license_class fail-closed attachment (MC-E4 α reuse · `internal_only` default)
- A2.3 · Canonical→occurrence trace walkability (**single code path** · FENCE 1 AST-attested)

## Delta 4 · Locator vocabulary extended additively (Owner E1 α)

`NormalizedUnit.provenance.locator: Dict[str, Any]` now carries additive occurrence keys `{canonical_id, station, timestamp_ms, batch_lineage}` for occurrence-modality units. Additive by proof (AST cell hard-fails on any five_rings@v0 mutation), not by intent. Owner ruling: `docs/rulings/eab_1_e1_2026-07-15.md`.

## Delta 5 · AST cell landed (load-bearing per Owner)

`backend/tests/invariants/test_five_rings_v0_zero_mutation_ast_cell.py` (3 sub-cells) parses five_rings.py AST + snapshot; asserts class-list + ring-field-list equivalence. **Hard-fails the build** (`raise AssertionError`) on any drift. Not `warnings.warn` · not `pytest.skip` · not print+continue. Manually verified: temporary synthetic mutation → cell red; restore → cell green.

## Delta 6 · R4 sidecar landed (13 rows · zero new promises)

`docs/registry/function_promise_registry_v1_eab1_sidecar.md` SHA `8437894f7c72143bd3d1256fd78225d75ad0b100c5eeb96d3f00f39491ce61cb`. All 13 rows attach to existing v0.md §2 promises via foreign-key resolution. Conservation-not-authorship posture per Registry v1 §M G-2 precedent.

## Delta 7 · Parity 31 held

`backend/contracts/*.py` (31 files) + `backend/tests/invariants/*.contract_snapshot.json` (31 files) diff-empty · EAB-2's Parity 31→32 seal via `Service1Refusal@v1` remains future work.

## Delta 8 · Sequence progress + D-9 auto-proceed to EAB-2

Ratified sequence: EAB-1 CLOSED → **EAB-2 auto-proceeds** (Stage A opens next builder turn per standing ruling `docs/rulings/no_deferrals_d9_autoproceed_2026-07-15.md`). Sequence positions unchanged: 2 (EAB-2) · 3 (EAB-3) · 4 (Critic-pass) · 5 (G-13) · 6 (UI-1) · 7 (UI-2).

## Delta 9 · Phase Ledger figure attest

Part A: closed 38 (was 37) · open 1 (was 2; EAB-1 transitioned open→closed · sequencing_harness_stage_a remains open) · defined-undispatched 7 (unchanged; EAB-1 row-lifecycle-annotated) · denominator 46 · **figure `38/46 = 82.6%`**. Owner-verbatim standing rule: figure GROWS as phases close; growth is information, not a defect.

Part B: no state changes this atomic (owner-side deliverables unaffected).

## Delta 10 · Engine seats designed-empty · unchanged

Solva Probability weighting · Targeta yield layer · rung-3 owned text models remain designed-empty per v1.5 §5. Per D-12, seats fill at their evidence events; not gaps.

## Delta 11 · Governance stack unchanged this atomic

`docs/governance/registry_doctrine_v1.md` diff-empty this atomic (D-12 amendment carried from prior atomic).
`docs/governance/tiered_ruling_model.md` diff-empty this atomic (§20 + §21 carried from prior atomic).
Standing Rule v3 held: v0 lineage + v1.md + all requirements canon + all mandates + all rulings + registers v1.0..v1.5 + `/app/salvage/` + `backend/contracts/**` + snapshots + governance stack outside sanctioned amendments — **all `git diff --stat HEAD <path>` empty at close**.

## Delta 12 · Full-sweep verification

- pytest 1296 passed · 1 skipped · 0 failed (was 1279 · +17: AST cell 3 tests + EAB-1 pipeline 14 tests)
- Jest 154 passed · 24 suites (unchanged)
- Playwright chromium 2 passed (unchanged · trace smoke)
- MRR gates 7/7 GREEN (unchanged · no MRR touch this atomic)

---

*Outstanding-Work & Gap Register v1.6 · 2026-07-15 · Siblings pattern (v1.5 preserved byte-identical). Sequencing anchor: register v1.5 §15 Delta 8. Under D-12 · Standing Rule v3 · Parity 31.*
