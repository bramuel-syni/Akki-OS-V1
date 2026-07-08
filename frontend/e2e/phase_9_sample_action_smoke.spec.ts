// Phase 9 Sub-stage 9.3 smoke: wizard sample action → grounding marker + result card.
import { test, expect } from '@playwright/test';

test.describe('Phase 9 · Sample flow smoke', () => {
  test('extraction console home renders with sample action + grounding marker', async ({ page }) => {
    await page.goto('/extraction/console');
    // Wait for the console home to render.
    await expect(page.getByTestId('extraction-console-home')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('extraction-console-home-title')).toContainText('Extraction Console');
    // Grounding marker renders with UI Spec §3.3 verbatim including em-dash.
    await expect(page.getByTestId('commit-review-grounding-marker')).toContainText('No sample run — estimates only.');
  });

  test('wizard sample action button visible when reach drafted', async ({ page }) => {
    await page.goto('/extraction/console');
    await expect(page.getByTestId('wizard-sample-action-button')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('wizard-sample-action-button')).toContainText('Run a sample');
  });
});
