"""Mtafiti invariants — mandate §17 + §14.

Test file consolidates the six §14 test obligations plus additional
G4-invariants derived from the closed-seam doctrine (V3 overlay,
source-standing placeholder flags, freshness L1/L2, no-deletion-path).

Structural + import-boundary tests (no MongoDB); async persistence
tests moved to a distinct file where MongoDB is available.
"""
from __future__ import annotations

import inspect
import json
from pathlib import Path

import pytest

from contracts.five_rings import (
    DefensibilityClass,
    DefensibilityRing,
    Modality,
    NormalizedUnit,
    ProvenanceRing,
    ReextractionHandleRing,
    RelationalRing,
    ScoreVector,
    SignalRing,
)
from contracts.mtafiti_registry import (
    FreshnessStamp,
    MtafitiRegistryRecord,
    MtafitiScoreVector,
    SourceStanding,
)
from services.mtafiti import (
    census,
    declaration,
    inference,
    measure,
    registry,
    source_standing,
    v3_overlay,
    verdict,
)
from services.mtafiti.v3_overlay import V3Result, V3Thresholds
from tests.invariants._ep_v0_fixtures import ep_v0

SNAPSHOT_PATH = (
    Path(__file__).parent / "mtafiti_registry_record.contract_snapshot.json"
)


def _test_unit(feed_id: str = "feed_a",
               source_ref: str = "synthetic://feed_a/test.raw",
               modality: Modality = Modality.TEXT) -> NormalizedUnit:
    ctx = json.dumps({
        "programme": "test",
        "feed_id": feed_id,
        "logged_date": "2026-07-01T12:00:00Z",
        "structural_signature": "0123456789abcdef",
        "author_labels": {
            "claim_genre": "news_anchor_read",
            "source_standing": "primary_recorded",
            "contested_status": "uncontested",
        },
    })
    return NormalizedUnit(
        unit_id="test-1",
        provenance=ProvenanceRing(
            source_ref=source_ref, modality=modality,
            locator={}, speaker_or_author="anchor", context=ctx,
        ),
        signal=SignalRing(dimensions={}, depth_judged=False),
        relational=RelationalRing(),
        reextraction_handle=ReextractionHandleRing(
            raw_pointer=source_ref, model_id="test-model", model_version="v0",
            extraction_params=ep_v0(modality),
        ),
        defensibility=DefensibilityRing(
            defensibility_class=DefensibilityClass.FACT,
            score_vector=ScoreVector(),
            matrix_rule_ref="news_anchor_read.primary_recorded",
            runtime_mode="declaration_baseline",
        ),
    )


# ------- §14 test obligation #1 — inference emits no verdict ---------------
def test_inference_emits_no_verdict_structural():
    """Structural: `services/mtafiti/inference.py` has NO import of
    `verdict.py` and never constructs a `DefensibilityClass`."""
    src_path = (Path(__file__).parent.parent.parent / "services" / "mtafiti"
                / "inference.py")
    lines = src_path.read_text(encoding="utf-8").splitlines()
    # Consider only real import statements (not docstring / comment prose)
    import_lines = [
        line.strip() for line in lines
        if line.strip().startswith(("import ", "from "))
    ]
    for line in import_lines:
        assert "verdict" not in line, (
            f"inference.py has import touching verdict: {line!r} — violates §17 #3"
        )
    src = src_path.read_text(encoding="utf-8")
    assert "DefensibilityClass(" not in src, (
        "inference.py constructs DefensibilityClass — violates §17 #3"
    )


def test_inference_returns_only_detections():
    unit = _test_unit()
    det = inference.detect(unit, estate_index=None)
    assert isinstance(det, inference.Detections)
    assert not hasattr(det, "defensibility_class"), (
        "Detections must never carry a defensibility_class field"
    )


# ------- §14 #2 — verdict is Matrix lookup, carries matrix_rule_ref ---------
def test_verdict_is_matrix_lookup():
    v = verdict.assign_verdict("news_anchor_read", "primary_recorded",
                               verdict.default_handle())
    assert v.matrix_rule_ref, "verdict must carry a matrix_rule_ref"
    assert "@" in v.matrix_rule_ref, "matrix_rule_ref should be `<id>@<rev>`"
    assert v.defensibility_class in ("fact", "utterance", "non_factual")


def test_verdict_unmapped_cell_fails_toward_caution():
    v = verdict.assign_verdict("unknown_genre", "unknown_context",
                               verdict.default_handle())
    assert v.defensibility_class == "non_factual"
    assert v.matrix_rule_ref == "unmapped_cell"


# ------- §14 #3 — baseline stands alone (V3 overlay dark) --------------------
def test_baseline_stands_alone_when_overlay_not_admitted():
    """§17 invariant #2: baseline always available and stands alone."""
    unit = _test_unit()
    record = registry.compose_record(unit)
    assert record.defensibility_runtime_mode == "declaration_baseline"
    # Detections contributions zeroed when overlay closed
    assert record.defensibility_measure.attachment == 0.0
    assert record.defensibility_measure.corroboration == 0.0
    # Baseline still populated
    assert record.defensibility_measure.source_standing is not None


# ------- §14 #4 — census objective-blind ------------------------------------
def test_census_signature_takes_no_objective():
    sig = inspect.signature(census.census)
    params = list(sig.parameters.keys())
    for name in params:
        assert "objective" not in name.lower(), (
            f"census signature contains an objective param ({name}) — violates §17 #1, #9"
        )


def test_census_output_is_objective_blind():
    """Same units yield same census output regardless of any downstream
    objective — the function has no objective input to consult."""
    unit = _test_unit()
    output_a = list(census.census([unit]))
    output_b = list(census.census([unit]))
    assert output_a == output_b


# ------- §14 #5 — Registry record frozen (snapshot) --------------------------
def test_registry_record_contract_frozen():
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    actual = MtafitiRegistryRecord.model_json_schema()
    assert json.dumps(actual, indent=2, sort_keys=True) == \
           json.dumps(expected, indent=2, sort_keys=True), (
        "MtafitiRegistryRecord schema drifted; re-bless snapshot in review "
        "if intentional."
    )


# ------- §14 #6 — freshness re-measures only affected region -----------------
def test_freshness_l1_present_on_new_records():
    unit = _test_unit()
    record = registry.compose_record(unit)
    assert record.freshness_stamp.logged_date, "L1 logged_date must be recorded"


def test_freshness_l2_present_when_fixture_provides():
    unit = _test_unit()
    record = registry.compose_record(unit)
    # Fixture-embedded structural_signature at G4 v0
    assert record.freshness_stamp.structural_signature is not None
    assert len(record.freshness_stamp.structural_signature) == 16


def test_freshness_detects_scoped_change():
    """§17 #8: L2 delta detects a change; only the changed source is
    returned. Not the whole estate."""
    unit_a = _test_unit(source_ref="synthetic://a.raw")
    unit_b_v1 = _test_unit(source_ref="synthetic://b.raw")
    # Simulate prior Registry state:
    prior = [
        registry.compose_record(unit_a).model_dump(mode="json"),
        registry.compose_record(unit_b_v1).model_dump(mode="json"),
    ]
    # Now b changes (structural sig would differ if content changed;
    # simulate by mutating the pointer):
    unit_b_v2 = _test_unit(source_ref="synthetic://b.raw")
    # Overwrite the fixture-embedded structural_signature to force a
    # delta on unit b:
    new_ctx = json.loads(unit_b_v2.provenance.context or "{}")
    new_ctx["structural_signature"] = "deadbeefcafebabe"
    unit_b_v2 = unit_b_v2.model_copy(update={
        "provenance": unit_b_v2.provenance.model_copy(update={
            "context": json.dumps(new_ctx)
        })
    })
    stale = registry.detect_stale_records(prior, [unit_a, unit_b_v2])
    assert stale == ["synthetic://b.raw"], (
        f"freshness should return only affected region; got {stale}"
    )


# ------- V3 overlay closed seam ----------------------------------------------
def test_v3_overlay_returns_false_when_thresholds_none():
    assert v3_overlay.overlay_admitted(None) is False
    assert v3_overlay.overlay_admitted(None, V3Result(1.0, 1.0, 1.0)) is False


def test_v3_overlay_runtime_mode_defaults_to_declaration_baseline():
    assert v3_overlay.runtime_mode(None) == "declaration_baseline"


def test_v3_overlay_admits_when_thresholds_met():
    """The closed-seam pattern MUST also work when config lands.
    Synthetic threshold + synthetic result → admitted."""
    t = V3Thresholds(fact_precision=0.8, genre_accuracy=0.8, inter_annotator_floor=0.7)
    ok = V3Result(fact_precision=0.9, genre_accuracy=0.9, inter_annotator_kappa=0.75)
    assert v3_overlay.overlay_admitted(t, ok) is True
    assert v3_overlay.runtime_mode(t, ok) == "overlay"


def test_v3_overlay_kappa_floor_gates_before_accuracy():
    """§12 note: inter-annotator kappa >= floor BEFORE accuracy is computed."""
    t = V3Thresholds(fact_precision=0.5, genre_accuracy=0.5, inter_annotator_floor=0.7)
    below_kappa = V3Result(fact_precision=1.0, genre_accuracy=1.0, inter_annotator_kappa=0.5)
    assert v3_overlay.overlay_admitted(t, below_kappa) is False


# ------- MEA source-standing placeholder flags -------------------------------
def test_source_standing_placeholder_flags():
    """User directive (4): every G4 entry is synthetic_placeholder + non-editorial.

    When MEA lands a real table, THIS TEST FAILS naturally — forcing the
    deployment ceremony to update the invariant alongside the real table.
    Correct behaviour.
    """
    table = source_standing.table()
    assert len(table) > 0, "placeholder table must not be empty (breaks plumbing)"
    for feed_id, entry in table.items():
        assert entry.synthetic_placeholder is True, (
            f"{feed_id}: placeholder flag is False — real table detected? "
            "Re-bless this invariant and update the deployment ceremony."
        )
        assert entry.editorial_authority is False, (
            f"{feed_id}: editorial_authority is True — usurps MEA authority "
            "at G4. Real table swap should reset this via config."
        )


def test_source_standing_covers_fixture_feed_ids():
    """Placeholder table must cover every fixture feed_id (else plumbing breaks)."""
    fixture_path = (Path(__file__).parent.parent.parent
                    / "services" / "data_source" / "synthetic_assets"
                    / "rms_adversarial_v1" / "fixture.json")
    fx = json.loads(fixture_path.read_text(encoding="utf-8"))
    fixture_feeds = set()
    for unit in fx["units"]:
        ctx = json.loads(unit["provenance"]["context"])
        fixture_feeds.add(ctx.get("feed_id", "unknown"))
    covered = source_standing.feed_ids()
    missing = fixture_feeds - covered
    assert not missing, (
        f"placeholder table missing feed_ids: {missing}. This breaks "
        "declaration baseline plumbing."
    )


# ------- Composition-alone completeness (baseline + census + declaration) ---
def test_declaration_baseline_complete_alone_across_fixture():
    """§14 obligation #3: census + declaration produce a valid Registry
    without any V3 overlay contribution. Run against the on-disk fixture."""
    fixture_path = (Path(__file__).parent.parent.parent
                    / "services" / "data_source" / "synthetic_assets"
                    / "rms_adversarial_v1" / "fixture.json")
    fx = json.loads(fixture_path.read_text(encoding="utf-8"))
    for u_dict in fx["units"][:5]:  # first 5 units — smoke coverage
        unit = NormalizedUnit.model_validate(u_dict)
        record = registry.compose_record(unit)  # v3 thresholds None → closed
        assert isinstance(record, MtafitiRegistryRecord)
        assert record.defensibility_runtime_mode == "declaration_baseline"
        assert record.defensibility_measure.source_standing in SourceStanding
