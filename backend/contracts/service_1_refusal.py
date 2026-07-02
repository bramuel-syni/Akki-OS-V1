"""Service1Refusal@v0 — governed refusal envelope for Service 1 (A2 frozen).

14th frozen contract. Additive to the 13 pre-A2 frozen contracts; no
mutation of `NormalizedUnit`, `DefensibilityRing`, or any other prior
freeze.

§-anchors:
  * `RMS_Interface_Specification.md` §183-210 — refusal is a first-class
    result; behavioural table lists `asked / supported / to_raise`.
  * `RMS_Interface_Specification.md` §201 — `asked: <objective + required
    floor, in plain terms>`.
  * `RMS_Interface_Specification.md` §186-190 + §202-203 — `supported: <the
    class the evidence supports, e.g. 'recorded statement'>`.
  * `RMS_Interface_Specification.md` §204-205 — `to_raise: <what would
    lift it: corroboration / accountable source>`. Content categories, not
    verbatim strings — A2 HAZARD-STOP (f) check confirmed source
    prescribes categories only.
  * `RMS_UX_Architecture_Specification.md` §240-256 — refusal-below-floor
    as a visible, explained event.

Doctrinal notes:
  * `outcome: Literal["refused"]` is the load-bearing discriminator that
    distinguishes a governed refusal from FastAPI's default
    `RequestValidationError` (which has `detail: list`, no `outcome`).
    The frontend keys on `body.outcome === "refused"`, never on
    structural inference over the shape of `detail`.
  * `supported_class` is `Optional[DefensibilityClass]` because the
    two pre-composition refusals (`no_defensibility_floor`,
    `no_lawful_basis`) fire BEFORE any composition — there is no
    aggregate class to report and honesty forbids fabricating one.
  * For `composition_below_floor`, `supported_class` is the `max` over
    the input units' per-unit Ring-5-governed `defensibility_class`
    values — reading, not recomputing. See A2 D6a in
    `BUILD_JOURNAL.md`.

Snapshot invariant:
  `tests/invariants/service_1_refusal.contract_snapshot.json`
  compared in `tests/invariants/test_service_1_refusal_envelope.py`.
  Any drift fails CI (Operating Protocol §1.7).
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.five_rings import DefensibilityClass


class Service1Refusal(BaseModel):
    """Flat governed-refusal envelope emitted by `POST /api/service_1/run`."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    outcome: Literal["refused"] = Field(
        default="refused",
        description=(
            "Discriminator: distinguishes a governed refusal from a "
            "validation-422 body (which has detail: list, no outcome). "
            "Frontend keys on body.outcome === 'refused'."
        ),
    )
    reason: str = Field(
        ...,
        description=(
            "Refusal reason code. One of: no_defensibility_floor | "
            "no_lawful_basis | composition_below_floor."
        ),
    )
    run_id: str = Field(..., description="Run correlation ID.")
    trace_id: str = Field(..., description="Trace correlation ID.")
    asked: str = Field(
        ...,
        description=(
            "Plain-language objective + required floor. "
            "See RMS_Interface_Specification.md §201."
        ),
    )
    supported_class: Optional[DefensibilityClass] = Field(
        default=None,
        description=(
            "Highest defensibility class the input evidence supports "
            "(max over per-unit Ring-5-governed defensibility_class "
            "values). None for pre-composition refusals where no "
            "aggregate has been computed. "
            "See RMS_Interface_Specification.md §186-190, §202-203."
        ),
    )
    what_would_raise_it: str = Field(
        ...,
        description=(
            "Actor-appropriate hint on what would raise support to the "
            "requested floor. Category anchors: corroboration / "
            "accountable source. "
            "See RMS_Interface_Specification.md §204-205, "
            "RMS_UX_Architecture_Specification.md §247."
        ),
    )
