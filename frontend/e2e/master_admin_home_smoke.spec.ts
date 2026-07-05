// Phase 8 Stage B-4 Block 1 — Master Admin Home smoke (§6.1 verbatim).
//
// Owner Condition 1 (standing operational pattern): surfaces do not
// land ungated with smokes deferred a sub-stage. §6.1 surface lands
// WITH this Playwright chromium smoke IN THE SAME COMMIT.
//
// Scope (§6.1 verbatim elements):
//   * pending banner (plain-language, count-substituted) + Review button;
//   * prompt "What do you want to do?";
//   * six action buttons with binding labels VERBATIM;
//   * footer link VERBATIM "See everything I've changed — every action is recorded.";
//   * NEGATIVE: no dashboards / no version strings / no config syntax.
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';
const MOCK_IDENTITY = {
  user_id: 'e2e-master-admin-1',
  email: 'admin@rms.example.com',
  name: 'Master Admin E2E',
  roles: ['admin', 'master_admin'],
  key_grants: [],
  created_at: '2026-07-05T00:00:00Z',
};

const MOCK_PENDING_SEAMS = {
  count: 5,
  pending_seams: [
    { seam_id: 'targeta_yield_thresholds', plain_language_line: 'Targeta yield thresholds — awaiting Owner values', awaiting_whom: 'owner', seam_status: 'closed' },
    { seam_id: 'mtafiti_v3_thresholds', plain_language_line: 'Mtafiti V3 thresholds — awaiting Owner values', awaiting_whom: 'owner', seam_status: 'closed' },
    { seam_id: 'northena_retention_window', plain_language_line: 'Northena ledger retention window — awaiting DPO decision', awaiting_whom: 'dpo', seam_status: 'closed' },
    { seam_id: 'v2_cumulative_disclosure_envs', plain_language_line: 'V2 cumulative-disclosure thresholds', awaiting_whom: 'dpo', seam_status: 'closed' },
    { seam_id: 'mea_source_standing_table', plain_language_line: 'MEA source-standing table', awaiting_whom: 'mea', seam_status: 'closed' },
  ],
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
  }, { tok: MOCK_ACCESS_TOKEN });
  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  await page.route(/\/api\/master_admin\/pending_seams$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_PENDING_SEAMS) })
  );
});

test('master_admin_home_renders_ui_spec_6_1_verbatim_elements', async ({ page }) => {
  await page.goto('/master-admin');
  await expect(page.getByTestId('master-admin-home-page')).toBeVisible({ timeout: 5000 });
  // §6.1 pending banner (plural-aware, count-substituted).
  await expect(page.getByTestId('master-admin-pending-banner')).toBeVisible();
  await expect(page.getByTestId('master-admin-pending-copy')).toContainText(
    'Five rules are waiting on your decision before they can take effect.'
  );
  await expect(page.getByTestId('master-admin-pending-review')).toBeVisible();
  await expect(page.getByTestId('master-admin-pending-review')).toContainText('Review');
  // §6.1 prompt VERBATIM.
  await expect(page.getByTestId('master-admin-prompt')).toContainText('What do you want to do?');
  // §6.1 six action buttons with binding labels VERBATIM.
  await expect(page.getByTestId('master-admin-action-assign-a-role')).toContainText('Assign a role');
  await expect(page.getByTestId('master-admin-action-change-a-rule')).toContainText('Change a rule');
  await expect(page.getByTestId('master-admin-action-manage-keys-and-access')).toContainText('Manage keys & access');
  await expect(page.getByTestId('master-admin-action-update-the-taxonomy')).toContainText('Update the taxonomy');
  await expect(page.getByTestId('master-admin-action-set-pricing')).toContainText('Set pricing');
  await expect(page.getByTestId('master-admin-action-apportion-gpu-capacity')).toContainText('Apportion GPU capacity');
  // §6.1 footer link VERBATIM.
  await expect(page.getByTestId('master-admin-audit-footer-link')).toContainText(
    "See everything I've changed — every action is recorded."
  );
});

test('master_admin_home_rules_verbatim_no_dashboards_no_version_strings_no_config_syntax', async ({ page }) => {
  await page.goto('/master-admin');
  await expect(page.getByTestId('master-admin-home-page')).toBeVisible({ timeout: 5000 });
  // NEGATIVE: no chart/graph testids.
  await expect(page.locator('[data-testid*="chart"]')).toHaveCount(0);
  await expect(page.locator('[data-testid*="graph"]')).toHaveCount(0);
  await expect(page.locator('[data-testid*="plot"]')).toHaveCount(0);
  // NEGATIVE: no version strings visible (v0/vN.json/semantic versioning).
  const bodyText = await page.locator('main').textContent();
  expect(bodyText).not.toMatch(/\bv\d+\.json\b/);
  expect(bodyText).not.toMatch(/\b@v0-exploratory\b/);
  // NEGATIVE: no JSON blobs visible on the surface (curly-brace-key-colon).
  expect(bodyText).not.toMatch(/\{\s*"[a-z_]+":/);
});

test('master_admin_home_review_button_navigates_to_change_a_rule_page', async ({ page }) => {
  await page.goto('/master-admin');
  await expect(page.getByTestId('master-admin-home-page')).toBeVisible({ timeout: 5000 });
  await page.getByTestId('master-admin-pending-review').click();
  await expect(page).toHaveURL(/\/master-admin\/change-a-rule\/tier-lock$/);
});
