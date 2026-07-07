// Phase 8 Seam 3 Sub-stage 3 — CounterSignBanner Playwright chromium smoke.
//
// First-commit gating per Owner Ruling 5 (Amendment G, 2026-07-07): this
// smoke ships in the same atomic commit as the checker impl + tests +
// frontend banner + close report.
//
// Assertions per Ruling 2 (capacity-role render) + E7 (middle-dot glyph
// strict):
//   * Banner renders on ComplianceHomePage with data-role="compliance".
//   * Banner renders on MasterAdminHomePage with data-role="admin".
//   * Middle-dot U+00B7 glyph is present in rendered text on both pages.
//   * Header lists pending items with capacity roles rendered verbatim.
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';
const MOCK_IDENTITY = {
  user_id: 'e2e-dpo-1',
  email: 'dpo@rms.example.com',
  name: 'DPO E2E',
  roles: ['dpo', 'admin', 'master_admin'],
  key_grants: [],
  created_at: '2026-07-07T00:00:00Z',
};

const MOCK_RETENTION_ALL_UNSET = {
  global_default: { days: null, set_at: null, set_by: null },
  held_classes: [
    { class_name: 'ledger_row', posture: 'unset', days: null, set_at: null, set_by: null },
    { class_name: 'wizard_transcript', posture: 'unset', days: null, set_at: null, set_by: null },
    { class_name: 'delivered_artifact', posture: 'unset', days: null, set_at: null, set_by: null },
  ],
  resolved_at: '2026-07-07T00:00:00Z',
};

const MOCK_REFUSALS_EMPTY = {
  month: '2026-07',
  totals: { admission_refusals: 0, composition_below_floor: 0, outer_gate_refusals: 0, unclassified: 0, total: 0 },
  by_reason: [],
  by_day: [],
};

const MOCK_PENDING_ADMIN = {
  pending: [
    {
      request_id: 'rc-adm-001',
      rule_class: 'retention_windows',
      initiator_role: 'compliance',
      state: 'pending_counter_sign',
      consequence_class: 'dual_control',
    },
  ],
  count: 1,
};

const MOCK_PENDING_COMPLIANCE = {
  pending: [],
  count: 0,
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
    window.localStorage.setItem('rms_auth_token', tok);
  }, { tok: MOCK_ACCESS_TOKEN });
  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  await page.route(/\/api\/compliance\/retention_config$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_RETENTION_ALL_UNSET) })
  );
  await page.route(/\/api\/compliance\/refusals/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_REFUSALS_EMPTY) })
  );
  await page.route(/\/api\/master_admin\/pending_seams/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ count: 0, seams: [] }) })
  );
});

test('counter_sign_banner_renders_on_compliance_home_with_middle_dot', async ({ page }) => {
  await page.route(/\/api\/checker\/pending.*role=compliance/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_PENDING_COMPLIANCE) })
  );
  await page.goto('/compliance');
  const banner = page.getByTestId('counter-sign-banner');
  await expect(banner).toBeVisible({ timeout: 5000 });
  await expect(banner).toHaveAttribute('data-role', 'compliance');
  await expect(page.getByTestId('counter-sign-banner-empty')).toBeVisible();
  // E7 middle-dot U+00B7 assertion — byte-strict on rendered text.
  const bannerText = await banner.textContent();
  expect(bannerText).toContain('\u00B7');
});

test('counter_sign_banner_renders_on_master_admin_home_with_pending_item', async ({ page }) => {
  await page.route(/\/api\/checker\/pending.*role=admin/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_PENDING_ADMIN) })
  );
  await page.goto('/master-admin');
  const banner = page.getByTestId('counter-sign-banner');
  await expect(banner).toBeVisible({ timeout: 5000 });
  await expect(banner).toHaveAttribute('data-role', 'admin');
  await expect(page.getByTestId('counter-sign-banner-header')).toBeVisible();
  // Ruling 2: capacity role rendered in list item, not identity primary role.
  await expect(page.getByTestId('counter-sign-banner-item-rc-adm-001')).toContainText('compliance');
  // E7 middle-dot glyph strict.
  const bannerText = await banner.textContent();
  expect(bannerText).toContain('\u00B7');
});

test('counter_sign_banner_header_singular_count_grammar', async ({ page }) => {
  await page.route(/\/api\/checker\/pending.*role=admin/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_PENDING_ADMIN) })
  );
  await page.goto('/master-admin');
  const header = page.getByTestId('counter-sign-banner-header');
  await expect(header).toBeVisible({ timeout: 5000 });
  const t = await header.textContent();
  expect(t).toMatch(/^1 pending rule-change request(?!s)/);
  expect(t).toContain('admin console');
});

test('counter_sign_banner_error_state_renders_when_endpoint_fails', async ({ page }) => {
  await page.route(/\/api\/checker\/pending/, (route) =>
    route.fulfill({ status: 500, contentType: 'application/json', body: JSON.stringify({ reason: 'infra', detail: 'boom' }) })
  );
  await page.goto('/compliance');
  await expect(page.getByTestId('counter-sign-banner-error')).toBeVisible({ timeout: 5000 });
});
