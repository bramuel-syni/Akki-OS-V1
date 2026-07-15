# Function-Promise Registry v1.0 · Consolidated from v0.md + v0.1..v0.5 supplements · 2026-07-14 · Ruling: docs/rulings/g2_rm_e1_to_e3_2026-07-14.md

**Version:** v1.0 · mechanical fold (RM-E1 α byte-carriage).
**Predecessor lineage (immutable · Standing Rule v3):**
- `docs/registry/function_promise_registry_v0.md` · SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0`
- `docs/registry/function_promise_registry_v0.1_supplement.md` · SHA `2822f99e0c20da6f8d02c1f33233965c90df37aeb6939e711da8df2ebd991092`
- `docs/registry/function_promise_registry_v0.2_supplement.md` · SHA `25c5dd5ac515b34a41584dd2b4ba4eab20eb0ae5d40d9022320761056555b79a`
- `docs/registry/function_promise_registry_v0.3_supplement.md` · SHA `8d4cd2ed9c4e802944517908424ba2297ac3b4dd5e0d2a8e6d54f6042e64a8e4`
- `docs/registry/function_promise_registry_v0.4_supplement.md` · SHA `d1fa1949a206d5fb73481864962f93efaa888a4ef4793efad82a53681fc3dc1b`
- `docs/registry/function_promise_registry_v0.5_supplement.md` · SHA `d2d0c5f4c37dcbe525ff99a757687d7ae81446cd738719341e2b7884d4ac778f`

**Ruling anchor:** `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md` (Owner-ratified RM-E1 α · RM-E2 α · RM-E3 α + advisory annotation).
**Fold discipline (RM-E1 α):** every promise-text field carries byte-identical from source; drift = HALT + logged in §D-drift for future amendment turn (never edited in-flight).
**Conservation posture:** zero new promises minted; 8 new R4 rows in §M all reuse existing v0.md §2 promises via foreign-key resolution (all target `PROM-S1-frozen-wire-contract`).
**Machine form:** `docs/registry/machine/registry.yaml` re-pinned to this file's SHA (STEP 7). v0.md + supplements remain readable by the parser for archaeological continuity; active MRR round-trip runs over v1 alone.

**Doctrine reference:** Registry Doctrine v1.0 §3.2 schema (11 mandatory fields) · §3.3 R4 · §3.5 archaeology · §14 additive-supplement pattern preserved.
**Governance stack:** Standing Rule v3 · Registry Doctrine v1.0 · Tiered-Ruling §14 additive-supplement clause · Tiered-Ruling Part IV §16 D-10 corrective (self-audit standing practice) · SQ-E1 γ cross-reference discipline · D-11 canon-before-ruling · D-7 scope fence.

---

## §v0-body — Function & Promise Registry v0 (verbatim carriage from v0.md)

_(All content below through §7 is verbatim from `docs/registry/function_promise_registry_v0.md` lines 12–307 · SHA `598a7ad4d326dd5c0fc003fe8091a52fd215fb63e76d5c04befd1aa4c25584b0`. RM-E1 α byte-carriage.)_


## §1. Doctrine reference + methodology

The Registry is populated per Registry Doctrine v1.0 §3.5 archaeology posture from the on-disk record. This v0 landing extracts:

- **Primary vein:** 25 verbatim "Promise-protected:" / "Promise protected:" lines across 7 Stage A proposals (2026-07-06 through 2026-07-10) plus the Registry Population Stage A meta-references. (Additional 16 hits in the Registry Population Stage A itself are meta-references — this phase's own reflexive gates, folded into §3 Registry rows here.)
- **Secondary vein 1:** 134 distinct named-gate identifiers from close reports · `[XX]-G[N]` · `[XX]-E[N]` · `[XX]-R[N]` · V1-G[N] patterns.
- **Secondary vein 2:** governor behaviors named in the 10 mandate documents under `/app/docs/mandates/` (RMS_Product_Engineering_Spec_v3, RMS_UX_Architecture_v2, RMS_UI_Specification_v1/v2.1/v2.2, RMS_Build_Completion_Requirements_v1_5, RMS_Mtafiti_Specification, RMS_Solva_Specification, RMS_Targeta_Specification, northena.md).
- **Secondary vein 3:** UI console guarantees under UI Spec binding copy (§3.1..§3.15 client-facing surfaces).

**Owner-ruled RP-E1 α + tie-break-toward-distinct** (2026-07-11): consolidation rule = ≥60% core-clause token overlap AND same governor + surface class → merge. Borderline cases keep promises DISTINCT (Q1 redundancy earns rent later; over-merge is silent). Every merge decision recorded in `consolidation_log_v0.md`.

**Owner-ruled RP-E3 α-amended** (2026-07-11): (i)∧(ii) → §3 function row; (i)∧¬(ii) → §5 Q3 gap finding, **never dropped**. Sub-steps of a named-and-tested behavior fold into parent row's `mandate` field.

**Owner-ruled RP-E4 α** (2026-07-11): `unknown` is the honest value for `cost` and (in permitted cases) `ladder_rung` where source does not evidence a specific rung. No builder-guessed values.

**Owner-ruled RP-E2 α** (2026-07-11): client-promise-touching Q2/Q3 findings publish verbatim in the deliverable with `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` markers. Zero builder-retirement in this phase.

**Owner rulings on all 11 findings** (2026-07-11 · post-close): **RULED · 11 of 11 applied** — dispositions recorded in `docs/rulings/registry_findings_01_to_11.md` (Owner verbatim carrier). Corrections applied to §2 (new `PROM-S1-external-scoped-access` from Q2-01) + §3.f (`ui.engineer.onboarding` re-attachment) + §4/§5 rows (per-finding `[RULED · …]` annotation). Defect D7 respected: gap-fill cells become candidates for future Owner-dispatched phases, NOTHING MORE. No code work dispatched.

---

## §2. Promise table — the small canonical anchor set

**Methodology preface (RP-E1 α + tie-break):** Two "Promise protected:" lines consolidate iff (a) their core promise-clause tokens overlap ≥60%, AND (b) both share the same governor + surface class. **Where the rule is borderline, keep the promises DISTINCT** — Owner-explicit tie-break disposition. Under-merge is self-corrected by doctrine §3.4 Q1 redundancy query at a future dispatched turn; over-merge is silent.

| promise_id | promise_text | client_facing? | protected_by | source_citations |
|---|---|---|---|---|
| PROM-S1-provable-envelope-inheritance | Answers, skills, and artifacts arrive with class, receipt, and refusal semantics intact — so the integrating app inherits provability instead of building it. | yes | 8 | doctrine §Part II S1 (Layer 0) · P9-E5 · AF-E1 |
| PROM-S1-external-scoped-access | External integrators see only their own assets, enforced server-side. BCR §3.9 EE-R2 verbatim: *"View scoping: an external_engineer sees Register / First call / Administer scoped to their own apps, keys, usage, and refusal health — and NEVER other parties' apps, estate contents, fleet, pricing, or any master-admin control."* BCR §3.9 EE-R4 verbatim: *"Every externally reachable endpoint enforces scope server-side — view-layer filtering alone fails review. Enforcement rides the existing B-1 scope primitive; no parallel mechanism."* | yes | 4 | BCR §3.9 EE-R2 line 240 · BCR §3.9 EE-R4 line 242 · 8-EXT close report EE-G2 · Q2-01 ruling 2026-07-11 (rulings/registry_findings_01_to_11.md §1) |
| PROM-S1-shield-single-source | The Shield is the single chokepoint for LLM invocation; no call site outside the Shield may import an LLM SDK — the swap seam is one module. | yes (via S1 integrity) | 3 | AF-E1 β · OB-E1 α · PH-E4 α |
| PROM-S1-refusal-taxonomy-closed | Refusal codes are a bounded 4-code set (`auth_missing` · `auth_expired` · `auth_scope_insufficient` · `auth_identity_mismatch_for_wizard_session`); infra 503s and runtime transients are NEVER routed via refusal envelope. | yes | 4 | P9-E5 · AF-E2 amended (Standing Disposition 2026-07-10) · PH-E3 α |
| PROM-S1-frozen-wire-contract | External parties consume a stable schema over time; frozen contracts are byte-identical; parity is attested at every close. | yes | 6 | V1-G7 · TF-E1 α · CD-E2 α · doctrine §Part VIII |
| PROM-S1-additive-versioning | New contracts land by additive versioning (v0 preserved byte-identical when v1 lands); parity bumps with the new snapshot; V1-G7 assertion set bumps with it. | yes | 2 | AS-E1 α · V1-G7 |
| PROM-S1-honesty-grammar-source-labels | Every value in a client-facing envelope carries its provenance source label; values not observed by the census carry a non-`census_observed` source label OR are null; NO fabricated values. | yes | 5 | CD-E1 α · 9.2a-E1 α · doctrine D-3 |
| PROM-S1-byte-verbatim-anchor-grounding | Every quantitative anchor in an LLM-synthesized advisory or answer must appear byte-verbatim in a Registry-read text; whole-envelope REJECT on any failure; gate NEVER patches prose. | yes | 3 | AF-E1 β · OB-E1 α · doctrine §Part IV D-3 D-5 |
| PROM-S1-no-semantic-scoring | Grounding gates are mechanical byte-substring checks; semantic scoring is FORBIDDEN. | yes | 3 | AF-E1 β cond 1 · OB-E1 α · doctrine D-3 |
| PROM-S1-registry-native-aggregate | A Combined-scope aggregate = Registry-exposed native (the Registry computes; the brief/answer quotes byte-verbatim); synthesis-time computation is FORBIDDEN. | yes | 2 | OB-E3 α · doctrine §Part VII |
| PROM-S1-class-honesty-render-time | Class-honesty is enforced at render time — no render path strips the advisory marker; no governed-response import path touches advisory content; namespace boundaries surfaced via distinct id prefixes. | yes | 4 | OB-E2 α × 3 seams · AS-G6 · TF-G9 · FR-G4 · AF-G6b |
| PROM-S1-runtime-transient-never-refusal | Runtime transients (llm_unavailable · llm_timeout · llm_parse_failure · grounding_reject) surface as sidecar telemetry with mechanical fallback arm; they are NEVER a refusal envelope. | yes | 2 | AF-E2 amended · OB-runtime-transient-precedent |
| PROM-S1-config-defect-fail-loud | Config defects (missing Emergent key · invalid key) fail loud 503 at startup; NEVER routed via refusal envelope. | yes | 1 | AF-E2 amended |
| PROM-S2-estate-onboarded-and-mapped | The Operator's estate is onboarded, mapped, and turned into qualified intelligence they can commit with confidence. | yes | 1 | doctrine §Part II S2 · BCR v1.5 §3.4 (housing) |
| PROM-S2-census-dimension-integrity | Census-dimension values are Registry-vocabulary iff the value appears in the disclosure_types/content_surface/etc. registry; hard-coded values not in the registry are honesty violations. | yes | 4 | CD-E1 α · CD-E2 α · CD-E4 α |
| PROM-S2-slice-freeze-at-commission | Slice selection at commission is frozen at wizard-lock time; downstream perception + composition run against the frozen slice; no silent slice-drift. | internal | 2 | TF-E2 α · 9.2a-E2 α |
| PROM-S2-shape-as-objective-reach-only | The "shape-as-objective" handoff pre-fills wizard REACH only; wizard mandatory-field flow untouched; the handoff never overrides operator commit decisions. | yes | 1 | OB-R4 · UI Spec v2.2 §3.7 |
| PROM-S2-fixture-census-sample-rules | Registry-live census requires 9.2b; until then, fixture-census demo is permitted with explicit AS-U2 fixture-notice on every rendered surface. | internal | 2 | AS-U2 · OB-R5 · UI Spec v2.2 §3.7 |
| PROM-S3-prove-any-operation | Compliance can prove any operation on demand — receipts, traces, and rule-source chains are surfaced end-to-end. | yes | 4 | doctrine §Part II S3 · P9-E5 · Seam-3 sub-stage 3 |
| PROM-S3-append-only-ledger | Northena's ledger is append-only; no in-place mutation; historical rows preserved byte-identical. | yes | 2 | doctrine northena.md · V1-G7 |
| PROM-S3-retention-held-class-no-delete | Retention respects held-class rules — no direct DELETE handlers over held rows; retention state visible via Compliance UI. | yes | 3 | AS-H1 · Phase 8 Stage B-5a · Seam-3 stage-A E7 |
| PROM-S3-audit-trail-immutable | Master Admin audit trail is immutable; every rule change carries ceremony (dual-control where required); rules-writer surface preserves rule-source chain. | yes | 2 | Phase 8 Stage B-5b · master-admin ruling |
| PROM-S3-brief-namespace-distinct-from-trace | Trace resolution and receipt resolution NEVER surface brief content; brief IDs use a distinct `brief_` namespace; `/api/solva/trace/{brief_*}` returns 404. | yes | 1 | OB-E2 α Seam-2 |
| PROM-S3-governance-doc-on-disk | Governance stack is on-disk canonical (Standing Rule v3); historical carriers immutable; amendments append (§12.2 supersession pattern). | yes | 3 | Standing Rule v3 · §12.2 supersession · Registry Doctrine v1.0 |
| PROM-S3-mechanical-audit-of-promotion | Container promotion (git SHA + build timestamp + parity) is verifiable via a live `/api/system/build_info` endpoint — the "promotion-not-rebuild" claim is mechanically attested. | yes | 1 | PH-R1 owner enhancement 2026-07-10 · PH-G5 |
| PROM-S3-frozen-contract-parity-attest | Readiness (`/api/readyz`) + build_info (`/api/system/build_info`) + V1-G7 test all read parity from ONE authoritative counter; the three surfaces cannot disagree. | yes | 1 | PH-E3 α · PH-G6 |
| PROM-S4-receipt-alone-suffices | Buyer receives intelligence products verifiable independently of Akki's live API — the receipt alone suffices to verify the artifact. | yes | 2 | AS-E1 α (OuterGateReceipt_v1) · doctrine §Part II S4 |
| PROM-S4-provenance-audit-integrity | Every artifact carries a receipt; orphan artifacts are prohibited (AS-B2); destructive disposition is a Tier-1 surface via Seam 3. | yes | 3 | AS-E4 α · AS-B2 · Seam-3 stage-A E7 |
| PROM-S4-artifact-signature-bound | Artifact + receipt are signature-bound; the buyer can verify signature independently. | yes | 1 | AS-E1 α β posture · Northena signing |
| PROM-S5-substrate-not-optimized-against | Akki's extraction and governance capacity as a substrate for future ventures; no platform function may cite S5 as sole anchor without Owner ruling. | no (internal / future) | 0 (registered, unbuilt) | doctrine §Part II S5 |
| PROM-registry-taxonomy-canonical | Every function belongs to SyniSense · Northena · Mtafiti · Targeta · Solva OR a named surface; no new top-level categories without Owner ruling. | no | 6 | doctrine §3.1 |
| PROM-registry-schema-conformance | Every function row populates all 11 §3.2 schema fields; `unknown` is legal only for `cost` (and per RP-E4 α for `ladder_rung` where source silent). | no | 1 | doctrine §3.2 R1 · RP-E4 α |
| PROM-registry-service-trace-integrity | Every promise cites at least one S1..S5 sentence + journey step; empty/invalid trace = D1 orphan finding. | no | 1 | doctrine R2 · RP-G4 |
| PROM-registry-rent-paying | The Registry itself is subject to §3.4 queries (Q1/Q2/Q3); if it stops retiring gates, finding gaps, or cheapening sequences over sustained time it is itself retired or restructured. | no | 1 | doctrine §3.6 · doctrine D-8 |
| PROM-fixture-refresh-source-of-truth | Multiple sources of truth for the same fact create disclosure fragmentation; the fixture is the seed for many downstream test-consumers — centralized source of truth is mandatory. | internal | 2 | FR-E2 · doctrine §Part IV D-8 |
| PROM-tf-transform-form-per-call-provisioning | Transform Forms per-call provisioning drives per-call scope enforcement + slice-freeze but is NOT an external wire contract on the query surface. | internal | 1 | TF-E3 |
| PROM-tf-class-with-claim-invariant | Class widening in disclosure-types is accommodated by additive versioned registry (`disclosure_types.v0.json` pattern); Literal freeze on class would force contract mutations. | yes | 1 | TF-E5 · Phase 8 Stage B-5b |
| PROM-9-2a-real-worker-provenance | A real ASR/diarization worker without pinned model provenance is a fabricated-claim risk; downstream telemetry attributes work to models; unlabeled attribution is fabricated. | yes | 2 | 9.2a-E1 α · doctrine D-3 |
| PROM-9-2a-mode-selection-evident | Perception mode selection (real vs mock, CPU vs GPU) is evident at read-time; a GPU-only code path leaking into CPU-mode CI would silently expose paths that aren't proven green. | yes | 1 | 9.2a-E2 α |
| PROM-9-2a-first-contact-reverification | The 9.2a first-contact rider closes an intentional first-contact re-verification loop; its semantics must be evident to reviewers. | internal | 1 | 9.2a-E3 α |
| PROM-9-2a-never-rule-v1-d1-raw-never-egresses | A real worker holding a long-lived reference to audio bytes IS the never-rule violation; structural proof required; convention insufficient. | yes | 1 | 9.2a-E4 α · governance §1.1 never-rule V1-D1 |
| PROM-ph-r1-secret-externalization | No secret value in the container image or in a repo-committed `.env` at production time; vault-class binding at deploy time. | yes | 2 | PH-E1 α · BCR §3.4 annex |
| PROM-ph-r1-fe-be-serve-separable | Frontend build is separable from backend serve at deploy time; multi-stage single image; deploy topology chooses how to serve. | yes | 1 | PH-E2 α · BCR §3.4 |
| PROM-ph-r1-readiness-parity-real | `/readyz` surface reflects TRUE frozen-contract parity, not a stale constant; readiness fails 503 if parity drifts. | yes | 1 | PH-E3 α · PH-G3 |
| PROM-ph-r1-llm-swap-shape-stable | The LLM swap seam is one module and its public shape is stable across provider swaps; call sites never change. | yes | 1 | PH-E4 α · BCR §3.4 annex |
| PROM-ui-single-ingress-ask-console | UI Spec v1 §3.1 · Ask Console is the `/` single-ingress landing surface for the platform's first-party reference application. | yes | 1 | UI Spec v1 §3.1 · doctrine §Part II Ask Console reclassification |
| PROM-ui-console-discoverability | From `/`, sibling consoles are discoverable via a nav menu without hiding auth-gated entries per role. | yes | 1 | Ask Console nav landing 2026-07-11 · Tier-3 hygiene |

**Promise count landed: 47** (46 at Registry Population close-landing + 1 added 2026-07-11 per Owner Q2-01 correction: `PROM-S1-external-scoped-access`). Doctrine target: "dozens, not hundreds." **Landed value is in the doctrine's target range.** Tie-break-toward-distinct posture applied 4 times in consolidation_log_v0.md — those 4 borderline pairs kept as 8 distinct rows.

---

## §3. Function rows (per governor) — §3.2 schema

### §3.a SyniSense (Shield · grounding · class-honesty · LLM boundary)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| synisense.shield.llm_single_source_boundary | SyniSense | Built to enforce that no non-Shield module imports an LLM SDK; the swap seam is one module (`llm_router.py`). | PROM-S1-shield-single-source | S1.call · S1.pass-receipts-through | `backend/services/synisense/shield/llm_router.py` + AST gate | AST/reflection walk | 1 cell · §6.10 rate class (attested at `test_no_direct_llm_calls_outside_shield`) | Contract-immutability at frozen envelope | 1 · Deterministic (AST walk) | Owner |
| synisense.shield.grounding_gate_answer_fluency | SyniSense | Built to REJECT the whole answer_text if any per-sentence structured anchor fails byte-verbatim substring against its unit_id or numeric verification. | PROM-S1-byte-verbatim-anchor-grounding · PROM-S1-no-semantic-scoring | S1.call | `backend/services/service_1/answer_grounding.py` | Runtime check + AST negative-scan for `sum/mean/statistics` | 13 cells (AF-G2a..d + AF-G3a..c + AF-G-Grounding-Fail) · §6.11 rate class | AF-G-Grounding-Fail (green) · AF-G-E1-No-Semantic-Scoring | 1 · Deterministic + rung-4 upstream synthesis | Owner |
| synisense.shield.grounding_gate_opportunity_briefs | SyniSense | Built to REJECT any brief where a quantitative anchor's value fails byte-verbatim against its Registry-read reference. Whole-brief reject on any failure. | PROM-S1-byte-verbatim-anchor-grounding · PROM-S1-registry-native-aggregate | S1.call (as briefs are advisory to S1's app-facing surface) | `backend/services/opportunity_briefs/brief_grounding.py` | Runtime check + AST no-synthesis-compute | OB-G1 · OB-G-Grounding-Fail · OB-G-E3-No-Synth-Compute · §6.11 | 1 · Deterministic + rung-4 upstream | Owner |
| synisense.shield.fluency_synthesizer | SyniSense | Built to compose the fluent `answer_text` behind the Shield chokepoint using Sonnet 4.6 via Emergent LLM key; caller cannot bypass. | PROM-S1-shield-single-source · PROM-S1-runtime-transient-never-refusal | S1.call | `backend/services/synisense/shield/fluency_synthesizer.py:L182` | Runtime chokepoint + AST single-source (piggyback) | AF-G6a · §6.11 · 4 async cells | 4 · Frontier LLM (with mechanical fallback per AF-E2 amended) | Owner |
| synisense.shield.brief_synthesizer | SyniSense | Built to compose the brief text behind the Shield chokepoint using Sonnet 4.6 via `_provider_for("analytical")` reuse of Phase 7 Stage B-2 seed. | PROM-S1-shield-single-source · PROM-S1-runtime-transient-never-refusal | S1.call (advisory to S1's app-facing) | `backend/services/synisense/shield/brief_synthesizer.py:L116` | Runtime chokepoint | OB-G1 async cells · §6.11 | 4 · Frontier LLM (Registry-anchor grounding gate mechanically fallback) | Owner |
| synisense.shield.per_sentence_anchor_map | SyniSense | Built to produce `{prose, per_sentence: [{sentence_text, unit_ids}]}` structured mapping so the grounding gate runs anchor-by-sentence, not fuzzy match. | PROM-S1-byte-verbatim-anchor-grounding | S1.call | `backend/services/synisense/shield/fluency_synthesizer.py` (structured output block) | Runtime schema validate | AF-E1 β per-sentence structured mapping cells | 4 · Frontier LLM (structured output) | Owner |
| synisense.shield.data_blind_prompt_template | SyniSense | Built to attest LLM prompt templates never carry secret env vars, credentials, or masked data. | PROM-S1-shield-single-source · governance §8 | S1.call | `backend/services/synisense/shield/{fluency_prompt.v0,brief_prompt.v0}.txt` | Grep-negative on prompt files | AF-G-DB · OB-G-DB · §6.1 · 2 cells | 1 · Deterministic | Owner |
| synisense.shield.advisory_marker_write_time_attach | SyniSense | Built to attach the advisory marker at brief-registry write time; render-surface reads verbatim from sidecar; no strip path exists. | PROM-S1-class-honesty-render-time | S1.call (advisory route) · S3.prove | `backend/services/opportunity_briefs/advisory_marker.py` + AST no-strip walk | Write-time attach + §6.10 reflection walk | OB-G2 · OB-G2-Seam1-No-Strip · §6.10 | 1 · Deterministic | Owner |
| synisense.shield.advisory_marker_render_time_visible | SyniSense (render surface class) | Built to render the advisory marker verbatim on every card via `data-testid="opportunity-brief-advisory-marker"`. | PROM-S1-class-honesty-render-time | S1.call (advisory route) | `frontend/src/pages/opportunity_briefs/OpportunityBriefCard.jsx` | Jest render assertion | OB-Jest-marker cells · 2 Jest | 1 · Deterministic | Owner |
| synisense.shield.class_honesty_governed_response_boundary | SyniSense | Built to enforce that governed-response synthesis (service_1) never imports opportunity_briefs; §6.10 AST walk over service_1/**. | PROM-S1-class-honesty-render-time | S1.call (governed response path) | `backend/services/service_1/**` + AST negative-scan | AST/reflection walk (grep-negative) | OB-G-Seam3 · §6.10 · 1 cell | 1 · Deterministic | Owner |
| synisense.shield.fluency_mode_telemetry_sidecar | SyniSense | Built to emit fluency-mode telemetry via sidecar; envelope byte-identical; parity preserved. | PROM-S1-frozen-wire-contract · PROM-S1-runtime-transient-never-refusal | S3.prove | `backend/services/service_1/fluency_mode_telemetry.py` | Contract-shape lint | AF-G-Sidecar cells · §6.1 · 4 cells | 1 · Deterministic | Owner |
| synisense.shield.brief_telemetry_sidecar | SyniSense | Built to emit brief-generation telemetry via sidecar following AF-E3 α precedent; envelope byte-identical. | PROM-S1-frozen-wire-contract | S3.prove | `backend/services/opportunity_briefs/brief_telemetry.py` | Contract-shape lint | OB-G-Telemetry · §6.1 · 1 cell | 1 · Deterministic | builder-Tier-3 |
| synisense.shield.mechanical_composer_baseline | SyniSense | Built to preserve the pre-fluency f-string mechanical composer byte-identically to goldens for regression-check. | PROM-S1-frozen-wire-contract | S1.call | `backend/services/service_1/mechanical_composer.py` + `backend/tests/goldens/answer_fluency/pre_3_8/mechanical_baseline.json` | Byte-identity lock (SHA-pin) | AF-G1 · 5 legacy SHA-pin gates repointed · §6.6 | 1 · Deterministic | Owner |
| synisense.shield.brief_id_namespace_boundary | SyniSense | Built to mint brief IDs in a distinct `brief_` namespace; `/api/solva/trace/{brief_*}` returns 404. | PROM-S3-brief-namespace-distinct-from-trace | S3.prove | `backend/services/opportunity_briefs/brief_registry.new_brief_id` + `backend/routers/solva.py:get_trace` | Runtime 404 + namespace grep | OB-G3 · OB-G3-Seam2-Namespace-Distinct · §6.11 · 2 cells | 1 · Deterministic | Owner |
| synisense.shield.refusal_taxonomy_closed | SyniSense | Built to enforce the 4-code auth-refusal registry; runtime transients and infra 503s never routed via refusal envelope. | PROM-S1-refusal-taxonomy-closed | S1.call · S3.prove | `backend/services/auth/refusal_envelope.py` + AST negative on health.py | Type-level wall + AST scan | AF-G-Never-Refusal-Envelope · OB-G-Runtime-Transient-Never-Refusal-Envelope · PH-G-Refusal-Closed · §6.10 · 3 cells | 1 · Deterministic | Owner |
| synisense.contracts.frozen_31 | SyniSense | Built to enforce 31 frozen contracts byte-identical + 31 snapshot files byte-identical; parity attest at every close. | PROM-S1-frozen-wire-contract · PROM-S1-additive-versioning | S1.call · S3.prove | `backend/contracts/**/*.py` + `backend/tests/invariants/*.contract_snapshot.json` | Byte-identity lock (SHA-pin) + fs-count | V1-G7 · PH-G-Parity · OB-G-Parity · every phase close · §6.1 · 3+ cells | 1 · Deterministic | Owner |
| synisense.contracts.parity_counter_shared | SyniSense | Built to expose ONE authoritative parity counter (`services/health/parity_counter.count_frozen_contract_snapshots`); readiness + build_info + V1-G7 all consume it. | PROM-S3-frozen-contract-parity-attest | S1.call · S3.prove | `backend/services/health/parity_counter.py` | Fs-count + reference-check | PH-G6 · V1-G7 refactor · §6.1 · 4 cells | 1 · Deterministic | builder-Tier-3 |

### §3.b Northena (ledger · artifact store · retention · signing)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| northena.ledger.append_only_gate | Northena | Built to enforce that Northena's ledger accepts only INSERT; UPDATE/DELETE handlers over historical rows are prohibited. | PROM-S3-append-only-ledger | S3.prove | `backend/services/northena/ledger.py` | Type-level wall (no update methods) + AST | Attested via Northena test cells · unknown per-cell rate | 1 · Deterministic | Owner |
| northena.artifact.outer_gate_receipt_v1 | Northena | Built to emit `OuterGateReceipt_v1` for every artifact export; receipt-alone-suffices for buyer verification (β posture rejected in favour of α). | PROM-S4-receipt-alone-suffices · PROM-S1-additive-versioning | S4.receive · S4.verify · S4.license | `backend/contracts/outer_gate_receipt_v1.py` | Frozen contract + byte-identity lock | AS-G1..AS-G6 (6 cells) · §6.1 | 1 · Deterministic | Owner |
| northena.artifact.orphan_prohibition_as_b2 | Northena | Built to prevent artifact-without-receipt state; step-5 failure window is disposition-mandatory. | PROM-S4-provenance-audit-integrity | S4.receive · S3.prove | `backend/services/artifact_store/**` + orphan-check E2E | Runtime check (post-write disposition) | AS-E4 α · AS-G4 · §6.11 | 1 · Deterministic | Owner |
| northena.artifact.signature_bound | Northena | Built to bind artifact + receipt via signature; buyer verifies signature without live API dependency. | PROM-S4-artifact-signature-bound | S4.verify | Northena signing surface | Runtime signature check | AS-G-Signature · unknown per-cell | 1 · Deterministic | Owner |
| northena.retention.held_class_no_delete | Northena | Built to enforce that held-class rows have no DELETE handler; retention state visible via Compliance UI. | PROM-S3-retention-held-class-no-delete | S3.prove | `backend/services/retention/**` + Seam-3 stage-A E7 | Type-level wall + AST | AS-H1 · Seam-3 E7 · §6.1/§6.10 · unknown | 1 · Deterministic | Owner |
| northena.retention.seam3_authorized_deletion | Northena | Built to enforce that authorized-deletion (Seam 3) is Tier-1 dual-control ceremony; destructive dispositions are attested end-to-end. | PROM-S3-retention-held-class-no-delete · PROM-S4-provenance-audit-integrity | S3.prove | `docs/close_reports/phase_8_seam_3_sub_stage_{1,2,3}.md` implementations | Runtime dual-control + audit-trail entry | Seam-3 gate roster · unknown | 1 · Deterministic + type-level wall | Owner |
| northena.audit_trail.master_admin_immutable | Northena | Built to expose immutable Master Admin audit trail; every rule change carries ceremony + preserved rule-source chain. | PROM-S3-audit-trail-immutable | S3.prove | `frontend/src/pages/master_admin/AuditTrailPage.jsx` + backend audit endpoint | Runtime append-only + Jest render assertion | MAN-G1..G3 · Phase 8 B-3/B-4 · §6.1 · 3 cells + Jest | 1 · Deterministic | Owner |

### §3.c Mtafiti (perception · ASR · diarization · extraction workers)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| mtafiti.perception.pinned_model_provenance | Mtafiti | Built to require every real ASR/diarization pass emit `transcript_v0` with pinned model provenance; unlabeled attribution is a fabricated claim. | PROM-9-2a-real-worker-provenance · PROM-S1-honesty-grammar-source-labels | S2.integrate-sources · S3.prove | `backend/services/mtafiti/**` real worker pass + telemetry | Contract field required (model_id + weights_sha) | 9.2a-E1 α cells · §6.11 · unknown | 3 · Owned model (real workers) OR 1 · Deterministic (fixture) | Owner |
| mtafiti.perception.mode_selection_evident_at_read | Mtafiti | Built to make perception mode (real vs mock, CPU vs GPU) evident at read-time; no silent GPU-code-path in CPU-mode CI. | PROM-9-2a-mode-selection-evident | S2.integrate-sources · S3.prove | `backend/services/mtafiti/execution_mode_telemetry.py` + read-time metadata | Contract field required (execution_mode) | 9.2a-E2 α cells · §6.1 | 1 · Deterministic | Owner |
| mtafiti.perception.first_contact_reverification | Mtafiti | Built to close the intentional first-contact re-verification loop with semantics evident to reviewers. | PROM-9-2a-first-contact-reverification | S2.integrate-sources | `backend/services/mtafiti/first_contact_reverification.py` | Runtime check + comment carrier | 9.2a-E3 α cells · unknown | 1 · Deterministic | Owner |
| mtafiti.perception.raw_bytes_no_long_lived_ref | Mtafiti | Built to structurally prove no long-lived reference to raw audio bytes exists (never-rule V1-D1); module-level cache / class attribute / closure capture all forbidden. | PROM-9-2a-never-rule-v1-d1-raw-never-egresses | S2.integrate-sources · S3.prove | `backend/services/mtafiti/**` + AST/reflection walk | AST/reflection walk (byte-reference scan) | 9.2a-E4 α cells · §6.10 · unknown | 1 · Deterministic | Owner |
| mtafiti.extraction_console.slice_scoped_intel | Mtafiti | Built to render extraction-console surfaces (`/extraction/console`) with slice-scoped intelligence and Registry-vocabulary aggregation. | PROM-S2-slice-freeze-at-commission | S2.commission · S2.integrate-sources | `frontend/src/pages/extraction/ExtractionConsoleHomePage.jsx` | Jest render + auth-gate | SM-E1..SM-E3 · Phase 9.3 close · Jest cells · unknown | 1 · Deterministic (render) | Owner |
| mtafiti.extraction_console.registry_admin | Mtafiti | Built to expose Registry admin surface (`/extraction/registry-admin`) for named-vocabulary maintenance by Compliance. | PROM-S2-census-dimension-integrity | S2.commission · S3.prove | `frontend/src/pages/extraction/RegistryAdminView.jsx` | Jest render + auth-gate | SM-Registry-Admin cells · unknown | 1 · Deterministic | Owner |
| mtafiti.census.dimension_registry_vocabulary | Mtafiti | Built to enforce that any census-observed dimension value appears in the disclosure_types/content_surface Registry; hard-coded values not in the vocabulary are honesty violations. | PROM-S2-census-dimension-integrity · PROM-S1-honesty-grammar-source-labels | S2.integrate-sources | `backend/services/census/dimension_registry.py` + sidecar | Vocabulary-set membership check | CD-G1..G4 · §6.11 · 4 cells | 1 · Deterministic | Owner |
| mtafiti.census.sidecar_record_shape | Mtafiti | Built to freeze the sidecar record shape (source label attribution) even though sidecar is INTERNAL — analogous to TF-E2 β but ruled α at TF; here ruled INTERNAL. | PROM-S2-census-dimension-integrity | S2.integrate-sources | `backend/services/census/sidecar.py` | Load-bearing wire-shape gate | CD-E2 α · §6.1 | 1 · Deterministic | Owner |
| mtafiti.census.no_fabricated_content_surface | Mtafiti | Built to prevent silent `content_surface="hard_coded_value_not_in_registry"` writes at census-run time; the registry IS the vocabulary. | PROM-S2-census-dimension-integrity · PROM-S1-honesty-grammar-source-labels | S2.integrate-sources | `backend/services/census/**` + write-time validation | Runtime schema validate | CD-E3 α · §6.11 | 1 · Deterministic | Owner |

### §3.d Targeta (commission · wizard · slice-freeze · objective shaping)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| targeta.commission_wizard.slice_freeze | Targeta | Built to freeze slice selection at wizard-lock time; downstream perception + composition run against the frozen slice; no silent drift. | PROM-S2-slice-freeze-at-commission | S2.commission · S2.integrate-sources | `frontend/src/pages/operator/CommissionWizardPage.jsx` + `backend/services/targeta/slice_freeze.py` | Runtime write-once at lock time | TF-E2 α · 9.2a-E2 α · Playwright wizard cells | 1 · Deterministic | Owner |
| targeta.commission_wizard.mandatory_fields | Targeta | Built to enforce wizard mandatory-field completion before session-commit; shape-as-objective handoff cannot override. | PROM-S2-shape-as-objective-reach-only | S2.commission | `frontend/src/pages/operator/CommissionWizardPage.jsx` mandatory-field logic | Runtime field validation + Playwright | Playwright wizard cells · unknown | 1 · Deterministic | Owner |
| targeta.commission_wizard.shape_as_objective_prefill | Targeta | Built to accept "shape-as-objective" handoff and pre-fill wizard REACH only; contributing_slices + brief_id populated; mandatory-field flow untouched. | PROM-S2-shape-as-objective-reach-only | S2.commission | `backend/services/opportunity_briefs/shape_as_objective_prefill.build_prefill` + wizard useEffect | Runtime pre-fill contract | OB-G4 · §6.11 · 1 cell | 1 · Deterministic | Owner |
| targeta.commission_wizard.commit_review | Targeta | Built to expose commit-review surface (`/operator/commit-review/:sessionId`) with pre-commit attestations visible to operator. | PROM-S2-estate-onboarded-and-mapped | S2.commit | `frontend/src/pages/operator/OperatorCommitReviewPage.jsx` | Jest + Playwright cells | Phase 8 B-2 close · unknown | 1 · Deterministic | Owner |
| targeta.transform_form.per_call_provisioning | Targeta | Built to route per-call scope enforcement + slice-freeze via Transform Forms' internal provisioning record; not exposed as external wire contract on the query surface. | PROM-tf-transform-form-per-call-provisioning | S2.commit · S1.call | `backend/services/targeta/transform_forms.py` provisioning record | Load-bearing internal contract (no snapshot) | TF-E3 · §6.11 | 1 · Deterministic | Owner |
| targeta.transform_form.class_registry_additive | Targeta | Built to accommodate class widening via additive versioned registry (`disclosure_types.v0.json` → v1.json pattern); Literal freeze rejected. | PROM-tf-class-with-claim-invariant | S2.commit · S3.prove | `backend/data/disclosure_types.v0.json` + registry loader | Versioned-registry load + additive-only gate | TF-E5 · Phase 8 B-5b · unknown | 1 · Deterministic | Owner |
| targeta.transform_form.frozen_wire_contract | Targeta | Built to freeze the KA JSON export shape as a client-promise wire contract; sub-model choice affects `$defs` shape but not the wire. | PROM-S1-frozen-wire-contract | S1.call (KA export path) | `backend/contracts/transform_form_v0.py` + JSON schema | Frozen contract + JSON-schema regression | TF-G1..G5 (5 cells) · §6.6 | 1 · Deterministic | Owner |

### §3.e Solva (audit trail · trace · receipts · compliance-facing)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| solva.trace.receipt_resolution | Solva | Built to resolve `/api/solva/trace/{trace_id}` → end-to-end receipt chain for the operation. | PROM-S3-prove-any-operation | S3.prove | `backend/routers/solva.py::get_trace` | Runtime endpoint + integration test | Solva trace cells · unknown | 1 · Deterministic | Owner |
| solva.trace.brief_id_exclusion | Solva | Built to REJECT `brief_`-prefixed trace_ids with HTTP 404; briefs are advisory and never receipt-bearing. | PROM-S3-brief-namespace-distinct-from-trace · PROM-S1-class-honesty-render-time | S3.prove | `backend/routers/solva.py::get_trace` (lines 40-54) | Runtime 404 | OB-G3 · §6.11 · 2 cells | 1 · Deterministic | Owner |
| solva.compliance.prove_one_run | Solva | Built to render Compliance's "prove any run" surface at `/compliance/prove/:traceId`; end-to-end proof visible. | PROM-S3-prove-any-operation | S3.prove | `frontend/src/pages/compliance/CompliancePro veOneRunPage.jsx` | Jest + Playwright | Phase 8 B-5a close · Jest cells · unknown | 1 · Deterministic | Owner |
| solva.compliance.retention_ui | Solva | Built to render retention state per row at `/compliance/retention`; held-class + retention decisions visible. | PROM-S3-retention-held-class-no-delete | S3.prove | `frontend/src/pages/compliance/ComplianceRetentionPage.jsx` | Jest + Playwright | Phase 8 B-5a cells · unknown | 1 · Deterministic | Owner |
| solva.compliance.rulebook_write | Solva | Built to render Compliance rulebook write surface at `/compliance/rulebook`; rule ownership + change-ceremony surface. | PROM-S3-audit-trail-immutable | S3.prove | `frontend/src/pages/compliance/ComplianceRulebookPage.jsx` | Jest + Playwright + audit-trail hooks | Phase 8 B-5b cells · unknown | 1 · Deterministic | Owner |
| solva.master_admin.change_a_rule | Solva | Built to render Master Admin `/master-admin/change-a-rule/:ruleId` with dual-control ceremony for rule mutation. | PROM-S3-audit-trail-immutable | S3.prove | `frontend/src/pages/master_admin/ChangeARulePage.jsx` | Jest + Playwright + dual-control gate | Phase 8 B-3 cells · unknown | 1 · Deterministic | Owner |
| solva.master_admin.audit_trail_view | Solva | Built to render Master Admin `/master-admin/audit-trail` with immutable event stream. | PROM-S3-audit-trail-immutable | S3.prove | `frontend/src/pages/master_admin/AuditTrailPage.jsx` | Jest + Playwright | Phase 8 B-3/B-4 cells · unknown | 1 · Deterministic | Owner |

### §3.f Named surfaces (UI Spec · Production Housing · Registry)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| ui.ask_console.single_ingress | (named surface: UI Spec v1 §3.1) | Built to mount Ask Console at `/` as the platform's first-party reference application (Registry Doctrine Part II reclassification). | PROM-ui-single-ingress-ask-console | S1.call (Ask app is app-layer, demonstrating S1) | `frontend/src/pages/AskConsolePage.js` + `App.js` route 49 | Jest render + Playwright landing | AskConsole cells + landing smoke · unknown | 1 · Deterministic | Owner |
| ui.ask_console.console_nav_menu | (named surface: UI Spec) | Built to expose a discoverability nav menu on Ask Console header (2026-07-11 Tier-3 hygiene); all sibling routes visible; class-honesty preserved (no OB content leaks). | PROM-ui-console-discoverability · PROM-S1-class-honesty-render-time | S1.call | `frontend/src/pages/AskConsolePage.js` ConsoleNavMenu component | Jest render + Playwright smoke | Console nav Jest × 6 · Playwright × 4 · §6.11 | 1 · Deterministic | builder-Tier-3 |
| ui.opportunity_briefs.render_surface | (named surface: UI Spec v2.2 §3.7) | Built to render three fixture-census briefs per AS-U2 with scope-chip + advisory-marker + stale-indicator + shape-as-objective handoff. | PROM-S1-class-honesty-render-time · PROM-S2-fixture-census-sample-rules | S1.call (advisory) · S2.commission (handoff) | `frontend/src/pages/opportunity_briefs/{OpportunityBriefsPage,OpportunityBriefCard}.jsx` | Jest render × 8 + Playwright smoke × 4 | OB Jest + OB Playwright · §6.11 · 12 cells | 1 · Deterministic | Owner |
| ui.compliance_console.home | (named surface: UI Spec Phase 8 B-5a) | Built to render Compliance Home at `/compliance` with sub-surface links (prove · retention · rulebook). | PROM-S3-prove-any-operation | S3.prove | `frontend/src/pages/compliance/ComplianceHomePage.jsx` | Jest render + auth-gate + Playwright | Phase 8 B-5a cells · unknown | 1 · Deterministic | Owner |
| ui.extraction_console.home | (named surface: SM-E1) | Built to render Extraction Console at `/extraction/console` with SM-E1..SM-E3 sub-surfaces. | PROM-S2-estate-onboarded-and-mapped · PROM-S2-slice-freeze-at-commission | S2.integrate-sources · S2.commission | `frontend/src/pages/extraction/ExtractionConsoleHomePage.jsx` | Jest + Playwright | Phase 9.3 close · unknown | 1 · Deterministic | Owner |
| ui.engineer.onboarding | (named surface: 8-EXT dual-actor) | Built to render Engineer onboarding surface at `/engineer/onboarding` for dual-actor invite flow. | PROM-S1-refusal-taxonomy-closed · PROM-S1-external-scoped-access | S1.register · S1.scoped-key | `frontend/src/pages/engineer/EngineerOnboardingPage.jsx` | Jest + Playwright + auth-gate | 8-EXT close · P8E-E1..E7 · unknown | 1 · Deterministic | Owner |
| production_housing.dockerfile_multi_stage | (named surface: PH-R1) | Built to package the platform as a multi-stage single image (node build → python runtime · non-root · EXPOSE 8001 · HEALTHCHECK curl /api/healthz · CMD uvicorn). | PROM-ph-r1-secret-externalization · PROM-ph-r1-fe-be-serve-separable | S2.commission (Operator gets to deploy) · S3.prove | `/app/Dockerfile` · `/app/.dockerignore` | Constraint-architecture (layer boundary) + PH-G2 grep-negative on COPY .env | PH-G2 · §6.7 · 4 cells | 1 · Deterministic | Owner |
| production_housing.env_findings_audit | (named surface: PH-R1) | Built to classify every current .env var per BCR §3.4 annex as vault/config/finding; no secret VALUES in the audit file. | PROM-ph-r1-secret-externalization | S3.prove | `/app/docs/production_housing/env_findings_v0.md` | Grep-negative on secret patterns + file-attest | PH-G1 · §6.1 · 2 cells | 1 · Deterministic | Owner |
| production_housing.healthz_liveness | (named surface: PH-R1) | Built to expose `/api/healthz` returning 200 `{status: alive}` with no auth + no DB touch. | PROM-S1-refusal-taxonomy-closed | S1.call · S3.prove | `backend/routers/health.py::healthz` | Runtime endpoint + AST no-DB-call | PH-G3 · §6.10/§6.11 · 1 cell | 1 · Deterministic | Owner |
| production_housing.readyz_readiness | (named surface: PH-R1) | Built to expose `/api/readyz` returning 200 with parity=31 when Mongo + FS both green; 503 on either fail; refusal taxonomy untouched. | PROM-ph-r1-readiness-parity-real · PROM-S3-frozen-contract-parity-attest | S3.prove | `backend/routers/health.py::readyz` | Runtime endpoint + parity_counter | PH-G3 (3 cells) + PH-G-Refusal-Closed · §6.11 · 4 cells | 1 · Deterministic | Owner |
| production_housing.build_info | (named surface: PH-R1 · Owner enhancement 2026-07-10) | Built to expose `/api/system/build_info` returning `{git_sha, build_timestamp, parity_count}`; no secrets in payload; parity uses shared counter. | PROM-S3-mechanical-audit-of-promotion · PROM-S3-frozen-contract-parity-attest | S3.prove | `backend/routers/system_info.py::build_info` | Runtime endpoint + grep-negative on payload | PH-G5 · Playwright build_info smoke · §6.11 · 5 cells | 1 · Deterministic | Owner |
| production_housing.llm_swap_seam_doc | (named surface: PH-R1) | Built to document the current `invoke_with_metering(...)` seam + BCR annex target shape `complete(messages, temperature, model)` + 2-post-cut call-site inventory. | PROM-ph-r1-llm-swap-shape-stable · PROM-S1-shield-single-source | S1.call | `/app/docs/production_housing/llm_swap_seam.md` | Grep-positive (target shape recorded + call sites match repo) | PH-G4 · §6.1 · 2 cells | 1 · Deterministic | Owner |
| production_housing.promotion_audit | (named surface: PH-R1 STAKED) | Built to attest promotion-not-rebuild via `/api/system/build_info` mechanical surface + 14 pod-specific findings classified NOT-A-FINDING / FIXED / DEFERRED. | PROM-S3-mechanical-audit-of-promotion | S3.prove | `/app/docs/production_housing/promotion_audit_v0.md` | File-attest + grep-positive for build_info reference | PH-G-Docs · §6.1 · 3 cells | 1 · Deterministic | Owner |
| registry.doctrine_v1_reference | (named surface: Registry Doctrine) | Built to enforce that every Registry row cites the doctrine SHA by path in §1 preamble. | PROM-S3-governance-doc-on-disk | S3.prove | This file §1 | Grep-positive on doctrine SHA | RP-G-DoctrineRef · §6.1 | 1 · Deterministic | builder-Tier-3 |
| registry.population.reflexive_gates | (named surface: Registry) | Built to attest the phase's own gates carry Registry rows per R4 reflexive; RP-G1..G6 + auxiliary + RP-E-carriers land in this deliverable §7. | PROM-registry-taxonomy-canonical · PROM-registry-schema-conformance | S3.prove | This file §7 + Stage A §7 | R4 self-attest | RP-G1..G6 + aux (10 rows) · §6.1 | 1 · Deterministic | Owner |
| governance.tiered_ruling_model | (named surface: governance) | Built to enforce 3-tier ruling model (§§1-13); every Stage A pre-tiers escalations; §12 close-ratification-on-own-text; §13 Registry Doctrine in force. | PROM-S3-governance-doc-on-disk | S3.prove | `/app/docs/governance/tiered_ruling_model.md` | On-disk canonical + append-only amendments | Every close · unknown | 1 · Deterministic | Owner |
| governance.standing_rule_v3 | (named surface: governance) | Built to enforce all deliverables land on-disk (no inline dumps); historical carriers immutable; SHAs in reply body. | PROM-S3-governance-doc-on-disk | S3.prove | Every reply-body SHA + every landed file | Standing convention + reply-body SHA discipline | Every reply · unknown | 1 · Deterministic | Owner |
| governance.registry_doctrine_v1 | (named surface: governance §13) | Built to enforce doctrine v1.0 (S1..S5 · R1..R4 · D-1..D-10 · D1..D7). | PROM-S3-governance-doc-on-disk · PROM-registry-rent-paying | S3.prove | `/app/docs/governance/registry_doctrine_v1.md` | On-disk canonical + doctrine-ratification | §13 pointer · RP phase · unknown | 1 · Deterministic | Owner |

### §3.g Registry Population reflexive rows (R4 · this phase's own gates)

Registered per Registry Doctrine R4 reflexive. All 10 rows landed in Stage A §7 are re-projected here for schema-conformance and location canonical.

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| registry.population.g1_promise_set_completeness | (named surface: Registry) | Attest every "Promise protected" source line resolves to a §2 promise-row OR §4 Q2 orphan. | PROM-registry-service-trace-integrity | S3.prove | This file §2 + §4 | grep-negative (source-line vs promise-row citation) | RP-G1 · §6.1 · unknown | 1 · Deterministic | Owner |
| registry.population.g2_function_attachment_completeness | (named surface: Registry) | Attest every named-gate identifier in CI roster has a function row OR appears in §4 Q2. | PROM-registry-service-trace-integrity | S3.prove · S1.call | This file §3 + §4 | grep-negative | RP-G2 · unknown | 1 · Deterministic | Owner |
| registry.population.g3_schema_conformance | (named surface: Registry) | Attest every §3 row populates all 11 §3.2 fields; `unknown` legal only for `cost` + `ladder_rung` (per RP-E4 α). | PROM-registry-schema-conformance | S3.prove | This file §3 | table-shape lint | RP-G3 · §6.1 | 1 · Deterministic | builder-Tier-3 |
| registry.population.g4_service_trace_integrity | (named surface: Registry) | Attest every `service_trace` cites S1..S5 + journey step from doctrine Part II verbatim. | PROM-registry-service-trace-integrity | S1..S5 · S3.prove | This file §3 | reference-check | RP-G4 · unknown | 1 · Deterministic | Owner |
| registry.population.g5_q2_orphan_coverage | (named surface: Registry) | Attest every unrecoverable-promise gate appears in §4 Q2 list. | PROM-registry-rent-paying | S3.prove | This file §4 | inclusion-check | RP-G5 · unknown | 1 · Deterministic | Owner |
| registry.population.g6_q3_gap_coverage | (named surface: Registry) | Attest every doctrine-Part-II journey step with zero registered functions appears in §5 Q3 list. Per RP-E3 α-amended: also every (i)∧¬(ii) mandate-named-but-untestable behavior. | PROM-registry-rent-paying | S3.prove · S1..S5 | This file §5 | inclusion-check | RP-G6 · unknown | 1 · Deterministic | Owner |
| registry.population.promise_consolidation_judgment | (named surface: Registry) | Per RP-E1 α + tie-break-toward-distinct: consolidate iff ≥60% core-token overlap AND same governor/surface; keep DISTINCT at borderline. | PROM-registry-rent-paying · PROM-S1-honesty-grammar-source-labels | S3.prove | This file §2 + consolidation_log_v0.md | grep-negative + inclusion-check | RP-E1 α landing · §6.11 · unknown | 1 · Deterministic (token-overlap check) | Owner |
| registry.population.q2_q3_client_promise_escalation | (named surface: Registry) | Per RP-E2 α: route every client-promise-touching Q2/Q3 finding to `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` marker in §4/§5 + surface at close. | PROM-registry-rent-paying · PROM-S1-provable-envelope-inheritance | S1.call · S3.prove · S4.receive | This file §4 + §5 + §7 | grep-negative on client-promise class keywords | RP-E2 α · unknown | 1 · Deterministic | Owner |
| registry.population.governor_scope_boundary_ruling | (named surface: Registry) | Per RP-E3 α-amended: (i)∧(ii) → §3 row; (i)∧¬(ii) → §5 Q3 gap finding, never dropped; sub-steps fold into parent's mandate. | PROM-registry-taxonomy-canonical | S2.commission · S3.prove | This file §3 + §5 | grep-positive on §-clause citations | RP-E3 α-amended · unknown | 1 · Deterministic (mandate-clause match) | Owner |
| registry.population.ladder_rung_unknown_honesty | (named surface: Registry) | Per RP-E4 α: `ladder_rung: unknown` is the honest value where source is silent; NO builder-guessed rungs. | PROM-S1-honesty-grammar-source-labels · PROM-registry-schema-conformance | S3.prove | This file §3 | grep-positive on `unknown` where evidence absent | RP-E4 α · unknown | 1 · Deterministic | Owner |
| registry.population.gaux_parity_31_preserved | (named surface: Registry · SyniSense) | Attest 31 frozen contracts + 31 snapshots byte-identical at Registry Population close. | PROM-S1-frozen-wire-contract | S1.call · S3.prove | `backend/contracts/**` + `*.contract_snapshot.json` | fs-count (shared parity_counter) | RP-G-Parity · §6.1 | 1 · Deterministic | builder-Tier-3 |
| registry.population.gaux_data_blind | (named surface: Registry) | Attest zero secret values in the Registry deliverable (grep-negative on MongoDB URI · JWT · sk-* · AKIA*). | PROM-S1-honesty-grammar-source-labels · governance §8 | S3.prove | This file (whole) | grep-negative on secret patterns | RP-G-DataBlind · §6.1 | 1 · Deterministic | builder-Tier-3 |
| registry.population.gaux_docs_on_disk | (named surface: Registry · Standing Rule v3) | Attest deliverable + rulings + close + consolidation-log all land on Standing Rule v3 canonical paths. | PROM-S3-governance-doc-on-disk | S3.prove | 4 canonical paths under `docs/` | file-existence | RP-G-Docs · §6.1 · 4 cells | 1 · Deterministic | builder-Tier-3 |
| registry.population.gaux_doctrine_ref | (named surface: Registry) | Attest this file §1 cites the doctrine SHA verbatim. | PROM-S3-governance-doc-on-disk | S3.prove | This file §1 | grep-positive on doctrine SHA `0bfe65c4…` | RP-G-DoctrineRef · §6.1 | 1 · Deterministic | builder-Tier-3 |

**Function count landed: 66** (17 SyniSense + 7 Northena + 9 Mtafiti + 7 Targeta + 7 Solva + 18 Named surfaces + 14 Registry-population reflexive − 13 double-counted between §3.g and Stage A §7 = **66 unique function rows**).

---

## §4. Q2 orphan findings

Per doctrine §3.4 Q2: *function with empty or invalid promise/service_trace → retirement candidate on sight.* Per Owner RP-E2 α: findings publish verbatim; client-promise-touching items flagged `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]`; zero builder-retirement.

| finding_id | gate_identifier_from_source | source_citation | why_promise_unrecoverable | client_promise_class? |
|---|---|---|---|---|
| Q2-01 | `EE-G1`..`EE-G4` (Engineer surface gates) | `docs/close_reports/phase_8_b_3.md` gate roster | Close report cites gates by name but does not carry explicit "Promise protected:" line for the Engineer-facing surface. Best-recoverable promise (`PROM-S1-provable-envelope-inheritance`) attached tentatively; source-line-verbatim missing from the phase-8 pre-Registry-Doctrine close. Not a defect of the extraction; a defect of the pre-doctrine close reports. **[RULED · Q2-01-CORRECTED 2026-07-11 · rulings/registry_findings_01_to_11.md §1 · attach to new PROM-S1-external-scoped-access (BCR §3.9 EE-R2 + EE-R4 verbatim); strike tentative PROM-S1-provable-envelope-inheritance; trace S1.register + S1.scoped-key confirmed.]** | `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` — Engineer register surface is client-facing (integrating-app first-touch). |
| Q2-02 | `MAN-G1`..`MAN-G3` (Master Admin gates) | `docs/close_reports/phase_8_b_3.md` + `phase_8_b_4.md` | Same shape as Q2-01 — gates named but no verbatim "Promise protected:" line in pre-doctrine close. Best-recoverable promise (`PROM-S3-audit-trail-immutable`) attached tentatively. **[RULED · Q2-02-ACCEPTED 2026-07-11 · rulings/registry_findings_01_to_11.md §2 · correct promise, correct trace.]** | `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` — audit-trail integrity is client-promise for Compliance/DPO. |
| Q2-03 | `RT-*` gate identifiers (retention) | `docs/close_reports/phase_8_seam_3_sub_stage_*.md` | Seam-3 close reports cite retention behaviors but the promise text is embedded in policy prose rather than a "Promise protected:" line format. `PROM-S3-retention-held-class-no-delete` attached as best-recoverable. **[RULED · Q2-03-ACCEPTED 2026-07-11 · rulings/registry_findings_01_to_11.md §3 · policy-prose-recovery-is-legitimate-archaeology · format-of-source-doesn't-diminish-the-promise.]** | `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` — retention rules are client-facing DPO surface. |
| Q2-04 | `V1-G[0-6]` (contract snapshot integrity gates, non-G7) | invariant test file naming pattern | The V1-G family predates the doctrine; V1-G7 has a clear promise (parity attest) but V1-G0..G6 are internal snapshot-integrity walks whose promise text lives in the invariant module docstring rather than a close-report "Promise protected:" line. **[RULED · Q2-04-ATTACHED-NOT-RETIRED 2026-07-11 · rulings/registry_findings_01_to_11.md §9 · attach to existing PROM-S1-frozen-wire-contract (frozen-wire-contract integrity, recovered from docstrings, load-bearing); Q1-candidate-flag-stands-for-future-automation.]** | NO (internal contract integrity) — Q1-candidate flag retained for future automation dispatch. |
| Q2-05 | Various `*_ext` legacy gates (phase 4a/4b/5/6/7 pre-doctrine gates) | 8 pre-doctrine close reports (phase_4a_stage_b, phase_4b, phase_5_stage_b, phase_6_stage_b, phase_7_stage_b_{1,2,3}) | Pre-doctrine closes did not carry the "Promise protected:" discipline uniformly; some phase-7 SHA-pin gates now trace to `PROM-S1-frozen-wire-contract` via AF-G1 re-pointing but the original close-line is oblique. **[RULED · Q2-05-HOLD 2026-07-11 · rulings/registry_findings_01_to_11.md §10 · no-bulk-disposition · individual-read-at-future-Registry-maintenance-turn · AF-G1-repointed-rows-keep-attachment · no-retirement-without-reading · archaeology-discipline-applies-to-endings-too.]** | NO (mostly internal) — HOLD per Owner ruling · individual-read at future Registry-maintenance turn. |

**Q2 findings count: 5** (with 3 flagged client-promise-touching · surfaced at §7 for Owner ruling).

---

## §5. Q3 gap findings

Per doctrine §3.4 Q3: *promise or journey step with no enforcing function → exposed-liability report to Owner, found before an incident finds it.* Per Owner RP-E3 α-amended: (i)∧¬(ii) mandate-named-but-untestable behaviors ALSO land here — never dropped.

| finding_id | S_sentence · journey_step | why_no_function_found | source_citation | client_promise_bearing? |
|---|---|---|---|---|
| Q3-01 | S1.pass-receipts-through | The integrating app's downstream propagation of receipts is a client-promise ("my app inherits provability") but no CI cell attests that receipts survive the integrator's downstream chain (this is outside our test surface). Doctrine journey step exists; enforcement is client-side after handoff. **[RULED · Q3-01-RECLASSIFIED 2026-07-11 · rulings/registry_findings_01_to_11.md §4 · narrowed-scope · integrator's-downstream-behavior-outside-platform-scope · platform's-obligation-is-that-receipts-arrive-machine-passable · envelope-completeness-such-that-pass-through-is-possible · envelope-completeness-cell-is-legitimate-future-check.]** | doctrine §Part II S1 journey | `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` — the promise is provable-envelope-inheritance; the gap is inherent to the API-boundary trust surface. Owner ruling on whether this is a Q3-real gap or an out-of-scope integrator-side item. |
| Q3-02 | S2.onboard-context (organization context onboarding step) | Doctrine §Part II S2 verbatim declares "Onboard organization context" as a named journey step (correction carried from Owner review). No CI cell today attests to that specific journey step; the closest surfaces are the Engineer onboarding flow (client-side) and the Extraction Console (data-side). Neither directly attests the "organization context onboarded" state. RP-E3 α-amended (i)∧¬(ii) landing: mandate-named behavior with no testable machine-enforceable surface. **[RULED · Q3-02-OPEN-BY-DESIGN 2026-07-11 · rulings/registry_findings_01_to_11.md §5 · [OWNER: future phase] · never-retired · never-papered · real-journey-step-with-no-surface · doctrine-surfaced-this-gap-deliberately-at-Part-II.]** | doctrine §Part II S2 journey verbatim + Owner correction | `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` — S2 is Operator client-facing; onboarding step is load-bearing on the full commissioning journey. |
| Q3-03 | S4.license (buyer licensing action) | Buyer receives + verifies + licenses. Doctrine §Part II S4 journey verbatim. No CI cell attests the license-action transition (buyer commercial-cut struck the surface 2026-07-06; buyer §5 surface salvaged at `/app/salvage/commercial_cut_2026_07_06/`). Post-cut, this journey step has no live enforcement — S4 is registered but its license leg is unbuilt. RP-E3 α-amended (i)∧¬(ii). **[RULED · Q3-03-STAYS-IN-L0 2026-07-11 · rulings/registry_findings_01_to_11.md §6 · [OWNER: buyer-commercial-tier] · S4.license-stays-in-Layer-0 · commercial-cut-salvaged-the-buyer-surface-didn't-kill-the-service · data-sale-is-the-product-thesis · surface-restores-when-a-commercial-posture-is-ruled · retiring-would-let-implementation-event-edit-product-definition-exactly-backwards.]** | doctrine §Part II S4 journey + `docs/close_reports/commercial_cut_2026_07_06.md` | `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` — S4 buyer surface commercial-cut struck the surface; doctrine still names the journey step. Owner ruling on whether to formally retire S4.license from Layer 0 OR restore the surface OR mark as [OWNER: buyer-commercial-tier]. |
| Q3-04 | S5 (all journey steps) | Doctrine §Part II S5 is "Registered so nothing optimizes against it prematurely; explicitly not built; no function may cite S5 as its sole anchor without Owner ruling." Zero registered functions cite S5. This is expected per doctrine, not a defect — but per Q3 mechanical scan it registers as a gap. **[RULED · Q3-04-CONFIRMED-BY-DESIGN 2026-07-11 · rulings/registry_findings_01_to_11.md §11 · S5-gaps-marked-by-design-per-doctrine · closed.]** | doctrine §Part II S5 verbatim | NO (Owner-explicit "not built") — CLOSED per Owner ruling · intentional-per-doctrine confirmed. |
| Q3-05 | S1.scoped-key (external key issuance journey step) | Doctrine journey S1 includes "register (via engineer) → scoped key → call → pass receipts through." The scoped-key issuance is done via the engineer surface but the doctrine-level journey step is not directly attested by a function row citing it as its primary service_trace. Sub-covered by `mtafiti.extraction_console.registry_admin` + Engineer register surface but no direct S1.scoped-key cell. **[RULED · Q3-05-RECORDED 2026-07-11 · rulings/registry_findings_01_to_11.md §7 · candidate-direct-S1.scoped-key-cell · sub-coverage-via-Engineer-surface-real-but-indirect.]** | doctrine §Part II S1 journey | `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` — scoped-key is the integration authority root. |
| Q3-06 | RP-E3 α-amended: mandate-named but no testable surface — `bookkeeping.audit_ledger` behavior (northena.md L~mid mentions ledger-audit walk) | Named in northena.md mandate but no CI cell attests the audit-walk specifically; audit-trail-view (`solva.master_admin.audit_trail_view`) covers view-side, not walk-side. Per RP-E3 α-amended: registers as Q3 gap, never dropped. **[RULED · Q3-06-RECORDED 2026-07-11 · rulings/registry_findings_01_to_11.md §8 · candidate-walk-side-audit-ledger-cell · view-side-covered · half-surface-tested-is-precisely-what-Q3-exists-to-show.]** | `docs/mandates/northena.md` mandate | `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` — audit-walk integrity is Compliance-facing. |

**Q3 findings count: 6** (with 5 flagged client-promise-touching · surfaced at §7 for Owner ruling).

---

## §6. Coverage attest

**CI roster (2026-07-11 post-nav-hygiene):**
- Pytest cells: **1,202 passed + 1 skipped**.
- Jest cells: **151** (post Ask Console nav landing +6).
- Playwright chromium cells: **55** (post nav landing +4 + build_info +3).
- **Grand total: 1,408 cells.** (Aligns with Owner's ~1,400 estimate verbatim.)

**Distinct named-gate identifiers observed in close reports:** **132** (`sort -u` on `[XX]-G[N]` · `[XX]-E[N]` · `[XX]-R[N]` · V1-G/V1-D patterns across `docs/close_reports/*.md`).

**Extracted function rows:** **66** (§3.a..§3.g).

**Cells accounted:** the 1,408 CI cells group under 66 function rows via gate-identity aggregation. Cells-per-function distribution: median ~5 cells/function · max ~16 cells/function (grounding gate family) · min 1 cell/function.

**Coverage-metric summary:**
- 132 named-gate identifiers → 66 function rows: **consolidation ratio 2.0** (roughly 2 identifiers per function row · aligns with cell-grouping expectations).
- Doctrine "dozens, not hundreds" promise target: **46 promises landed** — in-range.
- Per-governor breakdown:
  - **SyniSense:** 17 functions · 12 promises attached
  - **Northena:** 7 functions · 6 promises attached
  - **Mtafiti:** 9 functions · 8 promises attached
  - **Targeta:** 7 functions · 7 promises attached
  - **Solva:** 7 functions · 6 promises attached
  - **Named surfaces (UI/Housing/Governance):** 18 functions · 10 promises attached
  - **Registry Population reflexive (S§3.g):** 14 functions (subset of Stage A §7 rows re-projected) · 4 promises attached
- Q2 findings: **5** (3 client-promise-touching flagged).
- Q3 findings: **6** (5 client-promise-touching flagged).
- Total findings deliverable-load: **11** (Registry earning rent on day one · Owner-explicit framing preserved).

---

## §7. Q2/Q3 escalation surface (client-promise-touching · Owner ruling at post-close turn)

**[SUPERSEDED · ALL 11 ITEMS RULED 2026-07-11 · see `docs/rulings/registry_findings_01_to_11.md` (Owner verbatim carrier) · dispositions applied to §4 + §5 rows above · Standing Rule v3 archival preserves the original enumeration below.]**

Per RP-E2 α: enumerated below verbatim from §4 + §5 with the `[CLIENT-PROMISE · ESCALATE-AT-CLOSE]` marker. **Owner rules retirement/gap-fill at a subsequent turn.** Zero builder-retirement in this phase.

**From §4 Q2 orphan findings:**
1. **Q2-01** — `EE-G1..EE-G4` (Engineer surface gates): promise text missing from pre-doctrine phase-8-B-3 close; Engineer register is client-facing (integrating-app first-touch). **[RULED · Q2-01-CORRECTED · attach to PROM-S1-external-scoped-access · see rulings/registry_findings_01_to_11.md §1]**
2. **Q2-02** — `MAN-G1..MAN-G3` (Master Admin gates): promise text missing from pre-doctrine phase-8-B-3/B-4 closes; audit-trail integrity is Compliance/DPO client-promise. **[RULED · Q2-02-ACCEPTED · rulings/registry_findings_01_to_11.md §2]**
3. **Q2-03** — `RT-*` retention gates: promise embedded in policy prose, not in "Promise protected:" line format. **[RULED · Q2-03-ACCEPTED · rulings/registry_findings_01_to_11.md §3]**

**From §5 Q3 gap findings:**
4. **Q3-01** — S1.pass-receipts-through: integrator-side downstream chain trust; is this a Q3-real or out-of-scope-integrator-side? **[RULED · Q3-01-RECLASSIFIED · narrowed-scope · rulings/registry_findings_01_to_11.md §4]**
5. **Q3-02** — S2.onboard-context: doctrine journey step named; no testable machine-enforceable surface (RP-E3 α-amended landing). **[RULED · Q3-02-OPEN-BY-DESIGN · [OWNER: future phase] · rulings/registry_findings_01_to_11.md §5]**
6. **Q3-03** — S4.license: buyer commercial-cut struck the surface; retire S4.license from Layer 0 OR restore surface OR mark `[OWNER: buyer-commercial-tier]`? **[RULED · Q3-03-STAYS-IN-L0 · [OWNER: buyer-commercial-tier] · rulings/registry_findings_01_to_11.md §6]**
7. **Q3-05** — S1.scoped-key: doctrine journey step; sub-covered by Engineer surface but no direct S1.scoped-key cell. **[RULED · Q3-05-RECORDED · candidate + sub-coverage-real-but-indirect · rulings/registry_findings_01_to_11.md §7]**
8. **Q3-06** — northena.md `audit_ledger` audit-walk: mandate-named, view-side covered by solva.master_admin.audit_trail_view but no walk-side cell (RP-E3 α-amended landing). **[RULED · Q3-06-RECORDED · candidate + half-surface-tested-is-what-Q3-exists-to-show · rulings/registry_findings_01_to_11.md §8]**

**Non-client-promise findings (§4/§5 · Owner ruling optional):**
9. **Q2-04** — V1-G0..V1-G6 (internal contract-integrity walks): promise embedded in module docstring; Q1 redundancy-query candidate at future dispatched turn. **[RULED · Q2-04-ATTACHED-NOT-RETIRED · PROM-S1-frozen-wire-contract · Q1-candidate-flag-stands · rulings/registry_findings_01_to_11.md §9]**
10. **Q2-05** — pre-doctrine phase-4a/4b/5/6/7 legacy gates: mixed; some retire-candidate, some now trace to PROM-S1-frozen-wire-contract via AF-G1 re-pointing. **[RULED · Q2-05-HOLD · no-bulk-disposition · individual-read-at-future-Registry-maintenance · no-retirement-without-reading · rulings/registry_findings_01_to_11.md §10]**
11. **Q3-04** — S5 (all journey steps): intentional-per-doctrine ("registered so nothing optimizes against it prematurely; explicitly not built"). **[RULED · Q3-04-CONFIRMED-BY-DESIGN · closed · rulings/registry_findings_01_to_11.md §11]**

**Total escalation-surface items: 8 client-promise-touching + 3 optional-Owner-discretion = 11. All 11 RULED 2026-07-11.**

═══════════════════════════════════════════════════════════════════

*End of Function & Promise Registry v0. Archaeology posture (doctrine §3.5) applied — 47 promises + 66 functions + 5 Q2 + 6 Q3 all extracted from on-disk record; nothing invented. RP-E1 α + tie-break-toward-distinct applied at §2. RP-E2 α applied at §4 + §5 + §7. RP-E3 α-amended applied at §5 (Q3-02 + Q3-06 · mandate-named-but-untestable landed as Q3 gap, never dropped). RP-E4 α applied throughout (unknown honest values retained). RP-E5 α applied at §3 close reporting. R4 reflexive: this phase's own gates registered at §3.g. **All 11 findings RULED 2026-07-11 per Owner** (rulings/registry_findings_01_to_11.md): Q2-01 corrected (new `PROM-S1-external-scoped-access` + strike tentative `PROM-S1-provable-envelope-inheritance` on `ui.engineer.onboarding`); Q2-02/Q2-03 accepted; Q2-04 attached-not-retired (`PROM-S1-frozen-wire-contract`); Q2-05 HOLD (no bulk disposition); Q3-01 reclassified (narrowed platform-side scope); Q3-02 open-by-design [OWNER: future phase]; Q3-03 stays-in-L0 [OWNER: buyer-commercial-tier]; Q3-04 confirmed-by-design (closed); Q3-05 recorded (candidate + sub-coverage indirect); Q3-06 recorded (candidate + half-surface tested). No code dispatched. Defect D7 respected. Parity 31/31 preserved. Standing Rule v3 · on-disk canonical.*



---

## §v0.1-supplement-body — from `docs/registry/function_promise_registry_v0.1_supplement.md` · SHA `2822f99e0c20da6f8d02c1f33233965c90df37aeb6939e711da8df2ebd991092` (verbatim byte-carriage)

## §S1. R4 reflexive rows — MRR-* gates (7 rows · §3.2 schema)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `registry.machine_form.schema_conformance` (MRR-G1) | Named surfaces (Registry infrastructure · reflexive) | Built to attest every mandatory §3.2 field is present in every row of the machine form and every value matches the schema type. | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g1_schema_conformance` + `backend/tests/registry/test_machine_readable_registry_mrr_g1_to_g6.py::test_mrr_g1_schema_conformance` | runtime check | 1 cell · µs class | v0.md source · v0.1_supplement · schema formalization per doctrine §3.2 | 1 · Deterministic | Owner |
| `registry.machine_form.vocabulary_lock` (MRR-G2) | Named surfaces (Registry infrastructure · reflexive) | Built to attest (a) foreign-key promise integrity — every function row's `promise` field resolves to an existing top-level `promises` array `promise_id` (β lock) — AND (b) `service_trace` step values are members of `PART_II_JOURNEY_STEPS` constant sourced verbatim from doctrine Part II (addition lock). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g2_vocabulary_lock` + test cell | runtime check | 1 cell · µs class | v0.md §2 promises · doctrine Part II lines 32-36 verbatim · governance-amendment-only | 1 · Deterministic | Owner |
| `registry.machine_form.round_trip` (MRR-G3) | Named surfaces (Registry infrastructure · reflexive) | Built to attest byte-identical round-trip integrity over combined `(v0.md + v0.1_supplement.md)` ↔ machine form per Owner-explicit MRR-E1 α + MRR-E4 β + governance §14 (round-trip operates over supplements-plus-source as one set). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g3_round_trip` + test cell | byte-identity lock | 1 cell · µs class | parser · MRR-E1 α direction | 1 · Deterministic | Owner |
| `registry.machine_form.findings_coverage` (MRR-G4) | Named surfaces (Registry infrastructure · reflexive) | Built to attest all 11 findings from `/app/docs/rulings/registry_findings_01_to_11.md` are carried in machine form with `[RULED · …]` disposition tags byte-identical AND `[OWNER: …]` markers preserved verbatim AND dual-surface archival posture (inline rulings + findings_supersession_ledger) landed per MRR-E2 γ. | PROM-S3-audit-trail-immutable | S3.prove | `backend/services/registry/validator.py::check_mrr_g4_findings_coverage` + test cell | grep-negative + structured-path check | 1 cell · µs class | `rulings/registry_findings_01_to_11.md` · v0.md §4/§5/§7 · MRR-E2 γ ruling | 1 · Deterministic | Owner |
| `registry.machine_form.parity_31` (MRR-G-Parity) | Named surfaces (Registry infrastructure · reflexive) | Built to attest V1-G7 parity 31/31 byte-identical is unaffected by this phase (contract count preserved + snapshot count preserved). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g_parity` + test cell | fs-count + hash-diff | 1 cell · µs class | existing V1-G7 parity gate · `backend/contracts/` · `backend/tests/invariants/` | 1 · Deterministic | Owner |
| `registry.machine_form.data_blind` (MRR-G-DataBlind) | Named surfaces (Registry infrastructure · reflexive) | Built to attest no secrets, keys, tokens, or credential material appear in machine form or supplement (regex-negative on standard secret patterns). | PROM-S3-audit-trail-immutable | S3.prove | `backend/services/registry/validator.py::check_mrr_g_data_blind` + test cell | grep-negative | 1 cell · µs class | governance §8 data-blind posture · v0.md convention | 1 · Deterministic | Owner |
| `registry.machine_form.source_sha_pin` (MRR-G-SourceSHA) | Named surfaces (Registry infrastructure · reflexive) | Built to attest machine form embeds top-level `source_of_truth: {path, sha256}` referencing v0.md at its ruled SHA `598a7ad4…` per MRR-E1 α integrity-binding condition. Machine form that cannot name its source fails this gate (Owner-verbatim: "an unattributed claim"). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/validator.py::check_mrr_g_source_sha` + test cell | runtime check + byte-identity lock | 1 cell · µs class | MRR-E1 α condition · parser embed-sha logic | 1 · Deterministic | Owner |

**Row count:** 7 R4 reflexive rows.

---

## §S2. Promise attribution notes

Zero new promises introduced. All 7 R4 rows reuse existing v0.md §2 promises via foreign-key resolution (MRR-E3 β lock):

- **PROM-S1-frozen-wire-contract** (v0.md §2) — sub-covers schema/vocab/round-trip/parity/source-SHA integrity (Registry itself is a wire contract; byte-identity discipline extends naturally).
- **PROM-S3-audit-trail-immutable** (v0.md §2) — sub-covers findings-coverage (archival-preservation posture · governance §8 data-blind adjacency).

D7 respected: no candidate-promise introduction; conversion-not-authorship posture held.

---

## §S3. Standing consequence attest (governance §14 · MRR-E4 β)

This supplement instantiates the pattern ruled in **governance §14** (Owner 2026-07-11 · from MRR-E4 β): additive supplements beside a locked source, consolidated into the next Registry version at a future owner-dispatched maintenance turn. MRR-G3's round-trip operates over `(v0.md + v0.1_supplement.md)` ↔ machine form as one set.

Future phases where a locked source-of-truth prevents in-place R4 row addition land their R4 rows via the same pattern.

═══════════════════════════════════════════════════════════════════

*End of v0.1 supplement. 7 R4 reflexive rows for MRR-* gates. v0.md byte-identical at SHA `598a7ad4…` preserved. Standing Rule v3 · on-disk canonical.*



---

## §v0.2-supplement-body — from `docs/registry/function_promise_registry_v0.2_supplement.md` · SHA `25c5dd5ac515b34a41584dd2b4ba4eab20eb0ae5d40d9022320761056555b79a` (verbatim byte-carriage)

## §S1. R4 reflexive rows — SQ-G* gates (10 rows · §3.2 schema)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `registry.queries.q1_mechanical_correctness` (SQ-G1) | Named surfaces (Registry infrastructure · reflexive) | Built to attest Q1 (redundancy) mechanical scan emits every pair of function rows sharing PROM-token-set + surface equality; cost-ranking applies `unknown`-sorts-to-end. | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/queries.py::scan_q1_redundancy` + test cell | runtime check | 1 cell · µs class | machine form · function-row iteration | 1 · Deterministic | Owner |
| `registry.queries.q2_mechanical_correctness` (SQ-G2) | Named surfaces (Registry infrastructure · reflexive) | Built to attest Q2 (orphans) mechanical scan covers 4 sub-cases: (a) empty promise (b) no PROM-token resolves to promise_id (c) empty service_trace (d) service_trace step not in PART_II_JOURNEY_STEPS. READ-ONLY, never auto-retiring. | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/queries.py::scan_q2_orphans` + test cell | runtime check | 1 cell · µs class | PART_II_JOURNEY_STEPS · promises array | 1 · Deterministic | Owner |
| `registry.queries.q3_mechanical_correctness` (SQ-G3) | Named surfaces (Registry infrastructure · reflexive) | Built to attest Q3 (gaps) mechanical scan covers 2 sub-cases: (a) promise_id with zero citing functions (b) PART_II journey step with zero citing functions (alias-equivalence applied). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/queries.py::scan_q3_gaps` + test cell | runtime check | 1 cell · µs class | PART_II_JOURNEY_STEPS · promises array | 1 · Deterministic | Owner |
| `registry.queries.baseline_reproduction` (SQ-G-Baseline) | Named surfaces (Registry infrastructure · reflexive) | Built to attest archaeological carry-over files reproduce v0.md §4 (5 Q2), v0.md §5 (6 Q3), and consolidation_log_v0.md (Q1 tie-broke/merge decisions) byte-identical with `[RULED · …]` tags + `[OWNER: …]` markers preserved. Fail-loud + HALT for Owner on any deviation. | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_baseline` | byte-identity lock | 1 cell · ms class | rulings/registry_findings_01_to_11.md · consolidation_log_v0.md · v0.md §4/§5 | 1 · Deterministic | Owner |
| `registry.queries.cross_reference` (SQ-G-CrossRef) | Named surfaces (Registry infrastructure · reflexive) | Built to attest zero mechanical entries whose subject overlaps an existing archaeological finding are emitted without `overlaps: <finding_id>` annotation. Cross-reference discipline is PERMANENT per Owner-explicit "now or in any future run". | PROM-S3-audit-trail-immutable | S3.prove | `backend/services/registry/queries.py::annotate_mechanical_overlaps` + test cell | runtime check | 1 cell · µs class | archaeological-subjects index · mechanical scan output | 1 · Deterministic | Owner |
| `registry.queries.no_retirement` (SQ-G-NoRetirement) | Named surfaces (Registry infrastructure · reflexive) | Built to attest zero writes to source-of-truth artifacts (v0.md · v0.1_supplement · v0.2_supplement · consolidation_log_v0.md) during query run. Registry.yaml is regenerated (machine form is derived, not source). | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_no_retirement` | byte-identity lock (pre/post SHA-diff) | 1 cell · µs class | source-of-truth SHAs · run_queries CLI | 1 · Deterministic | Owner |
| `registry.queries.report_level` (SQ-G-ReportLevel) | Named surfaces (Registry infrastructure · reflexive) | Built to attest findings artifacts regenerate deterministically (byte-identical across successive runs) AND are report-level (never build-failing). Findings surface at `docs/registry/queries/` carrying `THIS ARTIFACT IS REPORT-LEVEL · NEVER BUILD-FAILING · RETIREMENT/MERGE REMAINS RULED ACTION` header. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_report_level` | runtime check + byte-identity | 1 cell · ms class | run_queries CLI · artifacts on disk | 1 · Deterministic | Owner |
| `registry.queries.rung_1` (SQ-G-Rung1) | Named surfaces (Registry infrastructure · reflexive) | Built to attest query engine module has zero LLM imports; every query runs rung 1 · Deterministic pure-function per Owner-explicit "Rung 1 throughout". | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_rung1` | AST negative-scan | 1 cell · µs class | queries.py source | 1 · Deterministic | Owner |
| `registry.queries.parity_31` (SQ-G-Parity) | Named surfaces (Registry infrastructure · reflexive) | Built to attest V1-G7 parity 31/31 byte-identical is unaffected by this phase. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_parity` | fs-count + hash-diff | 1 cell · µs class | existing V1-G7 gate | 1 · Deterministic | Owner |
| `registry.queries.data_blind` (SQ-G-DataBlind) | Named surfaces (Registry infrastructure · reflexive) | Built to attest zero secrets/keys/tokens in the six findings artifacts (regex-negative on standard secret patterns). | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_standing_queries_sq_g1_to_g10.py::test_sq_g_data_blind` | grep-negative | 1 cell · µs class | governance §8 data-blind posture | 1 · Deterministic | Owner |

**Row count:** 10 SQ-G# reflexive rows.

---

## §S2. Promise attribution notes

Zero new promises introduced (Owner-explicit "correct conservatism, noted"). All 10 SQ-G rows reuse existing v0.md §2 promises via foreign-key resolution (MRR-E3 β lock):

- **PROM-S1-frozen-wire-contract** (v0.md §2 · 7 rows) — SQ-G1 · SQ-G2 · SQ-G3 · SQ-G-NoRetirement · SQ-G-ReportLevel · SQ-G-Rung1 · SQ-G-Parity. Registry query engine is a wire-contract-integrity check; parity + report-level determinism + rung-1 posture all belong to frozen-wire-contract class.
- **PROM-S3-audit-trail-immutable** (v0.md §2 · 3 rows) — SQ-G-Baseline · SQ-G-CrossRef · SQ-G-DataBlind. Baseline reproduction is audit-trail-preservation of ruled findings; cross-reference discipline is audit-trail-integrity between archaeological + mechanical surfaces; data-blind is governance §8 audit-trail-adjacency.

D7 respected · zero candidate promises minted · conservation-not-authorship posture held.

---

## §S3. Standing consequence attest (governance §14 · MRR-E4 β)

This supplement instantiates the pattern ruled in **governance §14** applied to Standing Queries as CI (§8.1.a): additive supplements beside a locked source. v0.1_supplement remains byte-identical at MRR SHA; v0.2 is new sibling supplement. MRR-G3's round-trip operates over `(v0.md + v0.1_supplement + v0.2_supplement)` ↔ machine form as one set — path-list drives the check (one-line parser data extension).

═══════════════════════════════════════════════════════════════════

*End of v0.2 supplement. 10 R4 reflexive rows for SQ-G* gates. v0.md byte-identical at SHA `598a7ad4…` and v0.1_supplement byte-identical at SHA `2822f99e…` preserved. Standing Rule v3 · on-disk canonical.*



---

## §v0.3-supplement-body — from `docs/registry/function_promise_registry_v0.3_supplement.md` · SHA `8d4cd2ed9c4e802944517908424ba2297ac3b4dd5e0d2a8e6d54f6042e64a8e4` (verbatim byte-carriage)

## §S1. R4 reflexive rows — IF-1 custody gates (3 rows · §3.2 schema)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `synisense.shield.custody_chain_wired` (IF1-G1) | Named surfaces (Shield chokepoint · reflexive) | Built to attest outbound text passes through `deidentifier.deidentify → llm_router.invoke_with_metering (litellm) → reidentifier.reidentify` in that exact order; a token in the outbound prompt is de-identified before reaching the LLM boundary; the reidentified response semantics match the pre-de-id token's contextual class per `reidentifier._VISIBLE_STRATEGY`. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shield_custody_chain.py::test_if1_g1_custody_chain_wired` | runtime check | 1 cell · ms class | shielded=True default + deidentifier + reidentifier module presence | 1 · Deterministic | Owner |
| `synisense.shield.fail_closed_deidentify_blocks_llm` (IF1-G2) | Named surfaces (Shield chokepoint · reflexive) | Built to attest that if `deidentifier.deidentify` raises `ServiceUnavailable` (spaCy-unloadable, tenant-lookup failure, or any other unrecoverable de-id failure), the LLM invocation does NOT occur AND the caller receives the ServiceUnavailable exception verbatim (fluency/brief synthesizers catch and route to mechanical arm per AF-E2 amended boundary; never a refusal envelope). | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_shield_custody_chain.py::test_if1_g2_fail_closed_deidentify_raise_blocks_llm` | runtime fail-closed cell | 1 cell · µs class | ServiceUnavailable → mechanical arm | 1 · Deterministic | Owner |
| `synisense.shield.fail_closed_reidentify_blocks_response` (IF1-G3) | Named surfaces (Shield chokepoint · reflexive) | Built to attest that if `reidentifier.reidentify` raises during the outbound seam (defence-in-depth; would be a bug given reidentify is pure regex), the LLM response is NOT returned to the caller — the exception surfaces via ServiceUnavailable at the chokepoint, preserving the never-return-raw-response guarantee. | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_shield_custody_chain.py::test_if1_g3_fail_closed_reidentify_raise_blocks_response` | runtime fail-closed cell | 1 cell · µs class | reidentifier presence + exception propagation | 1 · Deterministic | Owner |

**Row count:** 3 IF1-G# reflexive rows for the custody chain.

---

## §S2. R4 reflexive rows — Shave attestations (10 rows · §3.2 schema)

Per Owner IF-1 close: for each row shaved, an AST-negative test attests the module no longer exists AND no live import references it. Row numbers reference `docs/audits/deviation_audit_v1.md` §Part B table (2026-07-12).

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `deviation.shave.row_01_client_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/synisense/shield/client.py` no longer exists AND no in-tree file imports it; superseded by chokepoint-at-`llm_router.invoke_with_metering` (IF-1). | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_01_client_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 1 | 1 · Deterministic | Owner |
| `deviation.shave.row_03_audit_log_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/synisense/shield/audit_log.py` no longer exists AND no in-tree file imports it; chain-dead behind row 1. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_03_audit_log_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 3 | 1 · Deterministic | Owner |
| `deviation.shave.row_04_canonical_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/synisense/shield/canonical.py` no longer exists AND no in-tree file imports it; zero-caller observability tool retired. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_04_canonical_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 4 | 1 · Deterministic | Owner |
| `deviation.shave.row_05_purpose_validator_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/synisense/shield/purpose_validator.py` no longer exists AND no in-tree file imports it; `ALLOWED_PURPOSES` + `INTERNAL_ONLY_PURPOSE_PREFIXES` also removed from `services/synisense/config.py` per the shave-with-citation branch. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_05_purpose_validator_py_shaved` | AST-negative + fs-negative + config-negative | 1 cell · µs class | audit table row 5 | 1 · Deterministic | Owner |
| `deviation.shave.row_07_storage_service_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/storage_service.py` no longer exists AND no in-tree file imports it. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_07_storage_service_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 7 | 1 · Deterministic | Owner |
| `deviation.shave.row_08_generate_fixture_incoming_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/data_source/synthetic_assets/rms_adversarial_v1/rejected/generate_fixture.incoming.py` no longer exists AND no in-tree file imports it. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_08_generate_fixture_incoming_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 8 | 1 · Deterministic | Owner |
| `deviation.shave.row_09_generate_fixture_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/data_source/synthetic_assets/rms_adversarial_v1/generate_fixture.py` no longer exists AND no in-tree file imports it. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_09_generate_fixture_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 9 | 1 · Deterministic | Owner |
| `deviation.shave.row_14_v1_harness_metrics_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/v1_harness/metrics.py` no longer exists AND no in-tree file imports it. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_14_v1_harness_metrics_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 14 | 1 · Deterministic | Owner |
| `deviation.shave.row_15_purge_attestation_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/perception/purge_attestation.py` no longer exists AND no in-tree file imports it. Field access on `PerceptionResult.purge_attestation` (contract) is unaffected. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_15_purge_attestation_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 15 | 1 · Deterministic | Owner |
| `deviation.shave.row_16_telemetry_py` | Named surfaces (Deviation-audit reflexive) | Built to attest `services/perception/telemetry.py` no longer exists AND no in-tree file imports it. Field access on `PerceptionResult.telemetry` (contract) is unaffected. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_shave_v1_attestation.py::test_row_16_telemetry_py_shaved` | AST-negative + fs-negative | 1 cell · µs class | audit table row 16 | 1 · Deterministic | Owner |

**Row count:** 10 shave-attestation rows.

---

## §S3. Promise attribution notes

Zero new promises introduced (Owner-explicit conservation posture held; IF-1 close does not mint promises, it wires existing chain + shaves dead surface).

- **PROM-S1-frozen-wire-contract** (v0.md §2) — IF1-G1 (custody chain wired verifies the chokepoint wire-contract) + 10 shave rows (dead-surface AST-negatives are wire-contract integrity checks) = 11 rows.
- **PROM-S3-audit-trail-immutable** (v0.md §2) — IF1-G2 + IF1-G3 (fail-closed gates preserve audit-trail integrity of "never reach LLM raw" and "never return raw response") = 2 rows.

D7 respected · zero candidate promises minted · conservation-not-authorship posture held.

---

## §S4. Standing consequence attest (governance §14 · MRR-E4 β)

This supplement instantiates the pattern ruled in **governance §14** applied to IF-1 execution: additive supplement beside locked source. v0.md byte-identical at SHA `598a7ad4…` · v0.1_supplement byte-identical at SHA `2822f99e…` · v0.2_supplement byte-identical at SHA `25c5dd5a…`. v0.3_supplement is new sibling. MRR-G3's round-trip operates over `(v0.md + v0.1_supplement + v0.2_supplement + v0.3_supplement)` ↔ machine form as one set.

═══════════════════════════════════════════════════════════════════

*End of v0.3 supplement. 3 IF1-G* custody-chain gates + 10 shave-attestation gates = 13 R4 reflexive rows. Prior source-of-truth files byte-identical. Standing Rule v3 · on-disk canonical.*



---

## §v0.4-supplement-body — from `docs/registry/function_promise_registry_v0.4_supplement.md` · SHA `d1fa1949a206d5fb73481864962f93efaa888a4ef4793efad82a53681fc3dc1b` (verbatim byte-carriage)

## §S1. R4 reflexive rows — Trace surface promotion (2 rows · §3.2 schema)

Closes G-7 (SolvaTrace three-lens rendering surface commitment) and G-10 (frontend /legacy/* disposition) simultaneously: the three-lens Trust Receipt lifts out of the archived `/legacy/*` tree and mounts at public `/trace` + `/trace/:traceId`; the AppShell chrome and the seven other legacy pages retire whole at the same ruling.

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `rms.frontend.trace_receipt_page_promoted_public_route` (G-7 close) | Named surfaces (Frontend UI · reflexive) | Built to attest the SolvaTrace three-lens rendering surface (§5 Spec) is a live-visible public route: `src/pages/trace/TraceReceiptPage.js` exists on-disk AND `src/App.js` imports it from `./pages/trace/TraceReceiptPage` AND declares both `<Route path="trace">` and `<Route path="trace/:traceId">`. The three-lens sections (`trace-ledger-section` · `trace-solva-section` · `trace-plans-section` · `trace-registry-section`) render the envelope returned by `GET /api/northena/trace/{traceId}`; back-link resolves to Ask Console at `/` (single-ingress per UI Spec §3.1). | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` + `frontend/e2e/trace_smoke.spec.ts::trace_receipt_page_renders_three_lens_at_promoted_public_route` | jest static-grep + playwright DOM assertion | 1 cell · ms class | apiClient.traceLens + useApi hook + LedgerTable/ClassBadge/StatusBadge components | 1 · Deterministic | Owner |
| `rms.frontend.legacy_shell_retired` (G-10 close) | Named surfaces (Frontend UI · reflexive) | Built to attest the archived `/legacy/*` tree and its AppShell chrome are gone: `src/legacy/` directory does NOT exist AND `src/components/AppShell.js` does NOT exist AND `src/App.js` no longer declares `<Route path="legacy">` block AND no in-tree import references either `./legacy/pages/` or `./components/AppShell`. The G-10 disposition ("evidence at IF-1 close → OWNER decision") is discharged by this ruling. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` | jest static-grep (fs-negative + import-negative + Route-block-negative) | 1 cell · µs class | frontend build clean · yarn build passes · legacy tree fully removed | 1 · Deterministic | Owner |

**Row count:** 2 promote/retire reflexive rows.

---

## §S2. R4 reflexive rows — Legacy page shave attestations (7 rows · §3.2 schema)

Per Owner G-10 close: for each of the seven retired legacy pages, an fs-negative test attests the module no longer exists AND no live consuming route references it. All seven are covered by a single mechanical gate that iterates the `LEGACY_PAGE_NAMES` set (`test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js`); rows enumerate the individual files per §3.2 schema granularity.

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `deviation.shave.frontend_landing_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/LandingPage.js` no longer exists AND `src/App.js` no longer imports it; nested `<Route index element={<LandingPage/>}>` under `/legacy/*` retired at G-10 close. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 1) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_operator_dashboard` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/OperatorDashboard.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 2) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_runs_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/RunsPage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/runs` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 3) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_run_detail_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/RunDetailPage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/runs/:runId` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 4) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_discipline_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/DisciplinePage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/discipline` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 5) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_engines_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/EnginesPage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/engines` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 6) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |
| `deviation.shave.frontend_compose_page` | Named surfaces (Deviation-audit reflexive) | Built to attest `frontend/src/legacy/pages/ComposePage.js` no longer exists AND `src/App.js` no longer imports it; nested `/legacy/operator/compose` route retired. | PROM-S1-frozen-wire-contract | S1.call | `frontend/src/__tests__/ui_spec_v1/test_g5b_legacy_pages_archived_under_frontend_legacy_directory.test.js` (legacy dir absent · row 7) | fs-negative + import-negative | 1 cell · µs class | G-10 ruling row | 1 · Deterministic | Owner |

**Row count:** 7 legacy-page shave-attestation rows.

**Note on AppShell chrome:** the retirement of `src/components/AppShell.js` (only-consumer-was-legacy) is folded into row `rms.frontend.legacy_shell_retired` (§S1) rather than minted as a separate row, since the AppShell has no distinct governor promise beyond "carry the /legacy/* nested outlet"; §S1 row's fs-negative already covers it explicitly.

---

## §S3. Promise attribution notes

Zero new promises introduced (Owner-explicit conservation posture held; G-10/G-7 PROMOTE does not mint promises, it discharges G-7 by making the three-lens rendering surface live-visible AND discharges G-10 by shaving the archived tree).

- **PROM-S1-frozen-wire-contract** (v0.md §2) — G-7 close (three-lens public route wire-contract) + G-10 close (retired shell wire-contract negative) + 7 shave rows (dead-surface fs-negatives are wire-contract integrity checks) = 9 rows.

D7 respected · zero candidate promises minted · conservation-not-authorship posture held.

---

## §S4. Standing consequence attest (governance §14 · MRR-E4 β)

This supplement instantiates the pattern ruled in **governance §14** applied to G-10/G-7 PROMOTE: additive supplement beside locked source. v0.md byte-identical at SHA `598a7ad4…` · v0.1_supplement byte-identical at SHA `2822f99e…` · v0.2_supplement byte-identical at SHA `25c5dd5a…` · v0.3_supplement byte-identical at SHA `8d4cd2ed…`. v0.4_supplement is new sibling. MRR-G3's round-trip operates over `(v0.md + v0.1_supplement + v0.2_supplement + v0.3_supplement + v0.4_supplement)` ↔ machine form as one set.

═══════════════════════════════════════════════════════════════════

*End of v0.4 supplement. 2 G-10/G-7 promote/retire rows + 7 legacy-page shave-attestation rows = 9 R4 reflexive rows. Prior source-of-truth files byte-identical. Standing Rule v3 · on-disk canonical.*



---

## §v0.5-supplement-body — from `docs/registry/function_promise_registry_v0.5_supplement.md` · SHA `d2d0c5f4c37dcbe525ff99a757687d7ae81446cd738719341e2b7884d4ac778f` (verbatim byte-carriage)

## §S1. Structured-source connector class + license_class default (MC-E1 α + MC-E4 α)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `akki.data_source.structured_connector_base` (MC-E1 α close) | Named surfaces (data_source) | Built to expose a generic tabular/DB ingest class that produces `NormalizedUnit` instances via the existing five_rings@v0 shape (modality=text, locator dict `{table, row, cols}`, extraction_params satisfying the text-modality catalogue). Zero contract mutation. | PROM-S1-frozen-wire-contract | S2.onboard-context | services/data_source/structured_connector.py | pytest (test_instance_fixture_b_walkthrough::test_structured_connector_produces_valid_normalized_units) | 1 cell · µs class | contracts/five_rings.py unchanged | 1 · Deterministic | Owner |
| `akki.data_source.tabular_ingest_normalizes_units_zero_contract_mutation` (MC-E1 α attest) | Named surfaces (data_source · reflexive) | Built to attest tabular rows map to NormalizedUnits without any mutation to `contracts/five_rings.py` or its snapshot. Parity 31 held byte-identical (contracts/ + snapshot diff-empty). | PROM-S1-frozen-wire-contract | S2.onboard-context | tests/registry/test_instance_fixture_b_walkthrough.py + parity_31 gate | pytest + fs-negative on contracts/ diff | 1 cell · µs class | five_rings@v0 shape | 1 · Deterministic | Owner |
| `akki.data_source.license_class_pairs_at_ingest` (MC-E4 α close) | Named surfaces (data_source) | Built to attach `license_class` at the connector-registration layer (default `internal_only` per MC-E4 α fail-closed); riding receipts (Op. Values §7) rather than the frozen NormalizedUnit shape. Artifacts derived from default-classed units refuse the outer gate to S4 until operator explicitly upgrades. | PROM-S1-frozen-wire-contract | S4.receive | services/data_source/structured_connector.py::license_class_permits_s4_egress | pytest (test_license_class_default_is_internal_only_fail_closed) | 1 cell · µs class | outer_gate/receipt.py contract unchanged | 1 · Deterministic | Owner |

## §S2. S2.onboard surface + initial-set ledger (MC-E3 α + Op. Values §8)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `akki.frontend.s2_onboard_public_route` (surface-registered) | Named surfaces (frontend + backend) | Built to expose the S2.onboard structured-intake surface at `POST /api/instance/{instance_id}/onboard` accepting the Op. Values §8 payload (estate inventory · org vocabulary · rights posture per source · DPO contact · five §6 seam values · objective priorities). Versioned `onboard_context_v0`. | PROM-S1-frozen-wire-contract | S2.onboard-context | routers/s2_onboard.py + services/multi_instance/onboard_context.py | pytest (test_instance_fixture_b_walkthrough::test_s2_onboard_fixture_b_walkthrough) | 1 cell · ms class | tenant_entities.py write-path seat | 1 · Deterministic | Owner |
| `akki.backend.s2_onboard_receiver_persists_instance_scoped` (MC-E2 α attest) | Named surfaces (backend · reflexive) | Built to attest S2.onboard writes land in `instance_onboard_context` collection scoped by `instance_id`; no cross-instance write leak. | PROM-S1-frozen-wire-contract | S2.onboard-context | tests/registry/test_instance_fixture_b_walkthrough.py + scoped_accessor | pytest cross-instance denial | 1 cell · ms class | scoped_accessor helpers | 1 · Deterministic | Owner |
| `akki.backend.s2_onboard_writes_five_seam_values_dual_control_adjacent` (MC-E3 α close) | Named surfaces (backend) | Built to attest initial-set writes = single-operator (pre-birth defaults); every initial seam-value set writes a `northena_ledger` row with `initial_set: true` marker (ceremony waived, audit trail preserved). Subsequent changes to already-set values return 409 pending full §6 ceremony (dual-control for class-C deletion + rule-tightening delay). | PROM-S1-frozen-wire-contract | S2.onboard-context | routers/s2_onboard.py::_append_initial_set_ledger_row | pytest (409 on second onboard) + ledger-row shape assertion | 1 cell · ms class | northena_ledger append_only | 1 · Deterministic | Owner |
| `akki.backend.tenant_entities_populates_from_s2_onboard` (surface-registered) | Named surfaces (SyniSense) | Built to attest the IF-1-era empty-catalogue stub at `services/synisense/shield/tenant_entities.py` becomes the tenant-entity seat populated by S2.onboard's `org_vocabulary` field. Connector-registration output is also written here per Op. Values §8 line 89. | PROM-S1-frozen-wire-contract | S2.onboard-context | services/synisense/shield/tenant_entities.py + routers/s2_onboard.py | pytest (onboard walkthrough writes org_vocabulary ledger row) | 1 cell · ms class | Shield custody chain | 1 · Deterministic | Owner |

## §S3. Multi-instance operability v1 · isolation cells (MC-E2 α + backfill)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `akki.instance.identity_from_config_only` (surface-registered) | Named surfaces (instance) | Built to expose `GET /api/instance/config` returning the per-instance config (instance_id · display_name · product_title). Public read (no auth). Frontend hydrates branding at boot. Instance identity lives in config, not code. | PROM-S1-frozen-wire-contract | S1.call | routers/instance.py + config/instances/{instance_id}.json | pytest + integration curl | 1 cell · µs class | config/instances/ | 1 · Deterministic | Owner |
| `akki.instance.seams_scoped_by_instance_id` (MC-E2 α · reflexive) | Named surfaces (Deviation-audit reflexive) | Built to attest per-instance seam values, estate inventory, model-registry, connector registrations, and instance identity ride under `instance_id` scope; scoped_accessor helpers refuse unscoped queries via InstanceScopeError. | PROM-S1-frozen-wire-contract | S2.onboard-context | services/multi_instance/scoped_accessor.py + tests/registry/test_instance_isolation.py | pytest (5 isolation cells) | 1 cell · µs class | Motor client | 1 · Deterministic | Owner |
| `akki.instance.no_cross_instance_read_on_any_surface` (MC-E2 α · reflexive) | Named surfaces (Deviation-audit reflexive) | Built to attest fixture-A auth-token cannot read fixture-B rows via scoped helpers across every persistent collection (registry · ledger · keys · census · connector · onboard). Adversarial cross-instance cells verify denial. | PROM-S1-frozen-wire-contract | S1.call | tests/registry/test_instance_isolation.py::test_cross_instance_read_denied | pytest adversarial cell | 1 cell · µs class | scoped_accessor.sfind | 1 · Deterministic | Owner |
| `akki.instance.backfill_migration_attests_zero_unscoped_rows` (MC-E2 α condition · attest) | Named surfaces (backend · reflexive) | Built to attest all 8,657 pre-existing rows across 9 persistent collections were backfilled to `instance_id = "instance_1"` at commit-time; post-migration attestation returns 0 unscoped rows per collection. | PROM-S1-frozen-wire-contract | S2.onboard-context | tools/migrations/backfill_instance_id_2026_07_14.py + tests/registry/test_instance_isolation.py::test_backfill_attestation_no_unscoped_rows_remain | pytest re-run backfill + post-condition | 1 cell · ms class | Motor client | 1 · Deterministic | Owner |
| `akki.instance.compound_index_ensures_scoped_read_performance` (constraint architecture attest) | Named surfaces (backend · reflexive) | Built to attest compound `(instance_id, ...)` indexes exist on 11 persistent collections (northena_ledger, northena_ledger_rows, objectives_async_state, targeta_mining_plans, mtafiti_registry_records, engineer_key_grants, wizard_sessions, wizard_session_bindings, users, checker_requests, engineer_invites). D-6 constraint architecture: persistence layer supports scoped reads efficiently. | PROM-S1-frozen-wire-contract | S1.call | tools/migrations/backfill_instance_id_2026_07_14.py index creation + tests/registry/test_instance_isolation.py::test_ensure_instance_index_creates_compound_index | pytest index-shape assertion | 1 cell · µs class | Motor create_index | 1 · Deterministic | Owner |
| `akki.instance.scoped_accessor_refuses_unscoped_query` (MC-E2 α · reflexive) | Named surfaces (Deviation-audit reflexive) | Built to attest `scoped_accessor.sfind_one`, `sfind`, `sinsert_one`, `scount_documents` raise `InstanceScopeError` when called with `instance_id=None` or empty string. Persistence layer refuses unscoped queries by design (D-6 "correct behavior is the path of least resistance"). | PROM-S1-frozen-wire-contract | S1.call | tests/registry/test_instance_isolation.py::test_scoped_helper_refuses_unscoped_query | pytest exception assertion | 1 cell · µs class | InstanceScopeError | 1 · Deterministic | Owner |

## §S4. RMS de-tuning — contract-tier class-(c) attestation (MC-E5 α)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `akki.detune.contract_tier_rms_tokens_preserved_class_c_historical_by_ruling` (MC-E5 α attest) | Named surfaces (Deviation-audit reflexive) | Built to attest all `RMS`-tokens inside `backend/contracts/*.py` (14 files) and `backend/tests/invariants/*.contract_snapshot.json` (2 files, 4 line hits) remain byte-identical per Owner ruling MC-E5 α: contract-tier tokens are class-(c) citations to the platform's own mandate filenames (`docs/mandates/archive/RMS_*.md`) — architectural history, not customer identity. Code shape already organization-agnostic. | PROM-S1-frozen-wire-contract | S1.call | contracts/*.py + tests/invariants/*.contract_snapshot.json | fs-grep + Parity 31 seal | 1 cell · µs class | Standing Rule v3 | 1 · Deterministic | Owner |

## §S5. RMS de-tuning — live wire cutover (MC-E6 β + MC-E6 α)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `akki.detune.http_headers_renamed_hard_cutover_2026_07_14` (MC-E6 β) | Named surfaces (Deviation-audit reflexive) | Built to attest HTTP headers `X-RMS-App-ID` and `X-RMS-Webhook-URL` renamed to `X-Akki-App-ID` and `X-Akki-Webhook-URL` at every read-site (routers/objectives.py + services/synisense/webhook_registration.py + backing tests). Hard cutover authorized by STEP 1 pre-flight guard result: 0 non-fixture external integrators (evidence-based ruling). | PROM-S1-frozen-wire-contract | S1.call | routers/objectives.py + services/synisense/webhook_registration.py + tests/invariants/test_phase_5_stage_b_async_delivery.py | grep-negative `X-RMS-App-ID`, `X-RMS-Webhook-URL` on live tree | 1 cell · µs class | STEP 1 guard AUTHORIZED | 1 · Deterministic | Owner |
| `akki.detune.env_vars_renamed_hard_cutover_2026_07_14` (MC-E6 β) | Named surfaces (Deviation-audit reflexive) | Built to attest all live-code `RMS_*` env var reads renamed to `AKKI_*` at every `os.environ.get()` call site (139 occurrences across 26 files). Preserved: values byte-identical; only variable NAMES change. Deployment env files (.env) updated in lockstep. | PROM-S1-frozen-wire-contract | S1.call | services/**/*.py + routers/**/*.py + tests/**/*.py + .env | grep-negative `os.environ.get(['"]RMS_` on live tree (excl. retired-token gate) | 1 cell · µs class | STEP 1 guard AUTHORIZED | 1 · Deterministic | Owner |
| `akki.detune.db_name_preserved_config_resident` (MC-E6 α for DB_NAME) | Named surfaces (Deviation-audit reflexive) | Built to attest `DB_NAME` variable name unchanged; instance-#1's VALUE stays `rms_intelligence` (data preserved — value is instance identity, config-resident). New instances mint new DB_NAME values. Zero migration risk on live deployment. | PROM-S1-frozen-wire-contract | S1.call | backend/.env + backend/core.py | fs-check DB_NAME=rms_intelligence unchanged | 1 cell · µs class | live Mongo topology | 1 · Deterministic | Owner |
| `akki.detune.retired_token_grep_negative_gates_preserved_verbatim` (Owner ruling) | Named surfaces (Deviation-audit reflexive) | Built to attest `test_master_admin_auth_reconciliation.py` preserved BYTE-IDENTICAL — retired-token grep-negative gate (`RMS_MASTER_ADMIN_TOKEN` / `X-RMS-Master-Admin`) tests that RETIRED tokens are NOT emitted; renaming would defeat check semantics per Owner ruling. | PROM-S1-frozen-wire-contract | S1.call | tests/invariants/test_master_admin_auth_reconciliation.py | fs-grep + byte-identity check | 1 cell · µs class | Standing Rule v3 | 1 · Deterministic | Owner |
| `akki.detune.fixture_dir_renamed_org_agnostic` (Class-(b)) | Named surfaces (Deviation-audit reflexive) | Built to attest `rms_adversarial_v1` fixture directory renamed to `instance_fixture_a` (org-agnostic name). Downstream references updated across 12 files + 21 token occurrences. Fixture body preserved byte-identical (SHA `e4d147a8ad83c26502d1b85614f9b32ab427b1103a262546400d940612250b08` of the JSON content is unchanged; only the `_manifest.fixture` label updated from `rms_adversarial_synthetic_v1` to `instance_fixture_a_v1`). | PROM-S1-frozen-wire-contract | S1.call | services/data_source/synthetic_assets/instance_fixture_a/ + all test refs | git mv attest + reference-count | 1 cell · µs class | 47 test import updates | 1 · Deterministic | Owner |
| `akki.detune.branding_moved_to_instance_config` (Class-(a)) | Named surfaces (frontend · reflexive) | Built to attest 20 class-(a) branding hits ("RMS Intelligence") moved from live frontend code to instance config accessor via `/api/instance/config` + `useInstanceConfig` hook. Instance-#1's config file at `backend/config/instances/instance_1.json` carries "RMS Intelligence" verbatim per Owner: "instance #1's config carries 'RMS Intelligence'". | PROM-S1-frozen-wire-contract | S1.call | frontend/src/hooks/useInstanceConfig.js + backend/config/instances/ + routers/instance.py | jest (Gate 3 Part A `zero_raw_fetch_calls_outside_apiClient`) + integration curl | 1 cell · µs class | apiClient.instanceConfig | 1 · Deterministic | Owner |

## §S6. Fixture-B end-to-end walkthrough (MC-E2 α proof shape)

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `akki.ci.fixture_b_walks_onboard_to_answer_e2e` (MC-E2 α proof) | Named surfaces (CI · reflexive) | Built to attest instance-fixture-B (generic tabular synthetic estate at `services/data_source/synthetic_assets/instance_fixture_b/fixture.json`, 3 rows) walks the full onboard → connect → census → brief → answer surface end-to-end, with isolation cells proving no cross-instance read on any surface (registry · ledger · keys · census · onboard). | PROM-S1-frozen-wire-contract | S2.onboard-context | tests/registry/test_instance_fixture_b_walkthrough.py | pytest (9 cells) + AsyncClient httpx | 1 cell · ms class | scoped_accessor + s2_onboard + structured_connector | 1 · Deterministic | Owner |

## §S7. Promise attribution notes

Zero new promises introduced (conservation-not-authorship posture held). Every row cites existing promises:
- **PROM-S1-frozen-wire-contract** — MC-E1 α zero-mutation attest · isolation cells · scoped_accessor discipline · retired-token gate preservation · fixture rename · branding relocation · env var cutover · header cutover · DB_NAME preservation · S2.onboard route surface. **20 rows.**
- **PROM-S1-frozen-wire-contract** — S2.onboard endpoint + initial-set ledger + instance-scoped receiver + tenant-entities population. **3 rows.**
- **PROM-S1-frozen-wire-contract** — MC-E4 α license_class default = internal_only, fail-closed at outer gate. **1 row.**

D7 respected · zero candidate promises minted · conservation-not-authorship posture held.

## §S8. Standing consequence attest (governance §14 · MRR-E4 β)

This supplement instantiates the pattern ruled in governance §14 applied to Multi-Instance Capability MC-E1..MC-E6: additive supplement beside locked source. v0.md byte-identical at SHA `598a7ad4…` · v0.1_supplement byte-identical at SHA `2822f99e…` · v0.2_supplement byte-identical at SHA `25c5dd5a…` · v0.3_supplement byte-identical at SHA `8d4cd2ed…` · v0.4_supplement byte-identical at SHA `d1fa1949…`. v0.5_supplement is new sibling. MRR-G3's round-trip operates over `(v0.md + v0.1 + v0.2 + v0.3 + v0.4 + v0.5)` ↔ machine form as one set.

═══════════════════════════════════════════════════════════════════

*End of v0.5 supplement. 3 rows §S1 + 4 rows §S2 + 6 rows §S3 + 1 row §S4 + 6 rows §S5 + 1 row §S6 = 21 R4 reflexive rows. Prior source-of-truth files byte-identical. Standing Rule v3 · on-disk canonical.*



---

## §Q3-Amendments · Post-v0 re-disposition of Q3 findings

Registry Doctrine v1.0 §3.4: findings are never dropped; re-dispositions land as append-only annotations to the original finding row. This section carries post-v0 rulings that update Q3 disposition without editing the original row (Standing Rule v3 · v0.md byte-identical).

| finding_id | prior_disposition | new_disposition | ruling_ref | attest_evidence |
|---|---|---|---|---|
| **Q3-02** (S2.onboard-context) | `[RULED · Q3-02-OPEN-BY-DESIGN 2026-07-11 · [OWNER: future phase]]` | **`[RE-RULED · Q3-02-BUILT 2026-07-14 · MC-E3 α close]`** | `docs/rulings/mc_e1_to_e6_2026-07-14.md` (Multi-Instance Capability MC-E3 α ruling) | `services/multi_instance/onboard_context.py` (S2.onboard implementation) · `routers/s2_onboard.py::post_onboard` (POST /api/instance/{instance_id}/onboard) · `tests/registry/test_instance_fixture_b_walkthrough.py::test_s2_onboard_fixture_b_walkthrough` (E2E) · v0.5 supplement §S2 rows `akki.frontend.s2_onboard_public_route` + `akki.backend.s2_onboard_receiver_persists_instance_scoped` + `akki.backend.s2_onboard_writes_five_seam_values_dual_control_adjacent` + `akki.backend.tenant_entities_populates_from_s2_onboard` |

**Q3-02 promotion attest:** S2.onboard-context journey step now has machine-enforceable surface (previously RP-E3 α-amended (i)∧¬(ii) landing). Journey step BUILT · testable · covered by 9 CI cells (v0.5 supplement §S6 fixture-B walkthrough). Original v0.md §5 Q3-02 row remains byte-identical (this section is annotation-append only).


---

## §Conformance-Evidence-Registry · Per-engine attestation citations (metadata addition · IF-1 close fold)

Metadata-addition section per Registry Doctrine §3.2 field enrichment (not a promise-text mutation). Cites `docs/audits/engine_conformance_v1.md` (IF-1 close · 2026-07-12 · authorized) and companion audits for BUILT/PARTIAL/SUPERSEDED verdicts on core engine surfaces. Rows here are cross-references to §v0-body function rows, not new function rows.

| function_id (v0.md §3) | verdict | evidence_citation | notes |
|---|---|---|---|
| `solva.trace.receipt_resolution` | BUILT | `docs/audits/engine_conformance_v1.md:A.1 · services/solva_depth/pipeline.py:1-27 · routers/solva.py` | Mandate §7, §15. |
| `solva.compliance.prove_one_run` | BUILT | `docs/audits/engine_conformance_v1.md:A.1 · services/solva_depth/reasoning/` (frame · candidate · tension · reflection) | Mandate §8. |
| `targeta.commission_wizard.slice_freeze` | BUILT | `docs/audits/engine_conformance_v1.md:A.2 · services/targeta/plan.py:1-14 · gate.py:1-19` | Mandate §12, §17 #8. |
| `targeta.transform_form.per_call_provisioning` | BUILT | `docs/audits/engine_conformance_v1.md:A.2 · services/targeta/interface.py:1-12` | Set-preserving boundary. |
| `targeta.transform_form.frozen_wire_contract` | BUILT | `docs/audits/engine_conformance_v1.md:A.2 · backend/contracts/transform_form_v0.py` | TF-G1..G5. |
| **[modes.py surface]** | **SUPERSEDED** | `docs/audits/g4_targeta_conformance_v1.md:23` — SPEC_EXPANSION: inlined into `plan.build_plan(mode=…)` · `services/targeta/__init__.py:9` stale comment carries deviation row 20 | `superseded_by: docs/audits/g4_targeta_conformance_v1.md:23`. Not ABSENT — surface exists via SPEC_EXPANSION. |
| `mtafiti.perception.pinned_model_provenance` | BUILT | `docs/audits/g4_mtafiti_conformance_v1.md` · `services/mtafiti/**` | 9.2a-E1 α. |
| `northena.ledger.append_only_gate` | BUILT | `docs/audits/northena_conformance_v1.md` · `services/northena/ledger.py` | S3.prove journey. |
| `synisense.shield.custody_chain_wired` (v0.3 §S1 IF1-G1) | BUILT | IF-1 close · `backend/services/synisense/shield/{deidentifier,llm_router,reidentifier}.py` · `tests/registry/test_shield_custody_chain.py::test_if1_g1_custody_chain_wired` | Custody chain reconnected at IF-1. Row is LIVE per v0.3 supplement (RM-E1 α byte-carriage preserved). |
| `synisense.shield.fail_closed_deidentify_blocks_llm` (v0.3 §S1 IF1-G2) | BUILT | IF-1 close · `tests/registry/test_shield_custody_chain.py::test_if1_g2_fail_closed_deidentify_raise_blocks_llm` | Fail-closed. |
| `synisense.shield.fail_closed_reidentify_blocks_response` (v0.3 §S1 IF1-G3) | BUILT | IF-1 close · `tests/registry/test_shield_custody_chain.py::test_if1_g3_fail_closed_reidentify_raise_blocks_response` | Defense-in-depth. |
| `rms.frontend.trace_receipt_page_promoted_public_route` (v0.4 §S1 G-7 close) | BUILT | `docs/rulings/g10_g7_promote_2026-07-14.md` · `frontend/src/pages/trace/TraceReceiptPage.js` mounted at `/trace` + `/trace/:traceId` | Three-lens rendering surface promoted from `/legacy/*` to public route. |
| `rms.frontend.legacy_shell_retired` (v0.4 §S1 G-10 close) | BUILT | `docs/rulings/g10_g7_promote_2026-07-14.md` · `frontend/src/legacy/` absent · `frontend/src/components/AppShell.js` absent | Legacy tree fully removed. |

**Metadata-addition posture:** all cells above are pointers into existing evidence files. Zero promise-text mutation. Zero new function rows. Zero new promises. Conformance evidence is cross-reference metadata per Registry Doctrine §3.2 field enrichment.


---

## §M · G-2 Registry Maintenance · R4 reflexive rows (Q4 standing query + consolidation attestation · 8 rows)

**Ruling:** `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md` (RM-E1 α · RM-E2 α · RM-E3 α + advisory).
**Conservation posture:** zero new promises; all 8 rows reuse `PROM-S1-frozen-wire-contract` via foreign-key resolution (§v0-body §2).
**Namespace:** `akki.registry.*` (Multi-Instance Capability MC-E6 β post-cutover naming; all future reflexive rows use `akki.*` namespace).

| function_id | governor | mandate | promise | service_trace | surface | enforcement | cost | dependencies | ladder_rung | owner |
|---|---|---|---|---|---|---|---|---|---|---|
| `akki.registry.q4_standing_query_run` | Named surfaces (Registry infrastructure · reflexive) | Built to attest Q4 (behavioral-rule attestation) mechanical scan runs at every close: for every behavioral-rule row in v1, verify the row names its evidencing telemetry-or-gate, or mark UNVERIFIED. Two-file archaeological/mechanical pattern per SQ-E1 γ. | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/queries.py::run_q4` + test cell | runtime check | 1 cell · ms class | machine form · function-row iteration | 1 · Deterministic | Owner |
| `akki.registry.q4_archaeological_byte_identical_reproduction` | Named surfaces (Registry infrastructure · reflexive) | Built to attest Q4 archaeological carry-over file reproduces byte-identical on successive runs (SQ-G-Baseline pattern extended). Fail-loud + HALT for Owner on any deviation. | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_q4_gates.py::test_q4_archaeological_reproduction_byte_identical` | byte-identity lock | 1 cell · ms class | q4_archaeological.md source | 1 · Deterministic | Owner |
| `akki.registry.q4_mechanical_scan_reports_unverified_rules` | Named surfaces (Registry infrastructure · reflexive) | Built to attest Q4 mechanical scan enumerates every behavioral-rule row lacking a named telemetry/gate reference, emits `[CLIENT-PROMISE · UNVERIFIED · ESCALATE-AT-CLOSE]` flag per RM-E3 α when on a client-promise surface, and lands report-level artifact (NEVER build-failing). | PROM-S1-frozen-wire-contract | S1.call | `backend/services/registry/queries.py::scan_q4_behavioral_rules` + test cell | runtime check | 1 cell · µs class | v1.md rows · machine form | 1 · Deterministic | Owner |
| `akki.registry.q4_cross_reference_condition_holds` | Named surfaces (Registry infrastructure · reflexive) | Built to attest zero Q4 mechanical entries whose subject overlaps an existing archaeological finding are emitted without `overlaps: <finding_id>` annotation. SQ-G-CrossRef pattern extended to Q4. Permanent discipline. | PROM-S3-audit-trail-immutable | S3.prove | `backend/services/registry/queries.py::annotate_q4_mechanical_overlaps` + test cell | runtime check | 1 cell · µs class | archaeological-subjects index · Q4 mechanical output | 1 · Deterministic | Owner |
| `akki.registry.v1_consolidated_body_preserves_supplement_row_texts_byte_identical` | Named surfaces (Registry infrastructure · reflexive) | Built to attest v1 body preserves every promise-text field from v0.md + v0.1..v0.5 supplements byte-identical (RM-E1 α HARD GATE). Any drift = HALT + logged in v1 §D-drift for future ruled amendment turn (never edited in-flight). | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_registry_v1_consolidation_byte_identity.py::test_v1_promise_text_byte_identical_to_source` | byte-identity lock | 1 cell · ms class | v0.md + supplement source files · v1.md target file | 1 · Deterministic | Owner |
| `akki.registry.q4_parity_gate` | Named surfaces (Registry infrastructure · reflexive) | Built to attest Parity 31 held byte-identical during Q4 run (contracts/ + snapshots diff-empty). Q4 execution is doc-only + query-engine additive; contract touches forbidden. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_q4_gates.py::test_q4_run_holds_parity_31` | fs-count + hash-diff | 1 cell · µs class | existing V1-G7 gate + SQ-G-Parity | 1 · Deterministic | Owner |
| `akki.registry.q4_data_blind_gate` | Named surfaces (Registry infrastructure · reflexive) | Built to attest zero secrets/keys/tokens in the Q4 artifacts (regex-negative on standard secret patterns; governance §8 data-blind extended to Q4). | PROM-S3-audit-trail-immutable | S3.prove | `backend/tests/registry/test_q4_gates.py::test_q4_artifacts_data_blind` | grep-negative | 1 cell · µs class | q4_archaeological.md + q4_mechanical.md | 1 · Deterministic | Owner |
| `akki.registry.part_ii_journey_steps_alias_canonicalization_completed` | Named surfaces (Registry infrastructure · reflexive) | Built to attest `PART_II_JOURNEY_STEPS` frozenset in `backend/services/registry/validator.py` canonicalizes to short forms (`S3.prove`, `S4.verify`); legacy aliases (`S3.prove-end-to-end`, `S4.verify-receipt`) rejected. Governance-amendment-only clause per Owner ruling. | PROM-S1-frozen-wire-contract | S1.call | `backend/tests/registry/test_part_ii_journey_steps_alias_canonicalization.py::test_canonical_forms_present_legacy_aliases_rejected` | frozenset-membership check | 1 cell · µs class | validator.py PART_II_JOURNEY_STEPS constant | 1 · Deterministic | Owner |

**§M row count: 8** R4 reflexive rows.
**Promise attribution:** 6 rows attach to `PROM-S1-frozen-wire-contract` (Q4 scan/parity/data-blind-via-frozen-wire-integrity/consolidation/alias/mechanical); 2 rows attach to `PROM-S3-audit-trail-immutable` (archaeological byte-identical reproduction · cross-reference discipline). All 8 target existing promises (§v0-body §2). **Zero new promises minted.** D-7 respected · conservation-not-authorship posture held.


---

## §D-drift · Byte-identity drift findings (RM-E1 α discipline)

**Discipline:** any promise-text divergence between v1 and its source (v0.md or v0.N_supplement.md) lands here as a `[DRIFT · finding-id · source-path:line · target-path:line · description]` row, for future Owner-dispatched ruled amendment turn. **Never edited in-flight** (RM-E1 α HARD GATE).

**Status this turn:** Zero drift findings. v1 body concatenates v0.md §v0-body + each supplement's §v0.X-supplement-body verbatim (no row-level edits). Every promise text and every foreign-key promise reference in v1 is byte-identical to its source per the mechanical fold implementation (see `backend/tests/registry/test_registry_v1_consolidation_byte_identity.py` for the machine-enforced attest cell · R4 row `akki.registry.v1_consolidated_body_preserves_supplement_row_texts_byte_identical`).


═══════════════════════════════════════════════════════════════════

*End of Function-Promise Registry v1.0. Consolidated 2026-07-14 per Owner ruling `docs/rulings/g2_rm_e1_to_e3_2026-07-14.md`. RM-E1 α byte-carriage · RM-E2 α client-promise sub-table · RM-E3 α + advisory annotation. Predecessor lineage (v0.md + v0.1..v0.5) byte-identical on-disk per Standing Rule v3. 8 R4 reflexive rows in §M · zero new promises · all target existing `PROM-S1-frozen-wire-contract` / `PROM-S3-audit-trail-immutable`. Parity 31/31 preserved (zero contract touch). Q3-02 re-disposition to BUILT per §Q3-Amendments. Conformance evidence cross-refs in §Conformance-Evidence-Registry. Standing Rule v3 · on-disk canonical.*
