"""Phase 8 Seam 3 Sub-stage 2 — retention-config write service.

Owner ruling (Stage A §5.1): retention-config write half. Loads current
config (or defaults to v0 with all-null windows), validates DPO write
payload, persists as `retention.vN.json` (versioned; append-only version
bumps). Also emits a `NorthenaLedgerRow_v1` for the write itself
(governance-audit trail).

E2 binding condition (Amendment F rulings §10; Stage A §5.1 line 238):
  Loosening writes are REFUSED with 403 access-control class body
  citing `awaiting_consequence_class_checker` until Sub-stage 3 checker
  lands. Tightening writes are ACCEPTED (unilateral-with-delay is a
  Sub-stage 3 concern).

E5 (4-code auth registry closed): the 403 refusal reuses
  `auth_scope_insufficient` as the top-level reason (the closed code)
  and carries `awaiting_consequence_class_checker:` as a detail prefix
  the LB gate asserts on.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

from services.compliance.held_class_registry import HELD_CLASSES, HeldClassName

_CONFIG_DIR = Path(__file__).parent  # writes retention.vN.json next to retention.v0.json


@dataclass
class WriteAttempt:
    """Result of a retention-config write attempt.

    Owner ruling §10 R-5-adjacent: emission-order for the ledger event
    (write half) is emit AFTER on-disk persist — because the persist IS
    the semantic write; the ledger row records that write happened.
    (Contrast with I5/I6 refusal emission where write-ahead is required
    for undercount-elimination.) The retention config write flow has
    no async retry crash class; a crash between persist + ledger emit
    is recoverable by rerun.
    """

    outcome: str  # "loosening_refused" | "accepted_tightening" | "accepted_setting_from_unset"
    old_version: int
    new_version: int
    persisted_path: Optional[str]  # None if refused
    old_window_days_per_class: dict
    new_window_days_per_class: dict
    refusal_detail: Optional[str] = None  # populated when outcome=="loosening_refused"


class LoosengingRefused(Exception):
    """Loosening/lengthening write refused (E2 binding). Carries the
    detail string the router encodes into the 403 body."""

    def __init__(self, *, detail: str, attempt: WriteAttempt):
        super().__init__(detail)
        self.detail = detail
        self.attempt = attempt


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _latest_config_path_and_version() -> Tuple[Path, int]:
    """Scan `_CONFIG_DIR` for the highest retention.vN.json version.

    Fresh-install fallback: v0 is landed alongside the module at
    Sub-stage 2 landing; if nothing found we return (v0 path, 0)
    which will fail-fast on read if v0 is missing.
    """
    latest_v = -1
    latest_path = _CONFIG_DIR / "retention.v0.json"
    for entry in _CONFIG_DIR.glob("retention.v*.json"):
        stem = entry.stem  # e.g. "retention.v3"
        try:
            v = int(stem.split(".v", 1)[1])
        except (IndexError, ValueError):
            continue
        if v > latest_v:
            latest_v = v
            latest_path = entry
    return latest_path, max(latest_v, 0)


def read_current_config() -> Tuple[dict, int]:
    """Read the latest retention.vN.json + return (config_dict, N)."""
    path, version = _latest_config_path_and_version()
    with path.open("r", encoding="utf-8") as f:
        return json.load(f), version


def _is_loosening(old_days: Optional[int], new_days: Optional[int]) -> bool:
    """Loosening = window LENGTHENS (or int → null on already-set class).

    Per Stage A §5.1 line 246:
      - `window_days` increase → loosening
      - `int → null` transition on already-set class → loosening
    """
    if old_days is None and new_days is None:
        return False
    if old_days is not None and new_days is None:
        return True  # int → null: removes finite retention (data now indefinite).
    if old_days is None and new_days is not None:
        return False  # null → int: adds finite retention. Tightening.
    return int(new_days) > int(old_days)  # both int; larger new = loosening.


def _classify(old_days: Optional[int], new_days: Optional[int]) -> str:
    """Classify a per-class window_days delta.

    Returns one of:
      - "unchanged" — new_days == old_days (no write needed for this class)
      - "loosening" — window lengthens (refused pre-checker)
      - "tightening" — window shortens (accepted at Sub-stage 2)
      - "setting_from_unset" — old was null, new is int (tightening subclass)
    """
    if old_days == new_days:
        return "unchanged"
    if _is_loosening(old_days, new_days):
        return "loosening"
    if old_days is None and new_days is not None:
        return "setting_from_unset"
    return "tightening"


def _validate_payload(payload: dict) -> dict:
    """Extract + validate the per-class window_days from the write payload.

    Payload shape: `{held_class_name: {window_days: int|null}, ...}`.
    Any subset of the 3 held-classes is acceptable (partial write).
    Unknown keys are rejected fail-fast (transcription safety).
    """
    if not isinstance(payload, dict):
        raise ValueError("payload MUST be a dict of {held_class: {window_days:int|null}}")
    result = {}
    for key, value in payload.items():
        if key not in HELD_CLASSES:
            raise ValueError(
                f"unknown held_class {key!r}; must be one of {list(HELD_CLASSES)}"
            )
        if not isinstance(value, dict) or "window_days" not in value:
            raise ValueError(
                f"payload[{key!r}] must be a dict with a 'window_days' field"
            )
        window_days = value["window_days"]
        if window_days is not None:
            if not isinstance(window_days, int):
                raise ValueError(
                    f"payload[{key!r}].window_days must be int|null, got {type(window_days).__name__}"
                )
            if window_days <= 0:
                raise ValueError(
                    f"payload[{key!r}].window_days must be positive; got {window_days}"
                )
        result[key] = window_days
    return result


async def write_retention_config(
    *, payload: dict, actor_user_id: str, actor_email: str,
) -> WriteAttempt:
    """Attempt to persist a retention-config write.

    E2 binding: any loosening in the payload REFUSES THE ENTIRE WRITE
    (transactional — no partial persist). Tightening writes persist to
    retention.v{N+1}.json.

    Raises:
        LoosengingRefused if any per-class delta is a loosening. The
        exception carries a WriteAttempt with outcome="loosening_refused"
        (no ledger row emitted — E2 gate assertion).
        ValueError on payload validation failure.
    """
    parsed = _validate_payload(payload)
    current, old_version = read_current_config()
    old_per_class = {
        cls: current["held_classes"][cls]["window_days"] for cls in HELD_CLASSES
    }
    new_per_class = dict(old_per_class)
    outcomes = {}
    for cls, new_days in parsed.items():
        cls_outcome = _classify(old_per_class[cls], new_days)
        outcomes[cls] = cls_outcome
        new_per_class[cls] = new_days

    # E2 refusal — any loosening refuses the ENTIRE write.
    loosening_classes = [c for c, o in outcomes.items() if o == "loosening"]
    if loosening_classes:
        attempt = WriteAttempt(
            outcome="loosening_refused",
            old_version=old_version,
            new_version=old_version,  # unchanged; nothing persisted
            persisted_path=None,
            old_window_days_per_class=old_per_class,
            new_window_days_per_class=new_per_class,
            refusal_detail=(
                f"awaiting_consequence_class_checker: retention window "
                f"loosening refused pre-Sub-stage-3-checker for classes "
                f"{sorted(loosening_classes)}. Tightening (shortening window_days "
                "or null→int transition) is accepted unilaterally at Sub-stage 2; "
                "loosening (lengthening window_days or int→null transition) "
                "requires the Sub-stage 3 checker countersign path (not yet landed). "
                "See Amendment F rulings §10 + Stage A §5.1."
            ),
        )
        raise LoosengingRefused(detail=attempt.refusal_detail, attempt=attempt)

    # Determine outcome label for the accepted case.
    if any(o == "setting_from_unset" for o in outcomes.values()) and not any(
        o == "tightening" for o in outcomes.values()
    ):
        write_outcome = "accepted_setting_from_unset"
    else:
        write_outcome = "accepted_tightening"

    new_version = old_version + 1
    new_config = {
        "$comment": (
            f"Retention config v{new_version} — persisted by {actor_email} at "
            f"{_now_iso()}. E2-accepted write (tightening only per Sub-stage 2 "
            "binding condition). Append-only immutable snapshot."
        ),
        "version": new_version,
        "created_at": _now_iso(),
        "created_by": actor_user_id,
        "held_classes": {
            cls: {
                "window_days": new_per_class[cls],
                "set_by": (actor_user_id if outcomes.get(cls) in (
                    "tightening", "setting_from_unset",
                ) else current["held_classes"][cls]["set_by"]),
                "set_at": (_now_iso() if outcomes.get(cls) in (
                    "tightening", "setting_from_unset",
                ) else current["held_classes"][cls]["set_at"]),
            }
            for cls in HELD_CLASSES
        },
    }

    new_path = _CONFIG_DIR / f"retention.v{new_version}.json"
    with new_path.open("w", encoding="utf-8") as f:
        json.dump(new_config, f, indent=2)
        f.write("\n")

    return WriteAttempt(
        outcome=write_outcome,
        old_version=old_version,
        new_version=new_version,
        persisted_path=str(new_path),
        old_window_days_per_class=old_per_class,
        new_window_days_per_class=new_per_class,
    )
