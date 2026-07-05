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
import BuyerShapePage from './pages/buyer/BuyerShapePage';
import BuyerAcquirePage from './pages/buyer/BuyerAcquirePage';
import BuyerReceivePage from './pages/buyer/BuyerReceivePage';
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
          {/* Phase 8 Stage B-3 — Buyer surface (UI Spec §5) */}
          <Route path="buyer/shape" element={<BuyerShapePage />} />
          <Route path="buyer/acquire/:sessionId" element={<BuyerAcquirePage />} />
          <Route path="buyer/receive/:sessionId" element={<BuyerReceivePage />} />
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
