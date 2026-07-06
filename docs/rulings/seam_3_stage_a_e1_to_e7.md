# Seam 3 + §8 Checker Stage A — Owner Rulings E1 through E7

**Ruling date:** 2026-07-06
**Dispatch class:** Amendment-only pass on Stage A proposal (E1) + BCR v1.4 (E7).
**Build status:** PAUSED. Sub-stage 1 dispatches only after this rulings record + Amendment A + Amendment B are all on-disk with confirmed SHAs.
**Standing Rule v3:** All rulings verbatim; no paraphrase.

═══════════════════════════════════════════════════════════════════

## §1. Owner rulings — verbatim (from dispatch message, 2026-07-06)

### E1

> **E1** — Reject both α and β. Apply the registry pattern. Refusal-family is a constrained-str backed by an external versioned registry (`refusal_families.v0.json`), per the admission-refusal-reasons precedent. α (reason-string overloaded onto `stage="converge"`) makes the ledger row misreport its own stage — rejected. β widens a frozen Literal — the scheduled hazard-stop. `NorthenaLedgerRow_v1` stays byte-identical; families extend as registry additions. Amend the Stage A proposal to reflect this before Sub-stage 2 dispatches.

### E2

> **E2** — Confirm dev disposition: backend endpoint at Sub-stage 2, retention-write UI queued for B-5b. One binding condition: the retention endpoint and its consequence-class routing land in the same commit, or the endpoint ships loosening-disabled. A retention write is protection-relevant — tightening is unilateral-with-delay, loosening/lengthening requires Administration counter-sign. **No ungated loosening write ships "because the UI is later."**

### E3

> **E3** — Server-computed ISO date. A compliance record's date is a fact of the record, computed once server-side, identical across every viewer and export. Client-locale composition rejected.

### E4

> **E4** — Colocate in `services/compliance/`. One consumer exists; a shared `_helpers/` module is speculative. Extract on second use, not before.

### E5

> **E5** — Confirmed, no action. Unauthorized on the checker is access-control class; the 4-code registry covers it. The rejected 409 was the trap — a counter-sign-pending state is not an HTTP conflict. Reuse the 403 path, no new codes.

### E6

> **E6** — Close. `MasterAdminHomePage.js` exists on disk; the HAZARD-STOP branch is dead. Extend inline at Sub-stage 3.

### E7

> **E7** — UI Spec v2.1 is the surface authority; middle-dot wins. "Verbatim per CK-U1" currently points at two different strings — an unsatisfiable spec. Correct BCR v1.4's two hyphen instances to middle-dots. One-glyph doc fix, rides the E1 amendment pass, not a separate phase.

═══════════════════════════════════════════════════════════════════

## §2. File SHAs — before and after amendments

### §2.1 Stage A proposal (`/app/docs/stage_a_proposals/phase_8_seam_3_and_checker.md`)

- **Pre-amendment SHA-256 (2026-07-06 morning delivery):** `111b4c43339b7b4db456fcf5c78d38cbbdad959ed419f2808d7ef83374142b89`
- **Post-amendment SHA-256 (this pass):** `19368bae8b09ddf3af18707a7ae183342c1f6a5df914bedc16e3346721fd8963`

### §2.2 BCR v1.4 (`/app/docs/mandates/RMS_Build_Completion_Requirements_v1_4.md`)

- **Pre-amendment SHA-256:** `d1f49bc5d7cbf1dea044ca4069a1dc2d45f01876e531b7500d860ae3f48aebdd`
- **Post-amendment SHA-256 (v1.4.1 doc-correction):** `ce5206c9e244fe58edb6824f785077c1c835bdf3f5b347f6a4fb98c036212524`

═══════════════════════════════════════════════════════════════════

## §3. Notes attached to individual rulings

### §3.1 E2 binding condition — Sub-stage 2 dispatch precondition

**Binding condition (verbatim):** *"the retention endpoint and its consequence-class routing land in the same commit, or the endpoint ships loosening-disabled."*

**MUST be re-cited in the Sub-stage 2 build brief.** Given the split ordering has Sub-stage 3 (checker) landing AFTER Sub-stage 2, the natural fit is **loosening-disabled at Sub-stage 2 close**, enabled at Sub-stage 3 close via the checker's countersign path. The Sub-stage 2 build brief MUST re-cite this binding condition to prevent silent regression.

**Corresponding named gate at Sub-stage 2:** `test_retention_endpoint_loosening_disabled_pre_checker` — LOAD-BEARING. Attempt a loosening/lengthening write pre-checker → 403 access-control body with reason `awaiting_consequence_class_checker`. Retires at Sub-stage 3 close, replaced by `test_retention_loosening_write_requires_administration_countersign` per CK-B3 symmetry.

### §3.2 E6 CLOSED

**Verified via 2026-07-06 recon:** `frontend/src/pages/master_admin/MasterAdminHomePage.js` present on-disk. HAZARD-STOP branch is dead. Sub-stage 3 extends the page **inline** — adds `CounterSignBanner` render + pending-items read wiring. No page-creation escalation. No sub-stage 3 dispatch precondition attached to E6.

### §3.3 E5 CLOSED

**Cross-reference (added post-acknowledgment, 2026-07-06):** the 409-for-governance-state anti-rule stated in this section is ELEVATED TO STANDING per Owner refinement at §8.2 below — applies to any checker-adjacent work, all phases, all seams; no longer Seam-3-scoped. This §3.3 body preserved verbatim as the historical Seam-3-scoped record; §8.2 carries the standing elevation.

**No action, no proposal change.** The 4-code auth registry closed posture is preserved (`auth_scope_insufficient` / `auth_missing` / `auth_expired` / `auth_identity_mismatch_for_wizard_session`). Explicitly ruled OUT: any HTTP 409 pattern for counter-sign-pending states — counter-sign-pending is NOT an HTTP conflict. The 403 access-control path is reused for unauthorized-on-checker denials. No new §0.1 dispositions expected across Sub-stages 1-3.

### §3.4 E3 + E4 CLOSED — ruled, no further proposal change required

**Cross-reference (added post-Sub-stage-1-ratification, 2026-07-06):** E3 mechanism REFINED per Owner ratification-point Point 1 — REJECT deploy-date config store (α), APPLY query-time first-timestamp-per-family (β) with honest-cost binding. See §8.4 below for the standing refinement text; see Stage A proposal §7.3.β + §7.3.β.1 for the codified mechanism. E4 remains unchanged.

- **E3:** Server-computed ISO date. Client-locale composition rejected. Applied in Stage A §7.3 amendment.
- **E4:** Colocate in `services/compliance/`. Applied in Stage A §7.4 amendment; `emit_refusal_ledger_row` lives at `services/compliance/refusal_ledger.py`; dead stub at `services/service_1/async_state.py:238` receives migration docstring but stays byte-identical (BC preserved).

═══════════════════════════════════════════════════════════════════

## §4. Amendment audit trail (Standing Rule v3)

### §4.1 Amendment A — Stage A proposal (E1 + downstream propagation)

**File:** `/app/docs/stage_a_proposals/phase_8_seam_3_and_checker.md`

**Changes:**
- §7.1 restructured — pre-ruling α/β analysis preserved verbatim in §7.1.α + §7.1.β (marked RULED AGAINST); new §7.1.γ subsection describes the constrained-str + external versioned registry pattern per Owner ruling.
- §7.2, §7.3, §7.4, §7.5, §7.6 — each block gains a **RULED** marker + Owner verbatim ruling text + binding-disposition line.
- New §7.7 added — E7 binding-copy correction record.
- §3.1 cumulative frozen-contract count block — removed α/β conditional; states parity 26 unchanged across all 3 sub-stages.
- §4.1 Sub-stage 1 deliverables — `emit_refusal_ledger_row` module location updated to `services/compliance/refusal_ledger.py` (per E4); `refusal_families.v0.json` registry file added to deliverables (per E1.γ); dead-stub migration path clarified.
- §5.1 Sub-stage 2 deliverables — E1.γ + E2 binding condition prefix note added; retention-config write endpoint gains E2 loosening-disabled semantics + new named gate `test_retention_endpoint_loosening_disabled_pre_checker`.
- §5 LoC budget — removed α/β conditional; single band `[2500, 2900]` with `snapshot_lloc_in_band = no`.
- §6.1 Sub-stage 3 deliverables — E1.γ (reused) + E6 CLOSED + E2 loosening-enablement note added.
- §8 Standing constraints one-liner — removed "UNLESS E1.β" conditional.
- §9 Total table — removed α/β conditional; single total band `[5900, 7200]` with parity 26 preserved.
- §10 Dispatch posture — all 3 sub-stages marked ready (Sub-stage 1 on Owner go-signal; Sub-stages 2 + 3 post-prior-sub-stage-ratification).
- Lines carrying CK-U1 verbatim quote (formerly 87 + 322, now 88 + 331 after amendment insertions shifted line offsets) updated: ASCII hyphens → middle-dots (·, U+00B7), matching post-E7-corrected BCR.

**Historical α/β analysis preserved.** Owner-directed: no deletion of ruled-against branches. Marked inline as **RULED AGAINST (2026-07-06)** with the Owner ruling text carried verbatim in each ruled-against subsection.

### §4.2 Amendment B — BCR v1.4 (E7 doc-correction)

**File:** `/app/docs/mandates/RMS_Build_Completion_Requirements_v1_4.md`

**Changelog entry (v1.4.1, line 3 amendment):**

> *"v1.4.1 (owner ruling E7, 2026-07-06) aligns CK-U1 binding-copy glyph (§3.11) with UI Spec v2.1 §8/§10 middle-dot (·, U+00B7) rendering; two ASCII hyphens on line 256 replaced with middle-dots. Doc-correction only, no requirement change."*

**Byte-level edit (line 256, single line containing both hyphens):**
- **Pre-edit:** `Commit line binding copy: 'Signed by {initiator} - counter-signed by {checker} - recorded with both identities.'`
- **Post-edit:** `Commit line binding copy: 'Signed by {initiator} · counter-signed by {checker} · recorded with both identities.'`
- Two ASCII hyphens (`-`, U+002D) → two middle-dots (`·`, U+00B7).
- Both hyphens on the same line 256 (single-line CK-U1 rendering in the BCR); verified via `grep -c` sweep: post-edit BCR file has **zero** occurrences of `Signed by {initiator} -` (pre-edit had 1 line containing 2 hyphens).

═══════════════════════════════════════════════════════════════════

## §5. Downstream propagation notes (Sub-stage 1 build precondition)

### §5.1 Registry file location + shape (E1.γ operationalization)

- **On-disk path:** `/app/backend/services/compliance/refusal_families.v0.json` — colocated with the consumer per E4 ruling; mirroring the admission-refusal-reasons location convention (`/app/backend/services/service_1/admission_refusal_reasons.vN.json` — service-local, consumer-adjacent).
- **Landing:** the JSON file itself lands as PART of Sub-stage 1 build (NOT this amendment pass). This pass only *specifies* it in the amended Stage A proposal.
- **Initial families enumerated at Sub-stage 1 build:** `admission_refusals`, `composition_below_floor`, `outer_gate_refusals`, `unclassified`.
- **Version bump discipline:** family additions land as `v0` → `v1` → `v2` … registry version bumps (append-only). Registry version bumps are per-Sub-stage-close events, NEVER inline Literal widenings on `NorthenaLedgerRow_v1`.

### §5.2 `emit_refusal_ledger_row` canonical location (E4 operationalization)

- **On-disk path:** `/app/backend/services/compliance/refusal_ledger.py` — colocated with the compliance package (its consumer).
- **Dead-stub disposition:** `/app/backend/services/service_1/async_state.py:238::emit_ledger_terminate_refused` stays byte-identical (BC preserved). Gains migration docstring: `# MIGRATED: canonical single-source is services/compliance/refusal_ledger.py::emit_refusal_ledger_row`.

### §5.3 Coverage-marker `{date}` composition (E3 operationalization)

- **Server-computed ISO date** at Sub-stage 1 close (`YYYY-MM-DD` in UTC).
- **Client renders verbatim** — no frontend-side date formatting.
- Backend surface at `GET /api/compliance/refusals_coverage` returns the ISO literal directly.

═══════════════════════════════════════════════════════════════════

## §6. Constraints reaffirmed at this pass

- **No code changes.** ✅ Documentation and JSON-registry-planning only. The `refusal_families.v0.json` file itself does NOT land this pass — it lands as part of Sub-stage 1 build.
- **No dispatch of Sub-stage 1, Sub-stage 2, or Sub-stage 3.** ✅
- **No test runs.** ✅ No `make ci`, no Jest, no Playwright.
- **26 frozen contracts + snapshots untouched.** ✅ E1.γ ruling explicitly preserves them byte-identical.
- **Historical α/β analysis in §7.1 preserved.** ✅ Not deleted; marked RULED AGAINST verbatim per Owner directive.
- **Owner rulings in §1 above are verbatim.** ✅ No paraphrase.

═══════════════════════════════════════════════════════════════════

## §7. Post-amendment posture

**All escalations E1 through E7 ruled at the 2026-07-06 amendment pass.** Sub-stage 1 dispatches only after Owner acknowledges this rulings record + Amendment A + Amendment B are all on-disk with confirmed SHAs. Sub-stage 2 dispatches only after Sub-stage 1 ratification, WITH the E2 binding condition re-cited in the Sub-stage 2 build brief. Sub-stage 3 dispatches only after Sub-stage 2 ratification.

═══════════════════════════════════════════════════════════════════

## §8. Owner refinements (post-acknowledgment, 2026-07-06)

Owner refinement dispatch received 2026-07-06 (post-acknowledgment of §1-§7 above). Two refinements landed as an addendum-only pass — Amendment C (Stage A §7.1.γ.1 subsection) + Amendment D (this section). Owner refinement text is verbatim below; no paraphrase.

### §8.1 Observation 1 refinement — carrier + wire-shape gate

**Owner refinement verbatim:**

> Sidecar is the right container, wrong as a loose Dict. Pin the key. The refusal-family value is a queried, grouped dimension (it feeds the refusals-by-month aggregate and the regulator surface), not audit metadata — burying it in an unschematized stamp_audit Dict means every aggregate reads a key with no guarantee it exists or holds a registry-valid value. But a top-level typed field mutates NorthenaLedgerRow_v1 and breaks byte-identity. Resolve both the same way §6.1 was: keep the sidecar, pin `stamp_audit["refusal_family"]` under a load-bearing wire-shape gate asserting presence and registry-validity on every refusal-terminal row. Contract stays byte-identical, parity 26 holds, the aggregate reads a guaranteed key. One-line addendum to §7.1.γ.

**Applied disposition (binding):**
- **Pinned-key mechanism:** the registry-backed constrained-str family value lives at **`stamp_audit["refusal_family"]`** — pinned key inside the existing `stamp_audit: Optional[Dict]` sidecar on `NorthenaLedgerRow_v1`. Contract stays byte-identical (parity 26 holds).
- **Load-bearing wire-shape gate:** **`test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit`** — LB. Asserts on every refusal-terminal row (any `NorthenaLedgerRow_v1` with `decision="refused"`): (a) `stamp_audit` is present; (b) `stamp_audit["refusal_family"]` is present as a key; (c) its value is a registry-valid entry per the currently-loaded `refusal_families.vN.json`. **Retirement condition: never** — permanent load-bearing gate protecting aggregate + regulator-surface consumers from unschematized reads.
- **§6.1 precedent cited:** Sub-stage 3 CK-B1 dual-identity uses the same pattern — `services/checker/countersign_ledger.py` (Stage A proposal line 319) emits with pinned-key stamp_audit + gate CK-G2 `test_countersign_row_carries_both_identities` (Stage A proposal §6.1 test matrix line 342) asserts LB presence of the pinned keys on every countersign row.
- **First-commit gating:** the wire-shape gate lands in the same commit as `emit_refusal_ledger_row` + the 4 emission-site instrumentations at Sub-stage 1 build.
- **Amendment C landing location:** Stage A proposal §7.1.γ.1 subsection immediately after §7.1.γ body (before §7.2); §7.1.α, §7.1.β, and existing §7.1.γ body all UNMODIFIED.

### §8.2 Observation 3 elevation — 409-for-governance-state anti-rule (STANDING)

**Owner refinement verbatim:**

> Keep, elevated. 409-for-governance-state is a trap on any checker-adjacent work, not just Seam 3. The standing anti-rule is better than my narrower version.

**Applied disposition (binding, STANDING):**
- **Elevation:** the "counter-sign-pending is NOT an HTTP conflict; reuse the 403 access-control path, no 409-for-governance-state" anti-rule is **ELEVATED TO STANDING** — applies to any checker-adjacent work, all phases, all seams. Not Seam-3-scoped.
- **Historical §3.3 (E5 CLOSED) preserved verbatim** as the original Seam-3-scoped record; §3.3 now carries a cross-reference note pointing at this §8.2 for the standing elevation. The Seam-3-scoped body was NOT rewritten.
- **Enforcement footprint:** applies to every future dispatch touching state-machine transitions, dual-control paths, tightening-effective/objection paths, retention-write consequence routing (Sub-stage 2 loosening path), and any B-5b write path that routes through the §8 checker. If any such surface proposes 409 for a governance-pending state, that proposal is anti-rule-violating and MUST be rewritten to use the 403 access-control class with a plain-language reason.
- **Naming convention for the anti-rule (for future citation):** *"409-for-governance-state anti-rule (standing, ruled 2026-07-06)"*.

### §8.3 Observation 2 record — test-gate enforcement of E2 loosening block

**Owner refinement verbatim:**

> Keep test-gate enforcement of the E2 loosening block. No change.

**Applied disposition (record only):**
- No change to §3.1 (E2 binding condition — Sub-stage 2 dispatch precondition).
- The named gate `test_retention_endpoint_loosening_disabled_pre_checker` (from §3.1) is confirmed by Owner as the load-bearing mechanism enforcing the E2 loosening block at Sub-stage 2 close. Retires at Sub-stage 3 close per §3.1.

### §8.4 Point 1 refinement — E3 mechanism (RULED, 2026-07-06 Amendment E)

**Owner refinement verbatim (Point 1):**

> Reject the deploy-date store; use query-time first-timestamp-per-family (the proposal's β). Deploy date is false-by-construction: it claims coverage from the moment emission went live, but three families were historically un-ledgered, so their true coverage-since is the first timestamp a row actually carries `refusal_family` — a fact in the ledger, not a config value. Store the deploy date and you assert coverage that may not exist. β reports what the ledger contains. If β has a query-cost problem (unindexed scan on every card render), solve it honestly — index or a materialized value showing its as-of timestamp — never substitute a wrong-but-cheap date. Flag the cost if it's real; don't route around correctness.

**Applied disposition (binding):**
- (a) **Query-time first-timestamp-per-family is the canonical mechanism.** For each family, the `{date}` literal is the ISO-8601 date (`YYYY-MM-DD` UTC) of the earliest `NorthenaLedgerRow_v1` whose `stamp_audit["refusal_family"]` matches that family. Query filter: `{decision: "refused", "stamp_audit.refusal_family": <family>}` sorted timestamp ascending; picks first row per family. Pre-wire-up rows without the pinned key are naturally excluded — β reports what the ledger contains AND carries the family key.
- (b) **`refusal_family_since_dates.v0.json` config file does NOT land at Sub-stage 1.** The pre-Amendment-A filename is permanently ruled out; the pre-Amendment-A OR-branch language ("set once server-side at Sub-stage 1 close and persisted immutably in the versioned config") is also permanently ruled out. The registry `refusal_families.v0.json` (per §7.1.γ) remains the family-enumeration authority; its `since_date` field (if present in the Sub-stage 1 registry shape decision) MUST NOT be consumed for coverage-marker `{date}` rendering — that consumption path is the exact α trap.
- (c) **Honest-cost flagging obligation on `e1_dev` at Sub-stage 1 build:** IF the query cost manifests as a measurable problem during Sub-stage 1 implementation (observable render latency on v2.1 §4.1 Refusals card, unindexed-scan warnings from MongoDB explain plans, or equivalent honest evidence), `e1_dev` MUST flag this HONESTLY in the Sub-stage 1 close report with concrete evidence (measured latency numbers, explain-plan output, or equivalent).
- (d) **NO pre-optimization.** Do NOT pre-emptively add an index. Do NOT pre-emptively add a materialization file. Do NOT pre-emptively add a cached-value store. Owner rules the mechanism if and only if a cost problem is honestly flagged. Correctness-preserving posture: any future cost-solving mechanism ruled by Owner must preserve query-time correctness — index the SAME query, or materialize with an AS-OF timestamp visible to the read, never fabricate a coverage claim.
- (e) **Stage A proposal §7.3.β + §7.3.β.1 are the canonical codification.** §7.3.α + §7.3.γ are RULED AGAINST verbatim-preserved. §7.3.β.1 (Honest-cost binding) carries the pure-query-time default + honest-cost obligation + no-pre-optimization + correctness-preserving posture verbatim.

### §8.5 Point 2 narrowing — §8.2 anti-rule scope at Sub-stage 1 (RECORD)

**Owner refinement verbatim (Point 2):**

> Narrow to "no 409 introduced by this sub-stage." Full anti-rule enforcement on a sub-stage that builds no checker code is machinery for an absent risk. The 409 ban stands globally; Sub-stage 1 carries only the obligation not to introduce one.

**Applied disposition (record only, NO re-ruling of §8.2):**
- The standing 409-for-governance-state anti-rule (§8.2) applies GLOBALLY across all phases, all seams, all checker-adjacent work. That standing remains untouched.
- Sub-stage 1 obligation NARROWED to: **"no 409 introduced by this sub-stage."** Sufficient because Sub-stage 1 builds no checker code — full anti-rule enforcement machinery (per-endpoint scan, per-router grep, cross-console negative gates) on a sub-stage that ships zero checker semantics is machinery for an absent risk.
- Sub-stage 1 enforcement mechanism: `e1_dev` at Sub-stage 1 build confirms — via inspection of the Sub-stage 1 diff — that no new endpoint or handler in the Sub-stage 1 changeset returns HTTP 409. No dedicated gate required at Sub-stage 1; the diff-inspection assertion is captured as a one-line confirmation in the Sub-stage 1 close report.
- Full anti-rule enforcement machinery (dedicated grep-negative gate + AST negative gate + cross-endpoint audit) reactivates at Sub-stage 2 (retention endpoint touches checker-adjacent surface via loosening path) and Sub-stage 3 (§8 checker itself lands with its state machine + counter-sign transitions).

### §8.6 Point 3 confirmation — Playwright glyph assertion (RECORD)

**Owner refinement verbatim (Point 3):**

> Keep the glyph assertion. E7 exists because the glyph was wrong. A smoke that checks surrounding words but not the glyph passes on the exact defect E7 fixed. Glyph-level assertion is brittle only when the glyph doesn't matter; here it's the point.

**Applied disposition (record only):**
- Playwright chromium smoke for the coverage-marker refusals-card rider (part of Sub-stage 1 first-commit-gated smoke suite) MUST assert the middle-dot glyph (`·`, U+00B7) **specifically** — not just the surrounding words. This applies wherever the Owner-supplied binding-copy pattern renders: v2.1 §4.1 Refusals card coverage-marker text (Sub-stage 1) AND downstream at v2.1 §8 checker CK-U1 commit-line binding-copy render (Sub-stage 3).
- Rationale (Owner verbatim): E7 fixed a glyph-level defect (hyphens vs middle-dots); a smoke that asserts only surrounding words would pass on the exact defect E7 corrected. Glyph-level assertion is correctness-preserving here — not brittleness — because the glyph IS the point.
- Concrete smoke assertion pattern (indicative; exact syntax settled at build): `expect(page.locator('[data-testid="coverage-marker-text"]')).toHaveText(/·/)` — MUST match the U+00B7 middle-dot byte specifically. Naming convention: `test_coverage_marker_renders_middle_dot_glyph_verbatim` (Sub-stage 1); `test_countersign_commit_line_renders_middle_dot_glyphs_verbatim` (Sub-stage 3).

═══════════════════════════════════════════════════════════════════

## §9. Post-Amendment-C+D posture

**All Owner refinements (Observations 1 + 2 + 3) applied.** Per Owner directive on this dispatch: *"Authorize Sub-stage 1 after the Observation-1 addendum lands (pinned key + gate). E1.γ / E2 / E3 / E4 / E7 pre-carry as listed, cited to `038bd24d…`."* — Sub-stage 1 is **pre-authorized** once this addendum pass lands with confirmed SHAs. Build agent does NOT self-dispatch Sub-stage 1; awaits the Sub-stage 1 build brief in a follow-up Owner message.

═══════════════════════════════════════════════════════════════════

*End of rulings record. Build stays PAUSED through this addendum pass.*
