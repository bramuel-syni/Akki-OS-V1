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

// Phase 8a-lite (Ask Console) — RMS UI Specification v1 §3 landing.
//
// Primary surface at `/` is the Ask Console (`AskConsolePage`). The
// legacy G5b Operator Console + Consumer Terminal pages are archived
// under `src/legacy/pages/` and remain reachable at `/legacy/*` for
// (a) Trust receipt deep-links from the Ask Console answer surface
// and (b) continuity of the four operator surfaces + consumer trace
// while Phase 8 full rebuilds them against UI Spec v1.
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<AskConsolePage />} />
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
    </BrowserRouter>
  );
}
