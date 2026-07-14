# **AKKI · GOVERNED ARTIFACT · OPERATING VALUES & MODEL DECISIONS**

## **Operating Values v1.0**

Requirements, thresholds, and tool/model decisions — defined now, correct-by-exception · 2026-07-11

*Every value below carries an evidence class per the Solva discipline — the assertion never exceeds its evidence: ***FACT ***(verifiable, cite freely) · ***NORM ***(literature/convention-anchored placement within a defensible range) · ***DEFAULT ***(operating constant, cheap to correct, revisable via dual-control config swap without reopening this document). Values revise only by Owner ruling except where marked DEFAULT. This document defines values and decisions; it mints no gates — enforcement belongs to the phases that consume each value.*

## **§1 — Model & tooling decisions (locked)**

| **Component** | **Decision** | **License** | **Rung** | **Role** | **Notes / fallback** |
| --- | --- | --- | --- | --- | --- |
| ASR · production base | whisper-large-v3 | MIT · FACT | 3 | Production extraction base; built-in LID serves language routing (no separate LID model) | Registry-pinned at deployment; CI tier stays whisper-tiny per 9.2a-E1 |
| ASR · adaptation | LoRA adapters via HF transformers + peft | Apache-2.0 · FACT | 3 | Per-stratum fine-tunes (Swahili, code-switch, accent, degraded audio) trained in-perimeter | Adapters, not full fine-tunes: 10–100× cheaper, per-stratum swappable, version additively in the model registry |
| ASR · benchmark-only | Meta MMS | CC-BY-NC · FACT | — | Rung-1 comparison baseline ONLY | NEVER production or fine-tune lineage — non-commercial license. See §10 amendment |
| Diarization | pyannote speaker-diarization | Open-weights · verify commercial terms at acquisition · FLAG | 3 | Production speaker attribution | If current license text fails commercial use: fall back to NeMo-class (Apache-2.0) |
| VAD | Silero VAD (as integrated) | MIT · FACT | 3 | Voice activity detection | No churn — integrated and sufficient |
| Inference runtime | faster-whisper (CTranslate2) | MIT · FACT | — | Serving layer; large-v3 in CT2 format within ≤40GB envelope with batch headroom | Already the integrated backend |
| Embeddings / entity resolution | multilingual-e5-class | MIT · FACT | 3 | Default for Mtafiti entity/similarity surfaces when that phase dispatches | Named now so no future Stage A reopens the category |
| Fluent synthesis | Sonnet via Shield (as built) | — | 4 | Answer fluency + briefs, mechanical fallback arms stand | Rung-3 owned text models: out until an estate-trained corpus exists — dependency, not deferral |

**Open by measurement, deliberately (the one non-decision): **which adapter strata are needed at all — rung-1 domain-transfer measurement determines whether bare large-v3 already clears §3 thresholds on some strata. Deciding this by fiat would be fabricating a measurement.

## **§2 — Production model selection criteria**

A model is eligible for the production registry iff all four hold — **FACT-class criteria, mechanical to check:**

- **C1 · License: **permits commercial use and derivative fine-tunes (Apache-2.0 / MIT / CC-BY class).

- **C2 · Coverage: **handles the target stratum’s language natively or via a licensed fine-tune path.

- **C3 · Envelope: **single-GPU inference ≤40GB VRAM on the deployment class.

- **C4 · Improvement bar: **beats the incumbent registry model on the stratum’s checkpoint by ≥5% relative (DEFAULT — below that, churn costs more than it buys).

Procedure: rung-1 measurement ranks candidates → highest eligible wins → registry bump with pinned provenance (checksum, license, origin).

## **§3 — De-risking working thresholds (NORM)**

Anchors: human transcription WER 4–12% on clean speech; published ASR on African-accented / low-resource speech 15–40% pre-adaptation. These gate remediation, not the product: at-or-below → stratum enters census-grade extraction; above → the stratum’s lever fires (adapter / augmentation) before production mining touches it.

| **Stratum** | **Working threshold** | **Lever on miss** |
| --- | --- | --- |
| Clean / studio speech | WER ≤ 15% | Adapter fine-tune on census-curated stratum corpus |
| Degraded / telephone / AM archival | WER ≤ 25% | Augmentation in training loop + era-stratified corpus |
| Code-switched segments (Sheng, SW–EN) | WER ≤ 30% | Code-switch adapter on census-curated CS corpus |
| Multi-speaker / call-in | DER ≤ 20% | Diarizer swap or overlap-aware recipe via registry |

## **§4 — BM-V PASS bar**

- **Qualification correctness ≥ 90% **— machine-qualified units in the post-census slice confirmed correct by the human baseline on attribution + content + class. **Class: NORM-anchored PRODUCT COMMITMENT **(inter-annotator agreement norms 85–95%); citable to clients once measured; the bar itself revises only by Owner ruling.

- **Zero fabricated attributions **in the slice — absolute. **Class: FACT **(derives from the honesty-grammar architecture; one invented attribution is an incident, not an error rate).

Below either clause → INVESTIGATE. P9-E5 bindings unchanged: verdict inside the phase, uncurated slice, no production mining until PASS.

## **§5 — BM-C drift threshold (DEFAULT)**

Alert at >3 percentage-point degradation from the BM-V baseline on any stratum, sustained across two consecutive periodic human samples — tight enough to catch drift, loose enough to ignore sampling noise.

## **§6 — Governance seam values (the five §3.14 config values · DEFAULT, dual-control swap)**

- **Deletion consequence classes: **class-C (irreversible, cross-slice) → dual-control always · class-B batch >1,000 units → Owner escalation · class-A (reversible, single-slice) → operator-level.

- **Rule-tightening delay window: **72 hours.

- **Objection escalation window: **7 days, then auto-annotate-and-proceed.

- **Suspension re-review: **30 days, ledgered.

- **Outer-gate manual-review threshold: **>10,000 units or >1GB per export artifact.

## **§7 — Buyer-commercial-tier requirements (S4 surface restoration · completes Q3-03)**

- Receipt verification without platform access — checksum + trace independently checkable (already built: OuterGateReceipt_v1). FACT.

- License terms machine-attached to every artifact — license_class from the v1 registry rides the receipt. FACT.

- **Aggregation floor: **no product exposes units traceable to a single non-public individual; k ≥ 20 for aggregated personal-adjacent data (NORM · conservative k-anonymity convention, Kenya-DPA-aligned).

- Revocation semantics fixed at sale: bought artifacts immutable; standing skills honor slice-freeze. FACT.

Pricing is excluded by design — instrumented practice per §3.14, genuinely emergent.

## **§8 — Org-context onboarding requirements (S2.onboard · completes Q3-02 specification)**

The surface, when dispatched, captures minimally — structured intake, versioned like everything else:

- Estate inventory: sources, systems, custodians.

- Organizational vocabulary: entities, brands, people-of-record — seeds Targeta targeting and Mtafiti entity resolution.

- Rights posture per source: what the organization may license onward — feeds license_class at ingest.

- DPO contact + the five §6 seam values, set per-instance here.

- Objective priorities — seeds the first opportunity-brief cycle.

## **§9 — PH-R2/R3/R4 acceptance criteria**

- **Data plane (PH-R2): **managed replicated DB · RPO ≤ 1h / RTO ≤ 4h (NORM) · ledger archival append-only to object storage, 7-year retention (NORM · audit-record convention, DPA-compatible) · quarterly restore drill (DEFAULT).

- **Domain + TLS (PH-R3): **TLS ≥ 1.2 + HSTS (FACT-class floor) · trace ids survive domain moves — receipt URLs stable as config.

- **LLM swap (PH-R4): **target shape per llm_swap_seam.md · cutover proven by the AF golden set: mechanical arm byte-identical, fluent arm re-validated through the grounding gates · zero call-site changes per BCR.

## **§10 — Amendment note: Registry Doctrine Part VII**

**The Part VII “existing art” column’s reading of Meta MMS is narrowed by §1 of this document: **MMS = rung-1 benchmark baseline only (CC-BY-NC); production and fine-tune lineage carry on whisper-large-v3 (MIT) and Apache-class checkpoints. The doctrine file remains byte-identical per Standing Rule v3; this note is the live reading.

## **§11 — Change discipline**

FACT rows revise only if the underlying fact changes (e.g., a license re-issue). NORM rows revise by Owner ruling with the new anchor stated. DEFAULT rows revise via the dual-control config-swap path without reopening this document; each swap ledgered. This document is consumed by: the de-risking sequence (§2–§4), 9.2b deployment (§1, §9), future S2.onboard and S4 phases (§7–§8), and BM-C operations (§5).

Syni.ai · Operating Values v1.0 · 2026-07-11 · Companion to: Registry Doctrine v1.0 · Extraction De-Risking Spec v1 · BCR v1.5

<!-- style-map
docx-style / feature       -> markdown construct
Paragraph P0 (banner, bold) -> `#` H1
Paragraph P1 (title, bold)  -> `##` H2
Paragraph "Heading 1"       -> `##` H2  (used for §1..§11)
Paragraph "List Paragraph"  -> `- ` unordered list item
Paragraph style None        -> plain paragraph
Run.bold=True               -> `**text**`
Run.italic=True             -> `*text*`
Run.bold and Run.italic     -> `***text***`
w:tbl                       -> GFM pipe table (`| ... |` rows + `| --- |` separator)
tool: python-docx 1.2.0 (pandoc unavailable in this environment); document body walked
      in native XML order to interleave paragraphs and tables faithfully.
Token identity: whitespace-normalized token stream from source .docx matches the
      stripped-markdown token stream of this file (see /tmp diff).
-->
