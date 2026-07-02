# Iteration 1 — G5b Frontend Operator Console + Consumer Terminal v0

## What was implemented

### Pages (6 total)
1. **LandingPage** (`/`) — Hero with shield icon, tagline, Operator Console + Consumer Terminal cards, health status
2. **OperatorDashboard** (`/operator`) — Portfolio overview: system state, data source posture, V-gates, frozen contracts, exception banner
3. **RunsPage** (`/operator/runs`) — Northena open runs list, filter input, refresh button, Northena status info
4. **RunDetailPage** (`/operator/runs/:runId`) — Per-run ledger table, trace links, governing artifact metadata
5. **DisciplinePage** (`/operator/discipline`) — Lift manifest metadata, spec fingerprints, Rule 2 v2 accounting table, lift entries
6. **EnginesPage** (`/operator/engines`) — 5-engine status cards: Northena, Solva, Service 1, V1 Harness, V3 Harness
7. **TraceReceiptPage** (`/trace/:traceId`) — Consumer Terminal v0: envelope summary, ledger rows, Solva traces, mining plans, registry records, trace search

### Components (6 total)
- AppShell — sidebar + header layout with persistent nav
- StatusBadge — colored status indicator (ok/pending/refused/admitted/synthetic/live)
- ClassBadge — defensibility class badge (fact/utterance/non_factual)
- LedgerTable — ledger row table with trace links
- RefusalCard — first-class refusal rendering with reasoning
- EngineCard — per-engine status card with metadata

### API Client
- Uses REACT_APP_BACKEND_URL + /api prefix
- 14 endpoints mapped: health, systemState, northenaStatus, openRuns, ledgerByRun, traceLens, v1Status, v3Status, solvaStatus, service1Status, liftManifest, stampAuditRecent, contractFiveRings, contractQualMatrix
- useApi hook with loading/error/data/refetch pattern

## Design decisions
- Exception-first surface: amber banner shows when synthetic data or pending V-gates
- Sidebar navigation: 5 items (Home, Portfolio, Runs, Discipline, Engines)
- Trace search allows Consumer Terminal v0 access via /trace/:traceId
- Collapsible sections in trace receipt for progressive disclosure
- Governance class badge always shown with any unit (as per spec: "class inseparable on surface")

## Dependencies installed
- lucide-react (icons)

## Known issues
- Tailwind CSS PostCSS integration via craco doesn't process @tailwind directives; worked around by pre-compiling CSS
- If new Tailwind utility classes are needed, must re-run: `cd /app/frontend && npx tailwindcss -i src/index.css -o src/tailwind-compiled.css --minify`
