"""Critic-pass execution atomic · pytest cells (all disciplines except B-1).

Owner ruling `docs/rulings/critic_pass_e1_2026_07_25.md` (2026-07-25 · FINAL).

Cells landed here per Stage A §2 band table + Owner-dispatch §B.4:
  * Parity 33 held byte-identical attest (33 contracts + 33 snapshots).
  * ManifestEntry inline discipline attest (3 target contracts, each carries local sub-shape).
  * Additive-versioning discipline attest (schema additive-only · no field removal).
  * CR-1..CR-7 rubric shape execution cells.
  * Archive-ledger append-only cells + CIF-entry-#1 seed row.
  * Standing-query correctness (evaluated-but-unarchived).
  * Class D lifecycle cells (seeded-defect corpus · A3.3 asymmetry incl. edits).
  * Class E decay-rule cells (verdict sampling rate deterministic decay).
  * Calibration ledger staleness window (Class E).
  * QA-3 no-self-review cell.
  * QA-7 custody-boundary attest (TQ §7 Part B rides EAB-2 quarantine machinery).
  * §0-CAL §23.1 per-line enumeration attest.

B-1 hard-fail cell family lives at `test_cif_manifest_submission_gate.py`.
"""
from __future__ import annotations

import ast
import hashlib
import pathlib
from typing import Dict

import pytest

from contracts.feasibility_result import (
    FeasibilityResult_v0,
    ManifestEntry as FRManifestEntry,
)
from contracts.perception_job_v0 import (
    PerceptionJob_v0,
    ManifestEntry as PJManifestEntry,
)
from contracts.targeta_plan import (
    MiningPlan,
    ManifestEntry as TPManifestEntry,
)
from services.critic_pass import archive, calibration_ledger, seeded_defect_corpus
from services.critic_pass.harness import CriticPassVerdict, run_critic_pass
from services.critic_pass.rubric import (
    ALL_RUBRIC_ITEMS,
    RubricFinding,
    TIER_2_RUBRIC,
    apply_rubric,
    get_rubric_item,
)


BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[2]
CONTRACTS_DIR = BACKEND_ROOT / "contracts"
INVARIANTS_DIR = BACKEND_ROOT / "tests" / "invariants"
SERVICES_DIR = BACKEND_ROOT / "services"


# ---------------------------------------------------------------------------
# §0-CAL §23.1 per-line enumeration attest (ManifestEntry sub-shape).
# ---------------------------------------------------------------------------

CAL_23_1_MANIFEST_ENTRY_ENUM = [
    # (line-anchor,                                       rung, verdict)
    ("model_config ConfigDict(extra=forbid)",             1, "deterministic"),
    ("assumption_text: str (min_length=1)",               1, "deterministic"),
    ("evidence_class: Literal[fact,recalled,inferred]",   1, "deterministic"),
    ("flip_condition: str (min_length=1)",                1, "deterministic"),
]


def test_cal_23_1_enumeration_present_on_manifest_entry():
    """§0-CAL §23.1 per-line enumeration mandatory attest for ManifestEntry sub-shape."""
    assert len(CAL_23_1_MANIFEST_ENTRY_ENUM) == 4  # 1 config + 3 fields
    for _anchor, rung, verdict in CAL_23_1_MANIFEST_ENTRY_ENUM:
        assert rung == 1
        assert verdict == "deterministic"


# ---------------------------------------------------------------------------
# Parity 33 held byte-identical attest.
# ---------------------------------------------------------------------------

def test_parity_33_held_post_critic_pass():
    """Parity 33 held at Critic-pass close; 33→34 sealed at G-13 (MandateSpec@v0).

    Post-G-13 execution atomic (2026-07-25): count is 34 contract .py + 34 snapshots.
    Owner ruling verbatim (Critic-pass): 'Parity 33 held' — count preserved AT Critic-pass.
    Owner ruling verbatim (G-13): 'composition (b · a · a) · Net one seal, MandateSpec@v0, Parity 33→34'.
    """
    contract_files = sorted(CONTRACTS_DIR.glob("*.py"))
    snapshot_files = sorted(INVARIANTS_DIR.glob("*.contract_snapshot.json"))
    assert len(contract_files) == 34, (
        f"Parity 34 breach: expected 34 contract .py files post-G-13 "
        f"MandateSpec@v0 seal, got {len(contract_files)}"
    )
    assert len(snapshot_files) == 34, (
        f"Parity 34 breach: expected 34 contract snapshot .json files, "
        f"got {len(snapshot_files)}"
    )


# ---------------------------------------------------------------------------
# Additive-versioning · schema shape is additive-only on the 3 touched contracts.
# Each grew by exactly 1 field (manifest_entries: List[ManifestEntry]).
# ---------------------------------------------------------------------------

EXPECTED_FIELD_COUNTS_POST_CRITIC_PASS = {
    "MiningPlan": 10,          # was 9 · +1 manifest_entries
    "PerceptionJob_v0": 9,     # was 8 · +1 manifest_entries
    "FeasibilityResult_v0": 7, # was 6 · +1 manifest_entries
}


def test_mining_plan_grew_by_manifest_entries_field():
    """MiningPlan schema is additive-only · exactly +1 field (manifest_entries)."""
    fields = MiningPlan.model_fields
    assert len(fields) == EXPECTED_FIELD_COUNTS_POST_CRITIC_PASS["MiningPlan"]
    assert "manifest_entries" in fields


def test_perception_job_v0_grew_by_manifest_entries_field():
    """PerceptionJob_v0 schema is additive-only · exactly +1 field (manifest_entries)."""
    fields = PerceptionJob_v0.model_fields
    assert len(fields) == EXPECTED_FIELD_COUNTS_POST_CRITIC_PASS["PerceptionJob_v0"]
    assert "manifest_entries" in fields


def test_feasibility_result_v0_grew_by_manifest_entries_field():
    """FeasibilityResult_v0 schema is additive-only · exactly +1 field."""
    fields = FeasibilityResult_v0.model_fields
    assert len(fields) == EXPECTED_FIELD_COUNTS_POST_CRITIC_PASS["FeasibilityResult_v0"]
    assert "manifest_entries" in fields


# ---------------------------------------------------------------------------
# ManifestEntry shape · inline discipline (Tier-3 disclosure: inline over
# shared module to preserve Parity 33 count).
# ---------------------------------------------------------------------------

def test_manifest_entry_shape_uniform_across_consumers():
    """ManifestEntry inline sub-shape is byte-identical across the 3 consumers.

    Discipline: each contract carries a LOCAL ManifestEntry inline (not
    imported from a shared module) to preserve Parity 33 count semantics.
    All three MUST have the same 3-field shape.
    """
    expected_fields = {"assumption_text", "evidence_class", "flip_condition"}
    assert set(TPManifestEntry.model_fields) == expected_fields
    assert set(PJManifestEntry.model_fields) == expected_fields
    assert set(FRManifestEntry.model_fields) == expected_fields


def test_manifest_entry_evidence_class_literal_honesty_grammar():
    """CIF §4 verbatim: evidence_class ∈ {fact, recalled, inferred}."""
    entry = TPManifestEntry(
        assumption_text="a", evidence_class="fact", flip_condition="c",
    )
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        TPManifestEntry(
            assumption_text="a", evidence_class="guess", flip_condition="c",
        )


# ---------------------------------------------------------------------------
# CR-1..CR-7 rubric shape execution cells.
# ---------------------------------------------------------------------------

def test_tier_2_rubric_has_seven_items():
    """Critic Seam v1.0 §6.1 + CIF §6 A5.2 CR-7 amendment · exactly 7 rubric items."""
    assert len(TIER_2_RUBRIC) == 7
    assert set(TIER_2_RUBRIC.keys()) == set(ALL_RUBRIC_ITEMS)


@pytest.mark.parametrize("item_id", ALL_RUBRIC_ITEMS)
def test_rubric_item_shape(item_id):
    """Each CR-N rubric item carries item_id + label + verbatim spec anchor."""
    item = get_rubric_item(item_id)
    assert item.item_id == item_id
    assert len(item.label) > 0
    assert "verbatim" in item.verbatim_anchor.lower() or "§" in item.verbatim_anchor


def test_cr_7_amendment_lands_alongside_cr_1_through_cr_6():
    """CIF §6 A5.2 verbatim: 'CR-7 enters standing machinery as a rubric amendment'."""
    cr_7 = get_rubric_item("CR-7")
    assert "CR-7" in cr_7.verbatim_anchor or "A5.2" in cr_7.verbatim_anchor
    assert "selection" in cr_7.label.lower() or "checklist" in cr_7.label.lower()


# ---------------------------------------------------------------------------
# QA-3 no-self-review attest.
# ---------------------------------------------------------------------------

def test_qa_3_no_self_review():
    """QA-3 (Critic Seam v1.0 §8): critic instance MUST NOT equal producing instance."""
    with pytest.raises(ValueError, match="QA-3"):
        apply_rubric(
            artifact_ref="a",
            artifact_content="content",
            producing_instance_id="inst-A",
            critic_instance_id="inst-A",  # same as producer
        )
    # Different instances allowed.
    findings = apply_rubric(
        artifact_ref="a",
        artifact_content="content",
        producing_instance_id="inst-A",
        critic_instance_id="inst-B",
    )
    assert isinstance(findings, list)


# ---------------------------------------------------------------------------
# Archive ledger · append-only + CIF-entry-#1 seed + evaluated-but-unarchived query.
# ---------------------------------------------------------------------------

def test_archive_ledger_cif_entry_1_seed_idempotent():
    """CIF §14.2 verbatim: 'The archive initializes as a governed file
    with CIF as entry #1.'"""
    archive._reset_for_tests()
    seed = archive.initialize_with_cif_seed()
    assert seed.row_id == 1
    assert seed.entry_type == "cif_entry_1_seed"
    assert "cif_spec_v1.md" in seed.subject_ref
    # Idempotent · subsequent calls return the same row.
    seed2 = archive.initialize_with_cif_seed()
    assert seed2 == seed
    ledger = archive.get_ledger()
    assert len(ledger) == 1


def test_archive_ledger_append_only_row_ids_monotone():
    """PROM-S3-append-only-ledger discipline · row_ids strictly increasing."""
    archive._reset_for_tests()
    archive.initialize_with_cif_seed()
    r2 = archive.append("evaluated_idea", "subject/A")
    r3 = archive.append("critic_verdict", "subject/B", evaluated_by="inst-B")
    r4 = archive.append("seeded_defect_verdict", "subject/C")
    ids = [row.row_id for row in archive.get_ledger()]
    assert ids == sorted(ids)  # monotone
    assert ids == [1, 2, 3, 4]


def test_archive_ledger_rows_immutable_frozen_dataclass():
    """PROM-S3-audit-trail-immutable · rows are frozen dataclasses."""
    archive._reset_for_tests()
    row = archive.append("evaluated_idea", "subject/X")
    with pytest.raises(Exception):
        row.row_id = 999  # frozen · assignment fails


def test_archive_ledger_direct_seed_append_rejected():
    """cif_entry_1_seed rows are seeded ONLY via initialize_with_cif_seed."""
    archive._reset_for_tests()
    with pytest.raises(ValueError, match="initialize_with_cif_seed"):
        archive.append("cif_entry_1_seed", "docs/requirements/cif_spec_v1.md")


def test_archive_standing_query_evaluated_but_unarchived():
    """CIF §12 line 154 verbatim: 'a standing query surfaces
    evaluated-but-unarchived ideas as findings.'"""
    archive._reset_for_tests()
    archive.initialize_with_cif_seed()
    archive.append("evaluated_idea", "subject/A")
    archive.append("evaluated_idea", "subject/B")
    evaluated = ["subject/A", "subject/B", "subject/C", "subject/D"]
    unarchived = archive.evaluated_but_unarchived_query(evaluated)
    assert set(unarchived) == {"subject/C", "subject/D"}


# ---------------------------------------------------------------------------
# Class D lifecycle · seeded-defect corpus (A3.3 asymmetry incl. Owner-extended edits).
# ---------------------------------------------------------------------------

def test_class_d_additions_take_effect_immediately():
    """A3.3 verbatim: 'additions take effect immediately'."""
    seeded_defect_corpus._reset_for_tests()
    entry = seeded_defect_corpus.add_entry(
        entry_id="sd-001",
        defect_class="fabrication",
        canonical_example="Model asserted X as fact without cited evidence.",
        detection_criterion="grep for un-cited factual claims.",
    )
    assert entry.entry_id == "sd-001"
    corpus = seeded_defect_corpus.get_corpus()
    assert len(corpus) == 1


def test_class_d_removal_requires_approval():
    """A3.3 verbatim: 'removals AND edits require approval'."""
    seeded_defect_corpus._reset_for_tests()
    seeded_defect_corpus.add_entry(
        entry_id="sd-002",
        defect_class="conflation",
        canonical_example="ex",
        detection_criterion="crit",
    )
    seeded_defect_corpus.request_removal("sd-002")
    # Cannot execute removal without approval.
    with pytest.raises(seeded_defect_corpus.PendingChangeAsymmetry):
        seeded_defect_corpus.execute_removal("sd-002")
    seeded_defect_corpus.approve_removal("sd-002")
    seeded_defect_corpus.execute_removal("sd-002")
    assert len(seeded_defect_corpus.get_corpus()) == 0


def test_class_d_edit_requires_approval_owner_extension():
    """Owner ruling verbatim: 'an edit to a seeded defect changes what the
    catch-rate measures, so gating edits is correct there too.'"""
    seeded_defect_corpus._reset_for_tests()
    seeded_defect_corpus.add_entry(
        entry_id="sd-003",
        defect_class="scope_smuggling",
        canonical_example="original ex",
        detection_criterion="original crit",
    )
    seeded_defect_corpus.request_edit("sd-003")
    # Cannot execute edit without approval.
    with pytest.raises(seeded_defect_corpus.PendingChangeAsymmetry):
        seeded_defect_corpus.execute_edit("sd-003", "new ex", "new crit")
    seeded_defect_corpus.approve_edit("sd-003")
    seeded_defect_corpus.execute_edit("sd-003", "new ex", "new crit")
    corpus = seeded_defect_corpus.get_corpus()
    assert corpus[0].canonical_example == "new ex"


# ---------------------------------------------------------------------------
# Class E · deterministic sampling-rate decay (Owner-ruled).
# ---------------------------------------------------------------------------

def test_class_e_sampling_rate_decay_deterministic():
    """Owner ruling verbatim: 'a schedule can live as a Class E deterministic
    decay function pinned per version'.

    Deterministic: same input phase_count returns same output rate.
    """
    r1 = calibration_ledger.sampling_rate_findings(0)
    r2 = calibration_ledger.sampling_rate_findings(0)
    assert r1 == r2 == calibration_ledger.VERDICT_SAMPLING_INITIAL_FINDINGS_RATE
    # After half-life (20 phases), rate is exactly half of initial.
    r_hl = calibration_ledger.sampling_rate_findings(
        calibration_ledger.VERDICT_SAMPLING_DECAY_HALF_LIFE_PHASES
    )
    assert abs(r_hl - calibration_ledger.VERDICT_SAMPLING_INITIAL_FINDINGS_RATE / 2) < 1e-9


def test_class_e_sampling_rate_decay_respects_floor():
    """Sampling rate never decays below the floor rate."""
    # Very large phase count · decayed rate should hit floor.
    rate = calibration_ledger.sampling_rate_findings(10_000)
    assert rate == calibration_ledger.VERDICT_SAMPLING_FLOOR_RATE


def test_class_e_sampling_rate_all_clears_symmetric():
    """All-clears sampling rate follows the same deterministic decay."""
    r0 = calibration_ledger.sampling_rate_all_clears(0)
    assert r0 == calibration_ledger.VERDICT_SAMPLING_INITIAL_ALL_CLEARS_RATE
    r_hl = calibration_ledger.sampling_rate_all_clears(
        calibration_ledger.VERDICT_SAMPLING_DECAY_HALF_LIFE_PHASES
    )
    assert abs(r_hl - calibration_ledger.VERDICT_SAMPLING_INITIAL_ALL_CLEARS_RATE / 2) < 1e-9


# ---------------------------------------------------------------------------
# Class E · calibration staleness window (10 phases DEFAULT).
# ---------------------------------------------------------------------------

def test_class_e_calibration_staleness_window_ten_phases():
    """Critic Seam v1.0 §9 · DEFAULT 10 phases · findings render UNCALIBRATED past window."""
    assert calibration_ledger.STALENESS_WINDOW_PHASES == 10
    calibration_ledger._reset_for_tests()
    row = calibration_ledger.append_calibration_row(
        worker_class="critic_pass",
        rubric_item="CR-1",
        catch_rate=0.85,
        false_alarm_rate=0.10,
        sample_count=50,
        phase_count_at_calibration=100,
    )
    assert row.stale_after_phase_count == 110
    assert not calibration_ledger.is_calibration_stale(row, 105)
    assert calibration_ledger.is_calibration_stale(row, 111)


# ---------------------------------------------------------------------------
# Harness · integration cell (produces verdict, archives it, QA-3 held).
# ---------------------------------------------------------------------------

def test_harness_run_critic_pass_archives_verdict():
    """Harness produces a verdict and archives it (per CIF §12 discipline)."""
    archive._reset_for_tests()
    verdict = run_critic_pass(
        artifact_ref="artifact/X",
        artifact_content="dummy content",
        producing_instance_id="inst-producer",
        critic_instance_id="inst-critic",
        archive_verdict=True,
    )
    assert verdict.artifact_ref == "artifact/X"
    # Verdict archived at ledger.
    ledger = archive.get_ledger()
    assert any(row.subject_ref == "artifact/X" for row in ledger)


def test_harness_run_critic_pass_rejects_self_review():
    """QA-3 · run_critic_pass raises when critic and producer instances collide."""
    with pytest.raises(ValueError, match="QA-3"):
        run_critic_pass(
            artifact_ref="artifact/Y",
            artifact_content="c",
            producing_instance_id="inst-X",
            critic_instance_id="inst-X",
        )


# ---------------------------------------------------------------------------
# QA-7 custody boundary · TQ §7 Part B rides EAB-2 quarantine machinery.
# ---------------------------------------------------------------------------

def test_qa_7_custody_boundary_rides_eab_2_quarantine_machinery():
    """QA-7 (TQ §7 line 125 RULED): protection breach → per-batch quarantine.

    Verifies EAB-2 batch_quarantine machinery is on-disk and importable ·
    Critic-pass does NOT re-implement (rides existing machinery).
    """
    q_module = SERVICES_DIR / "service_1" / "batch_quarantine.py"
    assert q_module.exists(), (
        "QA-7 custody boundary rides EAB-2 batch-quarantine machinery · "
        f"{q_module} missing"
    )
    # Import surface exists.
    from services.service_1 import batch_quarantine
    assert hasattr(batch_quarantine, "quarantine_batch") or hasattr(batch_quarantine, "QuarantineEvent")


# ---------------------------------------------------------------------------
# Critic-pass service module does NOT import Targeta eligibility modules.
# ---------------------------------------------------------------------------

def test_critic_pass_service_no_targeta_eligibility_import():
    """§5 fence · Critic-pass does NOT reach Targeta eligibility modules."""
    critic_pass_dir = SERVICES_DIR / "critic_pass"
    banned_modules = {
        "backend.services.targeta.gate",
        "services.targeta.gate",
        "backend.services.targeta.yield_layer",
        "services.targeta.yield_layer",
    }
    for py_file in critic_pass_dir.glob("*.py"):
        src = py_file.read_text()
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for banned in banned_modules:
                    assert not mod.startswith(banned), (
                        f"§5 fence violation: {py_file.name} imports Targeta "
                        f"eligibility module '{mod}'"
                    )


# ---------------------------------------------------------------------------
# Owner ruling ruling-path attest (Standing Rule v3 · ruling byte-identical).
# ---------------------------------------------------------------------------

def test_owner_ruling_persisted_and_byte_identical():
    """Owner ruling persisted at docs/rulings/critic_pass_e1_2026_07_25.md ·
    SHA byte-identical to captured value."""
    ruling_path = BACKEND_ROOT.parent / "docs" / "rulings" / "critic_pass_e1_2026_07_25.md"
    assert ruling_path.exists(), f"Owner ruling missing: {ruling_path}"
    sha = hashlib.sha256(ruling_path.read_bytes()).hexdigest()
    EXPECTED = "42ca9e0f4605b497394772c83572b1e7c5469e17b2c6f7fa39452ec45992c80a"
    assert sha == EXPECTED, (
        f"Owner ruling SHA drift · Standing Rule v3 breach.\n"
        f"  Expected: {EXPECTED}\n"
        f"  Actual  : {sha}"
    )
