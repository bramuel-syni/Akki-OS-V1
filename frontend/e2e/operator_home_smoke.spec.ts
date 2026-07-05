// Phase 8 Stage B-3 First Commit — Coverage gate for B-2 §2.1 Operator Home.
//
// Owner mandate: "B-2 surface coverage must be GREEN before any B-3 UI work."
// Chromium-only per Owner E7. Mocks network to keep the smoke hermetic —
// backend semantics are covered by the 791 backend gates; this spec is a
// surface-wiring gate.
//
// Scope (§2.1 verbatim elements exercised):
//   * Header calm-pattern + Commission-objective button
//   * Status line binding-copy
//   * At-most-one attention card (null path at B-2 baseline)
//   * Running list (empty state) + Capacity strip from GET /api/fleet/policy
//   * Navigation: Commission-objective click → /operator/commission

const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';

const MOCK_IDENTITY = {
  user_id: 'e2e-operator-1',
  email: 'operator@example.com',
  name: 'Operator E2E',
  roles: ['operator'],
  key_grants: [{ class: 'external', path: 'live_query', floor: 'utterance', scope: 'estate' }],
  created_at: '2026-07-05T00:00:00Z',
};

const MOCK_OPERATOR_STATUS = {
  identity: { user_id: MOCK_IDENTITY.user_id, email: MOCK_IDENTITY.email, roles: MOCK_IDENTITY.roles },
  running: [],
  attention: null,
  status_line: 'Running normally.',
};

const MOCK_FLEET_POLICY = {
  version: 'v0',
  apportionment: { mining: 0.4, transforms: 0.4, live_path: 0.2 },
  ceilings: {},
  hazard_stop_notes: [],
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
    window.localStorage.setItem('rms.b1.auth.refresh_token', 'refresh-e2e-mock');
  }, { tok: MOCK_ACCESS_TOKEN });

  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  await page.route(/\/api\/operator\/status$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_OPERATOR_STATUS) })
  );
  await page.route(/\/api\/fleet\/policy$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_FLEET_POLICY) })
  );
});

test('operator_home_renders_ui_spec_2_1_verbatim_elements', async ({ page }) => {
  await page.goto('/operator');

  // Surface visible under authenticated identity.
  await expect(page.getByTestId('operator-home-page')).toBeVisible({ timeout: 5000 });

  // §2.1 status line — binding-copy default when nothing is running.
  await expect(page.getByTestId('operator-status-line')).toContainText('Running normally.');

  // §2.1 at-most-one attention card — null at baseline, so element absent.
  await expect(page.getByTestId('operator-attention-card')).toHaveCount(0);

  // §2.1 Running list — empty-state present.
  await expect(page.getByTestId('operator-running-list')).toBeVisible();
  await expect(page.getByTestId('running-empty')).toContainText('Nothing running.');

  // §2.1 Commission-objective button present.
  await expect(page.getByTestId('operator-commission-objective')).toBeVisible();

  // §2.1 approved capacity strip — reads /api/fleet/policy.
  await expect(page.getByTestId('operator-capacity-strip')).toBeVisible();
  await expect(page.getByTestId('capacity-mining')).toContainText('40%');
  await expect(page.getByTestId('capacity-transforms')).toContainText('40%');
  await expect(page.getByTestId('capacity-live-path')).toContainText('20%');
});

test('operator_home_commission_objective_navigates_to_commission_wizard', async ({ page }) => {
  await page.goto('/operator');
  await expect(page.getByTestId('operator-home-page')).toBeVisible({ timeout: 5000 });
  await page.getByTestId('operator-commission-objective').click();
  await expect(page).toHaveURL(/\/operator\/commission$/);
});
