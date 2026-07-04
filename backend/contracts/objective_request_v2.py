"""ObjectiveRequest v2 — RMS Service-2 request envelope (Phase 0 freeze).

OWNER RULING (Substrate-Drop v2 close, 2026-07-03): loose-as-frozen is
deliberate. Ranges are learned, not invented. Hardening lands as a NEW
contract version; in-place narrowing is mutation → HAZARD-STOP. The
HAZARD-STOP-NOTES below are RESOLVED, not pending.

Spec authority: RMS Product & Engineering Spec v3 §3.2.

**Additive extension of `objective_request@v0`.** The v0 contract at
`contracts/objective_request.py` remains byte-identical and continues to
serve any legacy path. This v2 lives alongside as a separate frozen
contract; v0 is neither mutated nor superseded at the schema level.

v3 §3.2 verbatim declaration:
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

Owner ruling (Substrate-Drop v2, Part 2, Phase 0):
  * `shaping` is nested as `shaping.operator` for variant symmetry with
    `commercial.buyer`.
  * `commercial` is nested as `commercial.buyer` for the same reason.
  * `output.form` accepts `model` at contract level; the shaping-time
    refusal for the off-menu model form lives at Phase 3, not at
    contract validation (per v3 §6.5).

HAZARD-STOP-NOTES (Owner rule may narrow at any time via new frozen contract;
never silently mutate a typed field here — Substrate-Drop v2 elevated
"validation surface IS contract surface"):

  * `Reach.depth` — v3 §3.2 declares field presence; v3 §3.1 describes it
    as "extraction/reasoning depth"; v3 §4 states depth sizes mining
    volume, reasoning depth, compliance layers, worker allocation. No
    scalar type is declared. Typed here as `str` (free-form authored)
    following v0's `ObjectiveRequest.objective_text` precedent. Owner
    may narrow (enum, int, float) via a new frozen contract when
    depth's runtime semantics land.
  * `Envelope.budget` — v3 §3.2 declares presence, no scalar type. Typed
    `str` (authored) pending owner ruling.
  * `Envelope.scope_ceiling` — v3 §3.2 declares presence, no scalar type.
    Typed `str` (authored) pending owner ruling.
  * `Envelope.availability_snapshot` and `Envelope.floor_feasibility` —
    outputs of the Estate Feasibility Query (v3 §5, not yet built).
    Typed `Dict[str, Any]` (open-shape) matching v0's
    `EstateRegionSelector.filters` precedent.
  * `Envelope.committed_at` — timestamp; typed `str` (ISO-8601) matching
    `MiningPlan.generated_at` precedent.

Freeze contract: `ObjectiveRequest_v2.model_json_schema()` snapshotted to
`tests/invariants/objective_request_v2.contract_snapshot.json`.
Mechanical parity invariant
(`tests/invariants/test_frozen_contract_snapshot_parity.py`) enforces
that this file has exactly one canonical snapshot and vice versa.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.objective_request import DefensibilityFloor


class ObjectiveEntry(str, Enum):
    """v3 §3.2: entry-point discriminator. Values verbatim from v3.

    * `work_order`      — Day-Zero, wizard-shaped operator objective.
    * `external_request`— Day-to-Day, arrives complete over the API or
                          is refused at admission.
    """

    WORK_ORDER = "work_order"
    EXTERNAL_REQUEST = "external_request"


class OutputForm(str, Enum):
    """v3 §3.1 output.form enumeration. All five accepted at contract;
    `model` refusal lives at the shaping wizard (Phase 3, per v3 §6.5)."""

    QUALIFIED_DATA = "qualified_data"
    KNOWLEDGE_ARTIFACT = "knowledge_artifact"
    MODEL = "model"
    CALLABLE_SKILL = "callable_skill"
    COMPOSED_CONCLUSION = "composed_conclusion"


class OutputConsumer(str, Enum):
    """v3 §3.1 output.consumer enumeration."""

    PERSON = "person"
    SYSTEM = "system"
    TRAINING_PIPELINE = "training_pipeline"


class OutputGrain(str, Enum):
    """v3 §3.1 output.grain enumeration."""

    PER_CLAIM = "per_claim"
    AGGREGATED = "aggregated"
    SYNTHESIZED_WHOLE = "synthesized_whole"


class Reach(BaseModel):
    """v3 §3.2 verbatim shape: `reach: { scope_refs[], exclusions[], depth }`.

    See module HAZARD-STOP-NOTE on `depth` type.
    """

    model_config = ConfigDict(extra="forbid")

    scope_refs: List[str] = Field(
        default_factory=list,
        description="Estate slice refs (breadth). v3 §3.1.",
    )
    exclusions: List[str] = Field(
        default_factory=list,
        description="Excluded refs (breadth). v3 §3.1.",
    )
    depth: str = Field(
        ..., min_length=1,
        description="Extraction/reasoning depth. v3 §3.1 semantic; scalar "
                    "type pending owner narrowing per module HAZARD-STOP-NOTE.",
    )


class Output(BaseModel):
    """v3 §3.2 verbatim shape: `output: { form, consumer, grain, standard }`.

    `standard` reuses `DefensibilityFloor` from v0 (same semantic role).
    """

    model_config = ConfigDict(extra="forbid")

    form: OutputForm
    consumer: OutputConsumer
    grain: OutputGrain
    standard: DefensibilityFloor = Field(default_factory=DefensibilityFloor)


class Envelope(BaseModel):
    """v3 §3.2 envelope block. See module HAZARD-STOP-NOTES on scalar-type
    fields (`budget`, `scope_ceiling`) and open-shape fields
    (`availability_snapshot`, `floor_feasibility`).
    """

    model_config = ConfigDict(extra="forbid")

    lawful_basis: str = Field(..., min_length=1)
    done_condition: str = Field(..., min_length=1)
    budget: str = Field(..., min_length=1)
    scope_ceiling: str = Field(..., min_length=1)
    availability_snapshot: Dict[str, Any] = Field(default_factory=dict)
    floor_feasibility: Dict[str, Any] = Field(default_factory=dict)
    commissioner: str = Field(..., min_length=1)
    committed_at: str = Field(..., min_length=1, description="ISO-8601 UTC.")


class OperatorShaping(BaseModel):
    """v3 §3.2: `shaping: { agent_assumed_fields[], transcript_ref }`.

    Owner ruling: nested under `shaping.operator` for variant symmetry
    with `commercial.buyer`. Populated only on `work_order` entry.
    """

    model_config = ConfigDict(extra="forbid")

    agent_assumed_fields: List[str] = Field(default_factory=list)
    transcript_ref: str = Field(default="")


class Shaping(BaseModel):
    """v3 §3.2 shaping block, wrapped per owner ruling."""

    model_config = ConfigDict(extra="forbid")

    operator: OperatorShaping = Field(default_factory=OperatorShaping)


class BuyerCommercial(BaseModel):
    """v3 §3.2: `commercial: { quote_ref, price_model_version }`.

    Owner ruling: nested under `commercial.buyer` for variant symmetry
    with `shaping.operator`. Populated only on the buyer path.
    """

    model_config = ConfigDict(extra="forbid")

    quote_ref: str = Field(default="")
    price_model_version: str = Field(default="")


class Commercial(BaseModel):
    """v3 §3.2 commercial block, wrapped per owner ruling."""

    model_config = ConfigDict(extra="forbid")

    buyer: BuyerCommercial = Field(default_factory=BuyerCommercial)


class ObjectiveRequest_v2(BaseModel):
    """v3 §3.2: additive extension of `objective_request@v0`.

    Additive-only relationship: v0 remains byte-identical; v2 is a
    separate frozen contract. Both may co-exist at runtime; dispatch
    logic (Phase 2, NOT this phase) chooses which to accept per
    entry-point discriminator.
    """

    model_config = ConfigDict(extra="forbid")

    entry: ObjectiveEntry
    reach: Reach
    output: Output
    envelope: Envelope
    shaping: Optional[Shaping] = Field(
        default=None,
        description="v3 §3.2: # work_order only.",
    )
    commercial: Optional[Commercial] = Field(
        default=None,
        description="v3 §3.2: # buyer path only.",
    )
    idempotency_key: Optional[str] = Field(
        default=None,
        description="v3 §3.2: # external_request. Also see v3 §7 async contract.",
    )
