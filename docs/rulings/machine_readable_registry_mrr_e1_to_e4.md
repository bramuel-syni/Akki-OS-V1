# Machine-Readable Registry · MRR-E1..MRR-E4 Owner Rulings Record

**Dispatched:** 2026-07-11 (post-Stage-A verbatim relay).
**Basis:** `/app/docs/stage_a_proposals/machine_readable_registry_stage_a.md` @ SHA `a4c2642c…`.
**Doctrine SHA:** `0bfe65c47e2c55f35e2a860fec405c05b8ed32b3473bcb63a0a259fb810ab471` (in force).
**Governance:** Standing Rule v3 · on-disk canonical · Registry Doctrine v1.0 R4 + D-10 in force · Defect D7 binds.

---

## §1. Ruling — MRR-E1 · α (with integrity-binding condition)

**Owner verbatim:**
> "MRR-E1 — α. Human doc → machine form, parser-derived. This is the doctrine's own graduation sentence made literal: the governed document remains the authored source; the machine form is generated and never hand-edited. One condition, integrity-binding by construction: **the generated form embeds the source SHA it was derived from** (`source_sha: 598a7ad4…`) — a machine form that can't name its source is an unattributed claim. β is the right *future* (once queries and harness operate on the machine form, authority graduates to it) — but that flip is a governance amendment when the time comes, never drift; recorded as the acknowledged path, not taken now. γ is the dual-maintenance spiral the doctrine exists to prevent."

**Applied at execution:**
- Parser at `backend/services/registry/parser.py` reads v0.md + `v0.1_supplement.md` at ruled SHAs; emits machine form. Regeneration only via `tools/registry/regenerate.py` — NO hand-edit permitted.
- Machine form embeds top-level `source_of_truth: {path, sha256}` block referencing v0.md SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0`.
- Header comment on machine form: `# GENERATED FROM function_promise_registry_v0.md + v0.1_supplement.md · DO NOT HAND-EDIT · regenerate via tools/registry/regenerate.py`.
- MRR-G-SourceSHA new gate cell (see §5 gate roster) asserts machine form's embedded SHA matches v0.md's on-disk SHA.

## §2. Ruling — MRR-E1 β acknowledged future path (formal note · not standing rule)

**Owner verbatim:**
> "β is the right *future* (once queries and harness operate on the machine form, authority graduates to it) — but that flip is a governance amendment when the time comes, never drift; recorded as the acknowledged path, not taken now."

**Recorded as:** acknowledged-future-path note (NOT a governance addendum · NOT a standing rule). Class: formal acknowledgment of graduation trajectory. Trigger: future Owner dispatch when doctrine §8.1.a executable queries + §8.1.b sequencing harness land AND operate on machine form as canonical source. Mechanism: governance amendment (not drift-driven).

## §3. Ruling — MRR-E2 · γ (both surfaces)

**Owner verbatim:**
> "MRR-E2 — γ. Both surfaces — inline rulings on affected rows *and* the top-level supersession ledger with cross-references. The v0.md carries a dual-surface archival posture by Standing Rule v3; a lossy conversion of an archival posture is a content change wearing a format costume. γ is the only 1:1 reading."

**Applied at execution:**
- Machine form carries BOTH:
  - Inline `rulings: [{id, tag, ref}]` field on affected function/finding rows (all 11 items Q2-01..Q3-04).
  - Top-level `findings_supersession_ledger: [{finding_id, original_state, superseded_state, ruling_ref}]` array with cross-references to inline rulings.
- Verbatim v0.md dual-surface archival posture preserved 1:1.

## §4. Ruling — MRR-E3 · β + addition (foreign-key promise integrity + Part II vocab constant)

**Owner verbatim:**
> "MRR-E3 — β, one addition. Foreign-key promise integrity: every function's `promise` must resolve to an existing promise row — the builder's own typo example is precisely the fabrication class this closes (a promise reference that resolves to nothing is a fabricated attribution). Addition, closing the same class on the other field without γ's artifact coupling: **`service_trace` steps validate against the Part II journey-step vocabulary embedded as a constant in the validator** — sourced verbatim from the doctrine, updated only via governance amendment. A typo'd journey step silently minting a phantom step is the identical defect one field over. γ's separate doctrine-derived enum file is declined: new artifact class, new coupling, same protection available as a constant."

**Applied at execution:**
- Validator at `backend/services/registry/validator.py` implements MRR-G2 with two-field lock:
  - **(a) Foreign-key promise integrity:** every function row's `promise` field must reference an existing top-level `promises` array's `promise_id`. Unresolved reference = fail.
  - **(b) Part II journey-step constant lock:** `PART_II_JOURNEY_STEPS` frozenset embedded in validator source file, sourced verbatim from `/app/docs/governance/registry_doctrine_v1.md` Part II lines 32-36. Every function row's `service_trace` step values must be members of the constant. Vocab updates require governance amendment (not code edit).
- Note on v0.md-observed forms: v0.md source-of-truth uses canonical short forms `S3.prove` (= doctrine `prove-end-to-end`) and `S4.verify` (= doctrine `verify-receipt`). Both forms are enrolled in the constant as sanctioned equivalents with source cites; drift-vs-doctrine surfaced at close §6 as Tier-2 disclosure. Both sets remain governance-amendment-only.

## §5. Ruling — MRR-E4 · β (supplement sidecar + standing consequence)

**Owner verbatim:**
> "MRR-E4 — β. The supplement sidecar. It's the only option honoring both bindings: v0.md stays byte-identical at its ruled SHA, and R4's rows are queryable Registry members, not attest-only residue (γ would weaken R4 on the doctrine's first code-adjacent phase — a precedent we'd regret). And β isn't a new invention — it's the system's own additive-versioning pattern applied to the Registry itself. **Standing consequence, so this tension never re-escalates:** future phases' R4 rows land the same way — additive supplements beside the locked source, consolidated into the next Registry version at a future owner-dispatched maintenance turn. MRR-G3's round-trip operates over (v0.md + supplements) ↔ machine form as one set."

**Applied at execution:**
- Supplement sidecar at `/app/docs/registry/function_promise_registry_v0.1_supplement.md` carries THIS PHASE'S 7 R4 reflexive rows (MRR-G1..G4 + MRR-G-Parity + MRR-G-DataBlind + MRR-G-SourceSHA · reflexive-placement subsumed by MRR-G-SourceSHA gate + attest).
- v0.md remains byte-identical at SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0` — verified pre/post commit.
- Parser accepts `(v0.md + v0.1_supplement.md)` as combined source; emits machine form covering both.
- MRR-G3 round-trip operates over combined source as one set per Owner-explicit.

**Standing consequence landed as governance §14** in `/app/docs/governance/tiered_ruling_model.md` — verbatim per Owner directive.

## §6. Ruling — Band `[1,600, 3,000]` RATIFIED · Format Tier-3

**Owner verbatim:**
> "Band `[1,600, 3,000]`: RATIFIED. Format remains the builder's Tier-3 as scoped — with E1 ruled α, the pending recommendation (YAML, split-by-record-class) unblocks; the builder's call, disclosed at close."

**Applied at execution:**
- **Band ratified** `[1,600, 3,000]` raw LoC.
- **Format Tier-3 decision:** builder-selected **YAML · single-file `registry.yaml`** — single-file for cleanest round-trip attest (one file to `sha256sum`); split-by-record-class deferred to future phase as size grows. Disclosed at close §4.3.

## §7. Ruling — Execute atomic commit

**Owner verbatim:**
> "Execute: atomic commit → close with gate roster (MRR-G1..G4 + parity + data-blind, E3's two-field lock attested), source-SHA pin shown, supplement landed, band actual in raw LoC, D-10 riding per standing."

**Applied:** atomic single commit landing this rulings record + governance §14 addendum + supplement sidecar + parser + validator + machine form YAML + test cells + close report. Test triad: Pytest re-run (new cells added) · Jest/Playwright not re-run (backend-only, per Owner). §12 auto-ratification-on-own-text applied if (a) gates green, (b) rulings + E1 condition + E3 addition + E4 β + §14 attested, (c) no new Tier-1 mid-execution.

---

## §8. Standing constraints preserved

- **D7 binds:** no code · no CI · no query automation · no harness · no worker wiring · no Playbook/Thesis · no Registry content changes to v0.md · no Q2-05 reads · no next-cell scaffolds.
- **MANDATE-COMPLETE 2026-07-10 held.** Registry Doctrine v1.0 in force.
- **Parity 31/31 preserved** (envelope untouched).
- **Standing Rule v3:** on-disk canonical · SHAs in reply body.
- **v0.md byte-identical** at SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0` throughout.
- **Governance §14 in force** (standing consequence per MRR-E4 β).

═══════════════════════════════════════════════════════════════════

*End of MRR-E1..MRR-E4 rulings record. All 4 Tier-1s ruled: α · γ · β+addition · β. Standing consequence §14 landed. Format Tier-3 disclosed. Standing Rule v3 · on-disk canonical.*
