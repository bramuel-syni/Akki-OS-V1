"""Refusal family classifier — Amendment 2 (2026-07-06 B-5a Stage B dispatch).

Owner ruling verbatim [Owner ruling, Phase 8 Stage B-5a dispatch,
2026-07-06]:
    "The NorthenaLedgerRow_v1 source stands conditional on family-by-family
     coverage verification at Stage B: admission refusals,
     composition-below-floor, late refusals, outer-gate refusals — each
     confirmed to emit ledger rows, with evidence. The close report
     states which families the aggregate counts. Any governed-refusal
     family found un-ledgered is a FINDING in the close, never a silent
     omission — this card is the 'governance bites' evidence surface;
     undercounting there is dishonesty at the exact point honesty is
     the product. Auth 403s and validation 422s correctly excluded —
     not refusals."

This module is a PURE-FUNCTION classifier that maps a
`NorthenaLedgerRow_v1` refusal row (`decision == "refused"`) into a
governed-refusal family. It does NOT read the ledger or ask which rows
were emitted — that's the coverage statement's job (see close report
§Refusals-by-Month Coverage Statement).

Families (Owner-enumerated at dispatch):
  * `admission_refusals` — governance refusals at admission time via
    `AdmissionRefusal_v0` (v3 registry codes)
  * `composition_below_floor` — Service_1 refusals at conclusion class
    (`Service1Refusal(composition_below_floor)`; sibling of
    `no_defensibility_floor` + `no_lawful_basis`)
  * `late_refusals` — async-delivery-time refusals via
    `async_state.emit_ledger_terminate_refused` (Phase 5 §7)
  * `outer_gate_refusals` — V2 gate refusals absorbed via
    `northena.converge.absorb_v2_refusal` (reason prefixed `v2_refused:`)

Classification rules (deterministic, pure-function):
  1. If `reason` starts with `v2_refused:` → `outer_gate_refusals`
  2. Elif `reason` in SERVICE_1_REASONS → `composition_below_floor` family
     (three reasons: `composition_below_floor`, `no_defensibility_floor`,
      `no_lawful_basis`)
  3. Elif `reason` in ADMISSION_REASONS → `admission_refusals` family
  4. Else → `unclassified` (row falls outside known families; MUST be
     surfaced honestly — not silently dropped)

Note on `late_refusals`: the current ledger row shape does not carry a
distinct emission-context marker for async-worker-fired refusals vs
sync-dispatch-fired refusals — both flow through the SAME reason-code
alphabet (admission or composition-below-floor). Classification by
timing is therefore not possible from the ledger alone. In practice
"late refusals" is a TIMING context that overlays the four families
below, not a distinct family in itself. See close-report §Refusals-by-
Month Coverage Statement for the finding disposition.

Auth 403s (auth_scope_insufficient / auth_missing / auth_expired /
auth_identity_mismatch_for_wizard_session) and validation 422s are
NOT governed-refusal envelopes — they do NOT reach this classifier.
Enforcement: aggregate query filters `decision == "refused"` in the
ledger; auth denials never write to the ledger. Exclusion gate
`test_refusals_by_month_excludes_auth_403_and_validation_422` covers.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import FrozenSet, Literal, Optional


FamilyName = Literal[
    "admission_refusals",
    "composition_below_floor",
    "outer_gate_refusals",
    "unclassified",
]


# LOAD-BEARING deterministic sets — loaded ONCE at import time from
# on-disk versioned registries. `composition_below_floor` family carries
# the three Service_1-refusal reasons per docstring & registry.
_SERVICE_1_REGISTRY = Path(__file__).resolve().parents[2] / "services" / "service_1" / "service_1_refusal_reasons.v0.json"
_ADMISSION_REGISTRY = Path(__file__).resolve().parents[2] / "services" / "service_1" / "admission_refusal_reasons.v3.json"


def _load_reason_set(path: Path) -> FrozenSet[str]:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return frozenset(entry["reason"] for entry in payload.get("valid_reasons", []))


SERVICE_1_REASONS: FrozenSet[str] = _load_reason_set(_SERVICE_1_REGISTRY)
ADMISSION_REASONS: FrozenSet[str] = _load_reason_set(_ADMISSION_REGISTRY)


V2_REFUSED_PREFIX = "v2_refused:"


def classify_family(reason: str) -> FamilyName:
    """Pure-function family classifier. Given a NorthenaLedgerRow_v1's
    `reason` string (from a row where `decision == "refused"`), return
    the governed-refusal family.

    Order matters: V2 prefix check BEFORE admission-registry check
    (an admission-family reason could theoretically collide with a
    substring, though registry codes don't currently share prefixes).
    """
    if not reason:
        return "unclassified"
    if reason.startswith(V2_REFUSED_PREFIX):
        return "outer_gate_refusals"
    if reason in SERVICE_1_REASONS:
        return "composition_below_floor"
    if reason in ADMISSION_REASONS:
        return "admission_refusals"
    return "unclassified"


# Human-readable family display order (for close-report + aggregate
# response ordering; alphabetical by family name for determinism).
FAMILY_DISPLAY_ORDER = (
    "admission_refusals",
    "composition_below_floor",
    "outer_gate_refusals",
    "unclassified",
)
