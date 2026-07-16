# Function-Promise Registry v1 · G-3 Sidecar · Operating Values v1.1 execution · 2026-07-15

**Sidecar pattern:** Tiered-Ruling §14 additive-supplement clause · v1-era pattern (sibling to consolidated `docs/registry/function_promise_registry_v1.md` at SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a`).
**Ruling authority:** `docs/rulings/g3_operating_values_v1_1_2026-07-15.md`.
**Conservation posture:** zero new promises minted; all rows attach to existing v0.md §2 promises (preserved in v1.md §v0-body byte-identical per RM-E1 α) via foreign-key resolution.
**Namespace:** `akki.registry.*` (post-MC-E6 β cutover · consistent with G-2 §M and v0.5 supplement §S1–§S6).
**Row count:** **6** (matches Stage A §6 pre-enumeration exactly; zero increment beyond the pre-enumerated set per Owner-verbatim *"G-3's sidecar grows only by rows its own execution mints"*).

═══════════════════════════════════════════════════════════════════

## §M — G-3 R4 reflexive rows (6 rows · Op. Values v1.1 execution)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `akki.registry.op_values_v1_1_sibling_landed_v1_0_byte_identical` | Named surfaces (Requirements canon · reflexive) | Built to attest Op. Values v1.1 sibling lands at `docs/requirements/operating_values_v1_1.md` AND v1.0 (`docs/requirements/operating_values_v1.md`) preserves byte-identity (SHA `a6c4a455175ef37dc71362aea2e41b2ce406baaf9a1c77b3f0f1326e0aa608ee`) per Standing Rule v3 · register-precedent sibling pattern (identical to `outstanding_work_and_gap_register_v1.{0..4}` chain). | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_g3_op_values_v1_1_execution.py::test_v1_0_diff_empty_at_v1_1_landing` + `test_v1_1_sibling_lands_on_disk` | byte-identity lock (SHA-pin on v1.0) + fs-check on v1.1 | 1 cell · µs class | requirements/*.md · SHA registry | 1 · Deterministic | Owner |
| `akki.registry.seam_values_carries_six_fields_post_g3` | Named surfaces (Multi-instance seam config · reflexive) | Built to attest `SeamValues` model (`backend/services/multi_instance/onboard_context.py`) carries exactly 6 fields post-G-3 (5 v1.0 seams + sixth: `quarantine_systemic_halt_threshold: float` DEFAULT 0.02 · G3-E1 α additive · non-breaking · no Parity contact); `extra="forbid"` remains binding; range check `[0.0, 1.0]` enforced. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_g3_op_values_v1_1_execution.py::test_seam_values_has_quarantine_threshold_field` + `test_seam_values_field_count_is_six` + `test_seam_values_quarantine_threshold_range_check` + `test_seam_values_extra_forbid_still_binding` | schema-shape check + pydantic validation | 1 cell · µs class | Pydantic BaseModel introspection | 1 · Deterministic | Owner |
| `akki.registry.s2_onboard_writes_eight_initial_set_rows` | Named surfaces (S2.onboard endpoint · reflexive) | Built to attest S2.onboard endpoint (`POST /api/instance/{instance_id}/onboard`) writes **8** `initial_set` ledger rows total per onboarding: **6 seam values** (deletion_consequence_classes · rule_tightening_delay_hours · objection_escalation_days · suspension_re_review_days · outer_gate_manual_review_threshold · **quarantine_systemic_halt_threshold [G-3 sixth]**) + estate_inventory + org_vocabulary_seat. Return payload carries `seam_values_ledgered: 6` + `total_initial_set_rows: 8`. MC-E3 α semantics unchanged. | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_g3_op_values_v1_1_execution.py::test_seam_keys_iteration_covers_six_names` + `backend/tests/registry/test_instance_fixture_b_walkthrough.py::test_s2_onboard_fixture_b_walkthrough` (E2E · asserts `seam_values_ledgered == 6` + `total_initial_set_rows == 8` post-G-3) | source-code AST scan + E2E mongo write | 2 cells · ms class | northena_ledger collection · s2_onboard router | 1 · Deterministic | Owner |
| `akki.registry.op_values_v1_1_per_language_gates_present_in_doc` | Named surfaces (Requirements canon · reflexive) | Built to attest Op. Values v1.1 §12 F1 subsection carries per-language WER ≤1.0pp gate + tagging F1 ≤1.5 points gate + perception-NO-efficiency-valve rule + text-tagging first-run-only valve permission (per EAB v1.1 §Part VII F1 line 157 verbatim absorption). | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_g3_op_values_v1_1_execution.py::test_f1_per_language_gates_present` | grep-positive on required strings in v1.1 body | 1 cell · µs class | operating_values_v1_1.md | 1 · Deterministic | Owner |
| `akki.registry.op_values_v1_1_no_run_without_telemetry_rule_present` | Named surfaces (Requirements canon · reflexive) | Built to attest Op. Values v1.1 §12 F3 subsection carries the "no run without telemetry" rule verbatim from EAB v1.1 §Part VII F3 line 161 + §Part VIII ES-3 line 169 binding. | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_g3_op_values_v1_1_execution.py::test_f3_telemetry_rule_present` | grep-positive | 1 cell · µs class | operating_values_v1_1.md | 1 · Deterministic | Owner |
| `akki.registry.op_values_v1_1_spacy_ner_rung_2_row_present` | Named surfaces (Requirements canon · reflexive) | Built to attest Op. Values v1.1 §1 carries spaCy NER conformance-correction row at Rung 2, fail-closed de-identification role in the Shield chokepoint — authorization `docs/rulings/outstanding_register_v1_amendment_2026-07-12.md:13` + `docs/audits/deviation_audit_v1.md:14` (RECONNECTED IF-1). | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_g3_op_values_v1_1_execution.py::test_spacy_ner_row_present_at_rung_2` | grep-positive | 1 cell · µs class | operating_values_v1_1.md | 1 · Deterministic | Owner |

**Row count: 6.** All rows target existing v0.md §2 promises (`PROM-S1-frozen-wire-contract` × 4 + `PROM-S3-audit-trail-immutable` × 2). Zero new promises minted. Ladder rung 1 (Deterministic) uniform.

═══════════════════════════════════════════════════════════════════

## §M · Additional attest cells (execution-adjacent · G-3 sidecar-companion coverage · zero R4 rows)

The following test cells run alongside the 6 R4 rows above but do NOT constitute additional R4 rows in the sidecar (per Owner-verbatim *"G-3's sidecar grows only by rows its own execution mints"* → sidecar row count remains **6**). These are execution-adjacent coverage attestations that reuse existing R4 row attribution:

- `test_tq_5_1_speech_values_absorbed_by_citation` — attests TQ §5.1 absorption-by-citation discipline (VAD-loss · LID · de-id recall citations present in v1.1 body).
- `test_tq_6_moac_absorbed_by_citation` — attests TQ §6 MOAC (M-a..M-f) citation set present in v1.1 body.
- `test_g3_ruling_record_lands_on_disk` — attests `docs/rulings/g3_operating_values_v1_1_2026-07-15.md` presence + G3-E1 + G3-E2 body references.

These 3 execution-adjacent cells attach to the existing R4 rows above via composite attest surfaces (they verify the CITATION discipline that satisfies rows #4/#5/#6's mandate that "v1.1 body carries the F1/F3/spaCy content"). No sidecar-row inflation.

═══════════════════════════════════════════════════════════════════

*End of G-3 Sidecar. Six R4 rows minted per Stage A §6 pre-enumeration. Zero increment beyond pre-enumerated. Zero new promises. Parity 31 held byte-identical. Registry v1.md byte-identical at SHA `d6ad136f…`. Standing Rule v3 · on-disk canonical.*
