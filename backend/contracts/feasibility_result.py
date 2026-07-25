"""FeasibilityResult v0 — Estate Feasibility Query response envelope
(Phase 1 freeze).

Spec authority: RMS Product & Engineering Spec v3 §5.

**16th frozen contract.** Additive to the 15 pre-Phase-1 frozen contracts;
no mutations. Response envelope for the read-only feasibility query
`POST /api/mtafiti/feasibility`.

v3 §5 verbatim (line 77):
    "A Registry read returning, for a given reach: qualifying volume and
     the defensibility-class distribution. Consumed by both wizard
     variants (grounding every shaping turn) and by admission (the
     warm/fresh fork). Precondition: Registry freshness for the queried
     region — a stale or un-censused region returns `unknown`, never a
     fabricated distribution. Recorded into the envelope as
     `availability_snapshot` + `floor_feasibility` at shaping time."

**Why frozen (D4b precedent):** the response feeds
`ObjectiveRequest_v2.Envelope.availability_snapshot` inside a frozen
envelope, AND shaping-time honesty binds to this field set. Drift here
silently breaks the wizard's grounding — exactly the class of silent
gate-break freezing exists to prevent. The `Freshness` enum carrying the
`unknown`/`stale`/`fresh` honesty semantics is contract behaviour, not
implementation detail.

**Owner ruling on `reach_ref` (Substrate-Drop v2 → Phase 1 dispatch,
2026-07-03):** KEEP. Not general-audit rationale — iterative-shaping
failure mode. The wizard queries per-turn as reach changes, so a frozen
objective could carry a snapshot computed for an earlier turn's reach
beside a later frozen reach. `reach_ref` makes snapshot↔reach
correspondence mechanical instead of assumed. Without it,
`availability_snapshot` is a floating number the DPO's prove-one-run
cannot independently bind.

**Convention anchors:**
  * `computed_at: str` (ISO-8601 UTC) mirrors `MiningPlan.generated_at`
    at `contracts/targeta_plan.py`.
  * `Freshness` three-value enum is v3 §5 verbatim (`unknown`) plus the
    complementary `fresh`/`stale` implied by "Registry freshness".
  * `DefensibilityClass` values in `ClassDistribution` are the canonical
    Ring-5 taxonomy from `contracts/five_rings.py:62-73` (three values:
    fact | utterance | non_factual). NOTE: the UI Spec §2.2 illustrative
    "62% recorded statement · 21% established fact" is ILLUSTRATIVE
    ONLY per §8 binding-copy directive — the code's canonical taxonomy
    is what freezes.

**Loose-as-frozen posture (Standing Owner Disposition):** where v3 §5 is
silent on scalar type (e.g. `snapshot_ref` format beyond "deterministic
pointer"), fields are typed permissively (`str`) following v0's
`objective_text` precedent. Hardening lands as new contract version when
ranges learn.

Freeze contract: `FeasibilityResult_v0.model_json_schema()` snapshotted
to `tests/invariants/feasibility_result.contract_snapshot.json`.
Mechanical parity invariant enforces the source→snapshot bijection at
16 entries post-Phase-1.
"""
from __future__ import annotations

from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class Freshness(str, Enum):
    """v3 §5 three-value freshness signal. Load-bearing for
    honesty-under-absence.

    * `fresh`   — censused; freshness_stamp within the configured
                  threshold. Real qualifying_volume + class_distribution.
    * `stale`   — censused; freshness_stamp past the configured threshold.
                  Real qualifying_volume + class_distribution + snapshot_ref
                  still surfaced (staleness is not un-known — the numbers
                  are real, just old).
    * `unknown` — un-censused (no Registry rows match the reach).
                  qualifying_volume, class_distribution, snapshot_ref all
                  NULL. v3 §5 verbatim: "never a fabricated distribution".
    """

    FRESH = "fresh"
    STALE = "stale"
    UNKNOWN = "unknown"


class ClassDistribution(BaseModel):
    """Per-DefensibilityClass unit count over the qualifying reach.

    Values sourced from `contracts.five_rings.DefensibilityClass` — the
    canonical Ring-5 taxonomy (fact | utterance | non_factual). Sum of
    counts equals `FeasibilityResult_v0.qualifying_volume` when
    freshness != UNKNOWN.
    """

    model_config = ConfigDict(extra="forbid")

    fact: int = Field(
        default=0, ge=0,
        description="Count of units at DefensibilityClass.FACT.",
    )
    utterance: int = Field(
        default=0, ge=0,
        description="Count of units at DefensibilityClass.UTTERANCE.",
    )
    non_factual: int = Field(
        default=0, ge=0,
        description="Count of units at DefensibilityClass.NON_FACTUAL.",
    )


class ManifestEntry(BaseModel):
    """CIF §12 line 152 verbatim manifest entry — shared additive substructure.

    Landed at Critic-pass execution atomic under Owner ruling
    `docs/rulings/critic_pass_e1_2026_07_25.md` (SHA
    `42ca9e0f4605b497394772c83572b1e7c5469e17b2c6f7fa39452ec45992c80a`)
    posture (a1): additive fields on existing frozen contracts.

    ManifestEntry is FROZEN on landing; evolution is additive
    (`ManifestEntry_v1` at future seal, same as any contract).
    """

    model_config = ConfigDict(extra="forbid")

    assumption_text: str = Field(
        ..., min_length=1,
        description="The load-bearing assumption text carried on the verdict.",
    )
    evidence_class: Literal["fact", "recalled", "inferred"] = Field(
        ...,
        description="Honesty-grammar source label per PROM-S1-honesty-grammar-source-labels.",
    )
    flip_condition: str = Field(
        ..., min_length=1,
        description=(
            "The counterfactual probe per CIF §4 verbatim: 'what, if false, "
            "flips this?'"
        ),
    )


class FeasibilityResult_v0(BaseModel):
    """v3 §5 Estate Feasibility Query response envelope.

    Consumed by:
      * Shaping wizard variants — per-turn feasibility grounding
        (v3 §3.3 guard 3).
      * Admission — warm/fresh fork determination (v3 §4 + §71).

    Feeds `ObjectiveRequest_v2.Envelope.availability_snapshot` at
    shaping-time freeze.

    Honesty-under-absence: an un-censused reach returns
    `freshness=UNKNOWN` with `qualifying_volume=None` and
    `class_distribution=None`. Never fabricates a distribution.
    """

    model_config = ConfigDict(extra="forbid")

    reach_ref: str = Field(
        ..., min_length=1,
        description="Deterministic hash of the input Reach (scope_refs, "
                    "exclusions, depth). Correlates response to the query "
                    "that produced it. Enables idempotent replay and "
                    "envelope-level provenance so the DPO's prove-one-run "
                    "can independently bind snapshot↔reach.",
    )
    qualifying_volume: Optional[int] = Field(
        default=None, ge=0,
        description="Unit count matching the reach. NULL iff freshness==UNKNOWN.",
    )
    class_distribution: Optional[ClassDistribution] = Field(
        default=None,
        description="Ring-5 DefensibilityClass → count over the qualifying "
                    "set. NULL iff freshness==UNKNOWN.",
    )
    freshness: Freshness = Field(
        ...,
        description="v3 §5 three-value freshness signal. Load-bearing for "
                    "honesty-under-absence.",
    )
    snapshot_ref: Optional[str] = Field(
        default=None,
        description="Deterministic pointer to the Registry state that "
                    "produced this response (aggregate hash over qualifying "
                    "rows' freshness stamps). NULL iff freshness==UNKNOWN. "
                    "Enables reproducibility + audit correlation.",
    )
    computed_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC. When the response was computed.",
    )
    manifest_entries: List[ManifestEntry] = Field(
        default_factory=list,
        description=(
            "CIF §12 schema-required verdict manifest · load-bearing "
            "assumptions evidence-classed · unmanifested verdict rejects at "
            "submission per B-1 (Owner ruling "
            "docs/rulings/critic_pass_e1_2026_07_25.md · additive-versioning "
            "per PROM-S1-additive-versioning)."
        ),
    )
