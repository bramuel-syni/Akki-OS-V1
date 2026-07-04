"""AdmissionRefusal@v0 — governed admission-time refusal envelope
(Phase 3 freeze — 17th frozen contract).

Spec authority: RMS Product & Engineering Spec v3 §6.5 (Model form off
the offerable menu) — FIRST firing reason. Envelope is designed to
accommodate FUTURE admission-time refusal reasons via versioned registry
extension (Condition 2, Phase 3 dispatch ruling 2026-07-03).

**Family consistency with `Service1Refusal@v0` (Condition 1).**
Both share the outer refusal pattern: `outcome: Literal["refused"]` +
`trace_id: str` + `reason: str`. Discriminated by REASON semantics and
FIRING SITE — admission-time (this envelope) vs composition-time
(`Service1Refusal@v0`) — NOT by a second refusal grammar. Consumers
rendering refusals can treat both as members of the same family at the
outer pattern level.

**Reason extension path — LOAD-BEARING (Condition 2 + doctrinal-tension
resolution, 2026-07-03).**

The `reason` field is typed as constrained `str` (snake_case pattern),
NOT `Literal`. The valid-reason SET lives in a plain versioned registry
at `services/service_1/admission_refusal_reasons.v0.json`. Adding a
future reason is a REGISTRY BUMP (v0.json → v1.json, or an append-only
entry per the config policy), NEVER a contract file modification and
NEVER a Literal-widening. This preserves three simultaneous constraints:
  * **Owner ruling (Condition 2)** — reasons extend by ADDITION via
    registry, never new contracts.
  * **Standing Ruling 2** — Literal-widening on a frozen contract is a
    HAZARD-STOP (breaks byte-identical snapshot).
  * **Elevated Doctrine (Substrate-Drop v2)** — validation surface IS
    contract surface; the registry lives OUTSIDE the contract so the
    contract's JSON schema is byte-invariant across reason additions.

**Precedent anchors** for this pattern:
  * `qualification_matrix` — shape-classes-plus-config (shape frozen;
    values in `v0.json`).
  * `feasibility-config@vN` (Phase 1) — control-surface pattern:
    versioned, recorded, reversible; never in-place mutation.

Service-layer validation reads the registry at construction/validation
time (see `services/service_1/admission_refusal.py::is_valid_reason`).
The contract file (this file) and its `.contract_snapshot.json` stay
byte-identical when a reason is added — that is the intended alarm
behaviour of the mechanical parity invariant.

**Consumed by (Condition 4 — dual consumer):**
  1. **Admission at `external_request` entry** — Phase 2 v2 dispatch
     emits this envelope INSTEAD of the scaffold 501 placeholder when
     `output.form == "model"`. HTTP 422 (matching `Service1Refusal@v0`
     family status settled at A2).
  2. **Wizard rendering at `work_order` entry** — refusal-with-path per
     UI Spec §3.3 (Phase 7 receiver, not yet built). The contract is
     shaped such that Phase 7's wizard-side rendering will consume this
     envelope unchanged — refusal, never error.

**Actor-appropriate content (Condition 3).**
The caller-facing action string states the caller's actionable move
("choose a different output form"). It NEVER surfaces owner-side
deliberations ("await owner acceptance of the ingredient-manifest
guarantee" or similar) as if they were caller-actionable. Enforced by
grep-negative gate `test_admission_refusal_actor_appropriate_string`.

**Convention anchors:**
  * `computed_at: str` (ISO-8601 UTC) mirrors `MiningPlan.generated_at`
    at `contracts/targeta_plan.py`.
  * `outcome: Literal["refused"]` mirrors `Service1Refusal@v0` outer
    discriminator — this literal is the SHAPE-INVARIANT MARKER (not an
    extensible enum) so Literal-freeze here is safe under Ruling 2.

Freeze contract: `AdmissionRefusal_v0.model_json_schema()` snapshotted
to `tests/invariants/admission_refusal.contract_snapshot.json`.
Mechanical parity invariant enforces the source→snapshot bijection at
17 entries post-Phase-3.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class AdmissionRefusal_v0(BaseModel):
    """Governed admission-time refusal envelope.

    First firing reason: `form_not_offerable` (v3 §6.5). Future reasons
    (e.g. standard-not-met, offerability-out-of-scope) land as REGISTRY
    additions at `services/service_1/admission_refusal_reasons.vN.json`
    — this contract file is NOT modified when a reason is added.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    outcome: Literal["refused"] = Field(
        default="refused",
        description=(
            "Family discriminator. Same value + type as "
            "Service1Refusal@v0.outcome — refusal envelopes are a "
            "family, distinguished by firing site + reason semantics, "
            "not by a second grammar."
        ),
    )
    reason: str = Field(
        ...,
        min_length=1,
        pattern=r"^[a-z][a-z_]*[a-z]$",
        description=(
            "Refusal reason code. snake_case. First firing value: "
            "'form_not_offerable' (v3 §6.5). Valid-reason SET governed "
            "by `services/service_1/admission_refusal_reasons.vN.json` "
            "(versioned registry) — NOT by a Literal here. Adding a "
            "reason = registry bump, NEVER contract modification. "
            "See module docstring 'Reason extension path'."
        ),
    )
    trace_id: str = Field(
        ...,
        min_length=1,
        description=(
            "Correlation ID. Same field semantic as "
            "Service1Refusal@v0.trace_id — family consistency."
        ),
    )
    requested_output_form: Optional[str] = Field(
        default=None,
        description=(
            "Contextual echo of the value that was rejected — e.g. "
            "'model' when reason == 'form_not_offerable'. Nullable so "
            "future non-form admission reasons can leave it null."
        ),
    )
    off_menu_fact: str = Field(
        ...,
        min_length=1,
        description=(
            "Plainly-stated fact of the deliberate off-menu / refused "
            "state (v3 §6.5: 'a deliberate, unambiguous state, not an "
            "omission'). Contains no apology, no owner-side "
            "deliberation, no 'await …' phrasing (Condition 3)."
        ),
    )
    what_you_can_do: str = Field(
        ...,
        min_length=1,
        description=(
            "Actor-appropriate path forward — what the CALLER can "
            "actionably do. Grep-negative on owner-side deliberations: "
            "no 'await owner', 'owner acceptance', 'ingredient "
            "manifest' phrasing (Condition 3, LOAD-BEARING)."
        ),
    )
    computed_at: str = Field(
        ...,
        min_length=1,
        description=(
            "ISO-8601 UTC. When the refusal envelope was constructed. "
            "Convention-anchored to MiningPlan.generated_at."
        ),
    )
