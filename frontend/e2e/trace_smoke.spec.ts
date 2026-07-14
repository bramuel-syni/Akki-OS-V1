// G-10/G-7 PROMOTE smoke — Owner ruling docs/rulings/g10_g7_promote_2026-07-14.md
//
// Verifies the public /trace and /trace/:traceId surface (Owner ruling
// 2026-07-14): TraceReceiptPage lifted out of /legacy/*, mounted at the
// top of the routes tree. Hermetic: /api/northena/trace/:id is intercepted
// so the smoke tests the surface wiring (route → useApi hook →
// three-lens render), not backend dispatch semantics (covered by pytest).
//
// Scope: chromium-only (Owner E7 ratified at B-1); ~50 LoC.

const { test, expect } = require('@playwright/test');

const TRACE_ID = 'trace-g10g7-promote-smoke-xyz789';

const MOCK_ENVELOPE = {
  resolved_at: '2026-07-14T00:00:00Z',
  run_ids: ['run-alpha-1'],
  engines_touched: ['solva', 'targeta', 'northena'],
  registry_freshness: { snapshot_pinned: true },
  ledger_rows: [
    {
      stage: 'admit',
      decision: 'admitted',
      reason: 'promote_smoke',
      defensibility_class: 'utterance',
      trace_id: TRACE_ID,
      artifact_ref: null,
      at: '2026-07-14T00:00:00Z',
    },
  ],
  solva_traces: [
    {
      unit_id: 'u-alpha-1',
      computed_class: 'utterance',
      decision: 'admitted',
      conclusion: 'promote smoke conclusion',
      stages: [{ stage_name: 'admit' }, { stage_name: 'compose' }],
      load_bearing_unit_ids: ['u-alpha-1'],
    },
  ],
  mining_plans: [],
  registry_records: [],
};

test.beforeEach(async ({ page }) => {
  await page.route(/\/api\/northena\/trace\/[^/?#]+$/, (route) =>
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(MOCK_ENVELOPE),
    }),
  );
});

test('trace_receipt_page_renders_three_lens_at_promoted_public_route', async ({ page }) => {
  await page.goto(`/trace/${TRACE_ID}`);
  // Page container renders.
  await expect(page.getByTestId('trace-receipt-page')).toBeVisible();
  // Summary section (envelope resolved_at / run_ids / engines_touched).
  await expect(page.getByTestId('trace-summary')).toBeVisible();
  // Lens 1: ledger (default open).
  await expect(page.getByTestId('trace-ledger-section')).toBeVisible();
  // Lens 2: Solva reasoning traces.
  await expect(page.getByTestId('trace-solva-section')).toBeVisible();
  // Back-link points to Ask Console at "/" (single-ingress doctrine).
  await expect(page.getByTestId('back-from-trace')).toHaveAttribute('href', '/');
});

test('trace_search_form_renders_at_naked_trace_route', async ({ page }) => {
  await page.goto('/trace');
  await expect(page.getByTestId('trace-receipt-search')).toBeVisible();
  await expect(page.getByTestId('trace-search-input')).toBeVisible();
  await expect(page.getByTestId('trace-search-btn')).toBeVisible();
});
