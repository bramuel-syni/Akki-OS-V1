# Mandates Manifest — Substrate-Drop v1

**Drop date:** 2026-07-01
**Norm ref:** BUILD_JOURNAL Substrate-Drop v1 Reconciliation section; ORCHESTRATOR_CONTINUITY §0 substrate-drop gate rule.

This is the substrate-drop record: it lists every canonical spec required by phases G3/G4/G5/G6, with SHA-256 for tamper-detection and source URL for provenance. `test_substrate_drop_gate.py` reads this file and asserts (a) that every declared spec is present on disk under `/app/docs/mandates/`, (b) that its SHA-256 matches, and (c) that phase-scoped requirements per `phase_source_requirements.yaml` are all satisfied before that phase opens.

## Specs filed

| Filename | Source `.docx` SHA-256 | First received | Source URL | One-line summary |
|---|---|---|---|---|
| `RMS_Solva_Specification.md` | `f375b5acfe949682122c7a2f5954512acd262a25bb9c8db124d2995c2fa297db` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/hzf43k78_RMS_Solva_Specification.docx | Solva Engine Spec v1.0 — two faculties (free reasoning + bound assertion boundary), the one-way seam. |
| `RMS_Targeta_Specification.md` | `aae06440c6af3b72d870151faa79932f873ad3fa214403363d33e75500889fad` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/2815ktpv_RMS_Targeta_Specification.docx | Targeta Engine Spec v1.0 — deterministic eligibility core + objective-conditioned yield layer with two-arm admission gate. |
| `RMS_Mtafiti_Specification.md` | `8e4a7ece76bd5fcc3f0a9a0e1b019bc19a12bd5b69c46560a424350ff463a7db` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/uv828hz5_RMS_Mtafiti_Specification.docx | Mtafiti Engine Spec v1.0 — objective-blind census + two-layer measure + detect-versus-decide boundary. |
| `northena.md` | `74c4a5ccb74de5ca26f05b5269153846af72f6b60cad2903486b80a57fa1f355` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/m8l10dgh_RMS_Northena_Specification.docx | Northena Engine Spec v1.0 — canonical merged Mandate & Engineering Spec (supersedes `archive/northena_v1.0_predrop.md`). |
| `RMS_Product_Engineering_Spec_v2.1.md` | `9f956e470c9f06e36581f3d12413d5cfffc3ecd54dedecbfdb431a36cf2751f7` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/8wfxuske_RMS_Product_Engineering_Spec_v2.1.docx | RMS Product & Engineering Spec v2.1 — canonical parent that prevails on conflict; six frozen contracts; 14 system invariants. |
| `RMS_Interface_Specification.md` | `25653e46a815ddd7cd0b0a3454fbe543eb635eaf960695b2a2ffe206148d30ac` | 2026-07-01T15:54Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/pdd2qevw_RMS_Interface_Specification.docx | RMS Interface Spec v1.0 — single-entry routing; six user surfaces; §11 response contract with governance inline; realises UX Architecture Spec. |
| `RMS_UX_Architecture_Specification.md` | `88c487a51fce687e11697d384a04b092b70b80f05bd7e5e0ed0f9bce89bfa41d` | 2026-07-01T15:54Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/g46nz4k6_RMS_UX_Architecture_Specification.docx | RMS UX Architecture Spec v1.0 — experience architecture; six users + promises; three-lens trust model (unit/reasoning/audit joined by trace_id). |

## Raw `.docx` provenance

All raw `.docx` files preserved at `/app/docs/mandates/source/<filename>.docx`. SHA-256 above is over the `.docx` source (not the pandoc-converted `.md`), so future integrity checks can be run against the untouched original.

## Archive

- `/app/docs/mandates/archive/northena_v1.0_predrop.md` — pre-drop Northena consolidation (retained for provenance; superseded by `northena.md`).
