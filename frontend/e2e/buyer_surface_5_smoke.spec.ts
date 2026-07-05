// Phase 8 Stage B-3 Block 3 — Buyer §5 shape + acquire + receive smoke.
// Owner Condition 1: same-commit gating. Owner Condition 3: §5 dual-delta
// pair visible on the buyer rail (E6 Visibility-not-prohibition).
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';
const SESSION_ID = 'wiz-buyer-e2e-abc123';

const MOCK_IDENTITY = {
  user_id: 'e2e-buyer-1',
  email: 'buyer@example.com',
  name: 'Buyer E2E',
  roles: ['buyer'],
  key_grants: [{ class: 'external', path: 'live_query', floor: 'utterance', scope: 'estate' }],
  created_at: '2026-07-05T00:00:00Z',
};

const MOCK_SESSION = { session_id: SESSION_ID, variant: 'buyer', status: 'draft', trace_id: 't-b1', initiated_at: 'x' };
const MOCK_TURN = {
  turn_ref: 'turn-buyer-e2e-t01',
  agent_content: 'Which cohort are you looking to acquire?',
  feasibility_snapshot_ref: 'feas-snap-buyer-e2e-001',
  ask_slots: ['reach'],
  at: '2026-07-05T00:00:01Z',
};
const MOCK_STATE = {
  session_id: SESSION_ID,
  variant: 'buyer',
  status: 'draft',
  committed_values: {},
  turns: [MOCK_TURN],
  proposals: [],
  license_class: null,
};
const MOCK_PROPOSAL = {
  proposal_id: 'prop-buyer-e2e-01',
  price_delta: 'cuts price by 38%',
  class_delta: 'lowers to recorded_statement',
  proposal_content: 'Narrow to last 5 years cuts price by 38%.',
};

test.beforeEach(async ({ page, context }) => {
  await context.addInitScript(({ tok }) => {
    window.localStorage.setItem('rms.b1.auth.access_token', tok);
  }, { tok: MOCK_ACCESS_TOKEN });
  await page.route(/\/api\/auth\/me$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_IDENTITY) })
  );
  await page.route(/\/api\/wizard\/buyer\/[^/]+$/, (route) => {
    if (route.request().method() === 'GET') {
      route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_STATE) });
      return;
    }
    route.fallback();
  });
  await page.route(/\/api\/wizard\/buyer\/[^/]+\/turn$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_TURN) })
  );
  await page.route(/\/api\/wizard\/buyer\/[^/]+\/propose$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_PROPOSAL) })
  );
  await page.route(/\/api\/wizard\/buyer\/[^/]+\/freeze$/, (route) =>
    route.fulfill({
      status: 200, contentType: 'application/json',
      body: JSON.stringify({ session_id: SESSION_ID, status: 'frozen', trace_id: 't-b1', ledger_run_id: 'lr-b1' }),
    })
  );
  await page.route(/\/api\/wizard\/buyer\/session$/, (route) =>
    route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify(MOCK_SESSION) })
  );
});

test('buyer_shape_renders_ui_spec_5_1_verbatim_including_price_card', async ({ page }) => {
  await page.goto('/buyer/shape');
  await expect(page.getByTestId('buyer-shape-page')).toBeVisible({ timeout: 5000 });
  // §5.1 layout: chat pane + acquisition rail.
  await expect(page.getByTestId('buyer-chat-pane')).toBeVisible();
  await expect(page.getByTestId('buyer-acquisition-rail')).toBeVisible();
  // §5.1 rail rows.
  await expect(page.getByTestId('buyer-rail-reach')).toBeVisible();
  await expect(page.getByTestId('buyer-rail-output-form')).toBeVisible();
  await expect(page.getByTestId('buyer-rail-output-grain')).toBeVisible();
  await expect(page.getByTestId('buyer-rail-output-standard')).toBeVisible();
  await expect(page.getByTestId('buyer-rail-license-class')).toBeVisible();
  // §5.1 price card — verbatim "moves as you shape" + feasible-and-offerable.
  await expect(page.getByTestId('buyer-price-card')).toBeVisible();
  await expect(page.getByTestId('buyer-price-moves-as-you-shape')).toContainText('moves as you shape');
  await expect(page.getByTestId('buyer-delivery-estimate')).toBeVisible();
  await expect(page.getByTestId('buyer-feasible-line')).toContainText('Feasible-and-offerable');
});

test('buyer_shape_dual_delta_renders_as_pair_on_rail', async ({ page }) => {
  // Owner Condition 3 verbatim: {price_delta, class_delta} MUST render as a PAIR.
  await page.goto('/buyer/shape');
  await expect(page.getByTestId('buyer-shape-page')).toBeVisible();
  // Emit an illustrative proposal via the seam button.
  await page.getByTestId('buyer-emit-proposal').click();
  // §5 dual-delta pair present and BOTH deltas rendered.
  await expect(page.getByTestId('buyer-dual-delta-container')).toBeVisible({ timeout: 5000 });
  const pair = page.getByTestId('buyer-dual-delta-pair').first();
  await expect(pair).toBeVisible();
  await expect(page.getByTestId('buyer-dual-delta-price').first()).toContainText('cuts price by 38%');
  await expect(page.getByTestId('buyer-dual-delta-class').first()).toContainText('lowers to recorded_statement');
});

test('buyer_acquire_renders_ui_spec_5_2_verbatim_including_footer_binding_copy', async ({ page }) => {
  await page.goto(`/buyer/acquire/${SESSION_ID}`);
  await expect(page.getByTestId('buyer-acquire-page')).toBeVisible({ timeout: 5000 });
  // §5.2 framing line verbatim.
  await expect(page.getByTestId('buyer-acquire-framing-copy')).toContainText(
    'Every acquisition passes the outer gate. These checks are what make the data lawfully yours to use.'
  );
  // §5.2 four check rows.
  for (const id of ['rights_check', 'irreversibility_transform', 'cumulative_disclosure_check', 'license_issue']) {
    await expect(page.getByTestId(`buyer-check-row-${id}`)).toBeVisible();
  }
  // §5.2 footer binding-copy verbatim.
  await expect(page.getByTestId('buyer-acquire-footer-binding-copy')).toContainText(
    'If any check fails, the acquisition is refused with the reason and a path forward — never partially delivered.'
  );
});

test('buyer_receive_renders_ui_spec_5_3_verbatim_including_outer_gate_receipt', async ({ page }) => {
  await page.goto(`/buyer/receive/${SESSION_ID}`);
  await expect(page.getByTestId('buyer-receive-page')).toBeVisible({ timeout: 5000 });
  // §5.3 delivered header + download.
  await expect(page.getByTestId('buyer-receive-delivered-header')).toContainText('Delivered');
  await expect(page.getByTestId('buyer-receive-download-btn')).toBeVisible();
  // §5.3 artifact per-claim structure.
  await expect(page.getByTestId('buyer-receive-claim-text')).toBeVisible();
  await expect(page.getByTestId('buyer-receive-defensibility')).toContainText('class=');
  await expect(page.getByTestId('buyer-receive-provenance')).toContainText('trace_id=');
  // §5.3 outer-gate receipt card.
  await expect(page.getByTestId('buyer-outer-gate-receipt')).toBeVisible();
  await expect(page.getByTestId('outer-gate-transform')).toBeVisible();
  await expect(page.getByTestId('outer-gate-fingerprint')).toBeVisible();
  await expect(page.getByTestId('outer-gate-categories')).toBeVisible();
  await expect(page.getByTestId('outer-gate-license-ref')).toBeVisible();
  // §5.3 public trust-receipt line.
  await expect(page.getByTestId('buyer-public-trust-receipt-line')).toBeVisible();
  await expect(page.getByTestId('buyer-public-trust-receipt-url')).toContainText('rms.intel/trace/');
});
