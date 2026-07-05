// Phase 8 Stage B-3 Block 3 — Engineer §4.2 First call smoke + §4.3 Administer smoke.
// Owner Condition 1: same-commit gating.
//
// Scope §4.2 verbatim:
//   * request block; two response panels (Answered / Refused);
//   * async 202 accepted body variant;
//   * Binding copy: "There is no response shape in which the claim is separable from its class..."
//
// Scope §4.3 verbatim:
//   * apps list + extract-path acquisitions section + lifecycle chips;
//   * Footer binding copy: "Key scope is enforced server-side on every call."
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';
const MOCK_IDENTITY = {
  user_id: 'e2e-engineer-2',
  email: 'engineer2@example.com',
  name: 'Engineer 4.2 E2E',
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
        status: 200, contentType: 'application/json',
        body: JSON.stringify({ grantee_email: MOCK_IDENTITY.email, grants: [] }),
      });
      return;
    }
    route.fallback();
  });
});

test('engineer_first_call_renders_ui_spec_4_2_verbatim_including_binding_copy', async ({ page }) => {
  await page.goto('/engineer/first-call');
  await expect(page.getByTestId('engineer-first-call-page')).toBeVisible({ timeout: 5000 });
  // §4.2 request block.
  await expect(page.getByTestId('first-call-request-block')).toBeVisible();
  await expect(page.getByTestId('first-call-request-block')).toContainText('POST /v1/objectives');
  // §4.2 two response panels side by side.
  await expect(page.getByTestId('first-call-response-panels')).toBeVisible();
  await expect(page.getByTestId('first-call-answered-panel')).toBeVisible();
  await expect(page.getByTestId('first-call-answered-panel')).toContainText('outcome');
  await expect(page.getByTestId('first-call-answered-panel')).toContainText('trace_id');
  await expect(page.getByTestId('first-call-answered-panel')).toContainText('defensibility');
  await expect(page.getByTestId('first-call-refused-panel')).toBeVisible();
  await expect(page.getByTestId('first-call-refused-panel')).toContainText('"outcome": "refused"');
  await expect(page.getByTestId('first-call-refused-panel')).toContainText('asked');
  await expect(page.getByTestId('first-call-refused-panel')).toContainText('supported_class');
  await expect(page.getByTestId('first-call-refused-panel')).toContainText('what_would_raise_it');
  // §4.2 async 202 variant.
  await expect(page.getByTestId('first-call-async-variant')).toBeVisible();
  await expect(page.getByTestId('first-call-async-variant')).toContainText('objective_id');
  await expect(page.getByTestId('first-call-async-variant')).toContainText('delivery_estimate');
  // §4.2 Binding copy VERBATIM — Owner Condition 3 mandate.
  await expect(page.getByTestId('first-call-binding-copy')).toContainText(
    'There is no response shape in which the claim is separable from its class'
  );
  await expect(page.getByTestId('first-call-binding-copy')).toContainText(
    'Infrastructure faults return 500 and are never rendered as refusals'
  );
});

test('engineer_administer_renders_ui_spec_4_3_verbatim_footer_binding_copy', async ({ page }) => {
  await page.goto('/engineer/administer');
  await expect(page.getByTestId('engineer-administer-page')).toBeVisible({ timeout: 5000 });
  // §4.3 apps list empty state.
  await expect(page.getByTestId('administer-apps-empty')).toBeVisible();
  // §4.3 lifecycle-state chips.
  for (const s of ['accepted', 'running', 'delivered', 'refused']) {
    await expect(page.getByTestId(`administer-lifecycle-${s}`)).toBeVisible();
  }
  // §4.3 extract-path note.
  await expect(page.getByTestId('administer-extract-path-note')).toBeVisible();
  // §4.3 Footer binding-copy VERBATIM.
  await expect(page.getByTestId('administer-footer-binding-copy')).toContainText(
    'Key scope is enforced server-side on every call.'
  );
});
