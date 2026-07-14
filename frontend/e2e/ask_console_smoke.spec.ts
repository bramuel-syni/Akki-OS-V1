// Phase 8 Stage B-1 — Ask Console smoke test (Owner E7 chromium-only).
//
// Scope (per Stage A §3.2, refined at Owner dispatch to ~40 LoC):
//   authenticated login → submit Ask → assert render → click Trust receipt →
//   assert navigation to `/trace/{traceId}` (promoted public route at
//   Owner ruling G-10/G-7 PROMOTE, 2026-07-14).
//
// This smoke intercepts the network to keep the test hermetic; the surface
// wiring (Auth + AskConsole + apiClient) is the target under test, not the
// backend dispatch semantics (which are covered by 740 backend gates).

const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN =
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE'; // placeholder — the surface only reads it

const MOCK_IDENTITY = {
  user_id: 'e2e-user-1',
  email: 'e2e@example.com',
  name: 'E2E User',
  roles: ['ask_console_user'],
  key_grants: [],
  created_at: '2026-07-05T00:00:00Z',
};

const MOCK_COMPOSED_CONCLUSION = {
  outcome: 'answered',
  conclusion_class: 'recorded_statement',
  answer_text: 'The composed conclusion for the E2E smoke test.',
  load_bearing_unit_ids: ['u-1', 'u-2', 'u-3'],
  trace_id: 'trace-e2e-b1-smoke-abc123',
};

test.beforeEach(async ({ page, context }) => {
  // Seed authenticated session state.
  await context.addInitScript(({ tok, identity }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
    window.localStorage.setItem('rms.b1.auth.refresh_token', 'refresh-e2e-mock');
  }, { tok: MOCK_ACCESS_TOKEN, identity: MOCK_IDENTITY });

  // Intercept /api/auth/me — return the mock identity.
  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );

  // Intercept /api/service_1/v2/dispatch — return the mock composed conclusion.
  await page.route(/\/api\/service_1\/v2\/dispatch$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_COMPOSED_CONCLUSION) })
  );
});

test('ask_console_smoke_authenticated_flow_end_to_end', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByTestId('ask-console-page')).toBeVisible();
  await expect(page.getByTestId('ask-input')).toBeVisible();
  await page.getByTestId('ask-input').fill('What is the answer to the E2E smoke test?');
  await page.getByTestId('ask-submit').click();
  await expect(page.getByTestId('answer-view')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('answer-headline')).toContainText('composed conclusion for the E2E');
  await expect(page.getByTestId('answer-trust-receipt')).toHaveAttribute(
    'href',
    /\/trace\/trace-e2e-b1-smoke-abc123/,
  );
});
