"""Sequencing-harness executor · dispatches registered functions.

Fold A.SH.1 · Registry Doctrine §5.2 verbatim: *"executes registered
functions against fixture traffic"* + *"you do not simulate a
deterministic gate, you run it"*.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Literal


RungLabel = Literal["rung-1", "rung-2", "rung-3", "rung-4"]


@dataclass(frozen=True)
class RegisteredFunction:
    """Handle for a registered function as consumed by the harness."""

    function_id: str
    rung: RungLabel
    callable_ref: Callable[[Any], Any]


def execute_registered_function(
    fn: RegisteredFunction,
    payload: Any,
) -> Any:
    """Execute the registered function against payload · deterministic gates run directly.

    Rung-1/rung-2 deterministic: single-run verdict.
    Rung-3/rung-4 statistical: driven via measurement.run_statistical_measurement().

    This function is the primitive dispatch cell; statistical repetition
    is the concern of measurement.py.
    """
    return fn.callable_ref(payload)
