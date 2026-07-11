"""Health service package (PH-R1 · shared readiness helpers).

Public surface:
    * parity_counter — single authoritative FS-enumeration counter
      shared by /api/readyz, /api/system/build_info, and V1-G7 test.
"""
from __future__ import annotations

from .parity_counter import (  # noqa: F401
    EXPECTED_PARITY,
    count_frozen_contract_snapshots,
    parity_ok,
    snapshot_directory,
)
