"""A2.2 · license_class attachment (DEFAULT · MC-E4 α precedent).

`license_class` = `internal_only` fail-closed at ingest for occurrence rows.
S4 egress refuses under default license_class; explicit rights posture required
for external release (existing MC-E4 α gate at data-source ingest layer).

License_class is a per-row attribute stored alongside the NormalizedUnit in
worker-side plane storage (S1 memory plane · UI-2 landing). At A2 emission,
we attach the fail-closed default to a companion envelope; the S4 outer gate
consults it at egress via the existing MC-E4 α mechanism.

Parameters (D-12 · known and parameterized):
- default_license_class: "internal_only" (MC-E4 α fail-closed default)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DEFAULT_LICENSE_CLASS: Literal["internal_only"] = "internal_only"

# License class enumeration — mirrors MC-E4 α default set.
# Additive classes (e.g. "public_derivative", "member_owned") land per Owner ruling
# in downstream plane commissioning; NOT this atomic.
LicenseClass = Literal["internal_only", "public_derivative", "member_owned"]


@dataclass(frozen=True)
class LicenseClassEnvelope:
    """Companion envelope carrying license_class for an occurrence NormalizedUnit.

    Worker-side; not a Parity 31 contract. Storage-adjacent to the unit; consulted
    by the S4 outer gate before any egress via the shared MC-E4 α gate mechanism.
    """
    unit_id: str
    license_class: LicenseClass
    fail_closed_default: bool


def attach_default_license_class(unit_id: str) -> LicenseClassEnvelope:
    """Attach the MC-E4 α fail-closed default to an occurrence unit at ingest.

    Deterministic; no per-unit configuration. Explicit rights posture upgrades
    happen via subsequent plane-lifecycle rulings (UI-2 landing).
    """
    if not unit_id:
        raise ValueError("unit_id required")
    return LicenseClassEnvelope(
        unit_id=unit_id,
        license_class=DEFAULT_LICENSE_CLASS,
        fail_closed_default=True,
    )
