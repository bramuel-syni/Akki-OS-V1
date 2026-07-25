"""G-13 Binding B-2 discharge · MandateSpec@v0 emitter regeneration-diff + shadow-canon prevention.

Owner ruling verbatim (Binding B-2):
    "The emitter is deterministic — same mandate input yields
    byte-identical YAML — every generated file carries a
    generated-do-not-edit header naming its source mandate + SHA, and a
    CI cell regenerates and diffs: any divergence between
    docs/generated/mandate_specs/ and fresh emitter output is a hard
    fail. Generated artifacts that can be hand-edited silently are a
    shadow-canon vector; the regeneration diff closes it."
"""
from __future__ import annotations

import pathlib

import pytest

from services.far_endpoint.mandate_reader import (
    MANDATES_DIR,
    list_mandate_paths,
    parse_mandate,
)
from services.far_endpoint.mandate_spec_emitter import (
    GENERATED_SPECS_DIR,
    HEADER_TEMPLATE,
    emit_mandate_spec,
    render_spec_yaml,
)


# ---------------------------------------------------------------------------
# B-2 regeneration-diff cell.
# ---------------------------------------------------------------------------

def test_b2_regeneration_diff_all_specs():
    """B-2 hard-fail: every on-disk spec byte-matches fresh emitter output.

    For each mandate source, regenerate the spec and compare to the
    on-disk YAML. Any divergence = hard fail (Owner-verbatim: 'not warn').
    """
    assert GENERATED_SPECS_DIR.exists(), (
        f"B-2 hard-fail: {GENERATED_SPECS_DIR} missing · run emitter"
    )
    for mandate_path in list_mandate_paths():
        parsed = parse_mandate(mandate_path)
        fresh_spec = emit_mandate_spec(parsed)
        fresh_yaml = render_spec_yaml(fresh_spec)
        on_disk_path = GENERATED_SPECS_DIR / f"{fresh_spec.spec_id}.yaml"
        assert on_disk_path.exists(), (
            f"B-2 hard-fail: on-disk spec missing for mandate "
            f"{mandate_path.name}: {on_disk_path}"
        )
        on_disk_yaml = on_disk_path.read_text()
        assert on_disk_yaml == fresh_yaml, (
            f"B-2 hard-fail: regeneration diff at {on_disk_path.name} "
            f"(source: {mandate_path.name}). Shadow-canon vector detected."
        )


def test_b2_emitter_deterministic():
    """B-2: emitter is deterministic · same mandate input yields byte-identical YAML."""
    mandates = list_mandate_paths()
    assert len(mandates) > 0, "B-2 attest requires at least one mandate document"
    m = mandates[0]
    a = render_spec_yaml(emit_mandate_spec(parse_mandate(m)))
    b = render_spec_yaml(emit_mandate_spec(parse_mandate(m)))
    c = render_spec_yaml(emit_mandate_spec(parse_mandate(m)))
    assert a == b == c


def test_b2_generated_do_not_edit_header_present():
    """B-2: every generated YAML carries the do-not-edit header (source + SHA + generator + regenerate)."""
    for yaml_path in sorted(GENERATED_SPECS_DIR.glob("*.yaml")):
        text = yaml_path.read_text()
        assert text.startswith("# GENERATED · DO NOT EDIT"), (
            f"B-2 hard-fail: {yaml_path.name} missing generated-do-not-edit header"
        )
        for required in ("# Source:", "# Source SHA-256:", "# Generator:", "# Regenerate:"):
            assert required in text[:400], (
                f"B-2 hard-fail: {yaml_path.name} missing required header line '{required}'"
            )


def test_b2_no_orphan_mandates():
    """B-2: every mandate under docs/mandates/ has a corresponding generated spec (no orphans)."""
    mandate_stems = {p.stem for p in list_mandate_paths()}
    spec_stems = {p.stem for p in GENERATED_SPECS_DIR.glob("*.yaml")}
    orphans = mandate_stems - spec_stems
    assert not orphans, (
        f"B-2 hard-fail: orphan mandates without generated specs: {sorted(orphans)}"
    )


def test_b2_no_stray_generated_specs():
    """B-2 shadow-canon prevention: no generated spec without a source mandate."""
    mandate_stems = {p.stem for p in list_mandate_paths()}
    spec_stems = {p.stem for p in GENERATED_SPECS_DIR.glob("*.yaml")}
    strays = spec_stems - mandate_stems
    assert not strays, (
        f"B-2 hard-fail: stray generated specs without source mandates: {sorted(strays)}. "
        f"Shadow-canon vector detected."
    )
