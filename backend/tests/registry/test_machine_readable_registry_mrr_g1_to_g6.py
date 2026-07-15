"""MRR-G1..MRR-G-SourceSHA gate tests · Machine-Readable Registry.

Owner rulings (2026-07-11): MRR-E1 α · MRR-E2 γ · MRR-E3 β+addition · MRR-E4 β.
See /app/docs/rulings/machine_readable_registry_mrr_e1_to_e4.md.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from backend.services.registry.parser import (
    REPO_ROOT,
    V0_PATH,
    SUPPLEMENT_PATHS,
    parse_source,
    render_yaml,
    sha256_file,
)
from backend.services.registry.validator import (
    LOCKED_V0_SHA,
    PART_II_JOURNEY_STEPS,
    check_mrr_g1_schema_conformance,
    check_mrr_g2_vocabulary_lock,
    check_mrr_g3_round_trip,
    check_mrr_g4_findings_coverage,
    check_mrr_g_data_blind,
    check_mrr_g_parity,
    check_mrr_g_source_sha,
)


MACHINE_YAML_PATH = REPO_ROOT / "docs" / "registry" / "machine" / "registry.yaml"


@pytest.fixture(scope="module")
def model():
    return parse_source(V0_PATH, SUPPLEMENT_PATHS)


@pytest.fixture(scope="module")
def rendered_yaml(model):
    return render_yaml(model)


# ---------------------------------------------------------------------------
# MRR-G1 · Schema conformance
# ---------------------------------------------------------------------------


def test_mrr_g1_schema_conformance(model):
    ok, errs = check_mrr_g1_schema_conformance(model)
    assert ok, "MRR-G1 schema conformance failed:\n" + "\n".join(errs)


# ---------------------------------------------------------------------------
# MRR-G2 · Vocabulary lock (β + addition)
# ---------------------------------------------------------------------------


def test_mrr_g2_vocabulary_lock(model):
    ok, errs = check_mrr_g2_vocabulary_lock(model)
    assert ok, "MRR-G2 vocab lock failed:\n" + "\n".join(errs)


def test_mrr_g2_part_ii_journey_constant_present():
    """Sanity: verifiy PART_II_JOURNEY_STEPS carries S1..S4 doctrine-Part-II steps.

    G-2 · 2026-07-14 (docs/rulings/g2_rm_e1_to_e3_2026-07-14.md · RM-E3 α
    canonicalization ruling): S3.prove and S4.verify are the canonical short
    forms; legacy long-form aliases (S3.prove-end-to-end, S4.verify-receipt)
    are RETIRED and MUST NOT be present in the frozenset (verified by
    test_part_ii_journey_steps_alias_canonicalization).
    """
    required_seed = {
        "S1.register",
        "S1.scoped-key",
        "S1.call",
        "S1.pass-receipts-through",
        "S2.onboard-context",
        "S2.integrate-sources",
        "S2.census-fills",
        "S2.commission",
        "S2.sample",
        "S2.commit",
        "S3.pick-run",
        "S3.prove",   # G-2 canonical (was S3.prove-end-to-end pre-2026-07-14)
        "S3.see-retention",
        "S3.change-rules-with-ceremony",
        "S4.receive",
        "S4.verify",  # G-2 canonical (was S4.verify-receipt pre-2026-07-14)
        "S4.license",
    }
    missing = required_seed - PART_II_JOURNEY_STEPS
    assert not missing, f"PART_II_JOURNEY_STEPS missing Doctrine Part II seeds: {sorted(missing)}"


# ---------------------------------------------------------------------------
# MRR-G3 · Round-trip integrity over (v0.md + supplement) ↔ machine form
# ---------------------------------------------------------------------------


def test_mrr_g3_round_trip(model):
    ok, errs = check_mrr_g3_round_trip(model)
    assert ok, "MRR-G3 round-trip failed:\n" + "\n".join(errs)


def test_mrr_g3_combined_source_governance_section_14():
    """Governance §14 attest: round-trip operates over (v0.md + supplements) as one set."""
    v0_sha = sha256_file(V0_PATH)
    assert v0_sha == LOCKED_V0_SHA, (
        f"v0.md byte-identity drift: on-disk {v0_sha} vs locked {LOCKED_V0_SHA}"
    )
    # Every supplement must exist and hash cleanly (append-only additive discipline).
    for supp in SUPPLEMENT_PATHS:
        assert supp.exists(), f"supplement missing: {supp}"
        _ = sha256_file(supp)


# ---------------------------------------------------------------------------
# MRR-G4 · Findings coverage (dual-surface archival per MRR-E2 γ)
# ---------------------------------------------------------------------------


def test_mrr_g4_findings_coverage(model):
    ok, errs = check_mrr_g4_findings_coverage(model)
    assert ok, "MRR-G4 findings coverage failed:\n" + "\n".join(errs)


def test_mrr_g4_all_eleven_findings_ruled(model):
    """Each of the 11 findings has a `[RULED · …]` tag referencing the rulings carrier."""
    for f in model.findings:
        assert f.ruling_tag, f"finding {f.finding_id} missing ruling tag"
        assert "RULED" in f.ruling_tag
        assert f.ruling_ref, f"finding {f.finding_id} missing ruling_ref"


def test_mrr_g4_dual_surface_ledger(model):
    """MRR-E2 γ : supersession ledger contains cross-refs for every RULED finding."""
    ledger_ids = {entry["finding_id"] for entry in model.findings_supersession_ledger}
    ruled_finding_ids = {f.finding_id for f in model.findings if f.ruling_tag}
    assert ledger_ids == ruled_finding_ids, (
        f"ledger/finding-id mismatch: ledger={sorted(ledger_ids)} findings={sorted(ruled_finding_ids)}"
    )


# ---------------------------------------------------------------------------
# MRR-G-Parity · V1-G7 31/31 byte-identical unaffected
# ---------------------------------------------------------------------------


def test_mrr_g_parity(model):
    ok, errs = check_mrr_g_parity(model)
    assert ok, "MRR-G-Parity failed:\n" + "\n".join(errs)


# ---------------------------------------------------------------------------
# MRR-G-DataBlind · no secrets in machine form or supplement
# ---------------------------------------------------------------------------


def test_mrr_g_data_blind(rendered_yaml):
    supplement_text = SUPPLEMENT_PATHS[0].read_text(encoding="utf-8")
    ok, errs = check_mrr_g_data_blind(rendered_yaml, supplement_text)
    assert ok, "MRR-G-DataBlind failed:\n" + "\n".join(errs)


# ---------------------------------------------------------------------------
# MRR-G-SourceSHA (MRR-E1 α condition · integrity-binding by construction)
# ---------------------------------------------------------------------------


def test_mrr_g_source_sha(model, rendered_yaml):
    ok, errs = check_mrr_g_source_sha(model, rendered_yaml)
    assert ok, "MRR-G-SourceSHA failed:\n" + "\n".join(errs)


def test_mrr_g_source_sha_pin_matches_locked_v0(model):
    """MRR-E1 α condition: machine form's embedded source SHA equals Owner-locked v0.md SHA."""
    assert model.source_of_truth["sha256"] == LOCKED_V0_SHA


# ---------------------------------------------------------------------------
# MRR-E4 β + governance §14 · supplement + v0.md byte-identity discipline
# ---------------------------------------------------------------------------


def test_v0_md_byte_identity():
    """Source-of-truth v0.md remains byte-identical at Owner-locked SHA throughout this phase."""
    actual = sha256_file(V0_PATH)
    assert actual == LOCKED_V0_SHA, (
        f"v0.md drifted from locked SHA {LOCKED_V0_SHA} to {actual}"
    )


def test_machine_form_generated_header_present():
    """MRR-E1 α : machine form carries DO-NOT-HAND-EDIT header."""
    if not MACHINE_YAML_PATH.exists():
        pytest.skip("machine form not yet generated (run tools/registry/regenerate.py first)")
    head = MACHINE_YAML_PATH.read_text(encoding="utf-8").splitlines()[:4]
    joined = "\n".join(head)
    assert "GENERATED FROM" in joined
    assert "DO NOT HAND-EDIT" in joined
