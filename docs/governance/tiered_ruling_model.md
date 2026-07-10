# Tiered Ruling Model — Standing Governance

**Source:** Owner Message post-8-EXT ratification (2026-07-08).
**Effect:** Effective immediately upon landing of this file.
**Precedes:** All prior "verbatim rulings on every escalation" doctrine. This tiered model REPLACES that doctrine at Artifact Store Stage A dispatch and forward.

**Standing Rule v3 preserved:** this doc lives on disk. Reply body carries SHA + tier tags only.

---

## §0. Verbatim carrier (Owner text, no paraphrase)

> Governance correction, effective now — rules carry a stated basis and block function only where a client promise is at risk:
>
> Tier 1 — client-promise (full rigor): provenance/audit integrity, security boundaries (auth scope, key custody, raw-never-egresses), honesty grammar (class-with-claim, refusal-first, no hidden mocks, no fabricated values), frozen wire contracts. Verbatim rulings and named gates stay.
>
> Tier 2 — cost/rework (proportionate): bands, rates, split thresholds. Disclosure, never blocking — a miss is a line in the close, not a halt.
>
> Tier 3 — hygiene (silent default): naming, glyphs, doc/registry mechanics, backlog accuracy. Builder defaults + one disclosure line. No escalations, no round-trips.
>
> Operational: escalations arrive pre-tiered — Tier 3 never escalates; Tier 2 only at thresholds; Tier 1 keeps verbatim treatment. Pre-flight attestations end unless the dispatch touches Tier-1 surface — the green-light is implicit in the dispatch. Before any rule blocks function: name the promise it protects, or the rule yields with a one-line log.

---

## §1. Tier 1 — Client-Promise (Full Rigor)

**Definition (Owner verbatim):** *"client-promise (full rigor): provenance/audit integrity, security boundaries (auth scope, key custody, raw-never-egresses), honesty grammar (class-with-claim, refusal-first, no hidden mocks, no fabricated values), frozen wire contracts. Verbatim rulings and named gates stay."*

### §1.1 Surface list (non-exhaustive; extend at dispatch time)

- **Provenance / audit integrity:** `NorthenaLedgerRow_v1` shape and emission discipline, trace_id chain integrity, `stamp_audit.data_class` sidecar registry additivity.
- **Security boundaries:**
  - **Auth scope:** own-vs-foreign gates (`require_own_scope_or_deny` and equivalents); 4-code auth-refusal registry closure; JWT class/claim discipline.
  - **Key custody:** `SYNISENSE_MASTER_SECRET`, trust-receipt signature invariants, HMAC/signature boundaries.
  - **Raw-never-egresses:** raw content bytes do not leave the boundary without authz having fired first (mechanism-not-convention).
- **Honesty grammar:**
  - **Class-with-claim:** every disposition/refusal carries a class label.
  - **Refusal-first:** authorization checks precede content emission.
  - **No hidden mocks:** if a value is stubbed for dev-tier, it is loudly disclosed at close.
  - **No fabricated values:** empirical rates come from observed builds, not aspirational figures.
- **Frozen wire contracts:** 28 Pydantic snapshot bijection (V1-G7 assertion set). Any addition is a Tier-1 escalation (parity delta requires Owner rulings).

### §1.2 Discipline

- **Escalations:** verbatim ruling loop (existing template: Class / Question / Authority-source language / Options α/β/γ / Recommended). Owner ruling required BEFORE execution.
- **Named gates:** stay. Grep-negative anti-rule gates stay. Attestation cells stay.
- **Pre-flight attestation:** required only when the dispatch touches Tier-1 surface.
- **Promise-naming rule:** *"Before any rule blocks function: name the promise it protects, or the rule yields with a one-line log."*

---

## §2. Tier 2 — Cost / Rework (Proportionate)

**Definition (Owner verbatim):** *"cost/rework (proportionate): bands, rates, split thresholds. Disclosure, never blocking — a miss is a line in the close, not a halt."*

### §2.1 Surface list

- **Bands:** Owner-anchored LoC/cell bands per phase (`[bottom, top]` snapshot_lloc_in_band verdict).
- **Rates:** amortised cell-cost rates (12 LoC/cell backend Pytest shared-helper · 9 LoC/cell Playwright data-testid · 16 LoC/cell frontend Jest standalone · endpoint/component amortisation rates).
- **Split thresholds:** `§4.2` pre-authorized split (currently 1,500 LoC / 60 cells).

### §2.2 Discipline

- **Escalations:** only at threshold-adjacent choices (e.g., "if the adapter surface exceeds the split threshold, land put_once as commit A and get+head as commit B"). Format: one-paragraph `if X, then split` statement. NO Owner ruling required unless threshold hits AT EXECUTION TIME.
- **Miss handling:** a band miss is a line in the close report, not a halt to execution. Symmetric miss-disclosure per Ruling 5 stays.
- **No pre-flight round-trip.**

---

## §3. Tier 3 — Hygiene (Silent Default)

**Definition (Owner verbatim):** *"hygiene (silent default): naming, glyphs, doc/registry mechanics, backlog accuracy. Builder defaults + one disclosure line. No escalations, no round-trips."*

### §3.1 Surface list

- **Naming:** module names, function names, file names, path conventions.
- **Glyphs:** middle-dot U+00B7, em-dash U+2014, hyphen U+002D discipline — EXCEPT where a glyph carries a Tier-1 promise (e.g., anti-slop charCodeAt gates on UI Spec verbatim copy stay Tier 1 because they protect the "honesty grammar / no fabricated values" surface).
- **Doc/registry mechanics:** file layout, section numbering conventions, close-report skeleton, rulings-record skeleton.
- **Backlog accuracy:** sequence lines, dispatch-order strings.

### §3.2 Discipline

- **NO escalation.**
- **NO Owner round-trip.**
- **Builder chooses default** based on repo conventions + Read-First / Reuse-Always mandate.
- **ONE disclosure line** in the close report using the format:
  ```
  [Tier 3 default] {item} → {chosen default} — {one-line rationale}.
  ```

---

## §4. Operational rules (Owner verbatim carrier)

> Operational: escalations arrive pre-tiered — Tier 3 never escalates; Tier 2 only at thresholds; Tier 1 keeps verbatim treatment. Pre-flight attestations end unless the dispatch touches Tier-1 surface — the green-light is implicit in the dispatch. Before any rule blocks function: name the promise it protects, or the rule yields with a one-line log.

### §4.1 Escalations arrive pre-tiered

Every escalation at Stage A carries an explicit tier tag: `[Tier 1]`, `[Tier 2]`, or `[Tier 3]`. Untagged escalations are a Stage A defect.

### §4.2 Pre-flight attestation

- **Tier-1 surface touched:** pre-flight attestation still required (existing pattern).
- **Tier-1 surface NOT touched:** pre-flight attestation ends. Green-light is IMPLICIT in the dispatch.

### §4.3 Promise-naming rule

Before any rule blocks function: name the promise the rule protects, or the rule yields with a one-line log.

Format for a yielding rule (in close report):
```
[Rule yield] {rule name} yielded on {surface} — {no client promise identified}.
```

### §4.4 Report cadence

- Stage A reply lands → main agent relays [Tier 1] escalations verbatim to Owner. [Tier 2] and [Tier 3] items are disclosure-only, no Owner round-trip.
- **Zero [Tier 1] escalations** → dispatch is complete on Owner side; agent receives implicit green-light and proceeds to execution immediately.
- **≥1 [Tier 1] escalation** → verbatim relay + Owner rulings loop, same as prior.

---

## §5. What stays unchanged

- **Standing Rule v3** — on-disk canonical is the record. Reply body carries SHA + one-line quotes / tier tags.
- **§4.1 baseline atomic first-commit discipline.**
- **§4.2 pre-authorized split thresholds** (LoC and cell numbers; the threshold values themselves are Tier 2 per this model — miss disclosure not blocking).
- **28 frozen contracts + 28 snapshot bijection (V1-G7).** (Post-Artifact-Store bumped additively to 29/29; V1-G7 assertion set at 29.)
- **4-code auth-refusal registry closure.**
- **BCR §5.1 sequence + [OWNER] gate lines.**

---

## §6. Codified rate ledger

Rates below are the on-disk canonical record; Stage A proposals cite this section rather than restating.

### §6.1 Backend Pytest — shared-helper amortised · **12 LoC/cell**

Empirical basis: multiple prior closes (9.1, 9.3, 8-EXT).
Trigger: cells in the "classic shared-helper class" (sync client, shared fixture, ~3-5 assertions per cell).

### §6.2 Backend endpoint impl — amortised 3-share · **40 LoC/endpoint**

Empirical basis: 8-EXT actual (3 grant endpoints via `require_own_scope_or_deny`).

### §6.3 Backend service module — standalone · **100 LoC/module**

Empirical basis: 8-EXT `engineer_scope.py` (84) + `engineer_invites.py` (170) 2-share.

### §6.4 Frontend Jest structural — standalone fallback · **16 LoC/cell**

Empirical basis: pre-9.1 codification; 8-EXT observed −50 delta on `renderHook` micro-cells (rate-composition finding, not rate-shift).

### §6.5 Playwright chromium data-testid amortised · **9 LoC/cell**

Empirical basis: codified at 9.1/9.3.

### §6.6 Frozen Pydantic contract class · **60 LoC/class**

Empirical basis: `OuterGateReceipt_v1` at AS close (103 LoC actual; 60 LoC class body + ~40 LoC docstrings/verbatim-Owner-carriers). Rate cites the class-only shape; verbatim docstrings are one-off overhead.

### §6.7 Frozen contract snapshot JSON — standalone · **~155 LoC/snapshot**

**Codified at 2026-07-08 post-Artifact-Store close.**

- **Class label:** *"snapshot = schema size"* — the LoC of a snapshot reflects the Pydantic-auto-generated JSON Schema's expansion of nested `$defs`, `enum`, and field-description shape. It is a mechanical function of the contract's field graph, NOT of developer effort.
- **Empirical basis:** `OuterGateReceipt_v1` snapshot at AS close — **155 LoC actual vs 20 planned (+735%).** The contract inherits `LedgerArtifactRef` + transitive types; those get spelled out under `$defs` in the JSON Schema.
- **Amortisation trigger:** NONE. Standalone class. Snapshots do not share code with other cells; each frozen contract emits exactly one snapshot; the size is a byte-cost of schema honesty on disk.
- **Named trigger:** *"Any Stage A adding a new frozen contract MUST price its snapshot at ~155 LoC/snapshot standalone in §3 band derivation. No hidden buffering; no padding; explicit line-item."*
- **Deviation clause:** if a specific contract's snapshot lands materially above or below 155 LoC (>±30%), disclose the delta at close per Tier-2 discipline (governance §2.2 — cost/rework class).

### §6.8 Watched rate classes (NOT YET codified — require second observation)

Per Ruling 5 discipline: a rate class is codified only after two observations. The following are candidates:

- **Async httpx backend Pytest cells** — ~25 LoC/cell empirical at AS (vs 22 standalone / 12 amortised). Auth-overhead class (`AsyncClient` + token minting + trace/artifact provisioning per cell). **Requires second observation to codify.**
- **AST/reflection gate cells** — ~40 LoC/cell empirical at AS (AS-G6 grep-negative walker + whitelist + violation formatting). Reflection-gate class. **Requires second observation to codify.**

If either class recurs at Transform Forms or beyond with similar per-cell LoC, it becomes eligible for codification via a companion Stage A rate note.

---

## §7. Backlog correction (Owner verbatim carrier)

> Backlog correction: strike "§5.4 Dual-actor Integration Console" — 8-EXT was §5.4; done, not queued.

**Effect:** the backlog line *"§5.4 Dual-actor Integration Console"* is STRUCK from PHASE_STATE.md and PRD.md. 8-EXT (closed 2026-07-08, ratified in this same Owner message) IS §5.4.

═══════════════════════════════════════════════════════════════════

*End of standing governance record. Effective 2026-07-08 forward. On-disk canonical per Standing Rule v3.*
