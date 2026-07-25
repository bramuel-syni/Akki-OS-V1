# G-13 R4 Sidecar · Function Promise Registry v1

**Landing atomic:** G-13 execution atomic · 2026-07-25 (Parity 33→34 sealed at `MandateSpec@v0`).
**Sanction:** `docs/rulings/g_13_e1_e2_e3_2026_07_25.md` · SHA `6abdde0072affbe48758922330aa627ccd25767ac0674f44b1e89a51f49a64f7` (Owner ruling composition (b · a · a) + B-1/B-2/B-3 · 2026-07-25 · FINAL · non-re-openable · not builder-modifiable).
**Parent:** `docs/registry/function_promise_registry_v1.md` · SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a` (unchanged).
**Sibling precedents:**
  * EAB-1 sidecar · SHA `8437894f7c72143bd3d1256fd78225d75ad0b100c5eeb96d3f00f39491ce61cb`
  * EAB-2 sidecar · SHA `ddf89929ee072f7c06436c34de5c9c34d8a274c9715f98f96492ef2c7fb067c9`
  * EAB-3 sidecar · SHA `6368f3a1007492e243d2bcaf6db6d3c70d5ccc3097c2d1eb89c8becf50521672`
  * Critic-pass sidecar · SHA `a46e41f94359d5758c1c0b6a5739031df372868a2c4534045b1595b5d48c50ce`
**Discipline:** conservation-not-authorship per Registry v1 §M · zero new promises minted.

---

## §1 · R4 rows landed at this atomic (16 rows + 1 reflexive = 17)

| # | Sidecar row | Rung | Promise attachment |
|---:|---|---:|---|
| 1 | `akki.sequencing_harness.registered_function_executor` — A.SH.1 · dispatches registered functions against fixture traffic (Registry Doctrine §5.2 verbatim) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 2 | `akki.sequencing_harness.candidate_ordering_enumerator` — A.SH.2 · reads Registry cost + dependency fields (Registry Doctrine §5.2 verbatim) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 3 | `akki.sequencing_harness.ordering_optimizer` — A.SH.3 · cheap-before-expensive · deterministic-before-model · fail-fast-surfaced (Registry Doctrine §5.2 verbatim) | 1 · Deterministic | `PROM-S3-mechanical-audit-of-promotion` |
| 4 | `akki.sequencing_harness.fixture_traffic_ingest` — A.SH.4 · rides existing backend/tests/fixtures/ per §5.4 downgrade | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 5 | `akki.sequencing_harness.real_cost_measurement_cell` — A.SH.5 · rung-1/rung-2 exact measurement | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` |
| 6 | `akki.sequencing_harness.statistical_cost_measurement_cell` — A.SH.6 · rung-3/rung-4 statistical N=10 · α=0.05 · Class E pinned per sequencing-harness-v0 | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` + `PROM-S1-runtime-transient-never-refusal` |
| 7 | `akki.sequencing_harness.measurement_ledger_append_only` — A.SH.7 · frozen dataclass rows · immutable | 1 · Deterministic | `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable` |
| 8 | `akki.sequencing_harness.measured_best_path_emitter_registry_backfill` — A.SH.8 · lowest-score ordering + registry cost back-fill map | 1 · Deterministic | `PROM-S3-mechanical-audit-of-promotion` |
| 9 | `akki.registry_context.functions_in_scope_resolver` — B.WCH.1 · static-declared-list posture at landing | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 10 | `akki.registry_context.registry_row_triplet_reader` — B.WCH.2 · mandate + promise + service_trace triplet | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 11 | `akki.registry_context.operating_prompt_injector_single_writer_b1` — B.WCH.3 · **single-writer discipline per Owner Binding B-1** · block emitted by prompt_builder.py alone · content sourced from Registry record · never hand-authored · golden-snapshot cell asserts byte-identical rendered serialization for fixture function `PROM-S1-frozen-wire-contract` | 1 · Deterministic | Service-layer only per Owner §5.1 (b) ruling (no frozen wire contract touch · Parity 33 held at this row) |
| 12 | `akki.registry_context.three_role_attest` — B.WCH.4 · source of truth for humans + compile-source for gates + system context for workers (Registry Doctrine §6.2 verbatim) | 1 · Deterministic | Registry v1 §M sidecar-pattern authority |
| 13 | `akki.registry_context.context_injection_audit_ledger` — B.WCH.5 · append-only per-invocation logging (deferred to future atomic per this landing's minimal-viable posture) | 1 · Deterministic | `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable` |
| 14 | `akki.far_endpoint.mandate_reader_parser` — C.FE.1 · parses `docs/mandates/*.md` into ParsedMandate | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 15 | `akki.far_endpoint.mandate_spec_emitter_deterministic_b2` — C.FE.2 · **MandateSpec@v0 frozen contract landing · Parity 33→34 seal** · YAML output at `docs/generated/mandate_specs/*.yaml` · **Binding B-2 regeneration-diff cell** asserts on-disk YAML byte-identical to fresh emitter output · generated-do-not-edit headers with source + SHA + generator + regenerate lines · orphan-mandate + shadow-canon prevention cells | 1 · Deterministic | `PROM-S1-additive-versioning` (MandateSpec@v0 additive first-issue) + `PROM-S3-frozen-contract-parity-attest` (Parity 34 attest) |
| 16 | `akki.far_endpoint.gate_generator_stubs_with_source_anchors_b3` — C.FE.3 + C.FE.4 · Python function stubs at `backend/services/generated_gates/<spec_id>.py` · source-anchor docstrings per gate · **Binding B-3 regeneration-diff + import-and-invoke smoke cells** ensure generated code cannot rot as unexecuted text | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` (source-anchor docstring) + service-layer only per Owner §5.3 (a) ruling |

**Reflexive sidecar-file row (per EAB-1/EAB-2/EAB-3/Critic-pass precedent · Registry v1 §M):**

| # | Sidecar row | Rung | Promise attachment |
|---:|---|---:|---|
| 17 | `akki.registry.g_13_sidecar_reflexive_row` — this sidecar file itself · lands at G-13 execution atomic · attaches to Registry v1 §M sidecar-pattern authority | 1 · Deterministic | Registry v1 §M sidecar-pattern authority |

**Additional cross-attach (annotation · not a new row):**

| # | Attach point | Note |
|---:|---|---|
| — | `akki.registry.instance_replication_playbook_v1_document_class_landing` (annotation only) | Instance Replication Playbook v1 landed at `docs/mandates/instance_replication_playbook_v1.md` · document class per Registry Doctrine §8.1 line 159 · content evolution Owner-word-driven · out of code-level Registry v1 §2 promise-ID attachment scope (annotation lives here for cross-reference completeness) |

**Total rows: 16 R4 + 1 reflexive = 17 rows. Zero new promises minted.** Conservation-not-authorship posture per Registry v1 §M.

---

## §2 · Cross-references (annotations · not new rows)

| Attach point | Annotation |
|---|---|
| `PROM-S1-frozen-wire-contract` | Under Owner ruling §5.2 (a) at G-13, `MandateSpec@v0` lands as a NEW frozen wire contract at `backend/contracts/mandate_spec_v0.py` (SHA `0d3f6de687c1543a61822e460cda93e0fb1d7208be39cc9a9518005abd24b1a7`). Parity 33→34 sealed. The 33 prior frozen contracts remain byte-identical (Standing Rule v3 held). |
| `PROM-S1-additive-versioning` | `MandateSpec@v0` is v0-first-issue · frozen on landing · evolution is additive (`MandateSpec_v1` at future seal). |
| `PROM-S3-frozen-contract-parity-attest` | Parity 34 attest lands at `test_partition_schema_v0_envelope.py::test_parity_33_contracts_and_snapshots` (name preserved for git-blame continuity · asserts 34 contracts + 34 snapshots · Owner-verbatim Parity 33→34 sealed). Companion attests at `test_9_2a_real_perception.py` + `test_production_housing_ph_g1_to_g6.py` + `test_critic_pass_execution_atomic.py`. |
| `PROM-S1-honesty-grammar-source-labels` | Every generated gate function carries a source-anchor docstring (Owner ruling §5.3 (a) verbatim) · every generated YAML spec carries source + SHA + generator + regenerate lines (Owner ruling §5.2 (a) verbatim). |
| `PROM-S3-append-only-ledger` | Sequencing-harness measurement ledger + Critic-pass archive ledger + Critic-pass calibration ledger all ride the same append-only discipline. G-13 measurement ledger rows are frozen dataclasses (immutable). |
| Rules Taxonomy A3.4 (Class E deterministic decay + pinning) | Two Class E parameters land pinned per engine version `sequencing-harness-v0`: `REPETITION_COUNT=10` + `SIGNIFICANCE_ALPHA=0.05` (Owner ruling §5.5 verbatim: *"approved as pinned values [...] neither shows a promotion trigger. No early E→O promotions"*). |
| Owner Binding B-1 (single-writer discipline) | Rendered registry-context block has EXACTLY ONE writer (`prompt_builder.py`). AST-scan cell asserts no other file emits the block-header sentinel. Golden-snapshot cell asserts byte-identical rendered serialization for fixture function `PROM-S1-frozen-wire-contract`. |
| Owner Binding B-2 (regeneration-diff + shadow-canon prevention) | CI cell regenerates every mandate spec and byte-diffs against on-disk YAML. Orphan-mandate cell + stray-spec cell close both directions of the shadow-canon vector. |
| Owner Binding B-3 (regeneration-diff + import-and-invoke smoke) | CI cell regenerates every gate module and byte-diffs. Import-and-invoke smoke cell family (parameterized per generated module) asserts every gate function is callable. |

---

*G-13 R4 sidecar v1.0 · Landed 2026-07-25 · Owner ruling composition (b · a · a) + B-1/B-2/B-3. Parent registry `docs/registry/function_promise_registry_v1.md` byte-identical. Zero new promises minted. Parity 33→34 sealed at MandateSpec@v0. Standing Rule v3 held.*
