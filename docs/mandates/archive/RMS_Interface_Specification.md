> **SUPERSEDED** by `RMS_UI_Specification_v1.md` on 2026-07-03. Retained for lineage only; consult the successor for binding rules.

**RMS Intelligence System**

Interface Specification

The concrete interface: the single entry and its sign-in routing, the
layout and behaviour of each surface, how the three trace lenses render,
how defensibility and refusal appear, and the integration surface with
its response contract. The companion to the UX Architecture
Specification, which it realises and which prevails on experience
matters.

Version 1.0 · consistent with the UX Architecture Specification and the
Product & Engineering Specification v2.1.

*Prepared by Syni.ai for Royal Media Services · July 2026 ·
Confidential*

This document specifies the concrete interface. It defines the single
entry and the sign-in routing that resolves each user to their surface,
the layout and behaviour of each surface, the rendering of the three
trace lenses, the appearance of the defensibility class and the refusal,
and the integration surface’s response contract. It is a forward
specification: it states what the interface must be, and does not assume
one has been built. It realises the UX Architecture Specification and
defers to it on experience matters. The first surface to build is the
entry and its routing (§5); the surfaces behind it are specified here
and built as each is reached — the specification is complete; the build
is staged.

**Contents**

**Part I — The Interface Model**

1\. One Entry, Routed by Sign-In

The interface has a single entry — one public landing — and sign-in
routes each authenticated user to their surface. Role differentiation is
a routing concern, not a layout concern: the landing makes one promise
legible to everyone, and the account behind the sign-in is where the
role-specific surface lives. There is no separate landing per user;
there is one landing and six destinations.

2\. Interface Principles

Four principles govern every surface. They are the concrete expression
of the UX Architecture’s trust model.

-   **Calm by default, depth on reach.** Every surface opens at its
    shallowest, most legible state. Detail — the reasoning, the record,
    the underlying data — appears when the user reaches for it, never
    imposed on arrival.

-   **The class is always present.** Wherever a unit of intelligence
    appears, its defensibility class appears with it, in plain language.
    No surface renders a claim without its class.

-   **One thread throughout.** A single trace_id joins an answer to its
    reasoning, its record, and its API response. Every ‘go deeper’
    action follows that thread; the user never re-finds an answer in
    another surface.

-   **A refusal is a first-class result.** The interface renders a
    refusal-below-floor as an explained state with a path forward —
    never an empty result and never a silent downgrade.

3\. The Surface Inventory

Six surfaces sit behind the single entry, one per user promise.

|                     |                                                                                    |
|---------------------|------------------------------------------------------------------------------------|
| **Surface**         | **Realises**                                                                       |
| Decisions console   | The RMS decision-maker’s ask-and-answer experience; the unit and reasoning lenses. |
| Product surface     | The external buyer’s product-and-guarantee experience.                             |
| Integration surface | The engineer’s keys, endpoints, and response contract; the two paths.              |
| Operator surface    | The operator’s exception-first monitoring.                                         |
| Governance surface  | The DPO’s accountable record; the audit lens at system scope.                      |
| Control surface     | The super-admin’s guarded high-privilege functions.                                |

**Part II — The Entry and Routing**

4\. The Landing

The landing is one page. Its single job is to make the promise legible —
governed intelligence you can act on and defend — and to present one
action: sign in. It states what the system is in terms that read true to
every user, and it does not attempt to serve any role’s working
experience; that is behind the sign-in. The one design constraint
load-bearing on the landing is that the promise it makes legible is
governance, not raw power: what distinguishes the system is that its
intelligence is defensible, and the landing must make that felt before
sign-in.

|                     |                                                                                                                 |
|---------------------|-----------------------------------------------------------------------------------------------------------------|
| **Landing element** | **Purpose**                                                                                                     |
| The promise line    | States, plainly, that the system delivers intelligence that is honest about how far it can be trusted.          |
| The trust signal    | Makes the governance felt — that every answer carries its own defensibility — without explaining the machinery. |
| Sign in             | The single action. Resolves identity and routes to the user’s surface.                                          |

5\. Sign-In and Routing

Sign-in resolves the user’s identity and role and routes to the
corresponding surface. Routing is deterministic on role; a user with
more than one role is routed to a chooser, not shown a merged surface.
The routing is the first thing built — the entry and the resolution to a
surface — because it is the spine every other surface hangs from.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>routing — deterministic on resolved role
(behavioural)</strong></p>
<p>on sign_in(identity) -&gt; Surface:</p>
<p>role = resolve_role(identity) # from access authority</p>
<p>return {</p>
<p>'decision_maker': DecisionsConsole,</p>
<p>'buyer': ProductSurface,</p>
<p>'engineer': IntegrationSurface,</p>
<p>'operator': OperatorSurface,</p>
<p>'dpo': GovernanceSurface,</p>
<p>'super_admin': ControlSurface,</p>
<p>}[role] # multi-role -&gt; role chooser</p></td>
</tr>
</tbody>
</table>

**Part III — The Consumption Interfaces**

6\. The Decisions Console

The decisions console is where the RMS decision-maker asks and receives.
It opens on a single, quiet prompt — what do you need to know — not a
dashboard. An answer returns as intelligence in plain terms with its
defensibility class shown as the one trust signal; the reasoning and the
record are one reach away, not on the screen by default. The console
never asks the decision-maker to think as an analyst; the depth is
available, and absent until wanted.

Composing the objective

The decision-maker states a need in plain language. The interface
composes that into the governed Objective Request beneath the surface —
the objective, the required defensibility floor, the scope, the lawful
basis — without making the user assemble those fields by hand. Where the
floor or scope needs a choice, the interface asks one plain question,
not a form; the composition into the frozen request is the system’s
work, admitted by Northena, not the user’s.

7\. Rendering the Three Lenses

The three trace lenses render as one progressive view, not three tabs.
The unit lens is the default; the reasoning and audit lenses are reached
in place, deepening the same answer.

|           |                                                                                                                                                                                   |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Lens**  | **Renders as**                                                                                                                                                                    |
| Unit      | The claim in plain terms, its defensibility class as the headline trust signal, and provenance one reach away. The default view.                                                  |
| Reasoning | On reach: the load-bearing units, what was corroborated / contradicted / retracted, and why the answer was asserted at its class. The shape of the judgment, not model internals. |
| Audit     | On reach: provenance, the governed verdict and its Matrix rule, the lawful basis, and the Ledger entry. The same record the DPO sees.                                             |

**The thread, in the interface.** Each deeper lens is reached from the
answer itself, following its trace_id — not by navigating to another
screen and re-finding the answer. A decision-maker moving from the claim
to why-this-answer to the full record stays on one continuous surface;
the DPO opening the same trace_id in the governance surface sees the
identical record.

8\. Rendering Class and Refusal

The defensibility class

The class renders in plain language as what the claim may be asserted
as: an established fact, a recorded statement (‘X stated …’), or
non-factual context. It is the headline of the answer, not a badge in a
corner and not a numeric score. It is never suppressed to make an answer
read stronger, and never expanded into a false-precision figure.

The refusal-below-floor

When the available intelligence cannot meet the required floor, the
interface renders a refusal as a complete, explained state: what was
asked, that the answer would fall below the required standard, the class
the available evidence actually supports, and what would raise it. The
refusal occupies the answer position — it is the answer — rendered with
the same care as an affirmative result.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>the refusal state (behavioural)</strong></p>
<p>Refusal:</p>
<p>headline: 'Not to the standard you required.'</p>
<p>asked: &lt;objective + required floor, in plain terms&gt;</p>
<p>supported: &lt;the class the evidence supports, e.g. 'recorded
statement'&gt;</p>
<p>to_raise: &lt;what would lift it: corroboration / accountable
source&gt;</p>
<p># occupies the answer position; never an empty result, never
silent.</p></td>
</tr>
</tbody>
</table>

9\. The Product Surface

The product surface is the external buyer’s interface. It foregrounds
the intelligence product — a dataset or a skill — and its guarantee, and
shows none of the estate, the governors, or the extraction. The buyer
sees what the product asserts, at what defensibility, under what rights;
the unit lens is available so any item can be inspected to its class and
provenance, but the reasoning and audit internals of the estate are not
the buyer’s surface. Delivery is experienced as either live access
(inner-gate) or a governed acquisition (outer-gate), per §13.

**Part IV — The Integration Interface**

10\. The Developer Surface

The integration surface is the engineer’s interface: a developer landing
with self-serve key generation, scoped keys, endpoint documentation, and
the response contract. It foregrounds the response shape, because that
is where governance lives for a programmatic consumer — the class
travels inline with the claim, and cannot be requested away.

Keys and scope

Keys are self-serve and scoped. A productization key grants live query
through the inner gate; a data-buying key grants governed extract
through the outer gate, and carries the rights and disclosure scope the
buyer is entitled to. The scope is enforced server-side at every call; a
key cannot exceed its scope by any client-side action.

11\. The Response Contract — Governance Inline

Every response returns the claim and its defensibility inline,
inseparably. The class is a field of the same object as the claim, not a
separate optional block; the floor is enforced before the response is
formed, not offered as a client-side filter; the trace_id is returned so
the response can be reconciled to its record. A consumer cannot take the
claim without its class, because they are one object.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>the live response contract (productization /
inner-gate)</strong></p>
<p>{</p>
<p>'trace_id': '…', # reconciles to the audit record</p>
<p>'claim': '…', # the intelligence, in plain terms</p>
<p>'defensibility': { # inline, inseparable from the claim</p>
<p>'class': 'fact|utterance|non_factual',</p>
<p>'claim_genre': '…',</p>
<p>'source_standing': '…',</p>
<p>'matrix_rule_ref': '…' }, # the governed verdict's rule</p>
<p>'provenance': { … }, # source, modality, locator</p>
<p>'floor_met': true # server-side; a below-floor ask returns a
refusal</p>
<p>}</p>
<p># a refusal returns the same shape with the refusal state, never a
bare error.</p></td>
</tr>
</tbody>
</table>

**Governance cannot be requested away.** There is no response mode that
returns the claim without its defensibility. The class is a field of the
claim object, the floor is enforced server-side, and the audit trail is
written whether or not the integrator reads it. A careless integration
cannot strip the governance, because the response contract does not
offer a shape in which the claim is separable from its class.

12\. The Data-Buying Path

The data-buying path is the governed-acquisition interface: a request
for a dataset or skill that passes the outer gate. The interface makes
the friction legible as assurance — the rights check, the
irreversibility transform, the cumulative-disclosure guard — and returns
a deliverable the buyer may lawfully use, with its per-item
defensibility intact. A file-out that would breach rights or reconstruct
identities across successive acquisitions is refused with the same
explained-refusal treatment as a below-floor answer.

**Part V — Operator, Governance, Control Interfaces**

13\. The Operator Surface

The operator surface is exception-first. It opens calm — a single
legible statement that the system is healthy — and surfaces an exception
only when a dimension crosses its threshold. It does not present
always-on dashboards; it presents attention when attention is warranted,
and quiet otherwise. Depth (the underlying volume, the specific tenancy,
the failing model) is one reach from each exception.

|                     |                                                                                    |
|---------------------|------------------------------------------------------------------------------------|
| **Exception class** | **Rendered when…**                                                                 |
| Throughput          | A queue, rate, or backlog crosses a health threshold.                              |
| Governance          | A floor is refused at rate, a class distribution shifts, or a gate result changes. |
| Tenancy             | A sensitive-tier tenancy or rights boundary needs attention.                       |
| Infrastructure      | Compute, substrate, or a perception model degrades against budget.                 |

14\. The Governance Surface

The governance surface is the DPO’s interface: the audit lens at the
scope of the whole system. It foregrounds the accountable record —
lawful basis on every run, refusals, the Northena Ledger, retention
state — as evidence retrievable on demand, not as logs to trawl. Any run
is reachable by its trace_id, and the record shown is the same one the
decision-maker’s audit lens reaches; there is one record, seen at two
scopes.

15\. The Control Surface

The control surface is the super-admin’s interface: high-privilege
functions in classes, each guarded and logged. It is administrative, not
editorial — it presents the functions as governed operations, every one
of which is versioned, diffed against its prior state, and written to an
audit trail on commit.

|                    |                                                                                                        |
|--------------------|--------------------------------------------------------------------------------------------------------|
| **Function class** | **What it controls (each action versioned, diffed, logged)**                                           |
| Taxonomy           | The Qualification Matrix and the source-standing declaration — the governed genre and standing tables. |
| Thresholds         | Governance thresholds — gate bars, floors’ class-defaults — within their owners’ authority.            |
| Access             | Roles, keys, and their scopes — who may reach which surface and which path.                            |
| Tenancy / tier     | Customer tenancy and sensitivity-tier configuration.                                                   |

**High-privilege actions are safe by construction.** Every control
action is versioned and diffed against its prior state before it
commits, and written to an audit trail on commit. Authority is total in
scope and never un-audited in exercise — a change to the taxonomy or a
threshold is a governed, reversible, recorded operation, not a silent
edit.

**Part VI — Interface Invariants**

16\. Invariants

Binding on any correct interface. A design that violates one fails the
specification regardless of how it looks.

1.  There is one entry. Sign-in routes each user to their surface
    deterministically on role; a multi-role user is offered a chooser,
    never a merged surface.

2.  Every surface opens calm and reveals depth on reach; no surface
    imposes detail on arrival.

3.  Wherever a unit of intelligence appears, its defensibility class
    appears with it in plain language — never suppressed, never rendered
    as a bare score.

4.  The three lenses render as one progressive view joined by trace_id;
    a user reaching deeper follows the thread and never re-finds the
    answer in another surface.

5.  A refusal-below-floor occupies the answer position as an explained
    state with a path forward — never an empty result, never a silent
    downgrade.

6.  The integration response contract returns the claim and its
    defensibility as one object; there is no response shape in which the
    claim is separable from its class, and the floor is enforced
    server-side.

7.  Key scope is enforced server-side at every call; no client-side
    action lets a key exceed its scope, and the data-buying path passes
    the outer gate.

8.  The operator surface is exception-first: calm when healthy,
    surfacing attention only when a threshold is crossed.

9.  One record, seen at two scopes: the DPO’s governance surface and a
    user’s audit lens reach the identical record by trace_id.

10. Every control-surface action is versioned, diffed against its prior
    state, and logged on commit; no high-privilege change is a silent
    edit.

**Status.** This specification is complete. It fixes the single entry
and its routing, the layout and behaviour of all six surfaces, the
rendering of the three lenses, the class and the refusal, and the
integration response contract in which governance travels inline. It
realises the UX Architecture Specification and defers to it on
experience matters. The build is staged from the entry and routing
outward; the specification is whole, and each surface is built as it is
reached.

---

## Unified Refusal Taxonomy

*Load-bearing addendum, post-A2. Documents the five governed refusal paths that ship today, the body-discriminator HTTP semantic (never status code), and the three non-overlapping render paths in the frontend. Sourced from shipped code — no synthetic behaviour.*

### The Five Refusal Paths

Five distinct refusal paths exist in the shipped system. Each has a contract, a service-layer emission site, and a consumer path.

| # | Refusal path | Envelope contract | Emission site | Correlation |
|---|---|---|---|---|
| 1 | **V2 governed refusal** (single-packet, terminal) | `V2RefusalEnvelope@v0` — `backend/contracts/v2_refusal.py` (frozen contract #12) | `services/v2_gate/refusal.py` | Absorbed into `LedgerRow.stamp_audit` via the side-channel; surfaces at `GET /api/northena/trace/{trace_id}` |
| 2 | **Service 1 composition-below-floor refusal** (governed refusal at `POST /api/service_1/run`) | `Service1Refusal@v0` — `backend/contracts/service_1_refusal.py` (frozen contract #14) | `services/service_1/service.py` (three raise sites: `no_defensibility_floor`, `no_lawful_basis`, `composition_below_floor`) | Envelope carries `run_id` + `trace_id` for join |
| 3 | **Solva assertion-boundary refusal** (below-floor conclusion at the Solva boundary) | `services/solva_depth/enforce.py::Refusal` (frozen `@dataclass`; not a Pydantic contract, threaded on the trace via `SolvaTrace.computed_class` at `services/solva_depth/pipeline.py` per X1 discipline — read once at the boundary, threaded downstream) | `services/solva_depth/enforce.py:37` via `enforce(conclusion_text, load_bearing_units, floor)` — comparison at `enforce.py:_below_floor` | Threaded to `SolvaTrace`; absorbed into ledger via `absorb_solva_trace` in Northena converge |
| 4 | **Northena Admit refusal** (at admit boundary) | `LedgerRow` with `stage="admit"`, `decision="refused"` | `services/northena/admit.py:156` | Ledger row itself carries `run_id`+`trace_id` |
| 5 | **Northena Gate refusal** (at gate boundary) | `LedgerRow` with `stage="gate"`, `decision="refused"` | `services/northena/gate.py:32` | Ledger row itself carries `run_id`+`trace_id` |

Refusal paths 1, 2, and 3 emit dedicated envelope contracts; paths 4 and 5 encode the refusal as a decision string on the frozen `LedgerRow` (`northena_ledger_row@v0`) rather than a separate envelope — the ledger row IS the record.

### HTTP Semantics — Body Discriminator, Never Status Code

At the HTTP layer, governed refusals are distinguished from validation errors and infrastructure faults **by BODY FIELD, not by HTTP status code**.

- **Governed refusal:** flat JSON body with `outcome: "refused"` at top level. HTTP status is `422`.
  - Emission site: `backend/routers/service_1.py:113-127` via `return JSONResponse(status_code=422, content=refusal.model_dump(mode="json"))` (A2 D3a settlement).
  - OpenAPI documents this: `responses={422: {"model": Service1RefusalContract, "description": "Governed refusal (outcome='refused'). Frontend keys on body.outcome === 'refused'. Distinct from FastAPI's validation-422 which has detail: list and no outcome field."}}`.
- **Validation error (Pydantic RequestValidationError):** FastAPI-default body with `detail: [<list of field errors>]`. HTTP status is `422`. **No `outcome` field.** Consumers key on `Array.isArray(body.detail)` **as a secondary check**, but the primary discriminator remains the absence of `outcome`.
- **Infrastructure fault:** any uncaught exception (Mongo outage, Pydantic internal `ValidationError`, etc.). HTTP status is `5xx`. Body is FastAPI-default `{"detail": "Internal Server Error"}` or the specific fault text. **Must never carry `outcome === "refused"`** — the router `except service.Service1Refusal` catch at `routers/service_1.py:120` is intentionally narrow to prevent silent conflation.

**The 422 status code is shared** between governed refusal and validation error. **The 500 status code is unique** to infrastructure fault. The frontend must never infer refusal from status code alone.

### Three Render Paths — No Overlap by Branching Logic

The shipped React frontend distinguishes three render paths in `frontend/src/pages/ComposePage.js:48-58`:

```
if (resp.ok)                               → success branch  (renders Service1RunSummary)
else if (data.outcome === 'refused')       → refusal branch  (renders RefusalCard, first-class)
else if (data.detail && Array.isArray(...))→ validation branch (renders inline error, field-scoped)
else                                       → infra-fault branch (renders unexpected-error banner)
catch (err) ...                            → network-fault branch
```

- **Governed refusal → first-class render.** Consumer contract: `Service1Refusal@v0`. Rendered by `frontend/src/components/RefusalCard.js` as a real product outcome; NOT rendered inside an error banner. Frontend gate tests: `frontend/src/__tests__/gate2_refusal_firstclass.test.js`.
- **Validation error → input feedback.** Consumer shape: FastAPI-default validation-422 body with `detail: list[<field-error>]`. Rendered as an inline compose-form error citing the failing field(s).
- **Infrastructure fault → system error.** Consumer shape: any 5xx body OR client-side network exception. Rendered as an unexpected-error banner — never as a refusal card.

**Branching logic is distinct.** The rendering surface for the last two paths (validation + infra) is a shared error banner today in `ComposePage.js`; the branching logic that reaches each is separate. Any consumer implementing these three paths must key on `body.outcome === "refused"` for path 1, `Array.isArray(body.detail)` for path 2, and the else-branch for path 3. HTTP status code is a hint, not a discriminator.

### Cross-Reference

- Backend handoff surface: `/app/docs/handoff/backend_contract_surface_v1.md` §2 route #17 error cell + §2.1 example blocks + §4 refusal semantics table.
- UX obligation: this specification §14 "Refusal-Below-Floor as a Visible, Explained Event" + UX Architecture Specification §14.
- Contract snapshot: `service_1_refusal.contract_snapshot.json` under `backend/tests/invariants/`.