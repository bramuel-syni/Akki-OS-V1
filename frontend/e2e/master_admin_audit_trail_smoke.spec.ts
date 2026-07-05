// Phase 8 Stage B-4 Block 1 — §6.3 What-I've-changed audit trail smoke.
//
// Scope (§6.3 verbatim elements):
//   * confirmation line for the latest change (plain: what is now in
//     effect, from when).
//   * recent actions rows — plain description of the change, who, when.
//   * footer binding copy VERBATIM.
//   * Rule VERBATIM: "the diff exists in the record; it is never the
//     primary display" — verified by "See full diff" affordance being
//     collapsed by default and expanding on demand.
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';
const MOCK_IDENTITY = {
  user_id: 'e2e-master-admin-audit-1',
  email: 'admin@rms.example.com',
  name: 'MA audit E2E',
  roles: ['admin', 'master_admin'],
  key_grants: [],
  created_at: '2026-07-05T00:00:00Z',
};

const MOCK_AUDIT_TRAIL = {
  count: 2,
  actions: [
    {
      run_id: 'run-recent',
      trace_id: 'trace-r',
      at: '2026-07-05T14:00:00Z',
      rule_id: 'tier_lock',
      grantor_id: 'admin-uid',
      plain_description: 'Pricing tier lock turned on (was off).',
      full_diff_ref: '/api/northena/ledger/by_run/run-recent',
    },
    {
      run_id: 'run-older',
      trace_id: 'trace-o',
      at: '2026-07-04T14:00:00Z',
      rule_id: 'tier_lock',
      grantor_id: 'admin-uid',
      plain_description: 'Pricing tier lock turned off (was on).',
      full_diff_ref: '/api/northena/ledger/by_run/run-older',
    },
  ],
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
  }, { tok: MOCK_ACCESS_TOKEN });
  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  await page.route(/\/api\/master_admin\/audit_trail/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_AUDIT_TRAIL) })
  );
  await page.route(/\/api\/northena\/ledger\/by_run\/run-recent$/, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify([{
        run_id: 'run-recent', trace_id: 'trace-r',
        stamp_audit: { data_class: 'master_admin_rule_change', rule_change: { rule_id: 'tier_lock' } },
      }]),
    })
  );
});

test('audit_trail_renders_ui_spec_6_3_verbatim_elements', async ({ page }) => {
  await page.goto('/master-admin/audit-trail');
  await expect(page.getByTestId('master-admin-audit-trail-page')).toBeVisible({ timeout: 5000 });
  // §6.3 confirmation line for the latest change.
  await expect(page.getByTestId('audit-trail-confirmation-line')).toBeVisible();
  await expect(page.getByTestId('audit-trail-confirmation-line')).toContainText(
    'Pricing tier lock turned on (was off).'
  );
  // §6.3 recent actions rows.
  await expect(page.getByTestId('audit-trail-recent-actions')).toBeVisible();
  await expect(page.getByTestId('audit-row-run-recent')).toBeVisible();
  await expect(page.getByTestId('audit-row-run-older')).toBeVisible();
  await expect(page.getByTestId('audit-row-plain-run-recent')).toContainText(
    'Pricing tier lock turned on (was off).'
  );
  await expect(page.getByTestId('audit-row-who-run-recent')).toContainText('by admin-uid');
  // §6.3 footer binding copy VERBATIM.
  await expect(page.getByTestId('audit-trail-footer-binding-copy')).toContainText(
    'Every row carries its full diff. This trail is itself append-only and readable by the regulator surface.'
  );
});

test('audit_trail_see_full_diff_is_collapsed_by_default_and_expands_on_click', async ({ page }) => {
  await page.goto('/master-admin/audit-trail');
  await expect(page.getByTestId('master-admin-audit-trail-page')).toBeVisible({ timeout: 5000 });
  // Diff body absent on load — Rule: "never the primary display".
  await expect(page.getByTestId('audit-row-diff-body-run-recent')).toHaveCount(0);
  // Click "See full diff" — diff appears.
  await page.getByTestId('audit-row-see-full-diff-run-recent').click();
  await expect(page.getByTestId('audit-row-diff-body-run-recent')).toBeVisible();
  // Click "Hide full diff" — diff collapses again.
  await page.getByTestId('audit-row-see-full-diff-run-recent').click();
  await expect(page.getByTestId('audit-row-diff-body-run-recent')).toHaveCount(0);
});
