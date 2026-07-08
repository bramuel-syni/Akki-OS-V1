# Artifact Store · Stage A Proposal (BCR §3.2)

**Dispatch:** Owner post-8-EXT-ratification message, 2026-07-08.
**Sequence position:** BCR §5.1 line 314 — *"3. Artifact store (3.2) — the only gap that is purely a decision plus a small phase; unblocks V3's done-condition and is a dependency of 3.7."*
**Governance model:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md` (adopted 2026-07-08). Escalations arrive pre-tiered.
**Standing Rule v3:** this proposal is the on-disk canonical. Reply body carries file SHA + line-range map + tier tags only.

---

## §1. Cell-density assumption (rates carried forward from 8-EXT + 9.1/9.3)

Empirical amortised rates (matrix-enumerated; no fresh cost class expected at Artifact Store):

| Cell class | Rate | Basis |
|---|---:|---|
| Backend Pytest (shared-helper amortised) | 12 LoC/cell | Amendment I; observed at 9.1/9.3/8-EXT close. |
| Backend endpoint impl (amortised 3-share) | 40 LoC/endpoint | 8-EXT actual: 3 grant endpoints via `require_own_scope_or_deny` at ~40 LoC/endpoint. |
| Backend service module (standalone) | 100 LoC/module | 8-EXT actual: `engineer_scope.py` 84 · `engineer_invites.py` 170 (2-share). |
| Frozen contract Pydantic class + snapshot | 80 LoC (class 60 + snapshot 20) | Historical: `OuterGateReceipt@v0` at G6. |
| Frontend Jest (structural, standalone) | 16 LoC/cell fallback | 8-EXT observed −50 delta on `renderHook` micro-cells; new AS surface has no UI, so this row is DNA. |
| Playwright chromium (data-testid amortised) | 9 LoC/cell | Codified at 9.1/9.3; no Playwright cells expected at AS Stage A (no UI surface). |

**No new AS-specific cost class emerges** — the adapter port is a standalone module (rate row 3), the atomic-write protocol is procedural (folded into backend service LoC), the orphan-scan is another module (row 3), and download/head endpoints ride row 2.

**[Tier 2] Rate stability note:** the +145 LoC docstring overshoot on backend Pytest observed at 8-EXT (§5 composition finding) is one-shot to that phase; no rate revision. Symmetric miss-disclosure honored at close.

---

## §2. Matrix enumeration

### §2.1 Backend adapter surface — the three-operation seam

**Authority-source (BCR v1.4 §3.2 lines 122–126):**

```
StorageAdapter (single seam; provider = config, call sites never change)
  put_once(key: str, data: bytes, content_type: str) -> {sha256, size}
       MUST fail if key exists (write-once)
  get(key: str) -> bytes
  head(key: str) -> {exists: bool, sha256: str, size: int}
```

**Landing shape:**

- `backend/services/artifact_store/adapter.py` NEW — abstract `StorageAdapterProtocol` (Python `Protocol`) + concrete dev-tier implementation.
- `backend/services/artifact_store/__init__.py` NEW — barrel export.

**LoC estimate:** protocol + concrete (dev-tier) = **~140 LoC** (module 1 × 100 LoC amortised + 40 LoC protocol overhead).

**Reuse mandate (Read-First):** search backend for prior `store`/`adapter` prototypes before writing. If none exist, this is greenfield.

### §2.2 Key format

**Authority-source (BCR v1.4 §3.2 line 128):**

> Key format:  artifacts/{trace_id}/{artifact_id}.{ext}

**Landing:** enforced as an f-string builder in `services/artifact_store/keys.py` (or inline in adapter). `{ext}` extension is Tier-3 defaulted (see §5 Tier-3 defaults).

**LoC estimate:** ~15 LoC helper + 2 keys/cell attestation ~20 LoC. Folded into §2.1 rate.

### §2.3 Six-step atomic write protocol

**Authority-source (BCR v1.4 §3.2 lines 130–133):**

```
Atomic write protocol (no partial artifact is ever visible):
  1 put to {key}.tmp   2 verify sha256   3 move/copy to final key
  4 head-verify        5 write receipt   6 emit ledger row
  failure at any step before 5 => tmp garbage-collected, nothing visible
```

**Landing:** procedural coordinator function `atomic_put_with_receipt(...)` at `services/artifact_store/atomic_write.py` NEW. Six ordered steps with try/finally garbage-collection on tmp key. Failure between steps 1–4 → tmp GC'd; failure at step 5 or 6 is a **client-promise violation** (see §5 AS-E1 [Tier 1]) — the ordering here is Owner-rulable.

**LoC estimate:** ~120 LoC coordinator + 10 LoC GC. Tier-1 (provenance integrity).

### §2.4 SHA-on-receipt via additive version path — receipt.v1

**Authority-source (BCR v1.4 §3.2 line 134):**

> Receipt binding: the artifact SHA-256 and key land on the outer-gate receipt via the additive version path (receipt v1: artifact_sha256, artifact_key) [STAKED — the buyer must be able to verify independently, which argues on-receipt over sidecar; D4b argued at dispatch].

**Landing shape (staked):**

- `backend/contracts/outer_gate_receipt_v1.py` NEW — `OuterGateReceiptV1(BaseModel)` extends v0 by ADDITION of two Optional[str] fields: `artifact_sha256`, `artifact_key`. Frozen. Parity **28 → 29** contracts if v1 lands as a frozen contract.
- `backend/tests/invariants/outer_gate_receipt_v1.contract_snapshot.json` NEW.
- `contracts/outer_gate_receipt.py` (v0) preserved BYTE-IDENTICAL. Snapshot v0 unchanged.
- Call sites at outer-gate emission update to import v1 and populate the two new fields.

**Parity 28 adjacency** — this is the Tier-1 escalation AS-E1.

**LoC estimate:** v1 contract 60 + snapshot 20 + call-site rewiring 30 = **~110 LoC**.

### §2.5 Orphan-scan mechanism

**Authority-source (BCR v1.4 §3.2 lines 115, 118):**

> AS-B2  No artifact exists without its receipt and ledger row; an orphan-artifact scan MUST return zero.
> ... AS-G3 test_orphan_artifact_scan_zero ...

**Landing shape:**

- `backend/services/artifact_store/orphan_scan.py` NEW — walk of the `artifacts/**` key-space, correlated against the ledger (`stamp_audit.artifact_ref`? or a new `artifact_key` lookup on the ledger row's outer-gate receipt sidecar). Returns list of orphan keys (empty in the well-formed system).
- Scan periodicity is Tier-3 defaulted (see §5 Tier-3 defaults) — startup-time OR admin-invoked.
- Deletion posture on orphan is Tier-1 (see §5 AS-E3): quarantine-and-report vs delete-attest — Owner ruling required.

**LoC estimate:** ~80 LoC (module rate). Tier-1 for orphan disposition; Tier-3 for periodicity.

### §2.6 Download 403 taxonomy on `get`

**Authority-source (BCR v1.4 §3.2 line 116):**

> AS-B3  Download is authenticated by the buyer's key scope; a wrong-key request returns 403 access-control class ({reason, detail}, never outcome=refused).

**Landing shape:**

- `backend/routers/artifact_store.py` NEW — `GET /api/artifacts/{trace_id}/{artifact_id}` endpoint. Wrong-key → HTTP 403 with `{"reason": "auth_scope_insufficient", "detail": "..."}`, NEVER `{"outcome": "refused", ...}`.
- **4-code registry reuse (P9-E3/P8E-E4 α pre-carry):** `auth_scope_insufficient` is the code. Zero new refusal codes. Attested by grep-negative gate.
- HEAD endpoint `HEAD /api/artifacts/{trace_id}/{artifact_id}` — same 403 posture, no body.

**LoC estimate:** ~100 LoC (endpoint amortised rate × ~2.5). Tier-1 for the 403-class posture (security boundary; honesty grammar); Tier-3 for the endpoint path literal.

### §2.7 Retention held-class

**Authority-source (BCR v1.4 §3.2 line 117):**

> AS-H1  Behavioral: artifacts are a retention held-class (delivered_artifact); deletion exists only via the Seam 3 authorized path (3.5).

**Landing shape:** artifact-store surface enforces "no direct DELETE endpoint on the adapter." Deletion routes via `Seam 3` (retention config + authorized_deletion path, both already LIVE). Tier-1 discipline; attested by grep-negative on any DELETE handler in `routers/artifact_store.py`.

**LoC estimate:** ~5 LoC attest cell (no new code — this is a negative gate on the router).

### §2.8 Dev-tier backing choice

**Authority-source (BCR v1.4 §3.2 line 113):**

> AS-I1  Integration: one storage adapter module presenting an S3-class interface (put-once, get, head). The store choice is config [OWNER: object-store choice]; swapping providers touches the adapter's config, never call sites.

**Landing:** dev-tier backing is Tier-3 default. See §5 Tier-3 defaults. Owner-side production choice is `AS-OWN-1` at §4.3.

### §2.9 Named gate roster (AS-G1..AS-G4 + Tier-1 attestations)

| Gate | Authority-source line | Landing test | Cell count |
|---|---|---|---:|
| **AS-G1** `test_receipt_sha_equals_stored_object` | BCR §3.2:118 | `test_artifact_store.py::test_as_g1_receipt_sha_equals_stored_object` | 1 |
| **AS-G2** `test_refetch_byte_identity` | BCR §3.2:118 | `test_artifact_store.py::test_as_g2_refetch_byte_identity` | 1 |
| **AS-G3** `test_orphan_artifact_scan_zero` | BCR §3.2:118 | `test_artifact_store.py::test_as_g3_orphan_artifact_scan_zero` | 1 |
| **AS-G4** `test_download_403_is_access_control_class` | BCR §3.2:118 | `test_artifact_store.py::test_as_g4_download_403_is_access_control_class` | 1 |
| Tier-1 attest · atomic-write step-5-halt | §2.3 | `test_atomic_write_fails_atomically_before_receipt` | 1 |
| Tier-1 attest · receipt v0 byte-identical | §2.4 | `test_outer_gate_receipt_v0_snapshot_byte_identical_at_artifact_store_close` | 1 |
| Tier-1 attest · parity delta (28→29) IF v1 lands frozen | §2.4 | `test_v1_g7_attestation_parity_at_artifact_store_close` | 1 |
| Tier-1 attest · put_once write-once | §2.1 | `test_put_once_rejects_second_write_to_same_key` | 1 |
| Tier-1 attest · raw-never-egresses (authz-before-bytes) | §2.6 | `test_get_returns_403_before_content_bytes_computed` | 1 |
| Tier-1 attest · 4-code registry closure | §2.6 | `test_auth_refusal_registry_still_closed_at_four_codes` (re-run at AS close) | 1 |
| Tier-1 attest · retention held-class (no DELETE handler) | §2.7 | `test_no_delete_handler_in_artifact_store_router` (grep-negative) | 1 |
| Tier-1 attest · outer-gate emission populates receipt.v1 fields | §2.4 | `test_outer_gate_emission_populates_artifact_sha256_and_key` | 1 |

**Backend cell count total: 12.**

### §2.10 Frontend adjacency

**Zero frontend cells at AS Stage A.** The extractor has no "buyer Receive" surface — Sales Service (UI Spec v2.1 §12) is CUT from extractor scope; the Sales Service is not in current build. AS-U1 clause is call-site contract for a future Sales Service caller.

`[Tier 3 default]` (see §5): no frontend module lands; no Jest cell; no Playwright cell.

---

## §3. Band derivation

### §3.1 Point-estimate (matrix × rates)

| Bucket | LoC |
|---|---:|
| §2.1 adapter (protocol + dev-tier concrete) | 140 |
| §2.2 keys helper (folded into §2.1) | — |
| §2.3 atomic-write coordinator | 130 |
| §2.4 receipt.v1 contract + snapshot + call-site rewire | 110 |
| §2.5 orphan-scan module | 80 |
| §2.6 download + head endpoints (router) | 100 |
| §2.7 retention held-class (attest only) | 5 |
| §2.9 backend tests (12 cells × 12 LoC/cell shared-helper amortisation + fixtures 30) | 174 |
| Docs (close report + rulings record) | *(excluded from LoC per §4.1 baseline discipline)* |
| **Point-estimate total** | **~739 LoC** |

**Cell count total: 12 backend Pytest cells. Zero frontend Jest cells. Zero Playwright cells.**

### §3.2 Owner-anchored band

**Anchored band:** `[610, 870]` LoC (point-estimate ± ~18% shave/cushion).

**Rationale (Tier 2, disclosure-only):** the 18% shave/cushion mirrors the 8-EXT band width proportion (`[900, 1,180]` ≈ ±14%) and the 9.1/9.3 band width proportion (~±15%). Wider cushion at AS reflects the receipt.v1 parity-adjacency dependence: if AS-E1 [Tier 1] rules that v1 does NOT land as a frozen contract (falls back to sidecar), the 110 LoC in §2.4 drops to ~40 LoC, pulling the actual toward the bottom of the band. If v1 lands as designed, actual sits at 52-55% of top (matching 8-EXT convergence).

**§4.2 pre-authorized split thresholds:** unchanged from Amendment I / 8-EXT — **1,500 LoC OR 60 cells**. AS point-estimate (739 LoC / 12 cells) is 49% of LoC threshold and 20% of cell threshold. **Not expected to trigger.**

### §3.3 Symmetric miss-disclosure discipline

Per new governance §2.2 (Tier 2): a band miss is a line in the close report, not a halt. Symmetric disclosure of over/under stays. Applied at close.

---

## §4. Dispatch discipline

### §4.1 Baseline atomic first-commit

Single atomic commit bundling: adapter module + keys helper + atomic-write coordinator + receipt.v1 contract + snapshot + call-site rewire + orphan-scan + router + all tests + rulings record + close report. Same pattern as 8-EXT / 9.1+9.3.

### §4.2 Pre-authorized split thresholds

**Trigger:** ≥1,500 LoC **OR** ≥60 cells. Not expected to trigger (see §3.2). If it triggers autonomously during execution, split into two commits by natural boundary (put_once/coordinator as commit A; get+head+router+orphan-scan as commit B). Trigger and split disclosed at close.

### §4.3 Dispatch-independence and [OWNER] gates

**AS-OWN-1 — Object-store choice (production backing).** Owner: Owner. ETA: unknown. **Not gating this Stage A.** Not gating execution. Not gating Phase 9 Stage B. Adapter seam is dispatch-independent; production provider swaps as config when the fact arrives. Call sites never change (attested by the adapter Protocol interface).

Artifact Store Stage A is **fully dispatch-independent** on all other axes.

---

## §5. Escalations — PRE-TIERED per new governance

### §5.1 AS-E1 [Tier 1] · receipt.v1 parity-adjacency

**Class:** frozen wire contract (per Tiered Model §1.1 last bullet).
**Question:** does `receipt v1` (artifact_sha256 + artifact_key on the outer-gate receipt, per BCR §3.2:134 STAKED) land as a NEW frozen contract `OuterGateReceipt_v1` (parity 28 → 29), OR as sidecar fields on the existing v0 (v0 mutation — mutation of a frozen contract, prohibited unless Owner rules a version-bump equivalent), OR as a service-layer post-receipt attachment (adjunct dict on the ledger row's `stamp_audit`) — the sidecar-not-on-receipt path?

**Authority-source language (BCR §3.2:134 verbatim):**

> Receipt binding: the artifact SHA-256 and key land on the outer-gate receipt via the additive version path (receipt v1: artifact_sha256, artifact_key) [STAKED — the buyer must be able to verify independently, which argues on-receipt over sidecar; D4b argued at dispatch].

**Promise-protected (§4.3 promise-naming rule):** provenance/audit integrity — the buyer's ability to verify the artifact independently from the receipt is the surface here. A sidecar path preserves the promise if the sidecar is signature-bound; an on-receipt path preserves the promise directly.

**Options:**

- **α** — Land `OuterGateReceipt_v1` as a NEW frozen contract by ADDITION (v0 preserved byte-identical; parity 29 at Artifact Store close). `artifact_sha256` + `artifact_key` are two Optional[str] fields on v1 (populated by outer-gate emission at successful atomic-write step 5). V1-G7 assertion set BUMPS to 29. Snapshot bijection at 29.
- **β** — Land the two fields on `NorthenaLedgerRow_v1.stamp_audit` as a SIDECAR dict entry (`stamp_audit["artifact_binding"] = {"sha256": ..., "key": ...}`). No new frozen contract. Parity stays 28. Buyer verification path goes via ledger row (`GET /api/northena/trace/{trace_id}`) rather than the receipt.
- **γ** — Add the two fields directly to `OuterGateReceipt@v0` as Optional[str]. This is MUTATION of a frozen contract; prohibited unless Owner rules a v0-mutation equivalent (broke the "byte-identical" promise). **NOT recommended.**

**Recommended:** **α**. Rationale: (1) the [STAKED] language explicitly argues on-receipt over sidecar; (2) additive-by-new-contract mirrors the successful pattern from `data_class_registry.v2→v3` at 8-EXT (P8E-E7 α) — additive-only, prior byte-identical, new contract lands with its consumers; (3) parity 29 is the honest count when a new frozen contract lands, not a violation of the 28 promise.

**Escalation surface:** frozen contract + parity assertion set. Full-rigor Tier-1 treatment. Owner ruling required BEFORE execution.

### §5.2 AS-E2 [Tier 1] · atomic-write step-5 crash posture

**Class:** provenance/audit integrity (Tiered Model §1.1 first bullet).
**Question:** the six-step protocol says "*failure at any step BEFORE 5 => tmp garbage-collected, nothing visible*." Silent on failure at step 5 (receipt write) AFTER step 3 (move to final key). What is the correct disposition when receipt write fails but the object is at the final key — reverse-move to tmp (which then GC's), OR emit a compensating "orphan-attest" ledger row (documenting the artifact-without-receipt honestly), OR delete the object at final key + fail the call?

**Authority-source language (BCR §3.2:130–133 verbatim):**

```
Atomic write protocol (no partial artifact is ever visible):
  1 put to {key}.tmp   2 verify sha256   3 move/copy to final key
  4 head-verify        5 write receipt   6 emit ledger row
  failure at any step before 5 => tmp garbage-collected, nothing visible
```

**Also:** AS-B2 (BCR §3.2:115): *"No artifact exists without its receipt and ledger row; an orphan-artifact scan MUST return zero."*

**Promise-protected:** provenance/audit integrity — an artifact without a receipt is precisely the orphan state AS-B2 prohibits. The step-5 failure window is a client-promise-violation window if not disposed correctly.

**Options:**

- **α** — Reverse-move step-3 (i.e., step 3 uses copy-not-move, so the tmp survives; on step-5 failure, delete final-key object). Best atomicity but requires copy-semantics (cost).
- **β** — Delete-at-final-key on step-5 failure + retry from step 1 (no compensating row; the orphan window is closed by the deletion).
- **γ** — Copy-not-move at step 3 + retention of both tmp and final until step 6 completes (dual-copy; step-6 emits ledger row THEN GC's tmp).

**Recommended:** **γ** — copy-not-move at step 3, dual-copy retention until step 6 ledger-row emit succeeds, then GC tmp. This makes the six-step protocol fully atomic in the AS-B2 sense (no step-5-or-6 crash leaves an orphan at the final key).

**Escalation surface:** provenance boundary. Full-rigor Tier-1. Owner ruling required BEFORE execution.

### §5.3 AS-E3 [Tier 1] · orphan-scan disposition on detection

**Class:** provenance/audit integrity + honesty grammar.
**Question:** on orphan detection (an artifact key with no matching receipt+ledger row), does the scan (a) DELETE the orphan (delete-attest — writes a `orphan_artifact_deleted` ledger row via `stamp_audit.data_class` sidecar), (b) QUARANTINE the orphan to a `quarantine/` sub-key + emit a `orphan_artifact_quarantined` ledger row for later human review, or (c) REPORT-ONLY (return the list to caller; take no destructive action)?

**Authority-source language (BCR §3.2:115, 118 verbatim):**

> AS-B2  No artifact exists without its receipt and ledger row; an orphan-artifact scan MUST return zero.
> ... AS-G3 test_orphan_artifact_scan_zero ...

**Promise-protected:** provenance/audit integrity — an orphan is a defect state, but destructive disposition is a client-visible action that itself demands attestation (deletion is a Tier-1 surface via Seam 3).

**Options:**

- **α** — REPORT-ONLY. Scan is read-only; returns the orphan list; human/Owner disposes. Simplest; fully preserves audit integrity; matches AS-H1 "deletion exists only via the Seam 3 authorized path."
- **β** — QUARANTINE. Scan moves orphans to `quarantine/{key}` + emits `orphan_artifact_quarantined` ledger row (`data_class_registry.v3→v4` additive bump). Requires new data_class + Seam 3 non-quarantine-delete path.
- **γ** — DELETE-ATTEST. Scan deletes orphans + emits `orphan_artifact_deleted` ledger row. Violates AS-H1 (deletion only via Seam 3); NOT recommended.

**Recommended:** **α** — REPORT-ONLY. Rationale: honours AS-H1 verbatim; keeps scan mechanism-simple; disposition of a real orphan (if ever) is an Owner-facing decision, not an automated one.

**Escalation surface:** provenance + retention held-class boundary. Full-rigor Tier-1. Owner ruling required BEFORE execution.

### §5.4 AS-E4 [Tier 1] · raw-never-egresses on `get` — authz boundary location

**Class:** security boundary (Tiered Model §1.1 · "raw-never-egresses").
**Question:** does the `StorageAdapter.get(key)` method enforce authorization internally (mechanism-not-convention — the adapter accepts a `caller_scope` argument and denies before reading bytes), OR does the router-level endpoint enforce authz before calling `adapter.get(key)` (convention — the call site must check)?

**Authority-source language (BCR §3.2:116 verbatim):**

> AS-B3  Download is authenticated by the buyer's key scope; a wrong-key request returns 403 access-control class ({reason, detail}, never outcome=refused).

**Promise-protected:** security boundary — raw content bytes MUST NOT leave the adapter surface without authz having fired. Mechanism-not-convention is the "raw-never-egresses" promise (Tiered Model §1.1 second bullet).

**Options:**

- **α** — Adapter's `get(key)` accepts `caller_scope: Optional[Scope]` and enforces the buyer-key match INSIDE the adapter. Reading bytes happens ONLY after authz check. Mechanism-enforced. Adapter signature changes: `get(key, caller_scope=None)`.
- **β** — Adapter's `get(key)` is authz-agnostic; the router endpoint enforces authz before calling. Convention-enforced. Adapter signature stays clean at `get(key) -> bytes`.
- **γ** — Split: adapter has both `_get_raw(key)` (private, no authz) and `get(key, caller_scope)` (public, authz-first). Router uses public path only. Belt-and-suspenders.

**Recommended:** **α**. Rationale: "raw-never-egresses" is a mechanism-not-convention promise; the adapter is the boundary; authz MUST fire before bytes are returned. This mirrors the P8E-E2 α rationale (dedicated helper is the single source; not a parallel mechanism).

**Escalation surface:** security boundary. Full-rigor Tier-1. Owner ruling required BEFORE execution.

### §5.5 AS-E5 [Tier 2] · adapter surface split threshold (disclosure-only, no ruling required)

**Class:** cost/rework · split threshold (Tiered Model §2.1 third bullet).

**Statement (per new governance format):** if execution LoC exceeds 1,500 OR cell count exceeds 60, split the adapter surface: **commit A** lands `put_once` + atomic-write coordinator + receipt.v1 + orphan-scan (write-side); **commit B** lands `get` + `head` + router (read-side). Natural boundary; call-site rewiring can defer to commit B.

**Disclosure-only:** no Owner ruling required. Trigger status disclosed at close.

**Expected trigger:** NO (point-estimate 739 LoC / 12 cells — 49% / 20% of thresholds).

### §5.6 Tier-3 defaults (silent; disclosed at close, no escalation)

Per new governance §3.2 (Tier 3): builder defaults + one disclosure line per item. Format: `[Tier 3 default] {item} → {chosen default} — {one-line rationale}.`

Expected Tier-3 defaults at Artifact Store execution:

1. **`[Tier 3 default]` Dev-tier backing choice → local filesystem at `/tmp/rms_artifact_store/` (or `os.environ["RMS_ARTIFACT_STORE_ROOT"]` if set) — matches the pattern used elsewhere in the codebase (env-var-with-dev-default); trivial to swap when AS-OWN-1 lands.**
2. **`[Tier 3 default]` Extension whitelist for `{ext}` in key format → `{"json", "csv", "parquet", "bin"}`; unknown-ext raises `ValueError` at `put_once`. Rationale: extractor output forms per BCR §6 today produce these four extensions; whitelist is trivially extendable via config.**
3. **`[Tier 3 default]` Module structure → `backend/services/artifact_store/` (singular directory, plural noun) — matches `services/auth/` (singular noun, singular-topic module) and `services/compliance/` conventions; the `artifact_store` name reads as one thing.**
4. **`[Tier 3 default]` Orphan-scan periodicity → on-demand only (invoked by admin endpoint `POST /api/master_admin/artifact_store/orphan_scan`; NO CRON/scheduled invocation). Rationale: Owner-invoked semantics preserve the AS-H1 "deletion only via Seam 3" doctrine; scheduled destructive work is Tier-1 surface, avoided.**
5. **`[Tier 3 default]` Router path → `POST /api/artifacts` (write) is INTERNAL-only (outer-gate emission calls the adapter directly; no external POST endpoint at this build); `GET /api/artifacts/{trace_id}/{artifact_id}` (read) is the external download endpoint. `HEAD` mirrors GET.**
6. **`[Tier 3 default]` Content-type validation on `put_once` → accept any string, no MIME sniffing (the caller is trusted at this seam; SHA-256 is the integrity contract, not content-type).**
7. **`[Tier 3 default]` `artifact_id` generation → uuid4 hex string at outer-gate emission time (caller supplies, adapter does not generate). Rationale: adapter is stateless w.r.t. IDs; the outer-gate is the ID-minting surface (matches trace_id pattern).**
8. **`[Tier 3 default]` Backlog/registry docs → `stage_a_proposals/artifact_store.md` (this file) + `close_reports/artifact_store.md` (at close) + `rulings/artifact_store_as_e1_to_as_e4.md` (Tier-1 rulings only; Tier-2 and Tier-3 folded into close report per new governance).**

---

## §6. Standing constraints preserved

| Constraint | Attestation at close |
|---|---|
| 28 frozen contracts + 28 snapshots byte-identical (V1-G7) — OR 29/29 if AS-E1 α rules | Attestation cell `test_v1_g7_attestation_parity_at_artifact_store_close`. |
| 4-code auth-refusal registry closed (P9-E3/P8E-E4 pre-carry) | Attestation cell `test_auth_refusal_registry_still_closed_at_four_codes` re-run. |
| E5 (no HTTP 409 in AS diff) | Grep-negative on `artifact_store.py` + `atomic_write.py` + `orphan_scan.py`. |
| E7 middle-dot / P9-E6 α em-dash | No new UI copy at AS Stage A (§2.10). No enforcement cell. |
| Standing Rule v3 (on-disk canonical) | Proposal on disk (this file); reply carries SHA + line-range map only. |
| AS-H1 retention held-class · no direct DELETE | Grep-negative on `routers/artifact_store.py` for DELETE handlers. |

---

## §7. §0.2 Plan-debts status expected at close

- **No new debt anticipated.**
- **AS-OWN-1** (production object-store choice) is an [OWNER] gate line, not a debt. Listed at §4.3; adapter seam is dispatch-independent.

═══════════════════════════════════════════════════════════════════

*End of Artifact Store Stage A proposal. Standing Rule v3: on-disk canonical. Reply body carries file SHA + line-range map + tier-tagged escalation IDs.*
