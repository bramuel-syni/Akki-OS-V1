**Solva**

The Depth Governor — Engine Specification

The complete specification of the reasoner: the two faculties and the
one-way seam between them — a free reasoning faculty and a bound
assertion boundary — with the module structure, typed contracts, the
assertion boundary as code, and the test obligations that implement
them.

Engine Specification · Version 1.0 · elaborates the Product &
Engineering Specification v2.1 (§23), which prevails on conflict.

*Prepared by Syni.ai · July 2026 · Confidential*

This document is binding. Part I states what Solva must do and why; Part
II specifies how it is built — modules, typed contracts, the reasoning
stages, the assertion boundary as code, and the test obligations; Part
III states governance and invariants. It is a forward specification: it
defines what must be true of any correct implementation. Solva is the
one governor that reasons; the greater part of this document specifies
the seam at which its reasoning meets a governed ceiling, so the
system’s most powerful component can never launder a claim past its
defensibility class. Points marked **CONFIRM** resolve against the real
contract before use.

**Contents**

**Part I — Mandate**

1\. What Solva Is

Solva is the depth governor: the component that judges whether reasoning
is sound, whether preservation is sufficient, and whether an output
asserts within its defensibility. It is the one governor that reasons —
Northena is deterministic, Targeta’s learning is walled from
eligibility, Mtafiti’s inference only detects. Solva is where genuine
judgment lives. It never extracts and never reaches into the operator
primitives; it issues operations, interprets results, and governs depth.

Because Solva reasons, it is also the component that could do the most
damage: the system launders a claim precisely when its strongest
reasoning pushes against a defensibility ceiling. This mandate therefore
specifies Solva as two faculties with a one-way seam — a reasoning
faculty that is free, and an assertion boundary that is bound to the
governed class and deaf to how strong the reasoning was.

2\. The Anchor

Every rule is judged against one anchor: what makes Solva do its job —
sound reasoning that improves the extraction — while never letting its
reasoning override a governed constraint.

|                                          |                                                                                                                                                                                                                                                  |
|------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Half**                                 | **What it demands**                                                                                                                                                                                                                              |
| **Reason well**                          | Judge soundness, identify the load-bearing units, judge preservation sufficiency, and compose the best conclusion the evidence supports. No governed artifact dictates these judgments — a Matrix cannot tell you whether an inference is sound. |
| **Never override a governed constraint** | The defensibility floor (the Objective Request) and the class verdict (the Qualification Matrix) are fixed. Solva reads them; it never sets or relaxes them. No strength of reasoning may raise a unit’s ceiling.                                |

**The system’s thesis, at its sharpest point.** Northena walls dynamism
from auditability; Targeta walls learning from eligibility; Mtafiti
walls inference from the verdict. Solva walls reasoning from the
assertion ceiling — the same guard, at the point where good reasoning
meets a hard ceiling, which is exactly where laundering would occur.

3\. The Two Faculties

Solva is two faculties with a one-way seam — what lets it reason freely
without letting reasoning corrupt what may be asserted.

|                        |                                                                                                                                                                                                                                                  |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Faculty**            | **Definition**                                                                                                                                                                                                                                   |
| **Reasoning faculty**  | Judges the quality of reasoning — soundness, load-bearingness, preservation sufficiency, the conclusion the evidence supports. Free: no governed artifact dictates these judgments. This is Solva’s power, and it is genuine.                    |
| **Assertion boundary** | Determines what the conclusion may be asserted as — its defensibility class. Bound: computed mechanically as the floor of the load-bearing units’ classes. Not a judgment Solva makes; a governed computation it executes and cannot argue with. |

**The seam is one-way:** the reasoning faculty informs the composition
freely, but its strength — how confident, how well-evidenced — is not an
input to the assertion boundary. A conclusion built from utterance-class
units is asserted as “X was stated,” however overwhelming Solva finds
the evidence. Reasoning shapes the composition; it can never raise the
ceiling.

4\. The Assertion Boundary

The assertion boundary is the guard, specified as code in §10. Three
rules define it, and they are mechanical — not judgments Solva could be
reasoned out of.

-   **A conclusion inherits the floor of its load-bearing units’
    classes.** If any load-bearing unit is utterance-class, the
    conclusion is utterance-class — the weakest load-bearing unit sets
    the ceiling.

-   **An utterance-class conclusion is asserted as “was stated,” never
    as fact.** The phrasing is a function of the class, not of Solva’s
    confidence.

-   **Reasoning strength is not an input to the class.** The assertion
    boundary computes the class from the units’ governed classes alone;
    it cannot read the reasoning faculty’s confidence, so strong
    reasoning cannot unlock a higher class.

**Which load-bearing is Solva’s, and which is not.** Solva’s reasoning
faculty decides which units are load-bearing — a genuine reasoning
judgment. The assertion boundary then computes the class as the floor
over those units — mechanically. Solva chooses the units; it does not
choose the class those units imply.

5\. The Two Bars

Solva reasons against two bars, set by where it operates. Both are
governed by the same two-faculty structure; only the target differs.

|                |                            |                                                                                                                                                                |
|----------------|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Mode**       | **Bar**                    | **Function**                                                                                                                                                   |
| At convergence | Wide (vs. Mandate-class)   | Judge which signal descriptors, relational edges, and defensibility refinements to preserve for the whole class the Mandate targets. Errs toward keeping more. |
| At extraction  | Narrow (vs. the objective) | Reason to a conclusion (Reasoned) or certify a dataset/skill (Packaged) for the specific objective; enforce the assertion boundary; write the trace.           |

6\. The Trace

Every extraction-time judgment Solva makes is recorded in a trace: the
reasoning path (the five stages), the units found load-bearing, the
class computed at the assertion boundary, and the conclusion. The trace
is what makes Solva’s reasoning auditable despite being genuine
reasoning — a reader can see why a conclusion was reached and why it was
asserted at the class it was. The trace carries a trace_id joining it to
the unit-level intelligence and the three trace lenses (parent §5 UX).

**Part II — Engineering Specification**

7\. Module Structure and Dependency Rules

Solva is a reasoning faculty (the five stages), an assertion boundary,
and the enforcement/trace surfaces. The dependency direction encodes the
seam: the assertion boundary does not import the reasoning faculty’s
confidence, and the reasoning faculty does not import the
class-computation.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>services/solva_depth/ — module layout</strong></p>
<p>services/solva_depth/</p>
<p>reasoning.py # the 5 stages:
frame/candidate/tension/probability/reflection</p>
<p>load_bearing.py # identifies load-bearing units (a reasoning
judgment)</p>
<p>assertion.py # computes defensibility class = floor over
load-bearing</p>
<p>enforce.py # applies the floor from the Objective Request;
refuses</p>
<p>stamp.py # Ring 5 emission at convergence</p>
<p>trace.py # records path + load-bearing + class + conclusion</p>
<p>interfaces.py # opaque handles (MatrixHandle, FloorSpec) —
read-only</p>
<p>routers/</p>
<p>solva.py # enforcement + trace read surfaces</p></td>
</tr>
</tbody>
</table>

Dependency rules (enforced by import assertion)

-   **assertion.py computes the class from unit classes only.** It does
    not import reasoning confidence — the seam is a dependency rule.

-   **reasoning.py judges soundness and load-bearingness;** it does not
    import the class-computation or set the class.

-   **enforce.py reads the floor and the Matrix verdict through
    read-only handles;** it never mutates a governed value.

8\. The Reasoning Faculty — the Five Stages

The reasoning faculty is a five-stage pipeline. Each stage is a genuine
judgment; no governed artifact dictates its output. The Tension stage is
where contested units — a claim and its retraction, a fact and its
correction — are surfaced rather than averaged.

|             |                                                                                                                      |
|-------------|----------------------------------------------------------------------------------------------------------------------|
| **Stage**   | **Judgment**                                                                                                         |
| Frame       | Establishes the question and the relevant slice of the Normalized tier.                                              |
| Candidate   | Proposes the units and compositions that could answer it.                                                            |
| Tension     | Surfaces contradiction, corroboration, retraction among candidates (reads Ring 3 edges); does not average them away. |
| Probability | Weighs the candidates toward the best-supported conclusion.                                                          |
| Reflection  | Judges soundness and sufficiency; identifies the load-bearing units; composes the conclusion.                        |

Reflection’s output includes the set of load-bearing units — the units
the conclusion actually rests on. That set is the reasoning faculty’s
product and the only thing the assertion boundary consumes from it (the
units, not the confidence).

9\. Load-Bearing — a Reasoning Judgment

Identifying which units are load-bearing is a genuine reasoning judgment
and belongs to the reasoning faculty. It is not the class computation;
it is the input to it. This separation is what keeps the assertion
boundary mechanical.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>load_bearing.py — a reasoning judgment
(free)</strong></p>
<p>def load_bearing(conclusion, candidates) -&gt; list[UnitRef]:</p>
<p># a genuine reasoning judgment: which units does the conclusion</p>
<p># actually rest on? free — no governed artifact dictates this.</p>
<p># returns unit refs only; carries NO class decision.</p>
<p>... # CONFIRM: UnitRef + candidate shape against
five_rings@v0.</p></td>
</tr>
</tbody>
</table>

10\. The Assertion Boundary — as Code

The assertion boundary computes the conclusion’s defensibility class as
the floor over the load-bearing units’ classes. It reads unit classes
only; it does not, and structurally cannot, read the reasoning faculty’s
confidence. This is the guard — the point at which strong reasoning is
prevented from raising a ceiling.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>assertion.py — class is a floor over units, deaf to
reasoning strength</strong></p>
<p>CLASS_ORDER = {'non_factual': 0, 'utterance': 1, 'fact': 2}</p>
<p>INV_ORDER = {0: 'non_factual', 1: 'utterance', 2: 'fact'}</p>
<p>def conclusion_class(load_bearing_units) -&gt; str:</p>
<p># floor over the load-bearing units' governed classes.</p>
<p># input is unit classes ONLY — no reasoning confidence is a
parameter.</p>
<p>floor = min(CLASS_ORDER[u.defensibility_class] for u in
load_bearing_units)</p>
<p>return INV_ORDER[floor]</p>
<p>def assert_conclusion(text, load_bearing_units) -&gt; Assertion:</p>
<p>klass = conclusion_class(load_bearing_units)</p>
<p>if klass == 'fact':</p>
<p>return Assertion(claim=text, klass='fact')</p>
<p>if klass == 'utterance':</p>
<p>return Assertion(claim=stated_form(text), klass='utterance') # 'X was
stated'</p>
<p>return Assertion(claim=None, klass='non_factual',
context_only=text)</p>
<p># conclusion_class takes NO confidence argument. Strong reasoning</p>
<p># cannot raise the class — the signature makes it
unrepresentable.</p></td>
</tr>
</tbody>
</table>

**Why this is the guard.** conclusion_class takes the load-bearing units
and nothing else — no confidence, no reasoning strength, no evidence
weight. The laundering case (“the evidence is overwhelming, assert the
utterance as fact”) is not policed at runtime; it is unrepresentable,
because the function that computes the class has no parameter through
which reasoning strength could enter. Reasoning chose the units; the
class those units imply is a floor, computed mechanically.

11\. Enforcement — the Floor and the Verdict

At extraction time, Solva enforces the objective’s defensibility_floor
and the governed class. The floor and the Matrix verdict are read
through read-only handles; Solva never sets or relaxes them. A
conclusion whose computed class falls below the objective’s floor is
refused with a structured reason — visibly, not silently.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>enforce.py — read-only governed values; refuse below
floor</strong></p>
<p>def enforce(conclusion, load_bearing_units, floor: FloorSpec) -&gt;
Result:</p>
<p>klass = assertion.conclusion_class(load_bearing_units)</p>
<p>if below_floor(klass, floor): # floor is read-only, from the</p>
<p>return Refusal(reason='below_defensibility_floor', # Objective
Request</p>
<p>computed_class=klass, floor=floor)</p>
<p>return assertion.assert_conclusion(conclusion,
load_bearing_units)</p>
<p># Solva reads the floor and the Matrix verdict; it never mutates
them.</p>
<p># CONFIRM: FloorSpec against objective_request@v0; class enum
against</p>
<p># qualification_matrix@v0 / five_rings@v0 Ring 5.</p></td>
</tr>
</tbody>
</table>

12\. Ring 5 Stamp at Convergence

At convergence, Solva’s wide-bar mode judges which refinements to
preserve and emits the Ring 5 defensibility stamp per unit. The verdict
itself is the governed Qualification Matrix lookup (Mtafiti’s domain);
Solva applies it and judges preservation depth. Refusal reasons are
recorded in the stamp-audit side-channel, which Northena’s Ledger
absorbs — the unit and its audit trace stay in separate envelopes.

13\. The Trace and Interfaces

The trace

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>trace.py — the reasoning made auditable</strong></p>
<p>@dataclass(frozen=True)</p>
<p>class SolvaTrace:</p>
<p>trace_id: str # joins to units + three lenses</p>
<p>stages: Sequence[StageRecord] # frame..reflection, each judged</p>
<p>load_bearing: Sequence[UnitRef] # what the conclusion rests on</p>
<p>computed_class: str # floor over load-bearing</p>
<p>conclusion: Assertion # claim + class (or refusal)</p>
<p># CONFIRM: StageRecord shape at build; trace_id joins the
lenses.</p></td>
</tr>
</tbody>
</table>

Interfaces

|                                  |                  |                                                                                                  |
|----------------------------------|------------------|--------------------------------------------------------------------------------------------------|
| **Interface**                    | **Direction**    | **Shape / status**                                                                               |
| Normalized tier → reasoning      | in               | Reads units (five_rings@v0) for Frame/Candidate. Read-only.                                      |
| Objective Request → enforce      | in               | defensibility_floor via read-only FloorSpec. CONFIRM against objective_request@v0.               |
| Matrix / Ring 5 → assertion      | in               | Unit defensibility_class via read-only handle. Solva applies, never sets.                        |
| assertion → conclusion           | internal one-way | class computed from unit classes only; no confidence input.                                      |
| Solva → Akki                     | out              | Operation requests { operator, slice, params, floor }; interprets results. Solva never extracts. |
| Solva → Ledger (via stamp-audit) | out              | Refusal/decision audit; absorbed by Northena.                                                    |

14\. Test Obligations

|                                           |                                                                                                                       |
|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| **Test**                                  | **Asserts**                                                                                                           |
| test_class_is_floor_over_load_bearing     | conclusion_class returns the minimum class among load-bearing units.                                                  |
| test_class_takes_no_confidence            | conclusion_class has no confidence/strength parameter (signature assertion); strong reasoning cannot raise the class. |
| test_utterance_never_asserted_as_fact     | An utterance-class conclusion is phrased 'was stated', never as fact, regardless of evidence weight.                  |
| test_refuse_below_floor                   | A conclusion below the objective's floor is refused with a structured reason, not silently downgraded away.           |
| test_solva_reads_governed_values_readonly | enforce/assertion never mutate the floor or the Matrix verdict (read-only handle assertion).                          |
| test_solva_never_extracts                 | Solva issues operations to Akki and interprets results; it never runs an operator primitive itself.                   |
| test_trace_records_load_bearing_and_class | Every extraction-time judgment produces a trace carrying load-bearing units and computed class.                       |

15\. Construction Requirements

1.  **Assertion boundary first, as construction.** Build
    assertion.conclusion_class so it takes the load-bearing units and
    nothing else. The seam — no confidence parameter — is the guard;
    build it before the reasoning faculty binds to it.

2.  **The five stages emit judgments and a load-bearing set.** Each
    stage is a genuine judgment; Reflection emits the load-bearing set
    the assertion boundary consumes.

3.  **Enforcement reads governed values read-only.** The floor and the
    Matrix verdict enter through read-only handles; Solva refuses below
    floor and never mutates a governed value.

4.  **Trace from the first commit.** Every extraction-time judgment
    produces a trace carrying the load-bearing set and the computed
    class — the auditability that justifies letting Solva reason.

**Part III — Governance, Invariants, Open Decisions**

16\. Governance and Compliance

-   **Solva never overrides a governed constraint.** The floor and the
    Matrix verdict are read-only; Solva reasons within them and refuses
    below them, but never sets or relaxes them.

-   **Reasoning is auditable.** Every extraction-time judgment produces
    a trace — the reasoning path, the load-bearing units, the computed
    class — so a powerful reasoner remains inspectable.

-   **The assertion boundary is the integrity guarantee.** Because the
    conclusion’s class is a mechanical floor over its units and deaf to
    reasoning strength, Solva cannot launder a claim past its
    defensibility — the guarantee the whole system rests on, held at its
    most powerful component.

17\. Invariants

Binding. Any implementation that violates one is incorrect regardless of
behaviour.

1.  Solva reasons; it never extracts and never reaches into the operator
    primitives. It issues operations and interprets results.

2.  Solva is two faculties: a free reasoning faculty (soundness,
    load-bearingness, preservation, conclusion) and a bound assertion
    boundary (the defensibility class). The seam is one-way.

3.  The conclusion’s defensibility class is computed as the floor over
    its load-bearing units’ classes. Reasoning strength is not an input
    to that computation and cannot raise the class.

4.  An utterance-class conclusion is asserted as “was stated,” never as
    fact, however strong the evidence Solva finds.

5.  Solva identifies which units are load-bearing (a reasoning
    judgment); it does not choose the class those units imply (a
    mechanical floor).

6.  The defensibility floor (Objective Request) and the class verdict
    (Qualification Matrix) are read-only to Solva. Solva reasons within
    them and refuses below the floor; it never sets or relaxes them.

7.  A conclusion below the objective’s defensibility floor is refused
    with a structured reason, never silently downgraded and served.

8.  Every extraction-time judgment produces a trace carrying the
    reasoning path, the load-bearing units, and the computed class.

9.  Solva governs depth only. Direction is Northena; boundary is
    SyniSense. The three axes are never collapsed, and Solva never
    performs another governor’s function.

18\. Open Decisions

No design decision in this mandate is left open. The reasoning-faculty
method (how each stage judges) is a build-time implementation choice
bounded by the invariants — not a governance decision, and requires no
sign-off, provided the assertion boundary (§10) and the read-only
enforcement (§11) hold. Solva depends on the governed values it reads
being present: the Qualification Matrix, the Objective Request floor,
and the Ring 5 class — all frozen contracts. No owner or DPO decision
blocks this component.

**Status.** This specification is complete. Every structural rule — the
two faculties, the assertion boundary as a floor deaf to reasoning
strength, read-only enforcement, the trace — is settled, and no
governance sign-off blocks it. Points marked CONFIRM resolve against the
real contract; a shape that cannot be confirmed is recorded, not
inferred.
