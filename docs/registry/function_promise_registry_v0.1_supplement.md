# Function & Promise Registry — v0.1 Supplement (R4 reflexive rows)

**Purpose:** carries this phase's (Machine-Readable Registry · doctrine §8.1.d) own R4 reflexive Registry rows, landed per **MRR-E4 β** ruling (see `/app/docs/rulings/machine_readable_registry_mrr_e1_to_e4.md` §5) and **governance §14** (see `/app/docs/governance/tiered_ruling_model.md` §14 · standing consequence).

**Source lock:** primary source-of-truth `/app/docs/registry/function_promise_registry_v0.md` remains byte-identical at SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0`. This supplement extends the queryable Registry via additive-supplement discipline (governance §14); combined source `(v0.md + this supplement)` is what MRR-G3 round-trip operates over.

**Doctrine reference:** Registry Doctrine v1.0 (SHA `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471`) §3.2 schema (11 mandatory fields) · §3.3 R4 (new functions register before they land) · §8.1.d (machine-readable form).

**Landed:** 2026-07-11 (atomic commit with MRR-E1..E4 rulings + machine form + parser + validator + tests + close).

---

## §S1. R4 reflexive rows — MRR-* gates (7 rows · §3.2 schema)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `registry.machine_form.schema_conformance` (MRR-G1) | Named surfaces (Registry infrastructure · reflexive) | Built to attest every mandatory §3.2 field is present in every row of the machine form and every value matches the schema type. | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g1_schema_conformance` + `backend/tests/registry/test_machine_readable_registry_mrr_g1_to_g6.py::test_mrr_g1_schema_conformance` | runtime check | 1 cell · µs class | v0.md source · v0.1_supplement · schema formalization per doctrine §3.2 | 1 · Deterministic | Owner |
| `registry.machine_form.vocabulary_lock` (MRR-G2) | Named surfaces (Registry infrastructure · reflexive) | Built to attest (a) foreign-key promise integrity — every function row's `promise` field resolves to an existing top-level `promises` array `promise_id` (β lock) — AND (b) `service_trace` step values are members of `PART_II_JOURNEY_STEPS` constant sourced verbatim from doctrine Part II (addition lock). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g2_vocabulary_lock` + test cell | runtime check | 1 cell · µs class | v0.md §2 promises · doctrine Part II lines 32-36 verbatim · governance-amendment-only | 1 · Deterministic | Owner |
| `registry.machine_form.round_trip` (MRR-G3) | Named surfaces (Registry infrastructure · reflexive) | Built to attest byte-identical round-trip integrity over combined `(v0.md + v0.1_supplement.md)` ↔ machine form per Owner-explicit MRR-E1 α + MRR-E4 β + governance §14 (round-trip operates over supplements-plus-source as one set). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g3_round_trip` + test cell | byte-identity lock | 1 cell · µs class | parser · MRR-E1 α direction | 1 · Deterministic | Owner |
| `registry.machine_form.findings_coverage` (MRR-G4) | Named surfaces (Registry infrastructure · reflexive) | Built to attest all 11 findings from `/app/docs/rulings/registry_findings_01_to_11.md` are carried in machine form with `[RULED · …]` disposition tags byte-identical AND `[OWNER: …]` markers preserved verbatim AND dual-surface archival posture (inline rulings + findings_supersession_ledger) landed per MRR-E2 γ. | PROM-S3-audit-trail-immutable | S3.prove | `backend/services/registry/validator.py::check_mrr_g4_findings_coverage` + test cell | grep-negative + structured-path check | 1 cell · µs class | `rulings/registry_findings_01_to_11.md` · v0.md §4/§5/§7 · MRR-E2 γ ruling | 1 · Deterministic | Owner |
| `registry.machine_form.parity_31` (MRR-G-Parity) | Named surfaces (Registry infrastructure · reflexive) | Built to attest V1-G7 parity 31/31 byte-identical is unaffected by this phase (contract count preserved + snapshot count preserved). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g_parity` + test cell | fs-count + hash-diff | 1 cell · µs class | existing V1-G7 parity gate · `backend/contracts/` · `backend/tests/invariants/` | 1 · Deterministic | Owner |
| `registry.machine_form.data_blind` (MRR-G-DataBlind) | Named surfaces (Registry infrastructure · reflexive) | Built to attest no secrets, keys, tokens, or credential material appear in machine form or supplement (regex-negative on standard secret patterns). | PROM-S3-audit-trail-immutable | S3.prove | `backend/services/registry/validator.py::check_mrr_g_data_blind` + test cell | grep-negative | 1 cell · µs class | governance §8 data-blind posture · v0.md convention | 1 · Deterministic | Owner |
| `registry.machine_form.source_sha_pin` (MRR-G-SourceSHA) | Named surfaces (Registry infrastructure · reflexive) | Built to attest machine form embeds top-level `source_of_truth: {path, sha256}` referencing v0.md at its ruled SHA `598a7ad4…` per MRR-E1 α integrity-binding condition. Machine form that cannot name its source fails this gate (Owner-verbatim: "an unattributed claim"). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g_source_sha` + test cell | runtime check + byte-identity lock | 1 cell · µs class | MRR-E1 α condition · parser embed-sha logic | 1 · Deterministic | Owner |

**Row count:** 7 R4 reflexive rows.

---

## §S2. Promise attribution notes

Zero new promises introduced. All 7 R4 rows reuse existing v0.md §2 promises via foreign-key resolution (MRR-E3 β lock):

- **PROM-S1-frozen-wire-contract** (v0.md §2) — sub-covers schema/vocab/round-trip/parity/source-SHA integrity (Registry itself is a wire contract; byte-identity discipline extends naturally).
- **PROM-S3-audit-trail-immutable** (v0.md §2) — sub-covers findings-coverage (archival-preservation posture · governance §8 data-blind adjacency).

D7 respected: no candidate-promise introduction; conversion-not-authorship posture held.

---

## §S3. Standing consequence attest (governance §14 · MRR-E4 β)

This supplement instantiates the pattern ruled in **governance §14** (Owner 2026-07-11 · from MRR-E4 β): additive supplements beside a locked source, consolidated into the next Registry version at a future owner-dispatched maintenance turn. MRR-G3's round-trip operates over `(v0.md + v0.1_supplement.md)` ↔ machine form as one set.

Future phases where a locked source-of-truth prevents in-place R4 row addition land their R4 rows via the same pattern.

═══════════════════════════════════════════════════════════════════

*End of v0.1 supplement. 7 R4 reflexive rows for MRR-* gates. v0.md byte-identical at SHA `598a7ad4…` preserved. Standing Rule v3 · on-disk canonical.*
