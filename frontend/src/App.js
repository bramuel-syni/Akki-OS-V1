import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AskConsolePage from './pages/AskConsolePage';
import AppShell from './components/AppShell';
import LandingPage from './legacy/pages/LandingPage';
import OperatorDashboard from './legacy/pages/OperatorDashboard';
import RunsPage from './legacy/pages/RunsPage';
import RunDetailPage from './legacy/pages/RunDetailPage';
import DisciplinePage from './legacy/pages/DisciplinePage';
import EnginesPage from './legacy/pages/EnginesPage';
import TraceReceiptPage from './legacy/pages/TraceReceiptPage';
import ComposePage from './legacy/pages/ComposePage';
import AuthLoginPage from './pages/AuthLoginPage';
import AuthRegisterPage from './pages/AuthRegisterPage';
import OperatorHomePage from './pages/operator/OperatorHomePage';
import CommissionWizardPage from './pages/operator/CommissionWizardPage';
import CommitReviewPage from './pages/operator/CommitReviewPage';
import EngineerRegisterAppPage from './pages/engineer/EngineerRegisterAppPage';
import EngineerFirstCallPage from './pages/engineer/EngineerFirstCallPage';
import EngineerAdministerPage from './pages/engineer/EngineerAdministerPage';
// Commercial-cut 2026-07-06 (BCR v1.4 §12): buyer §5 surface (BuyerShape/
// Acquire/Receive) cut whole — buyer wizard variant is not built on this
// tree post-cut. Salvage location:
//   /app/salvage/commercial_cut_2026_07_06/frontend/pages/
import MasterAdminHomePage from './pages/master_admin/MasterAdminHomePage';
import ChangeARulePage from './pages/master_admin/ChangeARulePage';
import AuditTrailPage from './pages/master_admin/AuditTrailPage';
// Phase 8 Stage B-5a — Compliance Console (UI Spec v2.1 §4).
import ComplianceHomePage from './pages/compliance/ComplianceHomePage';
import ComplianceProveOneRunPage from './pages/compliance/ComplianceProveOneRunPage';
import ComplianceRetentionRightsPage from './pages/compliance/ComplianceRetentionRightsPage';
import { AuthProvider } from './hooks/useAuth';

// Phase 8 Stage B-1 — Auth landing (Owner E1 ratified: custom JWT + bcrypt).
// The AuthProvider wraps the entire tree so any surface can call useAuth().
// Ask Console remains the primary surface at `/`; auth surface at `/auth/*`.
// Legacy G5b operator pages remain nested under `/legacy/*` for continuity.
export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route index element={<AskConsolePage />} />
          <Route path="auth/login" element={<AuthLoginPage />} />
          <Route path="auth/register" element={<AuthRegisterPage />} />
          {/* Phase 8 Stage B-2 — Operator surface (UI Spec §2) */}
          <Route path="operator" element={<OperatorHomePage />} />
          <Route path="operator/commission" element={<CommissionWizardPage />} />
          <Route path="operator/commit-review/:sessionId" element={<CommitReviewPage />} />
          {/* Phase 8 Stage B-3 — Engineer surface (UI Spec §4) */}
          <Route path="engineer/register" element={<EngineerRegisterAppPage />} />
          <Route path="engineer/first-call" element={<EngineerFirstCallPage />} />
          <Route path="engineer/administer" element={<EngineerAdministerPage />} />
          {/* Phase 8 Stage B-3 — Buyer surface (UI Spec §5) CUT at
              commercial cut 2026-07-06 (BCR v1.4 §12); no live routes. */}
          {/* Phase 8 Stage B-4 — Master Admin surface (UI Spec §6) */}
          <Route path="master-admin" element={<MasterAdminHomePage />} />
          <Route path="master-admin/change-a-rule/:ruleId" element={<ChangeARulePage />} />
          <Route path="master-admin/audit-trail" element={<AuditTrailPage />} />
          {/* Phase 8 Stage B-5a — Compliance Console (UI Spec v2.1 §4) */}
          <Route path="compliance" element={<ComplianceHomePage />} />
          <Route path="compliance/prove" element={<ComplianceProveOneRunPage />} />
          <Route path="compliance/prove/:traceId" element={<ComplianceProveOneRunPage />} />
          <Route path="compliance/retention" element={<ComplianceRetentionRightsPage />} />
          {/* Legacy G5b surfaces — nested under /legacy/* (Phase 8a-lite archival) */}
          <Route path="legacy" element={<AppShell />}>
            <Route index element={<LandingPage />} />
            <Route path="operator" element={<OperatorDashboard />} />
            <Route path="operator/runs" element={<RunsPage />} />
            <Route path="operator/runs/:runId" element={<RunDetailPage />} />
            <Route path="operator/discipline" element={<DisciplinePage />} />
            <Route path="operator/engines" element={<EnginesPage />} />
            <Route path="operator/compose" element={<ComposePage />} />
            <Route path="trace/:traceId" element={<TraceReceiptPage />} />
          </Route>
          {/* Anything else falls back to the Ask Console (single ingress per UI Spec §3.1). */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
