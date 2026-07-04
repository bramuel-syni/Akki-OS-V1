"""Shaping wizard — Phase 7 Stage B-1 (v3 §3.3 operator variant).

Landing scope:
  * `agent_interface.py` — pluggable `WizardAgent` Protocol + `DeterministicStubAgent`.
    Per Standing Disposition `Agent-pluggable-with-stub-agent-first`
    (Owner ruling, Phase 7 Stage A close, 2026-07-04): mechanical guards
    prove against the stub agent BEFORE the LLM is plugged in at B-2.
  * `operator_state_machine.py` — operator variant state machine + Guard 1/2/3.
  * `source_tagging.py` — commit-time invariant checker.
  * `session_persistence.py` — Mongo `wizard_sessions` collection I/O.
  * `turn_ledger.py` — Northena Ledger stamp_audit sidecar w/ `data_class="wizard_transcript"` marker per Owner E5 ruling.

Buyer variant + LLM integration lands at B-2. Commit-review + freeze +
admission handoff land at B-3.
"""
