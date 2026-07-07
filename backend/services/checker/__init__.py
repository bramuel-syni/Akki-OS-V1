"""Phase 8 Seam 3 Sub-stage 3 — §8 consequence-class checker package.

Owner rulings (Amendment G, 2026-07-07):
    * Ruling 1: §12 retrofit collapsed; artifact_ref vestigial-by-ruling;
      existing Sub-stage 2 data-class LB gate extends over new rule-change
      classes. NO parallel sidecar key, NO backfill.
    * Ruling 2: CounterSignBanner renders capacity role (endpoint-required).
    * Ruling 3: object() annotates + escalates + writes tightening_objected
      row, NEVER halts. suspend() is the only halt action.
    * Ruling 4: data_class_registry v0->v1 append rule-change classes.
    * Ruling 5: one atomic commit, no split, no band-widening.
    * Ruling 6: test_every_retention_write_emits_ledger_row_with_consequence_class.
    * Ruling 7: Sub-stage 2 close c17b578b... FINAL ACCEPTANCE.

Standing state-conflict anti-rule (rulings section 8.2 elevated): state
conflicts use HTTP 403 access-control-class response body only.
"""
