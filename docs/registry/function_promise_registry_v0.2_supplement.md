# Function & Promise Registry — v0.2 Supplement (Standing Queries SQ-G rows)

**Purpose:** carries this phase's (Standing Queries as CI · doctrine §8.1.a) own R4 reflexive Registry rows, landed per Owner ruling **SQ-E1 γ + cross-reference condition** (see `/app/docs/rulings/standing_queries_sq_e1.md`) and **governance §14** (additive-supplement discipline).

**Source lock:** primary source-of-truth `/app/docs/registry/function_promise_registry_v0.md` remains byte-identical at SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0`. Prior supplement `/app/docs/registry/function_promise_registry_v0.1_supplement.md` remains byte-identical at SHA `2822f99e0c20da6f8d02c1f33233965c90df37aeb6939e711da8df2ebd991092`.

**Combined source per §14:** `(v0.md + v0.1_supplement + v0.2_supplement)` ↔ `registry.yaml` — one set. MRR-G3 round-trip attests transparent extension to N supplements (path-list drives the check).

**Doctrine reference:** Registry Doctrine v1.0 §3.2 schema (11 mandatory fields) · §3.3 R4 · §8.1.a executable queries.

**Landed:** 2026-07-11 (atomic commit with SQ-E1 ruling + query engine + six findings artifacts + tests + close).

---

## §S1. R4 reflexive rows — SQ-G* gates (10 rows · §3.2 schema)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `registry.queries.q1_mechanical_correctness` (SQ-G1) | Named surfaces (Registry infrastructure · reflexive) | Built to attest Q1 (redundancy) mechanical scan emits every pair of function rows sharing PROM-token-set + surface equality; cost-ranking applies `unknown`-sorts-to-end. | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/queries.py::scan_q1_redundancy` + test cell | runtime check | 1 cell · µs class | machine form · function-row iteration | 1 · Deterministic | Owner |
| `registry.queries.q2_mechanical_correctness` (SQ-G2) | Named surfaces (Registry infrastructure · reflexive) | Built to attest Q2 (orphans) mechanical scan covers 4 sub-cases: (a) empty promise (b) no PROM-token resolves to promise_id (c) empty service_trace (d) service_trace step not in PART_II_JOURNEY_STEPS. READ-ONLY, never auto-retiring. | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/queries.py::scan_q2_orphans` + test cell | runtime check | 1 cell · µs class | PART_II_JOURNEY_STEPS · promises array | 1 · Deterministic | Owner |
| `registry.queries.q3_mechanical_correctness` (SQ-G3) | Named surfaces (Registry infrastructure · reflexive) | Built to attest Q3 (gaps) mechanical scan covers 2 sub-cases: (a) promise_id with zero citing functions (b) PART_II journey step with zero citing functions (alias-equivalence applied). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/queries.py::scan_q3_gaps` + test cell | runtime check | 1 cell · µs class | PART_II_JOURNEY_STEPS · promises array | 1 · Deterministic | Owner |
| `registry.queries.baseline_reproduction` (SQ-G-Baseline) | Named surfaces (Registry infrastructure · reflexive) | Built to attest archaeological carry-over files reproduce v0.md §4 (5 Q2), v0.md §5 (6 Q3), and consolidation_log_v0.md (Q1 tie-broke/merge decisions) byte-identical with `[RULED · …]` tags + `[OWNER: …]` markers preserved. Fail-loud + HALT for Owner on any deviation. | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_baseline` | byte-identity lock | 1 cell · ms class | rulings/registry_findings_01_to_11.md · consolidation_log_v0.md · v0.md §4/§5 | 1 · Deterministic | Owner |
| `registry.queries.cross_reference` (SQ-G-CrossRef) | Named surfaces (Registry infrastructure · reflexive) | Built to attest zero mechanical entries whose subject overlaps an existing archaeological finding are emitted without `overlaps: <finding_id>` annotation. Cross-reference discipline is PERMANENT per Owner-explicit "now or in any future run". | PROM-S3-audit-trail-immutable | S3.prove | `backend/services/registry/queries.py::annotate_mechanical_overlaps` + test cell | runtime check | 1 cell · µs class | archaeological-subjects index · mechanical scan output | 1 · Deterministic | Owner |
| `registry.queries.no_retirement` (SQ-G-NoRetirement) | Named surfaces (Registry infrastructure · reflexive) | Built to attest zero writes to source-of-truth artifacts (v0.md · v0.1_supplement · v0.2_supplement · consolidation_log_v0.md) during query run. Registry.yaml is regenerated (machine form is derived, not source). | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_no_retirement` | byte-identity lock (pre/post SHA-diff) | 1 cell · µs class | source-of-truth SHAs · run_queries CLI | 1 · Deterministic | Owner |
| `registry.queries.report_level` (SQ-G-ReportLevel) | Named surfaces (Registry infrastructure · reflexive) | Built to attest findings artifacts regenerate deterministically (byte-identical across successive runs) AND are report-level (never build-failing). Findings surface at `docs/registry/queries/` carrying `THIS ARTIFACT IS REPORT-LEVEL · NEVER BUILD-FAILING · RETIREMENT/MERGE REMAINS RULED ACTION` header. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_report_level` | runtime check + byte-identity | 1 cell · ms class | run_queries CLI · artifacts on disk | 1 · Deterministic | Owner |
| `registry.queries.rung_1` (SQ-G-Rung1) | Named surfaces (Registry infrastructure · reflexive) | Built to attest query engine module has zero LLM imports; every query runs rung 1 · Deterministic pure-function per Owner-explicit "Rung 1 throughout". | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_rung1` | AST negative-scan | 1 cell · µs class | queries.py source | 1 · Deterministic | Owner |
| `registry.queries.parity_31` (SQ-G-Parity) | Named surfaces (Registry infrastructure · reflexive) | Built to attest V1-G7 parity 31/31 byte-identical is unaffected by this phase. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_parity` | fs-count + hash-diff | 1 cell · µs class | existing V1-G7 gate | 1 · Deterministic | Owner |
| `registry.queries.data_blind` (SQ-G-DataBlind) | Named surfaces (Registry infrastructure · reflexive) | Built to attest zero secrets/keys/tokens in the six findings artifacts (regex-negative on standard secret patterns). | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_data_blind` | grep-negative | 1 cell · µs class | governance §8 data-blind posture | 1 · Deterministic | Owner |

**Row count:** 10 SQ-G# reflexive rows.

---

## §S2. Promise attribution notes

Zero new promises introduced (Owner-explicit "correct conservatism, noted"). All 10 SQ-G rows reuse existing v0.md §2 promises via foreign-key resolution (MRR-E3 β lock):

- **PROM-S1-frozen-wire-contract** (v0.md §2 · 7 rows) — SQ-G1 · SQ-G2 · SQ-G3 · SQ-G-NoRetirement · SQ-G-ReportLevel · SQ-G-Rung1 · SQ-G-Parity. Registry query engine is a wire-contract-integrity check; parity + report-level determinism + rung-1 posture all belong to frozen-wire-contract class.
- **PROM-S3-audit-trail-immutable** (v0.md §2 · 3 rows) — SQ-G-Baseline · SQ-G-CrossRef · SQ-G-DataBlind. Baseline reproduction is audit-trail-preservation of ruled findings; cross-reference discipline is audit-trail-integrity between archaeological + mechanical surfaces; data-blind is governance §8 audit-trail-adjacency.

D7 respected · zero candidate promises minted · conservation-not-authorship posture held.

---

## §S3. Standing consequence attest (governance §14 · MRR-E4 β)

This supplement instantiates the pattern ruled in **governance §14** applied to Standing Queries as CI (§8.1.a): additive supplements beside a locked source. v0.1_supplement remains byte-identical at MRR SHA; v0.2 is new sibling supplement. MRR-G3's round-trip operates over `(v0.md + v0.1_supplement + v0.2_supplement)` ↔ machine form as one set — path-list drives the check (one-line parser data extension).

═══════════════════════════════════════════════════════════════════

*End of v0.2 supplement. 10 R4 reflexive rows for SQ-G* gates. v0.md byte-identical at SHA `598a7ad4…` and v0.1_supplement byte-identical at SHA `2822f99e…` preserved. Standing Rule v3 · on-disk canonical.*
