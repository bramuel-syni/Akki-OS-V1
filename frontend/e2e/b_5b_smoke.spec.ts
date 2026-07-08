// Phase 8 Stage B-5b — Playwright chromium smokes.
//
// Owner Rulings B5b-E1..B5b-E5 (Amendment H, 2026-07-07) pre-carried.
// Middle-dot U+00B7 strict per E7.
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.B5B';
const MOCK_MASTER_ADMIN_IDENTITY = {
  user_id: 'e2e-ma-1',
  email: 'owner@rms.example.com',
  name: 'Owner E2E',
  roles: ['master_admin', 'admin', 'dpo'],
  key_grants: [],
  created_at: '2026-07-07T00:00:00Z',
};
const MOCK_DPO_IDENTITY = {
  user_id: 'e2e-dpo-1',
  email: 'dpo@rms.example.com',
  name: 'DPO E2E',
  roles: ['dpo'],
  key_grants: [],
  created_at: '2026-07-07T00:00:00Z',
};

const MOCK_RETENTION_ALL_UNSET = {
  global_default: { days: null, set_at: null, set_by: null },
  held_classes: [],
  resolved_at: '2026-07-07T00:00:00Z',
};

test.describe('B-5b — Compliance rulebook write page', () => {
  test.beforeEach(async ({ context }) => {
    await context.addInitScript(({ tok }) => {
      window.localStorage.setItem('rms.b1.auth.access_token', tok);
      window.localStorage.setItem('rms_auth_token', tok);
    }, { tok: MOCK_ACCESS_TOKEN });
  });

  test('rulebook page renders 4 writers with middle-dot intro', async ({ page }) => {
    await page.route(/\/api\/auth\/me$/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_DPO_IDENTITY) })
    );
    await page.goto('/compliance/rulebook');
    await expect(page.getByTestId('compliance-rulebook-write-page')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('retention-writer')).toBeVisible();
    await expect(page.getByTestId('disclosure-writer')).toBeVisible();
    await expect(page.getByTestId('lawful-basis-writer')).toBeVisible();
    await expect(page.getByTestId('source-standing-writer')).toBeVisible();
    const intro = await page.getByTestId('rulebook-intro').textContent();
    expect(intro).toContain('\u00B7'); // E7 middle-dot strict
  });

  test('disclosure writer submit posts to disclosure_thresholds and renders pending state', async ({ page }) => {
    await page.route(/\/api\/auth\/me$/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_DPO_IDENTITY) })
    );
    await page.route(/\/api\/compliance\/disclosure_thresholds$/, (route) =>
      route.fulfill({
        status: 202,
        contentType: 'application/json',
        body: JSON.stringify({
          outcome: 'pending_counter_sign',
          state: 'pending_counter_sign',
          consequence_class: 'dual_control',
          request_id: 'rc-e2e-1',
          rule_class: 'disclosure_thresholds',
        }),
      })
    );
    await page.goto('/compliance/rulebook');
    await page.getByTestId('disclosure-writer-from').fill('3');
    await page.getByTestId('disclosure-writer-to').fill('5');
    await page.getByTestId('disclosure-writer-submit').click();
    await expect(page.getByTestId('disclosure-writer-response-state')).toBeVisible({ timeout: 5000 });
    const respText = await page.getByTestId('disclosure-writer-response-state').textContent();
    expect(respText).toContain('pending_counter_sign');
    expect(respText).toContain('\u00B7'); // E7 middle-dot
  });
});

test.describe('B-5b — Admin read-only retrofit (RT-R1)', () => {
  test.beforeEach(async ({ context }) => {
    await context.addInitScript(({ tok }) => {
      window.localStorage.setItem('rms.b1.auth.access_token', tok);
      window.localStorage.setItem('rms_auth_token', tok);
    }, { tok: MOCK_ACCESS_TOKEN });
  });

  test('admin console renders compliance classes read-only with owned-by-Compliance marker', async ({ page }) => {
    await page.route(/\/api\/auth\/me$/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_MASTER_ADMIN_IDENTITY) })
    );
    await page.route(/\/api\/checker\/pending/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ pending: [], count: 0 }) })
    );
    await page.route(/\/api\/master_admin\/pending_seams/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ count: 0, seams: [] }) })
    );
    await page.goto('/master-admin');
    await expect(page.getByTestId('admin-compliance-read-only-view')).toBeVisible({ timeout: 5000 });
    for (const rc of ['retention_windows', 'disclosure_thresholds', 'lawful_basis_registry', 'source_standing_table']) {
      const marker = page.getByTestId(`admin-compliance-marker-${rc}`);
      await expect(marker).toBeVisible();
      await expect(marker).toHaveText('owned by Compliance');
    }
  });
});

test.describe('B-5b — Suspend button gating (Ruling B5b-E1 α)', () => {
  test.beforeEach(async ({ context }) => {
    await context.addInitScript(({ tok }) => {
      window.localStorage.setItem('rms.b1.auth.access_token', tok);
      window.localStorage.setItem('rms_auth_token', tok);
    }, { tok: MOCK_ACCESS_TOKEN });
  });

  test('Suspend button absent on dual_control rows', async ({ page }) => {
    await page.route(/\/api\/auth\/me$/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_MASTER_ADMIN_IDENTITY) })
    );
    await page.route(/\/api\/checker\/pending/, (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          pending: [{
            request_id: 'rc-dual-e2e',
            rule_class: 'retention_windows',
            initiator_role: 'compliance',
            state: 'pending_counter_sign',
            consequence_class: 'dual_control',
          }],
          count: 1,
        }),
      })
    );
    await page.route(/\/api\/master_admin\/pending_seams/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ count: 0, seams: [] }) })
    );
    await page.goto('/master-admin');
    await expect(page.getByTestId('counter-sign-banner-item-rc-dual-e2e')).toBeVisible({ timeout: 5000 });
    // Named gate assertion: no Suspend button on dual_control rows.
    await expect(page.getByTestId('suspend-by-owner-btn-rc-dual-e2e')).toHaveCount(0);
  });

  test('Suspend button present on tightening_unilateral rows for master_admin', async ({ page }) => {
    await page.route(/\/api\/auth\/me$/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_MASTER_ADMIN_IDENTITY) })
    );
    await page.route(/\/api\/checker\/pending/, (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          pending: [{
            request_id: 'rc-tight-e2e',
            rule_class: 'source_standing_table',
            initiator_role: 'admin',
            state: 'pending_delay',
            consequence_class: 'tightening_unilateral',
          }],
          count: 1,
        }),
      })
    );
    await page.route(/\/api\/master_admin\/pending_seams/, (route) =>
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ count: 0, seams: [] }) })
    );
    await page.goto('/master-admin');
    await expect(page.getByTestId('suspend-by-owner-btn-rc-tight-e2e')).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId('suspend-by-owner-btn-rc-tight-e2e')).toHaveText('Suspend by Owner');
  });
});
