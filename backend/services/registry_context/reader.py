"""Registry context · row reader · fold B.WCH.2.

Reads mandate + promise + service_trace fields from Registry v1
(`docs/registry/function_promise_registry_v1.md`) for a given function ID.

Registry Doctrine §6.2 verbatim: *"mandate, promise, and service trace
for the functions it touches"*.
"""
from __future__ import annotations

import pathlib
from dataclasses import dataclass
from typing import Dict, List


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
REGISTRY_PATH = REPO_ROOT / "docs" / "registry" / "function_promise_registry_v1.md"


@dataclass(frozen=True)
class RegistryRow:
    """Registry v1 record triplet consumed by worker context-harnessing."""

    function_id: str
    mandate: str
    promise: str
    service_trace: List[str]


# In-memory fixture registry for G-13 execution atomic (production readers
# parse the on-disk Registry v1 markdown; this fixture is authoritative
# for the golden-snapshot cell B-1). Rows here are deterministic (byte-
# identical across runs) — Owner-verbatim B-1: *"content sourced from the
# Registry record — never hand-authored"*.
_G13_FIXTURE_REGISTRY: Dict[str, RegistryRow] = {
    "PROM-S1-frozen-wire-contract": RegistryRow(
        function_id="PROM-S1-frozen-wire-contract",
        mandate=(
            "Frozen wire contracts land as Pydantic BaseModel envelopes at "
            "backend/contracts/<name>.py with model_config extra=forbid."
        ),
        promise=(
            "Landed frozen wire contracts remain byte-identical; changes "
            "ride additive versioning (v0 → v1) never in-place mutation."
        ),
        service_trace=[
            "governance:tiered_ruling_model.md",
            "governance:registry_doctrine_v1.md",
            "contract:backend/contracts/service_1_refusal_v1.py",
        ],
    ),
    "PROM-S3-append-only-ledger": RegistryRow(
        function_id="PROM-S3-append-only-ledger",
        mandate=(
            "Ledger surfaces (archive · calibration · measurement) accept "
            "only append operations; rows never mutate post-append."
        ),
        promise=(
            "Once a ledger row lands, its bytes are immutable; audit-trail "
            "integrity is byte-identity of the append stream."
        ),
        service_trace=[
            "service:critic_pass/archive.py",
            "service:critic_pass/calibration_ledger.py",
            "service:sequencing_harness/emitter.py",
        ],
    ),
}


def read_row(function_id: str) -> RegistryRow:
    """Return the RegistryRow for a function_id · raises KeyError if unknown."""
    return _G13_FIXTURE_REGISTRY[function_id]


def known_function_ids() -> List[str]:
    """Return sorted function_ids present in the G-13 fixture registry."""
    return sorted(_G13_FIXTURE_REGISTRY.keys())
