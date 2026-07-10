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

# Answer Fluency AF-E2 amended (Owner, 2026-07-10): hermetic tests opt
# into mock LLM mode via `SYNISENSE_LLM_MODE=mock`. In this mode the
# fluent-arm synthesis produces echo output (not valid JSON) which
# trips LLMParseFailureError → mechanical arm falls through. CI never
# performs a live LLM call for fluency; tests that specifically need
# the LLM-succeeds path monkey-patch the fluency_synthesizer seams.
# Without this default, missing EMERGENT_LLM_KEY would surface as 503
# EmergentKeyMissingError (which is the correct production behaviour
# for a misconfigured deployment, but wrong for hermetic CI).
os.environ.setdefault("SYNISENSE_LLM_MODE", "mock")

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Session-scoped event loop for pytest-asyncio."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
