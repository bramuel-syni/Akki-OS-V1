# Standing Queries as CI · SQ-E1 Owner Ruling Record

**Dispatched:** 2026-07-11 (post-Stage-A verbatim relay of SQ-E1).
**Basis:** `/app/docs/stage_a_proposals/standing_queries_as_ci_stage_a.md` @ SHA `942c9f73…`.
**Doctrine SHA:** `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471` (in force).
**Governance:** Standing Rule v3 · on-disk canonical · Registry Doctrine v1.0 R4 + D-10 · §12/§12.1/§12.2/§13/§14 · Defect D7 binds.

---

## §1. Ruling — SQ-E1 · γ (with cross-reference condition)

**Owner verbatim:**

> "SQ-E1 — γ, with one condition. Two files per query, baseline attest over the archaeological files only.
>
> The rationale is the platform's own invention applied reflexively: **provenance-paired facts.** A finding's epistemic source — *ruled by archaeology* versus *detected by mechanical scan* — is exactly the value-plus-source pairing the Registry enforces on estate dimensions, and it deserves structural representation, not an inline tag a reader can miss. γ makes the split byte-visible, mirrors the dual-surface archival posture already ruled at MRR-E2, and keeps the baseline attest honest: the carry-over reproduces the 11 ruled findings losslessly (that *is* the reproduction — the builder's ground-truth analysis showing mechanical scan structurally cannot reproduce them is correct and accepted), while the mechanical files stand as fresh detection candidates for future ruling turns, never mingled with ruled state.
>
> **Condition — cross-reference, never duplicate:** where a mechanical entry's subject overlaps an existing archaeological finding (now or in any future run), the mechanical file annotates with the finding id (`overlaps: Q3-05`) rather than raising it as new — 'zero phantom findings' applies to the mechanical surface too, permanently, not just at baseline.
>
> Baseline failure mode (fail-loud + HALT) confirmed as proposed. Band `[650, 1,400]`: RATIFIED. v0.2 supplement per §14, zero new promises minted — correct conservatism, noted.
>
> Execute: atomic commit → close with gate roster, baseline-attest result shown (11/11 archaeological carry-over + mechanical candidate counts per query), cross-reference condition attested, band actual, D-10 riding."

---

## §2. Doctrinal framing — "provenance-paired facts applied reflexively"

**Canonical citation** (per Owner directive to pin the novel framing):

The Registry's own doctrine on estate dimensions requires each value-carrying fact to be paired with its provenance (source, confidence class, extraction lineage). SQ-E1 γ applies the same discipline **reflexively** to the Registry's own findings: a finding IS a value-plus-source pair where the "value" is the finding text/subject and the "source" is either `ruled-by-archaeology` (Owner has read + ruled) or `detected-by-mechanical-scan` (engine has flagged; awaiting Owner turn). The two provenance classes get byte-visible structural representation — separate files — rather than an inline tag class that a reader can overlook.

**Canonical name:** *provenance-paired facts applied reflexively.*

**Doctrinal position:** SQ-E1 γ ruling · 2026-07-11. Reflexive application of doctrine's estate-dimension provenance discipline to Registry findings themselves. Standing pattern for future query designs.

---

## §3. Applied at execution

**γ output shape** (per Owner verbatim §1):
- Six findings artifacts under `/app/docs/registry/queries/`:
  - `q1_archaeological.md` · `q1_mechanical.md`
  - `q2_archaeological.md` · `q2_mechanical.md`
  - `q3_archaeological.md` · `q3_mechanical.md`

**Archaeological files** (per query · byte-identical carry-over):
- Q1 arch source: `docs/registry/consolidation_log_v0.md` (RP-E1 α + tie-broke-toward-distinct decisions).
- Q2 arch source: v0.md §4 (5 findings Q2-01..Q2-05 with `[RULED · …]` tags).
- Q3 arch source: v0.md §5 (6 findings Q3-01..Q3-06 with `[RULED · …]` tags + `[OWNER: …]` markers).
- Byte-identical reproduction attested by `SQ-G-Baseline` gate.

**Mechanical files** (per query · fresh scan):
- Q1 mech: pair-scan for same-PROM-set + same-surface function-row pairs; cost-ranked with `unknown` sorted to end.
- Q2 mech: 4 sub-cases (a/b/c/d) over function rows.
- Q3 mech: 2 sub-cases (a/b) over function rows + PART_II_JOURNEY_STEPS.

**Cross-reference condition (SQ-G-CrossRef)** — Owner-explicit PERMANENT:
- Mechanical entries whose `subject_identifier` matches any archaeological finding's subject → annotated `overlaps: <finding_id>` inline; NEVER raised as new mechanical entry.
- Zero phantom findings on mechanical surface applies **now or in any future run** — cross-reference is standing discipline, not first-run heuristic.
- Attested by `SQ-G-CrossRef` gate cell.

**Baseline failure mode:** fail-loud + HALT for Owner (matches MRR-G3 discipline). No auto-heal. No auto-degrade.

**Band ratified:** `[650, 1,400]` raw LoC.

**v0.2 supplement:** 10 SQ-G# rows (SQ-G1..SQ-G3 + SQ-G-Baseline + SQ-G-CrossRef + SQ-G-NoRetirement + SQ-G-ReportLevel + SQ-G-Rung1 + SQ-G-Parity + SQ-G-DataBlind). Zero new promises minted (Owner-explicit "correct conservatism, noted").

---

## §4. Standing constraints preserved (per Owner dispatch)

- **D7 binds:** no sequencing harness · no worker context-harnessing · no Registry content changes to v0.md or v0.1_supplement · no Q2-05 reads · no next-cell scaffolds beyond queries scope.
- **v0.md byte-identical** at SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0` throughout.
- **v0.1_supplement byte-identical** at SHA `2822f99e0c20da6f8d02c1f33233965c90df37aeb6939e711da8df2ebd991092` throughout.
- **MRR-G3 round-trip extends** to `(v0.md + v0.1_supplement + v0.2_supplement)` ↔ `registry.yaml` per §14 standing consequence (one-line parser data extension).
- **MANDATE-COMPLETE 2026-07-10 held.** Registry Doctrine v1.0 + §14 in force. Parity 31/31.
- **Cross-reference condition is PERMANENT** — not first-run only.

═══════════════════════════════════════════════════════════════════

*End of SQ-E1 ruling record. Provenance-paired facts applied reflexively pinned as canonical framing (§2). γ + cross-reference condition applied at §3. Standing Rule v3 · on-disk canonical.*
