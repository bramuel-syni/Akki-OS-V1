**Targeta**

The Targeting Engine — Engine Specification

The complete specification of the targeting engine: the deterministic
eligibility core, the objective-conditioned yield layer, the eligibility
guard enforced as a type, the two-arm admission gate, and the module
structure, typed contracts, algorithms, and test obligations that
implement them.

Engine Specification · Version 1.0 · elaborates the Product &
Engineering Specification v2.1 (§25), which prevails on conflict.

*Prepared by Syni.ai · July 2026 · Confidential*

This document is binding. Part I states what Targeta must do and why;
Part II specifies how it is built — modules, typed contracts, the
eligibility algorithm, the guard interface, and the gate computation;
Part III states governance, invariants, and the open threshold decision.
It is a forward specification: it defines what must be true of any
correct implementation. Targeta is the one component permitted to learn;
the greater part of this document bounds that learning so it can improve
targeting and can never narrow what the extraction objective may reach.
Points marked **CONFIRM** resolve against the real contract before use.

**Contents**

**Part I — Mandate**

1\. What Targeta Is

Targeta is the targeting engine. It reads the defensibility-measured
Registry that Mtafiti writes and decides where to mine and in what
order, so an extraction objective is served as fully as possible within
its budget. It does not extract and it does not govern — it plans the
order of extraction, turning “what exists, and how defensible it is”
into “what to mine first.” It has two modes: portfolio (Service 1,
ranking the estate against the Portfolio Mandate) and per-run (Service
2, ranking where to mine to satisfy one Objective Request).

2\. The Anchor

Every rule is judged against one anchor: what makes Targeta do its job
better, in service of the extraction objective. The anchor has two
halves, held at once.

|                                       |                                                                                                                                                                                  |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Half**                              | **What it demands**                                                                                                                                                              |
| **Does the job better**               | Reach objective-satisfying, floor-meeting intelligence in fewer mined units — target the sources that pay off for the objective at hand.                                         |
| **Services the extraction objective** | Never narrow what the objective may reach. The defensibility floor is inviolable, and the estate coverage the objective is entitled to is never silently reduced for efficiency. |

**The design in one line.** The part that makes Targeta better —
learning what pays off — is structurally prevented from touching the
part that must not narrow: what is eligible, and the floor. Learning
improves the order; it can never change the eligible set.

3\. The Two-Layer Design

Targeta is two layers with a one-way relationship.

|                                       |                                                                                                                                                                                                                                                    |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Layer**                             | **Definition**                                                                                                                                                                                                                                     |
| **Deterministic eligibility core**    | An explicit, inspectable ranking that decides what is eligible to mine and enforces the defensibility floor as a hard filter. Never learns; governance-grade; correct and sufficient on its own.                                                   |
| **Objective-conditioned yield layer** | A learned signal that refines the order within what the core already permits. Learns which sources satisfy objectives of a given shape at a given floor, and reorders the already-eligible candidates. Reorders only; never re-admits or excludes. |

The distinction the design rests on: objective-conditioned yield (which
sources satisfy this kind of objective) is competence and is permitted;
unconditioned source-preference (which sources are good in general) is
bias and is denied. The yield layer is granted the first and
structurally refused the second (§9).

4\. The Eligibility Guard

The separation between the core and the yield layer is a structural
property of the interface between them, not a rule the yield layer is
trusted to follow. §10 specifies it as code.

-   **Input is the floor-passing eligible set, and nothing else.** The
    yield layer does not receive the floor value, the raw defensibility
    measure, or the eligibility logic.

-   **Output is a permutation of that exact set.** Same members,
    reordered — no member added, none removed.

-   **A non-permutation output is a type error.** A result that drops or
    adds any member is malformed and rejected by the interface — not a
    ranking to review.

5\. The Yield-Layer Admission Gate

The yield layer is learned, so it is admitted to influence ordering only
after passing a gate with two arms, the second a veto.

-   **Arm 1 — Helps.** On a held-out set of past objectives, the yield
    ordering reaches objective-satisfaction in fewer mined units than
    the core.

-   **Arm 2 — Coverage veto.** Across estate classes, the yield layer
    must not drive any eligible class’s mining rate below the core’s,
    for objectives that class is eligible to satisfy. Improving
    efficiency by starving a class fails the gate regardless of the
    efficiency number.

On failure of either arm, Targeta runs on the deterministic core. The
core is never blocked by the yield layer’s failure. The gate thresholds
are owner-signed (§17).

6\. The Two Modes

Portfolio mode reads the whole Registry against the Portfolio Mandate
and ranks the estate to select the priority strata to seed; the core
applies the Mandate’s class-default floor, the yield layer (if admitted)
reorders within eligible strata. Per-run mode reads the Registry against
one Objective Request; the core applies the objective’s floor as a hard
filter and weights by relevance, the yield layer reorders the eligible
sources by objective-conditioned yield. Both honour the floor absolutely
and produce a plan reproducible for a given Registry state, governing
artifact, and yield-layer version.

**Part II — Engineering Specification**

7\. Module Structure and Dependency Rules

Targeta is a set of modules whose dependency direction encodes the
eligibility guard: the yield module never imports the floor or the
eligibility logic; the gate module is the only one that compares the two
orderings.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>services/targeta/ — module layout</strong></p>
<p>services/targeta/</p>
<p>core.py # deterministic eligibility + ranking; never imports
yield</p>
<p>yield_layer.py # learned reorderer; imports ONLY interface types</p>
<p>interface.py # the one-way set-preserving boundary (the guard)</p>
<p>gate.py # yield admission gate: Arm 1 helps, Arm 2 veto</p>
<p>plan.py # MiningPlan assembly + version stamping</p>
<p>modes.py # portfolio / per-run orchestration</p>
<p>contracts/</p>
<p>targeta_plan.py # frozen: MiningPlan (schema + snapshot +
invariant)</p>
<p>routers/</p>
<p>targeta.py # plan + status API</p></td>
</tr>
</tbody>
</table>

Dependency rules (enforced by import assertion)

-   **core.py imports the Registry read and the governing artifact; it
    never imports yield_layer, and imports no ML library.**

-   **yield_layer.py imports only the interface types (YieldInput,
    Permutation); never the floor, the raw measure, or core’s
    eligibility.**

-   **gate.py imports core, yield_layer, and mining history; it is the
    only module that compares the two orderings.**

8\. Data Contracts

Four types carry Targeta’s data. The split between EligibleCandidate
(core-internal, carries the measure) and YieldCandidate (crosses to the
yield layer, carries no floor and no raw measure) is what makes the
guard structural.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>core-internal and boundary types</strong></p>
<p>@dataclass(frozen=True)</p>
<p>class EligibleCandidate: # core-internal only</p>
<p>source_ref: str</p>
<p>region: str</p>
<p>objective_relevance: float # [0,1], core-computed, deterministic</p>
<p>registry_defensibility: float # from Registry; NEVER crosses to
yield</p>
<p>baseline_rank: int # core-assigned deterministic position</p>
<p>@dataclass(frozen=True)</p>
<p>class YieldCandidate: # the ONLY thing the yield layer sees</p>
<p>source_ref: str</p>
<p>features: Mapping[str, float] # opaque; excludes floor + raw
measure</p>
<p>objective_shape: str # conditioning key, NOT the floor value</p>
<p>YieldInput = Sequence[YieldCandidate]</p>
<p>Permutation = Sequence[str] # an ordering of source_refs, nothing
more</p></td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>contracts/targeta_plan.py — the frozen plan</strong></p>
<p>@dataclass(frozen=True)</p>
<p>class MiningPlan:</p>
<p>plan_id: str</p>
<p>mode: Literal['portfolio', 'per_run']</p>
<p>governing_artifact_ref: ArtifactRef</p>
<p>registry_snapshot_ref: str</p>
<p>ordered_targets: Sequence[TargetLocation]</p>
<p>defensibility_floor: FloorSpec # carried through to Layer A</p>
<p>core_baseline_ranking: Sequence[str] # for attribution / audit</p>
<p>yield_layer_version: str # or 'core-only'</p>
<p>generated_at: str</p>
<p># CONFIRM: FloorSpec + TargetLocation against five_rings@v0,</p>
<p># objective_request@v0, and the Registry contract.</p></td>
</tr>
</tbody>
</table>

9\. The Deterministic Eligibility Core

The core reads the Registry and the governing artifact, applies the
floor as a hard filter, and ranks the eligible set by a fixed,
inspectable function. It contains no model and no learned weight.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>core.py — eligibility + deterministic
ranking</strong></p>
<p>def eligible_and_rank(registry, artifact) -&gt;
list[EligibleCandidate]:</p>
<p>floor = artifact.defensibility_floor # hard filter, core-only</p>
<p>out = []</p>
<p>for s in registry.sources(): # CONFIRM: Registry iface</p>
<p>if not meets_floor(s.defensibility_measure, floor):</p>
<p>continue # excluded, full stop</p>
<p>out.append(EligibleCandidate(</p>
<p>source_ref=s.ref, region=s.region,</p>
<p>objective_relevance=relevance(s, artifact), # deterministic</p>
<p>registry_defensibility=s.defensibility_measure,</p>
<p>baseline_rank=-1))</p>
<p>out.sort(key=rank_key, reverse=True) # fixed, inspectable</p>
<p>return [replace(c, baseline_rank=i) for i, c in
enumerate(out)]</p></td>
</tr>
</tbody>
</table>

10\. The One-Way Interface — the Guard as a Type

The yield layer is never called directly; it is called only through
apply_yield, which constructs the stripped YieldInput, invokes the yield
function, and validates that the result is a permutation of the exact
input before it may reorder anything. A non-permutation raises — it is
not caught and corrected, it is rejected.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>interface.py — the set-preserving boundary</strong></p>
<p>class NonPermutationError(TypeError): ...</p>
<p>def to_yield_input(eligible) -&gt; list[YieldCandidate]:</p>
<p># the ONLY view the yield layer receives. excludes floor +</p>
<p># registry_defensibility + eligibility by construction.</p>
<p>return [YieldCandidate(source_ref=c.source_ref,</p>
<p>features=safe_features(c),</p>
<p>objective_shape=shape_key(c)) for c in eligible]</p>
<p>def apply_yield(eligible, yield_fn) -&gt;
list[EligibleCandidate]:</p>
<p>order = yield_fn(to_yield_input(eligible)) # learned reorderer</p>
<p>src = {c.source_ref for c in eligible}</p>
<p>if len(order) != len(eligible) or set(order) != src:</p>
<p>raise NonPermutationError('yield output is not a permutation')</p>
<p>pos = {ref: i for i, ref in enumerate(order)}</p>
<p>return sorted(eligible, key=lambda c: pos[c.source_ref])</p></td>
</tr>
</tbody>
</table>

**Why this is the guard.** apply_yield is the only path from core to
yield and back. The yield function receives YieldCandidate objects that
do not carry the floor or the raw measure, so it cannot act on them; its
output is validated set-equal to the input, so it cannot drop or add a
source. Reordering is the only effect it can have. The bias hazard is
not policed at runtime — it is unrepresentable in the types.

11\. The Objective-Conditioned Yield Layer

The yield layer is a learned function from YieldInput to a Permutation.
It conditions on the objective shape — it may learn that sources of a
given standing tend to satisfy objectives of a given shape — but it
never enforces or relaxes the floor, because everything it receives has
already passed the floor and it never receives the floor value.
Conditioning on the objective shape is competence; it is not floor
enforcement, which is upstream and invisible to it. The learning method
is an implementation choice bounded by these constraints: input is
YieldInput only, output is a permutation, and admission is through the
gate (§12).

12\. The Yield Gate — Computable Definitions

The gate is computed against a held-out set of past objectives with
recorded outcomes. Both arms are computable; Arm 2 is a veto.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>gate.py — two-arm admission, Arm 2 is a veto</strong></p>
<p>def evaluate_gate(held_out, core_fn, yield_fn, thresholds) -&gt;
GateResult:</p>
<p>gains = [] # Arm 1 — Helps</p>
<p>for obj in held_out:</p>
<p>u_core = units_to_satisfy(core_fn, obj)</p>
<p>u_yield = units_to_satisfy(yield_fn, obj)</p>
<p>gains.append((u_core - u_yield) / u_core)</p>
<p>helps = median(gains) &gt;= thresholds.min_efficiency_gain</p>
<p>veto = False # Arm 2 — Coverage veto</p>
<p>for k in estate_classes(held_out): # source-standing x genre</p>
<p>if coverage(yield_fn,k) &lt; thresholds.alpha *
coverage(core_fn,k):</p>
<p>veto = True # class starved -&gt; veto</p>
<p>return GateResult(admitted=(helps and not veto), helps=helps,
veto=veto)</p></td>
</tr>
</tbody>
</table>

If admitted is false for either reason, the caller uses the core
ordering and stamps the plan yield_layer_version = 'core-only'.

13\. Interfaces and Test Obligations

Interfaces

|                          |                  |                                                                                                                     |
|--------------------------|------------------|---------------------------------------------------------------------------------------------------------------------|
| **Interface**            | **Direction**    | **Shape / status**                                                                                                  |
| Registry → core          | in               | Reads { source_ref, region, sensitivity, defensibility_measure, freshness }. CONFIRM against the Registry contract. |
| Artifact → core          | in               | Portfolio Mandate or Objective Request incl. floor. objective_request@v0.                                           |
| core → yield             | internal one-way | YieldInput only; no floor, no raw measure.                                                                          |
| yield → core             | internal one-way | Permutation; non-permutation rejected.                                                                              |
| Targeta → Akki Retrieval | out              | MiningPlan.ordered_targets carrying the floor. CONFIRM TargetLocation.                                              |
| Targeta → plan store     | out              | MiningPlan with yield_layer_version + baseline. CONFIRM storage.                                                    |

Test obligations

|                                    |                                                                                                              |
|------------------------------------|--------------------------------------------------------------------------------------------------------------|
| **Test**                           | **Asserts**                                                                                                  |
| test_yield_output_is_permutation   | A yield fn returning a dropped/added/duplicated member raises NonPermutationError; no plan is built from it. |
| test_yield_never_sees_floor        | YieldCandidate has no floor and no raw-measure field; to_yield_input carries neither.                        |
| test_floor_is_hard_filter          | A source below the floor never appears in the eligible set, regardless of yield ordering.                    |
| test_fallback_to_core              | Gate failure (either arm) → plan uses core ordering; yield_layer_version == 'core-only'.                     |
| test_coverage_veto_overrides_helps | A yield fn that improves efficiency but starves a class is not admitted.                                     |
| test_plan_reproducible             | Same Registry state + artifact + yield-layer version → byte-identical plan.                                  |
| test_core_has_no_ml_import         | core.py imports no ML library (import assertion).                                                            |

14\. Construction Requirements

1.  **Core first.** Build the deterministic eligibility core, the
    interface, the plan contract, and the two modes; the core is a
    complete targeter and the fallback the yield layer degrades to.

2.  **The interface is construction, not convention.** apply_yield
    rejects a non-permutation as a type error; the boundary is not a
    runtime check the yield layer is trusted to respect.

3.  **Yield layer second, gated.** The yield layer is admitted only
    through the two-arm gate; until admitted, and on any gate failure,
    Targeta runs core-only.

4.  **Every plan is versioned.** Each plan records its yield-layer
    version (or 'core-only'), so targeting is always attributable.

**Part III — Governance, Invariants, Open Decisions**

15\. Governance and Compliance

-   **Targeta never overrides the floor or widens scope.** It targets
    within the eligibility the core computes; boundary governance is
    SyniSense’s, run governance Northena’s.

-   **Every plan is auditable.** It carries the yield-layer version and
    the deterministic baseline, so any ordering can be explained and
    reproduced.

-   **Coverage is a governed property.** The gate’s veto arm is the
    guard against the system quietly ceasing to serve part of the estate
    — a fairness-of-coverage guarantee.

16\. Invariants

Binding. Any implementation that violates one is incorrect regardless of
behaviour.

1.  Targeta plans the order of extraction; it does not extract and does
    not govern.

2.  The deterministic eligibility core never learns — no model, no
    adaptive weight; ranking fixed and inspectable. Targeta on the core
    alone is complete and correct.

3.  The yield layer may only reorder the eligible set the core cleared:
    it receives YieldInput and nothing else, and returns a permutation.
    A non-permutation is a type error.

4.  The defensibility floor is applied by the core alone, as a hard
    filter, before the yield layer sees anything. The yield layer never
    receives the floor and can never relax, override, or trade against
    it.

5.  Learning may improve the order of mining; it may never change what
    is eligible. The bias hazard is denied by construction.

6.  The yield layer is admitted only through the two-arm gate — helps,
    and a coverage veto that overrides the efficiency arm.

7.  On gate failure, Targeta runs on the deterministic core; the core is
    never blocked by the yield layer’s failure.

8.  Every plan is reproducible for a given Registry state, governing
    artifact, and yield-layer version, and records that version.

9.  Targeta never widens scope or lowers a floor; boundary and run
    governance remain SyniSense’s and Northena’s.

17\. Open Decisions

|                                                                                      |                                     |                                                                                                                 |
|--------------------------------------------------------------------------------------|-------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| **Decision**                                                                         | **Owner**                           | **Blocks**                                                                                                      |
| Yield-gate thresholds: min_efficiency_gain, coverage_alpha, held-out set composition | Project owner (as with the V-gates) | Admission of the yield layer only. Not a blocker for the deterministic core, which ships and runs without them. |

Proposed values (for sign-off)

|                             |                                                                                                                                           |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| **Parameter**               | **Proposed**                                                                                                                              |
| min_efficiency_gain (Arm 1) | Median ≥ 0.15 reduction in mined units to objective-satisfaction across the held-out set, no objective worsened beyond a small tolerance. |
| coverage_alpha (Arm 2 veto) | 0.90 — no eligible class mined below 90% of the core’s rate for objectives it is eligible to satisfy.                                     |
| held-out set                | Representative across objective shapes, floors, and estate classes; sized so per-class coverage is measurable.                            |

**Status.** This specification is complete. Every structural rule — the
two-layer design, the one-way guard as a type, the two-arm gate with its
bias veto, the deterministic fallback — is settled. Only the yield-gate
threshold values await sign-off, and they gate the yield layer alone,
not the core. Points marked CONFIRM resolve against the real contract; a
shape that cannot be confirmed is recorded, not inferred.
