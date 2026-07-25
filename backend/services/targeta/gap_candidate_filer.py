"""Targeta gap-candidate filer — A3.4 EAB-2 landing (2026-07-24).

Files coverage-gap descriptors as demand-signal records on Targeta's
planning inputs. **This is NOT a cap-seat contact** — eligibility wall
stands per `docs/stage_a_proposals/eab_2_stage_a.md` §1.2 discipline:
*"Filing is demand signal, not authorization: extraction of filed gaps
happens only under normally-governed objectives — the eligibility wall
stands; learning/demand may reorder, never widen."*

Idempotency contract (Owner ruling composition ε + α + γ · Locus 2 = α):
  * Key: `(estate_region, period, source_class)` tuple.
  * Second identical ask returns the same `filed_candidate_id` — no
    duplicate filing per AC-A3.b.
  * Filed record carries `estimated_effort` derived at file-time;
    Prove issues a companion GET against this record at render time
    per Owner ruling Locus 2 = α (envelope does NOT carry
    `estimated_effort`).

Companion-read failure-mode binding (Owner ruling §2):
  If companion GET fails / times out / returns empty, Prove renders the
  coverage_gap refusal without the effort line, in refusal styling.
  NEVER degrades to fault surface, NEVER converts to something-broke.
  This module raises `GapCandidateNotFound` on unknown FK; caller MUST
  treat as "companion channel down" and render refusal without effort
  line — asserted by `test_gap_candidate_companion_channel_down.py`.

Registry attachment:
  * `PROM-S1-frozen-wire-contract` (idempotent record shape)
  * `PROM-S1-honesty-grammar-source-labels` (registry-vocabulary only)
  * `akki.targeta.a3_gap_candidate_filing_idempotent_demand_signal`
    (R4 sidecar row 7)
  * `akki.targeta.a3_gap_candidate_no_cap_seat_contact_ast_negative`
    (R4 sidecar row 8 · AST-enforced no import from eligibility modules)

Sanction: `docs/rulings/eab_2_hazard_stop_a_ruling_2026_07_24.md`
(SHA `8b074dc152b41ed300d5a7626a2a1bd5aa1213371f6eeeac0a096e12f2d6d4a5`).
"""
from __future__ import annotations

import hashlib
import threading
from dataclasses import dataclass, field
from typing import Dict, Optional


class GapCandidateNotFound(Exception):
    """Raised on companion GET against unknown `filed_candidate_id`.

    Caller MUST treat as "companion channel down" and render refusal
    without effort line (Owner ruling §2 failure-mode binding).
    """


@dataclass(frozen=True)
class GapCandidate:
    """Demand-signal-side record on Targeta's planning inputs.

    NOT an eligibility widener. NOT a cap-seat contact. See §1.2 in
    `docs/stage_a_proposals/eab_2_stage_a.md`.
    """

    filed_candidate_id: str
    estate_region: str
    period: str
    source_class: str
    estimated_effort: str  # human-readable, e.g. "≈ 3 days" or "1-2 weeks"


@dataclass
class _GapCandidateStore:
    """In-memory idempotent store keyed by `(estate_region, period, source_class)` tuple."""

    _by_id: Dict[str, GapCandidate] = field(default_factory=dict)
    _by_tuple: Dict[tuple, str] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)


_STORE = _GapCandidateStore()


def _derive_candidate_id(estate_region: str, period: str, source_class: str) -> str:
    """Deterministic FK derivation for idempotency per `(estate_region, period, source_class)`."""
    material = f"{estate_region}|{period}|{source_class}".encode("utf-8")
    return "OBJ-" + hashlib.sha256(material).hexdigest()[:16].upper()


def file_gap_candidate(
    estate_region: str,
    period: str,
    source_class: str,
    estimated_effort: str,
) -> GapCandidate:
    """File a coverage-gap descriptor · idempotent per `(estate_region, period, source_class)`.

    Second identical call returns the same `GapCandidate` (AC-A3.b).
    """
    key = (estate_region, period, source_class)
    with _STORE._lock:
        existing_id = _STORE._by_tuple.get(key)
        if existing_id is not None:
            return _STORE._by_id[existing_id]
        candidate_id = _derive_candidate_id(estate_region, period, source_class)
        candidate = GapCandidate(
            filed_candidate_id=candidate_id,
            estate_region=estate_region,
            period=period,
            source_class=source_class,
            estimated_effort=estimated_effort,
        )
        _STORE._by_id[candidate_id] = candidate
        _STORE._by_tuple[key] = candidate_id
        return candidate


def read_gap_candidate(filed_candidate_id: str) -> GapCandidate:
    """Companion GET target for Prove render per Owner ruling Locus 2 = α.

    Raises `GapCandidateNotFound` on unknown FK; caller MUST render refusal
    without effort line (Owner ruling §2 failure-mode binding).
    """
    with _STORE._lock:
        candidate = _STORE._by_id.get(filed_candidate_id)
    if candidate is None:
        raise GapCandidateNotFound(filed_candidate_id)
    return candidate


def _reset_for_tests() -> None:
    """Test-only helper. Not to be called from production code."""
    with _STORE._lock:
        _STORE._by_id.clear()
        _STORE._by_tuple.clear()
