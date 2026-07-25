"""Far-endpoint mandate reader · fold C.FE.1.

Reads on-disk mandate documents at `docs/mandates/*.md` and extracts
structured content (title + gate-declaring stanzas).

Registry Doctrine §8.1 (e) verbatim: *"mandates as structured specs from
which gates are generated"* — this module handles the input side.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
from dataclasses import dataclass
from typing import List, Optional


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
MANDATES_DIR = REPO_ROOT / "docs" / "mandates"


@dataclass(frozen=True)
class ParsedMandate:
    """Structured content extracted from one mandate document."""

    source_path: str  # repo-root-relative
    source_sha_256: str  # 64-hex SHA-256 of file contents
    title: str
    gate_stanzas: List[str]  # verbatim gate-declaring lines


_TITLE_RE = re.compile(r"^#\s+(.*)$", re.MULTILINE)
# Gate-declaring stanza pattern: lines that look like machine-actionable
# gates. G-13 landing uses a conservative default: any bullet or
# paragraph containing a "must/MUST" or "refuse/reject" keyword is a
# candidate. Concrete refinement follows a future engine-version bump
# (Class E · out of scope this atomic).
_GATE_KEYWORD_RE = re.compile(
    r"\b(?:MUST|must|refuse[sd]?|reject[sd]?|hard[-\s]fail|B-\d+|Binding)\b"
)


def _sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_mandate(path: pathlib.Path) -> ParsedMandate:
    """Parse a single mandate document into structured form."""
    text_bytes = path.read_bytes()
    text = text_bytes.decode("utf-8")
    title_match = _TITLE_RE.search(text)
    title = title_match.group(1).strip() if title_match else path.stem
    gate_stanzas = [
        line.strip()
        for line in text.split("\n")
        if _GATE_KEYWORD_RE.search(line) and line.strip()
    ]
    # Deterministic: preserve source order (matches Owner-verbatim
    # "deterministic — same mandate input yields byte-identical YAML").
    return ParsedMandate(
        source_path=str(path.relative_to(REPO_ROOT)),
        source_sha_256=_sha256_hex(text_bytes),
        title=title,
        gate_stanzas=gate_stanzas,
    )


def list_mandate_paths() -> List[pathlib.Path]:
    """Return sorted list of mandate document paths."""
    if not MANDATES_DIR.exists():
        return []
    return sorted(MANDATES_DIR.glob("*.md"))
