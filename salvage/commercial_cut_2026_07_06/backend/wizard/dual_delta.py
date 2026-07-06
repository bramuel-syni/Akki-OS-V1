"""Dual-delta gate — Phase 7 Stage B-2 (Owner E6 mechanical application).

Owner Standing Owner Disposition #8 (`Visibility-not-prohibition`,
[Owner ruling, Phase 7 Stage A close, 2026-07-04]):
    *"Visibility is the guard; prohibition would be the wrong guard."*

Mechanical application: any agent proposal that changes a
governance-material axis (currently `output.standard` or `output.grain`)
MUST carry BOTH `price_delta` AND `class_delta` on the turn payload.
Missing either → refuse the proposal at emission. The buyer sees the
deltas before accepting.

Declarative-table pattern mirroring `services/service_1/provenance_preservation.py`
(Owner E7 landing at B-1). Single-source derivation — no re-implementation
in state machines. Enforced by
`test_dual_delta_uses_single_source_derivation` grep-negative gate.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Optional, Tuple


# The set of axes that trigger the dual-delta requirement. These are
# the "governance-material" axes per v3 §3.3 buyer semantics: changing
# them changes the price band AND the license class the buyer receives.
# Additional axes MAY land additively at B-3+ under Owner ruling.
_DUAL_DELTA_REQUIRED_AXES: FrozenSet[str] = frozenset({
    "output.standard",
    "output.grain",
})


@dataclass(frozen=True)
class DualDeltaResult:
    """Outcome of the dual-delta check.

    `admissible=True` means the proposal payload is complete and may
    be emitted on the turn. `admissible=False` names the missing
    delta(s) in `missing_deltas` and carries a bounded refusal reason.
    """
    admissible: bool
    missing_deltas: Tuple[str, ...] = ()
    refusal_reason: Optional[str] = None


def required_axes() -> FrozenSet[str]:
    """Return the frozen set of axes that trigger the dual-delta gate.
    Read-only helper for tests / debug surface introspection.
    """
    return _DUAL_DELTA_REQUIRED_AXES


def evaluate_dual_delta(
    axes_changed: FrozenSet[str],
    *,
    price_delta: Optional[str],
    class_delta: Optional[str],
) -> DualDeltaResult:
    """Evaluate a proposal payload against the dual-delta gate.

    * If none of the changed axes are in the required set → admissible
      (e.g. a `reach`-only shift does NOT require dual-delta at B-2).
    * If ANY changed axis is in the required set → BOTH deltas must
      be present and non-empty. Missing either → refuse.

    Standing Owner Disposition #8 (`Visibility-not-prohibition`)
    binding: the guard is visibility, not prohibition. The proposal
    itself is legitimate; the failure mode is a delta-missing
    payload, and the refusal name reflects that (`dual_delta_missing`
    on the emission surface, NOT `proposal_refused`).
    """
    triggered = axes_changed & _DUAL_DELTA_REQUIRED_AXES
    if not triggered:
        return DualDeltaResult(admissible=True)
    missing = []
    if price_delta is None or not str(price_delta).strip():
        missing.append("price_delta")
    if class_delta is None or not str(class_delta).strip():
        missing.append("class_delta")
    if missing:
        return DualDeltaResult(
            admissible=False,
            missing_deltas=tuple(missing),
            refusal_reason=(
                f"dual_delta_missing on axes {sorted(triggered)!r}: "
                f"proposal MUST carry {missing} to be admissible "
                f"(Owner Visibility-not-prohibition, Phase 7 Stage A close)."
            ),
        )
    return DualDeltaResult(admissible=True)
