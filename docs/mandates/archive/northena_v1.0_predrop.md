# Northena The Direction Governor — Mandate

The governed, verbatim specification of Northena: what it must do at each stage, what makes each decision valid, and what it writes.

**Governed Artifact  ·  Version 1.0  ·  binds the Northena reshape at build phase G2.**
**Prepared by Syni.ai  ·  June 2026  ·  Confidential**

This is a governed artifact, not a description. Where it states a rule, that rule binds the implementation of Northena. It is the companion to the Product & Engineering Specification v2.0 ("the Spec"), which defines Northena's place in the system (Spec §2.2, §3.2); this document specifies Northena's behaviour in full so the build can reshape it without paraphrasing. One decision in this document — ledger retention — is marked as requiring DPO confirmation; every other rule is settled.

---

## 1. What Northena Is
Northena is the direction governor: the component that keeps every run on-objective and brings it to a defined stop, and that writes the durable record of how the run was directed. It answers two questions, run after run — "is this still in scope?" and "is this run done?" — and it records the answers in an audit-grade ledger.

Northena is one of three governors operating on three independent axes. It must not absorb the work of the other two, and this mandate is written to keep those boundaries sharp.

| Governor | Axis | Question it answers |
| :--- | :--- | :--- |
| SyniSense | Boundary (in / out) | May this data cross this access point, and in what transformed state? |
| Northena | Direction (on-objective / convergent) | Is this still in scope, and is the run done? |
| Solva | Depth (sound / defensible) | Is the reasoning sound, is preservation sufficient, does the output assert within its defensibility? |

Northena governs both services, through their two governing artifacts: the Portfolio Mandate for Service 1 (Estate Extraction / Day Zero) and the Objective Request for Service 2 (Objective Extraction / Day to Day). It governs the run lifecycle; it does not define the contents of those artifacts, which are fixed by the Spec (§6) and their own mandates.

## 2. Design Principle — Deterministic by Construction
Northena is deterministic by construction. It contains no machine-learning model, no learned weights, and no adaptive behaviour. This is not a limitation the design tolerates; it is the property that makes Northena trustworthy as a governor.

### 2.1 Dynamism without learning
Northena's behaviour varies from run to run — it admits different objectives, gates different scopes, stops on different conditions, and writes different ledgers. But every part of that variation is driven by the frozen governing artifact it reads, not by Northena adapting. Its scope check is membership against the scope the artifact declares; its stop is a threshold check against the done-condition and budget the artifact fixes. Northena is dynamic the way a thermostat is dynamic: its behaviour changes completely as the setpoint changes, while the mechanism itself neither learns nor infers. That dynamism is sufficient for everything Northena must do.

### 2.2 Why it must not learn
The moment Northena learns — adjusts its gating from past runs, infers scope probabilistically, tunes its convergence by experience — it stops being auditable, and auditability is Northena's entire reason to exist. Its ledger is read by the DPO and by the operator audit lens. Any run must be answerable deterministically: admitted because these fields were valid, gated in because scope-membership held, stopped because this condition was met. A learned gate cannot give that answer — "admitted because the model scored it 0.72" is precisely the un-auditable, un-defensible outcome the system exists to avoid.

**The determinism rule.**
Northena performs presence checks, completeness checks, set-membership tests, threshold comparisons, and state transitions — all deterministic. It performs no inference. Any decision that would require judgement is Solva's: Northena may invoke Solva and then act deterministically on the result it returns, but Northena itself never reasons. See §9.

## 3. The Four Stages
Northena operates in four stages. Each is specified in §4–§7 as trigger, decision rule, and output. The stages are ordered but not strictly linear: in Service 2 they run as a loop (§8).

| Stage | Does | Decision is |
| :--- | :--- | :--- |
| Admit | Compiles a raw intent into a frozen governing artifact and freezes it | Validity check (presence, completeness, membership) |
| Gate | Checks whether a (sub-)objective is in the frozen artifact's scope; routes it | Strict set-membership |
| Converge | Decides whether the run is done | Threshold check (done-condition or budget) |
| Ledger | Writes the durable, audit-grade record of the run | None — it records, deterministically |

## 4. Stage 1 — Admit
Compile a raw intent into a frozen governing artifact, and freeze it.

*   **Trigger:** A raw intent enters the system: an internal job (Service 1 or an internal Service 2 objective), or a consumer request arriving at a terminal (an external Service 2 objective, contract-bounded).
*   **Function:** Admit compiles the raw intent into the governing artifact appropriate to the service — the Portfolio Mandate for Service 1, the Objective Request for Service 2 — and freezes it. Compilation resolves the intent into the artifact's fields; where that resolution needs judgement (for example, resolving an ambiguous scope or setting a preservation depth), Admit invokes Solva for assistance and then freezes the returned result. The freeze is Northena's act; the judgement, where any is needed, is Solva's.
*   **Validity rule (deterministic):** An admission is valid only if all of the following hold. Each is a deterministic check; a failure refuses the admission and writes a refusal to the Ledger.
    *   **Lawful basis present.** The artifact carries a lawful_basis; a run without one is refused (Spec §11.2, INV-16).
    *   **Completeness.** Every required field of the governing artifact is populated (Spec §6 for the Objective Request).
    *   **Scope resolves.** The declared scope resolves against the Registry — it names estate that exists.
    *   **Defensibility floor valid.** Where a defensibility_floor is declared, it is a well-formed floor the run can be held to (Spec §6.3).
*   **Output:** A frozen, immutable governing artifact, and an admission entry in the Ledger recording what was admitted, the artifact reference and version, the lawful basis, and the timestamp.
*   **Immutability.** Once frozen, the governing artifact is immutable for the run. Northena does not mutate it, and no downstream stage may. A changed intent is a new admission with a new frozen artifact — never an edit of a live one. This is what lets every later stage bind to a fixed shape.

## 5. Stage 2 — Gate
Is this (sub-)objective in scope? Route it accordingly.

*   **Trigger:** A compiled objective, or a sub-objective returned by the loop (§8), needs routing.
*   **Function and decision rule (strict set-membership):** Gate tests whether the (sub-)objective falls within the scope declared by the frozen governing artifact. Scope is a defined set; Gate checks membership. It routes on the result:
    *   **In scope, already converged/certified:** Warm-serve from the Intelligence tier (Spec §8.2).
    *   **In scope, not yet converged:** Fresh extraction — Layer D over the Normalized tier, with A→B→C fallback for un-converged slices.
    *   **Out of scope:** Refuse. Logged to the Ledger as a governed refusal — not an error, and not silently dropped.
*   **No inferential scope decisions.** Gate is strict set-membership. If membership is genuinely ambiguous, that is a compilation defect — Admit should have resolved it, with Solva's help, before freezing. Gate does not decide ambiguous membership by inference; it acts on the resolved scope in the frozen artifact. This is the sharpest edge of the determinism rule.
*   **Output:** A routing decision (warm | fresh | refuse) and a Gate entry in the Ledger recording the decision and its reason.

## 6. Stage 3 — Converge
Is the run done? Northena owns the stop.

*   **Trigger:** After each extraction or warm-serve cycle, and on each pass of the loop (§8).
*   **Decision rule (threshold check):** Converge decides whether to terminate, on two conditions fixed in the frozen artifact:
    *   **Done-condition met** — the completion criterion declared in the artifact is satisfied. Terminate: success.
    *   **Budget ceiling hit** — the resource ceiling declared in the artifact is reached. Terminate: budget-exhausted.
    *   **Neither** — continue; return to the loop.
*   Both are threshold checks against values the artifact fixed at Admit. There is no learned or adaptive stopping.
*   **Northena owns the halt.** The authority to stop a run is Northena's alone — not the engine's, not Solva's. Solva may report that it cannot reason further soundly; that report becomes an input Converge acts on, but the stop decision and its record are Northena's.
*   **Output:** A convergence decision (terminate-success | terminate-budget | continue) and a Converge entry in the Ledger.

## 7. Stage 4 — Ledger
The durable, audit-grade record of how the run was directed. The Ledger is Northena's memory and the system's primary audit surface for direction. It records every decision Northena made and the material events of the run. It is read by the DPO and the operator audit lens, and it is joined to unit-level intelligence by identifiers so the Author (justification) and Engineer (diagnostics) lenses can read it too (Spec §5 UX; the three trace lenses).

### 7.1 What the Ledger records
*   **Admission** — what was admitted, the frozen artifact reference and version, the lawful basis, and the timestamp.
*   **Gate decisions** — each routing decision and its reason (in-scope-warm, in-scope-fresh, or out-of-scope-refused).
*   **Refusals and drops** — every out-of-scope or refused item, so mis-framed requests are surfaced rather than lost. This is how the system shows what it declined to do.
*   **Convergence** — the stop decision and its reason.
*   **Absorbed stamp-audit entries** — the defensibility stamp's refusal/decision audit records. At build phase G1 these live in a side-channel buffer; from G2 the Ledger absorbs them (see §7.3).

### 7.2 The Ledger row — a contract-grade artifact
Because the Ledger is read by the DPO and the audit lens, its shape is a contract, not an internal log. It is frozen and versioned like any governed schema — snapshot plus invariant — and it is stable and audit-legible from the first build commit that writes it. The row carries at least the following.

| Field | Type | Description |
| :--- | :--- | :--- |
| run_id | string (uuid) | The run this row belongs to. One run has one closed Ledger. |
| trace_id | string | Joins the Ledger to unit-level intelligence and the three trace lenses. |
| stage | enum | admit \| gate \| converge — which stage wrote the row. |
| decision | enum | The stage's outcome (e.g. admitted \| refused \| warm \| fresh \| terminate_success \| terminate_budget \| continue). |
| reason | string | The deterministic reason for the decision (e.g. out_of_scope, done_condition_met, budget_exhausted, missing_lawful_basis). |
| artifact_ref | object | { artifact_type: portfolio_mandate \| objective_request, artifact_id, version } — the frozen artifact governing the run. |
| lawful_basis_ref | string | The lawful basis under which the run was admitted. |
| stamp_audit | object \| null | Absorbed defensibility stamp-audit entry when present: { unit_id, decision, reason, judged_signal_dimensions, floor_violation }. |
| at | string (iso 8601) | When the row was written. |

**No run without a closed Ledger.** A run is not complete until its Ledger is closed. A run with no closed Ledger row is an incomplete, non-auditable run and is invalid (N-INV-6). The Ledger is append-only: rows are added, never edited or deleted within the retention window.

### 7.3 Absorbing the defensibility stamp-audit
The Ring-5 defensibility stamper records why a stamp was assigned or a floor refused. Per the build decision at phase G1, those records live in a side-channel (a StampAuditEntry buffer) so the frozen DefensibilityRing stays byte-identical to its schema. From phase G2, Northena's Ledger absorbs those entries into the stamp_audit field above, joined by unit_id and trace_id. This keeps the unit (the output) and the audit (the trace of how it was decided) in separate envelopes with separate lifecycles, while making both readable from one audit surface.

## 8. The Northena Loop (Service 2)
In Service 2, the four stages run as a loop around Layer D and Solva, which is what lets a single objective resolve across several cycles and what densifies the warm Intelligence tier over time.

*   **Admit** compiles and freezes the Objective Request.
*   **Gate** routes the objective (or a sub-objective) warm or fresh, or refuses it.
*   **Layer D and Solva** execute the routed work and return results and any unmet gaps.
*   **Gaps return to Gate:** in-scope gaps are re-tasked to fresh extraction; out-of-scope gaps are logged to the Ledger and dropped.
*   **Converge** checks the done-condition and budget: terminate, or continue the loop.

Each answered objective adds to the Intelligence tier, so adjacent future objectives are cheaper to serve warm. The loop is Northena's; Layer D and Solva do the work inside it, but the direction — what to route, what to re-task, when to stop — is Northena's throughout.

## 9. The Determinism Boundary — Northena vs. Solva
This section is the operational form of the design principle (§2). It states exactly what Northena does and does not do, so the reshape cannot let direction drift into reasoning.

| Northena does (deterministic) | Northena does NOT do (Solva's) |
| :--- | :--- |
| Presence and completeness checks on the artifact | Judge whether reasoning is sound |
| Set-membership scope tests at Gate | Disambiguate scope by inference |
| Threshold comparison at Converge (done-condition, budget) | Judge defensibility, or set a defensibility floor by judgement |
| State transitions across the four stages | Judge preservation depth |
| Write the Ledger | Reason to a conclusion or certify an output |

**The interaction rule.** Northena may invoke Solva — at Admit, to resolve a scope or set a preservation depth or defensibility floor — and then acts deterministically on the value Solva returns. Northena never performs the judgement itself. Conversely, Solva never directs the run: it does not admit, gate, stop, or write the direction Ledger. The two governors are orthogonal and are never collapsed (Spec §2.2, N-INV-10).

## 10. Interfaces
Northena's interfaces are normative in shape and direction; field names illustrate structure.

*   **Intent → Admit:** A raw intent (internal job or consumer terminal request). Admit compiles and freezes it.
*   **Admit ↔ Solva:** Admit may request compilation assistance (scope resolution, preservation, floor); Solva returns values; Admit freezes them. Northena does not reason.
*   **Gate → execution:** A routing decision: warm-serve (Intelligence tier) | fresh (Layer D) | refuse.
*   **Converge → loop:** terminate-success | terminate-budget | continue.
*   **Northena → Ledger:** Contract-grade rows (§7.2), append-only.
*   **Stamp-audit → Ledger:** From G2, absorbs StampAuditEntry records by unit_id / trace_id (§7.3).
*   **Northena ↔ SyniSense:** Northena checks that a lawful_basis is present (direction); SyniSense enforces the boundary crossing (boundary). Orthogonal; neither performs the other's function.

## 11. Governance and Compliance
Northena is a governance component and carries direct compliance obligations under the Kenya Data Protection Act, 2019 (Spec §11). This section states design constraints; it is not a legal opinion.

*   **Lawful basis is enforced at Admit.** No run is admitted without a valid lawful_basis; purpose limitation is enforced at the point of admission, before any extraction.
*   **The Ledger is the accountability record.** It evidences, for any run, that a lawful basis was present and that direction was governed — the record the DPO relies on.
*   **Refusals are recorded, not hidden.** Out-of-scope and refused items are logged, so the system can show what it declined and why.
*   **Open decision — requires DPO confirmation.** Ledger retention is the one rule in this mandate not settled here, because it is a DPA-shaped decision that interacts with breach-notification and data-subject-rights obligations (Spec §11.4). Default proposed: the Ledger is append-only and immutable within a retention window, with no silent deletion; the retention duration and the deletion/immutability rule at end-of-window are to be confirmed by the DPO. Until confirmed, the build implements append-only immutability and leaves the retention duration configurable, defaulting to indefinite retention pending the decision.

## 12. Reshape Directive (build phase G2)
This section directs the build. Northena is a reshape, not a greenfield component: the foundation codebase carries the judge-a-flow-and-write-a-ledger pattern, but in a session-shaped form. The reshape lifts that discipline and re-forms it into a run-level, four-stage governor.

*   **Cousin substrate.** The pattern exists across the foundation's validator, grounding-contract, and audit-log code (session-shaped). Lift the ledger-writing discipline and the validator structure; do not copy the session shape.
*   **What is new.** The four-stage Admit / Gate / Converge / Ledger state machine; the per-run Ledger collection; the convergence judge; and stamp-audit absorption (from G2).
*   **Ledger first.** The Ledger row (§7.2) is contract-grade from the first commit — snapshot plus invariant — not an internal log tidied later.
*   **Governors never re-implemented.** Solva and SyniSense are integrated, not re-built inside Northena (Spec INV-1, INV-15).
*   **Rule 2 is live.** This is the first heavy reshape. If net-new code exceeds lifted substrate, pause and surface cut / proceed / re-sequence options rather than absorbing the rewrite silently.
*   **Dependency.** This mandate is the text the reshape binds to. It must be present and frozen before Northena integration begins at G2.

## 13. Northena Invariants
Binding invariants for Northena. Any implementation that violates one is incorrect regardless of behaviour.

1.  Northena is deterministic: it contains no machine-learning model, no learned weights, and no adaptive behaviour. Its dynamism is entirely a function of the frozen governing artifact.
2.  Any decision that would require inference is Solva's. Northena may invoke Solva and act deterministically on the result; Northena itself never reasons.
3.  Every run is governed by exactly one frozen governing artifact, admitted by Northena, carrying a valid lawful_basis. No run proceeds without one.
4.  The frozen governing artifact is immutable for the run. A changed intent is a new admission, never an edit of a live artifact.
5.  Gate is strict set-membership. Ambiguous membership is a compilation defect resolved at Admit, never decided by inference at Gate.
6.  Northena owns the halt. Converge terminates only on the done-condition or the budget declared in the frozen artifact.
7.  No run closes without a closed, audit-grade Ledger.
8.  The Ledger is a contract-grade artifact — versioned, snapshot-and-invariant, stable and audit-legible from the first commit that writes it. It is append-only and immutable within the retention window.
9.  Out-of-scope and refused items are recorded in the Ledger, never silently dropped.
10. From build phase G2, the Ledger absorbs the defensibility stamp-audit entries by unit_id / trace_id; the unit (output) and the audit (trace) remain in separate envelopes with separate lifecycles.
11. Northena governs direction only. Boundary is SyniSense; depth is Solva. The three axes are never collapsed, and Northena never performs another governor's function.

## 14. Open Decisions
One decision in this mandate is deliberately left open, to be closed by the named owner before the gate it blocks.

| Decision | Owner | Blocks |
| :--- | :--- | :--- |
| Ledger retention duration and end-of-window deletion / immutability rule (§11) | DPO | Not a build blocker for G2 integration — the build defaults to append-only immutability with configurable, indefinite retention until confirmed. Must be closed before any production data-subject-rights or retention obligation is exercised. |

**Status.** This mandate is complete and ready to bind the Northena reshape at G2, with the single retention decision flagged for the DPO. Every other rule is settled. Where the build finds a case this mandate does not resolve, it attempts a defensible reading consistent with the determinism principle (§2) and the invariants (§13), journals it, and surfaces it — it does not freeze an unconfirmed rule into the Ledger contract.
