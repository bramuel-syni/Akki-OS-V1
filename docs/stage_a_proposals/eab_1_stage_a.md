# EAB-1 · Stage A Proposal

**Phase:** EAB-1 · A1 (Pre-perception restructuring pass) + A2 (Occurrence index)
**Dispatch class:** D-9 auto-proceed under standing ruling `docs/rulings/no_deferrals_d9_autoproceed_2026-07-15.md` (SHA `1f5ea9de8031cde2…`) following clean close of the S1 Memory Model + Five-Flag atomic (2026-07-15).
**Sequence position:** 1 of 7 (per phase ledger `docs/registers/phase_ledger_v1.md` §5, SHA `cbb428c2dcaf10b4…`).
**Source of truth:** EAB Tier-1 Adoption Spec v1.1 (`docs/requirements/eab_tier1_adoption_spec_v1.1.md`, SHA `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9`).

---

## §1 · Scope (Owner-dispatched · verbatim absorption)

EAB v1.1 Part IX Execution model verbatim: *"Phase EAB-1 = A1+A2 (ingestion side, one seam); Phase EAB-2 = A3+A4 (refusal grammar + quarantine); Phase EAB-3 = A5 (serving pattern; may ride a first-party surface as its proving consumer). Split/merge is builder Tier-3 at Stage A, disclosed."*

Builder Tier-3 disclosure: **NO SPLIT** — A1 and A2 co-land as a single execution atomic. Rationale: A2 (occurrence index) is a strict downstream consumer of A1.4 (acoustic-fingerprint dedup output); splitting them would land A1 without a proving consumer for its dedup output, contradicting D-12 (*"the capability deploys in force with UI-2; no trial modes exist"* — same D-12 discipline applies here: A1's dedup deploys in force with A2's occurrence-writer as its proving consumer). Merge is not creating a new scope; it is executing the specified scope as one seam per §IX's own "ingestion side, one seam" language.

**Adopted mechanics landing in EAB-1:**
- **A1.1** Demux & normalize (Part II §2.2 R-A1.1)
- **A1.2** Batch segmentation (Part II §2.2 R-A1.2)
- **A1.3** Voice-activity detection (Part II §2.2 R-A1.3 · Silero registry-pinned · no new model)
- **A1.4** Acoustic-fingerprint dedup (Part II §2.2 R-A1.4 · chromaprint-class · exact/near-exact match only)
- **A2.1** Occurrence rows as NormalizedUnits (Part III §3.2 R-A2.1 · five_rings@v0 shape · MC-E1 α anchor)
- **A2.2** license_class attachment (Part III §3.2 R-A2.2 · MC-E4 α default fail-closed · internal_only)
- **A2.3** Canonical→occurrence trace walkability (Part III §3.2 R-A2.3 · honesty grammar applies)

**Acceptance criteria in scope:** AC-A1.a, AC-A1.b, AC-A1.c, AC-A1.d (Part II §2.3) + AC-A2.a, AC-A2.b (Part III §3.3) — 6 acceptance criteria total.

**Explicitly out of scope (fences from EAB v1.1 §1.2 + §IX):**
- A3 · Coverage-gap refusal class — EAB-2 scope
- A4 · Per-batch quarantine with systemic-halt threshold — EAB-2 scope
- A5 · Precomputed evidence partitions + session working set — EAB-3 scope
- Parity 31→32 seal via Service1Refusal@v1 — EAB-2's Tier-1 relay (this phase holds Parity 31)
- Any new perception model beyond the registry-pinned Silero (§IX D7 fence)
- Any commercial premise (§1.2)
- Batch schema landing in `contracts/` (§1.2 · MC-E3 placement precedent · batch schema stays in worker contracts)
- Scheduler beside Targeta (§1.2 · engine re-derivation defect class per conformance-audit precedent)
- Double-buffering / quantization execution (§1.2 · measurement-era; ES-4 measure-before-optimize)

---

## §2 · Band (Governance §9 · raw LoC verdict-unit · §4.2 split-threshold citation)

Per `docs/governance/tiered_ruling_model.md` §9 (raw LoC verdict-unit ruling, 2026-07-10 Owner-verbatim) and §4.2 (pre-authorized split thresholds — Tier 2, disclosure-not-blocking). Rate ledger applied per §6.1–§6.11.

**Estimated LoC breakdown (Tier-2 · disclosure-not-blocking):**

| Component | LoC low | LoC high | Rate ledger row |
|---|---:|---:|---|
| A1.1 · demux/normalize worker module (ffmpeg-driven; existing provenance discipline) | 60 | 90 | §6.3 · 100 LoC/module standalone |
| A1.2 · batch segmentation module (batch_id content-address · programme-block vs 30-min window) + worker-side batch schema | 90 | 130 | §6.3 + additive |
| A1.3 · VAD worker wrapper (Silero registry-pinned · non-speech content-type index writer) | 70 | 110 | §6.3 |
| A1.4 · acoustic-fingerprint dedup (chromaprint-class · canonical/occurrence emitter) | 130 | 190 | §6.3 (larger module) |
| A2.1 · occurrence-writer emitting NormalizedUnits (five_rings@v0 · zero contract touch) | 80 | 130 | §6.3 |
| A2.2 · license_class attachment (reuse MC-E4 α default · fail-closed at outer gate) | 20 | 40 | §6.2 amortised endpoint-adjacent |
| A2.3 · canonical→occurrence trace-walkability wiring (existing trace lens; +walk endpoint) | 40 | 70 | §6.2 · 40 LoC/endpoint amortised |
| Pytest cells: 6 AC gates + 6 pipeline invariant cells (rung-1 gate that no audio bypasses A1; VAD grep-negative; dedup false-positive audit fixture; occurrence-index count; MC-E1 α zero-mutation attest; MC-E4 α license_class default) | 90 | 140 | §6.1 · 12 LoC/cell |
| Playwright chromium cell: none required (server-side pipeline; no interactive UI) | 0 | 0 | §6.5 |
| Frontend Jest cells: none required (ingestion-side; no interactive UI landing this phase) | 0 | 0 | §6.4 |
| §6.9 verbatim-carrier overhead (Owner-ruled invariant text carried in modules per AF-E4 α precedent) | 40 | 80 | §6.9 · 100-150 LoC/carrier (partial use) |
| §6.10 AST/reflection gate (batch-schema-NOT-in-contracts negative-scan + no-scheduler negative-scan) | 40 | 60 | §6.10 · 40 LoC/cell |
| Contract touch | 0 | 0 | **Parity 31/31 preserved · zero contracts/ file touched · zero snapshot touched** |

**Total band estimate: raw LoC `[low=660, high=1040]`.**

**§4.2 split-threshold disclosure:** If total execution LoC exceeds 1200 raw LoC at execution time, the seam splits as commit A = A1 (demux + segmentation + VAD + dedup) and commit B = A2 (occurrence-writer + license_class + trace walkability). NO Owner ruling required unless threshold hits at execution time (§4.2 · disclosure-not-blocking · Tier 2). Rationale for split boundary: A2 depends on A1.4's dedup output emission; commit A lands the dedup-emit surface with a placeholder no-op consumer; commit B lands the occurrence-writer against that surface. Both commits carry MC-E1 α parity attest independently.

---

## §3 · Fold enumeration · row-by-row

Each fold is FACT / NORM / DEFAULT class per Op. Values §7 discipline, with Registry v1 row citation.

### §3.A · A1 folds (Part II)

- **A1.1 · Demux & normalize** — **FACT-class** (deterministic transcoding; no measurement dependency). Registry anchor: `PROM-S1-frozen-wire-contract` (provenance discipline unchanged; derived artifact carries lineage to source object). No existing v1.md row for demux specifically; A1.1 lands as new R4 row in the EAB-1 sidecar (§6) attaching to existing `PROM-S1-frozen-wire-contract`.

- **A1.2 · Batch segmentation** — **NORM-class** (target 15–60 minutes; programme-block vs 30-minute default is estate-conditioned). Registry anchor: MC-E3 α placement precedent (schema lives in worker contracts, NOT in `contracts/` — Parity-31 conservation). v1.md rows §S2 (S2.onboard-context + tenant_entities population) establish the worker-contracts-not-frozen pattern. New sidecar row.

- **A1.3 · Voice-activity detection (Silero)** — **DEFAULT-class** (Silero threshold and registry-pin are estate-conditioned; non-speech logging is FACT). Registry anchor: `PROM-9-2a-real-worker-provenance` (v1.md row `mtafiti.perception.pinned_model_provenance`) — Silero as VAD is a pinned model, same provenance discipline as ASR workers. No new perception model per §IX D7 fence.

- **A1.4 · Acoustic-fingerprint dedup** — **DEFAULT-class** (chromaprint threshold set for exact/near-exact only; false-positive rate ≤ 0.5% is DEFAULT, revisited per AC-A1.c audit). Registry anchor: honesty grammar (`PROM-S1-honesty-grammar-source-labels`) — a suppressed span retains a re-queue pointer; a dedup false positive is recoverable, not an honesty violation, because the pointer preserves the pre-dedup evidence. New sidecar row.

### §3.B · A2 folds (Part III)

- **A2.1 · Occurrence rows as NormalizedUnits** — **FACT-class** (occurrence rows land in five_rings@v0 shape; zero contract mutation). Registry anchor: **MC-E1 α close** (v1.md row `akki.data_source.structured_connector_base` + `akki.data_source.tabular_ingest_normalizes_units_zero_contract_mutation`, §S1). Zero mutation to `contracts/five_rings.py` or its snapshot. Locator carries `{canonical_id, station, timestamp, batch lineage}` — additive dict content, no schema change.

- **A2.2 · license_class attachment** — **DEFAULT-class** (`internal_only` per MC-E4 α fail-closed; S4 egress only on explicit rights posture). Registry anchor: **MC-E4 α close** (v1.md row `akki.data_source.license_class_pairs_at_ingest`, §S1). Reuse of existing outer-gate refusal envelope; zero contract touch.

- **A2.3 · Canonical→occurrence trace walkability** — **FACT-class** (relation is walkable in the trace via existing trace-lens contract; honesty grammar applies). Registry anchor: `PROM-S3-audit-trail-immutable`. No new contract; walk endpoint reuses existing trace-lens envelope.

### §3.C · Acceptance-criteria (AC) folds (Part II §2.3 + Part III §3.3)

- **AC-A1.a** — **FACT-class** — rung-1 job-seam gate; no audio to perception queue without A1 pass. New sidecar row.
- **AC-A1.b** — **NORM-class** — per-month report of raw hours, speech hours, dedup ratio, occurrence-index row count (30–50% NORM expectation).
- **AC-A1.c** — **DEFAULT-class** — 100-hour stratified sample audit; false-positive ≤ 0.5% DEFAULT.
- **AC-A1.d** — **FACT-class** — news-classified blocks dedup-exempt; exemption cost visible in AC-A1.b report.
- **AC-A2.a** — **FACT-class** — occurrence-index dimensions exposed via census (data-blind discipline; dimensions emerge from estate).
- **AC-A2.b** — **FACT-class** — brief citing occurrence data grounds in registry reads (existing OB gates); S4 artifact refuses egress under default license_class (existing MC-E4 gate; one new cell for occurrence artifact class).

---

## §4 · Registry v1 citations (D-11 canon-before-attest · v1.md is active source)

Every fold cites `docs/registry/function_promise_registry_v1.md` (SHA `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a`) as active source. Zero citations to v0 lineage as active source (v0.md + v0.1..v0.5 supplements are historical byte-carried body inside v1.md per G-2 Registry Maintenance close).

**Aggregate citation count in this Stage A body:** 11 distinct v1.md rows cited across §3 folds + §5 escalations + §6 sidecar enumeration:

1. `PROM-S1-frozen-wire-contract` (v1 §2) — A1.1 provenance discipline · AC-A1.a rung-1 gate
2. MC-E3 α placement precedent (v1 §S2) — A1.2 batch schema
3. `PROM-9-2a-real-worker-provenance` (v1 §2 + `mtafiti.perception.pinned_model_provenance` v1 §3.c) — A1.3 Silero pinning
4. `PROM-S1-honesty-grammar-source-labels` (v1 §2) — A1.4 dedup honesty
5. `akki.data_source.structured_connector_base` (v1 §S1, MC-E1 α close) — A2.1 anchor
6. `akki.data_source.tabular_ingest_normalizes_units_zero_contract_mutation` (v1 §S1, MC-E1 α attest) — A2.1 zero-mutation
7. `akki.data_source.license_class_pairs_at_ingest` (v1 §S1, MC-E4 α close) — A2.2 anchor
8. `PROM-S3-audit-trail-immutable` (v1 §2) — A2.3 trace walkability
9. `PROM-S2-census-dimension-integrity` (v1 §2 + `mtafiti.census.dimension_registry_vocabulary` v1 §3.c) — AC-A2.a data-blind
10. `PROM-S1-runtime-transient-never-refusal` (v1 §2) — VAD/dedup runtime error posture (fault-never-refusal fence carried from §1.2 A3 discipline)
11. §14 sidecar pattern (v1 §M · G-2 R4 reflexive rows precedent) — EAB-1 sidecar filing pattern

---

## §5 · Tier-1 escalation surfaces (pre-named)

Per Owner-verbatim §IX: *"Pre-named Tier-1 surfaces: occurrence-unit locator vocabulary (A2; expect zero-mutation per MC-E1 α, Tier-1 if not) · refusal-envelope contract contact (A3; expect additive v-next, Tier-1 if any frozen byte is touched)."*

### §5.1 · E1 · Occurrence-unit locator vocabulary · **Tier-1** (pre-named)

**Surface:** the `NormalizedUnit.provenance.locator: Dict[str, Any]` field (`backend/contracts/five_rings.py:113-119` · ProvenanceRing §5.2). A2.1 requires locator to carry `{canonical_id, station, timestamp, batch lineage}` for occurrence rows.

**Builder analysis (does NOT resolve):** the locator field is typed `Dict[str, Any]` and free-form per the docstring: *"Modality-native locator. Examples: text → {page:int, span:[int,int]}; audio/video → {t_start_ms:int, t_end_ms:int}; image → {bbox:[x,y,w,h]}."* Adding `{canonical_id, station, timestamp, batch lineage}` for the occurrence modality is dict-content, not schema — the field's Dict[str, Any] type accepts it without contract mutation. This APPEARS additive per MC-E1 α ("zero contract mutation").

**Why Tier-1 anyway:** the locator vocabulary is load-bearing on the trace resolver (Registry Doctrine §3.2 byte-identity lock enforcement class). A new locator key family (`canonical_id`, `station`, `batch_lineage`) may implicitly change how the trace lens or an audit-walk parses locators. Even without byte contact to the frozen contract, the vocabulary contact is Tier-1 material per §IX pre-naming.

**Owner ruling surface:**
- (a) admit `{canonical_id, station, timestamp, batch lineage}` as the additive occurrence-modality locator vocabulary in the v1 R4 sidecar (§6 below), with an AST/reflection cell (§6.10) proving zero contract mutation on `contracts/five_rings.py` and its snapshot;
- (b) require a new modality enum value on `Modality` (`five_rings.py:44`, current `text|audio|video|image`) → occurrence is not a modality, it's a lineage layer over an existing modality (audio for A1-processed content); (b) inspects only if a Modality contact is proposed — expected NONE, but named for Owner ratification of the fence;
- (c) other Owner ruling.

Builder Tier-3 recommendation: (a) — locator dict-content addition is the least-mutation posture; MC-E1 α zero-mutation attest carries the parity gate.

### §5.2 · E2 · Batch schema placement · **Tier-3 (pre-authorized · disclosed)**

**Surface:** the batch (§1.2 vocabulary: "shard in source vocabulary — the processing/batch unit of the job seam ONLY"). A1.2 R-A1.2 verbatim: *"The batch is job-seam vocabulary per §1.2 — its schema lives with the worker contracts, NOT in contracts/ (Parity-31 conservation per the MC-E3 placement precedent)."*

**Builder analysis (resolves at Tier-3 authority):** MC-E3 α placement precedent is explicit. Batch schema is a worker-contract type, not a frozen Parity-31 contract. It lands in a new file `backend/services/perception/batch_schema.py` (or equivalent worker-side path) with its own Pydantic model. Zero contact to `backend/contracts/`. Parity 31 held byte-identical.

**Downgrade rationale (D-11 read):** §1.2 rules the placement explicitly ("*NOT in contracts/*"); the ruling authority is the EAB v1.1 spec itself. No Owner ruling surface remains — this is a builder Tier-3 execution decision at execution time. Enforced by a new AST/reflection cell (§6.10) grepping for batch-schema imports into `backend/contracts/` at CI.

Disclosed as pre-named per §IX; downgraded on evidence (spec ruling is explicit).

### §5.3 · Tier-3 remainder (dev Tier-3 judgment · disclosed at close)

- Dedup threshold value (chromaprint distance cutoff) — DEFAULT class per AC-A1.c; set at execution time per estate; disclosed at close.
- 30-minute default window for batch segmentation without programme-block metadata — NORM class per R-A1.2 ("*target 15–60 minutes*"); 30-minute is the pre-authorized default.
- Occurrence-writer chunk size for batch commit — DEFAULT class; no Owner ruling surface.
- Non-speech content-type index storage location — worker-side, disclosed at close.

---

## §6 · R4 sidecar (enumerated only · NOT created this Stage A)

Per Tiered-Ruling `docs/governance/tiered_ruling_model.md` §14 sidecar pattern (v1-era sidecar precedent, ratified 2026-07-11) + Registry v1 §M G-2 R4 reflexive-rows precedent (`docs/registry/function_promise_registry_v1.md:639`).

**Proposed sidecar path:** `docs/registry/function_promise_registry_v1_eab1_sidecar.md`

**Row count proposed: 13 rows**, all attaching to existing v0.md §2 promises via foreign-key resolution (zero new promises minted — conservation-not-authorship posture per §M):

| # | Proposed sidecar row | Rung | Promise attachment |
|---:|---|---:|---|
| 1 | `akki.perception.a1_demux_normalize` — A1.1 rung-1 CPU demux/normalize with source-object lineage | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 2 | `akki.perception.a1_batch_segmentation_content_addressed` — A1.2 content-addressed batch_id with programme-block vs 30-min default | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 3 | `akki.perception.a1_batch_schema_worker_contracts_not_frozen` — MC-E3 α placement precedent · batch schema outside `contracts/` (AST negative-scan gate) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 4 | `akki.perception.a1_vad_silero_registry_pinned` — A1.3 Silero VAD registry-pinned with mode-selection-evident-at-read | 1 · Deterministic | `PROM-9-2a-real-worker-provenance` |
| 5 | `akki.perception.a1_non_speech_content_type_index` — VAD-stripped spans logged as content-type index (never discarded) | 1 · Deterministic | `PROM-S3-audit-trail-immutable` |
| 6 | `akki.perception.a1_acoustic_fingerprint_dedup` — A1.4 chromaprint-class exact/near-exact match; suppressed spans retain re-queue pointer | 1 · Deterministic | `PROM-S1-honesty-grammar-source-labels` |
| 7 | `akki.perception.a1_gate_no_audio_bypass` — AC-A1.a rung-1 job-seam gate (zero audio to perception queue without A1) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 8 | `akki.perception.a1_per_month_report` — AC-A1.b monthly reduction-ratio report (raw hours, speech hours, dedup ratio) | 1 · Deterministic | `PROM-S3-audit-trail-immutable` |
| 9 | `akki.perception.a1_stratified_sample_audit_default_class` — AC-A1.c 100-hour stratified sample false-positive audit (≤ 0.5% DEFAULT) | 2 · Owner (or fixture) | `PROM-S1-honesty-grammar-source-labels` |
| 10 | `akki.perception.a1_news_block_dedup_exempt` — AC-A1.d news-classified blocks dedup-exempt by default | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 11 | `akki.perception.a2_occurrence_row_five_rings_zero_mutation` — A2.1 occurrence-writer emits NormalizedUnits (MC-E1 α zero-mutation attest) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 12 | `akki.perception.a2_license_class_default_internal_only` — A2.2 license_class = internal_only fail-closed (MC-E4 α reuse) | 1 · Deterministic | `PROM-S1-frozen-wire-contract` |
| 13 | `akki.perception.a2_canonical_occurrence_trace_walkable` — A2.3 canonical→occurrence walkable in trace-lens; honesty grammar applies (fingerprint match class stated) | 1 · Deterministic | `PROM-S3-audit-trail-immutable` |

**Zero new promises minted** (conservation-not-authorship posture per Registry v1 §M · G-2 precedent). All 13 rows target existing `PROM-S1-frozen-wire-contract` / `PROM-9-2a-real-worker-provenance` / `PROM-S1-honesty-grammar-source-labels` / `PROM-S3-audit-trail-immutable`.

**Sidecar file NOT created this Stage A** (per Owner-verbatim REPLY FORMAT §6 · "enumerated only · NOT created"). Sidecar lands at execution atomic, byte-carried inside the closing report or as a sibling file per Registry Doctrine §5 v1-era pattern.

---

## §7 · D-7 fence attestation

Verdicts uncurated per D-7 (Registry Doctrine Part IV D-7): *"engineer the inputs relentlessly; never touch the test."* Every acceptance criterion above is measured on real inputs against the pre-declared threshold; verdicts are drawn from measured composition, not curated. The AC-A1.c 100-hour audit is the D-7 exemplar: sample discipline is fixed pre-execution; verdict is whatever the audit measures.

**No EAB-2 content:** A3 (coverage-gap refusal class) and A4 (per-batch quarantine with systemic-halt threshold) are EAB-2 scope. Zero fold in this Stage A touches the refusal envelope, admission_refusal contract, or the F2 seam-value threshold set. Parity 31 held byte-identical (EAB-2's Parity 31→32 seal via Service1Refusal@v1 is future).

**No Critic-pass content:** Tier-2 harness · CR-7 checklist amendment · CIF manifest schema fields · archive ledger — all Critic-pass phase scope, out of scope here.

**No G-13 content:** Registry Doctrine §8.1 additive-surface completion (remaining 5 of 8) — G-13 scope, out of scope here.

**No UI-1 / UI-2 content:** Extraction Console to Designer Brief depth (UI-1) and Integration Console + S1 memory plane (UI-2) — out of scope. No frontend/src touch anticipated in EAB-1 execution.

**No model acquisition:** zero curl of model weights, zero `pip install` of AI models, zero pyannote/NeMo/Silero fetch. Silero VAD is registry-pinned per §2.2 R-A1.3 and consumed via existing perception worker infrastructure (`backend/services/perception/`).

**No calibration machinery:** measurement telemetry (F3) lands as-declared in EAB v1.1 §Part VII F3; no calibration harness beyond the F3 rule.

**Governance-stack byte-identity:** §14/§15.1/§18/§19/§20/§21 sanctioned amendment blocks unchanged; `docs/governance/` diff-empty expected at EAB-1 close.

**Standing Rule v3:** all protected artifacts remain byte-identical — v0 lineage · v1.md · Op. Values v1.0/v1.1 · EAB v1.1 · Critic Seam v1.0/v1.1 · TQ v1.0 · CIF v1.0 · TT v1.0 · Extraction De-risking v1.0 · S1 Memory v1.0 · SJM v1.0 · SyniSense mandate · registry doctrine v1.0 · MANIFEST · registers v1.0..v1.5 · all 25+ prior rulings · `/app/salvage/` · `backend/contracts/**` · snapshots · governance stack outside sanctioned amendments. All `git diff --stat HEAD <path>` empty at close.

---

## §8 · D-10 self-audit table (D-1..D-12 · STANDING PRACTICE per QA-2)

| # | Defect | Verdict (this Stage A) | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Every fold in §3 traces to an EAB v1.1 §II/§III mandate line + a Registry v1 row citation. |
| D-2 | NL-only claim | PASS | Every claim above is disk-verifiable (EAB v1.1 SHA `312427c672e9db8a` at line ranges cited; Registry v1 SHA `d6ad136f65426c0f` at row/section cited; governance §4.2/§6/§9/§14 at line ranges cited). |
| D-3 | Curated verdict | PASS | 13 R4 rows enumerated · 6 AC criteria enumerated · 2 Tier-1 surfaces named with builder analysis · 1 Tier-1 downgraded to Tier-3 with evidence · Tier-3 remainder disclosed. |
| D-4 | Rung inflation | PASS | 12 of 13 sidecar rows at Rung-1 Deterministic (§6.11 shared-helper); AC-A1.c audit row at Rung-2 (fixture-or-owner class per §6.11 audit precedent). No fold proposed at rung above what MC-E1 α, MC-E4 α, or 9.2a-E1 α precedent bounds. |
| D-5 | Cross-phase content leakage | PASS | Zero A3/A4/A5 content (EAB-2/EAB-3 scope); zero Critic-pass / G-13 / UI-1 / UI-2 content. §7 fence attest lists each explicit exclusion. |
| D-6 | Silent scope drift | PASS | Split/merge decision at §1 disclosed builder Tier-3 with rationale (D-12-aligned: single-seam execution deploys in force; no observe-first single-A1-without-consumer proving). |
| D-7 | Invented scope | PASS | Every acceptance criterion is EAB v1.1 verbatim (§2.3 + §3.3); zero fabricated criteria. Tier-1 escalations pre-named per §IX; zero fabricated escalation. §7 explicit D-7 attest carried. |
| D-8 | Silent drift | PASS | Parity 31 attest carried in §2 band table (contract touch = 0/0); §14 sidecar pattern cited for R4 rows; all Standing Rule v3 artifacts named for byte-identity guard at close. |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked at Stage A landing. Native pytest cell suite proposed for execution atomic per §2 band table. |
| D-10 | Menu emission | PASS | Zero permission-menu emitted this Stage A. Tier-1 surface §5.1 states three ruling options (a/b/c) as *Owner ruling surface enumeration*, not builder menu — pre-named per §IX and structured per prior Stage A precedent (g3 §5.1 pattern). |
| D-11 | Canon-before-ruling / LLM-memory recall | PASS | Full canon read log at §9 below with SHAs + line ranges. Every EAB v1.1 mandate citation traces to a live-command-verified line range this session; every Registry v1 citation traces to a live grep this session. No memory recall presented as fact. |
| **D-12** | **Experimentation at system level only** | PASS | Every fold in §3 deploys in force with known parameters: A1.1 demux/normalize is deterministic transcoding (FACT); A1.2 batch segmentation is content-addressed with pre-authorized 30-minute default (NORM); A1.3 Silero VAD is registry-pinned pre-execution (DEFAULT with named threshold at execution); A1.4 chromaprint threshold is DEFAULT-set with AC-A1.c audit measuring the specification-gap (not a trial mode — the audit is a verdict on the parameter, per D-7); A2.1-A2.3 occurrence-writer + license_class + trace walkability all reuse MC-E1 α / MC-E4 α / trace-lens as-built mechanics. **Zero observe-first · zero shadow phase · zero trial modes · zero staged proving.** The AC-A1.c stratified sample audit (100 hours) is D-7 measurement, not D-12 staged proving: verdict names the DEFAULT threshold as measured, and if the DEFAULT fails the audit, the fold narrows to advertising/jingle classes only per R-A1.4 — that narrowing is a parametric adjustment against a pre-declared threshold, not a "run tentatively" posture. |

---

## §9 · D-11 canon-before-ruling read log

Files read during Stage A authoring (this session):

| File | SHA-256 | Line range read | Purpose |
|---|---|---|---|
| `docs/requirements/eab_tier1_adoption_spec_v1.1.md` | `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9` | 1–217 (full) | Scope source of truth (§I..§X) — A1/A2 in scope, A3/A4/A5 out of scope; §IX pre-named Tier-1 surfaces; §1.2 fences |
| `docs/registry/function_promise_registry_v1.md` | `d6ad136f65426c0f86df2227a540aac8142b24dd0cbb015b71ef2991a7a6718a` | Grepped rows for MC-E1 α, MC-E4 α, 9.2a-E1 α, PROM-S1/S3, §M sidecar precedent, §S1 (structured connector class), §Conformance-Evidence-Registry | Row citations for §3 folds + §5 escalations + §6 sidecar |
| `docs/governance/tiered_ruling_model.md` | `3aa4609fdb00c8131ae7c896e009c18d04332f2fc80b241a9ed130f156fbbab5` (post-§20/§21) | §4.2 (L127) split-threshold pointer · §6 rate ledger (L138–150) · §9 raw-LoC verdict-unit (L249) · §14 sidecar pattern | Band derivation + sidecar pattern citation |
| `docs/registers/phase_ledger_v1.md` | `cbb428c2dcaf10b495a23a23531200f27b61246ac7cf0d755a7bb7ff5f90bf93` | §5 SEQUENCE (EAB-1 position 1) + Part B (S1 dep-cleared B-5) | Sequence position + D-9 auto-proceed context |
| `docs/stage_a_proposals/g3_operating_values_v1_1_stage_a.md` | `117d2401e91d0f75a885de5b543e24a3703cd8f5ab0231c5ac35aa07b36da228` | §1–§9 structural headings | Prior Stage A precedent for structure |
| `backend/contracts/five_rings.py` | (Parity 31 · immutable) | L44 (Modality enum) · L87 (ProvenanceRing) · L113–119 (locator dict field docstring) · L247 (DefensibilityRing) · L276 (NormalizedUnit) | §5.1 Tier-1 locator vocabulary analysis; A2.1 zero-mutation posture |
| `docs/rulings/no_deferrals_d9_autoproceed_2026-07-15.md` | `1f5ea9de8031cde255db0efd476074c9c3c9f8cc05ead2f20171dbb5c0d81d1d` | Full body | D-9 auto-proceed authorization for this Stage A |

**Zero recall from memory or summary presented as fact.** All row citations, SHAs, line ranges verified this session.

---

## §10 · QA-1..QA-6 attest (Critic Seam Spec v1.0 §5 gates apply · v1.1 Part B pointer active)

Critic Seam Spec v1.0 (`docs/requirements/critic_seam_spec_v1.md` SHA `110a0d0448f66f44…`) + v1.1 sibling (SHA `ad4529b9462cf789…`) apply as landed requirements canon.

| Gate | Attest |
|---|---|
| **QA-1** · Trace lens · every claim resolvable to on-disk source | PASS — every §3 fold traces to EAB v1.1 line + Registry v1 row; §9 read log carries SHAs |
| **QA-2** · Format gate · standing practice · D-10 table with D-1..D-12 rows | PASS — §8 D-10 table carries all 12 rows |
| **QA-3** · Fence explicit · scope out-of-scope named | PASS — §7 fence attest carries EAB-2/EAB-3/Critic-pass/G-13/UI-1/UI-2 exclusions explicitly |
| **QA-4** · Uncurated verdict · verdicts drawn from measured composition | PASS — §7 D-7 attest reinstates the discipline; AC-A1.c is the exemplar; D-12 §8 row reinforces |
| **QA-5** · Zero-secret · data-blind extended | PASS — this Stage A carries no secrets/keys/tokens; grep-negative on standard secret patterns is standing practice for all governance-tier artifacts |
| **QA-6** · Registry attribution · every fold cites v1.md row | PASS — §4 aggregate 11 rows cited; §6 sidecar 13 rows enumerated with promise-attachment column |

Part B pointer (per Critic Seam v1.1 · TQ v1.0 §7): Tier-1 RV cells for EAB-1 folds will ride the atomic execution close, not Stage A. This Stage A is the "*Stage A landing → verbatim Tier-1 relay → rulings → atomic execution → close*" first step of the standard loop.

---

*EAB-1 · Stage A Proposal · Landed 2026-07-15 · D-9 auto-proceed close-of-prior-atomic authorization · Owner rules Tier-1 escalation §5.1 (E1) · builder Tier-3 downgrade of §5.2 (E2) disclosed. Companion to: EAB Tier-1 Adoption Spec v1.1 · Registry v1 · Op. Values v1.1 · TQ v1.0 · Critic Seam v1.0/v1.1 · SyniSense mandate · S1 Memory Model v1.0. Under D-12: every fold deploys in force with known parameters; the AC-A1.c 100-hour audit is D-7 verdict measurement against a pre-declared DEFAULT, not staged proving.*
