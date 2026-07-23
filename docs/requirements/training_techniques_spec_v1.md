**AKKI · GOVERNED ARTIFACT · REQUIREMENTS SPECIFICATION**

**Training & Optimization Techniques Specification v1.0**

The training-recipe seat · optimizer selection · ensemble critics · cascade offload · Owner-ratified · 2026-07-17

***Scope and reading guide:** this specification governs four technique areas in Akki's model-producing and quality-assurance paths. It is written for a reader with no prior context: §1 supplies the systems each requirement references. Adoption principle, Owner-ratified: a technique enters the platform only where proven use cases match the platform's targeted results, and every adoption decision is made on measured evidence from the platform's own material. Normative language: MUST / MUST NOT / MAY. Evidence classes on values: FACT (established, verifiable) · NORM (anchored in a defensible range) · DEFAULT (operating constant, revisable on evidence without reopening this document).*

**§1 — Referenced systems**

-   **Model training path:** Akki trains adapters (LoRA/PEFT) on registered open base models, using qualified, de-duplicated units from the customer estate. Trained models are accepted through MOAC — six criteria including improvement over base (M-a), no collateral regression (M-b), lineage completeness (M-d), and calibration (M-e) — defined in the Transformation Quality Specification v1.0 §6.

-   **P4 baseline harness:** the first real-material run of any extraction or training pipeline is instrumented by design — utilization, throughput, and quality deltas emitted from run one (EAB Tier-1 Adoption Spec v1.1, Part X).

-   **The Critic Seam:** the three-tier QA layer for worker output — deterministic checks, an independent critic model, human calibration with seeded-defect audits (Critic Seam Specification v1.0). QA-1: the layer detects and never decides.

-   **F3 run telemetry:** every run emits throughput telemetry; cost columns activate only when compute is metered.

-   **ES-4:** efficiency machinery builds only against a measured shortfall; a measured shortfall makes it mandatory.

-   **D-7:** verdicts are never curated — evaluation inputs may be engineered, evaluation samples may not.

**§2 — T-1 · The training-recipe seat**

**Purpose**

Every trained model must be reproducible and attributable to the exact configuration that produced it, and configuration must improve only on evidence. The recipe seat makes training configuration a governed, versioned object rather than code.

**Requirements**

-   **T-1.1 ·** All training configuration — optimizer and its parameters, learning-rate schedule, batch and epoch parameters, adapter rank and target modules — MUST live under training_params@v0, a sidecar configuration class with the same discipline as extraction_params@v0: versioned, ledgered, outside contracts/, no Parity contact.

-   **T-1.2 ·** The seat ships EMPTY. No default recipe exists until the first training run fills it through the §3 protocol.

-   **T-1.3 ·** Every trained model's registry entry MUST cite the recipe_version that trained it. MOAC M-d (lineage) extends by this field.

-   **T-1.4 ·** Recipe revisions are DEFAULT-class: no approval ceremony. Each revision MUST attach the measured comparison that justifies it and MUST write a ledger row. A revision without attached evidence is a defect.

-   **T-1.5 ·** Foundation methods (FACT, standing from Operating Values §1–§2): LoRA/PEFT adapters on registered open bases; training material drawn exclusively from de-duplicated, VAD-cleaned, qualified units; acceptance exclusively through MOAC on uncurated held-out sets.

**§3 — T-2 · Optimizer selection protocol**

**Purpose**

The optimizer is a recipe component with material effect on compute cost and model quality. Candidate optimizers — Muon is the first named candidate — are selected by measured comparison on the platform's own workload, because published optimizer results concentrate at transformer pretraining scale and the platform's workload is adapter fine-tuning.

**Requirements**

-   **T-2.1 Trigger:** the protocol executes at the first adapter training on real material, inside the P4-instrumented run.

-   **T-2.2 Shape:** one two-arm comparison — the baseline optimizer versus the candidate — with identical training data, identical base model, identical evaluation sets, and an identical compute budget cap, executed on the smallest stratum that yields a valid MOAC evaluation. The comparison's cost MUST be disclosed in the carrying phase's LoC/compute band.

-   **T-2.3 Measured outputs:** target-stratum improvement (the MOAC M-a metric) · non-target regression (M-b) · wall-clock and GPU-hours to convergence · calibration quality (M-e input). All four MUST be reported for both arms.

-   **T-2.4 Verdict rule:** quality parity on M-a and M-b is MANDATORY for a candidate to remain eligible. Compute-to-convergence is REPORTED. The adopt/reject decision is an Owner ruling made on the measured results; no adoption threshold exists in advance of the evidence. Verdict samples are uncurated per D-7.

-   **T-2.5 Outcome recording:** on adoption, the winning arm writes training_params@v0 v1 with the comparison attached (satisfying T-1.4). On rejection, the candidate is recorded as tested with its numbers. Either way the result is permanent record.

-   **T-2.6 Recurrence:** the same protocol governs every future optimizer or recipe-component candidate: two arms, identical conditions, parity mandatory, Owner-ruled on evidence.

**§4 — T-3 · Ensemble critics**

**Purpose**

Detection quality in the Critic Seam may require more than one reviewing instance. Ensembles are legitimate for detection and prohibited for decision: multiple reviewers may surface findings; no collection of models may hold decision authority on any platform surface. This boundary is permanent and follows from the platform's design (one walled learner; one reasoning faculty; QA-1).

**Requirements**

-   **T-3.1 Deployment order:** when Tier-3 seeded audits show single-critic catch-rate below the standing bar on any fall class across two consecutive audits, rubric and context repair MUST execute first. An ensemble MAY deploy only if the repaired critic still misses on a subsequent audit.

-   **T-3.2 Independence:** ensemble members MUST differ genuinely — a different base model, or a materially different context shape. Same-base, same-context replicas are prohibited: correlated reviewers share failure modes and add cost without detection gain (FACT, established ensemble-diversity results).

-   **T-3.3 Findings-only:** all ensemble output is findings, per QA-1. Voting, override, and critic-of-critic structures are prohibited.

-   **T-3.4 Disagreement:** disagreement between critics is itself a finding class (CRITIC-DISAGREE), routed to rulings like every finding class.

-   **T-3.5 Bounds:** N ≤ 3 members without an Owner ruling. Cost-per-review telemetry MUST be emitted per member.

-   **T-3.6 Rent:** the ensemble retires if its catch-rate gain over the single repaired critic is under 10pp (DEFAULT) after one full calibration cycle.

**§5 — T-4 · Local-cascade LLM offload**

**Purpose**

Where a metered LLM carries workload that cheaper local models could filter, a cascade — local model drafts, LLM handles only what the local model cannot — reduces spend. Cascades carry a documented failure mode: when too many items escalate, each escalated item pays twice and the cascade is net-negative. The platform already minimizes LLM load by construction (the rung ladder; record-derived facts are never re-asked of the LLM; the mechanical composition arm; the critic-succession seat), so a cascade builds only against demonstrated cost pressure.

**Requirements**

-   **T-4.1 Trigger:** cascade work MAY begin only when F3 telemetry, with cost columns active, shows LLM spend on a named seam exceeding a threshold the Owner sets at that time. No threshold is defined in advance of metered evidence.

-   **T-4.2 Pre-work:** before the trigger, no cascade scaffolding, draft-model acquisition, or routing machinery may be built (D7 fence). ES-4 governs: a measured shortfall makes the build mandatory; absent one, it never builds.

-   **T-4.3 Shape:** local model drafts → deterministic acceptance check → LLM invoked only on rejects. The acceptance check is rung-1 machinery, not a second model judgment.

-   **T-4.4 Kill metric:** the double-pay rate — the share of items incurring both local and LLM cost. The cascade MUST emit it from first run and MUST retire if escalation makes the cascade net-negative against the pre-cascade baseline.

**§6 — Registry and execution**

-   R4 registry rows for these requirements land only with their carrying phases: T-1 and T-2 with the first training phase; T-3 with a Critic Seam calibration phase; T-4 only if its trigger fires. Nothing lands from this specification alone.

-   This document is the drafting source for those phases' Stage As. It lands on-disk as requirements canon with the first carrying phase, or earlier on Owner word, via the standard doc-landing pattern (verbatim conversion, SHA reply, governance pointer).

Syni.ai · Training & Optimization Techniques Specification v1.0 · 2026-07-17 · Companion to: Operating Values v1.0 · Transformation Quality Specification v1.0 · Critic Seam Specification v1.0 · EAB Tier-1 Adoption Specification v1.1
