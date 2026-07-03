**RMS Intelligence System**

Product & Engineering Specification

The master specification for a governed multimodal
intelligence-extraction platform. This document is comprehensive at the
level of architecture and behaviour: it specifies the system whole — the
engine, the five rings, the defensibility model, the three governors and
two engines, the frozen contracts, and the validation gates — to full
technical and behavioural depth. It sits above the four engine
specifications, which carry each component’s module structure, typed
contracts, and test obligations.

Version 2.1 · the canonical parent; prevails over any engine
specification on conflict.

*Prepared by Syni.ai for Royal Media Services · July 2026 ·
Confidential*

This is the binding master specification. It states the system as it is
designed to be — a forward specification from which the system is built,
not a description of an implementation. Where it states a rule, that
rule binds. Findings settled to date appear here as settled design
decisions: the founding six frozen contracts (extensible by addition; see §26), the ring refinements, the two-layer
measures, the unit-versus-audit separation, and the common structural
guard (§3). Nothing in this document assumes a build has occurred; it
specifies what must be true of any correct build.

**Contents**

**Part I — The System**

1\. Purpose and Scope

The RMS Intelligence System converts a twenty-year multimodal broadcast
archive into intelligence: governed claims, extracted on demand, reused
across objectives, and delivered either inside Royal Media Services for
decisions or externally as a governed product. It is an extraction
platform, not a storage platform. The archive remains under RMS control;
what leaves the system is intelligence — transformed, governed, and
honest about its own standing — never the raw estate.

This specification defines the product and its engineering to the depth
required to build it without re-interpretation. It covers the extraction
engine, the shape of every unit of intelligence, the model that governs
what may be asserted, the governors and engines that bound the system,
the contracts everything binds to, the gates that validate it against
reality, and the data-protection posture. It is the parent of four
engine specifications (Northena, Targeta, Mtafiti, Solva); those
elaborate module-level implementation, and are consistent with this
document, which prevails on conflict.

What the system is not

-   **Not a search index.** It does not return documents or passages
    ranked by relevance; it returns governed claims with provenance and
    a defensibility measure.

-   **Not a data lake.** It does not pool raw content for arbitrary
    query; it extracts intelligence against the estate in place, under
    governance.

-   **Not a truth oracle.** It does not adjudicate whether contested
    claims are true; it measures how defensibly each claim may be
    asserted (Part IV).

2\. The Two Services

The system runs two services over one engine and one Normalized tier.
Service 1 stands the estate up; Service 2 operates against it day to
day.

2.1 Service 1 — Estate Extraction (Day Zero)

Service 1 is the standing-up pass. Under a Portfolio Mandate — the
governing artifact that declares which estate, at what priority, to what
class-default floor — the system censuses, prioritises, and converges
the estate into the Normalized tier. The flow is Mtafiti (census +
defensibility measure) → Targeta (prioritise where to mine) → Akki A→B→C
(retrieve, perceive, converge). It terminates at convergence: Service 1
populates the tier; it does not answer objectives. It is re-run when the
Registry materially changes (Part IV, freshness).

2.2 Service 2 — Objective Extraction (Day to Day)

Service 2 is the standing operation. Against an Objective Request — the
governing artifact that declares the objective, its defensibility floor,
its scope, its lawful basis — Layer D composes intelligence over the
Normalized tier, calling A→B→C as fallback only for un-converged slices.
The run is directed by Northena (is it in scope, is it done) and
governed for depth by Solva (is the reasoning sound, does the output
assert within its defensibility). It returns a governed answer carrying
provenance, defensibility class, and a trace. Each answered objective
densifies the warm tier, so adjacent future objectives are cheaper to
serve.

2.3 One engine, one tier, two services

Both services compose the same Akki engine over the same Five-Rings
Normalized tier. The engine is consumer-blind (§9): it produces
intelligence identically whether the eventual consumer is internal or
external. The consumer’s location selects the delivery perimeter (§4),
which is a governance concern, not an engine concern — the extraction is
the same.

3\. The Governing Principle — One Guard, Applied Four Times

The system’s integrity rests on one structural principle, applied once
in each component that carries power. In each, the powerful part is
separated by construction from the governed decision it must not touch:
the guarded value is not an input the powerful part receives, so a
violation is unrepresentable rather than merely disallowed. The
separation is enforced by a type, a dependency rule, or an interface —
never by runtime policing or good behaviour.

|               |                        |                                                                                                                                                 |
|---------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| **Component** | **The powerful part**  | **Separated from**                                                                                                                              |
| **Northena**  | Run-to-run dynamism    | Auditability. Dynamism comes only from the frozen governing artifact; Northena contains no model and never learns.                              |
| **Targeta**   | Learned yield ordering | Eligibility. The yield layer receives only the floor-passing set and returns a permutation of it; a non-permutation is a type error.            |
| **Mtafiti**   | Learned inference      | The verdict. Inference emits detections only; the defensibility verdict is a governed Qualification Matrix lookup.                              |
| **Solva**     | Genuine reasoning      | The assertion ceiling. The conclusion’s class is a floor over its load-bearing units’ classes, computed without reasoning strength as an input. |

**Why the guard is structural.** In every case the failure is the
powerful part reaching the governed decision — a learned layer
suppressing a source below the floor, reasoning asserting an utterance
as fact. The design makes the reach unrepresentable: the guarded value
is simply absent from what the powerful part receives, so the violation
cannot be expressed. This is what allows the system to be both maximally
capable in its powerful parts and fully defensible at its governed
decisions. Every component specification in Parts V–VI is an instance of
this one principle.

4\. Delivery — Two Wrappers, Two Perimeters

One extraction is delivered four ways. The extracted unit or composition
is packaged in one of two wrappers and delivered across one of two
perimeters; the extraction itself is unchanged by either choice.

|             |                                                                                                               |
|-------------|---------------------------------------------------------------------------------------------------------------|
| **Wrapper** | **Meaning**                                                                                                   |
| Dataset     | Structured intelligence — a set of governed units, each with its rings, delivered as data.                    |
| Skill       | A named, bounded capability that answers a class of objective — a reusable extraction, wrapped and invocable. |

|               |                                                                                                                                                                                      |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Perimeter** | **Meaning**                                                                                                                                                                          |
| Inner gate    | Live intelligence served in-tenancy. De-identifies before any external model call, re-identifies on return, fail-closed, audited. The default, and buildable without the outer gate. |
| Outer gate    | File-out for external sale. Applies the irreversibility transform, validates rights (gate V2), and guards cumulative disclosure. Only irreversibly transformed data crosses it.      |

The two perimeters are governed by SyniSense (§20). The wrapper and
perimeter are chosen per delivery; the same extracted intelligence may
be served live in-tenancy to one consumer and, subject to V2, filed out
irreversibly to another.

**Part II — The Extraction Engine (Akki / CIPP)**

5\. The Engine in Four Layers

Akki — the Convergent Intelligence Processing Pipeline — is the
extraction engine. It is four layers: Retrieval (A), Modality Extractors
(B), Convergence (C), and the Extraction Orchestrator (D). Layers A–C
run in Service 1 and terminate at the Normalized tier; Layer D runs in
Service 2 over that tier, calling A→B→C only as fallback for
un-converged slices. The engine is consumer-blind and objective-agnostic
below Layer D: A, B, and C extract the estate the same way regardless of
what will later be asked of it, which is what allows one Normalized tier
to serve every objective.

|           |                         |                                                                                                                                  |
|-----------|-------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| **Layer** | **Name**                | **Function**                                                                                                                     |
| A         | Retrieval               | Modality-aware fetch of the raw estate slice the mining plan targets, carrying the objective’s defensibility floor forward.      |
| B         | Modality Extractors     | Parallel, in-tenancy perception per modality; emits modality-native output plus genre-form and source-attachment markers.        |
| C         | Convergence             | Normalises modality-native output into the modality-neutral Five-Rings representation; computes relational edges; stamps Ring 5. |
| D         | Extraction Orchestrator | Consumer-blind primitives composing over the Normalized tier to answer an objective; two output-forms, two consumer-locations.   |

6\. Layer A — Retrieval

Layer A fetches the raw estate slice named by the mining plan and routes
it to the correct modality handler. It is modality-aware but
perception-blind: it retrieves bytes and dispatches them; it interprets
nothing.

Behaviour

-   **Dispatch by modality.** A single dispatcher routes each source to
    its handler — audio, video, image, text, or transcript — by the
    source’s declared modality, not by inspection of content.

-   **Carry the floor.** The objective’s defensibility floor travels
    with the retrieval request, so downstream layers extract only
    material capable of meeting it and Targeta’s plan is honoured
    end-to-end.

-   **No interpretation.** Layer A performs no perception, no
    classification, no extraction. A source that cannot be retrieved is
    recorded as such; it is never inferred or substituted.

The five handlers

|             |                                                                                                                      |
|-------------|----------------------------------------------------------------------------------------------------------------------|
| **Handler** | **Retrieves**                                                                                                        |
| audio       | Broadcast audio streams/files — passed to the ASR + diarization sub-pipeline in Layer B.                             |
| video       | Video with its audio track — frames to vision perception, audio track to the audio sub-pipeline.                     |
| image       | Still images — to scene perception and OCR where text is present.                                                    |
| text        | Documents, captions, wire copy — to native text perception.                                                          |
| transcript  | Pre-existing transcripts (VTT/SRT/JSON) — to text perception, with the transcript hash recorded for reproducibility. |

7\. Layer B — Modality Extractors

Layer B runs modality-native perception in parallel, entirely
in-tenancy. Each extractor emits its native output together with the
genre-form and source-attachment markers that Layer C and the
defensibility model consume. Perception is a self-hosted, in-tenancy
operation without exception: no raw personal data leaves RMS tenancy for
perception.

7.1 The extractors

|              |                                                                                                                                                                                                                             |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Modality** | **Extraction and emitted signal**                                                                                                                                                                                           |
| Audio        | ASR over Swahili / English / Sheng code-switching, plus speaker diarization. Emits transcript, speaker turns, and prosodic signal (prosody, vocal emphasis, affect, speech rate, pause density).                            |
| Video        | Frame/scene perception and on-screen-text OCR, plus the full audio sub-pipeline on the audio track. Emits visual signal (visual emphasis, scene-change density, framing markedness), on-screen text, and the audio outputs. |
| Image        | Scene perception and OCR where text is present. Emits visual signal (visual emphasis, composition markedness) and any recognised text.                                                                                      |
| Text         | Native text perception over documents, captions, and wire copy. Emits genre-form and stance signal (lexical intensity, stance intensity, hedging density).                                                                  |

7.2 Markers, not verdicts

Layer B emits markers — a source-attachment marker (is a claim
attributed and cited), a genre-form label (is the form a report, a
monologue, a performance) — that are detections, not verdicts. They are
inputs to the defensibility model (Part IV) and to Solva; Layer B never
assigns a defensibility class. This is the Mtafiti detect-versus-decide
boundary (§24) applied at the point of perception: perception detects;
the governed Matrix decides.

**In-tenancy perception is a hard invariant.** All Layer B perception
runs inside RMS tenancy on self-hosted models. Where external reasoning
is used (Part IX), it is reached only through the SyniSense inner gate
after de-identification, and the result is re-identified in-tenancy.
De-identified data remains personal data and never leaves on that basis;
only irreversibly transformed data crosses the outer gate (Part VIII).

8\. Layer C — Convergence

Layer C is where modality-native outputs become one comparable shape. It
normalises the parallel Layer B outputs into the modality-neutral
Five-Rings unit (Part III), so that a claim made in a video segment, a
radio call-in, and a wire report become units of the same kind,
comparable and composable. Service 1 terminates here: the Normalized
tier is the product of A→B→C.

8.1 What convergence does

-   **Normalise to the modality-neutral unit.** Each perceived claim
    becomes a Five-Rings unit whose content is modality-independent; the
    modality survives only in Provenance (Ring 1) and Signal (Ring 2).

-   **Build the rings.** Provenance and the Re-extraction Handle are
    computed deterministically; Signal descriptors are attached with
    Solva-judged depth; Relational edges are computed where
    corroboration, contradiction, or retraction is detectable across
    units.

-   **Stamp Ring 5.** The defensibility stamp is applied by the governed
    model (Part IV) — the claim-genre ceiling, the source-standing
    level, the score vector, the Matrix rule reference. A unit leaves
    convergence only with a complete Ring 5.

8.2 The Normalized tier

The Normalized tier is the durable store of converged units — the
substrate Layer D composes over in Service 2. It is modality-neutral,
defensibility-stamped, and relationally linked. Composition over the
tier does not re-extract: an objective is answered by composing existing
units, and A→B→C is invoked only where the tier lacks a needed unit.

9\. Layer D — the Extraction Orchestrator

Layer D composes intelligence over the Normalized tier to answer an
Objective Request. It exposes consumer-blind primitives and composes
them under Northena’s direction and Solva’s depth governance. It is the
only engine layer that is objective-shaped; A, B, and C are
objective-agnostic.

9.1 The primitives

Layer D’s primitives are consumer-blind — they compose the same way
regardless of where the result will go.

|               |                                                                                          |
|---------------|------------------------------------------------------------------------------------------|
| **Primitive** | **Composes**                                                                             |
| extract       | Retrieves the units relevant to the objective from the Normalized tier.                  |
| validate      | Checks units against corroboration and contradiction (Ring 3) to test a claim’s support. |
| forecast      | Projects from time-ordered units to a forward estimate.                                  |
| simulate      | Runs a scenario over the units to test an outcome.                                       |
| triangulate   | Cross-checks a claim across independent sources and modalities.                          |
| aggregate     | Composes many units into a summary or dataset.                                           |

9.2 Two axes of output

Layer D’s output has two axes. Output-form is Reasoned (a composed
conclusion, governed by Solva’s assertion boundary) or Packaged (a
dataset or a skill). Consumer-location is in-house or external, and
selects the delivery perimeter (§4) — in-house serving through the inner
gate, external through the inner gate for live intelligence or the outer
gate for file-out. The consumer-location selects the perimeter; it does
not change the extraction.

**Part III — The Five Rings (the Unit of Intelligence)**

10\. The Unit and Its Rings

Every unit of intelligence is a modality-neutral claim wrapped in five
metadata rings. The rings separate the deterministic and always-present
(Provenance, Re-extraction, the Defensibility stamp) from the judged
(Signal depth) and the relational (edges to other units). The unit is
the atom the whole system operates on: the engine produces it, the
governors reason over it, delivery wraps it. Its shape is frozen as
five_rings@v0; a unit without a complete Ring 5 is invalid and cannot
enter the Normalized tier.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>the unit — anchor + five rings (shape,
behavioural)</strong></p>
<p>Unit:</p>
<p>unit_id # stable identity</p>
<p>content # the modality-neutral assertion</p>
<p>provenance # where it came from (deterministic)</p>
<p>signal # modality-native descriptors, depth-judged</p>
<p>relational # typed edges to other units</p>
<p>reextraction_handle # deterministic means to reproduce the unit</p>
<p>defensibility # how defensibly it may be asserted (always
present)</p></td>
</tr>
</tbody>
</table>

**Where an illustrative block differs from the frozen contract, the contract prevails.** The frozen `NormalizedUnit` (backend/contracts/five_rings.py) uses these flat field names — `provenance`, `signal`, `relational`, `reextraction_handle`, `defensibility` — not ring-prefixed variants. Any older ring-numbered rendering in prose is illustrative-only and defers to the contract.

11\. Ring 1 — Provenance

Provenance is deterministic and always present. It records where a unit
came from, precisely enough to locate and reproduce it, and it carries
source-type metadata that the defensibility model reads at the feed
level.

|                   |                                                                                                                                    |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **Field**         | **Content**                                                                                                                        |
| source_file_ref   | The raw source the unit was extracted from.                                                                                        |
| modality          | The perception modality: text \| audio \| video \| image \| composite. This is the perception mechanism, not the source type.      |
| locator           | A modality-appropriate position: timestamp for audio/video, coordinate for image, offset for text.                                 |
| speaker_or_author | The identified speaker or author, where known.                                                                                     |
| capture_context   | Programme, feed_id (which keys the source-standing declaration), and source-type (e.g. that a unit originated from a social feed). |

**Source-type is provenance, not a modality.** A social-media post is,
by perception modality, text or video — “social” is its source type and
lives in the capture context, not in the modality enum. The modality
axis names how the unit was perceived; the source-type names where it
came from. Conflating them would corrupt the perception axis.

12\. Ring 2 — Signal (frozen: signal_ring_dimensions@v0)

The Signal ring carries modality-native descriptors whose depth Solva
judges. It measures observable, graded properties of the unit — how
emphatic, how marked, how hedged — as floats in \[0,1\]. Two rules are
binding and settle what the ring may and may not carry.

Signals measure markedness, not intent

A descriptor measures an observable property; it does not name an
inferred intent. “Framing markedness” is how deliberately framed a shot
is — a perception can score that; “framing intent” is a downstream
inference and is not a signal. Any descriptor that names an intent is
renamed to the markedness it actually measures. Intent, where it
matters, is inferred later by Solva or Layer D — never carried as a raw
signal.

Facts are not signals

A boolean fact — for example, that on-screen text is present — is not a
Signal dimension. Presence is Provenance or a Relational edge to an
OCR-derived unit; the Signal ring carries graded depth, not presence
flags. Forcing a boolean into a \[0,1\] dimension produces a meaningless
value and blurs the ring’s purpose.

|              |                                                                                     |
|--------------|-------------------------------------------------------------------------------------|
| **Modality** | **Dimensions (float \[0,1\], depth-judged)**                                        |
| Audio        | prosody, vocal_emphasis, affect_valence, affect_arousal, speech_rate, pause_density |
| Video        | visual_emphasis, scene_change_density, framing_markedness                           |
| Image        | visual_emphasis, composition_markedness                                             |
| Text         | lexical_intensity, stance_intensity, hedging_density                                |
| Composite    | no native dimensions — aggregates from constituent modalities                       |

The dimension set is frozen and versioned (signal_ring_dimensions@v0)
and extensible by re-bless: real perception may emit descriptors worth
adding, and the set revs by the snapshot mechanism rather than being
broken open.

13\. Ring 3 — Relational

The Relational ring is the estate graph. It carries typed edges from a
unit to other units, which is how the system represents that claims
support, dispute, or withdraw one another across the archive.

|               |                                                                        |
|---------------|------------------------------------------------------------------------|
| **Edge type** | **Meaning**                                                            |
| corroborates  | The unit supports a target unit’s claim.                               |
| contradicts   | The unit disputes a target unit’s claim.                               |
| retracts      | The unit withdraws a target unit’s claim (a correction, a retraction). |

**Edges are relations, not judgments.** An edge records that one unit
corroborates or retracts another, and points to the target unit and,
where it exists, an evidence reference. It carries no confidence scalar:
a confidence is an inference judgment, and judgment belongs to Solva’s
reasoning faculty, not to the graph layer. Solva’s Tension stage reads
these edges to surface contradiction and retraction — it does not
average them into a score.

14\. Ring 4 — the Re-extraction Handle (frozen: extraction_params@v0)

The Re-extraction Handle is the deterministic means to reproduce a unit
byte-identically: the raw pointer, the perception model and version, and
the extraction parameters. Its purpose is reproducibility, and the
parameter set is defined by what determines the output — not by what
merely identifies the run.

Output-determining, not run-identifying

Provider and version identify the run; the parameters that determine the
result are the mandatory set. For audio these include the sample rate,
the chunking, and the decoding parameters; for video the keyframe
strategy and interval plus the audio sub-block; for image the target
resolution and OCR engine; for text the source format and encoding.
These are mandatory-when-that-modality, because two runs identical on
provider and version but differing on chunking produce different units.

Determinism requires temperature = 0

A non-zero temperature makes extraction stochastic and cannot reproduce
byte-identically regardless of what else is pinned. The reproducibility
path requires temperature = 0; a non-zero run is flagged
non-reproducible-by-construction and is not silently compared.
Provider-specific parameters beyond the reproducibility set live in an
explicit provider-extras slot — declared, not hidden.

Timestamp is provenance, not reproducibility

The extraction time records when a run happened; it does not determine
the output and is excluded from the reproducibility comparison set. Two
runs identical but for their timestamps must reproduce identically; if
they do not, the non-determinism lies elsewhere and the timestamp must
not mask it.

15\. Ring 5 — Defensibility

The Defensibility ring is the integrity stamp, always present, and the
reason the system’s output is sellable: every unit is honest about how
defensibly it may be asserted. Its fields carry the model specified in
full in Part IV.

|                     |                                                                                                            |
|---------------------|------------------------------------------------------------------------------------------------------------|
| **Field**           | **Content**                                                                                                |
| defensibility_class | fact \| utterance \| non_factual — what the unit may be asserted as.                                       |
| claim_genre         | The genre that sets the ceiling (report, speech, opinion, advertisement, drama, call_in, documentary).     |
| source_standing     | The standing that sets the level under the ceiling (accountable, licensed wire, aggregator, UGC, unknown). |
| score_vector        | The graded components: genre_ceiling, source_standing, corroboration, recency_validity, contested.         |
| matrix_rule_ref     | The Qualification Matrix rule that produced the verdict — the auditability handle.                         |
| contested_status    | uncontested \| contested \| retracted — from the Relational graph.                                         |

**The unit and its audit are separate envelopes.** The unit is the
output of a stamp decision; the audit of that decision — why a stamp was
assigned, why a floor was refused — is a separate trace with a different
lifecycle. The unit schema is frozen; the audit trace evolves. Refusal
and decision reasons therefore live in a stamp-audit side-channel, not
on the unit; Northena’s Ledger absorbs them, joined by unit_id and
trace_id. The Defensibility ring stays byte-identical to its frozen
shape while the audit format is free to change.

**Part IV — The Defensibility Model**

16\. What Defensibility Is

The system does not judge truth. It measures how defensibly a claim may
be asserted, and it never presents a claim as more defensible than it
can be defended. Truth on a contested claim is not a machine judgment;
defensibility is — it is a function of the genre of the claim, the
standing of its source, its corroboration, its recency, and whether it
has been contested. This model is what makes the platform sellable: a
buyer receives intelligence that is honest about its own standing, and
the system can never be made to launder an opinion or a performance into
a fact.

17\. Two Axes, Never Collapsed

Defensibility is set by two axes that are held separate at every point
in the system. Collapsing them into a single score would allow authority
to launder genre — the precise failure the model exists to prevent.

|                     |                                                                         |                                                                                                                                                                  |
|---------------------|-------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Axis**            | **Sets**                                                                | **Rule**                                                                                                                                                         |
| **Claim-genre**     | The ceiling — the most a claim of this genre could ever be asserted as. | Authority-blind. A report can reach fact; a speech never exceeds ‘was stated’; an advertisement or drama is non-factual — regardless of how trusted the feed is. |
| **Source-standing** | The level beneath the ceiling.                                          | Can only lower, never raise. An unattributed UGC report does not become a fact because the report genre could reach fact — standing lowers it to utterance.      |

Worked consequences

-   **A political speech on the most trusted feed is utterance, not
    fact.** The genre ceiling for speech is ‘was stated’; no source
    standing raises it. The system can attribute the statement, never
    assert it as true.

-   **An advertisement read in an anchor’s voice is non-factual.** The
    genre ceiling for advertisement is non-factual; the anchor’s
    standing cannot lift it. Native advertising cannot be laundered into
    news.

-   **An unattributed ‘breaking’ post is utterance, not fact.** Report
    genre could reach fact, but UGC standing lowers it. The claim is
    carried as ‘was stated’ until corroborated by accountable sourcing.

18\. The Qualification Matrix (frozen: qualification_matrix@v0)

The Qualification Matrix is the governed taxonomy that maps a claim’s
genre and context to a defensibility verdict. It is the mechanism by
which the two axes produce a class. Three properties define it.

-   **Governed, not learned.** The Matrix is a versioned, inspectable
    table — not a model weight. Every verdict a unit carries is a Matrix
    lookup that records its rule reference (matrix_rule_ref), so every
    verdict is traceable to a governed rule and is auditable.

-   **Editorially owned.** The Matrix is owned and edited by the MEA
    (the editorial authority) through a versioned editor with an
    invariant-snapshot diff on every edit. The system ships the
    mechanism; the cell content is MEA-authored.

-   **Ceiling then level.** The lookup applies the genre ceiling first
    (authority-blind), then the source-standing level beneath it — never
    the reverse, and never merged.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>the verdict is a governed lookup, not a weight
(behavioural)</strong></p>
<p>verdict(claim_genre, context) -&gt; { defensibility_class,
matrix_rule_ref }</p>
<p># deterministic lookup over the governed table.</p>
<p># ceiling = genre_ceiling[claim_genre] (authority-blind)</p>
<p># level = lower_by_standing(ceiling, context.source_standing)</p>
<p># class = level (never raised by standing)</p>
<p># records matrix_rule_ref -&gt; every verdict is auditable to a
rule.</p></td>
</tr>
</tbody>
</table>

19\. The Two-Layer Measure

Defensibility is measured in two layers, so it scales across a
twenty-year estate without a per-item human bottleneck — the same
certain-baseline-plus-gated-refinement pattern the system uses
throughout. The layers are produced by Mtafiti (§24) and stamped by
Layer C.

|                          |                                                                                                                                                                                                                                                                                                                                      |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Layer**                | **Definition and status**                                                                                                                                                                                                                                                                                                            |
| **Declaration baseline** | RMS declares source-standing once per feed — accountable, licensed wire, aggregator, UGC, unknown. Low cardinality, stable, deterministic, always available. The certain floor the measure rests on. Declared at the feed level, never per item.                                                                                     |
| **Inference overlay**    | A learned signal refining the baseline from content — attachment markers, genre-form, cross-estate corroboration. Finer but softer: a prior, not a verdict. Emits detections only; the verdict remains the governed Matrix lookup. Admitted only on a V3 pass (Part VII); until then, and on any failure, the baseline stands alone. |

**Detect versus decide.** The learned overlay produces detections — an
attachment marker is present, the genre-form is monologic, a claim
recurs across the estate. It never produces a verdict. The verdict is
always the governed Matrix lookup over those detections. This keeps
defensibility auditable: if the learned layer assigned the class,
defensibility would rest on a model weight, which is the un-auditable
outcome the whole system rejects. Learning sharpens the inputs; the
governed Matrix makes the decision.

**Part V — The Governors and Engines**

20\. Three Governors, Three Orthogonal Axes

Three governors bound the system on three independent axes, and are
never collapsed — no governor performs another’s function. This section
specifies each governor and the two engines to full behavioural and
technical depth; module structure, typed contracts, and test obligations
for each live in the component’s own specification, of which this is the
parent.

|               |                     |                                                                                                      |
|---------------|---------------------|------------------------------------------------------------------------------------------------------|
| **Governor**  | **Axis**            | **Governs**                                                                                          |
| **SyniSense** | Boundary (in / out) | Whether data may cross an access point and in what transformed state.                                |
| **Northena**  | Direction           | Whether a run is in scope and whether it is done.                                                    |
| **Solva**     | Depth               | Whether reasoning is sound, preservation sufficient, and an output asserts within its defensibility. |

21\. SyniSense — the Boundary Governor

SyniSense governs every crossing between the protected estate and
anything outside it. It is two gates.

21.1 The inner gate

The inner gate governs calls to external reasoning. Before any external
model call it de-identifies the payload; on return it re-identifies
in-tenancy. It is fail-closed — a failure blocks the crossing rather
than leaking — and every crossing is audited with a receipt. Live
intelligence is served through the inner gate: the intelligence leaves
in a de-identified form and the identification is restored only inside
tenancy.

21.2 The outer gate

The outer gate governs file-out for external sale. It applies the
irreversibility transform (pseudonymisation with a purged mint,
k-anonymity / l-diversity / generalisation, optional
differential-privacy noise on numerics), validates rights past
extract-for-RMS (gate V2), and guards cumulative disclosure across
repeated file-outs so that successive releases cannot be recombined to
reconstruct identities. Only irreversibly transformed data crosses it.

**De-identified is not anonymised.** De-identified data — as passes the
inner gate — is still personal data and remains in-tenancy. Only
irreversibly anonymised data — as the outer gate produces — may egress
for sale. The two gates enforce two different thresholds, and the
distinction is a data-protection requirement (Part VIII), not an
implementation detail.

22\. Northena — the Direction Governor

Northena keeps every run on-objective, brings it to a defined stop, and
writes the audit-grade record of how it was directed. It is
deterministic by construction: it contains no model, no learned weight,
and no adaptive behaviour. Its behaviour varies run to run only because
the frozen governing artifact it reads varies — it is dynamic the way a
thermostat is dynamic, never by learning. Determinism is what makes it
auditable, and auditability is its purpose.

22.1 The four stages

|           |                                                                                                                                                                                                                                                                                                                                                                                 |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Stage** | **Behaviour**                                                                                                                                                                                                                                                                                                                                                                   |
| Admit     | Compiles a raw intent into the governing artifact (Portfolio Mandate or Objective Request) and freezes it. Validates deterministically: lawful_basis present, artifact complete, scope resolves against the Registry, floor well-formed. Where compilation needs judgment, it invokes Solva and freezes the returned value. Once frozen, the artifact is immutable for the run. |
| Gate      | Tests whether a (sub-)objective is within the frozen artifact’s scope — strict set-membership — and routes: warm-serve if already converged, fresh extraction if in scope and not converged, refuse (logged, not dropped) if out of scope. Ambiguous membership is an Admit-time compilation defect, never resolved by inference at Gate.                                       |
| Converge  | Decides termination on two conditions fixed in the artifact: done-condition met (terminate success) or budget exhausted (terminate budget); otherwise continue. Northena owns the halt — not the engine, not Solva.                                                                                                                                                             |
| Ledger    | Writes the durable, audit-grade record: admission, each Gate decision and reason, every refusal, the convergence decision, and the absorbed defensibility stamp-audit. Append-only; no run closes without a closed Ledger.                                                                                                                                                      |

22.2 The determinism boundary

Northena performs presence and completeness checks, set-membership
tests, threshold comparisons, and state transitions — all deterministic.
It performs no inference. Any decision requiring judgment is Solva’s:
Northena invokes Solva through an opaque handle and acts
deterministically on the returned value; it never reads Solva’s
reasoning and never reasons itself. The Ledger row is frozen as
northena_ledger_row@v0.

23\. Solva — the Depth Governor

Solva is the one governor that reasons — and therefore the one that
could do the most damage, because the system launders a claim precisely
when its strongest reasoning meets a defensibility ceiling. Solva is
specified as two faculties with a one-way seam between them: a reasoning
faculty that is free, and an assertion boundary that is bound.

23.1 The reasoning faculty (free)

The reasoning faculty is a five-stage pipeline; each stage is a genuine
judgment that no governed artifact dictates.

|             |                                                                                                                    |
|-------------|--------------------------------------------------------------------------------------------------------------------|
| **Stage**   | **Judgment**                                                                                                       |
| Frame       | Establishes the question and the relevant slice of the Normalized tier.                                            |
| Candidate   | Proposes the units and compositions that could answer it.                                                          |
| Tension     | Surfaces contradiction, corroboration, and retraction among candidates (reads Ring 3); does not average them away. |
| Probability | Weighs the candidates toward the best-supported conclusion.                                                        |
| Reflection  | Judges soundness and sufficiency, identifies the load-bearing units, and composes the conclusion.                  |

Identifying which units are load-bearing is part of this free judgment.
It is the reasoning faculty’s product and the only thing the assertion
boundary consumes from it — the units, never the confidence.

23.2 The assertion boundary (bound)

The assertion boundary determines what the conclusion may be asserted as
— its defensibility class — and it is mechanical, not a judgment. The
class is the floor over the load-bearing units’ classes, computed
without reasoning strength as an input.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>the assertion boundary — class is a floor, deaf to
reasoning strength</strong></p>
<p>conclusion_class(load_bearing_units) -&gt; class:</p>
<p># floor over the units' governed classes.</p>
<p># takes the units ONLY — no confidence, no evidence weight
parameter.</p>
<p>return min(class of u for u in load_bearing_units) #
non_factual&lt;utterance&lt;fact</p>
<p># an utterance-class conclusion is asserted as 'X was stated', never
as</p>
<p># fact, however overwhelming the evidence Solva finds. The laundering
case</p>
<p># is unrepresentable: the function has no parameter through which
reasoning</p>
<p># strength could raise the class.</p></td>
</tr>
</tbody>
</table>

**Solva chooses the units; it does not choose the class.** The reasoning
faculty decides which units are load-bearing — a genuine judgment. The
assertion boundary then computes the class as the floor over those units
— mechanically, with no confidence input. Solva reads the objective’s
floor and the Matrix verdict read-only and refuses below the floor with
a structured reason; it never sets or relaxes a governed value, and it
never extracts. Every extraction-time judgment produces a trace — the
reasoning path, the load-bearing units, the computed class — which is
what keeps a genuine reasoner auditable.

24\. Mtafiti — the Discovery and Measurement Engine

Mtafiti censuses the estate and writes the defensibility-measured
Registry. It is objective-blind: it measures the estate as it is, so one
Registry serves every objective. It discovers and measures; it does not
extract, target, or govern.

24.1 The census

The census walks the estate exhaustively and objective-blind, producing
one candidate record per source: its reference, region, feed identity
(which keys the declaration baseline), and a deterministic sensitivity
classification. No objective is consulted; one census serves all.

24.2 The measure and the detect-versus-decide boundary

The measure is the two-layer model of Part IV — the deterministic
declaration baseline, and the learned inference overlay (admitted only
on V3). Its guard is detect-versus-decide: the inference emits
detections (attachment markedness, genre-form, corroboration) and never
a verdict; the defensibility class is the governed Matrix lookup over
those detections, recording its rule reference. The inference module
never imports the verdict logic — the boundary is a dependency rule, not
a runtime check.

24.3 The Registry and freshness

Mtafiti writes one Registry record per source — existence, sensitivity,
the defensibility measure, the runtime mode (baseline or overlay), and a
freshness stamp. The Registry is the objective-blind substrate Targeta
and Layer C read. Freshness is a deterministic two-level check (a logged
date and a structural-delta signature); a detected change drives scoped
re-discovery of only the affected region, re-running the measure —
including a changed contested_status when a retraction appears.

25\. Targeta — the Targeting Engine

Targeta reads the defensibility-measured Registry and decides where to
mine and in what order, so an objective is served as fully as possible
within budget. It is two layers with a one-way relationship, and it is
the one component permitted to learn — bounded so that learning can
improve targeting and can never narrow what the objective may reach.

25.1 The deterministic eligibility core

The core reads the Registry and the governing artifact and produces the
eligible set and a baseline ranking. It applies the objective’s
defensibility floor as a hard filter (a source that cannot meet the
floor is not eligible), weights the eligible set by objective relevance
and Registry defensibility, and ranks by a fixed, inspectable function.
It contains no model; Targeta on the core alone is a complete, correct
targeter.

25.2 The objective-conditioned yield layer

The yield layer learns which sources satisfy which kinds of objective
and reorders the already-eligible candidates by expected
objective-yield. It is bounded by construction: it receives only the
floor-passing eligible set (never the floor value, the raw measure, or
the eligibility logic) and returns a permutation of that exact set. A
non-permutation output — dropping or adding a source — is a type error,
rejected by the interface, not a ranking to review.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>the eligibility guard — yield may only reorder
(behavioural)</strong></p>
<p>apply_yield(eligible, yield_fn) -&gt; ordered:</p>
<p>yin = strip(eligible) # floor + raw measure removed; source_refs +
features only</p>
<p>order = yield_fn(yin) # the learned reorderer</p>
<p>assert set(order) == set(eligible.refs) # non-permutation -&gt; type
error</p>
<p>return eligible reordered by order</p>
<p># learning improves the order; it can never change what is
eligible.</p></td>
</tr>
</tbody>
</table>

25.3 The two-arm admission gate

The yield layer is admitted only through a gate with two arms, the
second a veto. Arm 1 (helps): on held-out past objectives, the yield
ordering reaches objective-satisfaction in fewer mined units than the
core. Arm 2 (coverage veto): across estate classes, the yield layer must
not drive any eligible class below the core’s coverage for objectives it
is eligible to satisfy — improving efficiency by starving a class fails
the gate regardless of the efficiency number. On failure of either arm,
Targeta runs on the deterministic core. The gate thresholds are
owner-signed (Part VII / §30).

**Part VI — Frozen Contracts**

26\. The Frozen Contract Set

The founding set of frozen contracts numbered six; the set is extensible by addition (never mutation). The canonical registry is the CI-checked contract manifest under `/app/backend/contracts/` with corresponding invariant snapshots under `/app/backend/tests/invariants/`. Each contract is a schema, a JSON snapshot, and an invariant test; drift fails CI. Everything downstream binds to the contracts, and they change only by an explicit, versioned re-bless — never to accommodate a fixture, a prep sketch, or a convenience. A change that looks additive and free, such as an optional field on an existing contract, is still a mutation and is held to the same bar, because everything bound to the contract must be able to trust its shape. Adding a *new* frozen contract to the registry is not a mutation of any existing one and is governed by the same freeze discipline (schema + snapshot + invariant test) applied to the addition.

|                           |                                                                                                                                                       |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Contract**              | **Governs**                                                                                                                                           |
| five_rings@v0             | The unit shape — anchor plus the five rings. The core Normalized-tier contract; a unit without a complete Ring 5 is invalid.                          |
| objective_request@v0      | The Service 2 request — objective, defensibility floor, provenance requirement, scope, lawful basis. What Northena.Admit freezes.                     |
| qualification_matrix@v0   | The governed genre × context → verdict taxonomy. MEA-editable, versioned; every verdict records its rule reference.                                   |
| signal_ring_dimensions@v0 | The per-modality Signal dimension set — markedness not intent, no presence booleans, composite carries none. Versioned, extensible by re-bless.       |
| extraction_params@v0      | The reproducibility parameter set — output-determining keys mandatory-by-modality, temperature=0 for deterministic re-extraction, timestamp excluded. |
| northena_ledger_row@v0    | The audit-grade Ledger row — append-only, the DPO / audit-lens surface, absorbs the defensibility stamp-audit from build phase G2.                    |

**Contract-first hierarchy.** The frozen contracts are the source of
truth. Test fixtures, prep sketches, and convenience shapes conform to
the contracts — never the reverse. A fixture that disagrees with a
contract is the fixture’s defect, corrected by regenerating it against
the contract, not a licence to re-bless the contract. Re-blessing is
reserved for genuine design change, versioned and deliberate.

**Part VII — Validation Gates**

27\. Three Gates Against Reality

Three gates validate the system against reality rather than against its
own assumptions. Each has a certain fallback that does not depend on the
gated capability, so a gate failure narrows scope rather than blocking
the system. Two of the three (V1 and V3) require real RMS material and
cannot pass on synthetic data: accuracy measured against author-labelled
synthetic data is circular by construction — synthetic data proves the
pipeline runs, never that it works.

28\. V1 — Convergence Quality

V1 gates the perception-compute commitment: does the engine produce
sound Five-Rings intelligence from real broadcast material. It is run on
a real broadcast hour, with the production hour held out from any hour
used to tune the engine — validating on the tuning hour would confirm
only what was tuned for.

|                                   |                                                                                                                                                                      |
|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Metric**                        | **Bar**                                                                                                                                                              |
| Transcription WER (vs human gold) | ≤ 18% — the working bar; Kenyan-broadcast code-switching is the operating reality, not an edge case.                                                                 |
| Diarization DER (speakers ≥ 30s)  | ≤ 18%; sub-30s speakers may merge.                                                                                                                                   |
| Named-entity recall               | Measured twice: against the clean gold transcript (the gate, ≥ 85%) and against the ASR output (reported, to show how much transcription error degrades extraction). |
| Five-Rings completeness           | ≥ 95% on Provenance / Re-extraction / Defensibility; ≥ 80% on Signal; Relational tracked, not gated.                                                                 |
| Runtime                           | ≤ 4× realtime on the chosen compute.                                                                                                                                 |
| Defensibility distribution        | Reported, not gated — an opinion-dominant hour should score as such; a distribution bar would fail a correct system and pass a broken one.                           |

On failure: halt the perception-compute commitment, change the model
class or narrow modality coverage, and re-run on the same hour. Do not
advance downstream on a broken engine.

29\. V2 — Rights and Substrate; V3 — Defensibility Detection

29.1 V2 — Rights and Substrate

V2 gates the outer-gate file-out. It confirms rights past
extract-for-RMS, resolves the substrate/rights contract, verifies a
sample file-out cryptographically, and demonstrates the
cumulative-disclosure guard refusing a reconstruction attempt. Until V2
passes, delivery is inner-gate-only — live intelligence in-tenancy —
which is a complete service on its own.

29.2 V3 — Defensibility Detection

V3 gates the inference overlay of the defensibility measure. It is run
on a real labelled slice: at least 300 units, at least four genres, two
labellers plus an adjudicator, with inter-annotator agreement κ ≥ 0.70
computed before any model accuracy — if the labellers do not agree, no
accuracy against their labels means anything.

|                                  |                                                                                                                                      |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| **Metric**                       | **Bar**                                                                                                                              |
| fact-class precision             | ≥ 90% — the gate. A false fact is the catastrophic error; a missed fact degrades safely to utterance. Precision gates, not accuracy. |
| Genre-classification accuracy    | ≥ 80% (top-1).                                                                                                                       |
| utterance-vs-fact disambiguation | ≥ 85%.                                                                                                                               |
| non_factual precision            | ≥ 95%.                                                                                                                               |

On failure: keep the declaration baseline live, do not admit the
inference overlay, surface the state, and re-attempt when more labelled
data and a better detector are both ready. The baseline is a complete
measure on its own.

**Part VIII — Data Protection, Invariants, Open Governance**

30\. Data Protection (Kenya DPA, 2019)

The system is designed to the Kenya Data Protection Act, 2019. The
following are design constraints, not a legal opinion.

-   **De-identified is still personal data.** It stays in-tenancy; only
    irreversibly anonymised data may egress via the outer gate.

-   **Purpose limitation at admission.** Northena enforces a valid
    lawful_basis at Admit; no run proceeds without one, and purpose
    limitation is enforced before any extraction.

-   **Controller and processor.** RMS is the controller; Syni is the
    processor. Registration, a DPIA, and breach-notification timelines
    apply.

-   **Data-subject rights and retention.** The Northena Ledger retention
    duration and end-of-window rule are a DPO determination; until
    confirmed, the build defaults to append-only immutability with
    configurable, indefinite retention (§32).

31\. System Invariants

Binding across the whole system. Any implementation that violates one is
incorrect regardless of behaviour.

1.  Every unit of intelligence carries a complete Ring 5 defensibility
    stamp; a unit without one is invalid and cannot enter the Normalized
    tier.

2.  Defensibility is set by two axes never collapsed: claim-genre sets
    the ceiling (authority-blind); source-standing sets the level and
    can only lower, never raise.

3.  The defensibility verdict is a governed Qualification Matrix lookup
    recording its rule reference — never a learned model weight.

4.  In each engine, the powerful part is walled by construction from the
    governed decision it must not touch: Northena’s dynamism from
    auditability, Targeta’s learning from eligibility, Mtafiti’s
    inference from the verdict, Solva’s reasoning from the assertion
    ceiling. The violation is unrepresentable, not merely disallowed.

5.  The three governors operate on orthogonal axes and are never
    collapsed; no governor performs another’s function.

6.  The frozen contract registry is the source of truth. Fixtures and
    convenience shapes conform to it; any contract in the registry
    changes only by explicit versioned re-bless; the registry itself
    is extended by addition (see §26).

    **Authoring-direction convention (post-2026-07-02):** the canonical
    source for every filed mandate is the markdown at
    `/app/docs/mandates/*.md`. The `.docx` at `/app/docs/mandates/source/`
    are generated presentation artefacts, retained for provenance only.
    `MANIFEST.md` SHA-256s hash the `.md`; the substrate-drop gate
    reads and re-hashes the `.md`. Citable anchors going forward are
    markdown `§`-anchors, not `.docx` page/paragraph references. See
    `MANIFEST.md` preamble for the load-bearing statement.

7.  The unit (output) and its audit (trace) are separate envelopes with
    separate lifecycles; the Defensibility ring stays byte-identical
    while the audit trace evolves.

8.  All Layer B perception runs in-tenancy; external reasoning is
    reached only through the inner gate after de-identification; only
    irreversibly transformed data crosses the outer gate.

9.  Signals measure markedness, not intent; a boolean fact is Provenance
    or a Relational edge, never a Signal dimension.

10. Reproducible re-extraction is deterministic (temperature = 0); the
    reproducibility set contains only output-determining parameters, and
    excludes the extraction timestamp.

11. Northena is deterministic — no model, no learning; any decision
    requiring inference is Solva’s, invoked through an opaque handle and
    acted on deterministically.

12. No run proceeds without a valid lawful basis admitted by Northena;
    no run closes without a closed, audit-grade Ledger.

13. V1 and V3 pass only on real RMS material; accuracy against
    author-labelled synthetic data is circular and never constitutes a
    pass.

14. Each gate has a certain fallback that does not depend on the gated
    capability, so a gate failure narrows scope rather than blocking the
    system.

32\. Open Governance Decisions

Decisions owned outside the build, each with a certain default so none
blocks construction of the parts that do not depend on it.

|                                                                      |               |                                                                                          |
|----------------------------------------------------------------------|---------------|------------------------------------------------------------------------------------------|
| **Decision**                                                         | **Owner**     | **Default / status**                                                                     |
| Northena Ledger retention duration + end-of-window rule              | DPO           | Append-only immutability, configurable retention. Not a build blocker.                   |
| Targeta yield-gate thresholds                                        | Project owner | Gates the yield layer only; the deterministic core ships without them.                   |
| Mtafiti V3 thresholds (shared with the V3 gate)                      | Project owner | Gates the inference overlay only; the census and baseline ship without them.             |
| MEA source-standing declaration table + Qualification Matrix content | MEA           | Populates the baseline and the Matrix; the mechanism ships, the content is MEA-authored. |

**Status.** This is the canonical parent specification. It states the
system to full technical and behavioural depth and prevails over any
engine specification on conflict. The four engine specifications carry
each component’s module structure, typed contracts, and test
obligations, consistent with this document. Where a build meets a case
this document does not resolve, it attempts a defensible reading
consistent with the invariants (§31), records it, and surfaces it; it
does not freeze an unconfirmed rule.

---

## Closed Seam — Unlock: V2 Cumulative-Disclosure Arm

The V2 single-packet refusal arm is LIVE; the cumulative-disclosure arm (repeated file-outs) is BUILT and GATED. `services/v2_gate/cumulative.py::cumulative_arm_admitted()` returns `False` when any of the three env vars is unset or unparseable (`cumulative.py:27-50`), holding the arm closed. Per §21.2 (k-anonymity / l-diversity / DP-noise primitives) + §29.1 ("Until V2 passes") + §32 (DPO-owned).

- **Owner:** Data Protection Officer (DPO-signed decision required).
- **Config keys (env vars, verbatim from `services/v2_gate/cumulative.py:40-42`):**
  - `RMS_G6_K_ANONYMITY_THRESHOLD` — integer, minimum group size (k in k-anonymity, §21.2).
  - `RMS_G6_L_DIVERSITY_THRESHOLD` — integer, minimum distinct-value count within a group (l in l-diversity, §21.2).
  - `RMS_G6_DP_EPSILON_BUDGET` — float, cumulative DP epsilon budget (§21.2).
  All three must parse and cross zero-value guards for `cumulative_arm_admitted()` to return True.
- **Unlock procedure:**
  1. DPO decides threshold values.
  2. Set env vars at container/deployment layer:
     ```
     RMS_G6_K_ANONYMITY_THRESHOLD=5
     RMS_G6_L_DIVERSITY_THRESHOLD=3
     RMS_G6_DP_EPSILON_BUDGET=1.0
     ```
  3. Restart backend for cache coherence (env is read at request time; no restart strictly required).
  4. `cumulative_arm_admitted()` returns True; the load-bearing arm becomes live.
- **Behavioral delta when opened:** V2 refusal envelope gains a new reason code path — `cumulative_disclosure_risk` — defined at G6 for exactly this unlock. Individually-clean egresses that re-combine to reconstruct identities get refused when the k-anonymity or l-diversity threshold is crossed, or when the DP epsilon budget is exhausted. The V2 tracking store begins persisting egress fingerprints across sessions.
- **Test that proves it opened:** the closed-seam invariant at `test_v2_gate_refusal_cumulative.py` (region ~L105-137) asserts `cumulative_arm_admitted() is False` when env vars unset. A LOAD-BEARING unlock-simulation test at the same file (region ~L144+) monkey-patches all three env vars and asserts `True` — already green in closed-state and becomes an end-to-end guarantee at real unlock. Optional additions: `test_cumulative_arm_refuses_at_k_threshold`, `test_cumulative_arm_epsilon_budget_exhaustion_refuses`. Consolidated in `/app/docs/handoff/seam_unlock_runbook.md` (Seam 5).
