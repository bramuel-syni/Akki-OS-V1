"""Freeze `conclusion_class` signature — Solva spec §10 + §14 test #2.

`conclusion_class(load_bearing_units) -> DefensibilityClass` — one parameter
only, no confidence, no strength; return type is the frozen Ring 5 enum.
Signature mutation fails CI loudly.
"""
from __future__ import annotations

import inspect
import json
from pathlib import Path

from contracts.five_rings import DefensibilityClass
from services.solva_depth.assertion import conclusion_class


SNAPSHOT = Path(__file__).parent / "conclusion_class_signature.snapshot.json"


def _current_signature_dict() -> dict:
    sig = inspect.signature(conclusion_class)
    return {
        "parameters": [
            {
                "name": p.name,
                "kind": str(p.kind),
                "annotation": p.annotation.__name__ if hasattr(p.annotation, "__name__") else str(p.annotation),
                "default": "empty" if p.default is inspect.Parameter.empty else str(p.default),
            }
            for p in sig.parameters.values()
        ],
        "return_annotation": sig.return_annotation.__name__ if hasattr(sig.return_annotation, "__name__") else str(sig.return_annotation),
    }


def test_conclusion_class_signature_matches_snapshot():
    """The frozen boundary signature MUST match its snapshot."""
    current = _current_signature_dict()
    with SNAPSHOT.open() as f:
        expected = json.load(f)
    assert current == expected, f"Signature drift — current={current} expected={expected}"


def test_conclusion_class_takes_no_confidence():
    """Solva spec §14 #2: strong reasoning cannot raise the class — signature has no confidence input."""
    sig = inspect.signature(conclusion_class)
    param_names = list(sig.parameters.keys())
    assert param_names == ["load_bearing_units"], (
        f"conclusion_class MUST have exactly one parameter 'load_bearing_units'; "
        f"got {param_names}. If the signature grew, source §14 #2 is violated."
    )
    forbidden = {"confidence", "strength", "weight", "probability", "evidence_weight"}
    assert not any(n in forbidden for n in param_names), (
        f"conclusion_class MUST NOT accept any confidence/strength-like parameter; "
        f"got {param_names}."
    )


def test_conclusion_class_returns_defensibility_class():
    """Return type is the frozen Ring 5 enum, not raw str."""
    sig = inspect.signature(conclusion_class)
    assert sig.return_annotation is DefensibilityClass, (
        f"conclusion_class MUST return DefensibilityClass; got {sig.return_annotation!r}."
    )
