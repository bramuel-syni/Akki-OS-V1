// Phase 8 Seam 3 Sub-stage 1 — Playwright chromium smoke (E7 middle-dot glyph strict).
//
// Named gate (per Amendment F §5 test matrix):
//   test_coverage_marker_renders_middle_dot_glyph_verbatim
//
// Assertion (per §8.6 Point 3 refinement, Owner verbatim):
//   "MUST match the U+00B7 middle-dot byte specifically."
//   Not "surrounding words" — the glyph IS the point.
//
// First-commit gating: this smoke lands in the same commit as the wire-up,
// registry, backend router, frontend rider, and Pytest LB gate.
const { test, expect } = require('@playwright/test');

const MOCK_ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MOCK.SIGNATURE';
const MOCK_IDENTITY = {
  user_id: 'e2e-dpo-seam3',
  email: 'dpo-seam3@rms.example.com',
  name: 'DPO E2E Seam 3',
  roles: ['dpo', 'admin'],
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

const MOCK_COVERAGE_POPULATED = {
  families_since_system_start: [],
  families_since_seam_3: ['admission_refusals', 'composition_below_floor'],
  per_family_since_date: {
    admission_refusals: '2026-07-07',
    composition_below_floor: '2026-07-07',
  },
  seam_3_earliest_date: '2026-07-07',
  honest_note_when_no_families_covered: null,
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
  // ORDER MATTERS: refusals_coverage first (more specific) then refusals.
  await page.route(/\/api\/compliance\/refusals_coverage$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_COVERAGE_POPULATED) })
  );
  await page.route(/\/api\/compliance\/refusals\?/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(MOCK_REFUSALS_EMPTY) })
  );
});

test('test_coverage_marker_renders_middle_dot_glyph_verbatim', async ({ page }) => {
  await page.goto('/compliance');
  await expect(page.getByTestId('compliance-home-page')).toBeVisible({ timeout: 5000 });
  await expect(page.getByTestId('card-refusals-this-month')).toBeVisible();

  const rider = page.getByTestId('coverage-marker-rider');
  await expect(rider).toBeVisible({ timeout: 5000 });

  // The glyph gate — assert U+00B7 middle-dot appears verbatim, NOT hyphen.
  const riderText = await rider.textContent();
  expect(riderText).toContain('\u00B7');
  // Adversarial-to-comfort: assert hyphen substitution is NOT present.
  // (The rider must never render `-` where a middle-dot is required.)
  const seam3Line = await page.getByTestId('coverage-marker-since-seam-3').textContent();
  expect(seam3Line).toContain('\u00B7');
  expect(seam3Line).not.toMatch(/ - earlier events /);
  const perFamilyAdmission = await page.getByTestId('coverage-marker-family-admission_refusals').textContent();
  expect(perFamilyAdmission).toContain('\u00B7');
});

test('coverage_marker_empty_state_renders_honest_note_with_middle_dot', async ({ page, context }) => {
  // Override the coverage mock for THIS test only — empty payload.
  await page.route(/\/api\/compliance\/refusals_coverage$/, (route) =>
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({
      families_since_system_start: [],
      families_since_seam_3: [],
      per_family_since_date: {},
      seam_3_earliest_date: null,
      honest_note_when_no_families_covered: 'No refusal-family coverage yet \u00B7 this card will populate as families fire.',
    }) })
  );
  await page.goto('/compliance');
  await expect(page.getByTestId('compliance-home-page')).toBeVisible({ timeout: 5000 });
  const empty = page.getByTestId('coverage-marker-empty');
  await expect(empty).toBeVisible({ timeout: 5000 });
  const emptyText = await empty.textContent();
  expect(emptyText).toContain('\u00B7');
  expect(emptyText).not.toContain(' - ');
});
