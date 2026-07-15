**AKKI · GOVERNED ARTIFACT · ADOPTION SPECIFICATION**

**The Critic Seam — Worker Quality Assurance Specification v1.0**

Record-verification checks, an independent critic pass, and human calibration for all build-loop worker output · 2026-07-15

***Audience and status:** engineering and governance readers; no prior context assumed — §2 defines every named system. For adoption decision. Origin: Owner-identified pattern from this build’s own correction history (§3); specified by the ruling authority. Normative language: MUST = mandatory for acceptance; SHOULD = mandatory unless a recorded exception is approved; MAY = permitted. Evidence classes on values: FACT (verifiable) / NORM (convention-anchored) / DEFAULT (operating constant, cheap to revise).*

**§1 — Purpose and the decision requested**

Every intelligent worker in this build — the builder agent that executes phases, any LLM worker the platform harnesses, and the ruling authority itself — produces output whose quality today is assured by one mechanism: the Owner reading it and catching errors by hand. This specification mechanizes the half of that catching which is mechanizable: verification of worker output against the on-disk record. It deliberately does not attempt the other half — reframing the problem, changing the product’s direction — which is the Owner’s seat and is named as a protected non-goal (§10).

Decision requested: adopt the three-tier layer (§5 deterministic record-verification · §6 the critic pass · §7 human calibration sampling), the behavioral rules QA-1..QA-6 (§8), and the verification metrics (§9), for incorporation into the build’s standing loop per the execution model (§11).

**§2 — Context: the named systems (normative for this document)**

**Akki** is a governed intelligence platform built through a dispatched, audited loop. The build’s standing machinery, all on-disk in the repository:

-   **The Registry** (docs/registry/, consolidating to v1): every platform function registered with its mandate (“built to…”), the promise it protects (“why this matters…”), its service trace, enforcement, cost, and owner. A machine-readable form (registry.yaml) is parser-derived from the human document and pinned to its source SHA.

-   **The Registry Doctrine** (docs/governance/registry_doctrine_v1.md): the binding behavioral rules of the build. Referenced throughout this spec: D-2 (rules pay rent), D-3 (the conflation test — every function traces to a named service), D-5 (natural language is never an enforcement medium), D-7 (no invented schedule or scope), D-10 (builder conduct: proposals self-audit before submission), D-11 (canon before ruling: no assertion from memory where the record exists on disk).

-   **The ruling loop:** work enters as an Owner dispatch → the builder lands a Stage A proposal with pre-tiered escalations → Owner-value escalations are relayed verbatim and ruled → atomic execution → a close report with gate results and a D-10 self-audit. Stage A proposals and close reports are the two artifact classes this layer reviews.

-   **The standing queries** (Q1 redundancy · Q2 orphans · Q3 gaps · Q4 unverified rules): executable checks over the Registry that emit findings reports — never actions. Retirements and fixes happen only by ruling. This findings-not-actions pattern is the constitutional precedent this layer extends to worker output.

-   **Targeta’s wall** (the platform’s learning engine): learning may improve ordering but can never widen or narrow what an objective may reach — the precedent that a subordinate intelligence detects and optimizes but never decides. The critic inherits this wall verbatim.

-   **Workers, in this document:** (a) the builder agent executing dispatched phases; (b) LLM workers the platform harnesses at runtime; (c) the ruling authority’s own drafts and rulings. All three are in scope — the correction history in §3 shows all three falling in the same classes.

**§3 — The problem, from the build’s own record**

This layer is not speculative: every check in §5–§6 mechanizes a catch the Owner actually made, by hand, during this build. The documented fall classes, named as they occurred:

-   **Memory-ruling (D-11’s origin).** The ruling authority asserted “SyniSense has no spaCy” and “the engine mandates are not in hand” — both false against the on-disk record, both caught by the Owner. The correction cost a full audit cycle and produced doctrine rule D-11.

-   **Re-derivation.** The ruling authority proposed “Bayesian aggregation and triangulation for Solva” as fresh advice — re-deriving the Owner’s own Solva specification (its Probability and Tension stages) from a partially-read document. Caught by the Owner in one line: the most expensive single error class in the session.

-   **Invented scope/schedule (D7).** A “deferred” work category invented without instruction; a sequencing-harness Stage A authored by the builder against an explicit D7 fence. Both caught by the Owner or surfaced under direct question.

-   **False status.** The outstanding-work register shipped claiming a phase’s close was never returned — while the close sat on disk, one day old (LT-1). A builder close claimed a test baseline that a later bisect proved false (self-caught, disclosed).

-   **Unclassed assertion.** Values and claims stated without their evidence class — corrected repeatedly until evidence-classing became standing practice.

**The mechanizable/non-mechanizable split, which fixes this layer’s boundary:** every catch above is a verification — the truth existed on disk and the worker diverged from it. Verifications mechanize. The Owner’s other interventions — “the product is rails, not a governed-intelligence tool,” “platform users are applications, not end-users,” “the law of reduction is the solution” — were frame changes: they rewrote canon rather than diverging from it. No layer that verifies against canon can catch a correction to canon. Frame authority is the Owner’s seat, permanently outside this layer’s scope (§10).

> ***Counter-check.** The obvious objection: the correction rate already fell to zero across recent phases under the behavioral disciplines alone — why build machinery for a solved problem? Because the current zero is carried by two expensive mechanisms: the Owner still reading everything, and discipline held in context windows that compaction is documented to destroy (twice this session). The layer converts a behavioral achievement into a structural property that survives context loss and scales past what one reader can review. If the measured catch-rate stays at zero as phases grow, the layer’s cost is a few cells per close — rent it can afford.*

**§4 — Design principles (each traces to a standing precedent)**

-   **Detect, never decide.** The layer emits findings; every consequence is a ruling. Precedent: Targeta’s wall; the standing queries. A QA layer with veto power over workers would be a governor nobody mandated.

-   **Canon is the oracle.** All Tier-1 verification resolves against the on-disk record — never against a summary, a context window, or another model’s recollection. Precedent: D-11, mechanized.

-   **Zero loop drag.** The layer adds no turns to the dispatch loop and never blocks atomic execution mid-flight: Tier-1 runs as cells at submission boundaries (Stage A landing, close landing); the critic runs asynchronously between turns; findings arrive with, not before, the artifacts they review. The one hard-gate exception is scoped in QA-2.

-   **Halving, not zeroing — stated honestly.** A critic sharing a worker’s blind spot misses what both cannot see. The layer’s claim is that it catches the record-verifiable half and measurably shrinks the residual; Tier-3 exists because the layer itself must be measured, not trusted.

-   **The critic is calibrated like a model, because it is one.** Catch-rate and false-alarm rate per worker class are versioned, measured numbers maintained by human sampling — the same calibration discipline the platform applies to extraction confidence.

-   **The layer pays rent.** Its own catch/false-alarm ledger is standing; per D-2, if it stops catching and starts noising, it shrinks or retires by ruling. No meta-layer above it, ever.

**§5 — Tier 1: deterministic record-verification (rung 1)**

Six check families, all mechanical, all resolving against the repository. They run on the two artifact classes of the loop — Stage A proposals and close reports — and on ruling-authority documents at landing time. Each check emits PASS or a finding row; findings are inputs to rulings except where QA-2 scopes a hard gate.

|                              |                                                                                                                                                                                                                                                   |                                                                                                                                 |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| **Check**                    | **Definition**                                                                                                                                                                                                                                    | **Mechanizes which catch**                                                                                                      |
| RV-1 citation-existence      | Every SHA, file path, ruling id, registry row id, and contract name cited in the artifact resolves to an existing on-disk object; cited SHAs match the object’s actual hash.                                                                      | Memory-ruling: “the document says X at SHA Y” becomes checkable; a citation to a nonexistent or mismatched object is a finding. |
| RV-2 scope-trace             | Every work item in the artifact traces to an authorizing instrument: a dispatch, a register row, a ruling, or R4’s own-phase rows. Untraceable items are D7 finding candidates.                                                                   | Invented scope: the sequencing-harness class of pre-work is flagged at submission, not discovered later.                        |
| RV-3 evidence-class presence | Assertions in classed sections (status claims, values, verdicts) carry their class (FACT/NORM/DEFAULT or fact/recalled/inferred); classed values match their class’s form (a FACT cites; a DEFAULT names its revision path).                      | Unclassed assertion: the repeated correction becomes a schema check.                                                            |
| RV-4 schema-completeness     | Stage As carry: band + derivation, pre-tiered escalations, R4 rows, D-10 self-audit table. Closes carry: gate roster with results, artifact SHAs, R4/negative attest, D-10 table. Missing sections reject the submission format (QA-2 hard gate). | Submission discipline generally; the D-10 table’s presence stops being voluntary.                                               |
| RV-5 status-truth            | Every status claim about an on-disk artifact (“no close returned,” “phase X open,” “file absent”) is cross-checked against the repository state at submission time. A claim contradicted by disk is a finding with the contradicting path cited.  | False status: the LT-1 error — a register claiming a close never returned while it sat on disk — is caught mechanically.        |
| RV-6 novelty collision       | Proposed function ids, promise ids, module names, and concept labels are matched (exact + normalized-token) against the Registry and mandate documents; collisions flag as re-derivation candidates for Tier-2 semantic confirmation.             | Re-derivation, first line of defense: cheap lexical tripwire before the expensive semantic check.                               |

**Acceptance criteria.** (a) All six families run as cells at both submission boundaries; a run without them is incomplete per QA-2. (b) Each check’s findings are two-file per the standing-queries pattern: mechanical findings separate from any ruled/archaeological state, cross-referenced, never duplicated. (c) The checks themselves register in the Registry with R4 rows (they are functions; they pay rent like all functions).

> ***Counter-check.** Failure mode: check theater — RV families passing trivially because artifacts are written to the letter of the schema while gaming its intent (e.g., citing real SHAs for irrelevant objects). Conceded as residual: Tier 1 verifies form and existence, not pertinence; pertinence is exactly Tier 2’s rubric. The two tiers are designed as a pair; adopting Tier 1 alone would buy the cheap half and advertise the whole.*

**§6 — Tier 2: the critic pass (rung 3/4)**

An independent model instance reviews each Stage A and close report against a fixed rubric, asynchronously, after landing. Its output is a findings report — classed, cited, never blocking, never editing.

**§6.1 The rubric — the Owner’s catch history, made standing**

-   **CR-1 anti-re-derivation:** does anything proposed here already exist in the record under any name? The critic receives the Registry (machine form) and the mandate documents’ section inventory as context, and answers semantically — the check that would have caught “Bayesian aggregation for Solva” against Solva’s own Probability stage.

-   **CR-2 anti-fabrication:** is any assertion stronger than its evidence class permits? Are recalled claims dressed as facts? Are values stated without a basis where one is owed?

-   **CR-3 conflation test (D-3):** does every proposed function trace to a named service sentence — and is the trace real rather than decorative?

-   **CR-4 scope semantics (D7):** beyond RV-2’s mechanical trace — does the work’s substance stay inside the dispatch’s intent? Sequencing invented under cover of execution; scope smuggled as “riders”?

-   **CR-5 enforcement honesty (D-5):** is any rule proposed whose only enforcement is prose? Is any gate claimed that no cell proves?

-   **CR-6 self-audit audit:** does the artifact’s D-10 table’s reasoning hold, or is it reflexive PASS-stamping?

**§6.2 Independence and harness rules**

-   **The critic never shares the worker’s conversation.** Its context is exactly: the artifact under review, the canon set (Registry machine form, doctrine, relevant mandates, the authorizing dispatch), and the rubric. Not the worker’s reasoning, drafts, or self-justification — a critic reading the worker’s rationale inherits the worker’s frame, which is the blind-spot-sharing failure this design exists to avoid.

-   **No self-review (QA-3):** the critic instance is never the instance that produced the artifact; where both are the same base model, independence is by context isolation, and Tier-3’s seeded audits measure whether that isolation suffices (§7).

-   **Ladder discipline:** the critic runs at the cheapest sufficient rung — initially the platform’s existing governed LLM path (rung 4 behind the Shield), one review per artifact (not per token); an owned rung-3 critic is the transformation-layer’s natural successor once training data (the findings ledger itself) accumulates. Cost per review is a standing metric (§9).

-   **Findings are evidence-classed themselves (QA-4):** a critic finding states what it checked, what it found, at what confidence class, with citations — the honesty grammar applies to the critic exactly as to every other producer.

> ***Counter-check.** Failure mode one: rubber-stamping — a critic that finds nothing is indistinguishable from a critic that looks at nothing. Answered structurally in §7: seeded-defect audits measure the catch-rate on known defects, so “found nothing” is only credible from a critic whose detection is measured. Failure mode two: noise — a critic rewarded for finding things drowns rulings in trivia. Answered by the false-alarm ledger (§9) and D-2: a critic whose findings are repeatedly ruled non-findings gets its rubric tightened or its scope shrunk, by ruling. Failure mode three: the infinite regress — who reviews the reviewer? Stopped by construction: the critic’s findings reports are subject to Tier-1 checks only (they must cite what they claim) plus Tier-3 human sampling; there is no critic-of-the-critic, and proposing one is a D-5-class meta-spiral finding.*

**§7 — Tier 3: human calibration sampling**

**The Owner’s reviewing role compresses; it does not disappear.** Three sampling instruments, all lightweight, all producing versioned numbers:

-   **Verdict sampling:** a fraction of critic findings and critic all-clears (DEFAULT: 20% of findings, 10% of all-clears; decays as measured reliability accumulates) is human-reviewed. Each sample scores the critic: true catch, false alarm, or miss-in-sample.

-   **Seeded-defect audits:** on a standing cadence (DEFAULT: one per five phases), a known defect of a documented fall class (§3) is deliberately planted in a review copy — never in a landing artifact — and the critic’s catch or miss is recorded. This is the only honest measure of a reviewer that mostly reports “clean”: detection proven on known positives. Verdict discipline applies — the seeded set is drawn across fall classes, never curated toward the critic’s strengths (D-7 applied to our own QA).

-   **The calibration ledger:** catch-rate and false-alarm rate per worker class and per rubric item, versioned like model calibration. The critic’s trustworthiness is thereafter a measured, citable number — and the sampling rate is a function of it, so human attention shrinks exactly as fast as the evidence says it may.

> ***Counter-check.** Failure mode: sampling fatigue — Tier 3 quietly stops, and the layer’s numbers freeze at their last measured values while its real performance drifts. Mitigation is mechanical: the calibration ledger carries a staleness field; a critic whose calibration is stale past its window (DEFAULT: 10 phases) has its findings marked UNCALIBRATED at render — the same honesty rule the platform applies to model confidence. A stale QA layer visibly says so.*

**§8 — Behavioral rules (binding on adoption)**

-   **QA-1 · Detect, never decide.** No finding blocks execution, edits an artifact, or gates a phase — every consequence is a ruling. One scoped exception: QA-2.

-   **QA-2 · The format gate.** RV-4 schema-completeness is the single hard gate: a Stage A or close missing its required sections (including the D-10 table) is returned for completion before it enters the loop — form, never substance. All other checks, Tier 1 and Tier 2, are findings-only.

-   **QA-3 · No self-review.** No worker critics its own output; critic independence is by context isolation per §6.2 and is itself measured by seeded audits.

-   **QA-4 · Findings carry the honesty grammar.** Every finding is evidence-classed and cited; an unclassed finding is itself a finding.

-   **QA-5 · The layer pays rent.** The catch/false-alarm ledger is standing; a layer that stops catching shrinks by ruling; a second QA layer above this one is a meta-spiral defect on sight.

-   **QA-6 · Frame authority is untouchable.** No check, rubric item, or critic finding may dispute an Owner ruling, a service sentence, or a frame decision. The layer verifies divergence FROM canon; it has no standing on changes TO canon.

**§9 — Verification set (the layer’s own dashboard)**

|                             |                                       |                                                                                                                                                       |
|-----------------------------|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Metric**                  | **Source**                            | **Target / default**                                                                                                                                  |
| Owner-catch count per phase | Close-report correction record        | Baseline: §3 history (several per phase early-build → zero last five). Target: stays zero as phase size grows — with the Owner reading less, not more |
| Worker self-catch count     | D-10 tables + disclosed findings      | Reported; rising self-catch with falling Owner-catch is the healthy signature                                                                         |
| Critic catch-rate (seeded)  | §7 seeded-defect audits               | ≥ 80% on seeded defects across fall classes (DEFAULT; revised on evidence)                                                                            |
| Critic false-alarm rate     | Ruling outcomes on findings           | ≤ 20% of findings ruled non-findings (DEFAULT); breach triggers rubric review                                                                         |
| Catch latency               | Finding timestamp vs artifact landing | Caught at submission boundary, not post-landing — reported per finding                                                                                |
| Cost per review             | Critic telemetry                      | Reported from first run; input to the rung-3 succession decision                                                                                      |
| Calibration staleness       | Calibration ledger                    | Within window (10 phases DEFAULT) or findings render UNCALIBRATED                                                                                     |

**§10 — What this layer is not (rejected on sight)**

-   **Not a governor.** It holds no mandate, asserts nothing about the estate, and gates nothing but format. Proposing veto authority for it is rejected in advance.

-   **Not the Owner’s replacement.** Frame changes — rewriting what the product is, what a service means, what the reduction is — are constitutionally outside a canon-verifying layer. The build’s three largest course-corrections were frame changes; this layer would have caught none of them, by design, and claims otherwise are the exact overclaim its CR-2 exists to flag.

-   **Not inline.** Nothing here adds a synchronous step to any serving path or a turn to the dispatch loop.

-   **Not a new meta-artifact class.** It reuses the standing machinery — queries-engine patterns, Registry rows, calibration-ledger form; its documents are ruling records and findings files in existing locations.

-   **Not a zero-residual claim.** The layer halves the residual, measurably, repeatedly. It does not promise perfection, and its own dashboard is built to show its misses.

**§11 — Execution model (no schedule exists or is implied)**

-   **On adoption:** this document lands as a governed artifact; QA-1..QA-6 bind behaviorally at once (they are disciplines, costing nothing).

-   **Tier 1:** the six RV families enter as cells riding the next test-bearing phases’ closes (the EAB phases are the natural carriers) — each family a small deterministic checker over repository state; R4 rows per the supplement pattern.

-   **Tier 2:** the critic pass enters as its own small phase through the standard loop (Stage A → rulings → execution → close) — harness, rubric encoding, findings format, Shield-path wiring. It reviews artifacts from its first run; its first calibration cycle begins immediately after.

-   **Tier 3:** begins with Tier 2’s first output; the calibration ledger is a document before it is ever a tool.

-   **Sequencing:** within the standing lane — after G-2/G-3 close, alongside or after the EAB phases at the ruling authority’s sequencing judgment; nothing herein reorders anything already dispatched.

Syni.ai · The Critic Seam v1.0 · 2026-07-15 · Companion to: Registry Doctrine v1.0 · EAB Tier-1 Adoption Spec v1.1 · Operating Values v1.0 · Standing Queries close
