"""Phase 8 Stage B-1 — Identity model.

Identity is the auth boundary primitive (federation-forward: JWT claims
today; OAuth-fronted claims later share this shape). The frozen
contracts at parity 26 are UNTOUCHED; Identity is an unfrozen
service-layer Pydantic model per Ruling 3.

Roles enumerate the six UI Spec v1 surfaces + the anonymous / admin
edges. Roles are additive: a user may hold multiple roles (e.g.,
operator+engineer). Scope enforcement reads roles + key_grants; the
JWT carries both.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# Roles are additive; a user carries a list of roles. Anonymous is
# implicit (absent user); admin is orthogonal to the six surface roles.
RoleName = Literal[
    "operator",
    "engineer",
    "buyer",
    "master_admin",
    "dpo",
    "ask_console_user",
    "admin",
    "external_engineer",
]


class KeyGrant(BaseModel):
    """A single scope grant, per UI Spec §4.1 key-grants panel.

    Every governed endpoint verifies the {class, path, floor, scope}
    tuple server-side per call (Owner E1 scope condition). The scope
    check runs inside the router handler AND is visible to the response
    envelope. `class` mirrors UI Spec §4.1's Internal / External
    dichotomy; `path` mirrors the Live query / Governed extract
    dichotomy; `floor` is the DefensibilityFloor minimum_class; `scope`
    is a free-form estate identifier.
    """

    model_config = ConfigDict(extra="forbid")

    grant_id: str = Field(..., description="Deterministic grant identifier.")
    key_class: Literal["internal", "external"] = Field(
        ..., description="UI Spec §4.1 class dichotomy."
    )
    path: Literal["live_query", "governed_extract"] = Field(
        ..., description="UI Spec §4.1 path dichotomy."
    )
    floor: str = Field(
        ...,
        description=(
            "DefensibilityFloor.minimum_class (e.g., 'utterance', "
            "'recorded_statement', 'established_fact')."
        ),
    )
    scope: str = Field(
        ..., description="Estate scope identifier (free-form; matched exact)."
    )


class Identity(BaseModel):
    """The authenticated caller's identity.

    Populated from JWT decode. Backed by a Mongo `users` document. The
    `password_hash` field NEVER leaves this module — `user_store.py`
    strips it before returning Identity out.
    """

    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(..., description="Mongo _id as string.")
    email: str = Field(..., description="Lowercased email.")
    name: Optional[str] = None
    roles: List[RoleName] = Field(default_factory=list)
    key_grants: List[KeyGrant] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
