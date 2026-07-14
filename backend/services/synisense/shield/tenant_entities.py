"""Synisense Shield — tenant entity dictionary (stub layer).

**S2.onboard-era seat.** RMS does not carry the cousin's accounts / contexts /
cycles Mongo harvest (that vocabulary is inapplicable to the extraction
substrate). Regex + spaCy layers in `deidentifier.py` carry the identifier-
detection promise on their own. This module returns an empty catalogue so
the middle layer of the three-layer de-id stack never blocks the chokepoint.

When S2.onboard binds (the buyer-onboarding journey seat), estate vocabulary
lands here per the OWNER-decision register (OD-1) and Op. Values §8.

Contract preserved (do not alter without an Owner ruling):
    async def lookup_in_text(text: str, *, tenant_id: str) -> list[dict]
    Each returned dict shape: {"start": int, "end": int, "type": str, "match": str}

IF-1 execution close (2026-07-14) landed this stub. See:
- Owner amendment: `docs/rulings/outstanding_register_v1_amendment_2026-07-12.md`
- Register: `docs/briefs/outstanding_work_and_gap_register_v1.1.md` §2 IF-1.
"""
from __future__ import annotations

from typing import Any, Dict, List


async def lookup_in_text(text: str, *, tenant_id: str) -> List[Dict[str, Any]]:
    """Empty catalogue — no tenant-dictionary hits, ever, at this era.

    Return type matches the shape `deidentifier.deidentify` expects at
    line 583-585: a list of `{"start", "end", "type", "match"}` dicts.
    An empty list means: "no tenant matches; proceed to spaCy layer."
    """
    # tenant_id is accepted (contract stability) but not consulted — the
    # tenant catalogue is empty until S2.onboard populates it.
    _ = (text, tenant_id)  # silence unused-arg lints
    return []
