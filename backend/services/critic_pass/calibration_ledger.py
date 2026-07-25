"""Critic-pass calibration ledger + Class E deterministic sampling-rate
decay + seeded-defect corpus scaffold (Owner-side sampling ceremony
executes elsewhere — this module lands machinery only).

Owner ruling `docs/rulings/critic_pass_e1_2026_07_25.md` (2026-07-25 · FINAL):

    "Early E→O promotion of the verdict sampling rate — DECLINED,
    without prejudice. 'Decays as measured reliability accumulates'
    describes a schedule, and a schedule can live as a Class E
    deterministic decay function pinned per version — runtime tunability
    is not yet demonstrated as needed, and pre-emptive promotion is
    exactly the reclassification creep A3.2 exists to prevent. Land it
    Class E with the decay rule explicit in the engine spec."

Critic Seam v1.0 §7 verbatim (Tier-3): sampling parameters — DEFAULT class,
versioned like model calibration. Staleness window 10 phases DEFAULT.

Rules Taxonomy v1 A3.4: verdict sampling rate = Class E (Engine settings ·
pinned per engine version · A3.2 E→O promotion for runtime tunability).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Literal, Optional
import threading


# ---------------------------------------------------------------------------
# §5.5 Class E defaults · pinned per engine version · Owner ITEM 1 forward-binding.
# ---------------------------------------------------------------------------

ENGINE_VERSION: str = "critic-pass-v0"

# Class E · staleness window (Critic Seam v1.0 §9 · DEFAULT 10 phases).
STALENESS_WINDOW_PHASES: int = 10

# Class E · seeded-defect audit cadence (Critic Seam v1.0 §7 · 1/5 phases DEFAULT).
SEEDED_DEFECT_AUDIT_CADENCE_PHASES: int = 5

# Class E · critic catch-rate target (Critic Seam v1.0 §9 · ≥80% DEFAULT).
CRITIC_CATCH_RATE_TARGET: float = 0.80

# Class E · critic false-alarm rate (Critic Seam v1.0 §9 · ≤20% DEFAULT).
CRITIC_FALSE_ALARM_RATE_MAX: float = 0.20

# Class E · TQ §7 Part B sample selection rate (TQ v1.0 §7 line 121 DEFAULT).
TQ7B_SAMPLE_SELECTION_RATE: float = 0.01  # 1% of production volume
TQ7B_SAMPLE_SELECTION_ITEM_CAP: int = 100  # OR 100 items/class/period · whichever smaller

# Class E · TQ §7 Part B tripwire thresholds (TQ v1.0 §7 line 117-119 · numeric DEFAULTs).
TQ7B_EMPTY_OUTPUT_RATE_TRIPWIRE: float = 0.05           # 5% empty-output rate → tripwire
TQ7B_DISTRIBUTION_SHIFT_TRIPWIRE: float = 0.15          # 15% distribution shift vs baseline
TQ7B_CONFIDENCE_PROFILE_ANOMALY_TRIPWIRE: float = 0.10  # 10% confidence-profile anomaly rate

# Class E · verdict sampling rate · deterministic decay function.
# Owner ruling: DECLINED E→O promotion · Class E deterministic decay pinned per version.
VERDICT_SAMPLING_INITIAL_FINDINGS_RATE: float = 0.20   # 20% of findings sampled initially
VERDICT_SAMPLING_INITIAL_ALL_CLEARS_RATE: float = 0.10  # 10% of all-clears sampled initially
VERDICT_SAMPLING_DECAY_HALF_LIFE_PHASES: int = 20      # Half-life in phases (deterministic)
VERDICT_SAMPLING_FLOOR_RATE: float = 0.02              # Sampling never decays below 2%


def sampling_rate_findings(phase_count: int) -> float:
    """Class E deterministic decay function · verdict sampling rate for findings.

    Owner ruling: *"a schedule can live as a Class E deterministic decay
    function pinned per version"*.

    rate(n) = max(FLOOR, INITIAL × 2^(-n / HALF_LIFE))

    Pinned parameters (all Class E · pinned per engine version):
      * INITIAL   = VERDICT_SAMPLING_INITIAL_FINDINGS_RATE (0.20)
      * HALF_LIFE = VERDICT_SAMPLING_DECAY_HALF_LIFE_PHASES (20 phases)
      * FLOOR     = VERDICT_SAMPLING_FLOOR_RATE (0.02)
    """
    if phase_count < 0:
        raise ValueError(f"phase_count must be >= 0, got {phase_count}")
    decayed = VERDICT_SAMPLING_INITIAL_FINDINGS_RATE * (
        2.0 ** (-phase_count / VERDICT_SAMPLING_DECAY_HALF_LIFE_PHASES)
    )
    return max(VERDICT_SAMPLING_FLOOR_RATE, decayed)


def sampling_rate_all_clears(phase_count: int) -> float:
    """Class E deterministic decay function · verdict sampling rate for all-clears."""
    if phase_count < 0:
        raise ValueError(f"phase_count must be >= 0, got {phase_count}")
    decayed = VERDICT_SAMPLING_INITIAL_ALL_CLEARS_RATE * (
        2.0 ** (-phase_count / VERDICT_SAMPLING_DECAY_HALF_LIFE_PHASES)
    )
    return max(VERDICT_SAMPLING_FLOOR_RATE, decayed)


# ---------------------------------------------------------------------------
# Calibration ledger — per-worker-class + per-rubric-item · versioned.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CalibrationRow:
    """Calibration ledger row · versioned like model calibration.

    Owner-side sampling ceremony executes elsewhere; this row shape is
    the machinery landing.
    """

    row_id: int
    worker_class: str  # e.g., "critic_pass" · "tq7b_production_critic"
    rubric_item: Optional[str]  # None for aggregate rows; else "CR-1".."CR-7"
    catch_rate: float
    false_alarm_rate: float
    sample_count: int
    engine_version: str  # pinned per engine version (Class E discipline)
    phase_count_at_calibration: int
    calibrated_at: str  # ISO-8601 UTC
    stale_after_phase_count: int  # phase_count_at_calibration + STALENESS_WINDOW_PHASES


_LEDGER_LOCK = threading.Lock()
_CALIBRATION_LEDGER: List[CalibrationRow] = []
_NEXT_CALIB_ROW_ID: int = 1


def _reset_for_tests() -> None:
    """Test hook."""
    global _NEXT_CALIB_ROW_ID
    with _LEDGER_LOCK:
        _CALIBRATION_LEDGER.clear()
        _NEXT_CALIB_ROW_ID = 1


def append_calibration_row(
    worker_class: str,
    rubric_item: Optional[str],
    catch_rate: float,
    false_alarm_rate: float,
    sample_count: int,
    phase_count_at_calibration: int,
) -> CalibrationRow:
    """Append a calibration row · pinned to current ENGINE_VERSION."""
    global _NEXT_CALIB_ROW_ID
    with _LEDGER_LOCK:
        row = CalibrationRow(
            row_id=_NEXT_CALIB_ROW_ID,
            worker_class=worker_class,
            rubric_item=rubric_item,
            catch_rate=catch_rate,
            false_alarm_rate=false_alarm_rate,
            sample_count=sample_count,
            engine_version=ENGINE_VERSION,
            phase_count_at_calibration=phase_count_at_calibration,
            calibrated_at=datetime.now(timezone.utc).isoformat(),
            stale_after_phase_count=(
                phase_count_at_calibration + STALENESS_WINDOW_PHASES
            ),
        )
        _CALIBRATION_LEDGER.append(row)
        _NEXT_CALIB_ROW_ID += 1
        return row


def is_calibration_stale(row: CalibrationRow, current_phase_count: int) -> bool:
    """Critic Seam v1.0 §9: findings render UNCALIBRATED past staleness window."""
    return current_phase_count > row.stale_after_phase_count


def get_calibration_ledger() -> List[CalibrationRow]:
    with _LEDGER_LOCK:
        return list(_CALIBRATION_LEDGER)
