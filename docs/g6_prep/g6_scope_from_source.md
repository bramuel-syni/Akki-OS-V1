# G6 Scope Note — from source

**Filed:** 2026-07-02T00:30Z
**Sources:**
- `docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` (canonical parent — §21.2 Outer Gate; §29.1 V2; §30 Data Protection; §31 System Invariants; §32 Open Governance)
- `docs/mandates/northena.md` (§7.2 Ledger Row, §7.3 stamp_audit absorption, §12 Ledger, §14 stamp-audit side-channel obligation)
- `docs/mandates/RMS_Interface_Specification.md` (§5 auth-deferred; §11 consumer surface — outer-gate emit surfaces are consumer-adjacent)

**Substrate-drop gate:** PASS (`test_substrate_drop_gate.py::test_phase_gate_ready[G6]`).
**Baseline CI at scope time:** 301/301.

---

## 1.1 Outer-gate irreversibility topology (per Product v2.1)

**§-anchor:** Product v2.1 §21.2 (verbatim):

> "The outer gate governs file-out for external sale. It applies the **irreversibility transform (pseudonymisation with a purged mint, k-anonymity / l-diversity / generalisation, optional differential-privacy noise on numerics)**, validates rights past extract-for-RMS (gate V2), and guards cumulative disclosure across repeated file-outs so that successive releases cannot be recombined to reconstruct identities. **Only irreversibly transformed data crosses it.**"

**Verbatim §22.1 Gate row:** *"Tests whether a (sub-)objective is within the frozen artifact's scope — strict set-membership — and routes: warm-serve if already converged, fresh extraction if in scope and not converged, refuse (logged, not dropped) if out of scope."*

**V2 promise verbatim (§21.2 continued):**
> "**De-identified is not anonymised.** De-identified data — as passes the inner gate — is still personal data and remains in-tenancy. Only **irreversibly anonymised data** — as the outer gate produces — may egress for sale. The two gates enforce two different thresholds, and the distinction is a **data-protection requirement (Part VIII), not an implementation detail**."

**System-Invariant #8 (§31):** *"All Layer B perception runs in-tenancy; external reasoning is reached only through the inner gate after de-identification; **only irreversibly transformed data crosses the outer gate**."*

### What is "outer gate"?

Egress boundary for **file-out for external sale**. Distinct from the inner gate (which is per-call de-identification for external LLM reasoning, re-identified on return). The outer gate is a **write-out event**, not a per-call event.

### What identifiers must be one-way-transformed?

Per §21.2 "irreversibility transform (pseudonymisation with a purged mint, k-anonymity / l-diversity / generalisation)":

**Categories of identifier subject to the one-way transform** (derived from the substrate on-hand — frozen contracts + Registry semantics):
1. `unit.unit_id` (five_rings@v0 provenance) → pseudonymised via keyed HMAC.
2. `unit.provenance.source_ref` (feed_id / locator) → pseudonymised; k-anonymised across the egress batch.
3. `unit.provenance.speaker_or_author` → pseudonymised.
4. `unit.provenance.context` (feed_id, structural_signature, author_labels) → generalised (feed_id categories collapsed).
5. Solva `SolvaTrace.load_bearing_unit_ids` → pseudonymised (matching unit_id pseudonyms consistently within the batch).
6. `LedgerRow.run_id` and `LedgerRow.trace_id` → pseudonymised; the ledger's run/trace identity does not egress in raw form.
7. Numerics (Signal-ring dimensions, Solva probability scores) → optional differential-privacy noise (per-numeric epsilon per DPO config); v0: **no noise** (config unset — closed-seam behavior).

### Acceptable transform primitive per spec

Product v2.1 §21.2 specifies **"pseudonymisation with a purged mint"** as the primary primitive. This maps to a **keyed cryptographic pseudonymisation** function where:
- The key ("the mint") is generated once per mint-window.
- The key is **destroyed at end of window** (the "purge" — this is what makes the transform irreversible: without the key, no inverse exists in polynomial time).
- Between generation and purge, the mint is used to pseudonymise identifiers consistently (same identifier → same pseudonym within window).

Concretely: **HMAC-SHA256(key, plaintext_identifier) → hex**. Cryptographic irreversibility hinges on HMAC's PRF property + destruction of the key at purge.

### V2 promise verbatim §-anchor

Product v2.1 §21.2 (already cited): **"De-identified is not anonymised … Only irreversibly anonymised data — as the outer gate produces — may egress for sale … the distinction is a data-protection requirement (Part VIII), not an implementation detail."**

This is **the acceptance bar for Gate Condition 1**: the transform is irreversibility, not de-identification. Reversibility would collapse V2's promise into a de-identification promise, which spec explicitly refuses. Gate Condition 1's test must prove non-reconstructibility from the egress artifact alone.

---

## 1.2 V2 gate semantics

**§-anchor:** Product v2.1 §29.1 (verbatim):
> "V2 gates the outer-gate file-out. It **confirms rights past extract-for-RMS, resolves the substrate/rights contract, verifies a sample file-out cryptographically, and demonstrates the cumulative-disclosure guard refusing a reconstruction attempt**. Until V2 passes, delivery is inner-gate-only — live intelligence in-tenancy — which is a complete service on its own."

### Single-packet arm (LIVE at v0)

V2 refuses on any of four grounds derived from §29.1:
1. **`lawful_basis_absent`** — no `lawful_basis_ref` accompanies the file-out request (§30 purpose limitation).
2. **`substrate_rights_expired`** — the substrate/rights contract for the units being egressed has expired or is not resolvable (§29.1 rights past extract-for-RMS).
3. **`sample_file_out_crypto_verify_failed`** — the cryptographic verify of a sample egress failed (§29.1 "verifies a sample file-out cryptographically").
4. **`cumulative_disclosure_risk`** — the cumulative-disclosure guard refuses (see §1.2 cumulative arm below).

Refusal contract: **`V2RefusalEnvelope@v0`** (new frozen contract at G6). Fields (derived from §29.1 + §30):
- `reason_code: Literal[…4 codes above…]`
- `refused_at: str` (ISO-8601 UTC)
- `run_id`, `trace_id`, `artifact_ref` (correlation)
- `lawful_basis_ref: Optional[str]` (what was checked)
- `substrate_contract_ref: Optional[str]` (what was resolved against)
- `detail: str` (deterministic, no PII).

**Refusal invariant (§29.1 + §30 "purpose limitation"):** structured refusal envelope; NO partial egress ever. Any V2 refusal halts the egress with zero content bytes emitted.

### Cumulative-disclosure arm — SHAPE DECISION

**§-anchor:** Product v2.1 §29.1 (verbatim):
> "and demonstrates the cumulative-disclosure guard refusing a reconstruction attempt. **Until V2 passes, delivery is inner-gate-only** — live intelligence in-tenancy — which is a complete service on its own."

**Shape decision: SHAPE B — built-closed seam at G6 v0.**

**Rationale (spec-anchored, not agent-invented):**
1. §29.1 declares V2 itself is a FUTURE gate ("Until V2 passes, delivery is inner-gate-only"). At G6 v0, V2 is not the live delivery path — inner-gate is. So V2's cumulative arm being closed-seam-at-v0 is spec-consistent.
2. §32 Open Governance table shows three DPO/Owner-pending config unlocks (Ledger retention, Targeta yield, Mtafiti V3). The cumulative-disclosure arm's threshold parameters (k in k-anonymity, l in l-diversity, epsilon in differential-privacy) are analogous **DPO-owned config decisions**, not agent-selectable. Building the arm's code path + closing the gate until DPO thresholds land matches the closed-seam pattern used at G4 for Mtafiti V3 + Targeta yield.
3. §21.2 cites "k-anonymity / l-diversity / generalisation" as the primitives — these require k, l, and generalisation-hierarchy parameters that are policy decisions. No numeric threshold is spec-frozen.

**Shape B implementation:**
- `services/v2_gate/cumulative.py` — full arm code path built:
  - `CumulativeDisclosureLedger@v0` contract (tracking store for prior-egress fingerprints — a new frozen contract).
  - `cumulative_arm_admitted() -> bool` returns **False unconditionally** at v0 (thresholds not configured).
  - `evaluate(egress_artifact, prior_ledger) -> Optional[V2RefusalEnvelope]` — evaluator function; short-circuits to `None` when `cumulative_arm_admitted() is False`.
- Invariant `test_v2_gate_refusal_cumulative.py` asserts closed-seam state (same shape as Mtafiti V3 overlay + Targeta yield closed seams).
- Declared in `system_state.py::g6_components` as `cumulative_arm_status: "built_closed_seam"` with `config_unlock_path: "DPO thresholds — k / l / generalisation_hierarchy / dp_epsilon"`.

---

## 1.3 Ledger absorption path — CONTRACT-MUTATION HAZARD CHECK

**§-anchor:** Northena §14 ("Stamp-audit → Ledger: Absorbs StampAudit by unit_id / trace_id") + §7.3 (permissive stamp_audit shape) + §12 ("It absorbs the defensibility stamp-audit entries by unit_id and trace_id").

**Current `northena_ledger_row@v0` shape (from `contracts/northena_ledger.py`):**
- `stage: Literal["admit", "gate", "converge"]`
- `decision: Literal["admitted", "refused", "warm", "fresh", "terminate_success", "terminate_budget", "continue"]`
- `stamp_audit: Optional[Dict]` — permissive Dict.
- `reason: str` — deterministic reason string, free-form.

**Mapping outer-gate + V2 events onto existing row shape:**

Product v2.1 §29.1 verbatim: "V2 **gates** the outer-gate file-out." → V2 IS a gate. So:
- **V2 refusal** → `stage="gate", decision="refused"`, `reason="v2_refused:<reason_code>"`, `stamp_audit={"v2_refusal": V2RefusalEnvelope.model_dump()}`.
- **Outer-gate transform (irreversibility receipt)** → the outer gate emits fresh anonymised data → `stage="gate", decision="fresh"`, `reason="outer_gate_transform_applied:<transform_version>"`, `stamp_audit={"outer_gate_receipt": OuterGateReceipt.model_dump()}`.

**Contract-mutation check:**
- No new `stage` literal needed (both events map to `gate`).
- No new `decision` literal needed (both events use `refused` or `fresh`).
- No new field on `northena_ledger_row@v0` (payload lives in permissive `stamp_audit` Dict).
- `reason` field is free-form `str` — no enum change.
- Snapshot `northena_ledger_row.contract_snapshot.json` remains byte-identical.

**HAZARD-STOP (a) NOT raised.** All outer-gate + V2 events absorb cleanly into stamp_audit side-channel. No contract mutation. This is the point of Northena §14's "CONFIRM against the stamp-audit side-channel" obligation — the side-channel is the extension point.

**Invariant test obligation (Step 4):** `test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit.py` MUST assert `northena_ledger_row.contract_snapshot.json` is byte-identical after G6 close.

---

## 1.4 New frozen contracts implied

Three new frozen contracts at G6:

1. **`OuterGateReceipt@v0`** — `contracts/outer_gate_receipt.py`. Irreversibility receipt.
   - Fields (spec-derived from §21.2):
     - `transform_version: Literal["hmac-sha256-v1"]`
     - `key_fingerprint: str` (SHA-256 of the mint key material — **never the key itself**)
     - `applied_transformations: List[str]` (e.g., `["pseudonymise:unit_id", "pseudonymise:source_ref", "generalise:feed_id", "pseudonymise:speaker_or_author"]`)
     - `input_identifier_categories: List[str]` (categories transformed, not values)
     - `mint_window_id: str` (uuid of the mint window; the window's key will be purged at end)
     - `applied_at: str` (ISO-8601 UTC)
     - `run_id: str`, `trace_id: str` (correlation)
     - `k_anonymity_bucket_size: Optional[int]` (if generalisation applied)
     - `differential_privacy_epsilon: Optional[float]` (v0: None — closed-seam)

2. **`V2RefusalEnvelope@v0`** — `contracts/v2_refusal.py`. Structured V2 refusal.
   - Fields (spec-derived from §29.1 + §30):
     - `reason_code: Literal["lawful_basis_absent", "substrate_rights_expired", "sample_file_out_crypto_verify_failed", "cumulative_disclosure_risk"]`
     - `refused_at: str`
     - `run_id: str`, `trace_id: str`, `artifact_ref: LedgerArtifactRef`
     - `lawful_basis_ref: Optional[str]`
     - `substrate_contract_ref: Optional[str]`
     - `detail: str` (deterministic, no PII)

3. **`CumulativeDisclosureLedger@v0`** — `contracts/cumulative_disclosure.py`. Tracking-state contract for the closed-seam arm.
   - Fields:
     - `mint_window_id: str`
     - `egress_fingerprints: List[str]` (SHA-256 fingerprints of prior egress artifacts; empty at v0 since arm is closed)
     - `k_threshold: Optional[int]` (None at v0 — closed-seam)
     - `l_threshold: Optional[int]` (None at v0)
     - `epsilon_budget: Optional[float]` (None at v0)
     - `arm_admitted: bool` (False at v0 — closed-seam mirror of `cumulative_arm_admitted()`)

**All three are ADDITIONS.** None mutates the 10 existing frozen contracts (six pre-G4 + `MtafitiRegistryRecord@v0` + `MiningPlan@v0` + `TraceLensEnvelope@v0` + `LiftManifestEnvelope@v0`). HAZARD-STOP (a) NOT raised.

**Total frozen contracts after G6: 10 → 13.**

---

## 1.5 Cross-spec §-anchor grid

| G6 module | §-anchor | Verdict target |
|---|---|---|
| `services/outer_gate/transform.py` | Product v2.1 §21.2 "pseudonymisation with a purged mint" | MATCH |
| `services/outer_gate/mint.py` | Product v2.1 §21.2 "purged mint" | MATCH |
| `services/outer_gate/receipt.py` | Product v2.1 §21.2 + §22.1 "each Gate decision and reason" | MATCH |
| `services/v2_gate/refusal.py` | Product v2.1 §29.1 + §30 purpose limitation | MATCH |
| `services/v2_gate/cumulative.py` | Product v2.1 §29.1 "cumulative-disclosure guard" + §32 DPO/Owner-pending config pattern | MATCH (closed-seam, Shape B per §29.1 "Until V2 passes") |
| `services/v2_gate/gate.py` | Product v2.1 §29.1 (V2 as composition of 4 checks) | MATCH |
| `contracts/outer_gate_receipt.py` | Product v2.1 §21.2 + §22.1 record obligation | MATCH |
| `contracts/v2_refusal.py` | Product v2.1 §29.1 + §22.1 "every refusal" | MATCH |
| `contracts/cumulative_disclosure.py` | Product v2.1 §29.1 + §32 config-unlock pattern | MATCH (closed-seam) |
| `services/northena/converge.py::absorb_outer_gate_receipt` | Northena §14 stamp-audit side-channel + Product v2.1 §22.1 Ledger absorption | MATCH |
| `services/northena/converge.py::absorb_v2_refusal` | Northena §14 + Product v2.1 §22.1 "every refusal" | MATCH |
| `test_outer_gate_irreversibility.py` | Product v2.1 §21.2 irreversibility + Sys-Invariant #8 | MATCH (Gate Condition 1) |
| `test_v2_gate_refusal_cumulative.py` | Product v2.1 §29.1 V2 obligation + §32 closed-seam pattern | MATCH (Gate Condition 2, Shape B) |
| `test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit.py` | Northena §14 + `northena_ledger_row@v0` frozen shape | MATCH (contract-shape invariant) |

**Zero MATERIAL_GAP required at Step 5 audit. Zero contract-mutation demands surfaced by this scope note. HAZARD-STOPs raised at scope-note stage: NONE.**
