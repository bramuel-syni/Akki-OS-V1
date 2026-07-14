"""Instance config router — public read of `/api/instance/config`.

Owner ruling: MC-E6 close 2026-07-14. Public surface (no auth).
"""
from __future__ import annotations

from typing import Dict, Optional

from fastapi import APIRouter, Header

from config import current_instance_id, load_instance_config

router = APIRouter(prefix="/instance", tags=["instance"])


@router.get("/config")
async def get_instance_config(
    x_instance_id: Optional[str] = Header(default=None, alias="X-Instance-Id"),
) -> Dict:
    """Return the resolved instance configuration.

    Instance is resolved by (in priority order):
      1. Explicit `X-Instance-Id` header, if present.
      2. `INSTANCE_ID` env var (default 'instance_1').
    """
    iid = x_instance_id or current_instance_id()
    return load_instance_config(iid)
