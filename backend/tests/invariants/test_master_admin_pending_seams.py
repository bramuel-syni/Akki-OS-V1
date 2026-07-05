"""Phase 8 Stage B-4 — §6.1 pending-seams enumeration gates.

Owner amendment verbatim (2026-07-05):
    "The system already HAS real pending decisions — the gated-closed
     seams awaiting owner/DPO/MEA values. Five exist today: Targeta
     yield thresholds, Mtafiti V3 thresholds, retention window,
     cumulative-disclosure envs, MEA source-standing table. That is
     literally what the approved §6.1 mockup rendered."

Endpoint under test: `GET /api/master_admin/pending_seams`.
Data source: env presence + config presence per seam (NO database
queue backend; the seams ARE the data).

Gates:
  * All five seams enumerated when their env vars are absent (baseline
    test setup — env pruned).
  * Each seam entry carries the fields {seam_id, plain_language_line,
    awaiting_whom, seam_status="closed"}.
  * `count` matches `len(pending_seams)`.
  * Setting an env var closes (removes-from-pending) a seam.
  * Master-admin auth required (401 unauthenticated).
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from server import app
from services.master_admin.pending_seams import enumerate_pending_seams


ADMIN_EMAIL = "admin@rms.example.com"
ADMIN_PASSWORD = "admin-b1-test-pw"

EXPECTED_SEAM_IDS_BASELINE = {
    "targeta_yield_thresholds",
    "mtafiti_v3_thresholds",
    "northena_retention_window",
    "v2_cumulative_disclosure_envs",
    "mea_source_standing_table",
}


async def _login_admin(client: AsyncClient) -> str:
    resp = await client.post(
        "/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_pending_seams_endpoint_enumerates_all_five_seams_at_baseline(monkeypatch):
    """With no gating env vars set, all five seams are pending."""
    for env_var in (
        "RMS_TARGETA_MIN_EFFICIENCY_GAIN",
        "RMS_TARGETA_COVERAGE_ALPHA",
        "RMS_TARGETA_HELD_OUT_SET_COMPOSITION",
        "RMS_MTAFITI_V3_FACT_PRECISION",
        "RMS_MTAFITI_V3_GENRE_ACCURACY",
        "RMS_MTAFITI_V3_INTER_ANNOTATOR_FLOOR",
        "RMS_NORTHENA_LEDGER_RETENTION_MODE",
        "RMS_G6_K_ANONYMITY_THRESHOLD",
        "RMS_G6_L_DIVERSITY_THRESHOLD",
        "RMS_G6_DP_EPSILON_BUDGET",
        "RMS_MEA_SOURCE_STANDING_TABLE_PATH",
    ):
        monkeypatch.delenv(env_var, raising=False)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        token = await _login_admin(client)
        resp = await client.get(
            "/api/master_admin/pending_seams",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["count"] == 5
    seam_ids = {s["seam_id"] for s in body["pending_seams"]}
    assert seam_ids == EXPECTED_SEAM_IDS_BASELINE, (
        f"Expected exactly 5 seams at baseline, got {seam_ids!r}."
    )
    for seam in body["pending_seams"]:
        assert set(seam.keys()) >= {"seam_id", "plain_language_line", "awaiting_whom", "seam_status"}
        assert seam["seam_status"] == "closed"
        assert seam["awaiting_whom"] in {"owner", "dpo", "mea"}


def test_enumerate_pending_seams_pure_function_baseline(monkeypatch):
    """Pure-fn contract — five seams at baseline."""
    for env_var in (
        "RMS_TARGETA_MIN_EFFICIENCY_GAIN",
        "RMS_TARGETA_COVERAGE_ALPHA",
        "RMS_TARGETA_HELD_OUT_SET_COMPOSITION",
        "RMS_MTAFITI_V3_FACT_PRECISION",
        "RMS_MTAFITI_V3_GENRE_ACCURACY",
        "RMS_MTAFITI_V3_INTER_ANNOTATOR_FLOOR",
        "RMS_NORTHENA_LEDGER_RETENTION_MODE",
        "RMS_G6_K_ANONYMITY_THRESHOLD",
        "RMS_G6_L_DIVERSITY_THRESHOLD",
        "RMS_G6_DP_EPSILON_BUDGET",
        "RMS_MEA_SOURCE_STANDING_TABLE_PATH",
    ):
        monkeypatch.delenv(env_var, raising=False)
    seams = enumerate_pending_seams()
    assert len(seams) == 5
    assert {s["seam_id"] for s in seams} == EXPECTED_SEAM_IDS_BASELINE


def test_enumerate_pending_seams_closes_targeta_when_all_three_env_vars_set(monkeypatch):
    """Setting the three targeta env vars removes the seam from pending."""
    for env_var in ("RMS_MTAFITI_V3_FACT_PRECISION", "RMS_MTAFITI_V3_GENRE_ACCURACY",
                    "RMS_MTAFITI_V3_INTER_ANNOTATOR_FLOOR", "RMS_G6_K_ANONYMITY_THRESHOLD",
                    "RMS_G6_L_DIVERSITY_THRESHOLD", "RMS_G6_DP_EPSILON_BUDGET",
                    "RMS_NORTHENA_LEDGER_RETENTION_MODE",
                    "RMS_MEA_SOURCE_STANDING_TABLE_PATH"):
        monkeypatch.delenv(env_var, raising=False)
    monkeypatch.setenv("RMS_TARGETA_MIN_EFFICIENCY_GAIN", "0.15")
    monkeypatch.setenv("RMS_TARGETA_COVERAGE_ALPHA", "0.90")
    monkeypatch.setenv("RMS_TARGETA_HELD_OUT_SET_COMPOSITION", "genre_stratified_10")
    seams = enumerate_pending_seams()
    seam_ids = {s["seam_id"] for s in seams}
    assert "targeta_yield_thresholds" not in seam_ids, (
        "Setting all three targeta env vars must close the seam."
    )


def test_enumerate_pending_seams_partial_env_keeps_seam_pending(monkeypatch):
    """If only some env vars land, seam stays pending (all-or-nothing)."""
    for env_var in ("RMS_TARGETA_COVERAGE_ALPHA", "RMS_TARGETA_HELD_OUT_SET_COMPOSITION",
                    "RMS_MTAFITI_V3_FACT_PRECISION", "RMS_MTAFITI_V3_GENRE_ACCURACY",
                    "RMS_MTAFITI_V3_INTER_ANNOTATOR_FLOOR",
                    "RMS_G6_K_ANONYMITY_THRESHOLD", "RMS_G6_L_DIVERSITY_THRESHOLD",
                    "RMS_G6_DP_EPSILON_BUDGET",
                    "RMS_NORTHENA_LEDGER_RETENTION_MODE",
                    "RMS_MEA_SOURCE_STANDING_TABLE_PATH"):
        monkeypatch.delenv(env_var, raising=False)
    monkeypatch.setenv("RMS_TARGETA_MIN_EFFICIENCY_GAIN", "0.15")
    seams = enumerate_pending_seams()
    seam_ids = {s["seam_id"] for s in seams}
    assert "targeta_yield_thresholds" in seam_ids, (
        "Partial env var landing must NOT close the seam."
    )


def test_enumerate_pending_seams_retention_mode_indefinite_stays_pending(monkeypatch):
    """The retention seam is pending when mode is `indefinite`
    (the current unset-decision default) and closed otherwise."""
    monkeypatch.setenv("RMS_NORTHENA_LEDGER_RETENTION_MODE", "indefinite")
    seams = enumerate_pending_seams()
    assert "northena_retention_window" in {s["seam_id"] for s in seams}
    monkeypatch.setenv("RMS_NORTHENA_LEDGER_RETENTION_MODE", "P30D")
    seams = enumerate_pending_seams()
    assert "northena_retention_window" not in {s["seam_id"] for s in seams}


def test_enumerate_pending_seams_ordering_matches_mockup_precedent(monkeypatch):
    """Ordering: Targeta → Mtafiti → Retention → Cumulative-disclosure → MEA."""
    for env_var in (
        "RMS_TARGETA_MIN_EFFICIENCY_GAIN", "RMS_TARGETA_COVERAGE_ALPHA",
        "RMS_TARGETA_HELD_OUT_SET_COMPOSITION",
        "RMS_MTAFITI_V3_FACT_PRECISION", "RMS_MTAFITI_V3_GENRE_ACCURACY",
        "RMS_MTAFITI_V3_INTER_ANNOTATOR_FLOOR",
        "RMS_NORTHENA_LEDGER_RETENTION_MODE",
        "RMS_G6_K_ANONYMITY_THRESHOLD", "RMS_G6_L_DIVERSITY_THRESHOLD",
        "RMS_G6_DP_EPSILON_BUDGET",
        "RMS_MEA_SOURCE_STANDING_TABLE_PATH",
    ):
        monkeypatch.delenv(env_var, raising=False)
    seams = enumerate_pending_seams()
    ordered_ids = [s["seam_id"] for s in seams]
    assert ordered_ids == [
        "targeta_yield_thresholds",
        "mtafiti_v3_thresholds",
        "northena_retention_window",
        "v2_cumulative_disclosure_envs",
        "mea_source_standing_table",
    ]
