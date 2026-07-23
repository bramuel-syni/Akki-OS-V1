**AKKI · GOVERNED ARTIFACT · UX ARCHITECTURE**

**Surface & Journey Map v1.0**

The three user motions, the two day-zero dashboards, and the surface inventory that follows from them · 2026-07-15

***Origin and status:** Owner-framed at the UX review of 2026-07-15 (“the system must be built around the way humans extract and consume data”); drafted by the ruling authority for Owner review. This document is the ruling artifact for UI/UX sequencing: surfaces build against this map, not against feature availability. Audience: no prior context assumed. The platform: Akki — a governed intelligence platform installed inside an organization’s perimeter that turns its data estate into provable answers, products, and owned models. Every capability named below exists in the backend unless marked GAP.*

**§1 — The design law**

**Surfaces follow human motions, not platform modules.** The prior UI grew around one page (Ask) because the build was backend-first; this map corrects the frame. Three distinct motions exist, performed by different people at different moments, and they must never be collapsed into one surface again (RULED). Every screen belongs to exactly one motion; a screen serving two masters serves neither.

**Professional register:** target users are estate managers, analysts, engineers, compliance officers — people who live in warehouse-management, BI, and audit tooling. Surfaces are simple (1-2-3 steps, one primary action per screen) but seasoned: dense-information-calm-layout, numbers with provenance, zero marketing chrome inside the product. The trace page’s progressive-disclosure pattern is the house standard.

**§2 — The two day-zero dashboards (day-zero success, RULED)**

**§2.1 The Registry Dashboard — the warehouse floor**

**What it is:** inventory management for the data estate — because that is literally what the platform is. The estate manager’s home screen.

-   **Connected:** every source (archive mounts, DB connectors), its status, last census, rights posture, license class — the “what’s plugged in” rack view.

-   **Holdings:** census composition — volumes, media types, languages, eras, quality strata — rendered as a warehouse map, drillable to stratum level. Values + insights: coverage numbers, growth since last census, occurrence-index highlights.

-   **Intelligence on the inventory:** the standing opportunity Opportunity Briefs (info-memo class, advisory, refreshed with the census — never a gate); coverage-to-objective bars for live objectives; extraction activity (what’s mining now, what’s queued).

-   **Backend status:** census machinery BUILT · registry reads BUILT · Opportunity Briefs BUILT · coverage-to-objective SPEC’D (P1, Targeta phase) · the dashboard surface itself GAP — highest-priority build.

**§2.2 The Trust Center — the DPO’s warehouse of rules**

**What it is:** the same inventory idea applied to governance — every rule the instance runs under, and how it has been respected or violated. The compliance officer’s home screen.

-   **The rule inventory:** seam values (all six, current settings, who set them, when, initial-set vs changed), retention windows, license classes in force, active refusal grammar — each rule shown with its enforcement (which gates prove it), per the rules-pay-rent doctrine.

-   **The respect record:** refusals issued (by class), quarantine events and their resolution, deletions executed through the authorized path, rule changes with their dual-control ceremony, de-identification activity — each walkable to its ledger receipt.

-   **The violation record, unhidden:** custody events (QA-7 class), failed attempts, threshold breaches — stated plainly with disposition status. A Trust Center that only shows green is marketing; this one is the audit surface, and its honesty IS the product.

-   **Backend status:** ledger BUILT · prove-a-run BUILT · seam-value ledger BUILT (MC-E3) · audit pages PARTIAL (master-admin only) · the unified Trust Center surface GAP — second-priority build.

**Day-zero success, restated as ruled:** onboarding (stages 0–2) ends with both dashboards live and populated — the estate manager sees their warehouse, the DPO sees their rules working. Test objectives run by master admin + DPO at commissioning verify parameters through these two screens — day-zero mining is verification, not value production.

**§3 — The three motions**

**§3.1 Motion V · Verification (master admin + DPO · commissioning-time, then periodic)**

-   Purpose: prove the instance’s parameters work before anyone relies on them — seam values hold, de-id fires, refusals behave, receipts walk end-to-end.

-   Journey (1-2-3): run a supplied test-objective pack against fixture + first-census data → watch each rail fire on the Trust Center → sign the commissioning record (ledgered).

-   Surfaces: Trust Center (§2.2) + a small Verification Runner (pick pack · run · see rail-by-rail results). Backend: gates + fixtures BUILT; runner surface GAP (small).

**§3.2 Motion E · Exploration (analyst / engineer · ongoing — the shopping floor)**

-   Purpose: discover what the estate holds and what it would support, BEFORE committing to purchase or integration. Pre-purchase by design (RULED).

-   Journey: browse the Registry Dashboard’s holdings → read standing Opportunity Briefs → converse with the agent (grounded in inventory + Opportunity Briefs): “what do we hold on X? what would answering Y take?” → coverage-gap answers auto-file extraction candidates → shortlist forms.

-   Surfaces: Registry Dashboard (§2.1) + Ask (exists — correctly scoped as this motion’s conversation, not the whole product). Backend: Ask + gap-filing BUILT; inventory-grounded agent context PARTIAL (registry reads exist; memo-grounding wiring is EAB-3-adjacent).

**§3.3 Motion C · Consumption (buyer / integrating engineer · the purchase and the pipe)**

-   Purpose: turn a shortlist into a governed fetch — buy a dataset, stand up a standing service, or integrate an application.

-   Journey (the wizard): design the fetch objective — what (strata, classes), at what floor (defensibility), under what rights (license class), delivered how (dataset export · API · standing service) → see cost/coverage preview (coverage-to-objective) → commission → receive with receipts + evaluation card.

-   Surfaces: the Objective Wizard — exists half-built as operator commissioning; must be reframed as the buyer experience (GAP: reframe + coverage preview + delivery-choice step). App integration: scoped keys + S1 API BUILT; developer surface (key issue, docs, envelope explorer) GAP.

**§4 — Surface inventory (the build list, priority-ordered)**

|                                           |            |                   |                                                                                                           |
|-------------------------------------------|------------|-------------------|-----------------------------------------------------------------------------------------------------------|
| **Surface**                               | **Motion** | **Status**        | **Build note**                                                                                            |
| Registry Dashboard                        | E (home)   | GAP               | Priority 1 — day-zero success artifact; warehouse metaphor; drillable census + Opportunity Briefs + activity           |
| Trust Center                              | V (home)   | GAP (parts exist) | Priority 2 — unifies prove-a-run, audit pages, seam-value ledger, quarantine record into one DPO home     |
| Objective Wizard (buyer-framed)           | C          | PARTIAL           | Priority 3 — reframe commissioning console: fetch design · coverage preview · delivery choice · receipts  |
| Ask (agent conversation)                  | E          | BUILT             | Keep; deepen grounding to inventory + Opportunity Briefs (EAB-3-adjacent); refusal classes render distinctly (adopted) |
| Verification Runner                       | V          | GAP (small)       | Test-pack runner over existing gates; commissioning sign-off writes ledger row                            |
| Trace Receipt (public)                    | All        | BUILT             | House pattern for progressive disclosure; already promoted to /trace/:id                                  |
| Developer surface (keys, docs, envelopes) | C          | GAP               | Rides first real integration; not before (rules pay rent)                                                 |
| Model Registry / MOAC view                | E/V        | GAP               | Registry + evaluation cards exist as data at MOAC adoption; surface rides first trained model             |

**§5 — Rules and sequencing**

-   **SJ-1 ·** Every screen belongs to exactly one motion; cross-motion screens are a finding.

-   **SJ-2 ·** Day-zero success = both dashboards live at stage-2 close; verification (Motion V) precedes any value claim to the customer.

-   **SJ-3 ·** Opportunity Briefs are info-memo class — advisory, standing, refreshed; never approval gates (RULED).

-   **SJ-4 ·** Mining is ongoing conversation + commissioning, never a launch ceremony; BM-V attaches to the first product from mining, not to day one.

-   **SJ-5 ·** Surfaces build in inventory order (§4) after the designer walkthrough (OD-3) reviews this map; no UI phase dispatches against feature availability.

-   **Sequencing:** this map lands as canon → OD-3 walkthrough reviews it → UI phases enter the lane after EAB (or interleaved at ruling-authority judgment). The surface-inventory audit (read-only) runs against §4 to verify the status column before any build.

Syni.ai · Surface & Journey Map v1.0 · 2026-07-15 · Companion to: UI Spec v2.2 · Transformation Quality Spec v1.0 · Critic Seam Spec v1.0
