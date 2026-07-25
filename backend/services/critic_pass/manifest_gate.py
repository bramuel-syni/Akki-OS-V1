"""Critic-pass B-1 hard-fail manifest submission gate.

Owner ruling `docs/rulings/critic_pass_e1_2026_07_25.md` verbatim:

    "Binding B-1 (part of the ruling, test at the execution atomic):
    default_factory=list makes an empty manifest type-legal, which means
    the schema alone no longer enforces 'unmanifested verdict rejects.'
    Therefore the format-gate must reject empty or missing
    manifest_entries at submission for all five verdict types, and this
    lands as a hard-fail cell in the execution atomic — per your own
    A3.1 line, a rail without a hard-fail cell does not exist. The
    default factory is a serialization convenience, never permission.
    If any verdict type has a legitimate zero-manifest state, that is a
    HAZARD-STOP, not a silent exemption."

CIF §12 line 152 verbatim: *"Manifests: schema-required fields on every
verdict-bearing artifact (Stage As, close reports, plan objects,
training-run records, acceptance verdicts); an unmanifested verdict
rejects at submission — the standing format-gate pattern, form only."*

QA-2 (Critic Seam v1.0 §8 verbatim): *"the format gate — RV-4
schema-completeness is single hard gate; form never substance."*
"""
from __future__ import annotations

from typing import Any, Dict, Literal

from contracts.feasibility_result import FeasibilityResult_v0
from contracts.perception_job_v0 import PerceptionJob_v0
from contracts.targeta_plan import MiningPlan


VerdictType = Literal[
    "stage_a",
    "close_report",
    "plan_object",
    "training_run",
    "acceptance_verdict",
]

# All five verdict types per CIF §12 line 152 verbatim.
ALL_VERDICT_TYPES: tuple[str, ...] = (
    "stage_a",
    "close_report",
    "plan_object",
    "training_run",
    "acceptance_verdict",
)


class UnmanifestedVerdictError(ValueError):
    """B-1 hard-fail — verdict submitted without a populated manifest.

    Owner ruling: *"an unmanifested verdict rejects at submission — the
    standing format-gate pattern, form only."*
    """


def validate_pydantic_verdict_at_submission(
    verdict: MiningPlan | PerceptionJob_v0 | FeasibilityResult_v0,
) -> None:
    """B-1 hard-fail gate for Pydantic-typed verdict envelopes.

    Rejects empty or missing manifest_entries at submission time. The
    schema constructor allows default_factory=list (Owner-ruled shape) as
    a serialization convenience; this gate is the format-gate that
    enforces the manifest-required rule.

    Raises `UnmanifestedVerdictError` if `manifest_entries` is empty.
    """
    entries = getattr(verdict, "manifest_entries", None)
    if entries is None:
        raise UnmanifestedVerdictError(
            f"B-1 hard-fail: verdict {type(verdict).__name__!s} missing "
            f"manifest_entries field. CIF §12 line 152: an unmanifested "
            f"verdict rejects at submission."
        )
    if len(entries) == 0:
        raise UnmanifestedVerdictError(
            f"B-1 hard-fail: verdict {type(verdict).__name__!s} has empty "
            f"manifest_entries. CIF §12 line 152: an unmanifested verdict "
            f"rejects at submission. The default factory is a "
            f"serialization convenience, never permission."
        )


def validate_markdown_frontmatter_at_submission(
    frontmatter: Dict[str, Any],
    verdict_type: VerdictType,
) -> None:
    """B-1 hard-fail gate for markdown-document verdicts (Stage A + close report).

    Enforces the same schema-required + fail-closed discipline on the
    markdown-document path (Stage-A proposals · close reports). The
    document frontmatter MUST contain a `manifest_entries` list with at
    least one entry.

    Raises `UnmanifestedVerdictError` if `manifest_entries` is missing or empty.
    """
    if verdict_type not in ALL_VERDICT_TYPES:
        raise ValueError(f"unknown verdict_type {verdict_type!r}")
    entries = frontmatter.get("manifest_entries")
    if entries is None:
        raise UnmanifestedVerdictError(
            f"B-1 hard-fail: markdown {verdict_type} missing "
            f"'manifest_entries' key in frontmatter. CIF §12 line 152: "
            f"an unmanifested verdict rejects at submission."
        )
    if not isinstance(entries, list) or len(entries) == 0:
        raise UnmanifestedVerdictError(
            f"B-1 hard-fail: markdown {verdict_type} has empty "
            f"'manifest_entries' in frontmatter. CIF §12 line 152: an "
            f"unmanifested verdict rejects at submission."
        )
    # Every entry must carry the three schema-required fields per
    # ManifestEntry shape (assumption_text · evidence_class · flip_condition).
    valid_evidence_classes = {"fact", "recalled", "inferred"}
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise UnmanifestedVerdictError(
                f"B-1 hard-fail: markdown {verdict_type} manifest entry {i} "
                f"is not a mapping; ManifestEntry schema requires "
                f"assumption_text + evidence_class + flip_condition."
            )
        for required_key in ("assumption_text", "evidence_class", "flip_condition"):
            v = entry.get(required_key)
            if not isinstance(v, str) or len(v) == 0:
                raise UnmanifestedVerdictError(
                    f"B-1 hard-fail: markdown {verdict_type} manifest "
                    f"entry {i} missing/empty '{required_key}' field."
                )
        if entry["evidence_class"] not in valid_evidence_classes:
            raise UnmanifestedVerdictError(
                f"B-1 hard-fail: markdown {verdict_type} manifest entry "
                f"{i} evidence_class {entry['evidence_class']!r} not in "
                f"{sorted(valid_evidence_classes)}."
            )
