# Owner Ruling · EAB Tier-1 Adoption Spec v1.0 · Amendment 1 · 2026-07-14

**Authority:** Owner-ratified. **Target:** docs/requirements/eab_tier1_adoption_spec_v1.md (SHA `6f3052ea22536643af62251f5dac166dd6c33fc0247acb66f1abd7fdfa5ab738`).
**Supersession:** additive; v1.0 body remains canonical; amendment lands at v1.1 under Part X verbatim.
**Companion:** docs/rulings/es1_scope_2026-07-14.md (Axis 4 dispositions).

## Amendment text (verbatim)

Dispatch — Adoption Spec v1.0 → v1.1 amendment. One doc-only commit, register-precedent pattern: v1.0 immutable; land docs/requirements/eab_tier1_adoption_spec_v1.1.md (v1.0 body + version delta + Part X below verbatim) + the ES-1 ruling record + amendment ruling record; update §17 pointer SHA. Reply with SHAs.
Part X — Tier-2/3 promotions (Owner-ruled 2026-07-14).
P1 · Dependency-set coverage as a Targeta output. Every extraction objective carries a declared dependency set (the batch/unit population its products require); Targeta planning reports coverage-to-objective % as a first-class, operator-visible output — plans answer "how evidence-complete is objective X," never merely "hours processed." Lands at the next Targeta-touching phase alongside the compute-cap input seat (§1.2). Service trace: S2.commission.
P2 · Merkle-root anchoring of batch receipts. Receipt volume at corpus scale is a named risk; receipt chains are anchored by periodic Merkle roots written as Northena ledger rows (cadence: per run-completion — DEFAULT, config-resident, revisited on measured receipt volume at corpus scale), so single-chain verification stays cheap and bulk storage stays flat. Rides EAB-2 as the receipts-extension rider. Service trace: S3.prove.
P3 · Rules name their telemetry. G-2 rider: every standing behavioral rule row in the Registry names the telemetry or gate that evidences it in operation, or is marked UNVERIFIED — and UNVERIFIED becomes a standing findings class (Q4) beside Q1–Q3. A rule whose practice cannot be evidenced is presumed skipped under pressure.
P4 · Baseline harness. The first real-material extraction run is an instrumented baseline by design: per-run utilization, items/hour, per-language WER/DER deltas emitted from run one (F3 discipline). E3/E4-class efficiency decisions (buffering, quantization) resolve automatically from this baseline per ES-4 — measured shortfall makes the build mandatory; no shortfall, no build. Harness spec rides de-risking rung-1; no efficiency machinery builds ahead of it.
Boundaries unchanged: §1.2 stands in full; P1–P4 add no scheduler, no premature optimization, no commercial premises.
R4 check: doc-only; no rows owed this commit (P1–P4 rows land with their carrying phases). Parity 31 untouched; triad not re-run. Sequencing unchanged: G-2 (now carrying P3's Q4 rider) → G-3 → EAB-1/2/3. Builder returns to IDLE after SHAs.

## Effect on sequencing

Sequencing unchanged from prior standing lane:
- G-2 (Registry maintenance) — now carries P3's Q4 rider (UNVERIFIED findings class beside Q1–Q3).
- G-3 (Operating Values v1.1 fold) — absorbs Part VII + F2 6th seam value.
- EAB-1/2/3 phases enter standard loop after G-3 close.
- P1 (Targeta coverage-to-objective %) rides next Targeta-touching phase.
- P2 (Merkle-root anchoring) rides EAB-2 as receipts-extension rider.
- P4 (Baseline harness) rides de-risking rung-1.

## R4 posture (no rows owed)

Doc-only commit; no Registry rows, no supplement, no tests. P1–P4 rows land with their carrying phases per Owner.
