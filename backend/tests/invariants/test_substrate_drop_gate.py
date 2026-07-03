"""Substrate-drop gate — CI invariant.

Substrate-Drop v1 institutionalisation (2026-07-01):
- Every phase G3/G4/G5a/G5b/G6 declares the source specs it depends on.
- This test asserts, at CI time:
  1. Every required spec listed in `docs/mandates/phase_source_requirements.yaml`
     exists at `docs/mandates/<filename>`.
  2. Every spec present has its SHA-256 recorded in `docs/mandates/MANIFEST.md`
     and the recorded hash matches the actual `.md` file. (Post-2026-07-02
     authoring-direction inversion: canonical hash target is the `.md`, not
     the `.docx`; see MANIFEST preamble.)
  3. Machine-readable `phase_source_requirements.yaml` and `MANIFEST.md` are
     both parseable.

Norm: a phase does not open until its required specs are all present + hash-matching.

Failure mode: prints the exact missing filename(s) or the phase(s) that would
be blocked. No implicit fallback.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Dict, List

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MANDATES_DIR = REPO_ROOT / "docs" / "mandates"
SOURCE_DIR = MANDATES_DIR / "source"
MANIFEST = MANDATES_DIR / "MANIFEST.md"
PHASE_REQS = MANDATES_DIR / "phase_source_requirements.yaml"


def _load_yaml_phase_reqs(path: Path) -> Dict[str, List[str]]:
    """Minimal YAML parser for our top-level {phase: [file, ...]} shape.

    We don't want to add PyYAML as a test-only dep; this parser handles
    exactly the shape we ship — top-level keys mapping to `- item` lists.
    """
    text = path.read_text()
    out: Dict[str, List[str]] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" ") and line.endswith(":"):
            current_key = line[:-1].strip()
            out[current_key] = []
            continue
        stripped = line.lstrip()
        if current_key is not None and stripped.startswith("- "):
            out[current_key].append(stripped[2:].strip())
    return out


def _load_manifest_hashes(path: Path) -> Dict[str, str]:
    """Parse `MANIFEST.md` and return {filename.md: sha256_of_canonical_md}.

    Post-2026-07-02 authoring-direction inversion: the manifest hash is
    over the `.md` file itself (canonical), not the `.docx` (generated
    presentation). See MANIFEST.md preamble.

    Expects a markdown table row per spec of the form
    `| \`filename.md\` | \`sha256_hex\` | ... |`.
    """
    text = path.read_text()
    out: Dict[str, str] = {}
    # Match a row: | `filename.md` | `hexhash` | ...
    row_re = re.compile(r"^\|\s*`(?P<name>[^`]+\.md)`\s*\|\s*`(?P<hash>[0-9a-fA-F]{64})`", re.MULTILINE)
    for m in row_re.finditer(text):
        out[m.group("name")] = m.group("hash").lower()
    return out


def _sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 15), b""):
            h.update(chunk)
    return h.hexdigest()


def _md_to_source_docx(md_name: str) -> Path:
    """Map `northena.md` -> `RMS_Northena_Specification.docx` etc.

    Our convention: the .md filename matches its .docx source filename
    at the root of `source/`, except for `northena.md` which was
    intentionally renamed at file time. Look up the original by scanning
    `source/` for a matching stem or a canonical mapping.
    """
    canonical = {
        "northena.md": "RMS_Northena_Specification.docx",
    }
    if md_name in canonical:
        return SOURCE_DIR / canonical[md_name]
    return SOURCE_DIR / md_name.replace(".md", ".docx")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_manifest_and_phase_reqs_parseable():
    """Both machine-readable governance files must exist and parse."""
    assert MANIFEST.exists(), f"MANIFEST missing: {MANIFEST}"
    assert PHASE_REQS.exists(), f"phase_source_requirements missing: {PHASE_REQS}"
    manifest_hashes = _load_manifest_hashes(MANIFEST)
    phase_reqs = _load_yaml_phase_reqs(PHASE_REQS)
    assert manifest_hashes, "MANIFEST contains no parseable filename/sha256 rows"
    assert phase_reqs, "phase_source_requirements contains no parseable phase entries"


def test_all_phase_required_specs_are_present():
    """For every phase, every required spec must exist on disk."""
    phase_reqs = _load_yaml_phase_reqs(PHASE_REQS)
    missing_by_phase: Dict[str, List[str]] = {}
    for phase, files in phase_reqs.items():
        missing: List[str] = []
        for f in files:
            spec_path = MANDATES_DIR / f
            if not spec_path.exists():
                missing.append(f)
        if missing:
            missing_by_phase[phase] = missing
    assert not missing_by_phase, (
        "Substrate-drop gate FAIL — phases blocked by missing specs: "
        f"{missing_by_phase}"
    )


def test_manifest_hashes_match_canonical_md():
    """Every manifest entry must hash to the canonical `.md` file at MANDATES_DIR.

    Post-2026-07-02 authoring-direction inversion: the manifest records
    the SHA-256 of the canonical `.md` under `docs/mandates/`, not the
    `.docx` source. The `.docx` files under `source/` are presentation
    artefacts retained for provenance only.
    """
    manifest_hashes = _load_manifest_hashes(MANIFEST)
    mismatches: Dict[str, str] = {}
    missing_specs: List[str] = []
    for md_name, recorded_hash in manifest_hashes.items():
        md_path = MANDATES_DIR / md_name
        if not md_path.exists():
            missing_specs.append(f"{md_name} at {md_path}")
            continue
        actual = _sha256_of(md_path)
        if actual.lower() != recorded_hash.lower():
            mismatches[md_name] = f"expected {recorded_hash}, got {actual}"
    assert not missing_specs, f"Manifest references canonical .md files that are missing: {missing_specs}"
    assert not mismatches, f"Manifest SHA-256 tamper-detection FAIL: {mismatches}"


def test_all_phase_required_specs_have_manifest_entries():
    """Every spec referenced by a phase requirement must be listed in the MANIFEST."""
    phase_reqs = _load_yaml_phase_reqs(PHASE_REQS)
    manifest_hashes = _load_manifest_hashes(MANIFEST)
    referenced = {f for files in phase_reqs.values() for f in files}
    unlisted = sorted(referenced - set(manifest_hashes.keys()))
    assert not unlisted, (
        "Phase requirements reference specs not listed in MANIFEST.md: "
        f"{unlisted}"
    )


@pytest.mark.parametrize("phase", ["G3", "G4", "G5a", "G5b", "G6"])
def test_phase_gate_ready(phase: str):
    """Fine-grained per-phase readiness — each phase asserts its full spec set is present + hash-matches.

    Post-2026-07-02: hash target is the canonical `.md`, not the `.docx`.
    """
    phase_reqs = _load_yaml_phase_reqs(PHASE_REQS)
    manifest_hashes = _load_manifest_hashes(MANIFEST)
    if phase not in phase_reqs:
        pytest.skip(f"phase {phase} not in requirements (backlog placeholder)")
    for md_name in phase_reqs[phase]:
        spec_path = MANDATES_DIR / md_name
        assert spec_path.exists(), f"{phase} blocked: {md_name} missing at {spec_path}"
        assert md_name in manifest_hashes, f"{phase} blocked: {md_name} not in MANIFEST.md"
        actual = _sha256_of(spec_path)
        assert actual.lower() == manifest_hashes[md_name].lower(), (
            f"{phase} blocked: SHA-256 mismatch on {md_name} "
            f"(manifest {manifest_hashes[md_name]}, actual {actual})"
        )
