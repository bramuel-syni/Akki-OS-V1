# RMS Intelligence System — UX Architecture Specification
## Version 2.0 · canonical (markdown)

**Status: binding at the level of experience architecture.** Supersedes v1.0. Records the converged design of this working session; open decisions are marked open with owners, never filled by drafting. The concrete screens live in the companion UI Document; engineering contracts in the Product & Engineering Specification.

---

## 1. What the experience must deliver

The system produces governed intelligence — claims honest about how defensibly they may be asserted. The experience must make that intelligence usable by people who are not analysts, and make the governance **felt as trust, not operated as machinery**. No surface mirrors the system's internals; every surface is designed from its user's promise inward. An interface that renders the build (engines, gates, phases) instead of the product is a defect regardless of how faithfully it renders.

## 2. The architecture the experience serves

Three layers (per the owner's architecture): **Data Substrate** → **Data Extraction Service** → **Data Utilization / Applications Integration Substrate**. The Registry is the incremental indexed and qualified record of the estate.

**Scope, Phase 1:** owned data only — RMS's archive, digital platforms, systems data, and RMS-owned social accounts. Raw audio/video sale is out of scope (irreversibility cannot be honoured on raw media). Unowned/open-web data is Phase 2 — a separate project, not designed here.

## 3. The users and their promises

Every role, internal or external, is a first-class user with a promise. The surfaces exist to keep these promises.

| User | Promise |
|---|---|
| **Operator** | Commission extraction with confidence — shape a vague strategic intent into a committed, bounded, feasibility-checked objective — and hold confidence over volume, governance, and infrastructure without watching everything. The system brings you what needs you. |
| **Engineer** | Integrate governed intelligence into a product or pipeline fast, with governance travelling inline — impossible to strip — and administer the day-to-day integration workflow in one place. |
| **Data buyer** | Know what you are buying, acquire it lawfully (the friction is the assurance), and use it with confidence — per-item defensibility and a verifiable receipt. |
| **Master Admin** | Total control over what the system permits — roles, rules, keys, taxonomy, pricing, capacity — exercised in everyday language, with every change recorded, reversible, and never silent. |
| **Regulator (DPO)** | Prove, on demand, that any run was lawful and accountable — on a surface built to be checked against, not to reassure. |
| **Internal app users** (decision-maker via the ask console) | Ask what you need in plain language; get an answer you can act on and defend, without becoming an analyst. |

## 4. The objective — the core experience primitive

The objective is the most important function in the extraction and application service. It is **dynamic**: it expresses its own shape and the system responds to what it expresses. Nothing is picked from fixed menus.

### 4.1 The grammar — three dimensions
1. **Entry point** — internal work-order (Day Zero, shaped through the wizard) or external request (Day-to-Day, arrives complete through the API or is refused at admission).
2. **Reach** — breadth × depth. Sizes the operation: mining volume, reasoning depth, compliance layers, workers.
3. **Output** — four declared fields: **form** (qualified data · knowledge artifact · model · callable skill · composed conclusion), **consumer** (person · system · training pipeline), **grain** (per-claim · aggregated · synthesized-whole), **standard** (the defensibility floor the output must meet).

First build: one objective, one output. A changed intent is a new objective — frozen means immutable.

### 4.2 The commit envelope
Beyond the three dimensions, a shaped objective freezes only with: lawful basis, done-condition, budget, scope ceiling + exclusion set, availability snapshot + floor feasibility (recorded at shaping time), attribution (commissioner, committed_at).

### 4.3 The shaping wizard — two variants, one mechanism
- **Operator variant (Day Zero):** multi-turn; the agent **asks, never proposes** on mandatory fields; every agent-supplied value is **marked** and the commit review separates operator-said from agent-inferred; each turn is **feasibility-grounded** in the estate. The operator reviews and freezes — the operator is the check at one-trusted-operator scale.
- **Buyer variant:** same shaping mechanism, different ceiling — the agent shapes within **offerability** (owned estate, license class, disclosure limits) and **may propose**, because steering a buyer toward a cheaper feasible shape is sales, not laundering. Price and delivery-time compute live as the shape moves.

### 4.4 The transform layer
Two stages: **mine** (extraction to qualified intelligence, sized by reach) then **transform** (qualified intelligence into the declared output, inside the system). **Provenance bound:** the transform produces the shaped output only where the declared standard survives it; an output whose form or grain would destroy required provenance is refused at shaping time with a path forward. Surfaces **render** outputs; they never re-shape them — a different form or grain is a new objective (no micro-analytics drift through export).

## 5. The trust model

- **Progressive:** the answer, then the reasoning on reach, then the accountable record on reach — one `trace_id` threads all of it and every surface.
- **Class always present:** wherever a claim appears, its defensibility class appears with it, in plain language, as the headline — never a buried score.
- **Refusal is first-class and actor-appropriate:** it occupies the answer position, names the gap, and offers only actions the user can actually take (accept as recorded statement · narrow the objective · lower the standard). A refusal is the system keeping its promise.
- **Receipts:** the outer-gate receipt renders fact and fingerprint of the transform only — nothing that could aid reversal. Any delivered item resolves at a public, read-only trust receipt by `trace_id` — the same record the audit sees.
- **Refusal ≠ error:** governed refusals are distinguished by body discriminator, never status code; infrastructure faults are never rendered as refusals.

## 6. Per-surface experience principles

- **Operator:** exception-first. Calm when healthy; surfaces exactly what needs a human when a threshold crosses. Commissioning is the wizard; fleet capacity view sits beside per-objective budget burn.
- **Engineer:** contract-forward. Register (class + path, key grants stated plainly) → first call (the response contract with governance inline) → administer (apps, keys, usage, refusal health). Key scope is enforced server-side on every call.
- **Buyer:** objective-guided sale. The buyer shapes what they need; price and delivery-time move with the shape; the outer-gate checks render as the assurance that makes the data theirs; the deliverable carries per-claim class and the receipt.
- **Master Admin:** everyday language, plain actions. Rules stated as what they do; changes shown as what changes, in sentences; consequence visible before commit; every action recorded, dated, reversible. Simple to act on — never a config editor.
- **Regulator (DPO):** adversarial to comfort. Surfaces what can be independently checked — refusals as evidence the governance bites, retention overruns and unset rules shown as problems, never a wall of green. Read-only; the record itself, not a summary.
- **Internal apps (ask console):** one plain question; output preset (composed conclusion · person · synthesized-whole · their floor); no output picker; export is a rendering of the same artifact with class markings intact.

## 7. Economics in the experience

- **Cost is measured, price is shaped.** Throughput and cost-per-qualified-unit come from real-material runs; price is set above measured cost.
- **Price is config, not code:** versioned models (`price-model@vN`); every quote stamps its model version. Learning-phase quotes are structurally marked non-precedent (exploratory tier, time-boxed).
- **Capacity reaches users as delivery time,** never GPU numbers: acquisitions from already-qualified intelligence quote fast delivery; fresh-extraction acquisitions quote queued, longer delivery. Fleet allocation policy is a Master Admin control; live management is the operator's.
- **Instrument the shaping:** quotes log accepted / rejected / negotiated-to per shape, where negotiations stall, and which lever buyers pull first — the goal is understanding pricing dynamics, not scoring quotes.

## 8. Open decisions — recorded, not filled

| Open item | Owner | State |
|---|---|---|
| Transform-layer internals (production + provenance rules for knowledge artifact, model, callable skill, composed conclusion) | Design (with owner) | Only qualified-data has defined semantics |
| Fleet allocation arbitration logic | Design (policy: Master Admin) | Surface exists; arbitration undesigned |
| Pricing model values | Owner, via instrumented practice | Mechanism designed; v0-exploratory |
| Partner-side portal (external app's own runtime view: usage, refusals, license, key health) | Design | Unaccounted surface — candidate seventh |
| Async contract mechanics (webhooks/callbacks for long-running objectives, contract versioning, sandbox) | Design | First-call contract only is specified |
| Retention window & deletion rule | DPO | System holds indefinitely, append-only, until set |
| Throughput/cost figures | Measurement (real material, GPU grant) | All current figures illustrative |

## 9. Invariants

1. Every surface is designed from its user's promise inward; no surface renders the build.
2. The objective is dynamic across all three dimensions; the system responds to what it expresses.
3. Governance is felt, not operated; class is always present; refusal is first-class and actor-appropriate.
4. One `trace_id` threads answer → reasoning → record across every surface; the DPO reads the same record.
5. Surfaces render outputs; only a new objective re-shapes one. The provenance bound is enforced at shaping time.
6. Agent-supplied values are always marked; the seam between user-said and agent-inferred stays visible to commit.
7. High-privilege change is plain-language, consequence-visible, versioned, recorded, reversible — never silent.
8. The friction of acquisition is rendered as assurance; nothing partial ever egresses.
9. Cost is measured before price is modelled; no invented figure ships as a real one.
10. Open decisions are surfaced honestly on the relevant surfaces (e.g. the unset retention rule on the DPO surface) — never papered.
