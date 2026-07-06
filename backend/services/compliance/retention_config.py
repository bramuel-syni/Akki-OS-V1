"""Retention config read service (v2.1 §4.3 substrate; B-5a).

Builds a `RetentionConfigResponse` from environment variables read
through the held-class registry. This is the READ-ONLY half of the
retention/rights surface; write mechanics are B-5b (§4.4-4.5).

Semantics per Owner E5 (2026-07-04):
  * three classes separately addressable
  * inheritance-as-default
  * "retention-unset states honestly" (B5a-G3)
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from services.compliance.retention_config_response import (
    GlobalDefaultRetention,
    HeldClassRetention,
    RetentionConfigResponse,
)
from services.compliance import held_class_registry


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_retention_config() -> RetentionConfigResponse:
    """Pure-function read (no I/O to Mongo; env-driven at B-5a).

    B-5b (rulebook writes) will replace the env-var read with a
    versioned config path anchored in the ledger. B-5a shape is fixed
    now so the render surface can consume it byte-stable.
    """
    global_days = held_class_registry.global_default_days()
    global_default = GlobalDefaultRetention(
        days=global_days,
        set_at=None,   # env-driven at B-5a; ledger-versioned at B-5b
        set_by=None,
    )
    held_classes = []
    for class_name in held_class_registry.HELD_CLASSES:
        posture, days = held_class_registry.resolve_posture(class_name)
        held_classes.append(HeldClassRetention(
            class_name=class_name,
            posture=posture,
            days=days,
            set_at=None if posture != "explicit" else None,
            set_by=None if posture != "explicit" else None,
        ))
    return RetentionConfigResponse(
        global_default=global_default,
        held_classes=held_classes,
        resolved_at=_now_iso(),
    )
