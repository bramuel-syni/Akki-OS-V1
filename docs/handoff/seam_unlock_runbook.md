# Seam-Unlock Runbook

**STATUS: OPERATIONAL REFERENCE. LIVE.**

Five closed seams exist in the RMS Intelligence System backend as of G6+A2 close. Four are owned externally (Owner, DPO, MEA); one is DPO-owned. Each seam is BUILT (code path complete, invariants passing in closed state) and GATED (returns closed-state decision until configured).

**Doctrine (per user, at G4 dispatch):** ship the deterministic/baseline path live; hold the learned/governed path as a built seam behind a closed gate. Never ship a learned path open on a permissive or invented value.

This runbook is the unlock-time reference. Each seam has: owner, current closed-state behavior, config keys, unlock procedure, behavioral change, verification test.

---

## Seam 1 — Targeta yield layer (Owner)

**Owner:** RMS product owner (Owner-signed decision required)
**Phase gate:** G4
**§-anchor:** Targeta Spec §12 (yield gate) + §17 (Owner-ownership)

**What's currently closed:**
`services/targeta/gate.py::evaluate_gate(thresholds: Optional[YieldThresholds], held_out: Sequence[dict]) → GateResult(admitted=False, reason="thresholds_not_configured")` when `thresholds is None` (`gate.py:60-62`). Targeta runs core-only via `services/targeta/core.py::eligible_and_rank`. The two-arm gate composition (`gate.py::compose_ordering`) uses core baseline; yield contribution is zero.

**Config keys** (verified against `services/targeta/yield_layer.py:20-24`):
- `YieldThresholds` dataclass, two fields:
  - `min_efficiency_gain: float` — Arm 1 (Helps) threshold. Median efficiency gain over the held-out set must clear this.
  - `coverage_alpha: float` — Arm 2 (Coverage) threshold.
- Additional runtime input at `evaluate_gate()`: `held_out: Sequence[dict]` — the held-out composition set, NOT part of `YieldThresholds`. Owner also decides this set's composition (`gate.py:64-67` refuses with `reason="no_held_out_set_or_functions"` when absent).

**Unlock procedure:**
1. Owner delivers threshold values + held-out composition set.
2. Config landing point: currently no config file — a `YieldThresholds(min_efficiency_gain=..., coverage_alpha=...)` dataclass is constructed at call time by the caller. Choose a config surface (env vars, JSON config, or governance registry) and load into a `YieldThresholds` at Service 1 or Service 2 boundary.
3. Pass to `evaluate_gate(thresholds=YieldThresholds(...), held_out=<sequence>)` from the composition pipeline.

**Behavioral change on unlock:**
- `evaluate_gate` returns `GateResult(admitted=True|False, reason="passed"|"below_efficiency"|"below_coverage", median_efficiency_gain=…)` based on held-out measurement.
- Two-arm gate composition (`compose_ordering`) begins reflecting yield contribution alongside core.
- `MiningPlan` ordering blends core-relevance with yield rank when Arm 2 admits.

**Verification test:**
- **Current invariant:** `test_targeta_invariants.py::test_yield_gate_closed_when_no_thresholds` — asserts `admitted=False, reason="thresholds_not_configured"` when `thresholds=None`.
- **On unlock:** re-scope the closed-seam invariant to explicitly the null-threshold case (parameterize; do NOT delete). Add new tests:
  - `test_yield_gate_admits_at_or_above_min_efficiency_gain` — passes a held-out set with median gain ≥ threshold; asserts `admitted=True`.
  - `test_yield_gate_refuses_below_min_efficiency_gain` — median gain below threshold; asserts `admitted=False, reason="below_efficiency"`.
  - `test_two_arm_composition_reflects_yield_when_admitted` — ordering under admitted yield differs from ordering under core-only.

---

## Seam 2 — Mtafiti V3 overlay (Owner)

**Owner:** RMS product owner (Owner-signed decision required)
**Phase gate:** G4
**§-anchor:** Mtafiti Spec §7 (V3 admission) + §18 (thresholds Owner-owned)

**What's currently closed:**
`services/mtafiti/v3_overlay.py::overlay_admitted(thresholds, v3_result) → False` when `thresholds is None` (`v3_overlay.py:11-15`). Registry composition at `services/mtafiti/registry.py::compose_record(v3_thresholds=None)` passes `v3_admitted=False` into `measure()` (`measure.py:5-9`), which zeroes the V3 signal fields (`attachment`, `corroboration`) — declaration_baseline runtime_mode dominates.

**Config keys** (verified against `services/mtafiti/v3_overlay.py:25-30`):
- `V3Thresholds` dataclass, three fields:
  - `fact_precision: float` — held-out fact-class precision floor.
  - `genre_accuracy: float` — held-out genre-classification accuracy floor.
  - `inter_annotator_floor: float` — inter-annotator agreement floor (κ or equivalent).
- Runtime input: `V3Result` (also a dataclass — the actual held-out measurement) with matching field names + `inter_annotator_kappa`.

**Unlock procedure:**
1. Owner scores a real held-out V3 evaluation set → produces `V3Result(fact_precision=..., genre_accuracy=..., inter_annotator_kappa=...)`.
2. Owner delivers thresholds → construct `V3Thresholds(fact_precision=..., genre_accuracy=..., inter_annotator_floor=...)`.
3. Threshold decision lands as config (choose surface as in Seam 1).
4. Pass to `mtafiti_registry.compose_record(unit, v3_thresholds=..., v3_result=..., ...)`.

**Behavioral change on unlock:**
- `overlay_admitted` returns True when `v3_result.fact_precision >= thresholds.fact_precision AND v3_result.genre_accuracy >= thresholds.genre_accuracy` (`v3_overlay.py:14-15`). *Note: the current code does NOT compare `inter_annotator_kappa` against `inter_annotator_floor`; if the third threshold is intended to gate, `v3_overlay.py::overlay_admitted` needs a small extension. Journal at unlock time.*
- `v3_admitted=True` flows into `measure()`; Registry entries gain non-zero `attachment` and `corroboration` signals.
- `runtime_mode` on `NormalizedUnit.defensibility` shifts from `declaration_baseline` to `v3_admitted` on admitted units.

**Verification test:**
- **Current invariant:** `test_mtafiti_invariants.py` grep-guards `overlay_admitted` and confirms `v3_admitted=False` when thresholds are None (Registry-level).
- **On unlock:** parameterize the closed-seam invariant; add:
  - `test_v3_overlay_admits_when_all_thresholds_met` — construct `V3Result` clearing all thresholds; assert `overlay_admitted → True`.
  - `test_v3_overlay_refuses_when_any_threshold_missed` — one metric below floor; assert `False`.
  - `test_registry_reflects_v3_signals_when_admitted` — composed `MtafitiRegistryRecord.score_vector.corroboration` is non-zero.

---

## Seam 3 — Northena Ledger retention (DPO)

**Owner:** Data Protection Officer (DPO-signed decision required)
**Phase gate:** G4
**§-anchor:** Northena Spec §7.4 (retention) + Product v2.1 §22 (governance record)

**What's currently closed:**
`services/northena/ledger.py:38-48` documents `retention_policy` as INDEFINITE default. **NO deletion code path exists in `services/northena/`.** Enforced by `tests/invariants/test_northena_ledger_retention.py::test_no_deletion_path_in_northena_services` which grep-guards forbidden tokens `("delete_", "purge_", "expire_")` across the northena services directory and asserts none exist.

**Config keys:**
DPO defines exact shape. Likely surface:
- Retention window: bounded duration (days or ISO-8601 duration) OR a bounded-interval schedule.
- Deletion mechanism choice: application-level sweep, scheduled job, or MongoDB TTL index on a datetime field of `northena_ledger_rows`.
- Deletion audit posture: DPO decides whether deletion events are themselves ledger-recorded (recommended: yes, via stamp_audit side-channel; preserves G6 doctrine).

**Unlock procedure:**
1. DPO decides retention window + deletion mechanism.
2. **`test_no_deletion_path_in_northena_services` WILL fail on unlock — that is the correct deployment ceremony.** Re-bless the invariant alongside the deletion implementation. Options:
   - Delete the invariant test entirely (retention now controls the discipline).
   - Re-scope it: `test_no_unauthorized_deletion_path` — assert only paths matching an `authorized_deletion_` prefix exist.
3. Implement deletion (application-level function OR Mongo TTL index migration).
4. Add authenticated audit trail for every deletion event.

**Behavioral change on unlock:**
- `LedgerRow` history becomes bounded rather than indefinite.
- Rows older than the retention window get deleted according to policy.
- Deletion events land as `stamp_audit`-decorated ledger rows (if DPO chose recorded-deletion posture).

**Verification test:**
- Current: `test_no_deletion_path_in_northena_services` (will fail on unlock — expected).
- On unlock: add
  - `test_deletion_respects_retention_window` — insert a row older than the window; run deletion sweep; assert row absent.
  - `test_deletion_preserves_within_window_rows` — insert a row inside the window; assert survives sweep.
  - `test_deletion_is_ledger_recorded` — every deletion emits a companion `LedgerRow` with `stamp_audit.deletion_event=True` (or DPO-chosen equivalent).

---

## Seam 4 — MEA source-standing table (MEA)

**Owner:** Media Editorial Authority (MEA — or equivalent authority)
**Phase gate:** G4
**§-anchor:** Mtafiti Spec §7 (source-standing input) + Product v2.1 §16 (editorial authority)

**What's currently closed:**
`services/mtafiti/source_standing.py` contains a synthetic placeholder table (`source_standing.py:44-63`) covering the on-disk fixture's `feed_ids`. **Every entry** has `synthetic_placeholder=True, editorial_authority=False` (`L60-61`). Enforced by `tests/invariants/test_mtafiti_invariants.py::test_source_standing_placeholder_flags` (`L248-263`) which iterates the table and asserts both flags per entry.

**Config keys:**
MEA-owned editorial table with the shape defined by `services/mtafiti/source_standing.py::SourceStandingEntry` (`L20-31`):
- `feed_id: str` — feed identifier (fixture-locked at G4; real feed_ids on unlock).
- `standing: str` — the editorial standing classification (matches the enum values already present in the placeholder).
- `synthetic_placeholder: bool` — MUST be `False` in the real table.
- `editorial_authority: bool` — MUST be `True` in the real table.
- Plus any additional editorial-metadata fields MEA decides to extend the shape with (extension is safe: `SourceStandingEntry` is not one of the 13 frozen contracts).

**Unlock procedure:**
1. MEA lands real editorial-authority-signed table.
2. Drop-in as config-swap for the placeholder at `services/mtafiti/source_standing.py`. The synthetic placeholder is REPLACED, not merged.
3. **`test_source_standing_placeholder_flags` WILL fail loudly on drop-in — that is the correct deployment ceremony.** It forces the deployment operator to update the invariant alongside the real table.

**Behavioral change on unlock:**
- Real editorial-standing declarations flow into Mtafiti per-feed governance.
- `MtafitiRegistryRecord` composition begins reflecting MEA-authority-scored standings rather than synthetic defaults.
- The G4 fixture-locked `feed_ids` set may or may not survive the drop-in; unrecognized `feed_ids` at composition time need a decided fallback (probably: refuse with `no_source_standing_for_feed` — extend at unlock time).

**Verification test:**
- Current: `test_source_standing_placeholder_flags` (will fail on unlock — expected).
- On unlock: add
  - `test_source_standing_editorial_authority_flags` — every entry has `synthetic_placeholder=False, editorial_authority=True` (inverse invariant).
  - `test_source_standing_covers_current_feed_universe` — every `feed_id` referenced by any live fixture or admitted run has a corresponding entry (no silent gaps).
  - `test_source_standing_table_signed` — table load path checks a signed manifest or hash-match against a MEA-signed digest (if MEA chose that posture).

---

## Seam 5 — G6 Cumulative-Disclosure Arm (DPO)

**Owner:** Data Protection Officer (DPO-signed decision required)
**Phase gate:** G6
**§-anchor:** Product v2.1 §21.2 (k-anonymity / l-diversity / DP-noise primitives) + §29.1 ("Until V2 passes") + §32 (DPO-owned)

**What's currently closed:**
`services/v2_gate/cumulative.py::cumulative_arm_admitted() → False` when any of the three env vars is unset or unparseable (`cumulative.py:27-50`). V2 single-packet refusal is live (`services/v2_gate/refusal.py`); cumulative-disclosure arm across repeated file-outs is dark.

**Config keys** (verbatim from `services/v2_gate/cumulative.py:40-42`):
- `RMS_G6_K_ANONYMITY_THRESHOLD` — integer, minimum group size (k in k-anonymity, §21.2).
- `RMS_G6_L_DIVERSITY_THRESHOLD` — integer, minimum distinct-value count within a group (l in l-diversity, §21.2).
- `RMS_G6_DP_EPSILON_BUDGET` — float, cumulative DP epsilon budget (§21.2).

All three must parse and cross zero-value guards for `cumulative_arm_admitted()` to return True.

**Unlock procedure:**
1. DPO decides threshold values.
2. Set env vars at container/deployment layer:
   ```bash
   export RMS_G6_K_ANONYMITY_THRESHOLD=5
   export RMS_G6_L_DIVERSITY_THRESHOLD=3
   export RMS_G6_DP_EPSILON_BUDGET=1.0
   ```
3. Restart backend (env is read at request time per `cumulative.py:36-50`; no restart strictly required, but recommended for cache coherence).
4. `cumulative_arm_admitted()` returns True; the load-bearing arm becomes live.

**Behavioral change on unlock:**
- V2 refusal envelope gains a new reason code path: `cumulative_disclosure_risk` (defined at G6 for this exact unlock).
- Individually-clean egresses that re-combine to reconstruct identities get refused when the k-anonymity or l-diversity threshold is crossed, OR when the DP epsilon budget is exhausted.
- The V2 tracking store begins persisting egress fingerprints across sessions (implementation lives behind `cumulative_arm_admitted()` guard at `cumulative.py:73`).

**Verification test:**
- Current: `test_v2_gate_refusal_cumulative.py` (`L105-137` region) asserts `cumulative_arm_admitted() is False` when env vars unset; also parametrizes-off env at test time to guarantee closed-seam.
- Test file already includes an unlock-simulation test at `L144+` that monkey-patches all three env vars and asserts `cumulative_arm_admitted() is True` — this is the LOAD-BEARING seam test that flips on unlock (already green).
- On real unlock: no new test file needed; the LOAD-BEARING test at `L144+` becomes an end-to-end guarantee. Optionally add:
  - `test_cumulative_arm_refuses_at_k_threshold` — construct a synthetic egress-history that crosses `k` at the current threshold; assert refusal.
  - `test_cumulative_arm_epsilon_budget_exhaustion_refuses` — repeated queries deplete epsilon budget; assert next query refuses.

---

## Cross-seam invariant

**No two seams share unlock timing.** Each is independently owner-owned and independently unlockable. Unlock ordering is not prescribed by architecture — order is a governance/rollout decision. Practical dependency observations:

- Seam 4 (MEA source-standing) should land before Seam 2 (Mtafiti V3 overlay) — the V3 overlay's `attachment` and `corroboration` signals meaningfully use the standing table.
- Seam 1 (Targeta yield) and Seam 3 (Northena retention) are independent of the others and independent of each other.
- Seam 5 (V2 cumulative) is independent; can unlock any time.

---

## Substrate manifest cross-reference

Filed canonical specs (7) under `/app/docs/mandates/`:
- `RMS_Solva_Specification.md`
- `RMS_Targeta_Specification.md` — §12 (yield gate), §17 (Owner-owned)
- `RMS_Mtafiti_Specification.md` — §7 (V3 admission), §18 (thresholds Owner-owned)
- `RMS_Northena_Specification.md` — §7.4 (retention)
- `RMS_Product_Engineering_Spec_v2.1.md` — §21.2, §22, §29.1, §32
- `RMS_Interface_Specification.md`
- `RMS_UX_Architecture_Specification.md`

SHA-256 fingerprints filed at `/app/docs/mandates/MANIFEST.md`. Substrate-drop gate CI-enforced via `backend/tests/invariants/test_substrate_drop_gate.py`.

For each seam unlock, cite the specific spec § anchor in the unlock PR / governance decision record so drift is auditable.

---

## Version

- **Filed:** 2026-07-02T02:45Z
- **Post-A2 amendment vintage** (Service1Refusal@v0 landed; X1 discipline fixed in the same wrap).
- **Applies to:** backend contract surface `v1.1-a2-e1_dev-20260702T021500Z` (see `/app/docs/handoff/backend_contract_surface_v1.md §8`).
- **Successor amendments** to this runbook: append below with dated headers; do not overwrite.
