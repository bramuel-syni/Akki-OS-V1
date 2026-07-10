"""Defensibility class loader (TF-E3 α condition — single-source vocabulary).

Owner ruling TF-E3 α + condition (2026-07-08):

    'α, one condition: single-source the class vocabulary. Settled
     doctrine (CK-I1 never-a-widening-Literal; registry precedents at
     B-5b/8-EXT/AS). Condition: defensibility_classes.v0.json is seeded
     verbatim from the class vocabulary the production composition path
     emits today and becomes the canonical registry going forward —
     existing frozen contracts stay byte-identical; no second vocabulary
     may diverge from this one. Gate added: registry ⊇ every class the
     live composition path can emit.'

Landing:
  * `ALLOWED_DEFENSIBILITY_CLASSES` — frozenset loaded from JSON at import.
  * `validate_defensibility_class(class_)` — raises ValueError if not in
    the registry. Used by KA construction paths.
  * TF-G8 (`test_defensibility_registry_superset_live_composition_path`)
    asserts the registry is a superset of every class the live
    composition path (`five_rings.DefensibilityClass`) can emit.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, FrozenSet


_REGISTRY_PATH = Path(__file__).parent / "defensibility_classes.v0.json"


def load_defensibility_classes() -> Dict[str, Any]:
    """Load the canonical registry JSON. Called at module import + on-demand."""
    with _REGISTRY_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


_registry = load_defensibility_classes()
ALLOWED_DEFENSIBILITY_CLASSES: FrozenSet[str] = frozenset(_registry["classes"].keys())


def validate_defensibility_class(class_: str) -> str:
    """Validate a defensibility class label against the canonical registry.

    Returns the label unchanged if valid; raises ValueError if not.
    """
    if class_ not in ALLOWED_DEFENSIBILITY_CLASSES:
        raise ValueError(
            f"defensibility class {class_!r} not in canonical registry "
            f"({sorted(ALLOWED_DEFENSIBILITY_CLASSES)}). "
            "Additive widening requires an update to "
            "`defensibility_classes.v0.json`."
        )
    return class_
