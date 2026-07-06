"""Phase 8 Stage B-5a — Compliance Console read/prove services.

Modules:
  * `held_class_registry` — single-source enumeration of the three
    separately-addressable held-classes (v2.1 §4.3, Owner E5 seam):
    `ledger_row`, `wizard_transcript`, `delivered_artifact`.
  * `trust_receipt_allowlist` — Amendment 1 (2026-07-06): the anonymous
    trace-view field allowlist derived from the public trust-receipt
    spec (fact + fingerprint). Anonymous responses are BUILT UP from
    this allowlist, never derived by masking off the full record.
  * `refusal_family_classifier` — Amendment 2 (2026-07-06):
    family-by-family classifier for `NorthenaLedgerRow_v1` where
    `decision == "refused"`. Maps deterministic reason strings to
    governed-refusal families for the §4.1 Home refusals-this-month
    aggregate.
  * `retention_config` — service reading the current retention posture
    (global-default + per-class explicit/inheriting/unset) for the
    v2.1 §4.3 Retention & rights surface.
  * `refusals_aggregate` — service aggregating `NorthenaLedgerRow_v1`
    refusal rows by month, grouped by reason AND by day (dev-default
    posture ratified at Stage A).

Standing constraints (B-5a scope):
  * READ-ONLY. Zero writes to persistent stores from any surface here.
  * No LLM. No Shield boundary crossing.
  * Zero touch to frozen contracts (parity 26 stays byte-identical).
  * Uses existing E2 4-code auth-refusal registry — no new codes.
"""
from __future__ import annotations
