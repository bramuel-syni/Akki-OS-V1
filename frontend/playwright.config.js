// Phase 8 Stage B-1 — Playwright config (Owner E7 ratified: chromium-only).
//
// Config file is CommonJS-friendly (frontend uses CRACO/webpack + Jest for
// unit tests; Playwright is standalone e2e). No TypeScript required at B-1;
// keeps zero extra tsconfig surface. Multi-browser expansion (Firefox/WebKit)
// waits for renderer-specific regression — see §8 E7 Stage-A proposal.
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: 'line',
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:3000',
    trace: 'off',
    // Bearer token is stored in localStorage; the smoke test seeds it directly.
    // No global fixtures at B-1.
  },
  projects: [
    // Owner E7 ratified: chromium-only at B-1.
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
