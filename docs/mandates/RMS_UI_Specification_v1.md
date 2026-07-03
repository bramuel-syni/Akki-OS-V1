# RMS Intelligence System — UI Specification
## Version 1.0 · canonical (markdown) · binding

**Status: binding.** This document is the textual binding form of the six approved journey mockups plus the approved async additions. The builder implements structure, copy marked binding, and rules without interpretation. Figures, names, and percentages inside screens are **illustrative**; layout, elements, states, and the rules are **binding**. Anything not specified here or in the UX Architecture v2 is not licensed by omission — it is out of scope.

---

## 1. Global rules — every surface

1. **No build state on any surface.** No phase badges, gate names, fixture names, or engine names as navigation. The nav of a surface is its user's job, never the system's internals.
2. **Class-with-claim.** Wherever a claim appears, its defensibility class appears adjacent, in plain language (e.g. "Established fact", "Recorded statement"), in the headline position — never a buried score.
3. **Refusal rendering.** A governed refusal occupies the answer position with warning treatment. It names the gap, shows asked vs supported class, and offers only actions the user can take. It is never rendered as an error. Infrastructure faults render as system errors and **never** as refusals.
4. **Agent-assumed marking.** Any value an agent supplied carries an amber `agent-assumed` chip. Commit reviews separate "You supplied" from "Agent assumed — confirm or change".
5. **One trace thread.** Every intelligence element links to its trust receipt by `trace_id`. The public receipt at `rms.intel/trace/{id}` is read-only and is the same record the audit sees.
6. **Plain language.** No config syntax, enum values, or JSON on any user surface except the engineer's contract views (§4), where it is the product.
7. **Visual family.** Calm header (`product · role`), quiet defaults, single attention card for exceptions, bordered row lists, minimal chrome. Calm by default; the system brings the user what needs them.

## 2. Operator surface

### 2.1 Home — land
Elements: header (`RMS Intelligence · operator`) with **Commission objective** button; status line (binding copy pattern: "Running normally. One item needs you."); at most one attention card per exceeded threshold — what happened, the number vs threshold, one **Review** action; **Running** list — rows of objective name, entry type · stage (`Day zero work-order · mining`), budget consumed; capacity strip (approved addition, not in mockup): fleet apportionment and current consumption at a glance.
Rules: no dashboards or charts by default; exceptions appear only on threshold crossings; everything else stays quiet.

### 2.2 Commission — the shaping wizard
Layout: chat pane (left) + **Objective draft** rail (right).
Chat: operator states intent; agent **asks** for operator-mandatory fields, never proposes on them; estate-check chip renders inline before a feasibility-dependent question (illustrative: "4,180 hours match · 62% recorded statement · 21% established fact").
Draft rail: three dimensions + envelope with three visual states — filled (check), open (muted "— open"), agent-assumed (amber chip). Envelope line lists done-condition · budget · lawful basis until supplied.
Rules: mandatory fields (reach, output×4, done-condition, budget, lawful basis) are asked, never pre-filled; preference fields may carry agent recommendations; every turn is grounded in a real estate read — no fabricated availability.

### 2.3 Freeze — commit review
Elements: "You supplied" rows; "Agent assumed — confirm or change" rows (amber chip + **change** link each); feasibility verdict card (success treatment; binding copy pattern: "Floor feasible — {n}% of in-scope estate meets your standard"); envelope line (lawful basis ref · budget · commissioner · scope ceiling respected); **Freeze objective** button.
Binding copy: "Frozen is immutable — a changed intent is a new objective."

## 3. Ask console — first internal app

### 3.1 Ask
Elements: centered prompt — binding copy: "What do you need to know?"; single input; quiet defaults line ("Standard: … · Scope: … · change"); **Recent** list.
Rules: output is preset and invisible (composed conclusion · person · synthesized-whole · standing floor). **No output picker exists anywhere on this surface.** Wanting data or a different form is a new objective, made elsewhere.

### 3.2 Answer
Elements: question echoed in header; class badge + meta line ("{n} sources examined · answered in {t}"); headline finding (one sentence, plain); support paragraph; up to three metric cards; actions — **Why this answer**, **Export report**, **Trust receipt** link.
Rules: export is a rendering of the same artifact, class markings intact — never a data download, never a re-shape.

### 3.3 Refusal
Warning card in the answer position. Binding copy: title "Not to the standard you asked for."; body names the gap in the actor-appropriate form (pattern: "No corroboration at the required standard was found for the load-bearing claims. The statement itself is on record — it can be reported as a recorded statement, not asserted as fact."); line "Asked: {floor} · Supported: {class}"; actions (binding labels): **Accept as recorded statement** · **Narrow the objective** · **Lower the standard**.
Footer (binding copy): "A refusal is the system keeping its promise…" + **Why this was refused** link.

## 4. Engineer surface

### 4.1 Register an app
Elements: app name; class choice **Internal / External**; path choice with one-line grants — "Live query — inner gate · per-call governance · answers in responses" / "Governed extract — outer gate · rights-checked · datasets and skills out"; key grants panel stating in plain terms what the key permits ("External class · live query only · floor: … · scope: … · enforced server-side on every call"); **Issue key**.
Async additions (approved): optional **webhook URL** field with note "receives event + status only — never content"; **sandbox** toggle (key mode, served from fixture estate).

### 4.2 First call — the contract
Elements: request block (`POST /v1/objectives` with ask / standard / scope); two response panels side by side — **Answered** (`outcome`, `trace_id`, claim, `defensibility` inline, provenance) and **Refused — same envelope, body discriminator** (`outcome: refused`, `asked`, `supported_class`, `what_would_raise_it`).
Async addition: a third variant noted beneath — fresh-extraction asks return `202 { objective_id, accepted, delivery_estimate }`; status transitions appear in Administer.
Binding copy: "There is no response shape in which the claim is separable from its class. Infrastructure faults return 500 and are never rendered as refusals."

### 4.3 Administer
Elements: at most one attention card (pattern: app name — refusal rate — plain-language cause — **Review**); apps list rows — name + class badge, path + key, calls + refusal rate; extract-path rows show acquisitions + rights state; async addition: long-running objectives show lifecycle state (`accepted / running / delivered / refused`).
Footer (binding copy): "Key scope is enforced server-side on every call."

## 5. Buyer surface

### 5.1 Shape — buyer objective wizard
Layout: chat pane + **Your acquisition** rail.
Chat: buyer states need; agent **may propose** shapes and price levers (illustrative: "Narrowing to the last 5 years cuts the price by 38%…"); estate-check chip inline.
Rail: reach; output (form · grain · standard); license; price card — "Estimated price", figure, qualifying volume, binding copy "moves as you shape"; **delivery estimate beside price** (approved addition): served-from-qualified = fast; requires-fresh-extraction = queued, longer; feasible-and-offerable line.
Rules: shaping is bounded by offerability (owned estate, license class, disclosure limits) — out-of-bounds shapes are refused with the reason; buyer never sets lawful basis.

### 5.2 Acquire — the governed acquisition
Elements: framing line (binding copy): "Every acquisition passes the outer gate. These checks are what make the data lawfully yours to use."; four check rows with states — Rights check · Irreversibility transform · Cumulative disclosure check · License issue — each with a one-line plain description.
Binding copy (footer): "If any check fails, the acquisition is refused with the reason and a path forward — never partially delivered."

### 5.3 Receive — deliverable and receipt
Elements: delivered header + **Download**; artifact sample block showing per-claim structure (claim, `defensibility { class, contested }`, `provenance { source_ref, trace_id }`); **Outer-gate receipt** card — transform name, key fingerprint, identity categories transformed, license ref — fact and fingerprint only, nothing that could aid reversal; public trust-receipt line with URL pattern.

## 6. Master Admin

### 6.1 Home
Elements: pending banner in plain language ("Two rules are waiting on your decision before they can take effect." + **Review**); prompt "What do you want to do?"; six action buttons (binding labels): **Assign a role** · **Change a rule** · **Manage keys & access** · **Update the taxonomy** · **Set pricing** · **Apportion GPU capacity**; footer link "See everything I've changed — every action is recorded."
Rules: buttons and sentences only. No dashboards, no version strings, no config syntax anywhere on this surface.

### 6.2 Change a rule
Elements: "The rule" — one sentence stating what it does in everyday language; a short paragraph of current behaviour and what turning it on/off means; plain **Off / On** options with natural labels; "What changes" info box — one or two sentences, includes that nothing running now changes (when true) and that it can be switched back; commit button in natural language ("Turn it on").
Binding copy: "Recorded as your change, with today's date."

### 6.3 What I've changed — audit trail
Elements: confirmation line for the latest change (plain: what is now in effect, from when); recent actions rows — plain description of the change (from → to in words), who, when.
Footer (binding copy): "Every row carries its full diff. This trail is itself append-only and readable by the regulator surface."
Rule: the diff exists in the record; it is never the primary display.

## 7. Regulator / DPO

### 7.1 Home
Elements: trace lookup ("Look up any run, claim, or acquisition by trace…"); attention card stating problems honestly (pattern: "One retention window has passed — … It has not been auto-deleted; that rule isn't set."); three cards — runs with lawful basis, refusals this month + **See what was refused** link, retention windows past due.
Rules: adversarial to comfort — overruns, unset rules, and refusals are surfaced as problems and evidence, never hidden behind all-green summaries.
Footer (binding copy): "This is the same record every user's audit view reaches — read-only, nothing reconstructed for display."

### 7.2 Prove one run
Elements: lawfulness banner (LB ref · commissioner · frozen and immutable); record rows — Lawful basis (verified present at admission) · Scope (nothing mined outside it) · Refused ("{n} items — below the required standard, recorded not dropped" + **See them**) · Standard (enforced on every unit, server-side) · Ledger (append-only; current retention state stated honestly).
Footer (binding copy): "Read-only. This is the record itself, not a summary of it. Export for a regulator on request."

### 7.3 Retention & rights
Elements: honest banner (binding copy): "No deletion rule is set. The system holds everything indefinitely and append-only until you set a retention window. This is a decision only you can make — the system won't guess a duration."; holdings rows — within window / past due (+ **Decide**) / delivered acquisitions (irreversibly transformed · licensed · receipts on file).
Footer (binding copy): "Setting a retention window here becomes a governed rule — versioned, dated, and recorded like every control change."

## 8. Cross-surface bindings

- **Binding copy set** (verbatim across surfaces): "Not to the standard you asked for." · the three refusal action labels · "agent-assumed" · "Frozen is immutable — a changed intent is a new objective." · the §4.2 contract caption · the §5.2 acquisition framing and footer · the §7.3 retention banner.
- **Trust receipt**: public, read-only, resolves any delivered or rendered claim by `trace_id`; identical record across ask console, buyer deliverable, engineer responses, and DPO lookup.
- **Out of scope for this document**: partner-side portal (open item, candidate seventh surface), fleet arbitration UI beyond the operator capacity strip, any Phase 2 surface.
