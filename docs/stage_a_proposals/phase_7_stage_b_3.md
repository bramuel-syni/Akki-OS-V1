# Phase 7 Stage B-3 — Stage A Proposal (Owner-Pre-Ratified)

**Owner ruling verbatim (Phase 7 Stage B-2 close dispatch, 2026-07-04):**

> *"Scope as settled at split ratification: commit-review + buyer freeze +
> admission handoff to POST /api/objectives. The Option C seam,
> license-class-at-selection gate, and dual-delta acceptance recording are
> already landed or ruled — zero open questions."*

Per the dispatch, **no Owner round-trip required.** This Stage A doc lands
on disk per Standing Rule v3 and per the CI-count-attestation posture
(Owner ruling (a) standing) — dispatch proceeds directly to Stage B
implementation blocks.

---

## 1. Scope (from Owner dispatch)

**Three deliverables closing the wizard trilogy (B-1 + B-2 + B-3).**

### 1.1 Commit-review path completion (both variants)

Currently at B-2 close: operator commit-review (B-1) + buyer commit-review
(B-2) both return `{you_supplied, agent_assumed_items, violations,
ready_to_freeze}`. Buyer variant additionally returns `proposals`.

**B-3 additions:**

- **`dual_delta_summary`** (NEW field on buyer commit-review response) —
  aggregate of `class_delta` + `price_delta` from every recorded proposal,
  keyed by `proposal_id`. Sourced from `services/wizard/dual_delta.py`
  (landed at B-2) via a NEW helper `summarise_proposals(proposals)`.
  Single-source per Owner Condition-2 posture (no in-router computation).

- **License-class-at-selection integration** (both variants) — commit-review
  invokes `services/service_1/license_class_selection.py::derive_license_class(
  envelope, wizard_state)` against the reviewed state; surfaces any
  class-drift between `wizard_state.license_class` (user-committed) and
  the primary-arm derivation. Class drift is a soft signal (NOT a hard
  refusal); it renders in the commit-review body as
  `license_class_drift: {committed: str, derived: str} | null`.

- **Buyer variant only:** commit-review body extended with the two new
  fields above.

- **Operator variant:** commit-review body extended with
  `license_class_drift` only (operator has no proposals — no
  `dual_delta_summary`).

### 1.2 Buyer freeze parity with operator freeze

Currently at B-2 close: buyer freeze lands the machinery + `variant="buyer"`
frozen state, but is missing:

- **Ledger write via `record_wizard_freeze`** (operator has it; buyer does
  NOT) — required by Owner E5 `wizard_transcript` retention class marker
  landing at B-1.

**B-3 additions:**

- Buyer freeze calls `services/wizard/turn_ledger.py::record_wizard_freeze(
  frozen, lawful_basis_ref=...)` after the `session_persistence.upsert_session(
  frozen)` call. Idempotent per `(trace_id, run_id='wizard-freeze-{session_id}')`
  (existing invariant from B-1).

- Body now accepts optional `lawful_basis_ref` (defaults to
  `"wizard-lawful-basis-unset"` matching operator).

### 1.3 Admission handoff (NEW endpoint on both variants)

New endpoint: **`POST /api/wizard/{variant}/{session_id}/handoff`** where
`{variant}` ∈ `{operator, buyer}`.

**Semantics:**

1. Load frozen wizard state from Mongo (post-freeze). If session not
   frozen yet → HTTP 422 `wizard_not_frozen` reason (bounded string).
2. Invoke NEW helper `services/wizard/admission_handoff.py::compose_objective_request_from_frozen_state(wizard_state)`
   → returns `ObjectiveRequest_v2`.
3. Submit the composed `ObjectiveRequest_v2` through the existing async
   admission surface (`routers/objectives.py::create_objective(...)`),
   using the session's `idempotency_key` = `f"handoff-{session_id}"`
   (deterministic — repeat handoff on same session returns same
   `objective_id` per Phase 5 §7 idempotency guarantee).
4. Return:
   - `HTTP 202 AsyncDeliveryAccepted_v1` on admission accept (payload
     carries `objective_id + trace_id + delivery_estimate + quote`).
   - `HTTP 422 AdmissionRefusal_v0` on admission refuse (payload carries
     `reason + supported_class + what_would_raise_it`) — passthrough of
     existing refusal codes; **NO new refusal codes for handoff.**
   - `HTTP 503` on infra fault (existing async admission behavior).
5. On accept: persist `frozen_objective_ref = objective_id` back onto the
   frozen wizard state (Mongo update; no schema change — the field
   `WizardCommitState_v0.frozen_objective_ref` already exists at B-1).

**Idempotency:**

- Repeat handoff on the same frozen session returns the same
  `objective_id` (existing async idempotency guarantee, keyed on
  `idempotency_key`).
- Second handoff detects `wizard_state.frozen_objective_ref` is already
  populated and short-circuits to fetch the existing objective via
  `GET /api/objectives/{objective_id}` — returns the same 202/422 body
  shape.

**Dual-delta acceptance recording (buyer only, from B-2):**

The composed `ObjectiveRequest_v2` MUST propagate `class_delta` +
`price_delta` from the wizard's `proposals` list into the objective's
`stamp_audit` sidecar. Mechanism: `compose_objective_request_from_frozen_state`
attaches a `dual_delta_summary` dict onto a NEW sidecar field consumed
by the async admission layer's `stamp_audit` path (single-source; no
in-router assembly). If ObjectiveRequest_v2 does not have a natural home
for this sidecar (its frozen shape at B-2), the summary lands on the
`envelope.floor_feasibility` open-shape dict per Substrate-Drop v2 Part 2
`Dict[str, Any]` posture — verified against the frozen shape at
implementation time.

**No new frozen contracts at B-3.** Parity holds at 26. If B-3 discovers
a genuine new-envelope need (e.g., `WizardHandoffReceipt_v0`), it lands
as a NEW versioned file (never in-place mutation), and escalates to
Owner as governance-semantic contact.

---

## 2. Router-touch enumeration

### 2.1 `backend/routers/wizard_buyer.py` (existing router)

| Edit | Type | Description |
|---|---|---|
| `POST /{session_id}/commit-review` | modify | Extend response body with `dual_delta_summary` + `license_class_drift`. |
| `POST /{session_id}/freeze` | modify | Add `record_wizard_freeze(...)` call after `upsert_session(...)`. Add `lawful_basis_ref` body param. Return body extended with `ledger_run_id`. |
| `POST /{session_id}/handoff` | add | NEW endpoint; ~40 LoC. |

### 2.2 `backend/routers/wizard_operator.py` (existing router)

| Edit | Type | Description |
|---|---|---|
| `POST /{session_id}/commit-review` | modify | Extend response body with `license_class_drift` only. |
| `POST /{session_id}/handoff` | add | NEW endpoint; ~40 LoC. |

### 2.3 `backend/services/wizard/admission_handoff.py` (NEW module)

| Function | Description |
|---|---|
| `compose_objective_request_from_frozen_state(wizard_state)` | Single-source composer; returns `ObjectiveRequest_v2`. |
| `summarise_dual_deltas(proposals)` | Helper; aggregates class_delta + price_delta from a proposals list, keyed by `proposal_id`. Buyer-variant only. |

Estimated ~120 LoC. Declarative-table pattern (mirroring `dual_delta.py`
+ `provenance_preservation.py`); pure function; no LLM; no I/O; no
network.

### 2.4 `backend/services/wizard/buyer_state_machine.py` (modify)

| Edit | Type | Description |
|---|---|---|
| `preflight_freeze(session)` | modify | +1 line to import `record_wizard_freeze` reuse discipline (single-source, no reimpl). Actually NO edit — `record_wizard_freeze` is already imported by the router; SM stays untouched. |
| (no change) | — | Buyer SM is at parity with the operator SM shape; the ledger call lives at the router layer per B-1 pattern. |

### 2.5 `backend/services/service_1/license_class_selection.py` (existing, unchanged)

Byte-identical. `derive_license_class(envelope, wizard_state)` was landed
at B-1; commit-review invokes it as-is.

### 2.6 `backend/routers/objectives.py` (existing async admission router)

Not touched at the wire layer. The handoff endpoint invokes the
existing `create_objective_endpoint(request_body, ...)` handler
function directly (in-process, no HTTP hop) OR via httpx-to-self (TBD
at implementation — single-source posture prefers direct function call).

---

## 3. Test roster (est. 25-30 gates)

Test file: `backend/tests/invariants/test_phase_7_stage_b_3_wizard.py` (NEW).

### 3.1 Buyer commit-review extensions (~5 gates)

- `test_buyer_commit_review_returns_dual_delta_summary_when_proposals_present`
- `test_buyer_commit_review_returns_empty_dual_delta_summary_when_no_proposals`
- `test_buyer_commit_review_returns_license_class_drift_when_committed_differs_from_derived`
- `test_buyer_commit_review_license_class_drift_is_null_when_committed_matches_derived`
- `test_buyer_commit_review_e2e_via_asgi_transport` (E2E smoke)

### 3.2 Operator commit-review extensions (~2 gates)

- `test_operator_commit_review_returns_license_class_drift_only_no_dual_delta_summary`
- `test_operator_commit_review_shape_stable_after_7b_3` (regression)

### 3.3 Buyer freeze ledger parity (~3 gates)

- `test_buyer_freeze_writes_wizard_freeze_ledger_row`
- `test_buyer_freeze_ledger_carries_wizard_transcript_data_class` (Owner E5)
- `test_buyer_freeze_returns_ledger_run_id_in_response_body`

### 3.4 Admission handoff — operator variant (~5 gates)

- `test_operator_handoff_returns_202_on_admission_accept`
- `test_operator_handoff_returns_422_admission_refusal_on_governance_refuse` (LB — no new refusal codes)
- `test_operator_handoff_returns_422_wizard_not_frozen_when_session_not_frozen` (LB — bounded reason)
- `test_operator_handoff_idempotent_returns_same_objective_id_on_repeat`
- `test_operator_handoff_persists_frozen_objective_ref_on_accept`

### 3.5 Admission handoff — buyer variant (~4 gates)

- `test_buyer_handoff_returns_202_with_quote_carrying_dual_delta_summary` (LB — dual-delta persistence)
- `test_buyer_handoff_returns_422_admission_refusal_passthrough` (LB — no new refusal codes)
- `test_buyer_handoff_idempotent_returns_same_objective_id_on_repeat`
- `test_buyer_handoff_dual_delta_summary_lands_in_stamp_audit_sidecar`

### 3.6 Single-source guards for admission_handoff.py (Owner Condition-2 posture) (~3 gates)

- `test_admission_handoff_does_not_reimplement_shared_symbol` (parametrised × 3: `derive_license_class`, `_record_feasibility_snapshot`, `summarise_proposals_dual_delta` — the third being the new symbol we define ONCE in this module and reuse; ensures no other module reimplements it).
- `test_admission_handoff_imports_shared_helpers_from_proven_modules`
- `test_no_new_refusal_codes_at_7b_3` (grep-negative on new `Literal` widening; **LB** — Owner ruling: no new refusal codes for handoff).

### 3.7 Frozen-contract posture regression (~4 gates)

- `test_prior_26_contracts_count_at_26_still` (count invariant)
- `test_prior_contract_file_exists_and_stable_at_7b_3` (parametrised over 25 contract source files — byte-identity)
- `test_composed_conclusion_synthesis_lines_untouched_at_7b_3` (Verdict A regression)
- `test_operator_router_still_mounts_7_endpoints_at_7b_3` (existing 6 + new /handoff = 7)
- `test_buyer_router_still_mounts_8_endpoints_at_7b_3` (existing 7 + new /handoff = 8)

### 3.8 Struck-code regression (~1 gate)

- `test_no_caller_cancelled_or_async_queue_saturated_code_at_7b_3`

**Total: ~27 named gates + parametrised expansions.** Anchored CI delta:
685 → ~712 (+27).

---

## 4. Rule 2 v2 line accounting — anticipated band

**Lift budget:**
- `derive_license_class` from B-1 (~40L reuse; already single-source; imported)
- Async admission endpoint from Phase 5b (~150L reuse; existing endpoint invoked)
- Ledger write from B-1 (~15L reuse; `record_wizard_freeze` imported)
- `dual_delta.py` from B-2 (~30L reuse; declarative table imported)
- Router idempotency pattern from Phase 5b (~40L reuse; `idempotency_key` handling)

**Anticipated total lift:** ~275 LoC.

**Net-new discretionary anticipated:**
- `admission_handoff.py` NEW module ~120L (declarative-table style; mandate-forced by v3 §3.3 + Owner ruling)
- `/handoff` endpoint × 2 routers ~80L total
- Buyer freeze ledger call ~8L
- Commit-review extensions × 2 routers ~40L total
- Test file ~700L (27 named gates + parametrised expansions)

**Anticipated total net-new:** ~950 LoC.

**Anchored band: 800-1100 LoC.**

**Snapshot LoC in band:** `no` (no new frozen contracts anticipated; no
snapshot JSON generation. If Owner ruling shifts and a new
`WizardHandoffReceipt_v0` frozen contract becomes necessary at
implementation time, `snapshot_lloc_in_band` becomes `yes` and the band
expands by ~180 LoC for snapshot JSON.)

**Stop-and-judge triggers:**
- (a) `>1265 LoC` (+15% over top-of-band) → Owner stop-and-judge before landing.
- (b) `discretionary-only >2.5×` → same.

---

## 5. Standing constraints (re-confirmed)

- 26 frozen contracts byte-identical.
- No LLM code outside `services/synisense/shield/*` (Shield boundary preserved from B-2).
- No new §0.1 Standing Dispositions (§0.1 FROZEN).
- No refactoring.
- No `git push`.
- No fresh Rule-2 derivation.
- Infra-not-refusal (503) invariant preserved: any infra fault → 503, never a governed 422.
- Cancellation-is-a-state-not-a-refusal preserved.
- Single-source posture (Owner Condition-2 flavor): `admission_handoff.py` uses IMPORTS from operator-proven modules for all shared symbols.
- **No new refusal codes at B-3.** Handoff refusals passthrough the existing catalog (`form_not_offerable`, `standard_ineligible`, `composition_below_floor`, etc.). If genuine new-semantic surfaces → escalate as governance-semantic contact.

---

## 6. Commit-block sequence

**Block A — buyer freeze ledger parity + commit-review extensions**
- Buyer freeze `record_wizard_freeze(...)` call
- Commit-review `dual_delta_summary` + `license_class_drift` extensions (both variants)
- Anticipated CI delta: 685 → ~695 (+10 gates).

**Block B — admission_handoff.py + `/handoff` endpoints (both variants)**
- NEW module `admission_handoff.py`
- NEW `POST /api/wizard/{variant}/{sid}/handoff` on both routers
- Anticipated CI delta: 695 → ~712 (+17 gates).

**Block C — frozen-contract posture regression + struck-code + count invariants**
- Byte-identity gate parametrised over 25 contract sources at 7b-3
- Router mount-count invariants (operator now mounts 7; buyer now mounts 8)
- Anticipated CI delta: 712 → ~715 (+3 gates).

**Total anchored: 685 → ~715 (+30 net).**

---

## 7. Non-goals at B-3 (deferred)

- Frontend wizard surfaces (Phase 8 full — Operator §2.2 Commission Wizard).
- §6.3 Knowledge Artifact / §6.4 Callable Skill (STAKED per Owner).
- Phase 8 Stage A frozen-contract trajectory restatement (Phase 8 kickoff scope).
- Governance seam unlock config swaps (Owner-side, blocked).
- New refusal codes for handoff semantics (Owner ruling: escalate if new-semantic surfaces).

---

## 8. Proceed condition

Per Owner dispatch: **no Owner round-trip required.** Stage A doc on
disk → proceed directly to Stage B Block A implementation.

---

*End of Phase 7 Stage B-3 Stage A proposal.*
