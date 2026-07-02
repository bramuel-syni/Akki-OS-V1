"""Lift manifest lint — CI enforcement of the transitive-lift discipline.

Manifest file: /app/docs/lift_manifest.json
Journal entry:  BUILD_JOURNAL.md discipline-moment #7 (this test is what
                converts transitive-lift discipline from something the
                builder must remember into something CI enforces).

Two non-negotiable conditions (stakeholder-locked, journaled 2026-07-01):

  Condition 1 — the lint resolves the CLAIM, not the citation string.
    A `direct` claim must resolve the cousin path AND grep-find every
    identifier in `resolves_by` INSIDE the cousin file.
    A `transitive` claim must resolve every intermediate module in
    `transitive_chain` AND grep-find every `resolves_by` identifier
    somewhere IN the chain.

  Condition 2 — substrate-absent is a valid honest state.
    `unverifiable-substrate-absent` PASSES the lint IF the (still-in-pod)
    `transitive_chain` grep-resolves AND `notes` is non-empty. Empty
    reason is a FAIL — silent gaps are the failure mode the guard exists
    to catch.

  `mandate-forced-net-new` PASSES IF `notes` cites a mandate/spec section
    (heuristic: contains one of "mandate", "spec", "§").
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]  # /app
MANIFEST_PATH = REPO_ROOT / "docs" / "lift_manifest.json"
REFERENCE_ROOT = Path("/reference/akki-legacy")  # may or may not exist

VALID_LIFT_KINDS = {
    "direct",
    "transitive",
    "unverifiable-substrate-absent",
    "mandate-forced-net-new",
}

# ---------------------------------------------------------------------------
# Manifest loading.
# ---------------------------------------------------------------------------
def _load_manifest() -> Dict:
    assert MANIFEST_PATH.exists(), (
        f"lift_manifest.json missing at {MANIFEST_PATH} — transitive-lift "
        f"discipline requires the manifest to exist."
    )
    with open(MANIFEST_PATH) as fh:
        return json.load(fh)


MANIFEST = _load_manifest()
ENTRIES: List[Dict] = MANIFEST["entries"]


def _read_source(rel_path: str) -> str:
    """Read a source file relative to /app. Returns '' if the file does
    not exist (callers decide whether that's a FAIL)."""
    p = REPO_ROOT / rel_path
    if not p.exists():
        return ""
    return p.read_text()


# ---------------------------------------------------------------------------
# Structural checks per manifest entry.
# ---------------------------------------------------------------------------
def _check_entry(e: Dict) -> None:
    module_path = e["module"]
    kind = e["lift_kind"]

    assert kind in VALID_LIFT_KINDS, (
        f"[{module_path}] invalid lift_kind {kind!r}; must be one of "
        f"{sorted(VALID_LIFT_KINDS)}"
    )
    # The module itself must actually exist — a manifest entry for a
    # deleted/missing module is nonsense.
    assert (REPO_ROOT / module_path).exists(), (
        f"[{module_path}] module file does not exist at claimed path"
    )
    # resolves_by must be a list of concrete identifier strings.
    resolves_by = e.get("resolves_by", [])
    assert isinstance(resolves_by, list) and all(isinstance(x, str) and x for x in resolves_by), (
        f"[{module_path}] resolves_by must be a non-empty list of "
        f"concrete identifier strings; prose descriptions are "
        f"unresolvable-by-construction"
    )

    if kind == "direct":
        _check_direct(e, module_path)
    elif kind == "transitive":
        _check_transitive(e, module_path)
    elif kind == "unverifiable-substrate-absent":
        _check_unverifiable(e, module_path)
    elif kind == "mandate-forced-net-new":
        _check_mandate_forced(e, module_path)


def _check_direct(e: Dict, module_path: str) -> None:
    cousin = e.get("cousin_citation")
    assert cousin, f"[{module_path}] direct lift MUST cite a cousin path"
    cousin_path = Path(cousin)
    # Direct lifts assume the reference substrate is in-pod.
    assert cousin_path.exists(), (
        f"[{module_path}] direct lift cites {cousin!r} but that path does "
        f"not exist. If the substrate is absent, mark this entry as "
        f"'unverifiable-substrate-absent' with a `notes` field explaining."
    )
    src = cousin_path.read_text()
    for ident in e["resolves_by"]:
        assert ident in src, (
            f"[{module_path}] direct claim: identifier {ident!r} not "
            f"found in cousin {cousin!r}. Claim does not resolve."
        )


def _check_transitive(e: Dict, module_path: str) -> None:
    chain = e.get("transitive_chain") or []
    assert chain, (
        f"[{module_path}] transitive lift MUST have a non-empty "
        f"transitive_chain of /app intermediate module paths"
    )
    # Every intermediate must exist AND we need to grep every
    # `resolves_by` identifier somewhere in the combined chain source.
    combined = ""
    for step in chain:
        step_src = _read_source(step)
        assert step_src, (
            f"[{module_path}] transitive_chain step {step!r} does not "
            f"exist at claimed /app path. Chain broken."
        )
        combined += "\n" + step_src
    for ident in e["resolves_by"]:
        assert ident in combined, (
            f"[{module_path}] transitive claim: identifier {ident!r} "
            f"not found anywhere in transitive_chain {chain!r}. Claim "
            f"does not resolve — either the shape isn't actually lifted "
            f"through that chain, or resolves_by lists the wrong "
            f"identifier."
        )


def _check_unverifiable(e: Dict, module_path: str) -> None:
    # Condition 2: honest absent-substrate state.
    #  - transitive_chain (if any) must grep-resolve (protects against
    #    a broken chain hiding behind the substrate-absent label).
    #  - notes must be non-empty (silent gaps are the failure mode this
    #    guard exists to catch).
    notes = e.get("notes", "")
    assert notes and notes.strip(), (
        f"[{module_path}] unverifiable-substrate-absent MUST carry a "
        f"non-empty `notes` field documenting the reason. Silent gaps "
        f"are the failure mode this guard exists to catch."
    )
    chain = e.get("transitive_chain") or []
    if chain:
        combined = ""
        for step in chain:
            step_src = _read_source(step)
            assert step_src, (
                f"[{module_path}] unverifiable entry declares a "
                f"transitive_chain but step {step!r} does not exist. If "
                f"the chain is broken, drop the chain or fix the path."
            )
            combined += "\n" + step_src
        for ident in e["resolves_by"]:
            assert ident in combined, (
                f"[{module_path}] unverifiable entry with a chain: "
                f"identifier {ident!r} still doesn't grep-resolve in "
                f"the chain. Drop the resolves_by or fix the chain."
            )


def _check_mandate_forced(e: Dict, module_path: str) -> None:
    # cousin_citation may be null.
    assert e.get("cousin_citation") is None, (
        f"[{module_path}] mandate-forced-net-new must have cousin_citation=null"
    )
    notes = (e.get("notes") or "").lower()
    assert notes, (
        f"[{module_path}] mandate-forced-net-new MUST cite a mandate/spec "
        f"section in `notes`."
    )
    # Heuristic: notes must reference a mandate/spec anchor.
    anchors = ("mandate", "spec", "§")
    assert any(a in notes for a in anchors), (
        f"[{module_path}] mandate-forced-net-new `notes` must reference a "
        f"specific mandate/spec section (one of {anchors!r}). Got: "
        f"{notes[:100]!r}"
    )


# ---------------------------------------------------------------------------
# One test per manifest entry (auto-generated) — pytest parametrization.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "entry",
    ENTRIES,
    ids=[e["module"] for e in ENTRIES],
)
def test_manifest_entry_resolves(entry: Dict) -> None:
    """Verifies the claim resolves per Conditions 1 & 2."""
    _check_entry(entry)


# ---------------------------------------------------------------------------
# Schema-level checks (structural + one aggregate).
# ---------------------------------------------------------------------------
def test_manifest_top_level_shape() -> None:
    for k in ("manifest_version", "generated_at", "entries", "substrate_state"):
        assert k in MANIFEST, f"lift_manifest.json missing top-level key {k!r}"
    assert MANIFEST["manifest_version"] == "v0"


def test_no_duplicate_module_entries() -> None:
    mods = [e["module"] for e in ENTRIES]
    dupes = {m for m in mods if mods.count(m) > 1}
    assert not dupes, f"duplicate module entries in lift_manifest: {sorted(dupes)}"


def test_substrate_state_matches_reality() -> None:
    """The substrate_state.reference_akki_legacy_present flag must
    reflect the actual filesystem — no drift between the manifest's
    declared state and what's really in the pod."""
    declared = MANIFEST["substrate_state"]["reference_akki_legacy_present"]
    actual = REFERENCE_ROOT.exists() and any(REFERENCE_ROOT.iterdir()) if REFERENCE_ROOT.exists() else False
    assert declared == actual, (
        f"substrate_state.reference_akki_legacy_present={declared} but "
        f"filesystem says {actual}. Update the manifest."
    )
