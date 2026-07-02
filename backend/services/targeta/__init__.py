"""Targeta — deterministic eligibility core + one-way yield boundary.

Module layout (mandate §7 verbatim):
  * core.py         — deterministic eligibility + ranking; never imports yield
  * yield_layer.py  — learned reorderer; imports ONLY interface types
  * interface.py    — the one-way set-preserving boundary (the guard)
  * gate.py         — yield admission: Arm 1 helps + Arm 2 veto
  * plan.py         — MiningPlan assembly + version stamping
  * modes.py        — portfolio / per_run orchestration

Dependency rules (enforced by import assertions):
  * core.py imports Registry read + governing artifact; never yield_layer;
    never any ML library.
  * yield_layer.py imports ONLY interface types; never floor, raw
    measure, or core's eligibility.
  * gate.py is the ONLY module that compares the two orderings.
"""
