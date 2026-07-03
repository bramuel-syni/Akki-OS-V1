# Mandates Manifest — Substrate-Drop v1 (post-A2, authoring-direction inverted)

**Drop date:** 2026-07-01
**Authoring-direction inverted:** 2026-07-02T03:15Z (this pass)
**Norm ref:** BUILD_JOURNAL Substrate-Drop v1 Reconciliation section; ORCHESTRATOR_CONTINUITY §0 substrate-drop gate rule; DOCS-PASS 2026-07-02 §Item 8.

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
| `RMS_Solva_Specification.md` | `e38b0370eed0b065468072a0ab393a66d39760f87c4d12a64f7560b5f0e260b5` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/hzf43k78_RMS_Solva_Specification.docx | Solva Engine Spec v1.0 — two faculties (free reasoning + bound assertion boundary), the one-way seam. |
| `RMS_Targeta_Specification.md` | `7e0ca7a373684cf30ca39d6a9c98f3a59e57c29f8ce1179eac0cbef9e4086990` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/2815ktpv_RMS_Targeta_Specification.docx | Targeta Engine Spec v1.0 — deterministic eligibility core + objective-conditioned yield layer with two-arm admission gate. Post-A2 closed-seam unlock subsection appended. |
| `RMS_Mtafiti_Specification.md` | `664fb76680cd8b9e62cfeac084a9d7d9410122a26d692f873c0242b59c78a1da` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/uv828hz5_RMS_Mtafiti_Specification.docx | Mtafiti Engine Spec v1.0 — objective-blind census + two-layer measure + detect-versus-decide boundary. Post-A2 two closed-seam unlock subsections appended (V3 overlay, MEA source-standing). |
| `northena.md` | `ab0beeddf23c9530cc54c6ddd4255b4b3d0435df0d4c156d05de478e65af8345` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/m8l10dgh_RMS_Northena_Specification.docx | Northena Engine Spec v1.0 — canonical merged Mandate & Engineering Spec (supersedes `archive/northena_v1.0_predrop.md`). Post-A2 §8 `stamp_audit` typed as `Optional[Dict]` with intentional-design note + closed-seam unlock subsection appended. |
| `RMS_Product_Engineering_Spec_v2.1.md` | `f983fc959d26054c27a9bd4832bce4d6fef59d403f2113f8ba8ed7a19c64f8dc` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/8wfxuske_RMS_Product_Engineering_Spec_v2.1.docx | RMS Product & Engineering Spec v2.1 — canonical parent that prevails on conflict; extensible frozen contract registry (see §26; founding six + additions); 14 system invariants. Post-A2: §10 field names flattened to frozen contract shape; §26 extensibility framing; V2 cumulative-disclosure closed-seam unlock subsection appended; invariant #6 authoring-direction convention documented (canonical `.md`, generated `.docx`). |
| `RMS_Interface_Specification.md` | `2bdebfca53957cb4a0b11929880f7ad45a86d1470551c4b2da17be0208f68985` | 2026-07-01T15:54Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/pdd2qevw_RMS_Interface_Specification.docx | RMS Interface Spec v1.0 — single-entry routing; six user surfaces; §11 response contract with governance inline; realises UX Architecture Spec. Post-A2 Unified Refusal Taxonomy addendum appended (5 refusal paths + HTTP body-discriminator semantic + 3 render paths). |
| `RMS_UX_Architecture_Specification.md` | `4c5fc92703be5ab9b72da11936c7a02a1a38077791e6ab776592f99aed141898` | 2026-07-01T15:54Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/g46nz4k6_RMS_UX_Architecture_Specification.docx | RMS UX Architecture Spec v1.0 — experience architecture; six users + promises; three-lens trust model (unit/reasoning/audit joined by trace_id). Post-A2 §14 refusal-below-floor remediation framing updated to actor-appropriate actions (lower floor / narrow objective). |

## Raw `.docx` provenance (historical, non-canonical)

All raw `.docx` files preserved at `/app/docs/mandates/source/<filename>.docx` from the Substrate-Drop v1 pandoc-inbound. Retained as historical artefacts; not used for integrity checks going forward.

## Archive

- `/app/docs/mandates/archive/northena_v1.0_predrop.md` — pre-drop Northena consolidation (retained for provenance; superseded by `northena.md`).
