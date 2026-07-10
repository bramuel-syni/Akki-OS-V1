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

9.2a-E2 α condition 1 (Owner, 2026-07-10): env var
`PERCEPTION_EXECUTION_MODE` unset → import-time failure. CI sets `cpu`
explicitly; setting happens HERE at conftest top-level (before any
perception module import at test-collection time).
"""
import asyncio
import os

# 9.2a-E2 α condition 1: CI mode. Set BEFORE any perception import so
# `services/perception/gpu_execution/cuda_runtime.py` imports cleanly.
os.environ.setdefault("PERCEPTION_EXECUTION_MODE", "cpu")

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Session-scoped event loop for pytest-asyncio."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
