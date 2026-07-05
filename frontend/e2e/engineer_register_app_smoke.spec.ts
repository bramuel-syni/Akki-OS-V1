// Phase 8 Stage B-3 Block 3 — Engineer §4.1 Register app smoke.
// Owner Condition 1 verbatim: "surfaces do not land ungated" —
// this spec lands IN THE SAME COMMIT as EngineerRegisterAppPage.
//
// Scope (§4.1 verbatim):
//   * app name; class choice Internal/External; path choice with one-line grants;
//   * key grants panel plain-terms; Issue key button;
//   * async additions: webhook URL + sandbox toggle.
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';
const MOCK_IDENTITY = {
  user_id: 'e2e-engineer-1',
  email: 'engineer@example.com',
  name: 'Engineer E2E',
  roles: ['engineer'],
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
  await page.route(/\/api\/engineer\/key_grants$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ grantee_email: 'engineer@example.com', grants: [] }),
      });
      return;
    }
    // POST — mint returns a grant.
    const body = JSON.parse(route.request().postData() || '{}');
    route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({
        grant_id: 'gid-e2e-eng-001',
        grantee_email: MOCK_IDENTITY.email,
        grantor_id: MOCK_IDENTITY.user_id,
        key_class: body.key_class,
        path: body.path,
        floor: body.floor,
        scope: body.scope,
        justification: body.justification,
        lawful_basis_ref: body.lawful_basis_ref,
        issued_at: '2026-07-05T00:00:01Z',
        revoked_at: null,
        revocation_reason: null,
      }),
    });
  });
});

test('engineer_register_app_renders_ui_spec_4_1_verbatim_elements', async ({ page }) => {
  await page.goto('/engineer/register');
  await expect(page.getByTestId('engineer-register-app-page')).toBeVisible({ timeout: 5000 });
  // §4.1 app name input.
  await expect(page.getByTestId('engineer-app-name')).toBeVisible();
  // §4.1 class choice Internal/External.
  await expect(page.getByTestId('engineer-class-internal')).toBeVisible();
  await expect(page.getByTestId('engineer-class-external')).toBeVisible();
  // §4.1 path choice + one-line grants copy.
  await expect(page.getByTestId('engineer-path-live_query')).toBeVisible();
  await expect(page.getByTestId('engineer-path-governed_extract')).toBeVisible();
  await expect(page.getByTestId('engineer-path-copy-live_query')).toContainText(
    'Live query — inner gate · per-call governance · answers in responses'
  );
  await expect(page.getByTestId('engineer-path-copy-governed_extract')).toContainText(
    'Governed extract — outer gate · rights-checked · datasets and skills out'
  );
  // §4.1 floor + scope inputs.
  await expect(page.getByTestId('engineer-floor')).toBeVisible();
  await expect(page.getByTestId('engineer-scope')).toBeVisible();
  // §4.1 Async additions verbatim.
  await expect(page.getByTestId('engineer-webhook-url')).toBeVisible();
  await expect(page.getByTestId('engineer-webhook-note')).toContainText(
    'receives event + status only — never content'
  );
  await expect(page.getByTestId('engineer-sandbox-toggle')).toBeVisible();
  // §4.1 Issue key button.
  await expect(page.getByTestId('engineer-issue-key-btn')).toBeVisible();
});

test('engineer_register_app_issue_key_shows_grants_panel_plain_terms', async ({ page }) => {
  await page.goto('/engineer/register');
  await expect(page.getByTestId('engineer-register-app-page')).toBeVisible();
  await page.getByTestId('engineer-app-name').fill('test-app');
  await page.getByTestId('engineer-justification').fill('End-to-end integration test.');
  await page.getByTestId('engineer-issue-key-btn').click();
  // §4.1 grants panel present with plain-terms sentence.
  await expect(page.getByTestId('key-grants-panel')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('grants-panel-plain-terms')).toContainText('enforced server-side on every call');
});
