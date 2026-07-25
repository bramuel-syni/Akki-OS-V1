"""Far-endpoint gate generator · fold C.FE.3 · Owner ruling §5.3 (a).

Consumes MandateSpec@v0 records · emits Python function-stub gate
modules at `backend/services/generated_gates/<spec_id>.py`.

Owner ruling §5.3 (a) verbatim: *"one .py file per mandate · executable
Python functions with docstrings tracing back to source mandate
line-anchors · imported by gate-consumers"*.

Binding B-3 (Owner-verbatim):
    "Same regeneration-diff regime as B-2 — generated gates are never
    hand-edited; a needed change lands at the mandate source and flows
    through the emitter. Additionally, every generated gate gets at
    least an import-and-invoke smoke cell inside the far-endpoint rail
    set, so generated code cannot rot as unexecuted text."
"""
from __future__ import annotations

import pathlib
from typing import List

from contracts.mandate_spec_v0 import GateSpec, MandateSpec_v0
from services.far_endpoint.mandate_reader import list_mandate_paths, parse_mandate
from services.far_endpoint.mandate_spec_emitter import (
    REPO_ROOT,
    emit_mandate_spec,
)


GENERATED_GATES_DIR = REPO_ROOT / "backend" / "services" / "generated_gates"

# Owner-verbatim B-3: same generated-do-not-edit header pattern as B-2.
HEADER_TEMPLATE = (
    "# GENERATED · DO NOT EDIT\n"
    "# Source: {source_path}\n"
    "# Source SHA-256: {source_sha}\n"
    "# Generator: backend/services/far_endpoint/gate_generator.py\n"
    "# Regenerate: python -m services.far_endpoint.gate_generator\n"
)


def _render_gate_function(gs: GateSpec) -> str:
    """Deterministic function-stub rendering · source-anchor docstring per Owner ruling §5.3 (a).

    Function shape:
        def <gate_id>(payload) -> None:
            \"\"\"<source-anchor docstring>\"\"\"
            # gate condition placeholder (refined per future engine-version bump)
            return None
    """
    # Escape internal quotes for docstring safety.
    safe_refusal = gs.refusal_reason.replace('"""', '"" "')
    safe_condition = gs.condition_expr.replace('"""', '"" "')
    safe_anchor = gs.source_line_anchor.replace('"""', '"" "')
    return (
        f"def {gs.gate_id}(payload):\n"
        f'    """Source anchor: {safe_anchor}\n'
        f"\n"
        f"    Refusal reason: {safe_refusal}\n"
        f"    Condition (verbatim from source): {safe_condition}\n"
        f'    """\n'
        f"    # Gate condition placeholder · executable via import-and-invoke smoke cell (B-3).\n"
        f"    # Concrete condition body evolves per engine-version bump (Class E discipline).\n"
        f"    return None\n"
    )


def render_gate_module(spec: MandateSpec_v0) -> str:
    """Render a full gate-module file for a MandateSpec@v0."""
    header = HEADER_TEMPLATE.format(
        source_path=spec.source_mandate_path,
        source_sha=spec.source_mandate_sha_256,
    )
    if not spec.gates:
        body = (
            f"# Zero gates identified in source mandate {spec.source_mandate_path}.\n"
            f"# Module remains loadable · smoke-cell coverage is trivially satisfied.\n"
        )
    else:
        body = "\n\n".join(_render_gate_function(gs) for gs in spec.gates)
    return header + "\n" + body


def emit_all_gates_to_disk() -> List[pathlib.Path]:
    """Regenerate ALL generated-gate modules from source · overwrite on-disk .py files."""
    GENERATED_GATES_DIR.mkdir(parents=True, exist_ok=True)
    # Landing an __init__.py so the package is importable.
    init_path = GENERATED_GATES_DIR / "__init__.py"
    if not init_path.exists():
        init_path.write_text(
            '"""Generated gates package · Owner ruling §5.3 (a) · G-13 execution atomic.\n'
            "\n"
            "Every module in this package is generated · do not hand-edit.\n"
            'Regenerate via `python -m services.far_endpoint.gate_generator`."""\n'
        )
    written: List[pathlib.Path] = [init_path]
    for mandate_path in list_mandate_paths():
        parsed = parse_mandate(mandate_path)
        spec = emit_mandate_spec(parsed)
        module_text = render_gate_module(spec)
        out_path = GENERATED_GATES_DIR / f"{spec.spec_id}.py"
        out_path.write_text(module_text)
        written.append(out_path)
    return sorted(written)


if __name__ == "__main__":
    paths = emit_all_gates_to_disk()
    for p in paths:
        print(f"Emitted: {p.relative_to(REPO_ROOT)}")
