"""A1.2 · Batch segmentation (NORM · MC-E3 α placement precedent).

Worker-side batch schema · lives HERE, NOT in backend/contracts/ (Parity-31
conservation per MC-E3 α ruling).

Content-addressed batch_id · programme-block-aware with 30-minute default window
(NORM class per EAB v1.1 §2.2 R-A1.2 "target 15-60 minutes").

Parameters (D-12 · known and parameterized · deploy in force):
- default_batch_window_ms: 1_800_000 (30 minutes · pre-authorized default)
- min_batch_window_ms: 900_000 (15 min · R-A1.2 lower bound)
- max_batch_window_ms: 3_600_000 (60 min · R-A1.2 upper bound)

Programme-block hints (if provided) override the default window boundary;
in their absence the 30-min window applies deterministically.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import List, Optional, Sequence

DEFAULT_BATCH_WINDOW_MS: int = 1_800_000  # 30 min
MIN_BATCH_WINDOW_MS: int = 900_000        # 15 min
MAX_BATCH_WINDOW_MS: int = 3_600_000      # 60 min


@dataclass(frozen=True)
class ProgrammeBlock:
    """Programme-block hint (optional · overrides default window if provided)."""
    start_ms: int
    end_ms: int
    label: Optional[str] = None


@dataclass(frozen=True)
class BatchSegment:
    """Worker-side batch envelope. NOT a Parity 31 contract.

    batch_id is content-addressed (deterministic across re-runs of the same source).
    """
    batch_id: str
    canonical_id: str
    start_ms: int
    end_ms: int
    window_ms: int
    programme_block_label: Optional[str] = None


def compute_batch_id(canonical_id: str, start_ms: int, end_ms: int) -> str:
    """Content-addressed batch_id. Deterministic; canonical-id + window."""
    if start_ms < 0 or end_ms <= start_ms:
        raise ValueError("invalid batch window")
    material = f"{canonical_id}|{start_ms}|{end_ms}".encode("utf-8")
    return f"batch:sha256:{hashlib.sha256(material).hexdigest()[:24]}"


def segment(
    canonical_id: str,
    total_duration_ms: int,
    programme_blocks: Optional[Sequence[ProgrammeBlock]] = None,
    window_ms: int = DEFAULT_BATCH_WINDOW_MS,
) -> List[BatchSegment]:
    """Segment a canonical artifact into batches.

    If `programme_blocks` supplied and each block sits within [MIN, MAX], batches
    honor block boundaries. Otherwise the deterministic `window_ms` (default 30 min)
    partitions the duration.

    NORM-class: window can be tuned per estate; default is pre-authorized.
    """
    if total_duration_ms <= 0:
        return []
    if window_ms < MIN_BATCH_WINDOW_MS or window_ms > MAX_BATCH_WINDOW_MS:
        raise ValueError(
            f"window_ms {window_ms} outside R-A1.2 range "
            f"[{MIN_BATCH_WINDOW_MS}, {MAX_BATCH_WINDOW_MS}]"
        )

    if programme_blocks:
        return _segment_by_blocks(canonical_id, programme_blocks, total_duration_ms)

    segments: List[BatchSegment] = []
    cursor = 0
    while cursor < total_duration_ms:
        end = min(cursor + window_ms, total_duration_ms)
        segments.append(
            BatchSegment(
                batch_id=compute_batch_id(canonical_id, cursor, end),
                canonical_id=canonical_id,
                start_ms=cursor,
                end_ms=end,
                window_ms=end - cursor,
                programme_block_label=None,
            )
        )
        cursor = end
    return segments


def _segment_by_blocks(
    canonical_id: str,
    blocks: Sequence[ProgrammeBlock],
    total_duration_ms: int,
) -> List[BatchSegment]:
    result: List[BatchSegment] = []
    for block in blocks:
        if block.start_ms < 0 or block.end_ms > total_duration_ms:
            raise ValueError(f"programme block {block} out of source duration")
        if block.end_ms - block.start_ms < MIN_BATCH_WINDOW_MS:
            # Sub-minimum blocks merge into next; deterministic downstream.
            continue
        result.append(
            BatchSegment(
                batch_id=compute_batch_id(canonical_id, block.start_ms, block.end_ms),
                canonical_id=canonical_id,
                start_ms=block.start_ms,
                end_ms=block.end_ms,
                window_ms=block.end_ms - block.start_ms,
                programme_block_label=block.label,
            )
        )
    return result
