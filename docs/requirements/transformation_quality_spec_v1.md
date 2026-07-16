**AKKI · GOVERNED ARTIFACT · ADOPTION SPECIFICATION**

**Transformation Quality & Output Acceptance Specification v1.0**

The quality matrix across all output formats, model acceptance criteria (MOAC), production QA machinery, and three-stage coverage · 2026-07-15

***Audience and status:** engineering and governance readers; no prior context assumed — §2 defines every named system. For adoption decision; Owner-ruled decisions from the transformation-quality review of 2026-07-15 are carried verbatim and marked RULED. Normative language: MUST / SHOULD / MAY. Evidence classes on values: FACT (verifiable) / NORM (convention-anchored placement in a defensible range) / DEFAULT (operating constant, revisable via the dual-control config path without reopening this document).*

**§1 — Purpose and the decision requested**

Akki’s transformation layer — the machinery that converts an organization’s raw data estate into transcripts, structured records, tags, derived artifacts, and trained models — is a principal value proposition of the platform. Until this specification, its quality assurance was concentrated on one input format (speech) and one endpoint verdict (unit qualification), leaving every intermediate transformation and every non-speech format under-instrumented, and leaving the platform’s flagship output — models the customer owns — with no acceptance bar at all.

Decision requested: adopt the class-keyed Quality Matrix (§4–§5), the Model Output Acceptance Criteria (§6), the production QA machinery (§7), the three-stage coverage frame (§8), and behavioral rules TQ-1..TQ-6 (§9), per the execution model (§11).

**§2 — Context: the named systems (normative for this document)**

-   **Akki** is a governed intelligence platform deployed as a single-tenant instance inside a customer organization’s perimeter. It is organization-agnostic by ruling: the estate’s contents — never the customer’s identity — decide which capabilities do work. Instance \#1 (a broadcast estate) is one instantiation, not a development metric (RULED, 2026-07-15).

-   **The pipeline, three stages:** Extraction (perception and connectors read raw material — audio, video, documents, databases), Transformation (extracted material becomes qualified units, tags, structures, and trained models), Production (units compose into deliverables: answers, briefs, datasets, artifacts, deliverable models).

-   **NormalizedUnit** (contract five_rings@v0, frozen): the atomic intelligence unit — every extracted fact with who/what/when/where, provenance, and a defensibility class. All transformation outputs that assert content land as units or reference them.

-   **The census:** the platform’s first act on any estate — measuring what it actually holds, by composition. The census is this specification’s activation mechanism: it determines which output classes are live for an instance.

-   **Standing measurement events (already ruled, docs/requirements/):** rung-1 domain-transfer measurement (models run on a small real sample; first quality numbers) → targeted adaptation → BM-V (the uncurated human-baseline verdict: ≥90% qualification correctness, zero fabricated attributions) → BM-C (drift watch: \>3pp degradation over two samples alerts). This specification adds columns to these events; it creates no new measurement era (RULED).

-   **The Critic Seam** (docs/requirements/critic_seam_spec_v1.md): the three-tier QA layer for build-loop worker output — deterministic checks, an independent critic model, human calibration sampling. §7 of this document extends the same architecture to production output; the Critic Seam document gains a one-line Part B pointer to §7 at landing.

-   **Doctrine rules cited:** D-2 (rules pay rent: every gate names its promise and cost, or retires) · D-7 (verdicts never curated) · MC-E4 α (license_class defaults internal_only, fail-closed) · Operating Values §2 C1–C4 (model acquisition criteria — §6 is their output-side twin).

**§3 — The problem, from the record**

-   Quality instruments existed for speech extraction (WER/DER thresholds, a five-surface de-risking table) and for the endpoint (BM-V) — and for nothing between. Speaker naming, de-identification recall, voice-activity loss, language routing, tabular mapping fidelity, tagging accuracy, and every non-speech format were function-built and quality-blind.

-   Trained models — sold as “models you own” — had acquisition criteria (which model may enter) but zero acceptance criteria (whether a model the platform produces is good enough to ship).

-   The de-risking spec’s weak surfaces were all speech: instance \#1’s estate silently promoted to a platform assumption. Caught by the Owner; ruled: speech depth stands, every other class upgrades to it (§5), and no instance is a development metric (TQ-5).

-   Endpoint-only measurement means a failed unit starts a manual archaeology: BM-V sees the composite and cannot say which of six upstream transformations broke. The matrix gives every stage its own instrument, so failures read off a dashboard.

> ***Counter-check.** The standing objection, raised by the Owner and answered structurally: is this over-building in pursuit of quality? Partially conceded at review — the original draft researched full weak-surface depth for formats no estate has activated. The ruled trim: dormant classes carry row definitions and instruments only (one line each); full depth builds at the moment a census activates the class (TQ-1). Paper is cheap; speculative research is not; machinery runs only when production runs.*

**§4 — The Quality Matrix: structure**

**The matrix is keyed by OUTPUT CLASS, never by media type, customer, or instance.** Every class carries the same four dimensions, instrumented the same sector-agnostic way: a stratified human-verified sample drawn from census composition, uncurated (D-7), thresholds evidence-classed, drift-watched BM-C-style.

|                              |                                                                                                                                                                                                                         |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Dimension**                | **Definition**                                                                                                                                                                                                          |
| Correctness                  | Is the output right — measured per class in its native unit (WER for speech transcripts, field accuracy for OCR/mapping, F1 for tags, delta-vs-base for models).                                                        |
| Loss                         | What the transformation silently dropped — the unrecoverable defect class (speech discarded by VAD, rows dropped in mapping, spans missed in perception). Bounded tightest, because loss cannot be repaired downstream. |
| Precision / over-application | What it wrongly included or over-applied (false dedup merges, over-redaction in de-identification, spurious tags).                                                                                                      |
| Attribution fidelity         | Is the who/where/when preserved through the transformation (speaker naming, page/region provenance, source-row lineage).                                                                                                |

**Activation rule (TQ-1, RULED):** the census activates matrix rows. A class with no material in the estate stays dormant — registered, instrumented on paper, zero build. A class the census observes activates: its checkpoints join the instance’s rung-1 sample and its thresholds bind before that class enters production mining.

**§5 — Class specifications**

**§5.1 Perception outputs — speech (ACTIVE on instance \#1; full depth, carried as ruled)**

-   Correctness: WER ≤ 15% clean / ≤ 25% degraded-telephone-archival / ≤ 30% code-switched (NORM, standing from Operating Values §3); DER ≤ 20% multi-speaker.

-   **Loss — NEW:** VAD false-negative ≤ 1% speech-loss (DEFAULT) on a stratified human-checked sample deliberately weighted to quiet speakers, vernacular, and degraded strata — measured before full-corpus rollout; the A1 restructuring audit gains this column.

-   **Precision — standing:** dedup false-positive ≤ 0.5% of deduped spans (adopted, EAB Tier-1); de-identification over-redaction rate reported (utility loss, no gate until a claim depends on it).

-   **Attribution — NEW:** speaker-naming correctness enters BM-V as its own scored column (the “who” verified separately from content); language-ID routing accuracy ≥ 98% (DEFAULT) on the rung-1 sample, misroutes logged with cascade tags so downstream WER anomalies trace to routing.

-   **Custody row — NEW, incident-class:** de-identification recall ≥ 99% (NORM) on a seeded-PII sample per language — seeded set includes local names, ID formats, phone formats (the platform’s weak-surface logic applied to its own shield). A recall miss is a governance event, not a quality score (§7 QA-7).

**§5.2 Perception outputs — documents/OCR, image, video (DORMANT: row definitions + instruments only, per TQ-1)**

-   Documents/OCR: correctness = character/field accuracy per stratum (print, degraded scan, handwriting, mixed-language); loss = page/region drop rate; attribution = page/region locator fidelity. Instrument: stratified human-verified sample at activation. Thresholds set at activation from that class’s literature — not invented now.

-   Image/video frame perception: correctness = description/classification accuracy on sampled frames; loss = segment drop; attribution = timestamp/frame lineage. Same instrument; values at activation.

**§5.3 Structured-mapping outputs (ACTIVE — multi-instance connector live)**

-   Per-connector, N-row human-verified mapping sample at onboarding (N = 50 DEFAULT) proving field→ring mapping before census publish: correctness = field accuracy; loss = row/field drop; attribution = primary-key + source-table lineage intact. S2.onboard gains this step; connector fixtures gain the gate.

**§5.4 Analytic outputs — entity extraction, classification, tagging, summarization**

-   Absolute per-class baselines on the per-language/per-domain evaluation sets (the sets already mandated by the serving-gates fold) — reported at rung-1; gates bind per class only when a product claim depends on that class (D-2).

-   Summarization carries a faithfulness check: no claim in a summary absent from its sources — the anti-fabrication gate’s semantic sibling, sample-verified, never inline.

**§5.5 Derived intelligence artifacts — briefs, claim graphs, datasets, occurrence indexes, partitions**

-   Grounding gates already bind numbers verbatim (standing). The matrix adds completeness sampling: does the artifact contain what the corpus supports — a measured miss rate, not only no-fabrication. Datasets re-verify the k ≥ 20 aggregation floor per release; license_class inheritance per MC-E4 α attested per artifact.

**§5.6 Retrieval/index outputs (DORMANT until the embedding surface dispatches)**

-   Row registered now: recall@k on a sampled query set, per language. Values and build at that phase — no gate before the surface exists.

> ***Counter-check.** Threshold honesty: several values above are DEFAULT-class placements, not derivations — stated as such deliberately. Inventing precise thresholds for unmeasured classes would be fabrication; the evidence-class system exists exactly so a DEFAULT can ship, bind behavior, and be revised from the first measured sample without reopening this document.*

**§6 — MOAC: Model Output Acceptance Criteria (RULED — the output-side twin of acquisition criteria C1–C4)**

A model the platform trains — adapter or fine-tune — is accepted into the registry, deployed into extraction, or delivered to a customer ONLY when all six hold:

-   **M-a · Improvement:** beats its base model on the target stratum by ≥ 5% relative (C4 reused as an output gate).

-   **M-b · No collateral regression:** no degradation beyond 1pp absolute (DEFAULT) on non-target strata — the fine-tune didn’t buy Swahili by breaking English.

-   **M-c · Uncurated evaluation:** held-out, census-stratified sets; D-7 applies to model verdicts exactly as to BM-V.

-   **M-d · Complete lineage:** training-data unit set recorded; license_class inheritance binding — a model trained on internal_only data carries internal_only egress restrictions; base checksum + adapter version pinned in the model registry.

-   **M-e · Calibration:** confidence calibration measured and versioned before the model’s scores feed any downstream gate.

-   **M-f · The evaluation card:** customer-deliverable models ship with their measured numbers — whatever they are. The honesty grammar applied to the flagship product.

> ***Counter-check.** Failure mode: MOAC as launch-blocker theater — six criteria misread as six review meetings. All six are artifacts of the training run itself (eval outputs, lineage records, registry fields); acceptance is a checklist over files that already exist, executed as cells. A training run that cannot produce them wasn’t a governed training run.*

**§7 — Production QA machinery (the Critic Seam’s Part B — same three tiers, second domain)**

The Critic Seam guards what workers produce; this section applies the identical architecture to what the pipeline produces. One QA design, two production domains, one calibration discipline.

-   **Tier 1 — deterministic, always-on, in-pipeline (rung 1):** schema completeness (incomplete units/facts reject at write — standing pattern); referential integrity (every locator resolves to its source object); grounding verbatim (standing); plus statistical tripwires per batch — empty-output rates, distribution shifts vs the census baseline, confidence-profile anomalies. Zero serving-path cost; runs where the pipeline runs.

-   **Tier 2 — the production critic, sampled, asynchronous:** a critic model reviews a SAMPLE of outputs per active class, continuously — transcript spot-agreement, tag/summary faithfulness against sources, mapping spot-checks, de-identification residue scan. Sampling rates are DEFAULT-class per class (initial: 1% of production volume or 100 items/class/period, whichever is smaller); findings carry routing leads (which stratum, which model, which lever). Never blocks; emits findings and leads only.

-   **Tier 3 — human calibration:** the matrix’s stratified human samples (rung-1, BM-V, BM-C columns) double as the critic’s calibration — catch-rate and false-alarm rate per output class, versioned, staleness-marked; a stale critic’s findings render UNCALIBRATED. Seeded-defect audits per the Critic Seam §7 discipline: known-defective outputs planted in review samples, drawn across defect classes, never curated toward the critic’s strengths.

-   **QA-7 — the custody boundary (RULED):** quality of PROTECTION escalates as governance; quality of PRODUCT routes as findings. A de-identification recall breach, detected by any tier, is a governance failure: the affected batch quarantines fail-closed (the per-batch quarantine machinery, adopted). Utility-class findings (WER, F1, mapping fidelity) never block — detect-never-decide holds everywhere else.

-   **One calibration mechanism, three consumers:** fact-confidence calibration, the build-critic’s ledger, and the production-critic’s per-class ledger are the same versioned, staleness-marked form — three instances of one mechanism. A parallel calibration machine is a meta-spiral defect on sight.

> ***Counter-check.** Failure mode: the sampled critic misses systematic defects between samples. Answered by division of labor — Tier 1’s statistical tripwires are exhaustive (every batch) and cheap, catching distribution-level anomalies; Tier 2’s sampling catches instance-level quality; BM-C catches slow drift. A defect class that evades all three — systematic, distribution-neutral, drift-free — is by construction the class only Tier 3’s human samples find, which is why Tier 3 never fully decays.*

**§8 — Three-stage coverage (Extraction → Transformation → Production)**

|                |                                                                                                       |                                                                                                                                                                                     |
|----------------|-------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Stage**      | **Quality question**                                                                                  | **Instruments (this spec + standing)**                                                                                                                                              |
| Extraction     | Did we read the raw material right, and lose nothing we can’t recover?                                | Per-input-class weak surfaces + rung-1 checkpoints (speech full-depth standing; other classes per TQ-1 activation); VAD-loss bound; connector mapping samples; A1 dedup audit.      |
| Transformation | Is what we produced from it correct, complete, attributed — and are the models we trained acceptable? | The §4–§5 matrix per output class; MOAC (§6) for trained models; Tier-1 in-pipeline checks + Tier-2 sampled critic (§7).                                                            |
| Production     | Do deliverables carry only what the corpus supports, with rights and floors intact?                   | Grounding gates (standing) + completeness sampling; k≥20 per release; license inheritance attest; evaluation cards on deliverable models; BM-V as the uncurated composite endpoint. |

**BM-V’s role, restated to prevent drift:** the matrix explains failures per stage and gates per-class claims; BM-V remains the single uncurated composite verdict. Neither substitutes for the other.

**§9 — Behavioral rules (binding on adoption)**

-   **TQ-1 · Depth on activation.** Dormant classes carry row definitions + instruments only; full weak-surface depth builds when a census activates the class. Speculative depth for dormant formats is a D-2 defect.

-   **TQ-2 · New class, new row, at Stage A.** Any phase introducing a new transformation output class includes its matrix row (dimensions, instrument, thresholds or explicit at-activation deferral) in its Stage A — R4’s discipline extended to quality.

-   **TQ-3 · Measurement reuses events.** Matrix checkpoints ride rung-1, BM-V, and BM-C samples as added columns. Proposing a new measurement era is a finding.

-   **TQ-4 · Speech is never diluted; peers are upgraded.** The ruled speech thresholds stand verbatim; parity across formats is achieved upward.

-   **TQ-5 · No instance is a development metric.** Platform quality specification is class-keyed; instance estates instantiate rows. An instance-derived assumption entering platform canon is a reportable finding.

-   **TQ-6 · Verdicts uncurated, always.** Every sample in this document draws from measured census composition; engineering the inputs is legitimate; touching a verdict sample is D-7.

**§10 — Verification set**

|                                               |                  |                                                                             |
|-----------------------------------------------|------------------|-----------------------------------------------------------------------------|
| **Metric**                                    | **Source**       | **Target / class**                                                          |
| Per-class checkpoint results at rung-1        | §5 active rows   | Within thresholds or lever fires before that class enters production mining |
| VAD speech-loss rate                          | §5.1             | ≤ 1% DEFAULT on stratified sample                                           |
| De-id recall on seeded PII                    | §5.1 custody row | ≥ 99% NORM; miss = governance event                                         |
| Mapping-sample pass per connector             | §5.3             | 100% of onboarded connectors sampled before census publish                  |
| MOAC completeness per trained model           | §6               | 6/6 criteria as cells; no registry entry without them                       |
| Production-critic catch/false-alarm per class | §7 Tier 3        | Calibrated + within staleness window, or findings render UNCALIBRATED       |
| Matrix row coverage                           | TQ-2             | 100% of live output classes carry rows; gap = Q3-class finding              |

**§11 — Not adopted, and execution model**

-   **Rejected:** full-depth research for dormant classes (TQ-1) · any new measurement era (TQ-3) · QA veto over utility-class quality (QA-7 boundary) · per-instance quality specs (TQ-5) · a second calibration mechanism (§7).

-   **On landing (doc-only):** this document is canon for transformation quality. Three pointers land with it: Critic Seam spec gains a one-line Part B reference to §7 (v1.1 sibling, register-precedent pattern); the G-3 Operating Values v1.1 phase absorbs §5.1’s new values and §6 MOAC as its quality section, citing this document; the de-risking spec’s speech table is re-scoped by reference as the §5.1 instantiation — no rewrite, one pointer.

-   **Build entry:** Tier-1 in-pipeline checks and matrix cells ride the EAB phases and rung-1 events already sequenced; the production-critic sampling rides the critic-pass phase already specced. No schedule exists or is implied; nothing herein reorders anything dispatched.

Syni.ai · Transformation Quality & Output Acceptance Specification v1.0 · 2026-07-15 · Companion to: Operating Values v1.0 · Critic Seam Spec v1.0 · EAB Tier-1 Adoption Spec v1.1 · Extraction De-Risking Spec v1
