**Northena**

The Direction Governor — Engine Specification

The complete specification of the direction governor: its four stages,
its determinism boundary, its contract-grade ledger, and the module
structure, typed contracts, algorithms, and test obligations that
implement it.

Engine Specification · Version 1.0 · elaborates the Product &
Engineering Specification v2.1 (§22), which prevails on conflict.

*Prepared by Syni.ai · July 2026 · Confidential*

This document is binding. It specifies Northena to full technical and
behavioural depth: Part I states what Northena must do and why; Part II
specifies how it is built — modules, typed contracts, the four stages as
algorithms, and the tests that discharge the invariants; Part III states
governance, invariants, and the one open decision. It is a forward
specification: it defines what must be true of any correct
implementation, and does not assume one exists. Points that resolve
against contracts defined elsewhere are marked **CONFIRM** and are
resolved against the real contract before use.

**Contents**

**Part I — Mandate**

1\. What Northena Is

Northena is the direction governor: it keeps every run on-objective,
brings it to a defined stop, and writes the durable, audit-grade record
of how the run was directed. It answers two questions, run after run —
is this still in scope, and is this run done — and records the answers
in the Ledger. It does not extract, and it does not reason.

Northena is one of three governors on three orthogonal axes; it must not
absorb the work of the others. SyniSense governs the boundary (whether
data may cross an access point). Solva governs depth (whether reasoning
is sound and an output asserts within its defensibility). Northena
governs direction. It governs both services through their governing
artifacts: the Portfolio Mandate for Service 1 (Day Zero) and the
Objective Request for Service 2 (Day to Day). It governs the run
lifecycle; it does not define the contents of those artifacts.

2\. Deterministic by Construction

Northena is deterministic by construction: it contains no
machine-learning model, no learned weights, and no adaptive behaviour.
This is the property that makes it trustworthy as a governor, not a
limitation.

Its behaviour varies from run to run — different objectives admitted,
different scopes gated, different stops — but every part of that
variation is driven by the frozen governing artifact it reads, not by
Northena adapting. Its scope check is membership against the scope the
artifact declares; its stop is a threshold check against the
done-condition and budget the artifact fixes. It is dynamic the way a
thermostat is dynamic: behaviour changes completely as the setpoint
changes, while the mechanism neither learns nor infers.

**Why it must not learn.** The moment Northena learns — adjusts gating
from past runs, infers scope probabilistically — it stops being
auditable, and auditability is its entire reason to exist. Every run
must be answerable deterministically: admitted because these fields were
valid, gated in because scope-membership held, stopped because this
condition was met. “Admitted because the model scored it 0.72” is the
un-auditable outcome the system exists to avoid.

3\. The Four Stages

Northena operates in four stages, each a deterministic function
specified as code in Part II. In Service 2 they run as a loop (§6).

|           |                                                                               |                                                     |
|-----------|-------------------------------------------------------------------------------|-----------------------------------------------------|
| **Stage** | **Does**                                                                      | **Decision is**                                     |
| Admit     | Compiles a raw intent into a frozen governing artifact and freezes it         | Validity check (presence, completeness, membership) |
| Gate      | Checks whether a (sub-)objective is in the frozen artifact’s scope; routes it | Strict set-membership                               |
| Converge  | Decides whether the run is done                                               | Threshold check (done-condition or budget)          |
| Ledger    | Writes the durable, audit-grade record of the run                             | None — it records, deterministically                |

4\. The Determinism Boundary

Northena performs mechanical checks and never reasons. Where a decision
needs judgment, that decision is Solva’s: Northena invokes Solva and
acts deterministically on the value it returns, but Northena itself
never reasons and never reads how a judgment was made.

|                                                |                                                 |
|------------------------------------------------|-------------------------------------------------|
| **Northena does (deterministic)**              | **Northena does NOT do (Solva’s)**              |
| Presence / completeness checks on the artifact | Judge whether reasoning is sound                |
| Set-membership scope tests at Gate             | Disambiguate scope by inference                 |
| Threshold comparison at Converge               | Judge defensibility, or set a floor by judgment |
| State transitions across the four stages       | Judge preservation depth                        |
| Write the Ledger                               | Reason to a conclusion or certify an output     |

5\. The Ledger

The Ledger is Northena’s memory and the system’s primary audit surface
for direction. It records every decision Northena makes and the material
events of a run: admission, each Gate routing and its reason, every
refusal or drop, the convergence decision, and the absorbed
defensibility stamp-audit entries. Because it is read by the Data
Protection Officer and the operator audit lens, its row shape is a
contract, not an internal log: frozen, versioned, append-only, and
closed on every run. A run with no closed Ledger row is an incomplete,
non-auditable run and is invalid.

6\. The Two Modes

Northena governs Service 1 through the Portfolio Mandate and Service 2
through the Objective Request. In Service 2 the four stages run as a
loop around Layer D and Solva: Admit freezes the request; Gate routes
the objective or a sub-objective warm, fresh, or refused; Layer D and
Solva execute and return any unmet gaps; in-scope gaps are re-tasked and
out-of-scope gaps logged and dropped; Converge stops on the
done-condition or budget. Each answered objective densifies the warm
tier. The direction throughout — what to route, what to re-task, when to
stop — is Northena’s.

**Part II — Engineering Specification**

7\. Module Structure and Dependency Rules

Northena is a set of modules whose dependency direction encodes the
determinism boundary. No module imports a model or a learned component;
the orchestration reaches Solva only through an opaque handle.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>services/northena/ — module layout</strong></p>
<p>services/northena/</p>
<p>admit.py # compile + deterministic validity + atomic freeze</p>
<p>gate.py # strict set-membership routing</p>
<p>converge.py # threshold stop; owns the halt</p>
<p>ledger.py # append-only writer; absorbs stamp-audit</p>
<p>state_machine.py # the four-stage orchestration</p>
<p>interfaces.py # opaque handles (SolvaHandle, RegistryHandle)</p>
<p>contracts/</p>
<p>northena_ledger.py # frozen: LedgerRow (schema + snapshot +
invariant)</p>
<p>routers/</p>
<p>northena.py # read-side + run-status API</p></td>
</tr>
</tbody>
</table>

Dependency rules (enforced by import assertion)

-   **No module imports an ML library or a learned component.**
    Determinism is checked structurally, not by review.

-   **state_machine.py reaches Solva only through SolvaHandle.** It
    never reads Solva’s internals and never performs inference.

-   **ledger.py exposes append only.** No update or delete path exists
    on the writer.

8\. Data Contracts

The governing artifact Northena freezes is the Objective Request
(Service 2) or the Portfolio Mandate (Service 1); Northena consumes
their shapes and does not define them. The one contract Northena owns is
the Ledger row.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>the frozen artifact Northena freezes (consumed, not
owned)</strong></p>
<p>@dataclass(frozen=True)</p>
<p>class FrozenArtifact:</p>
<p>artifact_type: Literal['portfolio_mandate', 'objective_request']</p>
<p>artifact_id: str</p>
<p>version: str</p>
<p>scope: Scope # the set Gate tests membership against</p>
<p>defensibility_floor: FloorSpec</p>
<p>done_condition: DoneSpec</p>
<p>budget: BudgetSpec</p>
<p>lawful_basis: str</p>
<p># CONFIRM: field shapes against objective_request@v0 and the</p>
<p># Portfolio Mandate contract. Immutable once frozen.</p></td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>contracts/northena_ledger.py — the frozen row
(northena_ledger_row@v0)</strong></p>
<p>@dataclass(frozen=True)</p>
<p>class LedgerRow:</p>
<p>run_id: str # one run has one closed Ledger</p>
<p>trace_id: str # joins to units + the three trace lenses</p>
<p>stage: Literal['admit', 'gate', 'converge']</p>
<p>decision: str # admitted|refused|warm|fresh|</p>
<p># terminate_success|terminate_budget|continue</p>
<p>reason: str # deterministic reason string</p>
<p>artifact_ref: ArtifactRef # {type, id, version}</p>
<p>lawful_basis_ref: str</p>
<p>stamp_audit: Optional[Dict] # absorbed side-channel; else None</p>
<p>at: str # ISO 8601</p></td>
</tr>
</tbody>
</table>

**`stamp_audit: Optional[Dict]` — permissive by design.** The untyped `Dict` shape is intentional, not a lapse: it is the load-bearing reason engine artifacts from later phases (G3 Solva boundary emissions, G4 Mtafiti/Targeta stamps, G5a trace correlation, G6 outer-gate receipts, A2 refusal envelopes) can be absorbed into a Ledger row without mutating the frozen `northena_ledger_row@v0` contract. Every engine that emits a stamp landed downstream via this side-channel, allowing 14 frozen contracts to remain byte-identical across G3–G6 while the ledger's semantic reach grew. Any future proposal to type `stamp_audit` (e.g. `Optional[StampAudit]`) would harden it into a mutation surface and lose this property; the permissive contract is a deliberate design decision guarded by `test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit.py::test_northena_ledger_row_contract_snapshot_unchanged_at_g6`.

9\. Admit — Compile, Validate, Freeze

Admit compiles a raw intent into the governing artifact, validates it
deterministically, and freezes it atomically. Where compilation needs
judgment (resolving an ambiguous scope, setting a preservation depth or
a floor), Admit invokes Solva and freezes the returned value; the
judgment is Solva’s, the freeze is Northena’s. Once frozen, the artifact
is immutable for the run — a changed intent is a new admission.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>admit.py — validity is deterministic; the freeze is
atomic</strong></p>
<p>def admit(raw_intent, service, solva: SolvaHandle) -&gt;
FrozenArtifact:</p>
<p>draft = compile_artifact(raw_intent, service, solva) # Solva may
assist</p>
<p>if not draft.lawful_basis:</p>
<p>return refuse(draft, 'missing_lawful_basis')</p>
<p>if not is_complete(draft):</p>
<p>return refuse(draft, 'incomplete_artifact')</p>
<p>if not scope_resolves(draft, registry):</p>
<p>return refuse(draft, 'scope_unresolved')</p>
<p>if not floor_well_formed(draft.defensibility_floor):</p>
<p>return refuse(draft, 'floor_malformed')</p>
<p>frozen = freeze(draft) # immutable for the run</p>
<p>ledger.write(stage='admit', decision='admitted',</p>
<p>artifact_ref=frozen.ref, lawful_basis_ref=frozen.lawful_basis)</p>
<p>return frozen</p></td>
</tr>
</tbody>
</table>

10\. Gate — Strict Set-Membership

Gate tests whether a (sub-)objective falls within the scope the frozen
artifact declares and routes on the result. Scope is a defined set; Gate
checks membership. Ambiguous membership is a compilation defect Admit
should have resolved — Gate does not decide it by inference.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>gate.py — membership, not judgment</strong></p>
<p>def gate(sub_objective, frozen) -&gt; Routing:</p>
<p>if not in_scope(sub_objective, frozen.scope): # set-membership
only</p>
<p>ledger.write(stage='gate', decision='refused',
reason='out_of_scope')</p>
<p>return Routing.REFUSE # governed refusal, logged</p>
<p>if is_converged(sub_objective):</p>
<p>ledger.write(stage='gate', decision='warm',
reason='in_scope_converged')</p>
<p>return Routing.WARM_SERVE</p>
<p>ledger.write(stage='gate', decision='fresh',
reason='in_scope_unconverged')</p>
<p>return Routing.FRESH_EXTRACT</p></td>
</tr>
</tbody>
</table>

11\. Converge — Northena Owns the Halt

Converge decides termination on two conditions fixed in the frozen
artifact — both threshold checks, no learned stopping. The authority to
stop is Northena’s alone. Solva may report it cannot reason further
soundly; that report is an input Converge acts on, but the stop decision
and its record are Northena’s.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>converge.py — threshold stop against the frozen
artifact</strong></p>
<p>def converge(run_state, frozen) -&gt; Convergence:</p>
<p>if done_condition_met(run_state, frozen.done_condition):</p>
<p>ledger.write('converge', 'terminate_success',
'done_condition_met')</p>
<p>return Convergence.TERMINATE_SUCCESS</p>
<p>if budget_exhausted(run_state, frozen.budget):</p>
<p>ledger.write('converge', 'terminate_budget', 'budget_exhausted')</p>
<p>return Convergence.TERMINATE_BUDGET</p>
<p>return Convergence.CONTINUE</p></td>
</tr>
</tbody>
</table>

12\. Ledger — the Contract-Grade Record

The Ledger is written append-only, one closed row set per run. Its row
is frozen (northena_ledger_row@v0) — stable and audit-legible from the
outset. It absorbs the defensibility stamp-audit entries by unit_id and
trace_id, keeping the unit (output) and the audit (trace) in separate
envelopes with separate lifecycles.

**No run without a closed Ledger.** A run is not complete until its
Ledger is closed. The writer exposes only append — no update or delete
within the retention window. Out-of-scope and refused items are
recorded, never silently dropped.

13\. The Determinism Boundary — as Code

Solva is reached only through an opaque handle, so the orchestration
cannot read Solva’s internals or reason itself. Northena calls out for a
judgment and acts deterministically on the returned value.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr class="odd">
<td><p><strong>interfaces.py + state_machine.py — Solva is opaque to
Northena</strong></p>
<p>class SolvaHandle(Protocol): # opaque — Northena sees no
internals</p>
<p>def resolve_scope(self, draft) -&gt; Scope: ...</p>
<p>def set_preservation(self, draft) -&gt; PreservationVector: ...</p>
<p>def run(intent, service, solva: SolvaHandle):</p>
<p>frozen = admit(intent, service, solva)</p>
<p>if frozen.refused: return frozen</p>
<p>while True:</p>
<p>routing = gate(next_sub_objective(frozen), frozen)</p>
<p>execute(routing) # Layer D / warm-serve / refuse</p>
<p>c = converge(run_state, frozen)</p>
<p>if c is not Convergence.CONTINUE:</p>
<p>ledger.close(run_id) # no run closes without this</p>
<p>return c</p></td>
</tr>
</tbody>
</table>

14\. Interfaces and Test Obligations

Interfaces

|                      |               |                                                                                                                                            |
|----------------------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| **Interface**        | **Direction** | **Shape / status**                                                                                                                         |
| Intent → Admit       | in            | Raw intent (internal job or consumer terminal request).                                                                                    |
| Admit ↔ Solva        | out/in        | Via SolvaHandle: request scope/preservation/floor resolution; receive values; freeze. CONFIRM SolvaHandle against the Solva specification. |
| Gate → execution     | out           | warm-serve (Intelligence tier) \| fresh (Layer D) \| refuse.                                                                               |
| Converge → loop      | out           | terminate-success \| terminate-budget \| continue.                                                                                         |
| Northena → Ledger    | out           | Append-only LedgerRow (northena_ledger_row@v0).                                                                                            |
| Stamp-audit → Ledger | in            | Absorbs StampAudit by unit_id / trace_id. CONFIRM against the stamp-audit side-channel.                                                    |
| Northena ↔ SyniSense | —             | Northena checks lawful_basis presence; SyniSense enforces the crossing. Orthogonal.                                                        |

Test obligations

|                                   |                                                                                             |
|-----------------------------------|---------------------------------------------------------------------------------------------|
| **Test**                          | **Asserts**                                                                                 |
| test_no_run_without_lawful_basis  | An intent with no lawful_basis is refused at Admit; no downstream stage runs.               |
| test_frozen_artifact_immutable    | A frozen artifact cannot be mutated for the run; a changed intent produces a new admission. |
| test_gate_is_set_membership       | Gate routes purely on scope membership; no inferential path exists.                         |
| test_converge_owns_halt           | Termination occurs only on done-condition or budget from the frozen artifact.               |
| test_no_run_without_closed_ledger | A run cannot close without a closed Ledger row set.                                         |
| test_ledger_append_only           | The ledger writer exposes no update or delete within the retention window.                  |
| test_ledger_row_frozen            | LedgerRow conforms to northena_ledger_row@v0 (snapshot assertion).                          |
| test_northena_has_no_ml_import    | No Northena module imports an ML library (import assertion).                                |
| test_solva_is_opaque              | state_machine reaches Solva only through SolvaHandle; no internal access.                   |

15\. Construction Requirements

Requirements on any correct implementation, in the order construction
must respect them.

1.  **The Ledger row is contract-grade from the outset.** Freeze
    northena_ledger_row@v0 (schema, snapshot, invariant) before the
    stages write to it. It is the audit surface, not an internal log.

2.  **The four stages are a single state machine.** Admit, Gate,
    Converge, and the Ledger writer are orchestrated as one loop; each
    stage writes its row; the run closes only on a closed Ledger.

3.  **Determinism is structural.** No ML import in any module; Solva
    reached only through the opaque handle; the import assertion is part
    of continuous integration.

4.  **The governors are integrated, not re-implemented.** Solva and
    SyniSense are reached through their interfaces; neither is rebuilt
    inside Northena.

**Part III — Governance, Invariants, Open Decisions**

16\. Governance and Compliance

-   **Lawful basis is enforced at Admit.** No run is admitted without a
    valid lawful_basis; purpose limitation is enforced at admission,
    before any extraction.

-   **The Ledger is the accountability record.** It evidences, for any
    run, that a lawful basis was present and that direction was
    governed.

-   **Refusals are recorded, not hidden.** Out-of-scope and refused
    items are logged, so the system can show what it declined and why.

17\. Invariants

Binding. Any implementation that violates one is incorrect regardless of
behaviour.

1.  Northena is deterministic: no model, no learned weights, no adaptive
    behaviour. Its dynamism is entirely a function of the frozen
    governing artifact.

2.  Any decision requiring inference is Solva’s. Northena invokes Solva
    through an opaque handle and acts deterministically on the result;
    it never reasons and never reads Solva’s internals.

3.  Every run is governed by exactly one frozen governing artifact,
    admitted by Northena, carrying a valid lawful_basis. No run proceeds
    without one.

4.  The frozen governing artifact is immutable for the run. A changed
    intent is a new admission, never an edit of a live artifact.

5.  Gate is strict set-membership. Ambiguous membership is a compilation
    defect resolved at Admit, never decided by inference at Gate.

6.  Northena owns the halt. Converge terminates only on the
    done-condition or budget in the frozen artifact. No run closes
    without a closed, audit-grade Ledger.

7.  The Ledger is contract-grade — versioned, snapshot-and-invariant,
    append-only, immutable within the retention window — audit-legible
    from the first record.

8.  Out-of-scope and refused items are recorded in the Ledger, never
    silently dropped.

9.  The Ledger absorbs the defensibility stamp-audit by unit_id /
    trace_id; unit and audit remain in separate envelopes with separate
    lifecycles.

10. Northena governs direction only. Boundary is SyniSense; depth is
    Solva. The three axes are never collapsed.

18\. Open Decisions

|                                                                          |           |                                                                                                                                                                                                                       |
|--------------------------------------------------------------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Decision**                                                             | **Owner** | **Status**                                                                                                                                                                                                            |
| Ledger retention duration and end-of-window deletion / immutability rule | DPO       | Not a build blocker — the default is append-only immutability with configurable, indefinite retention until confirmed. Must be closed before any production data-subject-rights or retention obligation is exercised. |

**Status.** This specification is complete. Every structural rule — the
four stages, the determinism boundary as an opaque handle, the
append-only contract-grade ledger, no-run-without-a-closed-ledger — is
settled. Only ledger retention awaits DPO confirmation, and it is not a
construction blocker. Points marked CONFIRM are resolved against the
real contract; a shape that cannot be confirmed is recorded, not
inferred.

---

## Closed Seam — Unlock: Ledger Retention Window

The Northena Ledger currently defaults to INDEFINITE retention. `services/northena/ledger.py:38-48` documents `retention_policy` as INDEFINITE. **No deletion code path exists** in `services/northena/` and this is guarded by `tests/invariants/test_northena_ledger_retention.py::test_no_deletion_path_in_northena_services`, which grep-guards forbidden tokens `("delete_", "purge_", "expire_")` across the northena services directory and asserts none exist.

- **Owner:** Data Protection Officer (DPO-signed decision required).
- **Config keys:** DPO defines exact shape. Likely surface:
  - Retention window: bounded duration (days or ISO-8601) OR a bounded-interval schedule.
  - Deletion mechanism choice: application-level sweep, scheduled job, or MongoDB TTL index on a datetime field of `northena_ledger_rows`.
  - Deletion audit posture: DPO decides whether deletion events are themselves ledger-recorded. **Recommended: yes, via `stamp_audit` side-channel;** preserves the G6 doctrine and the append-only guarantee (deletion is recorded as an entry, not a mutation).
- **Unlock procedure:**
  1. DPO decides retention window + deletion mechanism.
  2. **`test_no_deletion_path_in_northena_services` WILL fail on unlock — that is the correct deployment ceremony.** Re-bless alongside the deletion implementation. Options: delete the invariant, or re-scope to `test_no_unauthorized_deletion_path` — assert only paths matching an `authorized_deletion_` prefix exist.
  3. Implement deletion (application-level function OR Mongo TTL index migration).
  4. Add authenticated audit trail for every deletion event.
- **Behavioral delta when opened:** `LedgerRow` history becomes bounded rather than indefinite. Rows outside the retention window are deleted/expired according to policy. Deletion events (per recommended posture) land as `stamp_audit`-decorated ledger rows.
- **Test that proves it opened:** current no-deletion-path test will fail (expected). Add: `test_deletion_respects_retention_window`, `test_deletion_preserves_within_window_rows`, `test_deletion_is_ledger_recorded`. Consolidated in `/app/docs/handoff/seam_unlock_runbook.md` (Seam 3).
