"""KnowledgeArtifactV0 — additive frozen contract (Transform Forms, TF-E1 α).

BCR §3.7 annex verbatim shape (`ka.v0`):

    { schema_version: ka.v0,
      nodes: [ { claim_id, claim_text,
                 defensibility: {class, contested: bool},
                 trace_id, provenance: {source_ref} } ],
      edges: [ { from_claim_id, to_claim_id,
                 relation: corroborates | contradicts | retracts } ] }

Owner ruling TF-E1 α (2026-07-08):

    'α. Single top-level KnowledgeArtifactV0, Node/Edge as nested
     sub-models, parity 29→30. The wire is one document (ka.v0);
     one contract is the honest count. β is wire-identical at triple
     the snapshots — ~310 LoC of ceremony for zero external difference.
     γ abandons the discipline on the exact surface external parties
     consume.'

Owner ruling TF-E3 α + condition (2026-07-08):

    'α, one condition: single-source the class vocabulary. Settled
     doctrine (CK-I1 never-a-widening-Literal; registry precedents at
     B-5b/8-EXT/AS). Condition: defensibility_classes.v0.json is seeded
     verbatim from the class vocabulary the production composition path
     emits today and becomes the canonical registry going forward —
     existing frozen contracts stay byte-identical; no second vocabulary
     may diverge from this one. Gate added: registry ⊇ every class the
     live composition path can emit.'

Provenance preservation (Owner Tier-1 line): every KA node carries
`defensibility.class` + `trace_id` inline (mechanism-not-convention).
Structural attestation lives at `test_transform_forms.py::TF-G3`.
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeArtifactNodeDefensibility(BaseModel):
    """Per-node defensibility carrier (BCR §3.7 annex line 222 verbatim shape).

    `class` is a constrained-str per TF-E3 α (never a widening Literal;
    single-sourced from `defensibility_classes.v0.json`).
    """

    model_config = ConfigDict(extra="forbid")

    class_: str = Field(
        ...,
        min_length=1,
        alias="class",
        description="Defensibility class label. Constrained-str per TF-E3 α; "
                    "validated at construction against `defensibility_classes.v0.json` "
                    "by the loader — the JSON registry is the single source of "
                    "vocabulary (governance §6.7 / B-5b Ruling E3 γ precedent).",
    )
    contested: bool = Field(
        ...,
        description="True if the claim is contested per the matrix contested-status stamp.",
    )


class KnowledgeArtifactNodeProvenance(BaseModel):
    """Per-node provenance carrier (BCR §3.7 annex line 224 verbatim shape)."""

    model_config = ConfigDict(extra="forbid")

    source_ref: str = Field(..., min_length=1)


class KnowledgeArtifactNode(BaseModel):
    """One claim in the KA (BCR §3.7 annex line 220-225 verbatim shape).

    Provenance preservation invariant (Owner Tier-1 line): every node
    carries `defensibility.class` + `trace_id` inline. Both are required
    (no `Optional`, no default) — the promise is enforced at contract-
    construction time.
    """

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(..., min_length=1)
    claim_text: str = Field(..., min_length=1)
    defensibility: KnowledgeArtifactNodeDefensibility
    trace_id: str = Field(
        ...,
        min_length=1,
        description="Trace ID inline on each claim — provenance preservation invariant "
                    "(BCR §3.7 line 216 + Owner Tier-1 line 'every claim in a KA "
                    "carries class + trace_id inline').",
    )
    provenance: KnowledgeArtifactNodeProvenance


class KnowledgeArtifactEdge(BaseModel):
    """One edge in the KA (BCR §3.7 annex line 225-226 verbatim shape).

    `relation` is closed at 3 values per BCR §3.7 annex verbatim — a
    Literal here matches the RelationType shape already at
    `contracts/five_rings.py:RelationType`. Widening requires a bless.
    """

    model_config = ConfigDict(extra="forbid")

    from_claim_id: str = Field(..., min_length=1)
    to_claim_id: str = Field(..., min_length=1)
    relation: Literal["corroborates", "contradicts", "retracts"]


class KnowledgeArtifactV0(BaseModel):
    """Knowledge Artifact export (`ka.v0`) — TF-R1 landed per TF-E1 α.

    Single top-level frozen contract with nested sub-models emitted under
    `$defs` in the JSON schema. One snapshot at
    `backend/tests/invariants/knowledge_artifact_v0.contract_snapshot.json`.

    Parity 29 → 30 (this contract is the +1 additive; v0 pre-existing
    snapshots preserved byte-identical).
    """

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["ka.v0"] = Field(
        default="ka.v0",
        description="Wire version tag (BCR §3.7 annex line 220 verbatim). "
                    "Closed Literal — a new schema version requires a new "
                    "frozen contract (`KnowledgeArtifactV1`).",
    )
    nodes: List[KnowledgeArtifactNode]
    edges: List[KnowledgeArtifactEdge]
