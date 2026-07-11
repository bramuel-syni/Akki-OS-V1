"""System info router (PH-R1 · Owner enhancement promotion 2026-07-10).

Endpoint:
    GET /api/system/build_info  →  {git_sha, build_timestamp, parity_count}

Rationale (Owner ruling):
    "Ruled in rather than deferred because it converts PH-R1's own STAKED
    claim ('promotion-not-rebuild') from asserted to verifiable — a
    deployed artifact that states its git SHA is the audit made
    mechanical."

Payload contract:
    * `git_sha` — 40-char full SHA of the container source (build-arg
      `GIT_SHA` when set; falls back to git-tree inspection at startup;
      falls back to "dev-<local-uncommitted>" if neither is available).
    * `build_timestamp` — ISO-8601 UTC of image build (build-arg
      `BUILD_TIMESTAMP` when set; falls back to server startup time).
    * `parity_count` — same authoritative counter as `/api/readyz`.

Owner constraint (verbatim): "no secrets in the payload".
"""
from __future__ import annotations

import logging
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter

from services.health import count_frozen_contract_snapshots

router = APIRouter(prefix="/system", tags=["system"])
log = logging.getLogger("rms.system_info")


def _resolve_git_sha() -> str:
    """Resolve container source git SHA.

    Precedence:
        1. GIT_SHA env var (Dockerfile ARG · production posture).
        2. `git rev-parse HEAD` at container startup (dev posture).
        3. "dev-unknown" fallback (never a secret; never blocking).
    """
    env_sha = os.environ.get("GIT_SHA", "").strip()
    if env_sha:
        return env_sha
    try:
        repo_root = Path(__file__).resolve().parents[2]
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2.0,
            check=False,
        )
        if result.returncode == 0:
            sha = result.stdout.strip()
            if sha:
                return sha
    except Exception:  # noqa: BLE001 — never fail build_info on git
        pass
    return "dev-unknown"


def _resolve_build_timestamp() -> str:
    """Resolve container build timestamp (ISO-8601 UTC).

    Precedence:
        1. BUILD_TIMESTAMP env var (Dockerfile ARG · production posture).
        2. Container start time (dev posture · resolved at import).
    """
    env_ts = os.environ.get("BUILD_TIMESTAMP", "").strip()
    if env_ts:
        return env_ts
    return _CONTAINER_START_TS


_CONTAINER_START_TS: str = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@router.get("/build_info")
async def build_info() -> dict:
    """Return git SHA + build timestamp + parity count (no secrets).

    Payload is the mechanical audit of the "promotion-not-rebuild" claim:
    a deployed artifact that states its git SHA, so promotion can be
    verified without opening the container.
    """
    return {
        "git_sha": _resolve_git_sha(),
        "build_timestamp": _resolve_build_timestamp(),
        "parity_count": count_frozen_contract_snapshots(),
    }
