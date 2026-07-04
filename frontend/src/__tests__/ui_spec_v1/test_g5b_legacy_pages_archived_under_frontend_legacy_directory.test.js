/**
 * G5b legacy pages archived under `src/legacy/pages/` — Phase 8a-lite
 * invariant.
 *
 * Owner ruling (Phase 8a-lite dispatch, 2026-07-04): Ask Console is the
 * new primary surface at `/`. The eight G5b pages are archived under
 * `src/legacy/pages/`; no active route in `src/App.js` may reference
 * `src/pages/{Landing,OperatorDashboard,Runs,RunDetail,Discipline,
 * Engines,TraceReceipt,Compose}Page.js` — those files must live under
 * `src/legacy/pages/` only. This gate enforces the archival mechanically.
 *
 * Framework: Node fs (static grep) — legitimate for code-hygiene checks
 * (same pattern as G5b Gate 3 Part A).
 */
const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '..', '..');
const LEGACY_PAGE_NAMES = [
  'LandingPage',
  'OperatorDashboard',
  'RunsPage',
  'RunDetailPage',
  'DisciplinePage',
  'EnginesPage',
  'TraceReceiptPage',
  'ComposePage',
];

describe('Phase 8a-lite: G5b legacy pages archived under src/legacy/pages/', () => {
  test('no page file with a legacy name exists directly under src/pages/', () => {
    const pagesDir = path.join(SRC_DIR, 'pages');
    if (!fs.existsSync(pagesDir)) {
      // If the pages dir doesn't exist that's fine — Ask Console lives there
      // but is not one of the legacy names.
      return;
    }
    const entries = fs.readdirSync(pagesDir);
    const stragglers = entries.filter((name) =>
      LEGACY_PAGE_NAMES.some((legacy) => name === `${legacy}.js`)
    );
    expect(stragglers).toEqual([]);
  });

  test('every legacy page file exists under src/legacy/pages/', () => {
    const legacyDir = path.join(SRC_DIR, 'legacy', 'pages');
    expect(fs.existsSync(legacyDir)).toBe(true);
    const entries = fs.readdirSync(legacyDir);
    for (const legacyName of LEGACY_PAGE_NAMES) {
      expect(entries).toContain(`${legacyName}.js`);
    }
  });

  test('src/App.js never imports a legacy page from `./pages/`', () => {
    const appPath = path.join(SRC_DIR, 'App.js');
    const content = fs.readFileSync(appPath, 'utf8');
    for (const legacyName of LEGACY_PAGE_NAMES) {
      // A legacy import from `./pages/<Legacy>` is a violation. Imports
      // from `./legacy/pages/<Legacy>` are fine (nested under /legacy/*).
      const bareImport = new RegExp(
        `from\\s+['"]\\.\\/pages\\/${legacyName}['"]`
      );
      expect(content).not.toMatch(bareImport);
    }
  });

  test('src/App.js declares AskConsolePage at the index route', () => {
    const appPath = path.join(SRC_DIR, 'App.js');
    const content = fs.readFileSync(appPath, 'utf8');
    expect(content).toMatch(/from\s+['"]\.\/pages\/AskConsolePage['"]/);
    expect(content).toMatch(/<Route\s+index\s+element=\{<AskConsolePage\s*\/>\}/);
  });
});
