"""Five Rings — RMS Normalized Tier schema (G0 freeze).

Spec authority: RMS Product & Engineering Spec v2.0 §5 (Normalized Tier).

The Normalized Tier is *the* critical seam of the RMS engine: every Layer-D
primitive reads from here, no Service ever re-implements engine logic, and
the rings decouple modality from product. Spec §4.4: "normalize all
modality outputs into one modality-neutral representation and build the
five metadata rings".

Five rings per spec:
  1. Provenance       (§5.2) — deterministic, always present.
  2. Signal           (§5.3) — Solva-judged depth, modality-native dimensions.
  3. Relational       (§5.4) — corroborates / contradicts / retracts edges.
  4. Re-extraction Handle (§5.5) — deterministic raw pointer + model fingerprint.
  5. Defensibility    (§5.6) — class + score_vector + matrix_rule_ref.

Multimodal authoring discipline (G0 brief): every field below must be able
to carry audio / video / image / text cases without forcing a text-only
shape. Where a field is necessarily modality-specific, the parent envelope
carries `modality` and the child fields are nullable / extensible.

Freeze contract: this Pydantic model's `model_json_schema()` is snapshotted
to `tests/invariants/five_rings.contract_snapshot.json` and an invariant
test fails on any drift. Bumping the schema requires re-blessing the
snapshot in code review.

Cousin substrate (pattern only): the freeze-via-snapshot discipline is
ported from /reference/akki-legacy/backend/tests/invariants/test_invariant_contract_snapshots.py.
The ring schemas themselves are net-new — the cousin has 116 ad-hoc
provenance envelopes but no canonical normalized tier.
"""
from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ---------------------------------------------------------------------------
# Shared enums.
# ---------------------------------------------------------------------------
class Modality(str, Enum):
    """What kind of raw bytes were the source for this unit.

    Spec §4.3: "parallel per-modality perception pipelines". This enum is
    the modality-aware seam between Layer A (Retrieve) and Layer B
    (Perceive). New modalities require an explicit enum extension AND a
    snapshot bless.
    """

    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    IMAGE = "image"
    # Composite is reserved for units whose perception was joint across
    # modalities (e.g. video frame + audio segment co-perceived).
    COMPOSITE = "composite"


class DefensibilityClass(str, Enum):
    """Spec §5.6: `fact | utterance | non_factual`.

    *fact*        — the unit asserts something the matrix permits as fact.
    *utterance*   — someone said it; the system stands by the saying, not
                    the substance.
    *non_factual* — opinion / interpretation / rhetorical content.
    """

    FACT = "fact"
    UTTERANCE = "utterance"
    NON_FACTUAL = "non_factual"


class RelationType(str, Enum):
    """Spec §5.4: edge taxonomy. Closed at G0; extension requires bless."""

    CORROBORATES = "corroborates"
    CONTRADICTS = "contradicts"
    RETRACTS = "retracts"


# ---------------------------------------------------------------------------
# Ring 1 — Provenance.
# ---------------------------------------------------------------------------
class ProvenanceRing(BaseModel):
    """Spec §5.2: deterministic, always present.

    Fields:
      * source_ref          — file/feed pointer the raw bytes came from
      * modality            — which modality this unit was perceived from
      * locator             — modality-native locator (page+span for text,
                              t_start_ms/t_end_ms for audio/video, bbox
                              for image). Carried as a free dict so each
                              modality can declare its own shape; the
                              schema does not constrain content here.
      * speaker_or_author   — attributed person/org if known; None if
                              perception couldn't attribute.
      * context             — free text describing the surrounding
                              context (programme title, file purpose,
                              segment label …).
    """

    model_config = ConfigDict(extra="forbid")

    source_ref: str = Field(
        ..., description="Stable pointer to the source file or feed slice."
    )
    modality: Modality = Field(
        ..., description="Which modality this unit was perceived from."
    )
    locator: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Modality-native locator. Examples: text → {page:int, span:[int,int]}; "
            "audio/video → {t_start_ms:int, t_end_ms:int}; image → {bbox:[x,y,w,h]}."
        ),
    )
    speaker_or_author: Optional[str] = Field(
        default=None,
        description="Attributed person or organisation. Null if not attributable.",
    )
    context: Optional[str] = Field(
        default=None,
        description="Free-text surrounding context: programme, segment label, file purpose.",
    )


# ---------------------------------------------------------------------------
# Ring 2 — Signal.
# ---------------------------------------------------------------------------
class SignalRing(BaseModel):
    """Spec §5.3: Solva-judged depth; modality-native dimensions.

    G0 declares the *shape*; the catalogue of valid dimension keys per
    modality is extensible. The Qualification Matrix and the Solva depth
    governor will, at G1, restrict which dimension keys are recognised
    per modality. At G0, dimensions are a free dict.

    Examples:
      * audio   → {affect: float, prosody: float, vocal_emphasis: float}
      * text    → {hedge_density: float, attribution_density: float}
      * image   → {salience: float, occlusion: float}

    `depth_judged` is the Solva stamp — only Solva (G1) writes this field.
    TODO[G1]: enforce a catalogue per modality. Currently free.
    """

    model_config = ConfigDict(extra="forbid")

    dimensions: Dict[str, float] = Field(
        default_factory=dict,
        description="Modality-native signal dimensions, key → numeric value.",
    )
    depth_judged: bool = Field(
        default=False,
        description="True iff Solva has judged this unit's signal depth.",
    )
    depth_notes: Optional[str] = Field(
        default=None,
        description="Optional Solva note on depth judgement.",
    )


# ---------------------------------------------------------------------------
# Ring 3 — Relational.
# ---------------------------------------------------------------------------
class RelationalEdge(BaseModel):
    """One edge in the Relational ring graph. Spec §5.4."""

    model_config = ConfigDict(extra="forbid")

    type: RelationType
    target_unit_ref: str = Field(
        ..., description="unit_id of the related NormalizedUnit."
    )
    evidence_ref: Optional[str] = Field(
        default=None,
        description="Optional pointer to the evidence that grounds this edge.",
    )


class RelationalRing(BaseModel):
    """Spec §5.4: edges between units.

    A unit may have zero edges (e.g. an isolated utterance). Empty
    Relational ring is valid and expected at V1 timing.
    """

    model_config = ConfigDict(extra="forbid")

    edges: List[RelationalEdge] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Ring 4 — Re-extraction Handle.
# ---------------------------------------------------------------------------
class ReextractionHandleRing(BaseModel):
    """Spec §5.5: deterministic re-extraction handle.

    Carries enough information to re-run perception against the same raw
    bytes with the same model + params, byte-for-byte reproducible.
    """

    # `model_id` / `model_version` collide with Pydantic's `model_` protected
    # namespace; we silence the warning because the doctrine names carry
    # domain meaning we will not rename.
    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    raw_pointer: str = Field(
        ..., description="Stable storage key for the raw bytes (S3 / local)."
    )
    model_id: str = Field(
        ..., description="Identifier of the perception model used."
    )
    model_version: str = Field(
        ..., description="Version of the perception model used."
    )
    extraction_params: Dict[str, Any] = Field(
        default_factory=dict,
        description="All inputs that materially affect output (sample-rate, "
                    "chunk-size, prompt, thresholds, …).",
    )


# ---------------------------------------------------------------------------
# Ring 5 — Defensibility.
# ---------------------------------------------------------------------------
class ScoreVector(BaseModel):
    """Spec §5.6: five-dimensional defensibility score.

    Each dimension is `float` in [0, 1]. The Solva depth governor (G1)
    writes these; at G0 they are populated by the synthetic fixture or
    left at 0.0 default.
    """

    model_config = ConfigDict(extra="forbid")

    genre_ceiling: float = Field(default=0.0, ge=0.0, le=1.0)
    source_standing: float = Field(default=0.0, ge=0.0, le=1.0)
    corroboration: float = Field(default=0.0, ge=0.0, le=1.0)
    recency: float = Field(default=0.0, ge=0.0, le=1.0)
    contested_status: float = Field(default=0.0, ge=0.0, le=1.0)


class DefensibilityRing(BaseModel):
    """Spec §5.6: class + score_vector + matrix_rule_ref.

    `matrix_rule_ref` ties this unit back to a specific row of the
    governed Qualification Matrix. Solva will refuse to stamp a
    `defensibility_class` higher than the matrix row's ceiling.

    `runtime_mode` flags whether this stamp was produced by the
    declaration baseline (per-feed MEA declaration) or the inference
    overlay (V3-gated content classifier). Until V3 passes, all
    stamps run with `runtime_mode == "declaration_baseline"`.
    """

    model_config = ConfigDict(extra="forbid")

    defensibility_class: DefensibilityClass
    score_vector: ScoreVector = Field(default_factory=ScoreVector)
    matrix_rule_ref: str = Field(
        ..., description="Foreign key into the Qualification Matrix (matrix_rule_id@rev)."
    )
    runtime_mode: Literal["declaration_baseline", "inference_overlay"] = Field(
        default="declaration_baseline",
        description="Spec: declaration baseline by default; inference overlay once V3 passes.",
    )


# ---------------------------------------------------------------------------
# Aggregate.
# ---------------------------------------------------------------------------
class NormalizedUnit(BaseModel):
    """The single modality-neutral unit produced by Layer C.

    Every Layer-D primitive reads from `NormalizedUnit`s. Services 1 and 2
    never see the raw bytes — only this. Spec §4.4 + §5.1.
    """

    model_config = ConfigDict(extra="forbid")

    unit_id: str = Field(
        ..., description="Stable UUID for this unit; cross-referenced by Relational edges."
    )
    provenance: ProvenanceRing
    signal: SignalRing = Field(default_factory=SignalRing)
    relational: RelationalRing = Field(default_factory=RelationalRing)
    reextraction_handle: ReextractionHandleRing
    defensibility: DefensibilityRing

    # Pre-G2 hardening (2026-07-01): enforce extraction_params@v0
    # mandatory keys against the unit's modality. Pydantic
    # `model_validator` decorators do NOT alter `model_json_schema()`,
    # so `five_rings.contract_snapshot.json` stays byte-identical.
    # (Comment lives here as code, NOT in the class docstring — the
    # docstring is read into the JSON schema `description` and would
    # break the frozen snapshot.)
    @model_validator(mode="after")
    def _enforce_extraction_params_v0(self) -> "NormalizedUnit":
        from contracts.extraction_params import validate_extraction_params
        validate_extraction_params(
            self.provenance.modality.value,
            self.reextraction_handle.extraction_params,
        )
        return self
