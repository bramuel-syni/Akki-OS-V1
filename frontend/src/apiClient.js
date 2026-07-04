import axios from 'axios';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const client = axios.create({ baseURL: API, timeout: 15000 });

export const api = {
  health: () => client.get('/health').then(r => r.data),
  systemState: () => client.get('/system/state').then(r => r.data),
  northenaStatus: () => client.get('/northena/status').then(r => r.data),
  openRuns: () => client.get('/northena/ledger/open_runs').then(r => r.data),
  ledgerByRun: (runId) => client.get(`/northena/ledger/by_run/${runId}`).then(r => r.data),
  traceLens: (traceId) => client.get(`/northena/trace/${traceId}`).then(r => r.data),
  v1Status: () => client.get('/v1/status').then(r => r.data),
  v3Status: () => client.get('/v3/status').then(r => r.data),
  solvaStatus: () => client.get('/solva/status').then(r => r.data),
  service1Status: () => client.get('/service_1/status').then(r => r.data),
  liftManifest: () => client.get('/discipline/lift_manifest').then(r => r.data),
  stampAuditRecent: (limit = 50) => client.get(`/v1/stamp_audit/recent?limit=${limit}`).then(r => r.data),
  contractFiveRings: () => client.get('/contracts/five_rings').then(r => r.data),
  contractQualMatrix: () => client.get('/contracts/qualification_matrix').then(r => r.data),
  // Phase 8a-lite (Ask Console) — v2 dispatch consumer.
  // Backend contract is frozen at ObjectiveRequest_v2 in / (200|422|202|501 body-shape) out.
  // Callers pass the raw ObjectiveRequest_v2 payload; the router discriminates the
  // response envelope by HTTP status (200 = ComposedConclusion_v0 or qualified_data
  // payload dict; 422 = AdmissionRefusal_v0 or Service1Refusal_v0; 202 =
  // AsyncDeliveryAccepted_v0/v1; 503 = infra-not-refusal). We return `{status, body}`
  // so the surface can key on the discriminator per UI Spec §4.2 ("There is no
  // response shape in which the claim is separable from its class").
  dispatchV2: (objectiveRequestV2) =>
    client
      .post('/service_1/v2/dispatch', objectiveRequestV2, {
        // Do NOT throw on 4xx — refusal is a first-class body per A2 doctrine.
        validateStatus: (s) => s >= 200 && s < 500,
      })
      .then((r) => ({ status: r.status, body: r.data })),
};

export default api;
