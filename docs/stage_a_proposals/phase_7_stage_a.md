# Phase 7 Stage A — Shaping Wizard §3.3 (DESIGN-ONLY)

**Phase:** 7 Stage A (Design-only, no code writes)
**Date:** 2026-07-04
**Delivery format:** Standing Rule v3 (Owner ruling, Phase 6 Stage B close, 2026-07-04): on-disk canonical + SHA in return; return summary carries one-line disposition enumerations only.
**Doctrine anchors:** RMS v3 §3.3 (shaping wizard) + §5 (feasibility) + §6 (provenance-preservation bound) + §6.1 (qualified-data) + §6.2 (composed-conclusion) + §8 (economics) + UI Spec §2.2 / §2.3 / §5.1 + UX v2 §4.3.
**Owner pre-rulings binding this proposal:** Ruling 4 (shared-derivation) + Ruling 3 (config-as-versioned-not-frozen) + Ask-vs-propose enforcement mechanics (field-level source-tagging) + license-class Phase 7 seam (fallback-arm wrap) + frozen-field-changes-as-new-versions + loose-as-frozen + provenance-preservation bound (§6).
**Status:** DESIGN PROPOSAL. Parity stays 22. Zero code writes. No new frozen contracts landing at Stage A.

---

## Return 1 — Two-variant state machine (Operator + Buyer)

### 1.1 Operator variant state machine

**Field tiers (v3 §3.3 verbatim):**
- **operator-mandatory (Guard 1):** reach, output's four fields (form, consumer, grain, standard), done_condition, budget, lawful_basis. Agent ASKS never PROPOSES.
- **preference (Guard 2):** weighting, ordering, formatting, sampling within budget. Agent MAY RECOMMEND — every recommendation lands as `agent_assumed`.
- **Guard 3:** every turn feasibility-grounded in the estate (§5 shared-derivation).

**States + transitions:**
```
                    ┌─────────────────────────────────────┐
                    │            initial                  │
                    │  new WizardCommitState_v0 minted    │
                    │  session_id + trace_id allocated    │
                    └────────────────┬────────────────────┘
                                     │ POST /api/wizard/operator/session
                                     ▼
                    ┌─────────────────────────────────────┐
                    │      turn(N) — asking loop          │
                    │  Guard 3: feasibility.compute       │
                    │  Guard 1: agent asks mandatory      │
                    │  Guard 2: agent may recommend pref  │
                    └────────────┬────────────────────────┘
                                 │ POST /api/wizard/{session_id}/turn
                                 │  (loop while unclosed mandatory fields)
                                 │
                                 │  (all mandatory fields have a supplied
                                 │   value from operator OR agent)
                                 ▼
                    ┌─────────────────────────────────────┐
                    │        commit-review                │
                    │  Paint "You supplied" vs            │
                    │  "Agent assumed — confirm/change"   │
                    │  Every mandatory field displayed    │
                    │  with source tag                    │
                    └──┬──────────────────────────────┬───┘
                       │ user changes                 │ user confirms all
                       │ any agent_assumed            │ (Guard 1 hard-check:
                       ▼                              │  every mandatory field
                (loop back to turn or                 │  is now operator_supplied)
                 in-place edit at commit-             │
                 review with re-tag)                  ▼
                                              ┌───────────────────────┐
                                              │       freeze          │
                                              │  WizardCommitState_v0 │
                                              │  persisted; mint      │
                                              │  ObjectiveRequest_v2  │
                                              │  handoff to admission │
                                              └───────────┬───────────┘
                                                          │ POST /api/wizard/{session_id}/freeze
                                                          ▼
                                              ┌───────────────────────┐
                                              │  admission handoff    │
                                              │  reuse Phase 5 async  │
                                              │  admission surface —  │
                                              │  POST /api/objectives │
                                              └───────────────────────┘

    Any turn OR commit-review can transition to:
                    ┌─────────────────────────────────────┐
                    │       refuse-with-path              │
                    │  Uses existing AdmissionRefusal_v0  │
                    │  reason code + path forward.        │
                    │  Registry-bump adds new reasons     │
                    │  (Ruling 2 pattern).                │
                    └─────────────────────────────────────┘
```

**Turn cycle pseudocode (operator):**
```python
async def operator_turn_cycle(session: WizardCommitState_v0, user_content: str):
    # Guard 3: feasibility-ground first — WHOLE turn is feasibility-conditioned
    feasibility_snap = compute_feasibility(session.working_reach, session.working_standard)
    session.feasibility_history.append(feasibility_snap)  # append-only
    if not feasibility_snap.floor_feasible:
        # Refuse-with-path per §5. Reason: not_feasible_at_declared_floor.
        return emit_refuse_with_path(session, reason="not_feasible_at_declared_floor")

    # Guard 1: identify next mandatory field the operator has not supplied
    next_mandatory = pick_unsupplied_mandatory(session)
    if next_mandatory is not None:
        # ASK, don't propose. LLM produces an ask-shaped turn.
        agent_content = ask_llm.render_ask(next_mandatory, feasibility_snap, session.turns)
        turn = OperatorTurn_v0(
            turn_ref=new_uuid(), at=iso_now(),
            user_content=user_content, agent_content=agent_content,
            feasibility_snapshot_ref=feasibility_snap.snapshot_ref,
        )
        session.turns.append(turn)
        # Operator's next POST /turn will carry the user's response.
        return turn

    # All mandatory fields have a value. Move to Guard 2: agent may recommend
    # any preference-tier fields still empty.
    next_preference = pick_recommendable_preference(session)
    if next_preference is not None:
        agent_content = recommend_llm.render_recommendation(...)
        # This recommendation lands as agent_assumed on commit if user confirms.
        turn = OperatorTurn_v0(...)
        session.turns.append(turn)
        # If user accepts recommendation, an AgentAssumption_v0 lands per field.
        return turn

    # All mandatory + preference exhausted → gate to commit-review.
    return transition_to_commit_review(session)
```

**Refusal-with-path flow (both variants):**
```
                    turn discovers:
                        - not_feasible_at_declared_floor
                        - offerability_bound_exceeded (buyer variant only)
                        - form_not_offerable (already firing at admission)
                        - provenance_preservation_impossible (§6 bound)
                             │
                             ▼
                    ┌─────────────────────────────────────┐
                    │  emit_admission_refusal_v0(         │
                    │    reason=<code>,                   │
                    │    trace_id=session.trace_id,       │
                    │    requested_output_form=...,       │
                    │    off_menu_fact=...,               │
                    │    what_you_can_do=...              │
                    │  )                                  │
                    │  Render at wizard surface via       │
                    │  Phase 8 refusal-with-path pattern  │
                    │  (never as error; UI Spec §3.3)     │
                    └─────────────────────────────────────┘
```

### 1.2 Buyer variant state machine

**Same shaping mechanism, DIFFERENT ceiling** per v3 §3.3:
- Agent shapes within **offerability** (owned estate + license class + disclosure limits).
- Shapes OUTSIDE offerability → REFUSED via `AdmissionRefusal_v0` (registry bump for new reasons per Ruling 2 pattern).
- Agent MAY PROPOSE (steering cheaper feasible shapes = sales, not laundering).
- Price + delivery-time compute live via Phase 6 seam (`quote_service.issue_quote(...)` per turn).
- Buyer NEVER sets `lawful_basis`; `use_purpose` drives `license_class` (per WizardCommitState_v0 primary arm — Return 4).

**States + transitions (buyer):**
```
                    ┌─────────────────────────────────────┐
                    │            initial                  │
                    │  variant="buyer"                    │
                    │  no lawful_basis field surfaced     │
                    │  use_purpose surfaced instead       │
                    └────────────────┬────────────────────┘
                                     │ POST /api/wizard/buyer/session
                                     ▼
                    ┌─────────────────────────────────────┐
                    │      turn(N) — shape-move loop      │
                    │  Guard 3: feasibility.compute       │
                    │  offerability-check per turn        │
                    │  quote_service.issue_quote per turn │
                    │  (live price + delivery estimate)   │
                    │  agent MAY PROPOSE cheaper shapes   │
                    └────────────┬────────────────────────┘
                                 │ POST /api/wizard/{session_id}/turn
                                 │  (loop until buyer commits shape)
                                 │
                                 ▼
                    ┌─────────────────────────────────────┐
                    │        commit-review                │
                    │  Same source-tag paint as operator, │
                    │  PLUS: current quote (figure +      │
                    │  qualifying_volume + delivery       │
                    │  estimate) painted per Phase 6      │
                    │  quote_envelope.model_dump          │
                    └──┬──────────────────────────────┬───┘
                       │ buyer refines shape          │ buyer accepts
                       │ (may re-quote)               │
                       ▼                              ▼
                (loop back to turn)          ┌───────────────────────┐
                                             │       freeze          │
                                             │  WizardCommitState_v0 │
                                             │  → ObjectiveRequest   │
                                             │  → POST /api/objectives│
                                             │  Buyer accepts quote  │
                                             │  (quote_id sealed).   │
                                             └───────────────────────┘
```

**Offerability-check per turn (buyer):**
```python
async def buyer_offerability_check(session: WizardCommitState_v0, working_shape: dict) -> Optional[AdmissionRefusal_v0]:
    """Buyer variant offerability bounds — three sub-checks."""
    # (a) Owned-estate: reach must lie inside the operator's owned scope refs.
    if not scope_refs_within_owned_estate(working_shape["reach"]["scope_refs"]):
        return emit_admission_refusal(
            reason="reach_outside_owned_estate",
            what_you_can_do="Narrow scope_refs to the operator's owned estate.",
        )
    # (b) License-class: use_purpose must map to a valid license class.
    lc = derive_license_class(working_shape)  # primary arm reads use_purpose
    if not is_valid_class(lc):
        return emit_admission_refusal(reason="license_class_unavailable")
    # (c) Disclosure-limits: cumulative-disclosure ledger check (G6 seam).
    if would_breach_cumulative_disclosure(working_shape, lc):
        return emit_admission_refusal(reason="cumulative_disclosure_breach")
    # (d) Provenance-preservation bound (v3 §6): form/grain rule must
    # satisfy declared standard. Refuse DURING SHAPING with path.
    if not provenance_preservation_satisfies_standard(working_shape):
        return emit_admission_refusal(reason="provenance_preservation_impossible")
    return None
```

### 1.3 Variant discriminator flow

`WizardCommitState_v0.variant: Literal["operator", "buyer"]` carries the discriminator end-to-end. Router mounts two prefixes (`/api/wizard/operator/*` + `/api/wizard/buyer/*`) but same state-machine engine reads `variant` to branch guards. Discriminator baked in at `initiate` and immutable for session life (guard against variant-switch mid-session).

**Named LOAD-BEARING gate:** `test_wizard_variant_discriminator_immutable_within_session` (variant set at initiate; commit refuses if any turn changes variant).

---

## Return 2 — Ask-vs-propose enforcement — field-level source-tagging mechanics

### 2.1 Source-tag structure per committed field

```python
class CommittedValue_v0(BaseModel):
    """v3 §3.3 Guard 1/2 discipline — every committed value carries a source tag.

    Invariant (structural, enforced by model_validator):
      exactly one of `operator_turn_ref` / `agent_assumption_id` is set;
      the other is None. Never both, never neither.
    """
    model_config = ConfigDict(extra="forbid")
    value: Any                                        # the actual committed value
    source: Literal["operator_supplied", "agent_assumed"]
    operator_turn_ref: Optional[str] = None           # references OperatorTurn_v0.turn_ref
    agent_assumption_id: Optional[str] = None         # references AgentAssumption_v0.assumption_id
    committed_at: str = Field(..., min_length=1)      # ISO-8601 UTC

    @model_validator(mode="after")
    def _validate_source_tag_invariant(self):
        n_refs = sum([self.operator_turn_ref is not None, self.agent_assumption_id is not None])
        if n_refs != 1:
            raise ValueError(
                "CommittedValue_v0 invariant: exactly one of operator_turn_ref or "
                f"agent_assumption_id must be set; got {n_refs}."
            )
        if self.source == "operator_supplied" and self.operator_turn_ref is None:
            raise ValueError("operator_supplied source requires operator_turn_ref.")
        if self.source == "agent_assumed" and self.agent_assumption_id is None:
            raise ValueError("agent_assumed source requires agent_assumption_id.")
        return self
```

### 2.2 Commit-time validator

`WizardCommitState_v0.committed_values: Dict[str, CommittedValue_v0]`. On freeze:

```python
@model_validator(mode="after")
def _validate_freeze_time_invariants(self):
    if self.committed_at is None:
        return self  # not yet frozen; invariants only fire at freeze
    # Guard 1 HARD-MECHANICAL: every operator-mandatory field must be operator_supplied.
    OPERATOR_MANDATORY = {"reach", "output.form", "output.consumer", "output.grain",
                          "output.standard", "envelope.done_condition",
                          "envelope.budget", "envelope.lawful_basis"}  # operator variant only
    if self.variant == "operator":
        for field in OPERATOR_MANDATORY:
            cv = self.committed_values.get(field)
            if cv is None:
                raise ValueError(f"Guard 1: mandatory field {field!r} missing at freeze.")
            if cv.source != "operator_supplied":
                raise ValueError(
                    f"Guard 1: mandatory field {field!r} committed with source "
                    f"{cv.source!r}; must be operator_supplied."
                )
    # Guard 2: every agent_assumed value must reference a valid agent_assumption_id.
    known_assumption_ids = {a.assumption_id for a in self.agent_assumptions}
    for name, cv in self.committed_values.items():
        if cv.source == "agent_assumed":
            if cv.agent_assumption_id not in known_assumption_ids:
                raise ValueError(
                    f"Guard 2: field {name!r} references unknown agent_assumption_id."
                )
    return self
```

### 2.3 Turn ledger

- Every operator turn → `OperatorTurn_v0(turn_ref=uuid, at, user_content, agent_content, feasibility_snapshot_ref)` appended to `WizardCommitState_v0.turns[]` (append-only).
- Every agent inference → `AgentAssumption_v0(assumption_id=uuid, at, field, inferred_value, evidence_ref)` appended to `WizardCommitState_v0.agent_assumptions[]` (append-only).
- Neither list can shrink; commit-review overrides land as new CommittedValue rebinds, not turn/assumption deletions.

### 2.4 Commit-review UI seam

Frontend (Phase 8) reads `committed_values[field].source` per field, renders per UI Spec §2.3:
- `operator_supplied` → "You supplied" indicator + value display + edit button.
- `agent_assumed` → "Agent assumed — confirm or change" prompt + inferred value + confirm-button + change-button. Confirming re-tags to `operator_supplied` with a NEW `operator_turn_ref` at commit-review. Changing loops back to turn cycle.

Backend surface serialises `WizardCommitState_v0` byte-identically via `model_dump(mode="json")`.

### 2.5 Named LOAD-BEARING gates (Return 2)

1. **`test_committed_value_v0_source_tag_invariant`** (LB): exactly-one-of-two enforcement fires; both-null and both-set both raise.
2. **`test_wizard_commit_state_v0_freeze_refuses_agent_assumed_on_operator_mandatory_field`** (LB): Guard 1 hard-mechanical check.
3. **`test_wizard_commit_state_v0_freeze_refuses_orphaned_agent_assumption_ref`** (LB): Guard 2 orphan-reference check.
4. **`test_no_second_llm_judge_in_wizard_pipeline`** (grep-negative regression on Owner pre-ruling): grep `services/wizard/*` for any second LLM-provider call between commit-review and freeze; assert 0 matches.
5. **`test_ask_vs_propose_committed_mandatory_fields_all_operator_supplied`** (LB): parametrised across every operator-mandatory field — commit refuses on `agent_assumed` for any of the 8 mandatory fields.

---

## Return 3 — `WizardCommitState_v0` shape + D4b argument

### 3.1 Full field roster

```python
class WizardCommitState_v0(BaseModel):
    """v3 §3.3 shaping-wizard commit state.

    Persistence: `wizard_sessions` Mongo collection, keyed on session_id.
    Correlation: `trace_id` shared with downstream admission surface —
    Northena Ledger reads see the WHOLE wizard→admission→terminal arc
    under one trace_id, matching the Phase 5 async_state pattern.

    Governance discipline (Owner pre-ruling, PM review 2026-07-04):
    every committed field carries a CommittedValue_v0 source tag;
    invariant enforcement is STRUCTURAL (model_validator), not prompt.
    """
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., min_length=1)         # uuid-like
    trace_id: str = Field(..., min_length=1)           # Northena/Solva correlator; same used by downstream admission
    variant: Literal["operator", "buyer"]              # discriminator; immutable within session
    initiated_at: str = Field(..., min_length=1)       # ISO-8601 UTC
    committed_at: Optional[str] = None                 # populated at freeze
    turns: List[OperatorTurn_v0] = Field(default_factory=list)                # append-only
    agent_assumptions: List[AgentAssumption_v0] = Field(default_factory=list) # append-only
    committed_values: Dict[str, CommittedValue_v0] = Field(default_factory=dict)  # keyed by dotted field path
    feasibility_history: List[FeasibilityResultRef] = Field(default_factory=list) # per-turn snapshot refs
    license_class: Optional[str] = None                # populated at commit-review; primary-arm value for Return 4 wrap
    frozen_objective_ref: Optional[str] = None         # populated at freeze; refs the minted ObjectiveRequest_v2

    # Buyer-variant only:
    use_purpose: Optional[str] = None                  # buyer never sets lawful_basis; use_purpose drives license class
    latest_quote_ref: Optional[str] = None             # references most recent QuoteEnvelope_v0.quote_id from live re-quote
```

### 3.2 Inner frozen-shape candidates

```python
class OperatorTurn_v0(BaseModel):
    """Append-only turn record. One per POST /api/wizard/{session_id}/turn."""
    model_config = ConfigDict(extra="forbid")
    turn_ref: str = Field(..., min_length=1)          # uuid
    at: str = Field(..., min_length=1)                # ISO-8601 UTC
    user_content: str = Field(..., min_length=0)      # empty on ask-turns before user replies
    agent_content: str = Field(..., min_length=0)     # empty on turns before agent replies
    feasibility_snapshot_ref: str = Field(..., min_length=1)  # Guard 3 enforcement point

class AgentAssumption_v0(BaseModel):
    """Append-only agent-inference record. One per agent-supplied value."""
    model_config = ConfigDict(extra="forbid")
    assumption_id: str = Field(..., min_length=1)     # uuid
    at: str = Field(..., min_length=1)                # ISO-8601 UTC
    field: str = Field(..., min_length=1)             # dotted path (e.g. "output.grain")
    inferred_value: Any
    evidence_ref: str = Field(default="")             # trace pointer if evidence available; loose-as-frozen empty otherwise

class CommittedValue_v0(BaseModel):
    """Per-field source-tagged committed value. See Return 2.1 for invariant."""
    # (definition in Return 2.1)
```

### 3.3 D4b argument — does `WizardCommitState_v0` FREEZE?

**Case FOR freezing:**
1. **External state.** Persists across HTTP requests during the multi-turn wizard (a session may span minutes to hours). External to the process.
2. **External integrator dependency.** Backend serves `WizardCommitState_v0` to the Phase 8 frontend at commit-review; the frontend's rendering logic is bound to the shape. Any drift would silently break commit-review.
3. **Governance-carrying.** The source-tag structure (`CommittedValue_v0.source`) is enforced at the commit boundary — every downstream admission reads it. A drift on `source` semantics would silently unwind Guard 1/2.
4. **Standing pattern.** All prior boundary contracts froze (ObjectiveRequest_v2, AsyncDeliveryAccepted_v0/v1, QuoteEnvelope_v0). Same discipline applies.

**Case AGAINST freezing:**
1. **Session-scoped.** Unlike AsyncDeliveryAccepted (which is integrator-durable), WizardCommitState_v0 is per-session. Once frozen, the downstream truth is `ObjectiveRequest_v2` — WizardCommitState_v0 exists mainly as audit trail.
2. **UI-consumption surface.** Phase 8 frontend is the primary reader. Backend integrators arguably read `ObjectiveRequest_v2` (post-freeze), not `WizardCommitState_v0`.
3. **Governance sits on INNER shapes.** The real doctrinal freeze is `CommittedValue_v0` (source-tag invariant) — freezing the outer wrapper adds parity load without adding governance guarantees.

**Recommendation:** **FREEZE `WizardCommitState_v0` AND its three inner shapes as SEPARATE frozen contracts.** Rationale:
- Freezing only the inner shapes leaves the outer wrapper's shape (session_id + trace_id + committed_values dict structure + turns/assumptions list ordering) unstamped — a subtle Phase 8 breakage on wrapper-drift becomes hard to detect.
- Freezing all four is the doctrinally-consistent posture with all prior "external state persisted across requests" contracts (northena_ledger_row_v0/v1, async_delivery_accepted_v0/v1, async_state doc-shape which SHOULD have been frozen — Phase 5 Stage B tech debt).
- Parity 22 → **26** at Phase 7 Stage B landing (four new frozen contracts: `WizardCommitState_v0` + `OperatorTurn_v0` + `AgentAssumption_v0` + `CommittedValue_v0`).

**Escalation to Owner:** ratify the FREEZE-all-four recommendation OR narrow to a smaller freeze set (e.g. only `CommittedValue_v0`) at Stage B open.

### 3.4 Inner-shape freeze granularity argument

- **`OperatorTurn_v0` (freeze YES):** frontend renders per-turn history at commit-review (turn scroll surface). Contract governs `user_content` / `agent_content` rendering. Shape drift → Phase 8 breakage.
- **`AgentAssumption_v0` (freeze YES):** frontend renders per-assumption confirm-or-change UI. `field` + `inferred_value` are display bindings. Shape drift → subtle governance breakage (assumption references dangling).
- **`CommittedValue_v0` (freeze YES — LOAD-BEARING):** source-tag invariant is enforced structurally. THE freeze target from a governance perspective. Without it, Guard 1/2 collapse.

Recommendation stands: freeze all four.

---

## Return 4 — License-class fallback-arm wrap per pre-committed docstring

### 4.1 Fallback-arm wrap design

```python
def derive_license_class(objective_or_wizard_state) -> str:
    """
    Owner Ruling 4 (Phase 4a Stage B close, 2026-07-03): Phase 7 seam
    pre-committed. Two arms:
      1. PRIMARY: explicit-value-if-present. If the caller passes a
         WizardCommitState_v0 (or an ObjectiveRequest_v2 whose envelope
         carries the wizard-committed license_class via the sidecar
         landing per Return 4.2), return that value verbatim.
      2. FALLBACK: commissioner-derived. If no explicit license_class,
         delegate to the existing `derive_license_class_from_commissioner`.

    Ruling 4 shared-derivation preserved — ONE site
    (services/service_1/license_class_selection.py). Existing
    `derive_license_class_from_commissioner` UNCHANGED (fallback arm).
    """
    # Arm 1: primary — check for WizardCommitState_v0 provenance.
    if isinstance(objective_or_wizard_state, WizardCommitState_v0):
        if objective_or_wizard_state.license_class is not None:
            return objective_or_wizard_state.license_class
        envelope = None  # wizard state without license_class → fall through to commissioner
    else:
        # ObjectiveRequest_v2 path.
        envelope = objective_or_wizard_state.envelope
        # Arm 1 alternate: envelope carries wizard-committed license_class
        # via sidecar landing (Return 4.2 Option A OR B).
        wizard_lc = _wizard_committed_license_class(objective_or_wizard_state)
        if wizard_lc is not None:
            return wizard_lc

    # Arm 2 — fallback.
    return derive_license_class_from_commissioner(envelope)
```

### 4.2 HAZARD-STOP-CANDIDATE — `ObjectiveRequest_v2.envelope` lacks `license_class` field

**Verified 2026-07-04 (Phase 7 Stage A):** grep of `contracts/objective_request_v2.py` confirms `Envelope` has 8 fields (`lawful_basis`, `done_condition`, `budget`, `scope_ceiling`, `availability_snapshot`, `floor_feasibility`, `commissioner`, `committed_at`) — **NO `license_class` field.**

The pre-committed docstring at `services/service_1/license_class_selection.py:23-32` anticipates this exact HAZARD-STOP: *"the negotiated `license_class` arrives on the objective via a versioned frozen-contract addition (form TBD by Phase 7's dispatch — likely a `WizardCommitState_v0` or similar sidecar)."*

Two options for the sidecar landing:

**Option A — new `ObjectiveRequest_v3` with `envelope.license_class` field.**
- Follows `frozen-field-changes-as-new-versions` ruling verbatim (v2 stays byte-identical; v3 is a new frozen contract).
- Every consumer of ObjectiveRequest reads `envelope.license_class` directly.
- Parity 22 → 27 at Phase 7 Stage B (four wizard freezes + ObjectiveRequest_v3).
- Cost: significant migration surface. All prior services (dispatch, service_1, mtafiti, etc.) that switch from v2 to v3 need review. Phase 5 Stage B and Phase 6 Stage B built against v2; not all callers auto-benefit from a v3 envelope field.

**Option B — `ObjectiveRequest_v2.envelope.frozen_wizard_ref: Optional[str]` via a v3 version file.**
- Same freeze pattern (v3 file, not in-place edit), but the `envelope` carries ONLY a reference to `WizardCommitState_v0.session_id` — the license_class is READ from the wizard state, not duplicated on the envelope.
- Single source of truth: WizardCommitState_v0. Downstream reads follow the ref pointer.
- Parity 22 → 27 (same count) but the derivation function reads via ref; requires a lookup at every derive call.
- Cost: introduces a runtime lookup dependency; less clean than Option A for read paths.

**Option C — no ObjectiveRequest_v3; wizard state is a SEPARATE first-class argument.**
- Callers that need license_class pass `WizardCommitState_v0` alongside `ObjectiveRequest_v2`. Callers without wizard state (legacy pre-Phase-7 external_request path) fall through to commissioner-derived.
- Parity 22 → 26 (only four wizard freezes, no ObjectiveRequest_v3).
- Cost: two-argument derive; every caller must know whether wizard-state exists.

**Recommendation:** **Option C is the cleanest** — no ObjectiveRequest version churn; `derive_license_class` becomes explicit about which sources it reads; the pre-committed docstring's wording (*"WizardCommitState_v0 or similar sidecar"*) is exactly this shape. Phase 4a Stage B closed the identity-proxy hazard by naming the SEAM in this docstring, not by pre-committing which ObjectiveRequest version lands the field.

**Escalation to Owner:** ratify Option A / B / C at Stage B open. If Option A, parity → 27 (four wizard + ObjectiveRequest_v3). If Option B, parity → 27 same shape different semantics. If Option C, parity → 26 (four wizard only).

### 4.3 Named regression gates (Return 4)

- **`test_license_class_docstring_still_documents_phase_7_seam`** (Ruling 4 docstring grep — must survive the wrap): grep `services/service_1/license_class_selection.py` for `"Phase 7 seam pre-committed"` + `"fallback arm"` — both present.
- **`test_license_class_primary_arm_prefers_explicit_over_commissioner_derived`** (LB): construct WizardCommitState_v0 with `license_class="premium"`; assert `derive_license_class(state)` returns `"premium"` even when commissioner would default to `"standard"`.
- **`test_license_class_fallback_arm_unchanged_when_no_explicit_value`** (regression): `derive_license_class` on an ObjectiveRequest_v2 without wizard state returns the same value as `derive_license_class_from_commissioner(envelope)` byte-identical.
- **`test_derive_license_class_from_commissioner_untouched_at_7b`** (byte-identity): SHA of `license_class_selection.py:derive_license_class_from_commissioner` function body slice = SHA captured at Phase 6 Stage B close.

---

## Return 5 — LLM choice + transcript-retention posture (DPO flag)

### 5.1 LLM choice proposal

**Primary model recommendation:** **Claude Sonnet 4.6** via Emergent Universal Key + `emergentintegrations` library.

Rationale:
- **Governance discipline surface.** Sonnet 4.6 has strong instruction-following at moderate temperature; the ask-vs-propose Guard 1 discipline is a governance-instruction-heavy task. Claude Sonnet family is documented as reliable in refusing to fabricate mandatory-field values (matches Owner's ask-don't-propose intent).
- **Multi-turn coherence.** Wizard turns are conversational; Sonnet handles multi-turn context well.
- **Cost vs GPT-5.2 / Opus 4.8.** Sonnet 4.6 is mid-tier — cheaper than Opus for a high-turn-volume surface (a wizard session may run 15-30 turns).
- **Governance seam:** all calls route through the SyniSense Shield chokepoint per the standing invariant (§0 rule 12 equivalent).

**Fallback model:** **hard-refuse-user (no silent-degrade).** Per infra-not-refusal doctrine, LLM provider 429/5xx → HTTP 503 to the wizard client with a retry hint. Do NOT silently degrade to a lower-quality model (fabricated turn content is a governance failure worse than a rate-limited failure). Owner ratification required.

**Temperature discipline:**
- **Turn generation temperature:** `0.2` (near-deterministic, slight variation for turn-tone naturalness).
- **Commit-review summarisation temperature:** `0.0` (fully deterministic — summarising the marked draft is a governance-critical read; no variation).
- **Both settings loose-as-frozen in a `wizard_llm_config.v0.json` config file** (Ruling 3 pattern; Master Admin bumps to vN for tuning post-G2b).

**Escalation to Owner:** ratify (a) Claude Sonnet 4.6 as primary model, (b) hard-refuse-user fallback posture, (c) temperature settings 0.2 / 0.0.

### 5.2 Transcript-retention posture — DPO FLAG

**Where wizard transcripts persist:**
- Turn content (`OperatorTurn_v0.user_content` + `agent_content`) lives in `WizardCommitState_v0.turns[]` → persisted to `wizard_sessions` Mongo collection AND mirrored to Northena Ledger via existing `stamp_audit` sidecar (Phase 6 Stage B pattern — one ledger row per session freeze with turn-transcript sidecar).
- **Retention window:** SAME as ObjectiveRequest lifecycle per doctrine. Currently INDEFINITE (Seam 3 CLOSED — Northena Ledger retention window awaits DPO ruling).

**Seam 3 unlock pre-anticipation:**
- When Seam 3 unlocks with DPO-decided window, wizard transcripts INHERIT that window automatically — no separate wizard-transcript retention config needed at Phase 7. The lift is exactly the same as Northena Ledger record retention.
- Zero additional Phase 7 code churn required at Seam 3 unlock.

**DPO flag content classes carried by wizard transcripts:**
| Class | Present in transcript? | Existing retention policy covers? |
|---|---|---|
| Buyer identity (buyer variant `commissioner` + `use_purpose`) | YES | PARTIAL — commissioner covered by ObjectiveRequest v0/v2 policy; `use_purpose` is Phase 7 new (needs DPO ruling) |
| Buyer intent / negotiation lever pulls (turn history) | YES (buyer variant) | NO — no prior retention policy covers negotiation history |
| Competitive signals (may leak in buyer's ask content) | POSSIBLY | NO — new content class at Phase 7 |
| Agent-inferred content (agent_assumed values) | YES | PARTIAL — inferred values covered by ObjectiveRequest retention; assumption evidence is Phase 7 new |
| Feasibility snapshots (Guard 3) | YES (refs only, full result in feasibility_history) | YES — covered by existing FeasibilityResult_v0 retention |

**Escalation to Owner + DPO:** confirm (a) Northena Ledger stamp_audit sidecar pattern (Phase 6 Stage B pattern) is the right ledger surface for wizard transcripts; (b) `use_purpose` + negotiation history + competitive signals need explicit DPO ruling BEFORE Seam 3 unlock (retention window matters differently for these classes than for pure request metadata); (c) whether the buyer-variant transcript needs stricter retention than operator-variant (buyer's `use_purpose` may be highly-sensitive competitive intent).

---

## Return 6 — Per-turn feasibility grounding via canonical shared derivations

### 6.1 Shared-derivation import discipline (Ruling 4)

Every wizard turn (BOTH variants) calls:

```python
from services.mtafiti.floor_feasibility import compute_feasibility
from services.service_1.grain_compatibility import evaluate_grain_form   # buyer offerability
from services.service_1.license_class_selection import derive_license_class  # Return 4 wrap

# In services/wizard/turn_engine.py:
async def turn_grounding(session: WizardCommitState_v0, working_shape: dict):
    fs = compute_feasibility(working_shape["reach"], working_shape["output"]["standard"])
    session.feasibility_history.append(FeasibilityResultRef(
        snapshot_ref=fs.snapshot_ref, at=iso_now(),
    ))
    if session.variant == "buyer":
        # Buyer additional: offerability check.
        grain_ok = evaluate_grain_form(working_shape["output"])
        if not grain_ok.compatible:
            return emit_admission_refusal(reason="grain_form_incompatible")
    return fs
```

### 6.2 Per-turn feasibility snapshot persistence

- Each `OperatorTurn_v0.feasibility_snapshot_ref` stores a reference to a persisted `FeasibilityResult_v0` — full result lives in `WizardCommitState_v0.feasibility_history[]`, keyed by `snapshot_ref`. Per-turn is the pointer.
- Buyer variant additionally stores the per-turn `QuoteEnvelope_v0.quote_id` for live-quote-move UI at commit-review.

### 6.3 Named LOAD-BEARING gates (Return 6)

- **`test_wizard_feasibility_grounding_uses_shared_derivation_only`** (LB): grep-negative sweep — NO re-implementation of `compute_feasibility` or `evaluate_grain_form` inside `services/wizard/*` OR `routers/wizard*`. Wizard MUST import from canonical modules.
- **`test_every_wizard_turn_carries_feasibility_snapshot_ref`** (LB): every `OperatorTurn_v0` in a freeze-time `WizardCommitState_v0` has a non-null `feasibility_snapshot_ref` OR commit refuses at validation (Guard 3 mechanical enforcement).
- **`test_buyer_variant_offerability_bounded_refuses_out_of_bounds_shapes_via_admission_refusal_v0`** (LB per Return 1.2): mock a buyer session that tries a scope_refs outside the owned estate; expect `AdmissionRefusal_v0(reason="reach_outside_owned_estate")` @422 via registry-bump v3→v4.
- **`test_grain_compatibility_derivation_untouched_at_7b`** (byte-identity regression): SHA of `services/service_1/grain_compatibility.py` = SHA captured at Phase 6 Stage B close (Ruling 4 shared-derivation must not be re-implemented).

### 6.4 Registry bumps anticipated

- **`admission_refusal_reasons.v3.json` → `v4.json`** additive: `reach_outside_owned_estate` (buyer offerability), `cumulative_disclosure_breach` (buyer offerability), `provenance_preservation_impossible` (§6 bound violation), `not_feasible_at_declared_floor` (Guard 3), `wizard_variant_immutable_within_session` (variant-switch guard).
- Enforced by `test_admission_refusal_v4_extends_v3_additively`.

---

## Return 7 — Sizing + gates + §3.3 scope-bullet accounting + SPLIT PROPOSAL

### 7.1 Lifted candidates (Phase 7 Stage B reuse)

| Module | Origin phase | Reuse role |
|---|---|---|
| `FeasibilityResult_v0` (contract 16) | Phase 1 | Guard 3 per-turn ground truth |
| `services/mtafiti/floor_feasibility.compute_feasibility` | Phase 1 | Ruling 4 shared-derivation — Guard 3 caller |
| `services/service_1/grain_compatibility.evaluate_grain_form` | Phase 4a | Ruling 4 shared-derivation — buyer offerability caller |
| `services/service_1/license_class_selection.derive_license_class_from_commissioner` | Phase 4a | Fallback arm of Return 4 wrap |
| `AdmissionRefusal_v0` + `admission_refusal_reasons.vN.json` registry | Phase 3/4/5/6 | Wizard refusal-with-path surface |
| `ObjectiveRequest_v2` (contract 15) | Phase 0 | Frozen at commit-time; wizard mints on freeze |
| `QuoteEnvelope_v0` + `services/economics/quote_service.issue_quote` | Phase 6 Stage B | Buyer variant live-quote per turn |
| Northena Ledger row v1 + stamp_audit sidecar | Phase 5 / 6 Stage B | Transcript persistence pattern |
| Solva boundary + composed conclusion flow | G3 + Phase 4b | Downstream at admission (unchanged by Phase 7) |

### 7.2 Net-new candidates (Phase 7 Stage B new landings)

| Item | Est LoC |
|---|---|
| `contracts/wizard_commit_state.py` (WizardCommitState_v0) | 130 |
| `contracts/wizard_operator_turn.py` (OperatorTurn_v0) | 55 |
| `contracts/wizard_agent_assumption.py` (AgentAssumption_v0) | 60 |
| `contracts/wizard_committed_value.py` (CommittedValue_v0 with source-tag validator) | 90 |
| 4 new contract snapshots | 620 (machine-generated) |
| `services/wizard/__init__.py` + package docstring | 25 |
| `services/wizard/state_machine.py` (operator + buyer state engine) | 300 |
| `services/wizard/turn_engine.py` (LLM-backed ask/recommend/propose loop) | 220 |
| `services/wizard/source_tag_validator.py` (Guard 1/2 commit-time invariant checker) | 90 |
| `services/wizard/session_store.py` (Mongo `wizard_sessions` collection I/O) | 130 |
| `services/wizard/wizard_llm_config.v0.json` (Ruling 3 config; model + temperatures) | 30 |
| `services/wizard/admission_handoff.py` (freeze → ObjectiveRequest_v2 mint + POST /api/objectives) | 90 |
| `routers/wizard.py` (4 endpoints; operator + buyer prefixes) | 180 |
| `services/service_1/admission_refusal_reasons.v4.json` (registry bump; 5 new codes) | 65 |
| `services/service_1/admission_refusal.py` — 5 new emit helpers (additive) | 200 |
| `services/service_1/license_class_selection.py` — Return 4 wrap (additive `derive_license_class`) | 45 |
| `server.py` — mount router | 3 |
| `contracts/__init__.py` — 4 new exports | 12 |
| Test surface — `test_phase_7_stage_b_wizard.py` (~20+ named gates) | 700 |
| Test surface — `test_v0_paths_byte_identical_after_7b.py` (parametrised 22 files) | 115 |
| Test surface — `test_composed_conclusion_v0_contract_frozen.py` count invariant 22 → 26 | +10 additive |
| Test surface — `test_frozen_contract_snapshot_parity.py` map 22 → 26 (four new entries) | +6 additive |
| **Subtotal source + config** | **~1650** |
| **Subtotal contracts + snapshots** | **~955** |
| **Subtotal tests** | **~830** |
| **Total net-new estimate (SNAPSHOTS INCLUDED)** | **~3435 LoC** |

### 7.3 Sizing anchor + SPLIT PROPOSAL

**Anticipated Stage B LoC band (Rule 2 v2 anchor):**
- **PM band from prior forecasting:** 1500-2500 LoC.
- **Stage A analysis result:** ~3435 LoC MONOLITH → **would breach top of band by ~37%.**
- **Contract-freeze count at Stage B:** 4 new frozen contracts (WizardCommitState_v0 + 3 inner shapes) → breaches Owner's "4+ contract-freeze count" split threshold.

**⇒ SPLIT PROPOSAL — Phase 7 Stage B is TOO LARGE for a single stage.**

Three-part split proposal:

**Stage B-1 — Contract + shared-derivation wraps + operator state machine** (~1550 LoC)
- 4 new frozen contracts + 4 snapshots (~955 LoC)
- `services/service_1/license_class_selection.py` Return 4 wrap (~45 LoC)
- `services/wizard/source_tag_validator.py` + `state_machine.py` (operator branch only) (~350 LoC)
- `services/wizard/session_store.py` (~130 LoC)
- Router endpoints: `POST /api/wizard/operator/session` + `POST /api/wizard/{session_id}/turn` + `POST /api/wizard/{session_id}/commit-review` + `POST /api/wizard/{session_id}/freeze` (~100 LoC)
- Test surface: ~10 gates for source-tag invariant + Guard 1/2/3 + license-class wrap + shared-derivation regression + byte-identity (~350 LoC)
- Sizing band: 1200-1700 LoC.
- **Snapshot LoC IN band per Standing Disposition 1** (Owner ratified at Phase 6 Stage B close).

**Stage B-2 — Buyer state machine + LLM integration + turn cycles** (~700 LoC)
- Buyer branch of state machine + offerability-check (~200 LoC)
- LLM integration `services/wizard/turn_engine.py` + `wizard_llm_config.v0.json` (~250 LoC)
- Registry bump admission_refusal_reasons.v4.json (~65 LoC) + 5 new emit helpers (~200 LoC)
- Test surface: buyer variant + LLM integration + refusal-with-path (~200 LoC)
- Sizing band: 600-900 LoC.
- **Snapshot LoC IN band** (no new snapshots at this stage).

**Stage B-3 — Commit-review + freeze + admission handoff** (~450 LoC)
- Commit-review flow finalization (paint marked draft)
- Freeze pathway → `services/wizard/admission_handoff.py` → mint ObjectiveRequest_v2 → POST /api/objectives
- End-to-end integration tests
- Sizing band: 350-550 LoC.
- **Snapshot LoC IN band** (no new snapshots at this stage).

**Rationale for split:** each sub-stage is testable end-to-end at a strict Stage B close (Owner ratifies each before the next dispatches). Fits the "small enough to be executed well" doctrine. Alternative — a monolith Stage B — would breach both LoC band AND contract-freeze count, guaranteeing a Rule 2 v2 restatement at close.

**Escalation to Owner:** ratify Stage B split into three sub-stages OR pick monolith with restated band.

### 7.4 Snapshot-in-band declaration (Standing Disposition 1 — forward clause)

Per Standing Disposition 1 (`Sizing-anchor-declares-snapshot-inclusion`) landing at this Stage A close:

**`snapshot_lloc_in_band: yes`** for all three sub-stages proposed above. Established convention (G6 + Phase 6 Stage B ratification) applies: machine-generated snapshot JSON counts against the sizing band. Explicit declaration lands here to satisfy the new forward clause.

### 7.5 Gates roster (Stage B target — full enumeration)

**LOAD-BEARING gates:**
1. `test_wizard_variant_discriminator_immutable_within_session` (Return 1.3)
2. `test_committed_value_v0_source_tag_invariant` (Return 2.5.1) — exactly-one-of-two enforcement
3. `test_wizard_commit_state_v0_freeze_refuses_agent_assumed_on_operator_mandatory_field` (Return 2.5.2)
4. `test_wizard_commit_state_v0_freeze_refuses_orphaned_agent_assumption_ref` (Return 2.5.3)
5. `test_ask_vs_propose_committed_mandatory_fields_all_operator_supplied` (Return 2.5.5)
6. `test_wizard_commit_state_v0_contract_frozen` (D4b freeze)
7. `test_wizard_operator_turn_v0_contract_frozen` (per-inner-shape freeze)
8. `test_wizard_agent_assumption_v0_contract_frozen`
9. `test_wizard_committed_value_v0_contract_frozen`
10. `test_source_tag_invariant_operator_turn_ref_XOR_agent_assumption_id` (structural)
11. `test_license_class_primary_arm_prefers_explicit_over_commissioner_derived` (Return 4.3)
12. `test_wizard_feasibility_grounding_uses_shared_derivation_only` (Return 6.3 — Ruling 4)
13. `test_every_wizard_turn_carries_feasibility_snapshot_ref` (Return 6.3 — Guard 3)
14. `test_buyer_variant_offerability_bounded_refuses_out_of_bounds_shapes_via_admission_refusal_v0` (Return 1.2)
15. `test_operator_variant_agent_never_proposes_on_mandatory_fields` (Return 1.1 — Guard 1)
16. `test_agent_assumed_marking_survives_commit_review` (Return 2.4 — Guard 2)
17. `test_v0_paths_byte_identical_after_7b` (22 prior frozen contract sources SHA-preserved)

**Coverage gates:**
18. `test_no_second_llm_judge_in_wizard_pipeline` (Return 2.5.4 — grep-negative)
19. `test_license_class_docstring_still_documents_phase_7_seam` (Return 4.3)
20. `test_license_class_fallback_arm_unchanged_when_no_explicit_value` (Return 4.3)
21. `test_derive_license_class_from_commissioner_untouched_at_7b` (Return 4.3 — byte-identity slice)
22. `test_grain_compatibility_derivation_untouched_at_7b` (Return 6.3 — byte-identity slice)
23. `test_admission_refusal_v4_extends_v3_additively` (Return 6.4 — registry bump)
24. `test_no_caller_cancelled_or_async_queue_saturated_code_anywhere` (regression from 5b/6b — grep-negative)
25. `test_composed_conclusion_answer_text_lines_316_321_untouched_after_7b` (Verdict A protection regression from 4b/5b/6b)
26. `test_wizard_transcript_persisted_to_northena_ledger_stamp_audit_sidecar` (Return 5.2 — persistence pattern)

Total: **26 named gates** at Stage B — matches Owner's "~15-25 gates" projection (slight above; explained by four-contract freeze + two-variant test doubling on Guard 1/2/3).

### 7.6 §3.3 scope-bullet accounting

Bullets extracted from `/app/docs/mandates/RMS_Product_Engineering_Spec_v3.md` §3.3 (lines 55-65):

| Bullet (verbatim excerpt) | Return covering | Stage B gate(s) enforcing | Residual ambiguity |
|---|---|---|---|
| **Operator variant** "Field tiers: **operator-mandatory** (reach, output's four fields, done-condition, budget, lawful basis) — the agent asks, never proposes." | Return 1.1 + Return 2 | #5, #15 (Guard 1 LB) | None. Mandatory-field list is exhaustive per Return 2.2. |
| **Operator variant** "**Preference** (weighting, ordering, formatting, sampling within budget) — the agent may recommend." | Return 1.1 (Guard 2 in state machine) | #3, #4, #16 (LB) | None. Preference-tier list intentionally not exhaustive — v3 leaves room for §3.3 evolution. |
| **Operator variant** "Guards: (1) ask-don't-propose on mandatory fields; (2) every agent-supplied value marked `agent_assumed`; (3) every turn feasibility-grounded in the estate (§5)." | Guards 1/2/3 explicit throughout Returns 1/2/6 | #5, #16, #13 (all three LB) | None. Guards enumerated in state machine pseudocode. |
| **Operator variant** "Enforcement: the operator reviews the complete marked draft and freezes." | Return 1.1 (commit-review flow) + Return 2.4 (UI seam) | #16 (LB) — agent_assumed marking survives to commit-review paint | Phase 8 rendering seam — captured in Return 2.4; frontend implementation deferred to Phase 8. |
| **Buyer variant** "Same shaping mechanism, different ceiling." | Return 1.2 | #14 (buyer LB) | None. Same state engine + variant discriminator. |
| **Buyer variant** "The agent shapes within **offerability**: owned estate only, license class, disclosure limits. Shapes outside offerability are refused with the reason." | Return 1.2 (offerability-check function) + Return 6 | #14 (LB), #23 (registry bump) | Cumulative-disclosure check reads G6 ledger — Phase 7 relies on Seam existing; if seam paths change, gate needs update. |
| **Buyer variant** "The agent **may propose** (steering a buyer to a cheaper feasible shape is sales, not laundering)." | Return 1.2 (state engine may-propose branch) | Coverage in state-engine tests (#14 LB implicit) | Sales-vs-laundering line is codified in the buyer-variant state engine; Owner ratification recommended at Stage B open. |
| **Buyer variant** "Price and delivery-time (§8) compute live and move as the shape moves." | Return 1.2 (per-turn quote_service.issue_quote invocation) | Coverage: latest_quote_ref field validation gate (implicit via Return 3.1) | None. Phase 6 Stage B seam fully wired. |
| **Buyer variant** "The buyer never sets lawful basis; use-purpose drives license class." | Return 3.1 (buyer-variant `use_purpose` field; no `lawful_basis` surface) + Return 4 | #11 (LB — primary arm prefers explicit); coverage: `test_buyer_variant_never_sets_lawful_basis` (new coverage gate — add to Stage B roster) | HAZARD-STOP-CANDIDATE per Return 4.2 — `envelope.license_class` field absent on ObjectiveRequest_v2; Owner ratification needed. |
| **§6 provenance-preservation bound** (cross-ref) "The transform produces the shaped output only where the declared standard survives it." | Return 1.2 (buyer offerability sub-check (d)) | Coverage: `test_provenance_preservation_impossible_refuses_during_shaping` (new gate — add to Stage B roster) | Phase 6 code has provenance discipline embedded; Phase 7 lifts into shaping-time refusal — requires shared-derivation module (should live at `services/service_1/provenance_preservation.py` — new module at Stage B). |

**Residual ambiguities → Escalations to Owner (Stage A close):**
- (E1) `envelope.license_class` seam landing (Option A / B / C from Return 4.2).
- (E2) LLM primary + fallback + temperature (Return 5.1).
- (E3) WizardCommitState_v0 D4b freeze posture + inner-shape freeze granularity (Return 3.3-3.4).
- (E4) Split Stage B into three sub-stages OR monolith with restated band (Return 7.3).
- (E5) Transcript-retention DPO ruling for use_purpose + negotiation history + competitive signals BEFORE Seam 3 unlock (Return 5.2).
- (E6) Sales-vs-laundering line codification review (§3.3 buyer "may propose" bullet).
- (E7) Provenance-preservation shared-derivation module landing at Stage B-1 vs B-2 (new `services/service_1/provenance_preservation.py`).

---

## Verification tail — Two Phase 6 Stage B addendum flags

### Flag i — Discretionary figure reconcile

**Authoritative source:** `/app/docs/close_reports/phase_6_stage_b.md` §5 Rule 2 v2 accounting table, Total row (line 191).

Verbatim quote from the table's Total row:
> *"~2812 LoC | Above the projected 1800-2400 band; overage entirely explained by (a) 372 LoC of mechanical parity snapshot JSON (non-discretionary) + (b) ~250 LoC of retroactive citation content mandated by the Owner's new meta-doctrine + (c) mandatory HAZARD-STOP-NOTES in every economics module (discipline-driven, no discretion). **Discretionary LoC ≈ 2190.**"*

**Reconcile arithmetic:**
- Total: 2812
- Back-out (a) snapshot JSON: 372
- Back-out (b) retroactive citation: 250
- Back-out (a) + (b) = 622
- 2812 − 622 = 2190 ✓ arithmetic clean.

**Small-N coincidence check:** The 2190 figure IS the arithmetic of backing out (372 + 250) = 622 from 2812. It is NOT a summary-artifact.

However — Owner's post-close ruling (this dispatch) states: *"Snapshot LoC (372) and mandatory HAZARD-STOP-NOTES LoC (~90) STAY in the band count (prior-phase precedent; mandated discipline is standard load). Only the 250 LoC of Owner-mandated retroactive citation content backs out."*

Under this ruling, the AUTHORITATIVE Owner-side accounting is:
- Total: 2812
- Back-out only (b) retroactive citation: 250
- **Effective discretionary against band: 2812 − 250 = 2562.**
- 2562 vs 2400 top = +162 / 2400 = **+6.75% delta ABOVE band** ← matches Owner's verdict.

**Result:** The close report's "discretionary ≈ 2190" figure IS honest arithmetic per its own §5 table (backs out snapshot AND citation). The Owner's ruling narrows the back-out set to citation-only, yielding **2562** as the authoritative comparison against the projected 1800-2400 band. Both figures are correct; they answer different questions (report backs out (a)+(b); Owner ruling backs out only (b)). **No summary-artifact detected.** Small-N-collision coincidence is NEGATIVE — the arithmetic is real.

**Recommended remediation:** at future Stage B close reports, distinguish "arithmetic-backed-out" (report's discipline) from "band-comparison-backed-out" (Owner-ruling discipline) as two rows in the accounting table so the two figures don't confuse the audit read.

### Flag ii — Non-precedent marking coverage

**Grep results across `services/economics/*.json` + `contracts/quote_envelope.py` + `contracts/async_delivery_accepted_v1.py`:**

| File | Illustrative-value inventory | Marker present? | Marker class |
|---|---|---|---|
| `price_model.v0-exploratory.json` | 12 multiplier values + `base_figure_illustrative: "10.00"` + delivery estimate defaults | YES × 3 | (a) `tier="exploratory"` reference (line 3), (b) filename `v0-exploratory` (line 1 implicit), (c) explicit `hazard_stop_notes` block at line 44 — 4 hazard notes |
| `pricing_tiers.v0.json` | 1 tier definition (`exploratory`) | YES × 3 | (a) `tier: "exploratory"` (line 9), (b) `spec_ref: "structurally non-precedent time-boxed exploratory tier"` (line 4), (c) spec_anchor quoting v3 §8 bullet 2 (line 13) |
| `fleet_policy.v0.json` | Apportionment (0.40 / 0.35 / 0.25) | YES × 1 | (c) `hazard_stop_notes` block at line 21 with R4-SD2 arbitration-deferral notes |
| `admission_refusal_reasons.v3.json` | Reason codes only; no illustrative values | N/A (no illustrative values) | — |
| `contracts/quote_envelope.py` | Field descriptions reference illustrative values via config indirection | YES × 2 | Docstring at line 6-8 quotes Owner ruling "*structural non-precedent marker*"; line 12-14 module docstring HAZARD-STOP-NOTES referencing G2b |
| `contracts/async_delivery_accepted_v1.py` | No illustrative values (wrapper contract) | N/A (no illustrative values) | — |

**Unmarked-leak enumeration:** **ZERO.**

Every illustrative value across the Phase 6 Stage B surface satisfies at least one (typically multiple) of the Owner's three marking conditions (a) `pricing_tier="exploratory"` reference, (b) `price_model.v0-exploratory.json` file containment (marker in filename), (c) explicit HAZARD-STOP-NOTES in-file.

**Verdict:** **Phase 6 Stage B ratio is nature-of-phase, not drift.** Config-values phases structurally require high discretionary (mechanism > mechanics ratio), and the marking coverage is complete. No remediation ticket needed.

---

## Machine-attested block (Stage A close)

```
[GREEN] pytest -q                                                        550 / 550 unchanged
[GREEN] test_frozen_contract_snapshot_parity                             22 / 22 (parity UNCHANGED at Stage A)
[GREEN] substrate-drop invariants                                        13 / 13 (Phase_7 GREEN — no new contracts at Stage A)
[STATUS] Stage A design-only: ZERO code files written outside /app/docs/stage_a_proposals/phase_7_stage_a.md
[STATUS] Zero new frozen contracts landing at Stage A
[STATUS] No `git push`
[CANONICAL] /app/docs/stage_a_proposals/phase_7_stage_a.md (SHA quoted in return message)
```

---

## Escalations to Owner for Stage B dispatch conditions

E1 — `envelope.license_class` seam landing: Option A (ObjectiveRequest_v3 with envelope field) / Option B (envelope.frozen_wizard_ref via v3) / Option C (two-arg derive; no ObjectiveRequest version bump).
E2 — LLM primary (Claude Sonnet 4.6 proposed) + fallback posture (hard-refuse-user proposed) + temperature settings (0.2 / 0.0 proposed).
E3 — WizardCommitState_v0 + three inner shapes D4b freeze posture (freeze all four recommended) + parity 22 → 26 or 27 depending on E1 outcome.
E4 — Split Stage B into three sub-stages (B-1 contract+operator, B-2 buyer+LLM, B-3 commit-review+freeze+handoff) recommended, OR monolith with restated band.
E5 — Transcript-retention DPO ruling for use_purpose + negotiation history + competitive signals BEFORE Seam 3 unlock.
E6 — Sales-vs-laundering line codification review for buyer variant `may propose` bullet.
E7 — Provenance-preservation shared-derivation module (new `services/service_1/provenance_preservation.py`) landing sub-stage: B-1 vs B-2.

---

*End of Phase 7 Stage A design proposal. Awaiting Owner rulings on E1-E7 before Stage B dispatch.*
