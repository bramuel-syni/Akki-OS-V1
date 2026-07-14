"""Held-class registry — single-source enumeration for v2.1 §4.3.

Owner E5 seam (2026-07-04, refined at 2026-07-06 B-5a dispatch):
    "Three classes separately addressable: `ledger_row`,
     `wizard_transcript`, `delivered_artifact` — each renders as an
     independently-configurable entity with its own retention row.
     Inheritance-as-default — retention window inherits from a
     system-wide default UNLESS DPO explicitly splits per class."

This module is the SINGLE SOURCE of the held-class list. Consumers:
  * `services.compliance.retention_config` — builds the 3-class response
  * `frontend/src/pages/compliance/ComplianceRetentionRightsPage.js` —
    renders 3 separately-addressable DOM regions (via mirror JSON at
    `held_classes.v0.json`)
  * `test_held_class_enumeration_single_source` invariant gate

Any change here must be reflected in the mirror JSON + gate simultaneously.
"""
from __future__ import annotations

import os
from typing import Literal, Optional, Tuple


HeldClassName = Literal["ledger_row", "wizard_transcript", "delivered_artifact"]

# LOAD-BEARING: this tuple order is the deterministic render order for
# v2.1 §4.3 held-class regions. Tests parametrise over this tuple.
HELD_CLASSES: Tuple[HeldClassName, ...] = (
    "ledger_row",
    "wizard_transcript",
    "delivered_artifact",
)


# Per-class explicit retention env-var pattern (dev default).
# Master Admin / DPO would set these via a controlled write path at
# B-5b (rulebook writes). At B-5a (read/prove), we READ them.
_PER_CLASS_ENV_PATTERN = "AKKI_COMPLIANCE_RETENTION_{class_upper}_DAYS"


def global_default_days() -> Optional[int]:
    """Global retention default in days. Owner E5 inheritance-as-default:
    unless a class is explicitly split, it inherits from this."""
    raw = os.environ.get("AKKI_NORTHENA_LEDGER_RETENTION_WINDOW_DAYS")
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def explicit_days_for_class(class_name: HeldClassName) -> Optional[int]:
    """Per-class explicit retention days, or None if not explicitly set."""
    env_key = _PER_CLASS_ENV_PATTERN.format(class_upper=class_name.upper())
    raw = os.environ.get(env_key)
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


PostureName = Literal["inheriting", "explicit", "unset"]


def resolve_posture(class_name: HeldClassName) -> Tuple[PostureName, Optional[int]]:
    """Resolve (posture, effective_days) for a held-class per Owner E5.

    Semantics:
      * `explicit` — class has its own env-var set; days field is authoritative.
      * `inheriting` — global_default is set AND class does not have its
        own env-var; days field mirrors global_default.
      * `unset` — no global_default AND no class-specific setting; days is None.
        This is the B5a-G3 substrate — "retention-unset states honestly".
    """
    class_days = explicit_days_for_class(class_name)
    if class_days is not None:
        return "explicit", class_days
    global_days = global_default_days()
    if global_days is not None:
        return "inheriting", global_days
    return "unset", None
