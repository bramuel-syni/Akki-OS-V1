"""Synisense Phase A — service config.

Holds:
- `SYNISENSE_MASTER_SECRET` resolution (env var, with dev fallback + STARTUP WARNING)
- Allow-listed purposes (initial Phase A set)
- Latency budgets
- Environment flag for dev-only routes

The structure here is locked by the user-approved Phase A brief. No
runtime config changes; settings are read once at import time.
"""
from __future__ import annotations

import logging
import os
import secrets

log = logging.getLogger("synisense.config")

# ─────────────────────────────────────────────────────────────────────
# Master secret resolution.
#
# Production MUST set SYNISENSE_MASTER_SECRET to a stable, high-entropy
# value (at least 32 bytes of base64 / hex). Per-tenant HMAC keys are
# derived via HKDF from this master secret with `tenant_id` as the
# info parameter (see `shield/trust_receipt.py`).
#
# If the env var is missing we generate a dev-only ephemeral secret and
# log a STARTUP WARNING in caps. Restarts will rotate the dev secret
# and invalidate every receipt signed with the previous one — which is
# the whole point of warning loudly.
# ─────────────────────────────────────────────────────────────────────
_DEV_FALLBACK_GENERATED = False


def _resolve_master_secret() -> bytes:
    global _DEV_FALLBACK_GENERATED
    raw = os.environ.get("SYNISENSE_MASTER_SECRET", "").strip()
    if raw:
        return raw.encode("utf-8")
    _DEV_FALLBACK_GENERATED = True
    dev_secret = secrets.token_bytes(32)
    log.warning(
        "*** STARTUP WARNING *** SYNISENSE_MASTER_SECRET ENV VAR IS NOT SET. "
        "USING AN EPHEMERAL DEV-ONLY SECRET. ALL TRUST RECEIPT SIGNATURES "
        "WILL BE INVALIDATED ON RESTART. DO NOT SHIP THIS CONFIGURATION "
        "TO PRODUCTION."
    )
    return dev_secret


MASTER_SECRET: bytes = _resolve_master_secret()


def is_dev_fallback_active() -> bool:
    """Test/admin probe — True iff the master secret came from the
    dev fallback (env var absent)."""
    return _DEV_FALLBACK_GENERATED


# ─────────────────────────────────────────────────────────────────────
# Purpose catalogue — SHAVED at IF-1 close (2026-07-14).
#
# Superseding citation: `docs/audits/deviation_audit_v1.md` row 5
# (`services/synisense/shield/purpose_validator.py` shaved as chain-dead
# behind row 1 `client.py`). The chokepoint-at-`llm_router.invoke_with_metering`
# reconnection does not route through the purpose gate; ALLOWED_PURPOSES +
# INTERNAL_ONLY_PURPOSE_PREFIXES had no remaining consumer, so both are
# shaved together with `purpose_validator`.
#
# The chat.* legacy entries (cousin's vocabulary — chat.session.summarise,
# chat.streaming.standard_response, chat.standard_response, chat.fm_a.*,
# chat.fm_b.*, chat.fm_c.*, chat.refusal.compose, chat.*) were the specific
# prune target named in the Owner amendment 2026-07-12 §3 "Legacy purpose
# catalogue". Since the entire catalogue module shaves, the prune lands as
# a delete-with-citation per the amendment's disclosed vehicle branch.
# ─────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────
# Latency budgets (informational — surfaced in metrics).
#
# Regex pass <5ms, LLM-NER <2000ms, full Shield invoke median <300ms
# overhead (LLM provider call is excluded from the overhead measure).
# ─────────────────────────────────────────────────────────────────────
LATENCY_BUDGET_REGEX_MS: int = 5
LATENCY_BUDGET_LLM_NER_MS: int = 2000
LATENCY_BUDGET_SHIELD_TOTAL_MS: int = 300

# ─────────────────────────────────────────────────────────────────────
# Environment — gates dev-only routes such as /engine/admin/reseed.
# ─────────────────────────────────────────────────────────────────────
ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development").lower()


def is_production() -> bool:
    return ENVIRONMENT == "production"
