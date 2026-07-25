# Function-Promise Registry v1 · EAB-3 Sidecar · 2026-07-24

**Class:** Sidecar per Registry Doctrine §5 v1-era pattern + Registry v1 §M reflexive-rows precedent + EAB-1 sidecar precedent (`docs/registry/function_promise_registry_v1_eab1_sidecar.md` · SHA `8437894f7c72143b`) + EAB-2 sidecar precedent (`docs/registry/function_promise_registry_v1_eab2_sidecar.md` · SHA `ddf89929ee072f7c`).

**Sanction:** `docs/rulings/eab_3_e1_2026_07_24.md` · SHA `319d9f14ce35625ed62bc8f033b48ea7f7bdc9522fb15fa191ec6e64e4bd371f` (Owner-authored 2026-07-25 · FINAL · composition (a1) single-contract landing).

**Landing atomic:** EAB-3 execution atomic 2026-07-24 (Parity 32→33 seal · `PartitionSchema@v0` landed at `backend/contracts/partition_schema.py` · single-contract landing per Owner ruling (a1)).

**Row count:** 15 rows · **zero new promises minted** (conservation-not-authorship posture per Registry v1 §M · EAB-1 + EAB-2 sidecar precedents).

**Enumeration source:** `docs/stage_a_proposals/eab_3_stage_a.md` §6 (15-row table pre-enumerated Stage A · landed byte-for-byte at execution atomic per §6 verbatim).

---

## §1 · Sidecar rows

| # | Row (dotted-name attest) | Rung | Promise attachment |
|---:|---|---:|---|
| 1 | `akki.partition.a5_partition_schema_v0_frozen_additive` — A5.1.1 new frozen contract at Parity 33 · additive-versioning attest · prior 32 contracts byte-identity preserved (Service1Refusal@v0 + Service1Refusal@v1 byte-identity guarded) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` |
| 2 | `akki.partition.a5_partition_schema_per_surface_key_configuration` — A5.1.2 keys are per-surface configuration; extension only via schema versioning per R-A5.1 verbatim | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 3 | `akki.partition.a5_partition_per_instance_scoping` — A5.1.3 partitions do not cross instance boundary · MC-E2 α reflexive discipline extended | 1 · Deterministic | `akki.instance.seams_scoped_by_instance_id` (v1 §S1 · MC-E2 α) |
| 4 | `akki.partition.a5_es1_ast_negative_scan_interactive_surface` — A5.2.1 ES-1 CI import/route check · AST negative-scan on any estate-query client reachable from interactive-surface code path | 1 · Deterministic | `PROM-S1-frozen-wire-contract` (structural invariance) |
| 5 | `akki.partition.a5_es1_scope_boundary_operational_record_whitelist` — A5.2.2 ES-1 scope-boundary respects Owner-ruled operational-record exemption (`es1_scope_2026-07-14.md`) · whitelist includes TraceReceipt / Compliance / AuditTrail / CommitReview / OpportunityBriefs surfaces | 1 · Deterministic | `PROM-S3-audit-trail-immutable` |
| 6 | `akki.partition.a5_refresh_cold_path_batch_job` — A5.3.1 partition refresh runs on cold-path batch job schedule · NOT request-time scheduler primitive · orthogonal to OD-10 census-scheduler | 1 · Deterministic | `PROM-S3-append-only-ledger` |
| 7 | `akki.partition.a5_atomic_promotion_previous_version_serves` — A5.3.2 previous partition version serves until new version is atomically promoted · zero read-time interruption during refresh · mechanical-audit-of-promotion extended from container-promotion to partition-promotion | 1 · Deterministic | `PROM-S3-mechanical-audit-of-promotion` |
| 8 | `akki.partition.a5_promotion_ledgered_immutable` — A5.3.3 partition-promotion writes append-only Northena ledger row · immutable · walkable | 1 · Deterministic | `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable` |
| 9 | `akki.partition.a5_session_cache_partition_version_binding` — A5.4.1 session-scoped cache binds to partition version · promotion invalidates dependents · one cited result NEVER mixes evidence versions · AC-A5.c version-skew wire attest | 1 · Deterministic | `PROM-S2-slice-freeze-at-commission` (slice-freeze-at-commission extended to session-freeze-at-open) |
| 10 | `akki.partition.a5_cache_references_and_arithmetic_never_raw` — A5.4.2 cache stores partition references + derived arithmetic ONLY · never re-materialized raw · no ungoverned data path | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` |
| 11 | `akki.partition.a5_cache_reads_inherit_session_purpose` — A5.4.3 cache reads inherit session's validated purpose · purpose validation is not bypassable through working-set path | 1 · Deterministic | `PROM-S3-audit-trail-immutable` (purpose-validated ledger-provenance) |
| 12 | `akki.partition.a5_no_targeta_cap_seat_contact_ast_negative` — §5.2 AST negative-scan · A5 session-working-set service imports NOT reaching Targeta eligibility modules (`gate.py` · `yield_layer.py`) · eligibility wall stands | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 13 | `akki.partition.a5_lineage_partition_version_receipt_set` — A5.5.1 every partition version records receipt set it was built from · walkable chain number → partition → receipts → operations | 1 · Deterministic | `PROM-S3-audit-trail-immutable` + `PROM-S3-append-only-ledger` |
| 14 | `akki.partition.a5_answer_citation_includes_partition_version` — A5.5.2 the citation IS the identifier the request touched · zero additional retrieval at request time | 1 · Deterministic | `PROM-S3-audit-trail-immutable` |
| 15 | `akki.parity.eab3_partition_schema_parity_33_attest` — Parity 33 attest cell asserts 33 contracts + 33 snapshots · V1-G7 bumps; Service1Refusal@v0 + Service1Refusal@v1 byte-identity attests extended (all 32 prior contracts byte-identical under new landing) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` |
| 16 | `akki.registry.eab3_sidecar_reflexive_row` — this sidecar itself · §14 pattern · §M reflexive-rows precedent · EAB-1 + EAB-2 sidecar precedents | 1 · Deterministic | Registry v1 §M sidecar-pattern authority |

---

## §2 · Promise attachment tally (zero new promises · conservation-not-authorship)

- `PROM-S1-frozen-wire-contract` — 6 attachments (rows 1, 2, 4, 12, 15, reflexive-carrier via §M)
- `PROM-S1-additive-versioning` — 2 attachments (rows 1, 15)
- `PROM-S1-honesty-grammar-source-labels` — 1 attachment (row 10)
- `PROM-S2-slice-freeze-at-commission` — 1 attachment (row 9)
- `PROM-S3-append-only-ledger` — 3 attachments (rows 6, 8, 13)
- `PROM-S3-audit-trail-immutable` — 4 attachments (rows 5, 8, 11, 13, 14)
- `PROM-S3-mechanical-audit-of-promotion` — 1 attachment (row 7)
- `akki.instance.seams_scoped_by_instance_id` (v1 §S1 · MC-E2 α) — 1 attachment (row 3)
- Registry v1 §M sidecar-pattern authority — 1 attachment (row 16)

**Zero new promises minted.** Every row targets an existing v1.md §2 promise (or Registry v1 §M authority for the reflexive row). Attachment-tally cross-verifies against Stage A §6 enumeration (per §6 footer verbatim).

---

## §3 · Cross-reference to on-disk cell landings

| Row | Test cell landing path |
|---:|---|
| 1 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_partition_schema_v0_additive_versioning_extends_parity_32` |
| 2 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_partition_schema_v0_field_count_9` (`key_dimensions: List[str]` field attest) |
| 3 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_partition_schema_v0_field_count_9` (`instance_id: str` field attest) |
| 4 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_ac_a5_c_es1_ci_import_check_green` |
| 5 | (whitelist attest carried in test cell #4 · operational-record exemption per Owner ruling `es1_scope_2026-07-14.md` L15-19) |
| 6 | `backend/services/partitions/session_working_set.py::promote_partition` (module-level attest · cold-path batch job discipline) |
| 7 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_partition_refresh_atomic_promotion_previous_serves_until_swap` |
| 8 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_partition_promotion_ledgered_append_only` |
| 9 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_ac_a5_c_version_skew_wire_cell_session_cannot_mix_versions` + `::test_session_working_set_promotion_invalidates_dependents` |
| 10 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_session_working_set_stores_references_and_arithmetic_only` |
| 11 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_session_working_set_purpose_inheritance` |
| 12 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_session_working_set_no_targeta_eligibility_import` |
| 13 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_lineage_partition_version_receipt_set_walkable` |
| 14 | (`answer_citation includes partition_version` · attest carried by test cell #13 · walkable both ways) |
| 15 | `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_parity_33_contracts_and_snapshots` + `::test_prior_32_contracts_byte_identity_under_eab3` + `::test_prior_32_snapshots_byte_identity_under_eab3` |
| 16 | this sidecar file (reflexive-row landing) |

Additional Owner ITEM 1 forward-binding attest: `backend/tests/invariants/test_partition_schema_v0_envelope.py::test_class_e_annotation_partition_shape_kind_registry_pinned` (Class E discipline attest · Change Order A3.4 forward-binding).

---

*EAB-3 R4 sidecar · 15 rows (+ 1 reflexive carrier · 16 total) · zero new promises minted · landed 2026-07-24 · Standing Rule v3 held · Parity 32→33 sealed · Registry v1 §M conservation-not-authorship posture · Owner ruling (a1) single-contract landing.*
