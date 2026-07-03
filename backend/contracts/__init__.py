"""RMS Intelligence System — contracts package.

G0-frozen contracts:
  * five_rings        — Normalized Tier schema (Provenance, Signal, Relational,
                        Re-extraction Handle, Defensibility). Spec §5.
  * objective_request — Service-2 request envelope. Spec §8.1.
  * qualification_matrix — governed taxonomy mapping (genre × source-standing)
                           → asserts_what ceiling. Spec §3.4. MEA-owned.

Pattern: every contract = Pydantic schema + JSON snapshot + invariant test
that fails on drift. Cousin pointer:
/reference/akki-legacy/backend/tests/invariants/test_invariant_contract_snapshots.py
"""
from contracts.five_rings import (  # noqa: F401
    DefensibilityClass,
    DefensibilityRing,
    Modality,
    NormalizedUnit,
    ProvenanceRing,
    RelationalEdge,
    RelationalRing,
    ReextractionHandleRing,
    RelationType,
    ScoreVector,
    SignalRing,
)
from contracts.objective_request import (  # noqa: F401
    DefensibilityFloor,
    EstateRegionSelector,
    ObjectiveMode,
    ObjectiveRequest,
)
from contracts.objective_request_v2 import (  # noqa: F401
    BuyerCommercial,
    Commercial,
    Envelope,
    ObjectiveEntry,
    ObjectiveRequest_v2,
    OperatorShaping,
    Output,
    OutputConsumer,
    OutputForm,
    OutputGrain,
    Reach,
    Shaping,
)
from contracts.qualification_matrix.loader import (  # noqa: F401
    QualificationMatrix,
    QualificationRule,
    load_qualification_matrix,
)
