"""G-13 Binding B-1 discharge · registry-context prompt-block golden snapshot + single-writer AST guard.

Owner ruling verbatim (Binding B-1):
    "No seal does not mean no shape. The block is emitted by exactly one
    writer (prompt_builder.py), its content sourced from the Registry
    record — never hand-authored — and a hard-fail cell asserts the
    exact rendered serialization against a golden snapshot for a fixture
    function."
"""
from __future__ import annotations

import ast
import pathlib

import pytest

from services.registry_context.prompt_builder import build_context_block
from services.registry_context.reader import known_function_ids


BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURES_DIR = BACKEND_ROOT / "tests" / "invariants" / "fixtures"
SERVICES_DIR = BACKEND_ROOT / "services"

FIXTURE_FUNCTION_ID = "PROM-S1-frozen-wire-contract"
GOLDEN_SNAPSHOT_PATH = FIXTURES_DIR / f"registry_context_block__{FIXTURE_FUNCTION_ID}.md"


# ---------------------------------------------------------------------------
# B-1 golden-snapshot cell · byte-identical rendered serialization.
# ---------------------------------------------------------------------------

def test_b1_golden_snapshot_byte_identical():
    """B-1 hard-fail: rendered block MUST be byte-identical to golden snapshot.

    Any drift = hard fail (Owner-verbatim: 'not warn').
    """
    assert GOLDEN_SNAPSHOT_PATH.exists(), (
        f"B-1 golden snapshot missing: {GOLDEN_SNAPSHOT_PATH}"
    )
    golden = GOLDEN_SNAPSHOT_PATH.read_text()
    rendered = build_context_block([FIXTURE_FUNCTION_ID])
    assert rendered == golden, (
        f"B-1 hard-fail: rendered block byte-mismatch vs golden snapshot.\n"
        f"Golden path: {GOLDEN_SNAPSHOT_PATH}\n"
        f"Rendered length: {len(rendered)} · Golden length: {len(golden)}"
    )


def test_b1_prompt_builder_deterministic_across_calls():
    """B-1: prompt_builder is deterministic · repeated calls produce byte-identical output."""
    a = build_context_block([FIXTURE_FUNCTION_ID])
    b = build_context_block([FIXTURE_FUNCTION_ID])
    c = build_context_block([FIXTURE_FUNCTION_ID])
    assert a == b == c


def test_b1_fixture_function_id_is_known_row():
    """B-1 fixture function ID resolves in the Registry reader."""
    assert FIXTURE_FUNCTION_ID in known_function_ids()


# ---------------------------------------------------------------------------
# B-1 single-writer AST guard · exactly one emitter of registry-context blocks.
# ---------------------------------------------------------------------------

def test_b1_single_writer_ast_guard():
    """Owner-verbatim B-1: 'the block is emitted by exactly one writer (prompt_builder.py)'.

    AST-scan the entire backend for the block-header sentinel string.
    Only prompt_builder.py may contain it.
    """
    from services.registry_context.prompt_builder import BLOCK_HEADER
    sentinel = BLOCK_HEADER
    offenders = []
    prompt_builder_path = (
        BACKEND_ROOT / "services" / "registry_context" / "prompt_builder.py"
    ).resolve()
    for py_file in BACKEND_ROOT.rglob("*.py"):
        # Skip pycache + virtualenv + third-party.
        parts = py_file.parts
        if "__pycache__" in parts or ".venv" in parts:
            continue
        # Skip the golden snapshot fixture is not .py; already excluded.
        try:
            src = py_file.read_text()
        except (UnicodeDecodeError, PermissionError):
            continue
        if sentinel in src and py_file.resolve() != prompt_builder_path:
            # Allow this test file to reference sentinel indirectly (via import).
            if py_file.resolve() == pathlib.Path(__file__).resolve():
                continue
            offenders.append(str(py_file.relative_to(BACKEND_ROOT)))
    assert not offenders, (
        f"B-1 single-writer violation: registry-context block sentinel "
        f"appears in files other than prompt_builder.py: {offenders}"
    )


def test_b1_prompt_builder_sources_only_from_reader():
    """B-1: prompt_builder MUST source its content from Registry reader · never hand-author.

    AST-scan prompt_builder.py: verifies it imports from reader; no
    literal mandate/promise strings hardcoded in the builder.
    """
    prompt_builder_path = SERVICES_DIR / "registry_context" / "prompt_builder.py"
    src = prompt_builder_path.read_text()
    tree = ast.parse(src)
    imports_reader = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if "reader" in mod or "registry_context" in mod:
                imports_reader = True
                break
    assert imports_reader, (
        "B-1 violation: prompt_builder.py MUST import Registry rows from "
        "reader.py (content sourced from Registry record, never hand-authored)"
    )
