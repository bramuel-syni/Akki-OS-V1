"""Run the three Standing Queries and emit findings artifacts.

Owner rulings 2026-07-11 · SQ-E1 γ + cross-reference condition:
Six files land under `docs/registry/queries/` — one archaeological + one mechanical
per query class (Q1 · Q2 · Q3).

Usage:
    python -m tools.registry.run_queries          # write findings artifacts
    python -m tools.registry.run_queries --check  # regenerate + verify no source-of-truth writes
"""
from __future__ import annotations

import argparse
import sys

from backend.services.registry.parser import (
    CONSOLIDATION_LOG_PATH,
    SUPPLEMENT_PATHS,
    V0_PATH,
    sha256_file,
)
from backend.services.registry.queries import run_queries


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="Regenerate + verify no source-of-truth writes.")
    args = ap.parse_args()

    pre_shas = {
        "v0.md": sha256_file(V0_PATH),
        "v0.1_supplement.md": sha256_file(SUPPLEMENT_PATHS[0]),
        "v0.2_supplement.md": sha256_file(SUPPLEMENT_PATHS[1]),
        "v0.3_supplement.md": sha256_file(SUPPLEMENT_PATHS[2]),
        "v0.4_supplement.md": sha256_file(SUPPLEMENT_PATHS[3]),
        "v0.5_supplement.md": sha256_file(SUPPLEMENT_PATHS[4]),
        "consolidation_log_v0.md": sha256_file(CONSOLIDATION_LOG_PATH),
    }
    outs = run_queries(write=not args.check)
    post_shas = {
        "v0.md": sha256_file(V0_PATH),
        "v0.1_supplement.md": sha256_file(SUPPLEMENT_PATHS[0]),
        "v0.2_supplement.md": sha256_file(SUPPLEMENT_PATHS[1]),
        "v0.3_supplement.md": sha256_file(SUPPLEMENT_PATHS[2]),
        "v0.4_supplement.md": sha256_file(SUPPLEMENT_PATHS[3]),
        "v0.5_supplement.md": sha256_file(SUPPLEMENT_PATHS[4]),
        "consolidation_log_v0.md": sha256_file(CONSOLIDATION_LOG_PATH),
    }
    for k, v in pre_shas.items():
        if post_shas[k] != v:
            print(f"SOURCE-OF-TRUTH DRIFT: {k}", file=sys.stderr)
            return 2
    if args.check:
        print(f"OK · {len(outs)} artifacts regenerated (no write)")
    else:
        for name in outs:
            print(f"wrote docs/registry/queries/{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
