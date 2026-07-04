"""Config expiry check — Phase 6 Stage B (§8 bullet 2).

`price-model@v0-exploratory` is time-boxed per v3 §8 bullet 2. When the
config's `expires_at` is in the past, quote issuance MUST refuse via
`exploratory_tier_expired` (governance refusal @422 AdmissionRefusal_v0).

Actor-appropriate: NEVER surface owner-side deliberations; surface only
the fact that the tier expired + what the caller can do.

HAZARD-STOP-NOTES (v3 §8 bullet 2):
  * Time-boxed model version — expiry attaches to the model, not the tier.
  * Master Admin bumps to a fresh price-model@vN via control surface;
    every quote stamps the current-bless version at mint time.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict


def is_expired(config: Dict, *, now: datetime = None) -> bool:
    """Return True iff the config's `expires_at` is strictly past.

    Loose-as-frozen: `expires_at` is a string; we parse it. Missing key
    → not expired (defensive: allow deployments to omit expiry on
    stable, non-exploratory tiers).
    """
    expires_at_raw = config.get("expires_at")
    if not expires_at_raw:
        return False
    try:
        expires_at = datetime.fromisoformat(expires_at_raw.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        # Un-parseable → treat as not-expired here; separate validator
        # would flag this at admin-write time.
        return False
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    current = now or datetime.now(timezone.utc)
    return current > expires_at
