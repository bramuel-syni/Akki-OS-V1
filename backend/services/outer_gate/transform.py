"""Outer-gate transform — the one-way irreversibility function (§21.2).

The transform reads a pre-egress artifact (a `PreEgressArtifact` dict
containing plaintext identifiers) and returns an egress artifact
(`EgressArtifact` dict) where every identifier has been one-way transformed
via the mint's `pseudonymise` function.

**Irreversibility (§21.2 + Sys-Invariant #8):** the output does not carry
any plaintext identifier. Recovering the input from the output requires
the mint key; the mint key is purged at end of window.

Categories transformed (spec-derived, §21.2 "pseudonymisation with a purged
mint, k-anonymity / l-diversity / generalisation"):
- `unit_id`, `source_ref`, `speaker_or_author`, `run_id`, `trace_id`
  → HMAC-SHA256 pseudonymisation
- `feed_id`, `structural_signature` → generalisation (category collapse)
- numeric signal scores → optional DP noise (v0: no noise, closed-seam)

Post-Fixture-Refresh 2026-07-10 (FR-E2 α): distributed `_FEED_ID_BUCKET`
table DELETED. Feed_id → bucket_category mapping is now read from the
centralized single-source-of-truth `services/service_1/license_classes.v1.json`
via `services.service_1.license_class_selection.get_bucket_category`.
Default bucket returned by that helper is `unknown_broadcast_category`
(preserved for behavior parity with the pre-refresh _FEED_ID_BUCKET_DEFAULT).
"""
from __future__ import annotations

from typing import Any, Dict, List

from services.outer_gate.mint import MintWindow, pseudonymise
from services.service_1.license_class_selection import get_bucket_category


PSEUDONYMISED_FIELDS = (
    "unit_id",
    "source_ref",
    "speaker_or_author",
    "run_id",
    "trace_id",
    "load_bearing_unit_ids",
)

GENERALISED_FIELDS = (
    "feed_id",
    "structural_signature",
)


def _generalise_feed_id(value: str) -> str:
    """Generalisation into broadcaster-category buckets.

    Reads the mapping from central v1 registry via
    `get_bucket_category(value)`. Unknown feed_ids resolve to the
    registry's `default_bucket_category` (currently
    `unknown_broadcast_category`, preserved from the pre-refresh
    `_FEED_ID_BUCKET_DEFAULT`).
    """
    return get_bucket_category(value)


def _generalise_structural_signature(value: str) -> str:
    """v0 generalisation for a structural_signature (a hex hash): keep the
    first 4 chars ("hash prefix bucket") and drop the rest. Deterministic;
    lossy; irreversible for the specific unit."""
    return (value or "")[:4] + "-generalised"


def transform_artifact(
    pre_egress: Dict[str, Any],
    window: MintWindow,
) -> Dict[str, Any]:
    """Apply the one-way irreversibility transform to `pre_egress`.

    Returns a new dict; does not mutate the input.
    """
    if window.purged:
        raise ValueError(
            "cannot transform via a purged mint window (§21.2)."
        )
    out: Dict[str, Any] = {}
    applied: List[str] = []
    categories_present: List[str] = []

    for key, value in pre_egress.items():
        if key in PSEUDONYMISED_FIELDS and isinstance(value, str) and value:
            out[key] = pseudonymise(window, value)
            applied.append(f"pseudonymise:{key}")
            categories_present.append(key)
        elif key in PSEUDONYMISED_FIELDS and isinstance(value, list):
            # Lists of identifiers (e.g. Solva load_bearing_unit_ids)
            out[key] = [pseudonymise(window, v) for v in value if isinstance(v, str)]
            applied.append(f"pseudonymise:{key}[]")
            categories_present.append(key)
        elif key == "feed_id" and isinstance(value, str) and value:
            out[key] = _generalise_feed_id(value)
            applied.append(f"generalise:feed_id")
            categories_present.append(key)
        elif key == "structural_signature" and isinstance(value, str) and value:
            out[key] = _generalise_structural_signature(value)
            applied.append(f"generalise:structural_signature")
            categories_present.append(key)
        elif key in ("dp_noise_marker",):
            # Placeholder for closed-seam DP noise on numerics; v0 pass-through
            out[key] = value
        else:
            # Pass through non-identifier fields; category tracking on identifiers only
            out[key] = value

    # Attach transform metadata to the egress artifact for downstream audit
    out["_transform_meta"] = {
        "transform_version": "hmac-sha256-v1",
        "mint_window_id": window.mint_window_id,
        "key_fingerprint": window.key_fingerprint,
        "applied_transformations": applied,
        "input_identifier_categories": sorted(set(categories_present)),
    }
    return out
