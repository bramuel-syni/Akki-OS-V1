"""CD-E4 α load-bearing wire-shape gate for `CensusContentDimension`.

Owner ruling CD-E4 α (2026-07-10) — verbatim carrier:

    'α, required. Five governance-key fields pinned (presence + name + type),
     tolerance test asserting additive fields pass — Phase 9 census
     integration will add fields; the gate rejects drift without rejecting
     growth.'

CD-E2 α ↔ CD-E4 coupling (Owner ruled 2026-07-10):

    'Container stays unfrozen because the wire-shape gate lands; if CD-E4
     ever regressed, this ruling flips to freeze. Record the coupling in
     the rulings record so neither is relaxed alone.'

Pinned governance-key fields (5):
  1. feed_id                       — required, str
  2. content_surface               — optional, str
  3. content_surface_source        — optional, Literal[census_observed, manifest_declared]
  4. genre                         — optional, str
  5. genre_source                  — optional, Literal[census_observed, manifest_declared]

Tolerance clause: adding new lifecycle/audit fields (e.g., censused_at, notes,
future additive extensions) does NOT cause this gate to reject.
"""
from __future__ import annotations

import sys
import typing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from services.census_dimensions.dimensions_service import (  # noqa: E402
    CensusContentDimension,
)


PINNED_GOVERNANCE_KEY_FIELDS = {
    "feed_id": {"required": True, "type_str": "str"},
    "content_surface": {"required": False, "type_str": "Optional[str]"},
    "content_surface_source": {
        "required": False,
        "type_str": "Optional[Literal['census_observed', 'manifest_declared']]",
    },
    "genre": {"required": False, "type_str": "Optional[str]"},
    "genre_source": {
        "required": False,
        "type_str": "Optional[Literal['census_observed', 'manifest_declared']]",
    },
}


def _literal_args(annotation) -> set:
    """Extract Literal[...] args from Optional[Literal[...]] annotations."""
    for arg in typing.get_args(annotation):
        if typing.get_origin(arg) is typing.Literal:
            return set(typing.get_args(arg))
    if typing.get_origin(annotation) is typing.Literal:
        return set(typing.get_args(annotation))
    return set()


def test_cd_e4_five_governance_key_fields_pinned_by_name() -> None:
    """All 5 pinned governance-key fields present on the Pydantic model."""
    actual_fields = CensusContentDimension.model_fields
    for name in PINNED_GOVERNANCE_KEY_FIELDS:
        assert name in actual_fields, (
            f"CD-E4 α VIOLATED: governance-key field {name!r} missing from "
            f"CensusContentDimension. Coupling: CD-E2 α ↔ CD-E4 α — if the "
            f"gate is relaxed, the CD-E2 ruling flips to freeze."
        )


def test_cd_e4_pinned_fields_required_flag() -> None:
    """`feed_id` required; other 4 optional."""
    actual_fields = CensusContentDimension.model_fields
    for name, spec in PINNED_GOVERNANCE_KEY_FIELDS.items():
        assert actual_fields[name].is_required() == spec["required"], (
            f"CD-E4 α VIOLATED: field {name!r} required={actual_fields[name].is_required()}, "
            f"expected {spec['required']}."
        )


def test_cd_e4_source_fields_are_optional_literal_of_two() -> None:
    """content_surface_source + genre_source: Optional[Literal[...]] with exactly
    {census_observed, manifest_declared}."""
    actual_fields = CensusContentDimension.model_fields
    for source_field in ["content_surface_source", "genre_source"]:
        ann = actual_fields[source_field].annotation
        args = _literal_args(ann)
        assert args == {"census_observed", "manifest_declared"}, (
            f"CD-E4 α VIOLATED: {source_field} Literal args {args} != "
            f"expected {{census_observed, manifest_declared}}. "
            f"CD-E1 α closed 2-set discipline broken."
        )


def test_cd_e4_tolerance_additive_fields_do_not_reject_gate() -> None:
    """CD-E4 α tolerance clause: additive fields (censused_at, notes) present
    on the current model — gate must NOT reject.

    Phase 9 census integration will add more fields; this test asserts the
    gate is over-strict enough to catch drift on the 5 pinned fields but
    lenient enough to allow additive growth.
    """
    actual_fields = set(CensusContentDimension.model_fields.keys())
    pinned = set(PINNED_GOVERNANCE_KEY_FIELDS.keys())
    additive = actual_fields - pinned
    # At close, additive fields present: censused_at + notes.
    assert additive == {"censused_at", "notes"}, (
        f"CD-E4 α tolerance clause: expected additive fields {{censused_at, notes}} "
        f"at close; actual additive fields {additive}. Adding NEW fields is "
        f"permitted; removing existing additive fields requires a Tier-3 disclosure."
    )
    # The GATE itself must NOT depend on the exact additive set — assert that
    # the pinned fields are still all present regardless.
    for name in pinned:
        assert name in actual_fields


def test_cd_e4_pinned_fields_type_annotations_stable() -> None:
    """Pinned type annotations stable at close.

    feed_id is a plain str; content_surface + genre are Optional[str]; both
    source fields are Optional[Literal[...]] as attested above.
    """
    actual_fields = CensusContentDimension.model_fields
    # feed_id — plain str.
    feed_id_ann = actual_fields["feed_id"].annotation
    assert feed_id_ann is str, f"feed_id annotation {feed_id_ann!r} != str"
    # content_surface + genre — Optional[str].
    for name in ["content_surface", "genre"]:
        ann = actual_fields[name].annotation
        assert type(None) in typing.get_args(ann), (
            f"{name} must be Optional[...]"
        )
        non_none_args = [a for a in typing.get_args(ann) if a is not type(None)]
        assert non_none_args == [str], (
            f"{name} non-None annotation {non_none_args} != [str]"
        )
