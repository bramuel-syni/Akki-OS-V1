"""Phase 8 Stage B-4 — Read-only seam-pending enumeration.

Owner ratification (verbatim, 2026-07-05):
    "The system already HAS real pending decisions — the gated-closed seams
     awaiting owner/DPO/MEA values. Five exist today: Targeta yield
     thresholds, Mtafiti V3 thresholds, retention window, cumulative-
     disclosure envs, MEA source-standing table. That is literally what
     the approved §6.1 mockup rendered."

Derivation source: env-presence + config-presence check per seam.
Every seam whose gating value has NOT landed is included in the pending
enumeration. Seams whose values HAVE landed are excluded.

Zero ledger integration — this is a read-only projection of
config-presence state, not a change event.
"""
from __future__ import annotations

import os
from typing import Dict, List


def _has_env(*var_names: str) -> bool:
    """True iff ALL named env vars are set to a non-empty value."""
    return all(bool(os.environ.get(n)) for n in var_names)


def _pending_targeta_yield_thresholds() -> Dict[str, str]:
    if _has_env(
        "AKKI_TARGETA_MIN_EFFICIENCY_GAIN",
        "AKKI_TARGETA_COVERAGE_ALPHA",
        "AKKI_TARGETA_HELD_OUT_SET_COMPOSITION",
    ):
        return {}
    return {
        "seam_id": "targeta_yield_thresholds",
        "plain_language_line": "Targeta yield thresholds — awaiting Owner values",
        "awaiting_whom": "owner",
        "seam_status": "closed",
    }


def _pending_mtafiti_v3_thresholds() -> Dict[str, str]:
    if _has_env(
        "AKKI_MTAFITI_V3_FACT_PRECISION",
        "AKKI_MTAFITI_V3_GENRE_ACCURACY",
        "AKKI_MTAFITI_V3_INTER_ANNOTATOR_FLOOR",
    ):
        return {}
    return {
        "seam_id": "mtafiti_v3_thresholds",
        "plain_language_line": "Mtafiti V3 thresholds — awaiting Owner values",
        "awaiting_whom": "owner",
        "seam_status": "closed",
    }


def _pending_retention_window() -> Dict[str, str]:
    # DPO decision — northena ledger retention window duration.
    mode = os.environ.get("AKKI_NORTHENA_LEDGER_RETENTION_MODE", "indefinite")
    if mode != "indefinite":
        return {}
    return {
        "seam_id": "northena_retention_window",
        "plain_language_line": "Northena ledger retention window — awaiting DPO decision",
        "awaiting_whom": "dpo",
        "seam_status": "closed",
    }


def _pending_cumulative_disclosure_envs() -> Dict[str, str]:
    if _has_env(
        "AKKI_G6_K_ANONYMITY_THRESHOLD",
        "AKKI_G6_L_DIVERSITY_THRESHOLD",
        "AKKI_G6_DP_EPSILON_BUDGET",
    ):
        return {}
    return {
        "seam_id": "v2_cumulative_disclosure_envs",
        "plain_language_line": "V2 cumulative-disclosure thresholds (k-anonymity / l-diversity / DP epsilon) — awaiting DPO decision",
        "awaiting_whom": "dpo",
        "seam_status": "closed",
    }


def _pending_mea_source_standing() -> Dict[str, str]:
    # MEA source-standing table — if env var pointing to a real table
    # is set, seam is open. Absent → pending.
    if _has_env("AKKI_MEA_SOURCE_STANDING_TABLE_PATH"):
        return {}
    return {
        "seam_id": "mea_source_standing_table",
        "plain_language_line": "MEA source-standing table — awaiting MEA editorial-authority values",
        "awaiting_whom": "mea",
        "seam_status": "closed",
    }


def enumerate_pending_seams() -> List[Dict[str, str]]:
    """Return the ordered list of currently-pending seams.

    Ordering matches §6.1 mockup precedent (Targeta first, then Mtafiti,
    then retention, then cumulative-disclosure, then MEA). Empty list is
    a legitimate state (all seams landed) — the banner then collapses to
    the "nothing pending" empty state per §6.1 sentence-only rule.
    """
    candidates = [
        _pending_targeta_yield_thresholds(),
        _pending_mtafiti_v3_thresholds(),
        _pending_retention_window(),
        _pending_cumulative_disclosure_envs(),
        _pending_mea_source_standing(),
    ]
    return [c for c in candidates if c]
