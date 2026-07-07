/**
 * Phase 8 Seam 3 Sub-stage 3 — CounterSignBanner component.
 *
 * Per Owner Ruling 2 (Amendment G, 2026-07-07):
 *   "Banner renders the role the countersign endpoint required."
 *
 * The banner renders the CAPACITY role at each row (initiator_role +
 * checker_role are the auth capacities the endpoints required at time of
 * transition), not identity primary/bracket roles. Determinism from
 * endpoint requirement. Middle-dot `·` (U+00B7) is E7-strict for the
 * commit-line binding copy.
 */
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Middle-dot glyph is E7-strict. Kept as a named constant so grep-tests
// have a stable single-source location.
export const MIDDLE_DOT = '\u00B7';

/**
 * @param {Object} props
 * @param {'compliance' | 'admin'} props.role - The console's capacity role.
 * @param {string} props.token - Auth token; parent passes.
 */
export const CounterSignBanner = ({ role, token }) => {
  const [items, setItems] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    async function fetchPending() {
      if (!token || !role) {
        return;
      }
      try {
        const res = await axios.get(`${API}/checker/pending`, {
          params: { role },
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!cancelled) {
          setItems(res.data.pending || []);
          setError(null);
        }
      } catch (e) {
        if (!cancelled) {
          setError(e.response?.data?.detail || 'Failed to load pending items.');
        }
      }
    }
    fetchPending();
    return () => {
      cancelled = true;
    };
  }, [role, token]);

  if (error) {
    return (
      <div
        data-testid="counter-sign-banner"
        data-role={role}
        className="rounded-md border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-900"
      >
        <span data-testid="counter-sign-banner-error">{error}</span>
      </div>
    );
  }

  if (items === null) {
    return (
      <div
        data-testid="counter-sign-banner"
        data-role={role}
        className="rounded-md border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700"
      >
        <span data-testid="counter-sign-banner-loading">Loading pending items…</span>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div
        data-testid="counter-sign-banner"
        data-role={role}
        className="rounded-md border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700"
      >
        <span data-testid="counter-sign-banner-empty">
          No pending rule-change requests {MIDDLE_DOT} {role} console
        </span>
      </div>
    );
  }

  return (
    <div
      data-testid="counter-sign-banner"
      data-role={role}
      className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-900"
    >
      <div
        data-testid="counter-sign-banner-header"
        className="font-medium mb-2"
      >
        {items.length} pending rule-change request{items.length === 1 ? '' : 's'} {MIDDLE_DOT}{' '}
        {role} console
      </div>
      <ul data-testid="counter-sign-banner-list" className="space-y-1 list-none">
        {items.map((item) => (
          <li
            key={item.request_id}
            data-testid={`counter-sign-banner-item-${item.request_id}`}
            className="text-sm"
          >
            {item.rule_class} {MIDDLE_DOT} initiated by {item.initiator_role}{' '}
            {MIDDLE_DOT} state {item.state}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CounterSignBanner;
