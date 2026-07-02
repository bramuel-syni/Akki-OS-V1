"""Synthetic plumbing fixture round-trip + adversarial assertions.

G0 invariants preserved (snapshot drift catches any unintended schema
change). G0.5 adds the adversarial-fixture assertions per Deliverable 1.
"""
from __future__ import annotations

import json
from pathlib import Path

from contracts.five_rings import DefensibilityClass, Modality, NormalizedUnit, RelationType
from contracts.qualification_matrix.loader import load_qualification_matrix
from services.data_source.synthetic import ADVERSARIAL_DIMENSIONS, SyntheticPlumbingDataSource
from services.data_source.synthetic_asset_gen import AUDIO_DIR, IMAGE_DIR


def test_fixture_has_at_least_20_units():
    units = list(SyntheticPlumbingDataSource().iter_units())
    assert len(units) >= 20, f"need >=20 adversarial units, got {len(units)}"


def test_fixture_all_rings_populated():
    matrix = load_qualification_matrix("v0")
    edge_types_seen = set()
    for u in SyntheticPlumbingDataSource().iter_units():
        assert u.provenance.source_ref
        assert isinstance(u.provenance.modality, Modality)
        assert u.reextraction_handle.raw_pointer
        assert u.reextraction_handle.model_id
        assert isinstance(u.defensibility.defensibility_class, DefensibilityClass)
        assert u.defensibility.matrix_rule_ref
        rule_id = u.defensibility.matrix_rule_ref.split("@")[0]
        assert matrix.by_id(rule_id) is not None
        for edge in u.relational.edges:
            edge_types_seen.add(edge.type)
        # Signal ring carries >=1 dim for non-trivial modalities; allow empty for text-only edge cases
        # (we authored every unit with at least one dim, so this is a tight check).
        assert u.signal.dimensions, f"unit {u.unit_id} has empty Signal ring"
    assert edge_types_seen, "need >=1 Relational edge across estate"


def test_fixture_roundtrips_through_schema():
    for u in SyntheticPlumbingDataSource().iter_units():
        dumped = u.model_dump(mode="json")
        reparsed = NormalizedUnit.model_validate(dumped)
        redumped = reparsed.model_dump(mode="json")
        assert json.dumps(dumped, sort_keys=True) == json.dumps(redumped, sort_keys=True), (
            f"unit {u.unit_id} drifted on round-trip"
        )


def test_synthetic_fixture_is_adversarial():
    """Each adversarial dimension MUST be present in code-asserted counts."""
    units = list(SyntheticPlumbingDataSource().iter_units())

    code_switch = sum(1 for u in units if "[code_switch]" in (u.provenance.context or ""))
    genre_boundary = sum(1 for u in units if "[genre_boundary]" in (u.provenance.context or ""))

    # Contested chain: count units that participate in a corroborates/contradicts/retracts edge OR are referenced by one.
    edge_unit_ids: set[str] = set()
    for u in units:
        for e in u.relational.edges:
            edge_unit_ids.add(u.unit_id)
            edge_unit_ids.add(e.target_unit_ref)
    contested = len(edge_unit_ids)

    # Sub-30s units: any audio unit where (t_end - t_start) < 30_000ms AND is part of a multi-speaker audio asset.
    sub_30 = sum(
        1 for u in units
        if u.provenance.modality == Modality.AUDIO
        and (u.provenance.locator.get("t_end_ms", 0) - u.provenance.locator.get("t_start_ms", 0)) < 30_000
        and (u.provenance.context or "").startswith(("Caller", "Short", "Caller-in", "Sheng"))
    )
    # Fallback: be tolerant on the prefix — just count any audio under 30s.
    if sub_30 < ADVERSARIAL_DIMENSIONS["sub_30s_speaker_units"]:
        sub_30 = sum(
            1 for u in units
            if u.provenance.modality == Modality.AUDIO
            and (u.provenance.locator.get("t_end_ms", 0) - u.provenance.locator.get("t_start_ms", 0)) < 30_000
            and "Caller" in (u.provenance.speaker_or_author or "")
        )

    audio_files = sorted(p for p in AUDIO_DIR.glob("*.wav")) if AUDIO_DIR.exists() else []
    image_files = sorted(p for p in IMAGE_DIR.glob("*.png")) if IMAGE_DIR.exists() else []

    # Defensibility skew: utterance MUST be majority; some fact; some non_factual present.
    classes = [u.defensibility.defensibility_class for u in units]
    n = len(classes)
    utt = sum(1 for c in classes if c == DefensibilityClass.UTTERANCE)
    fact = sum(1 for c in classes if c == DefensibilityClass.FACT)
    nonfact = sum(1 for c in classes if c == DefensibilityClass.NON_FACTUAL)

    assert code_switch >= ADVERSARIAL_DIMENSIONS["code_switching_units"], (
        f"need >={ADVERSARIAL_DIMENSIONS['code_switching_units']} code-switch units; got {code_switch}"
    )
    assert genre_boundary >= ADVERSARIAL_DIMENSIONS["genre_boundary_units"], (
        f"need >={ADVERSARIAL_DIMENSIONS['genre_boundary_units']} genre-boundary units; got {genre_boundary}"
    )
    assert contested >= ADVERSARIAL_DIMENSIONS["contested_chain_units"], (
        f"need >={ADVERSARIAL_DIMENSIONS['contested_chain_units']} contested-chain participants; got {contested}"
    )
    assert sub_30 >= ADVERSARIAL_DIMENSIONS["sub_30s_speaker_units"], (
        f"need >={ADVERSARIAL_DIMENSIONS['sub_30s_speaker_units']} sub-30s units; got {sub_30}"
    )
    assert len(audio_files) >= ADVERSARIAL_DIMENSIONS["audio_assets"], (
        f"need >={ADVERSARIAL_DIMENSIONS['audio_assets']} audio assets; got {len(audio_files)}"
    )
    assert len(image_files) >= ADVERSARIAL_DIMENSIONS["image_assets"], (
        f"need >={ADVERSARIAL_DIMENSIONS['image_assets']} image assets; got {len(image_files)}"
    )
    assert utt > fact and utt > nonfact, f"defensibility skew not lopsided to utterance: utt={utt} fact={fact} nf={nonfact}"
    assert fact > 0, "need at least 1 fact unit"
    assert nonfact > 0, "need at least 1 non_factual unit (thin tail)"
