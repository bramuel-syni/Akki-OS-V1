"""Brief telemetry sidecar — mirrors AF-E3 α + 9.2a-E2 α cond 2 precedent.

Sidecar-only. Frozen contracts UNTOUCHED. Parity 31 preserved.

Payload shape:
    {
      "brief_id": <str>,
      "scope": "slice" | "combined" | "estate",
      "_regeneration_reason": "initial" | "census_change" | "on_demand",
      "_stale_flag": <bool>,
      "_advisory_marker_attached": <bool>,
      "_generation_status": "success" | "grounding_reject" | "llm_unavailable"
                           | "llm_timeout" | "llm_parse_failure",
      "_grounding_reject_detail": <str> | None,
    }
"""
from __future__ import annotations

from typing import Any, Dict, Optional


VALID_REGENERATION_REASONS = ("initial", "census_change", "on_demand")
VALID_GENERATION_STATUSES = (
    "success",
    "grounding_reject",
    "llm_unavailable",
    "llm_timeout",
    "llm_parse_failure",
)


def annotate_brief_result(
    *,
    brief_id: str,
    scope: str,
    telemetry_dict: Dict[str, Any],
    regeneration_reason: str,
    generation_status: str,
    stale_flag: bool,
    advisory_marker_attached: bool,
    grounding_reject_detail: Optional[str] = None,
) -> Dict[str, Any]:
    """Return a NEW dict with brief telemetry fields set (non-mutating).

    Validates:
      * `regeneration_reason` ∈ VALID_REGENERATION_REASONS
      * `generation_status` ∈ VALID_GENERATION_STATUSES
      * `grounding_reject_detail` populated iff `generation_status ==
        "grounding_reject"`
    """
    if regeneration_reason not in VALID_REGENERATION_REASONS:
        raise ValueError(
            f"regeneration_reason {regeneration_reason!r} not in "
            f"{VALID_REGENERATION_REASONS}"
        )
    if generation_status not in VALID_GENERATION_STATUSES:
        raise ValueError(
            f"generation_status {generation_status!r} not in "
            f"{VALID_GENERATION_STATUSES}"
        )
    if generation_status == "grounding_reject" and not grounding_reject_detail:
        raise ValueError(
            "grounding_reject_detail required when generation_status "
            "== 'grounding_reject'"
        )
    if generation_status != "grounding_reject" and grounding_reject_detail is not None:
        raise ValueError(
            "grounding_reject_detail populated iff generation_status "
            "== 'grounding_reject'"
        )
    out = dict(telemetry_dict)
    out.update({
        "brief_id": brief_id,
        "scope": scope,
        "_regeneration_reason": regeneration_reason,
        "_generation_status": generation_status,
        "_stale_flag": stale_flag,
        "_advisory_marker_attached": advisory_marker_attached,
        "_grounding_reject_detail": grounding_reject_detail,
    })
    return out
