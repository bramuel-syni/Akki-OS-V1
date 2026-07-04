/**
 * Gate 2 (UI Spec v1): Refusal first-class + validation distinguishability.
 * Re-landed at Phase 8a-lite; surface-under-test is the Ask Console
 * refusal branch, backed by the same `RefusalCard` shared component
 * (Owner Condition-2 posture: no reimplementation).
 *
 * Tests:
 *   T1: RefusalCard renders all displayable refusal envelope fields
 *   T2: `asked` is prominent (own test-id, visible, labelled)
 *   T3: `supported_class` rendered as ClassBadge in DOM
 *   T4: `what_would_raise_it` rendered with actionable text
 *   T5: RefusalCard returns null when refusal is null (no DOM output)
 *   T6: Validation-422 body shape {detail:[...]} is structurally distinct
 *       from refusal shape {outcome:"refused"} — RefusalCard shows no
 *       refusal field content when handed a validation-422 body.
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import RefusalCard from '../../components/RefusalCard';

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

describe('Gate 2 (UI Spec v1): Refusal first-class + validation distinguishability', () => {
  test('T1: RefusalCard renders all displayable refusal envelope fields', () => {
    render(<RefusalCard refusal={REFUSAL_PAYLOAD} />);
    expect(screen.getByTestId('refusal-asked')).toHaveTextContent(REFUSAL_PAYLOAD.asked);
    expect(screen.getByTestId('refusal-reason')).toHaveTextContent(REFUSAL_PAYLOAD.reason);
    expect(screen.getByTestId('refusal-supported-class')).toBeInTheDocument();
    expect(screen.getByTestId('refusal-raise')).toHaveTextContent(REFUSAL_PAYLOAD.what_would_raise_it);
    expect(screen.getByTestId('refusal-card')).toBeInTheDocument();
    expect(screen.getByTestId('refusal-headline')).toHaveTextContent('Not to the standard required.');
  });

  test('T2: asked is prominent — own test-id, visible text, labelled section', () => {
    render(<RefusalCard refusal={REFUSAL_PAYLOAD} />);
    const askedEl = screen.getByTestId('refusal-asked');
    expect(askedEl).toBeVisible();
    expect(askedEl).toHaveTextContent('What is the Kenyan economic outlook?');
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

  test('T6: Validation-422 body shape is structurally distinct from refusal shape', () => {
    render(<RefusalCard refusal={VALIDATION_422} />);
    const card = screen.getByTestId('refusal-card');
    expect(card).toBeInTheDocument();
    // Validation-422 has no asked / reason / supported_class / what_would_raise_it —
    // the field-conditional renders leave those DOM ids absent.
    expect(screen.queryByTestId('refusal-asked')).not.toBeInTheDocument();
    expect(screen.queryByTestId('refusal-reason')).not.toBeInTheDocument();
    expect(screen.queryByTestId('refusal-supported-class')).not.toBeInTheDocument();
    expect(screen.queryByTestId('refusal-raise')).not.toBeInTheDocument();
  });
});
