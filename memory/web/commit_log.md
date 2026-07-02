# Web Frontend Commit Log

## Iteration 1 — G5b Initial Build
- **Commit**: e8208b38384a6e18f188b4c983c86369a30de564
- **Date**: 2026-07-02T09:45Z
- **Changes**:
  - Complete frontend build: 7 pages, 6 components, 1 hook, 1 API client
  - Landing, Portfolio, Runs, Run Detail, Discipline, Engines, Trace Receipt pages
  - AppShell, StatusBadge, ClassBadge, LedgerTable, RefusalCard, EngineCard components
  - Tailwind CSS pre-compiled workaround for craco PostCSS pipeline issue
- **Files modified**: All frontend/src/ files (initial creation)

## Iteration 2 — G5b Acceptance Gate Completion
- **Commit**: 7ec95207c4b76ea07e13721dff626b7260cdb9cc
- **Date**: 2026-07-02T10:00Z
- **Changes**:
  - ComposePage: objective submission with client-side non-empty validation + Service1RunSummary/Refusal rendering
  - OuterGateReceiptInline: safe-field-only rendering (5-field allowlist per Interface Spec §21.2)
  - TrustReceiptLink: trust-receipt URL per Interface Spec §16.5
  - LedgerTable: added ClassBadge for defensibility class co-rendering (Gate 1 fix)
  - AppShell: added Compose nav item
  - 3 gate invariant tests (12/12 passing): class-inseparable, refusal-first-class, single-ingress
  - Tailwind CSS pipeline fix: concurrently runs tailwindcss --watch alongside craco start
  - Scope note, conformance audit, BUILD_JOURNAL, ORCHESTRATOR_CONTINUITY, PHASE_STATE updated
- **Files modified**:
  - frontend/src/pages/ComposePage.js (new)
  - frontend/src/components/OuterGateReceiptInline.js (new)
  - frontend/src/components/TrustReceiptLink.js (new)
  - frontend/src/components/LedgerTable.js (ClassBadge added)
  - frontend/src/components/AppShell.js (Compose nav)
  - frontend/src/App.js (Compose route)
  - frontend/src/__tests__/gate{1,2,3}_*.test.js (new)
  - frontend/package.json (concurrently + tailwind scripts)
  - docs/g5b_prep/g5b_scope_from_source.md (new)
  - docs/audits/g5b_conformance_v1.md (new)
  - docs/lift_manifest.json (7 G5b entries)
