"""Outer-gate ride + Ruling 3 wire-shape gates — Phase 4a.

Houses:
  * Gate 8 — `test_qualified_data_outer_gate_ride_receipt_unchanged`.
    Condition B3: outer_gate/{transform,mint,receipt}.py SHA-untouched;
    OuterGateReceipt@v0 schema unchanged.
  * Gate 12 — `test_qualified_data_wire_shape_pins_governance_keys`.
    Ruling 3 (Owner acceptance, Phase 4a Stage B dispatch, 2026-07-03):
    LOAD-BEARING wire-shape gate — top-level `units`/`receipt`/
    `unit_count` present; `receipt` parses as
    `OuterGateReceipt_v0.model_validate(...)`; every unit carries its
    `defensibility` field.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
import pytest
from httpx import ASGITransport

from contracts.mtafiti_registry import MTAFITI_REGISTRY_COLLECTION
from contracts.outer_gate_receipt import OuterGateReceipt
from core import db
from server import app


BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent  # /app/backend


# Pre-Phase-4a canonical SHA-256s of the three outer-gate files.
# Condition B3 asserts these stay byte-identical.
#
# Note (Fixture Refresh 2026-07-10 · FR-E2 α re-bless): the
# `services/outer_gate/transform.py` SHA was re-blessed at Fixture
# Refresh close per Owner ruling FR-E2 α condition 2 (distributed
# tables DELETED not shadowed — `_FEED_ID_BUCKET` removed, feed_id
# generalisation now reads from centralized
# `services/service_1/license_classes.v1.json`). Mint.py + receipt.py
# preserved byte-identical. The gate's intent (guard against
# unauthorized outer-gate reinvention) unchanged; only the pinned
# transform.py SHA is refreshed with disclosure. See
# `/app/docs/close_reports/fixture_refresh.md` §Rebless-Log.
OUTER_GATE_PRE_4A_SHA = {
    "services/outer_gate/transform.py": (
        "bb8ec05d1e24fefe42c437e73c66a803c1ab3b712bdd983ffe5a44181c95228b"
    ),
    "services/outer_gate/mint.py": (
        "01cfe0e0fe8762e4b4c0421db89668f7eb88e3a3caf9eae57719ad496129ebbf"
    ),
    "services/outer_gate/receipt.py": (
        "4591e5ff6834fc80e359a33b7ccd1faad88fa8980a62f687ad1976a0342e9348"
    ),
}


# Pre-Phase-4a canonical SHA of the OuterGateReceipt schema snapshot.
OUTER_GATE_RECEIPT_SNAPSHOT_SHA = None  # computed dynamically to avoid brittleness


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


async def _clear_registry() -> None:
    await db[MTAFITI_REGISTRY_COLLECTION].delete_many({})


async def _seed_row(
    *, source_ref: str, region: str, feed_id: str, klass: str,
) -> None:
    logged = (datetime.now(timezone.utc) - timedelta(days=0)).isoformat()
    await db[MTAFITI_REGISTRY_COLLECTION].insert_one({
        "source_ref": source_ref,
        "region": region,
        "feed_id": feed_id,
        "sensitivity": "standard",
        "defensibility_measure": {
            "source_standing": "accountable",
            "attachment": 0.0,
            "corroboration": 0.0,
            "recency_validity": 0.5,
            "contested": False,
        },
        "defensibility_runtime_mode": "declaration_baseline",
        "matrix_rule_ref": "qm.v0.rule.1",
        "defensibility_class": klass,
        "freshness_stamp": {
            "logged_date": logged,
            "structural_signature": None,
        },
    })


def _warm_success_body(*, scope_refs, commissioner: str = "operator_internal") -> dict:
    return {
        "entry": "external_request",
        "reach": {"scope_refs": scope_refs, "exclusions": [], "depth": "baseline"},
        "output": {
            "form": "qualified_data",
            "consumer": "person",
            "grain": "per_claim",
            "standard": {"minimum_class": "utterance"},
        },
        "envelope": {
            "lawful_basis": "test",
            "done_condition": "test",
            "budget": "test",
            "scope_ceiling": "test",
            "commissioner": commissioner,
            "committed_at": "2026-07-03T12:00:00+00:00",
        },
    }


# ---------------------------------------------------------------------------
# Gate 8 — outer-gate ride, files & receipt shape unchanged (Condition B3)
# ---------------------------------------------------------------------------


def test_qualified_data_outer_gate_ride_receipt_unchanged():
    """v0 outer_gate/{transform,mint,receipt}.py SHA-untouched;
    OuterGateReceipt@v0 schema unchanged (canonical snapshot
    byte-identical).
    """
    for rel_path, expected_sha in OUTER_GATE_PRE_4A_SHA.items():
        p = BACKEND_ROOT / rel_path
        actual = _sha256(p)
        assert actual == expected_sha, (
            f"Condition B3 violation — {rel_path} mutated during Phase 4a.\n"
            f"  pre-Phase-4a SHA: {expected_sha}\n"
            f"  post-Phase-4a SHA: {actual}\n"
            f"Outer-gate MUST be extended, not reinvented."
        )
    # Frozen contract snapshot for OuterGateReceipt unchanged.
    live_schema = OuterGateReceipt.model_json_schema()
    import json
    stored = json.loads(
        (BACKEND_ROOT / "tests" / "invariants" / "outer_gate_receipt.contract_snapshot.json"
         ).read_text(encoding="utf-8")
    )
    assert live_schema == stored, (
        "OuterGateReceipt@v0 schema drift during Phase 4a — Condition B3 "
        "violated. Snapshot MUST stay byte-identical."
    )


# ---------------------------------------------------------------------------
# Gate 12 (Ruling 3 wire-shape) — LOAD-BEARING
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_qualified_data_wire_shape_pins_governance_keys():
    """LOAD-BEARING — Ruling 3 (Owner, 2026-07-03).

    Container refactor that drops or renests `receipt` ships a
    deliverable without its outer-gate receipt: governance regression
    with no snapshot to catch it. This gate pins the container's
    governance-carrying keys so §6.1 payload UNFROZEN posture is
    honest: three top-level keys present, `receipt` parses as
    `OuterGateReceipt_v0`, every unit carries `defensibility`.
    """
    await _clear_registry()
    await _seed_row(
        source_ref="s://w/a.raw", region="wire_region",
        feed_id="feed_a", klass="fact",
    )
    await _seed_row(
        source_ref="s://w/b.raw", region="wire_region",
        feed_id="feed_a", klass="utterance",
    )

    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/service_1/v2/dispatch",
            json=_warm_success_body(scope_refs=["wire_region"]),
        )
    assert resp.status_code == 200, resp.text
    body = resp.json()

    # Ruling 3 governance-carrying keys — all three present at top level.
    for key in ("units", "receipt", "unit_count"):
        assert key in body, (
            f"Ruling 3 wire-shape violation — top-level key {key!r} "
            f"missing from qualified-data payload body: {sorted(body.keys())}"
        )

    # `receipt` parses as OuterGateReceipt_v0 exactly.
    receipt_obj = OuterGateReceipt.model_validate(body["receipt"])
    assert receipt_obj.transform_version == "hmac-sha256-v1"
    assert len(receipt_obj.key_fingerprint) == 64
    assert receipt_obj.run_id.startswith("qd-run-")

    # Every unit carries its `defensibility` field.
    assert isinstance(body["units"], list)
    assert body["unit_count"] == len(body["units"])
    for i, unit in enumerate(body["units"]):
        assert "defensibility" in unit, (
            f"Ruling 3 wire-shape violation — units[{i}] missing "
            f"`defensibility` field:\n{unit}"
        )
        assert isinstance(unit["defensibility"], dict)
        assert "defensibility_class" in unit["defensibility"]
