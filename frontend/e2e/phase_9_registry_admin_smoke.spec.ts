import { test, expect } from '@playwright/test';

test.describe('Phase 9 · Registry Admin smoke', () => {
  test('registry admin view renders with unknown-marker verbatim', async ({ page }) => {
    await page.goto('/extraction/registry-admin');
    await expect(page.getByTestId('registry-admin-view')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('registry-admin-title')).toContainText('Registry Admin');
    await expect(page.getByTestId('registry-census-state-archive://tenant-b')).toContainText('unknown');
  });

  test('trigger-census buttons render per row', async ({ page }) => {
    await page.goto('/extraction/registry-admin');
    await expect(page.getByTestId('registry-trigger-census-archive://tenant-a')).toBeVisible({ timeout: 10000 });
  });
});
