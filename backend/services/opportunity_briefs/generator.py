"""Brief generator — orchestrator threading selector → Shield → grounding → registry.

Salvage-lifted structural pattern per OB-R1 (see `README.md` salvage
carrier); no runtime dependency on any Akki system.

Sequence:
  1. Enumerate SliceCandidate rows at three scopes (selector).
  2. For each candidate: build Registry-read texts (caller supplies
     the map today; production wiring lands post-9.2b when the
     Registry read API is populated).
  3. Call Shield brief_synthesizer for a `{brief_text,
     quantitative_anchors}` payload.
  4. Verify grounding — mechanical byte-verbatim per OB-E1 α.
  5. If grounded → registry.write() + telemetry(success);
     else → NOT written, telemetry(grounding_reject).
  6. AF-E2-precedent-shaped runtime-transient handling: catch
     LLMUnavailable / LLMTimeout / LLMParseFailure at the Shield
     boundary → telemetry with the specific status; NEVER a refusal
     envelope. Failed brief is not written; caller / regeneration
     path may retry.

Owner ruling OB-E3 α: **no synthesis-time computation** of aggregates.
The generator does NOT `sum(...)` / `avg(...)` / `min(...)` /
`max(...)` / `count(...)` — Registry reads that carry aggregates are
Registry-computed; the generator only quotes.

Grep-negative attest is at
`test_ob_g_e3_no_synthesis_compute_ast`.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Tuple

from services.opportunity_briefs import brief_selector, brief_registry
from services.opportunity_briefs.brief_grounding import verify_brief_grounding
from services.opportunity_briefs.brief_telemetry import annotate_brief_result
from services.synisense.shield import brief_synthesizer as _synth


async def generate_one_brief(
    *,
    scope: str,
    contributing_slices: List[str],
    registry_read_texts: Dict[str, str],
    census_ref: str,
    regeneration_reason: str = "initial",
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Generate one brief candidate + record telemetry.

    Returns (brief_row_or_none, telemetry_dict).
    On any grounding_reject / runtime transient, brief_row_or_none is
    None; telemetry_dict records the reason.
    """
    reg = brief_registry.registry()
    try:
        payload = await _synth.synthesise_brief(
            scope=scope,
            contributing_slices=contributing_slices,
            registry_read_texts=registry_read_texts,
        )
    except _synth.EmergentKeyMissingError:
        # Config defect · 503 upstream · propagate.
        raise
    except _synth.LLMUnavailableError:
        telem = annotate_brief_result(
            brief_id="",
            scope=scope,
            telemetry_dict={},
            regeneration_reason=regeneration_reason,
            generation_status="llm_unavailable",
            stale_flag=False,
            advisory_marker_attached=False,
        )
        return None, telem
    except _synth.LLMTimeoutError:
        telem = annotate_brief_result(
            brief_id="",
            scope=scope,
            telemetry_dict={},
            regeneration_reason=regeneration_reason,
            generation_status="llm_timeout",
            stale_flag=False,
            advisory_marker_attached=False,
        )
        return None, telem
    except _synth.LLMParseFailureError:
        telem = annotate_brief_result(
            brief_id="",
            scope=scope,
            telemetry_dict={},
            regeneration_reason=regeneration_reason,
            generation_status="llm_parse_failure",
            stale_flag=False,
            advisory_marker_attached=False,
        )
        return None, telem

    # OB-E1 α grounding gate.
    result = verify_brief_grounding(
        brief_text=payload["brief_text"],
        quantitative_anchors=payload["quantitative_anchors"],
        registry_read_texts=registry_read_texts,
    )
    if not result.passed:
        telem = annotate_brief_result(
            brief_id="",
            scope=scope,
            telemetry_dict={},
            regeneration_reason=regeneration_reason,
            generation_status="grounding_reject",
            stale_flag=False,
            advisory_marker_attached=False,
            grounding_reject_detail=result.reject_detail,
        )
        return None, telem

    # Grounded — write to registry.
    row = reg.write(
        scope=scope,
        contributing_slices=contributing_slices,
        brief_text=payload["brief_text"],
        quantitative_anchors=payload["quantitative_anchors"],
        census_ref=census_ref,
    )
    telem = annotate_brief_result(
        brief_id=row["brief_id"],
        scope=scope,
        telemetry_dict={},
        regeneration_reason=regeneration_reason,
        generation_status="success",
        stale_flag=row["stale"],
        advisory_marker_attached=True,
    )
    return row, telem


def enumerate_candidates_at_all_scopes(
    census_dimensions: Dict[str, List[str]],
    *,
    max_combined_order: int = 2,
) -> List[Dict[str, Any]]:
    """Pass-through to selector for external callers (routers)."""
    candidates = brief_selector.enumerate_candidates(
        census_dimensions,
        max_combined_order=max_combined_order,
    )
    return [asdict(c) for c in candidates]
