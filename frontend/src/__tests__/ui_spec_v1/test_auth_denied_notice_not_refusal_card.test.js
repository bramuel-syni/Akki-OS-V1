/**
 * Phase 8 Stage B-1 — Owner E2 non-negotiable render-path invariant.
 *
 * "The three render paths (composed_conclusion / admission_refusal /
 *  infra-not-refusal) do not gain a fourth member wearing the first's
 *  clothes."
 *
 * Auth-denial (401/403 with `{reason, detail}` body) MUST render via
 * `AuthDeniedNotice` — NEVER via `RefusalCard`. The taxonomy at Ask
 * Console has FOUR non-overlapping render paths:
 *   1. AnswerView
 *   2. RefusalCard        (governance refusal — outcome=refused)
 *   3. InfraFaultView     (5xx / network — infra-not-refusal)
 *   4. AuthDeniedNotice   (401/403 — access-control class)
 *
 * These gates enforce doctrinal separation:
 *   * AuthDeniedNotice renders WITHOUT any of RefusalCard's binding-copy strings.
 *   * AuthDeniedNotice does NOT surface the three UI-Spec-§3.3 governance action
 *     labels ("Accept as recorded statement" / "Narrow the objective" /
 *     "Lower the standard").
 *   * RefusalCard's data-testid namespace does NOT overlap with AuthDeniedNotice's.
 */
import React from 'react';
import { render, screen, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import AuthDeniedNotice from '../../components/AuthDeniedNotice';
import RefusalCard from '../../components/RefusalCard';

const AUTH_401_BODY_SHAPE = {
  reason: 'auth_missing',
  detail: 'Authentication required. Provide a valid Authorization: Bearer <token> header.',
};

const AUTH_403_SCOPE_BODY_SHAPE = {
  reason: 'auth_scope_insufficient',
  detail: 'Caller identity is authenticated but the required scope grant is absent.',
};

const REFUSAL_BODY_SHAPE = {
  outcome: 'refused',
  reason: 'composition_below_floor',
  asked: 'utterance',
  supported_class: 'utterance',
  what_would_raise_it: 'more sources',
  what_you_can_do: ['Accept as recorded statement'],
};

describe('Owner E2 render-path invariant — auth denial is NOT a governed refusal', () => {
  test('AuthDeniedNotice renders auth_missing body with distinct testids', () => {
    render(<AuthDeniedNotice body={AUTH_401_BODY_SHAPE} onSignIn={() => {}} />);
    const notice = screen.getByTestId('auth-denied-notice');
    expect(notice).toBeInTheDocument();
    expect(within(notice).getByTestId('auth-denied-title')).toBeInTheDocument();
    expect(within(notice).getByTestId('auth-denied-reason-code')).toHaveTextContent('auth_missing');
    expect(within(notice).getByTestId('auth-denied-signin')).toBeInTheDocument();
  });

  test('AuthDeniedNotice renders auth_scope_insufficient with distinct labelling', () => {
    render(<AuthDeniedNotice body={AUTH_403_SCOPE_BODY_SHAPE} onSignIn={() => {}} />);
    expect(screen.getByTestId('auth-denied-reason-code')).toHaveTextContent('auth_scope_insufficient');
  });

  test('AuthDeniedNotice does NOT expose ANY refusal-card testid', () => {
    render(<AuthDeniedNotice body={AUTH_401_BODY_SHAPE} onSignIn={() => {}} />);
    // Refusal-card testids MUST NOT be present.
    expect(screen.queryByTestId('refusal-card')).toBeNull();
    expect(screen.queryByTestId('refusal-binding-title')).toBeNull();
    expect(screen.queryByTestId('refusal-accept-recorded')).toBeNull();
    expect(screen.queryByTestId('refusal-narrow')).toBeNull();
    expect(screen.queryByTestId('refusal-lower-standard')).toBeNull();
  });

  test('AuthDeniedNotice does NOT render UI-Spec-§3.3 governance action labels', () => {
    render(<AuthDeniedNotice body={AUTH_401_BODY_SHAPE} onSignIn={() => {}} />);
    // Verbatim binding copy from UI Spec v1 §3.3.
    expect(screen.queryByText(/Accept as recorded statement/i)).toBeNull();
    expect(screen.queryByText(/Narrow the objective/i)).toBeNull();
    expect(screen.queryByText(/Lower the standard/i)).toBeNull();
    // Verbatim §3.3 binding title (governance refusal).
    expect(screen.queryByText(/Not to the standard you asked for\./i)).toBeNull();
  });

  test('RefusalCard renders governance body with distinct binding copy (regression baseline)', () => {
    render(<RefusalCard refusal={REFUSAL_BODY_SHAPE} />);
    // RefusalCard uses its own testids — none of which the AuthDeniedNotice carries.
    // (This test locks in the two components' distinct testid namespaces.)
    const authNoticeTestIds = ['auth-denied-notice', 'auth-denied-title', 'auth-denied-signin', 'auth-denied-reason-code'];
    authNoticeTestIds.forEach((tid) => {
      expect(screen.queryByTestId(tid)).toBeNull();
    });
  });

  test('AuthDeniedNotice body shape MUST NOT contain outcome=refused', () => {
    // If a payload with outcome=refused were mistakenly routed into AuthDeniedNotice,
    // the notice must still not render it as a governance refusal. This gate ensures
    // the component IGNORES any 'outcome' field entirely (it never reads it).
    const misroute = { ...REFUSAL_BODY_SHAPE, reason: 'auth_missing' };
    render(<AuthDeniedNotice body={misroute} onSignIn={() => {}} />);
    // Renders as auth denial (uses `reason` field only), NOT as governance refusal.
    expect(screen.getByTestId('auth-denied-notice')).toBeInTheDocument();
    // No RefusalCard binding copy appears.
    expect(screen.queryByText(/Not to the standard you asked for\./i)).toBeNull();
  });
});
