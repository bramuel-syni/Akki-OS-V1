"""RMS Intelligence System — backend core.

Minimal substrate ported from the cousin repo (`/reference/akki-legacy/backend/core.py`)
and narrowed to what G0 actually needs:
  * Mongo client + db handle (Shield audit_log + canonical + deidentifier
    write here; future Mtafiti Registry will too).
  * Common helpers (`iso`, `now`, uuid).

The cousin's core.py carried 400+ lines of auth/session/RBAC glue. Per the
G0 brief Deliverable 1.d we lift ONLY the strictly-needed pieces; full
auth substrate is reshape territory for G5.

Cousin pointer: /reference/akki-legacy/backend/core.py L1-L60.
"""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

APP_NAME = os.environ.get("APP_NAME", "RMS Intelligence System")
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "rms_intelligence")

client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]


def now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime | None = None) -> str:
    return (dt or now()).isoformat()


def new_uuid() -> str:
    return str(uuid.uuid4())
