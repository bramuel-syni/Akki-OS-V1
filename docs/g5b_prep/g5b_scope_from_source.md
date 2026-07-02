# G5b Scope from Source — Pre-Build Formalisation

**Phase**: G5b — Frontend Operator Console + Consumer Terminal v0
**Date**: 2026-07-02
**Status**: FORMALISED POST-BUILD (build conceptually complete; this document back-fills the required source-anchored scope note)

---

## 1. Operator Console — 4 Surfaces

Per UX Architecture Spec §7 ("The Operator Surface"):

> "The operator carries the highest cognitive load in the system — volume, customer-sensitivity tiers, governance thresholds, infrastructure health — and the promise is confidence without vigilance. The surface is therefore exception-first, not dashboard-first."

The four operator exception dimensions (UX Arch §7, table) define the four surfaces:

| # | Surface name | UX Arch §7 dimension | Interface Spec §13 anchor | What it foregrounds |
|---|---|---|---|---|
| 1 | **Portfolio** | Governance | §13 "a floor is refused at rate, a class distribution shifts, or a gate result changes" | System state, V-gates, frozen contracts, data-source posture |
| 2 | **Runs** | Throughput / volume | §13 "a queue, rate, or backlog crosses a health threshold" | Northena open runs, per-run ledger, trace links |
| 3 | **Discipline** | Governance (lift-manifest / Rule 2 accounting) | §13 "a gate result changes" + UX Arch §16.10 "every control-surface action is versioned, diffed" (operator reads the diff) | Lift manifest, spec fingerprints, Rule 2 v2 accounting |
| 4 | **Engines** | Infrastructure | §13 "compute, substrate, or a perception model degrades against budget" | Per-engine status (Northena, Solva, Service 1, V1, V3) |

**Information architecture per §13:** "It opens calm — a single legible statement that the system is healthy — and surfaces an exception only when a dimension crosses its threshold."

Operator surfaces implement this via:
- Exception banners (amber, surfaced only when thresholds crossed — e.g. synthetic data, V-gate pending)
- Calm default state (no always-on dashboards per §7 mandate: "A wall of always-on dashboards would defeat the promise")
- Depth-on-reach (collapsible sections, click-through to run detail / trace)

## 2. Consumer Terminal v0

Per UX Architecture Spec §9–§12 ("The Three Trace Lenses"):

> "The trace lens is the experience primitive that makes trust progressive. One piece of intelligence can be inspected at three depths — the unit, the reasoning, the record — and the lenses are not three tabs a user chooses between; they are depth a user pulls toward."

**Consumer Terminal v0 shape** (per §12 "The Audit Lens and trace_id"):
- URL: `/trace/{trace_id}`
- Resolves a single `trace_id` to the full `TraceLensEnvelope` via `GET /api/northena/trace/{trace_id}`
- Progressive disclosure: envelope summary (shallow) → ledger rows → Solva traces (reasoning lens) → mining plans → registry records (deep)
- One thread throughout: §12 "A single trace_id joins the unit to its reasoning to its audit record"

**Scope boundary:** v0 is read-only trace resolution. It does not compose objectives or trigger runs — that is the Decisions Console (§6), not the Consumer Terminal.

## 3. Trust-Receipt Render Pattern

Per Interface Spec §16.5 ("One thread throughout"):

> "A single trace_id joins an answer to its reasoning, its record, and its API response. Every 'go deeper' action follows that thread."

Per Interface Spec §7 ("Rendering the Three Lenses"):

> "The three trace lenses render as one progressive view, not three tabs. The unit lens is the default; the reasoning and audit lenses are reached in place, deepening the same answer."

**Implementation anchor**: Every intelligence response component renders a trust-receipt link that resolves to `/trace/{trace_id}`, following the thread. The link appears in:
- `LedgerTable` (each row's trace_id links to `/trace/{trace_id}`)
- `RunDetailPage` (trace receipt links at top)
- `TraceReceiptPage` (the resolution endpoint itself)
- `Service1ResponseView` (trust-receipt link on successful run summary)

## 4. Outer-Gate Receipt Render

Per Interface Spec §12 ("The Data-Buying Path") + UX Architecture Spec §15 ("The Two Perimeters"):

The outer-gate receipt (`OuterGateReceipt@v0`) is rendered inline in the Consumer Terminal when the trace envelope contains an outer-gate stamp_audit entry. Only safe fields are surfaced:
- `transform_version`
- `mint_window_id`
- `key_fingerprint`
- `applied_transformations`
- `input_identifier_categories`

**NOT surfaced (per security posture):** mint key material, pre-image, raw identifiers.

**Scope boundary:** G5b renders the receipt read-only. G5b does NOT extend the backend contract — if the trace envelope's `stamp_audit` field contains an outer-gate receipt, we render it; if absent, we don't. No new backend routes.

## 5. Backend Contract Changes Implied by UX Spec

**None.** G5b is a pure consumer of existing backend contracts. Every §-anchor in the UX Spec that implies data shape is already satisfied by the 20 registered `/api/*` routes at G6+A2 close. Specifically:
- §7 operator exception dimensions → `GET /api/system/state` (V-gates, data source) + `GET /api/northena/ledger/open_runs` (throughput) + `GET /api/discipline/lift_manifest` (governance) + engine status endpoints (infrastructure)
- §9–§12 trace lenses → `GET /api/northena/trace/{trace_id}` (TraceLensEnvelope)
- §14 refusal → `POST /api/service_1/run` 422 body (Service1Refusal@v0)

**No contract extension required. No HAZARD-STOP (a) raised.**
