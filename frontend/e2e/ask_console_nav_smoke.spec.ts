// Ask Console · ConsoleNavMenu discoverability smoke (Tier-3 hygiene).
// Attests:
//   * Landing on `/` shows Ask Console + nav toggle.
//   * Click toggle → menu opens with all 8 sibling links.
//   * Public route (Opportunity Briefs) loads directly on click.
//   * Auth-gated route (Operator) bounces to /auth/login when unauth'd.
import { test, expect } from '@playwright/test';

test.describe('Ask Console · ConsoleNavMenu discoverability smoke', () => {
  test('landing / renders Ask Console + nav toggle', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByTestId('ask-console-page')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('console-nav-toggle')).toBeVisible();
    // Menu not rendered until toggled.
    await expect(page.getByTestId('console-nav-menu')).toHaveCount(0);
  });

  test('opening menu exposes all 8 sibling routes', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByTestId('console-nav-toggle')).toBeVisible({ timeout: 10000 });
    await page.getByTestId('console-nav-toggle').click();
    await expect(page.getByTestId('console-nav-menu')).toBeVisible();
    for (const testid of [
      'console-nav-link-operator',
      'console-nav-link-engineer-register',
      'console-nav-link-master-admin',
      'console-nav-link-compliance',
      'console-nav-link-extraction-console',
      'console-nav-link-extraction-registry-admin',
      'console-nav-link-opportunity-briefs',
      'console-nav-link-auth-login',
    ]) {
      await expect(page.getByTestId(testid)).toBeVisible();
    }
  });

  test('public route (Opportunity Briefs) loads directly on click', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByTestId('console-nav-toggle')).toBeVisible({ timeout: 10000 });
    await page.getByTestId('console-nav-toggle').click();
    await page.getByTestId('console-nav-link-opportunity-briefs').click();
    await expect(page).toHaveURL(/\/opportunity-briefs/);
    await expect(page.getByTestId('opportunity-briefs-page')).toBeVisible({ timeout: 10000 });
  });

  test('auth-gated route (Operator) bounces to /auth/login when unauth\'d', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByTestId('console-nav-toggle')).toBeVisible({ timeout: 10000 });
    await page.getByTestId('console-nav-toggle').click();
    await page.getByTestId('console-nav-link-operator').click();
    // AuthProvider bounces to /auth/login when accessing gated route without a token.
    await expect(page).toHaveURL(/\/auth\/login/, { timeout: 10000 });
  });
});
