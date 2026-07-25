# Critic-pass R4 Sidecar · Function Promise Registry v1

**Landing atomic:** Critic-pass execution atomic · 2026-07-25 (Parity 33 held byte-identical).
**Sanction:** `docs/rulings/critic_pass_e1_2026_07_25.md` · SHA `42ca9e0f4605b497394772c83572b1e7c5469e17b2c6f7fa39452ec45992c80a` (Owner ruling composition (a1) + Binding B-1 · 2026-07-25 · FINAL).
**Parent:** `docs/registry/function_promise_registry_v1.md` · SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a` (unchanged).
**Sibling precedents:**
  * EAB-1 sidecar: `docs/registry/function_promise_registry_v1_eab1_sidecar.md` · SHA `8437894f7c72143bd3d1256fd78225d75ad0b100c5eeb96d3f00f39491ce61cb`.
  * EAB-2 sidecar: `docs/registry/function_promise_registry_v1_eab2_sidecar.md` · SHA `ddf89929ee072f7c06436c34de5c9c34d8a274c9715f98f96492ef2c7fb067c9`.
  * EAB-3 sidecar: `docs/registry/function_promise_registry_v1_eab3_sidecar.md` · SHA `6368f3a1007492e243d2bcaf6db6d3c70d5ccc3097c2d1eb89c8becf50521672`.
**Discipline:** conservation-not-authorship per Registry v1 §M · zero new promises minted · all rows attach to existing v1.md §2 promise IDs by foreign-key resolution.

---

## §1 · R4 rows landed at this atomic (18 rows + 1 reflexive)

| # | Sidecar row | Rung | Promise attachment |
|---:|---|---:|---|
| 1 | `akki.critic.rv1_assertion_boundary_trace_cell` — RV-1 assertion-boundary trace (Critic Seam v1.0 §5) | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` |
| 2 | `akki.critic.rv2_scope_anchor_trace_cell` — RV-2 scope-anchor trace (Critic Seam v1.0 §5) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 3 | `akki.critic.rv3_registry_attribution_cell` — RV-3 registry attribution (Critic Seam v1.0 §5) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 4 | `akki.critic.rv4_schema_completeness_hard_gate_qa2` — RV-4 schema-completeness (QA-2 hard gate · Critic Seam v1.0 §5 + §8) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 5 | `akki.critic.rv5_standing_rule_v3_predecessor_byte_identity` — RV-5 predecessor byte-identity attest (Critic Seam v1.0 §5) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` |
| 6 | `akki.critic.rv6_parity_attest` — RV-6 parity count attest (Critic Seam v1.0 §5) | 1 · Deterministic | `PROM-S3-frozen-contract-parity-attest` |
| 7 | `akki.critic.cr1_anti_re_derivation_rubric_cell` — CR-1 anti-re-derivation (Critic Seam v1.0 §6.1) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 8 | `akki.critic.cr2_anti_fabrication_rubric_cell` — CR-2 anti-fabrication (Critic Seam v1.0 §6.1) | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` |
| 9 | `akki.critic.cr3_conflation_test_d3_rubric_cell` — CR-3 conflation test (Critic Seam v1.0 §6.1) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 10 | `akki.critic.cr4_scope_semantics_d7_rubric_cell` — CR-4 scope semantics (Critic Seam v1.0 §6.1) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 11 | `akki.critic.cr5_enforcement_honesty_d5_rubric_cell` — CR-5 enforcement honesty (Critic Seam v1.0 §6.1) | 1 · Deterministic | `PROM-S3-mechanical-audit-of-promotion` |
| 12 | `akki.critic.cr6_self_audit_audit_rubric_cell` — CR-6 self-audit audit (Critic Seam v1.0 §6.1) | 1 · Deterministic | `PROM-S3-mechanical-audit-of-promotion` |
| 13 | `akki.critic.cr7_cif_selection_defect_checklist_rubric_amendment` — CR-7 CIF selection-defect checklist (CIF §6 A5.2 verbatim: *"enters standing machinery as a Critic Seam rubric amendment (CR-7)"*) | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` |
| 14 | `akki.critic.qa1_detect_never_decide_binding` — QA-1 detect-never-decide (Critic Seam v1.0 §8) | 1 · Deterministic | `PROM-S1-refusal-taxonomy-closed` |
| 15 | `akki.critic.qa7_custody_boundary_protection_governance_utility_findings` — QA-7 custody boundary (TQ §7 line 125 RULED · rides EAB-2 `backend/services/service_1/batch_quarantine.py` machinery) | 1 · Deterministic | `PROM-S3-audit-trail-immutable` |
| 16 | `akki.critic.cif_manifest_schema_format_gate_at_submission` — CIF manifest schema (Owner-ruled (a1) additive fields on 3 existing frozen contracts · `MiningPlan` · `PerceptionJob_v0` · `FeasibilityResult_v0` · B-1 hard-fail gate at submission per CIF §12 line 152) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` |
| 17 | `akki.critic.archive_ledger_append_only_cif_entry_1_seed` — archive ledger append-only + CIF-entry-#1 seed row (CIF §12 line 154 + §14.2) | 1 · Deterministic | `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable` |
| 18 | `akki.critic.calibration_ledger_staleness_window_class_e_deterministic_decay` — calibration ledger with 10-phase staleness window + Class E deterministic sampling-rate decay function (Owner-ruled DECLINED early E→O promotion · pinned per engine version) | 1 · Deterministic | `PROM-S3-audit-trail-immutable` |

**Reflexive sidecar-file row (per EAB-1/EAB-2/EAB-3 precedent · Registry v1 §M):**

| # | Sidecar row | Rung | Promise attachment |
|---:|---|---:|---|
| 19 | `akki.registry.critic_pass_sidecar_reflexive_row` — this sidecar file itself · lands at Critic-pass execution atomic · attaches to Registry v1 §M sidecar-pattern authority | 1 · Deterministic | Registry v1 §M sidecar-pattern authority |

**Total rows: 18 R4 rows + 1 reflexive-sidecar-carrier row = 19 rows. Zero new promises minted.**

---

## §2 · Additional cross-references (annotations · not new rows)

| Attach point | Annotation |
|---|---|
| `PROM-S1-frozen-wire-contract` | Under Owner ruling (a1) at Critic-pass execution atomic, additive fields (`manifest_entries: List[ManifestEntry]`) landed on 3 existing frozen wire contracts: `MiningPlan` @ `targeta_plan.py` (SHA `4dfb8177d60900d5…`), `PerceptionJob_v0` @ `perception_job_v0.py` (SHA `7b1ec98d0cd166ed…`), `FeasibilityResult_v0` @ `feasibility_result.py` (SHA `e979e5155820a2c2…`). The 30 unchanged frozen contracts remain byte-identical. Parity count 33 held. |
| `PROM-S1-additive-versioning` | ManifestEntry sub-shape is FROZEN on landing (Owner ruling verbatim: *"ManifestEntry is frozen on landing; its evolution is additive (ManifestEntry_v1), same as any contract"*). Inline discipline: each of the 3 consumer contracts carries a local `ManifestEntry` sub-shape (byte-identical shape · uniform across consumers) — no new `backend/contracts/*.py` file added (Parity 33 count preserved). |
| `PROM-S3-append-only-ledger` | Critic-pass archive ledger + calibration ledger both ride existing Northena append-only ledger discipline. CIF §14.2 seed row (CIF as entry #1) lands via `initialize_with_cif_seed()` — idempotent. |
| `PROM-S3-audit-trail-immutable` | Archive `ArchiveLedgerRow` + calibration `CalibrationRow` are frozen dataclasses (immutable by construction). Standing query `evaluated_but_unarchived_query()` surfaces findings without editing the ledger. |
| Rules Taxonomy A3.4 (class-D lifecycle) | Seeded-defect corpus at `backend/services/critic_pass/seeded_defect_corpus.py` implements A3.3 asymmetry with Owner-extended edit-gating: additions immediate · removals require approval · edits require approval (Owner ruling verbatim: *"an edit to a seeded defect changes what the catch-rate measures, so gating edits is correct there too"*). |
| Rules Taxonomy A3.4 (class-E deterministic decay) | Verdict sampling rate lands at `backend/services/critic_pass/calibration_ledger.py::sampling_rate_findings()` as a deterministic decay function — pinned per engine version `critic-pass-v0` (initial 20% · half-life 20 phases · floor 2%). Owner DECLINED early E→O promotion (without prejudice). |

---

*Critic-pass R4 sidecar v1.0 · Landed 2026-07-25 · Owner ruling composition (a1) + Binding B-1. Parent registry `docs/registry/function_promise_registry_v1.md` byte-identical. Zero new promises minted. Standing Rule v3 held.*
