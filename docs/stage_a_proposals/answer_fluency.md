# §3.8 Answer Fluency — Stage A Proposal

**Dispatch:** Owner ruling post-Fixture-Refresh ratification (2026-07-10).
**Basis:** BCR v1.4 §5.1 line 336 (STILL_QUEUED · rides existing envelopes and gates); Owner scope anchors 2026-07-10.
**Governance:** 3-tier ruling model per `/app/docs/governance/tiered_ruling_model.md`. Metric-verdict in raw LoC per §9. Data-blind posture §8.
**Standing Rule v3:** on-disk canonical. This file is the persistent Stage A record.
**Precedent:** Rides existing envelopes (`ComposedConclusion_v0` #18) + existing gates (Shield chokepoint · Sonnet 4.6 model already lives inside Shield at `services/synisense/shield/llm_router.py` per Phase 7 Stage B-2).

---

## §1. Owner dispatch — verbatim carrier

> **Dispatch: §3.8 Answer Fluency Stage A. Scope anchors:**
> LLM synthesis of answer_text behind the Shield; frozen ComposedConclusion envelope untouched — any contract contact is Tier-1.
> Every sentence derived from load-bearing units; invented connectives or unsupported synthesis fail the gate — no-fabricated-values applied to prose.
> Mechanical composition retained as regression baseline; fluency is an upgrade path, not a replacement.
> LLM unavailability surfaces as infra fault (503), never refusal — refusal taxonomy stays closed.
> Escalations pre-tiered; matrix with all codified rates (§6.7–§6.11); band in raw LoC per §9; §4.2 thresholds stated.
> Sequence after: Opportunity Briefs (§3.15, fixture-census per AS-U2) → production housing (§3.4). 9.2b stays gated on 9.2-OWN-1..3, owner-side.
> Hard constraints unchanged: Stage A only — no code, no execution, no self-dispatch. Tier-1 escalations return via verbatim relay; Tier-2/3 as scoped.

**Ratification carrier for immediate parent** (verbatim): *"Fixture Refresh close: RATIFIED. All three rulings with conditions honored — shadow tables deleted with FR-G4 proving it, transform-golden re-blessed, historical closes preserved byte-identical, five_rings@v0 conformance green post-regen. Direction-consistency check: clean pass accepted; preserving the 5 residues in closed Stage A proposals is correct — records, not live carriers."*

**Metric correction carrier for immediate parent** (verbatim · record-only): *"Metric correction, record only, no action: 782 raw vs [1,200, 1,800] is a below-bottom miss, −35% vs band bottom (in_band=no) — per §9 the verdict is band-relative, not mid-relative. Miss accepted as disclosed; drivers credible."*

Effect on THIS Stage A: band verdicts stated as band-relative (per Owner §9 correction), NOT mid-relative. Below-bottom / above-top / in-band trichotomy.

---

## §2. Scope + design

### §2.1 What lands (this mini-phase — §3.8 execution scope, informing Stage A gate roster)

- **New:** LLM-synthesised prose arm for the `answer_text` field of `ComposedConclusion_v0`. Lives inside the Shield chokepoint at `services/synisense/shield/` (module name: **[Tier-3 default]** `fluency_synthesizer.py` — matches `llm_router.py` + `perception_router.py` co-tenancy pattern). Consumes the load-bearing_unit_ids + their five-rings text + defensibility class + objective_ref; emits fluent prose grounded per-sentence to unit_ids.
- **New:** Grounding-gate service module at `services/service_1/answer_grounding.py` (module name **[Tier-3 default]**) — post-hoc per-sentence anchor verifier. Executes at composed_conclusion package-time BEFORE the envelope leaves Service 1; on grounding-gate FAIL, the code path REJECTS the fluent draft and lands the mechanical baseline (see §2.2). This is a Tier-1 honesty-grammar gate — see AF-E1 for the specific grounding-discipline escalation.
- **New:** Fluency-mode sidecar telemetry at `services/service_1/fluency_mode_telemetry.py` (module name **[Tier-3 default]** · matches `execution_mode_telemetry.py` precedent from 9.2a-E2 α condition 2). Ships `fluency_mode ∈ {mechanical, llm}` + `_fluency_attribution_trace_id` as non-frozen sidecar — ContractEnvelope untouched, honest attribution preserved.
- **Modified (additive-only):** `services/service_1/composed_conclusion.py::package_composed_conclusion` — refactored to route `answer_text` synthesis through a dispatcher with two arms (`mechanical` = existing string-concat behaviour · byte-identical to pre-3.8 output for regression parity; `llm` = new Shield-routed fluent path). Owner scope anchor: *"Mechanical composition retained as regression baseline; fluency is an upgrade path, not a replacement."*
- **Modified (additive-only):** dispatch layer's 503-on-LLM-unavailable behaviour codified per Owner scope anchor: *"LLM unavailability surfaces as infra fault (503), never refusal — refusal taxonomy stays closed."* See AF-E2 for the specific 503-behaviour escalation.
- **New tests:** AF-G1..AF-G(N) gate roster per §5 below.

### §2.2 What is preserved byte-identical (Tier-1 non-negotiable)

- **`ComposedConclusion_v0` frozen contract** — schema/wire/snapshot byte-identical. Parity stays at 31. Attest at AF-G4.
- **All 30 other frozen contracts** — untouched at fluency scope.
- **4-code auth-refusal registry** — untouched (fluency is not an auth surface).
- **Refusal taxonomy** — untouched. LLM unavailability = 503 infra fault per Owner scope anchor.
- **Shield chokepoint** — the LLM call MUST route through `services/synisense/shield/` per Standing Rule (chokepoint enforcement at `test_no_direct_llm_calls_outside_shield`). Attest at AF-G6.
- **Mechanical composer** — the pre-3.8 `answer_text` string-concat behaviour remains callable + tested as regression baseline; produces byte-identical output for the same input. Attest at AF-G1.
- **Historical close reports** — Standing Rule v3 preserved.

### §2.3 Seam layout (pre-drafted for the execution commit's guidance)

```
[dispatch]        service_1/dispatch.py → package_composed_conclusion(request)
    │
    ▼
[Service 1]       service_1/composed_conclusion.py::package_composed_conclusion
    │             ├─ (existing) build load_bearing_unit_ids + computed_class
    │             ├─ (existing) NorthenaLedgerRow_v1 emit + stamp_audit
    │             └─ (new) answer_text = _synthesise_answer_text(
    │                        load_bearing_unit_ids, computed_class, mode="llm"|"mechanical")
    │
    ▼
[dispatcher]      _synthesise_answer_text(...)
    │             ├─ mode=="mechanical" → mechanical composer (pre-3.8 · byte-identical)
    │             └─ mode=="llm"        → Shield fluency arm (below)
    │                    │
    │                    ├─ [503] → infrastructure fault (raises ShieldUnavailable)
    │                    │           dispatch layer surfaces as 503 to caller
    │                    │           NEVER routes to refusal taxonomy
    │                    │
    │                    └─ [200] → fluent_prose + per_sentence_anchors[]
    │                              │
    │                              ▼
    │                         [grounding gate]
    │                         answer_grounding.verify_anchors(prose, anchors,
    │                                                        load_bearing_unit_ids)
    │                              │
    │                              ├─ [FAIL] → drop fluent draft;
    │                              │            fall through to mechanical arm
    │                              │            (fluency_mode telemetry: "mechanical")
    │                              │
    │                              └─ [PASS] → fluent prose returned as answer_text
    │                                          (fluency_mode telemetry: "llm")
    ▼
[Shield]         synisense/shield/fluency_synthesizer.py
                  ├─ builds prompt from load-bearing units + class + objective
                  ├─ calls Emergent LLM key (Claude Sonnet 4.6 already inside Shield
                  │  per Phase 7 Stage B-2 · reuse llm_router.py Sonnet backend)
                  ├─ enforces structured output: {prose, per_sentence_anchors:
                  │   [{sentence_text, unit_ids: [...]}]}
                  └─ Shield-standard de-id + trust-receipt discipline preserved
```

Load-bearing composition rule: mechanical composer remains the FALLBACK when grounding-gate rejects the fluent draft (this is NOT a "fallback = refusal" pattern — it's a quality-gate reject, tracked in fluency_mode telemetry as `mechanical` with a `_grounding_reject_reason` sidecar field). LLM-unavailability at the Shield boundary (503, timeout, model down) surfaces as 503 to the caller — see AF-E2.

### §2.4 Data-blind posture (governance §8) attest

- Fluency prompt template MUST NOT encode content-type assumptions about the RMS estate (no "broadcast news", no genre defaults, no regional priors). Prompt is content-neutral; consumes only the unit texts + class + objective at runtime. Attest at AF-G8 (grep-negative on the prompt template file for the neutralised-broadcaster-alias set + a positive attest that the prompt contains only category-generic language).

---

## §3. Band derivation — RAW LoC per governance §9

Rate composition per §6.1-6.11 + §6.9 verbatim-carrier overhead + §6.10 AST/reflection gate class.

### §3.1 Backend source

| Item | Rate class | Est. LoC (α) | Est. LoC (β) | Est. LoC (γ) |
|---|---|---:|---:|---:|
| `services/synisense/shield/fluency_synthesizer.py` (new module) | §6.3 standalone service module (~100) + §6.9 verbatim carrier (Owner scope anchors + no-fabricated-values docstring · ~100) | **200** | 220 | 180 |
| `services/service_1/answer_grounding.py` (new · grounding gate) | §6.3 standalone (~100) — grounding option-specific (post-hoc semantic overlap = light; per-sentence structured anchors = heavy) | **120** | 200 | 60 |
| `services/service_1/fluency_mode_telemetry.py` (new sidecar) | mechanical-mirror of `execution_mode_telemetry.py` (9.2a-E2 α cond 2) | **50** | 50 | 50 |
| `services/service_1/composed_conclusion.py` (modified · additive) | dispatcher arm + mechanical-composer extraction (2 arms · +~60 net) | **70** | 80 | 60 |
| `services/service_1/dispatch.py` (modified · additive) | 503 pass-through for `ShieldUnavailable` | **20** | 25 | 15 |
| Fluency prompt template (`services/synisense/shield/fluency_prompt.v0.txt` or `.json`) | config file · data-blind neutralised prompt · §6.7 approximate | **60** | 80 | 40 |
| **Backend source subtotal** | | **520** | **655** | **405** |

### §3.2 Backend tests

| Gate | Cell class | Cells | Rate | LoC |
|---|---|---:|---:|---:|
| AF-G1 mechanical composer preserved as regression baseline | §6.1 classic Pytest amortised | 2 | 12 | 24 |
| AF-G2 grounding gate — per-sentence anchor discipline (Tier-1 honesty gate) | §6.1 classic | 4 | 12 | 48 |
| AF-G3 LLM unavailability = 503, never refusal | §6.1 classic + §6.11 async httpx auth-overhead (E2E cells) | 2 | 25 | 50 |
| AF-G4 `ComposedConclusion_v0` envelope byte-identical (parity attest) | §6.1 classic | 1 | 12 | 12 |
| AF-G5 fluency mode observable via sidecar (no contract touch) | §6.1 classic | 2 | 12 | 24 |
| AF-G6 Shield chokepoint discipline — LLM call routed through Shield | §6.10 AST/reflection gate (grep-negative on `services/service_1/` for direct-LLM-call surfaces) | 1 | 40 | 40 |
| AF-G7 grounding-gate reject → fluency_mode=mechanical (quality-gate NOT refusal) | §6.1 classic | 2 | 12 | 24 |
| AF-G8 data-blind posture — prompt template contains no broadcaster-alias residues | §6.10 AST/reflection or grep-negative | 1 | 40 | 40 |
| **Backend tests subtotal** | | **15** | | **262** |

### §3.3 Frontend tests

Fluency is a backend-only content upgrade to `answer_text` (which the frontend already renders verbatim via the `AnswerView` component at `services/service_1/answer_grounding.py` consumer surface + the Ask Console). **Zero frontend cells at fluency scope.** Frontend Jest + Playwright regression remains at existing counts.

**One [Tier-3 default] line for frontend:** if fluency-mode observability is desired on the operator surface (e.g., a small badge on the answer card showing "llm" vs "mechanical"), that's a follow-up ride-along, not this scope. Rationale: Owner scope anchors do not name a frontend surface + BCR §5.1 line 336 said "rides existing envelopes and gates" (frontend already renders the envelope's `answer_text` without knowing the composition arm).

### §3.4 Frozen contract accounting

Owner scope anchor: *"frozen ComposedConclusion envelope untouched — any contract contact is Tier-1."*

- **Envelope untouched:** no §6.6 class LoC (~60/class) charged.
- **No new snapshot:** no §6.7 snapshot LoC (~155/snapshot) charged.
- Parity stays at **31**.

### §3.5 Band composition

Total estimate per scenario:

| Scenario | Backend source | Backend tests | Total raw LoC |
|---|---:|---:|---:|
| **α** (post-hoc semantic-overlap grounding · builder-recommended) | 520 | 262 | **782** |
| **β** (per-sentence structured-output anchor mapping · Tier-1-safer) | 655 | 262 | **917** |
| **γ** (verbatim quote-only grounding · most conservative) | 405 | 262 | **667** |

**Proposed band (raw LoC per §9):** `[650, 950]` — brackets all three scenarios with headroom on both ends. Band-relative verdict trichotomy (per §9 metric-verdict-in-derivation-unit + Owner §9 correction):
- below-bottom (< 650) — disclose driver at close per Tier-2 discipline
- in-band ([650, 950]) — no disclosure required beyond snapshot line
- above-top (> 950) — disclose driver at close per Tier-2 discipline

### §3.6 §4.2 threshold statement (Tier-2 disclosure)

- Raw LoC threshold: **1,500** (single-commit § 4.1 baseline). Point-estimate mid ~800 · scenario β top ~917 · all scenarios projected UNDER threshold with material headroom.
- Cell count threshold: **60** cells. Estimate: 15 backend cells + 0 frontend cells = **15**; well under.
- **Disposition anticipated: atomic single commit per §4.1 baseline** — dev's judgment at execution per governance §2.2 (no round-trip). §4.2 pre-authorized split-fallback registered: if cumulative diff crosses ≥1,500 raw LoC OR ≥60 cells during execution (unlikely per estimates), split at the natural seam:
  - **Split-A:** fluency_synthesizer + fluency_prompt template + Shield-side scaffolding (the "LLM-integration" unit)
  - **Split-B:** grounding gate + composed_conclusion dispatcher + fluency_mode telemetry + gate roster (the "Service-1-side + honesty-gate" unit)

---

## §4. Data-blind + honesty-grammar posture attest

Governance §8 attest: prompt template lives at `services/synisense/shield/fluency_prompt.v0.txt` (or `.json`) as **[Tier-3 default]**; MUST NOT encode content-type / genre / regional / dialectal / broadcaster assumptions about the RMS estate. Prompt phrasing built around content-neutral shape rules (defensibility class · load-bearing anchoring · claim-first prose discipline). AF-G8 attests via grep-negative walk over the prompt file for the neutralised-broadcaster-alias set (`citizen_tv_news` / `wire_kna` / etc. from the pre-Fixture-Refresh broadcaster list) + a positive attest that the prompt contains only category-generic language.

Governance §9 attest: band derived + verdict rendered in RAW LoC per Owner §9 ruling. Alternate-unit disclosure permitted (LLoC + cell count + cyclomatic) as disclosure lines only — never overturns raw-LoC verdict.

Governance §10 attest: fluency is dispatch-independent from 9.2a/9.2b (fluency does not touch perception workers or the census gate). No 9.2-OWN facts blocking. Fluency operates over any Registry composition — including the current empty-Registry synthetic-fixture state.

Standing Rule v3 attest: this Stage A is on-disk canonical. Reply body carries SHA + tier tags only.

---

## §5. Gate roster (AF-G1..AF-G8 · 15 cells · full escalation surface stated pre-execution)

| Gate | Tier | Cell class | Purpose |
|---|---|---|---|
| **AF-G1** | Tier-1 (regression baseline honesty) | §6.1 × 2 | Mechanical composer preserved · byte-identical output for the pre-3.8 test-fixture request set · attests the "fluency is upgrade path, not replacement" Owner scope anchor. |
| **AF-G2** | **Tier-1 (no-fabricated-values honesty grammar)** | §6.1 × 4 | Per-sentence grounding gate — every sentence in fluent draft has at least one anchor in `load_bearing_unit_ids`; anchors reference valid unit_ids; anchors are semantically defensible (per the AF-E1 grounding discipline). Reject → fluency_mode=mechanical. See AF-E1 escalation for the specific grounding-discipline ruling required. |
| **AF-G3** | **Tier-1 (refusal taxonomy closure)** | §6.11 × 2 | LLM-unavailable at Shield boundary → HTTP 503 to caller. NEVER routes to any refusal registry (admission_refusal or Service1Refusal). Attests refusal taxonomy stays closed per Owner scope anchor. See AF-E2 escalation for 503-behaviour ruling. |
| **AF-G4** | **Tier-1 (frozen contract preservation)** | §6.1 × 1 | `ComposedConclusion_v0.model_json_schema()` byte-identical against `composed_conclusion.contract_snapshot.json`. V1-G7 parity attest at 31 stays GREEN. |
| **AF-G5** | Tier-3 (observability) | §6.1 × 2 | Fluency mode + attribution surfaces in sidecar telemetry (matches `execution_mode_telemetry` from 9.2a). NOT on the frozen envelope. |
| **AF-G6** | **Tier-1 (Shield chokepoint)** | §6.10 × 1 | Reflection walk over `services/service_1/**` confirms no direct `litellm.` / `openai.` / `anthropic.` / `emergentintegrations.` imports outside the Shield boundary. The pre-existing `test_no_direct_llm_calls_outside_shield` is co-attested. |
| **AF-G7** | Tier-1 (quality-gate ≠ refusal) | §6.1 × 2 | Grounding-gate reject → `fluency_mode="mechanical"` + `_grounding_reject_reason` populated + NO refusal envelope emitted. Ledger row (`NorthenaLedgerRow_v1`) still fires with `data_class="composed_conclusion"` (not a new class). |
| **AF-G8** | Tier-1 (data-blind posture) | §6.10 × 1 | Prompt template file contains no broadcaster-alias residues + no genre-specific defaults + no regional priors. |

**Grand total: 15 cells · 262 raw LoC backend tests.**

---

## §6. Escalation matrix — PRE-TIERED

### §6.1 Tier-1 escalations (verbatim relay to Owner)

**AF-E1 · Grounding-gate discipline — how strict is "every sentence derived from load-bearing units"?**

> Owner scope anchor: *"Every sentence derived from load-bearing units; invented connectives or unsupported synthesis fail the gate — no-fabricated-values applied to prose."*
>
> Options (pre-authorised menu):
> - **α · Post-hoc semantic-overlap grounding.** Fluent draft emitted freely by the LLM; grounding gate runs a post-hoc lexical/semantic-overlap check per sentence against the load-bearing unit texts. Sentence is grounded IFF ≥1 unit contributes ≥K semantic overlap (K to be Owner-set; builder-recommendation K=0.35 semantic-token Jaccard). Cheap; permits fluent connectives; but "invented connectives" is a subtle failure mode that lexical overlap may miss.
> - **β · Per-sentence structured-output anchor mapping.** LLM is instructed to emit `{prose, per_sentence: [{sentence, unit_ids: [...]}]}` as structured output; grounding gate verifies each declared unit_id is in `load_bearing_unit_ids` + verifies each sentence in prose is covered by at least one anchor. Strictest; catches invented connectives directly (a connective sentence with no unit anchor fails); slight added cost in prompt engineering + LLM output tokens.
> - **γ · Verbatim quote-only grounding.** LLM's only permitted output is verbatim quotes from unit texts, stitched together with minimal ligature. Most conservative; sacrifices fluency; may not match the "upgrade path" spirit.
>
> **Builder-recommendation: β** — Owner text "invented connectives … fail the gate" reads as requiring positive per-sentence attribution, which β enforces mechanically. α risks a false-positive on smooth invented prose; γ underdelivers on the fluency upgrade. β also aligns with 9.2a-E1 α pattern (attest via structured attribution, not post-hoc heuristic).
>
> **Class:** Tier-1 (client-promise · no-fabricated-values honesty grammar applied to prose).
> **Ruling required BEFORE execution.**

**AF-E2 · LLM-unavailability behaviour — 503 boundary specification**

> Owner scope anchor: *"LLM unavailability surfaces as infra fault (503), never refusal — refusal taxonomy stays closed."*
>
> The scope anchor is directive; this escalation asks Owner to bless the specific 503-boundary set the builder proposes to implement:
>
> **Proposed boundary set (all 503 to caller · none routed to refusal taxonomy):**
> - Emergent LLM key missing / invalid → 503 (matches Standing Disposition `Infra-not-refusal` per Phase 7 Stage B-2).
> - Sonnet model unavailable / rate-limited / provider down → 503.
> - Shield boundary timeout (configurable · **[Tier-3 default]** 30s) → 503.
> - Structured-output parse failure at Shield boundary (LLM returned malformed anchor JSON) → 503 (interpreted as "LLM didn't answer coherently" — infra fault, not a refusal-worthy event).
> - Grounding-gate REJECT (fluent draft failed grounding check) → NOT 503 · falls through to mechanical arm · fluency_mode=mechanical + `_grounding_reject_reason` populated. This is a quality-gate outcome, not an infra fault.
>
> **Options (pre-authorised menu):**
> - **α · Blessed as proposed above** (builder-recommendation).
> - **β · Timeout narrower** (e.g., 10s) — reduces caller-side latency risk but increases false-503 rate.
> - **γ · Include structured-output parse failure as grounding-gate reject** (fall through to mechanical instead of 503) — smoother UX but blurs infra-fault vs quality-gate line.
>
> **Class:** Tier-1 (refusal taxonomy closure · security boundary posture).
> **Ruling required BEFORE execution** — the 503 boundary set is load-bearing on the "refusal stays closed" client promise.

**AF-E3 · Fluency-mode observability seam — sidecar vs contract-touch**

> Owner scope anchor: *"frozen ComposedConclusion envelope untouched — any contract contact is Tier-1."*
>
> The scope anchor prohibits envelope mutation. This escalation confirms the sidecar-telemetry design (mirroring 9.2a-E2 α condition 2) is the intended posture — OR opens the Tier-1 door if Owner prefers contract touch:
>
> **Options:**
> - **α · Sidecar telemetry** (builder-recommendation) — `fluency_mode_telemetry.annotate_result(request_id, {"fluency_mode": ...})` returns an OBSERVABILITY payload attached to the request context but NOT to `ComposedConclusion_v0`. Envelope stays byte-identical. Parity 31 preserved. Matches 9.2a-E2 α cond 2 precedent.
> - **β · Additive contract field** — `ComposedConclusion_v0.fluency_mode: Literal["mechanical", "llm"] = "mechanical"` (Optional with default; snapshot regenerated · Owner ruling required · parity 31→31 additive contract touch). Costlier (+~155 LoC snapshot + ~60 LoC class body + verbatim carrier ~100).
> - **γ · Ledger row `data_class` sidecar** — emit fluency_mode via `NorthenaLedgerRow_v1.stamp_audit` sidecar (open-shape dict); costs nothing at the contract; but stamp_audit is a governance surface (any new stamp_audit shape needs data_class-registry attention).
>
> **Builder-recommendation: α.** Owner scope anchor is explicit; α satisfies it with the least surface change. β is the load-bearing "if you want fluency_mode in the wire contract" answer — surfaced for Owner acknowledgement, not builder-preferred.
>
> **Class:** Tier-1 (frozen wire contract touch) IF Owner selects β; otherwise Tier-2 (design choice within scope).
> **Ruling required BEFORE execution** — the frozen-contract touch decision is Tier-1.

**AF-E4 · Mechanical composer preservation — regression baseline discipline**

> Owner scope anchor: *"Mechanical composition retained as regression baseline; fluency is an upgrade path, not a replacement."*
>
> **Options:**
> - **α · Byte-identical regression baseline** (builder-recommendation) — mechanical composer produces byte-identical `answer_text` for the same input as the pre-3.8 code path. Regression gate AF-G1 attests via golden-file comparison against pre-3.8 output snapshots.
> - **β · Semantic-equivalent regression baseline** — mechanical composer refactored (e.g., extracted to its own module) but produces text with the same information content (not necessarily byte-identical). Regression gate attests via semantic equivalence (softer).
> - **γ · Behavioural-parity regression baseline** — mechanical composer moves to a helper and callers get one arm of a dispatcher; regression gate attests only that mechanical arm is CALLABLE + returns a non-empty string.
>
> **Builder-recommendation: α.** Owner's word "retained" reads as "byte-identical retention". Any drift in the mechanical arm invites confusion about which arm is "the baseline". α is also the strictest anti-regression posture.
>
> **Class:** Tier-1 (client-promise · "retained as regression baseline" is a client-facing honesty statement).
> **Ruling required BEFORE execution.**

### §6.2 Tier-2 disclosures (cost/rework · no round-trip · lines in close report)

- **T2-D1:** proposed raw-LoC band `[650, 950]` derived per §6.1-6.11 rate ledger + §9 raw-LoC verdict rule. Below-bottom / above-top per Owner §9 correction (band-relative, not mid-relative).
- **T2-D2:** §4.2 thresholds stated pre-execution — 1,500 raw LoC / 60 cells. Point-estimate all three scenarios (α/β/γ) UNDER threshold with material headroom. Atomic single-commit disposition anticipated per §4.1 baseline. Split-fallback pre-authorised at the natural seam described in §3.6.
- **T2-D3:** cell count estimate 15 backend cells + 0 frontend cells; cell-density mix (§6.1 classic × 13 + §6.10 AST/reflection × 2 + §6.11 async httpx × 2 = 15 cells at 262 LoC = 17.5 LoC/cell avg).
- **T2-D4:** verbatim-carrier overhead (§6.9) counted at ~100 LoC in the fluency_synthesizer module (Owner scope anchors embedded verbatim as module docstring per Standing Rule v3 posture); disclosed under-band or on-band expected.
- **T2-D5:** snapshot in-band verdict rendered post-execution against raw wc-l counts; LLoC + cell density disclosed as disclosure lines only per Owner §9 ruling.

### §6.3 Tier-3 defaults (silent · one-line notes in close report)

- **[Tier 3 default]** module names: `services/synisense/shield/fluency_synthesizer.py` · `services/service_1/answer_grounding.py` · `services/service_1/fluency_mode_telemetry.py` — matches co-tenancy conventions (Shield chokepoint · Service-1 side · sidecar-telemetry mirror).
- **[Tier 3 default]** prompt template file: `services/synisense/shield/fluency_prompt.v0.txt` (or `.json` if structured output requires JSON schema anchoring; decided at execution per option chosen at AF-E1).
- **[Tier 3 default]** LLM model: **Sonnet 4.6 via Emergent LLM key** — already inside the Shield at `llm_router.py::SonnetWizardAgent` (Phase 7 Stage B-2 precedent). Fluency reuses the same backend; NO new integration required (no `integration_playbook_expert_v2` call). Temp 0.0 for hermetic tests · 0.2 for live per llm_router precedent.
- **[Tier 3 default]** Shield timeout: 30s at the LLM boundary; matches perception_router / wizard-agent conventions.
- **[Tier 3 default]** structured-output anchor JSON schema field names: `{prose, per_sentence: [{sentence_text, unit_ids: [...]}]}` — self-documenting.
- **[Tier 3 default]** test file names: `tests/invariants/test_answer_fluency_af_g1_to_g8.py` — matches `test_fixture_refresh_fr_g1_to_g7.py` + `test_9_2a_gates.py` naming convention.
- **[Tier 3 default]** rulings-record + close-report file paths on-disk canonical: `docs/rulings/answer_fluency_af_e1_to_e4.md` + `docs/close_reports/answer_fluency.md`.
- **[Tier 3 default]** grounding-gate config location: co-located with grounding module as constants (no runtime config file; §6.9 verbatim carrier suffices).

---

## §7. §DirectionConsistency preview (executable at execution STEP A)

At execution, the direction-consistency check will scan **4 surfaces × 4 check-types = 16 intersections**:

**Surfaces:**
- S1: `docs/mandates/RMS_Product_Engineering_Spec_v3.md` (§6.2 composed_conclusion locus)
- S2: `memory/PHASE_STATE.md` (live phase-state)
- S3: `memory/PRD.md` (PRD ledger)
- S4: `docs/mandates/RMS_UI_Specification_v2_1.md` (Ask surface / AnswerView binding copy)

**Check-types:**
- C1: pre-fluency `answer_text` wording (any spec text asserting mechanical composition IS the shipping form? · pre-supersession residue)
- C2: refusal-taxonomy contamination (any spec/live-doc wording suggesting LLM unavailability = refusal? · violates Owner scope anchor)
- C3: envelope-contact assumption (any spec text implying `ComposedConclusion_v0` gains a fluency field? · violates Owner scope anchor)
- C4: grounding-gate visibility (any spec text asserting grounding is a runtime-visible ledger row rather than a post-hoc gate that either succeeds silently or degrades to mechanical? · verified at execution)

CLEAN PASS expected on live-direction cells; residues in closed Stage A proposals PRESERVED per Standing Rule v3.

---

## §8. Standing constraints preserved at close (attested pre-execution)

| Constraint | Attest at execution |
|---|---|
| 31 frozen contracts + 31 snapshots byte-identical (V1-G7 at parity 31) | GREEN — no contract touch; snapshots untouched. |
| 4-code auth-refusal registry closed | GREEN — fluency is not an auth surface. |
| No HTTP 409 in fluency new/modified files (E5 discipline) | GREEN — 503 boundary only. |
| Standing Rule v3 (on-disk canonical · historical closes preserved) | GREEN — Stage A on-disk here; execution close lands separately. |
| AS-H1 retention held-class (no direct DELETE) | GREEN — fluency adds no DELETE handlers. |
| Governance §8 data-blind posture | GREEN — prompt template attests AF-G8. |
| Governance §9 metric-verdict-in-derivation-unit | GREEN — band + verdict in raw LoC. |
| Governance §10 9.2 split ruling | GREEN — fluency dispatch-independent from 9.2a/9.2b. |
| 9.2a-E1 α models_registry seed pattern | N/A (perception scope). |
| CD-E2 ↔ CD-E4 coupling | N/A (census scope). |
| FR-G4 no-shadow-source AST posture | GREEN — no new broadcaster residues introduced; grounding-gate anchors reference `load_bearing_unit_ids` (unit_ids, not feed_ids). |

---

## §9. Provenance + sequence forward

- **Stage A (this file):** `/app/docs/stage_a_proposals/answer_fluency.md`
- **Rulings record (post-Owner-ruling):** `/app/docs/rulings/answer_fluency_af_e1_to_e4.md`
- **Close report (post-execution):** `/app/docs/close_reports/answer_fluency.md`
- **Landing gate roster:** AF-G1..AF-G8 (15 cells · 262 raw LoC · full estimate 650-950 raw LoC)
- **Sequence after:** Opportunity Briefs (§3.15 · fixture-census permitted per AS-U2) → production housing (§3.4). 9.2b stays gated on 9.2-OWN-1..3 (owner-side).

═══════════════════════════════════════════════════════════════════

*End of §3.8 Answer Fluency Stage A proposal. Standing Rule v3: on-disk canonical. Awaiting Owner rulings on Tier-1 escalations AF-E1..AF-E4 (verbatim relay).*
