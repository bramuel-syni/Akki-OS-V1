"""Transform Forms service package — BCR §3.7 landing.

Owner rulings TF-E1..TF-E4 α (2026-07-08). Governance §4.4 three-tier model.

Modules:
  * defensibility_loader — loads and validates against the canonical
    `defensibility_classes.v0.json` registry (TF-E3 α condition).
  * knowledge_artifact — KA claim-graph assembly (TF-R1 landing).
  * callable_skill_gate — per-call inner gate decorator (TF-E4 (a) α).
  * callable_skill_persistence — write-once provisioning + revocation
    (TF-E4 (b) α — enforced by TF-G9 grep-negative gate).
"""
from .defensibility_loader import (
    ALLOWED_DEFENSIBILITY_CLASSES,
    load_defensibility_classes,
    validate_defensibility_class,
)
from .callable_skill_persistence import (
    provision_skill,
    revoke_skill,
    load_provisioning,
)
from .callable_skill_gate import require_governed_skill_query

__all__ = [
    "ALLOWED_DEFENSIBILITY_CLASSES",
    "load_defensibility_classes",
    "validate_defensibility_class",
    "provision_skill",
    "revoke_skill",
    "load_provisioning",
    "require_governed_skill_query",
]
