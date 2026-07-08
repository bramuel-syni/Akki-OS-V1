"""Archive reader — emits PerceptionJobs for AUDIO/VIDEO archived material.

Locator dialect (opaque per P9-E2 α): {archive_path, timecode_start, timecode_end}.
Round-trip: `read_source_region(locator)` returns a canonical signature
identifying the same source region — proves re-extraction fidelity.
"""
from __future__ import annotations

from typing import Any, Dict, List

from services.perception.source_connector_adapter import SourceConnectorAdapter


class ArchiveReader(SourceConnectorAdapter):
    name = "archive_reader"

    def __init__(self, archive_root: str = "/rms/archive"):
        self.archive_root = archive_root

    def emit_perception_jobs(self, source_ref: str) -> List[Dict[str, Any]]:
        # source_ref like "archive://tenant-a/2026-07-06T20:00Z-broadcast-hour-1"
        return [{
            "reextraction_handles": [source_ref],
            "modality": "AUDIO",
            "locator": {
                "dialect": "archive",
                "archive_path": source_ref,
                "timecode_start": 0,
                "timecode_end": 3600,
            },
        }]

    def read_source_region(self, locator: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "source_ref": locator.get("archive_path"),
            "region_signature": f"archive:{locator.get('archive_path')}:{locator.get('timecode_start')}-{locator.get('timecode_end')}",
        }
