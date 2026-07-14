"""V2 gate — cumulative-disclosure arm (§29.1).

**CLOSED SEAM at G6 v0** per Product v2.1 §29.1 ("Until V2 passes, delivery
is inner-gate-only") + §32 (DPO/Owner-owned config decisions).

The arm's structure is fully built (this module + the `CumulativeDisclosureLedger@v0`
contract) but held closed via `cumulative_arm_admitted() -> False` until the
DPO/Owner set k, l, and epsilon thresholds. Same pattern as the Mtafiti V3
overlay + Targeta yield closed seams from G4.

If/when thresholds land as config, `cumulative_arm_admitted()` returns True
and `evaluate()` becomes load-bearing.
"""
from __future__ import annotations

import hashlib
import json
import os
from typing import Optional

from contracts.cumulative_disclosure import CumulativeDisclosureLedger
from contracts.northena_ledger import LedgerArtifactRef
from contracts.v2_refusal import V2RefusalEnvelope
from services.v2_gate.refusal import build_refusal


def cumulative_arm_admitted() -> bool:
    """CLOSED SEAM guard. Returns True only when ALL three DPO/Owner-owned
    thresholds are present via config env vars (spec-anchored §32 pattern):

    - AKKI_G6_K_ANONYMITY_THRESHOLD (integer, k in k-anonymity, §21.2)
    - AKKI_G6_L_DIVERSITY_THRESHOLD (integer, l in l-diversity, §21.2)
    - AKKI_G6_DP_EPSILON_BUDGET (float, cumulative DP epsilon, §21.2)

    Any missing → arm closed. This is the acceptance bar for Shape B at G6.
    """
    return all(
        os.environ.get(k) is not None
        for k in (
            "AKKI_G6_K_ANONYMITY_THRESHOLD",
            "AKKI_G6_L_DIVERSITY_THRESHOLD",
            "AKKI_G6_DP_EPSILON_BUDGET",
        )
    )


def egress_fingerprint(egress_artifact_json: str) -> str:
    """SHA-256 hex of the serialised egress artifact. Fingerprint is what
    lands in the CumulativeDisclosureLedger row; the artifact itself does
    not (§21.2 "only irreversibly transformed data crosses").
    """
    return hashlib.sha256(egress_artifact_json.encode("utf-8")).hexdigest()


def evaluate(
    egress_artifact: dict,
    prior_ledger: CumulativeDisclosureLedger,
    *,
    run_id: str,
    trace_id: str,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: Optional[str] = None,
) -> Optional[V2RefusalEnvelope]:
    """Evaluate the cumulative-disclosure guard for a candidate egress.

    Returns a V2RefusalEnvelope if the guard refuses; None if the guard
    passes (or is closed-seam).

    **Closed-seam v0 posture:** if `cumulative_arm_admitted() is False`,
    this returns None. The arm is short-circuited. This is the spec-anchored
    Shape B behaviour per §29.1 "Until V2 passes".
    """
    if not cumulative_arm_admitted():
        # CLOSED SEAM — do not evaluate. Return None so the outer callflow
        # proceeds under the single-packet arm only.
        return None

    # -- Load-bearing path (executed only when thresholds land) --
    # Compute the candidate egress fingerprint, check whether adding it to
    # the prior ledger crosses the k-anonymity / l-diversity threshold.
    # The threshold check is intentionally structural: if the number of
    # fingerprints crossing the mint window equals k_threshold, refuse.
    candidate_fp = egress_fingerprint(json.dumps(egress_artifact, sort_keys=True))
    accumulated = list(prior_ledger.egress_fingerprints) + [candidate_fp]

    k = prior_ledger.k_threshold or 0
    if k > 0 and len(accumulated) >= k:
        # Cumulative-disclosure risk threshold crossed → refuse.
        return build_refusal(
            reason_code="cumulative_disclosure_risk",
            run_id=run_id,
            trace_id=trace_id,
            artifact_ref=artifact_ref,
            lawful_basis_ref=lawful_basis_ref,
            substrate_contract_ref=None,
            detail=(
                f"cumulative-disclosure k-anonymity threshold crossed "
                f"(k={k}, accumulated={len(accumulated)})"
            ),
        )
    return None
