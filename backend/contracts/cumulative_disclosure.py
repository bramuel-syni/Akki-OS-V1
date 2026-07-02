"""CumulativeDisclosureLedger@v0 — frozen contract for the V2 cumulative-disclosure arm (G6).

New at G6. Addition; no mutation.

Realises Product v2.1 §29.1 (V2 "demonstrates the cumulative-disclosure guard
refusing a reconstruction attempt") + §21.2 (k-anonymity / l-diversity /
generalisation primitives) + §32 (DPO/Owner-owned config decisions).

**Closed-seam at G6 v0.** The arm is built (code path present, contract frozen,
evaluator wired) but held closed via `arm_admitted=False` until DPO thresholds
land — same pattern as Mtafiti V3 overlay + Targeta yield seams at G4 close.
"""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# Frozen collection name — parallels the northena_ledger discipline.
CUMULATIVE_DISCLOSURE_COLLECTION = "v2_cumulative_disclosure_ledger"


class CumulativeDisclosureLedger(BaseModel):
    """§29.1 — the cumulative-disclosure guard's tracking-state contract.

    Fingerprints (hashed identifiers) accumulate across egresses within
    a mint window; the arm checks whether a new egress combined with
    prior egresses crosses the reconstruction-threshold.
    """

    model_config = ConfigDict(extra="forbid")

    mint_window_id: str = Field(
        ...,
        description="uuid of the mint window; when the window closes, the key is "
                    "purged (§21.2) and this ledger row is retained but no longer "
                    "combinable with future windows.",
    )
    egress_fingerprints: List[str] = Field(
        default_factory=list,
        description="SHA-256 hex fingerprints of prior egress artifacts in this "
                    "window. Empty at G6 v0 — the arm is closed-seam so no egress "
                    "accumulates via this arm's path.",
    )
    k_threshold: Optional[int] = Field(
        default=None,
        description="k parameter for k-anonymity (§21.2). None at G6 v0 — the "
                    "arm is closed-seam until DPO config lands (§32).",
    )
    l_threshold: Optional[int] = Field(
        default=None,
        description="l parameter for l-diversity (§21.2). None at G6 v0.",
    )
    epsilon_budget: Optional[float] = Field(
        default=None,
        description="Cumulative differential-privacy epsilon budget for the window "
                    "(§21.2). None at G6 v0.",
    )
    arm_admitted: bool = Field(
        default=False,
        description="Whether the cumulative arm is opened. False at G6 v0 by "
                    "spec-anchored closed-seam pattern (§29.1 'Until V2 passes'; "
                    "§32 DPO/Owner-owned thresholds).",
    )
