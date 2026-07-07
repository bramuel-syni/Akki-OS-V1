/**
 * UI Spec §6.1 — Master Admin · Home.
 *
 * Verbatim elements per Spec:
 *   * pending banner in plain language ("Two rules are waiting on your
 *     decision before they can take effect." + Review) — plural-aware,
 *     count-substituted (Phase 8 Stage B-4 amendment: real seams-pending
 *     enumeration reads `GET /api/master_admin/pending_seams`).
 *   * prompt "What do you want to do?"
 *   * six action buttons with binding labels:
 *       Assign a role · Change a rule · Manage keys & access ·
 *       Update the taxonomy · Set pricing · Apportion GPU capacity
 *   * footer link "See everything I've changed — every action is recorded."
 *
 * Rules verbatim: buttons and sentences only. No dashboards, no
 * version strings, no config syntax anywhere on this surface.
 */
import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ShieldCheck } from 'lucide-react';
import api from '../../apiClient';
import { useAuth } from '../../hooks/useAuth';
import { CounterSignBanner } from '../../components/ui_spec_v1';

const ACTION_BUTTONS = [
  { id: 'assign-a-role', label: 'Assign a role', target: '/master-admin/change-a-rule/tier-lock' },
  { id: 'change-a-rule', label: 'Change a rule', target: '/master-admin/change-a-rule/tier-lock' },
  { id: 'manage-keys-and-access', label: 'Manage keys & access', target: '/master-admin/change-a-rule/tier-lock' },
  { id: 'update-the-taxonomy', label: 'Update the taxonomy', target: '/master-admin/change-a-rule/tier-lock' },
  { id: 'set-pricing', label: 'Set pricing', target: '/master-admin/change-a-rule/tier-lock' },
  { id: 'apportion-gpu-capacity', label: 'Apportion GPU capacity', target: '/master-admin/change-a-rule/tier-lock' },
];

function pluralPendingCopy(n) {
  if (n === 1) return 'One rule is waiting on your decision before it can take effect.';
  const words = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'];
  const word = n < words.length ? words[n] : String(n);
  return `${word} rules are waiting on your decision before they can take effect.`;
}

export default function MasterAdminHomePage() {
  const { identity } = useAuth();
  const navigate = useNavigate();
  const [pendingCount, setPendingCount] = useState(null);

  const loadPending = useCallback(async () => {
    const r = await api.masterAdminPendingSeams();
    if (r.status === 200) {
      setPendingCount(r.body.count || 0);
    } else {
      setPendingCount(0);
    }
  }, []);

  useEffect(() => {
    if (identity === null) return;
    if (identity === false) {
      navigate('/auth/login', { replace: true });
      return;
    }
    loadPending();
  }, [identity, navigate, loadPending]);

  if (identity === null) {
    return (
      <div className="min-h-screen bg-rms-canvas text-rms-ink flex items-center justify-center">
        <div className="text-rms-mute">Loading…</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-rms-canvas text-rms-ink" data-testid="master-admin-home-page">
      <header className="border-b border-rms-line bg-white">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="p-1 hover:bg-rms-highlight rounded"
              data-testid="master-admin-nav-back"
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <div>
              <div className="text-xs text-rms-mute uppercase tracking-wide">RMS Intelligence · master admin</div>
              <h1 className="text-lg font-semibold">Home</h1>
            </div>
          </div>
          <ShieldCheck className="w-5 h-5 text-rms-mute" />
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8 space-y-8">
        {/* Phase 8 Seam 3 Sub-stage 3 — CounterSignBanner (Owner Ruling 2,
            Amendment G, 2026-07-07: capacity-role render). */}
        <CounterSignBanner
          role="admin"
          token={identity?.token || localStorage.getItem('rms_auth_token') || ''}
        />
        {/* §6.1 Pending banner — plural-aware, count-substituted, plain language. */}
        {pendingCount != null && pendingCount > 0 && (
          <section
            className="border border-amber-200 bg-amber-50 rounded-md p-4 flex items-start justify-between gap-3"
            data-testid="master-admin-pending-banner"
          >
            <p className="text-sm text-amber-900" data-testid="master-admin-pending-copy">
              {pluralPendingCopy(pendingCount)}
            </p>
            <button
              type="button"
              onClick={() => navigate('/master-admin/change-a-rule/tier-lock')}
              className="px-3 py-1 rounded bg-amber-900 text-white text-sm font-medium"
              data-testid="master-admin-pending-review"
            >
              Review
            </button>
          </section>
        )}
        {pendingCount === 0 && (
          <section
            className="text-sm text-rms-mute italic"
            data-testid="master-admin-pending-empty"
          >
            Nothing is waiting on your decision.
          </section>
        )}

        {/* §6.1 Prompt. */}
        <section>
          <p className="text-base font-medium" data-testid="master-admin-prompt">
            What do you want to do?
          </p>
        </section>

        {/* §6.1 Six action buttons — binding labels VERBATIM. */}
        <section
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3"
          data-testid="master-admin-actions"
        >
          {ACTION_BUTTONS.map((b) => (
            <button
              key={b.id}
              type="button"
              onClick={() => navigate(b.target)}
              className="px-4 py-3 rounded border border-rms-line bg-white text-left text-sm font-medium text-rms-ink hover:bg-rms-highlight"
              data-testid={`master-admin-action-${b.id}`}
            >
              {b.label}
            </button>
          ))}
        </section>

        {/* §6.1 Footer link VERBATIM. */}
        <footer className="border-t border-rms-line pt-4 text-sm">
          <button
            type="button"
            onClick={() => navigate('/master-admin/audit-trail')}
            className="underline text-rms-mute hover:text-rms-ink"
            data-testid="master-admin-audit-footer-link"
          >
            See everything I&apos;ve changed — every action is recorded.
          </button>
        </footer>
      </main>
    </div>
  );
}
