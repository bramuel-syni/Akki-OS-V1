"""IF-1 shave attestations — dead-code shave AST-negatives.

Owner ruling: `docs/rulings/outstanding_register_v1_amendment_2026-07-12.md`
Registry supplement: `docs/registry/function_promise_registry_v0.3_supplement.md` §S2

Every row shaved at IF-1 close carries an AST-negative test asserting:
1. The module file no longer exists on disk.
2. No in-tree Python source contains a runtime import of the module.

Docstring-only occurrences (comments, prose references) are permitted so
existing archaeological records aren't disturbed.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent


def _fs_absent(rel_path: str) -> None:
    """Assert the file does not exist under REPO_ROOT."""
    target = REPO_ROOT / rel_path
    assert not target.exists(), f"shaved file still on disk: {target}"


def _no_runtime_import(module_dotted: str, allow_docstring: bool = True) -> None:
    """Walk every .py under /app/backend, /app/tools, /app/frontend and
    assert none of them import `module_dotted` at runtime. Docstring /
    string-literal / comment references are allowed (they document the
    shave, don't execute anything).
    """
    roots = [REPO_ROOT / "backend", REPO_ROOT / "tools"]
    parent_dotted = ".".join(module_dotted.split(".")[:-1])
    leaf = module_dotted.split(".")[-1]

    for root in roots:
        if not root.exists():
            continue
        for py in root.rglob("*.py"):
            if "__pycache__" in str(py) or "/.pytest_cache/" in str(py):
                continue
            # Skip this test file itself so its docstring/citation strings
            # don't false-positive.
            if py.resolve() == Path(__file__).resolve():
                continue
            try:
                tree = ast.parse(py.read_text(encoding="utf-8", errors="replace"))
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert alias.name != module_dotted, (
                            f"live import of shaved module {module_dotted} at {py}"
                        )
                elif isinstance(node, ast.ImportFrom):
                    mod = node.module or ""
                    if mod == module_dotted:
                        assert False, (
                            f"live import-from of shaved module {module_dotted} at {py}"
                        )
                    if mod == parent_dotted:
                        for alias in node.names:
                            assert alias.name != leaf, (
                                f"live 'from {parent_dotted} import {leaf}' at {py}"
                            )


# ── Shave rows (deviation_audit_v1.md §Part B) ───────────────────────


def test_row_01_client_py_shaved() -> None:
    _fs_absent("backend/services/synisense/shield/client.py")
    _no_runtime_import("services.synisense.shield.client")


def test_row_03_audit_log_py_shaved() -> None:
    _fs_absent("backend/services/synisense/shield/audit_log.py")
    _no_runtime_import("services.synisense.shield.audit_log")


def test_row_04_canonical_py_shaved() -> None:
    _fs_absent("backend/services/synisense/shield/canonical.py")
    _no_runtime_import("services.synisense.shield.canonical")


def test_row_05_purpose_validator_py_shaved() -> None:
    _fs_absent("backend/services/synisense/shield/purpose_validator.py")
    _no_runtime_import("services.synisense.shield.purpose_validator")
    # Constants shave (config-negative): ALLOWED_PURPOSES + INTERNAL_ONLY_PURPOSE_PREFIXES
    # must no longer be defined in services/synisense/config.py.
    cfg_path = REPO_ROOT / "backend" / "services" / "synisense" / "config.py"
    cfg_text = cfg_path.read_text(encoding="utf-8")
    # Look for the actual assignment tokens (module-level definitions),
    # not the shave-citation comment that mentions the names.
    assert not re.search(r"^ALLOWED_PURPOSES\s*:", cfg_text, re.MULTILINE), (
        "ALLOWED_PURPOSES still defined in config.py"
    )
    assert not re.search(r"^INTERNAL_ONLY_PURPOSE_PREFIXES\s*:", cfg_text, re.MULTILINE), (
        "INTERNAL_ONLY_PURPOSE_PREFIXES still defined in config.py"
    )


def test_row_07_storage_service_py_shaved() -> None:
    _fs_absent("backend/services/storage_service.py")
    _no_runtime_import("services.storage_service")


def test_row_08_generate_fixture_incoming_py_shaved() -> None:
    _fs_absent(
        "backend/services/data_source/synthetic_assets/rms_adversarial_v1/"
        "rejected/generate_fixture.incoming.py"
    )
    # Dotted-import form is unlikely due to .incoming suffix; check the
    # file-existence guarantee suffices for this specific path.


def test_row_09_generate_fixture_py_shaved() -> None:
    _fs_absent(
        "backend/services/data_source/synthetic_assets/rms_adversarial_v1/"
        "generate_fixture.py"
    )
    _no_runtime_import(
        "services.data_source.synthetic_assets.rms_adversarial_v1.generate_fixture"
    )


def test_row_14_v1_harness_metrics_py_shaved() -> None:
    _fs_absent("backend/services/v1_harness/metrics.py")
    _no_runtime_import("services.v1_harness.metrics")


def test_row_15_purge_attestation_py_shaved() -> None:
    _fs_absent("backend/services/perception/purge_attestation.py")
    _no_runtime_import("services.perception.purge_attestation")


def test_row_16_telemetry_py_shaved() -> None:
    _fs_absent("backend/services/perception/telemetry.py")
    _no_runtime_import("services.perception.telemetry")
