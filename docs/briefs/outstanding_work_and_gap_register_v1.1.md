# Outstanding Work & Gap Register · v1.1 · 2026-07-12
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

## §11 · Amendment 1 · 2026-07-12 (Owner-ratified)
Predecessor: v1.0 at SHA cce17296a70b46ae6e1a1c64be1e9e3f18ca3f86a716758899037cf31f4d63d4. Ruling: docs/rulings/outstanding_register_v1_amendment_2026-07-12.md (SHA 06f51bf67d3c3b34024a814fd5d00bc6eb62c749181ac8945cf45f56f309ba27).

Add this that missed out;

Custody chain reconnection (G-1): deidentify → LLM → reidentify wired into the live outbound seam; fail-closed per its own spec; spaCy-unloadable → mechanical arm; client.py/purpose_validator.py reconnect only if the wiring routes through them, else shave with citation. Dispatched (IF-1).
Tenant-dictionary layer: the cousin's accounts/contexts/cycles harvest is inapplicable to RMS — stub to empty catalogue (regex + spaCy layers carry), recorded as the seat S2.onboard's estate vocabulary eventually feeds. Inside IF-1.
Legacy purpose catalogue — the one item the register didn't explicitly carry, adding it: ALLOWED_PURPOSES still lists the cousin's chat.* vocabulary (chat.session.summarise, chat.streaming.*), purposes RMS never serves. Fix: prune to RMS-live purposes. Rides IF-1 as a rider or lands with item 5, where the purpose catalogue gets properly defined — builder's call which vehicle, disclosed at close.
Model census correction (G-3 slice): spaCy NER enters Operating Values v1.1 as a rung-2 row (en_core_web_trf/sm, fail-closed de-id role). Rides the v1.1 revision.
The mandate document (G-12): SyniSense is the only governor without its own Mandate & Engineering Spec — I author it from the built reality + the bundle's distributed spec surface (the docstrings are already binding-grade: three-layer de-id stack, fail-closed semantics, perception-router doctrine, purpose catalogue, trust-receipt shape); you review verbatim; it lands as the fifth governed mandate; SyniSense re-anchors to it at the Registry maintenance turn. Drafts on your word — the only item waiting on you.
Dual perception paths (G-11): Shield perception_router (API-path, stub fallback) and 9.2a local workers both recorded in Registry v1 with distinct service traces — intentional venue split, not a defect; any retirement is a future evidence-based ruling. Rides the G-2 turn.

Anchors to existing register items:
- "Custody chain reconnection" → G-1 (§4) refinement + IF-1 (§2) scope confirmation.
- "Tenant-dictionary layer" → IF-1 (§2) rider.
- "Legacy purpose catalogue" → NEW G-13 rider on IF-1 (§2) or item 5 (§4 G-4/G-5/G-6 vehicle) — builder's-call disclosed at close per Owner.
- "Model census correction (G-3 slice)" → G-3 (§4) refinement carried into v1.1 revision.
- "The mandate document (G-12)" → NEW G-12 (§4) — SyniSense Mandate & Engineering Spec authoring, OPEN-OWNER (awaits Owner draft; item 5 register OD entry OD-7).
- "Dual perception paths (G-11)" → G-11 (§4) refinement, rides G-2 turn.
