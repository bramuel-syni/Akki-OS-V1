# Solva scope from source — G3 pre-code note

**Source:** `/app/docs/mandates/RMS_Solva_Specification.md` (SHA-256 `f375b5ac…297db` in `MANIFEST.md`).
**Parent cross-reference:** `/app/docs/mandates/RMS_Product_Engineering_Spec_v2.1.md` §23.
**Freshness:** all 7 specs classified CURRENT at `docs/audits/g3_precondition/spec_freshness_check.md`.
**Discipline:** source wins. HAZARD-STOP (H-a1) / (H-a2) checks performed against frozen contracts BEFORE any code.

## 1. Two-faculty split (source §5, §7, §8)

- **Reasoning faculty (FREE — five stages):** *Frame → Candidate → Tension → Probability → Reflection.*
  - Stage 1 **Frame**: establishes the question and the relevant slice of the Normalized tier.
  - Stage 2 **Candidate**: proposes the units and compositions that could answer it.
  - Stage 3 **Tension**: surfaces contradiction, corroboration, retraction among candidates (reads Ring 3 edges); does not average them away.
  - Stage 4 **Probability**: weighs the candidates toward the best-supported conclusion.
  - Stage 5 **Reflection**: judges soundness and sufficiency; identifies the load-bearing units; composes the conclusion.
- **Assertion boundary (BOUND — one function):** deterministic floor computation over the load-bearing units' governed classes.
- **The seam is one-way:** `assertion.py` does NOT import from `reasoning/`; `reasoning/` does NOT import from `assertion.py` nor return a class.

## 2. `conclusion_class` boundary signature (source §10)

Source §10 declares verbatim:
```python
CLASS_ORDER = {'non_factual': 0, 'utterance': 1, 'fact': 2}
INV_ORDER = {0: 'non_factual', 1: 'utterance', 2: 'fact'}

def conclusion_class(load_bearing_units) -> str:
    floor = min(CLASS_ORDER[u.defensibility_class] for u in load_bearing_units)
    return INV_ORDER[floor]
```

Verified: input is `load_bearing_units` (a sequence); output is a class name (`str` — one of `{'fact', 'utterance', 'non_factual'}`, drawn from `DefensibilityClass` frozen enum in `contracts/five_rings.py`). **NO confidence parameter. NO probabilistic term. NO other input.** Signature is the guard: laundering is unrepresentable.

- **Return typing decision:** the G3 impl types return as `DefensibilityClass` (the frozen enum), not raw `str`. Source uses `str` in the illustrative snippet, but `DefensibilityClass` is the frozen G0 enum for Ring 5 class values (source §11 confirms: "class enum against qualification_matrix@v0 / five_rings@v0 Ring 5") — enum is the stricter form of the source's `str`, sub-typed to `DefensibilityClass` for stronger static assurance without loss of behavioural equivalence.
- **Signature invariant test** freezes `parameters = (load_bearing_units,)`, `return annotation = DefensibilityClass`, no other params.

## 3. Ring 5 class enum — HAZARD-STOP (H-a1) check

Source §10 CLASS_ORDER = `{non_factual, utterance, fact}` (3 values).
Frozen `contracts/five_rings.py::DefensibilityClass` = `{FACT, UTTERANCE, NON_FACTUAL}` (3 values, str-valued Enum, values match verbatim).

- Source enum set = `{'non_factual', 'utterance', 'fact'}`.
- Frozen enum set = `{'non_factual', 'utterance', 'fact'}` (via `.value` attributes).
- **Set-membership check: EXACT MATCH.**
- **(H-a1) NOT RAISED.**

Cross-reference: Product Spec 2.1 §15 (Ring 5 — Defensibility) line 476 declares `defensibility_class: fact | utterance | non_factual` verbatim; §31 invariants preserve this triple. Coherent.

## 4. Layer C convergence obligations (source §12 + Product Spec 2.1 §C, §11–§15)

Layer C's job at G3:
- **Normalize** modality-native output (Layer B perceptions) into modality-neutral `NormalizedUnit`s (per `five_rings@v0`). ALREADY PRESENT in `services/layer_c/aggregator.py` at G0.5 discipline.
- **Compute relational edges** — Ring 3 (multi-unit corroboration / contradiction / retraction). Currently empty (`RelationalRing()`); this is G3 work IF a source spec obligation binds it here. Source §8 Tension stage says: *"reads Ring 3 edges"*. Ring 3 must be populated before Tension can read it — but that population is Layer C convergence work at G3-adjacency. **Deferred to G3 minimally: retain current empty `RelationalRing()` at Layer C; Solva `tension.py` treats empty edges as "no tension surfaced" (a correct read).** Full Ring 3 population lands at G4/G5 when multi-unit runs generate real edge material.
- **Stamp Ring 5** — currently done in `aggregator.py` as declaration-baseline. Solva `stamp.py` at G3 supplies the *wide-bar-mode* refinements per source §12: "judges which refinements to preserve and emits the Ring 5 defensibility stamp per unit". Existing Layer C stamps stay; Solva `stamp.py` adds a preserve-judgment overlay function callable at convergence-time.
- **Signal-ring conformance**: Every convergence output MUST validate that any `SignalRing` it emits has `dimensions` whose KEYS are a subset of the frozen `signal_ring_dimensions@v0` catalogue for that modality. G0.5 Layer C emits `dimensions={}` (trivially subset). G3 adds an explicit `assert_signal_ring_conformant()` guard callable at convergence-time.

Hand-off: Layer C convergence → Solva reasoning stage 1 (Frame). Solva reads `NormalizedUnit`s via `contracts.five_rings` — read-only. No mutation.

## 5. Signal-ring dimensions — HAZARD-STOP (H-a2) check

Frozen `signal_ring_dimensions@v0` snapshot content (verified 2026-07-01):
```json
{
  "catalogue": {
    "audio":     ["prosody", "vocal_emphasis", "affect_valence", "affect_arousal", "speech_rate", "pause_density"],
    "video":     ["visual_emphasis", "scene_change_density", "framing_markedness"],
    "image":     ["visual_emphasis", "composition_markedness"],
    "text":      ["lexical_intensity", "stance_intensity", "hedging_density"],
    "composite": []
  },
  "rev": "v0"
}
```

Solva spec references:
- Line 118 (§6.2 or table row): *"Judge which signal descriptors, relational edges, and defensibility refinements to preserve"* — abstract reference; no dimension list declared.
- No specific signal_ring dimension enumeration anywhere in the Solva spec.

Product Spec 2.1 §12 declares the dimension list verbatim (lines 399–402): audio (6 dims), video (3 dims), image (2 dims), text (3 dims), composite (0). **EXACT MATCH with frozen snapshot.**

- **Dimension-set diff: NONE.**
- **(H-a2) NOT RAISED.**

## 6. Trace integration path (source §13 + §11)

- Every extraction-time judgment produces a `SolvaTrace` carrying `{trace_id, stages, load_bearing, computed_class, conclusion}`.
- Source §13 declares `SolvaTrace` as `@dataclass(frozen=True)` — Python-frozen dataclass, **NOT** a Pydantic contract-grade snapshot. Distinction: `SolvaTrace` is code-frozen but not schema-registered in the six frozen contracts. Per Solva reconciliation §10: "Solva does not introduce a new frozen contract at G3 that appears in the six".
- **Flow:** `enforce` → assembles `SolvaTrace` → serialize to `dict` → hand to Northena `services/northena/ledger.py::absorb_solva_trace(run_id, trace_dict)` helper → written into `LedgerRow.stamp_audit` (already `Optional[Dict]` — no contract change needed).
- Cross-reference: source §13 "Solva → Ledger (via stamp-audit): Refusal/decision audit; absorbed by Northena."

## 7. Invariants — 9 (source §17, canonical count per Substrate-Drop v1)

Source §17 lists **9 invariants**. G3 landing:

| # | Invariant (abbrev.) | Landing shape at G3 | Test |
|---|---|---|---|
| 1 | Solva reasons; never extracts (issues ops, interprets results) | Reasoning stages emit reasoning artifacts; stamp.py never runs operator primitives | `test_solva_never_extracts` |
| 2 | Two faculties (free reasoning + bound assertion) with one-way seam | `assertion.py` does not import `reasoning/`; `reasoning/` does not import `assertion.py`; parametrized isolation test | `test_reasoning_faculty_isolation` |
| 3 | Class = floor over load-bearing units' classes; reasoning strength not an input | `conclusion_class(load_bearing_units) -> DefensibilityClass`; signature-invariant test | `test_conclusion_class_signature` + `test_class_is_floor_over_load_bearing` |
| 4 | Utterance-class asserted as "was stated", never fact | `assert_conclusion` distinguishes `Assertion(claim, klass='fact')` vs. `Assertion(stated_form(text), klass='utterance')` | `test_utterance_never_asserted_as_fact` |
| 5 | Solva identifies load-bearing; boundary computes class from their pre-existing classes | `load_bearing.py::load_bearing()` returns units only, no class decision | (behavioural test integrated in boundary tests) |
| 6 | Floor + Matrix verdict read-only to Solva | `enforce.py` reads through `FloorSpec` + `MatrixHandle` handles; no mutation call sites | (test asserts no `.model_copy` or setattr on FloorSpec) |
| 7 | Below-floor conclusion refused with structured reason | `enforce.py` returns `Refusal(reason='below_defensibility_floor', ...)` | `test_refuse_below_floor` |
| 8 | Every judgment produces a trace | Pipeline test asserts one Ledger stamp_audit entry per full run | `test_solva_trace_ledger_integration` |
| 9 | Solva governs depth only; three axes never collapsed | N-INV-11 orthogonality grep continues to enforce; import assertion for Solva→Northena boundary | (extends N-INV-11) |

## 8. Product Spec 2.1 §-anchored obligations satisfied at composition-time

- **§23** (Solva parent behavioural description) — MATCH; the G3 build realises §23 in full.
- **§31 invariant #1** (Every unit of intelligence carries a complete Ring 5 defensibility stamp) — Layer C stamps Ring 5 at G0.5 (declaration baseline); Solva `stamp.py` at G3 emits preserve-judgment refinements at convergence.
- **§31 invariant #2** (Two axes never collapsed at unit level — utterance vs. fact) — enforced by boundary's floor computation.
- **§31 invariant #3** (Governed Matrix verdict) — Solva reads Matrix through `MatrixHandle`, never sets.
- **§31 invariant #4** (Powerful-part-walled principle) — reasoning strength walled from assertion class; `conclusion_class` signature is the guard.
- **§31 invariant #5** (Three governors on orthogonal axes) — Solva governs depth only; N-INV-11 grep-guard continues.
- **§31 invariant #10** (Reproducibility via temperature=0) — reasoning-stage LLM calls (permitted per brief) MUST use `extraction_params@v0` temperature=0 discipline. Reasoning stages at G3 in this pass are code-only (no LLM calls yet); LLM binding is a G3+ implementation choice bounded by this invariant. Journal explicitly.
- **§31 invariant #14** (Gates have certain fallback) — Solva refuses below floor with structured reason (`Refusal`); fallback is refusal-with-reason, not silent downgrade.

## Non-hazard notes

- **`services/solva_depth/admit_assist.py`** (G2a-shipped) is the Northena-side admit-assist shim (per Northena spec §9). It stays at its current location. Source §7 module layout does not list it, but Solva reconciliation §4 already ratified this: it's Northena's caller-side shim, not Solva-internal. G3 build sits alongside it.

- **Reasoning stages as separate files vs. single `reasoning.py`**: source §7 uses single `reasoning.py`; G3 phase brief step 3 specifies `services/solva/reasoning/` package with one file per stage. Chosen: **5-file package at `services/solva_depth/reasoning/`** — behaviourally equivalent, structurally closer to brief's parametrized isolation-test discipline, and satisfies source §8 stage enumeration verbatim.

## Ready-to-code checklist

- [x] Source read end-to-end.
- [x] `conclusion_class` signature identified verbatim.
- [x] H-a1 (Ring 5 enum): NOT RAISED (set-membership match).
- [x] H-a2 (signal_ring dims): NOT RAISED (dimension-set match).
- [x] Trace integration path identified; no frozen-contract mutation required.
- [x] All 9 invariants mapped to landing shape + test names.
- [x] All Product Spec 2.1 §31 obligations satisfied at G3 composition-time.
- [x] Module layout finalised (source §7 shape + reasoning as 5-file package per brief).
