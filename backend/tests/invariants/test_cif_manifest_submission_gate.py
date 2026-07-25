"""Critic-pass B-1 hard-fail cell family — Binding B-1 discharge.

Owner ruling `docs/rulings/critic_pass_e1_2026_07_25.md` verbatim:

    "Binding B-1 (part of the ruling, test at the execution atomic):
    default_factory=list makes an empty manifest type-legal, which means
    the schema alone no longer enforces 'unmanifested verdict rejects.'
    Therefore the format-gate must reject empty or missing
    manifest_entries at submission for all five verdict types, and this
    lands as a hard-fail cell in the execution atomic — per your own
    A3.1 line, a rail without a hard-fail cell does not exist. The
    default factory is a serialization convenience, never permission."

Coverage · all 5 verdict types per CIF §12 line 152 verbatim:
  * Stage-A proposals    → markdown-document frontmatter path
  * Close reports        → markdown-document frontmatter path
  * Plan objects         → MiningPlan (targeta_plan.py)
  * Training-run records → PerceptionJob_v0 (perception_job_v0.py)
  * Acceptance verdicts  → FeasibilityResult_v0 (feasibility_result.py)

Zero silent exemption. If any verdict type surfaces a legitimate
zero-manifest state at landing, that is a HAZARD-STOP.
"""
from __future__ import annotations

import pytest

from contracts.feasibility_result import (
    FeasibilityResult_v0,
    Freshness,
    ManifestEntry as FRManifestEntry,
)
from contracts.perception_job_v0 import (
    PerceptionJob_v0,
    ManifestEntry as PJManifestEntry,
)
from contracts.targeta_plan import (
    MiningPlan,
    ManifestEntry as TPManifestEntry,
    TargetLocation,
    TargetaFloorSpec,
)
from contracts.five_rings import DefensibilityClass
from contracts.northena_ledger import LedgerArtifactRef
from services.critic_pass.manifest_gate import (
    ALL_VERDICT_TYPES,
    UnmanifestedVerdictError,
    validate_pydantic_verdict_at_submission,
    validate_markdown_frontmatter_at_submission,
)


# ---------------------------------------------------------------------------
# Fixture builders for the 3 Pydantic-typed verdict envelopes.
# Each helper accepts a `manifest_entries` list; callers vary the value
# to test B-1 rejection modes.
# ---------------------------------------------------------------------------

def _mk_mining_plan(manifest_entries=None):
    kwargs = dict(
        plan_id="p-B1",
        mode="portfolio",
        governing_artifact_ref=LedgerArtifactRef(
            artifact_type="portfolio_mandate",
            artifact_id="pm-1",
            version="v1",
        ),
        registry_snapshot_ref="reg-snap-1",
        ordered_targets=[TargetLocation(source_ref="s1", region="r1")],
        defensibility_floor=TargetaFloorSpec(minimum_class=DefensibilityClass.FACT),
        core_baseline_ranking=["s1"],
        generated_at="2026-07-25T00:00:00+00:00",
    )
    if manifest_entries is not None:
        kwargs["manifest_entries"] = manifest_entries
    return MiningPlan(**kwargs)


def _mk_perception_job(manifest_entries=None):
    kwargs = dict(
        job_id="j-B1",
        objective_ref="obj-1",
        trace_lineage="trace-1",
        reextraction_handles=["h1"],
        modality="AUDIO",
        extraction_params_ref="ep-1",
        idempotency_key="idem-1",
        issued_at="2026-07-25T00:00:00+00:00",
    )
    if manifest_entries is not None:
        kwargs["manifest_entries"] = manifest_entries
    return PerceptionJob_v0(**kwargs)


def _mk_feasibility_result(manifest_entries=None):
    kwargs = dict(
        reach_ref="reach-B1",
        freshness=Freshness.UNKNOWN,
        computed_at="2026-07-25T00:00:00+00:00",
    )
    if manifest_entries is not None:
        kwargs["manifest_entries"] = manifest_entries
    return FeasibilityResult_v0(**kwargs)


VERDICT_BUILDERS = [
    ("plan_object", _mk_mining_plan, TPManifestEntry),
    ("training_run", _mk_perception_job, PJManifestEntry),
    ("acceptance_verdict", _mk_feasibility_result, FRManifestEntry),
]


# ---------------------------------------------------------------------------
# Positive test · populated manifest_entries succeeds at submission.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("verdict_type,builder,entry_cls", VERDICT_BUILDERS)
def test_b1_populated_manifest_succeeds_at_submission(verdict_type, builder, entry_cls):
    """B-1 positive · populated manifest_entries passes the submission gate."""
    entry = entry_cls(
        assumption_text="load-bearing assumption A",
        evidence_class="fact",
        flip_condition="if X were false, this flips",
    )
    v = builder([entry])
    # Positive path: gate returns None (no raise).
    validate_pydantic_verdict_at_submission(v)


# ---------------------------------------------------------------------------
# Negative test (hard-fail) · empty manifest_entries=[] REJECTS.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("verdict_type,builder,entry_cls", VERDICT_BUILDERS)
def test_b1_empty_manifest_rejects_at_submission(verdict_type, builder, entry_cls):
    """B-1 hard-fail · empty manifest_entries rejects at submission gate."""
    v = builder([])
    # Confirm the Pydantic constructor allows empty (Owner-ruled default_factory=list).
    assert v.manifest_entries == []
    # Confirm the B-1 gate rejects on submission.
    with pytest.raises(UnmanifestedVerdictError):
        validate_pydantic_verdict_at_submission(v)


# ---------------------------------------------------------------------------
# Negative test (hard-fail) · omitted manifest_entries (default_factory=list) REJECTS.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("verdict_type,builder,entry_cls", VERDICT_BUILDERS)
def test_b1_omitted_manifest_rejects_at_submission(verdict_type, builder, entry_cls):
    """B-1 hard-fail · omitted manifest_entries (default_factory=[]) rejects at gate.

    Owner ruling verbatim: *"The default factory is a serialization
    convenience, never permission."*
    """
    v = builder(manifest_entries=None)  # omitted → default_factory=list produces []
    # Pydantic accepts the omission (default_factory triggers).
    assert v.manifest_entries == []
    # B-1 gate rejects.
    with pytest.raises(UnmanifestedVerdictError):
        validate_pydantic_verdict_at_submission(v)


# ---------------------------------------------------------------------------
# Markdown-document frontmatter path (Stage A + close report).
# ---------------------------------------------------------------------------

MARKDOWN_VERDICT_TYPES = ["stage_a", "close_report"]


@pytest.mark.parametrize("verdict_type", MARKDOWN_VERDICT_TYPES)
def test_b1_markdown_populated_frontmatter_succeeds(verdict_type):
    """B-1 positive · markdown-document frontmatter with populated manifest passes."""
    frontmatter = {
        "manifest_entries": [
            {
                "assumption_text": "load-bearing assumption",
                "evidence_class": "fact",
                "flip_condition": "if X were false, this flips",
            }
        ],
    }
    validate_markdown_frontmatter_at_submission(frontmatter, verdict_type)


@pytest.mark.parametrize("verdict_type", MARKDOWN_VERDICT_TYPES)
def test_b1_markdown_missing_frontmatter_rejects(verdict_type):
    """B-1 hard-fail · markdown missing 'manifest_entries' key rejects."""
    with pytest.raises(UnmanifestedVerdictError):
        validate_markdown_frontmatter_at_submission({}, verdict_type)


@pytest.mark.parametrize("verdict_type", MARKDOWN_VERDICT_TYPES)
def test_b1_markdown_empty_frontmatter_rejects(verdict_type):
    """B-1 hard-fail · markdown with empty 'manifest_entries' rejects."""
    with pytest.raises(UnmanifestedVerdictError):
        validate_markdown_frontmatter_at_submission({"manifest_entries": []}, verdict_type)


@pytest.mark.parametrize("verdict_type", MARKDOWN_VERDICT_TYPES)
def test_b1_markdown_malformed_entry_rejects(verdict_type):
    """B-1 hard-fail · markdown with malformed entry (missing required field) rejects."""
    frontmatter = {
        "manifest_entries": [
            {"assumption_text": "x", "evidence_class": "fact"},  # missing flip_condition
        ]
    }
    with pytest.raises(UnmanifestedVerdictError):
        validate_markdown_frontmatter_at_submission(frontmatter, verdict_type)


@pytest.mark.parametrize("verdict_type", MARKDOWN_VERDICT_TYPES)
def test_b1_markdown_invalid_evidence_class_rejects(verdict_type):
    """B-1 hard-fail · markdown entry with invalid evidence_class rejects."""
    frontmatter = {
        "manifest_entries": [
            {
                "assumption_text": "x",
                "evidence_class": "guess",  # not in {fact, recalled, inferred}
                "flip_condition": "if x then y",
            }
        ]
    }
    with pytest.raises(UnmanifestedVerdictError):
        validate_markdown_frontmatter_at_submission(frontmatter, verdict_type)


# ---------------------------------------------------------------------------
# Enumeration attest · all 5 verdict types covered per CIF §12 line 152.
# ---------------------------------------------------------------------------

def test_b1_all_five_verdict_types_enumerated():
    """CIF §12 line 152 · exactly 5 verdict types · B-1 covers all."""
    assert set(ALL_VERDICT_TYPES) == {
        "stage_a",
        "close_report",
        "plan_object",
        "training_run",
        "acceptance_verdict",
    }
    assert len(ALL_VERDICT_TYPES) == 5


# ---------------------------------------------------------------------------
# Zero silent exemption attest · every verdict type has a hard-fail path.
# ---------------------------------------------------------------------------

def test_b1_zero_silent_exemption_pydantic_types():
    """Owner ruling verbatim: 'no silent exemption'. Every Pydantic verdict
    type raises UnmanifestedVerdictError on empty manifest."""
    for verdict_type, builder, _entry_cls in VERDICT_BUILDERS:
        v = builder([])
        with pytest.raises(UnmanifestedVerdictError):
            validate_pydantic_verdict_at_submission(v)


def test_b1_zero_silent_exemption_markdown_types():
    """Every markdown verdict type raises UnmanifestedVerdictError on missing manifest."""
    for verdict_type in MARKDOWN_VERDICT_TYPES:
        with pytest.raises(UnmanifestedVerdictError):
            validate_markdown_frontmatter_at_submission({}, verdict_type)
