// Phase 8 Stage B-3 First Commit — Coverage gate for B-2 §2.3 CommitReview.
//
// Owner mandate: B-2 surface coverage GREEN before any B-3 UI work.
// Chromium-only per Owner E7. Mocks network; freeze semantics + commit-review
// state machine are covered by backend Phase 7 B-1/B-2/B-3 gates.
//
// Scope (§2.3 verbatim elements exercised):
//   * "You supplied" section
//   * "Agent assumed — confirm or change" section (amber chip + change link)
//   * Feasibility verdict card (Floor feasible)
//   * Envelope line
//   * Verbatim binding copy "Frozen is immutable — a changed intent is a new objective."
//   * Freeze objective button + click → frozen confirmation with trace_id + ledger_run_id

const { test, expect } = require('@playwright/test');

const SESSION_ID = 'wiz-e2e-cr-abc123';
const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';

const MOCK_IDENTITY = {
  user_id: 'e2e-operator-1',
  email: 'operator@example.com',
  name: 'Operator E2E',
  roles: ['operator'],
  key_grants: [{ class: 'external', path: 'live_query', floor: 'utterance', scope: 'estate' }],
  created_at: '2026-07-05T00:00:00Z',
};

const MOCK_COMMIT_REVIEW = {
  session_id: SESSION_ID,
  variant: 'operator',
  ready_to_freeze: true,
  you_supplied: [
    { field: 'reach', value: { region: 'KE', vertical: 'macro' } },
    { field: 'envelope.done_condition', value: 'delivered_by_2026-08-01' },
    { field: 'envelope.budget', value: 5000 },
    { field: 'envelope.lawful_basis', value: 'legitimate_interest' },
  ],
  agent_assumed_items: [
    { field: 'output.grain', value: 'synthesized_whole' },
    { field: 'output.standard', value: 'utterance' },
  ],
  violations: [],
  license_class_drift: null,
};

const MOCK_FREEZE_RESULT = {
  session_id: SESSION_ID,
  status: 'frozen',
  trace_id: 'trace-e2e-cr-freeze-xyz',
  ledger_run_id: 'run-e2e-cr-freeze-001',
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
    window.localStorage.setItem('rms.b1.auth.refresh_token', 'refresh-e2e-mock');
  }, { tok: MOCK_ACCESS_TOKEN });

  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  await page.route(/\/api\/wizard\/operator\/[^/]+\/commit-review$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_COMMIT_REVIEW) })
  );
  await page.route(/\/api\/wizard\/operator\/[^/]+\/freeze$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_FREEZE_RESULT) })
  );
});

test('commit_review_renders_ui_spec_2_3_verbatim_elements', async ({ page }) => {
  await page.goto(`/operator/commit-review/${SESSION_ID}`);

  await expect(page.getByTestId('commit-review-page')).toBeVisible({ timeout: 5000 });

  // §2.3 "You supplied" section present.
  await expect(page.getByTestId('you-supplied-section')).toBeVisible();
  await expect(page.getByTestId('you-supplied-reach')).toBeVisible();
  await expect(page.getByTestId('you-supplied-envelope.done_condition')).toBeVisible();

  // §2.3 "Agent assumed — confirm or change" section present + amber chips.
  await expect(page.getByTestId('agent-assumed-section')).toBeVisible();
  await expect(page.getByTestId('agent-assumed-output.grain')).toBeVisible();
  await expect(page.getByTestId('agent-assumed-chip-output.grain')).toBeVisible();
  await expect(page.getByTestId('agent-assumed-change-output.grain')).toBeVisible();

  // §2.3 Feasibility verdict card (Floor feasible) present.
  await expect(page.getByTestId('feasibility-verdict-card')).toBeVisible();

  // §2.3 Envelope line present.
  await expect(page.getByTestId('envelope-line')).toContainText('lawful basis');
  await expect(page.getByTestId('envelope-line')).toContainText('budget');

  // §2.3 Verbatim binding copy present before freeze.
  await expect(page.getByTestId('freeze-binding-copy')).toContainText(
    'Frozen is immutable — a changed intent is a new objective.'
  );

  // §2.3 Freeze objective button visible + enabled.
  const freezeBtn = page.getByTestId('freeze-objective-btn');
  await expect(freezeBtn).toBeVisible();
  await expect(freezeBtn).toBeEnabled();
});

test('commit_review_freeze_click_renders_frozen_confirmation', async ({ page }) => {
  await page.goto(`/operator/commit-review/${SESSION_ID}`);
  await expect(page.getByTestId('commit-review-page')).toBeVisible({ timeout: 5000 });

  await page.getByTestId('freeze-objective-btn').click();

  // §2.3 frozen confirmation with trace_id + ledger_run_id + verbatim binding copy.
  await expect(page.getByTestId('frozen-confirmation')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('frozen-confirmation')).toContainText(MOCK_FREEZE_RESULT.trace_id);
  await expect(page.getByTestId('frozen-confirmation')).toContainText(MOCK_FREEZE_RESULT.ledger_run_id);
  await expect(page.getByTestId('frozen-confirmation')).toContainText(
    'Frozen is immutable — a changed intent is a new objective.'
  );
});
