"""Census-dimensions mini-phase service package (Owner Message 565 · rulings 2026-07-10).

Owner rulings CD-E1..CD-E4 α + conditions:
  * CD-E1 α + symmetric contradiction — value/source present together or absent
    together; either lone state fails validation. 'β rejected — a required
    "unknown" label fabricates a value to represent absence.'
  * CD-E2 α ↔ CD-E4 coupling — Mongo-schema-only sidecar; container stays
    unfrozen because the load-bearing wire-shape gate lands. If CD-E4 ever
    regresses or is relaxed, this ruling flips to freeze. Neither is
    relaxed alone. Parity 31 preserved.
  * CD-E3 α + register-before-validate — census_observed novel values extend
    the registry via additive versioned bump (v0 → vN) during the census run.
    manifest_declared values get no such path — 'a manifest cannot invent
    vocabulary, only observation can.'
  * CD-E4 α + tolerance test — five governance-key fields pinned; additive
    fields tolerated (Phase 9 census integration will add fields).

Modules:
  * `dimensions_loader` — registry version discovery + additive bump + validation.
  * `dimensions_service` — sidecar record (Pydantic runtime validator, unfrozen)
    + write path (register-before-validate for census_observed; hard fail for
    manifest_declared) + read paths.
"""
from .dimensions_loader import (
    RegistryKind,
    current_registry_version,
    load_registry,
    register_observation,
    validate_content_surface,
    validate_genre,
)
from .dimensions_service import (
    CensusContentDimension,
    read_census_dimensions_for_feed,
    record_census_dimension,
    list_registry,
)

__all__ = [
    "RegistryKind",
    "current_registry_version",
    "load_registry",
    "register_observation",
    "validate_content_surface",
    "validate_genre",
    "CensusContentDimension",
    "read_census_dimensions_for_feed",
    "record_census_dimension",
    "list_registry",
]
