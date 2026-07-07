"""Reads consequence_class.v0.json for rule_class→consequence_class mapping
and effective_delay_seconds config."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

_CONFIG_PATH = (
    Path(__file__).parent.parent / "compliance" / "consequence_class.v0.json"
)
_cache: Optional[dict] = None


class UnknownRuleClassError(ValueError):
    pass


def load_config() -> dict:
    global _cache
    if _cache is None:
        with _CONFIG_PATH.open("r", encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def reset_cache_for_tests() -> None:
    """Test helper — invalidates the cache to re-read the JSON file."""
    global _cache
    _cache = None


def consequence_class_for(rule_class: str) -> str:
    cfg = load_config()
    rule_map = cfg.get("rule_class_map") or {}
    if rule_class not in rule_map:
        raise UnknownRuleClassError(
            f"rule_class={rule_class!r} not in consequence_class.v0.json "
            f"rule_class_map; known keys: {sorted(rule_map.keys())}"
        )
    return rule_map[rule_class]


def effective_delay_seconds() -> int:
    cfg = load_config()
    delay = cfg.get("effective_delay_seconds")
    if not isinstance(delay, int) or delay <= 0:
        raise ValueError(
            f"effective_delay_seconds must be positive int in "
            f"consequence_class.v0.json; got {delay!r}"
        )
    return delay
