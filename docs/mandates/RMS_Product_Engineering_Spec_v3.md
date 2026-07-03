# RMS Intelligence System — Product & Engineering Specification
## Version 3.0 · canonical (markdown) · fresh, whole-system

**Status: binding.** Supersedes v2.1 as the primary engineering brief. Defines the current whole system: the settled foundation by reference, and every engine and attribute converged in the design sessions in full technical and behavioural detail. Items marked `[STAKED]` are designer-supplied definitions awaiting the owner's strike-or-keep; items in §10 are open decisions with owners and are not filled anywhere in this document. Nothing else is ambiguous.

---

## 1. System definition and scope

Three layers: **Data Substrate** → **Data Extraction Service** → **Data Utilization / Applications Integration Substrate**. The **Registry** is the incremental, indexed, qualified record of the estate.

**Phase 1 scope (binding):** RMS-owned data only — broadcast archive, digital platforms (CMS), systems data, RMS-owned social accounts. Raw audio/video sale is out of scope (irreversibility cannot be honoured on raw media). Unowned/open-web collection is Phase 2 — a separate project, not specified here.

**Design-as-built rule:** this specification defines what must be true. Conformance of existing code is verified at the build gate at dispatch time (design↔build reconciliation is a builder execution step, never a design input).

## 2. Settled foundation (binding by reference)

The five engine/governance specifications remain binding: Product v2.1 architecture core, Northena (direction), Solva (depth), Mtafiti (discovery/measurement), Targeta (targeting). Unchanged and carried forward: the frozen `NormalizedUnit` (flat field names), five-rings defensibility model (genre ceiling authority-blind; standing only lowers), the three governors on three axes, the unified refusal taxonomy (body discriminator `outcome`, never status code; refusal ≠ validation ≠ infra fault), one `trace_id` threading unit → reasoning → record, the two-perimeter delivery (inner gate live, outer gate governed extract), append-only Ledger absorbing stamp-audit.

**Two verified facts folded in:**
- `NormalizedUnit` admits structured sources (`modality=TEXT`, free locator). No second intake contract is needed; a structured record becomes a unit without perception. The intake branch supplies TEXT-mandatory `extraction_params` for non-perceived sources.
- Nothing in the built execution layer branches on operation shape (`objective_shape` is a scoring input only; `mode` is a hardcoded pass-through). Shape-responsive execution (§4) is therefore a **build item**, not a description of current behaviour.

## 3. The Objective Service — NEW

The objective is the most important function in the extraction and application service. It is dynamic: it expresses its own shape and the system responds to what it expresses. No dimension is menu-picked.

### 3.1 The grammar — three dimensions

| Dimension | Declares | Values / range |
|---|---|---|
| **Entry point** | Where it originates | `work_order` (Day Zero, wizard-shaped) · `external_request` (Day-to-Day, arrives complete or is refused at admission) |
| **Reach** | Size and shape of the operation | breadth (estate slice: scope refs + exclusions) × depth (extraction/reasoning depth). Sizes mining volume, reasoning depth, compliance layers, workers |
| **Output** | What is produced | four fields: **form** (qualified_data · knowledge_artifact · model · callable_skill · composed_conclusion) · **consumer** (person · system · training_pipeline) · **grain** (per_claim · aggregated · synthesized_whole) · **standard** (defensibility floor) |

First build: one objective, one output. Frozen is immutable — a changed intent is a new objective.

### 3.2 The objective contract

```
ObjectiveRequest v2 (extends objective_request@v0 by addition)
  entry:      work_order | external_request
  reach:      { scope_refs[], exclusions[], depth }
  output:     { form, consumer, grain, standard }
  envelope:   { lawful_basis, done_condition, budget,
                scope_ceiling, availability_snapshot, floor_feasibility,
                commissioner, committed_at }
  shaping:    { agent_assumed_fields[], transcript_ref }     # work_order only
  commercial: { quote_ref, price_model_version }             # buyer path only
  idempotency_key                                            # external_request
```

Admission (maps to Northena Admit): an `external_request` missing any required field is refused with the validation envelope; a `work_order` cannot freeze until the wizard completes the envelope. Both admission paths write the Ledger.

### 3.3 The shaping wizard — one mechanism, two variants

**Operator variant (Day Zero).** Multi-turn conversation, one trusted operator.
- Field tiers: **operator-mandatory** (reach, output's four fields, done-condition, budget, lawful basis) — the agent asks, never proposes. **Preference** (weighting, ordering, formatting, sampling within budget) — the agent may recommend.
- Guards: (1) ask-don't-propose on mandatory fields; (2) every agent-supplied value marked `agent_assumed` — the commit review separates operator-said from agent-inferred; (3) every turn feasibility-grounded in the estate (§5).
- Enforcement: the operator reviews the complete marked draft and freezes. The operator is the check; no separate governor at one-trusted-operator scale.

**Buyer variant.** Same shaping mechanism, different ceiling.
- The agent shapes within **offerability**: owned estate only, license class, disclosure limits. Shapes outside offerability are refused with the reason.
- The agent **may propose** (steering a buyer to a cheaper feasible shape is sales, not laundering).
- Price and delivery-time (§8) compute live and move as the shape moves. The buyer never sets lawful basis; use-purpose drives license class.

## 4. Shape-responsive execution — NEW build item

The execution layer branches on the objective's expressed shape:
- **Reach sizes the operation**: mining volume, reasoning depth (Solva), compliance layers, worker allocation.
- **Warm/fresh fork at admission**: an ask servable from qualified intelligence is answered synchronously; one requiring fresh extraction returns the async contract (§7). The feasibility check (§5) makes this determination.
- **Intake branches by source structure**: perceived sources (raw AV) run the perception path; structured sources (CMS, social records) map fields to units directly (`modality=TEXT`), the branch supplying valid non-perception `extraction_params`.
- **Output form routes the transform** (§6) after mining completes.

## 5. Estate feasibility query — NEW

A Registry read returning, for a given reach: qualifying volume and the defensibility-class distribution. Consumed by both wizard variants (grounding every shaping turn) and by admission (the warm/fresh fork). Precondition: Registry freshness for the queried region — a stale or un-censused region returns `unknown`, never a fabricated distribution. Recorded into the envelope as `availability_snapshot` + `floor_feasibility` at shaping time.

## 6. The Transform Layer — NEW, full internals

Two stages: **mine** (extraction to qualified intelligence, sized by reach) → **transform** (qualified intelligence into the declared output, inside the system). The transform's input is stored qualified intelligence, not the live tail of a mining run.

**Provenance bound (machine-checkable, enforced at shaping time):** the transform produces the shaped output only where the declared standard survives it. Each form carries a provenance-preservation rule evaluable by the wizard; a form/grain whose rule cannot satisfy the declared standard is refused during shaping with a path forward — never discovered at execution. Surfaces **render** outputs and never re-shape them; a different form or grain is a new objective.

Per-form requirements on the six-point template — (1) definition, (2) production rule, (3) provenance-preservation rule, (4) grain compatibility, (5) delivery + governance mode, (6) standard enforcement point:

### 6.1 Qualified data — full
1. Per-claim units, each carrying defensibility class, contested status, provenance, `trace_id`.
2. Selection (reach + standard filter + license class) → packaging → outer-gate export (rights check, irreversibility, cumulative-disclosure, license issue, receipt).
3. Per-claim provenance intact end-to-end.
4. Grains: per_claim, aggregated. synthesized_whole unsupported (that is composed_conclusion).
5. Hand-over; governance enforced once at export via the outer gate.
6. Standard = hard input filter; below-floor units never enter the deliverable.

### 6.2 Composed conclusion — full
1. A synthesized answer to a specific ask, with class and trace.
2. Solva five-stage composition over selected units; load-bearing set identified; conclusion class = floor over load-bearing units' classes; trace mandatory.
3. Floor-over-load-bearing, carried as the conclusion's class; load-bearing set retrievable by `trace_id`.
4. Grain: synthesized_whole only.
5. Hand-over (rendered brief/report) or per-response on the live path; both carry class inline.
6. Enforced at conclusion class: below the objective's floor → the refusal envelope (asked / supported_class / what_would_raise_it).

### 6.3 Knowledge artifact — `[STAKED]`
1. `[STAKED]` A schema-versioned claim graph: nodes = claims (class, contested status, `trace_id` each), edges = Ring-3 relations (corroborates / contradicts / retracts). JSON export.
2. Selection per reach + standard → graph assembly from units and their relational edges.
3. Per-claim provenance intact at every node.
4. Grains: per_claim, aggregated.
5. Hand-over via outer gate (as 6.1).
6. Standard = input filter.

### 6.4 Callable skill — `[STAKED]`
1. `[STAKED]` A stay-running, key-scoped query capability over a defined corpus slice — an app queries it; it is not model weights. (The "trained behavior" reading of skill falls under §6.5.)
2. Corpus slice bound at freeze → endpoint provisioned → key scoped to it.
3. Per-response: every answer carries class inline (the live response contract), per-claim or composed per the query.
4. Grains: per_claim and synthesized_whole per query.
5. **Stay-running** via the inner gate: governance enforced per call, key scope server-side — the existing live-path enforcement mode, applied to a standing service.
6. Standard enforced per call; below-floor queries return the refusal envelope.

### 6.5 Model — off the offerable menu pending §10
1. Trained weights over a licensed slice. Training destroys per-claim traceability; the only honest guarantee is an **ingredient manifest** (provenance, standards, and license of what went in), not provenance of assertions.
2–6. Specified only if the owner accepts the manifest-level guarantee (§10). Until then the form is **not offerable**; the wizard refuses it with that reason. This is a deliberate, unambiguous state, not an omission.

## 7. Async delivery contract — NEW

- **Fork at admission**: warm → synchronous full response (existing contract). Fresh → `202` with `{ objective_id, status: accepted, delivery_estimate, quote? }`.
- **States**: `accepted → running → delivered | refused`. Sub-stages (mining, transforming) are detail on status reads, not states apps must handle.
- **Late refusal is first-class**: `accepted → … → refused` is a normal terminal state carrying the same refusal envelope. Integrating apps must render it as a governed refusal, never a failure.
- **Thin webhook, governed fetch**: webhook payload = `{ event, objective_id, trace_id, status }` — never claim content. The result is fetched over the app's authenticated key where scope is enforced. Polling `GET /v1/objectives/{id}` is the fallback. Rationale is binding: pushing claims to app-configured URLs would be an egress path the gates do not control.
- **No partial egress**, including on caller cancellation; a cancelled run is still ledgered.
- **Idempotency key** required on `external_request` submission; a retried POST must not double-commission or double-charge.
- **Versioning**: envelopes frozen and additive (the established A2 pattern); breaking change = new path version. **Sandbox** is a key mode set at registration, served from fixture estate.

## 8. Economics and capacity — NEW

- **Cost is measured; price is shaped.** Throughput (GPU-hours per broadcast-hour, per modality), unit yield, and cost per qualified unit come from instrumented real-material runs. All figures are illustrative until measured.
- **Price is config**: `price-model@vN`, versioned, swapped by the Master Admin control surface; every quote stamps its model version. Learning-phase quotes are structurally non-precedent: `price-model@v0-exploratory`, time-boxed.
- **Quote instrumentation** (the goal is understanding pricing dynamics, not scoring quotes): per quote — shape, model version, outcome (accepted / rejected / negotiated-to), the dimension negotiation stalled on, the first lever the buyer pulled.
- **Delivery time is the capacity signal** users see — never GPU numbers. Two cost classes: served-from-qualified (fast) vs requires-fresh-extraction (queued, longer, priced higher).
- **Fleet allocation is config**: `fleet-policy@vN` apportioning capacity across mining / transforms / live path, set at the control surface; the operator manages it live. Arbitration logic beyond apportionment is open (§10).

## 9. Surfaces — binding by reference

The UX Architecture v2 and the UI Document bind the six journeys: operator (land → commission → freeze), ask console (ask → answer → refusal), engineer (register → first call → administer), buyer (shape-with-price → governed acquisition → deliverable + receipt), Master Admin (plain-language actions; consequence visible; every change versioned, recorded, reversible), Regulator/DPO (adversarial-to-comfort; the record itself, read-only). Async additions to the engineer surface: webhook URL + sandbox toggle at registration; the objective lifecycle in the administer view.

## 10. Open decisions — recorded, not filled

| Item | Owner | State |
|---|---|---|
| Model form: is the ingredient-manifest guarantee acceptable under the defensibility promise? | Owner | Form off-menu until decided |
| Refused-after-acceptance acquisitions: does the buyer pay anything? | Owner | Commercial terms unset |
| Pricing model values | Owner, via instrumented practice | v0-exploratory only |
| Fleet arbitration logic beyond apportionment | Design (policy: Master Admin) | Simple apportionment holds until concurrency bites |
| Partner-side portal (external app's own runtime view) | Design | Candidate seventh surface |
| Retention window and deletion rule | DPO | System holds indefinitely, append-only, until set |
| Throughput / cost figures | Measurement (real material + GPU grant) | All figures illustrative until benchmarked |

## 11. Build doctrine (unchanged, restated as binding)

Phase-sized dispatches to sharp acceptance gates; contract-first — frozen contracts change by addition only; the standing hazard-stops (frozen-contract change, decision owed to an owner, substrate absent, gate failure / counting trip, seam-requires-invented-value); zero MATERIAL_GAP conformance at close; governance seams ship built-closed and unlock by config swap; design↔build reconciliation is scoped at dispatch, never absorbed silently.

## 12. System invariants (v3.0)

1. The objective is dynamic across all three dimensions; the system responds to what it expresses; nothing is menu-picked.
2. One objective, one output (first build); frozen is immutable.
3. Agent-supplied values are always marked; the user-said / agent-inferred seam stays visible to commit.
4. Shaping is feasibility-grounded; no objective freezes against a fabricated estate.
5. The provenance bound is enforced at shaping time; surfaces render, never re-shape; a new form or grain is a new objective.
6. Every output carries the strongest provenance its form permits, stated honestly — per-claim, floor-over-load-bearing, or (if accepted) ingredient manifest. No form is mis-promised.
7. Governance travels inline everywhere, including async: no response shape separates claim from class; webhooks never carry claims; nothing partial egresses.
8. Late refusal is a governed outcome, not an error, and is ledgered like every refusal.
9. Cost is measured before price is modelled; every quote stamps its price-model version; exploratory pricing is non-precedent by construction.
10. High-privilege change is plain-language, consequence-visible, versioned, recorded, reversible — never silent.
