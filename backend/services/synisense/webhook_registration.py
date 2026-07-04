"""SyniSense webhook-registration surface — Phase 5 Stage B (Owner Ruling 3).

Purpose:
  * Per-app webhook_url + HMAC signing secret derivation surface.
  * Per-app secret derived via HKDF-lite from `SYNISENSE_MASTER_SECRET`
    (see `services/synisense/config.py`) with `app_id` as info parameter.

Registration model — thin at Stage B:
  * Registration itself (persistent app record) is a Phase 8 UI surface;
    the backend seam this module provides is:
      - `derive_app_webhook_secret(app_id)` — deterministic per-app
        secret from the master secret, so a registered app has a stable
        key across restarts.
      - `sandbox_mode_default(app_id)` — key-mode toggle;
        `RMS_APP_SANDBOX_MODE_<APP_ID>` env var switch (test-substrate
        posture per Owner Ruling 1 / Standing Disposition).

Doctrinal note:
  * The master secret feeds ALL per-tenant HMAC derivations. Dev
    fallback is loud (config.py STARTUP WARNING). Production sets
    `SYNISENSE_MASTER_SECRET` to stable base64/hex.
"""
from __future__ import annotations

import hashlib
import hmac
import os
from typing import Optional

from services.synisense.config import MASTER_SECRET


def derive_app_webhook_secret(app_id: str) -> bytes:
    """Per-app HMAC secret — HKDF-lite over MASTER_SECRET.

    Identical to the pattern in `services/service_1/webhook.py::
    derive_app_secret`, exposed here as the app-registration seam so
    the objectives router doesn't need to import from webhook.py.
    """
    return hmac.new(
        MASTER_SECRET,
        f"webhook:{app_id}".encode("utf-8"),
        hashlib.sha256,
    ).digest()


def sandbox_mode_default(app_id: str) -> bool:
    """Return the sandbox-mode flag for `app_id`.

    Reads env var `RMS_APP_SANDBOX_MODE_<APP_ID_UPPER>`; truthy strings
    (`1`, `true`, `yes`, `on`) mean sandbox=True; anything else False.
    Phase 8 registration UI will replace this with a per-app record read.
    """
    key = f"RMS_APP_SANDBOX_MODE_{app_id.upper()}"
    raw = os.environ.get(key, "").strip().lower()
    return raw in {"1", "true", "yes", "on"}


def resolve_webhook_url(app_id: Optional[str], header_url: Optional[str]) -> Optional[str]:
    """Resolve the webhook URL for this admission.

    Precedence (Phase 5 Stage B; Phase 8 will replace with per-app record):
      1. Explicit `X-RMS-Webhook-URL` header, if present.
      2. Env var `RMS_APP_WEBHOOK_URL_<APP_ID_UPPER>`, if set.
      3. None → polling-only app.
    """
    if header_url:
        return header_url
    if app_id:
        key = f"RMS_APP_WEBHOOK_URL_{app_id.upper()}"
        raw = os.environ.get(key, "").strip()
        return raw or None
    return None
