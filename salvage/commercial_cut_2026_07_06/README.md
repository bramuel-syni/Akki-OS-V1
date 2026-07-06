# Commercial-cut salvage — README

**Owner ruling (BCR v1.4 §12, 2026-07-06):** the commercial half of the RMS build is cut from the extractor tree per subtractive-change-with-mandatory-preservation posture. Every artifact removed from the extractor tree is preserved verbatim under this folder for possible future restoration (a second-repo action or a doctrinal roll-back).

## What this is

A verbatim salvage of:
1. The Phase 7 B-2 **buyer wizard variant** (state machine + router + Sonnet driver + Playwright/Jest surface tests).
2. The Phase 6 **commercial-half wizard helpers** (dual-delta summariser + buyer-proposals composer).
3. The **Commercial Reference Application UI** (buyer §5.1 Shape / §5.2 Acquire / §5.3 Receive pages + §5.2 binding-copy Jest tests + §5 Playwright smoke).
4. Pre-cut source snapshots of every surgical-split file (for lineage + diff).

## What this is not

- Not a live tree. No `pytest`, `jest`, or `playwright` runners collect anything under this folder.
- Not a disable-flagged codepath. Post-cut the extractor tree has zero references to any file in this folder.
- Not doctrinal supersession. `QuoteEnvelope_v0` + `WizardCommitState_v0.variant: Literal["operator","buyer"]` remain frozen at parity 26 byte-identical under `/app/backend/contracts/`; those contracts stayed in-tree per §12.3 orphan-in-place.

## When it was salvaged

2026-07-06 — Owner Step-2 dispatch (post B-4 acceptance + push confirmation). See `/app/docs/close_reports/commercial_cut_2026_07_06.md` for the close SHA + full disposition.

## Contents

- `MANIFEST.md` — every artifact enumerated with pre-cut path × pre-cut SHA × post-move path × post-move SHA × kind.
- `backend/wizard/` — buyer wizard state machine, router, dual-delta evaluator, extracted `SonnetWizardAgent`, extracted buyer helpers, and pre-cut surgical-split source snapshots.
- `backend/tests/` — buyer session-binding tests + pre-cut source snapshots of the split B-2/B-3 test files.
- `frontend/pages/` — buyer §5 React pages.
- `frontend/e2e/` — buyer §5 Playwright chromium smoke.
- `frontend/__tests__/` — pre-cut §5.2 binding-copy Jest test snapshot.

## Reversibility

Every whole-file move preserved SHA-identity (pre-cut SHA == post-move SHA at cut execution). Restoration is mechanical `mv` for whole-file cuts and appropriate module-level re-appending for surgical extractions. See MANIFEST.md "Reversibility posture" section.
