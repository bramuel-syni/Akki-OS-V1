"""Northena — the direction governor (mandate `/app/docs/mandates/northena_v1.0.md`).

Package entrypoints. Every module in this package cites the mandate
section it binds to. Solva/SyniSense are integrated, NOT re-built here
(N-INV-11 grep-tested).
"""
from services.northena import admit, converge, gate, ledger, state_machine  # noqa: F401
