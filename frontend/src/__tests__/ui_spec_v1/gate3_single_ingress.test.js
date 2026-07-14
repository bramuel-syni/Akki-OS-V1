/**
 * Gate 3 (UI Spec v1): Single ingress + trace_id retention.
 *
 * Part A: Static analysis — scan `src/` (EXCLUDING `src/legacy/` because
 *         those pages are archived non-active surface per Phase 8a-lite
 *         archival ruling) for raw fetch()/axios()/XMLHttpRequest
 *         referencing `/api/`. Zero matches outside apiClient.js.
 *         This gate proves the ACTIVE surface at Ask Console has a single
 *         API ingress (apiClient.dispatchV2) with no lateral escape hatch.
 *
 * Part B: trace_id retention — RTL DOM verification. Mount LedgerTable
 *         and TrustReceiptLink with synthetic payloads containing
 *         trace_id → assert the trace_id appears in rendered DOM and
 *         links resolve to the promoted trust-receipt surface at
 *         `/trace/:traceId` (Owner ruling G-10/G-7 PROMOTE, 2026-07-14).
 *
 * Framework: Node fs (Part A) + React Testing Library (Part B).
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import LedgerTable from '../../components/LedgerTable';
import TrustReceiptLink from '../../components/TrustReceiptLink';

const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '..', '..');

function findRawApiCalls() {
  const violations = [];
  const excludePatterns = [
    'apiClient.js',
    '__tests__',
    'node_modules',
    'tailwind-compiled',
    'legacy', // archived non-active surface per Phase 8a-lite archival ruling
  ];

  function walkDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!excludePatterns.some((p) => fullPath.includes(p))) walkDir(fullPath);
      } else if (entry.name.endsWith('.js') || entry.name.endsWith('.jsx')) {
        if (excludePatterns.some((p) => fullPath.includes(p))) continue;
        const content = fs.readFileSync(fullPath, 'utf8');
        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          if (
            (line.includes('fetch(') ||
              line.includes('axios(') ||
              line.includes('axios.') ||
              line.includes('XMLHttpRequest')) &&
            line.includes('/api/')
          ) {
            violations.push({
              file: path.relative(SRC_DIR, fullPath),
              line: i + 1,
              text: line.trim(),
            });
          }
        }
      }
    }
  }
  walkDir(SRC_DIR);
  return violations;
}

describe('Gate 3 (UI Spec v1): Single ingress + trace_id retention', () => {
  test('Part A: Zero raw fetch/axios/XHR outside apiClient.js on the active surface', () => {
    const violations = findRawApiCalls();
    expect(violations).toEqual([]);
  });

  test('Part B: LedgerTable renders trace_id as link in DOM (promoted trust-receipt route)', () => {
    const rows = [
      {
        stage: 'admit',
        decision: 'admitted',
        reason: 'test_reason',
        defensibility_class: 'utterance',
        trace_id: 'trace-test-abc123',
        artifact_ref: null,
        at: '2026-07-02T00:00:00Z',
      },
    ];
    render(
      <MemoryRouter>
        <LedgerTable rows={rows} showTrace={true} />
      </MemoryRouter>
    );
    const link = screen.getByTestId('trace-link-trace-test-abc123');
    expect(link).toBeInTheDocument();
    // LedgerTable resolves to `/trace/{traceId}` — the public route wired
    // in `src/App.js` at Owner ruling G-10/G-7 PROMOTE (2026-07-14). The
    // App-level route wiring is covered by the promotion gate.
    expect(link).toHaveAttribute('href', '/trace/trace-test-abc123');
    expect(link.textContent).toContain('trace-test-abc123');
  });

  test('Part B: TrustReceiptLink renders trace_id in DOM', () => {
    render(
      <MemoryRouter>
        <TrustReceiptLink traceId="trace-test-abc123" />
      </MemoryRouter>
    );
    const link = screen.getByTestId('trust-receipt-link-trace-test-abc123');
    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute('href', '/trace/trace-test-abc123');
    expect(link).toHaveTextContent('trace-test-abc123');
  });

  test('Part B: TrustReceiptLink returns null when traceId is falsy', () => {
    const { container } = render(
      <MemoryRouter>
        <TrustReceiptLink traceId={null} />
      </MemoryRouter>
    );
    expect(container.innerHTML).toBe('');
  });
});
