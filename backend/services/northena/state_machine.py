"""Northena state machine — composes Admit → Gate → Converge → Ledger.

Mandate §3, §8. Service 1: linear (Admit → Gate → Converge → Ledger).
Service 2 loop scaffolding is here but Layer D + gap re-tasking wire
at G3.

No cousin — the four-stage machine is net-new (mandate §12 verbatim:
"What is new. The four-stage Admit / Gate / Converge / Ledger state
machine").
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from services.northena import admit, converge, gate


# `RegistryHandle` — opaque type for the Solva admit-assist registry.
# Mandate §13 invariant #11 (governors orthogonal): the admit stage alone
# may reach into services.solva_depth; the composer must hold the registry
# as opaque `object`. Folded into the composer at shrink pass to eliminate
# the standalone interfaces.py module.
RegistryHandle = object


async def run_service1_linear(
    *, run_id: str, trace_id: str, raw_intent: Dict[str, Any],
    sub_objective: str,
    done_condition_met: bool, budget_exhausted: bool,
    warm_index: Optional[Iterable[str]] = None,
    registry: Optional[RegistryHandle] = None,
) -> Dict[str, Any]:
    """Linear A→G→C sweep. Returns a summary of the four ledger rows written."""
    a = await admit.compile_and_freeze(raw_intent, run_id=run_id, trace_id=trace_id,
                                       registry=registry)
    if a["decision"] == "refused":
        return {"admit": a, "gate": None, "converge": None}

    frozen = a["frozen_artifact"]
    ar = frozen.artifact_ref()
    lawful_basis_ref = str(raw_intent["lawful_basis"])
    g = await gate.route(
        run_id=run_id, trace_id=trace_id, sub_objective=sub_objective,
        artifact_ref=ar, lawful_basis_ref=lawful_basis_ref,
        scope=list(frozen["scope"]), warm_index=warm_index,
    )
    if g["decision"] == "refused":
        # Out-of-scope: mandate §5 verbatim — logged, not silently dropped.
        # Converge still runs to close the run.
        pass
    c = await converge.check(
        run_id=run_id, trace_id=trace_id, artifact_ref=ar,
        lawful_basis_ref=lawful_basis_ref,
        done_condition_met=done_condition_met, budget_exhausted=budget_exhausted,
    )
    return {"admit": a, "gate": g, "converge": c}
