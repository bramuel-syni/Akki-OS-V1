// Phase 8 Stage B-4 Block 1 — §6.2 Change-a-rule smoke.
//
// Scope (§6.2 verbatim):
//   * "The rule" one-sentence descriptor.
//   * current-behaviour paragraph.
//   * plain Off / On options.
//   * "What changes" info box.
//   * commit button in natural language.
//   * Binding copy VERBATIM after commit — "Recorded as your change,
//     with today's date."
//   * Path A: tier_lock → 200 commit path.
//   * Path B: model_version → 501 with honest 501 language rendered.
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';
const MOCK_IDENTITY = {
  user_id: 'e2e-master-admin-change-1',
  email: 'admin@rms.example.com',
  name: 'MA change E2E',
  roles: ['admin', 'master_admin'],
  key_grants: [],
  created_at: '2026-07-05T00:00:00Z',
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
  }, { tok: MOCK_ACCESS_TOKEN });
  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  await page.route(/\/api\/pricing\/tier_lock$/, (route) => {
    if (route.request().method() === 'POST') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          locked: true,
          reason_note: 'e2e reason',
          trace_id: 'trace-e2e',
          ledger_run_id: 'run-e2e',
          versioned_file_path: 'services/economics/tier_lock.vN.json',
          at: new Date().toISOString(),
        }),
      });
      return;
    }
    route.fallback();
  });
});

test('change_a_rule_renders_ui_spec_6_2_verbatim_elements_and_commit_succeeds', async ({ page }) => {
  await page.goto('/master-admin/change-a-rule/tier-lock');
  await expect(page.getByTestId('master-admin-change-a-rule-page')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('change-rule-one-sentence')).toBeVisible();
  await expect(page.getByTestId('change-rule-current-behaviour')).toBeVisible();
  // Plain Off / On options.
  await expect(page.getByTestId('change-rule-option-off')).toBeVisible();
  await expect(page.getByTestId('change-rule-option-on')).toBeVisible();
  // Select "On" and commit.
  await page.getByTestId('change-rule-option-on').click();
  // "What changes" info box.
  await expect(page.getByTestId('change-rule-what-changes')).toBeVisible();
  // Commit button in natural language.
  await expect(page.getByTestId('change-rule-commit-button')).toBeVisible();
  await page.getByTestId('change-rule-commit-button').click();
  // Binding copy VERBATIM after commit.
  await expect(page.getByTestId('change-rule-recorded-binding-copy')).toContainText(
    "Recorded as your change, with today's date."
  );
});

test('change_a_rule_path_b_model_version_renders_honest_501_plain_language', async ({ page }) => {
  await page.goto('/master-admin/change-a-rule/model-version');
  await expect(page.getByTestId('master-admin-change-a-rule-page')).toBeVisible({ timeout: 5000 });
  // Path B rule — commit surface absent (no On/Off).
  await expect(page.getByTestId('change-rule-option-off')).toHaveCount(0);
  await expect(page.getByTestId('change-rule-option-on')).toHaveCount(0);
  // What-changes info box renders plain-language "requires versioned file" copy.
  await expect(page.getByTestId('change-rule-what-changes')).toContainText('versioned file update on the server');
  await expect(page.getByTestId('change-rule-what-changes')).toContainText('Contact Owner');
  await expect(page.getByTestId('change-rule-what-changes')).toContainText('No change applied');
});

test('change_a_rule_other_rules_sub_list_present', async ({ page }) => {
  await page.goto('/master-admin/change-a-rule/tier-lock');
  await expect(page.getByTestId('change-rule-other-rules')).toBeVisible();
  // Two Path B rules should be listed as "Other rules".
  await expect(page.getByTestId('change-rule-other-model-version')).toBeVisible();
  await expect(page.getByTestId('change-rule-other-fleet-policy')).toBeVisible();
});
