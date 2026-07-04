/**
 * Gate 1: Class inseparable — re-landed at Phase 8a-lite for UI Spec v1.
 *
 * Owner ruling (Phase 8a-lite dispatch, 2026-07-04): re-land the three
 * G5b invariant gates in `src/__tests__/ui_spec_v1/`. Copy-forward from
 * `src/legacy/__tests__/` with the surface-under-test updated to the
 * Ask Console + reused shared components (Owner Condition-2-flavored
 * posture: no reimplementation — ClassBadge, RefusalCard, LedgerTable
 * from `src/components/*` are reused as-is).
 *
 * For every component/surface that renders claim text, mount with a
 * synthetic payload and assert the defensibility class IS present in the
 * rendered DOM alongside the claim text.
 *
 * Framework: React Testing Library.
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import RefusalCard from '../../components/RefusalCard';
import ClassBadge from '../../components/ClassBadge';
import LedgerTable from '../../components/LedgerTable';

const REFUSAL_PAYLOAD = {
  outcome: 'refused',
  reason: 'composition_below_floor',
  run_id: 'run-test-abc123',
  trace_id: 'trace-test-def456',
  asked: 'What is the Kenyan economic outlook?',
  supported_class: 'utterance',
  what_would_raise_it: 'Supply corroborated material at fact class.',
};

const LEDGER_ROW_WITH_CLASS = {
  stage: 'admit',
  decision: 'admitted',
  reason: 'service_1_run_admitted',
  defensibility_class: 'utterance',
  trace_id: 'trace-ledger-001',
  artifact_ref: { artifact_id: 'art-001', artifact_type: 'mandate', version: 'v0' },
  lawful_basis_ref: 'legitimate_interest',
  at: '2026-07-02T01:23:52.439482Z',
};

const LEDGER_ROW_COMPUTED = {
  stage: 'converge',
  decision: 'continue',
  reason: 'solva_below_budget',
  computed_class: 'fact',
  trace_id: 'trace-ledger-002',
  artifact_ref: null,
  at: '2026-07-02T02:00:00Z',
};

describe('Gate 1 (UI Spec v1): Class inseparable', () => {
  test('RefusalCard renders supported_class alongside asked', () => {
    render(<RefusalCard refusal={REFUSAL_PAYLOAD} />);
    expect(screen.getByTestId('refusal-asked')).toHaveTextContent(
      'What is the Kenyan economic outlook?'
    );
    expect(screen.getByTestId('class-badge-utterance')).toBeInTheDocument();
    expect(screen.getByTestId('class-badge-utterance')).toHaveTextContent('Recorded statement');
  });

  test('RefusalCard renders reason and supported_class together', () => {
    render(<RefusalCard refusal={REFUSAL_PAYLOAD} />);
    expect(screen.getByTestId('refusal-reason')).toHaveTextContent('composition_below_floor');
    expect(screen.getByTestId('refusal-supported-class')).toBeInTheDocument();
  });

  test('LedgerTable renders defensibility_class alongside claim reason', () => {
    render(
      <MemoryRouter>
        <LedgerTable rows={[LEDGER_ROW_WITH_CLASS]} />
      </MemoryRouter>
    );
    expect(screen.getByText('service_1_run_admitted')).toBeInTheDocument();
    expect(screen.getByTestId('class-badge-utterance')).toBeInTheDocument();
  });

  test('LedgerTable renders computed_class when defensibility_class absent', () => {
    render(
      <MemoryRouter>
        <LedgerTable rows={[LEDGER_ROW_COMPUTED]} />
      </MemoryRouter>
    );
    expect(screen.getByText('solva_below_budget')).toBeInTheDocument();
    expect(screen.getByTestId('class-badge-fact')).toBeInTheDocument();
  });

  test('ClassBadge renders all three defensibility classes', () => {
    const { rerender } = render(<ClassBadge defensibilityClass="fact" />);
    expect(screen.getByTestId('class-badge-fact')).toHaveTextContent('Established fact');

    rerender(<ClassBadge defensibilityClass="utterance" />);
    expect(screen.getByTestId('class-badge-utterance')).toHaveTextContent('Recorded statement');

    rerender(<ClassBadge defensibilityClass="non_factual" />);
    expect(screen.getByTestId('class-badge-non_factual')).toHaveTextContent('Non-factual context');
  });

  test('ClassBadge returns null when defensibilityClass is falsy', () => {
    const { container } = render(<ClassBadge defensibilityClass={null} />);
    expect(container.innerHTML).toBe('');
  });

  test('ClassBadge renders Solva computed_class value (Solva boundary passthrough)', () => {
    render(<ClassBadge defensibilityClass="utterance" />);
    expect(screen.getByTestId('class-badge-utterance')).toBeInTheDocument();
  });
});
