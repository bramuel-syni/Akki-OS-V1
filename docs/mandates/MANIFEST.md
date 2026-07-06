# Mandates Manifest — Substrate-Drop v2 (post-A2, post-v3 supersession)

**Drop date:** 2026-07-01 (v1); **Substrate-Drop v2:** 2026-07-03 (v3 Engineering Spec + UI Spec v1 + UX Architecture v2 supersession).
**Authoring-direction inverted:** 2026-07-02T03:15Z.
**Norm ref:** BUILD_JOURNAL Substrate-Drop v1 Reconciliation section; ORCHESTRATOR_CONTINUITY §0 substrate-drop gate rule; DOCS-PASS 2026-07-02 §Item 8; Substrate-Drop v2 pass 2026-07-03.

## Authoring direction (LOAD-BEARING — canonical/derived inversion)

**The filed markdown under `/app/docs/mandates/*.md` is CANONICAL SOURCE.** The `.docx` files under `/app/docs/mandates/source/` are GENERATED PRESENTATION artefacts — not source of truth. Any edit-of-record on a canonical mandate lands directly in the markdown; the `.docx` is a re-render, not a re-authoring surface.

Consequences:
- **SHA-256 entries in this manifest hash the `.md` files.** Not the `.docx`. If the `.md` changes without a corresponding manifest update, `test_substrate_drop_gate` fails; that is the intended alarm.
- **Citable anchors going forward are markdown `§`-anchors** (heading-based line/section references into the `.md` file). The `.docx` may re-render with different page numbers, table breaks, or list positions; the `.md` is what invariants and audits cite.
- **The `.docx` files remain in `/app/docs/mandates/source/` for provenance only.** Deleting them is safe from a correctness standpoint (nothing depends on their SHA), but they are retained as historical artefacts of the pandoc-inbound path used at Substrate-Drop v1.
- **Rationale.** The docs-pass on 2026-07-02 revealed multiple settled-reality drift points where the shipped code diverged from spec prose (§10 ring-prefixed field names, §26 closed-count language, UX §14 remediation framing, northena §8 `stamp_audit` type). All were legitimate settlement to be reflected back into the specs. Under the earlier `.docx`-canonical direction, every such settlement would require re-rendering a `.docx`; under the markdown-canonical direction, the correction lands as a docs-pass. Substrate drops (v1 was pandoc-inbound) are the exception that installs a spec anew; ongoing settlement is a direct-markdown pass.

## Specs filed

| Filename (canonical `.md`) | SHA-256 (of the `.md`) | First received | Source URL (`.docx` provenance only) | One-line summary |
|---|---|---|---|---|
| `RMS_Product_Engineering_Spec_v3.md` | `af2e3cb2fccfd92278dedec725732ae1b5b48dff614fd6f7c8fbc805160d915a` | 2026-07-03T21:03Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/x6kge7ax_RMS_Product_Engineering_Spec_v3.md | RMS Product & Engineering Spec v3 — primary engineering brief; supersedes v2.1. Adds shape-responsive execution, ObjectiveRequest v2 additions, transform layer §6, off-menu refusal (§6.5), economics config, async contract, and §10 open decisions (owner-owned). V2 cumulative-disclosure arm closed-seam block appended 2026-07-04 (Housekeeping Pre-Flight). |
| `RMS_UI_Specification_v1.md` | `9053a4c451954cca1dc2f2b10216bef2058411a1911136581251e395d5bdcbf3` | 2026-07-03T21:03Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/380770m1_RMS_UI_Specification_v1.md | RMS UI Specification v1 — binding surface spec; **SUPERSEDED at 2026-07-05 by `RMS_UI_Specification_v2_1.md` per Owner ingestion**. SHA-256 refreshed at commercial-cut close 2026-07-06 to reflect the Owner-directed SUPERSEDED banner prepended at Part 1 ingest (2026-07-05). Row retained here until Part 3+ manifest re-authoring dispatch moves it to archive block. Figures and names remain illustrative only; §8 binding copy set is BINDING for reference lookups still pointing to v1. |
| `RMS_UX_Architecture_v2.md` | `e072fd307e00b207cd2a451791bc3650ad59f5f71b28ac5d4c04b1144b841d59` | 2026-07-03T21:03Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/7r848t68_RMS_UX_Architecture_v2.md | RMS UX Architecture v2 — experience rules; supersedes UX v1 (`RMS_UX_Architecture_Specification.md`). |
| `RMS_Solva_Specification.md` | `e38b0370eed0b065468072a0ab393a66d39760f87c4d12a64f7560b5f0e260b5` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/hzf43k78_RMS_Solva_Specification.docx | Solva Engine Spec v1.0 — two faculties (free reasoning + bound assertion boundary), the one-way seam. |
| `RMS_Targeta_Specification.md` | `7e0ca7a373684cf30ca39d6a9c98f3a59e57c29f8ce1179eac0cbef9e4086990` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/2815ktpv_RMS_Targeta_Specification.docx | Targeta Engine Spec v1.0 — deterministic eligibility core + objective-conditioned yield layer with two-arm admission gate. Post-A2 closed-seam unlock subsection appended. |
| `RMS_Mtafiti_Specification.md` | `664fb76680cd8b9e62cfeac084a9d7d9410122a26d692f873c0242b59c78a1da` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/uv828hz5_RMS_Mtafiti_Specification.docx | Mtafiti Engine Spec v1.0 — objective-blind census + two-layer measure + detect-versus-decide boundary. Post-A2 two closed-seam unlock subsections appended (V3 overlay, MEA source-standing). |
| `northena.md` | `ab0beeddf23c9530cc54c6ddd4255b4b3d0435df0d4c156d05de478e65af8345` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/m8l10dgh_RMS_Northena_Specification.docx | Northena Engine Spec v1.0 — canonical merged Mandate & Engineering Spec (supersedes `archive/northena_v1.0_predrop.md`). Post-A2 §8 `stamp_audit` typed as `Optional[Dict]` with intentional-design note + closed-seam unlock subsection appended. |

## Raw `.docx` provenance (historical, non-canonical)

All raw `.docx` files preserved at `/app/docs/mandates/source/<filename>.docx` from the Substrate-Drop v1 pandoc-inbound. Retained as historical artefacts; not used for integrity checks going forward.

## Archive

- `/app/docs/mandates/archive/northena_v1.0_predrop.md` — pre-drop Northena consolidation (retained for provenance; superseded by `northena.md`).
- `/app/docs/mandates/archive/RMS_Product_Engineering_Spec_v2.1.md` — pre-move SHA (lineage): `f983fc959d26054c27a9bd4832bce4d6fef59d403f2113f8ba8ed7a19c64f8dc`. Post-move SHA (with SUPERSEDED header): `510cc1a9f58138cf4753e907fdb68a1b0334b5336eff05db32a3c40071cf484b`. Superseded by `RMS_Product_Engineering_Spec_v3.md` on 2026-07-03.
- `/app/docs/mandates/archive/RMS_Interface_Specification.md` — pre-move SHA (lineage): `2bdebfca53957cb4a0b11929880f7ad45a86d1470551c4b2da17be0208f68985`. Post-move SHA (with SUPERSEDED header): `33084c83c594c899070df530150f78d95c1068d8d5b92b035417a08dd8603372`. Superseded by `RMS_UI_Specification_v1.md` on 2026-07-03. This was the G5b-era frontend mandate (surfaces + §11 response contract).
- `/app/docs/mandates/archive/RMS_UX_Architecture_Specification.md` — pre-move SHA (lineage): `4c5fc92703be5ab9b72da11936c7a02a1a38077791e6ab776592f99aed141898`. Post-move SHA (with SUPERSEDED header): `0a307cd8a8bb3714d58cb43fd079e12a9ef5e84984ec780dd29fc5d5d27fe6ad`. Superseded by `RMS_UX_Architecture_v2.md` on 2026-07-03.

Archive-lineage SHAs above are recorded as bullet items (not table rows) so `test_substrate_drop_gate` does not gate-verify them at top-level. Files remain on disk at `archive/` for provenance.
