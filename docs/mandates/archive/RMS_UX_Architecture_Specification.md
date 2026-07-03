> **SUPERSEDED** by `RMS_UX_Architecture_v2.md` on 2026-07-03. Retained for lineage only; consult the successor for binding rules.

**RMS Intelligence System**

UX Architecture Specification

The experience architecture: who the system serves, what each is
promised, the surfaces that deliver those promises, and the trust model
that carries the governance into the experience — the three trace
lenses, the visible defensibility class, and the explained refusal. It
specifies how the system is experienced; the concrete interface is
specified in the companion Interface Specification.

Version 1.0 · consistent with the Product & Engineering Specification
v2.1, which prevails on conflict.

*Prepared by Syni.ai for Royal Media Services · July 2026 ·
Confidential*

This document is binding at the level of experience architecture. It
states what the experience must deliver and why, the surfaces that serve
each user, the trust model that makes the system’s governance felt
rather than operated, and the trace model that lets any answer be
inspected to the depth a user reaches for. It is a forward
specification: it defines what must be true of any correct experience,
and does not assume one has been built. The concrete interface —
layouts, flows, components — is the companion Interface Specification;
this document is its parent on experience matters.

**Contents**

**Part I — The Experience Model**

1\. What the Experience Must Deliver

The system produces governed intelligence — claims that are honest about
how defensibly they may be asserted. The experience has a harder job
than showing that intelligence: it must make the intelligence usable by
people who are not analysts, and it must make the governance felt as
trust rather than presented as machinery. An interface that mirrors the
architecture — a screen per lens, a control per governor — would be
faithful and unusable. The experience is designed from the user’s
promise inward, and the architecture is drawn in only where it makes the
promise more trustworthy or the path shorter.

**The governing rule of the experience.** Governance is felt, not
operated. The defensibility apparatus — the class, the floor, the
provenance, the trace — is present in every answer, but it surfaces as
trust the user can reach for, not as controls the user must work. The
default experience delivers the promise without making anyone think
about lenses, classes, or governors; the depth is there the moment a
user doubts an answer, and invisible until then.

2\. The Users and Their Promises

The system serves six distinct users. Each is a first-class user with a
promise — including the internal roles, whose promises are as demanding
as any external one. The experience is anchored to these promises; a
surface with no promise behind it has nothing to design toward.

|                          |                                                                                                                                                                                        |
|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **User**                 | **Promise**                                                                                                                                                                            |
| **RMS decision-maker**   | Ask what you need to know; get an answer you can act on and defend, without becoming an analyst.                                                                                       |
| **External buyer**       | Buy intelligence you can rely on and use, that is honest about its own limits.                                                                                                         |
| **DPO / compliance**     | Show, on demand, that any run was lawful and accountable.                                                                                                                              |
| **Operator**             | Hold confidence over enormous volume and consequential governance without watching everything — the system brings you what needs you, when it needs you, and stays quiet otherwise.    |
| **Integrating engineer** | Integrate governed intelligence into your own product or pipeline quickly, with the governance travelling inline with the data — not something to re-implement or able to be stripped. |
| **Super-admin**          | Exercise total control over what the system permits — taxonomy, thresholds, access, tiers — with every high-privilege action safe by construction and fully accountable.               |

3\. The Trust Model

Trust is the experience’s central deliverable, and it is layered so it
is available on demand without being imposed. A decision-maker sees an
answer and a single, legible signal of how far it can be trusted; if
they reach further, they see why; if they reach further still, they see
the full accountable record. Trust is progressive: the surface is calm
by default and deepens only as the user asks.

|               |                                                                                                                                                         |
|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Layer**     | **What the user sees**                                                                                                                                  |
| The answer    | The intelligence itself, in plain terms, with one clear signal of its defensibility class — what it may be asserted as.                                 |
| The reasoning | On reach: why this answer, which units it rests on, what was contested, why it was asserted at the class it was.                                        |
| The record    | On reach: the full accountable trail — provenance, the governed verdict and its rule, the lawful basis, the refusals — the same substance the DPO sees. |

**Part II — The Surfaces**

4\. The Surface Map

Each user reaches the system through a surface designed for their
promise. The surfaces share one substrate — the governed intelligence
and its trace — and differ in what they foreground. A single public
entry routes each authenticated user to their surface; role
differentiation is a routing concern, not a layout concern (Interface
Specification).

|                     |                                                                                                                                             |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| **Surface**         | **Serves / foregrounds**                                                                                                                    |
| Decisions console   | The decision-maker. Foregrounds the question and the answer; trust on reach; nothing analytic imposed.                                      |
| Product surface     | The external buyer. Foregrounds the intelligence product and its guarantee; the estate, governors, and extraction are never shown.          |
| Integration surface | The integrating engineer. Foregrounds keys, endpoints, and the response contract in which governance travels inline. Two paths (§6).        |
| Operator surface    | The operator. Foregrounds exceptions — what needs attention across volume, governance, and infrastructure — and stays quiet otherwise (§7). |
| Governance surface  | The DPO. Foregrounds the accountable record: lawful basis, refusals, the Ledger, retention.                                                 |
| Control surface     | The super-admin. Foregrounds high-privilege functions, each guarded and logged (§8).                                                        |

5\. The Two Consumption Consoles

Two consoles consume intelligence, for two different promises. The
decisions console serves internal decision-making — the question, the
answer, trust on reach. The product surface serves external buyers — the
intelligence as a product, with its guarantee, and none of the system’s
internals. They share the trace substrate; they foreground opposite
things: the decisions console foregrounds the answer to a live question,
the product surface foregrounds a durable, reliable deliverable.

6\. The Integration Surface — Two Paths

The integrating engineer reaches the system programmatically and never
sees a console, so the governance cannot be rendered for them — it must
travel inline in the response contract, inseparable from the claim. The
surface serves two distinct integration promises.

|                           |                                                                                                                                                                                                                                                                                                  |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Path**                  | **Promise and shape**                                                                                                                                                                                                                                                                            |
| **Productization (live)** | Build fast on live intelligence through the inner gate. Self-serve key generation, live query, low friction — and every response carries the defensibility class inline with the claim, the floor enforced server-side, the trace_id returned. Governance is non-optional in the response shape. |
| **Data-buying (extract)** | Acquire datasets or skills through the outer gate, defensibly. Rights-checked, irreversibility-applied, cumulative-disclosure-guarded. The friction is the feature: it is what makes the data lawfully the buyer’s to use. Gated at the key’s scope.                                             |

**Governance travels with the data.** The integration surface’s defining
constraint: a careless integrator must not be able to take the claim and
drop its defensibility. The class is inline with the claim in the
response contract; the floor is enforced server-side, not client-side;
the file-out path is gated at the key’s scope; the audit trail is
generated whether or not the integrator requests it. This is the same
guard the system applies everywhere — the powerful thing (programmatic
access at scale) walled from the ungoverned thing (raw claims without
their defensibility) — expressed in the response contract.

7\. The Operator Surface

The operator carries the highest cognitive load in the system — volume,
customer-sensitivity tiers, governance thresholds, infrastructure health
— and the promise is confidence without vigilance. The surface is
therefore exception-first, not dashboard-first: it is calm when the
system is healthy and surfaces exactly what needs a human when something
crosses a threshold. A wall of always-on dashboards would defeat the
promise by making everything equally present, which is how the critical
thing slips.

|                     |                                                                                                        |
|---------------------|--------------------------------------------------------------------------------------------------------|
| **Dimension**       | **Surfaced as an exception when…**                                                                     |
| Throughput / volume | A queue, extraction rate, or backlog crosses a health threshold.                                       |
| Governance          | A floor is being refused at rate, a class distribution shifts materially, or a gate result changes.    |
| Customer / tenancy  | A sensitive-tier tenancy or a rights boundary needs attention.                                         |
| Infrastructure      | Compute, substrate, or a perception model degrades against its budget (e.g. runtime past 4× realtime). |

8\. The Governance and Control Surfaces

Governance surface (DPO)

The DPO’s promise is proof of lawfulness and accountability on demand.
The surface foregrounds the accountable record — the Northena Ledger,
the lawful basis on every run, the refusals, and retention — as
evidence, not as logs to trawl. It is the audit lens (§11) at the scope
of the whole system.

Control surface (super-admin)

The super-admin exercises the highest-privilege functions, in classes:
the governed taxonomy (the Qualification Matrix and source-standing),
governance thresholds, access and key authority, and tenancy/tier
control. The promise is total control with every high-privilege action
safe by construction — versioned, diffed, and logged — so authority
never becomes an un-audited edit. The surface is not editorial; it is
administrative, with each function class guarded and accountable.

**Part III — The Three Trace Lenses**

9\. The Lenses as the Core Experience Primitive

The trace lens is the experience primitive that makes trust progressive.
One piece of intelligence can be inspected at three depths — the unit,
the reasoning, the record — and the lenses are not three tabs a user
chooses between; they are depth a user pulls toward. The default surface
shows the shallowest lens; each deeper lens is reached only when the
user doubts what the shallower one showed. Every lens is joined by one
trace_id (§12).

10\. The Unit Lens

The unit lens shows a single piece of intelligence as it will be used:
the claim, in plain terms, with its defensibility class and its
provenance. It answers “what is this, and how far can I trust it”
without requiring the user to reason about the system. The class is the
one legible trust signal; the provenance is one reach away. This is the
lens the decision-maker and the buyer live in.

11\. The Reasoning Lens

The reasoning lens shows why an answer is what it is: the units the
conclusion rests on (the load-bearing set), what was corroborated,
contradicted, or retracted (the Tension the reasoning surfaced), and why
the conclusion was asserted at the class it was — the floor over its
load-bearing units. It makes Solva’s reasoning legible without exposing
its internals: the user sees the shape of the judgment and the reason
for the class, not model mechanics. This is the lens a decision-maker
reaches for when an answer surprises them.

12\. The Audit Lens and trace_id

The audit lens shows the full accountable record: provenance, the
governed verdict and the Matrix rule that produced it, the lawful basis
admitted for the run, the refusals, and the Ledger entry. It is the
DPO’s home surface and the deepest reach available from any answer.
Nothing in it is reconstructed for display — it is the same record the
system keeps for accountability.

**One trace_id joins every lens and every surface.** A single trace_id
joins the unit to its reasoning to its audit record, and joins an answer
in the decisions console to the same answer’s record in the governance
surface and to the response returned through the integration surface. A
user reaching from an answer to its reasoning to its record never
crosses a seam; the DPO auditing a run sees the same trace the
decision-maker acted on. The trace_id is the thread that makes the whole
experience one fabric.

**Part IV — How Governance Surfaces**

13\. Defensibility Class at the Point of Consumption

The defensibility class is present on every unit of intelligence,
everywhere it is consumed, as the one legible trust signal. It is shown
as what the claim may be asserted as — an established fact, a recorded
statement (‘X was stated’), or non-factual context — in plain language,
not as a score or a jargon label. The class is never hidden to make an
answer look stronger, and it is never elaborated into a number that
invites false precision. It is the honest headline of every answer.

14\. Refusal-Below-Floor as a Visible, Explained Event

When an objective demands a defensibility floor the available
intelligence cannot meet, the system refuses — and the refusal is a
first-class, explained experience, not an empty result or a silent
downgrade. The user is told that the answer would fall below the floor
they required, what class the available evidence actually supports, and
what would raise it — expressed as actor-appropriate actions the
decision-maker can take: lower the defensibility floor, or narrow the
objective to better-sourced material. (Anchor: shipped `Service1Refusal@v0`
contract; the frontend Refusal Card renders `asked` / `supported_class` /
`what_would_raise_it` as the visible surface, and the backend hint table
at `services/service_1/refusal_hints.py` supplies the actor-appropriate
strings. Category anchors from earlier drafts — "corroboration, an
accountable source" — remain the taxonomy of *what* would raise it; the
render frames that taxonomy as *actions* to the decision-maker.) A
refusal is
the system keeping its promise, and the experience presents it as such:
the honest ‘not to this standard, and here is why’ that makes the
affirmative answers trustworthy.

**Why the refusal is shown, not hidden.** A system that silently returns
a weaker answer than asked for, or an empty one, teaches the user not to
trust it. Showing the refusal — with the class the evidence supports and
the path to raise it — is what makes every non-refused answer credible.
The refusal is the visible edge of the guarantee.

15\. The Two Perimeters in the Experience

The two delivery perimeters surface as two different experiences of
receiving intelligence. Inner-gate delivery is live: intelligence served
in-tenancy, in the consoles and through the productization API, felt as
a fast, direct answer. Outer-gate delivery is an acquisition: a governed
file-out through the data-buying path, felt as a deliberate,
rights-checked transaction whose friction is the assurance. The user is
never asked to understand ‘gates’; they experience either a live answer
or a governed acquisition, and the perimeter is the system’s concern
beneath that.

**Part V — Experience Invariants**

16\. Invariants

Binding on any correct experience. A design that violates one fails the
promise regardless of how it looks.

1.  The experience is designed from each user’s promise inward; the
    architecture is surfaced only where it makes the promise more
    trustworthy or the path shorter. No surface mirrors the system’s
    internals for their own sake.

2.  Governance is felt as trust, not operated as machinery. The default
    experience delivers the promise without requiring the user to think
    about lenses, classes, or governors.

3.  Every unit of intelligence surfaces its defensibility class,
    everywhere it is consumed, in plain language — never hidden to
    strengthen an answer, never inflated into false precision.

4.  Trust is progressive across the three lenses: the answer, then the
    reasoning on reach, then the accountable record on reach. Depth is
    available on demand and imposed on no one.

5.  A single trace_id joins the three lenses and joins every surface, so
    a user never crosses a seam moving from an answer to its reasoning
    to its record, and the DPO audits the same trace the user acted on.

6.  A refusal-below-floor is a visible, explained event — the class the
    evidence supports and the path to raise it — never a silent
    downgrade or an empty result.

7.  Through the integration surface, governance travels inline with the
    data: the class is inseparable from the claim in the response
    contract, the floor is enforced server-side, and the audit trail is
    generated regardless of request.

8.  The operator surface is exception-first: calm when healthy,
    surfacing exactly what needs a human when a threshold is crossed. It
    never relies on constant vigilance over always-on dashboards.

9.  Every internal user — operator, DPO, super-admin — has a promise the
    experience is anchored to; none is treated as tooling without a
    designed experience.

10. High-privilege control actions are safe by construction — versioned,
    diffed, and logged — so administrative authority is never an
    un-audited edit.

**Status.** This specification is complete at the level of experience
architecture. It anchors every surface to a user’s promise, states the
trust model and the three trace lenses that deliver it, and fixes how
defensibility, refusal, and the two perimeters surface. The concrete
interface — the landing and routing, the console layouts, the developer
surface, the control panels — is specified in the companion Interface
Specification, consistent with this document, which prevails on
experience matters.