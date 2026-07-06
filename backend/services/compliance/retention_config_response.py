"""RetentionConfigResponse Pydantic model — UNFROZEN wire shape (B-5a).

Not a frozen contract. UNFROZEN under Ruling 3 wire-shape LOAD-BEARING
gate posture at 4a Stage B; a load-bearing test at Stage B pins the
governance-key fields (class_name, posture, days per held-class row +
global_default.days).

Held-class list length is ALWAYS 3, ordered per
`services.compliance.held_class_registry.HELD_CLASSES`.
"""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class GlobalDefaultRetention(BaseModel):
    model_config = ConfigDict(extra="forbid")

    days: Optional[int] = Field(
        default=None,
        description=(
            "Global default retention window in days. None = unset — "
            "B5a-G3 substrate ('retention-unset states honestly')."
        ),
    )
    set_at: Optional[str] = Field(
        default=None,
        description="ISO-8601 timestamp when set; None if unset.",
    )
    set_by: Optional[str] = Field(
        default=None,
        description="user_id who set it; None if unset.",
    )


class HeldClassRetention(BaseModel):
    model_config = ConfigDict(extra="forbid")

    class_name: Literal["ledger_row", "wizard_transcript", "delivered_artifact"] = Field(
        ..., description="Held-class name — one of Owner E5 three.",
    )
    posture: Literal["inheriting", "explicit", "unset"] = Field(
        ...,
        description=(
            "Retention posture per class: `explicit` = class-specific "
            "window; `inheriting` = mirrors global_default; `unset` = "
            "no rule set (B5a-G3 substrate)."
        ),
    )
    days: Optional[int] = Field(
        default=None,
        description=(
            "Effective retention days. Mirrors global_default when "
            "posture=inheriting; own value when posture=explicit; None "
            "when posture=unset."
        ),
    )
    set_at: Optional[str] = Field(
        default=None,
        description="ISO-8601 timestamp when explicitly set; None otherwise.",
    )
    set_by: Optional[str] = Field(
        default=None,
        description="user_id who explicitly set it; None otherwise.",
    )


class RetentionConfigResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    global_default: GlobalDefaultRetention = Field(...)
    held_classes: List[HeldClassRetention] = Field(
        ...,
        description=(
            "Exactly 3 entries — ordered per HELD_CLASSES tuple: "
            "['ledger_row', 'wizard_transcript', 'delivered_artifact']. "
            "LOAD-BEARING ordering (v2.1 §4.3 render + tests parametrise "
            "in this order)."
        ),
    )
    resolved_at: str = Field(..., description="ISO-8601 UTC of read moment.")
