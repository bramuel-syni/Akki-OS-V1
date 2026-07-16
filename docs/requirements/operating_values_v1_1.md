# **AKKI · GOVERNED ARTIFACT · OPERATING VALUES & MODEL DECISIONS**

## **Operating Values v1.1**

Sibling to v1.0 · Part VII absorption (F1/F2/F3) + conformance corrections (spaCy · diarization · Solva) + TQ §5.1 speech values by citation + TQ §6 MOAC by citation · 2026-07-15

*Every value below carries an evidence class per the Solva discipline — the assertion never exceeds its evidence: ***FACT*** (verifiable) · ***NORM*** (literature/convention-anchored placement within a defensible range) · ***DEFAULT*** (operating constant, cheap to correct, revisable via dual-control config swap without reopening this document). Values revise only by Owner ruling except where marked DEFAULT. This document defines values and decisions; it mints no gates — enforcement belongs to the phases that consume each value.*

---

## §Part A — Canonical body (v1.0 verbatim by reference)

The v1.0 body is canonical Part A: `docs/requirements/operating_values_v1.md` · SHA-256 `a6c4a455175ef37dc71362aea2e41b2ce406baaf9a1c77b3f0f1326e0aa608ee` · byte-identical on-disk per Standing Rule v3.

Every clause, row, and threshold in v1.0 §1–§11 remains binding under v1.1. This sibling adds:
- §1 amendments (spaCy NER row · diarization triple reconciliation) — B.1 + B.2a/b/c
- §6 amendment (sixth seam value) — A.F2
- §12 new subsection (Part VII absorption + Solva Bayesian seat + TQ absorption pointers) — A.F1 + A.F3 + B.3 + TQ §5.1 + TQ §6 MOAC
- §13 change discipline extension carried
- Ruling anchor: `docs/rulings/g3_operating_values_v1_1_2026-07-15.md`

---

## §1 (v1.0 §1 + v1.1 amendments)

**Retained verbatim from v1.0:** all 9 rows (ASR whisper-large-v3 · LoRA adapters · Meta MMS · Diarization pyannote · VAD Silero · faster-whisper runtime · multilingual-e5 embeddings · Sonnet via Shield · Open by measurement).

**v1.1 additions (Owner ruling `docs/rulings/g3_operating_values_v1_1_2026-07-15.md` · authorization: `outstanding_register_v1_amendment_2026-07-12.md:13` + `audits/deviation_audit_v1.md:14` + `audits/engine_conformance_v1.md:26`):**

| **Component** | **Decision** | **License** | **Rung** | **Role** | **Notes / evidence** |
|---|---|---|---|---|---|
| spaCy NER · fail-closed de-identification | `en_core_web_trf` (primary) / `en_core_web_sm` (fallback) | MIT / CC-BY-SA 4.0 · **FACT** | 2 | Fail-closed de-identification role · live in the Shield chokepoint (`backend/services/synisense/shield/deidentifier.py`) — spaCy-unloadable → `ServiceUnavailable` propagates → fluency_synthesizer routes to mechanical arm (AF-E2 amended boundary) | RECONNECTED at IF-1 close per `audits/deviation_audit_v1.md:14`; Registry v1.md line 419 attest cell `synisense.shield.fail_closed_deidentify_blocks_llm` (IF1-G2 · GREEN · live) |

**v1.1 diarization row reconciliation (v1.0 row preserved verbatim; reconciliation is metadata only):**
- **Silero VAD** — **FACT · live** (integration confirmed at `services/perception/gpu_execution/*`; MIT license verified · already integrated per v1.0 §1)
- **pyannote speaker-diarization** — **NORM · license-verify-at-acquisition FLAG retained** (v1.0 §1 verbatim preserved; open-weights; commercial-terms verification required at acquisition)
- **NeMo (Apache-2.0)** — **NORM · fallback** (v1.0 §1 fallback clause preserved verbatim if pyannote commercial terms fail)

## §6 (v1.0 §6 + §6.6 sixth seam value · Owner G3-E1 α)

**v1.0 §6 five seam values preserved verbatim.** V1.1 adds §6.6:

**§6.6 · Quarantine systemic-halt threshold (F2 · sixth seam value)** — **2% DEFAULT**, per-instance, set at S2.onboard per MC-E3 α initial-set/ledger semantics (unchanged); dual-control on change per §6 discipline. Model surface: `backend/services/multi_instance/onboard_context.py::SeamValues.quarantine_systemic_halt_threshold`. Authorization: `docs/requirements/eab_tier1_adoption_spec_v1.1.md §Part VII F2 line 159` + G-3 Owner ruling. Existing `instance_1` backfilled via `initial_set`-marked ledger row per MC-E3 α semantics. **Class: DEFAULT.**

## §12 (new subsection) — Serving discipline · Part VII absorption

**§12.F1 · Per-language model-serving accuracy gates** (per `docs/requirements/eab_tier1_adoption_spec_v1.1.md §Part VII F1 line 157`):
- **F1a** · ASR per-language WER degradation ≤ **1.0pp absolute** on held-out sets per language for any serving-efficiency change (quantization or successor). **Class: NORM.**
- **F1b** · Tagging/classification per-language F1 degradation ≤ **1.5 points** on held-out sets per language. **Class: NORM.**
- **F1c** · **Perception has NO efficiency valve** — ASR NEVER serves degraded without its per-language gate. Registry-pinned at deployment. **Class: FACT** (architectural absolute).
- **F1d** · Text-tagging MAY carry a first-run-only valve — inputs are cheap to re-process, perception is not. **Class: NORM.**
- Registry v1 citation: `synisense.contracts.frozen_31` · `perception.pinned_model_provenance` · `perception.execution_mode_telemetry` (§v0-body §3.a + §v0.5-supplement-body §S1).

**§12.F3 · Run-telemetry rule** (per `docs/requirements/eab_tier1_adoption_spec_v1.1.md §Part VII F3 line 161` + §Part VIII ES-3 line 169):
- Every perception/extraction run emits throughput telemetry (utilization, items/hour) from its first execution.
- A run without telemetry is a failed run regardless of output.
- Cost-per-hour columns dormant until compute is metered; the telemetry discipline is posture-independent.
- **Class: FACT** (behavioral absolute · matches ES-3 binding).
- Registry v1 citation: `perception.execution_mode_telemetry` (§v0-body §3.a) + `northena.ledger.append_only_gate` (§v0-body §3.b).

**§12.Solva-Bayesian-seat · Measurement-era weighting seat** (per `docs/audits/engine_conformance_v1.md:26` PARTIAL verdict):
- `extraction_params@v0.solva_weighting_method = "equal_weight"` — **DEFAULT**.
- Bayesian weighting is a **measurement-era seat**: dispatched on measured shortfall, not built ahead of measurement.
- Registry v1 citation: `solva.reasoning.probability_bayesian` (§v0-body §3.c PARTIAL row) + §Conformance-Evidence-Registry line `solva.compliance.prove_one_run`.
- **Class: DEFAULT.**

## §12 (continued) — Quality section · TQ absorption by citation (Owner scope-4 add · zero verbatim duplication)

**§12.TQ-§5.1 · Speech quality values (absorbed by citation into Op. Values v1.1 · canonical body lives in TQ spec):**
- **VAD false-negative ≤1% speech-loss** (per-language) — cite `docs/requirements/transformation_quality_spec_v1.md §5.1`. **Class: DEFAULT** (per TQ §5.1).
- **Language-ID routing accuracy ≥98%** — cite `docs/requirements/transformation_quality_spec_v1.md §5.1`. **Class: DEFAULT** (per TQ §5.1).
- **Speaker-naming correctness (BM-V column)** — cite `docs/requirements/transformation_quality_spec_v1.md §5.1`. **Class: NEW BM-V column** (per TQ §5.1 attribution row).
- **De-identification recall ≥99% (seeded-per-language custody row)** — cite `docs/requirements/transformation_quality_spec_v1.md §5.1`. **Class: NORM** (per TQ §5.1 custody row · governance event on miss per TQ QA-7).

**§12.TQ-§6 · Model Output Acceptance Criteria (M-a..M-f · absorbed by citation · canonical body lives in TQ spec):**
- **M-a · Improvement** ≥5% relative on target stratum — cite `docs/requirements/transformation_quality_spec_v1.md §6 M-a`.
- **M-b · No collateral regression** — ≤1pp absolute on non-target strata — cite `docs/requirements/transformation_quality_spec_v1.md §6 M-b`.
- **M-c · Uncurated evaluation** (held-out census-stratified · D-7) — cite `docs/requirements/transformation_quality_spec_v1.md §6 M-c`.
- **M-d · Complete lineage** (training-data unit set recorded · license_class inheritance binding · base+adapter checksum pinned) — cite `docs/requirements/transformation_quality_spec_v1.md §6 M-d`.
- **M-e · Calibration** (confidence calibration measured + versioned before feeding downstream gates) — cite `docs/requirements/transformation_quality_spec_v1.md §6 M-e`.
- **M-f · The evaluation card** (customer-deliverable models ship with measured numbers) — cite `docs/requirements/transformation_quality_spec_v1.md §6 M-f`.

**Absorption discipline (Owner-verbatim clause):** *"BY CITATION, NOT DUPLICATION"* — TQ spec is canonical body; v1.1 lands pointer lines only. Zero verbatim carriage.

## §13 · Change discipline (v1.0 §11 preserved · extension)

v1.0 §11 verbatim binding under v1.1. Extension: rows added under v1.1 carry evidence classes per Solva discipline; DEFAULT rows revise via dual-control config swap without reopening this document; each swap ledgered. This document is consumed by: the de-risking sequence (§2–§4 · unchanged), 9.2b deployment (§1 · §9 · unchanged), S2.onboard (§7–§8 + new §6.6 sixth seam value), BM-C operations (§5 · unchanged), and EAB-1/2/3 phases (§12 new — F1/F2/F3/Solva/TQ absorption).

Syni.ai · Operating Values v1.1 · 2026-07-15 · Sibling to Operating Values v1.0 · Companion to: Registry Doctrine v1.0 · Registry v1 · EAB Tier-1 Adoption Spec v1.1 · Transformation Quality & Output Acceptance Spec v1.0 · Critic Seam Spec v1.0/v1.1

═══════════════════════════════════════════════════════════════════

*End of Operating Values v1.1 sibling. v1.0 preserved byte-identical per Standing Rule v3. Zero verbatim duplication of TQ spec body (absorption by citation only). Governance stack §15 pointer amendment lands with this ruling. Standing Rule v3 · on-disk canonical.*
