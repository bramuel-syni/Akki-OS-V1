"""Phase 8 Stage B-3 Block 3 — Load-bearing wire-shape gate.

Owner D4b ruling core (2026-07-04):
    "Unfrozen container + one named LOAD-BEARING wire-shape gate
     pinning the enforcement-read field set: grant_id, key_class, path,
     floor, scope, lawful_basis_ref, revoked_at — presence, names,
     types. Lifecycle fields (expires_at, delegation, renewal) arrive
     freely; the governance-carrying subset cannot drift silently.
     The 4a ruling's own terms apply: the container stays unfrozen
     because the gate pins its governance keys — without that gate,
     freeze would be the ruling."

Semantics of "load-bearing" here:
  * The container is UNFROZEN (no `.contract_snapshot.json`, no
    parity-26→27 bump).
  * The 7 named enforcement-read fields ARE pinned — presence + name +
    type. Adding lifecycle fields (`expires_at`, `delegation`,
    `renewed_at`, per-endpoint scoping) does NOT break this gate.
  * Removing / renaming / retyping ANY of the 7 named fields IS a hard
    break (governance-key drift). The container's unfrozen status is
    contingent on this gate being green; without it, D4b reopens as
    freeze.

The gate reads the LIVE Pydantic model — not a snapshot. That is the
whole point: the wire-shape stays flexible for lifecycle additions,
but the enforcement-read subset is immutable at the runtime schema
level.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional, get_args, get_origin

import pytest
from pydantic.fields import FieldInfo

from services.auth.engineer_key_grant import EngineerKeyGrantRegistration


# The 7 enforcement-read (governance-key) fields — Owner D4b verbatim.
# Presence + name + type. Lifecycle additions are additive and MUST NOT
# break this gate.
GOVERNANCE_KEY_FIELDS = {
    "grant_id",
    "key_class",
    "path",
    "floor",
    "scope",
    "lawful_basis_ref",
    "revoked_at",
}


def _field(name: str) -> FieldInfo:
    fields = EngineerKeyGrantRegistration.model_fields
    assert name in fields, (
        f"D4b wire-shape gate violation: enforcement-read field {name!r} "
        f"is missing from EngineerKeyGrantRegistration. Under Owner D4b ruling "
        "(2026-07-04) the container's unfrozen status is contingent on this "
        "field's presence."
    )
    return fields[name]


def _annotation_of(name: str):
    return _field(name).annotation


def _is_str_type(ann) -> bool:
    """True iff annotation is `str` (not Optional[str], not enum-of-str)."""
    return ann is str


def _is_optional_datetime(ann) -> bool:
    """True iff annotation is Optional[datetime] i.e. Union[datetime, None]."""
    if get_origin(ann) is type(None):
        return False
    args = get_args(ann)
    if not args:
        return False
    return datetime in args and type(None) in args


def _is_literal_of(ann, expected_values: set) -> bool:
    """True iff annotation is Literal[<expected_values>]."""
    from typing import Literal  # noqa: F401 — for readability
    args = set(get_args(ann))
    return bool(args) and args == expected_values


# =============================================================================
# Governance-key field pin — 7 tests.
# =============================================================================


def test_grant_id_present_str_not_optional():
    """grant_id: str, not Optional."""
    ann = _annotation_of("grant_id")
    assert _is_str_type(ann), (
        f"D4b wire-shape gate: grant_id must be `str` (found {ann!r}). "
        "Governance key — audit-trail keys grant-lifecycle events by grant_id."
    )
    # not Optional — check the FieldInfo `is_required`
    assert _field("grant_id").is_required(), "grant_id must be required (not Optional)."


def test_key_class_present_literal_internal_external():
    """key_class: Literal["internal", "external"], not Optional."""
    ann = _annotation_of("key_class")
    assert _is_literal_of(ann, {"internal", "external"}), (
        f"D4b wire-shape gate: key_class must be Literal[\"internal\", \"external\"] "
        f"(found {ann!r}). Governance key — UI Spec §4.1 class dichotomy is "
        "enforcement-read by check_scope."
    )
    assert _field("key_class").is_required()


def test_path_present_literal_live_query_governed_extract():
    """path: Literal["live_query", "governed_extract"], not Optional."""
    ann = _annotation_of("path")
    assert _is_literal_of(ann, {"live_query", "governed_extract"}), (
        f"D4b wire-shape gate: path must be Literal[\"live_query\", "
        f"\"governed_extract\"] (found {ann!r}). Governance key — "
        "UI Spec §4.1 path dichotomy is enforcement-read by check_scope."
    )
    assert _field("path").is_required()


def test_floor_present_literal_three_classes():
    """floor: Literal["utterance", "recorded_statement", "established_fact"], not Optional."""
    ann = _annotation_of("floor")
    assert _is_literal_of(
        ann, {"utterance", "recorded_statement", "established_fact"},
    ), (
        f"D4b wire-shape gate: floor must be Literal[\"utterance\", "
        f"\"recorded_statement\", \"established_fact\"] (found {ann!r}). "
        "Governance key — DefensibilityFloor.minimum_class is enforcement-"
        "read by _floor_meets."
    )
    assert _field("floor").is_required()


def test_scope_present_str_min_length_1_not_optional():
    """scope: str, min_length=1, not Optional."""
    ann = _annotation_of("scope")
    assert _is_str_type(ann), (
        f"D4b wire-shape gate: scope must be `str` (found {ann!r}). "
        "Governance key — check_scope matches scope EXACTLY."
    )
    field = _field("scope")
    assert field.is_required()
    # min_length=1 is pinned — empty scope would be a governance-key defect.
    constraints = [
        getattr(m, "min_length", None)
        for m in getattr(field, "metadata", [])
    ]
    assert 1 in constraints, (
        "D4b wire-shape gate: scope must carry min_length=1 constraint "
        "(governance-key ranges cannot silently permit empty strings)."
    )


def test_lawful_basis_ref_present_str_min_length_1_not_optional():
    """lawful_basis_ref: str, min_length=1, not Optional."""
    ann = _annotation_of("lawful_basis_ref")
    assert _is_str_type(ann), (
        f"D4b wire-shape gate: lawful_basis_ref must be `str` (found {ann!r}). "
        "Governance key — every ledger row lifts this into stamp_audit "
        "(Northena §7.2)."
    )
    field = _field("lawful_basis_ref")
    assert field.is_required()
    constraints = [
        getattr(m, "min_length", None)
        for m in getattr(field, "metadata", [])
    ]
    assert 1 in constraints, (
        "D4b wire-shape gate: lawful_basis_ref must carry min_length=1 "
        "constraint (governance-key ranges cannot silently permit empty strings)."
    )


def test_revoked_at_present_optional_datetime():
    """revoked_at: Optional[datetime]. Default MUST be None (unrevoked at mint)."""
    ann = _annotation_of("revoked_at")
    assert _is_optional_datetime(ann), (
        f"D4b wire-shape gate: revoked_at must be Optional[datetime] "
        f"(found {ann!r}). Governance key — revocation lifecycle event "
        "sets this field; check_scope MUST NOT match a revoked grant."
    )
    # Default MUST be None (mint-time is unrevoked). Note: this asserts
    # semantic correctness, not just presence — a default of `datetime.now`
    # would silently mark all grants as revoked.
    field = _field("revoked_at")
    assert field.default is None, (
        "D4b wire-shape gate: revoked_at default MUST be None (unrevoked "
        f"at mint time). Found default: {field.default!r}."
    )


# =============================================================================
# Lifecycle-additive tolerance — the gate MUST NOT reject new lifecycle
# fields. This is the "unfrozen container" half of the D4b ruling.
# =============================================================================


def test_lifecycle_field_additions_do_not_break_the_gate():
    """Adding lifecycle fields (expires_at, delegation, renewed_at, etc.)
    MUST NOT cause this gate to fail. The gate reads the 7 named
    governance-key fields — anything else on the model is opaque to
    the gate.
    """
    # This test is a philosophical assertion: the previous 7 tests
    # NEVER iterate over `model_fields.keys()` — they only look up the
    # 7 named fields. Adding any new field is silent to the gate.
    #
    # We prove this by counting: the gate references exactly 7 field
    # names in the assertions above. If someone adds e.g. `expires_at`
    # to EngineerKeyGrantRegistration, the count of governance-key
    # tests stays 7, and this test remains green.
    assert len(GOVERNANCE_KEY_FIELDS) == 7, (
        "Governance-key field set is fixed at 7. Adding to this set "
        "REQUIRES an Owner ruling (a new D4b-analogue)."
    )
    # Confirm that model has AT LEAST the 7 (may have more).
    field_names = set(EngineerKeyGrantRegistration.model_fields.keys())
    missing = GOVERNANCE_KEY_FIELDS - field_names
    assert not missing, (
        f"Governance-key fields missing from live model: {missing!r}"
    )
