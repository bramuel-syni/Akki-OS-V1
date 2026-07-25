# EAB-3 · Stage A Proposal

**Phase:** EAB-3 · A5 (Precomputed evidence partitions + session working set)
**Dispatch class:** D-9 auto-proceed under standing ruling `docs/rulings/no_deferrals_d9_autoproceed_2026-07-15.md` (SHA `1f5ea9de8031cde255db0efd476074c9c3c9f8cc05ead2f20171dbb5c0d81d1d`) following clean close of EAB-2 execution atomic (2026-07-24 · close report `docs/close_reports/eab_2.md` SHA `0de07b1727c7b5a8f333e3b6b4c79b1cea94efebfd9ed00e5e9f715c08c1578e` · Parity 31→32 sealed · full-sweep 1,526 cells green).
**Sequence position:** 3 of 7 (per phase ledger `docs/registers/phase_ledger_v1.md` §5 · SHA `b8928cc65ebdc190f801da1042ea2a88b1a6d1cdda76f537605e2ad38bd9e382`).
**Source of truth:** EAB Tier-1 Adoption Spec v1.1 (`docs/requirements/eab_tier1_adoption_spec_v1.1.md` · SHA `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9`) · Part VI (A5) + §IX Execution model + ES-1 (Part VIII).

---

## §1 · Purpose + scope (Owner-dispatched · verbatim absorption)

EAB v1.1 §IX Execution model verbatim: *"Phase EAB-3 = A5 (serving pattern; may ride a first-party surface as its proving consumer). Split/merge is builder Tier-3 at Stage A, disclosed."*

EAB v1.1 §IX pre-naming verbatim: *"partition-schema contract class (A5; new artifact class → registered, additive)."*

**Builder Tier-3 disclosure: NO SPLIT** — R-A5.1 · R-A5.2 · R-A5.3 · R-A5.4 · R-A5.5 co-land as a single execution atomic. Rationale:
1. All five requirements interlock on a single partition-schema anchor: R-A5.2's ES-1 check requires R-A5.1 partition schema exists to be enforced against; R-A5.4 session-working-set binds to R-A5.1 partition-version; R-A5.5 lineage records the R-A5.3-promoted partition versions; R-A5.3 refresh discipline invalidates R-A5.4 session-working-set on atomic promotion.
2. §IX explicitly names EAB-3 = A5 (one fold family, not a split family).
3. Splitting R-A5.1 (contract) from R-A5.4 (session-working-set) would land the contract without its proving consumer, contradicting D-12 (*"the capability deploys in force"*).
4. The Parity 32→33 seal is a single sanctioned event; splitting the atomic across two commits would either (a) double-seal (defect) or (b) leave R-A5.4 session-working-set binding to a partition-version before the schema is Parity-sealed (order-of-operations defect). Single-seam execution is the only defect-free ordering.

**Adopted mechanics landing in EAB-3 (EAB v1.1 Part VI verbatim):**

**R-A5.1 · Partitions** (Part VI §6.2 line 137 verbatim): *"Evidence consumed by interactive surfaces is precomputed into versioned, columnar, memory-mappable partitions keyed on the dimensions the surface actually queries (keys are per-surface configuration; extension only via schema versioning). A request is partition reads plus arithmetic."*

**R-A5.2 · The estate-query prohibition (rule ES-1)** (Part VI §6.2 line 139 verbatim): *"Interactive-surface code MUST NOT query the raw or qualified estate at request time. Enforced at rung 1: a CI import/route check proves no estate-query client is reachable from interactive-surface code. Exceptions exist only by recorded Owner-tier ruling naming the latency consequence."*

**ES-1 scope (Owner-ruled 2026-07-14 · `docs/rulings/es1_scope_2026-07-14.md` · SHA `a4675cd83c4e500a2a36652fc8205e87e9dc1584228f508279b5736d595ac3a3` · verbatim line 9):** *"ES-1 scope = evidence-assembly reads — request-time queries over the raw estate or the qualified-unit corpus to compose an answer, simulation, or brief. Operational-record reads are outside ES-1 — ledger rows, receipts, plans, registry metadata, audit logs read by surfaces whose product is those records."*

**R-A5.3 · Refresh discipline** (Part VI §6.2 line 141 verbatim): *"Partition refresh is a cold-path batch job; the previous version serves until the new version is atomically promoted; promotion is ledgered."*

**R-A5.4 · Session working set** (Part VI §6.2 line 143 verbatim): *"Iterative surfaces (adjust→re-ask) reuse session-loaded partitions and intermediate aggregates; only deltas recompute. Cache entries bind to partition version — promotion invalidates dependents, so one cited result NEVER mixes evidence versions. Cache stores partition references + derived arithmetic, never re-materialized raw — no ungoverned data path; cache reads inherit the session's validated purpose."*

**R-A5.5 · Lineage** (Part VI §6.2 line 145 verbatim): *"Every partition version records the receipt set it was built from; every answer cites partition versions; the chain number→partition→receipts→operations is mechanically walkable with zero additional retrieval at request time (the citation IS the identifier the request touched)."*

**Acceptance criteria in scope (Part VI §6.3 verbatim):**
- **AC-A5.a** (line 149): *"Partition schema + refresh job exist before any interactive feature builds against live data (design-gate discipline)."*
- **AC-A5.b** (line 151): *"Latency telemetry per interactive request from first internal use; budgets are DEFAULT class (p95 ≤ 1.5s first-ask; re-ask p95 ≤ 40% of first-ask) revised only by measured pilot data."*
- **AC-A5.c** (line 153): *"Version-skew cell proves a session cannot cite two partition versions in one output; ES-1 CI check green; load test at 10× expected concurrency passes budget before any external demonstration."*

**Explicitly out of scope (fences from EAB v1.1 §1.2 + §IX D7 + Owner ruling composition ε + α + γ):**
- Critic-pass phase (Tier-2 harness · CR-7 · CIF manifest fields · archive ledger) — separate phase (§IX).
- G-13 · Registry Doctrine §8.1 additive-surface completion (remaining 5 of 8) — separate phase (Commercial Thesis Owner-side).
- UI-1 / UI-2 — Extraction Console (UI-1) · Integration Console + S1 memory plane (UI-2) — separate phases.
- Any refusal-envelope contact (EAB-2 sealed the family · v0/v1 held byte-identical from EAB-2 close).
- Any Targeta cap-seat contact (§IX pre-named surface · expect none).
- **DB-1 + DB-2** (from Owner ruling `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` §4) — Prove-module-phase items · early landing at EAB-3 = D-5 cross-phase leakage defect. Explicitly OUT.
- Any Lane 2b module scope (Connect · Registry · Extract · Govern · Prove · Team · Shared).
- Any Lane 1 GPU scope · model acquisition (§IX D7 fence · zero curl/download this atomic).
- Calibration machinery beyond F3 (measurement-era per ES-4).
- Scheduler beside Targeta (§1.2). R-A5.3 partition-refresh cold-path batch job is a compute pipeline, NOT a request-time scheduler primitive — orthogonal to OD-10 scheduler-primitive scope (Registry census auto-trigger · Connect post-signoff first-census kickoff). Explicit disclosure at §7 fence.
- Double-buffering / quantization execution (§1.2 · measurement-era).

**Parity fence:** the Parity 32→33 seal via new `PartitionSchema@v0` contract is a **sanctioned seal event** pre-named at Tier-1 relay §5.1 below. It **executes at the EAB-3 EXECUTION atomic**, NOT at this Stage A. Parity 32 held byte-identical through Stage A landing (32 contracts + 32 snapshots · v0 + v1 refusal envelope byte-identity guarded per Standing Rule v3 from EAB-2 close).

---

## §2 · Band (Governance §9 · raw LoC verdict-unit · §4.2 split threshold citation)

Per `docs/governance/tiered_ruling_model.md` §9 (raw LoC verdict-unit ruling · 2026-07-10 Owner-verbatim) and §2.1 / §4.2 (pre-authorized split threshold: 1,500 LoC / 60 cells · Tier 2 · disclosure-not-blocking). Rate ledger applied per §6.1–§6.11.

**Every figure below carries the Owner-mandated verbatim tag** (per Owner Configuration Dispatch §4.STEP-5 + Owner HAZARD-STOP ruling §5.5): **"Provisional planning anchor — not a commitment. Relative weight only."**

**Estimated LoC breakdown (Tier-2 · disclosure-not-blocking · provisional planning anchor — not a commitment. Relative weight only.):**

| Component | LoC low | LoC high | Rate ledger row |
|---|---:|---:|---|
| R-A5.1 · new `PartitionSchema@v0` frozen contract (Parity 32→33 · version-record shape: `partition_id` · `schema_version` · `key_dimensions: List[str]` · `receipt_set_ref: str` · `promoted_at: str` · `superseded_at: Optional[str]` · `partition_shape_kind: Literal["columnar_memmap"]` · `size_bytes: int` · per-instance scoping via `instance_id`) | 90 | 150 | §6.6 · frozen Pydantic contract class 60 LoC/class + doctrinal notes overhead |
| R-A5.1 · contract snapshot `partition_schema_v0.contract_snapshot.json` (new invariant JSON) | 40 | 80 | §6.7 · frozen contract snapshot ~155 LoC/snapshot fractional |
| R-A5.1 · partition storage adapter (columnar · memory-mappable · read-side `open_partition(version_id)` + `read_key(version_id, key_tuple)` · reads inherit session's validated purpose) | 100 | 160 | §6.3 · backend service module 100 LoC/module |
| R-A5.2 · ES-1 CI import/route check (AST negative-scan: no estate-query client reachable from any interactive-surface code path · walk `backend/routers/**` and `backend/services/**` reachability graph against grandfathered dispatchV2 whitelist per Owner ruling `es1_scope_2026-07-14.md` L10) | 60 | 100 | §6.10 · AST/reflection gate class ~40 LoC/cell × 2 cells (walker + whitelist) |
| R-A5.3 · partition refresh discipline · cold-path batch job runner + atomic-promotion writer + ledger row emission (`PROM-S3-append-only-ledger` · `PROM-S3-mechanical-audit-of-promotion` extended from container-promotion precedent to partition-promotion) | 100 | 150 | §6.3 · backend service module 100 LoC/module |
| R-A5.4 · session working set service (`session_id`-scoped · bounded time-scoped · cache stores `{partition_version_ref, derived_arithmetic}` · never re-materialized raw · promotion-invalidates-dependents · cache-reads-inherit-purpose) | 100 | 160 | §6.3 · backend service module 100 LoC/module |
| R-A5.5 · lineage recorder (`partition_version.receipt_set: List[receipt_ref]` binding · answer citation includes partition_version_id · walkable chain: number → partition → receipts → operations · zero additional retrieval at request time) | 60 | 100 | §6.3 partial · piggybacks R-A5.1 contract fields |
| Latency telemetry per interactive request (AC-A5.b · p95 ≤ 1.5s first-ask · re-ask p95 ≤ 40% of first-ask · DEFAULT class per Op. Values discipline) | 40 | 80 | §6.11 · async httpx auth-overhead cell class ~25 LoC/cell (adapts to latency-instrumentation cell class) |
| Pytest cells (design-gate AC-A5.a + version-skew AC-A5.c + ES-1-CI-check-green AC-A5.c + latency-budget AC-A5.b + load-test-10x-concurrency AC-A5.c + purpose-validation-inheritance R-A5.4 + partition-promotion-atomic R-A5.3 + lineage-walkable-chain R-A5.5 + previous-version-serves-until-atomic-promotion R-A5.3 + cache-partition-version-binding-invalidation R-A5.4 + Parity 33 attest + additive-versioning attest v0-refusal-envelope-and-v1-refusal-envelope byte-identity guard) | 130 | 190 | §6.1 · 12 LoC/cell · 12 cells (mixed §6.1 amortised + §6.10 AST-scan) |
| §6.9 verbatim-carrier overhead (R-A5.1..R-A5.5 invariant text carried in contract module + service modules per AF-E4 α precedent + EAB-2 v1 contract precedent) | 50 | 90 | §6.9 · verbatim-carrier overhead ~100-150 LoC/carrier partial |
| §6.10 AST/reflection gate class (Parity 33 attest cell + AST negative-scan on estate-query-client-reachable-from-interactive-surface + AST positive on `session_id` binding in working-set service) | 60 | 100 | §6.10 · AST/reflection gate ~40 LoC/cell × 2-3 cells |
| Contract touch (Parity 32→33 · SEALED at EXECUTION atomic · NOT this Stage A) | 0 | 0 | **Parity 32 held byte-identical this Stage A; +1 (`PartitionSchema@v0`) at execution** |

**Total band estimate: raw LoC `[low=830, high=1360]`.**

**Cell count estimate: `[low=14, high=17]`** (12 pytest cells + 2-3 AST/reflection cells + optional load-test cell).

**Provisional planning anchor — not a commitment. Relative weight only.**

**§2.1/§4.2 split-threshold disclosure:** governance threshold is **1,500 LoC / 60 cells** (`docs/governance/tiered_ruling_model.md` §2.1 · verbatim: *"Split thresholds: §4.2 pre-authorized split (currently 1,500 LoC / 60 cells)."*). If total execution LoC exceeds 1,500 raw LoC OR total cell count exceeds 60 cells at execution time, the seam splits as **commit A = R-A5.1 + R-A5.2 + R-A5.5** (partition-schema contract + ES-1 CI check + lineage · Parity 32→33 seal event lands in this commit · load-bearing sanctioned event) and **commit B = R-A5.3 + R-A5.4** (refresh discipline + session-working-set · operational machinery against sealed contract). NO Owner ruling required unless threshold hits at execution time (§4.2 · disclosure-not-blocking · Tier 2). Rationale for split boundary: commit A seals Parity 33 and lands the contract; commit B lands the operational machinery (refresh runner + session-working-set) against that sealed schema. Both commits carry Parity attest independently (Parity 32→33 in commit A · Parity 33 held in commit B). **Provisional planning anchor — not a commitment. Relative weight only.**

---

## §3 · Registry v1 citations (D-11 canon-before-attest · v1.md is active source)

Every fold cites `docs/registry/function_promise_registry_v1.md` (SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a`) as active source. Zero citations to v0 lineage as active source (v0.md + v0.1..v0.5 supplements are historical byte-carried body inside v1.md per G-2 Registry Maintenance close).

**Aggregate citation count in this Stage A body: 11 distinct v1.md rows** cited across §4 folds + §5 escalations + §6 sidecar enumeration:

1. `PROM-S1-frozen-wire-contract` (v1 §2 · L58) — R-A5.1 partition-schema contract byte-identity + additive-versioning root
2. `PROM-S1-additive-versioning` (v1 §2 · L59) — R-A5.1 Parity 32→33 additive seal · V1-G7 assertion set bumps with the new snapshot
3. `PROM-S1-honesty-grammar-source-labels` (v1 §2 · L60) — R-A5.4 cache stores partition references + derived arithmetic ONLY · never re-materialized raw · no fabricated values
4. `PROM-S2-slice-freeze-at-commission` (v1 §2 · L69) — R-A5.4 session-working-set binds to partition-version at session-open (analogous to slice-freeze-at-commission discipline · no silent version-drift)
5. `PROM-S3-append-only-ledger` (v1 §2 · L73) — R-A5.3 partition-promotion ledgered · superseded partition versions preserved byte-identical (immutability doctrine extended to partition-version records)
6. `PROM-S3-audit-trail-immutable` (v1 §2 · L75) — R-A5.5 lineage · walkable chain preserves audit trail immutability at partition-version → receipt-set boundary
7. `PROM-S3-mechanical-audit-of-promotion` (v1 §2 · L78) — R-A5.3 partition-promotion mechanically-audit precedent extended from container-promotion (PH-R1) to partition-promotion
8. `PROM-S3-frozen-contract-parity-attest` (v1 §2 · L79) — Parity 33 attest reads from ONE authoritative counter at `services/health/parity_counter.py::EXPECTED_PARITY` (already bumped 31→32 at EAB-2 close · bumps 32→33 at EAB-3 execution atomic)
9. `PROM-S3-retention-held-class-no-delete` (v1 §2 · L74) — R-A5.5 partition-version's receipt-set integrity: no DELETE handler over held-class receipt rows enters the partition-refresh path (retention discipline preserved through R-A5.3 cold-path batch job)
10. `akki.instance.seams_scoped_by_instance_id` (v1 §S1 · MC-E2 α reflexive · G-3 sixth-seam-value landing precedent) — R-A5.1 partition-schema per-instance scoping (multi-instance discipline · partitions do not cross instance boundary)
11. §14 sidecar pattern (v1 §M · G-2 R4 reflexive rows precedent + EAB-1 sidecar precedent SHA `8437894f7c72143bd3d1256fd78225d75ad0b100c5eeb96d3f00f39491ce61cb` + EAB-2 sidecar precedent SHA `ddf89929ee072f7c06436c34de5c9c34d8a274c9715f98f96492ef2c7fb067c9`) — EAB-3 sidecar filing pattern

---

## §4 · Fold enumeration · row-by-row

Each fold is FACT / NORM / DEFAULT class per Op. Values §7 discipline, with Registry v1 row citation.

### §4.A · R-A5.1 folds (partition schema · Part VI §6.2 L137)

- **A5.1.1 · Partition-schema frozen contract (`PartitionSchema@v0`)** — **FACT-class** (versioned columnar memory-mappable partition definition with pre-declared field-set · additive versioning · Parity 32→33 seal). Registry anchor: `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning`. New sidecar row.

- **A5.1.2 · Per-surface key-dimension configuration** — **FACT-class** (keys are per-surface configuration · extension only via schema versioning per R-A5.1 verbatim). Registry anchor: `PROM-S1-frozen-wire-contract`. New sidecar row.

- **A5.1.3 · Per-instance partition scoping** — **FACT-class** (partitions do not cross instance boundary · MC-E2 α reflexive discipline extended from seam-values to partitions). Registry anchor: `akki.instance.seams_scoped_by_instance_id` (v1 §S1). New sidecar row.

### §4.B · R-A5.2 folds (estate-query prohibition ES-1 · Part VI §6.2 L139)

- **A5.2.1 · ES-1 CI import/route check (AST negative-scan)** — **FACT-class** (no estate-query client reachable from interactive-surface code path · rung-1 enforced per R-A5.2 verbatim; grandfathered exception: dispatchV2 per Owner ruling `es1_scope_2026-07-14.md` Finding 1). Registry anchor: `PROM-S1-frozen-wire-contract` (structural invariance). New sidecar row.

- **A5.2.2 · ES-1 scope-boundary respect (Owner-ruled operational-record exemption)** — **FACT-class** (operational-record reads outside ES-1 per `es1_scope_2026-07-14.md` L10; A5.2.1 scan whitelist must include TraceReceipt / Compliance / AuditTrail / CommitReview / OpportunityBriefs surfaces per rulings L15-19). Registry anchor: `PROM-S3-audit-trail-immutable` (operational-record read boundary preserved). New sidecar row.

### §4.C · R-A5.3 folds (refresh discipline · Part VI §6.2 L141)

- **A5.3.1 · Cold-path batch job discipline** — **NORM-class** (partition refresh runs on a cold-path batch job schedule · NOT a request-time scheduler primitive · orthogonal to OD-10 census-scheduler scope · disclosed at §7 fence). Registry anchor: `PROM-S3-append-only-ledger`. New sidecar row.

- **A5.3.2 · Atomic-promotion + previous-version-serves-until-promotion** — **FACT-class** (previous partition version serves until the new version is atomically promoted per R-A5.3 verbatim · zero read-time interruption during refresh). Registry anchor: `PROM-S3-mechanical-audit-of-promotion` extended from container-promotion (PH-R1) to partition-promotion. New sidecar row.

- **A5.3.3 · Promotion ledgered** — **FACT-class** (every partition-promotion writes a Northena ledger row per R-A5.3 verbatim · immutable · walkable). Registry anchor: `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable`. New sidecar row.

### §4.D · R-A5.4 folds (session working set · Part VI §6.2 L143)

- **A5.4.1 · Session-scoped cache with partition-version binding** — **FACT-class** (cache entries bind to partition version per R-A5.4 verbatim · promotion invalidates dependents · one cited result NEVER mixes evidence versions · AC-A5.c version-skew wire attest). Registry anchor: `PROM-S2-slice-freeze-at-commission` (slice-freeze-at-commission discipline extended to session-freeze-at-open · no silent version-drift). New sidecar row.

- **A5.4.2 · Cache stores partition references + arithmetic ONLY (never re-materialized raw)** — **FACT-class** (no ungoverned data path per R-A5.4 verbatim · honesty-grammar preserved · derived arithmetic is Registry-native aggregate posture extended from OB-E3 α). Registry anchor: `PROM-S1-honesty-grammar-source-labels`. New sidecar row.

- **A5.4.3 · Cache reads inherit session's validated purpose** — **FACT-class** (per R-A5.4 verbatim · purpose validation is not bypassable through the working-set path · Shield-single-source discipline preserved). Registry anchor: `PROM-S3-audit-trail-immutable` (purpose-validated cache reads carry the session's ledger-provenance). New sidecar row.

### §4.E · R-A5.5 folds (lineage · Part VI §6.2 L145)

- **A5.5.1 · Partition-version records receipt set** — **FACT-class** (every partition version records the receipt set it was built from per R-A5.5 verbatim · walkable chain per number→partition→receipts→operations). Registry anchor: `PROM-S3-audit-trail-immutable` + `PROM-S3-append-only-ledger`. New sidecar row.

- **A5.5.2 · Answer citations include partition version identifier** — **FACT-class** (the citation IS the identifier the request touched per R-A5.5 verbatim · zero additional retrieval at request time). Registry anchor: `PROM-S3-audit-trail-immutable`. New sidecar row.

- **A5.5.3 · Held-class receipt integrity preserved through refresh** — **FACT-class** (no DELETE handler over held-class receipt rows enters the partition-refresh path · retention discipline preserved through R-A5.3 cold-path batch job). Registry anchor: `PROM-S3-retention-held-class-no-delete`. New sidecar row.

### §4.F · Acceptance-criteria (AC) folds (Part VI §6.3)

- **AC-A5.a** — **FACT-class** — Partition schema + refresh job exist before any interactive feature builds against live data (design-gate discipline · pytest cell asserts on-disk existence of contract + snapshot + refresh runner at EAB-3 close · no interactive feature can commence Lane 2b before EAB-3 close). Registry anchor: `PROM-S1-frozen-wire-contract`. New sidecar row.
- **AC-A5.b** — **DEFAULT-class** — Latency telemetry per interactive request from first internal use · budgets are DEFAULT class per Op. Values discipline (p95 ≤ 1.5s first-ask · re-ask p95 ≤ 40% of first-ask · revised only by measured pilot data per R-A5.4). Registry anchor: `PROM-S3-frozen-contract-parity-attest` extended to latency-telemetry attest via `services/health/**` seam.
- **AC-A5.c** — **FACT-class** — Version-skew cell proves a session cannot cite two partition versions in one output · ES-1 CI check green · load test at 10× expected concurrency passes budget before any external demonstration (three-part acceptance cell · all three wire-attested at EAB-3 close). Registry anchor: `PROM-S1-frozen-wire-contract` + `PROM-S3-audit-trail-immutable`.

---

## §5 · Tier-1 escalation surfaces (pre-named)

Per EAB v1.1 §IX pre-naming (line 179 verbatim): *"partition-schema contract class (A5; new artifact class → registered, additive)"* is the sole Tier-1 surface named for EAB-3.

Zero other pre-named Tier-1 surfaces from §IX apply to EAB-3:
- Refusal-envelope contract contact (A3) — **SEALED at EAB-2 close 2026-07-24** (composition ε + α + γ · v0 + v1 byte-identity preserved · no re-surfacing).
- Occurrence-unit locator vocabulary (A2) — landed under EAB-1 A2 with MC-E1 α zero-mutation attest · no contact this atomic.
- F2 seam-value admission — landed via G-3 · no re-landing this atomic.
- Any Targeta-input contact beyond the named cap seat — no contact this atomic (see §5.4 downgrade).

### §5.1 · E1 · Partition-schema contract class contact · **Tier-1** — Parity 32→33 seal via `PartitionSchema@v0` (pre-named · sanctioned)

**Surface:** A5 requires a **new artifact class** (per §IX pre-naming) at Parity 32→33 seal. Zero existing frozen contract carries partition-version semantics; the closest analogs are `NorthenaLedgerRow` (append-only receipt/ledger row · not partition-schema) and `KnowledgeArtifact_v0` (build artifact reference · not partition schema). A new frozen contract at `backend/contracts/partition_schema.py` is the load-bearing landing.

**Builder analysis (does NOT resolve):** three structurally distinct posture options exist and the Owner rules the posture. This is the second parity change since 2026-07-04 (first was EAB-2 A3 Parity 31→32 · this is A5 Parity 32→33).

**Owner ruling surface:**

- **(a1) One-contract landing · `PartitionSchema@v0` carries the full version-record shape** (schema definition + version-instance record fields co-located):
  - Byte-level: single frozen contract at `backend/contracts/partition_schema.py` with fields `partition_id: str · schema_version: str · key_dimensions: List[str] · receipt_set_ref: str · promoted_at: str (ISO-8601) · superseded_at: Optional[str] · partition_shape_kind: Literal["columnar_memmap"] · size_bytes: int · instance_id: str`. Snapshot at `backend/tests/invariants/partition_schema_v0.contract_snapshot.json`. Parity 32 → 33. V1-G7 assertion set bumps from 32 to 33.
  - Standing Rule v3 impact: PRESERVED (additive · no byte-contact with prior 32 contracts).
  - Trade-off: single-contract simplicity; schema-definition and version-instance-record co-located may couple future schema-versioning extensions to version-record migrations.
  - Precedent alignment: matches EAB-2 A3 posture (Owner-ruled `Service1Refusal_v1` as one contract at composition ε + α + γ · single-writer end-state).

- **(a2) Two-contract landing · `PartitionSchema@v0` (schema definition) + `PartitionVersion@v0` (version-instance record with receipt-set binding)** — Parity 32→33→34 as two seal events in one atomic:
  - Byte-level: two frozen contracts. `PartitionSchema@v0` carries `partition_id · schema_version · key_dimensions · partition_shape_kind · instance_id` (schema definition). `PartitionVersion@v0` carries `partition_id · schema_version · version_id · receipt_set_ref · promoted_at · superseded_at · size_bytes` (version-instance record). Two snapshots. Parity 32 → 33 → 34 as two additive seal events in one atomic commit.
  - Standing Rule v3 impact: PRESERVED (both additive).
  - Trade-off: cleaner schema-vs-instance separation; enables schema evolution without version-record migration; but double-seal is heavier ceremony and adds Parity budget.
  - Precedent alignment: matches the outer_gate_receipt v0 + v1 two-contract precedent (`backend/contracts/outer_gate_receipt.py` + `backend/contracts/outer_gate_receipt_v1.py`).

- **(b) Extend an existing frozen envelope in place (e.g., add partition fields to `KnowledgeArtifact_v0`)** — **REJECTED at pre-name by Standing Rule v3** · `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` require additive versioning, not in-place mutation of a frozen envelope. Option (b) is disclosed to complete the enumeration but is not a live posture · it violates a load-bearing invariant.

- **(c) Sidecar telemetry only (no frozen contract; partition-version records live in a JSON sidecar or unfrozen dict)** — **REJECTED at pre-name by R-A5.1 verbatim requirement** ("*keys are per-surface configuration; extension only via schema versioning*"). Schema versioning requires a frozen contract; sidecar telemetry cannot carry Parity-attested schema-versioning discipline. Named here to complete the enumeration.

**Builder Tier-3 recommendation: (a1)** — one-contract landing. Rationale:
1. Simpler operational surface; a partition record in the wild has ONE shape at ONE version.
2. Precedent alignment with EAB-2 A3 (Owner ruled a single-writer end-state · superset envelope · not a split-envelope posture). A5's partition-version is analogously well-modeled as a single-envelope superset.
3. Parity budget conservation: one seal event this atomic (32→33) vs (a2)'s two seals (32→33→34). Given EAB-1 (Parity 31 baseline) → EAB-2 (32) → EAB-3 (33) is a clean linear-additive progression, holding one-seal-per-phase is D-6-cleanest.
4. Schema-versioning extension per R-A5.1 (*"extension only via schema versioning"*) remains available in (a1): future field additions land as `PartitionSchema_v1` (like `Service1Refusal_v1` did for A3) · zero mutation of `PartitionSchema_v0`.

**Fence carried into this Stage A:** the seal is **pre-named**, not executed. Zero contract file created this Stage A · zero snapshot file created · Parity 32 held byte-identical at close of this Stage A landing.

### §5.2 · E2 · Targeta gap-candidate filing surface contact (§IX pre-named "any Targeta-input contact beyond the named cap seat" · expect none · downgrade to no-live-ruling-surface · disclosed)

**Surface:** §IX pre-names "any Targeta-input contact beyond the named cap seat" as Tier-1 material. A5 partition-schema + session-working-set is a serving-side / interactive-surface discipline; no Targeta-input surface contact is proposed. The gap-candidate filer landed at EAB-2 (composition α · Locus 2 · `backend/services/targeta/gap_candidate_filer.py`) is the demand-signal-side record, orthogonal to A5's serving-side partition surface.

**Builder analysis (resolves at Tier-3 authority):** A5 session-working-set service reads from Northena ledger + `PartitionSchema@v0`-defined partitions; it does NOT write to Targeta's cap-seat / eligibility-computing side. AST/reflection cell (§6 sidecar row #12 below) grepping for any import path from A5 session-working-set service into `backend/services/targeta/gate.py` or `backend/services/targeta/yield_layer.py` (Targeta eligibility modules) enforces at CI.

**Downgrade rationale (D-11 read):** EAB v1.1 §1.2 rules the eligibility-wall discipline explicitly; §IX pre-names expect none. A5 is orthogonal to Targeta cap-seat. Disclosed as pre-named per §IX; downgraded on evidence (spec discipline is explicit; expected-none contact is not a live escalation).

### §5.3 · E3 · Refusal-envelope contract contact (SEALED at EAB-2 · downgrade to no-live-ruling-surface · disclosed)

**Surface:** EAB-2 sealed `Service1Refusal@v1` (Parity 31→32) under Owner ruling composition ε + α + γ (2026-07-24). v0 byte-identity preserved.

**Downgrade rationale:** EAB-3 A5 has no refusal-envelope contact. AC-A5.a-c are wire-attested against partition-schema and refresh discipline, not against refusal grammar. `PROM-S1-refusal-taxonomy-closed` is not touched.

Disclosed as previously pre-named per §IX (A3 refusal-envelope surface); downgraded on evidence (A5 is orthogonal to refusal-family).

### §5.4 · E4 · F2 seam-value admission (already landed via G-3 · downgrade to no-live-ruling-surface · disclosed)

**Surface:** F2 sixth seam value `quarantine_systemic_halt_threshold` landed via G-3. EAB-3 does not touch seam-values.

**Downgrade rationale (D-11 read):** A5 partition-schema is orthogonal to `SeamValues` seam-value family. No re-landing; no admission surface. Disclosed as pre-named per §IX; downgraded on evidence.

### §5.5 · Tier-3 remainder (builder Tier-3 judgment · disclosed at close)

- **Partition-shape-kind enumeration** (e.g., `Literal["columnar_memmap"]` vs future `Literal["columnar_memmap", "row_hash_index", "reference_tree"]`) — DEFAULT class · set at execution time; extension via schema versioning per R-A5.1 verbatim ("*extension only via schema versioning*"). Initial landing is single-value `Literal["columnar_memmap"]`; future variants are `PartitionSchema_v1`.
- **Partition-refresh cadence** (event-driven-vs-cron; how often the cold-path batch job runs) — DEFAULT class; **NOT** OD-10 scheduler-primitive (which covers Registry census auto-trigger + Connect post-signoff kickoff · different scope). Partition-refresh runs on operator-invoked or first-material-arrival triggers; disclosed at close.
- **Session working-set eviction discipline** (LRU vs TTL vs promotion-invalidation only) — DEFAULT class; promotion-invalidation-only is the R-A5.4-canonical primary discipline (per verbatim "*promotion invalidates dependents*"); additional LRU/TTL is builder Tier-3 at execution time.
- **Latency-telemetry storage** (sidecar telemetry per PROM-S1-runtime-transient-never-refusal precedent vs first-class Northena ledger row) — DEFAULT class; sidecar telemetry per AF-E3 α + AF-E4 α precedent is the pre-authorized default (no new frozen contract for latency-telemetry beyond the AC-A5.b measurement discipline).
- **AC-A5.b latency budget revision discipline** — DEFAULT class per Op. Values discipline (verbatim from R-A5.4: "*budgets are DEFAULT class (p95 ≤ 1.5s first-ask; re-ask p95 ≤ 40% of first-ask) revised only by measured pilot data.*"); revision ceremony rides F2-precedent dual-control-on-change discipline.

---

## §6 · R4 sidecar (enumerated only · NOT created this Stage A)

Per Tiered-Ruling `docs/governance/tiered_ruling_model.md` §14 sidecar pattern (v1-era sidecar precedent · ratified 2026-07-11) + Registry v1 §M G-2 R4 reflexive-rows precedent + EAB-1 sidecar precedent (`docs/registry/function_promise_registry_v1_eab1_sidecar.md` · 13 rows · zero new promises · SHA `8437894f7c72143bd3d1256fd78225d75ad0b100c5eeb96d3f00f39491ce61cb`) + EAB-2 sidecar precedent (`docs/registry/function_promise_registry_v1_eab2_sidecar.md` · 14 rows · zero new promises · SHA `ddf89929ee072f7c06436c34de5c9c34d8a274c9715f98f96492ef2c7fb067c9`).

**Proposed sidecar path:** `docs/registry/function_promise_registry_v1_eab3_sidecar.md`

**Row count proposed: 15 rows**, all attaching to existing v1.md §2 promises via foreign-key resolution (zero new promises minted — conservation-not-authorship posture per §M):

| # | Proposed sidecar row | Rung | Promise attachment |
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

**Reflexive-sidecar-row placeholder:** the sidecar file itself will land as a 16th reflexive row at execution atomic per EAB-1/EAB-2 sidecar precedent (`akki.registry.eab3_sidecar_reflexive_row` · attaches to Registry v1 §M sidecar-pattern authority).

**Zero new promises minted** (conservation-not-authorship posture per Registry v1 §M · EAB-1 + EAB-2 sidecar precedents). All 15 rows target existing v1.md §2 promises (`PROM-S1-frozen-wire-contract` ×6 · `PROM-S1-additive-versioning` ×2 · `PROM-S1-honesty-grammar-source-labels` ×1 · `PROM-S2-slice-freeze-at-commission` ×1 · `PROM-S3-append-only-ledger` ×3 · `PROM-S3-audit-trail-immutable` ×4 · `PROM-S3-mechanical-audit-of-promotion` ×1 · `akki.instance.seams_scoped_by_instance_id` ×1).

**Sidecar file NOT created this Stage A** (per Owner-verbatim REPLY FORMAT §6 · "enumerated only · NOT created"). Sidecar lands at execution atomic, byte-carried as a sibling file per Registry Doctrine §5 v1-era pattern and per EAB-1 + EAB-2 sidecar precedents.

---

## §7 · D-7 fence attestation

Verdicts uncurated per D-7 (Registry Doctrine Part IV D-7): *"engineer the inputs relentlessly; never touch the test."* Every acceptance criterion above is measured on real inputs against the pre-declared threshold; verdicts are drawn from measured composition, not curated. AC-A5.b latency budget (p95 ≤ 1.5s first-ask · re-ask p95 ≤ 40% of first-ask) and AC-A5.c load-test-at-10× are D-7 exemplars for this atomic: measurement is on real request pathways against pre-declared budgets.

**No Critic-pass content:** Tier-2 harness · CR-7 checklist amendment · CIF manifest schema fields · archive ledger — all Critic-pass phase scope, out of scope here.

**No G-13 content:** Registry Doctrine §8.1 additive-surface completion (remaining 5 of 8) — G-13 scope, out of scope here. Commercial Thesis (G-13 §8.1.5 sub-surface) is Owner-side per Lane 1 discipline · not builder-dispatched.

**No UI-1 content:** Extraction Console to Designer Brief depth — out of scope. A5 session-working-set service may **later** back the Extraction Console interactive surface at UI-1, but that binding is UI-1 scope; A5 lands the service, not the surface consumption.

**No UI-2 content:** Integration Console + S1 memory plane — out of scope. No frontend/src touch to `IntegrationConsole*` anticipated in EAB-3 execution.

**No refusal-envelope contact:** EAB-2 sealed Service1Refusal@v1 (composition ε + α + γ · 2026-07-24). v0 + v1 held byte-identical from EAB-2 close. A5 has zero refusal-envelope wire contact; AC gates measure partition-side and session-side wires only.

**No Targeta cap-seat contact:** §5.2 AST negative-scan attests no import path from A5 session-working-set service into Targeta eligibility modules (`services/targeta/gate.py` · `services/targeta/yield_layer.py`); eligibility wall stands per EAB v1.1 §1.2.

**No Lane 2b module scope:** Connect · Registry · Extract · Govern · Prove · Team · Shared Components module-phase execution is downstream of the ratified 7-phase sequence UI-1/UI-2 dispatches (per STEP 5 re-band `docs/handoff/step_5_reband_2026_07_24.md` SHA `f8bae9f03442bfe2f579b7150306805116ab56d5ddb91d2ad98046880fa3cdcb`). Zero module-phase content this atomic.

**No Lane 1 GPU / model acquisition:** zero curl of model weights, zero `pip install` of AI models, zero pyannote/NeMo/Silero fetch this atomic. A5 is serving-pattern (partition storage + session working-set); it does NOT touch perception model registry.

**No calibration machinery:** measurement telemetry (F3) lands as-declared in EAB v1.1 §Part VII F3 · already in force via G-3 close; latency telemetry cell for AC-A5.b rides F3 discipline; no calibration harness beyond the F3 rule.

**No DB-1 · No DB-2:** Owner ruling `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` §4 preserves DB-1 (evidence-can't-support wire-reason plain-language render at Answer Card honesty strip) and DB-2 (companion-channel failure never converts refusal to fault render) for **Prove module phase Lane 2b · NOT EAB-3 content**. Landing DB-1 / DB-2 in this Stage A = D-5 cross-phase leakage defect. Both explicitly OUT.

**No OD-8 / OD-9 / OD-10 contact:** OD-8 (mail-provider) · OD-9 (public-surface exposure) · OD-10 (scheduler primitive) remain OPEN · sequence-blocking on Lane 2b module dispatches, NOT blocking on EAB-3. A5 does not send mail; A5 does not expose a public surface; A5's cold-path batch job (R-A5.3) is a compute pipeline orthogonal to OD-10's request-time scheduler-primitive scope. D-11 verified this session: R-A5.1..R-A5.5 verbatim text carries no mail-provider / public-surface / scheduler-primitive content.

**No re-landing of prior Tier-1 surfaces:** F2 seam-value (landed G-3); Service1Refusal@v0 (landed A2); Service1Refusal@v1 (landed EAB-2). A5 consumes none.

**Parity fence:** the Parity 32→33 seal via `PartitionSchema@v0` is a **sanctioned seal event** at the EAB-3 EXECUTION atomic. Zero contract file created this Stage A. Zero snapshot file created this Stage A. `git diff --stat HEAD backend/contracts/` expected empty at close of this Stage A landing. `git diff --stat HEAD backend/tests/invariants/*.contract_snapshot.json` expected empty at close of this Stage A landing. **Parity 32 held byte-identical this Stage A.**

**Governance-stack byte-identity:** §§1..23 sanctioned amendment blocks unchanged in this Stage A landing (`docs/governance/tiered_ruling_model.md` SHA `9b3c56c14a1159af35c382e1a68368fcf673a381f77cd4734e51a85cd57e51c4` unchanged this atomic).

**Standing Rule v3:** all protected artifacts remain byte-identical — v0 lineage · v1.md · Op. Values v1.0/v1.1 · EAB v1.1 · Critic Seam v1.0/v1.1 · TQ v1.0 · CIF v1.0 · TT v1.0 · Extraction De-risking v1.0 · S1 Memory v1.0 · SJM v1.0 · SyniSense mandate · registry doctrine v1.0 · MANIFEST · registers · all prior rulings · Owner ruling `eab_2_hazard_stop_a_ruling_2026_07_24.md` · Prove Step 4 amendment · `backend/contracts/**` (32 contracts byte-identical) · snapshots (32 snapshots byte-identical).

---

## §8 · D-10 self-audit table (D-1..D-12 · STANDING PRACTICE per QA-2)

| # | Defect | Verdict (this Stage A) | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Every fold in §4 traces to an EAB v1.1 Part VI §6.2 mandate line (R-A5.1 L137 · R-A5.2 L139 · R-A5.3 L141 · R-A5.4 L143 · R-A5.5 L145) + a Registry v1 row citation in §3. Every AC row (§4.F) traces to Part VI §6.3 verbatim (AC-A5.a L149 · AC-A5.b L151 · AC-A5.c L153). |
| D-2 | NL-only claim | PASS | Every claim is disk-verifiable (EAB v1.1 SHA `312427c672e9db8a` at line ranges cited · Registry v1 SHA `d6ad136f65426c0f` at row/section cited · governance §2.1/§9/§14 at line ranges cited · Op. Values v1.1 SHA `3a3cff3be0cb59d2` at §6.6 cited · ES-1 ruling SHA `a4675cd83c4e500a` at L9 verbatim · EAB-2 close SHA `0de07b1727c7b5a8` cited · Owner HAZARD-STOP ruling SHA `8b074dc152b41ed3` cited). |
| D-3 | Curated verdict | PASS | 15 R4 rows enumerated · 3 AC criteria enumerated (AC-A5.a-c) · 1 Tier-1 surface named (E1 partition-schema contract class) with builder analysis and three sub-options (a1/a2/b-rejected/c-rejected) · 3 pre-named surfaces downgraded on evidence with rationale (§5.2 Targeta-no-contact · §5.3 refusal-envelope-sealed-at-EAB-2 · §5.4 F2-landed-at-G-3) · Tier-3 remainder disclosed (§5.5 5 items). |
| D-4 | Rung inflation | PASS | All 15 sidecar rows at Rung-1 Deterministic (§6.11 shared-helper class or §6.10 AST/reflection class). No fold proposed at rung above what MC-E1 α · EAB-1 A1-A2 sidecar precedent · EAB-2 A3-A4 sidecar precedent bound. |
| D-5 | Cross-phase content leakage | PASS | Zero DB-1 / DB-2 content (Prove module phase Lane 2b · §7 explicit fence) · zero Critic-pass / G-13 / UI-1 / UI-2 content · zero refusal-envelope contact (EAB-2 sealed) · zero Targeta cap-seat contact (§5.2 downgrade + §6 sidecar row 12 AST-attested). §7 fence attest lists each explicit exclusion. |
| D-6 | Silent scope drift | PASS | Split/merge decision at §1 disclosed builder Tier-3 with rationale (D-12-aligned: single-seam execution deploys in force; Parity 32→33 seal is a single sanctioned event that cannot double-seal). §2.1/§4.2 split-threshold at 1,500 LoC / 60 cells (governance canon) pre-authorized-disclosed. |
| D-7 | Invented scope | PASS | Every acceptance criterion is EAB v1.1 Part VI §6.3 verbatim (AC-A5.a L149 · AC-A5.b L151 · AC-A5.c L153); zero fabricated criteria. Tier-1 escalation pre-named per §IX (partition-schema contract class); zero fabricated escalation. §7 explicit D-7 attest carried. AC-A5.b latency budget and AC-A5.c load-test-10x are D-7 exemplars (measurement on real request pathways · fixed verdict pathway). |
| D-8 | Silent drift | PASS | Parity 32 attest carried in §2 band table (contract touch = 0/0 this Stage A) and in §7 fence attest; §14 sidecar pattern cited for R4 rows; all Standing Rule v3 artifacts named for byte-identity guard at close. All 32 prior contracts + 32 prior snapshots + Owner ruling + Prove amendment byte-identical guard. |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked at Stage A landing. Native pytest cell suite proposed for execution atomic per §2 band table (12 pytest + 2-3 AST cells + optional load-test cell = 14-17 cells). |
| D-10 | Menu emission | PASS | Zero permission-menu emitted this Stage A. Tier-1 surface §5.1 states four ruling options (a1/a2/b-rejected/c-rejected) as *Owner ruling surface enumeration*, not builder menu — pre-named per §IX and structured per EAB-1 Stage A §5.1 + EAB-2 Stage A §5.1 precedents (three-live-options + rejections enumeration pattern). |
| D-11 | Canon-before-ruling / LLM-memory recall | PASS | Full canon read log at §9 below with SHAs + line ranges. Every EAB v1.1 mandate citation traces to a live-command-verified line range this session; every Registry v1 citation traces to a live grep this session; every governance §-anchor traces to a live grep this session; every prior-phase-artifact SHA traces to a live `sha256sum` this session. No memory recall presented as fact. |
| **D-12** | **Experimentation at system level only** | PASS | Every fold in §4 deploys in force with known parameters: A5.1.1 partition-schema contract has pre-declared field-set (`partition_id · schema_version · key_dimensions · receipt_set_ref · promoted_at · superseded_at · partition_shape_kind · size_bytes · instance_id`) · A5.1.2 per-surface key-dimension configuration is a schema-versioning discipline (not a trial-mode config) · A5.1.3 per-instance scoping is MC-E2 α reflexive discipline (settled) · A5.2.1 ES-1 CI check is an AST negative-scan gate that fails the build on violation (not warns) · A5.2.2 ES-1 scope-boundary is Owner-ruled (`es1_scope_2026-07-14.md`) settled · A5.3.1-3 refresh discipline is atomic-promotion + append-only ledger (pre-declared) · A5.4.1-3 session working-set is partition-version-binding + purpose-inheritance + reference-and-arithmetic-only (pre-declared) · A5.5.1-3 lineage is walkable-chain + citation-is-identifier + retention-preserved (pre-declared). AC cells are D-7 measurement (verdict on parameters via real request pathways), NOT staged proving. **Zero observe-first · zero shadow phase · zero trial modes · zero staged proving.** The Parity 32→33 seal event lands at execution atomic **in force** — the new `PartitionSchema@v0` contract carries the sealed schema; not a staged additive with revisit windows. |

---

## §9 · D-11 canon-before-ruling read log

Files read during Stage A authoring (this session):

| File | SHA-256 | Line range read | Purpose |
|---|---|---|---|
| `docs/requirements/eab_tier1_adoption_spec_v1.1.md` | `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9` | §Part VI L129-153 (A5 mandate + R-A5.1..5 + AC-A5.a-c) + §Part VIII L165-173 (ES-1 + ES-2 + ES-5) + §IX L177-181 (execution model + pre-named Tier-1 surfaces + D7 fences) + §1.2 (fences · eligibility-wall discipline · no scheduler beside Targeta · shard rejection) | Scope source of truth · A5 in full scope · pre-named Tier-1 surface (partition-schema contract class) · fences |
| `docs/registry/function_promise_registry_v1.md` | `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a` | Grepped for `PROM-S1-frozen-wire-contract` L58 · `PROM-S1-additive-versioning` L59 · `PROM-S1-honesty-grammar-source-labels` L60 · `PROM-S2-slice-freeze-at-commission` L69 · `PROM-S3-append-only-ledger` L73 · `PROM-S3-audit-trail-immutable` L75 · `PROM-S3-mechanical-audit-of-promotion` L78 · `PROM-S3-frozen-contract-parity-attest` L79 · `PROM-S3-retention-held-class-no-delete` L74 · §S1 `akki.instance.seams_scoped_by_instance_id` · §M sidecar-pattern authority | Row citations for §3 aggregate (11 rows) + §4 folds + §5 escalations + §6 sidecar (15 rows) |
| `docs/rulings/es1_scope_2026-07-14.md` | `a4675cd83c4e500a2a36652fc8205e87e9dc1584228f508279b5736d595ac3a3` | L9-19 verbatim (ES-1 scope definition + Finding-1 grandfathering + F2-F6 operational-record exemptions) | R-A5.2 ES-1 scope-boundary source of truth · §4.B A5.2.2 whitelist rationale |
| `docs/requirements/operating_values_v1_1.md` | `3a3cff3be0cb59d28cd06a7e25123155d6984323f78e386687ee05c20f2d9c5b` | §6 amendment L17 (sixth seam value F2 · governance seam-value family reference) + §6.6 L43 (dual-control-on-change · MC-E3 α initial-set/ledger semantics · pattern for AC-A5.b DEFAULT-class revision discipline) | AC-A5.b DEFAULT-class revision-ceremony pattern · F2-landed downgrade rationale |
| `docs/close_reports/eab_2.md` | `0de07b1727c7b5a8f333e3b6b4c79b1cea94efebfd9ed00e5e9f715c08c1578e` | §1 (composition ε + α + γ) + §2.2 (Parity 31→32 contract SHA `3d5d9845e03d8419` + snapshot SHA `b0695338edb633ee`) + §4 (Standing Rule v3 attest · v0 byte-identity preserved) + §9 (Phase Ledger L-4 row · 39/46 = 84.8%) | EAB-2 close preconditions verified · Parity 32 baseline SHAs · Standing Rule v3 continuity · D-9 auto-proceed authorization from EAB-2 close |
| `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` | `8b074dc152b41ed300d5a7626a2a1bd5aa1213371f6eeeac0a096e12f2d6d4a5` | Full body · §4 DB-1 + DB-2 deferred-bindings note (execute at Prove module phase Lane 2b · NOT EAB-3 content) | §7 fence attest source · D-5 cross-phase leakage guard on DB-1 + DB-2 |
| `docs/stage_a_proposals/eab_2_stage_a.md` | `60a49c47e95cf6d7eddc6631f17ba2533b06364c2615d7785958dc69a8d7d805` | §1-§11 structural template + §5.1 three-option enumeration pattern + §2 band table structure + §6 sidecar structure + §8 D-10 12-row table + §11 Phase Ledger discipline | Stage A precedent structure (this Stage A mirrors EAB-2 Stage A pattern exactly) |
| `docs/stage_a_proposals/eab_1_stage_a.md` | `d5231d93c303ce2b163e2115cae3d507688693e4e58a122202ae825a4b4118dc` | §5.1 three-option enumeration pattern + §2 band table + §6 sidecar 13-row structure | Precedent pattern reference (do NOT copy content; structure only) |
| `docs/stage_a_proposals/eab_2_stage_a_refresh_2026_07_24.md` | `5dfea8e08f295e2a5ecf4f447063ba86c13ba199691789b29acad6594d1abf3f` | §5.1 sub-option (α) Targeta-side channel via companion-read pattern · Locus 2 = α precedent | §5.1 sub-option (a1) Builder Tier-3 rationale · precedent for single-writer end-state posture aligned with EAB-2 A3 |
| `docs/registry/function_promise_registry_v1_eab1_sidecar.md` | `8437894f7c72143bd3d1256fd78225d75ad0b100c5eeb96d3f00f39491ce61cb` | Row-schema + row-count = 13 + promise-attachment column | §6 sidecar file precedent (15-row EAB-3 sidecar mirrors 13-row EAB-1 + 14-row EAB-2 sidecar pattern) |
| `docs/registry/function_promise_registry_v1_eab2_sidecar.md` | `ddf89929ee072f7c06436c34de5c9c34d8a274c9715f98f96492ef2c7fb067c9` | Row-schema + row-count = 14 + promise-attachment column | §6 sidecar file precedent · EAB-2 attachment-tally pattern (§2 promise-attachment tally reference) |
| `docs/governance/tiered_ruling_model.md` | `9b3c56c14a1159af35c382e1a68368fcf673a381f77cd4734e51a85cd57e51c4` | §2.1 L60 (split-threshold 1,500 LoC / 60 cells verbatim) · §6 rate ledger §6.1 L138 · §6.3 L147 · §6.6 L159 · §6.7 L163 · §6.9 L188 · §6.10 L202 · §6.11 L215 · §9 raw-LoC verdict-unit · §14 sidecar pattern L332 · §23 §0-CAL L390 | Band derivation + sidecar pattern citation + §23 §0-CAL per-line enumeration mandatory on backend/contracts/** + backend/services/** + test cells |
| `docs/registers/phase_ledger_v1.md` | `b8928cc65ebdc190f801da1042ea2a88b1a6d1cdda76f537605e2ad38bd9e382` | §5 SEQUENCE (EAB-3 position 3) + §1 EAB-2 CLOSED row + §3 EAB-3 defined-undispatched row (transitioning to open under this Stage A landing) + §4 terminal figure 39/46 = 84.8% + §7 L-4 row (EAB-2 close) | Sequence position + D-9 auto-proceed context + Phase Ledger update discipline (open transition on Stage A landing) |
| `docs/rulings/no_deferrals_d9_autoproceed_2026-07-15.md` | `1f5ea9de8031cde255db0efd476074c9c3c9f8cc05ead2f20171dbb5c0d81d1d` | Full body | D-9 auto-proceed authorization for this Stage A landing (EAB-2 close → EAB-3 Stage A auto-dispatch) |
| `backend/contracts/service_1_refusal.py` | `4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022` (Parity 32 slot 14 · immutable) | Full-file byte-identity verified via `sha256sum` this session · `git diff HEAD backend/contracts/service_1_refusal.py` empty | Standing Rule v3 continuity attest · v0 byte-identical post-EAB-2 · A5 does NOT touch this contract |
| `backend/contracts/service_1_refusal_v1.py` | `3d5d9845e03d841916e8ce47733710bc490585681fe5b1e8350243875a631fad` (Parity 32 slot 32 · post-EAB-2 landing) | Full-file byte-identity verified via `sha256sum` this session | Standing Rule v3 continuity attest · v1 byte-identical post-EAB-2 close · A5 does NOT touch this contract |
| `services/health/parity_counter.py` (`backend/services/health/parity_counter.py`) | Verified `EXPECTED_PARITY = 32` on-disk post-EAB-2 landing | Field-line inspection | Parity attest source for §2 band table (bumps 32→33 at EAB-3 execution atomic) |

**Zero recall from memory or summary presented as fact.** All row citations, SHAs, line ranges verified this session.

---

## §10 · QA-1..QA-6 attest (Critic Seam Spec v1.0 §5 gates apply · v1.1 Part B pointer active)

Critic Seam Spec v1.0 (`docs/requirements/critic_seam_spec_v1.md` SHA `110a0d0448f66f44…`) + v1.1 sibling (SHA `ad4529b9462cf789…`) apply as landed requirements canon.

| Gate | Attest |
|---|---|
| **QA-1** · Trace lens · every claim resolvable to on-disk source | PASS — every §4 fold traces to EAB v1.1 Part VI §6.2 line + Registry v1 row; §9 read log carries SHAs; §5.1 Tier-1 E1 traces to §IX pre-naming line 179; ES-1 scope traces to `es1_scope_2026-07-14.md` L9 verbatim |
| **QA-2** · Format gate · standing practice · D-10 table with D-1..D-12 rows | PASS — §8 D-10 table carries all 12 rows verbatim with D-12 as heavy-weight row |
| **QA-3** · Fence explicit · scope out-of-scope named | PASS — §7 fence attest carries Critic-pass / G-13 / UI-1 / UI-2 / refusal-envelope / Targeta cap-seat / Lane 2b / Lane 1 / DB-1 / DB-2 / OD-8/9/10 exclusions explicitly + Parity fence (no seal this Stage A) explicit + Standing Rule v3 byte-identity guard explicit |
| **QA-4** · Uncurated verdict · verdicts drawn from measured composition | PASS — §7 D-7 attest reinstates the discipline; AC-A5.b (p95 ≤ 1.5s first-ask · re-ask p95 ≤ 40% of first-ask) and AC-A5.c (load-test at 10× concurrency + version-skew wire cell + ES-1 CI check green) are exemplars (measurement on real request pathways · fixed verdict pathway); D-12 §8 row reinforces |
| **QA-5** · Zero-secret · data-blind extended | PASS — this Stage A carries no secrets/keys/tokens; grep-negative on standard secret patterns is standing practice for all governance-tier artifacts |
| **QA-6** · Registry attribution · every fold cites v1.md row | PASS — §3 aggregate 11 rows cited; §6 sidecar 15 rows enumerated with promise-attachment column; §4 folds carry inline Registry-anchor citations per fold |

Part B pointer (per Critic Seam v1.1 · TQ v1.0 §7): Tier-1 RV cells for EAB-3 folds will ride the atomic execution close, not Stage A. This Stage A is the "*Stage A landing → verbatim Tier-1 relay → rulings → atomic execution → close*" first step of the standard loop.

---

## §11 · Phase Ledger update (Stage A landing transition)

**Part A transitions (upon this Stage A landing):**
- §2 (open) N=0 → **N=1** (EAB-3 transitions defined-undispatched → open at Stage A landing per row-schema convention EAB-1/EAB-2 established: "*same schema convention applies to EAB-2 · EAB-3 · Critic-pass · G-13 · UI-1 · UI-2 upon their Stage A landings and closes*")
- §3 (defined-undispatched) N=6 → **N=5** (EAB-3 removed from defined-undispatched · row-lifecycle annotation `OPEN 2026-07-24 · Stage A landed docs/stage_a_proposals/eab_3_stage_a.md` added to §3 row for sequence traceability per row-schema convention)
- **§4 (Terminal figure)** — `closed 39 · open 1 · defined-undispatched 5 · HELD-D7 1 · denominator 46 · **figure `39/46 = 84.8%`**` — figure holds at 39/46 = 84.8% (denominator unchanged; open/defined-undispatched shuffle inside denominator per row-schema note).

**Part B:** no state changes this Stage A landing (owner-side deliverables unaffected). OD-8/9/10 remain OPEN · sequence-blocking on Lane 2b (not blocking EAB-3 per §7 fence).

**§7 (Owner Configuration Dispatches):** no new L-row this Stage A landing (Stage A is a builder-authored artifact under Owner-ruled EAB v1.1 canon · not an Owner-tier ruling · L-rows accrue on Owner ruling landings).

**Sequence progress:** EAB-2 CLOSED 2026-07-24 (composition ε + α + γ · Parity 32 sealed) → **EAB-3 Stage A OPEN** (this atomic) → **Owner rules Tier-1 E1 (Parity 32→33 seal via PartitionSchema@v0)** → EAB-3 execution atomic auto-proceeds under D-9 → EAB-3 CLOSED → Critic-pass auto-proceeds next (position 4 of 7).

---

*EAB-3 · Stage A Proposal · Landed 2026-07-24 · D-9 auto-proceed authorization from EAB-2 close · Owner rules Tier-1 escalation §5.1 (E1 · Parity 32→33 seal via PartitionSchema@v0) · builder Tier-3 downgrades of §5.2 (Targeta cap-seat no-contact by design) · §5.3 (refusal-envelope sealed at EAB-2 · no re-surface) · §5.4 (F2 seam-value landed via G-3 · no re-landing) disclosed. Companion to: EAB Tier-1 Adoption Spec v1.1 Part VI · Registry v1 · Op. Values v1.1 · ES-1 scope ruling · TQ v1.0 · Critic Seam v1.0/v1.1 · SyniSense mandate · Service1Refusal@v0 + Service1Refusal@v1 baseline · Owner ruling composition ε + α + γ (EAB-2 close) · Prove Step 4 amendment (Owner-authored). Under D-12: every fold deploys in force with known parameters; the Parity 32→33 seal lands as a sealed schema at execution, not staged. §0-CAL §23.1 per-line enumeration MANDATORY for backend/contracts/** + backend/services/** + backend/routers/** (if any) + test invariant cells at execution atomic (this Stage A is doc-only; §23.1 gate-cell roster pre-declared for execution). Every duration/credit figure in §2 carries the Owner-mandated verbatim tag: "Provisional planning anchor — not a commitment. Relative weight only."*
