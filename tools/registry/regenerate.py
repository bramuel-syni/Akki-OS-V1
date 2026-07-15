"""Regenerate the machine-readable Registry YAML.

Owner rulings 2026-07-11 · MRR-E1 α · MRR-E4 β · governance §14:
regeneration is automated ONLY. Machine form must never be hand-edited.

G-2 · 2026-07-14 (docs/rulings/g2_rm_e1_to_e3_2026-07-14.md): after v1
consolidation lands, v1 becomes the single active source; parse_v1_source()
runs the machine form. v0.md + v0.1..v0.5 supplements remain readable +
archaeological (path/SHA preserved in supplements metadata).

Usage:
    python -m tools.registry.regenerate                # write to default path
    python -m tools.registry.regenerate --check        # regenerate + gates; no write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from backend.services.registry.parser import (
    REPO_ROOT,
    V0_PATH,
    V1_PATH,
    SUPPLEMENT_PATHS,
    parse_source,
    parse_v1_source,
    render_yaml,
)
from backend.services.registry.validator import run_all_gates


MACHINE_PATH = REPO_ROOT / "docs" / "registry" / "machine" / "registry.yaml"


def regenerate(write: bool = True) -> str:
    # G-2 · 2026-07-14: v1 is the single active source when present.
    if V1_PATH.exists():
        model = parse_v1_source(V1_PATH, SUPPLEMENT_PATHS)
    else:
        model = parse_source(V0_PATH, SUPPLEMENT_PATHS)
    yaml_text = render_yaml(model)
    if write:
        MACHINE_PATH.parent.mkdir(parents=True, exist_ok=True)
        MACHINE_PATH.write_text(yaml_text, encoding="utf-8")
    return yaml_text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="Regenerate + run gates; no write.")
    args = ap.parse_args()
    if args.check:
        regenerate(write=False)
        results = run_all_gates()
        failed = [g for g, (ok, _) in results.items() if not ok]
        for gate, (ok, errs) in results.items():
            status = "GREEN" if ok else "FAIL"
            print(f"{gate}: {status}")
            for e in errs:
                print(f"  - {e}")
        return 0 if not failed else 1
    regenerate(write=True)
    print(f"Wrote {MACHINE_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
