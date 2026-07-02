# Fixture Substrate v1 — REJECTED

**Rejection date:** 2026-07-01 (end of Substrate-Drop v1 phase; user directive at G3 opening).
**Rejection path chosen:** Path 1 — Reject. On-disk stays canonical. Frozen contract holds.

## Rejected artifacts

| File | SHA-256 | Size |
|---|---|---|
| `generate_fixture.incoming.py` | `7c85a8c771fb6d91e766be45099fb44dec1e230a3ab86a13935d16a9e81b7460` | 17,628 bytes |
| `fixture.incoming.json` | `e3df6920b8213bcc0b9f94bb777e46eac285f84356224f05a6a32d47b32cf03e` | 46,513 bytes |

## Rejection rationale

### 1. Contract conformance FAIL

Incoming `fixture.incoming.json` fails frozen `NormalizedUnit` contract conformance: **0/19** units parse against `contracts.five_rings.NormalizedUnit` (on-disk 19/19 pass). Incoming uses ring-prefixed field naming (`ring1_provenance / ring2_signal / ring3_relational / ring4_reextraction / ring5_defensibility`) and adds top-level fields (`content: str`, `unit_type: str`, `freshness_stamp`, `_fixture`) absent from the G0-frozen contract shape. Adopting the incoming shape would require **mutating** the frozen `NormalizedUnit` contract — a HAZARD-STOP (a) cascade through `LedgerRow.artifact_ref`, Layer C stamp emission, and V1/V3 harnesses (see `docs/audits/substrate_drop_v1/fixture_substrate_diff.md` §4).

### 2. No source spec mandates the incoming shape

All 4 engine reconciliations + 1 interface/UX reconciliation across Substrate-Drop v1 recorded **0 CODE_IMPACT**. None of the 7 filed source specs (Solva, Targeta, Mtafiti, Northena, Product Spec 2.1, Interface, UX Architecture) demands the ring-prefixed field naming. Therefore adopting the incoming shape would produce a contract that **disagrees** with the source specs — objectively wrong.

### 3. Zero adversarial-coverage delta

Coverage-delta assessment (documented in the reply to user 2026-07-01T15:56Z):
- **Unit count**: 19 vs 19 (identical).
- **Adversarial classes**: 13 vs 13 (byte-for-byte identical set — code-switching, genre-boundary ambiguity, native-ad-as-news, contested chain 4-unit, authority-blind genre ceiling, source-standing lowering, sub-30s + overlapping speakers, cross-modal conflict, recency skew, drama-as-fact, malformed ingestion, opinion-dominant distribution, clean positive control).
- **Fixture generator logic**: no novel adversarial patterns; only refactor helpers (`defensibility_class`, `score_vector`) codifying policy already implicit in the on-disk generator.
- **`_fixture` field**: per-unit metadata re-representation of on-disk `provenance.context.author_labels` — same information, different location.
- **Verdict**: incoming would NOT give the current CI meaningfully stronger adversarial coverage.

### 4. Forward-looking `structural_signature` primitive carried forward

The one genuinely-new signal in the incoming fixture — `freshness_stamp.structural_signature` (a 16-hex sha256 of unit content) — maps to Mtafiti Spec §13 L2-freshness mechanism. It has no consumer in shipped G0..G2a code (Mtafiti is G4). **Carried forward as G4-scope reminder** in `docs/g4_prep/mtafiti_prep.md` (`## G4 TODO — structural_signature primitive`). At G4 opening, on-disk `generate_fixture.py` will be surgically extended to emit this field per unit; contract additions (if any) must go through frozen-schema re-bless.

## Provenance and preservation

Both rejected files remain on disk at `rejected/` for provenance / future-reference. They are NOT registered in `docs/lift_manifest.json` (rejected substrate is not lifted substrate — see BUILD_JOURNAL 2026-07-01T15:54Z Substrate-Drop v1 Addendum, T5 accounting note).

## Cross-references

- `docs/audits/substrate_drop_v1/fixture_substrate_diff.md` — full diff report + contract-conformance table + tests-would-break assessment.
- BUILD_JOURNAL `## Substrate-Drop v1 Addendum` — phase-close entry recording the HAZARD-STOP (a) surface.
- BUILD_JOURNAL `## Fixture Substrate v1 — Rejected` — this rejection's journal entry (G3 opening).
- `docs/g4_prep/mtafiti_prep.md` — `## G4 TODO — structural_signature primitive` (carry-forward).
