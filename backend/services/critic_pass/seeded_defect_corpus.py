"""Critic-pass seeded-defect corpus · Class D governed reference registry.

Owner ruling `docs/rulings/critic_pass_e1_2026_07_25.md` verbatim:

    "§5.5 classification — accepted as tallied: 28 S · 0 O · 7 E · 1 D.
    The seeded-defect corpus as Class D is confirmed, with the A3.3
    lifecycle applying in full including the addition/removal-edit
    asymmetry — an edit to a seeded defect changes what the catch-rate
    measures, so gating edits is correct there too."

A3.3 lifecycle (Rules Taxonomy v1 verbatim):
    "Upload (Excel/CSV) → schema validation (row-level errors,
    fail-closed on malformed) → diff view: added / removed / changed →
    confirm → versioned, receipted, effective-from stamped, rollback
    available. Every run records the registry version in force (audit
    answers 'was this term protected on date X'). Asymmetry (Owner-
    ruled): additions take effect immediately; removals AND edits
    require approval (counter-sign or configured waiting window) — the
    only edits that can weaken protection are the ones that gate."

Owner extension (this ruling): "an edit to a seeded defect changes what
the catch-rate measures, so gating edits is correct there too" — the
addition/removal-edit asymmetry applies with edits gated (not just
removals). Corpus versioned; Class E rubric parameters (catch-rate
target, false-alarm rate, seeded-defect audit cadence) reference this
registry by version.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional
import threading


DefectClass = Literal[
    "assertion_boundary_trace",   # falls under RV-1
    "fabrication",                # falls under CR-2
    "conflation",                 # falls under CR-3
    "scope_smuggling",            # falls under CR-4
    "enforcement_prose",          # falls under CR-5
    "reflexive_pass_stamp",       # falls under CR-6
    "selection_defect",           # falls under CR-7
]


@dataclass(frozen=True)
class SeededDefectEntry:
    """Class D governed reference registry entry.

    IMMUTABLE dataclass (per A3.3 registry discipline). Registry rows
    are versioned — edits land as new-version rows with the prior row
    superseded (never in-place edits).
    """

    entry_id: str
    defect_class: DefectClass
    canonical_example: str
    detection_criterion: str
    registry_version: str
    effective_from: str  # ISO-8601 UTC


@dataclass(frozen=True)
class CorpusVersion:
    """Registry version record · pinned per engine version."""

    version_id: str
    effective_from: str
    entry_count: int
    supersedes_version_id: Optional[str]


class PendingChangeAsymmetry(ValueError):
    """A3.3 asymmetry breach — removal or edit attempted without approval."""


_LOCK = threading.Lock()
_CORPUS: List[SeededDefectEntry] = []
_VERSIONS: List[CorpusVersion] = []
_CURRENT_VERSION: str = "v0"
_PENDING_REMOVALS: List[str] = []  # entry_ids pending approval
_PENDING_EDITS: List[str] = []     # entry_ids pending approval
_APPROVED_REMOVALS: set[str] = set()
_APPROVED_EDITS: set[str] = set()


def _reset_for_tests() -> None:
    global _CURRENT_VERSION
    with _LOCK:
        _CORPUS.clear()
        _VERSIONS.clear()
        _PENDING_REMOVALS.clear()
        _PENDING_EDITS.clear()
        _APPROVED_REMOVALS.clear()
        _APPROVED_EDITS.clear()
        _CURRENT_VERSION = "v0"


def _isoformat_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def add_entry(
    entry_id: str,
    defect_class: DefectClass,
    canonical_example: str,
    detection_criterion: str,
) -> SeededDefectEntry:
    """A3.3 asymmetry · additions take effect immediately."""
    with _LOCK:
        for existing in _CORPUS:
            if existing.entry_id == entry_id:
                raise ValueError(
                    f"duplicate entry_id {entry_id!r}; edits require approval "
                    f"via request_edit()."
                )
        entry = SeededDefectEntry(
            entry_id=entry_id,
            defect_class=defect_class,
            canonical_example=canonical_example,
            detection_criterion=detection_criterion,
            registry_version=_CURRENT_VERSION,
            effective_from=_isoformat_utc(),
        )
        _CORPUS.append(entry)
        return entry


def request_removal(entry_id: str) -> None:
    """A3.3 asymmetry · removals require approval (counter-sign)."""
    with _LOCK:
        if entry_id not in {e.entry_id for e in _CORPUS}:
            raise ValueError(f"entry_id {entry_id!r} not found in corpus")
        if entry_id in _PENDING_REMOVALS:
            return
        _PENDING_REMOVALS.append(entry_id)


def approve_removal(entry_id: str) -> None:
    """Counter-sign approval unlocks the pending removal."""
    with _LOCK:
        if entry_id not in _PENDING_REMOVALS:
            raise PendingChangeAsymmetry(
                f"cannot approve removal for {entry_id!r}: no pending "
                f"removal request exists."
            )
        _APPROVED_REMOVALS.add(entry_id)


def execute_removal(entry_id: str) -> None:
    """Execute the removal AFTER approval.

    A3.3 asymmetry: raises PendingChangeAsymmetry if the removal was not
    approved via counter-sign.
    """
    with _LOCK:
        if entry_id not in _APPROVED_REMOVALS:
            raise PendingChangeAsymmetry(
                f"removal of {entry_id!r} not approved; A3.3 asymmetry: "
                f"removals require approval (counter-sign or configured "
                f"waiting window)."
            )
        _CORPUS[:] = [e for e in _CORPUS if e.entry_id != entry_id]
        _PENDING_REMOVALS.remove(entry_id)
        _APPROVED_REMOVALS.discard(entry_id)


def request_edit(entry_id: str) -> None:
    """A3.3 asymmetry · edits require approval (Owner ruling extension).

    Owner: *"an edit to a seeded defect changes what the catch-rate
    measures, so gating edits is correct there too."*
    """
    with _LOCK:
        if entry_id not in {e.entry_id for e in _CORPUS}:
            raise ValueError(f"entry_id {entry_id!r} not found in corpus")
        if entry_id in _PENDING_EDITS:
            return
        _PENDING_EDITS.append(entry_id)


def approve_edit(entry_id: str) -> None:
    """Counter-sign approval unlocks the pending edit."""
    with _LOCK:
        if entry_id not in _PENDING_EDITS:
            raise PendingChangeAsymmetry(
                f"cannot approve edit for {entry_id!r}: no pending edit "
                f"request exists."
            )
        _APPROVED_EDITS.add(entry_id)


def execute_edit(
    entry_id: str,
    new_canonical_example: str,
    new_detection_criterion: str,
) -> SeededDefectEntry:
    """Execute the edit AFTER approval · lands as new-version entry.

    Raises PendingChangeAsymmetry if not approved.
    """
    with _LOCK:
        if entry_id not in _APPROVED_EDITS:
            raise PendingChangeAsymmetry(
                f"edit of {entry_id!r} not approved; A3.3 asymmetry (Owner "
                f"extension for seeded-defect corpus): edits require "
                f"approval — an edit changes what the catch-rate measures."
            )
        # Find the existing entry.
        idx: Optional[int] = None
        for i, e in enumerate(_CORPUS):
            if e.entry_id == entry_id:
                idx = i
                break
        if idx is None:
            raise ValueError(f"entry_id {entry_id!r} not found in corpus")
        old = _CORPUS[idx]
        new_entry = SeededDefectEntry(
            entry_id=old.entry_id,
            defect_class=old.defect_class,
            canonical_example=new_canonical_example,
            detection_criterion=new_detection_criterion,
            registry_version=_CURRENT_VERSION,
            effective_from=_isoformat_utc(),
        )
        _CORPUS[idx] = new_entry
        _PENDING_EDITS.remove(entry_id)
        _APPROVED_EDITS.discard(entry_id)
        return new_entry


def get_corpus() -> List[SeededDefectEntry]:
    with _LOCK:
        return list(_CORPUS)


def current_version() -> str:
    with _LOCK:
        return _CURRENT_VERSION
