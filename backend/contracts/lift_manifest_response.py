"""LiftManifestEnvelope — response contract for `/api/discipline/lift_manifest`.

New at G5a. Addition, not mutation.

Surfaces:
  * The full lift_manifest.json content (entries + substrate_state markers).
  * Current MANIFEST.md SHA-256s for all 7 filed specs.
  * Rule 2 v2 accounting per closed phase.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LiftEntry(BaseModel):
    """Mirror of `docs/lift_manifest.json` entry shape (kept permissive)."""
    model_config = ConfigDict(extra="allow")

    module: str
    lift_kind: str
    resolves_by: List[str] = Field(default_factory=list)
    transitive_chain: List[str] = Field(default_factory=list)
    cousin_citation: Optional[str] = None
    shape_signature: Optional[str] = None
    notes: Optional[str] = None


class SourceSpecFingerprint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filename: str
    sha256: str


class Rule2Accounting(BaseModel):
    """Rule 2 v2 numbers per closed phase."""
    model_config = ConfigDict(extra="forbid")

    lifted_verifiable: Optional[str] = Field(default="UNKNOWN")
    net_new_discretionary: Optional[str] = Field(default="UNKNOWN")
    mandate_forced_net_new: Optional[str] = Field(default="UNKNOWN")
    overall_ratio: Optional[str] = Field(default="UNKNOWN")
    discretionary_only_ratio: Optional[str] = Field(default="UNKNOWN")
    journal_ref: Optional[str] = None


class LiftManifestEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    manifest_version: str
    manifest_semantics: str
    generated_at: str
    generated_by: str
    substrate_state: Dict = Field(
        ...,
        description="Substrate state markers (e.g., reference_akki_legacy_present).",
    )
    substrate_settled_at: Optional[str] = None
    entries: List[LiftEntry]
    source_specs: List[SourceSpecFingerprint] = Field(
        default_factory=list,
        description="Live-read from docs/mandates/MANIFEST.md at request time.",
    )
    phase_accounting: Dict[str, Rule2Accounting] = Field(
        default_factory=dict,
        description="Rule 2 v2 per phase. Read from docs/rule2_accounting.json.",
    )
