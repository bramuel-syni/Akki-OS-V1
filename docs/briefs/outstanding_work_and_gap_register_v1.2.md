# Outstanding Work & Gap Register · v1.2 · 2026-07-14
**Authority:** Owner-ratified via ruling `docs/rulings/g10_g7_promote_2026-07-14.md`. **Purpose:** the single authoritative record of all outstanding work and all discovered-gap fixes as of this date. Survives context compaction on either side: where any future in-context summary conflicts with this document, THIS DOCUMENT GOVERNS until an Owner ruling supersedes it. **This register contains no schedule.** Sequencing inside sanctioned lanes is the ruling authority's; owner decisions are marked OWNER; nothing here is deadline-bearing. **This register adds no scope.** Every item cites its origin. A work item not traceable to this register or a later ruling is defect D7.

## §1 · Proven state (context, one paragraph)
BCR v1.5 mandate-complete (2026-07-10). Engine conformance audit (2026-07-12): Solva 12/12, Targeta 11/11, Mtafiti 7/7, Northena 7/7 BUILT against on-disk mandates; SyniSense 19 rows with one PARTIAL (custody chain, closed at IF-1 2026-07-14). Registry Doctrine v1.0 in force; Registry populated (46 promises · 66+ functions · v0 + supplements v0.1/v0.2/v0.3/v0.4); machine-readable form + parser/validator live. Operating Values v1.0 on-disk. Deviation audit baseline: 64,762 live LoC; 24-row deviation table on-disk. **G-10/G-7 PROMOTE closed 2026-07-14:** TraceReceiptPage promoted to public `/trace/:traceId`; seven other legacy pages + AppShell chrome retired; 1241 backend tests + 154 jest tests + 3 playwright smokes all GREEN.

## §2 · In-flight (dispatched, close owed)
*None.* IF-1 closed 2026-07-14 (custody-chain reconnection · dead-code shave · triad reconciliation). G-10/G-7 PROMOTE closed 2026-07-14 (atomic commit). Next dispatched item is Owner's to signal.

## §3 · Loose threads (status owed in next builder reply)
**LT-1 · Standing Queries as CI:** SQ-E1 ruled γ + condition; execution ordered; no close returned. Status: closed/in-progress/not-started, with evidence.
**LT-2 · sequencing_harness_stage_a.md** exists on-disk but was never dispatched. Provenance: when created, by what instruction. If unsanctioned pre-work: D7 finding, file held (not deleted) pending Owner disposition.

## §4 · Gap register — every discovered gap and its fix
| # | Gap | Evidence | Fix | Authority/status |
|---|---|---|---|---|
| G-1 | Shield custody chain unreachable from live LLM path | Conformance Part A.5; deviation rows (1,023 LoC chain) | Reconnection per IF-1 | **CLOSED 2026-07-14 (IF-1)** — v0.3 supplement §S1 rows IF1-G1/G2/G3 attest chain; triad GREEN. |
| G-2 | Registry lags conformance reality (custody functions absent; modes.py SUPERSEDED not carried; conformance evidence uncited) | Conformance tables vs registry v0 + supplements | Registry maintenance turn: fold conformance results; execute Q2-05 individual reads; canonicalize S3.prove/S4.verify aliases; consolidate v0.1/v0.2 supplements → Registry v1 | SANCTIONED lane; awaits Owner sequencing |
| G-3 | Operating Values v1.0 predates conformance findings | §1 model census omits spaCy NER (rung 2, live in Shield); diarization row states pyannote decision while build carries Silero(+seat); Solva weighting seat unrecorded | Revise to v1.1: add spaCy row (rung 2, en_core_web_trf/sm, fail-closed role); reconcile diarization row to built-state + decided-target; record Bayesian weighting as measurement-era seat under extraction_params@v0; carry §10-style amendment note | SANCTIONED; rides after G-2 so v1.1 cites Registry v1 |
| G-4 | S1 envelope-completeness (receipts machine-passable) has no direct cell | Registry Q3-01 (reclassified: platform-side, narrowed scope) | Candidate cell lands in next test-bearing phase (G-2 turn); one cell, no new surface | SANCTIONED |
| G-5 | S1.scoped-key has only indirect coverage | Q3-05 | Direct cell, same vehicle as G-4 | SANCTIONED |
| G-6 | Northena audit-walk: view-side covered, walk-side uncovered | Q3-06 | Walk-side cell, same vehicle as G-4 | SANCTIONED |
| G-7 | SolvaTrace three-lens UX commitment (Spec §5): rendering surface unverified | Read at G-10/G-7 dispatch: surface existed at `src/legacy/pages/TraceReceiptPage.js` with all three lenses wired; live consumer was Ask Console's Trust receipt hrefs | Promoted to public `/trace` + `/trace/:traceId`; nine R4 rows in v0.4 supplement §S1/§S2; playwright smoke attests three-lens render at promoted route | **CLOSED 2026-07-14 (G-10/G-7 PROMOTE)** |
| G-8 | S2.onboard: journey step + full requirements (Op. Values §8) exist; no surface | Q3-02, ruled open-by-design | Build timing is an OWNER decision, raised 2026-07-12, unanswered. Register holds it OPEN-OWNER; no default implied | OWNER (OD-1) |
| G-9 | S4 buyer-commercial tier: requirements defined (Op. Values §7); surface salvaged | Q3-03 ruling | Restores when Owner rules a commercial posture | OWNER (standing ruling) |
| G-10 | Frontend /legacy/* (1,118 LoC) disposition | Deviation table, entangled | At IF-1 close: only live consumer of `/legacy/*` was Ask Console's Trust receipt hrefs → TraceReceiptPage; other seven pages had zero external consumers | **CLOSED 2026-07-14 (G-10/G-7 PROMOTE)** — TraceReceiptPage promoted; seven other pages + AppShell chrome retired; v0.4 supplement §S2 attests seven fs-negatives |
| G-11 | Two perception paths (Shield perception_router w/ stub fallback · local 9.2a workers) | Bundle finding | NOT a defect: API-path vs in-perimeter path serve different venues. Fix = Registry v1 records both with distinct service traces; any retirement is a future OWNER ruling on evidence | RECORD in G-2 |
| G-12 | SyniSense lacks its own Mandate & Engineering Spec | Amendment 2026-07-12 · v1.1 §11 | Owner authors from built reality + bundle's distributed spec surface; lands as fifth governed mandate; SyniSense re-anchors at Registry maintenance turn | OWNER (OD-7) |
| G-13 | ALLOWED_PURPOSES carried cousin's chat.* vocabulary | Amendment 2026-07-12 · v1.1 §11 | Prune to RMS-live purposes | **CLOSED 2026-07-14 (IF-1)** — `purpose_validator.py` shaved whole (v0.3 supplement §S2 row 5) |

## §5 · Engine seats — designed-empty, NOT gaps (guard against re-litigation)
Solva Probability weighting: equal-weight default; method = measurement-era value under extraction_params@v0. Targeta yield layer: spec-mandated to wait for mining history; learning-method decision recorded for that era. Rung-3 owned text models: dependency-gated on estate corpus.

## §6 · Owner-decision register (raised; no deadlines; no defaults)
OD-1 S2.onboard build timing (G-8). ~~OD-2 /legacy/* disposition (G-10, after evidence).~~ **DISCHARGED 2026-07-14 (G-10/G-7 PROMOTE).** OD-3 Single-ingress navigation (after designer walkthrough; walkthrough itself is owner-side, standing). OD-4 9.2b "proceed". OD-5 PH-R2/R3/R4 bindings (acceptance criteria pre-defined in Op. Values §9). ~~OD-6 Trace-lens build timing IF G-7 returns data-only.~~ **DISCHARGED 2026-07-14 (three-lens surface is live-visible, not data-only).** OD-7 SyniSense Mandate & Engineering Spec authoring (G-12).

## §7 · Proceed-gated register (environment; no build motion possible)
Rung-1 domain-transfer measurement → adapter decisions → BM-V (bar: Op. Values §4) → BM-C operations (§5). Production model acquisition per §1/§2. PBK-2 deploy-attest at PH-R2/R4 window. All activate on OD-4/OD-5; none is builder motion today.

## §8 · Undispatched doctrine surface (no schedule exists or is implied)
§8.1.b sequencing harness (pending LT-2 provenance) · §8.1.c worker context-harnessing · §8.1.e mandates→specs→gates endpoint · MRR-E1 β graduation (future governance amendment) · Instance Replication Playbook · Commercial Thesis (ruling-authority drafts, on Owner word).

## §9 · Binding disciplines carried (violations are D-10-class findings)
Canon before ruling (D-11) · no re-derivation · complete dispatches · decisions-not-menus to Owner · rules pay rent · verdicts never curated · no invented schedules (D7) · evidence-classed assertions (Solva discipline).

## §10 · What this document is not
Not a schedule. Not new scope. Not a secondary goal carrier: no item herein authorizes work beyond its stated fix; product specs and function requirements are altered only by Owner ruling, never by register drift. Supersession: only by Owner ruling recorded in docs/rulings/.

## §11 · Amendment 1 · 2026-07-12 (Owner-ratified) — carried from v1.1 §11
Predecessor: v1.0 at SHA cce17296a70b46ae6e1a1c64be1e9e3f18ca3f86a716758899037cf31f4d63d4. Ruling: docs/rulings/outstanding_register_v1_amendment_2026-07-12.md (SHA 06f51bf67d3c3b34024a814fd5d00bc6eb62c749181ac8945cf45f56f309ba27). Body of amendment as recorded in v1.1 §11 (verbatim, carried into v1.2 by reference — v1.1 remains canonical for the amendment text at SHA `01016e2f679064613f6290ee4f50bdaa9874fb2e6b3c3973ccad53d3339f3224`).

## §12 · Amendment 2 · 2026-07-14 (Owner-ratified) — G-10/G-7 PROMOTE close
Predecessor: v1.1 at SHA `01016e2f679064613f6290ee4f50bdaa9874fb2e6b3c3973ccad53d3339f3224`. Ruling: `docs/rulings/g10_g7_promote_2026-07-14.md`.

Closes in one atomic commit (alongside IF-1 test-triad reconciliation):

- **G-7 (§4)**: CLOSED. Three-lens rendering surface promoted from `/legacy/*` archive to public `/trace` + `/trace/:traceId`. Playwright smoke `frontend/e2e/trace_smoke.spec.ts` attests the render at the promoted route.
- **G-10 (§4)**: CLOSED. TraceReceiptPage lifted out; the remaining seven legacy pages (`LandingPage`, `OperatorDashboard`, `RunsPage`, `RunDetailPage`, `DisciplinePage`, `EnginesPage`, `ComposePage`) retired whole; `src/components/AppShell.js` retired (only consumer was the legacy shell); `<Route path="legacy">` block removed from `src/App.js`; `AskConsolePage.js` Trust receipt hrefs updated from `/legacy/trace/${trace_id}` to `/trace/${trace_id}`.
- **OD-2 (§6)**: DISCHARGED (subsumed by the atomic PROMOTE-and-SHAVE ruling — no separate Owner decision needed).
- **OD-6 (§6)**: DISCHARGED (three-lens surface is live-visible, so the "data-only → OWNER decision" branch does not trigger).
- **Registry reflex (§4 · Registry Doctrine v1.0 §3.3 R4)**: v0.4 supplement lands with 9 R4 reflexive rows (2 promote/retire + 7 legacy-page shave-attestations). Prior supplements v0.1 · v0.2 · v0.3 byte-identical. v0.md byte-identical (SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0`).
- **Parity 31 preserved**: 31 contract snapshots under `backend/tests/invariants/` byte-identical; 1001 invariant tests GREEN; 1241 backend tests total GREEN.
- **G-13 (§4, added at Amendment 1)**: CLOSED at IF-1 2026-07-14 — the purpose-catalogue prune was executed as the shave of `services/synisense/shield/purpose_validator.py` (v0.3 supplement §S2 row 5) plus removal of `ALLOWED_PURPOSES` from `services/synisense/config.py`.

**Exit gates satisfied (verbatim from ruling §4):** triad reconciliation GREEN · frontend UI-spec gates 154/154 GREEN · yarn build clean · playwright smokes 3/3 GREEN · MRR gates 7/7 GREEN · run_queries coherence OK · backend full sweep 1241/0.

═══════════════════════════════════════════════════════════════════

*End of register v1.2. Standing Rule v3 · on-disk canonical.*
