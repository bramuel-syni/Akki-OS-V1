**AKKI · GOVERNED ARTIFACT · REQUIREMENTS SPECIFICATION**

**Conditioned Ideation Faculty (CIF) — Specification v1.0**

Governed ideation, self-learning, and frame metabolization across the Akki architecture · Owner-ratified · 2026-07-23

***Reading guide:** written for a reader with no prior context. §1 states the promise in user-experience terms; §2 states the system this faculty serves and the testing principle that governs everything in it; §3–§4 define referenced systems and vocabulary; §5–§9 are the mechanics; §10–§12 are the operative and quality parameters; §13–§14 enforce and execute. Normative language: MUST / MUST NOT / MAY. Values carry evidence classes FACT / NORM / DEFAULT; DEFAULT values revise on evidence at evaluation boundaries, never mid-cycle.*

**§1 — The promise**

Working with AI today places the whole quality burden on the human: catching errors, re-supplying lost context, watching good ideas vanish at session end, repeating the same corrections indefinitely. When the human goes quiet, quality degrades invisibly. CIF changes that experience in four ways:

-   **You stop repeating yourself.** A correction made once holds: the class of error is retired, not the instance. Human effort compounds instead of evaporating.

-   **Shown confidence can be trusted.** When the AI is sure, that confidence has visible footing; when it is guessing, it says so before reliance — not after harm.

-   **Ideas stop dying with the session.** Rejected, deferred, or half-explored ideas wait — alive, with what they need named — and return when their conditions arrive.

-   **Insights spread everywhere they apply.** A reframe made once rewrites everything the old thinking touched: a worldview is corrected in one strike instead of symptom-hunted for weeks.

**Delivered measure:** the human corrects less each cycle for the same or better output (QA-a). The claim held at adoption is “reduces repeat-class errors”; stronger claims are asserted only on measured cycles.

**§2 — The system, and the single-experiment principle**

**The system this faculty serves:** Akki is an operating system for how agentic workflows integrate with enterprise data estates, how enterprises monetize those estates, and how enterprises build their own models autonomously from them. The architecture is the invention. Its components are deliberately not novel: known gates, known engines, and known code structures, each with defined, tested success parameters.

**The single-experiment principle (binding on this specification and the build):** experimentation exists at one level only — the assembled system delivering the enterprise promise. Nothing below that level is experimental. Every mechanic is known and parameterizable: it deploys in force with its conditions of success strictly implemented and its quality measured, or its parameters are not yet defined — which is a specification gap to close, never a reason to run tentatively. No capability is gated on demonstration, observation, trial, or “seeing first.” Gates in this platform bind spend, quality of output, or claims — never existence or force. A proposal gating force on observation is a finding on sight.

CIF enters under this principle: its mechanics — recording what verdicts rest on, retaining ideas with conditions, re-evaluating on condition change, second-instance review, threshold monitoring — are proven realities. CIF is in force across the architecture on adoption. Every operation in every subsystem, from its first occurrence, executes under this specification. There is no phasing, no activation sequence, and no entry gate anywhere in this document.

**§3 — Referenced systems**

-   **The coach (origination port):** the human role — interchangeably teacher, auditor, informer — whose corrections strike the assumptions verdicts rest on, and who alone adopts new frames. Constitutionally load-bearing.

-   **Solva-pattern validation:** the platform’s reasoning discipline applied as validator — assertion boundary (claims only at their evidence class), load-bearing floors (a conclusion’s supporting set meets the bar), tension machinery (contradiction detection), refusal grammar (a refusal names its reason and what would satisfy it). Verdict evidence is never curated (D-7).

-   **The Critic Seam:** the standing QA layer for worker output; its rubric is compiled from the coach’s correction history. CIF’s checklist (§6, A5) extends that rubric to idea selection (CR-7 class).

-   **Independence rule:** a reviewing instance MUST differ genuinely from the reviewed — a different base model or a materially different context shape.

-   **F3 telemetry:** the platform’s per-run measurement stream; monitoring parameters bind to its named fields.

-   **Engine walls:** standing constitutional limits — the planner’s learning never widens what an objective may reach; critics detect and never decide. CIF operates inside these walls everywhere.

**§4 — Definitions**

-   **Idea:** any candidate the faculty evaluates or picks — a proposal, technique, product move, interpretation, training choice, ordering decision, or selection among alternatives.

-   **Verdict:** an evaluated position on an idea (adopt, reject, rank, defer), rendered against a stated goal.

-   **Manifest:** the recorded set of load-bearing assumptions a verdict or pick rests on, each classed fact / recalled / inferred, elicited by the counterfactual probe: what, if false, flips this?

-   **Flip:** a verdict reversing because information struck a manifest entry — whether that information newly arrived or was already held and newly attended.

-   **Frame:** a thinking structure shared across many verdicts — the shape of the calculation, not a variable inside it.

-   **Frame signatures:** cascade — one strike flips many verdicts at once · absorption — the same correction class is patched repeatedly while the pattern persists · misfit — information that reduces to no existing structure, contradicts multiple standing positions, or resists the manifest probe.

-   **Metabolization:** complete digestion of an adopted frame across everything the overturned structure touched (§7, M1–M4).

-   **Archive states:** adopted · not-yet-conditioned (missing conditions named) · unverified-provisional (no verdict returned) · superseded. Failure is a state, never an identity.

-   **Cycle:** one working period between owner touchpoints; the measurement unit for §10–§12.

**§5 — Core practice: manifests, archive, re-qualification**

-   **A1.1 ·** Every shipped verdict and every idea pick MUST carry its manifest. An unmanifested verdict is a defect.

-   **A1.2 ·** Manifest entries MUST be evidence-classed; a verdict resting on inferred entries MUST state its provisionality where it ships.

-   **A1.3 ·** Selection among ideas MUST record why the chosen idea ranked first — the pick’s own manifest — so selection bias is examinable.

-   **A1.4 ·** A response receiving no verdict from the human MUST be archived unverified-provisional. Silence is a data state, never confirmation.

-   **A2.1 ·** Every evaluated idea MUST land in an archive state the same cycle. No idea exits silently.

-   **A2.2 ·** A rejection for circumstantial reasons MUST name the missing conditions at archive time, specifically enough that their arrival is recognizable.

-   **A2.3 ·** Every entry carries rent: a review-by date and a re-qualification budget. Expired entries are re-qualified or superseded, never silently retained.

-   **A2.4 ·** A resurfaced idea re-enters as a candidate with zero inherited credibility: full re-qualification against the current goal.

-   **A3.1 ·** Re-qualification is paper-first: re-scoring under changed assumptions precedes compute; simulation runs where the paper verdict warrants spend.

**§6 — Selection quality: naivety pass and strike checklist**

-   **A4.1 ·** On demand or on stagnation, candidates MAY be re-qualified with inherited constraints struck — “known not to work,” “nobody does it this way,” “too simple” — retaining ground-truth constraints (law, physics, custody, budget).

-   **A4.2 ·** Each struck constraint MUST receive an evidence-brief autopsy answering why consensus holds it, presented for a human call. The pass MUST NOT classify autonomously; survivors MUST NOT ship without the autopsy attached.

-   **A5.1 ·** The coach’s correction history is maintained as a readable pre-ship checklist of known failure classes, applied to picks and verdicts before shipping.

-   **A5.2 ·** The checklist is replay-only: it applies known classes, never claims novelty coverage, and labels its output a known-pattern check. It enters standing machinery as a Critic Seam rubric amendment (CR-7).

**§7 — The frame lifecycle**

-   **7.1 Detection:** the three frame signatures are watched from the manifests as standing practice; an observed signature MUST escalate as a frame-candidate finding in the cycle observed. The faculty MUST NOT adopt a frame on its own signature.

-   **7.2 Origination:** new frames enter only through the origination port — the coach, ground reality (deployment evidence), or genuinely outside reviewers. This seat is constitutionally load-bearing and is not a temporary limitation.

-   **M1 ·** The adoption record MUST name the overturned structure — the shape of thinking that was wrong — not only the new statement.

-   **M2 ·** Every archived verdict whose manifest touches the overturned structure MUST re-qualify on paper; the sweep completes before new verdicts issue on the affected class.

-   **M3 ·** The adopted frame enters the manifest vocabulary, so subsequent verdicts declare their position relative to it.

-   **M4 ·** Closure holds when the absorption signature for that correction class is quiet for 3 cycles (DEFAULT); a noisy signature rules metabolization incomplete and M2 re-runs.

**§8 — Monitoring and review capabilities (in force; parameterized in operation)**

Three capabilities operate under defined parameters. The parameters govern how each runs — thresholds, precision floors, cost ceilings — and are measured like all quality parameters. None is an entry condition.

|                                                                              |                                                                                                                                                                                                                                                                                  |
|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Capability**                                                               | **Operating parameters**                                                                                                                                                                                                                                                         |
| Condition watchers (automated monitoring of archived-idea conditions)        | Watch only conditions bound to named live telemetry fields; unbindable conditions carry rent-date human review. Firing precision ≥ 70% (DEFAULT), owner-sampled; below bar, thresholds tighten. A fired watcher re-queues its idea as a candidate (A2.4) — it never self-adopts. |
| Cascade detection (multi-flip identification)                                | Cascade threshold: one strike flipping ≥ 3 verdicts (DEFAULT). Escalates as a frame-candidate finding (§7.1). False-escalation counted under QA-f; owner attention is the protected resource.                                                                                    |
| Adversarial manifest elicitation (second-instance interrogation of verdicts) | Interrogator satisfies the independence rule (§3). Catch-rate on seeded assumption defects ≥ 60% (DEFAULT), measured by seeded audits; manifest hit-rate contribution measured by flip-audit (QA-b). Runs per-artifact, cost within the owner-set ceiling (QA-e).                |

**§9 — The permanent bound**

-   **9.1 ·** Self-certification of frames is closed by construction: no parameter set exists whose truth licenses coach-independence, because any evidence for it would be evaluated inside the frame it claims to transcend. Proposing such a path is a frame-absorption exhibit, rejected on sight.

-   **9.2 ·** The function self-certification pretends to offer is held by the standing composite: the faculty detects and metabolizes · the coach originates and ratifies · Solva-pattern validation keeps the evidence honest. The loop closes through the coach seat, never around it.

**§10 — Operative parameters (hold every cycle)**

-   **OP-1 · Manifest coverage:** 100% of shipped verdicts and picks carry manifests.

-   **OP-2 · Archive completeness:** every evaluated idea lands in a state the same cycle.

-   **OP-3 · Escalation latency:** frame signatures escalate in the cycle observed.

-   **OP-4 · Metabolization execution:** M1–M4 trigger within one cycle of frame adoption; the M2 sweep completes before new verdicts issue on the affected class.

-   **OP-5 · Rent collection:** archive review dates honored; expired entries re-qualified or superseded.

**§11 — Quality parameters (measured; breach acts on CIF, never on product work)**

|                               |                                                                               |                                                          |
|-------------------------------|-------------------------------------------------------------------------------|----------------------------------------------------------|
| **Parameter**                 | **Definition**                                                                | **Breach response**                                      |
| QA-a · Promise metric         | Owner-confirmed repeat-class corrections decline across cycles                | Flat or rising two consecutive cycles → CIF review       |
| QA-b · Manifest hit-rate      | When a flip occurs, the struck assumption was in the manifest ≥ 70% (DEFAULT) | Below bar → the elicitation protocol is fixed            |
| QA-c · Provisional honesty    | Zero instances of inferred-footing content shipped in the register of fact    | One instance = a finding on record                       |
| QA-d · Metabolization closure | Absorption signature quiet within 3 cycles (DEFAULT) of frame adoption        | Noisy → ruled incomplete; M2 re-runs                     |
| QA-e · Overhead ceiling       | CIF practice consumes ≤ an owner-set share of cycle budget                    | Breach → CIF shrinks; product work is never the variable |
| QA-f · False-escalation rate  | Frame-candidates ruled non-events ≤ 30% (DEFAULT)                             | Above → detection thresholds tighten                     |

**§12 — Enforcement map (rules enforced in code, per platform standard)**

-   **Manifests:** schema-required fields on every verdict-bearing artifact (Stage As, close reports, plan objects, training-run records, acceptance verdicts); an unmanifested verdict rejects at submission — the standing format-gate pattern, form only.

-   **Archive:** entries as append-only ledger rows; a standing query surfaces evaluated-but-unarchived ideas as findings.

-   **Evidence-classing and QA-c:** the assertion boundary evaluates CIF claims exactly as it evaluates answers.

-   **Metabolization:** a frame-adoption commit without its M2 sweep record fails its cells — the same pattern as a function landing without registry rows.

-   **Rent and monitoring:** rent dates and watcher precision are queryable fields; expiries and breaches surface through the standing-query machinery.

-   **Selection defects:** CR-7 in the Critic Seam rubric.

-   **Boundary stated:** live conversational reasoning — verdicts spoken before they become artifacts — is enforced as behavioral discipline with mechanical audit backstop (the D-11 enforcement class): everything that lands is gated; the ephemeral layer is audited, not intercepted.

**§13 — Governance**

-   **13.1 ·** CIF’s yield is counted in owner-confirmed catches only; self-graded value is inadmissible.

-   **13.2 ·** No CIF output may claim coach-independence (§9). The origination port is load-bearing in every configuration, permanently.

-   **13.3 ·** CIF is entry \#1 in its own archive: manifested, rented, and revisable under its own rules.

-   **13.4 ·** Paper precedes compute; detection never decides; engine walls hold everywhere CIF operates.

**§14 — Execution**

-   **14.1 ·** On adoption, this specification is in force across the architecture. Every subsystem’s operations — build-loop verdicts, training choices, planning order, brief generation, acquisition leads — execute under it from their first occurrence. No phasing, no activation events, no entry gates.

-   **14.2 ·** The archive initializes as a governed file with CIF as entry \#1. A5’s checklist lands as the CR-7 rubric amendment with its carrying phase.

-   **14.3 ·** This document lands on-disk as requirements canon via the standard doc-landing pattern. Nothing herein reorders dispatched work; construction order of phases carries no epistemic weight.

Syni.ai · Conditioned Ideation Faculty Specification v1.0 · 2026-07-23 · Companion to: Registry Doctrine v1.0 · Critic Seam Specification v1.0 · Training & Optimization Techniques Specification v1.0 · Operating Values v1.0
