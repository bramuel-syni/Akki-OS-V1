"""Far-endpoint MandateSpec@v0 emitter · fold C.FE.2 · Owner ruling §5.2 (a).

Deterministic emitter · same input yields byte-identical YAML output ·
every generated file carries a `# GENERATED · DO NOT EDIT` header.

Binding B-2 (Owner-verbatim):
    "The emitter is deterministic — same mandate input yields
    byte-identical YAML — every generated file carries a
    generated-do-not-edit header naming its source mandate + SHA, and a
    CI cell regenerates and diffs: any divergence between
    docs/generated/mandate_specs/ and fresh emitter output is a hard
    fail. Generated artifacts that can be hand-edited silently are a
    shadow-canon vector; the regeneration diff closes it."
"""
from __future__ import annotations

import pathlib
from typing import List

from contracts.mandate_spec_v0 import GateSpec, MandateSpec_v0
from services.far_endpoint.mandate_reader import (
    MANDATES_DIR,
    ParsedMandate,
    REPO_ROOT,
    list_mandate_paths,
    parse_mandate,
)


GENERATED_SPECS_DIR = REPO_ROOT / "docs" / "generated" / "mandate_specs"

# Owner-verbatim B-2 header: names source mandate + SHA + generator + regenerate instruction.
HEADER_TEMPLATE = (
    "# GENERATED · DO NOT EDIT\n"
    "# Source: {source_path}\n"
    "# Source SHA-256: {source_sha}\n"
    "# Generator: backend/services/far_endpoint/mandate_spec_emitter.py\n"
    "# Regenerate: python -m services.far_endpoint.mandate_spec_emitter\n"
)

# Fixed generation timestamp anchor for deterministic emission. The
# emitter uses a source-derived value (mandate source SHA prefix) so the
# YAML is byte-identical for a given source; a wall-clock timestamp
# would defeat the regeneration-diff invariant.
_GENERATED_AT_ANCHOR = "generation-deterministic-per-source-sha"


def _stanza_to_gate_spec(mandate: ParsedMandate, i: int, stanza: str) -> GateSpec:
    """Deterministic mapping stanza → GateSpec (source-order preserved)."""
    return GateSpec(
        gate_id=f"{pathlib.Path(mandate.source_path).stem}_gate_{i:03d}",
        gate_kind="rail",  # conservative default · refined via future E→O engine version bump
        condition_expr=stanza,  # raw stanza as structured condition placeholder
        refusal_reason=f"Mandate gate {i:03d} from {mandate.source_path} · {mandate.title}",
        source_line_anchor=f"{mandate.source_path}#stanza-{i:03d}",
    )


def emit_mandate_spec(parsed: ParsedMandate) -> MandateSpec_v0:
    """Emit a MandateSpec@v0 record from a parsed mandate · deterministic."""
    return MandateSpec_v0(
        spec_id=pathlib.Path(parsed.source_path).stem,
        source_mandate_path=parsed.source_path,
        source_mandate_sha_256=parsed.source_sha_256,
        mandate_title=parsed.title,
        gates=[
            _stanza_to_gate_spec(parsed, i, stanza)
            for i, stanza in enumerate(parsed.gate_stanzas)
        ],
        generated_at=_GENERATED_AT_ANCHOR,
    )


def _dump_scalar(value: object) -> str:
    """Deterministic scalar-to-YAML rendering (no runtime state · byte-stable)."""
    if isinstance(value, str):
        # Fixed escaping · replace backslash first · then double quote.
        escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if value is None:
        return "null"
    raise ValueError(f"unsupported scalar type: {type(value).__name__}")


def _dump_gate_spec(gs: GateSpec) -> List[str]:
    """Deterministic per-gate YAML block · field order fixed."""
    return [
        f"  - gate_id: {_dump_scalar(gs.gate_id)}",
        f"    gate_kind: {_dump_scalar(gs.gate_kind)}",
        f"    condition_expr: {_dump_scalar(gs.condition_expr)}",
        f"    refusal_reason: {_dump_scalar(gs.refusal_reason)}",
        f"    source_line_anchor: {_dump_scalar(gs.source_line_anchor)}",
    ]


def render_spec_yaml(spec: MandateSpec_v0) -> str:
    """Deterministic YAML rendering · byte-stable for a given MandateSpec@v0.

    Custom emitter · not PyYAML · to guarantee byte-identity across the
    dependency graph (PyYAML dump order and escaping is version-dependent).
    """
    header = HEADER_TEMPLATE.format(
        source_path=spec.source_mandate_path,
        source_sha=spec.source_mandate_sha_256,
    )
    lines: List[str] = [
        f"spec_id: {_dump_scalar(spec.spec_id)}",
        f"source_mandate_path: {_dump_scalar(spec.source_mandate_path)}",
        f"source_mandate_sha_256: {_dump_scalar(spec.source_mandate_sha_256)}",
        f"mandate_title: {_dump_scalar(spec.mandate_title)}",
        f"generated_at: {_dump_scalar(spec.generated_at)}",
        f"generator_version: {_dump_scalar(spec.generator_version)}",
        "gates:",
    ]
    if spec.gates:
        for gs in spec.gates:
            lines.extend(_dump_gate_spec(gs))
    else:
        lines[-1] = "gates: []"
    return header + "\n".join(lines) + "\n"


def emit_all_specs_to_disk() -> List[pathlib.Path]:
    """Regenerate ALL mandate specs from source · overwrite on-disk YAML files.

    Owner-verbatim B-2: *"any divergence between docs/generated/mandate_specs/
    and fresh emitter output is a hard fail"* — this function is the
    deterministic reference emitter that the regeneration-diff cell
    compares against.
    """
    GENERATED_SPECS_DIR.mkdir(parents=True, exist_ok=True)
    written: List[pathlib.Path] = []
    for mandate_path in list_mandate_paths():
        parsed = parse_mandate(mandate_path)
        spec = emit_mandate_spec(parsed)
        yaml_text = render_spec_yaml(spec)
        out_path = GENERATED_SPECS_DIR / f"{spec.spec_id}.yaml"
        out_path.write_text(yaml_text)
        written.append(out_path)
    return sorted(written)


if __name__ == "__main__":
    # Regenerate all mandate specs from source · Binding B-2 regeneration entrypoint.
    paths = emit_all_specs_to_disk()
    for p in paths:
        print(f"Emitted: {p.relative_to(REPO_ROOT)}")
