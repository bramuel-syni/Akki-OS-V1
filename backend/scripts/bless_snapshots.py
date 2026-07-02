"""Re-bless contract snapshots after an intentional schema edit.

Usage:
  cd /app/backend && python3 scripts/bless_snapshots.py

This is the explicit-re-bless flow that the invariant tests demand.
Never run this in CI — it's a developer-loop tool. Re-blessing in CI
would defeat the purpose of the freeze.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from contracts.five_rings import NormalizedUnit  # noqa: E402
from contracts.objective_request import ObjectiveRequest  # noqa: E402
from contracts.qualification_matrix.loader import (  # noqa: E402
    QualificationMatrix,
    load_qualification_matrix,
)

SNAP_DIR = ROOT / "tests" / "invariants"


def _write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"blessed: {path.relative_to(ROOT)}")


def main() -> int:
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    _write(SNAP_DIR / "five_rings.contract_snapshot.json", NormalizedUnit.model_json_schema())
    _write(SNAP_DIR / "objective_request.contract_snapshot.json", ObjectiveRequest.model_json_schema())
    _write(SNAP_DIR / "qualification_matrix.schema_snapshot.json", QualificationMatrix.model_json_schema())
    _write(SNAP_DIR / "qualification_matrix.v0.content_snapshot.json", load_qualification_matrix("v0").model_dump())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
