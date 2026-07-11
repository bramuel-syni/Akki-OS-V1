// PH-R1 · Owner enhancement promotion (2026-07-10) · /api/system/build_info
// smoke. Attests the endpoint is reachable through the ingress, returns
// the exact Owner-approved payload shape, and carries no secrets.
//
// Reads REACT_APP_BACKEND_URL from frontend/.env at test time; makes the
// fetch from within the browser page context (matches production ingress
// topology where /api/* routes to the backend service).
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

function readBackendUrl(): string {
  const envPath = path.resolve(__dirname, '..', '.env');
  const text = fs.readFileSync(envPath, 'utf-8');
  const match = text.match(/^REACT_APP_BACKEND_URL=(.+)$/m);
  if (!match) {
    throw new Error('REACT_APP_BACKEND_URL not found in frontend/.env');
  }
  return match[1].trim();
}

const BACKEND_URL = readBackendUrl();

async function fetchBackend(page, apiPath: string) {
  await page.goto('/');
  return await page.evaluate(
    async ({ backend, apiPath }) => {
      const resp = await fetch(`${backend}${apiPath}`);
      return { status: resp.status, body: await resp.json() };
    },
    { backend: BACKEND_URL, apiPath },
  );
}

test.describe('§3.4 Production Housing PH-R1 · /api/system/build_info smoke', () => {
  test('build_info reachable and returns the Owner-approved payload shape', async ({ page }) => {
    const { status, body } = await fetchBackend(page, '/api/system/build_info');
    expect(status).toBe(200);
    // Payload shape (Owner explicit): {git_sha, build_timestamp, parity_count}.
    expect(Object.keys(body).sort()).toEqual(['build_timestamp', 'git_sha', 'parity_count']);
    expect(typeof body.git_sha).toBe('string');
    expect(body.git_sha.length).toBeGreaterThan(0);
    expect(typeof body.build_timestamp).toBe('string');
    expect(body.build_timestamp.length).toBeGreaterThan(0);
    // Same authoritative counter as PH-E3 · /api/readyz.
    expect(body.parity_count).toBe(31);
  });

  test('build_info payload carries no secrets (Owner explicit)', async ({ page }) => {
    const { body } = await fetchBackend(page, '/api/system/build_info');
    const bodyStr = JSON.stringify(body);
    // Grep-negative for common secret patterns.
    expect(bodyStr).not.toMatch(/mongodb:\/\/[^:]+:[^@]+@/);
    expect(bodyStr).not.toMatch(/eyJ[A-Za-z0-9_\-]{20,}/);
    expect(bodyStr).not.toMatch(/sk-[A-Za-z0-9]{20,}/);
  });

  test('healthz reachable · liveness · 200 alive', async ({ page }) => {
    const { status, body } = await fetchBackend(page, '/api/healthz');
    expect(status).toBe(200);
    expect(body).toEqual({ status: 'alive' });
  });
});
