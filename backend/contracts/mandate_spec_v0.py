"""MandateSpec@v0 · frozen wire contract · Parity 33→34 seal at G-13 execution atomic.

Sanction: `docs/rulings/g_13_e1_e2_e3_2026_07_25.md` · SHA
`6abdde0072affbe48758922330aa627ccd25767ac0674f44b1e89a51f49a64f7`
(Owner ruling 2026-07-25 · FINAL · composition (b · a · a) + B-1/B-2/B-3).

Landing anchor: Registry Doctrine §8.1 (e) verbatim: *"far endpoint —
mandates as structured specs from which gates are generated."*

Owner ruling §5.2 (a) verbatim: *"YAML on-disk + MandateSpec@v0 seal.
[...] an enforcement chain of mandate → spec → gate is only auditable
if the middle link is a persisted, SHA-verifiable artifact."*

§0-CAL §23.1 per-line enumeration:
  * `spec_id: str` · rung 1 · deterministic
  * `source_mandate_path: str` · rung 1 · deterministic
  * `source_mandate_sha_256: str` · rung 1 · deterministic
  * `mandate_title: str` · rung 1 · deterministic
  * `gates: List[GateSpec]` · rung 1 · deterministic
  * `generated_at: str` · rung 1 · deterministic
  * `generator_version: str` · rung 1 · deterministic

Standing Rule v3: this contract is FROZEN on landing; evolution is
additive (`MandateSpec_v1` at future seal, same as any contract).
Predecessor 33 contracts remain byte-identical.
"""
from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class GateSpec(BaseModel):
    """One gate declared inside a MandateSpec@v0.

    Sub-shape of MandateSpec@v0 · lives inline (Critic-pass ManifestEntry
    precedent · same substructure discipline as PJManifestEntry /
    TPManifestEntry / FRManifestEntry).
    """

    model_config = ConfigDict(extra="forbid")

    gate_id: str = Field(
        ..., min_length=1,
        description="Deterministic gate identifier · derived from mandate source line-anchor.",
    )
    gate_kind: Literal["rail", "rule", "engine_setting", "registry"] = Field(
        ...,
        description="A3.4 Rules Taxonomy class of the gate this spec generates (S/O/E/D via label).",
    )
    condition_expr: str = Field(
        ..., min_length=1,
        description="Boolean condition (structured expression) that the generated gate enforces.",
    )
    refusal_reason: str = Field(
        ..., min_length=1,
        description="Refusal reason (PROM-S1-refusal-taxonomy-closed compatible) emitted on gate fire.",
    )
    source_line_anchor: str = Field(
        ..., min_length=1,
        description="Verbatim line-anchor citation in the source mandate document.",
    )


class MandateSpec_v0(BaseModel):
    """MandateSpec@v0 · structured spec derived from a mandate document.

    Persisted output written to `docs/generated/mandate_specs/<spec_id>.yaml`
    by `backend/services/far_endpoint/mandate_spec_emitter.py`.
    Consumed by `backend/services/far_endpoint/gate_generator.py` to
    emit executable gate functions at `backend/services/generated_gates/`.

    D-11 round-trip discipline (Owner ruling verbatim): *"an enforcement
    chain of mandate → spec → gate is only auditable if the middle link
    is a persisted, SHA-verifiable artifact"*.
    """

    model_config = ConfigDict(extra="forbid")

    spec_id: str = Field(
        ..., min_length=1,
        description="Deterministic spec identifier · derived from source mandate filename stem.",
    )
    source_mandate_path: str = Field(
        ..., min_length=1,
        description="Relative path to source mandate document (repo-root-relative).",
    )
    source_mandate_sha_256: str = Field(
        ..., min_length=64, max_length=64,
        description="SHA-256 (64-hex) of source mandate at emission time.",
    )
    mandate_title: str = Field(
        ..., min_length=1,
        description="Extracted title of source mandate.",
    )
    gates: List[GateSpec] = Field(
        ...,
        description="Enumerated GateSpec entries · one per identified gate in source mandate.",
    )
    generated_at: str = Field(
        ..., min_length=1,
        description="ISO-8601 UTC timestamp at emitter invocation.",
    )
    generator_version: str = Field(
        default="mandate-spec-emitter-v0",
        description=(
            "Version pin of the emitter that produced this spec · pinned "
            "per engine version per A3.4 Class E discipline."
        ),
    )
