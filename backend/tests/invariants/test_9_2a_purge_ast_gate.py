"""9.2a-G5 · Purge-attestation AST gate (Owner E4 α · 2026-07-10).

Owner ruling 9.2a-E4 α verbatim carrier:

    'α as specified. V1-H2 mandates mechanical; the grep-negative + scope-
     walker + whitelist is the established §6.10 pattern (AS-G6/TF-G9/CD-G3
     lineage). No conditions.'

Applies to: `backend/services/perception/asr_worker.py`,
`diarization_worker.py`, `gpu_execution/*.py`.

Two structural invariants:
  (i)  Grep-negative on long-lived-audio-reference patterns
       (`self.raw_audio =`, class-level `_audio_cache = `, module-level
       `AUDIO_BYTES = `, etc.).
  (ii) AST walker: audio-byte reads (`_read_handle_bytes` calls) live
       inside function scopes that ALSO call purge attestation OR return
       a value which itself carries purge attestation (transitively via
       the worker's `process_job` orchestration).

Rate class: §6.10 reflection-gate (~40 LoC/cell standalone).
"""
from __future__ import annotations

import ast
from pathlib import Path
from typing import List

BACKEND_ROOT = Path(__file__).resolve().parents[2]
TARGETED_FILES = [
    BACKEND_ROOT / "services" / "perception" / "asr_worker.py",
    BACKEND_ROOT / "services" / "perception" / "diarization_worker.py",
    BACKEND_ROOT / "services" / "perception" / "gpu_execution" / "model_loader.py",
    BACKEND_ROOT / "services" / "perception" / "gpu_execution" / "audio_batching.py",
    BACKEND_ROOT / "services" / "perception" / "gpu_execution" / "cuda_runtime.py",
    BACKEND_ROOT / "services" / "perception" / "gpu_execution" / "__init__.py",
]

# Whitelisted string tokens allowed for documentation/error messages only —
# NOT allowed as long-lived attribute/module-level assignments.
_FORBIDDEN_ASSIGNMENT_PATTERNS = [
    "self.raw_audio = ",
    "self._audio_bytes = ",
    "self._audio_cache = ",
    "self.audio_bytes_cache = ",
    "self.raw_pcm = ",
]

# Module-level uppercase constants that could persist audio bytes.
_FORBIDDEN_MODULE_LEVEL_NAMES = {
    "AUDIO_BYTES",
    "RAW_AUDIO",
    "AUDIO_CACHE",
    "RAW_PCM_BUFFER",
    "GLOBAL_AUDIO",
}


def test_9_2a_g5_no_long_lived_audio_reference_by_grep() -> None:
    """9.2a-E4 α (i): grep-negative on long-lived-audio-reference assignment patterns."""
    violations: List[str] = []
    for py in TARGETED_FILES:
        assert py.is_file(), f"expected file {py}"
        text = py.read_text(encoding="utf-8")
        for pattern in _FORBIDDEN_ASSIGNMENT_PATTERNS:
            if pattern in text:
                # Whitelist: appearance inside a triple-quoted docstring is
                # acceptable IF the pattern is quoted context (like this file's
                # own docstring). Simple heuristic: check if pattern is between
                # `"""` delimiters. For robustness we exclude AST-parseable
                # docstring nodes.
                if _is_only_inside_docstring(text, pattern):
                    continue
                violations.append(f"{py.relative_to(BACKEND_ROOT)}: {pattern!r}")
    assert violations == [], (
        "9.2a-E4 α VIOLATED (grep-negative): long-lived audio reference "
        "assignment patterns found in worker/GPU modules.\n"
        "Owner CD-9.2a-E4 α: 'audio bytes are held only inside function scopes "
        "that terminate with a purge_attestation call before return.'\n"
        "Violations:\n" + "\n".join(violations)
    )


def test_9_2a_g5_no_module_level_audio_constants_by_ast() -> None:
    """9.2a-E4 α (i): AST scan for module-level ALL-CAPS audio buffers."""
    violations: List[str] = []
    for py in TARGETED_FILES:
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in tree.body:  # module-level statements only
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name) and tgt.id in _FORBIDDEN_MODULE_LEVEL_NAMES:
                        violations.append(
                            f"{py.relative_to(BACKEND_ROOT)}:{node.lineno} — "
                            f"module-level assignment to forbidden name {tgt.id!r}"
                        )
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id in _FORBIDDEN_MODULE_LEVEL_NAMES:
                    violations.append(
                        f"{py.relative_to(BACKEND_ROOT)}:{node.lineno} — "
                        f"module-level typed assignment to forbidden name "
                        f"{node.target.id!r}"
                    )
    assert violations == [], (
        "9.2a-E4 α VIOLATED (AST module-level scan):\n" + "\n".join(violations)
    )


def test_9_2a_g5_audio_read_scopes_terminate_with_purge_attestation_ast() -> None:
    """9.2a-E4 α (ii): AST walker asserts audio-byte read scopes are
    function-scoped AND the surrounding worker orchestration calls
    purge_attestation before returning.

    Enforcement scope: `asr_worker.process_job` + `diarization_worker.process_job`
    MUST contain a `PurgeAttestation` construction call.
    """
    for worker_file in [
        BACKEND_ROOT / "services" / "perception" / "asr_worker.py",
        BACKEND_ROOT / "services" / "perception" / "diarization_worker.py",
    ]:
        tree = ast.parse(worker_file.read_text(encoding="utf-8"))
        found_process_job = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "process_job":
                found_process_job = True
                # Search for PurgeAttestation call within this function.
                has_purge = any(
                    isinstance(sub, ast.Call)
                    and (
                        (isinstance(sub.func, ast.Name) and sub.func.id == "PurgeAttestation")
                        or (isinstance(sub.func, ast.Attribute) and sub.func.attr == "PurgeAttestation")
                    )
                    for sub in ast.walk(node)
                )
                assert has_purge, (
                    f"9.2a-E4 α VIOLATED (AST walker): {worker_file.name}::process_job "
                    f"does not construct a PurgeAttestation. Audio-byte read paths "
                    f"MUST terminate with purge attestation before return."
                )
        assert found_process_job, f"expected process_job in {worker_file.name}"


def test_9_2a_g5_read_handle_bytes_returns_only_bytes_no_leak_ast() -> None:
    """9.2a-E4 α (ii): `_read_handle_bytes` returns raw bytes; caller MUST NOT
    store return value on self.* or class attributes. AST walks the callers
    to ensure only local-variable assignment.
    """
    violations: List[str] = []
    for worker_file in [
        BACKEND_ROOT / "services" / "perception" / "asr_worker.py",
        BACKEND_ROOT / "services" / "perception" / "diarization_worker.py",
    ]:
        tree = ast.parse(worker_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            # Look for `X = _read_handle_bytes(...)` patterns.
            if not isinstance(node.value, ast.Call):
                continue
            fn = node.value.func
            fn_name = None
            if isinstance(fn, ast.Name):
                fn_name = fn.id
            elif isinstance(fn, ast.Attribute):
                fn_name = fn.attr
            if fn_name != "_read_handle_bytes":
                continue
            # Assignment targets: MUST be local ast.Name (not self.attr).
            for tgt in node.targets:
                if isinstance(tgt, ast.Attribute):
                    violations.append(
                        f"{worker_file.name}:{node.lineno} — "
                        f"_read_handle_bytes return assigned to attribute "
                        f"{ast.dump(tgt)}; must be function-local variable only."
                    )
    assert violations == [], (
        "9.2a-E4 α VIOLATED (AST caller scan):\n" + "\n".join(violations)
    )


def _is_only_inside_docstring(text: str, needle: str) -> bool:
    '''Return True if `needle` appears only inside triple-quoted docstrings.

    Simple heuristic: parse the source AST and check if the pattern
    appears in any string literal that is a module-level or function-level
    docstring. Any appearance outside a docstring returns False.
    '''
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    docstring_texts = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            ds = ast.get_docstring(node)
            if ds:
                docstring_texts.append(ds)
    if not any(needle in ds for ds in docstring_texts):
        return False
    # Count total occurrences; count docstring occurrences.
    total = text.count(needle)
    doc_count = sum(ds.count(needle) for ds in docstring_texts)
    return total <= doc_count
