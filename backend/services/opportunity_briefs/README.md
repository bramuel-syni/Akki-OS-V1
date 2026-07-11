# Opportunity Briefs — module directory

**BCR v1.5 §3.15 recommendation module.** Landed per Owner rulings OB-E1 α + OB-E2 α × 3 seams + OB-E3 α (2026-07-10). See `/app/docs/rulings/opportunity_briefs_ob_e1_to_e3.md` for full rulings + `/app/docs/close_reports/opportunity_briefs.md` for close.

## Salvage attestation carrier (OB-R1)

Reasoning patterns in `brief_selector.py` + `brief_proposer.py` are **lifted** from `github.com/bramuel-syni/Akki-Executive-Core` as reference logic — **lifted, not imported; no runtime dependency on any Akki system.**

Lifted design patterns (structural, not code):

1. **Census-slice enumeration** — three-scope walk (slice · combined · estate) matches Akki-Executive-Core's `executive/opportunity/scope_walker.py` structural pattern (single-slice → intersection → global-aggregate cascade). Lifted as structural shape only; no code imported.

2. **Product-shape proposal composition** — the `{gap_statement, precedent, proposal}` triple structure lifted from Akki's `executive/proposal_composer.py` narrative pattern. Adapted to Registry-anchored numerals per OB-R2.

3. **Gap-statement derivation from measured slice** — Akki's "measurement-first opportunity" doctrine lifted at structural level: gap emerges from the slice's measured shape, not from external market data. Reinforces data-blind posture per §8.

No files copied. No imports. No runtime dependency. The salvage is a design reference; the code is native to this repository.

## Modules

- `brief_selector.py` — census-slice selection at three scopes.
- `brief_proposer.py` — product-shape proposal + gap statement (salvage-lifted structure).
- `brief_grounding.py` — mechanical byte-verbatim grounding gate (OB-E1 α · mirrors AF-E1 β Owner Condition 1 discipline).
- `brief_registry.py` — brief-registry write/read layer; own table (`OpportunityBriefRow` sidecar · frozen contracts UNTOUCHED · parity 31 preserved).
- `advisory_marker.py` — write-time attach invariant + render-time reflection (OB-E2 Seam-1 α).
- `shape_as_objective_prefill.py` — commission wizard REACH pre-fill only (OB-R4).
- `brief_telemetry.py` — sidecar telemetry (mirrors 9.2a-E2 α cond 2 + AF-E3 α precedent).
- `generator.py` — orchestrator threading selector → proposer → Shield synthesizer → grounding → registry write.

## Governed-response boundary (OB-E2 Seam-3 α · §6.10 AST/reflection)

`services/service_1/**` MUST NOT `import` anything from `services/opportunity_briefs/**`. Enforced by `test_ob_g_seam3_governed_response_import_boundary` (grep-negative AST walk). No `ComposedConclusion_v0.answer_text` synthesis path can consume brief content — advisory ≠ governed.

## Trace/receipt boundary (OB-E2 Seam-2 α · route-level)

Brief ids use the `brief_` prefix (distinct namespace from `unit_id` / `trace_id` / `run_id` / `cc-unit-`). `GET /api/trace/{id}` returns 404 for `brief_`-prefixed ids. OB-G3 attests.
