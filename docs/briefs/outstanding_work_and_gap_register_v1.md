# Outstanding Work & Gap Register · v1.0 · 2026-07-12
**Authority:** Owner-ratified via ruling authority. **Purpose:** the single
authoritative record of all outstanding work and all discovered-gap fixes as of
this date. Survives context compaction on either side: where any future
in-context summary conflicts with this document, THIS DOCUMENT GOVERNS until an
Owner ruling supersedes it. **This register contains no schedule.** Sequencing
inside sanctioned lanes is the ruling authority's; owner decisions are marked
OWNER; nothing here is deadline-bearing. **This register adds no scope.** Every
item cites its origin. A work item not traceable to this register or a later
ruling is defect D7.

## §1 · Proven state (context, one paragraph)
BCR v1.5 mandate-complete (2026-07-10). Engine conformance audit (2026-07-12):
Solva 12/12, Targeta 11/11, Mtafiti 7/7, Northena 7/7 BUILT against on-disk
mandates; SyniSense 19 rows with one PARTIAL (custody chain, §2). Registry
Doctrine v1.0 in force; Registry populated (46 promises · 66+ functions);
machine-readable form + parser/validator live. Operating Values v1.0 on-disk.
Deviation audit baseline: 64,762 live LoC; 24-row deviation table on-disk.

## §2 · In-flight (dispatched, close owed)
**IF-1 · Shield custody reconnection + dead-code shave.** Ruling: RECONNECT the
de-identification chain (deidentify → LLM → reidentify, fail-closed per the
chain's own spec; spaCy-unloadable → mechanical arm per AF-E2 amended boundary;
tenant layer stubbed empty-catalogue as an S2.onboard-era seat). Shave the
clear-dead 2,359 LoC with four exemptions (spec-named modules incl. stamp.py ·
Standing-Rule-v3 records · /app/salvage · contract v0/v1 pairs). Entangled rows
HELD: deidentifier (reconnected, exits shave) · frontend /legacy/* (evidence of
any live consuming route returns at close; then OWNER decision). Riders:
targeta/__init__.py:9 stale comment; Part A/B tables land as canonicals.

## §3 · Loose threads (status owed in next builder reply)
**LT-1 · Standing Queries as CI:** SQ-E1 ruled γ + condition; execution ordered;
no close returned. Status: closed/in-progress/not-started, with evidence.
**LT-2 · sequencing_harness_stage_a.md** exists on-disk but was never
dispatched. Provenance: when created, by what instruction. If unsanctioned
pre-work: D7 finding, file held (not deleted) pending Owner disposition.

## §4 · Gap register — every discovered gap and its fix
| # | Gap | Evidence | Fix | Authority/status |
|---|---|---|---|---|
| G-1 | Shield custody chain unreachable from live LLM path | Conformance Part A.5; deviation rows (1,023 LoC chain) | Reconnection per IF-1 | RULED; in-flight |
| G-2 | Registry lags conformance reality (custody functions absent; modes.py SUPERSEDED not carried; conformance evidence uncited) | Conformance tables vs registry v0 + supplements | Registry maintenance turn: fold conformance results; execute Q2-05 individual reads; canonicalize S3.prove/S4.verify aliases; consolidate v0.1/v0.2 supplements → Registry v1 | SANCTIONED lane; dispatches after IF-1 close |
| G-3 | Operating Values v1.0 predates conformance findings | §1 model census omits spaCy NER (rung 2, live in Shield); diarization row states pyannote decision while build carries Silero(+seat); Solva weighting seat unrecorded | Revise to v1.1: add spaCy row (rung 2, en_core_web_trf/sm, fail-closed role); reconcile diarization row to built-state + decided-target; record Bayesian weighting as measurement-era seat under extraction_params@v0; carry §10-style amendment note | SANCTIONED; rides after G-2 so v1.1 cites Registry v1 |
| G-4 | S1 envelope-completeness (receipts machine-passable) has no direct cell | Registry Q3-01 (reclassified: platform-side, narrowed scope) | Candidate cell lands in next test-bearing phase (IF-1 close or G-2 turn); one cell, no new surface | SANCTIONED |
| G-5 | S1.scoped-key has only indirect coverage | Q3-05 | Direct cell, same vehicle as G-4 | SANCTIONED |
| G-6 | Northena audit-walk: view-side covered, walk-side uncovered | Q3-06 | Walk-side cell, same vehicle as G-4 | SANCTIONED |
| G-7 | SolvaTrace three-lens UX commitment (Spec §5): rendering surface unverified | Never checked; asserting either way would be fabrication | Verification question in next builder reply: surface exists / data-only. If data-only → OWNER decision on build timing | STATUS OWED, then OWNER if gap |
| G-8 | S2.onboard: journey step + full requirements (Op. Values §8) exist; no surface | Q3-02, ruled open-by-design | Build timing is an OWNER decision, raised 2026-07-12, unanswered. Register holds it OPEN-OWNER; no default implied | OWNER |
| G-9 | S4 buyer-commercial tier: requirements defined (Op. Values §7); surface salvaged | Q3-03 ruling | Restores when Owner rules a commercial posture | OWNER (standing ruling) |
| G-10 | Frontend /legacy/* (1,118 LoC) disposition | Deviation table, entangled | Evidence at IF-1 close → OWNER decision | PENDING EVIDENCE → OWNER |
| G-11 | Two perception paths (Shield perception_router w/ stub fallback · local 9.2a workers) | Bundle finding | NOT a defect: API-path vs in-perimeter path serve different venues. Fix = Registry v1 records both with distinct service traces; any retirement is a future OWNER ruling on evidence | RECORD in G-2 |

## §5 · Engine seats — designed-empty, NOT gaps (guard against re-litigation)
Solva Probability weighting: equal-weight default; method = measurement-era
value under extraction_params@v0. Targeta yield layer: spec-mandated to wait
for mining history; learning-method decision recorded for that era. Rung-3
owned text models: dependency-gated on estate corpus.

## §6 · Owner-decision register (raised; no deadlines; no defaults)
OD-1 S2.onboard build timing (G-8). OD-2 /legacy/* disposition (G-10, after
evidence). OD-3 Single-ingress navigation (after designer walkthrough;
walkthrough itself is owner-side, standing). OD-4 9.2b "proceed". OD-5
PH-R2/R3/R4 bindings (acceptance criteria pre-defined in Op. Values §9).
OD-6 Trace-lens build timing IF G-7 returns data-only.

## §7 · Proceed-gated register (environment; no build motion possible)
Rung-1 domain-transfer measurement → adapter decisions → BM-V (bar: Op. Values
§4) → BM-C operations (§5). Production model acquisition per §1/§2. PBK-2
deploy-attest at PH-R2/R4 window. All activate on OD-4/OD-5; none is builder
motion today.

## §8 · Undispatched doctrine surface (no schedule exists or is implied)
§8.1.b sequencing harness (pending LT-2 provenance) · §8.1.c worker
context-harnessing · §8.1.e mandates→specs→gates endpoint · MRR-E1 β
graduation (future governance amendment) · Instance Replication Playbook ·
Commercial Thesis (ruling-authority drafts, on Owner word).

## §9 · Binding disciplines carried (violations are D-10-class findings)
Canon before ruling (D-11) · no re-derivation · complete dispatches ·
decisions-not-menus to Owner · rules pay rent · verdicts never curated ·
no invented schedules (D7) · evidence-classed assertions (Solva discipline).

## §10 · What this document is not
Not a schedule. Not new scope. Not a secondary goal carrier: no item herein
authorizes work beyond its stated fix; product specs and function requirements
are altered only by Owner ruling, never by register drift. Supersession: only
by Owner ruling recorded in docs/rulings/.
