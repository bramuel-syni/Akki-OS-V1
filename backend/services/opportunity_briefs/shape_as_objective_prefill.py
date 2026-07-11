"""Shape-as-objective handoff — OB-R4.

Owner-verbatim (BCR v1.5 §3.15 OB-R4): *"'Shape as objective' pre-fills
the commission wizard reach from the brief's census slice(s); the
wizard proceeds under its normal rules (mandatory fields asked, never
pre-filled from the brief)."*

Discipline (OB-G4 attests):
  * ONLY the `reach` field of the wizard's prefill payload is
    populated (from the brief's contributing_slices).
  * All other wizard mandatory fields (`commissioner`, `objective`,
    `class`, etc.) are LEFT ABSENT in the prefill payload — the
    wizard prompts for them under its normal rules.
"""
from __future__ import annotations

from typing import Any, Dict


def build_prefill(brief: Dict[str, Any]) -> Dict[str, Any]:
    """Return a wizard-prefill payload from a brief.

    ONLY the `reach` field is populated (from `contributing_slices`).
    No other wizard field is pre-filled from the brief.
    """
    return {
        "reach": {
            "contributing_slices": list(brief.get("contributing_slices", [])),
            "brief_id": brief.get("brief_id", ""),
        },
    }
