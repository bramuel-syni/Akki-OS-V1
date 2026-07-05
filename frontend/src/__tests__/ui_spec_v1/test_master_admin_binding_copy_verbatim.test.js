/**
 * Phase 8 Stage B-4 — §6 Master Admin binding-copy VERBATIM gates.
 *
 * Owner Condition (standing): every governed binding-copy string
 * renders VERBATIM. Missing or altered copy on ANY surface is a
 * §6-verbatim defect.
 *
 * Four verbatim strings under audit:
 *   1. §6.1 pending banner:
 *      "Two rules are waiting on your decision before they can take effect."
 *      (plural-aware; the "Two" is count-substituted at render time)
 *   2. §6.1 footer link:
 *      "See everything I've changed — every action is recorded."
 *   3. §6.2 post-commit:
 *      "Recorded as your change, with today's date."
 *   4. §6.3 footer:
 *      "Every row carries its full diff. This trail is itself append-only
 *       and readable by the regulator surface."
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// eslint-disable-next-line import/first
import MasterAdminHomePage from '../../pages/master_admin/MasterAdminHomePage';
// eslint-disable-next-line import/first
import ChangeARulePage from '../../pages/master_admin/ChangeARulePage';
// eslint-disable-next-line import/first
import AuditTrailPage from '../../pages/master_admin/AuditTrailPage';

const MOCK_IDENTITY = {
  user_id: 'copy-master-1',
  email: 'admin@rms.example.com',
  name: 'MA Copy',
  roles: ['master_admin', 'admin'],
  key_grants: [],
  created_at: '2026-07-05T00:00:00Z',
};

jest.mock('../../hooks/useAuth', () => {
  const stable = {
    identity: {
      user_id: 'copy-master-1',
      email: 'admin@rms.example.com',
      name: 'MA Copy',
      roles: ['master_admin', 'admin'],
      key_grants: [],
      created_at: '2026-07-05T00:00:00Z',
    },
    login: () => {},
    register: () => {},
    logout: () => {},
    checkSession: () => {},
  };
  return {
    useAuth: () => stable,
    AuthProvider: ({ children }) => children,
  };
});

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: () => ({ ruleId: 'tier-lock' }),
}));

jest.mock('../../apiClient', () => {
  const mockedApi = {
    masterAdminPendingSeams: () =>
      Promise.resolve({
        status: 200,
        body: {
          count: 2,
          pending_seams: [
            { seam_id: 'x', plain_language_line: 'a', awaiting_whom: 'owner', seam_status: 'closed' },
            { seam_id: 'y', plain_language_line: 'b', awaiting_whom: 'dpo', seam_status: 'closed' },
          ],
        },
      }),
    masterAdminAuditTrail: () =>
      Promise.resolve({
        status: 200,
        body: {
          count: 1,
          actions: [
            {
              run_id: 'r1',
              trace_id: 't1',
              at: '2026-07-05T14:00:00Z',
              rule_id: 'tier_lock',
              grantor_id: 'admin-uid',
              plain_description: 'Pricing tier lock turned on (was off).',
              full_diff_ref: '/api/northena/ledger/by_run/r1',
            },
          ],
        },
      }),
    masterAdminTierLockCommit: () =>
      Promise.resolve({
        status: 200,
        body: { locked: true, reason_note: 'ok', trace_id: 't', ledger_run_id: 'r', at: '2026-07-05T14:00:00Z' },
      }),
    northenaLedgerByRunAbs: () => Promise.resolve([{ run_id: 'r1' }]),
  };
  return {
    __esModule: true,
    default: mockedApi,
    api: mockedApi,
    formatApiErrorDetail: (d) => String(d),
  };
});

describe('Phase 8 Stage B-4 — §6 verbatim binding-copy gates', () => {
  test('§6.1 pending copy VERBATIM (count-substituted, plural-aware) — "Two rules are waiting on your decision before they can take effect."', async () => {
    render(
      <BrowserRouter>
        <MasterAdminHomePage />
      </BrowserRouter>
    );
    const el = await screen.findByTestId('master-admin-pending-copy');
    expect(el).toHaveTextContent(
      'Two rules are waiting on your decision before they can take effect.'
    );
  });

  test('§6.1 footer link VERBATIM — "See everything I\'ve changed — every action is recorded."', async () => {
    render(
      <BrowserRouter>
        <MasterAdminHomePage />
      </BrowserRouter>
    );
    const el = await screen.findByTestId('master-admin-audit-footer-link');
    expect(el).toHaveTextContent("See everything I've changed — every action is recorded.");
  });

  test('§6.2 post-commit binding copy VERBATIM — "Recorded as your change, with today\'s date."', async () => {
    const { findByTestId } = render(
      <BrowserRouter>
        <ChangeARulePage />
      </BrowserRouter>
    );
    // Click commit button first (post-commit copy appears after).
    const commitBtn = await findByTestId('change-rule-commit-button');
    // React 18 hooks — trigger by dispatching click.
    commitBtn.click();
    const copy = await findByTestId('change-rule-recorded-binding-copy');
    expect(copy).toHaveTextContent("Recorded as your change, with today's date.");
  });

  test('§6.3 footer binding copy VERBATIM — "Every row carries its full diff..."', async () => {
    render(
      <BrowserRouter>
        <AuditTrailPage />
      </BrowserRouter>
    );
    const el = await screen.findByTestId('audit-trail-footer-binding-copy');
    expect(el).toHaveTextContent(
      'Every row carries its full diff. This trail is itself append-only and readable by the regulator surface.'
    );
  });

  test('§6.1 six action buttons carry their binding labels VERBATIM', async () => {
    render(
      <BrowserRouter>
        <MasterAdminHomePage />
      </BrowserRouter>
    );
    const expected = [
      ['master-admin-action-assign-a-role', 'Assign a role'],
      ['master-admin-action-change-a-rule', 'Change a rule'],
      ['master-admin-action-manage-keys-and-access', 'Manage keys & access'],
      ['master-admin-action-update-the-taxonomy', 'Update the taxonomy'],
      ['master-admin-action-set-pricing', 'Set pricing'],
      ['master-admin-action-apportion-gpu-capacity', 'Apportion GPU capacity'],
    ];
    for (const [tid, label] of expected) {
      const el = await screen.findByTestId(tid);
      expect(el).toHaveTextContent(label);
    }
  });

  test('§6.1 prompt VERBATIM — "What do you want to do?"', async () => {
    render(
      <BrowserRouter>
        <MasterAdminHomePage />
      </BrowserRouter>
    );
    const el = await screen.findByTestId('master-admin-prompt');
    expect(el).toHaveTextContent('What do you want to do?');
  });
});
