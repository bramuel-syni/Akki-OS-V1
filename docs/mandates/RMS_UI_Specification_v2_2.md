RMS Intelligence System
UI Specification — Version 2.2
Status: canonical, binding. Supersedes UI Specification v1, v2.0, and v2.1 in full. This document is self-contained: every screen of every surface is specified here — elements, binding copy, and rules — with no content carried by reference. The builder implements structure, rules, and copy marked BINDING COPY without interpretation. Figures, names, and percentages inside screens are illustrative; layout, elements, states, and rules are binding. Anything not specified here is not licensed by omission.
What v2 changes (owner harmonization, 2026-07-06). The platform has exactly four surfaces — consoles — defined by what can be done on them, not by a named person. Everything with an end-user in it, RMS-internal included, is an application built on the platform and enters through the Integration Console. New in v2.0: the rule-class split between Compliance and Administration and the consequence-class checker (Section 8). v2.1 (owner ruling, 2026-07-06) removes ALL commercial attributes from the extractor. Data sales is an application-layer service, separate, consuming the governed-extract API like any other application. Everything commercial — the buyer flow, sales provisioning, price display, pull-sampling-for-purchase — is cut from this document and rehomed to a separate Sales Service specification (stubbed, Section 12). The extractor has four operator consoles and one machine boundary (the governed-extract API, Section 5.5); it has no notion of price, offer, quote, catalogue, or buyer. Migration and the subtractive-cut list are Section 11. **v2.2 (owner amendment, 2026-07-08) adds §3.7 Opportunity Briefs under the Extraction Console — the recommendation surface consuming the Registry census; advisory output, never a governed claim.**
Precedence: Engineering Specification v3 governs contracts and behavior; this document governs surfaces; UX Architecture v2 governs experience rules; Build Completion Requirements v1.2 governs unbuilt work. Conflicts are HAZARD-STOPPED, never self-resolved. Marking: [OWNER] owner-supplied value; [config] versioned configuration value; [STAKED] designer position awaiting owner strike.
# 1. Global rules — every surface, every application
RULE  No build state on any surface. No phase badges, gate names, fixture names, or engine names as navigation. The navigation of a surface is its user's job, never the system's internals.
RULE  Class-with-claim. Wherever a claim appears, its defensibility class appears adjacent, in plain language (e.g. “Established fact”, “Recorded statement”), in the headline position — never a buried score. There is no render path in which a claim is separable from its class.
RULE  Refusal rendering. A governed refusal occupies the answer position with warning treatment. It names the gap, shows asked versus supported class, and offers only actions the user can actually take. It is never rendered as an error.
RULE  Four response classes, never conflated: governed refusal (outcome discriminator in body) · validation error · infrastructure fault (500/503, never dressed as refusal) · access-control denial (403 with {reason, detail}, never carrying an outcome key, never rendered through the refusal card).
RULE  Agent-assumed marking. Any value an agent supplied carries an amber agent-assumed chip. Commit reviews separate “You supplied” from “Agent assumed — confirm or change”. The seam between user-said and agent-inferred stays visible to commit.
RULE  One trace thread. Every intelligence element links to its trust receipt by trace_id. The public receipt at /trace/{id} is read-only and is the same record the compliance audit reaches.
RULE  Plain language. No configuration syntax, enum values, or JSON on any surface except the Integration Console's contract views (5.2), where the contract is the product.
RULE  Visual family. Calm header (product · role), quiet defaults, at most one attention card per exceeded threshold, bordered row lists, minimal chrome. Calm by default; the system brings the user what needs them.
# 2. The surface taxonomy
## 2.1 Four consoles — capability-defined

| Console | What can be done on it |
| --- | --- |
| Extraction Console | Shape and commission objectives; sample before committing; observe extraction quality live; administer the Registry; manage capacity and budget burn |
| Compliance Console | Own and update the compliance rulebook; monitor enforcement; set retention; prove any run to its lawful record; export for a regulator |
| Integration Console | The only door to the extractor's outputs, internal and external alike: register applications, issue and scope keys, expose the contract, provision data sales, sample the pull shape, monitor usage and refusal health |
| Administration Console | Reach everything; define roles and rights per console; own the operational rulebook (pricing, fleet, taxonomy); counter-sign per Section 8 |

## 2.2 The application tier and the boundary rule
Applications are anything with an end-user in it — internal or external. The boundary is mechanical, not organizational:
RULE  If a person who is not running the platform touches it, it is an application, and it enters through the Integration Console like any external party. Internal privilege is a key class (internal), never a back door — enforced server-side on every call.
## 2.3 Reclassifications — nothing deleted
The ask console becomes the Internal Reference Application (Section 7.1) — one reference implementation of an application consuming the platform, not the definition of asking. It consumes the platform through an Integration-Console-issued key; it is not a platform surface.
RULE  The buyer flow is NOT in this document. Buying data is a commercial act performed in the Sales Service (Section 12), a separate application-layer product. No buyer ever touches a console or the extractor directly; a buyer is an end-user of the Sales Service, which itself holds a scoped external key and passes the governed-extract API (5.5) like any third party — no privileged path.

# 3. Extraction Console
## 3.1 Home — land
Header  RMS Intelligence · operator, with a Commission objective button.
Status line  Binding copy pattern: “Running normally. One item needs you.”
Attention  At most one attention card per exceeded threshold — what happened, the number versus the threshold, one Review action.
Running list  Rows of objective name, entry type · stage (e.g. “Day zero work-order · mining”), budget consumed. Mining-stage visibility renders inside running status.
Capacity strip  Fleet apportionment and current consumption at a glance, reading the fleet policy.
RULE  No dashboards or charts by default; exceptions appear only on threshold crossings; everything else stays quiet.
## 3.2 Commission — the shaping wizard
Layout  Chat pane (left) + Objective draft rail (right).
Chat  Operator states intent; the agent asks for operator-mandatory fields and never proposes on them; an estate-check chip renders inline before any feasibility-dependent question (illustrative: “4,180 hours match · 62% recorded statement · 21% established fact”).
Draft rail  Three dimensions (entry, reach, output) plus envelope, each field in one of three visual states — filled (check), open (muted “— open”), agent-assumed (amber chip). Envelope line lists done-condition · budget · lawful basis until supplied.
Sample action  Run a sample — available once reach is drafted. See 3.4 for full mechanics.
RULE  Mandatory fields (reach, the four output fields, done-condition, budget, lawful basis) are asked, never pre-filled. Preference fields may carry agent recommendations. Every turn is grounded in a real estate read — no fabricated availability, ever.
## 3.3 Freeze — commit review
You supplied  Rows of operator-stated values.
Agent assumed  “Agent assumed — confirm or change” rows, each with the amber chip and a change link.
Feasibility verdict  Success-treatment card; binding copy pattern: “Floor feasible — {n}% of in-scope estate meets your standard.”
Grounding marker  States whether the objective was sample-grounded or estimate-grounded. BINDING COPY variants: “Grounded by sample {sample_ref}” / “No sample run — estimates only.”
Envelope line  Lawful basis reference · budget · commissioner · scope ceiling respected.
Action  Freeze objective button.
BINDING COPY  “Frozen is immutable — a changed intent is a new objective.”
## 3.4 Sampling — sample-before-commit (lands with Phase 9)
A sample is a first-class narrow-reach objective whose results ground the full commit. It exists because full extraction carries a real resource commitment and because feasibility honestly returns unknown on un-censused reach — the sample converts unknown into evidence.
Trigger  Run a sample action on the wizard once reach is drafted; the operator bounds the sample (illustrative: 2 hours from the drafted reach).
Result card  Renders in the same feasibility position: volume found, class distribution observed, per-hour cost observed. Recorded into the commit envelope beside the availability snapshot.
RULE  Sample cost draws the objective's budget and is shown doing so. The commit review carries the grounding marker (3.3). A sample result is evidence, not a promise — it grounds estimates, it does not guarantee full-run yield.
## 3.5 Registry administration (capability; screens land with Phase 9)
View census state by estate region; trigger or schedule census passes; un-censused regions marked honestly as unknown. No screen detail is invented here — Phase 9 Stage A proposes screens against this capability statement, and until then this section licenses no build.
## 3.6 Quality observation (existing elements, named as capability)
Mining-stage visibility inside running status; per-objective yield and class distribution as extraction proceeds; threshold-crossing attention cards per the 3.1 rules.

## 3.7 Opportunity Briefs — what this estate can do

The recommendation surface: a consumer of the Registry census that proposes what the estate could be used for, grounded in census facts and real-world precedent. Advisory output — never a governed claim.

Home card. Extraction Console Home gains one quiet card: "What this estate can do." One line — "Estate analysis current as of {date} · {n} opportunity briefs · {n} new since last census" — one action: Explore. Threshold-attention rules do not apply; this card never demands attention.

Briefs view. Bordered row list. Each row: plain-language title ("Twenty years of Kikuyu political speech supports a political-discourse research corpus"); grounding line of census facts ("4,100 hours · 62% recorded statement · 1998–2015 · 214 recurring speakers"); precedent chip naming a real-world reference ("Similar: BBC Archive licensing programme"); amber advisory marker. BINDING COPY, verbatim on every row and every brief: "Advisory — not a governed claim."

Brief scopes. Briefs come in three scopes, rendered in the same row list with a scope chip: Slice (one census region → one opportunity); Combined (two or more census regions whose intersection or join supports an opportunity neither supports alone — the grounding line cites each contributing slice's facts separately); Estate (the archive taken whole — grounding line cites estate-level census totals). Combined and Estate briefs state why the combination carries value beyond its parts, in one sentence. The "What's missing" section of a Combined brief names gaps per contributing slice, not collectively.

The brief. Three sections: What exists (the census slice or slices, rendered from Registry reads); What it could become (2–3 product shapes, each with a named real-world precedent and one line on how they monetized it); What's missing (honest gaps — rights, consent basis, licensing preconditions). One action: Shape as objective — pre-fills the commission wizard with the brief's reach. The brief's only exit is into the governed pipeline; it cannot publish, export, or transact.

Rules (binding). Every number in a grounding line is a live Registry read rendered verbatim — the generation layer may select facts, never produce them. No render path drops the advisory marker. Briefs sit outside the trust-receipt and trace system entirely. Generation runs behind the Shield. Briefs regenerate on census change, stamped "generated {date} against census {ref}"; superseded briefs are marked stale, never deleted.


# 4. Compliance Console
## 4.1 Home
Lookup  “Look up any run, claim, or acquisition by trace…”
Attention  Problems stated honestly. Pattern: “One retention window has passed — a 2019 call-in set is 14 days beyond its agreed hold. It has not been auto-deleted; that rule isn't set.”
Cards  Three: runs with lawful basis; refusals this month with a See what was refused link; retention windows past due.
RULE  Adversarial to comfort — overruns, unset rules, and refusals are surfaced as problems and as evidence the governance bites, never hidden behind all-green summaries.
BINDING COPY  “This is the same record every user's audit view reaches — read-only, nothing reconstructed for display.”
## 4.2 Prove one run
Banner  Lawfulness banner: lawful-basis reference · commissioner · frozen and immutable.
Record rows  Lawful basis (verified present at admission) · Scope (nothing mined outside it) · Refused (“{n} items — below the required standard, recorded not dropped” + See them) · Standard (enforced on every unit, server-side) · Ledger (append-only; current retention state stated honestly).
BINDING COPY  “Read-only. This is the record itself, not a summary of it. Export for a regulator on request.”
## 4.3 Retention & rights
Banner  Honest statement while unset. BINDING COPY: “No deletion rule is set. The system holds everything indefinitely and append-only until you set a retention window. This is a decision only you can make — the system won't guess a duration.”
Holdings rows  Within window / past due (+ Decide) / delivered acquisitions (irreversibly transformed · licensed · receipts on file). Held-classes render separately addressable: ledger rows, wizard transcripts, delivered artifacts — the compliance owner can scope one window or split per class.
BINDING COPY  “Setting a retention window here becomes a governed rule — versioned, dated, and recorded like every control change.”
## 4.4 The compliance rulebook (NEW)
The Compliance Console owns writes to the compliance rule classes: retention windows · disclosure thresholds (k-anonymity, l-diversity, differential-privacy budget) · the lawful-basis registry · the source-standing table. Rendering reuses the established plain-language rule pattern (6.2 mechanics): the rule as a sentence, current behavior, what changes, recorded with date. It is re-used, not redesigned.
## 4.5 Write mechanics under the checker (Section 8)
Tightening  Protection-tightening changes are unilateral: ledgered, effective after [config: effective_delay], with a recorded-objection path that escalates to the owner. Objections are themselves ledgered.
Loosening / destructive  Anything triggering deletion, lengthening retention, or weakening a threshold enters pending-counter-sign and takes effect only on Administration Console counter-signature; both identities are ledgered in one row.

# 5. Integration Console
## 5.1 Register an application
Fields  Application name; class choice Internal / External; path choice with one-line grants — “Live query — inner gate · per-call governance · answers in responses” / “Governed extract — outer gate · rights-checked · datasets and skills out”.
Key grants panel  Plain-terms statement of what the key permits: “External class · live query only · floor: … · scope: … · enforced server-side on every call.”
Async fields  Optional webhook URL with note “receives event + status only — never content”; sandbox toggle (key mode, served from fixture estate).
Action  Issue key. Grant issuance and revocation emit ledger rows.
## 5.2 First call — the contract
Request block  POST /api/objectives with ask / standard / scope.
Response panels  Two side by side — Answered (outcome, trace_id, claim, defensibility inline, provenance) and Refused — same envelope, body discriminator (outcome: refused, asked, supported_class, what_would_raise_it).
Async variant  Noted beneath: fresh-extraction asks return 202 { objective_id, accepted, delivery_estimate }; status transitions appear in Administer.
Fixture marking  The panel's sample JSON is clearly marked as illustration and is fixture-schema-gated: the sample parses through the frozen contracts. An unmarked sample is a hidden mock and is prohibited.
BINDING COPY  “There is no response shape in which the claim is separable from its class. Infrastructure faults return 500 and are never rendered as refusals.”
## 5.3 Administer
Attention  At most one card. Pattern: application name — refusal rate — plain-language cause — Review.
Applications list  Rows: name + class badge, path + key, calls + refusal rate; extract-path rows show acquisitions + rights state; long-running objectives show lifecycle state (accepted / running / delivered / refused / cancelled).
BINDING COPY  “Key scope is enforced server-side on every call.”
## 5.4 Dual-actor scoping (sequenced as 8-EXT)
Two roles, one console, identical screens, different scope — enforcement server-side, never view-layer filtering alone:

| Capability | internal_engineer | external_engineer |
| --- | --- | --- |
| Applications visible | all | own only |
| Grants visible | all | own only |
| Register application | yes | own, via approval |
| Issue / revoke keys | yes (ledgered) | own keys only (ledgered) |
| Usage & refusal view | all applications | own applications only |
| Estate contents | never (not this console's job) | never |
| Fleet / pricing | no (Administration) | no |

RULE  External-scope denials are 403 access-control class ({reason, detail}) — never outcome=refused, never the refusal card. Onboarding [STAKED]: external engineers are invited and approved by an internal engineer; open self-registration is a commercial decision, out of scope.
## 5.5 The governed-extract API — the machine boundary (operator-provisioned)
The Integration Console PROVISIONS access to the extractor's outputs; it does not itself sell, price, or transact. What it exposes is the governed-extract API — the single contract every application (internal or external, RMS-built or third-party) calls to reach extractor output. This section defines what the console provisions and what the API enforces; it defines no buyer-facing screen (those live in the applications that call it).
Provisioned here  Application registration (name, class internal|external, path live_query|governed_extract); key issuance and scope (floor, reach ceiling, license class, disclosure ceiling); offerability bounds for the key (which estate slices the key may reach); usage and refusal-health monitoring. All operator-side.
RULE  The API enforces, for EVERY caller with no exception for RMS-owned applications: the inner gate on live_query (per-call class inline) or the full outer gate on governed_extract (rights, irreversibility, cumulative-disclosure debit, license issue); server-side key-scope on every call; the four response classes (1). An application that appears to bypass any of these is a defect, not a tier.
RULE  No price, quote, offer, catalogue, order, or buyer-account concept exists on this console or in this API. Those are Sales-Service concerns (Section 12). The extractor charges nothing and knows no buyer; it governs access to output and records every egress. If a commercial decision (who may buy what, at what price) needs enforcing, it is enforced in the Sales Service BEFORE it calls this API — the API only sees a scoped key and a governed request.
Internal cost vs commercial price  The extractor's Administration Console owns internal cost/capacity economics (fleet apportionment, cost-per-unit telemetry) — needed to run the machine. It owns NO commercial price. The transfer relationship between extractor cost and any market price is a Sales-Service concern; this document specifies only that the boundary exists and that commercial price never appears on an extractor surface.
## 5.6 Dual-actor scoping continues to apply
The external_engineer (5.4) is an integrating partner's engineer wiring a partner SYSTEM to the governed-extract API — a platform-operator action performed by an outside party, legitimately seeing a scoped Integration Console view. This is NOT a data buyer. A buyer shaping a purchase is purely a Sales-Service end-user and sees no console. The two must never be conflated: external engineer -> scoped console; buyer -> Sales Service application only.

# 6. Administration Console
## 6.1 Home
Pending banner  Plain language, two backing classes: governance seams awaiting owner/compliance values, and items awaiting counter-signature (Section 8). Pattern: “Two rules are waiting on your decision before they can take effect.” + Review. Never a placeholder count.
Prompt  “What do you want to do?”
Actions  Six buttons, binding labels: Assign a role · Change a rule · Manage keys & access · Update the taxonomy · Set pricing · Apportion GPU capacity.
Footer  “See everything I've changed — every action is recorded.”
RULE  Buttons and sentences only. No dashboards, no version strings, no configuration syntax anywhere on this surface.
## 6.2 Change a rule
The rule  One sentence stating what it does in everyday language; a short paragraph of current behavior and what turning it on or off means; plain Off / On options with natural labels.
What changes  Info box — one or two sentences, natural language, includes that nothing running now changes (when true) and that it can be switched back.
Commit  Natural-language button (“Turn it on”).
RULE  Commit paths honor the registry-bump discipline: a committable rule writes a new versioned file server-side, recorded and reversible; a rule not yet committable through the surface states so honestly in plain language — the surface is never a bypass.
BINDING COPY  “Recorded as your change, with today's date.”
## 6.3 What I've changed — audit trail
Confirmation  Plain line for the latest change: what is now in effect, from when.
Rows  Recent actions — plain description of the change (from → to in words), who, when. Counter-signed changes show both identities.
RULE  The full diff exists in the record and opens on demand (collapsed link); it is never the primary display.
BINDING COPY  “Every row carries its full diff. This trail is itself append-only and readable by the compliance surface.”
## 6.4 Scope split — operational rulebook only
This console owns the operational rule classes: pricing models and tier locks, fleet apportionment, taxonomy. Compliance rule classes (4.4) render here read-only with the marker “owned by Compliance”.
## 6.5 Roles and rights (capability named)
Define roles and per-console rights; changes are plain-language, consequence-visible, and ledgered — the 6.2 pattern applied to role grants.
## 6.6 Counter-sign duties
The pending banner surfaces items awaiting this console's counter-signature with what changes, who initiated, and the consequence class. Symmetry rule: an Administration-side operational change that loosens protection requires Compliance counter-signature — the check binds both directions; there is no hierarchy between the two consoles.

# 7. Reference applications (binding application specs)
These are not platform surfaces. They are the first two applications, fully specified because they demonstrate the platform contract every future application follows.
## 7.1 Internal Reference Application — the ask console
### 7.1.1 Ask
Prompt  Centered. BINDING COPY: “What do you need to know?” Single input; quiet defaults line (“Standard: … · Scope: … · change”); Recent list.
RULE  Output is preset and invisible (composed conclusion · person · synthesized-whole · standing floor). No output picker exists anywhere on this application. Wanting data or a different form is a new objective, made elsewhere.
### 7.1.2 Answer
Elements  Question echoed in header; class badge + meta line (“{n} sources examined · answered in {t}”); headline finding (one sentence, plain); support paragraph; up to three metric cards; actions — Why this answer, Export report, Trust receipt link.
RULE  Export is a rendering of the same artifact, class markings intact — never a data download, never a re-shape.
### 7.1.3 Refusal
Card  Warning card in the answer position. BINDING COPY title: “Not to the standard you asked for.” Body names the gap (pattern: “No corroboration at the required standard was found for the load-bearing claims. The statement itself is on record — it can be reported as a recorded statement, not asserted as fact.”); line “Asked: {floor} · Supported: {class}”.
Actions  Binding labels: Accept as recorded statement · Narrow the objective · Lower the standard.
BINDING COPY  “A refusal is the system keeping its promise.”
## 7.2 Commercial applications — specified separately (Sales Service)
The buyer flow that v2.0 specified here is CUT and rehomed to the Sales Service (Section 12). It is a commercial application-layer product, not a reference implementation of the extractor contract, and folding it here re-fuses what the v2.1 ruling separates. What remains true and binding: any commercial application reaches extractor output ONLY through the governed-extract API (5.5), with a scoped external key, passing the full outer gate including the disclosure-budget debit — identical to any third-party caller. The Sales Service owns its own screens, its own admin, its own pricing and buyer-account model; none of it appears on an extractor surface.

# 8. The consequence-class checker (cross-console)
Consequential rule changes get a second pair of eyes — attached to consequence, not to role, so compliance independence is preserved and the check binds symmetrically.
Mechanism  Every rule class carries a registry attribute consequence_class: tightening_unilateral | dual_control.
Dual control  dual_control changes enter pending_counter_sign; effect only on the second console's signature; both identities and both timestamps ledgered in one row. Compliance-initiated loosening is counter-signed by Administration; Administration-initiated loosening is counter-signed by Compliance.
Tightening  tightening_unilateral changes take effect after [config: effective_delay] with a recorded-objection path escalating to the owner; the objection is itself ledgered.
Render  Pending items appear on both consoles' banners; the counter-signing console sees the full plain-language consequence statement before signing.
BINDING COPY  “Signed by {initiator} · counter-signed by {checker} · recorded with both identities.”
Honesty note, carried into the build record: while one person holds both roles, dual-control is ceremony — the seam is built now because it is cheap now and expensive to retrofit.
# 9. Sampling — extraction only in this document
v2.0 unified two samples as one primitive. v2.1 separates them: they were never the same thing.
Extraction sample (STAYS — Extraction Console 3.4)  A narrow-reach objective that spends the objective's GPU/extraction budget to convert feasibility unknown into evidence before the full-mine resource commitment. Pure capacity/quality planning; no commercial content. Fully specified at 3.4.
Pull sample (CUT — Sales Service)  A buyer-side sample of a prospective purchase, before buying, is a sales-demo act — commercial by nature. It is cut to the Sales Service (Section 12). Its one binding constraint on the extractor side, which the Sales Service MUST honor when it calls the governed-extract API: a sample is an egress — it passes the full outer gate and debits the cumulative-disclosure budget, or it is the assembly attack the disclosure ledger exists to catch (buy nothing, sample repeatedly, reconstruct the dataset). The extractor enforces this for the sample call exactly as for a full acquisition; the Sales Service cannot obtain a disclosure-free sample path.
# 10. Cross-surface bindings
The binding-copy set (verbatim wherever it appears): “Not to the standard you asked for.” · the three refusal action labels · “agent-assumed” · “Frozen is immutable — a changed intent is a new objective.” · the 5.2 contract caption · the 7.2.2 acquisition framing and footer · the 4.3 retention banner · the grounding markers (3.3) · the counter-sign line (Section 8) · “owned by Compliance” (6.4) · “Sample this pull” (5.6).
Trust receipt: public, read-only, resolves any delivered or rendered claim by trace_id; identical record across both reference applications, the Integration Console, and the Compliance Console.
# 11. Migration map and builder impact

| v1 / v2.0 | v2.1 home | Change |
| --- | --- | --- |
| §2 Operator | Section 3 Extraction Console | Rename + capabilities 3.4–3.6 |
| §3 Ask console | Section 7.1 Internal Reference Application | Reclassified as one reference app; screens fully restated here |
| §4 Engineer | Section 5 Integration Console | Rename + dual-actor scoping (5.4); commercial provisioning CUT; governed-extract API boundary added (5.5) |
| §5 Buyer / v2.0 §7.2 | Section 12 (Sales Service, stub) | CUT from the extractor; rehomed to a separate commercial product |
| v2.0 §9 sampling | Section 9 (extraction only) | Split: extraction sample stays (3.4); pull sample CUT to Sales Service |
| §6 Master Admin | Section 6 Administration Console | Scope split (6.4) + counter-sign (6.6); owns internal cost, NO commercial price |
| §7 Regulator/DPO | Section 4 Compliance Console | Rename + rulebook writes (4.4–4.5) |
| §8 bindings | Section 10 | Carried; commercial copy removed |

Builder impact — non-commercial changes: zero built operator screens demolished; navigation labels and role names update. B-5 consumes Section 4; because 4.4–4.5 add rulebook writes under the checker, B-5 splits [STAKED]: read/prove (4.1–4.3) first, rulebook writes + the Section 8 checker as follow-on. 8-EXT consumes 5.4. The consequence-class checker (Section 8) and the extraction sample (3.4) enter Build Completion Requirements; neither touches a frozen contract.
Builder impact — the commercial cut (owner ruling, 2026-07-06), specified in full in Build Completion Requirements v1.4: the buyer wizard (Phase 7 B-2 buyer variant), price/quote logic, dual-delta, and pull-sampling-for-purchase are CUT from the extractor build. Preservation is mandatory and verifiable — nothing is deleted:
Code  Moved to a salvage location outside the extractor build tree (directory or branch), removed from the extractor's tree, tests, and CI. Every line recoverable. Honest limit: this is a tested reference implementation for the future Sales Service, not a runnable module that switches back on — it assumed extractor scaffolding it no longer sits inside.
Frozen contracts  QuoteEnvelope_v0 and price-model configs: ORPHAN-IN-PLACE [STAKED — vacate is the alternative and needs a subtractive hazard-stop ruling]. Snapshot stays, parity count unchanged, nothing live imports them; a salvage copy goes to the Sales Service location. Audit history stays literally true; no subtractive precedent is set.
Salvage manifest  The builder produces a manifest at cut time: what moved, from where, to where, at what SHA — so 'preserved' is verifiable, not asserted. This is a named acceptance gate on the cut phase.
The boundary after the cut  The extractor retains internal cost/capacity economics (Administration Console) and the governed-extract API (5.5). It has no price, quote, offer, catalogue, order, or buyer. The Sales Service (Section 12), when built, calls that API with a scoped external key and passes the full outer gate including the disclosure debit — no privileged path.

# 12. Sales Service — separate product (stub)
This section is a STUB, not a specification. It exists to name the boundary and prevent the commercial concerns cut from this document from leaking back in. The Sales Service is a separate application-layer product with its own full specification, to be written when it is scoped. Nothing here licenses a build.
What it is  The commercial application through which data buyers discover, shape, price, purchase, and take delivery of extractor output. It is an APPLICATION, a client of the governed-extract API (5.5) — not a console, not part of the extractor.
What it owns  Catalogue and offers; commercial pricing, quotes, discounts, margin; buyer accounts and authentication; orders, fulfilment, receipts-to-buyer, refunds, disputes; a commerce-admin surface distinct from the extractor's Administration Console; pull-sampling-for-purchase as a sales-demo act.
What it does NOT get  No privileged path to the extractor. It holds a scoped external key like any third party and passes the full outer gate — rights, irreversibility, cumulative-disclosure debit, license — on every egress including samples. A disclosure-free or gate-free path for the RMS-owned sales business does not exist; that would be the separation in name only.
Single business vs marketplace  [STAKED] This stub assumes ONE sales business (RMS runs its own sales operation). If the intent is a marketplace (multiple commercial parties reselling extractor output), the commerce-admin model becomes per-tenant and the governed-extract API's key model must support multiple independent commercial callers — a materially larger design. Owner ruling required before the Sales Service is specified.
Salvage input  The Sales Service specification and build draw on the salvaged buyer-wizard code and orphaned commercial contracts (Section 11) as reference — recovered, not inherited.
— End of UI Specification v2.1 —
