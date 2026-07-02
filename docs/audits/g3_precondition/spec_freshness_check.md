# Spec Freshness Check — G3 Precondition

**Timestamp:** 2026-07-01T16:30Z
**Discipline:** verify the 7 filed specs are the current regenerated forward-spec set — not superseded merged drafts. If any is STALE → HAZARD-STOP (c) equivalent.

## Method

For each of the 7 specs at `/app/docs/mandates/*.md`:
- Header inspection (version marker, "elaborates X" / "consistent with X" / "supersedes X" language, prepared-by date).
- Status-section inspection (last-page closing status: "specification is complete" vs. "draft" / "merged" / "predecessor").
- Cross-reference against `MANIFEST.md` (SHA-256 provenance from `.docx` source).
- Cross-reference against `BUILD_JOURNAL` Substrate-Drop v1 entries.

## Per-spec verdict

| # | Spec (filename) | Version | Header claim | Status | Prepared date | SHA-256 known? | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | `RMS_Solva_Specification.md` | v1.0 | "elaborates the Product & Engineering Specification v2.1 (§23), which prevails on conflict" | "specification is complete" | July 2026 | ✅ `f375b5ac…297db` | **CURRENT** |
| 2 | `RMS_Targeta_Specification.md` | v1.0 | "elaborates the Product & Engineering Specification v2.1 (§25), which prevails on conflict" | "specification is complete" | July 2026 | ✅ `aae06440…89fad` | **CURRENT** |
| 3 | `RMS_Mtafiti_Specification.md` | v1.0 | "elaborates the Product & Engineering Specification v2.1 (§24), which prevails on conflict" | "specification is complete" | July 2026 | ✅ `8e4a7ece…a7db` | **CURRENT** |
| 4 | `northena.md` | v1.0 | "elaborates the Product & Engineering Specification v2.1 (§22), which prevails on conflict" (supersedes `archive/northena_v1.0_predrop.md` — supersession is documented) | "specification is complete" | July 2026 | ✅ `74c4a5cc…f1355` | **CURRENT** |
| 5 | `RMS_Product_Engineering_Spec_v2.1.md` | v2.1 | "the canonical parent; prevails over any engine specification on conflict" | "canonical parent specification" | July 2026 | ✅ `9f956e47…751f7` | **CURRENT** |
| 6 | `RMS_Interface_Specification.md` | v1.0 | "consistent with the UX Architecture Specification and the Product & Engineering Specification v2.1" | "specification is complete" | July 2026 | ✅ `25653e46…d30ac` | **CURRENT** |
| 7 | `RMS_UX_Architecture_Specification.md` | v1.0 | "consistent with the Product & Engineering Specification v2.1, which prevails on conflict" | "specification is complete" | July 2026 | ✅ `88c487a5…fa41d` | **CURRENT** |

## Version-coherence check

- All 5 engine/interface/UX specs declare v1.0.
- Product Spec declares v2.1 (parent, superseded v2.0 references in earlier planning docs — this is the CURRENT set per user's Substrate-Drop v1 correction).
- All 4 engine specs cite Product Spec v2.1 as parent-that-prevails. Consistent.
- Interface Spec + UX Spec both cite v2.1. Consistent.
- Northena spec supersession chain documented: `archive/northena_v1.0_predrop.md` retained for provenance; canonical `northena.md` is current.
- No "merged draft", "working draft", "consultation copy", or supersession-of-current markers in any spec header.
- All prepared-dates: July 2026. Coherent drop.

## Cross-reference against BUILD_JOURNAL

- Substrate-Drop v1 base entry (2026-07-01T15:39Z) filed 5 specs; addendum (2026-07-01T15:54Z) filed the remaining 2. All 7 SHA-256 provenance recorded in MANIFEST.md and matched by `test_substrate_drop_gate.py` (9/9 tests green including SHA-256 tamper-detection).
- Substrate-drop gate CI-enforced continues to pass at G3 opening — SHA-256 of all 7 source `.docx` files match MANIFEST.md within the current run.

## Verdict

- **CURRENT count: 7 / 7**
- **STALE count: 0 / 7**
- **HAZARD-STOP (c) equivalent: NOT RAISED.**

**Proceeding to STEP 1 (Solva scoping note) and STEP 2+ (Solva code) authorised.**
