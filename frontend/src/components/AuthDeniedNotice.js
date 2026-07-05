/**
 * AuthDeniedNotice — Phase 8 Stage B-1 (Owner E2 ratified).
 *
 * Renders auth-denial responses (401/403 with `{reason, detail}` body from
 * `services/auth/auth_refusal_reasons.v0.json`).
 *
 * Owner E2 non-negotiable:
 *   "The three render paths (composed_conclusion / admission_refusal /
 *    infra-not-refusal) do not gain a fourth member wearing the first's
 *    clothes."
 *
 * This component is VISUALLY + SEMANTICALLY distinct from `RefusalCard`:
 *   - RefusalCard uses amber warning treatment (governance refusal).
 *   - AuthDeniedNotice uses neutral gray access-boundary treatment.
 *   - RefusalCard offers three actor-appropriate governance actions.
 *   - AuthDeniedNotice offers one action: sign in / refresh identity.
 *
 * The four-render-paths taxonomy at Ask Console:
 *   1. AnswerView    — 200 with ComposedConclusion_v0
 *   2. RefusalCard   — 422 with `outcome=refused` (governance)
 *   3. InfraFaultView — 5xx / network (infra-not-refusal)
 *   4. AuthDeniedNotice — 401/403 with `{reason, detail}` (access-control class)
 */
import React from 'react';
import { LockKeyhole } from 'lucide-react';

// The 4-code bounded set (Owner E2 non-negotiable). Kept in sync verbatim
// with `services/auth/auth_refusal_reasons.v0.json` on the backend.
const AUTH_REASON_LABELS = {
  auth_missing: 'Sign-in required',
  auth_expired: 'Session expired',
  auth_scope_insufficient: 'This action needs a broader key grant',
  auth_identity_mismatch_for_wizard_session: 'This session belongs to a different account',
};

export default function AuthDeniedNotice({ body, onSignIn }) {
  const reason = body?.reason || 'auth_missing';
  const label = AUTH_REASON_LABELS[reason] || 'Access not permitted';
  const detail = body?.detail || '';

  return (
    <article
      data-testid="auth-denied-notice"
      className="w-full max-w-2xl mx-auto"
      aria-label="Access denied"
    >
      <div className="rounded-lg border border-slate-300 bg-slate-50 p-5">
        <div className="flex items-start gap-3">
          <LockKeyhole className="w-5 h-5 mt-0.5 text-slate-500 flex-shrink-0" />
          <div className="flex-1">
            <h2
              data-testid="auth-denied-title"
              className="text-sm font-semibold text-slate-900"
            >
              {label}
            </h2>
            {detail && (
              <p
                data-testid="auth-denied-detail"
                className="mt-1 text-xs text-slate-700"
              >
                {detail}
              </p>
            )}
            <p
              data-testid="auth-denied-reason-code"
              className="mt-2 text-[10px] font-mono uppercase tracking-wider text-slate-500"
            >
              {reason}
            </p>
          </div>
        </div>
      </div>
      <div className="mt-4 flex">
        <button
          type="button"
          data-testid="auth-denied-signin"
          onClick={onSignIn}
          className="px-3 py-1.5 rounded-md border border-slate-300 bg-white hover:bg-slate-100 text-sm text-slate-900"
        >
          {reason === 'auth_expired' ? 'Refresh session' : 'Sign in'}
        </button>
      </div>
    </article>
  );
}
