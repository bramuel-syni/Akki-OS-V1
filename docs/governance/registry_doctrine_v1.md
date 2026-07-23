AKKI · GOVERNED ARTIFACT · BINDING ON RATIFICATION

# The Registry Doctrine

Function & Promise Registry — Mandate, Engineering Specification, and Behavioral Doctrine · v1.0

Prepared by the Owner's ruling authority · July 2026 · Confidential. This document is binding on Owner ratification. Part I is the mandate — what changes and why. Part II fixes the service layer. Part III specifies the Registry. Part IV states behavioral doctrine in force on ratification. Part V specifies cost architecture. Part VI specifies the culture layer. Part VII carries the extraction-quality de-risking specification. Part VIII states the execution model and defect classes. Scope boundary, stated once and binding: nothing in this document reopens the mandate-complete build, dispatches work, or creates a schedule. Code-level items enter only through the standing Stage A → Owner ruling → atomic execution → close loop, each on explicit Owner dispatch. This document changes how work is scoped, ruled, and justified — it does not start any.

# Part I — Mandate: what changes, and why

## §1.1 The two weaknesses this doctrine answers

The platform's strength — enforcement-in-code at many levels — carries two failure modes at scale, both observed in miniature during the build:

- W1 · Rule proliferation. Gates are cheap to create and immortal by default. Unmanaged, the gate population grows superlinearly with estates and rule evolution; execution cost, maintenance burden, and false-positive load grow with it; and the signal value of any one gate failing decays toward noise. The build itself required a tiered ruling model invented mid-flight, two over-gating corrections, and dead-tracker sweeps — in one instance, with one engaged owner. The spiral is the default trajectory, not a tail risk.
- W2 · Natural-language dependency. Where correct behavior depends on a human or a model interpreting prose in the right sequence, cost and error scale with volume. NL is the correct interface for humans; it is an unacceptable enforcement medium.

## §1.2 The solution shape: the law of reduction

The answer is not more governance of the governance. It is one foundational baseline that every moving, evolving piece anchors to. Functions are many; the promises they protect are few; the services those promises serve are fewer still. The Registry makes the small set canonical and derives the large set from it. Reduction is the standing test: every artifact this doctrine creates must shrink something — the gate population, the judgment surface, the cost per decision — or it is retired under its own rules.

## §1.3 The anchor: service before function

The reasoning order for every future scoping, ruling, and review is fixed: service → journey → promise → function. A function justifies itself by the promise it protects; a promise by the journey step it secures; a journey by the service sentence it delivers. Anything that cannot trace upward is doing the wrong job well — the named failure this doctrine exists to prevent. The service layer belongs to the Owner: changing a service sentence changes the product, and occurs only by Owner ruling. Precedent already on the record: the AF-E2 owner-value amendment — "the asker's service is an answer, not an LLM answer" — is this doctrine applied before it was named.

# Part II — Layer 0: the services Akki issues

Correction carried from Owner review, binding: the platform's top-layer users are applications, not end-users. End-user experience (askers, executive readers) belongs to applications built on Akki — the Ask experience and Akki-for-Executives are apps consuming the platform, one of them first-party. Platform decisions never optimize for end-user UX directly; they optimize the service issued to the integrating application. Consequences: (a) the Ask Console is reclassified as a first-party reference application demonstrating S1; (b) end-user personas appear in the Registry only inside application definitions, one level below Layer 0, owned by the application; (c) "Onboard organization context" is a named journey step of S2, closing a known platform gap at the specification level.

The five service sentences — Layer 0, carried as proposed, canonical on Owner ratification, thereafter changeable only by Owner ruling:

- S1 · To the integrating application (internal or external — the top-layer user): "A governed intelligence surface my app can build on: answers, skills, and artifacts that arrive with class, receipt, and refusal semantics intact — so my app inherits provability instead of building it." Journey: register (via engineer) → scoped key → call → pass receipts through.
- S2 · To the operating organization / Operator: "My estate onboarded, mapped, and turned into qualified intelligence I can commit with confidence." Journey: onboard context → integrate sources → census fills → commission → sample → commit.
- S3 · To the Compliance Officer / DPO: "Proof of any operation on demand, and governed control of the rules over data." Journey: pick a run → prove end-to-end; see retention → change rules with ceremony.
- S4 · To the data buyer: "Intelligence products I can verify independently before I rely on them — never raw data." Journey: receive → verify receipt → license.
- S5 · To the infrastructure consumer (recorded-future): "Akki's extraction and governance capacity as a substrate my venture builds on." Registered so nothing optimizes against it prematurely; explicitly not built; no function may cite S5 as its sole anchor without Owner ruling.

# Part III — The Function & Promise Registry: engineering specification

## §3.1 What it is

One canonical, versioned artifact registering every named function in the platform — gate, governor behavior, worker obligation, console guarantee — with its mandate, the promise it protects, and its full accounting. It begins as a governed document and graduates to a machine-readable artifact by Owner-dispatched phase. It is the single source the standing queries run against, the input the sequencing harness optimizes over, and the operating context LLM workers receive. It inherits its top-level taxonomy from the constitution: every function belongs to SyniSense, Northena, Mtafiti, Targeta, or Solva (or, for UI guarantees, a named surface).

## §3.2 Schema — one row per function, all fields mandatory

| Field | Definition and discipline |
|---|---|
| function_id | Stable identifier, namespaced under its governor or surface (e.g. northena.ledger.append_only_gate). Never reused. |
| governor | Owning authority: SyniSense · Northena · Mtafiti · Targeta · Solva · or named surface. No new top-level categories without Owner ruling. |
| mandate | "Built to …" — one sentence, active voice, testable. What the function does, not how. |
| promise | "Why this matters …" — the promise protected, phrased so its breach is observable. Promises are the small set: many functions may cite one promise; no function may cite zero. |
| service_trace | The Layer 0 sentence(s) and journey step(s) this promise secures (e.g. S1.call, S3.prove). Empty or invalid trace = orphan (Q2). |
| surface | Where it acts: module path, route, contract, console element. |
| enforcement | Mechanism class: byte-identity lock · AST/reflection walk · grep-negative · runtime check · E2E cell · type-level wall · constraint-architecture (§6.1). "NL-only" is not a legal value (defect D2). |
| cost | Execution time class, maintenance burden, false-positive rate where known. "Unknown" is a legal initial value; it must be replaced by measurement when the sequencing harness first exercises the function. |
| dependencies | Functions or data required ordered-before. Input to sequencing. |
| ladder_rung | Implementing rung (§5.1): deterministic · classical-NLP · owned-model · frontier-LLM. Written justification required for any rung above the cheapest plausible. |
| owner | Change authority: Owner · builder-Tier-3 · dual-control. Inherits the tiered ruling model unchanged. |

## §3.3 Derivation rules — binding

- R1 · No gate without a promise. A function whose promise field cannot be honestly filled is not refactored into legitimacy; it is retired.
- R2 · No promise without a service trace. A promise serving no journey step of any Layer 0 sentence is either mis-stated or evidence of product drift; escalate to Owner, never paper over.
- R3 · No journey step without enforcement. Every step of every Layer 0 journey resolves to at least one registered function protecting it. An unprotected step is an exposed liability and is reported, not assumed safe.
- R4 · New functions register before they land. From ratification forward, any Stage A proposal introducing a gate or worker obligation includes its Registry row; the row is part of the Tier-1 ruling surface.

## §3.4 The three standing queries

Run on every Registry change and on a standing cadence. Results are reports; retirements and merges execute under the tiered ruling model — Tier-3 where mechanical, Tier-1 where a promise is touched:

- Q1 · Redundancy: two or more functions, same promise, same surface → merge/retire candidates, ranked by cost.
- Q2 · Orphans: function with empty or invalid promise/service_trace → retirement candidate on sight.
- Q3 · Gaps: promise or journey step with no enforcing function → exposed-liability report to Owner, found before an incident finds it.

## §3.5 Population — archaeology, not authorship

The Registry populates by extraction from what exists: the governor mandate documents, the rulings record, the close reports' gate rosters, and the BCR. Every Tier-1 escalation in the build already carried a "Promise protected" line — the raw material is on disk. Population invents nothing: where extraction finds a gate whose promise cannot be recovered, that is a Q2 finding, not a writing prompt.

## §3.6 The Registry pays rent

The Registry is subject to its own law. Its rent is the three queries: if over a sustained period it stops retiring gates, finding gaps, or cheapening sequences, it is itself retired or restructured by Owner ruling. One artifact, one schema; a second meta-layer above it is defect D5.

# Part IV — Behavioral doctrine (in force on ratification)

These bind every actor in the build — Owner's ruling authority, builder, and any agent or model worker — immediately on ratification, with no code change required:

- D-1 · Reasoning order. Service → journey → promise → function, in every scoping, escalation, and ruling. Escalations name the promise protected and its service trace (the existing "Promise protected" discipline, now with the trace made explicit).
- D-2 · Rules pay rent. Every gate carries its promise and its cost. A gate that protects no live promise is retired, not preserved out of caution. Caution that costs forever must justify itself forever.
- D-3 · The conflation test. Before any function is proposed: which Layer 0 sentence does this serve? No sentence, no build. This is the structural prevention of "doing the wrong job well."
- D-4 · Cheapest-sufficient rung. Every task lands on the lowest model-ladder rung that meets its promise (§5.1). Rung inflation requires written justification at Stage A.
- D-5 · NL is interface, never enforcement. Every natural-language rule pairs with a machine-enforced twin. NL-only enforcement is defect D2, reportable on sight.
- D-6 · Constraint architecture first. Prefer designs where correct behavior is the path of least resistance; gates are the backstop, not the mechanism. Every promise the architecture absorbs is a gate never written (§6.1).
- D-7 · Verdicts are never curated. Inputs, models, corpora, and discovery paths may be engineered without limit; validation verdicts are drawn from measured composition, uncurated, and published internally whatever they say (Part VII).
- D-8 · Reduction applies to its own output. Specs, trackers, and meta-artifacts are retired when they stop earning. The dead-tracker sweep is a standing pattern, not an event.
- D-9 · Platform serves applications. No platform decision optimizes end-user UX directly; end-user experience is application territory (Part II).
- D-10 · Builder conduct standard. Meticulousness is enforced by structure, not assumed: every proposal self-audits against defect classes D1–D7 before submission, and a proposal arriving with a defect the self-audit would have caught is itself a reportable finding.
- D-11 · Canon before ruling. No ruling, audit, or characterization of an engine or spec surface proceeds from memory or summary. The on-disk documents are canon; unread canon is read before ruling; recalled content is never presented as fact. Binding on the ruling authority and the builder alike.
- D-12 · Experimentation exists at system level only. The architecture — the assembled operating system delivering the enterprise promise — is the sole object under test; it is the novel invention, and deployment is its experiment. Every component mechanic is known and parameterizable: it deploys in force with its conditions of success strictly implemented and its quality measured, or its parameters are undefined — a specification gap to close, never a reason to run tentatively. Gates in this platform bind spend, quality of output, or claims — never existence or force. No capability with defined parameters is gated on demonstration, observation, trial modes, or staged proving. A Stage A proposing pilot flags, shadow phases, or "observe-first" sequencing for known mechanics is a D-12 finding on sight. Construction order of phases carries no epistemic weight.

*Part IV amendment record: D-11 admission 2026-07-14 · D-12 admission 2026-07-15.*

# Part V — Cost architecture

## §5.1 The model ladder

Four rungs, ordered by cost. Selection rule: the lowest rung that meets the promise. The registry's ladder_rung field makes every placement inspectable; the build's own precedent stands as the pattern — grounding gates were ruled as byte-mechanical checks, explicitly rejecting semantic scoring, and both frontier-LLM consumers carry mechanical fallback arms, so the expensive rung is architecturally optional everywhere it appears:

| Rung | What belongs here | Cost behavior |
|---|---|---|
| 1 · Deterministic code | Byte checks, regex, structural walks, contract locks, counting, routing. All current grounding verification lives here by ruling. | Near-zero marginal; fully auditable; never drifts. |
| 2 · Classical NLP (spaCy-class) | Tokenization, NER, sentence segmentation, language ID, rule-based tagging — anywhere linguistic structure is needed without open reasoning. | CPU-cheap, deterministic-enough, offline-capable. |
| 3 · Small owned models | Estate-fine-tuned perception and domain models (ASR, diarization, classifiers) from the transformation layer; registry-pinned. | Owned IP, near-free inference in-perimeter; the flywheel migrates work down to this rung continuously. |
| 4 · Frontier LLM | Open synthesis only: fluent composition, brief narrative — always behind the Shield, always with a lower-rung fallback arm. | Highest unit cost; every use answers "why not rung 3?" at Stage A. |

The deflation law: the transformation layer is the cost answer to itself. Every training cycle on the estate produces owned models that migrate rung-4 and rung-2 work to rung 3, and rung-3 findings that harden into rung-1 checks. The flywheel that improves quality is the same flywheel that deflates unit cost — by design, not by hope.

## §5.2 The sequencing harness

Specification (enters as code only on Owner dispatch): a harness that executes registered functions against fixture traffic in candidate orderings and measures real cost — not simulated approximations. Principle: this system is predominantly deterministic; you do not simulate a deterministic gate, you run it. Orderings are optimized over the Registry's cost and dependency fields: cheap gates before expensive, deterministic rungs before model rungs, independent functions in parallel, fail-fast paths surfaced. Honest boundary, stated as a spec constraint: rung-3/rung-4 behavior is measured statistically (repeated runs over the harness, route-level comparisons), never claimed as exact. Output: the measured best path of integration and sequencing per journey — replacing sequencing judgment with sequencing measurement, and back-filling every "unknown" cost field in the Registry.

# Part VI — The culture layer

"Culture" is operational here, not metaphorical: the environment that makes correct behavior natural for every worker class. Two mechanisms for two populations:

## §6.1 Deterministic components: constraint architecture

Defaults and affordances that make violation structurally awkward, so explicit gates become backstops. The build's strongest moments already work this way: the pull seam makes raw egress unnatural rather than merely forbidden; write-once storage makes slice mutation unnatural rather than merely tested; the two-faculty seam makes claim-laundering type-impossible rather than reviewed-for. Standing preference at every Stage A: absorb the promise into the architecture where possible, and register the absorption with enforcement class "constraint-architecture" — a promise absorbed is a gate never written, executed, or maintained.

## §6.2 Model workers: the Registry as operating context

An LLM worker's behavior is shaped by the context it receives; the Registry is that context. Harnessing rule (enters as code on Owner dispatch): every model worker receives the promises in force on its task — mandate, promise, and service trace for the functions it touches — as part of its operating prompt. One artifact thereby serves three roles: source of truth for humans, compile-source for gates, and system context for workers. A worker that knows why each rule exists errs toward the promise; a worker given only a task list errs toward the task.

# Part VII — Extraction quality: the de-risking specification

Premise, Owner-agreed: extraction quality on a specific estate is unmeasured until measured — but its weak surfaces are enumerable in advance, each has existing open art, and each maps to a designed lever in the platform. The gap is speccable, not fated. Governing principle, restating D-7: engineer the inputs relentlessly; never touch the test. Model choice, fine-tuning, augmentation, and corpus curation are legitimate curation of success; the validation verdict (the human-baseline benchmark, BM-V) is drawn from measured estate composition, post-census, uncurated — a rehearsed checkpoint is preparation; a curated verdict is worthless.

| Weak surface | Existing art (starting points) | Akki lever | Pre-verdict checkpoint |
|---|---|---|---|
| Swahili & Kenyan languages | Meta MMS (1,100+ languages); multilingual Whisper; Mozilla Common Voice Swahili; FLEURS; KenCorpus | Registry-pinned base models per language; language-routed model selection at job level | Per-language WER on a small real sample — measured in week one, not month three |
| Code-switching (Sheng, Swahili–English) | Code-switch fine-tuning recipes; East African community corpora (Masakhane ecosystem) | Census-curated code-switch corpus → in-perimeter fine-tune; improved model re-enters via registry bump | Code-switched-segment WER vs monolingual baseline, same speakers |
| Accented English | AfriSpeech-200 (pan-African accented English); accent-adaptation literature | Fine-tune or adapter on accented checkpoint; pinned provenance either way | Accent-stratified WER on real archive segments |
| Degraded / telephone / AM archival audio | Standard augmentation + domain-adaptation recipes for narrowband, noisy audio | Augmentation in the training loop; era- and quality-stratified census slices target hard bands | WER by decade and quality band — the census provides strata for free |
| Speaker overlap & call-in diarization | Open diarization stacks (pyannote-class); overlap-aware recipes | Diarization model swap via the registry; VAD/diarizer independently upgradable | DER on a multi-speaker call-in sample |

## §7.1 Sequencing — each rung cheap, each rung a real number

- 1 · Domain-transfer measurement (first). Run current registry models on a small genuine sample spanning the strata above. Output: baseline WER/DER per surface. Days of work; removes the largest unknown first.
- 2 · Targeted adaptation. Where a surface misses its working threshold, apply its lever — swap base model, fine-tune, augment — and re-measure the same checkpoint. The registry's additive versioning records every attempt with pinned provenance.
- 3 · Composition-scale validation. BM-V runs on a slice drawn from the censused estate's real composition. Whatever it says is published internally and stands as the claimable number. Its P9-E5 bindings are unchanged by this doctrine: verdict inside the phase; no production mining until PASS.
- 4 · Throughput & cost. Only after quality is known: hours-per-GPU-hour and cost per qualified unit on production hardware — planning-grade economics become quoted economics.

Claims discipline: until step 3 completes, collateral states the method, never a number; after step 3, the measured figure is the only accuracy claim in circulation — whatever it is.

# Part VIII — Execution model and defect classes

## §8.1 What is in force, what drafts, what codes

- In force on ratification (no build): Part II service layer; Part III derivation rules R1–R4 as scoping discipline; Part IV doctrine D-1–D-9; Part VII claims discipline.
- Documents (draft on Owner word, no code): Registry population (§3.5 archaeology); Instance Replication Playbook; Commercial Thesis.
- Code-level (each enters only via Stage A → Owner ruling → atomic execution → close, on explicit Owner dispatch; no schedule exists or is implied): (a) the three standing queries as executable checks over a machine-readable Registry; (b) the sequencing harness (§5.2); (c) Registry-as-context worker harnessing (§6.2); (d) the Registry's machine-readable form itself; (e) far endpoint — mandates as structured specs from which gates are generated.
- Untouched by this doctrine: the mandate-complete build; parity 31; all standing rulings; 9.2b's single-signal gate ("proceed"); P9-E5 BM-V bindings; the tiered ruling model, which this doctrine extends and does not replace.

## §8.2 Defect classes (named, reportable on sight)

- D1 · Orphan gate: function with no honest promise or no service trace.
- D2 · NL-only enforcement: a rule whose only enforcement is prose interpretation.
- D3 · Curated verdict: any selection of validation material by favorability rather than measured composition.
- D4 · Rung inflation: model-ladder placement above cheapest-sufficient without written Stage A justification.
- D5 · Meta-spiral: a second governance layer above the Registry; governance artifacts that stop paying rent.
- D6 · Service conflation: platform function optimized for an end-user persona rather than a Layer 0 service; the wrong job done well.
- D7 · Invented schedule or scope: sequencing, deferral, or owner-side workstreams introduced without Owner instruction — binding on the ruling authority and the builder alike.

## §8.3 Ratification

This document binds on Owner ratification of: (a) the five Layer 0 service sentences verbatim or as corrected; (b) the doctrine set D-1–D-9; (c) the defect classes D1–D7. On ratification it lands on-disk as a governed artifact beside the governor mandates, and R4 takes effect for all subsequent Stage A proposals.

Syni.ai · The Registry Doctrine v1.0 · Companion to: governor mandate documents · tiered ruling model · BCR v1.5 · Extraction De-Risking Spec v1
