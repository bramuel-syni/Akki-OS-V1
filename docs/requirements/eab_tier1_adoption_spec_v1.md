**AKKI · GOVERNED ARTIFACT · ADOPTION SPECIFICATION**

**EAB Tier-1 Adoption Specification v1.0**

Streamed-enrichment and precomputed-evidence mechanics, adopted into Akki canon · 2026-07-14

***Provenance and epistemic status: ****source ideas fronted in EAB-2026-01 (owner-provided). This specification re-authors the adopted subset against platform canon; it is the binding text — where it differs from EAB-2026-01, this document governs. Commercial premises in the source (metered GPU pricing, named products, revenue plans, funding checkpoints) are NOT adopted and do not enter the record; the platform is Akki, the current compute posture is unmetered baseline GPUs, and every adopted mechanic is justified on premise-independent gains (throughput, honesty, survivability, product surface). Evidence classes per Operating Values: FACT / NORM / DEFAULT.*

# **Part I — Adoption decision and boundaries**

## **§1.1 Adopted (five mechanics + two gate folds)**

- **A1 · Pre-perception restructuring pass **(CPU-only: demux/normalize → batch segmentation → VAD → acoustic-fingerprint dedup) — Part II.

- **A2 · The occurrence index **as a first-class intelligence artifact — Part III.

- **A3 · Coverage-gap refusal class **— the third member of the refusal grammar — Part IV.

- **A4 · Per-batch quarantine granularity **with a systemic-halt threshold — Part V.

- **A5 · Precomputed evidence partitions + session working set **for interactive surfaces — Part VI.

- **F1/F2 · Gate folds into Operating Values v1.1: **per-language model-serving accuracy gates; quarantine threshold as a governance seam value — Part VII.

## **§1.2 Explicitly NOT adopted — boundaries binding on all execution**

- **Shard-as-atomic-unit is REJECTED; subordination ruling stands. **The platform’s atomic intelligence unit is NormalizedUnit (five_rings@v0, Parity-31 frozen, MC-E1 α). The ingestion batch (“shard” in source vocabulary) is the processing/batch unit of the job seam ONLY: it bounds worker memory, carries quarantine, and anchors batch receipts. Its outputs are NormalizedUnits carrying batch lineage in provenance.locator per MC-E1 α. Any schema, code comment, or contract text that promotes the batch to “the atomic unit of the system” is defect D6-class (wrong-job) and reportable on sight.

- **Budget-capped priority scheduling is NOT a new scheduler. **Objective-serving, registry-read, budget-bounded extraction ordering is Targeta’s deterministic core by mandate. The single genuine delta — a compute/spend cap as a bound — registers as a named Targeta input seat (config, DEFAULT class, unset on unmetered baseline) at the next Targeta-touching phase. Building a scheduler beside Targeta is engine re-derivation, defect class per the conformance-audit precedent.

- **Double-buffering and quantization EXECUTION are measurement-era. **Per standing doctrine (measure-before-optimize; rung-1 measurement first): no prefetch machinery, no quantized serving lands until a measured shortfall or a measured gate-pass exists on real runs. Their acceptance disciplines (throughput telemetry per run; per-language gates) are adopted NOW as F1 and §8 rules; their build is not.

- **No commercial premise enters the record. **No metered-GPU cost machinery, no named commercial products, no external revenue or checkpoint dates ride this specification or its phases.

# **Part II — A1 · Pre-perception restructuring pass**

## **§2.1 Mandate and promise**

**Built to **ensure no expensive perception second is spent on bytes that carry no new information. **Why this matters: **broadcast estates are heavily repetitive (advertising spots, jingles, promos, rebroadcasts) and heavily non-speech (music beds, silence, tones); stripping both before ASR shrinks the perception workload materially — on unmetered baseline hardware this is throughput and time-to-census, and it compounds on every estate and every hardware posture thereafter. Service trace: S2.commission (extraction efficiency) + S4.receive (via A2’s artifact). Ladder rung: 1–2 throughout (deterministic DSP + classical signal processing; no model above rung 2 anywhere in this pass).

## **§2.2 Technical requirements**

Four ordered, CPU-only operations, each a stage in the existing job seam — no new worker class, no new pipeline framework:

- **R-A1.1 Demux & normalize. **Extract audio from source containers; transcode to 16 kHz mono lossless. Source objects are never modified or deleted; restructured audio is a derived artifact with lineage to the source object (existing provenance discipline; no new mechanism).

- **R-A1.2 Batch segmentation. **Cut continuous audio into ingestion batches: bounded by programme block where schedule metadata exists, by fixed 30-minute windows where it does not; target 15–60 minutes; identity is content-addressed (batch_id), carrying station/source id, start/end timestamps, source-object reference, content-type flags from R-A1.3/R-A1.4, and language hypothesis. The batch is job-seam vocabulary per §1.2 — its schema lives with the worker contracts, NOT in contracts/ (Parity-31 conservation per the MC-E3 placement precedent).

- **R-A1.3 Voice-activity detection. **Strip non-speech spans from the perception queue using the existing VAD (Silero, registry-pinned — no new model). Non-speech spans are not discarded: they are logged with timestamps as a distinct content-type index; music spans are analysable signal and enter A2’s index family.

- **R-A1.4 Acoustic-fingerprint dedup. **Compute chromaprint-class fingerprints across batches. Verbatim-repeated content is perceived ONCE against a canonical instance; every other occurrence writes (canonical_id, station/source, timestamp) to the occurrence index (Part III). Threshold set for exact/near-exact acoustic match only. Dedup NEVER deletes: every suppressed span retains a pointer sufficient to re-queue it for perception — any false positive is recoverable by re-queue, mechanically.

## **§2.3 Acceptance criteria**

- AC-A1.a · Zero audio enters the perception queue without passing A1 — enforced as a job-seam gate (rung 1), not convention.

- AC-A1.b · Per processed source-month, the pass reports: raw hours in, speech hours out, dedup ratio, occurrence-index row count — the reduction ratio is REPORTED, never assumed (expectation 30–50%, NORM class, validated per estate).

- AC-A1.c · A stratified sample (100 hours, DEFAULT) is human-audited for dedup false positives before full-corpus rollout on any estate; false-positive rate ≤ 0.5% of deduped spans (DEFAULT), else dedup narrows to advertising/jingle content classes only. This audit rides the existing de-risking rung-1 measurement — same sample discipline, one new column; verdicts uncurated per D-7.

- AC-A1.d · News-classified programme blocks (where schedule metadata identifies them) are dedup-exempt by default — near-identical bulletins with material deltas (updated figures, corrected names) are the named false-positive class; the exemption’s cost is visible in the AC-A1.b report.

# **Part III — A2 · The occurrence index**

## **§3.1 Mandate and promise**

**Built to **record, as first-class qualified intelligence, every repeat airing of identified content — when, on which station/source, from which canonical instance. **Why this matters: **a complete when/where log of repeated spans (advertising airings above all) is a sellable intelligence artifact that falls out of A1 at near-zero marginal cost, and the opportunity-brief layer cannot propose what the registry cannot see. Service trace: S4.receive + S2.commission (census dimension). 

## **§3.2 Technical requirements**

- **R-A2.1 **Occurrence rows are qualified units: each occurrence lands as a NormalizedUnit (modality per source, locator carrying {canonical_id, station, timestamp, batch lineage}) — NOT a side-table outside the unit grammar. The census counts them; briefs may cite them; the trace resolves them. Zero new contracts: the existing unit shape carries it per MC-E1 α.

- **R-A2.2 **license_class: occurrence intelligence derives from the estate; rows carry the connector’s license_class with the MC-E4 α default (internal_only, fail-closed) — S4 egress only on explicit rights posture.

- **R-A2.3 **The canonical→occurrence relation is walkable in the trace: an occurrence cites its canonical unit’s perception receipts; no occurrence asserts content it did not itself carry — the honesty grammar applies (an occurrence proves airing, not content identity beyond the fingerprint match class, which is stated).

## **§3.3 Acceptance criteria**

- AC-A2.a · Census exposes occurrence-index dimensions (counts by canonical, by station/source, by period) as observed vocabulary — data-blind discipline: dimensions emerge from the estate, never pre-seeded.

- AC-A2.b · A brief citing occurrence data grounds every number in registry reads (existing OB gates); an S4 artifact of occurrence data refuses egress under default license_class (existing MC-E4 gate; one new cell proving it for this artifact class).

# **Part IV — A3 · The coverage-gap refusal class**

## **§4.1 Mandate and promise**

**Built to **distinguish “the evidence does not exist YET” from “the evidence exists and is insufficient” — and to convert the former into a filed extraction candidate automatically. **Why this matters: **the refusal grammar currently carries two classes (evidential refusal; fault-never-dressed-as-refusal). A gap class completes it: an un-extracted region of the estate is neither weak evidence nor an error, and presenting it as either misleads the asker and hides demand signal from targeting. Service trace: S1.call (refusal semantics intact for integrating applications). This is an EXTENSION of the existing refusal envelope — one new class in the same grammar; a parallel taxonomy is prohibited (§1.2 discipline).

## **§4.2 Technical and behavioral requirements**

- **R-A3.1 **Every non-answer classifies as exactly one of: coverage gap · evidential refusal · system fault. The three are distinct response types in the wire contract — not copy variations. Contract impact is expected ADDITIVE (new class beside existing envelope, v-next by additive versioning); any byte-contact with a frozen envelope is Tier-1 per standing rule.

- **R-A3.2 Coverage gap behavior: **the response names the gap in the asker’s terms (estate region, period, source class — from registry vocabulary, observed not invented), carries the un-extracted region identifiers internally, and FILES the gap as an extraction candidate visible to Targeta’s planning inputs. Filing is demand signal, not authorization: extraction of filed gaps happens only under normally-governed objectives — the eligibility wall stands; learning/demand may reorder, never widen.

- **R-A3.3 Fault discipline preserved verbatim: **a retrieval timeout or downstream error is NEVER surfaced as any refusal class — a timeout dressed as scepticism corrupts every genuine refusal. Existing rule, restated because A3 adds a class adjacent to it.

- **R-A3.4 **No confidence language crosses the boundary: gap responses state absence and (where a plan exists) status — they never estimate what absent evidence “would show.” Solva’s assertion discipline applies to gaps exactly as to answers.

## **§4.3 Acceptance criteria**

- AC-A3.a · Three response types proven distinct at the wire (schema cells); fault-injection proves a forced timeout yields fault, never a refusal class (existing AF cells extended).

- AC-A3.b · A coverage-gap response produces an observable filed candidate in the targeting inputs; a second identical ask cites the same filed candidate (no duplicate filing).

- AC-A3.c · Ask Console (reference app) renders the three classes distinctly per UI-Spec binding-copy discipline; refusal copy is grammar-bound, not free text.

# **Part V — A4 · Per-batch quarantine with systemic-halt threshold**

## **§5.1 Mandate and promise**

**Built to **make fail-closed operationally survivable at corpus scale. **Why this matters: **fail-closed at job scope means one anomalous batch kills a multi-day run — which in practice pressures operators to weaken policy: the failure mode that destroys governance systems from the inside. Per-batch quarantine keeps the promise absolute per batch while the run survives; a threshold distinguishes bad batches from a systemically broken run. Service trace: S3.prove (quarantine events are ledgered, walkable) + S2.commission.

## **§5.2 Technical requirements**

- **R-A4.1 **A governance failure on one ingestion batch (purpose validation, de-identification fault, policy violation) quarantines THAT batch — ledger row, receipt marked, batch excluded from downstream — and the run continues.

- **R-A4.2 **Run-level halt triggers when the quarantine rate exceeds the systemic threshold (2% DEFAULT, per-instance seam value — Part VII F2, set at S2.onboard, dual-control on change per MC-E3 α). Halt is HALT: operator notification, no silent resume.

- **R-A4.3 **Quarantined batches are re-processable after remediation to a new output version with new receipts — never in-place mutation (existing immutability doctrine; restated as the quarantine exit path).

## **§5.3 Acceptance criteria**

- AC-A4.a · Synthetic policy-violation batch injected mid-run → quarantined, run completes, ledger row present.

- AC-A4.b · Synthetic systemic fault (>threshold) → run halts, notification observable.

- AC-A4.c · Quarantine→remediate→re-process walk visible end-to-end in the trace.

# **Part VI — A5 · Precomputed evidence partitions + session working set**

## **§6.1 Mandate and promise**

**Built to **guarantee that interactive surfaces never pay — or make the asker pay — extraction-class latency, and that governance never manifests as the product declining to work. **Why this matters: **an interactive surface that queries the estate at request time compounds two failures: seconds-to-minutes latency, and retrieval slowness triggering refusal paths — so the honesty grammar surfaces as unreliability. Precomputation is already the platform’s informal pattern (briefs and answers compose from qualified material); A5 formalizes it as an enforceable serving discipline for every interactive surface, first-party or integrating. Service trace: S1.call (the envelope the integrating application inherits).

## **§6.2 Technical requirements**

- **R-A5.1 Partitions. **Evidence consumed by interactive surfaces is precomputed into versioned, columnar, memory-mappable partitions keyed on the dimensions the surface actually queries (keys are per-surface configuration; extension only via schema versioning). A request is partition reads plus arithmetic.

- **R-A5.2 The estate-query prohibition (rule ES-1). **Interactive-surface code MUST NOT query the raw or qualified estate at request time. Enforced at rung 1: a CI import/route check proves no estate-query client is reachable from interactive-surface code. Exceptions exist only by recorded Owner-tier ruling naming the latency consequence.

- **R-A5.3 Refresh discipline. **Partition refresh is a cold-path batch job; the previous version serves until the new version is atomically promoted; promotion is ledgered.

- **R-A5.4 Session working set. **Iterative surfaces (adjust→re-ask) reuse session-loaded partitions and intermediate aggregates; only deltas recompute. Cache entries bind to partition version — promotion invalidates dependents, so one cited result NEVER mixes evidence versions. Cache stores partition references + derived arithmetic, never re-materialized raw — no ungoverned data path; cache reads inherit the session’s validated purpose.

- **R-A5.5 Lineage. **Every partition version records the receipt set it was built from; every answer cites partition versions; the chain number→partition→receipts→operations is mechanically walkable with zero additional retrieval at request time (the citation IS the identifier the request touched).

## **§6.3 Acceptance criteria**

- AC-A5.a · Partition schema + refresh job exist before any interactive feature builds against live data (design-gate discipline).

- AC-A5.b · Latency telemetry per interactive request from first internal use; budgets are DEFAULT class (p95 ≤ 1.5s first-ask; re-ask p95 ≤ 40% of first-ask) revised only by measured pilot data.

- AC-A5.c · Version-skew cell proves a session cannot cite two partition versions in one output; ES-1 CI check green; load test at 10× expected concurrency passes budget before any external demonstration.

# **Part VII — Operating Values v1.1 folds (ride G-3)**

- **F1 · Per-language model-serving accuracy gates: **any serving-efficiency change to a registered model (quantization or successor techniques) is gated per language on held-out sets — ASR WER degradation ≤ 1.0pp absolute per language; tagging/classification F1 degradation ≤ 1.5 points (both NORM). A model may serve efficient for passing languages and full-precision for failing ones — the gate is per-language. Perception (ASR) has NO efficiency valve: it never serves degraded without its per-language gate; text-tagging models MAY carry a first-run-only valve because their inputs are cheap to re-process, perception is not. Serving precision per model per language is queryable configuration, logged in the model registry with measured deltas.

- **F2 · Quarantine systemic-halt threshold **joins the governance seam values (§6 family): 2% DEFAULT, per-instance, set at S2.onboard, changes under dual-control where §6 requires. The seam-value set becomes six; MC-E3 α initial-set/ledger semantics apply unchanged.

- **F3 · Run-telemetry rule: **every perception/extraction run emits throughput telemetry (utilization, items/hour) from its first execution — a run without telemetry is a failed run regardless of output. Cost-per-hour columns activate only when compute is metered; the telemetry discipline is posture-independent.

# **Part VIII — Behavioral rules adopted (binding)**

- **ES-1 **· No interactive surface queries the estate at request time (R-A5.2). Rung-1 enforced.

- **ES-2 **· Every non-answer classifies into exactly one refusal-grammar class; an unclassifiable non-answer is a bug, triaged as such.

- **ES-3 **· No perception run without telemetry (F3).

- **ES-4 **· Measure before optimizing — restated from standing doctrine: efficiency machinery (buffering, quantization execution) builds only against a measured shortfall; a measured shortfall makes it mandatory, not discretionary.

- **ES-5 **· Batches immutable, enrich-once per model version; corrections are new versions with new receipts — restated from standing immutability doctrine as the ingestion-side reading.

# **Part IX — Execution model**

**Sequencing (ruling-authority lane, no schedule implied): **this specification lands on-disk now (doc-only). Its build phases dispatch AFTER the already-sequenced G-2 (Registry maintenance) and G-3 (Operating Values v1.1 — which absorbs Part VII) close, so the Registry and Op-Values fold once, not twice. Expected phase shape at dispatch: Phase EAB-1 = A1+A2 (ingestion side, one seam); Phase EAB-2 = A3+A4 (refusal grammar + quarantine); Phase EAB-3 = A5 (serving pattern; may ride a first-party surface as its proving consumer). Split/merge is builder Tier-3 at Stage A, disclosed. Standard loop per phase: Stage A → verbatim Tier-1 relay → rulings → atomic execution → close.

**Pre-named Tier-1 surfaces: **refusal-envelope contract contact (A3; expect additive v-next, Tier-1 if any frozen byte is touched) · occurrence-unit locator vocabulary (A2; expect zero-mutation per MC-E1 α, Tier-1 if not) · the F2 seam-value admission (touches §6 family definition) · partition-schema contract class (A5; new artifact class → registered, additive) · any Targeta-input contact beyond the named cap seat (§1.2; expect none).

**D7 fences: **no scheduler beside Targeta · no batch schema in contracts/ · no quantization/buffering execution · no commercial premises · no real estate data · no new perception models (Silero/whisper tiers stand per Op. Values §1). R4 rows per §14 supplement pattern; D-10 self-audit rides every phase; verdicts uncurated per D-7.

Syni.ai · EAB Tier-1 Adoption Specification v1.0 · 2026-07-14 · Companion to: Registry Doctrine v1.0 · Operating Values v1.0 · Extraction De-Risking Spec v1 · MC-E1..E6 rulings

<!-- style-map (zero-token contribution; python-docx body-XML walker, pandoc unavailable)
  Docx source: /tmp/eab_tier1_adoption_spec.docx (SHA-256: 93a72c9f5f62356b17c8063eb601dcb049e10859e005e03f626df0a4790aa198)
  Conversion path: python-docx v1.2.0 iterchildren(body.iterchildren()) preserving paragraph + table order (Operating Values v1.0 precedent, 2026-07-11).
  Element mapping:
    Heading 1..6            → ATX '#'..'######'
    Normal paragraph        → plain markdown text
    List Paragraph (numId>0)→ '  '*ilvl + '- ' + text (bullet default; numbered lists render as bullets under this walker)
    Bold run                → **text**
    Italic run              → *text*
    Bold+Italic run         → ***text***
    Table                   → GFM pipe table (single-line-per-cell; internal pipes escaped '\|', newlines flattened to spaces)
    Section properties      → skipped (zero-token; w:sectPr carries no body text)
    Runs                    → concatenated within their parent paragraph, preserving text order
  Verbatim discipline:
    - No smart-quote conversion.
    - No reflow / line-wrap.
    - Token identity checked whitespace-normalized (source .docx w:t stream vs landed .md text stream); token-identity diff empty.
-->
