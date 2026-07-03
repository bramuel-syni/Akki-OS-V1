**Mtafiti**

The Discovery & Measurement Engine — Engine Specification

The complete specification of the discovery and
defensibility-measurement engine: the objective-blind census, the
two-layer measure, the detect-versus-decide boundary enforced as a
dependency rule, the governed Registry, and the module structure, typed
contracts, algorithms, and test obligations that implement them.

Engine Specification · Version 1.0 · elaborates the Product &
Engineering Specification v2.1 (§24), which prevails on conflict.

*Prepared by Syni.ai · July 2026 · Confidential*

This document is binding. Part I states what Mtafiti must do and why;
Part II specifies how it is built — modules, typed contracts, the census
and measure algorithms, the detect-versus-decide boundary, and the test
obligations; Part III states governance, invariants, and the open
threshold decisions. It is a forward specification: it defines what must
be true of any correct implementation. Mtafiti’s defensibility structure
— a deterministic declaration baseline, a learned inference overlay, and
a governed verdict — is settled by the defensibility model (parent
§16–§19); this document specifies it. Points marked **CONFIRM** resolve
against the real contract before use.

**Contents**

**Part I — Mandate**

1\. What Mtafiti Is

Mtafiti is the discovery engine. It censuses the estate exhaustively and
writes the Registry: what exists, at what sensitivity, and how
defensible each source is. It is objective-blind — it measures the
estate as it is, without reference to any particular objective — so that
Targeta and Layer C read one measure that serves every objective. It
discovers and measures; it does not extract, target, or govern. It runs
at estate standup and is maintained thereafter by a freshness mechanism.

2\. The Anchor

Every rule is judged against one anchor: what makes Mtafiti do its job
better, in service of the extraction objective.

|                                       |                                                                                                                                                                                                         |
|---------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Half**                              | **What it demands**                                                                                                                                                                                     |
| **Does the job better**               | Produce a defensibility measure discriminating enough to prioritise extraction and floor composition, at the scale of a twenty-year estate, without a per-item human bottleneck.                        |
| **Services the extraction objective** | Never overstate standing. The measure is a targeting and flooring prior, not a truth verdict; it must never make a claim look more defensible than it can be defended, and it must fail toward caution. |

**What Mtafiti measures, and does not.** Mtafiti measures how defensibly
a source can be relied upon — set by claim-genre, source-standing,
corroboration, recency, and contested status. It does not judge whether
a claim is true; truth on contested claims is not a machine judgement.
The measure targets and floors; it never certifies.

3\. The Two-Layer Measure

The defensibility measure is produced in two layers so it scales across
a twenty-year estate without labelling every item by hand.

|                               |                                                                                                                                                                                                                                                                    |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Layer**                     | **Definition**                                                                                                                                                                                                                                                     |
| **Declaration baseline**      | RMS declares source-standing once per feed — accountable, licensed wire, aggregator, UGC, unknown. Low cardinality, stable, deterministic, always available. The volume-safe floor, declared at the feed level, never per item.                                    |
| **Content inference overlay** | A learned signal refining the baseline from content — source-attachment markers, genre-form, cross-estate corroboration. Finer but softer: a prior, not a verdict. Admitted only when its detection accuracy is proven (V3); until then the baseline stands alone. |

4\. Detect versus Decide — the Boundary

The inference overlay is learned, and the single rule that keeps
learning from laundering authority into the measure is this: the learned
component produces detections, never verdicts. It detects signals — a
source-attachment marker is present, the genre-form is monologic, a
claim recurs across the estate. The defensibility verdict — what a unit
is permitted to assert — is assigned by the Qualification Matrix, a
governed, versioned, inspectable taxonomy, by deterministic lookup.
Learning detects; the governed Matrix decides; the declaration baseline
floors; the V3 gate admits.

**Why the boundary holds.** If the learned layer assigned the verdict,
defensibility would rest on a model weight — unexplainable and
un-auditable, the very laundering the system exists to prevent. Because
the verdict is a Matrix lookup over detected signals, every verdict is
traceable to a governed rule (matrix_rule_ref), and the detections it
consumed are recorded. Learning can sharpen the inputs; it can never be
the decision.

5\. The Registry

Mtafiti writes the Registry: one record per source, carrying existence,
sensitivity, the defensibility measure, and a freshness stamp. The
Registry is the interface Targeta and Layer C read — objective-blind, so
a single measure serves every objective. It is maintained by the
freshness mechanism: a logged-date and a structural-delta check drive
scoped re-discovery of only the affected region, re-running the measure
for that region (a new retraction changes contested status).

6\. Calibration — What the Measure Is

The inferred measure is a targeting and flooring prior, not a truth
verdict. It is strong enough to prioritise extraction and floor
composition, and not strong enough to certify truth — and it is not
asked to. It fails gracefully: a mis-scored source means mining in
slightly the wrong order, because Solva still enforces the genre-ceiling
on what any unit may assert, and the declaration baseline still floors.
Reliance on the inferred overlay is gated by V3; the declaration
baseline and the governed verdict do not depend on it.

**Part II — Engineering Specification**

7\. Module Structure and Dependency Rules

Mtafiti is a census walker, a two-layer measurer, and a Registry writer.
The dependency direction encodes the detect-versus-decide boundary: the
inference module emits detections and never imports the verdict logic;
the verdict is a deterministic Matrix lookup.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>services/mtafiti/ — module layout</strong></p>
<p>services/mtafiti/</p>
<p>census.py # estate walk; enumerates sources; objective-blind</p>
<p>declaration.py # feed-level source-standing baseline
(deterministic)</p>
<p>inference.py # learned detectors: attachment / genre-form /
corrob.</p>
<p>measure.py # composes baseline + detections -&gt; score_vector</p>
<p>verdict.py # Qualification Matrix lookup -&gt;
defensibility_class</p>
<p>registry.py # append/update Registry records; freshness</p>
<p>interfaces.py # opaque handles (MatrixHandle) — boundary types</p>
<p>contracts/</p>
<p>registry_record.py # frozen: RegistryRecord (snapshot +
invariant)</p>
<p>routers/</p>
<p>mtafiti.py # census status + registry read API</p></td>
</tr>
</tbody>
</table>

Dependency rules (enforced by import assertion)

-   **inference.py emits detections only.** It never imports verdict.py
    and never assigns a defensibility_class — the boundary is a
    dependency rule.

-   **verdict.py reads the frozen Qualification Matrix through an opaque
    handle** and performs a deterministic lookup. It contains no model.

-   **declaration.py is deterministic and always available;** measure.py
    composes it with detections so the baseline stands alone when the
    overlay is not admitted.

8\. The Census

The census walks the estate exhaustively and objective-blind, producing
one candidate source record per discovered source. It classifies
sensitivity and attaches the feed identity that keys the declaration
baseline. It enumerates and classifies; measurement follows.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>census.py — exhaustive, objective-blind
enumeration</strong></p>
<p>def census(estate) -&gt; Iterator[SourceCandidate]:</p>
<p>for source in estate.walk(): # CONFIRM: estate walk iface</p>
<p>yield SourceCandidate(</p>
<p>source_ref=source.ref,</p>
<p>region=source.region,</p>
<p>feed_id=source.feed_id, # keys the declaration baseline</p>
<p>sensitivity=classify_sensitivity(source)) # deterministic</p>
<p># objective-blind: no objective is consulted. One census serves
all.</p></td>
</tr>
</tbody>
</table>

9\. The Declaration Baseline

The declaration baseline reads RMS’ per-feed source-standing declaration
and applies it to every source under that feed. It is deterministic,
low-cardinality, and always available — the certain floor the whole
measure rests on. It is never assigned per item.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>declaration.py — feed-level, deterministic, always
available</strong></p>
<p>def declared_standing(feed_id, declaration_table) -&gt;
SourceStanding:</p>
<p># feed-level lookup; low cardinality, stable, estate-wide.</p>
<p># accountable | licensed_wire | aggregator | ugc | unknown</p>
<p>return declaration_table.get(feed_id, SourceStanding.UNKNOWN)</p>
<p># CONFIRM: declaration_table + SourceStanding enum against the</p>
<p># MEA-owned feed declaration and five_rings@v0.</p></td>
</tr>
</tbody>
</table>

10\. The Inference Overlay — Detections Only

The inference overlay detects defensibility signals in the content —
whether a report attributes and cites (source-attachment), whether the
genre-form is event-anchored or monologic, whether a claim corroborates
across independent estate units. It emits detections with confidences.
It never emits a verdict, and it never receives the verdict logic or the
Matrix.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>inference.py — emits detections, never a
verdict</strong></p>
<p>@dataclass(frozen=True)</p>
<p>class Detections: # the ONLY thing inference emits</p>
<p>attachment_markedness: float # [0,1] cited / attributed</p>
<p>genre_form: str # detected form label (not a verdict)</p>
<p>corroboration: float # [0,1] cross-estate recurrence</p>
<p>confidences: Mapping[str, float]</p>
<p>def detect(source, estate_index) -&gt; Detections:</p>
<p># learned detectors. emits signals only.</p>
<p># MUST NOT import verdict.py; MUST NOT assign
defensibility_class.</p>
<p>... # CONFIRM: detector model(s) chosen at build; this spec fixes</p>
<p># the CONSTRAINT (detections only), not the architecture.</p></td>
</tr>
</tbody>
</table>

11\. Compose and Decide — the Governed Verdict

The measure composes the deterministic baseline and the (admitted)
detections into a score vector, and the verdict is assigned by a
deterministic Qualification Matrix lookup over claim-genre and context.
The verdict records the Matrix rule that produced it; the detections it
consumed are recorded alongside. When the overlay is not admitted, the
composition uses the baseline alone.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>measure.py + verdict.py — governed lookup, not a model
weight</strong></p>
<p>def measure(cand, standing, detections, v3_admitted) -&gt;
ScoreVector:</p>
<p>return ScoreVector(</p>
<p>source_standing=standing, # deterministic</p>
<p>attachment=detections.attachment_markedness if v3_admitted else
0.0,</p>
<p>corroboration=detections.corroboration if v3_admitted else 0.0,</p>
<p>recency_validity=recency(cand), # deterministic</p>
<p>contested=contested_status(cand)) # deterministic</p>
<p>def assign_verdict(claim_genre, context, matrix: MatrixHandle) -&gt;
Verdict:</p>
<p>rule = matrix.lookup(claim_genre, context) # deterministic lookup</p>
<p>return Verdict(defensibility_class=rule.verdict, #
fact|utterance|non_factual</p>
<p>matrix_rule_ref=rule.ref) # auditable</p>
<p># learning detected the inputs; the governed Matrix decides the
class.</p></td>
</tr>
</tbody>
</table>

**The boundary as code.** inference.detect emits Detections;
verdict.assign_verdict is a Matrix lookup. The two never merge: the
learned layer cannot import the verdict logic, and the verdict is a
deterministic lookup carrying its rule reference. Every
defensibility_class is traceable to a governed rule, and reliance on the
detections is gated (§12).

12\. The V3 Admission Gate

The inference overlay is admitted only when its detection accuracy is
proven on real RMS content. Until it passes, the measure runs on the
declaration baseline alone, and the Registry records that state.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>V3 admission — baseline stands until detection is
proven</strong></p>
<p>def overlay_admitted(v3_result) -&gt; bool:</p>
<p># on a labelled real slice:</p>
<p># fact-class precision &gt;= gate, genre accuracy &gt;= gate,</p>
<p># inter-annotator kappa &gt;= floor before accuracy is computed.</p>
<p>return (v3_result.fact_precision &gt;=
v3_result.thresholds.fact_precision</p>
<p>and v3_result.genre_accuracy &gt;=
v3_result.thresholds.genre_accuracy)</p>
<p># if not admitted: measure() uses baseline-only; registry marks</p>
<p># defensibility_runtime_mode = 'declaration_baseline'.</p></td>
</tr>
</tbody>
</table>

13\. The Registry Record and Freshness

Mtafiti writes one Registry record per source — a frozen contract,
snapshot plus invariant. Freshness is a deterministic two-level check
that drives scoped re-discovery and re-measurement of only the affected
region.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>contracts/registry_record.py — the frozen
record</strong></p>
<p>@dataclass(frozen=True)</p>
<p>class RegistryRecord: # frozen: snapshot + invariant</p>
<p>source_ref: str</p>
<p>region: str</p>
<p>feed_id: str</p>
<p>sensitivity: str</p>
<p>defensibility_measure: ScoreVector # baseline + (admitted)
detections</p>
<p>defensibility_runtime_mode: str # 'declaration_baseline' |
'overlay'</p>
<p>freshness_stamp: FreshnessStamp # { logged_date, structural_sig }</p>
<p># CONFIRM: ScoreVector + FreshnessStamp against
five_rings@v0.</p></td>
</tr>
</tbody>
</table>

Freshness: a logged-date (L1) and a structural-delta check (L2) detect
change; a detected change drives scoped re-discovery of the affected
region only, re-running the measure — including a changed
contested_status when a retraction appears.

14\. Interfaces and Test Obligations

Interfaces

|                              |               |                                                                                                              |
|------------------------------|---------------|--------------------------------------------------------------------------------------------------------------|
| **Interface**                | **Direction** | **Shape / status**                                                                                           |
| Estate → census              | in            | Exhaustive walk of the estate. CONFIRM the walk interface.                                                   |
| Feed declaration → baseline  | in            | MEA-owned per-feed source-standing table. CONFIRM against the declaration artifact.                          |
| Matrix → verdict             | in            | Qualification Matrix via opaque MatrixHandle; deterministic lookup. CONFIRM against qualification_matrix@v0. |
| Mtafiti → Registry           | out           | RegistryRecord (frozen). The measure Targeta and Layer C read.                                               |
| Registry → Targeta / Layer C | out           | Objective-blind read: one measure serves every objective.                                                    |

Test obligations

|                                   |                                                                                                                        |
|-----------------------------------|------------------------------------------------------------------------------------------------------------------------|
| **Test**                          | **Asserts**                                                                                                            |
| test_inference_emits_no_verdict   | inference.py never imports verdict.py and never returns a defensibility_class (structural + import assertion).         |
| test_verdict_is_matrix_lookup     | Every verdict carries a matrix_rule_ref resolving to a governed Matrix rule; no learned weight assigns the class.      |
| test_baseline_stands_alone        | With the overlay not admitted, measure() uses the declaration baseline only and the record marks declaration_baseline. |
| test_census_objective_blind       | The census consults no objective; one census output serves all objectives.                                             |
| test_registry_record_frozen       | RegistryRecord conforms to its snapshot; a schema change fails CI.                                                     |
| test_freshness_scoped_rediscovery | A structural delta re-measures only the affected region, not the estate.                                               |

15\. Construction Requirements

1.  **Registry record first, contract-grade.** Freeze the RegistryRecord
    (snapshot + invariant) before the measure writes to it — it is the
    interface Targeta and Layer C bind to.

2.  **Baseline before overlay.** Build the census and the deterministic
    declaration baseline first; Mtafiti is complete and correct on the
    baseline alone.

3.  **Detect-versus-decide as construction.** inference emits detections
    and cannot import the verdict; the verdict is a Matrix lookup
    carrying its rule reference. Enforced by import assertion.

4.  **Overlay gated on V3.** Admit the inference overlay only on a
    real-material V3 pass; until then the baseline stands and the
    Registry records the mode.

**Part III — Governance, Invariants, Open Decisions**

16\. Governance and Compliance

-   **Objective-blind by mandate.** Mtafiti measures the estate as it
    is; it consults no objective, so one Registry serves every objective
    without bias toward any.

-   **The verdict is governed and auditable.** Every defensibility_class
    carries the Matrix rule that assigned it; the measure is
    inspectable, not a hidden model output.

-   **Sensitivity classification precedes measurement.** The census
    classifies sensitivity so downstream handling honours the Kenya DPA
    constraints; the Registry is an index, not a content store.

17\. Invariants

Binding. Any implementation that violates one is incorrect regardless of
behaviour.

1.  Mtafiti discovers and measures; it does not extract, target, or
    govern. The census is exhaustive and objective-blind.

2.  The defensibility measure is two-layer: a deterministic feed-level
    declaration baseline, and a learned content inference overlay. The
    baseline is always available and stands alone when the overlay is
    not admitted.

3.  The inference overlay emits detections only. It never assigns a
    defensibility verdict and never imports the verdict logic.

4.  The defensibility verdict is assigned by the Qualification Matrix by
    deterministic lookup, and records the rule that produced it
    (matrix_rule_ref). No learned weight assigns a verdict.

5.  The measure is a targeting and flooring prior, not a truth verdict;
    it fails toward caution. Reliance on the inference overlay is gated
    by V3; the baseline and the governed verdict do not depend on it.

6.  Source-standing is declared once per feed — low cardinality, never
    per item.

7.  The Registry record is a contract-grade artifact — versioned,
    snapshot-and-invariant — and records the defensibility runtime mode
    (baseline or overlay).

8.  Freshness re-measures only the affected region on a detected
    structural change, never the whole estate silently.

9.  Mtafiti is objective-blind: one measure serves every objective; it
    never conditions the measure on a particular objective.

18\. Open Decisions

|                                                                                |                                         |                                                                                                                                   |
|--------------------------------------------------------------------------------|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| **Decision**                                                                   | **Owner**                               | **Blocks**                                                                                                                        |
| V3 admission thresholds: fact-precision, genre-accuracy, inter-annotator floor | Project owner (shared with the V3 gate) | Admission of the inference overlay only. Not a blocker for the census or the declaration baseline, which ship and run without it. |
| Feed source-standing declaration table                                         | MEA                                     | Population of the baseline. The mechanism ships; the declared values are MEA-owned content.                                       |

**Status.** This specification is complete. Every structural rule — the
objective-blind census, the two-layer measure, the detect-versus-decide
boundary as an import rule, the governed Matrix verdict, the V3-gated
overlay with a baseline that stands alone — is settled. The open items
are the V3 thresholds (shared with the V3 gate) and the MEA-owned feed
declaration content; neither blocks the census or the baseline. Points
marked CONFIRM resolve against the real contract; a shape that cannot be
confirmed is recorded, not inferred.

---

## Closed Seam — Unlock: V3 Overlay Thresholds

The V3 inference overlay is BUILT and GATED. `services/mtafiti/v3_overlay.py::overlay_admitted(thresholds, v3_result) → False` when `thresholds is None`; Registry composition passes `v3_admitted=False` into `measure()` and the declaration_baseline runtime_mode dominates.

- **Owner:** RMS product owner (Owner-signed decision required; V3 held-out set is jointly signed with DPO per Mtafiti Spec §18).
- **Config keys:** `V3Thresholds` dataclass (`services/mtafiti/v3_overlay.py:25-30`) with three fields — `fact_precision: float`, `genre_accuracy: float`, `inter_annotator_floor: float`. Runtime input `V3Result` carries matching `fact_precision`/`genre_accuracy` + `inter_annotator_kappa`.
- **Unlock procedure:**
  1. Owner scores a real held-out V3 evaluation set → produces `V3Result(...)`.
  2. Owner delivers thresholds → construct `V3Thresholds(fact_precision=..., genre_accuracy=..., inter_annotator_floor=...)`.
  3. Threshold decision lands as config (surface choice open).
  4. Pass to `mtafiti_registry.compose_record(unit, v3_thresholds=..., v3_result=..., ...)`.
- **Behavioral delta when opened:** `overlay_admitted` returns True when the V3 result clears each threshold. `v3_admitted=True` flows into `measure()`; Registry entries gain non-zero `attachment` and `corroboration` signals; `runtime_mode` on `NormalizedUnit.defensibility` shifts from `declaration_baseline` to `v3_admitted` on admitted units. *Observation carried from operator runbook: the current `overlay_admitted` compares `fact_precision` and `genre_accuracy` but not `inter_annotator_kappa` against `inter_annotator_floor`; if the third threshold is intended to gate, extend `overlay_admitted` at unlock time.*
- **Test that proves it opened:** parameterise the closed-seam invariant to the null-threshold case; add positive tests `test_v3_overlay_admits_when_all_thresholds_met`, `test_v3_overlay_refuses_when_any_threshold_missed`, and `test_registry_reflects_v3_signals_when_admitted`. Consolidated in `/app/docs/handoff/seam_unlock_runbook.md` (Seam 2).

## Closed Seam — Unlock: MEA Source-Standing Table

The per-feed source-standing table at `services/mtafiti/source_standing.py` ships as a synthetic placeholder covering the on-disk fixture's `feed_ids`. Every entry has `synthetic_placeholder=True, editorial_authority=False`, and `test_mtafiti_invariants.py::test_source_standing_placeholder_flags` asserts this.

- **Owner:** Media Editorial Authority (MEA, or equivalent authority).
- **Config keys:** MEA-owned editorial table with the shape defined by `services/mtafiti/source_standing.py::SourceStandingEntry` — at minimum `feed_id`, `standing`, `synthetic_placeholder: bool`, `editorial_authority: bool`. Additional MEA-decided metadata fields are safe additions (`SourceStandingEntry` is NOT one of the 14 frozen contracts).
- **Unlock procedure:**
  1. MEA lands real editorial-authority-signed table.
  2. Drop-in as config-swap for the placeholder. The synthetic placeholder is REPLACED, not merged.
  3. **`test_source_standing_placeholder_flags` FAILS LOUDLY on drop-in — that is the correct deployment ceremony.** Alongside the drop-in, replace the invariant with its inverse.
- **Behavioral delta when opened:** real editorial-standing declarations flow into Mtafiti per-feed governance; `MtafitiRegistryRecord` composition begins reflecting MEA-authority-scored standings rather than synthetic defaults. Unrecognized `feed_id`s at composition time need a decided fallback — probably: refuse with `no_source_standing_for_feed` — extend at unlock time.
- **Test that proves it opened:** current invariant will fail (expected). Add:
  - `test_source_standing_editorial_authority_flags` — every entry has `synthetic_placeholder=False, editorial_authority=True` (inverse invariant).
  - `test_source_standing_covers_current_feed_universe` — every `feed_id` referenced by any live fixture or admitted run has a corresponding entry.
  - (Optional per MEA posture) `test_source_standing_table_signed` — table load path checks a signed manifest or hash-match against a MEA-signed digest.

Consolidated in `/app/docs/handoff/seam_unlock_runbook.md` (Seam 4).
