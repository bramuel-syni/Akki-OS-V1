"""CMS reader — emits TEXT-modality units direct to intake (V1-I4)."""
from __future__ import annotations

from typing import Any, Dict, List

from services.perception.source_connector_adapter import SourceConnectorAdapter


class CmsReader(SourceConnectorAdapter):
    name = "cms_reader"

    def __init__(self, cms_endpoint: str = "https://cms.internal"):
        self.cms_endpoint = cms_endpoint

    def emit_direct_intake_units(self, source_ref: str) -> List[Dict[str, Any]]:
        # source_ref like "cms://tenant-a/item-42"
        return [{
            "modality": "TEXT",
            "content_ref": source_ref,
            "locator": {"dialect": "cms", "cms_url": source_ref, "item_id": source_ref.split("/")[-1]},
        }]

    def read_source_region(self, locator: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "source_ref": locator.get("cms_url"),
            "region_signature": f"cms:{locator.get('cms_url')}:{locator.get('item_id')}",
        }
