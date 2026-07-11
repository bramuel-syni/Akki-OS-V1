# §3.15 Opportunity Briefs — Rulings Record (OB-E1..OB-E3)

**Dispatch:** Owner rulings on Opportunity Briefs Stage A escalations (2026-07-10 · post-§3.8-Answer-Fluency-ratification).
**Basis:** Stage A proposal at `/app/docs/stage_a_proposals/opportunity_briefs.md` (SHA `39061210811943e21a5d1f68da99d356430e0a3bd7d52dc4829ba5fc373d8ab6`).
**Governance:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. §12 close-ratification-on-own-text (2026-07-10). §12.1 remaining-gates enumeration.
**Standing Rule v3:** on-disk canonical.
**Execution close:** `/app/docs/close_reports/opportunity_briefs.md`.

---

## §1. Owner rulings — verbatim carriers

### §1.1 OB-E1 α — Structured anchor + byte-verbatim substring check (Owner-ruled)

> **OB-E1 — α.** Structured anchor + byte-verbatim substring check, whole-brief reject on any failure, gate never patches — the AF-E1 β grammar ported intact, including its conditions (mechanical check, no semantic scoring). β declined: the "correct numeric from wrong read" gap it closes is citation precision, not fabrication — OB-R2's promise is no-fabricated-values, α closes it fully, and per-slice citation accuracy for Combined briefs is already OB-G5's job under E3 below. No gate beyond the promise.

**Disposition — applied verbatim:**

- LLM emits `{brief_text, quantitative_anchors: [{value, registry_read_ref}]}` structured JSON via Shield chokepoint at `services/synisense/shield/brief_synthesizer.py` (mirrors AF-E1 β precedent).
- Grounding gate at `services/opportunity_briefs/brief_grounding.py::verify_brief_grounding(...)`:
  - **(A) byte-verbatim value check:** every `value` in `quantitative_anchors` MUST appear byte-verbatim in the text of the Registry read at `registry_read_ref`. Mechanical byte-substring check; **no semantic scoring**.
  - **(B) numeric-coverage check:** every numeric appearing in `brief_text` (regex `[0-9]+(?:[.,][0-9]+)*%?`) MUST have a corresponding anchor entry with byte-matching `value`.
  - **(C) whole-brief reject (Owner-verbatim):** *"whole-brief reject on any failure, gate never patches"* — any (A)/(B) failure → brief NOT emitted; regeneration tagged `grounding_reject`; gate NEVER edits the brief.
- β declined per Owner rationale (citation precision vs fabrication distinction); β is not a gap OB-R2 protects against — that's OB-G5's job under OB-E3 α (per-slice citation for Combined briefs).

### §1.2 OB-E2 α across all three seams (Owner-ruled)

> **OB-E2 — α across all three seams.** Write-time attach + render reflection walk (Seam-1), route-level 404 with distinct `brief_id` namespace (Seam-2), grep-negative import boundary on the governed-response path (Seam-3). All three are the established §6.10 mechanism class (AS-G6/TF-G9/FR-G4 lineage) — mechanism enforced by structure, proven by gate, no new precedent minted. Seam-1 β stays acknowledged as the future contract-touch path, not selected.

**Disposition — applied verbatim per seam:**

**Seam-1 · Advisory marker on every render path — α:**
- `services/opportunity_briefs/advisory_marker.py::attach(brief)` invariant runs at Registry write time.
- Frontend render component (`OpportunityBriefCard`) reads the marker from the sidecar payload; render-time reflection walk (part of `test_af_g2_advisory_marker_present_on_every_brief_render`) confirms no frontend render code path can strip or hide the marker.
- Seam-1 β (contract-embed marker in frozen `OpportunityBrief_v0::advisory=True`) explicitly declined; acknowledged as future-additive path if a client-facing disclosure need emerges; **not selected** — parity 31 preserved.

**Seam-2 · Brief exclusion from trace/receipt resolution — α:**
- Distinct `brief_id` namespace: brief ids carry the prefix `brief_` (distinct from `unit_id` / `trace_id` / `run_id` / `cc-unit-` prefixes).
- Route-level 404 at trace/receipt resolution surfaces: `GET /api/trace/{id}` explicitly REJECTS brief-scoped ids with HTTP 404 (in `services/northena/trace_ledger.py` + router layer).
- OB-G3 E2E cell attests.

**Seam-3 · Brief content excluded from governed response — α:**
- §6.10 reflection walk (AST/reflection gate class established across AS-G6 / TF-G9 / FR-G4 / AF-G6b lineage · no new precedent minted per Owner ruling).
- Grep-negative on `services/service_1/**` for any `import ... services/opportunity_briefs/**` path.
- AST attest that no `ComposedConclusion_v0` `answer_text` synthesis path can consume brief content.

### §1.3 OB-E3 α — Registry-computable aggregate = Registry-exposed native (Owner-ruled)

> **OB-E3 — α.** A Registry-computable aggregate is one the Registry read API itself exposes and the brief quotes byte-verbatim; synthesis-time computation forbidden. This is the mandate's own sentence made mechanical — the Registry computes, the brief quotes. β moves computation to the exact layer the rule exists to keep it out of; γ guts Combined scope.

**Disposition — applied verbatim:**

- Registry-computable aggregate = a numeric field the Registry read API (`services/mtafiti/registry.py`) exposes as its own read (e.g., `count_of_units_in_slice(slice_id) → int`).
- The brief quotes the returned value byte-verbatim in `brief_text` with corresponding `registry_read_ref` in `quantitative_anchors`.
- **Synthesis-time computation FORBIDDEN:** no `sum(...)` / `avg(...)` / `min(...)` / `max(...)` / `count(...)` or equivalent operator applied inside `services/synisense/shield/brief_synthesizer.py` or `services/opportunity_briefs/brief_proposer.py` at synthesis time.
- Enforcement: §6.10 grep-negative reflection gate on generator + synthesizer paths for the operator whitelist.
- β (whitelisted operator replay) explicitly declined; γ (no aggregates) explicitly declined.
- Rationale (Owner verbatim): *"the mandate's own sentence made mechanical — the Registry computes, the brief quotes."*

### §1.4 Band `[1,300, 1,900]` — RATIFIED (Owner-ruled)

> **Band `[1,300, 1,900]`: RATIFIED.** Projected §4.2 crossing under α is Tier-2 disclosure per §12.1; split-fallback at the stated seam pre-authorized, atomic attempted first, dev's judgment, disclosed at close.

**Disposition:** band ratified. §4.2 raw threshold projected-CROSSED under scenario α (1,573 vs 1,500) — per governance §12.1 (Owner 2026-07-10 · verbatim): *"§4.2 thresholds and band disclosures — Tier-2, disclosure-only, never blocking."* Split-fallback pre-authorised at natural seam per Stage A §3.6. Atomic attempted first per §4.1 baseline; autonomous split fires if cumulative diff crosses mid-execution.

### §1.5 Acknowledgments (Owner-ruled)

> Dead-tracker sweep and §12/§12.1 landings: acknowledged as correct.

Acknowledged. §12 close-ratification-on-own-text applies at close-landing:
- (a) named gates green
- (b) rulings attested as applied
- (c) no new Tier-1 escalation surfaced during execution
If all three met, close ratifies on its own text.

---

## §2. Execution posture

### §2.1 Sequence (Owner-directive verbatim)

> **Execute:** atomic (or split at the seam) → close with gate roster OB-G1..G5 + the three seam gates, band actual in raw LoC, parity 31 attested, Tier-3 defaults one line each.
> Then §3.4 production housing — PH-R1 dispatches on OB's close.

**Applied:** atomic single commit attempted first. Split-fallback autonomous at natural seam per Stage A §3.6. §3.4 PH-R1 Stage A dispatches on OB close-landing per Owner pre-clearance.

### §2.2 No refusal-envelope emission on any runtime path

Refusal taxonomy (`admission_refusal` + `service_1_refusal`) untouched at OB scope. Briefs are ADVISORY output; brief-generation failures → mechanical fallback (stale-brief marking) OR grounding-reject (brief NOT written); NEVER a refusal envelope. §0.1 disposition from AF-E2 amended is AF-scope-only per Owner; briefs run under §12.1 remaining-gates posture.

### §2.3 Frozen contracts untouched

31 preserved. OB lands via new-registry-table pattern (`OpportunityBriefRow` sidecar) + sidecar telemetry (mirrors 9.2a-E2 α cond 2 + AF-E3 α precedent). Attested at OB-G-Parity.

### §2.4 No new precedent

Mechanism classes reused:
- **AF-E1 β + Condition 1 grounding grammar** → OB-E1 α byte-verbatim substring check.
- **§6.10 AST/reflection (AS-G6 / TF-G9 / FR-G4 / AF-G6b lineage)** → OB-E2 Seam-1/2/3 α mechanism.
- **Sidecar telemetry (9.2a-E2 α cond 2 + AF-E3 α)** → OB fluency-mode-style observability.
- **Shield chokepoint (Phase 7 Stage B-2)** → OB brief_synthesizer via `llm_router::_provider_for("analytical")`.

---

## §3. Gate roster (executed · full attestation at close)

| Gate | Tier | Purpose | Location |
|---|---|---|---|
| **OB-G1** | Tier-1 (OB-R2) | test_brief_numbers_are_registry_reads_verbatim | `test_opportunity_briefs_ob_g1_to_g5.py::test_ob_g1_*` |
| **OB-G2** | Tier-1 (OB-R3 Seam-1) | test_advisory_marker_present_on_every_brief_render | `...::test_ob_g2_*` |
| **OB-G3** | Tier-1 (OB-R3 Seam-2) | test_brief_excluded_from_trace_resolution (route 404 + namespace) | `...::test_ob_g3_*` |
| **OB-G4** | Tier-3 (OB-R4) | test_shape_as_objective_prefills_reach_only | `...::test_ob_g4_*` |
| **OB-G5** | Tier-1 (OB-R6) | test_combined_brief_numbers_trace_to_each_contributing_slice | `...::test_ob_g5_*` |
| **Seam-1 sub-gate** | Tier-1 | render-time reflection walk (attach + no-strip) | `...::test_ob_g2_seam1_no_strip_ast` |
| **Seam-2 sub-gate** | Tier-1 | brief_id namespace distinctness attest | `...::test_ob_g3_seam2_namespace_distinct` |
| **Seam-3 sub-gate** | Tier-1 (§6.10 AST) | grep-negative service_1/** → opportunity_briefs/** import | `...::test_ob_g_seam3_governed_response_import_boundary` |
| **OB-G-DB** | Tier-1 (§8 data-blind) | brief prompt template no residues | `...::test_ob_g_db_*` |
| **OB-G-Parity** | Tier-1 (frozen contracts) | parity 31 preserved | `...::test_ob_g_parity_31` |
| **OB-G-Refresh** | Tier-3 (OB-R5) | stale marking on census change | `...::test_ob_g_refresh_*` |
| **OB-G-Grounding-Fail** | Tier-1 (OB-R2 fail path) | grounding fail prevents brief write | `...::test_ob_g_grounding_fail_*` |
| **OB-G-E3-No-Synth-Compute** | Tier-1 (OB-E3 α · §6.10) | grep-negative synthesis-time aggregate operators | `...::test_ob_g_e3_no_synthesis_compute_ast` |

---

## §4. Standing constraints preserved

| Constraint | Attest |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | OB-G-Parity |
| 4-code auth-refusal registry closed | GREEN — not an auth surface |
| No HTTP 409 in OB new/modified files (E5) | GREEN — 503 boundary reuse from Shield precedent · no 409 |
| Standing Rule v3 | GREEN — this record on-disk canonical |
| AS-H1 retention held-class | GREEN — OB-R5 preserves stale briefs; no DELETE handlers |
| Governance §8 data-blind posture | OB-G-DB |
| Governance §9 metric-verdict-in-derivation-unit | GREEN — raw LoC (band-relative) |
| Governance §10 9.2 split ruling | GREEN — OB dispatch-independent from 9.2a/9.2b |
| Governance §11 9.2-OWN resolution | N/A (OB is control-plane) |
| Governance §12 close-ratification-on-own-text | applied at close-landing |
| Governance §12.1 remaining-gates | applied (Tier-1 verbatim ruling loop covers OB-R2/R3/R6) |
| AF-E2 amended boundary set (Standing Disposition 2026-07-10 · AF-scope-only) | preserved · scoped to AF; briefs under §12.1 posture |
| AF-E3 α sidecar telemetry precedent | reused |
| AS-U2 sample rules (fixture-census demo permitted) | applied |
| OB-R1 salvage-lifted-not-imported | attested via `services/opportunity_briefs/README.md` salvage carrier |

---

## §5. Provenance

- **Stage A proposal:** `/app/docs/stage_a_proposals/opportunity_briefs.md` (SHA `39061210...`)
- **Rulings record (this file):** `/app/docs/rulings/opportunity_briefs_ob_e1_to_e3.md`
- **Close report:** `/app/docs/close_reports/opportunity_briefs.md`
- **Salvage carrier (OB-R1):** `/app/backend/services/opportunity_briefs/README.md`
- **Landing commit SHA:** recorded post-commit (Emergent platform auto-commits).
- **Test attestation:** at close.
- **Parity:** 31/31 byte-identical (OB-G-Parity).
