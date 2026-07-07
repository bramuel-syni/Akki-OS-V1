/**
 * Phase 8 Seam 3 Sub-stage 3 — CounterSignBanner structural tests.
 *
 * Per Owner Ruling 2 (Amendment G, 2026-07-07): the banner renders the
 * CAPACITY role (endpoint-required at time of transition). This suite
 * asserts structural invariants (barrel export, testid presence,
 * middle-dot glyph strict, per-role prop wiring).
 */
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';

// eslint-disable-next-line import/first
import {
  CounterSignBanner as BarreledBanner,
  COUNTER_SIGN_MIDDLE_DOT,
} from '../../components/ui_spec_v1';
// eslint-disable-next-line import/first
import CounterSignBanner, {
  MIDDLE_DOT,
} from '../../components/ui_spec_v1/CounterSignBanner';

jest.mock('axios');
// eslint-disable-next-line import/first
import axios from 'axios';

describe('Phase 8 Seam 3 Sub-stage 3 — CounterSignBanner structure', () => {
  beforeEach(() => {
    axios.get.mockReset();
  });

  test('is exported from the ui_spec_v1 barrel', () => {
    expect(BarreledBanner).toBe(CounterSignBanner);
  });

  test('middle-dot constant is exactly U+00B7 (E7 strict)', () => {
    expect(MIDDLE_DOT).toBe('\u00B7');
    expect(MIDDLE_DOT.charCodeAt(0)).toBe(0x00B7);
    expect(COUNTER_SIGN_MIDDLE_DOT).toBe(MIDDLE_DOT);
  });

  test('renders empty-state with role attribute and middle-dot glyph', async () => {
    axios.get.mockResolvedValueOnce({ data: { pending: [], count: 0 } });
    render(<CounterSignBanner role="compliance" token="tok-x" />);
    await waitFor(() =>
      expect(screen.getByTestId('counter-sign-banner-empty')).toBeTruthy()
    );
    const banner = screen.getByTestId('counter-sign-banner');
    expect(banner.getAttribute('data-role')).toBe('compliance');
    expect(banner.textContent).toContain(MIDDLE_DOT);
  });

  test('renders header + list when pending items are present', async () => {
    axios.get.mockResolvedValueOnce({
      data: {
        pending: [
          {
            request_id: 'rc-abc',
            rule_class: 'retention_windows',
            initiator_role: 'compliance',
            state: 'pending_counter_sign',
          },
        ],
        count: 1,
      },
    });
    render(<CounterSignBanner role="admin" token="tok-x" />);
    await waitFor(() =>
      expect(screen.getByTestId('counter-sign-banner-header')).toBeTruthy()
    );
    expect(screen.getByTestId('counter-sign-banner-item-rc-abc')).toBeTruthy();
    const header = screen.getByTestId('counter-sign-banner-header');
    expect(header.textContent).toContain(MIDDLE_DOT);
    expect(header.textContent).toContain('admin console');
  });

  test('renders error state when the API call fails', async () => {
    axios.get.mockRejectedValueOnce({
      response: { data: { detail: 'boom' } },
    });
    render(<CounterSignBanner role="admin" token="tok-x" />);
    await waitFor(() =>
      expect(screen.getByTestId('counter-sign-banner-error')).toBeTruthy()
    );
    expect(screen.getByTestId('counter-sign-banner-error').textContent).toBe(
      'boom'
    );
  });

  test('calls checker/pending with role query param and Bearer token', async () => {
    axios.get.mockResolvedValueOnce({ data: { pending: [], count: 0 } });
    render(<CounterSignBanner role="compliance" token="tok-abc" />);
    await waitFor(() => expect(axios.get).toHaveBeenCalled());
    const call = axios.get.mock.calls[0];
    expect(call[0]).toMatch(/\/api\/checker\/pending$/);
    expect(call[1].params).toEqual({ role: 'compliance' });
    expect(call[1].headers.Authorization).toBe('Bearer tok-abc');
  });
});
