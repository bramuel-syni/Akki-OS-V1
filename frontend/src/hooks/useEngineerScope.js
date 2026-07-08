// Phase 8-EXT — shared engineer-scope hook (P8E-E2 α, 2026-07-08).
// P8E-E5 α: `engineer` is the internal identifier; only `external_engineer` is the added role.
// UI Spec v2.1 §5.4 line 102 verbatim: "Two roles, one console, identical screens,
// different scope — enforcement server-side, never view-layer filtering alone."
import { useMemo } from 'react';

export default function useEngineerScope(identity) {
  return useMemo(() => {
    const roles = new Set(identity?.roles || []);
    const isExternal = roles.has('external_engineer')
      && !roles.has('engineer') && !roles.has('admin') && !roles.has('master_admin');
    const ownEmail = (identity?.email || '').toLowerCase();
    const scopeFilter = (resource) => {
      if (!isExternal) return true; // internal authority → full scope
      const owner = (resource?.grantee_email || '').toLowerCase();
      return owner === ownEmail;
    };
    return { isExternal, ownEmail, scopeFilter };
  }, [identity]);
}
