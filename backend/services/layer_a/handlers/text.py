"""Layer A text handler.

LIFT_AS_IS dispatch from `/reference/akki-legacy/backend/documents_service.py::extract_text`.
At G0.5 we mount only the .txt / .md / .rtf fast-paths (stdlib) + a
hook for binary formats. Full pdf / docx / pptx / xlsx is on the
LIFT_AS_IS list; we will port the heavy dependencies (pypdf, python-docx,
openpyxl) only when a Service-2 path needs them.
"""
from __future__ import annotations

from pathlib import Path

from services.layer_a.types import RawTextArtifact


def retrieve(source_ref: str) -> RawTextArtifact:
    path = Path(source_ref)
    ext = path.suffix.lower().lstrip(".")
    if ext in {"txt", "md", "csv"}:
        text = path.read_text(encoding="utf-8", errors="replace")
        return RawTextArtifact(text=text, source_format=ext, page_breaks=[], source_ref=source_ref)
    if ext == "rtf":
        # crude rtf strip — G0.5 plumbing; full handler ports from cousin at G2 if needed
        raw = path.read_text(encoding="utf-8", errors="replace")
        stripped = "".join(c for c in raw if c not in {"{", "}", "\\"}).strip()
        return RawTextArtifact(text=stripped, source_format=ext, source_ref=source_ref)
    raise NotImplementedError(
        f"text handler at G0.5 supports txt/md/csv/rtf only; got {ext!r}. "
        "Heavy formats (pdf/docx/pptx/xlsx) port from cousin documents_service when a Service-2 path needs them."
    )
