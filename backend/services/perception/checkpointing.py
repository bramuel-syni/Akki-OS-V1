"""Checkpointing helpers (V1-B2). Kill-and-restart resumes cleanly."""
from __future__ import annotations

from typing import Dict, List

from contracts.perception_result_v0 import Checkpoint


def build_checkpoint(offset_s: int, completed_ids: List[str]) -> Checkpoint:
    return Checkpoint(last_completed_offset_s=offset_s, completed_unit_ids=completed_ids)


def merge_checkpoint(prior: Dict, incoming: Dict) -> Dict:
    """Merge two checkpoint dicts. Returns the greater offset + de-duped ids."""
    prior_ids = list(prior.get("completed_unit_ids", []) or [])
    incoming_ids = list(incoming.get("completed_unit_ids", []) or [])
    merged_ids = list(dict.fromkeys(prior_ids + incoming_ids))
    merged_offset = max(prior.get("last_completed_offset_s", 0),
                        incoming.get("last_completed_offset_s", 0))
    return {"last_completed_offset_s": merged_offset, "completed_unit_ids": merged_ids}
