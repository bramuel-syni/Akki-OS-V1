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
| `RMS_UI_Specification_v2_1.md` | `ef6da4b498117608a3091033b5cfa43571ad8a7a38b5954cae7c4a1a698de5e2` | 2026-07-05 | (ingested from Owner 2026-07-05; no `.docx` provenance) | RMS UI Specification v2.1 — CANONICAL binding surface spec; supersedes v1 in full. Four consoles (Extraction/Compliance/Integration/Administration); Section 5.5 governed-extract API as machine boundary; Section 4 Compliance Console (was v1 Regulator/DPO §7); Section 7.1 Internal Reference Application (was v1 Ask Console §3); §11 migration map + §12 Sales Service stub. v2.1 removes ALL commercial attributes from the extractor per Owner ruling (2026-07-06). 176 paragraphs, 3 tables, 207 LoC. |
| `RMS_Build_Completion_Requirements_v1_4.md` | `ce5206c9e244fe58edb6824f785077c1c835bdf3f5b347f6a4fb98c036212524` | 2026-07-07 | (ingested from Owner 2026-07-05; v1.4.1 middle-dot glyph correction landed per E7 ruling on 2026-07-06; no `.docx` provenance) | RMS Build Completion Requirements v1.4 — CANONICAL unbuilt-work brief; supersedes v1.2. §3 engineering requirements per gap (§3.1-3.14); §5 sequencing; §12 commercial cut mandate with 14 requirement IDs (CUT-1..4 / PRES-1..3-ALT / MAN-1 / MAN-G1..G3 / BND-1..2). 325 paragraphs, 2 tables, 341 LoC. Manifest SHA refreshed 2026-07-07 to reflect E7 v1.4.1 middle-dot correction landing (Sub-stage 1 housekeeping — pre-existing drift from E7 amendment). |
| `RMS_UX_Architecture_v2.md` | `e072fd307e00b207cd2a451791bc3650ad59f5f71b28ac5d4c04b1144b841d59` | 2026-07-03T21:03Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/7r848t68_RMS_UX_Architecture_v2.md | RMS UX Architecture v2 — experience rules; supersedes UX v1 (`RMS_UX_Architecture_Specification.md`). |
| `RMS_Solva_Specification.md` | `e38b0370eed0b065468072a0ab393a66d39760f87c4d12a64f7560b5f0e260b5` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/hzf43k78_RMS_Solva_Specification.docx | Solva Engine Spec v1.0 — two faculties (free reasoning + bound assertion boundary), the one-way seam. |
| `RMS_Targeta_Specification.md` | `7e0ca7a373684cf30ca39d6a9c98f3a59e57c29f8ce1179eac0cbef9e4086990` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/2815ktpv_RMS_Targeta_Specification.docx | Targeta Engine Spec v1.0 — deterministic eligibility core + objective-conditioned yield layer with two-arm admission gate. Post-A2 closed-seam unlock subsection appended. |
| `RMS_Mtafiti_Specification.md` | `664fb76680cd8b9e62cfeac084a9d7d9410122a26d692f873c0242b59c78a1da` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/uv828hz5_RMS_Mtafiti_Specification.docx | Mtafiti Engine Spec v1.0 — objective-blind census + two-layer measure + detect-versus-decide boundary. Post-A2 two closed-seam unlock subsections appended (V3 overlay, MEA source-standing). |
| `northena.md` | `ab0beeddf23c9530cc54c6ddd4255b4b3d0435df0d4c156d05de478e65af8345` | 2026-07-01T15:39Z | https://customer-assets.emergentagent.com/job_build-metrics-10/artifacts/m8l10dgh_RMS_Northena_Specification.docx | Northena Engine Spec v1.0 — canonical merged Mandate & Engineering Spec (supersedes `archive/northena_v1.0_predrop.md`). Post-A2 §8 `stamp_audit` typed as `Optional[Dict]` with intentional-design note + closed-seam unlock subsection appended. |
| `RMS_SyniSense_Specification.md` | `8778b9e3ef632e67329dbb0bf0f925367e977e44c1af1be58838f4ec214fc52d` | 2026-07-15 | (assembly from on-disk audited surfaces · `docs/audits/engine_conformance_v1.md` + `backend/services/synisense/**` + frozen contracts; zero new design; OD-1/OD-2/OD-3 dispositions applied per FLAG 1 ruling 2026-07-15; discharges register v1.5 §4 G-12) | SyniSense Engine Spec v1.0 — the Shield: outbound LLM chokepoint · custody chain · de-identification pipeline · purpose validation as-built at the seam · key custody · module structure · 19 conformance rows · fifth engine mandate (parity with Solva · Targeta · Mtafiti · Northena). |

## Substrate-Drop v3 · Module Specs Landing (Owner Configuration Dispatch 2026-07-24 §4.STEP-3)

Owner-verbatim sanction (`docs/rulings/owner_configuration_2026-07-24.md` §4.STEP-3): *"File the 8 uploaded artifacts (Product & System Document · Connect · Registry · Extract · Govern · Prove · Team · Shared Components · User Stories) as .md under docs/mandates/module_specs/, authoring-direction .md-canonical per the standing inversion. SHA each into docs/mandates/MANIFEST.md; extend phase_source_requirements.yaml."*

**Landed 2026-07-24 · `.md`-canonical per Owner standing inversion.** Owner's phrase "8 uploaded artifacts" tallies as 9 filed `.md` files (Product & System Document + 6 module specs + Shared Components + User Stories = 9 files; the "8" count in Owner text corresponds to the 8 URLs surfaced, of which Product Doc file 1 is Product & System Document — filed as `akki_product_system_document.md`).

| Filename | SHA-256 | Landed | Source URL | Notes |
|---|---|---|---|---|
| `module_specs/akki_product_system_document.md` | `f3adc17c054d7ca1314b9d7aa270f7ec7e25fa773f3d4e3072ebf0af1c2edb8d` | 2026-07-24 | https://customer-assets-39nsmqrw.emergentagent.net/job_build-metrics-10/artifacts/asjwzsa8_Akki_Product_System_Document.docx | Product & System Document (pandoc-converted from Owner-supplied `.docx`; SHA matches prior v3 landing at `docs/product/akki_product_system_document_v3.md` — same source docx by content). |
| `module_specs/01_connect_module.md` | `4e0f2705e9fd8159bae44c737ed28a93c251ac37549ff32e8e18542fb96b0c28` | 2026-07-24 | https://customer-assets-39nsmqrw.emergentagent.net/job_build-metrics-10/artifacts/hq5mp901_01_Connect_Module.md | Connect Module user journeys — DPO / Data Engineer roles · Org Setup · Add Source · Manage Sources · Governance Sponsor / Co-Signer contacts. |
| `module_specs/02_registry_module.md` | `6c382dcbe7f9064bccff3ef607025653964bdca1c7843de4b1f4b78bceccc540` | 2026-07-24 | https://customer-assets-39nsmqrw.emergentagent.net/job_build-metrics-10/artifacts/dwb40284_02_Registry_Module.md | Registry Module user journeys — What You Hold landing · First Census + Estate Review · auto-trigger + debounce (rides OD-10). |
| `module_specs/03_extract_module.md` | `82348a163d5827da365f0d754221d0978e1e27ea5619b4c05688b85a531fbf91` | 2026-07-24 | https://customer-assets-39nsmqrw.emergentagent.net/job_build-metrics-10/artifacts/3dangofe_03_Extract_Module.md | Extract Module user journeys — Shape Objective · Commission · Model Acceptance · Extracted Intel · Analyst / Run Approver / Model Acceptor roles. |
| `module_specs/04_govern_module.md` | `a1f6c13a37a5f023f1239ff73828fdc3594f03dc5374b81e32cf4e23bcfbf8aa` | 2026-07-24 | https://customer-assets-39nsmqrw.emergentagent.net/job_build-metrics-10/artifacts/yiz8q0qb_04_Govern_Module.md | Govern Module user journeys — DPO Estate · Change-a-Rule · Destroy-Data · Release Review · Quarantine · Governance Setup succession (2-party Co-Signer + 3-party Sponsor incl. CEO). |
| `module_specs/05_prove_module.md` | `12b1bea55b056dbd6acf1f4dd177bbb40b899be0153e1281069b5eab2f0b5cc6` | 2026-07-24 | https://customer-assets-39nsmqrw.emergentagent.net/job_build-metrics-10/artifacts/m3swzgoz_05_Prove_Module.md | Prove Module user journeys — Ask · Answer Card · Walk-the-Proof (Level 1/2/3) · Draft Memo · Public Receipts (DPO-only · rides OD-9) · 3 refusal shapes (not-extracted-yet + gap-queue + estimated effort · evidence-can't-support · something-broke). |
| `module_specs/06_team_module.md` | `f043514f0512d5b695893fa346692e3457e74620de68cd92babf7f232908d0d0` | 2026-07-24 | https://customer-assets-39nsmqrw.emergentagent.net/job_build-metrics-10/artifacts/24fc2o4t_06_Team_Module.md | Team Module user journey — Manage Users · Master Admin promotion routed through DPO approval · Governance Co-Signer / Sponsor succession pointer to Govern. |
| `module_specs/07_shared_components.md` | `5c4b8b0076dc3c17ae4f8aaab851d27cd4fbd55c3c7526b820333be0ec230d0d` | 2026-07-24 | https://customer-assets-39nsmqrw.emergentagent.net/job_build-metrics-10/artifacts/ohngkgkf_07_Shared_Components.md | Shared Components — Ask Akki Drawer (global right-side drawer · header trigger from every module · same Answer Card structure as Prove) · Answer Card + refusal-shape component family = single shared-shell implementation per Owner STEP 5 structural directive. |
| `module_specs/08_user_stories.md` | `fdb4fc3bfc535ada59b37c4d361635059e736bce5f601fe4fc87c66a945355d2` | 2026-07-24 | https://customer-assets-39nsmqrw.emergentagent.net/job_build-metrics-10/artifacts/ucequ3z2_08_User_Stories.docx | User Stories — role-anchored `As a <role>, I can <action>, so that <benefit>` stories organized by module (pandoc-converted from Owner-supplied `.docx`). |

**Reconciliation audit:** `docs/audits/substrate_drop_v3_reconciliation_2026_07_24.md` (per-artifact CODE_IMPACT + CONFLICT rows + OD-8/9/10 minted at `docs/registers/owner_decisions_v1.md`).

**§4.STEP-3 zero-loss attest:** every succession attestation (Co-Signer 2-party · Sponsor 3-party incl. CEO) · every waiting period (Change-a-Rule 72h · Destroy-Data 24h · Team promotion DPO-approval) · every refusal shape (3 shapes: not-extracted-yet + gap-queue + estimated effort · evidence-can't-support · something-broke) · every receipt behavior (DPO-only generation · no-login verify · expiry · revoke · verification-log) · every notification category (Connect DPO sign-off · Govern approvals · Extract approvals · Team promotion · Prove Release Review) · every usage-rights enum (4-value per Connect Module) — all entered the audit intact.

**Prior CODE_IMPACT preview table** (dispatched last turn per Owner phrasing) **carries no evidentiary weight** per Owner Configuration Dispatch §4.STEP-3.


## Archive

- `/app/docs/mandates/archive/northena_v1.0_predrop.md` — pre-drop Northena consolidation (retained for provenance; superseded by `northena.md`).
- `/app/docs/mandates/archive/RMS_Product_Engineering_Spec_v2.1.md` — pre-move SHA (lineage): `f983fc959d26054c27a9bd4832bce4d6fef59d403f2113f8ba8ed7a19c64f8dc`. Post-move SHA (with SUPERSEDED header): `510cc1a9f58138cf4753e907fdb68a1b0334b5336eff05db32a3c40071cf484b`. Superseded by `RMS_Product_Engineering_Spec_v3.md` on 2026-07-03.
- `/app/docs/mandates/archive/RMS_Interface_Specification.md` — pre-move SHA (lineage): `2bdebfca53957cb4a0b11929880f7ad45a86d1470551c4b2da17be0208f68985`. Post-move SHA (with SUPERSEDED header): `33084c83c594c899070df530150f78d95c1068d8d5b92b035417a08dd8603372`. Superseded by `RMS_UI_Specification_v1.md` on 2026-07-03. This was the G5b-era frontend mandate (surfaces + §11 response contract).
- `/app/docs/mandates/archive/RMS_UX_Architecture_Specification.md` — pre-move SHA (lineage): `4c5fc92703be5ab9b72da11936c7a02a1a38077791e6ab776592f99aed141898`. Post-move SHA (with SUPERSEDED header): `0a307cd8a8bb3714d58cb43fd079e12a9ef5e84984ec780dd29fc5d5d27fe6ad`. Superseded by `RMS_UX_Architecture_v2.md` on 2026-07-03.
- `/app/docs/mandates/RMS_UI_Specification_v1.md` — retained on-disk at current path (NOT relocated under `archive/`; Owner directive at Part 1 ingest was to mark SUPERSEDED at file top, not delete or move). SHA-256 `9053a4c451954cca1dc2f2b10216bef2058411a1911136581251e395d5bdcbf3` (post-SUPERSEDED-banner state, prepended by Owner Part 1 dispatch, 2026-07-05). **Status: SUPERSEDED-BY-v2.1 as of 2026-07-05; NO-LONGER-CONSUMED as of conformance-map dispatch 2026-07-06 — all phase pointers redirected to `RMS_UI_Specification_v2_1.md` in `phase_source_requirements.yaml`.** Retained for archive/reference; not gate-verified going forward (archive-block bullet, not `Specs filed` table row).

Archive-lineage SHAs above are recorded as bullet items (not table rows) so `test_substrate_drop_gate` does not gate-verify them at top-level. Files remain on disk at `archive/` (or in-place for v1 per Owner directive) for provenance.

## Rate ledger cross-reference (Owner post-CD housekeeping, 2026-07-10)

Downstream Stage A authors: consult `/app/docs/governance/tiered_ruling_model.md` §6 for the codified rate ledger. The ledger is the authoritative source; this block is a wayfinding index only.

| Rate class | Rate | Applies to | Ledger section |
|---|---:|---|---|
| Backend Pytest shared-helper amortised | 12 LoC/cell | Classic Pytest cells with shared fixtures | §6.1 |
| Backend endpoint impl 3-share amortised | 40 LoC/endpoint | FastAPI endpoint additions (min 3-share) | §6.2 |
| Backend service module standalone | 100 LoC/module | New service modules | §6.3 |
| Frontend Jest structural fallback | 16 LoC/cell | Frontend structural Jest cells | §6.4 |
| Playwright chromium data-testid | 9 LoC/cell | Chromium data-testid cells | §6.5 |
| Frozen Pydantic contract class | 60 LoC/class | New frozen contracts (parity++) | §6.6 |
| Frozen contract snapshot JSON | ~155 LoC/snapshot | New snapshot files (parity++) | §6.7 |
| Verbatim-carrier overhead | ~100-150 LoC/carrier | Owner-verbatim ruling/posture text in modules | §6.9 |
| AST/reflection gate class | ~40 LoC/cell | AST walker + whitelist + violation formatter | §6.10 |
| Async httpx auth-overhead cell | ~25 LoC/cell | Async httpx cells with 3+ auth-overhead lines | §6.11 |

**Watched list:** §6.8 (empty as of 2026-07-10; new watched classes admitted per Ruling 5 on first observation).

**Metric-verdict discipline:** §9 — bands derived and verdicts rendered in raw LoC. Alternate-unit disclosures welcome; unit change proposed at next Stage A.

**9.2 split ruling:** §10 — 9.2a (real perception workers, venue-agnostic build) vs 9.2b (deployment + census-at-scale + BM-V, gated on 9.2-OWN-1..3).
