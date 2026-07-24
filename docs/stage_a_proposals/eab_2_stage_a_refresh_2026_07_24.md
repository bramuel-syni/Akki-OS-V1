# EAB-2 · Stage-A Refresh · 2026-07-24 (STEP 4 pre-execution atomic)

**Class:** Stage-A refresh per Owner Configuration Dispatch 2026-07-24 §4.STEP-4 binding — verbatim: *"at Stage-A refresh, check Service1Refusal@v1's envelope against the Prove spec's three refusal shapes (not-extracted-yet + gap-queue affordance + estimated effort · evidence-can't-support · something-broke) — the drawer and Answer Card will render this exact contract. Shape mismatch = HAZARD-STOP (a) before the Parity 31→32 seal, not after."*

**Authority artifacts (D-11 canon-before-attest · live-read this session):**

| Artifact | Path | SHA-256 |
|---|---|---|
| Owner Configuration dispatch | `docs/rulings/owner_configuration_2026-07-24.md` | `ec95a0acec13d81b2fd5f1b1da04c83d2991f3876c795c8266a96eaef1230f52` |
| STEP-2 Surfaces ruling | `docs/rulings/owner_step2_surfaces_ruling_2026-07-24.md` | `2e11c7ea864a940d64b1a438b7bf1f0f5fd6e77b12aeb816d9bfad640779d178` |
| Substrate-Drop v3 reconciliation audit (§B.C-1 pre-naming) | `docs/audits/substrate_drop_v3_reconciliation_2026_07_24.md` | `33f20261c6a2b9cece19b077d4beedc1933ab850cf97cca6b2858ab73eb042f7` |
| EAB-2 Stage A (§5.1 sub-option a1) | `docs/stage_a_proposals/eab_2_stage_a.md` | `60a49c47e95cf6d7eddc6631f17ba2533b06364c2615d7785958dc69a8d7d805` |
| EAB Tier-1 Adoption Spec v1.1 | `docs/requirements/eab_tier1_adoption_spec_v1.1.md` | `312427c672e9db8a9bda83f5b0db79218c46b7f14085233ce974671d259571c9` |
| Prove Module spec | `docs/mandates/module_specs/05_prove_module.md` | `12b1bea55b056dbd6acf1f4dd177bbb40b899be0153e1281069b5eab2f0b5cc6` |
| Service1Refusal@v0 baseline contract | `backend/contracts/service_1_refusal.py` | `4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022` |
| Service1Refusal@v0 snapshot | `backend/tests/invariants/service_1_refusal.contract_snapshot.json` | `56ec42bb5a12bda02f98653ee5762dda62fe91bd5543fbef6ea2f20f5822020d` |

**Estimation-discipline attest:** no duration/credit figure emitted. Owner ruling surfaces at §4 below are grounded in byte-level evidence, not builder menu.

---

## §1 · Source (A) · `Service1Refusal@v1` envelope shape per EAB-2 Stage A §5.1 sub-option a1

Owner-ruled authorized posture (per Stage A §5.1 sub-option a1 · superset envelope · single-writer end-state at close · v0 byte-identity preserved). Field list constructed from:
- v0 baseline (`backend/contracts/service_1_refusal.py` L52-99) — all v0 fields preserved
- Stage A §5.1 additive fields (verbatim: *"A3 adds a `coverage_gap` reason plus gap-descriptor fields (`estate_region: str`, `period: str`, `source_class: str`, `filed_candidate_id: str`) that the v0 envelope cannot carry."*)

**Envelope A · `Service1Refusal_v1` (superset per sub-option a1):**

```python
class Service1Refusal_v1(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    # ─── v0-preserved fields (7 fields · byte-identity to v0 contract) ───
    outcome: Literal["refused"]                                   # discriminator
    reason: Literal[                                              # 4-value enum
        "no_defensibility_floor",                                 # v0 evidential-family
        "no_lawful_basis",                                        # v0 evidential-family
        "composition_below_floor",                                # v0 evidential-family
        "coverage_gap",                                           # v1 additive · A3 class
    ]
    run_id: str
    trace_id: str
    asked: str                                                    # plain-language objective + required floor
    supported_class: Optional[DefensibilityClass]                 # None on pre-composition + coverage_gap
    what_would_raise_it: str                                      # actor-appropriate lift hint

    # ─── v1 additive fields · coverage_gap descriptor set (4 fields) ───
    estate_region: Optional[str]      = None                      # Mtafiti registry vocabulary
    period: Optional[str]             = None                      # Mtafiti registry vocabulary
    source_class: Optional[str]       = None                      # Mtafiti registry vocabulary
    filed_candidate_id: Optional[str] = None                      # Targeta gap-candidate FK (referential to demand-signal-side record)
```

**Total: 11 fields · reason enum 4-value (3 evidential + 1 gap) · additive fields Optional=None for non-coverage-gap emissions (single-writer end-state).**

**Not in Envelope A (per R-A3.3 fault-never-dressed-as-refusal · verbatim from EAB v1.1 Part IV): fault-family responses are NOT carried in Service1Refusal@v1. Faults surface via a separate wire path (HTTP 503 + structured detail per `PROM-S1-config-defect-fail-loud` · or `PROM-S1-runtime-transient-never-refusal` sidecar telemetry for transients).**

---

## §2 · Target (B) · Prove Module spec's three refusal shapes

**Verbatim from `docs/mandates/module_specs/05_prove_module.md` lines 52-55 (SHA `12b1bea55b056dbd`):**

> **Step 4 — Refusal Shapes:** Three visually distinct states:
> - **Not extracted yet** — shows the gap plainly, estimated effort to close it, "Queue this gap" button
> - **Evidence can't support** — states the reason, no queue option (more extraction wouldn't help)
> - **Something broke** — plain error, never disguised as the other two

**Verbatim from `05_prove_module.md` lines 31-42 (flowchart of Journey 1 refusal branches):**

```
D -->|Not extracted yet| F[Shows gap + Queue this gap button]
D -->|Evidence can't support| G[Shows reason, no queue option]
D -->|Something broke| H[Plain error, distinct styling]
...
F --> L[Click Queue this gap]
L --> M[Routes to Extract's Shape an Objective
        prefilled, saved as draft]
M --> N[Answer Card updates:
        Queued as draft OBJ-XXX, link back]
```

**Verbatim from `05_prove_module.md` line 57:**

> **Step 5 — Queue a Gap:** Clicking routes to Extract's Shape an Objective, prefilled from the gap's description, saved as a **draft** (not commissioned). The originating Answer Card updates — "Queued as draft OBJ-XXX →" — closing the loop visibly.

**Field-set implied by Prove spec Target (B) per-shape:**

- **`not-extracted-yet` shape** requires: gap description (plain rendering) · `estimated_effort_to_close_it` · `queue_this_gap_button_action` (routes to Extract prefill with draft OBJ-XXX creation).
- **`evidence-can't-support` shape** requires: `reason` (plain-language) · **NO queue button** (explicit exclusion per spec: *"more extraction wouldn't help"*).
- **`something-broke` shape** requires: `plain error` render · **distinct styling** · Owner-verbatim spec line: *"never disguised as the other two"*.

---

## §3 · Byte-level field-by-field comparison

### §3.1 · Shape 1 — `not-extracted-yet`

| Prove spec need | Service1Refusal_v1 field | Match verdict | Notes |
|---|---|---|---|
| "the gap plainly" (estate region · period · source class rendered in asker's terms per EAB v1.1 R-A3.2) | `estate_region: Optional[str]` + `period: Optional[str]` + `source_class: Optional[str]` (populated on `reason="coverage_gap"`) | **MATCH** | Envelope carries the descriptor triple; Prove renders directly. |
| `reason` discriminator to select this shape | `reason: Literal["…", "coverage_gap"]` | **MATCH** | `reason=="coverage_gap"` → Prove selects `not-extracted-yet` render. |
| "estimated effort to close it" | **NOT IN ENVELOPE** | **MISMATCH · missing-in-envelope** | See §3.4.a below — Targeta-side channel via `filed_candidate_id` dereference, or envelope-side additive field. |
| "Queue this gap" button action (routes to `Extract's Shape an Objective prefilled saved as draft OBJ-XXX`) | `filed_candidate_id: Optional[str]` (referential FK) | **PARTIAL-MATCH · action-descriptor derivation** | Envelope carries the FK; button `href`/action must be derived at render (Prove reads `filed_candidate_id` → constructs Extract Shape-Objective URL with prefill). Not a byte-level envelope field. See §3.4.b below. |
| "Answer Card updates: Queued as draft OBJ-XXX →" (closing the loop visibly) | **NOT IN ENVELOPE** | **PARTIAL-MISMATCH · state-update out-of-band** | Post-queue state update is a UI-side interaction; envelope is emit-once. Prove UI-side observes the queue event separately. Not a byte-level envelope issue. |

### §3.2 · Shape 2 — `evidence-can't-support`

| Prove spec need | Service1Refusal_v1 field | Match verdict | Notes |
|---|---|---|---|
| `reason` discriminator to select this shape | `reason: Literal["no_defensibility_floor", "no_lawful_basis", "composition_below_floor", ...]` (three v0-preserved evidential-family values) | **MATCH · via bucketing** | Prove renders all three v0-family reasons as `evidence-can't-support` shape. Bucketing occurs at Prove render layer, not at envelope wire. |
| "states the reason" (plain-language reason text) | `asked: str` + `what_would_raise_it: str` + `supported_class: Optional[DefensibilityClass]` | **MATCH** | Envelope carries semantic triple; Prove composes plain-language render. |
| "no queue option (more extraction wouldn't help)" | Absence of `filed_candidate_id` on evidential-refusal-family emissions | **MATCH · via absence** | When `reason != "coverage_gap"`, `filed_candidate_id` is None (per single-writer end-state posture); Prove suppresses queue button on None. |

### §3.3 · Shape 3 — `something-broke`

| Prove spec need | Service1Refusal_v1 field | Match verdict | Notes |
|---|---|---|---|
| "plain error, distinct styling" | **NOT IN ENVELOPE AT ALL** | **HARD MISMATCH · shape-family boundary conflict** | Per EAB v1.1 §Part IV R-A3.3 verbatim: *"Fault discipline preserved verbatim: retrieval timeout / downstream error is NEVER surfaced as any refusal class. Existing rule, restated."* + `Service1Refusal@v0` L18-22 doctrinal note: *"`outcome: Literal[\"refused\"]` is the load-bearing discriminator that distinguishes a governed refusal from FastAPI's default `RequestValidationError` (which has `detail: list`, no `outcome`). The frontend keys on `body.outcome === \"refused\"`, never on structural inference over the shape of `detail`."* — faults MUST NOT enter the Service1Refusal envelope; they surface via HTTP 5xx + structured detail (`PROM-S1-config-defect-fail-loud`) or `PROM-S1-runtime-transient-never-refusal` sidecar telemetry. |
| "never disguised as the other two" (Prove spec verbatim) | Refusal-envelope discriminator `outcome: Literal["refused"]` explicitly separates refusals from faults | **CONVERGENT AT INTENT · DIVERGENT AT TAXONOMY** | Prove spec's intent (distinct visual family + no cross-shape confusion) MATCHES engineering canon (fault envelope disjoint from refusal envelope). But Prove spec's grouping of `something-broke` **UNDER** "Refusal Shapes" as one of three visually distinct states creates a taxonomic conflict: engineering-wire has TWO envelope families (refusal + fault), Prove-UI-family has THREE shape renders. |

### §3.4 · Peripheral considerations (per STEP 4 §2.2)

**§3.4.a · `estimated_effort` field on `not-extracted-yet`**

Prove spec (line 53): *"estimated effort to close it"* — where does this render source from?

Two on-disk-canonical postures:

- **(α) Targeta-side channel via `filed_candidate_id` dereference:** Envelope carries `filed_candidate_id: Optional[str]`; Prove issues a companion read against Targeta's demand-signal-side record to fetch `estimated_effort`. This is the R-A3.2-compliant posture ("*FILES the gap as an extraction candidate visible to Targeta's planning inputs (demand signal, not authorization)*" — filed candidate carries effort metadata, envelope carries the FK).
- **(β) Envelope-side additive field:** Add `estimated_effort: Optional[str]` to Service1Refusal_v1 (a1 sub-option would extend by one more field). This is a **byte-level envelope shape change beyond Stage A §5.1's declared 4-descriptor-field additive set**.

**Neither is currently authoritative.** The Stage A §5.1 envelope-additive set as literally declared includes only the 4-tuple `{estate_region, period, source_class, filed_candidate_id}` — **`estimated_effort` is not in the declared additive set**. Owner ruling required to select (α) or (β).

**§3.4.b · `gap-queue affordance` (URL / action descriptor)**

Prove spec (line 40): *"Routes to Extract's Shape an Objective, prefilled, saved as a draft"*.

- **(γ) Referential derivation:** Envelope carries `filed_candidate_id`; Prove UI derives the Extract Shape-Objective route (e.g., `/extract/shape?prefill=<filed_candidate_id>`) at render. **Compatible with Stage A §5.1 envelope declaration.**
- **(δ) Envelope-side action-descriptor field:** Add `queue_action_url: Optional[str]` or `queue_action: Optional[dict]` to Service1Refusal_v1. **Byte-level envelope shape change beyond Stage A §5.1's declared additive set.**

Stage A §5.1 does not literally include this field. Owner ruling required to select (γ) or (δ). (γ) is the D-12-cleaner posture (envelope stays minimal · Prove derives route from canonical FK).

**§3.4.c · `something-broke` fault envelope routing**

Per §3.3 above: `something-broke` is NOT a refusal class per R-A3.3.

Two on-disk-canonical postures:

- **(ε) Two-envelope wire · three-shape render:** Wire has (1) `Service1Refusal@v1` for the two refusal-family shapes, and (2) fault envelope (HTTP 503 + `{"error": "…", "trace_id": "…"}` structured detail per `PROM-S1-config-defect-fail-loud`) for `something-broke`. Prove render layer inspects HTTP status + body `outcome` discriminator, routes to one of 3 shapes. **This is the R-A3.3-compliant posture and is builder Tier-3 recommendation.**
- **(ζ) Amend Prove spec to explicitly exclude `something-broke` from the "Refusal Shapes" taxonomy** (rename Prove Step 4 to "Response Shapes" · treat `something-broke` as a fault-family render distinct from refusal-family renders). **This is a Prove-spec-side amendment**; requires Owner ruling on module-spec revision.

**§3.4.d · `evidence-can't-support` mapping to v0 3-way evidential taxonomy**

Prove spec collapses `no_defensibility_floor` · `no_lawful_basis` · `composition_below_floor` into a single UI shape (`evidence-can't-support`). No sub-shapes.

- Bucketing is at Prove render layer only (no envelope change · no wire change).
- **PARTIAL-EXTEND** — the semantic sub-distinctions are lost at UI (users cannot distinguish between "no defensibility floor met" vs "no lawful basis" vs "composition below floor") but preserved at wire (Prove render can access `reason` field directly if a debug view were added). Owner may want to preserve sub-distinctions at Prove UI in a "reveal details" or "walk-the-proof" tab. Not a blocker; defer to UI Stage A.

---

## §4 · Mismatch verdict + HAZARD-STOP (a) fires

**VERDICT: MISMATCH · HAZARD-STOP (a) FIRES.**

The mismatch is at the **taxonomy boundary** (§3.3 · §3.4.c) plus **two envelope-additive-set questions** (§3.4.a · §3.4.b). Byte-level evidence:

1. **Hard mismatch (§3.3):** Prove spec's "Refusal Shapes" family includes `something-broke`; engineering canon (EAB v1.1 R-A3.3 · v0 doctrinal note L18-22) treats `something-broke` as a fault envelope disjoint from Service1Refusal. Wire has 2 envelope families; Prove UI-family has 3 shape renders. **Convergent at intent, divergent at taxonomy.**
2. **Envelope-additive-set gap (§3.4.a):** `estimated_effort` is required by Prove spec's `not-extracted-yet` shape but is not in Stage A §5.1's declared 4-tuple additive set. Owner ruling required on (α) Targeta-side channel vs (β) envelope-side additive field.
3. **Envelope-additive-set gap (§3.4.b):** `queue_action_url` / gap-queue action descriptor is not literally in Stage A §5.1. Owner ruling required on (γ) referential derivation vs (δ) envelope-side action-descriptor field.

**Per Owner Configuration Dispatch §4.STEP-4 verbatim:** *"Shape mismatch = HAZARD-STOP (a) before the Parity 31→32 seal, not after."*

**PARITY 31→32 SEAL HALTED.** Zero contract touch this atomic (per Standing Rule v3 · zero `backend/contracts/**` mutation · Parity 31 held byte-identical). No `Service1Refusal_v1` file created. No snapshot created. No Solva dispatcher wiring. No Targeta gap-filer. No batch quarantine writer. **All EAB-2 execution scope deferred to a subsequent atomic post-Owner-ruling.**

---

## §5 · Owner ruling surface (Tier-1 escalation · byte-level grounded · NOT a menu)

Per Owner Configuration Dispatch §4.STEP-4 pre-naming + audit §B.C-1 pre-enumeration + Stage A §5.1 sub-option (a1) authorization, the ruling surface for HAZARD-STOP (a) has three orthogonal decision loci — one per mismatch class above. Each locus enumerates the byte-level-grounded options. **Every option preserves Standing Rule v3 (no byte contact with Service1Refusal@v0 · additive versioning only per `PROM-S1-additive-versioning`) and remains inside Owner-ruled sub-option (a1) posture (superset envelope · single-writer end-state).**

### §5.1 · Ruling locus 1 · `something-broke` taxonomy (§3.3 + §3.4.c)

- **Option ε · Two-envelope wire · three-shape render** (builder Tier-3 recommendation).
  - Byte-level: Service1Refusal_v1 carries only refusal-family (4-reason enum: 3 v0-evidential + coverage_gap). `something-broke` routes through fault envelope (HTTP 503 + structured detail per existing `PROM-S1-config-defect-fail-loud` regime). Prove render layer routes on HTTP status + body `outcome` discriminator.
  - Parity 31→32 seal impact: **PROCEEDS UNBLOCKED at ruling loci 2 + 3 resolution** (this locus does not require envelope shape change; R-A3.3 discipline preserved verbatim; AC-A3.a "three response types distinct at wire" is 2 refusal classes + 1 fault envelope = 3 response types).
  - Prove-spec-side implication: **NONE required** (Prove spec's 3 visual shapes are compatible with 2 wire envelopes; Prove renders at UI layer, not at wire layer). But Prove spec's use of "Refusal Shapes" as the umbrella term for all 3 remains a semantic-vocabulary drift with engineering canon — flag for UI-1 Stage A when Prove Module UI executes (may want to rename to "Response Shapes" in module spec, non-blocking here).
  - Standing Rule v3 impact: **PRESERVED** (no byte contact with v0 · no wire family change).

- **Option ζ · Amend Prove spec to exclude `something-broke` from "Refusal Shapes"** (spec-side amendment).
  - Byte-level: Same wire outcome as ε (2 envelope families · 3 render shapes with `something-broke` as fault-family render).
  - Prove-spec-side implication: rewrite `docs/mandates/module_specs/05_prove_module.md` Step 4 title from "Refusal Shapes" to "Response Shapes" (or Owner-authored replacement); reclassify `something-broke` as fault-family render outside refusal envelope.
  - This is a **module-spec amendment**, which is Owner-side scope (module specs are Owner-authored canon per Standing Rule v3). **Do NOT execute without Owner ruling.**
  - Parity 31→32 seal impact: independent of this decision — the seal only needs the envelope shape locked, not the Prove-spec taxonomy locked.
  - Standing Rule v3 impact: PRESERVED (module spec is Owner-authored; builder does not edit without Owner ruling).

- **Option η · Owner ruling that `something-broke` IS a refusal class at wire** (rejected at pre-name).
  - Would require adding `something_broke` as a fifth `reason` enum value in Service1Refusal_v1.
  - **REJECTED by R-A3.3** (fault-never-dressed-as-refusal) · **REJECTED by v0 doctrinal note L18-22** (`outcome` discriminator separates refusal from validation/fault) · listed only to complete enumeration.

**Builder Tier-3 recommendation:** ε (two-envelope wire · three-shape render · Prove-spec taxonomy note flagged for UI-1 Stage A · non-blocking).

### §5.2 · Ruling locus 2 · `estimated_effort` field placement (§3.4.a)

- **Option α · Targeta-side channel via `filed_candidate_id` dereference.**
  - Byte-level: Service1Refusal_v1 carries `filed_candidate_id` only (per Stage A §5.1 declared 4-tuple). Prove issues a companion GET against Targeta's demand-signal-side gap-candidate record to fetch effort estimate. Effort estimate rendered as a companion channel at UI.
  - Envelope shape: **unchanged from Stage A §5.1 declaration.**
  - Parity 31→32 seal impact: PROCEEDS UNBLOCKED (envelope byte-shape locked at Stage A design).
  - Runtime posture: two backend calls at Prove render (one for envelope, one for candidate details) OR the calling side batches (composition seam).
  - Standing Rule v3 impact: PRESERVED.

- **Option β · Envelope-side additive field `estimated_effort: Optional[str]`.**
  - Byte-level: Service1Refusal_v1 carries an additional 12th field beyond Stage A §5.1's declared 4-tuple. **Extends the additive set from 4 to 5 fields.**
  - Parity 31→32 seal impact: PROCEEDS at seal time with 12-field envelope (unchanged Parity count 31→32; only shape count of the new v1 module changes).
  - Runtime posture: single wire read at Prove render (envelope carries effort inline).
  - Standing Rule v3 impact: PRESERVED (v0 byte-identity untouched; v1 additive extension only).
  - Trade-off: envelope carries derived-render data (effort estimate is a Targeta-computation output, not a Solva-refusal-emission output). May couple envelope to Targeta computation lifecycle.

- **Option θ · Neither · effort estimate rendered via companion sidecar telemetry (`PROM-S1-runtime-transient-never-refusal` regime)** (listed for completeness · REJECTED at pre-name because effort is a governance-shaped output, not a runtime-transient signal).

**Builder Tier-3 recommendation:** α (Targeta-side channel · envelope remains minimal · effort estimate lives with the demand-signal-side candidate record · Prove render composes at UI).

### §5.3 · Ruling locus 3 · `queue_action_url` field placement (§3.4.b)

- **Option γ · Referential derivation.**
  - Byte-level: Service1Refusal_v1 carries `filed_candidate_id` only. Prove UI constructs the Extract Shape-Objective URL at render (e.g., `/extract/shape?prefill_from=<filed_candidate_id>`).
  - Envelope shape: unchanged from Stage A §5.1 declaration.
  - Parity 31→32 seal impact: PROCEEDS UNBLOCKED.
  - D-12 posture: canonical FK + client-side derivation is the least-drift · least-coupling posture. Envelope stays minimal; route templates live on Prove UI side.
  - Standing Rule v3 impact: PRESERVED.

- **Option δ · Envelope-side action-descriptor field `queue_action_url: Optional[str]` (or `queue_action: Optional[dict]`).**
  - Byte-level: additional 12th (or 13th if combined with §5.2 β) field on Service1Refusal_v1.
  - Parity 31→32 seal impact: PROCEEDS at seal time with extended envelope.
  - Runtime posture: envelope carries pre-rendered URL. Couples backend to URL scheme decisions.
  - Standing Rule v3 impact: PRESERVED.
  - Trade-off: hard-couples envelope to Prove URL structure; changes to URL scheme require envelope contract migration.

**Builder Tier-3 recommendation:** γ (referential derivation · envelope stays minimal · URL scheme lives Prove-side · easier to evolve).

### §5.4 · Composed builder Tier-3 recommendation (all three loci)

**ε + α + γ** — clean single-writer superset envelope per Stage A §5.1 sub-option (a1) declaration:

- Service1Refusal_v1 with the 11-field envelope as declared in §1 above (no additional fields beyond Stage A §5.1 4-tuple).
- `something-broke` routes through separate fault envelope (HTTP 503 + structured detail).
- `estimated_effort` and `queue_action_url` derived at Prove render via `filed_candidate_id` FK.
- Prove-spec "Refusal Shapes" umbrella term flagged for future UI-1 Stage A vocabulary reconciliation (non-blocking · module-spec authorship reserved to Owner).

**Owner may rule any composition** (e.g., ε + β + γ · or ε + α + δ · or ε + β + δ · or ζ instead of ε on locus 1 · etc.). Standing-rule-preserving; each option preserves v0 byte-identity and stays inside sub-option (a1) posture.

---

## §6 · Fences carried through this HAZARD-STOP atomic

- **Parity 31 held byte-identical.** `ls backend/contracts/*.py | wc -l = 31` · `ls backend/tests/invariants/*.contract_snapshot.json | wc -l = 31` · `git diff --stat HEAD backend/contracts/ backend/tests/invariants/` = empty. Verified live this session.
- **Zero code touch.** No `Service1Refusal_v1` module created. No snapshot created. No Solva dispatcher wiring. No Targeta gap-filer. No batch quarantine writer. No AST negative-scan cell. No AC-A3.a-c or AC-A4.a-c pytest cells. No Playwright cell. No Jest cell. No R4 sidecar file.
- **Zero governance-stack touch.** `docs/governance/tiered_ruling_model.md` §§1..23 byte-identical (verified via `sha256sum` this atomic).
- **Zero test-file touch.** `git diff --stat HEAD backend/tests/` = empty.
- **Zero Makefile touch.** Post-STEP-3 state preserved.
- **STEP 5 fence:** module re-band from STEP 3 audit rows is NOT triggered by this HAZARD-STOP (STEP 5 auto-proceeds only on EAB-2 execution atomic close, not on Stage-A-refresh HALT). Deferred until Owner rules and EAB-2 execution atomic closes.
- **§0-CAL §23 enumeration discipline:** this refresh document is a doc-only file (not code · not test · not migration); §23.1 per-line enumeration not triggered. §23.2 gate-cell roster: Stage A §2 band table's 11 pytest + 1 Playwright + 1 Jest gate cells remain pre-declared; execution deferred pending ruling.

---

## §7 · Predecessor byte-identity attests

- `backend/contracts/service_1_refusal.py` (v0) — SHA `4fe38c214dc592603ceeffaf07732d33e374bae825fc7556d8684f667e41b022` — **byte-identical to HEAD** (`git diff HEAD backend/contracts/service_1_refusal.py` empty).
- `backend/tests/invariants/service_1_refusal.contract_snapshot.json` (v0 snapshot) — SHA `56ec42bb5a12bda02f98653ee5762dda62fe91bd5543fbef6ea2f20f5822020d` — **byte-identical to HEAD**.
- `docs/governance/tiered_ruling_model.md` (§§1..23) — SHA `9b3c56c14a1159af35c382e1a68368fcf673a381f77cd4734e51a85cd57e51c4` (post-§23 STEP-3 landing) — **byte-identical to STEP-3-close state** (no additional §24 or beyond this atomic).
- `docs/stage_a_proposals/eab_2_stage_a.md` — SHA `60a49c47e95cf6d7eddc6631f17ba2533b06364c2615d7785958dc69a8d7d805` — **byte-identical to prior landing** (Stage A design authoritative · this refresh does not amend it).
- `docs/mandates/module_specs/05_prove_module.md` — SHA `12b1bea55b056dbd6acf1f4dd177bbb40b899be0153e1281069b5eab2f0b5cc6` — **byte-identical to STEP-3 landing** (Prove spec is source-of-truth for target shapes; this refresh does not amend it).

---

## §8 · D-1..D-11 self-audit table (standing practice · D-12 heavy-weight)

| # | Defect | Verdict | Note |
|---|---|---|---|
| D-1 | Orphan surface | PASS | Every claim traces to Owner-verbatim dispatch §4.STEP-4 (§1 above) + module-spec verbatim quote (§2 above) + on-disk v0 contract verbatim (§1 above) + Stage A §5.1 sub-option a1 verbatim (§1 above). Every ruling-locus option traces to one specific mismatch class in §3. |
| D-2 | NL-only claim | PASS | Every SHA verified live via `sha256sum` this session; every module-spec line quoted with exact line-number references (`05_prove_module.md:52-55`, `31-42`, `57`); every contract field quoted from source file live-read this session. |
| D-3 | Curated verdict | PASS | All 3 shapes analyzed exhaustively (§3.1 · §3.2 · §3.3); all 4 peripheral considerations enumerated (§3.4.a-d); all 3 ruling loci enumerated with byte-level-grounded options (§5.1 · §5.2 · §5.3); composed builder Tier-3 recommendation surfaced but does NOT self-rule (§5.4 explicit "Owner may rule any composition"). |
| D-4 | Rung inflation | PASS | No rung claims made in this refresh. |
| D-5 | Cross-phase content leakage | PASS | Refresh scoped strictly to STEP 4 pre-execution HAZARD-STOP surface. Zero STEP 5 (module re-band) content. Zero STEP 6 (EAB-3 / Critic-pass / G-13 / UI-1 / UI-2) content. Zero Lane 1 content. Prove-spec taxonomy note (§5.1 option ε) explicitly flagged for future UI-1 Stage A, not enacted here. |
| D-6 | Silent scope drift | PASS | Refresh is doc-only; no code, no tests, no migration. STEP 4 execution scope (§3 of STEP 4 dispatch) explicitly held pending Owner ruling at §5 above. |
| D-7 | Invented scope | PASS | Every ruling-locus option is grounded in a specific byte-level mismatch identified in §3; zero fabricated options. Stage A §5.1 sub-option (a1) is Owner-ruled authorized posture and is preserved as the outer container of all options. No `something_broke` reason value invented in the recommended posture (locus 1 option ε) — R-A3.3 preserved verbatim. |
| D-8 | Silent drift | PASS | Standing Rule v3 attest at §6 + §7 (v0 byte-identity · v0 snapshot byte-identity · governance §§1..23 byte-identical · Stage A byte-identical · Prove spec byte-identical). Parity 31 held. |
| D-9 | Testing-agent invocation | PASS | Banned; not invoked. This atomic is doc-only; no test execution triggered. Native `pytest`/`yarn test`/`npx playwright test` remain the only execution paths for future EAB-2 execution atomic (deferred). |
| D-10 | Menu emission | PASS | §5 ruling surfaces (§5.1, §5.2, §5.3, §5.4) are **Tier-1 escalation surfaces pre-named per Owner Configuration Dispatch §4.STEP-4** — structured per §5.1-precedent enumeration pattern from EAB-1 Stage A ruling surface. Each option is byte-level-grounded (traces to a specific mismatch class + specific standing rule preserved). **Not a builder permission menu**; ruling authority is Owner. Builder Tier-3 recommendation (§5.4) is disclosed transparently per Stage A §5.1 precedent (which itself carried a builder Tier-3 recommendation for (a1) that Owner ultimately authorized). |
| D-11 | Canon-before-ruling / LLM-memory recall | PASS | Every citation live-verified this session: Owner rulings via `sha256sum`, module spec via `sed -n` + line-number-referenced verbatim quotes, v0 contract via full-file `cat`, Stage A §5.1 via `sed -n`. Zero memory-recall presented as fact. Prior LT-2 forensic-correction lesson (BUILD_JOURNAL canon-first for historical claims) not applicable here (this refresh is forward-facing shape-mismatch analysis, not historical forensic). |
| **D-12** | **Experimentation at system level only** | PASS | This refresh document is a HAZARD-STOP surface, NOT an execution atomic. Zero deployment. Zero code. Zero test. Zero migration. Post-Owner-ruling, EAB-2 execution atomic will deploy **in force with known parameters** per §5.4 composed recommendation (or Owner's alternate composition). §23.2 gate-cell roster at Stage A remains pre-declared (11 pytest + 1 Playwright + 1 Jest cells per Stage A §2 band table); execution deferred pending ruling. **Zero observe-first · zero shadow phase · zero trial modes · zero staged proving.** The Parity 31→32 seal remains a sanctioned single event that lands in force when the ruling closes. |

---

*EAB-2 Stage-A Refresh · 2026-07-24 · Standing Rule v3 · D-11 canon-before-ruling · D-10 self-audit table attached · **HAZARD-STOP (a) fired · Parity 31→32 seal HALTED** · Owner ruling surface at §5 (3 loci · 8 total options with byte-level grounding · builder Tier-3 recommendation ε+α+γ at §5.4) · v0 contract + v0 snapshot + governance §§1..23 byte-identical · Parity 31 held · zero code touch this atomic.*
