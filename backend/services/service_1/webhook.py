"""Webhook signing + emit + retry — Phase 5 Stage B (Owner Ruling 3).

Doorbell posture: HMAC signing, bounded retry (5 attempts, exponential
backoff), NO dead-letter queue. Polling `GET /api/objectives/{id}` is
delivery guarantee; webhook only nudges the poll.

Payload shape (5 governance-thin keys, no claim content):
  {event, objective_id, trace_id, status, timestamp}
"""
from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from typing import Dict, Optional

import httpx

from services.service_1 import async_state


# HKDF-lite: derive per-app secret from master secret + app_id via HMAC-SHA256.
def derive_app_secret(master_secret: bytes, app_id: str) -> bytes:
    return hmac.new(master_secret, f"webhook:{app_id}".encode("utf-8"),
                    hashlib.sha256).digest()


def sign_payload(payload_json: str, timestamp: str, secret: bytes) -> str:
    message = f"{payload_json}.{timestamp}".encode("utf-8")
    return hmac.new(secret, message, hashlib.sha256).hexdigest()


def verify_signature(
    payload_json: str, timestamp: str, signature_hex: str, secret: bytes,
    *, skew_seconds: int = 300,
) -> bool:
    """Verify HMAC signature + timestamp within skew window."""
    expected = sign_payload(payload_json, timestamp, secret)
    if not hmac.compare_digest(expected, signature_hex):
        return False
    try:
        ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return False
    now = datetime.now(timezone.utc)
    return abs((now - ts).total_seconds()) <= skew_seconds


def build_payload(objective_id: str, trace_id: str, status: str) -> Dict[str, str]:
    """Payload with exactly 5 governance-thin keys per Stage A §4.1."""
    return {
        "event": "objective.status_changed",
        "objective_id": objective_id,
        "trace_id": trace_id,
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# 5 attempts, exponential backoff: 1s, 4s, 16s, 64s, 256s.
_BACKOFF_SECONDS = [1, 4, 16, 64, 256]
_MAX_ATTEMPTS = 5


async def _post_once(url: str, payload_json: str, headers: Dict[str, str],
                     timeout_seconds: float = 10.0) -> bool:
    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            resp = await client.post(url, content=payload_json, headers=headers)
            return 200 <= resp.status_code < 300
    except (httpx.RequestError, asyncio.TimeoutError):
        return False


async def fire_webhook(
    *, objective_id: str, trace_id: str, status: str,
    webhook_url: Optional[str], webhook_secret: Optional[bytes],
    _sleep=asyncio.sleep,
    _post=_post_once,
) -> bool:
    """Fire a doorbell webhook with 5 bounded retry attempts.
    Returns True on success (2xx within an attempt), False if all attempts
    fail — caller marks `webhook_undelivered=true`. No DLQ."""
    if not webhook_url or not webhook_secret:
        return True  # No webhook registered — polling-only app; not a failure.

    payload = build_payload(objective_id, trace_id, status)
    payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    timestamp = payload["timestamp"]
    signature = sign_payload(payload_json, timestamp, webhook_secret)
    headers = {
        "Content-Type": "application/json",
        "X-RMS-Signature": f"sha256={signature}",
        "X-RMS-Timestamp": timestamp,
    }

    for attempt in range(_MAX_ATTEMPTS):
        if await _post(webhook_url, payload_json, headers):
            return True
        if attempt < _MAX_ATTEMPTS - 1:
            await _sleep(_BACKOFF_SECONDS[attempt])
    await async_state.mark_webhook_undelivered(objective_id)
    return False
