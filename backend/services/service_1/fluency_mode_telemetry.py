"""Fluency-mode telemetry sidecar — Answer Fluency §3.8 (AF-E3 α).

Owner ruling AF-E3 α (2026-07-10) verbatim: *"Sidecar telemetry,
envelope byte-identical, parity 31, per the 9.2a-E2 precedent. Fluency
mode is operational metadata, not a truth claim — no honesty gap on the
wire. β acknowledged as the future additive path if a client-facing
disclosure need ever emerges; not selected."*

Mirrors `services/perception/execution_mode_telemetry.py` (9.2a-E2 α
condition 2 precedent). Returns a NEW dict — never mutates
`ComposedConclusion_v0` (which is frozen · parity 31 preserved).

Telemetry payload shape:
    {
      "fluency_mode": "mechanical" | "llm",
      "_fluency_attribution_trace_id": <trace_id str>,
      "_fluency_reason": "grounding_reject" | "llm_unavailable"
                        | "llm_timeout" | "llm_parse_failure"
                        | None,   # None only when fluency_mode="llm" (success)
      "_grounding_reject_detail": <str> | None,
    }

The `_grounding_reject_detail` field is populated iff `_fluency_reason
== "grounding_reject"`, per AF-E1 β condition 2 (any unanchored /
failing sentence → grounding REJECT → mechanical arm; detail names the
sub-gate that failed).
"""
from __future__ import annotations

from typing import Any, Dict, Optional


VALID_FLUENCY_MODES = ("mechanical", "llm")
VALID_FLUENCY_REASONS = (
    "llm_unavailable",
    "llm_timeout",
    "llm_parse_failure",
    "grounding_reject",
)


def annotate_result(
    trace_id: str,
    telemetry_dict: Dict[str, Any],
    *,
    fluency_mode: str,
    fluency_reason: Optional[str] = None,
    grounding_reject_detail: Optional[str] = None,
) -> Dict[str, Any]:
    """Return a NEW dict with fluency-mode attribution attached.

    `telemetry_dict` is not mutated; the returned dict is a shallow
    copy with the fluency-mode fields set.

    Rules:
      * `fluency_mode` MUST be in `VALID_FLUENCY_MODES`.
      * `fluency_reason` MUST be in `VALID_FLUENCY_REASONS` OR None.
        None is only valid when `fluency_mode == "llm"` (success path).
      * `grounding_reject_detail` populated iff `fluency_reason ==
        "grounding_reject"`.
    """
    if fluency_mode not in VALID_FLUENCY_MODES:
        raise ValueError(
            f"fluency_mode {fluency_mode!r} not in {VALID_FLUENCY_MODES}"
        )
    if fluency_reason is not None and fluency_reason not in VALID_FLUENCY_REASONS:
        raise ValueError(
            f"fluency_reason {fluency_reason!r} not in {VALID_FLUENCY_REASONS}"
        )
    if fluency_mode == "llm" and fluency_reason is not None:
        raise ValueError(
            "fluency_reason MUST be None when fluency_mode='llm' (success)"
        )
    if fluency_reason == "grounding_reject" and not grounding_reject_detail:
        raise ValueError(
            "grounding_reject_detail is required when "
            "fluency_reason == 'grounding_reject'"
        )
    if fluency_reason != "grounding_reject" and grounding_reject_detail is not None:
        raise ValueError(
            "grounding_reject_detail is populated iff "
            "fluency_reason == 'grounding_reject'"
        )

    out = dict(telemetry_dict)
    out["fluency_mode"] = fluency_mode
    out["_fluency_attribution_trace_id"] = trace_id
    out["_fluency_reason"] = fluency_reason
    out["_grounding_reject_detail"] = grounding_reject_detail
    return out
