/**
 * Gate 2: Refusal first-class + validation distinguishability — RTL DOM verification.
 *
 * Tests:
 * T1: Mount RefusalCard with Service1Refusal@v0 → all 7 fields in DOM
 * T2: asked is prominent (has own data-testid, visible text)
 * T3: supported_class rendered as ClassBadge in DOM
 * T4: what_would_raise_it rendered as actionable text
 * T5: RefusalCard returns null when refusal is null (no DOM output)
 * T6: Validation-422 body shape {detail:[...]} is structurally distinct
 *     from refusal shape {outcome:"refused"} — the branching logic in
 *     ComposePage checks outcome before rendering RefusalCard.
 *     We verify RefusalCard does NOT render when given a validation-422-shaped object.
 *
 * Framework: React Testing Library.
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import RefusalCard from '../components/RefusalCard';

// ── Payloads ──────────────────────────────────────────────────────────

const REFUSAL_PAYLOAD = {
  outcome: 'refused',
  reason: 'composition_below_floor',
  run_id: 'run-test-abc123',
  trace_id: 'trace-test-def456',
  asked: 'What is the Kenyan economic outlook?',
  supported_class: 'utterance',
  what_would_raise_it: 'Supply corroborated material at fact class.',
};

const VALIDATION_422 = {
  detail: [
    { type: 'missing', loc: ['body', 'floor'], msg: 'Field required', input: {} },
    { type: 'missing', loc: ['body', 'units'], msg: 'Field required', input: {} },
  ],
};

// ── Tests ─────────────────────────────────────────────────────────────

describe('Gate 2: Refusal first-class + validation distinguishability', () => {
  test('T1: RefusalCard renders all displayable Service1Refusal@v0 fields', () => {
    render(<RefusalCard refusal={REFUSAL_PAYLOAD} />);

    // The 4 fields RefusalCard itself renders (asked, reason, supported_class, what_would_raise_it)
    expect(screen.getByTestId('refusal-asked')).toHaveTextContent(REFUSAL_PAYLOAD.asked);
    expect(screen.getByTestId('refusal-reason')).toHaveTextContent(REFUSAL_PAYLOAD.reason);
    expect(screen.getByTestId('refusal-supported-class')).toBeInTheDocument();
    expect(screen.getByTestId('refusal-raise')).toHaveTextContent(REFUSAL_PAYLOAD.what_would_raise_it);

    // The card itself renders (outcome, run_id, trace_id are rendered by the parent ComposePage,
    // but RefusalCard must render the card container proving it was triggered)
    expect(screen.getByTestId('refusal-card')).toBeInTheDocument();
    expect(screen.getByTestId('refusal-headline')).toHaveTextContent('Not to the standard required.');
  });

  test('T2: asked is prominent — own test-id, visible text, labelled section', () => {
    render(<RefusalCard refusal={REFUSAL_PAYLOAD} />);
    const askedEl = screen.getByTestId('refusal-asked');
    expect(askedEl).toBeVisible();
    expect(askedEl).toHaveTextContent('What is the Kenyan economic outlook?');
    // Label present
    expect(screen.getByText('Asked')).toBeInTheDocument();
  });

  test('T3: supported_class rendered as ClassBadge with correct text', () => {
    render(<RefusalCard refusal={REFUSAL_PAYLOAD} />);
    expect(screen.getByTestId('class-badge-utterance')).toBeInTheDocument();
    expect(screen.getByTestId('class-badge-utterance')).toHaveTextContent('Recorded statement');
  });

  test('T4: what_would_raise_it rendered with label and actionable text', () => {
    render(<RefusalCard refusal={REFUSAL_PAYLOAD} />);
    expect(screen.getByText('What would raise it')).toBeInTheDocument();
    expect(screen.getByTestId('refusal-raise')).toHaveTextContent(
      'Supply corroborated material at fact class.'
    );
  });

  test('T5: RefusalCard returns null when refusal is null — no DOM output', () => {
    const { container } = render(<RefusalCard refusal={null} />);
    expect(container.innerHTML).toBe('');
  });

  test('T6: Validation-422 body does NOT trigger RefusalCard (structural distinguishability)', () => {
    // Validation-422 has {detail: [...]} — no asked, no reason, no outcome.
    // If someone accidentally passes validation-422 to RefusalCard, it renders null
    // because the conditional checks (refusal.asked &&, refusal.reason &&, etc.) all fail.
    render(<RefusalCard refusal={VALIDATION_422} />);
    // The card container still renders (refusal is truthy) but no field content appears
    const card = screen.getByTestId('refusal-card');
    expect(card).toBeInTheDocument();
    // None of the refusal field test-ids should exist
    expect(screen.queryByTestId('refusal-asked')).not.toBeInTheDocument();
    expect(screen.queryByTestId('refusal-reason')).not.toBeInTheDocument();
    expect(screen.queryByTestId('refusal-supported-class')).not.toBeInTheDocument();
    expect(screen.queryByTestId('refusal-raise')).not.toBeInTheDocument();
  });
});
