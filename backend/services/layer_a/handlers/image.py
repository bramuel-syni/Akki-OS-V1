"""Layer A image handler.

LIFT_AS_IS pattern from the cousin's image handling in
`/reference/akki-legacy/backend/documents_service.py::_ocr_image_bytes`
(simplified — OCR is Layer B's job; this handler only reads bytes +
metadata).
"""
from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image

from services.layer_a.types import RawImageArtifact


def retrieve(source_ref: str) -> RawImageArtifact:
    path = Path(source_ref)
    raw = path.read_bytes()
    img = Image.open(BytesIO(raw))
    return RawImageArtifact(
        bytes_=raw,
        width=img.width,
        height=img.height,
        format=(img.format or path.suffix.lstrip(".")).lower(),
        source_ref=source_ref,
    )
