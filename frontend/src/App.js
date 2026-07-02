import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppShell from './components/AppShell';
import LandingPage from './pages/LandingPage';
import OperatorDashboard from './pages/OperatorDashboard';
import RunsPage from './pages/RunsPage';
import RunDetailPage from './pages/RunDetailPage';
import DisciplinePage from './pages/DisciplinePage';
import EnginesPage from './pages/EnginesPage';
import TraceReceiptPage from './pages/TraceReceiptPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<LandingPage />} />
          <Route path="operator" element={<OperatorDashboard />} />
          <Route path="operator/runs" element={<RunsPage />} />
          <Route path="operator/runs/:runId" element={<RunDetailPage />} />
          <Route path="operator/discipline" element={<DisciplinePage />} />
          <Route path="operator/engines" element={<EnginesPage />} />
          <Route path="trace/:traceId" element={<TraceReceiptPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
