# EAB-2 · Stage A Proposal

**Phase:** EAB-2 · A3 (Coverage-gap refusal class) + A4 (Per-batch quarantine with systemic-halt threshold)
**Dispatch class:** D-9 auto-proceed under standing ruling `docs/rulings/no_deferrals_d9_autoproceed_2026-07-15.md` (SHA `1f5ea9de8031cde2…`) following clean close of EAB-1 execution atomic (2026-07-15 · close report `docs/close_reports/eab_1.md` SHA `e11bce82…`).
**Sequence position:** 2 of 7 (per phase ledger `docs/registers/phase_ledger_v1.md` §5 · SHA `bddc1362776981a9…`).
**Source of truth:** EAB Tier-1 Adoption Spec v1.1 (`docs/requirements/eab_tier1_adoption_spec_v1.1.md` · SHA `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9`) · Parts IV (A3) + V (A4) + VII F2 fold-into-Op-Values.

---

## §1 · Purpose + scope (Owner-dispatched · verbatim absorption)

EAB v1.1 §IX Execution model verbatim: *"Phase EAB-2 = A3+A4 (refusal grammar + quarantine); Split/merge is builder Tier-3 at Stage A, disclosed."*

**Builder Tier-3 disclosure: NO SPLIT** — A3 and A4 co-land as a single execution atomic. Rationale:
1. Both mechanics operate on the same wire-contract family (refusal envelope; A3 adds a class beside evidential/fault, A4 emits a quarantine-refusal at run scope that is a member of the same governed refusal family).
2. §IX explicitly names EAB-2 as "A3+A4 (refusal grammar + quarantine)" — same seam, same governance layer.
3. Splitting A3 from A4 would land the new refusal class without its per-batch operational proving consumer, contradicting D-12 (*"the capability deploys in force"*).
4. The Parity 31→32 seal is a single sanctioned event; splitting the atomic across two commits would either (a) double-seal (defect) or (b) leave A4 refusal-class-emitting the new envelope before Parity is sealed at A3 (order-of-operations defect). Single-seam execution is the only defect-free ordering.

**Adopted mechanics landing in EAB-2:**

**A3 · Coverage-gap refusal class (EAB v1.1 Part IV):**
- **R-A3.1** — Every non-answer classifies as exactly one of: coverage gap · evidential refusal · system fault. Wire contract additive: new class beside existing envelope, v-next by additive versioning; any byte-contact with a frozen envelope is Tier-1 per standing rule.
- **R-A3.2** — Coverage gap behavior: response names the gap in the asker's terms (estate region, period, source class — from registry vocabulary, observed not invented); carries the un-extracted region identifiers internally; FILES the gap as an extraction candidate visible to Targeta's planning inputs (demand signal, not authorization).
- **R-A3.3** — Fault discipline preserved verbatim: retrieval timeout / downstream error is NEVER surfaced as any refusal class. Existing rule, restated.
- **R-A3.4** — No confidence language crosses the boundary: gap responses state absence and (where a plan exists) status — they never estimate what absent evidence "would show." Solva's assertion discipline applies to gaps exactly as to answers.

**A4 · Per-batch quarantine + systemic-halt threshold (EAB v1.1 Part V):**
- **R-A4.1** — A governance failure on one ingestion batch (purpose validation, de-identification fault, policy violation) quarantines THAT batch — ledger row, receipt marked, batch excluded from downstream — and the run continues.
- **R-A4.2** — Run-level halt triggers when the quarantine rate exceeds the systemic threshold (2% DEFAULT · per-instance seam value · Part VII F2 · set at S2.onboard · dual-control on change per MC-E3 α). Halt is HALT: operator notification · no silent resume.
- **R-A4.3** — Quarantined batches are re-processable after remediation to a new output version with new receipts — never in-place mutation (existing immutability doctrine; restated as the quarantine exit path).

**Acceptance criteria in scope:** AC-A3.a, AC-A3.b, AC-A3.c (Part IV §4.3) + AC-A4.a, AC-A4.b, AC-A4.c (Part V §5.3) — 6 acceptance criteria total.

**Explicitly out of scope (fences from EAB v1.1 §1.2 + §IX):**
- A5 · Precomputed evidence partitions + session working set — EAB-3 scope (§IX).
- Critic-pass phase (Tier-2 harness · CR-7 · CIF manifest fields · archive ledger) — separate phase (§IX + Owner sequencing).
- G-13 · Registry Doctrine §8.1 additive-surface completion (remaining 5 of 8) — separate phase.
- UI-1 / UI-2 — Extraction Console (UI-1) · Integration Console + S1 memory plane (UI-2) — separate phases.
- Model acquisition (§IX D7 fence · zero curl/download this atomic).
- Calibration machinery beyond F3 (measurement-era per ES-4).
- Shard-as-atomic-unit (§1.2 REJECTED · NormalizedUnit is atomic).
- Scheduler beside Targeta (§1.2).
- Double-buffering / quantization execution (§1.2 · measurement-era).
- Any Targeta-input contact beyond the named cap seat (§IX pre-named surface · expect none).

**Parity fence:** the Parity 31→32 seal via new `Service1Refusal@v1` contract is a **sanctioned seal event** pre-named at Tier-1 relay §5.1 below. It **executes at the EAB-2 EXECUTION atomic**, NOT at this Stage A. Parity 31 held byte-identical through Stage A landing.

---

## §2 · Band (Governance §9 · raw LoC verdict-unit · §4.2 split threshold citation)

Per `docs/governance/tiered_ruling_model.md` §9 (raw LoC verdict-unit ruling · 2026-07-10 Owner-verbatim) and §4.2 (pre-authorized split thresholds · Tier 2 · disclosure-not-blocking). Rate ledger applied per §6.1–§6.11.

**Estimated LoC breakdown (Tier-2 · disclosure-not-blocking):**

| Component | LoC low | LoC high | Rate ledger row |
|---|---:|---:|---|
| A3 · new `Service1Refusal@v1` frozen contract (Parity 31→32 · additive class `coverage_gap` + gap descriptor fields: `estate_region`, `period`, `source_class`, `filed_candidate_id`) | 90 | 150 | §6.3 · new contract module |
| A3 · contract snapshot `service_1_refusal_v1.contract_snapshot.json` (new invariant JSON) | 40 | 80 | §6.3 additive |
| A3 · refusal-class dispatcher wiring at Solva composition boundary (route to v1 envelope when coverage-gap detected; preserve v0 emission for evidential/fault refusals during read-side migration) | 80 | 130 | §6.3 |
| A3 · Targeta gap-candidate filer (`file_gap_candidate` receives {estate_region, period, source_class}; idempotent per-key; visible to planning inputs) | 90 | 140 | §6.3 |
| A3 · fault-never-refusal AST negative-scan cell (extends existing `PROM-S1-runtime-transient-never-refusal` regime to the new envelope) | 30 | 50 | §6.10 · AST negative-scan |
| A4 · per-batch quarantine event writer (ledger row · receipt-marked · batch-excluded-from-downstream · run continues) | 100 | 150 | §6.3 |
| A4 · systemic-halt threshold evaluator (reads `SeamValues.quarantine_systemic_halt_threshold` · compares live quarantine rate · triggers HALT + operator notification) | 80 | 120 | §6.3 |
| A4 · remediation-to-new-version path (quarantined batch → new output version with new receipts; append-only preserved) | 60 | 100 | §6.3 |
| Pytest cells: 6 AC gates + 5 pipeline invariant cells (three-response-types-distinct-schema, fault-injection-forced-timeout-yields-fault, filed-candidate-idempotent, synthetic-policy-violation-batch, synthetic-systemic-fault-triggers-halt, remediation-walk-trace, Parity 32 attest, additive-versioning attest, seam-value-F2-live-read, coverage-gap-copy-grammar-bound) | 120 | 180 | §6.1 · 12 LoC/cell · 11 cells |
| Playwright chromium cell: Ask Console (reference app) renders three refusal classes distinctly (AC-A3.c) | 40 | 70 | §6.5 |
| Frontend Jest cell: refusal class copy grammar-bound (AC-A3.c static check on the reference-app renderer) | 30 | 50 | §6.4 |
| §6.9 verbatim-carrier overhead (R-A3.x + R-A4.x invariant text carried in modules per AF-E4 α precedent) | 50 | 90 | §6.9 · partial use |
| §6.10 AST/reflection gates (Parity 32 attest + AST negative on fault-as-refusal + AST positive on class-honesty-render-time in reference app) | 60 | 100 | §6.10 · 3 cells |
| Contract touch (Parity 31→32 · SEALED at EXECUTION atomic · NOT this Stage A) | 0 | 0 | **Parity 31 held byte-identical this Stage A; +1 (Service1Refusal@v1) at execution** |

**Total band estimate: raw LoC `[low=870, high=1410]`.**

**§4.2 split-threshold disclosure:** If total execution LoC exceeds 1200 raw LoC at execution time, the seam splits as **commit A = A3** (refusal grammar + Parity 31→32 seal + Targeta gap-candidate filer) and **commit B = A4** (per-batch quarantine + systemic-halt evaluator + remediation-to-new-version). NO Owner ruling required unless threshold hits at execution time (§4.2 · disclosure-not-blocking · Tier 2). Rationale for split boundary: A4's quarantine event writer, if it emits a refusal-family envelope on halt, depends on Parity 32 landing first; commit A seals Parity 32 and lands the envelope; commit B lands the operational per-batch machinery against that sealed envelope. Both commits carry Parity attest independently (Parity 31→32 in commit A · Parity 32 held in commit B).

---

## §3 · Registry v1 citations (D-11 canon-before-attest · v1.md is active source)

Every fold cites `docs/registry/function_promise_registry_v1.md` (SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a`) as active source. Zero citations to v0 lineage as active source (v0.md + v0.1..v0.5 supplements are historical byte-carried body inside v1.md per G-2 Registry Maintenance close).

**Aggregate citation count in this Stage A body:** 12 distinct v1.md rows cited across §4 folds + §5 escalations + §6 sidecar enumeration:

1. `PROM-S1-frozen-wire-contract` (v1 §2) — A3 envelope byte-identity + additive-versioning root
2. `PROM-S1-additive-versioning` (v1 §2) — A3 Parity 31→32 additive seal · V1-G7 assertion set bumps with the new snapshot
3. `PROM-S1-refusal-taxonomy-closed` (v1 §2 · currently 4-code auth-set) — A3 extends the taxonomy to admit `coverage_gap` as a governed class alongside evidential and fault classes; the taxonomy remains closed at v1 (four-code auth taxonomy is orthogonal to the three-class refusal grammar; A3 folds the two family definitions into a single unified closed enumeration under Service1Refusal@v1)
4. `PROM-S1-runtime-transient-never-refusal` (v1 §2) — A3 R-A3.3 fault-never-dressed rule preserved verbatim; AST negative-scan gate over new envelope module
5. `PROM-S1-honesty-grammar-source-labels` (v1 §2) — A3 R-A3.4 gap responses state absence / status; NO confidence language / NO estimate of absent-evidence-would-show
6. `PROM-S1-class-honesty-render-time` (v1 §2) — A3 AC-A3.c reference-app renders three refusal classes distinctly per UI-Spec binding-copy discipline
7. `synisense.shield.refusal_taxonomy_closed` (v1 §3.a) — SyniSense-side attest of the extended taxonomy under Service1Refusal@v1
8. `akki.instance.seams_scoped_by_instance_id` (v1 §S1 · MC-E2 α reflexive · G-3 sixth-seam-value landing) — A4 R-A4.2 seam-value `quarantine_systemic_halt_threshold` read at run scope · per-instance
9. `akki.backend.s2_onboard_writes_five_seam_values_dual_control_adjacent` (v1 §S1) — F2 fold: SeamValues cardinality moves five → six; G-3 close report `docs/close_reports/g3_operating_values_v1_1.md` SHA `0a91e1b4…` already landed the sixth field on-disk at `backend/services/multi_instance/onboard_context.py::SeamValues.quarantine_systemic_halt_threshold`; A4 consumes it (no re-landing)
10. `PROM-S3-append-only-ledger` (v1 §2) — A4 R-A4.1 quarantine ledger row · A4 R-A4.3 remediation-to-new-version (never in-place mutation)
11. `PROM-S3-audit-trail-immutable` (v1 §2) — A4 quarantine ceremony · remediation walk visible end-to-end
12. §14 sidecar pattern (v1 §M · G-2 R4 reflexive rows precedent + EAB-1 sidecar precedent `docs/registry/function_promise_registry_v1_eab1_sidecar.md`) — EAB-2 sidecar filing pattern

---

## §4 · Fold enumeration · row-by-row

Each fold is FACT / NORM / DEFAULT class per Op. Values §7 discipline, with Registry v1 row citation.

### §4.A · A3 folds (Part IV)

- **A3.1 · Three-class refusal grammar at wire (`Service1Refusal@v1`)** — **FACT-class** (three response types distinct at wire schema · not copy variations · schema cells prove distinctness). Registry anchor: `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning`. New sidecar row.

- **A3.2 · Fault-never-dressed-as-refusal preservation** — **FACT-class** (retrieval timeout / downstream error surfaces as fault-envelope · never any refusal class · existing rule restated verbatim R-A3.3). Registry anchor: `PROM-S1-runtime-transient-never-refusal` extended to v1 envelope. AST negative-scan cell enforces at CI. New sidecar row.

- **A3.3 · Coverage-gap descriptor (registry vocabulary observed not invented)** — **FACT-class** (gap descriptor fields `estate_region`, `period`, `source_class` draw values from Mtafiti registry vocabulary; hard-coded values not in the registry are honesty violations per `PROM-S2-census-dimension-integrity` precedent). Registry anchor: `PROM-S1-honesty-grammar-source-labels`. New sidecar row.

- **A3.4 · Targeta gap-candidate filing (idempotent · demand-signal not authorization)** — **DEFAULT-class** (idempotency key derived from `(estate_region, period, source_class)` tuple; second identical ask cites the same filed candidate; extraction of filed gaps happens only under normally-governed objectives — eligibility wall stands per §1.2 discipline). Registry anchor: reuses Targeta `slice_freeze` + `commission_wizard` inputs pattern (Targeta v1 §3.d rows); no new Targeta contract; filing is an additive record on the planning inputs surface. New sidecar row.

- **A3.5 · No-confidence-language boundary (assertion discipline over gaps)** — **FACT-class** (gap responses state absence / plan-status ONLY · zero estimate of what absent evidence "would show" · Solva's assertion boundary applies to gaps exactly as to answers). Registry anchor: `PROM-S1-honesty-grammar-source-labels` + `PROM-S1-byte-verbatim-anchor-grounding` (rules out semantic-strength language over unmeasured material). New sidecar row.

### §4.B · A4 folds (Part V)

- **A4.1 · Per-batch quarantine event (ledger row · receipt-marked · batch-excluded · run continues)** — **FACT-class** (governance failure on one batch quarantines THAT batch; ledger row is append-only per `PROM-S3-append-only-ledger`). Registry anchor: `PROM-S3-append-only-ledger` + `PROM-S3-audit-trail-immutable`. New sidecar row.

- **A4.2 · Systemic-halt threshold evaluator (F2 seam value read at run scope)** — **DEFAULT-class** (2% DEFAULT · per-instance · set at S2.onboard per MC-E3 α initial-set/ledger semantics · dual-control on change; the class is DEFAULT because the value is DEFAULT-class per Op. Values v1.1 §6.6 · seam-value read is FACT but the threshold value that decides halt-or-continue is DEFAULT). Registry anchor: `akki.instance.seams_scoped_by_instance_id` (v1 §S1) + G-3 close `docs/close_reports/g3_operating_values_v1_1.md` (SHA `0a91e1b4…`) F2 landing precedent. F2 seam-value already landed at `backend/services/multi_instance/onboard_context.py::SeamValues.quarantine_systemic_halt_threshold` per G-3 close; A4 consumes, does not re-land. New sidecar row.

- **A4.3 · Halt is HALT (operator notification · no silent resume)** — **FACT-class** (R-A4.2 verbatim). Registry anchor: `PROM-S3-audit-trail-immutable` (halt ceremony ledgered) + Op. Values v1.1 §6.6 dual-control discipline (change to threshold rides the same ceremony · which is orthogonal to the halt itself but shares the ceremony family). New sidecar row.

- **A4.4 · Remediation-to-new-version path (no in-place mutation)** — **FACT-class** (R-A4.3 · quarantined batches reprocess into a new output version with new receipts; immutability doctrine restated as quarantine exit path). Registry anchor: `PROM-S3-append-only-ledger` + `PROM-S1-additive-versioning`. New sidecar row.

### §4.C · Acceptance-criteria (AC) folds (Part IV §4.3 + Part V §5.3)

- **AC-A3.a** — **FACT-class** — Three response types proven distinct at wire (schema cells) · fault-injection proves forced timeout yields fault, never a refusal class (existing AF cells extended). New sidecar row.
- **AC-A3.b** — **FACT-class** — Coverage-gap response produces an observable filed candidate in targeting inputs · second identical ask cites the same filed candidate (idempotent · no duplicate filing).
- **AC-A3.c** — **FACT-class** — Ask Console (reference app) renders the three classes distinctly per UI-Spec binding-copy discipline · refusal copy is grammar-bound, not free text. Playwright cell + Jest static-grep cell.
- **AC-A4.a** — **FACT-class** — Synthetic policy-violation batch injected mid-run → quarantined · run completes · ledger row present.
- **AC-A4.b** — **FACT-class** — Synthetic systemic fault (>threshold) → run halts · notification observable.
- **AC-A4.c** — **FACT-class** — Quarantine → remediate → re-process walk visible end-to-end in the trace.

---

## §5 · Tier-1 escalation surfaces (pre-named)

Per Owner-verbatim EAB v1.1 §IX: *"Pre-named Tier-1 surfaces: refusal-envelope contract contact (A3; expect additive v-next, Tier-1 if any frozen byte is touched) · the F2 seam-value admission (touches §6 family definition) · partition-schema contract class (A5; new artifact class → registered, additive · **A5 scope** — deferred to EAB-3, not this atomic) · any Targeta-input contact beyond the named cap seat (§1.2; expect none)."*

### §5.1 · E1 · Refusal-envelope contract contact · **Tier-1** — Parity 31→32 seal via `Service1Refusal@v1` (pre-named · sanctioned)

**Surface:** the frozen `Service1Refusal@v0` contract at `backend/contracts/service_1_refusal.py` (SHA `4fe38c214dc59260…` · Parity slot 14 of 31 · v0.md L1-40 doctrinal note) + its snapshot at `backend/tests/invariants/service_1_refusal.contract_snapshot.json` (SHA `56ec42bb5a12bda0…`). A3 R-A3.1 requires "the three are distinct response types in the wire contract — not copy variations." The current v0 envelope carries three reason codes (`no_defensibility_floor` · `no_lawful_basis` · `composition_below_floor`) all of which are members of the evidential-refusal family. A3 adds a `coverage_gap` reason plus gap-descriptor fields (`estate_region: str`, `period: str`, `source_class: str`, `filed_candidate_id: str`) that the v0 envelope cannot carry.

**Builder analysis (does NOT resolve):** two structurally distinct posture options exist and the Owner rules the posture. This is the first parity change since 2026-07-04 (per EAB-1 close report §10 — "**Parity 31 → 32 seal event** via new `Service1Refusal@v1` contract at Tier-1 relay").

**Owner ruling surface:**

- **(a)** Land `Service1Refusal@v1` as a **new frozen contract module** at `backend/contracts/service_1_refusal_v1.py` with its own snapshot at `backend/tests/invariants/service_1_refusal_v1.contract_snapshot.json`. `Service1Refusal@v0` preserved byte-identical (v0-freeze doctrine per `PROM-S1-additive-versioning`). Parity 31 → 32. V1-G7 assertion set bumps from 31 to 32. Consumers migrate read-side to v1 for the coverage-gap class; write-side may continue emitting v0 for evidential/fault refusals during a bounded migration window OR v1 emits both existing v0 reasons AND the new `coverage_gap` reason as a single unified envelope (single-writer posture · cleaner). **Sub-option (a1):** v1 is a strict superset envelope · v0 remains registered but v0-emitting call-sites transition to v1 at the same commit as the seal · single-writer end-state at close. **Sub-option (a2):** v1 emits `coverage_gap` only · v0 continues emitting the three evidential-refusal reasons · two writers in force · A3.1 wire-distinctness is proven across both envelopes rather than within one.

- **(b)** Extend `Service1Refusal@v0` **in place** by admitting `coverage_gap` as a fourth reason plus optional gap-descriptor fields on the existing schema. **REJECTED at pre-name by standing rule** — Standing Rule v3 forbids byte contact with a frozen contract; `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` require additive versioning, not in-place mutation. Option (b) is disclosed to complete the enumeration but is not a live posture — it violates a load-bearing invariant.

- **(c)** Other Owner ruling (e.g., stage the coverage-gap descriptor in a sidecar telemetry channel outside the refusal envelope · REJECTED by A3 R-A3.1: coverage gap MUST be a wire-contract class, not a sidecar; but named here to complete the enumeration).

**Builder Tier-3 recommendation:** **(a1)** — single-writer end-state under a superset envelope is the least-drift posture: it collapses the refusal-family into one canonical shape at v1 (making AC-A3.a's wire-distinctness a within-envelope schema-cell attest rather than a cross-envelope class-detection attest), preserves v0 byte-identity per Standing Rule v3, and lands Parity 32 as a clean superset-additive event.

**Fence carried into this Stage A:** the seal is **pre-named**, not executed. Zero contract file created this Stage A · zero snapshot file created · Parity 31 held byte-identical at close of this Stage A landing.

### §5.2 · E2 · F2 seam-value admission (already landed via G-3 · downgrade to no-live-ruling-surface · disclosed)

**Surface:** `SeamValues.quarantine_systemic_halt_threshold` field at `backend/services/multi_instance/onboard_context.py`, landed via G-3 · `docs/close_reports/g3_operating_values_v1_1.md` (SHA `0a91e1b4…`) · sixth field · 2% DEFAULT · per-instance · set at S2.onboard per MC-E3 α initial-set/ledger semantics · dual-control on change.

**Builder analysis (resolves at Tier-3 authority — evidence-derived downgrade):** the F2 seam-value admission was pre-named as a Tier-1 surface at EAB v1.1 §IX ("*touches §6 family definition*"). G-3 has already ruled it and landed it on-disk; the seam-value cardinality has already moved from five to six per Op. Values v1.1 §6.6. A4 consumes the value at run scope. No new admission required at EAB-2; no new Owner ruling surface remains. Disclosed per §IX pre-naming; downgraded on evidence (G-3 ruling and landing are prior-atomic on-disk).

**Downgrade rationale (D-11 read):** `docs/close_reports/g3_operating_values_v1_1.md` §F2 landing block + `docs/requirements/operating_values_v1_1.md` §6.6 (SHA `3a3cff3b…`) + `backend/services/multi_instance/onboard_context.py::SeamValues` (six fields on disk) all confirm the admission has already happened. A4 R-A4.2 explicitly cites Part VII F2 as the authorization anchor; the F2 admission is the authority, not a new surface.

Disclosed as pre-named per §IX; downgraded on evidence (G-3 ruling and landing are on-disk canonical).

### §5.3 · E3 · Partition-schema contract class (A5 · **DEFERRED to EAB-3**)

**Surface:** partition-schema is A5-scope (§IX enumeration explicitly attaches it to A5). A5 is EAB-3 phase per §IX Execution model.

**Downgrade rationale:** A5 is not in scope for this atomic (§1 fence attest above). The partition-schema contract class will be pre-named as a Tier-1 surface at EAB-3 Stage A, not here.

Disclosed as pre-named per §IX; deferred by phase scope.

### §5.4 · E4 · Targeta gap-candidate filing input surface (§IX "any Targeta-input contact beyond the named cap seat" · expect none)

**Surface:** A3.4 files gap candidates as demand signal to Targeta's planning inputs. §IX pre-names "any Targeta-input contact beyond the named cap seat" as Tier-1 material. The named cap seat for Targeta inputs is the existing `slice_freeze` + `commission_wizard` intake (Targeta v1 §3.d rows).

**Builder analysis (resolves at Tier-3 authority):** gap candidates are additive to the demand-signal side of Targeta's planning inputs, not to its cap-seat / eligibility-computing side. The demand-signal record is a planning input (ranking helper), NOT an eligibility widener; the eligibility wall stands per §1.2 discipline ("*Filing is demand signal, not authorization: extraction of filed gaps happens only under normally-governed objectives — the eligibility wall stands; learning/demand may reorder, never widen.*"). No contact with the Targeta cap seat is proposed.

**Downgrade rationale (D-11 read):** §1.2 rules the discipline explicitly; §IX §Part V R-A3.2 rules the demand-signal-not-authorization posture explicitly. Gap-candidate filing is a demand-signal-side additive record with no cap-seat contact. Enforced by an AST/reflection cell (§6 sidecar row #12 below) grepping for any import path from the gap-filer module into `backend/services/targeta/slice_freeze.py` or any eligibility-computing module.

Disclosed as pre-named per §IX; downgraded on evidence (spec discipline is explicit; expected-none contact is not a live escalation).

### §5.5 · Tier-3 remainder (builder Tier-3 judgment · disclosed at close)

- **Coverage-gap descriptor null-vs-empty-string discipline** (e.g., `period: str | None` vs `period: str = ""`) — DEFAULT class · set at execution time per honesty grammar (`PROM-S1-honesty-grammar-source-labels` prefers null over fabricated empty strings for unmeasured dimensions).
- **Quarantine ledger row schema field-set** — DEFAULT class · reuse existing Northena ledger row shape with a `quarantine_reason` tag; no new contract; disclosed at close.
- **Systemic-halt threshold evaluator polling interval / event-driven-vs-cron discipline** — DEFAULT class; event-driven at batch-close is the pre-authorized default per §S3 append-only ledger semantics.
- **Remediation output-version naming convention** (`_r1`, `_r2` suffix vs semver-style vs receipt-chain child pointer) — DEFAULT class · builder Tier-3 at execution time.
- **Fault-envelope contract choice for R-A3.3** — the fault-never-dressed-as-refusal rule requires a fault envelope distinct from Service1Refusal; existing precedent is HTTP 503 with structured detail (per `PROM-S1-config-defect-fail-loud`) for infra faults and `PROM-S1-runtime-transient-never-refusal` sidecar telemetry for transients. No new contract; disclosed at close.

---

## §6 · R4 sidecar (enumerated only · NOT created this Stage A)

Per Tiered-Ruling `docs/governance/tiered_ruling_model.md` §14 sidecar pattern (v1-era sidecar precedent · ratified 2026-07-11) + Registry v1 §M G-2 R4 reflexive-rows precedent + EAB-1 sidecar precedent (`docs/registry/function_promise_registry_v1_eab1_sidecar.md` · 13 rows · zero new promises · SHA `8437894f…`).

**Proposed sidecar path:** `docs/registry/function_promise_registry_v1_eab2_sidecar.md`

**Row count proposed: 14 rows**, all attaching to existing v1.md §2 promises via foreign-key resolution (zero new promises minted — conservation-not-authorship posture per §M):

| # | Proposed sidecar row | Rung | Promise attachment |
|---:|---|---:|---|
| 1 | `akki.refusal.a3_service1refusal_v1_frozen_additive` — A3.1 new frozen contract at Parity 32 · additive-versioning attest · v0 byte-identity preserved | 1 · Deterministic | `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` |
| 2 | `akki.refusal.a3_three_class_wire_distinct_schema_cell` — AC-A3.a wire distinctness proven by schema cells (not copy variations) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 3 | `akki.refusal.a3_fault_never_dressed_ast_negative_scan` — R-A3.3 AST negative-scan over v1 envelope module (no fault-envelope-as-refusal-class path) | 1 · Deterministic | `PROM-S1-runtime-transient-never-refusal` |
| 4 | `akki.refusal.a3_coverage_gap_descriptor_registry_vocabulary_only` — R-A3.2 gap descriptor draws from Mtafiti registry vocabulary; hard-coded value = honesty violation | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` + `PROM-S2-census-dimension-integrity` |
| 5 | `akki.refusal.a3_no_confidence_language_over_gap` — R-A3.4 gap responses state absence / plan-status ONLY; assertion discipline applied to gaps | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` + `PROM-S1-byte-verbatim-anchor-grounding` |
| 6 | `akki.refusal.a3_ac_a3_c_reference_app_class_distinct_render` — AC-A3.c Ask Console renders three refusal classes distinctly; copy grammar-bound | 1 · Deterministic | `PROM-S1-class-honesty-render-time` |
| 7 | `akki.targeta.a3_gap_candidate_filing_idempotent_demand_signal` — A3.4 idempotent filing by `(estate_region, period, source_class)` tuple · AC-A3.b same-ask-cites-same-candidate | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 8 | `akki.targeta.a3_gap_candidate_no_cap_seat_contact_ast_negative` — §5.4 AST negative-scan · gap-filer imports NOT reaching Targeta eligibility modules · eligibility wall stands (§1.2) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 9 | `akki.batch.a4_per_batch_quarantine_ledger_row` — A4.1 per-batch quarantine event · ledger row · receipt-marked · batch-excluded · run continues | 1 · Deterministic | `PROM-S3-append-only-ledger` |
| 10 | `akki.batch.a4_systemic_halt_threshold_evaluator_reads_f2_seam_value` — A4.2 halt evaluator reads `SeamValues.quarantine_systemic_halt_threshold` at run scope · per-instance · 2% DEFAULT | 1 · Deterministic | `akki.instance.seams_scoped_by_instance_id` (v1 §S1 · MC-E2 α) |
| 11 | `akki.batch.a4_halt_is_halt_operator_notification_no_silent_resume` — A4.2 verbatim · halt ceremony ledgered · operator notification observable | 1 · Deterministic | `PROM-S3-audit-trail-immutable` |
| 12 | `akki.batch.a4_remediation_to_new_version_no_inplace_mutation` — A4.3 remediation produces new output version with new receipts · append-only preserved · AC-A4.c walk visible end-to-end | 1 · Deterministic | `PROM-S3-append-only-ledger` + `PROM-S1-additive-versioning` |
| 13 | `akki.parity.eab2_service1refusal_v1_parity_32_attest` — Parity 32 attest cell asserts 32 contracts + 32 snapshots · V1-G7 bumps; MC-E1 α zero-mutation attest extended to Service1Refusal@v0 (v0 byte-identity preserved under new landing) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` + `PROM-S1-additive-versioning` |
| 14 | `akki.registry.eab2_sidecar_reflexive_row` — this sidecar itself · §14 pattern · §M reflexive-rows precedent · EAB-1 sidecar precedent | 1 · Deterministic | Registry v1 §M sidecar-pattern authority |

**Zero new promises minted** (conservation-not-authorship posture per Registry v1 §M · EAB-1 sidecar precedent). All 14 rows target existing `PROM-S1-frozen-wire-contract` (×5), `PROM-S1-additive-versioning` (×3), `PROM-S1-runtime-transient-never-refusal` (×1), `PROM-S1-honesty-grammar-source-labels` (×2), `PROM-S2-census-dimension-integrity` (×1), `PROM-S1-byte-verbatim-anchor-grounding` (×1), `PROM-S1-class-honesty-render-time` (×1), `PROM-S3-append-only-ledger` (×3), `PROM-S3-audit-trail-immutable` (×1), `akki.instance.seams_scoped_by_instance_id` (×1), Registry v1 §M sidecar-pattern authority (×1).

**Sidecar file NOT created this Stage A** (per Owner-verbatim REPLY FORMAT §6 · "enumerated only · NOT created"). Sidecar lands at execution atomic, byte-carried as a sibling file per Registry Doctrine §5 v1-era pattern and per EAB-1 sidecar precedent.

---

## §7 · D-7 fence attestation

Verdicts uncurated per D-7 (Registry Doctrine Part IV D-7): *"engineer the inputs relentlessly; never touch the test."* Every acceptance criterion above is measured on real inputs against the pre-declared threshold; verdicts are drawn from measured composition, not curated. AC-A4.a and AC-A4.b are the D-7 exemplars for this atomic: synthetic policy-violation and synthetic systemic-fault injections are input-side constructions against a fixed verdict pathway.

**No EAB-3 content:** A5 (precomputed evidence partitions + session working set) is EAB-3 scope. Zero fold in this Stage A touches partition-schema, session working-set, or the partition contract class. §5.3 explicitly defers.

**No Critic-pass content:** Tier-2 harness · CR-7 checklist amendment · CIF manifest schema fields · archive ledger — all Critic-pass phase scope, out of scope here.

**No G-13 content:** Registry Doctrine §8.1 additive-surface completion (remaining 5 of 8) — G-13 scope, out of scope here.

**No UI-1 content:** Extraction Console to Designer Brief depth — out of scope. The reference-app Ask Console cell at AC-A3.c is a **reference-app** rendering cell against existing Ask Console surface only; it does NOT touch Extraction Console.

**No UI-2 content:** Integration Console + S1 memory plane — out of scope. No frontend/src touch to `IntegrationConsole*` anticipated in EAB-2 execution.

**No model acquisition:** zero curl of model weights, zero `pip install` of AI models, zero pyannote/NeMo/Silero fetch this atomic. A3 + A4 are governance-wire mechanics, not perception model mechanics.

**No calibration machinery:** measurement telemetry (F3) lands as-declared in EAB v1.1 §Part VII F3 · already in force via G-3 close; no calibration harness beyond the F3 rule.

**No Targeta cap-seat contact:** §5.4 AST negative-scan attests no import path from A3.4 gap-filer into Targeta eligibility modules; eligibility wall stands per §1.2.

**No re-landing of F2 seam value:** F2 sixth seam value `quarantine_systemic_halt_threshold` is already on-disk via G-3 close (`docs/close_reports/g3_operating_values_v1_1.md` SHA `0a91e1b4…`) at `backend/services/multi_instance/onboard_context.py::SeamValues`; A4 consumes, does not re-land.

**Parity fence:** the Parity 31→32 seal via `Service1Refusal@v1` is a **sanctioned seal event** at the EAB-2 EXECUTION atomic. Zero contract file created this Stage A. Zero snapshot file created this Stage A. `git diff --stat HEAD backend/contracts/` expected empty at close of this Stage A landing. `git diff --stat HEAD backend/tests/invariants/*.contract_snapshot.json` expected empty at close of this Stage A landing. **Parity 31 held byte-identical this Stage A.**

**Governance-stack byte-identity:** §14/§15.1/§18/§19/§20/§21/§22 sanctioned amendment blocks unchanged in this Stage A landing (§22 was landed prior in this same builder turn as a separate dispatch line per Msg 431); `docs/governance/` diff = §22 admission only + End-of-record footer extension (Dispatch 1 scope, disclosed under Dispatch 1 governance byte-identity guard, not Stage A scope).

**Standing Rule v3:** all protected artifacts remain byte-identical — v0 lineage · v1.md · Op. Values v1.0/v1.1 · EAB v1.1 · Critic Seam v1.0/v1.1 · TQ v1.0 · CIF v1.0 · TT v1.0 · Extraction De-risking v1.0 · S1 Memory v1.0 · SJM v1.0 · SyniSense mandate · registry doctrine v1.0 · MANIFEST · registers v1.0..v1.6 · all 27+ prior rulings · `/app/salvage/` · `backend/contracts/**` · snapshots · governance stack outside sanctioned §22 amendment.

---

## §8 · D-10 self-audit table (D-1..D-12 · STANDING PRACTICE per QA-2)

| # | Defect | Verdict (this Stage A) | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Every fold in §4 traces to an EAB v1.1 §IV/§V mandate line + a Registry v1 row citation in §3. |
| D-2 | NL-only claim | PASS | Every claim above is disk-verifiable (EAB v1.1 SHA `312427c672e9db8a` at line ranges cited; Registry v1 SHA `d6ad136f65426c0f` at row/section cited; governance §4.2/§6/§9/§14 at line ranges cited; G-3 close SHA `0a91e1b4b72b0059`; EAB-1 close SHA `e11bce8285eb1c78`). |
| D-3 | Curated verdict | PASS | 14 R4 rows enumerated · 6 AC criteria enumerated · 1 Tier-1 surface named with builder analysis and three sub-options (a1/a2/b-rejected/c) · 3 pre-named surfaces downgraded on evidence with rationale · Tier-3 remainder disclosed. |
| D-4 | Rung inflation | PASS | All 14 sidecar rows at Rung-1 Deterministic (§6.11 shared-helper class). No fold proposed at rung above what MC-E1 α, MC-E3 α, EAB-1 A1-A2 sidecar precedent bounds. |
| D-5 | Cross-phase content leakage | PASS | Zero A5 content (EAB-3 scope) · zero Critic-pass / G-13 / UI-1 / UI-2 content. §7 fence attest lists each explicit exclusion. AC-A3.c reference-app cell is on Ask Console only (existing surface), not on any UI-1/UI-2 phase console. |
| D-6 | Silent scope drift | PASS | Split/merge decision at §1 disclosed builder Tier-3 with rationale (D-12-aligned: single-seam execution deploys in force; Parity 31→32 seal is a single sanctioned event that cannot double-seal). §4.2 split-threshold at 1200 raw LoC pre-authorized-disclosed. |
| D-7 | Invented scope | PASS | Every acceptance criterion is EAB v1.1 verbatim (§4.3 + §5.3); zero fabricated criteria. Tier-1 escalations pre-named per §IX; zero fabricated escalation. §7 explicit D-7 attest carried. AC-A4.a and AC-A4.b are D-7 exemplars (synthetic input · fixed verdict path). |
| D-8 | Silent drift | PASS | Parity 31 attest carried in §2 band table (contract touch = 0/0 this Stage A) and in §7 fence attest; §14 sidecar pattern cited for R4 rows; all Standing Rule v3 artifacts named for byte-identity guard at close. §22 admission landing is Dispatch 1 governance-stack scope, disclosed under Dispatch 1 byte-identity guard, not Stage A scope. |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked at Stage A landing. Native pytest cell suite proposed for execution atomic per §2 band table. |
| D-10 | Menu emission | PASS | Zero permission-menu emitted this Stage A. Tier-1 surface §5.1 states four ruling options (a1/a2/b-rejected/c) as *Owner ruling surface enumeration*, not builder menu — pre-named per §IX and structured per EAB-1 Stage A §5.1 precedent (three-option enumeration pattern). |
| D-11 | Canon-before-ruling / LLM-memory recall | PASS | Full canon read log at §9 below with SHAs + line ranges. Every EAB v1.1 mandate citation traces to a live-command-verified line range this session; every Registry v1 citation traces to a live grep this session; every contract SHA traces to a live `sha256sum` this session. No memory recall presented as fact. |
| **D-12** | **Experimentation at system level only** | PASS | Every fold in §4 deploys in force with known parameters: A3.1 three-class refusal grammar has three distinct wire types with pre-declared schema · A3.2 fault-never-dressed rule has an AST negative-scan gate that fails the build on violation (not warns) · A3.3 coverage-gap descriptor draws from Mtafiti registry vocabulary (pre-declared surface) · A3.4 gap-candidate idempotency key is pre-declared as `(estate_region, period, source_class)` tuple · A3.5 no-confidence-language boundary is pre-declared (assertion discipline) · A4.1 quarantine event ledger row shape is pre-declared (existing Northena ledger row shape + `quarantine_reason` tag) · A4.2 systemic-halt threshold value is DEFAULT-class per Op. Values v1.1 §6.6 (2% DEFAULT with a named parametric adjustment ceremony) — NOT a trial-mode threshold · A4.3 halt-is-halt is verbatim R-A4.2 with no soft-halt intermediate · A4.4 remediation-to-new-version is pre-declared per `PROM-S3-append-only-ledger`. AC cells are D-7 measurement (verdict on parameters via synthetic inputs), NOT staged proving. **Zero observe-first · zero shadow phase · zero trial modes · zero staged proving.** The Parity 31→32 seal event lands at execution atomic **in force** — the new Service1Refusal@v1 envelope carries the sealed schema; not a staged additive with revisit windows. |

---

## §9 · D-11 canon-before-ruling read log

Files read during Stage A authoring (this session):

| File | SHA-256 | Line range read | Purpose |
|---|---|---|---|
| `docs/requirements/eab_tier1_adoption_spec_v1.1.md` | `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9` | §Part IV L83-105 (A3 mandate + requirements + AC) + §Part V L107-127 (A4 mandate + requirements + AC) + §Part VII L155-161 (F1/F2/F3 folds into Op. Values v1.1) + §IX L177-179 (execution model + pre-named Tier-1 surfaces) + §1.2 L27-37 (fences + shard-rejection + no-scheduler-beside-Targeta) | Scope source of truth · A3 + A4 in scope · A5 out of scope · pre-named Tier-1 surfaces · fences |
| `docs/registry/function_promise_registry_v1.md` | `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a` | Grepped for `PROM-S1-refusal-taxonomy-closed` · `PROM-S1-frozen-wire-contract` · `PROM-S1-additive-versioning` · `PROM-S1-runtime-transient-never-refusal` · `PROM-S1-honesty-grammar-source-labels` · `PROM-S1-class-honesty-render-time` · `PROM-S1-byte-verbatim-anchor-grounding` · `synisense.shield.refusal_taxonomy_closed` · `akki.instance.seams_scoped_by_instance_id` · `PROM-S3-append-only-ledger` · `PROM-S3-audit-trail-immutable` · §M sidecar precedent | Row citations for §3 aggregate + §4 folds + §5 escalations + §6 sidecar (12 aggregate cites · 14 sidecar rows) |
| `docs/requirements/operating_values_v1_1.md` | `3a3cff3be0cb59d28cd06a7e25123155d6984323f78e386687ee05c20f2d9c5b` | §6 amendment L17 (sixth seam value F2) + §6.6 L43 (quarantine_systemic_halt_threshold · 2% DEFAULT · MC-E3 α · dual-control) + §11 L87 (v1.1 evidence-class discipline for future rows) | F2 seam-value already-landed authority · A4.2 downgrade rationale · MC-E3 α initial-set/ledger semantics |
| `docs/close_reports/g3_operating_values_v1_1.md` | `0a91e1b4b72b00593a8c3a770615efae0ef150e1016bbaf906bbe62d9853ce3e` | Verified on-disk existence and SHA for §5.2 downgrade rationale | F2 landing precedent · SeamValues cardinality five → six |
| `docs/close_reports/eab_1.md` | `e11bce8285eb1c78392b8ac261c551d07033e9c27fa3f4d2f43aff2604f55289` | §10 D-9 auto-proceed declaration (EAB-2 scope preview) + §3 R4 sidecar landed (13-row precedent · SHA `8437894f…`) + §5 Full-sweep verification (Parity 31 baseline · pytest 1296 · 1 skipped) + §7 D-10 table (12-row precedent for §8 below) | Precedent citations for §6 sidecar pattern · §8 D-10 table pattern · §5.1 Tier-1 E1 pre-naming source |
| `docs/rulings/eab_1_e1_2026-07-15.md` | `eec9ea73f42758e006b4b5a3ad66f6657975919262ed0d99d8215cfc65b65d2e` | Full body | E1 ruling precedent + AST cell load-bearing precedent for §5.1 sub-option consideration + Tier-1 ruling-language pattern |
| `docs/stage_a_proposals/eab_1_stage_a.md` | `d5231d93c303ce2b163e2115cae3d507688693e4e58a122202ae825a4b4118dc` | §1-§10 structural headings + §5.1 three-option enumeration pattern + §2 band table structure + §6 sidecar structure + §8 D-10 12-row table | Stage A precedent structure (11-section EAB-2 mirrors EAB-1 pattern with §11 Phase Ledger addition per Owner-dispatched reply format) |
| `docs/governance/tiered_ruling_model.md` | `0da76e9b1de8cdb751910d375127f2fc9401dd06d528062041d51940ad80d041` (post-§22) | §4.2 split-threshold pointer · §6 rate ledger · §9 raw-LoC verdict-unit · §14 sidecar pattern · §22 admission (landed this builder turn under Dispatch 1) | Band derivation + sidecar pattern citation + §22 descriptive-canon subordination noted |
| `docs/registers/phase_ledger_v1.md` | `bddc1362776981a9375f3642bf15a2bc215597a64deab682412deaf85016d671` | §5 SEQUENCE (EAB-2 position 2) + §1 EAB-1 CLOSED row + §3 EAB-2 defined-undispatched row (transitioning to open under this Stage A landing) + row-schema note L63 | Sequence position + D-9 auto-proceed context + Phase Ledger update discipline (open transition on Stage A landing) |
| `docs/rulings/no_deferrals_d9_autoproceed_2026-07-15.md` | `1f5ea9de8031cde255db0efd476074c9c3c9f8cc05ead2f20171dbb5c0d81d1d` | Full body | D-9 auto-proceed authorization for this Stage A landing |
| `backend/contracts/service_1_refusal.py` | `4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022` (Parity 31 · immutable) | L1-99 full — reason-code enumeration L66-68, DefensibilityClass import L47, Literal["refused"] discriminator L55, family-consistency note with AdmissionRefusal L1-17 | §5.1 Tier-1 E1 Parity 31→32 seal source of truth · v0 envelope byte-identity anchor · additive-versioning target |
| `backend/tests/invariants/service_1_refusal.contract_snapshot.json` | `56ec42bb5a12bda02f98653ee5762dda62fe91bd5543fbef6ea2f20f5822020d` (Parity 31 · immutable) | Header + $defs list | §5.1 Tier-1 E1 snapshot pattern (v1 snapshot will land as new file at execution atomic; v0 snapshot byte-identity preserved) |
| `backend/services/multi_instance/onboard_context.py` | Verified `SeamValues.quarantine_systemic_halt_threshold` field on-disk (six-field cardinality) | Field-list inspection | §5.2 downgrade rationale · A4.2 seam-value read-target on-disk |
| `docs/registry/function_promise_registry_v1_eab1_sidecar.md` | `8437894f7c72143bd3d1256fd78225d75ad0b100c5eeb96d3f00f39491ce61cb` | Row-schema + row-count = 13 + promise-attachment column | §6 sidecar file precedent (14-row EAB-2 sidecar mirrors 13-row EAB-1 sidecar pattern) |

**Zero recall from memory or summary presented as fact.** All row citations, SHAs, line ranges verified this session.

---

## §10 · QA-1..QA-6 attest (Critic Seam Spec v1.0 §5 gates apply · v1.1 Part B pointer active)

Critic Seam Spec v1.0 (`docs/requirements/critic_seam_spec_v1.md` SHA `110a0d0448f66f44…`) + v1.1 sibling (SHA `ad4529b9462cf789…`) apply as landed requirements canon.

| Gate | Attest |
|---|---|
| **QA-1** · Trace lens · every claim resolvable to on-disk source | PASS — every §4 fold traces to EAB v1.1 §IV/§V line + Registry v1 row; §9 read log carries SHAs; §5.1 Tier-1 E1 traces to on-disk `service_1_refusal.py` L1-99 |
| **QA-2** · Format gate · standing practice · D-10 table with D-1..D-12 rows | PASS — §8 D-10 table carries all 12 rows verbatim with D-12 as heavy-weight row |
| **QA-3** · Fence explicit · scope out-of-scope named | PASS — §7 fence attest carries EAB-3/Critic-pass/G-13/UI-1/UI-2 exclusions explicitly + Parity fence (no seal this Stage A) explicit + F2 no-re-landing explicit + Targeta no-cap-seat-contact explicit |
| **QA-4** · Uncurated verdict · verdicts drawn from measured composition | PASS — §7 D-7 attest reinstates the discipline; AC-A4.a + AC-A4.b are exemplars (synthetic input · fixed verdict path); D-12 §8 row reinforces |
| **QA-5** · Zero-secret · data-blind extended | PASS — this Stage A carries no secrets/keys/tokens; grep-negative on standard secret patterns is standing practice for all governance-tier artifacts |
| **QA-6** · Registry attribution · every fold cites v1.md row | PASS — §3 aggregate 12 rows cited; §6 sidecar 14 rows enumerated with promise-attachment column |

Part B pointer (per Critic Seam v1.1 · TQ v1.0 §7): Tier-1 RV cells for EAB-2 folds will ride the atomic execution close, not Stage A. This Stage A is the "*Stage A landing → verbatim Tier-1 relay → rulings → atomic execution → close*" first step of the standard loop.

---

## §11 · Phase Ledger update (Stage A landing transition)

**Part A transitions (upon this Stage A landing):**
- §2 (open) N=1 → **N=2** (EAB-2 transitions defined-undispatched → open at Stage A landing per row-schema convention EAB-1 established: "*same schema convention applies to EAB-2 · EAB-3 · Critic-pass · G-13 · UI-1 · UI-2 upon their Stage A landings and closes*")
- §3 (defined-undispatched) N=7 → **N=6** (EAB-2 removed from defined-undispatched · row-lifecycle annotation `OPEN 2026-07-15 · Stage A landed docs/stage_a_proposals/eab_2_stage_a.md` added to §3 row for sequence traceability if row-schema convention prefers)
- **§4 (Terminal figure)** — `closed 38 · open 2 · defined-undispatched 6 · denominator 46 · **figure `38/46 = 82.6%`**` — figure holds at 38/46 = 82.6% (denominator unchanged; open/defined-undispatched shuffle inside denominator per row-schema note).

**Part B:** no state changes this Stage A landing (owner-side deliverables unaffected).

**Sequence progress:** EAB-1 CLOSED → **EAB-2 Stage A OPEN** (this atomic) → **Owner rules Tier-1 E1 (Parity 31→32 seal via Service1Refusal@v1)** → EAB-2 execution atomic auto-proceeds under D-9 → EAB-2 CLOSED → EAB-3 auto-proceeds next.

---

*EAB-2 · Stage A Proposal · Landed 2026-07-15 · D-9 auto-proceed close-of-prior-atomic authorization · Owner rules Tier-1 escalation §5.1 (E1 · Parity 31→32 seal via Service1Refusal@v1) · builder Tier-3 downgrade of §5.2 (F2 seam-value already landed via G-3), §5.3 (partition-schema deferred to EAB-3), and §5.4 (Targeta cap-seat no-contact by design) disclosed. Companion to: EAB Tier-1 Adoption Spec v1.1 · Registry v1 · Op. Values v1.1 · TQ v1.0 · Critic Seam v1.0/v1.1 · SyniSense mandate · Service1Refusal@v0 baseline. Under D-12: every fold deploys in force with known parameters; the Parity 31→32 seal lands as a sealed schema at execution, not staged.*
