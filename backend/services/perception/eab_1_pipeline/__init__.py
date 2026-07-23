"""EAB-1 pipeline · A1+A2 folds (ingestion side, one seam).

Landed under Owner E1 ruling 2026-07-15 (docs/rulings/eab_1_e1_2026-07-15.md).
Executes EAB-1 Stage A d5231d93… under D-12 (mechanics deploy in force with
known parameters; zero observe-first, zero staged proving).

A1 · Pre-perception restructuring pass (CPU-only):
    a1_demux           — A1.1 · demux/normalize (source → canonical audio artifact)
    a1_segmentation    — A1.2 · content-addressed batch segmentation
    a1_vad             — A1.3 · Silero registry-pinned VAD wrapper
    a1_dedup           — A1.4 · acoustic-fingerprint dedup emitting canonical/occurrence

A2 · Occurrence index:
    a2_occurrence_writer — A2.1 · occurrence rows as NormalizedUnits
    a2_license_class     — A2.2 · license_class fail-closed attachment (MC-E4 α reuse)
    a2_trace_walker      — A2.3 · SINGLE CODE PATH resolver (FENCE 1)

FENCE 1: trace resolver has ONE code path; no `if modality == "occurrence"`
         or `if source_type == "structured"` branch anywhere.
FENCE 2: audit-walk cell (test_a2_end_to_end_audit_walk.py) exercises a
         real occurrence unit through the production resolver, not a
         synthetic locator dict.

Parity 31 held byte-identical: batch schema lives HERE (worker-side), NOT in
backend/contracts/. MC-E3 α placement precedent. AST cell at
backend/tests/invariants/test_five_rings_v0_zero_mutation_ast_cell.py
fails the build hard on any five_rings@v0 drift.
"""
