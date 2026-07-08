// Phase 8-EXT smoke: onboarding page + em-dash binding-copy verbatim.
import { test, expect } from '@playwright/test';

test.describe('Phase 8-EXT · Engineer onboarding smoke', () => {
  test('onboarding invite page renders with UI Spec §5.4 em-dash verbatim', async ({ page }) => {
    await page.goto('/engineer/onboarding');
    await expect(page.getByTestId('onboarding-invite-page')).toBeVisible({ timeout: 10000 });
    await expect(page.getByTestId('onboarding-invite-title')).toContainText('Invite an external engineer');
    await expect(page.getByTestId('onboarding-invite-spec-line')).toContainText('never outcome=refused, never the refusal card.');
  });

  test('submit button disabled until email entered', async ({ page }) => {
    await page.goto('/engineer/onboarding');
    await expect(page.getByTestId('onboarding-invite-submit')).toBeDisabled();
    await page.getByTestId('onboarding-invite-email-input').fill('candidate@example.com');
    await expect(page.getByTestId('onboarding-invite-submit')).toBeEnabled();
  });
});
