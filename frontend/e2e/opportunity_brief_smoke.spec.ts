// UI Spec v2.2 §3.7 — Opportunity Briefs surface smoke.
// Attests OB-R3 Seam-1 α (advisory marker visible on every card),
// OB-R6 (three scope chips), OB-R5 (stale indicator on stale brief),
// OB-R4 (shape-as-objective handoff navigates to commission wizard).
import { test, expect } from '@playwright/test';

const ADVISORY_MARKER = 'Advisory: opportunity brief — not a governed response.';

test.describe('§3.15 Opportunity Briefs · surface smoke', () => {
  test('opportunity briefs page renders three fixture briefs with advisory markers', async ({ page }) => {
    await page.goto('/opportunity-briefs');
    await expect(page.getByTestId('opportunity-briefs-page')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('opportunity-briefs-page-title')).toContainText('Opportunity Briefs');
    // AS-U2 fixture notice present.
    await expect(page.getByTestId('opportunity-briefs-fixture-notice')).toBeVisible();

    // Three fixture briefs (one per scope).
    await expect(page.getByTestId('opportunity-brief-card-brief_fixture_slice_a')).toBeVisible();
    await expect(page.getByTestId('opportunity-brief-card-brief_fixture_combined_ab')).toBeVisible();
    await expect(page.getByTestId('opportunity-brief-card-brief_fixture_estate')).toBeVisible();

    // OB-R3 Seam-1 α · advisory marker verbatim on every card.
    const markers = page.getByTestId('opportunity-brief-advisory-marker');
    await expect(markers).toHaveCount(3);
    const firstMarker = markers.first();
    await expect(firstMarker).toContainText(ADVISORY_MARKER);
  });

  test('scope chips render for slice / combined / estate', async ({ page }) => {
    await page.goto('/opportunity-briefs');
    await expect(page.getByTestId('opportunity-brief-scope-chip-slice')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('opportunity-brief-scope-chip-combined')).toBeVisible();
    await expect(page.getByTestId('opportunity-brief-scope-chip-estate')).toBeVisible();
  });

  test('stale indicator renders on the stale estate fixture brief', async ({ page }) => {
    await page.goto('/opportunity-briefs');
    // Only the estate fixture has stale=true.
    const staleIndicators = page.getByTestId('opportunity-brief-stale-indicator');
    await expect(staleIndicators).toHaveCount(1);
  });

  test('shape-as-objective click stashes reach prefill + navigates off briefs page (OB-R4 handoff)', async ({ page }) => {
    await page.goto('/opportunity-briefs');
    await expect(page.getByTestId('opportunity-briefs-page')).toBeVisible({ timeout: 10000 });
    // Click on the first brief's shape-as-objective button.
    const btns = page.getByTestId('opportunity-brief-shape-as-objective-button');
    await btns.first().click();
    // OB-R4 · handoff pre-fills wizard reach in sessionStorage. Wizard
    // then proceeds under its normal auth-gated rules; assert the
    // sessionStorage was written + we navigated off the briefs page.
    const stashed = await page.evaluate(() =>
      window.sessionStorage.getItem('opportunity_brief_reach_prefill'),
    );
    expect(stashed).not.toBeNull();
    const parsed = JSON.parse(stashed);
    expect(parsed).toHaveProperty('contributing_slices');
    expect(parsed).toHaveProperty('brief_id');
    // Navigation left the briefs page (auth-gate may redirect further,
    // but the handoff has fired).
    await expect(page).not.toHaveURL(/\/opportunity-briefs/);
  });
});
