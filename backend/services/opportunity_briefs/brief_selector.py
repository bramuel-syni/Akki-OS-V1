"""Brief selector — census-slice enumeration at three scopes.

Salvage-lifted from `github.com/bramuel-syni/Akki-Executive-Core`
scope-walker pattern (OB-R1 · lifted-not-imported · see
`services/opportunity_briefs/README.md` salvage carrier).

Enumerates candidate slices at three scopes per OB-R6:
  * slice     — single census dimension
  * combined  — intersection of ≥2 dimensions
  * estate    — full-estate aggregate scope

Content-neutral · governance §8 data-blind (no broadcaster / regional /
genre / dialectal priors).
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Dict, List, Tuple


VALID_SCOPES = ("slice", "combined", "estate")


@dataclass(frozen=True)
class SliceCandidate:
    scope: str
    contributing_slices: Tuple[str, ...]  # sorted for determinism


def enumerate_candidates(
    census_dimensions: Dict[str, List[str]],
    *,
    max_combined_order: int = 2,
) -> List[SliceCandidate]:
    """Enumerate SliceCandidate rows at all three scopes.

    Args:
      census_dimensions: {dimension_name: [slice_name, ...]} — the
        census-dimensions surface (from `census_dimensions.v1.json`).
      max_combined_order: max number of slices in a Combined scope
        (Tier-3 default = 2 · pairwise intersections).

    Returns:
      List of SliceCandidate — sorted for determinism.
    """
    candidates: List[SliceCandidate] = []
    all_slices: List[str] = []
    for dim, slices in sorted(census_dimensions.items()):
        for slc in sorted(slices):
            slice_id = f"{dim}:{slc}"
            all_slices.append(slice_id)
            candidates.append(SliceCandidate(
                scope="slice",
                contributing_slices=(slice_id,),
            ))
    # Combined scope — pairwise (and up to max_combined_order) intersections.
    for k in range(2, max_combined_order + 1):
        for combo in combinations(all_slices, k):
            candidates.append(SliceCandidate(
                scope="combined",
                contributing_slices=tuple(sorted(combo)),
            ))
    # Estate scope — one row.
    candidates.append(SliceCandidate(
        scope="estate",
        contributing_slices=tuple(sorted(all_slices)),
    ))
    return candidates
