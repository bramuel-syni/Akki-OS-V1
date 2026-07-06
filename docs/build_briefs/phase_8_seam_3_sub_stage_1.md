Verification MATCHED. `3fe969c2…` cryptographically legitimate. Amendment E ratified in full. This is the Sub-stage 1 build brief. Build UN-PAUSED for Sub-stage 1 scope only. Respond in English only.

## §1. Authority sources (verbatim, no paraphrase, no expansion beyond cited scope)

- **Stage A proposal** — `/app/docs/stage_a_proposals/phase_8_seam_3_and_checker.md` — SHA `3fe969c2add52da7f4d80251a8bcb2d1bcf3154c82a10a7fb2241d44bb08500d`. §5 (Sub-stage 1 deliverables) is the scope authority — read verbatim, execute as written, do NOT flatten or expand.
- **Rulings record** — `/app/docs/rulings/seam_3_stage_a_e1_to_e7.md` — SHA `37db1729c26be94a7dfb8f4eb79cb14ab2ff62e56506b1a82b18d22cfab2e211`. §1 (E1–E7 verbatim) + §8 (Owner refinements) are the ruling authority.
- **BCR v1.4.1** — `/app/docs/mandates/RMS_Build_Completion_Requirements_v1_4.md` — SHA `ce5206c9e244fe58edb6824f785077c1c835bdf3f5b347f6a4fb98c036212524`. §3.5 + §3.11 CK-U1 (middle-dot binding copy).
- **Conformance map** — `/app/docs/close_reports/phase_8_conformance_map.md` — SHA `e747a0f6…` prefix. Canonical REUSE/EXTEND/NEW classification.
- **Rule 2 accounting** — `/app/docs/rule2_accounting.json`. Velocity baseline; Sub-stage 1 LoC delta cited to this file.

## §2. First step — copy this build brief to disk

Before touching any code, write this entire message verbatim to `/app/docs/build_briefs/phase_8_seam_3_sub_stage_1.md`. Return its SHA-256 in your reply. Close report cites brief SHA. Standing Rule v3: brief is a canonical artifact, not just an in-flight instruction.

## §3. Rulings pre-carried into Sub-stage 1

| Ruling | Pre-carry in Sub-stage 1 |
|---|---|
| **E1.γ** (rulings record §3.1 + §8.1) | Registry `refusal_families.v0.json` at `/app/backend/services/compliance/refusal_families.v0.json` — v0 schema per admission-refusal-reasons precedent (verify structure of `admission_refusal_reasons.vN.json` and mirror the shape). Family value carried at pinned `stamp_audit["refusal_family"]` — NOT a loose Dict key, pinned by LB gate. `NorthenaLedgerRow_v1` byte-identical (parity 26 unchanged). Load-bearing gate `test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit` — parametrised over all 4 refusal-terminal emission sites at `services/compliance/refusal_family_classifier.py:42-49` PLUS aggregate re-verification regression. Retirement: never. |
| **E2** (rulings record §3.2 + §8.3) | NOT exercised at Sub-stage 1. `test_retention_endpoint_loosening_disabled_pre_checker` NOT touched this pass. |
| **E3.β + honest-cost** (rulings record §3.4 + §8.4; Stage A §7.3.β + §7.3.β.1) | Coverage-marker `{date}` = **query-time first-timestamp-per-family** derived from earliest `NorthenaLedgerRow_v1` timestamp where `stamp_audit["refusal_family"] == <family>`. Query filter: `{decision: "refused", "stamp_audit.refusal_family": <family>}` sorted timestamp ascending, first result. **NO** `refusal_family_since_dates.v0.json` config file. **NO** materialization file. **NO** pre-emptive index. **NO** pre-optimization of any kind. **Honest-cost flagging obligation:** if query cost manifests during Sub-stage 1 (measured, not speculated), you MUST flag it honestly in the close report with concrete evidence (query time, dataset shape, page render time). Owner rules on mechanism if cost is real. Do NOT route around correctness with a wrong-but-cheap substitute. |
| **E4** (rulings record §3.4) | `emit_refusal_ledger_row` colocates at `/app/backend/services/compliance/refusal_ledger.py`. `services/service_1/async_state.py:238::emit_ledger_terminate_refused` gets a migration docstring pointing at the new canonical location, but the function body is byte-identical (BC preserved). Do NOT extract shared helpers to `_helpers/` — one consumer exists, that is the extraction rule. |
| **E5 narrowed** (rulings record §3.3 + §8.2 + §8.5) | No new auth codes. Sub-stage 1 obligation: **no HTTP 409 introduced by this sub-stage** (diff-inspection + one-line confirmation in close report; no dedicated gate). Standing 409-for-governance-state anti-rule (§8.2) applies globally but full enforcement machinery is not required at Sub-stage 1 (activates at Sub-stage 2/3). |
| **E7** (rulings record §3.5) | All binding-copy strings in Sub-stage 1 render with middle-dots (`·`, U+00B7) per BCR v1.4.1 + UI Spec v2.1 §8/§10. Playwright chromium coverage-marker smoke MUST assert the middle-dot glyph specifically — not just surrounding words. Named gate: `test_coverage_marker_renders_middle_dot_glyph_verbatim` (per §8.6). |

## §4. Scope binding — READ from Stage A §5 verbatim

Sub-stage 1 deliverables come from Stage A proposal §5 (post-Amendment-E, SHA `3fe969c2…`). Read that section verbatim and execute as written. Do NOT flatten, expand, or infer scope. If §5 is silent on something Sub-stage 1 needs, STOP and escalate to me — do not fill gaps with inference.

Known deliverables from prior recon (verify against current §5, then execute):
- Refusal-family ledger wire-up at 4 un-ledgered emission sites at `services/compliance/refusal_family_classifier.py:42-49`.
- New `services/compliance/refusal_ledger.py` module with canonical `emit_refusal_ledger_row`.
- `async_state.py:238` migration-docstring-only edit (body preserved).
- Registry file `refusal_families.v0.json` at `services/compliance/`.
- Coverage-marker read behavior at `services/compliance/coverage_marker.py` (query-time β per §7.3.β.1 amended §4.1 line 173).
- Compliance Console refusals-card rider carrying the coverage-marker binding-copy string with middle-dots.
- First-commit gate per Stage A §5 exact name.

## §5. Test matrix (matrix-enumerated per Standing Correction — cells × postures × cases, no LoC lumps)

Enumerate in close report as a table:
- **Backend invariants (Pytest):** existing 66 files + Sub-stage 1 additions. Each new test cell = endpoint × posture × case. LB gate `test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit` parametrised over 4 emission sites + 1 aggregate regression cell = 5 parametrised cases minimum.
- **Jest:** existing suites + refusals-card rider additions covering coverage-marker text rendering, refusal-family enumeration, empty-state.
- **Playwright chromium:** existing 26 smokes + coverage-marker smoke `test_coverage_marker_renders_middle_dot_glyph_verbatim` (assert `·` glyph, not just surrounding words) + refusals-card render.
- Any additional named gates from Stage A §5 exact roster.

Report cell counts per posture (happy path / auth-denied / registry-invalid / query-empty / aggregate) per endpoint. Not "N tests added" — the matrix itself, enumerated.

## §6. First-commit gating

Backend + registry file + tests + frontend rider + Playwright smoke land in **ONE commit**. No "testing later" split, no "frontend follows backend" split. If the commit exceeds LoC ceiling per `rule2_accounting.json` cell-derived velocity, STOP and escalate for a Sub-stage 1 split proposal — do not silently break the ceiling.

## §7. Standing disciplines

- **Standing Rule v3:** close report at `/app/docs/close_reports/phase_8_seam_3_sub_stage_1.md`. Full text on disk. Reply to me contains only SHA + one-line summary + numeric metrics — no full-file paste, no inline code.
- **Standing Correction:** matrix-enumerated sizing in close report (endpoints × postures × cases). No LoC lumping.
- **Standing 409 anti-rule (§8.2):** applies globally; Sub-stage 1 obligation narrowed to "no 409 introduced by this sub-stage" — self-audit with one-line confirmation in close report.
- **Honest-cost obligation (§7.3.β.1):** if query-time β surfaces measurable cost, flag with evidence — do NOT pre-optimize.
- **Middle-dot strictness (§8.6):** every binding-copy string in Sub-stage 1 uses `·` (U+00B7), not `-` (U+002D). Playwright smoke asserts glyph.

## §8. Reply format

Return only:
- SHA-256 of this build brief on disk (`/app/docs/build_briefs/phase_8_seam_3_sub_stage_1.md`).
- SHA-256 of the close report (`/app/docs/close_reports/phase_8_seam_3_sub_stage_1.md`).
- SHA-256 of `refusal_families.v0.json` (v0 content).
- Test pass counts: pytest new + total (both must be all-green); jest new + total; playwright chromium new + total.
- Rule 2 accounting LoC delta (cite `rule2_accounting.json` velocity baseline).
- Candidate commit hash (Owner pushes; you do NOT `git push`).
- One-line summary of the matrix-enumerated test roster (full table lives in close report).
- Honest-cost report on query-time β: "no cost problem observed" OR concrete evidence with query time + dataset shape.
- 409 self-audit: "no HTTP 409 introduced" one-line confirmation.
- Any Sub-stage 2 preconditions surfaced during Sub-stage 1 build.

## §9. Hard constraints

- Sub-stage 1 only. Do NOT dispatch Sub-stage 2 or Sub-stage 3.
- 26 frozen contracts + snapshots **untouched**.
- No `git push`. Owner pushes.
- No pre-optimization on E3.β (no index, no materialization).
- No 409 codes anywhere in the Sub-stage 1 diff.
- Middle-dot rendering strict — Playwright asserts glyph.
- If Stage A §5 is silent on any needed detail, STOP and escalate.
- If LoC ceiling breached, STOP and escalate for split proposal.
- If contract-adjacency risk surfaces during build (anything touching the 26 frozen contracts or their snapshots), STOP and escalate.

Fire when ready.
