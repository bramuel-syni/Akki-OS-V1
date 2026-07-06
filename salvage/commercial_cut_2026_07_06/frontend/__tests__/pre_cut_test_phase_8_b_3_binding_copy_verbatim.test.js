/**
 * Phase 8 Stage B-3 Block 3 — §4 + §5 verbatim binding-copy gates.
 *
 * Owner Condition 3 verbatim (attached to D4b Block 3, 2026-07-04):
 *   "§4 + §5 verbatim including §4's binding copy ('There is no response
 *    shape in which the claim is separable from its class') and §5's
 *    dual-delta visibility on the buyer rail — {price_delta, class_delta}
 *    rendered as the pair, per the E6 visibility ruling; backend
 *    enforcement already exists, the surface shows both."
 *
 * This gate parametrises over the four §4/§5 binding-copy locations
 * and asserts each renders VERBATIM. Missing or altered copy on ANY
 * surface is a §4/§5-verbatim defect.
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// eslint-disable-next-line import/first
import EngineerFirstCallPage from '../../pages/engineer/EngineerFirstCallPage';
// eslint-disable-next-line import/first
import EngineerAdministerPage from '../../pages/engineer/EngineerAdministerPage';
// eslint-disable-next-line import/first
import BuyerAcquirePage from '../../pages/buyer/BuyerAcquirePage';

jest.mock('../../hooks/useAuth', () => {
  const stable = {
    identity: {
      user_id: 'test-copy-1',
      email: 'copy@example.com',
      name: 'Copy',
      roles: ['engineer', 'buyer'],
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
  useParams: () => ({ sessionId: 'wiz-b3-copy-abc' }),
}));

jest.mock('../../apiClient', () => {
  const mockedApi = {
    engineerListKeyGrants: () =>
      Promise.resolve({ status: 200, body: { grantee_email: 'copy@example.com', grants: [] } }),
    wizardBuyerGet: () =>
      Promise.resolve({
        status: 200,
        body: {
          session_id: 'wiz-b3-copy-abc',
          variant: 'buyer',
          status: 'draft',
          committed_values: {},
          turns: [],
          proposals: [],
          license_class: null,
        },
      }),
    wizardBuyerFreeze: () =>
      Promise.resolve({
        status: 200,
        body: { session_id: 'wiz-b3-copy-abc', status: 'frozen', trace_id: 't-c1', ledger_run_id: 'lr-c1' },
      }),
    wizardBuyerHandoff: () =>
      Promise.resolve({ status: 202, body: { trace_id: 't-c1' } }),
  };
  return {
    __esModule: true,
    default: mockedApi,
    api: mockedApi,
    formatApiErrorDetail: (d) => String(d),
  };
});

describe('Phase 8 B-3 Block 3 — §4 + §5 verbatim binding-copy gates (Owner Condition 3)', () => {
  test('§4.2 binding copy VERBATIM — "There is no response shape in which the claim is separable from its class"', async () => {
    render(
      <BrowserRouter>
        <EngineerFirstCallPage />
      </BrowserRouter>
    );
    const el = await screen.findByTestId('first-call-binding-copy');
    // First quoted clause — the load-bearing Owner phrase.
    expect(el).toHaveTextContent('There is no response shape in which the claim is separable from its class');
    // Second clause — infra-not-refusal invariant (Owner E2 symmetric cut).
    expect(el).toHaveTextContent('Infrastructure faults return 500 and are never rendered as refusals');
  });

  test('§4.3 footer binding copy VERBATIM — "Key scope is enforced server-side on every call."', async () => {
    render(
      <BrowserRouter>
        <EngineerAdministerPage />
      </BrowserRouter>
    );
    const el = await screen.findByTestId('administer-footer-binding-copy');
    expect(el).toHaveTextContent('Key scope is enforced server-side on every call.');
  });

  test('§5.2 framing binding copy VERBATIM — "Every acquisition passes the outer gate..."', async () => {
    render(
      <BrowserRouter>
        <BuyerAcquirePage />
      </BrowserRouter>
    );
    const el = await screen.findByTestId('buyer-acquire-framing-copy');
    expect(el).toHaveTextContent(
      'Every acquisition passes the outer gate. These checks are what make the data lawfully yours to use.'
    );
  });

  test('§5.2 footer binding copy VERBATIM — "If any check fails, the acquisition is refused..."', async () => {
    render(
      <BrowserRouter>
        <BuyerAcquirePage />
      </BrowserRouter>
    );
    const el = await screen.findByTestId('buyer-acquire-footer-binding-copy');
    expect(el).toHaveTextContent(
      'If any check fails, the acquisition is refused with the reason and a path forward — never partially delivered.'
    );
  });
});
