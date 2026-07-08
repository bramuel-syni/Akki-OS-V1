"""Social-account reader — emits TEXT-modality units direct to intake.

Owned account credentials only per BCR §3.1 V1-U3 (owned sources only).
"""
from __future__ import annotations

from typing import Any, Dict, List

from services.perception.source_connector_adapter import SourceConnectorAdapter


class SocialReader(SourceConnectorAdapter):
    name = "social_reader"

    def __init__(self, platform: str = "twitter"):
        self.platform = platform

    def emit_direct_intake_units(self, source_ref: str) -> List[Dict[str, Any]]:
        # source_ref like "social://twitter/@owned_acct/post-1234"
        parts = source_ref.replace("social://", "").split("/", 2)
        platform = parts[0] if parts else self.platform
        account_ref = parts[1] if len(parts) > 1 else ""
        post_id = parts[2] if len(parts) > 2 else ""
        return [{
            "modality": "TEXT",
            "content_ref": source_ref,
            "locator": {
                "dialect": "social",
                "platform": platform,
                "account_ref": account_ref,
                "post_id": post_id,
            },
        }]

    def read_source_region(self, locator: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "source_ref": f"social://{locator.get('platform')}/{locator.get('account_ref')}/{locator.get('post_id')}",
            "region_signature": f"social:{locator.get('platform')}:{locator.get('account_ref')}:{locator.get('post_id')}",
        }
