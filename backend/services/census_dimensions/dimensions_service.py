"""Census-dimensions sidecar service (Owner CD-E1..CD-E4 α · 2026-07-10).

Owner ruling CD-E1 α + symmetric contradiction (2026-07-10) — verbatim carrier:

    'α, contradiction validator made symmetric. The proposal rejects
     value-null + source-present; the mirror is the real fabrication risk
     and must also reject: value present + source null. Rule: value and
     source present together or absent together; either lone state fails
     validation. β rejected — a required "unknown" label fabricates a
     value to represent absence.'

Owner ruling CD-E2 α ↔ CD-E4 coupling (2026-07-10) — verbatim carrier:

    'α, explicitly coupled to CD-E4. Per the B-3 D4b package: the container
     stays unfrozen because the wire-shape gate lands; if CD-E4 ever
     regressed, this ruling flips to freeze. Record the coupling in the
     rulings record so neither is relaxed alone. Parity stays 31.'

Landing:
  * `CensusContentDimension` — Pydantic model, runtime validator, UNFROZEN
    (parity 31 preserved). NOT a frozen wire contract (no snapshot). Load-
    bearing wire-shape gate (CD-E4 α) pins 5 governance-key fields.
  * `record_census_dimension(...)` — register-before-validate for
    census_observed values; hard fail for manifest_declared values that are
    not in the current registry.
  * `read_census_dimensions_for_feed(feed_id)` — read sidecar record.
  * `list_registry(kind)` — return current registry vocabulary.

MongoDB collection: `census_content_dimensions` with unique index on `feed_id`.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, ConfigDict, model_validator

from core import db as _default_db
from .dimensions_loader import (
    RegistryKind,
    load_registry,
    register_observation,
    validate_content_surface,
    validate_genre,
)

COLLECTION = "census_content_dimensions"

SourceLiteral = Literal["census_observed", "manifest_declared"]


class CensusContentDimension(BaseModel):
    """Sidecar record for census-observed content dimensions on a feed.

    UNFROZEN (Owner CD-E2 α ↔ CD-E4 coupling): container stays runtime
    Pydantic because the load-bearing wire-shape gate lands. If CD-E4 ever
    regresses, this ruling flips to freeze. Parity 31 preserved (no snapshot).

    Symmetric contradiction validator (Owner CD-E1 α):
        value and source present together or absent together;
        either lone state fails validation.
    """

    model_config = ConfigDict(extra="forbid")

    feed_id: str
    content_surface: Optional[str] = None
    content_surface_source: Optional[SourceLiteral] = None
    genre: Optional[str] = None
    genre_source: Optional[SourceLiteral] = None
    censused_at: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def _symmetric_contradiction(self) -> "CensusContentDimension":
        # CD-E1 α: value + source present together or absent together.
        for value_field, source_field in [
            ("content_surface", "content_surface_source"),
            ("genre", "genre_source"),
        ]:
            v = getattr(self, value_field)
            s = getattr(self, source_field)
            v_present = v is not None
            s_present = s is not None
            if v_present != s_present:
                raise ValueError(
                    f"CD-E1 α symmetric contradiction: {value_field}={v!r} + "
                    f"{source_field}={s!r} — value and source must be present "
                    f"together or absent together; either lone state fails "
                    f"validation. β 'unknown' label rejected — fabricates a "
                    f"value to represent absence."
                )
        return self


def _apply_register_before_validate(
    value: Optional[str],
    source: Optional[SourceLiteral],
    kind: RegistryKind,
) -> None:
    """CD-E3 α register-before-validate for census_observed; hard fail otherwise.

    * source == "census_observed" and value not in registry → bump v(N)→v(N+1),
      then validate against v(N+1).
    * source == "manifest_declared" and value not in registry → hard fail
      (ValueError; 'a manifest cannot invent vocabulary, only observation can').
    * source is None and value is None → nothing to do (symmetric absence).
    * source is None and value is present → CD-E1 will have already raised
      before this point.
    """
    if value is None:
        return
    if source == "census_observed":
        # Register-before-validate: additive bump if novel, then validate.
        current_vocab = load_registry(kind)
        if value not in current_vocab:
            register_observation(kind, value)
    # Runtime validator: check against now-current registry.
    if kind == "content_surfaces":
        validate_content_surface(value)
    else:
        validate_genre(value)


async def record_census_dimension(
    db: AsyncIOMotorDatabase = None,
    *,
    feed_id: str,
    content_surface: Optional[str] = None,
    content_surface_source: Optional[str] = None,
    genre: Optional[str] = None,
    genre_source: Optional[str] = None,
    censused_at: Optional[str] = None,
    notes: Optional[str] = None,
) -> CensusContentDimension:
    """Write a sidecar record for one feed_id.

    Order of operations (CD-E1..CD-E4 rulings):
      1. Construct Pydantic model → CD-E1 symmetric contradiction check.
      2. Register-before-validate for census_observed novel values (CD-E3 α).
      3. Runtime validate against current registry (hard fail for
         manifest_declared novel values).
      4. Upsert into MongoDB by feed_id (idempotent by feed_id).
    """
    if db is None:
        db = _default_db
    record = CensusContentDimension(
        feed_id=feed_id,
        content_surface=content_surface,
        content_surface_source=content_surface_source,
        genre=genre,
        genre_source=genre_source,
        censused_at=censused_at or datetime.now(timezone.utc).isoformat(),
        notes=notes,
    )
    # CD-E3 α register-before-validate — content_surface + genre independently.
    _apply_register_before_validate(
        record.content_surface, record.content_surface_source, "content_surfaces"
    )
    _apply_register_before_validate(record.genre, record.genre_source, "genres")
    # Upsert by feed_id (unique index).
    await db[COLLECTION].update_one(
        {"feed_id": record.feed_id},
        {"$set": record.model_dump()},
        upsert=True,
    )
    return record


async def read_census_dimensions_for_feed(
    db: AsyncIOMotorDatabase = None, *, feed_id: str
) -> Optional[CensusContentDimension]:
    """Return the sidecar record for a feed_id, or None if not present."""
    if db is None:
        db = _default_db
    doc = await db[COLLECTION].find_one({"feed_id": feed_id})
    if doc is None:
        return None
    doc.pop("_id", None)
    return CensusContentDimension.model_validate(doc)


def list_registry(kind: RegistryKind) -> Dict[str, Any]:
    """Return current registry vocabulary for `kind`."""
    from .dimensions_loader import current_registry_version

    n, vocab = current_registry_version(kind)
    return {"kind": kind, "version": f"v{n}", "vocabulary": list(vocab)}
