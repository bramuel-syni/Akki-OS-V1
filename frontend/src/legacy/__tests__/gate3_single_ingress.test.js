/**
 * Gate 3: Single ingress + trace_id retention.
 *
 * Part A: Static analysis — scan /app/frontend/src/ for raw fetch()/axios()/XMLHttpRequest
 *         referencing /api/. Zero matches outside apiClient.js and ComposePage POST.
 *         Framework: Node fs (static grep). This IS legitimate for code-hygiene checks.
 *
 * Part B: trace_id retention — RTL DOM verification.
 *         Mount LedgerTable and TrustReceiptLink with synthetic payloads containing
 *         trace_id: "trace-test-abc123" → assert that string appears in rendered DOM.
 *         Framework: React Testing Library.
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import LedgerTable from '../components/LedgerTable';
import TrustReceiptLink from '../components/TrustReceiptLink';

const fs = require('fs');
const path = require('path');

const SRC_DIR = path.join(__dirname, '..');

// ── Part A: Static analysis ───────────────────────────────────────────

function findRawApiCalls() {
  const violations = [];
  const excludePatterns = ['apiClient.js', '__tests__', 'node_modules', 'tailwind-compiled'];

  function walkDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        if (!excludePatterns.some(p => fullPath.includes(p))) walkDir(fullPath);
      } else if (entry.name.endsWith('.js') || entry.name.endsWith('.jsx')) {
        if (excludePatterns.some(p => fullPath.includes(p))) continue;
        const content = fs.readFileSync(fullPath, 'utf8');
        const lines = content.split('\n');
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          if (
            (line.includes('fetch(') || line.includes('axios(') || line.includes('axios.') || line.includes('XMLHttpRequest')) &&
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

describe('Gate 3: Single ingress + trace_id retention', () => {
  // ── Part A ──────────────────────────────────────────────────────────
  test('Part A: Zero raw fetch/axios/XHR outside apiClient.js (excl. ComposePage POST)', () => {
    const violations = findRawApiCalls();
    const significant = violations.filter(v => !v.file.includes('ComposePage'));
    expect(significant).toEqual([]);
  });

  test('Part A: ComposePage POST is the only raw fetch and is intentional', () => {
    const violations = findRawApiCalls();
    const composeFetches = violations.filter(v => v.file.includes('ComposePage'));
    // Exactly 1 raw fetch in ComposePage (the POST /api/service_1/run)
    expect(composeFetches.length).toBe(1);
    expect(composeFetches[0].text).toContain('service_1/run');
  });

  // ── Part B: trace_id retention — RTL DOM ────────────────────────────

  test('Part B: LedgerTable renders trace_id as link in DOM', () => {
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
