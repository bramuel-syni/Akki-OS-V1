"""G-3 Operating Values v1.1 · execution R4 attest cells.

Owner ruling: docs/rulings/g3_operating_values_v1_1_2026-07-15.md ·
G3-E1 α (additive in-place · sixth seam value · no Parity contact) ·
G3-E2 CONFIRMED downgrade · Tier-3 RATIFIED · scope-4 absorption
(TQ §5.1 speech values + TQ §6 MOAC by citation).

Six R4 rows attest here per sidecar
`docs/registry/function_promise_registry_v1_g3_sidecar.md`:
  1. akki.registry.op_values_v1_1_sibling_landed_v1_0_byte_identical
  2. akki.registry.seam_values_carries_six_fields_post_g3
  3. akki.registry.s2_onboard_writes_eight_initial_set_rows
  4. akki.registry.op_values_v1_1_per_language_gates_present_in_doc
  5. akki.registry.op_values_v1_1_no_run_without_telemetry_rule_present
  6. akki.registry.op_values_v1_1_spacy_ner_rung_2_row_present
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from backend.services.multi_instance.onboard_context import (
    OnboardContextV0,
    SeamValues,
)


REPO_ROOT = Path(__file__).resolve().parents[3]
OP_VALUES_V1_0_PATH = REPO_ROOT / "docs" / "requirements" / "operating_values_v1.md"
OP_VALUES_V1_1_PATH = REPO_ROOT / "docs" / "requirements" / "operating_values_v1_1.md"
V1_0_LOCKED_SHA = "a6c4a455175ef37dc71362aea2e41b2ce406baaf9a1c77b3f0f1326e0aa608ee"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# R4 #1 · Op. Values v1.1 sibling landed · v1.0 byte-identical
# ---------------------------------------------------------------------------


def test_v1_0_diff_empty_at_v1_1_landing():
    """v1.0 preserved byte-identical (Standing Rule v3) after v1.1 sibling landing."""
    assert OP_VALUES_V1_0_PATH.exists()
    assert _sha256(OP_VALUES_V1_0_PATH) == V1_0_LOCKED_SHA, (
        f"v1.0 SHA changed! v1.0 must be byte-identical per Standing Rule v3. "
        f"Expected {V1_0_LOCKED_SHA}, got {_sha256(OP_VALUES_V1_0_PATH)}."
    )


def test_v1_1_sibling_lands_on_disk():
    assert OP_VALUES_V1_1_PATH.exists()
    assert OP_VALUES_V1_1_PATH.stat().st_size > 100


# ---------------------------------------------------------------------------
# R4 #2 · SeamValues carries 6 fields post-G-3
# ---------------------------------------------------------------------------


def test_seam_values_has_quarantine_threshold_field():
    """Sixth seam value present per G3-E1 α + Owner ruling."""
    sv = SeamValues()
    assert hasattr(sv, "quarantine_systemic_halt_threshold")
    assert sv.quarantine_systemic_halt_threshold == 0.02  # 2% DEFAULT


def test_seam_values_field_count_is_six():
    fields = set(SeamValues.model_fields.keys())
    assert len(fields) == 6, f"Expected 6 seam values post-G-3; got {len(fields)}: {fields}"
    assert "quarantine_systemic_halt_threshold" in fields


def test_seam_values_quarantine_threshold_range_check():
    """Range-check [0, 1] per field definition."""
    with pytest.raises(Exception):
        SeamValues(quarantine_systemic_halt_threshold=-0.01)
    with pytest.raises(Exception):
        SeamValues(quarantine_systemic_halt_threshold=1.01)
    sv = SeamValues(quarantine_systemic_halt_threshold=0.5)
    assert sv.quarantine_systemic_halt_threshold == 0.5


def test_seam_values_extra_forbid_still_binding():
    """extra='forbid' preserved · schema is strict."""
    with pytest.raises(Exception):
        SeamValues(unknown_field="value")


# ---------------------------------------------------------------------------
# R4 #3 · S2.onboard writes 8 initial_set rows total (6 seams + estate + vocab)
# ---------------------------------------------------------------------------


def test_seam_keys_iteration_covers_six_names():
    """G-3 seam-key loop in s2_onboard router covers 6 keys (5→6 additive)."""
    router_src = (REPO_ROOT / "backend" / "routers" / "s2_onboard.py").read_text()
    assert '"quarantine_systemic_halt_threshold"' in router_src
    assert '"seam_values_ledgered": 6' in router_src
    assert '"total_initial_set_rows": 8' in router_src


# ---------------------------------------------------------------------------
# R4 #4 · Op. Values v1.1 per-language gates present in doc
# ---------------------------------------------------------------------------


def test_f1_per_language_gates_present():
    body = OP_VALUES_V1_1_PATH.read_text(encoding="utf-8")
    assert "F1a" in body
    assert "WER" in body
    assert "1.0pp" in body
    assert "1.5 points" in body
    assert "NO efficiency valve" in body


# ---------------------------------------------------------------------------
# R4 #5 · Op. Values v1.1 no-run-without-telemetry rule present
# ---------------------------------------------------------------------------


def test_f3_telemetry_rule_present():
    body = OP_VALUES_V1_1_PATH.read_text(encoding="utf-8")
    assert "F3" in body
    assert "no run without telemetry" in body.lower() or "run without telemetry is a failed run" in body.lower()


# ---------------------------------------------------------------------------
# R4 #6 · Op. Values v1.1 spaCy NER rung-2 row present
# ---------------------------------------------------------------------------


def test_spacy_ner_row_present_at_rung_2():
    body = OP_VALUES_V1_1_PATH.read_text(encoding="utf-8")
    assert "spaCy NER" in body or "spaCy" in body
    assert "Rung" in body or "rung-2" in body.lower() or "Rung** | 2" in body or "| 2 |" in body
    assert "fail-closed" in body.lower()


# ---------------------------------------------------------------------------
# R4 additional · TQ absorption citations in v1.1 (by citation, not duplication)
# ---------------------------------------------------------------------------


def test_tq_5_1_speech_values_absorbed_by_citation():
    body = OP_VALUES_V1_1_PATH.read_text(encoding="utf-8")
    assert "transformation_quality_spec_v1.md" in body
    assert "§5.1" in body
    assert "VAD false-negative" in body or "VAD-loss" in body or "≤1%" in body
    assert "LID" in body or "Language-ID routing" in body
    assert "≥99%" in body  # de-id recall custody row


def test_tq_6_moac_absorbed_by_citation():
    body = OP_VALUES_V1_1_PATH.read_text(encoding="utf-8")
    for m in ["M-a", "M-b", "M-c", "M-d", "M-e", "M-f"]:
        assert m in body, f"MOAC {m} missing from Op. Values v1.1 citation set"


# ---------------------------------------------------------------------------
# R4 additional · G-3 ruling record on-disk
# ---------------------------------------------------------------------------


def test_g3_ruling_record_lands_on_disk():
    ruling = REPO_ROOT / "docs" / "rulings" / "g3_operating_values_v1_1_2026-07-15.md"
    assert ruling.exists()
    body = ruling.read_text(encoding="utf-8")
    assert "G3-E1" in body
    assert "G3-E2" in body
    assert "α" in body or "alpha" in body.lower()
