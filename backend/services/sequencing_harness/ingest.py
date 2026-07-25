"""Sequencing-harness fixture-traffic ingest.

Fold A.SH.4 · Registry Doctrine §5.2 verbatim: *"executes registered
functions against fixture traffic"*.

Per Stage A §5.4 downgrade: fixture-traffic path rides existing
test-fixture machinery at `backend/tests/fixtures/`. Sequencing harness
reads from the established fixture path; no new fixture-carrier
contract required.
"""
from __future__ import annotations

import pathlib
from typing import Iterator, List


BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURES_DIR = BACKEND_ROOT / "tests" / "fixtures"


def iter_fixture_paths(pattern: str = "*") -> Iterator[pathlib.Path]:
    """Iterate fixture files under the established fixtures directory.

    Callers filter by pattern; the harness does not invent new fixture
    format or location.
    """
    if not FIXTURES_DIR.exists():
        return iter([])
    return FIXTURES_DIR.glob(pattern)


def load_fixture_payloads(pattern: str = "*") -> List[pathlib.Path]:
    """Load fixture paths for harness execution.

    Payload deserialization is the concern of the registered function
    (fixture consumers own their format); harness only surfaces the paths.
    """
    return sorted(iter_fixture_paths(pattern))
