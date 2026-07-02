"""Solva pipeline runner — Layer C → 5 reasoning stages → boundary → trace.

Source: `docs/mandates/RMS_Solva_Specification.md` §7 (module layout) +
§13 (trace) + §15 (construction requirements).

Not a G3 mandatory shipping component per source, but the seam that
lets `test_solva_trace_ledger_integration` verify Solva-spec invariant #8
(every extraction-time judgment produces a trace) end-to-end.
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence, Union

from contracts.five_rings import NormalizedUnit
from services.layer_c.convergence import converge_units
from services.solva_depth.assertion import Assertion
from services.solva_depth.enforce import Refusal, enforce
from services.solva_depth.interfaces import FloorSpec
from services.solva_depth.reasoning.candidate import candidate
from services.solva_depth.reasoning.frame import frame
from services.solva_depth.reasoning.probability import probability
from services.solva_depth.reasoning.reflection import reflection
from services.solva_depth.reasoning.tension import tension
from services.solva_depth.trace import (
    SolvaTrace,
    StageRecord,
    conclusion_to_dict,
    now_iso,
)


def _summarize(a: Dict[str, Any]) -> str:
    keys = sorted(a.keys())
    return f"stage={a.get('stage')} keys={keys}"


def run_solva(
    *,
    trace_id: str,
    run_id: str,
    question: str,
    units: Sequence[NormalizedUnit],
    floor: FloorSpec,
) -> SolvaTrace:
    """Run Layer C convergence → 5 reasoning stages → boundary. Return SolvaTrace.

    The pipeline is code-only at G3 (no LLM calls). Reasoning-faculty
    method is a build-time implementation choice bounded by the
    invariants (source §18).
    """
    stages: List[StageRecord] = []
    # Layer C convergence — validates signal-ring conformance + hands off.
    convergence_input = f"question={question!r}, units_count={len(units)}"
    layer_c_units: List[NormalizedUnit] = converge_units(units)
    stages.append(StageRecord(
        stage_name="layer_c_converge",
        input_summary=convergence_input,
        output_summary=f"conformant_units={len(layer_c_units)}",
        at=now_iso(),
    ))
    # 5 reasoning stages.
    a_frame = frame(question, layer_c_units)
    stages.append(StageRecord("frame", convergence_input, _summarize(a_frame), now_iso()))
    a_candidate = candidate(a_frame, layer_c_units)
    stages.append(StageRecord("candidate", _summarize(a_frame), _summarize(a_candidate), now_iso()))
    a_tension = tension(a_candidate)
    stages.append(StageRecord("tension", _summarize(a_candidate), _summarize(a_tension), now_iso()))
    a_probability = probability(a_candidate, a_tension)
    stages.append(StageRecord("probability", _summarize(a_tension), _summarize(a_probability), now_iso()))
    a_reflection = reflection(question, a_candidate, a_probability)
    stages.append(StageRecord("reflection", _summarize(a_probability), _summarize(a_reflection), now_iso()))
    # Boundary — via enforce (applies floor read-only; refuses below floor).
    lb: List[NormalizedUnit] = a_reflection["load_bearing_units"]
    result: Union[Assertion, Refusal] = enforce(a_reflection["conclusion_text"], lb, floor)
    # X1 discipline (post-A2): thread the boundary-computed class rather than
    # recomputing when the boundary already returned it. On the Refusal branch
    # enforce() has computed the class at enforce.py:60 and preserved it on
    # Refusal.computed_class (enforce.py:41). Reading is single-source; a
    # second conclusion_class(lb) call would be deterministic-safe but
    # architecturally a divergence surface ("one governed class, computed
    # once, read everywhere"). Assertion has no computed_class field today,
    # so preserve the recompute on that branch.
    from services.solva_depth.assertion import conclusion_class as _cc
    if isinstance(result, Refusal):
        computed_class = result.computed_class.value
    else:
        computed_class = _cc(lb).value
    return SolvaTrace(
        trace_id=trace_id,
        run_id=run_id,
        stages=stages,
        load_bearing_unit_ids=[u.unit_id for u in lb],
        computed_class=computed_class,
        conclusion=conclusion_to_dict(result),
    )
