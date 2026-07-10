"""Mechanical composer — Answer Fluency §3.8 regression baseline (AF-E4 α).

Owner ruling AF-E4 α (2026-07-10) verbatim: *"α, one ordering condition:
golden snapshots are captured from the pre-3.8 code path before any
refactor lands — capture-then-refactor, or the baseline is
self-referential. AF-G1 compares byte-identically thereafter."*

This module is a **byte-identical extraction** of the pre-3.8 mechanical
`answer_text` f-string at `composed_conclusion.py:330-335`. No logic
changes, no formatting changes. The mechanical composer stays callable
+ tested as the regression baseline against goldens at
`tests/goldens/answer_fluency/pre_3_8/mechanical_baseline.json` (captured
pre-refactor per AF-E4 α ordering condition).

Owner scope anchor (AF-E4 α): *"Mechanical composition retained as
regression baseline; fluency is an upgrade path, not a replacement."*
"""
from __future__ import annotations

from typing import List

from contracts.five_rings import DefensibilityClass


def synthesise_mechanical_answer_text(
    load_bearing_unit_ids: List[str],
    computed_class: DefensibilityClass,
) -> str:
    """Return the mechanical (pre-3.8) `answer_text` string.

    Byte-identical to the pre-refactor f-string at
    `services/service_1/composed_conclusion.py:330-335`. Any drift
    against `mechanical_baseline.json` fails AF-G1.
    """
    return (
        f"Composed conclusion over {len(load_bearing_unit_ids)} "
        f"load-bearing unit(s) at defensibility class "
        f"'{computed_class.value}'. Load-bearing set retrievable "
        f"via Northena Ledger by trace_id."
    )
