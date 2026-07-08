"""Grounding-marker binding-copy generator (Owner P9-E6 α, 2026-07-08).

Owner ruling verbatim: "E7 resolved a two-document glyph conflict by making
UI Spec authoritative; here no conflict exists — UI Spec §3.3 is unambiguous
and the em-dash is a syntactic pause, not a list separator. Binding copy is
verbatim including the em-dash; the test asserts the exact string."

UI Spec v2.1 §3.3 line 50 binding-copy variants verbatim:
  * "Grounded by sample {sample_ref}"
  * "No sample run — estimates only."   (em-dash "—" preserved verbatim)
"""
from __future__ import annotations

from typing import Optional

GROUNDED_TEMPLATE = "Grounded by sample {sample_ref}"
NO_SAMPLE_VERBATIM = "No sample run — estimates only."


def grounding_marker_copy(sample_ref: Optional[str]) -> str:
    """Return the exact UI Spec §3.3 binding-copy string.

    Em-dash "—" preserved verbatim on the no-sample variant (P9-E6 α).
    """
    if sample_ref:
        return GROUNDED_TEMPLATE.format(sample_ref=sample_ref)
    return NO_SAMPLE_VERBATIM
