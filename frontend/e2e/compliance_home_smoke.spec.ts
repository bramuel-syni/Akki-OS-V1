// Phase 8 Stage B-5a — Compliance Home smoke (§4.1 verbatim).
//
// First-commit gating (Owner standing operational pattern): the §4.1
// surface lands with this Playwright chromium smoke IN THE SAME COMMIT.
//
// Scope (§4.1 verbatim elements):
//   * lookup input renders + navigates on Enter;
//   * three cards render: runs-with-lawful-basis, refusals-this-month,
//     retention-past-due;
//   * refusals card carries "See what was refused" link;
//   * retention past-due card carries "Decide" affordance;
//   * BINDING COPY visible verbatim;
//   * attention posture (adversarial-to-comfort) present ONLY when
//     genuine attention exists.
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

const MOCK_RETENTION_ALL_UNSET = {
  global_default: { days: null, set_at: null, set_by: null },
  held_classes: [
    { class_name: 'ledger_row', posture: 'unset', days: null, set_at: null, set_by: null },
    { class_name: 'wizard_transcript', posture: 'unset', days: null, set_at: null, set_by: null },
    { class_name: 'delivered_artifact', posture: 'unset', days: null, set_at: null, set_by: null },
  ],
  resolved_at: '2026-07-06T00:00:00Z',
};

const MOCK_REFUSALS_EMPTY = {
  month: '2026-07',
  totals: { admission_refusals: 0, composition_below_floor: 0, outer_gate_refusals: 0, unclassified: 0, total: 0 },
  by_reason: [],
  by_day: [],
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
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
});

test('compliance_home_renders_ui_spec_4_1_verbatim_elements', async ({ page }) => {
  await page.goto('/compliance');
  await expect(page.getByTestId('compliance-home-page')).toBeVisible({ timeout: 5000 });
  // §4.1 lookup — search input.
  await expect(page.getByTestId('compliance-home-lookup-input')).toBeVisible();
  // §4.1 three cards.
  await expect(page.getByTestId('card-runs-with-lawful-basis')).toBeVisible();
  await expect(page.getByTestId('card-refusals-this-month')).toBeVisible();
  await expect(page.getByTestId('card-retention-past-due')).toBeVisible();
  // §4.1 refusals card — See what was refused link.
  await expect(page.getByTestId('card-refusals-see-what')).toContainText('See what was refused');
  // §4.1 retention past-due card — Decide affordance.
  await expect(page.getByTestId('card-retention-decide')).toContainText('Decide');
  // §4.1 BINDING COPY VERBATIM.
  await expect(page.getByTestId('compliance-home-binding-copy')).toContainText(
    "This is the same record every user's audit view reaches — read-only, nothing reconstructed for display."
  );
});

test('compliance_home_attention_at_most_one_and_adversarial_to_comfort', async ({ page }) => {
  await page.goto('/compliance');
  await expect(page.getByTestId('compliance-home-page')).toBeVisible({ timeout: 5000 });
  // All-unset seed fires the attention banner.
  const attention = page.getByTestId('compliance-home-attention');
  await expect(attention).toBeVisible();
  // No all-green summary — no "everything ok" or similar.
  const bodyText = await page.locator('main').textContent();
  expect(bodyText).not.toMatch(/all good|everything ok|nothing to do/i);
});
