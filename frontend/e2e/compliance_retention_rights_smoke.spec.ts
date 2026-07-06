// Phase 8 Stage B-5a — Compliance Retention & rights smoke (§4.3 verbatim).
//
// First-commit gating: §4.3 surface lands with this Playwright chromium
// smoke IN THE SAME COMMIT.
//
// Scope (§4.3 verbatim elements):
//   * BINDING COPY unset-banner verbatim when all classes unset (B5a-G3);
//   * three separately-addressable held-class regions:
//     ledger_row / wizard_transcript / delivered_artifact;
//   * governed-rule BINDING COPY visible verbatim;
//   * NO write route reachable — Decide affordance is placeholder text.
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

const MOCK_RETENTION_UNSET = {
  global_default: { days: null, set_at: null, set_by: null },
  held_classes: [
    { class_name: 'ledger_row', posture: 'unset', days: null, set_at: null, set_by: null },
    { class_name: 'wizard_transcript', posture: 'unset', days: null, set_at: null, set_by: null },
    { class_name: 'delivered_artifact', posture: 'unset', days: null, set_at: null, set_by: null },
  ],
  resolved_at: '2026-07-06T00:00:00Z',
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
  }, { tok: MOCK_ACCESS_TOKEN });
  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  await page.route(/\/api\/compliance\/retention_config$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_RETENTION_UNSET) })
  );
});

test('compliance_retention_renders_b5a_g3_verbatim_and_three_regions', async ({ page }) => {
  await page.goto('/compliance/retention');
  await expect(page.getByTestId('compliance-retention-page')).toBeVisible({ timeout: 5000 });
  // B5a-G3 verbatim banner when all classes unset.
  await expect(page.getByTestId('compliance-retention-unset-copy')).toContainText(
    "No deletion rule is set. The system holds everything indefinitely and append-only until you set a retention window. This is a decision only you can make — the system won't guess a duration."
  );
  // Three separately-addressable regions.
  await expect(page.getByTestId('retention-region-ledger_row')).toBeVisible();
  await expect(page.getByTestId('retention-region-wizard_transcript')).toBeVisible();
  await expect(page.getByTestId('retention-region-delivered_artifact')).toBeVisible();
  // Each region has a distinct heading.
  await expect(page.getByTestId('retention-region-heading-ledger_row')).toContainText('Ledger rows');
  await expect(page.getByTestId('retention-region-heading-wizard_transcript')).toContainText('Wizard transcripts');
  await expect(page.getByTestId('retention-region-heading-delivered_artifact')).toContainText('Delivered acquisitions');
  // Governed-rule binding copy verbatim.
  await expect(page.getByTestId('compliance-retention-governed-rule-copy')).toContainText(
    'Setting a retention window here becomes a governed rule — versioned, dated, and recorded like every control change.'
  );
});

test('compliance_retention_is_read_only_at_b_5a_no_write_button', async ({ page }) => {
  await page.goto('/compliance/retention');
  await expect(page.getByTestId('compliance-retention-page')).toBeVisible({ timeout: 5000 });
  // Decide affordance renders as placeholder text at B-5a (not a button).
  await expect(page.getByTestId('retention-holdings-decide-placeholder')).toContainText('coming in rulebook writes');
  // No "save" / "update" / "commit" buttons on this surface.
  const buttons = page.locator('main button');
  const count = await buttons.count();
  for (let i = 0; i < count; i++) {
    const text = (await buttons.nth(i).textContent()) || '';
    const lower = text.toLowerCase();
    expect(lower).not.toContain('save');
    expect(lower).not.toContain('update');
    expect(lower).not.toContain('commit');
    expect(lower).not.toContain('write');
  }
});
