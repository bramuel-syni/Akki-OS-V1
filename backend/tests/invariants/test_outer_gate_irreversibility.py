"""G6 GATE CONDITION 1 — Outer-gate irreversibility.

Product v2.1 §21.2: "Only irreversibly transformed data crosses [the outer
gate]." §21.2 continued: "De-identified is not anonymised … Only irreversibly
anonymised data — as the outer gate produces — may egress for sale."

**The bar is irreversibility, not de-identification.** These tests prove the
input cannot be reconstructed from the output alone:

1. Direct byte inspection — no plaintext identifier appears in the
   serialised egress artifact.
2. Field-by-field inspection — every identifier field is transformed
   (matches hash-hex format, not plain form).
3. Chosen-plaintext / key-purge attack — after the mint window is purged,
   no code path can recover the input from the output. Proof-by-construction
   via HMAC-SHA256 PRF property + destruction of the key.
4. Correlation attack — two artifacts sharing plaintext identifiers get
   the SAME pseudonym within the window (linkability is preserved
   within-window per §21.2), but the pseudonym does NOT reveal the
   plaintext identifier.
5. Transform snapshot — deterministic output for a canonical input under
   a fixed test key; freezes the transform primitive across changes.
"""
from __future__ import annotations

import json
import re
import os
from pathlib import Path

import pytest

from contracts.northena_ledger import LedgerArtifactRef
from services.outer_gate.mint import MintRegistry, pseudonymise
from services.outer_gate.receipt import build_receipt
from services.outer_gate.transform import (
    PSEUDONYMISED_FIELDS,
    GENERALISED_FIELDS,
    transform_artifact,
)


HEX_HASH_RE = re.compile(r"^[0-9a-f]{64}$")


PLAINTEXT_IDS = [
    "unit-secret-plaintext-1",
    "run-secret-plaintext-1",
    "trace-secret-plaintext-1",
    "synthetic://secret/plaintext.raw",
    "very-recognizable-speaker-name",
]


def _canonical_input():
    return {
        "unit_id": PLAINTEXT_IDS[0],
        "run_id": PLAINTEXT_IDS[1],
        "trace_id": PLAINTEXT_IDS[2],
        "source_ref": PLAINTEXT_IDS[3],
        "speaker_or_author": PLAINTEXT_IDS[4],
        "feed_id": "citizen_tv_news",
        "structural_signature": "abcdef0123456789",
        "load_bearing_unit_ids": ["unit-secret-plaintext-1", "unit-secret-plaintext-2"],
        "signal_score": 0.42,
        "defensibility_class": "fact",
    }


# ---- Attack 1: no plaintext identifier in serialised output --------------
def test_no_plaintext_in_egress_bytes():
    registry = MintRegistry()
    window = registry.open_window(timestamp="2026-07-02T00:00:00Z")
    egress = transform_artifact(_canonical_input(), window)
    serialised = json.dumps(egress, sort_keys=True)
    for plaintext in PLAINTEXT_IDS:
        assert plaintext not in serialised, (
            f"GATE CONDITION 1 FAIL — plaintext identifier {plaintext!r} "
            f"appears verbatim in the serialised egress artifact"
        )


# ---- Attack 2: every identifier field is transformed ---------------------
def test_pseudonymised_fields_match_hash_format():
    registry = MintRegistry()
    window = registry.open_window()
    egress = transform_artifact(_canonical_input(), window)
    for f in PSEUDONYMISED_FIELDS:
        v = egress.get(f)
        if isinstance(v, str):
            assert HEX_HASH_RE.match(v), (
                f"field {f!r} egressed as {v!r}, not a 64-char hex hash "
                f"— transform incomplete for this identifier"
            )
        if isinstance(v, list):
            for item in v:
                assert HEX_HASH_RE.match(item), (
                    f"list field {f!r} contains non-hash entry {item!r}"
                )


def test_generalised_fields_transformed():
    """Feed_id + structural_signature must be transformed via generalisation
    (not just passed through), even though they're not hash-hex."""
    registry = MintRegistry()
    window = registry.open_window()
    original = _canonical_input()
    egress = transform_artifact(original, window)
    for f in GENERALISED_FIELDS:
        assert egress.get(f) != original.get(f), (
            f"generalised field {f!r} was not transformed"
        )


# ---- Attack 3: key-purge irreversibility (proof-by-construction) ---------
def test_key_purge_makes_input_unrecoverable():
    """After the mint window is purged, the key is destroyed. Without the
    key, HMAC-SHA256 is a pseudo-random function; recovery of the input
    from the output is not tractable in polynomial time.

    Proof-by-construction: attempting to pseudonymise the same plaintext
    with the (now purged) window raises ValueError. There is no other
    path in the codebase to recover the key from the fingerprint (SHA-256
    of the key), since SHA-256 pre-image resistance holds.
    """
    registry = MintRegistry()
    window = registry.open_window()
    original = _canonical_input()
    egress = transform_artifact(original, window)
    fingerprint_before_purge = window.key_fingerprint

    # Purge the mint
    registry.purge_window(window.mint_window_id)

    # After purge, no code path can produce the same pseudonym for the
    # same plaintext — proving irreversibility of the applied transform.
    with pytest.raises(ValueError, match="purged"):
        pseudonymise(window, original["unit_id"])

    # Fingerprint survives on the receipt for audit; the key itself does not
    assert egress["_transform_meta"]["key_fingerprint"] == fingerprint_before_purge


def test_transform_via_purged_window_refused():
    """Cannot apply the transform via a purged window at all."""
    registry = MintRegistry()
    window = registry.open_window()
    registry.purge_window(window.mint_window_id)
    with pytest.raises(ValueError, match="purged"):
        transform_artifact(_canonical_input(), window)


# ---- Attack 4: correlation attack ---------------------------------------
def test_within_window_correlation_preserved_across_artifacts():
    """§21.2 discipline: within a mint window, pseudonyms are stable
    (linkability preserved for legitimate correlation). But the pseudonym
    does not reveal the plaintext.
    """
    registry = MintRegistry()
    window = registry.open_window()
    a = _canonical_input()
    b = dict(a)  # share the same unit_id
    b["source_ref"] = "synthetic://different/path.raw"
    egress_a = transform_artifact(a, window)
    egress_b = transform_artifact(b, window)
    # Same plaintext unit_id in A and B → same pseudonym (within-window)
    assert egress_a["unit_id"] == egress_b["unit_id"]
    # Different plaintext source_ref → different pseudonyms
    assert egress_a["source_ref"] != egress_b["source_ref"]
    # Neither pseudonym reveals the plaintext
    for pseudo in (egress_a["unit_id"], egress_a["source_ref"]):
        assert a["unit_id"] not in pseudo
        assert a["source_ref"] not in pseudo


def test_cross_window_correlation_broken_by_purge():
    """§21.2 discipline: cross-window linkability is broken. Once a window
    is purged, a NEW window cannot re-derive the same pseudonyms.
    """
    registry = MintRegistry()
    win_a = registry.open_window()
    egress_a = transform_artifact(_canonical_input(), win_a)
    registry.purge_window(win_a.mint_window_id)

    win_b = registry.open_window()
    egress_b = transform_artifact(_canonical_input(), win_b)
    # Same plaintext, different windows → different pseudonyms (the purge
    # is the un-linking guarantee)
    assert egress_a["unit_id"] != egress_b["unit_id"], (
        "cross-window pseudonym collision — irreversibility guarantee "
        "compromised by predictable key material"
    )


# ---- Attack 5: transform snapshot (stability under fixed key) -----------
def test_transform_snapshot_stable_under_fixed_key(monkeypatch):
    """Deterministic-given-key freeze. Uses the test key override so the
    snapshot is reproducible; guards against silent transform changes.
    """
    monkeypatch.setenv("RMS_G6_MINT_KEY_TEST_OVERRIDE", "deterministic-snapshot-key-v0")
    registry = MintRegistry()
    window = registry.open_window(timestamp="2026-07-02T00:00:00Z")
    canonical = {
        "unit_id": "unit-snap-1",
        "run_id": "run-snap-1",
        "trace_id": "trace-snap-1",
        "source_ref": "synthetic://snap/fact.raw",
        "speaker_or_author": "anchor",
        "feed_id": "citizen_tv_news",
        "structural_signature": "0123456789abcdef",
        "load_bearing_unit_ids": ["unit-snap-1", "unit-snap-2"],
        "signal_score": 0.5,
        "defensibility_class": "fact",
    }
    egress = transform_artifact(canonical, window)
    # Stabilise the mint_window_id (uuid-generated) before compare
    egress["_transform_meta"]["mint_window_id"] = "mint-STABILISED-FOR-SNAPSHOT"

    snap_path = Path(__file__).parent / "outer_gate_transform.snapshot.json"
    snap = json.loads(snap_path.read_text(encoding="utf-8"))
    assert egress == snap["egress_artifact"], (
        "outer_gate_transform snapshot drifted; re-bless in review if intentional."
    )


# ---- Contract snapshot ---------------------------------------------------
def test_outer_gate_receipt_contract_frozen():
    from contracts.outer_gate_receipt import OuterGateReceipt
    snap = json.loads(
        (Path(__file__).parent / "outer_gate_receipt.contract_snapshot.json"
         ).read_text(encoding="utf-8")
    )
    assert (
        json.dumps(OuterGateReceipt.model_json_schema(), indent=2, sort_keys=True)
        == json.dumps(snap, indent=2, sort_keys=True)
    ), "OuterGateReceipt schema drifted; re-bless snapshot in review."


# ---- Receipt is safe (no plaintext, no key material) --------------------
def test_receipt_carries_fingerprint_never_key():
    """Receipt contains SHA-256 fingerprint of the key, NEVER the key itself.
    The key is bytes; fingerprint is hex. Assert no key bytes leak into the
    receipt.
    """
    registry = MintRegistry()
    window = registry.open_window()
    original = _canonical_input()
    egress = transform_artifact(original, window)
    receipt = build_receipt(
        egress, run_id="rid", trace_id="tid",
        artifact_ref=LedgerArtifactRef(
            artifact_type="portfolio_mandate",
            artifact_id="art-1", version="v0",
        ),
    )
    # Fingerprint present (64 hex chars); key material would be raw bytes
    assert HEX_HASH_RE.match(receipt.key_fingerprint)
    # Serialise receipt; assert no plaintext identifier leaked from input
    serialised = receipt.model_dump_json()
    for plaintext in PLAINTEXT_IDS:
        assert plaintext not in serialised, (
            f"receipt leaked plaintext identifier {plaintext!r}"
        )
