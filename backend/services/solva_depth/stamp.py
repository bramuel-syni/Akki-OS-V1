"""Solva stamp — Ring 5 emission at convergence.

Source: `docs/mandates/RMS_Solva_Specification.md` §12.

At convergence, Solva's wide-bar mode judges which refinements to
preserve and emits the Ring 5 defensibility stamp per unit. The verdict
itself is the governed Qualification Matrix lookup (Mtafiti's domain);
Solva applies it and judges preservation depth.

G3 v0: preservation-depth judgment is a pass-through — every Ring 5
stamp already emitted by Layer C (declaration baseline) is preserved
verbatim. When Solva's wide-bar reflection judgment binds (post-G3), it
will refine preservation by consulting the Ring 5 stamp-audit trail.

Cousin chain (transitive):
  `services/g1_defensibility/ring5_stamper.py` — canonical Ring 5
    stamp emission pattern; same read-only-handle discipline.
"""
from __future__ import annotations

from typing import Dict, List, Sequence

from contracts.five_rings import DefensibilityRing, NormalizedUnit


def preserve_stamps(units: Sequence[NormalizedUnit]) -> List[Dict]:
    """Return preservation-annotated Ring 5 stamp blobs for the trace.

    G3 v0: identity-preservation of existing Layer C Ring 5 stamps. The
    wide-bar refinement judgment (source §12) is a G3+ implementation
    choice bounded by the read-only-handle invariant.
    """
    out: List[Dict] = []
    for u in units:
        ring: DefensibilityRing = u.defensibility
        out.append(
            {
                "unit_id": u.unit_id,
                "defensibility_class": ring.defensibility_class.value,
                "matrix_rule_ref": ring.matrix_rule_ref,
                "runtime_mode": ring.runtime_mode,
                "preserved": True,
            }
        )
    return out
