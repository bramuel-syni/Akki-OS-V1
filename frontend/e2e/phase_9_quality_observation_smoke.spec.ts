import { test, expect } from '@playwright/test';

test.describe('Phase 9 · Quality Observation smoke', () => {
  test('mining-stage visible inside extraction console running row', async ({ page }) => {
    await page.goto('/extraction/console');
    await expect(page.getByTestId('quality-observation-inline')).toBeVisible({ timeout: 10000 });
  });
});
