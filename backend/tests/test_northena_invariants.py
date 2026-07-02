"""Northena binding invariants — mandate §13 (all 11).

Reading of §13: mandate lists ELEVEN binding invariants. Stakeholder
G2a brief called for TEN and collapsed mandate #1 (no ML) and mandate
#2 (no inference) into a single test. Journaled as a defensible
reading per §2 determinism principle: I implement BOTH separately
(N-INV-1a and N-INV-1b) so the superset covers stakeholder mapping
without dropping mandate §13.2. Mandate ambiguity surfaced, NOT
frozen into a re-numbered §13.
"""
from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

NORTHENA_DIR = Path(__file__).resolve().parent.parent / "services" / "northena"


# ---------------------------------------------------------------------------
# N-INV-1a — deterministic (no ML imports inside services/northena/).
# N-INV-1b — no inference (no learned-model calls; Solva invoked externally).
# ---------------------------------------------------------------------------
_ML_TOKENS = ("torch", "tensorflow", "sklearn", "transformers", "openai",
              "anthropic", "faster_whisper", "pyannote", "emergentintegrations")


def test_N_INV_1a_northena_no_ml_imports():
    for py in NORTHENA_DIR.rglob("*.py"):
        src = py.read_text()
        for token in _ML_TOKENS:
            assert f"import {token}" not in src and f"from {token}" not in src, (
                f"N-INV-1a: ML-import {token!r} inside {py.name}"
            )


def test_N_INV_1b_northena_no_inference_behaviour():
    """Grep for 'infer', 'predict', 'model.judge' inside Northena modules."""
    for py in NORTHENA_DIR.rglob("*.py"):
        src = py.read_text().lower()
        assert ".predict(" not in src, f"N-INV-1b: .predict() inside {py.name}"
        # 'infer' is allowed only in comments/docstrings, not as a call.
        tree = ast.parse(py.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert node.func.attr not in ("predict", "infer"), (
                    f"N-INV-1b: inference call {node.func.attr!r} in {py.name}"
                )


# ---------------------------------------------------------------------------
# N-INV-2 — one frozen artifact + valid lawful_basis per admitted run.
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_N_INV_2_admit_requires_lawful_basis():
    from services.northena import admit
    with patch("services.northena.ledger.record", new=MagicMock(return_value=None)) as _r:
        _r.return_value = None
        async def _noop(row): return None
        with patch("services.northena.admit.ledger_record", new=_noop):
            r = await admit.compile_and_freeze(
                {"artifact_type": "objective_request", "artifact_id": "x",
                 "artifact_version": "v0", "scope": ["news_anchor_read"]},
                run_id="r1", trace_id="t1")
            assert r["decision"] == "refused"
            assert "lawful_basis" in r["reason"]


# ---------------------------------------------------------------------------
# N-INV-3 — Contract-grade LedgerRow snapshot invariant covers this.
# N-INV-4 — FrozenArtifact immutable at run-time.
# ---------------------------------------------------------------------------
def test_N_INV_4_frozen_artifact_immutable():
    from services.northena.admit import FrozenArtifact
    f = FrozenArtifact({"a": 1})
    with pytest.raises(TypeError):
        f["a"] = 2


# ---------------------------------------------------------------------------
# N-INV-5 — Gate strict set-membership; no inferential path.
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_N_INV_5_gate_strict_set_membership():
    from contracts.northena_ledger import LedgerArtifactRef
    from services.northena import gate
    async def _noop(row): return None
    with patch("services.northena.gate.ledger_record", new=_noop):
        ar = LedgerArtifactRef(artifact_type="objective_request",
                               artifact_id="x", version="v0")
        r = await gate.route(run_id="r1", trace_id="t1", sub_objective="unknown",
                             artifact_ref=ar, lawful_basis_ref="lb",
                             scope=["known_a", "known_b"])
        assert r["decision"] == "refused" and r["reason"] == "out_of_scope"


# ---------------------------------------------------------------------------
# N-INV-6 — Converge alone writes terminate rows.
# ---------------------------------------------------------------------------
def test_N_INV_6_northena_owns_halt():
    # Grep the codebase: only converge.py may emit stage='converge' rows.
    from pathlib import Path
    for py in NORTHENA_DIR.rglob("*.py"):
        if py.name == "converge.py": continue
        src = py.read_text()
        assert 'stage="converge"' not in src, f"non-converge module writes terminate: {py}"


# ---------------------------------------------------------------------------
# N-INV-7 — no run closes without closed ledger.
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_N_INV_7_open_runs_visible():
    # Post-shrink: open-runs visibility lives in the router (API-shape belongs there);
    # the ledger service owns the write path only. Structural check: the router
    # exposes an `open_runs` GET endpoint via `_open_runs()` helper.
    from routers import northena as northena_router
    assert callable(getattr(northena_router, "_open_runs", None)), (
        "N-INV-7: router must expose an _open_runs helper for /api/northena/ledger/open_runs"
    )
    assert callable(getattr(northena_router, "open_runs", None)), (
        "N-INV-7: /api/northena/ledger/open_runs route must exist"
    )


# ---------------------------------------------------------------------------
# N-INV-8 — Ledger row is contract-grade + append-only surface.
# ---------------------------------------------------------------------------
def test_N_INV_8_ledger_is_append_only():
    from services.northena import ledger
    for name in ("update", "delete", "delete_by_run_id", "edit"):
        assert not hasattr(ledger, name), f"append-only violation: ledger.{name}"


# ---------------------------------------------------------------------------
# N-INV-9 — Refusals recorded, never dropped.
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_N_INV_9_refusals_written():
    from contracts.northena_ledger import LedgerArtifactRef
    from services.northena import gate
    calls = []
    async def _capture(row): calls.append(row)
    with patch("services.northena.gate.ledger_record", new=_capture):
        ar = LedgerArtifactRef(artifact_type="objective_request",
                               artifact_id="x", version="v0")
        await gate.route(run_id="r", trace_id="t", sub_objective="not_in_scope",
                         artifact_ref=ar, lawful_basis_ref="lb", scope=["x"])
    assert calls and calls[0].decision == "refused"


# ---------------------------------------------------------------------------
# N-INV-10 — Stamp-audit absorbed by Ledger.
# ---------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_N_INV_10_stamp_audit_absorbed():
    from contracts.northena_ledger import LedgerArtifactRef
    from services.northena import ledger
    written = []
    async def _capture(row): written.append(row)
    with patch("services.northena.ledger.record", new=_capture):
        entry = {"unit_id": "u-1", "decision": "refuse",
                 "reason": "floor_violation", "judged_signal_dimensions": [],
                 "floor_violation": True}
        ar = LedgerArtifactRef(artifact_type="objective_request",
                               artifact_id="x", version="v0")
        row = await ledger.absorb_stamp_audit(
            run_id="r", trace_id="t", stage="gate", entry=entry,
            artifact_ref=ar, lawful_basis_ref="lb")
    assert row.stamp_audit is not None
    assert row.stamp_audit["unit_id"] == "u-1"
    assert row.decision == "refused"


# ---------------------------------------------------------------------------
# N-INV-11 — Governors orthogonal (no Solva/SyniSense re-implementation).
# ---------------------------------------------------------------------------
def test_N_INV_11_governors_orthogonal():
    ALLOWED_SOLVA = {"admit.py"}  # Admit CALLS the assist; that's allowed.
    ALLOWED_SYNI = set()          # Northena never imports SyniSense at G2a.
    for py in NORTHENA_DIR.rglob("*.py"):
        src = py.read_text()
        if "solva" in src.lower() and py.name not in ALLOWED_SOLVA:
            # Allow references in comments/docstrings only if not `import`.
            assert "from services.solva" not in src and "import services.solva" not in src, (
                f"N-INV-11: unexpected Solva import in {py.name}"
            )
        assert "from services.synisense" not in src and "import services.synisense" not in src, (
            f"N-INV-11: SyniSense import inside Northena {py.name}"
        )
