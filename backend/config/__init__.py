"""Instance configuration surface — Multi-Instance Capability MC-E1..MC-E6 close 2026-07-14.

Owner ruling: MC-E5 α + MC-E6 β + RMS de-tuning capability-4.
'Instance identity lives in configuration; platform code, contracts, and
vocabulary carry no organization.' Instance-#1's config carries the
'RMS Intelligence' branding verbatim per Owner: 'instance #1's config
carries "RMS Intelligence"'.

Read path: `GET /api/instance/config` returns the current instance's
configuration. Public surface (no auth) — analogous to
`/api/system/build_info`. Frontend hydrates branding + product title
from this endpoint at boot.

Instance resolution:
    Env var `INSTANCE_ID` (default 'instance_1') resolves the current
    instance. Config file lives at
    `/app/backend/config/instances/{instance_id}.json`.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional

_CONFIG_DIR = Path(__file__).parent / "instances"
_DEFAULT_INSTANCE_ID = "instance_1"


def current_instance_id() -> str:
    """Return the current instance identifier (env-var-driven; default instance_1)."""
    return os.environ.get("INSTANCE_ID", _DEFAULT_INSTANCE_ID).strip() or _DEFAULT_INSTANCE_ID


def load_instance_config(instance_id: Optional[str] = None) -> Dict:
    """Load the instance's config JSON from disk.

    Falls back to instance_1's config if the target instance's config
    file is absent (data-blind default per Governance §8).
    """
    iid = instance_id or current_instance_id()
    path = _CONFIG_DIR / f"{iid}.json"
    if not path.exists():
        path = _CONFIG_DIR / f"{_DEFAULT_INSTANCE_ID}.json"
    return json.loads(path.read_text(encoding="utf-8"))
