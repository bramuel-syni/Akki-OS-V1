"""Service1Refusal@v1 — superset governed-refusal envelope for Service 1 (EAB-2 A3 seal).

32nd frozen contract (Parity 31→32 seal · EAB-2 execution atomic · 2026-07-24).
Additive to the 31 prior frozen contracts; ZERO mutation of `Service1Refusal@v0`
(at `contracts/service_1_refusal.py`) or any other prior freeze. Standing Rule v3
byte-identity attest on v0 fires this atomic (see `tests/invariants/
test_service_1_refusal_v0_byte_identity_under_eab2.py`).

Sanction:
  * `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md` — Owner ruled
    composition **ε + α + γ** on the three HAZARD-STOP (a) ruling loci
    (SHA `8b074dc152b41ed300d5a7626a2a1bd5aa1213371f6eeeac0a096e12f2d6d4a5`).
  * `docs/stage_a_proposals/eab_2_stage_a.md` §5.1 sub-option (a1) — superset
    envelope · single-writer end-state at close.
  * `docs/requirements/eab_tier1_adoption_spec_v1.1.md` Part IV (A3) — refusal-
    envelope contract contact; three response types distinct at wire; coverage-gap
    class added with descriptor fields.

Composition summary (Owner-authored 2026-07-24 · FINAL):
  * Locus 1 = ε · reason enum = exactly 4 members = the 3 v0 evidential reasons
    + `coverage_gap`. `something-broke` is NOT a refusal class at wire; it routes
    on the fault channel (HTTP 503 + structured detail per
    `PROM-S1-config-defect-fail-loud`). Prove renders on HTTP status + `outcome`
    discriminator. Option η (adding `something_broke` as reason) rejected per
    R-A3.3 + v0 L18-22 doctrinal note.
  * Locus 2 = α · envelope carries `filed_candidate_id` only. `estimated_effort`
    is derived at Prove render via companion GET against Targeta's
    gap-candidate record. NO `estimated_effort` field on the envelope.
  * Locus 3 = γ · NO `queue_action_url` field on the envelope. Prove UI derives
    the Extract Shape-Objective route from `filed_candidate_id` at render.

Envelope shape (11 fields · 4-reason enum · 4-tuple additive set):
  v0-preserved fields (7):
    outcome · reason · run_id · trace_id · asked · supported_class ·
    what_would_raise_it
  v1 additive fields · coverage_gap descriptor set (4):
    estate_region · period · source_class · filed_candidate_id

Failure-mode binding (Owner ruling §2 · tested at EAB-2):
  If the Locus-2 companion read fails, times out, or returns empty: Prove
  renders the `coverage_gap` refusal without the effort line, in refusal
  styling. NEVER degrades to the fault surface; NEVER converts to
  `something-broke`; NEVER blocks the refusal render. The queue action is
  unaffected by companion-read failure — its URL derives from
  `filed_candidate_id` on the envelope itself.

Doctrinal notes (byte-preserved from v0 L18-22):
  * `outcome: Literal["refused"]` is the load-bearing discriminator that
    distinguishes a governed refusal from FastAPI's default
    `RequestValidationError` (which has `detail: list`, no `outcome`).
    The frontend keys on `body.outcome === "refused"`, never on structural
    inference over the shape of `detail`.
  * `supported_class` is `Optional[DefensibilityClass]` because the two
    pre-composition refusals (`no_defensibility_floor`, `no_lawful_basis`)
    AND the coverage-gap refusal all fire BEFORE any composition — there is
    no aggregate class to report and honesty forbids fabricating one.
  * For `composition_below_floor`, `supported_class` is the `max` over the
    input units' per-unit Ring-5-governed `defensibility_class` values —
    reading, not recomputing.
  * On `reason == "coverage_gap"`: `supported_class` is None; the four v1
    additive fields carry the gap descriptor drawn from Mtafiti registry
    vocabulary (`PROM-S2-census-dimension-integrity` + `PROM-S1-honesty-
    grammar-source-labels`); `filed_candidate_id` references the demand-
    signal-side record on Targeta's planning inputs (per §1.2 eligibility-
    wall discipline: filing is demand signal, NOT authorization).
  * On `reason != "coverage_gap"`: all four v1 additive fields are None
    (single-writer end-state posture · Prove suppresses queue button on
    None per Owner ruling Locus 3 = γ).

Snapshot invariant:
  `tests/invariants/service_1_refusal_v1.contract_snapshot.json`
  compared in `tests/invariants/test_service_1_refusal_v1_envelope.py`.
  Any drift fails CI (Operating Protocol §1.7).

§0-CAL §23.1 per-line enumeration: mandatory on this contract module
(backend/contracts/**). Each declarative line below carries a rung
verdict-line in the accompanying attest table at
`tests/invariants/test_service_1_refusal_v1_envelope.py::CAL_23_1_ENUM`.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from contracts.five_rings import DefensibilityClass


class Service1Refusal_v1(BaseModel):
    """Superset governed-refusal envelope emitted by `POST /api/service_1/run` post-EAB-2 seal.

    Single-writer end-state under Owner ruling composition ε + α + γ.
    v0 remains registered (`contracts/service_1_refusal.py`) at byte-identity;
    v0-emitting call-sites transition to v1 same commit as this landing.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    # ── v0-preserved fields (7 · byte-identity to v0 semantics · reason enum extended) ──

    outcome: Literal["refused"] = Field(
        default="refused",
        description=(
            "Discriminator: distinguishes a governed refusal from a "
            "validation-422 body (which has detail: list, no outcome). "
            "Frontend keys on body.outcome === 'refused'. "
            "NEVER assigned on fault-family responses (HTTP 503 fault "
            "envelope routes on `PROM-S1-config-defect-fail-loud` and "
            "carries structured detail with no `outcome`). R-A3.3 fault-"
            "never-dressed-as-refusal preserved verbatim from v0."
        ),
    )
    reason: Literal[
        "no_defensibility_floor",
        "no_lawful_basis",
        "composition_below_floor",
        "coverage_gap",
    ] = Field(
        ...,
        description=(
            "Refusal reason code. Exactly 4 members per Owner ruling "
            "Locus 1 = ε: 3 v0 evidential reasons preserved + coverage_gap "
            "additive. Option η (adding `something_broke`) rejected per "
            "R-A3.3 + v0 doctrinal note L18-22 — faults MUST NOT enter this "
            "envelope; they surface via HTTP 5xx + structured detail."
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
            "values). None for pre-composition refusals AND coverage-gap "
            "refusals where no aggregate has been computed. "
            "See RMS_Interface_Specification.md §186-190, §202-203."
        ),
    )
    what_would_raise_it: str = Field(
        ...,
        description=(
            "Actor-appropriate hint on what would raise support to the "
            "requested floor. Category anchors: corroboration / "
            "accountable source (evidential family) OR gap-close-via-"
            "extraction (coverage_gap family). "
            "See RMS_Interface_Specification.md §204-205, "
            "RMS_UX_Architecture_Specification.md §247."
        ),
    )

    # ── v1 additive fields · coverage_gap descriptor set (4 · Stage A §5.1 4-tuple) ──

    estate_region: Optional[str] = Field(
        default=None,
        description=(
            "Mtafiti registry vocabulary — estate region descriptor for "
            "coverage-gap refusals. None on evidential-family refusals "
            "(single-writer end-state · Prove suppresses gap render on "
            "None). Values MUST draw from the Mtafiti census-dimension "
            "vocabulary per PROM-S2-census-dimension-integrity + "
            "PROM-S1-honesty-grammar-source-labels; hard-coded values "
            "not in the registry are honesty violations."
        ),
    )
    period: Optional[str] = Field(
        default=None,
        description=(
            "Mtafiti registry vocabulary — period descriptor for coverage-"
            "gap refusals. None on evidential-family refusals. Same "
            "registry-vocabulary discipline as `estate_region`."
        ),
    )
    source_class: Optional[str] = Field(
        default=None,
        description=(
            "Mtafiti registry vocabulary — source-class descriptor for "
            "coverage-gap refusals. None on evidential-family refusals. "
            "Same registry-vocabulary discipline as `estate_region`."
        ),
    )
    filed_candidate_id: Optional[str] = Field(
        default=None,
        description=(
            "Targeta gap-candidate FK — referential to the demand-signal-"
            "side record on Targeta's planning inputs (filed by A3.4 gap-"
            "candidate filer; idempotent per (estate_region, period, "
            "source_class) tuple). None on evidential-family refusals. "
            "Per Owner ruling Locus 2 = α: `estimated_effort` is derived "
            "at Prove render via companion GET against this FK. "
            "Per Owner ruling Locus 3 = γ: the Extract Shape-Objective "
            "queue-action URL is derived at Prove render from this FK. "
            "Companion-channel failure NEVER converts the refusal into a "
            "fault render (Owner ruling §2 failure-mode binding · asserted "
            "at Prove module phase Lane 2b as DB-2 gate-cell)."
        ),
    )
