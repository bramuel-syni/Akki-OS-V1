# Function/Promise Registry v1 · EAB-1 R4 sidecar

**Landed:** 2026-07-15 · EAB-1 execution atomic close.
**Pattern:** Registry Doctrine §5 v1-era sidecar (per Tiered-Ruling Model §14 sanctioned amendment). Landing companion for atomic execution close; conservation-not-authorship posture (Registry v1 §M G-2 precedent).
**Predecessor:** `docs/registry/function_promise_registry_v1.md` (SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a`) held byte-identical.
**Owner ruling anchor:** `docs/rulings/eab_1_e1_2026-07-15.md` (E1 · additive locator vocabulary + load-bearing AST cell).
**Stage A:** `docs/stage_a_proposals/eab_1_stage_a.md` (SHA `d5231d93c303ce2b163e2115cae3d507688693e4e58a122202ae825a4b4118dc`).

**Zero new promises minted.** All 13 rows attach to existing v0.md §2 promises via foreign-key resolution.

---

## §1 · Rows landed (13 total · 12 Rung-1 Deterministic · 1 Rung-2 audit)

| # | Row ID | Rung | Attest cell (path::test) | Promise attachment |
|---:|---|---:|---|---|
| 1 | `akki.perception.a1_demux_normalize` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a1_1_demux_deterministic_and_source_lineage_preserved` | `PROM-S1-frozen-wire-contract` |
| 2 | `akki.perception.a1_batch_segmentation_content_addressed` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a1_2_segmentation_content_addressed_and_range_gated` | `PROM-S1-frozen-wire-contract` |
| 3 | `akki.perception.a1_batch_schema_worker_contracts_not_frozen` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a1_2_batch_schema_lives_worker_side_not_in_contracts` | `PROM-S1-frozen-wire-contract` |
| 4 | `akki.perception.a1_vad_silero_registry_pinned` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a1_3_vad_silero_registry_pin_and_non_speech_indexed` (first attest) | `PROM-9-2a-real-worker-provenance` |
| 5 | `akki.perception.a1_non_speech_content_type_index` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a1_3_vad_silero_registry_pin_and_non_speech_indexed` (second attest) | `PROM-S3-audit-trail-immutable` |
| 6 | `akki.perception.a1_acoustic_fingerprint_dedup` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a1_4_dedup_first_occurrence_canonical_subsequent_emit_pointer` | `PROM-S1-honesty-grammar-source-labels` |
| 7 | `akki.perception.a1_gate_no_audio_bypass` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a1_a_rung1_gate_no_audio_bypasses_pipeline` | `PROM-S1-frozen-wire-contract` |
| 8 | `akki.perception.a1_per_month_report` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_ac_a1_b_reduction_ratio_report_shape` | `PROM-S3-audit-trail-immutable` |
| 9 | `akki.perception.a1_stratified_sample_audit_default_class` | 2 · Owner (or fixture) | *Pre-declared DEFAULT · verdict measurement fixture rides carrying phase's audit deployment (Stage A §3.C AC-A1.c · DEFAULT class · D-7 measurement not D-12 staged proving)* | `PROM-S1-honesty-grammar-source-labels` |
| 10 | `akki.perception.a1_news_block_dedup_exempt` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a1_4_ac_a1_d_news_blocks_dedup_exempt` | `PROM-S1-frozen-wire-contract` |
| 11 | `akki.perception.a2_occurrence_row_five_rings_zero_mutation` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a2_1_occurrence_unit_five_rings_zero_mutation_shape` + `backend/tests/invariants/test_five_rings_v0_zero_mutation_ast_cell.py::*` (3 sub-cells · **load-bearing AST cell fails hard on any mutation**) | `PROM-S1-frozen-wire-contract` |
| 12 | `akki.perception.a2_license_class_default_internal_only` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_a2_2_license_class_default_internal_only_fail_closed` | `PROM-S1-frozen-wire-contract` |
| 13 | `akki.perception.a2_canonical_occurrence_trace_walkable` | 1 · Deterministic | `backend/tests/test_eab_1_pipeline.py::test_fence_2_audit_walk_end_to_end_real_occurrence` (FENCE 2 · real occurrence unit · not synthetic) + `test_fence_1_trace_resolver_single_code_path_no_modality_branch` (FENCE 1 · AST attest single code path) | `PROM-S3-audit-trail-immutable` |

---

## §2 · Attestation summary

- **Row count:** 13 (12 at Rung-1 Deterministic · 1 at Rung-2 audit).
- **New promises minted:** 0 (all rows attach to existing v0.md §2 promises).
- **Attest-cell coverage:** every Rung-1 row has a green pytest cell. Rung-2 row (AC-A1.c) is a pre-declared DEFAULT threshold whose verdict is D-7 measurement at first production audit (not staged proving per D-12 · not a build-time gate).
- **Parity 31 attest:** `backend/contracts/*.py` byte-identical (31 files) · `backend/tests/invariants/*.contract_snapshot.json` byte-identical (31 files) · AST cell hard-verifies five_rings@v0 zero mutation.

---

## §3 · Foreign-key resolution against existing promises

- **`PROM-S1-frozen-wire-contract`** (v0.md §2 · v1.md §2 carrier): 7 rows attach — rows 1, 2, 3, 7, 10, 11, 12. Deterministic wire contracts for A1 pipeline outputs + A2 shape enforcement.
- **`PROM-9-2a-real-worker-provenance`** (v0.md §2 · v1.md §2 · Registry row `mtafiti.perception.pinned_model_provenance`): 1 row — row 4. Silero registry-pinning discipline.
- **`PROM-S1-honesty-grammar-source-labels`** (v0.md §2): 2 rows — rows 6, 9. Dedup honesty grammar + audit's honesty-in-verdict.
- **`PROM-S3-audit-trail-immutable`** (v0.md §2): 3 rows — rows 5, 8, 13. VAD content-type index + monthly report + canonical→occurrence walkability.

---

## §4 · Under D-12

Every row above deploys in force with known parameters (D-12 · Part IV of Registry Doctrine v1.0):
- Rows 1-3: deterministic transcoding + content-addressed segmentation + placement invariant (mechanics fully parameterized).
- Rows 4-5: registry-pinned model with pre-declared threshold; non-speech content-type index shape known.
- Rows 6, 10: dedup with pre-declared `fingerprint_hex_length=32` and `match_distance_threshold=0`; news-exempt list frozen at ingest.
- Row 7: gate refuses empty payload; deterministic parametric refusal.
- Row 8: report shape defined; measurable inputs are A1 outputs.
- Row 9: DEFAULT threshold `≤ 0.5%` is pre-declared; verdict at first production audit is D-7 measurement (not staged proving).
- Rows 11, 13: shared code path across base audio + occurrence units; AST cell fails hard on shape mutation; single-code-path resolver AST-attested.
- Row 12: MC-E4 α reuse; `internal_only` fail-closed default is the mechanic, not a trial mode.

**Zero observe-first · zero shadow phase · zero trial modes · zero staged proving anywhere.**

---

*R4 sidecar · EAB-1 · 2026-07-15 · lands under Registry Doctrine §5 v1-era sidecar pattern per Tiered-Ruling Model §14. Predecessor v1.md byte-identical (SHA `d6ad136f65426c0f`). Companion to: EAB-1 close report (`docs/close_reports/eab_1.md`) · EAB-1 Stage A proposal (`docs/stage_a_proposals/eab_1_stage_a.md`) · EAB-1 E1 ruling (`docs/rulings/eab_1_e1_2026-07-15.md`).*
