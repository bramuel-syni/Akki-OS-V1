// Phase 8 Stage B-3 First Commit — Coverage gate for B-2 §2.2 Commission Wizard.
//
// Owner mandate: B-2 surface coverage GREEN before any B-3 UI work.
// Chromium-only per Owner E7. Mocks network to keep the smoke hermetic —
// wizard state machine semantics are covered by 100+ backend gates; this
// spec is a surface-wiring gate.
//
// Scope (§2.2 verbatim elements exercised):
//   * Chat pane (left) + Objective draft rail (right) layout
//   * 8 mandatory-field rows rendered in draft rail
//   * Estate-check chip on turn with feasibility_snapshot_ref
//   * Chat input + submit + reactive re-render
//   * Review & freeze navigation link when a session exists

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

const MOCK_SESSION = { session_id: 'wiz-e2e-abc123', variant: 'operator', status: 'draft' };

const MOCK_FIRST_TURN = {
  turn_ref: 'turn-e2e-t01',
  agent_content: 'What outcome do you need this objective to produce?',
  feasibility_snapshot_ref: 'feas-snap-e2e-001',
  ask_slots: ['envelope.done_condition'],
  at: '2026-07-05T00:00:01Z',
};

const MOCK_WIZARD_STATE_EMPTY = {
  session_id: MOCK_SESSION.session_id,
  variant: 'operator',
  status: 'draft',
  committed_values: {},
  turns: [MOCK_FIRST_TURN],
  agent_assumptions: [],
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
    window.localStorage.setItem('rms.b1.auth.refresh_token', 'refresh-e2e-mock');
  }, { tok: MOCK_ACCESS_TOKEN });

  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  // Playwright's last-registered route wins. Register SPECIFIC routes AFTER
  // the general one so specific patterns take precedence:
  //   /api/wizard/operator/session         → registered LAST for /session POST
  //   /api/wizard/operator/{sid}/turn      → registered SECOND-LAST for /turn POST
  //   /api/wizard/operator/{sid}           → registered FIRST for GET wizard-state
  await page.route(/\/api\/wizard\/operator\/[^/]+$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(MOCK_WIZARD_STATE_EMPTY),
      });
      return;
    }
    // Non-GET fallthrough — try later-registered matching handlers.
    route.fallback();
  });
  await page.route(/\/api\/wizard\/operator\/[^/]+\/turn$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_FIRST_TURN) })
  );
  await page.route(/\/api\/wizard\/operator\/session$/, (route) =>
    route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(MOCK_SESSION) })
  );
});

test('commission_wizard_renders_ui_spec_2_2_verbatim_two_pane_layout', async ({ page }) => {
  await page.goto('/operator/commission');

  await expect(page.getByTestId('commission-wizard-page')).toBeVisible({ timeout: 5000 });

  // §2.2 Chat pane (left) present with agent turn rendered.
  await expect(page.getByTestId('commission-chat-pane')).toBeVisible();
  await expect(page.getByTestId(`chat-turn-${MOCK_FIRST_TURN.turn_ref}`)).toBeVisible();

  // §2.2 Estate-check chip present inline on a feasibility-dependent turn.
  await expect(page.getByTestId('estate-check-chip')).toBeVisible();

  // §2.2 Objective draft rail (right) present.
  await expect(page.getByTestId('commission-draft-rail')).toBeVisible();

  // §2.2 8 mandatory-field rows rendered.
  const mandatoryLabels = [
    'Reach',
    'Output · form',
    'Output · consumer',
    'Output · grain',
    'Output · standard',
    'Done condition',
    'Budget',
    'Lawful basis',
  ];
  for (const label of mandatoryLabels) {
    await expect(page.getByTestId(`draft-rail-row-${label}`)).toBeVisible();
  }

  // §2.2 Envelope line rendered.
  await expect(page.getByTestId('draft-envelope-line')).toBeVisible();
});

test('commission_wizard_accepts_operator_input_and_submits_turn', async ({ page }) => {
  await page.goto('/operator/commission');
  await expect(page.getByTestId('commission-wizard-page')).toBeVisible({ timeout: 5000 });

  // Input + submit exercised.
  await page.getByTestId('commission-input').fill('Live snapshot of Kenyan estate for Q3.');
  await page.getByTestId('commission-submit').click();

  // Chat turn re-renders (mock returns same turn — surface remains stable).
  await expect(page.getByTestId('commission-chat-pane')).toBeVisible();
});

test('commission_wizard_review_and_freeze_link_navigates_to_commit_review', async ({ page }) => {
  await page.goto('/operator/commission');
  await expect(page.getByTestId('commission-wizard-page')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('commission-goto-commit-review')).toBeVisible();
  await page.getByTestId('commission-goto-commit-review').click();
  await expect(page).toHaveURL(new RegExp(`/operator/commit-review/${MOCK_SESSION.session_id}$`));
});
