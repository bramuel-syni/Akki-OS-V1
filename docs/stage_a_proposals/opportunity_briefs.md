# §3.15 Opportunity Briefs — Stage A Proposal

**Dispatch:** Owner ruling post-§3.8-ratification (2026-07-10 · unconditional).
**Basis:** BCR v1.5 §3.15 verbatim (lines 294-312) + UI Specification v2.2 §3.7 · v1.5 amendment 2026-07-08.
**Governance:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. Metric-verdict in raw LoC per §9 (band-relative trichotomy). Data-blind posture §8. Close-ratification discipline §12 (Owner 2026-07-10).
**Standing Rule v3:** on-disk canonical. Reply body carries SHA + tier tags + escalation matrix.
**Precedent:** Rides existing Registry read API + Shield chokepoint + sidecar-telemetry pattern (9.2a-E2 α cond 2 · AF-E3 α). Salvage-lifted reasoning per OB-R1 from `github.com/bramuel-syni/Akki-Executive-Core` (lifted, not imported; no runtime dependency).

---

## §1. Owner dispatch — verbatim carrier

> **Dispatch: Opportunity Briefs Stage A — §3.15 as amended.** OB-R1..R6, gates OB-G1..G5, three brief scopes (slice / combined / estate), fixture-census per AS-U2, estate-spanning examples, salvage-lifted reasoning per OB-R1. Escalations pre-tiered; band in raw LoC per §9; §4.2 thresholds stated. Tier-1 surfaces are already named in the mandate — OB-R2 grounding integrity, OB-R3 class honesty, OB-R6 per-slice grounding — expect escalations there and nowhere else. Then production housing (§3.4), then mandate-complete.

**Mandate reference (BCR v1.5 §3.15 verbatim · authority-source language):**

> **§3.15 Recommendation module — Opportunity Briefs (UI Spec v2.2 §3.7)**
>
> OB-R1 — A recommendation service consuming the Registry read API and producing opportunity briefs: census-slice selection, product-shape proposal with real-world precedent, gap statement. LLM generation behind the Shield, standard routing. Salvage input: reasoning patterns lifted from Akki-Executive-Core (github.com/bramuel-syni/Akki-Executive-Core) as reference logic — lifted, not imported; no runtime dependency on any Akki system.
>
> OB-R2 — Grounding integrity: every quantitative value in a brief is a Registry read passed through verbatim. The generation layer receives facts as structured input and may not emit numbers absent from that input. **Tier-1** — the no-fabricated-values promise applied to advisory output.
>
> OB-R3 — Class honesty: every brief carries the advisory marker with no render path that omits it; briefs are excluded from trace/receipt resolution; no brief content enters any governed response. **Tier-1**.
>
> OB-R4 — Hand-off: "Shape as objective" pre-fills the commission wizard reach from the brief's census slice(s); the wizard proceeds under its normal rules (mandatory fields asked, never pre-filled from the brief).
>
> OB-R5 — Refresh: regeneration on census change; briefs stamped with generation date + census ref; stale briefs marked, retained.
>
> OB-R6 — Scope coverage: the generation pass produces briefs at all three scopes — slice, combined (multi-slice intersection/join), estate-level — each scope-chipped. Grounding integrity (OB-R2) applies per contributing slice: a Combined brief's numbers trace to the Registry reads of each named slice; no derived or blended figure may appear unless it is itself a Registry-computable aggregate rendered verbatim. **Tier-1 (grounding clause)**.
>
> Gates: OB-G1 test_brief_numbers_are_registry_reads_verbatim · OB-G2 test_advisory_marker_present_on_every_brief_render · OB-G3 test_brief_excluded_from_trace_resolution · OB-G4 test_shape_as_objective_prefills_reach_only · OB-G5 test_combined_brief_numbers_trace_to_each_contributing_slice.
>
> Placement: post-Phase-9 — requires a populated Registry. Enters the queue after Phase 9 Stage B, before production housing. Fixture-census demo permitted earlier, marked per AS-U2 sample rules. Tier-1: OB-R2, OB-R3, OB-R6's grounding clause; all else Tier-3 defaults.

---

## §2. Scope + design

### §2.1 What lands (execution scope · informs Stage A gate roster)

**New (backend source):**

- `services/opportunity_briefs/` (new package · matches Service-N convention) containing:
  - `generator.py` — orchestrator: pulls Registry reads via `services/mtafiti/registry.py` read surface; produces per-scope structured facts; hands structured facts to Shield-side brief_synthesizer; wraps LLM output with grounding-integrity gate; stamps date + census_ref + advisory marker; returns `OpportunityBrief_v0` sidecar shape (frozen contract untouched · brief lives in its own registry table + read API).
  - `brief_registry.py` — Registry writer/reader for briefs (write-once + refresh-on-census-change semantics per OB-R5); regeneration marks stale briefs `stale=True` but preserves retention.
  - `census_slice_selector.py` — mechanical selector consuming census dimensions (`census_dimensions.v1.json` from CD close) + salvage-lifted reasoning patterns to propose slice combinations at three scopes.
  - `product_shape_proposer.py` — reasoning module lifting Akki-Executive-Core proposal patterns (lifted, not imported); consumes Registry-read facts + census-slice selection → emits structured brief candidates for Shield-side LLM synthesis.
  - `shape_as_objective_prefill.py` — OB-R4 hand-off: reach pre-fill only (mandatory-field masking preserved · wizard's own rules govern).
- `services/synisense/shield/brief_synthesizer.py` — Shield-side LLM boundary (mirrors `fluency_synthesizer.py` from AF · Sonnet via `llm_router::_provider_for("analytical")` reuse · Phase 7 Stage B-2 seed · 30s timeout). Enforces structured output `{brief_text, quantitative_anchors: [{value, registry_read_ref}], scope, contributing_slices: [...]}`.
- `services/synisense/shield/brief_prompt.v0.txt` — Shield-side prompt template (data-blind per §8 · content-neutral placeholders per Fixture Refresh precedent · no broadcaster/regional/genre priors).
- `services/opportunity_briefs/brief_grounding.py` — grounding-integrity gate (OB-R2 · OB-R6 grounding clause): every quantitative value in `brief_text` MUST have a `registry_read_ref` in `quantitative_anchors`; every anchor's `value` MUST appear byte-verbatim in the referenced Registry read (mechanical byte-substring check · **no semantic scoring** — matches AF-E1 β Owner Condition 1 discipline). Combined-scope briefs: every anchor's `registry_read_ref` MUST cite ONE of the brief's contributing slices; blended/derived numbers permitted iff Registry-computable aggregate rendered verbatim (OB-R6 verbatim).
- `services/opportunity_briefs/advisory_marker.py` — render-time marker attachment (OB-R3 · Tier-1). Every brief render path MUST include the advisory marker; separate render-time gate ensures no render path omits it. Governed-response exclusion: brief content NEVER enters any `ComposedConclusion_v0` `answer_text` synthesis (grep-negative attest on service-tier boundary).
- **Sidecar telemetry** at `services/opportunity_briefs/brief_telemetry.py` (mirrors `fluency_mode_telemetry.py` + `execution_mode_telemetry.py` precedent): scope + `_regeneration_reason` (`census_change` | `initial` | `on_demand`) + `_stale_flag` + `_advisory_marker_attached`. Frozen contracts UNTOUCHED · **parity 31 preserved**.

**New (frontend surface — UI Spec v2.2 §3.7):**

- Three-scope render card component (slice · combined · estate scope chips per OB-R6) with advisory marker mandatory-visible per OB-G2.
- "Shape as objective" button pre-fills wizard reach from brief's contributing slices; wizard mandatory-field flow untouched.
- Stale-brief visual indicator (OB-R5 · retained + marked).

**Test cells:** OB-G1..OB-G5 gate roster per §5 below.

### §2.2 What is preserved byte-identical (Tier-1 non-negotiable)

- **All 31 frozen contracts** — untouched. Parity stays at 31 (attested at OB-G attest cell).
- **4-code auth-refusal registry** — untouched.
- **Refusal taxonomy** — untouched. Briefs are ADVISORY output; NEVER enter a refusal envelope; brief-generation failure = infra fault path (per Shield-standard 503 or graceful stale-brief marking).
- **`ComposedConclusion_v0`** — untouched (OB-R3: brief content NEVER enters governed response).
- **Trace/receipt resolution** — briefs EXCLUDED per OB-R3 (a receipt trace_id never resolves to brief content; attested at OB-G3).
- **Historical close reports** — Standing Rule v3 preserved.

### §2.3 Seam layout (execution guidance)

```
[census surface]        census_dimensions.v1.json (CD close · governance §8 data-blind)
    │
    ▼
[selector]              opportunity_briefs/census_slice_selector.py
    │                     ├─ enumerates slice / combined / estate scope candidates
    │                     └─ salvage-lifted reasoning per OB-R1 (Akki pattern)
    │
    ▼
[reader]                mtafiti/registry.py read surface
    │                     └─ Registry reads per scope · structured facts assembled
    │
    ▼
[proposer]              opportunity_briefs/product_shape_proposer.py
    │                     └─ candidate brief shape + gap statement
    │
    ▼
[Shield]                synisense/shield/brief_synthesizer.py
    │                     ├─ structured-output prompt (data-blind · brief_prompt.v0.txt)
    │                     ├─ Sonnet via llm_router::analytical (Phase 7 Stage B-2 reuse)
    │                     ├─ 30s timeout · runtime transient → stale-brief graceful marking
    │                     └─ emits {brief_text, quantitative_anchors, scope, contributing_slices}
    │
    ▼
[grounding gate]        opportunity_briefs/brief_grounding.py
    │                     ├─ (A) every value in quantitative_anchors byte-verbatim in referenced Registry read
    │                     ├─ (B) every numeric appearing in brief_text has a corresponding anchor
    │                     ├─ (C) combined-scope: anchors trace per contributing_slice (OB-R6 verbatim)
    │                     └─ FAIL → brief NOT emitted; regeneration tagged reason=grounding_reject
    │
    ▼
[registry write]        opportunity_briefs/brief_registry.py
                          ├─ write-once per (scope, contributing_slices, census_ref) tuple
                          ├─ regeneration on census change (OB-R5): mark stale=True, retain
                          └─ advisory_marker attached at write time
    │
    ▼
[frontend]              UI Spec v2.2 §3.7 render card
                          ├─ scope chip (slice · combined · estate)
                          ├─ advisory marker mandatory-visible (OB-G2)
                          ├─ "Shape as objective" button (OB-R4 · reach pre-fill only)
                          └─ stale indicator (OB-R5)
```

### §2.4 Data-blind posture (§8) attest

- Brief prompt template MUST NOT encode content-type / broadcaster / regional / genre / dialectal priors about the RMS estate. Prompt phrases are content-neutral shape rules (scope · grounding · anchor discipline). Data-blind reflection attest at OB-G-DB (§6.10 · grep-negative on the prompt template file for the neutralized-broadcaster-alias set + a positive attest that the prompt contains only category-generic language).
- Fixture-census permitted per AS-U2 (Owner 2026-07-08 amendment): estate-spanning EXAMPLES rendered against the synthetic fixture census; the AS-U2 sample rules govern their presentation (advisory marker · synthetic-source indicator).

### §2.5 Estate-spanning examples (mandate scope)

Owner scope anchor: *"estate-spanning examples."* Three worked examples land in the Stage B execution commit — one per scope:

- **Slice-scope example:** brief consuming a single census dimension (e.g., high-defensibility-fact slice).
- **Combined-scope example:** brief consuming ≥2 census dimensions (e.g., intersection of high-defensibility slice AND wire-source-standing slice). OB-R6 grounding clause exercised.
- **Estate-scope example:** brief consuming the full estate census aggregate.

All three examples land against the fixture-census per AS-U2 rules (synthetic-source marked · advisory marker mandatory).

---

## §3. Band derivation — RAW LoC per governance §9

Rate composition per §6.1-6.11 + §6.9 verbatim-carrier overhead + §6.10 AST/reflection.

### §3.1 Backend source

| Item | Rate class | Est. LoC (α) | Est. LoC (β) | Est. LoC (γ) |
|---|---|---:|---:|---:|
| `services/opportunity_briefs/__init__.py` | §6.7 package boilerplate | 15 | 15 | 15 |
| `services/opportunity_briefs/generator.py` | §6.3 orchestrator + §6.9 verbatim carrier (OB-R1..R6 embedded) | 180 | 220 | 140 |
| `services/opportunity_briefs/brief_registry.py` | §6.3 Registry read/write · write-once + refresh semantics | 120 | 150 | 90 |
| `services/opportunity_briefs/census_slice_selector.py` | §6.3 mechanical + salvage-lifted reasoning | 100 | 140 | 80 |
| `services/opportunity_briefs/product_shape_proposer.py` | §6.3 salvage-lifted per OB-R1 (Akki lifted-not-imported) | 120 | 170 | 90 |
| `services/opportunity_briefs/shape_as_objective_prefill.py` | §6.3 hand-off (reach pre-fill only) | 60 | 80 | 40 |
| `services/opportunity_briefs/brief_grounding.py` | §6.3 mechanical byte-substring gate (mirrors AF `answer_grounding.py`) | 140 | 180 | 110 |
| `services/opportunity_briefs/advisory_marker.py` | §6.3 render-time attach + governed-response exclusion attest | 60 | 80 | 40 |
| `services/opportunity_briefs/brief_telemetry.py` | mirrors `fluency_mode_telemetry.py` | 70 | 80 | 60 |
| `services/synisense/shield/brief_synthesizer.py` | §6.3 Shield boundary (mirrors `fluency_synthesizer.py`) + §6.9 carrier | 220 | 250 | 190 |
| `services/synisense/shield/brief_prompt.v0.txt` | prompt template config | 50 | 70 | 35 |
| **Backend source subtotal** | | **1,135** | **1,435** | **890** |

### §3.2 Backend tests

| Gate | Cell class | Cells | Rate | LoC |
|---|---|---:|---:|---:|
| **OB-G1** test_brief_numbers_are_registry_reads_verbatim | §6.1 classic × 3 (three scopes) | 3 | 12 | 36 |
| **OB-G2** test_advisory_marker_present_on_every_brief_render | §6.1 classic + §6.10 reflection walk | 2 | 26 | 52 |
| **OB-G3** test_brief_excluded_from_trace_resolution | §6.11 async httpx (E2E trace surface) | 2 | 25 | 50 |
| **OB-G4** test_shape_as_objective_prefills_reach_only | §6.1 classic (wizard-flow parametrised) | 2 | 12 | 24 |
| **OB-G5** test_combined_brief_numbers_trace_to_each_contributing_slice | §6.1 classic (multi-slice + combined) | 3 | 12 | 36 |
| **OB-G-DB** test_brief_prompt_template_data_blind_no_residues (§8) | §6.10 grep-negative | 1 | 40 | 40 |
| **OB-G-Parity** test_parity_31_preserved_at_ob_landing | §6.1 classic | 1 | 12 | 12 |
| **OB-G-Refresh** test_stale_marking_on_census_change | §6.1 classic (OB-R5) | 2 | 12 | 24 |
| **OB-G-Grounding-Fail** test_grounding_fail_prevents_brief_write (OB-R2 fail path) | §6.1 classic | 2 | 12 | 24 |
| **Backend tests subtotal** | | **18** | | **298** |

### §3.3 Frontend tests

Frontend surface per UI Spec v2.2 §3.7 (three-scope render card + advisory marker + shape-as-objective button + stale indicator):

| Cell | Framework | LoC |
|---|---|---:|
| brief render card (Jest · component + advisory marker DOM presence) | Jest | 40 |
| shape-as-objective hand-off (Playwright chromium E2E · wizard reach pre-fill) | Playwright | 45 |
| stale-brief indicator (Jest) | Jest | 25 |
| scope-chip rendering (Jest, 3-scope parametrised) | Jest | 30 |
| **Frontend subtotal** | | **140** |

### §3.4 Frozen contract accounting

- **Envelope untouched:** no §6.6 class LoC charged.
- **No new snapshot:** no §6.7 snapshot LoC charged.
- Parity stays at **31**.

If any escalation ruling opens a Tier-1 contract-touch door: separately budgeted at ~+215 LoC (60 class body + 155 snapshot per §6.6 + §6.7 precedent). Proactive design goal: **zero Tier-1 contract-touches** — briefs land via new-registry-table pattern (matches Northena Ledger sidecar precedent).

### §3.5 Band composition

Total per scenario:

| Scenario | Backend source | Backend tests | Frontend | Total raw LoC |
|---|---:|---:|---:|---:|
| **α** (salvage-lifted-heavy · builder-recommended · Akki reasoning patterns landed as substantive modules) | 1,135 | 298 | 140 | **1,573** |
| **β** (verbose · verbatim carriers on every module) | 1,435 | 298 | 140 | **1,873** |
| **γ** (minimal · MVP briefs with tight salvage subset) | 890 | 298 | 140 | **1,328** |

**Proposed band (raw LoC per §9):** `[1,300, 1,900]` — brackets all three scenarios with headroom.

Band-relative trichotomy per §9 (Owner correction 2026-07-10):
- below-bottom (< 1,300) — disclose driver per Tier-2 discipline
- in-band ([1,300, 1,900]) — no disclosure beyond snapshot line
- above-top (> 1,900) — disclose driver per Tier-2 discipline

### §3.6 §4.2 threshold statement (Tier-2 disclosure · never blocking per §12.1)

- **Raw LoC threshold:** 1,500. Point-estimate: α = 1,573 · β = 1,873 · γ = 1,328. **§4.2 raw threshold projected-CROSSED under scenarios α and β · projected-under threshold under γ.**
- **Cell count threshold:** 60. Estimate: 18 backend cells + 4 frontend cells = **22**. Well under.
- **Disposition anticipated: split-at-natural-seam per §4.2 pre-authorised** — dev's judgment at execution per governance §2.2 (no round-trip). Split fallback pre-registered at the natural seam:
  - **Split-A:** `opportunity_briefs/` package + Registry surface + selector + proposer + grounding + telemetry + backend tests OB-G1/G5/G-Refresh/G-Grounding-Fail. The "generator + grounding + Registry" unit.
  - **Split-B:** Shield-side brief_synthesizer + prompt template + advisory_marker + shape_as_objective_prefill + backend tests OB-G2/G3/G4/G-DB/G-Parity + all frontend tests. The "Shield boundary + surface + hand-off" unit.
- **Atomic attempted first per §4.1 baseline; autonomous split fallback fires if cumulative diff ≥ 1,500 raw LoC OR ≥ 60 cells mid-execution**, per the Fixture-Refresh precedent.

Per governance §12.1 (Owner 2026-07-10): §4.2 thresholds and band disclosures are Tier-2, disclosure-only, never blocking.

---

## §4. Data-blind + honesty-grammar posture attest

- Governance §8: prompt template `services/synisense/shield/brief_prompt.v0.txt` MUST contain no broadcaster/regional/dialectal/genre residues. Attested at OB-G-DB.
- Governance §9: band derived + verdict rendered in RAW LoC (band-relative trichotomy per Owner correction 2026-07-10). LLoC + cell-density are disclosure lines only.
- Governance §10: Opportunity Briefs dispatch-independent from 9.2a/9.2b. Fixture-census permitted per AS-U2; real-registry operation gates on 9.2b (owner-side per §11) but Stage B lands against fixture-census for demo-scope.
- Governance §11: N/A (compute-to-data topology does not affect briefs; briefs are control-plane).
- Governance §12: this Stage A adheres — Tier-1 surfaces enumerated pre-execution; no conditional ratifications; band/thresholds Tier-2 disclosure only.
- Standing Rule v3: this Stage A is on-disk canonical; reply body SHA + tier tags + escalation matrix only.

---

## §5. Gate roster (OB-G1..OB-G5 mandate + OB-G-DB / -Parity / -Refresh / -Grounding-Fail auxiliary)

**Mandate gates (5 · from BCR v1.5 §3.15 verbatim):**

| Gate | Tier | Cell class | Purpose |
|---|---|---|---|
| **OB-G1** `test_brief_numbers_are_registry_reads_verbatim` | **Tier-1 (OB-R2 grounding)** | §6.1 × 3 | Every quantitative value in `brief_text` appears byte-verbatim in the referenced Registry read; no semantic scoring. Applied per scope (slice/combined/estate). |
| **OB-G2** `test_advisory_marker_present_on_every_brief_render` | **Tier-1 (OB-R3 class honesty)** | §6.1 + §6.10 reflection | Every render path emits the advisory marker; §6.10 reflection walk confirms no render path can strip it. |
| **OB-G3** `test_brief_excluded_from_trace_resolution` | **Tier-1 (OB-R3 class honesty)** | §6.11 async httpx | E2E: trace_id resolution returns 404/NOT_FOUND for a brief-scoped id; brief content NEVER surfaces via trace/receipt. |
| **OB-G4** `test_shape_as_objective_prefills_reach_only` | Tier-3 (OB-R4 hand-off discipline) | §6.1 × 2 | Wizard receives reach pre-fill only; mandatory fields NOT pre-filled from brief. |
| **OB-G5** `test_combined_brief_numbers_trace_to_each_contributing_slice` | **Tier-1 (OB-R6 grounding clause)** | §6.1 × 3 | Combined-scope brief anchors trace to each named contributing_slice; blended/derived numbers permitted iff Registry-computable aggregate rendered verbatim. |

**Auxiliary gates (4 · derived from §3.15 supporting rules):**

| Gate | Tier | Cell class | Purpose |
|---|---|---|---|
| **OB-G-DB** `test_brief_prompt_template_data_blind_no_residues` | Tier-1 (§8 data-blind) | §6.10 grep-negative | Prompt template contains no broadcaster/regional/genre/dialectal residues. |
| **OB-G-Parity** `test_parity_31_preserved_at_ob_landing` | Tier-1 (frozen contracts) | §6.1 | 31 frozen contracts + 31 snapshots byte-identical. |
| **OB-G-Refresh** `test_stale_marking_on_census_change` | Tier-3 (OB-R5 refresh) | §6.1 × 2 | Regeneration on census change; stale marks set; retained-not-deleted. |
| **OB-G-Grounding-Fail** `test_grounding_fail_prevents_brief_write` | Tier-1 (OB-R2 fail path) | §6.1 × 2 | Grounding gate REJECT → brief NOT written to Registry; regeneration tagged reason=grounding_reject. |

**Total: 9 named gate families · 22 cells · 298 raw LoC backend + 140 raw LoC frontend.**

---

## §6. Escalation matrix — PRE-TIERED

Per Owner 2026-07-10 dispatch (verbatim): *"Tier-1 surfaces are already named in the mandate — OB-R2 grounding integrity, OB-R3 class honesty, OB-R6 per-slice grounding — expect escalations there and nowhere else."*

### §6.1 Tier-1 escalations (verbatim relay to Owner · **exactly 3 · exactly the surfaces Owner named**)

**OB-E1 · OB-R2 grounding-integrity mechanism (Tier-1)**

> Owner authority-source language (BCR v1.5 §3.15 verbatim): *"Grounding integrity: every quantitative value in a brief is a Registry read passed through verbatim. The generation layer receives facts as structured input and may not emit numbers absent from that input. Tier-1 — the no-fabricated-values promise applied to advisory output."*
>
> **Promise protected:** the no-fabricated-values honesty promise applied to ADVISORY output (client-facing) — briefs cannot manufacture numbers.
>
> **Escalation:** the mandate is directive but the mechanic requires Owner selection.
>
> **Options (pre-authorised menu):**
> - **α · Structured anchor + byte-verbatim substring check (mirrors AF-E1 β + Owner Condition 1 precedent · builder-recommended).** LLM emits `{brief_text, quantitative_anchors: [{value, registry_read_ref}]}` structured output; grounding gate at `brief_grounding.py` verifies every `value` appears byte-verbatim in the referenced Registry read text; every numeric appearing in `brief_text` has a corresponding anchor; **no semantic scoring**. Mechanical byte-substring check per numeral (regex `[0-9]+(?:[.,][0-9]+)*%?`) matches AF-E1 β Owner Condition 1 verbatim (*"mechanical check, no semantic scoring"*). On any failure → brief NOT emitted (regeneration tagged `grounding_reject`); the gate NEVER patches the brief. This is the AF-honesty-grammar posture ported to advisory output — same discipline, same rate-class §6.1, no new precedent required.
> - **β · Per-numeral anchor with token-level Registry-cursor evidence** — for each numeric, the anchor MUST carry a Registry-cursor evidence tuple `(record_id, field_path, source_offset, source_length)`. Test cell verifies the Registry read at that cursor equals the numeric byte-for-byte. Strictest — catches "correct numeric quoted from wrong Registry read" (a self-declaration gap α does not close). Adds ~40 LoC + one distinct test cell.
> - **γ · Verbatim-quote-only briefs** — brief prose restricted to verbatim substrings of Registry reads with mechanical ligature only. Most conservative; sacrifices brief fluency; may not match the "product-shape proposal with real-world precedent" spirit of OB-R1 (proposals require some narrative synthesis around the Registry-anchored numbers).
>
> **Builder-recommendation: α.** Owner's Condition 1 precedent for AF-E1 β (*"mechanical check, no semantic scoring"*) is the identical grammar; briefs inherit the same rate + gate class + failure path. α closes the client-facing no-fabricated-values promise mechanically; β adds provenance-level protection at moderate cost (worth surfacing to Owner); γ underdelivers.
>
> **Class:** Tier-1 (client-promise · no-fabricated-values honesty grammar applied to advisory output · OB-R2 verbatim).
> **Ruling required BEFORE execution.**

**OB-E2 · OB-R3 class-honesty mechanism (Tier-1)**

> Owner authority-source language (BCR v1.5 §3.15 verbatim): *"Class honesty: every brief carries the advisory marker with no render path that omits it; briefs are excluded from trace/receipt resolution; no brief content enters any governed response. Tier-1."*
>
> **Promise protected:** briefs are ADVISORY, NEVER governed. No render path can strip the advisory marker; no trace/receipt resolution surfaces brief content; no `ComposedConclusion_v0` `answer_text` synthesis touches brief content. Class-honesty at the presentation + governed-response boundary.
>
> **Escalation:** three distinct enforcement seams; Owner selection required on the enforcement mechanic per seam.
>
> **Options (per seam):**
>
> **Seam-1 · Advisory marker on every render path:**
> - **α · Render-time attach via `advisory_marker.attach(brief)` invariant (builder-recommended).** The Registry write-path attaches the marker at write time; the frontend render component reads the marker from the sidecar payload; §6.10 reflection walk (OB-G2 sub-cell) confirms no frontend render code path can strip or hide the marker. Two protection layers: write-time attach + render-time reflection.
> - **β · Contract-embed the marker in the brief-registry sidecar shape (`OpportunityBrief_v0::advisory=True` frozen).** Contract-touch → parity 31 → 32 if landed. Tier-1 contract-touch door opened; not proactively taken. Deferred as future-additive path.
>
> **Seam-2 · Brief exclusion from trace/receipt resolution:**
> - **α · Route-level exclusion (builder-recommended).** `/trace/{id}` route explicitly REJECTS brief-scoped ids with 404; OB-G3 E2E cell attests. Brief ids live in their own id namespace (`brief_id` distinct from `unit_id`/`trace_id`/`run_id` prefixed pseudonyms).
> - **β · Namespace-prefix reflection walk** — all id-issuing sites reflect namespace prefixes to guarantee no collision. Adds ~40 LoC §6.10 reflection cell.
>
> **Seam-3 · Brief content excluded from governed response:**
> - **α · §6.10 reflection walk (builder-recommended)** — grep-negative on `services/service_1/**` for any import of `services/opportunity_briefs/**` (brief content boundary). Direct AST/reflection attest that no `ComposedConclusion_v0` `answer_text` synthesis path can consume brief content.
> - **β · Runtime enforcement via context-vars** — every governed-response synthesis carries a context-var flag; brief-registry read paths refuse to serve if the flag is set. Adds runtime overhead + additional test cells.
>
> **Builder-recommendation:** α across all three seams (Seam-1 α · Seam-2 α · Seam-3 α). Mechanical + reflection + route-level — no new precedent needed; matches AS-G6 / TF-G9 / FR-G4 §6.10 reflection-gate class established across prior mini-phases.
>
> **Class:** Tier-1 (class-honesty on the presentation + governed-response boundary · OB-R3 verbatim).
> **Ruling required BEFORE execution** — Owner names Seam-1/Seam-2/Seam-3 enforcement individually or blesses α across all three.

**OB-E3 · OB-R6 per-slice grounding clause (Tier-1)**

> Owner authority-source language (BCR v1.5 §3.15 verbatim): *"Scope coverage: the generation pass produces briefs at all three scopes — slice, combined (multi-slice intersection/join), estate-level — each scope-chipped. Grounding integrity (OB-R2) applies per contributing slice: a Combined brief's numbers trace to the Registry reads of each named slice; no derived or blended figure may appear unless it is itself a Registry-computable aggregate rendered verbatim."*
>
> **Promise protected:** in a Combined brief, every quantitative anchor must trace to a NAMED contributing_slice's Registry read (not to an implicit "combined" pseudo-read); blended/derived figures are permitted only if they are Registry-computable aggregates rendered verbatim (i.e., the Registry itself emits the aggregate, and the brief quotes it verbatim — no in-Shield-synthesis-time computation).
>
> **Escalation:** the "Registry-computable aggregate rendered verbatim" clause requires Owner definition of the aggregate set.
>
> **Options (pre-authorised menu):**
> - **α · Registry-computable aggregate = a numeric field that the Registry read API returns natively (builder-recommended).** Definition: the aggregate MUST be a field the Registry read surface (`services/mtafiti/registry.py`) exposes as its own read — e.g., `count_of_units_in_slice(slice_id) → int` is a Registry-computable aggregate iff the Registry read API has that method. The brief quotes the returned value byte-verbatim. In-Shield or in-generator computation of aggregates is FORBIDDEN (no `sum(...)` / `avg(...)` at synthesis time; only Registry-exposed aggregates).
> - **β · Registry-computable aggregate = any value derivable from Registry reads via a whitelisted operator set** (SUM, COUNT, AVG, MIN, MAX). The brief_grounding gate replays the operator against the Registry reads and verifies the emitted value byte-verbatim. Adds substantial gate LoC + operator whitelist maintenance.
> - **γ · No aggregates permitted** — every numeric MUST be a direct Registry read from a single slice. Combined briefs may render multiple direct reads side-by-side but never a computed aggregate.
>
> **Builder-recommendation: α.** Owner's "Registry-computable aggregate rendered verbatim" language reads most naturally as α — the aggregate IS Registry-computable when the Registry itself computes it. β pushes computation to synthesis-time (grounding-adjacent risk); γ underdelivers on OB-R6's "combined-scope" scope-chip semantic (a Combined brief with no aggregates is barely different from two Slice briefs side-by-side).
>
> **Class:** Tier-1 (OB-R6 grounding clause · Owner explicitly named).
> **Ruling required BEFORE execution.**

### §6.2 Tier-2 disclosures (cost/rework · no round-trip · lines in close report)

- **T2-D1:** proposed raw-LoC band `[1,300, 1,900]` per §3 rate ledger + §9 raw-LoC verdict. Band-relative trichotomy per Owner §9 correction.
- **T2-D2:** §4.2 thresholds stated. Raw threshold **1,500 projected-CROSSED under scenarios α and β** (below α, in-band γ). Cell count 22 << 60. Autonomous split-fallback pre-authorised at natural seam per §3.6 (per governance §12.1: §4.2 disclosures are never blocking · Tier-2 disclosure-only).
- **T2-D3:** cell-count estimate 18 backend + 4 frontend = 22 cells; density mix 12/25/26/40 LoC/cell (§6.1 × 12 + §6.10 × 6 + §6.11 × 2 + frontend × 4).
- **T2-D4:** verbatim-carrier overhead (§6.9) counted at ~100 LoC in `generator.py` + 100 LoC in `brief_synthesizer.py` (OB-R1..R6 embedded per Standing Rule v3 posture).
- **T2-D5:** salvage-lifted reasoning per OB-R1 (Akki-Executive-Core patterns lifted-not-imported) budgets ~120-170 LoC (α/β) in `product_shape_proposer.py` — this is the biggest α/β delta.
- **T2-D6:** snapshot in-band verdict rendered post-execution against raw `wc -l`; LLoC + cell density disclosure-only per Owner §9 ruling.
- **T2-D7:** frontend surface per UI Spec v2.2 §3.7 lands 4 test cells + Jest/Playwright coverage; frontend regression parity maintained (137/137 Jest + 44/44 Playwright baseline).

### §6.3 Tier-3 defaults (silent · one-line notes in close report)

Per Owner 2026-07-10 dispatch: *"escalations there and nowhere else"* + BCR v1.5 §3.15: *"all else Tier-3 defaults."*

- **[Tier 3 default]** module names: `services/opportunity_briefs/{generator,brief_registry,census_slice_selector,product_shape_proposer,shape_as_objective_prefill,brief_grounding,advisory_marker,brief_telemetry}.py` · `services/synisense/shield/brief_synthesizer.py`.
- **[Tier 3 default]** prompt template file: `services/synisense/shield/brief_prompt.v0.txt` (matches `fluency_prompt.v0.txt` naming convention).
- **[Tier 3 default]** LLM model: **Sonnet via Emergent LLM key** already inside Shield at `llm_router::_provider_for("analytical")` (Phase 7 Stage B-2 seed · AF precedent 2026-07-10 reuse). NO new integration; no `integration_playbook_expert_v2` call needed.
- **[Tier 3 default]** Shield timeout: 30s (matches AF-E2 amended Owner-affirmed default).
- **[Tier 3 default]** structured-output field names: `{brief_text, quantitative_anchors: [{value, registry_read_ref}], scope, contributing_slices: [...]}`.
- **[Tier 3 default]** brief-registry table shape: `OpportunityBriefRow` sidecar (NOT a frozen contract · lives in the brief_registry read/write layer only · matches Northena Ledger sidecar precedent).
- **[Tier 3 default]** advisory-marker string: `"Advisory: opportunity brief — not a governed response."` (data-blind wording; no estate references).
- **[Tier 3 default]** brief id namespace prefix: `brief-` (distinct from `cc-unit-` / `run-` / `trace-` prefixes; enables route-level exclusion at `/trace/{id}` per OB-E2 Seam-2 α).
- **[Tier 3 default]** stale-marking policy: `stale=True` set on regeneration; retention preserved (OB-R5 verbatim).
- **[Tier 3 default]** shape-as-objective pre-fill scope: reach only (contributing_slices → wizard `reach` field); NEVER pre-fills mandatory fields (OB-R4 verbatim).
- **[Tier 3 default]** test file naming: `tests/invariants/test_opportunity_briefs_ob_g1_to_g5.py` (mandate gates) + `test_opportunity_briefs_ob_g_auxiliary.py` (auxiliary gates) — matches AF + Fixture-Refresh convention.
- **[Tier 3 default]** salvage-lift reference path: `docs/salvage/akki_executive_core_reasoning_patterns.md` — a one-file salvage record cataloguing the lifted reasoning patterns (module names + method names + rationale · not code · lifted-not-imported).
- **[Tier 3 default]** frontend component naming: `OpportunityBriefCard`, `AdvisoryMarker`, `ScopeChip`, `ShapeAsObjectiveButton`, `StaleBriefIndicator` — matches existing PascalCase component convention.
- **[Tier 3 default]** rulings + close docs on-disk: `docs/rulings/opportunity_briefs_ob_e1_to_e3.md` + `docs/close_reports/opportunity_briefs.md`.

---

## §7. §DirectionConsistency preview (executable at execution STEP A · per-close section not mandatory per Owner §12 dead-tracker strike)

Owner 2026-07-10 struck the direction-consistency check as a recurring per-close section (verbatim: *"ran once, clean pass, done; it is not a recurring per-close section"*). This Stage A does NOT commit to running a per-close DirectionConsistency section; the check remains available at builder-discretion if a specific direction risk is identified during execution. Not a standing item.

---

## §8. Standing constraints preserved at close (attested pre-execution)

| Constraint | Attest at execution |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | GREEN — no contract touch; OB-G-Parity attests. |
| 4-code auth-refusal registry closed | GREEN — briefs not an auth surface. |
| No HTTP 409 in new/modified files (E5) | GREEN — advisory pattern; no 409 boundary. |
| Standing Rule v3 (on-disk canonical) | GREEN — Stage A on-disk here; close lands separately. |
| AS-H1 retention held-class (no direct DELETE) | GREEN — OB-R5 preserves stale briefs; no DELETE handlers. |
| Governance §8 data-blind posture | GREEN — OB-G-DB attests prompt template. |
| Governance §9 metric-verdict-in-derivation-unit | GREEN — band + verdict in raw LoC. |
| Governance §10 9.2 split ruling | GREEN — briefs dispatch-independent from 9.2a/9.2b. |
| Governance §11 9.2-OWN resolution | N/A (briefs are control-plane). |
| Governance §12 close-ratification discipline | GREEN — this Stage A adheres; conditions attach at ruling time per §12. |
| FR-G4 no-shadow-source AST posture | GREEN — brief anchors reference `registry_read_ref` (not feed_ids); prompt data-blind. |
| AF-E2 amended boundary set precedent | GREEN — Shield transients degrade to stale-brief marking; no refusal envelope. |
| AF-E3 α sidecar telemetry precedent | GREEN — brief_telemetry mirrors pattern. |
| AS-U2 sample rules (fixture-census demo permitted) | GREEN — estate-spanning examples marked per AS-U2. |
| OB-R1 salvage-lifted-not-imported | GREEN — Akki-Executive-Core lifted at design time; no runtime dependency; salvage record at `docs/salvage/akki_executive_core_reasoning_patterns.md`. |

---

## §9. Provenance + sequence forward

- **Stage A (this file):** `/app/docs/stage_a_proposals/opportunity_briefs.md`
- **Rulings record (post-Owner-ruling):** `/app/docs/rulings/opportunity_briefs_ob_e1_to_e3.md`
- **Close report (post-execution):** `/app/docs/close_reports/opportunity_briefs.md`
- **Salvage record (per OB-R1 · not code):** `/app/docs/salvage/akki_executive_core_reasoning_patterns.md`
- **Sequence after:** production housing (§3.4 · PH-R1 packaging builder-side dispatchable · no [OWNER] binding gates the builder-side half per Owner 2026-07-10) → mandate-complete gate. 9.2b remains owner-side per §11.

═══════════════════════════════════════════════════════════════════

*End of §3.15 Opportunity Briefs Stage A proposal. Standing Rule v3: on-disk canonical. Awaiting Owner rulings on Tier-1 escalations OB-E1..OB-E3 (verbatim relay). Per governance §12 (2026-07-10): band/threshold disclosures are Tier-2, disclosure-only, never blocking; Tier-1 escalations return via verbatim relay before execution.*
