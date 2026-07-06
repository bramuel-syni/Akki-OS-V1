// Phase 8 Stage B-5a — Compliance Prove-one-run smoke (§4.2 verbatim).
//
// First-commit gating: §4.2 surface lands with this Playwright chromium
// smoke IN THE SAME COMMIT.
//
// Scope (§4.2 verbatim elements):
//   * lawfulness banner (lawful-basis · commissioner · frozen);
//   * five record rows (Lawful basis / Scope / Refused / Standard / Ledger);
//   * BINDING COPY visible verbatim;
//   * "Refused" row surfaces count and "See them" link when refused>0;
//   * Export affordance present;
//   * Not-found (404) renders HONESTLY (not via RefusalCard).
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';
const MOCK_IDENTITY = {
  user_id: 'e2e-dpo-1',
  email: 'dpo@rms.example.com',
  name: 'DPO E2E',
  roles: ['dpo', 'admin'],
  key_grants: [],
  created_at: '2026-07-06T00:00:00Z',
};

const MOCK_TRACE_ENVELOPE = {
  trace_id: 'e2e-trace-1',
  resolved_at: '2026-07-06T00:00:00Z',
  run_ids: ['e2e-run-1'],
  engines_touched: ['northena_ledger'],
  ledger_rows: [
    {
      run_id: 'e2e-run-1',
      trace_id: 'e2e-trace-1',
      stage: 'admit',
      decision: 'admitted',
      reason: 'admitted',
      artifact_ref: {
        artifact_type: 'objective_request',
        artifact_id: 'a1',
        version: 'v0',
      },
      lawful_basis_ref: 'lb-2026-07-e2e',
      at: '2026-07-06T00:00:00Z',
      stamp_audit: null,
    },
  ],
  registry_freshness: { freshness_marker: 'ok' },
};

const MOCK_RETENTION_UNSET = {
  global_default: { days: null, set_at: null, set_by: null },
  held_classes: [
    { class_name: 'ledger_row', posture: 'unset', days: null, set_at: null, set_by: null },
    { class_name: 'wizard_transcript', posture: 'unset', days: null, set_at: null, set_by: null },
    { class_name: 'delivered_artifact', posture: 'unset', days: null, set_at: null, set_by: null },
  ],
  resolved_at: '2026-07-06T00:00:00Z',
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
  }, { tok: MOCK_ACCESS_TOKEN });
  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  await page.route(/\/api\/compliance\/retention_config$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_RETENTION_UNSET) })
  );
  await page.route(/\/api\/northena\/trace\/e2e-trace-1$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_TRACE_ENVELOPE) })
  );
  await page.route(/\/api\/northena\/trace\/notfound-xyz$/, (route) =>
    route.fulfill({
      status: 404,
      contentType: 'application/json',
      body: JSON.stringify({ detail: { reason: 'trace_id_not_found', message: 'no ledger rows', trace_id: 'notfound-xyz' } }),
    })
  );
});

test('compliance_prove_run_renders_ui_spec_4_2_verbatim_elements', async ({ page }) => {
  await page.goto('/compliance/prove/e2e-trace-1');
  await expect(page.getByTestId('compliance-prove-run-page')).toBeVisible({ timeout: 5000 });
  // Lawfulness banner.
  await expect(page.getByTestId('compliance-prove-lawfulness-banner')).toBeVisible();
  await expect(page.getByTestId('compliance-prove-lawfulness-banner')).toContainText('lb-2026-07-e2e');
  await expect(page.getByTestId('compliance-prove-lawfulness-banner')).toContainText('frozen and immutable');
  // Five record rows — all verbatim strings.
  await expect(page.getByTestId('compliance-record-row-lawful-basis')).toContainText('verified present at admission');
  await expect(page.getByTestId('compliance-record-row-scope')).toContainText('nothing mined outside it');
  await expect(page.getByTestId('compliance-record-row-refused')).toContainText('below the required standard, recorded not dropped');
  await expect(page.getByTestId('compliance-record-row-standard')).toContainText('enforced on every unit, server-side');
  await expect(page.getByTestId('compliance-record-row-ledger')).toContainText('append-only; current retention state stated honestly');
  // Export affordance.
  await expect(page.getByTestId('compliance-prove-export-button')).toContainText('Export for a regulator on request');
  // BINDING COPY VERBATIM.
  await expect(page.getByTestId('compliance-prove-binding-copy')).toContainText(
    'Read-only. This is the record itself, not a summary of it. Export for a regulator on request.'
  );
});

test('compliance_prove_run_404_renders_honestly_not_via_refusal_card', async ({ page }) => {
  await page.goto('/compliance/prove/notfound-xyz');
  await expect(page.getByTestId('compliance-prove-run-page')).toBeVisible({ timeout: 5000 });
  // Not-found panel is present.
  await expect(page.getByTestId('compliance-prove-not-found')).toBeVisible();
  // Refusal card is NOT used for this — E2 taxonomy separation.
  await expect(page.locator('[data-testid*="refusal-card"]')).toHaveCount(0);
});
