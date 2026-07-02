"""Pytest configuration for RMS Intelligence backend.

Session-scoped event loop for async tests. Motor's AsyncIOMotorClient
(instantiated at module import in `core.py`) binds to the event loop
that exists at first use; if pytest-asyncio creates a fresh loop per
test, Motor's underlying connection pool closes when a prior test
finishes, breaking subsequent async Mongo writes with
"RuntimeError: Event loop is closed".

Session-scoped loop shares one loop across all async tests in the
session, matching the runtime posture (long-lived FastAPI app with a
single event loop).
"""
import asyncio

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Session-scoped event loop for pytest-asyncio."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
