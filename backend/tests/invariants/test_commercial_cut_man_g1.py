"""Commercial-cut 2026-07-06 — MAN-G1 named regression gate.

BCR v1.4 §12.4 MAN-1 verbatim:
    "Gate MAN-G1: test_no_commercial_symbol_in_extractor_tree
     (grep-negative on price/quote/buyer symbols in the live tree)"

Post-cut, the live extractor tree (`/app/backend/`, `/app/frontend/src/`,
`/app/frontend/e2e/`) MUST NOT locally re-implement any of the
commercial-cut symbols. Only doctrine comments and orphan-in-place
byte-identical contract residue may reference these symbols.

Live-code check: for each forbidden symbol, no import statement (`from
… import`, `import …`) OR class/def declaration (`def <sym>(`,
`class <sym>(` / `class <sym>:`) may exist in the live tree.
Cross-reference doctrine comments (lines beginning with `#` or inside
docstrings) are allowed and expected — they document the cut.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


_ROOT = Path(__file__).resolve().parents[2]  # /app/backend
_APP_ROOT = _ROOT.parent  # /app

FORBIDDEN_COMMERCIAL_SYMBOLS = [
    # Buyer wizard variant (cut whole)
    "BuyerStateMachine",
    "new_buyer_session",
    # Extracted buyer helpers
    "summarise_dual_deltas",
    "compose_objective_request_from_frozen_state_with_proposals",
    "evaluate_dual_delta",
    # Sonnet wizard-agent driver (buyer variant introduction)
    "SonnetWizardAgent",
    "_sonnet_invoke",
    # Frontend buyer §5 surface
    "BuyerShapePage",
    "BuyerAcquirePage",
    "BuyerReceivePage",
    # Frontend buyer wizard client methods (post-cut removed)
    "wizardBuyerStart",
    "wizardBuyerTurn",
    "wizardBuyerPropose",
    "wizardBuyerCommitReview",
    "wizardBuyerFreeze",
    "wizardBuyerHandoff",
    "wizardBuyerGet",
]


_BACKEND_LIVE_ROOTS = [
    _ROOT / "routers",
    _ROOT / "services",
    _ROOT / "contracts",
]

_FRONTEND_LIVE_ROOTS = [
    _APP_ROOT / "frontend" / "src",
    _APP_ROOT / "frontend" / "e2e",
]

_LIVE_TREE_ROOTS = _BACKEND_LIVE_ROOTS + _FRONTEND_LIVE_ROOTS


def _iter_live_source_files():
    for root in _LIVE_TREE_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts:
                continue
            if "node_modules" in path.parts:
                continue
            if path.suffix not in {".py", ".js", ".jsx", ".ts", ".tsx"}:
                continue
            yield path


def _live_code_lines(path: Path):
    """Yield (lineno, code_line) for lines that are NOT pure comments
    or blank. Reasonably filters `#` (Python), `//` (JS/TS single-line),
    and `*` continuation lines inside `/* ... */` blocks."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        # Python line-comment
        if stripped.startswith("#"):
            continue
        # JS/TS line-comment
        if stripped.startswith("//"):
            continue
        # C-style block-comment continuation
        if stripped.startswith("*") or stripped.startswith("/*"):
            continue
        yield lineno, line


@pytest.mark.parametrize("symbol", FORBIDDEN_COMMERCIAL_SYMBOLS)
def test_no_commercial_symbol_in_extractor_tree(symbol: str):
    """Owner-named MAN-G1 gate (BCR v1.4 §12.4). No LIVE-code reference
    to any commercial-cut symbol may exist in the extractor tree post-cut."""
    # Live-code contact patterns per symbol.
    py_def_pattern = re.compile(rf"^\s*def\s+{re.escape(symbol)}\s*\(", re.MULTILINE)
    py_class_pattern = re.compile(rf"^\s*class\s+{re.escape(symbol)}\s*[(:]", re.MULTILINE)
    py_import_pattern = re.compile(rf"^\s*from\s+.*\s+import\s+(.+)$", re.MULTILINE)
    js_const_pattern = re.compile(rf"^\s*(const|let|var|function)\s+{re.escape(symbol)}\b", re.MULTILINE)
    js_import_pattern = re.compile(rf"^\s*import\s+(?:.*\bfrom\s+.*|{re.escape(symbol)}\b)", re.MULTILINE)
    js_object_key_pattern = re.compile(rf"^\s*{re.escape(symbol)}\s*:", re.MULTILINE)

    hits: list[tuple[str, int, str]] = []
    for path in _iter_live_source_files():
        # Reconstruct source text restricted to non-comment lines.
        live_lines_dict = dict(_live_code_lines(path))
        if not live_lines_dict:
            continue
        live_text = "\n".join(live_lines_dict.values())

        py_hit = (py_def_pattern.search(live_text) or py_class_pattern.search(live_text))
        js_hit = (js_const_pattern.search(live_text) or js_object_key_pattern.search(live_text))
        import_hit_py = None
        if path.suffix == ".py":
            for m in py_import_pattern.finditer(live_text):
                imported_symbols = m.group(1)
                if re.search(rf"\b{re.escape(symbol)}\b", imported_symbols):
                    import_hit_py = m
                    break
        import_hit_js = None
        if path.suffix in {".js", ".jsx", ".ts", ".tsx"}:
            for m in js_import_pattern.finditer(live_text):
                line = m.group(0)
                if re.search(rf"\b{re.escape(symbol)}\b", line):
                    import_hit_js = m
                    break

        for hit in (py_hit, js_hit, import_hit_py, import_hit_js):
            if hit is not None:
                # Find the line number in the reconstructed live_text.
                offset = hit.start()
                line_idx = live_text[:offset].count("\n")
                actual_line = list(live_lines_dict.values())[line_idx]
                actual_lineno = list(live_lines_dict.keys())[line_idx]
                hits.append((str(path.relative_to(_APP_ROOT)), actual_lineno, actual_line.strip()))
                break

    assert not hits, (
        f"MAN-G1 violation — commercial-cut symbol {symbol!r} has LIVE-code "
        f"contact in the extractor tree. Post-cut this symbol must exist "
        f"only as: (a) doctrine/lineage comments, or (b) orphan-in-place "
        f"contract byte-identical residue. Hits:\n"
        + "\n".join(f"  {p}:{lineno} {line}" for p, lineno, line in hits)
    )


def test_man_g1_symbol_list_covers_all_named_cut_targets():
    """Sanity — the FORBIDDEN list matches the cut execution manifest."""
    expected_count = 17
    assert len(FORBIDDEN_COMMERCIAL_SYMBOLS) == expected_count, (
        f"MAN-G1 symbol list changed from expected {expected_count} entries; "
        f"regenerate expectation before extending."
    )
    # Assert no duplicates.
    assert len(set(FORBIDDEN_COMMERCIAL_SYMBOLS)) == len(FORBIDDEN_COMMERCIAL_SYMBOLS)
