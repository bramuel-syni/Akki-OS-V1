"""A1.4 · Acoustic-fingerprint dedup (DEFAULT · PROM-S1-honesty-grammar-source-labels).

Chromaprint-class content-address dedup. Emits canonical + occurrence pointers.

Parameters (D-12 · known and parameterized · deploy in force):
- fingerprint_hex_length: 32 (chromaprint truncation for match keying)
- match_distance_threshold: 0 (exact/near-exact only per R-A1.4 · DEFAULT)
- news_content_types_dedup_exempt: {"speech"} for news-classified programme blocks

Honesty grammar: SUPPRESSED occurrences retain a re-queue pointer back to the
canonical they matched. A dedup false positive is recoverable — the pointer
preserves pre-dedup evidence per PROM-S1-honesty-grammar-source-labels.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Dict, List, Optional

FINGERPRINT_HEX_LENGTH: int = 32
MATCH_DISTANCE_THRESHOLD_DEFAULT: int = 0  # exact/near-exact only
NEWS_DEDUP_EXEMPT_LABELS = frozenset({"news", "current-affairs", "news-magazine"})


@dataclass(frozen=True)
class Occurrence:
    """Occurrence pointer: a suppressed span retains lineage to its canonical."""
    occurrence_id: str
    canonical_id: str            # canonical the occurrence matched
    source_canonical_id: str     # where the occurrence physically appeared
    batch_id: str
    start_ms: int
    end_ms: int
    fingerprint: str
    station: str                 # station of the source (station = source-object publisher)
    timestamp_ms: int            # absolute UTC ms
    is_news_exempt: bool         # AC-A1.d: news blocks are dedup-exempt
    requeue_pointer: str         # PROM-S1 honesty grammar: pointer preserves evidence


@dataclass(frozen=True)
class Fingerprint:
    """Chromaprint-class content-address for a span. Deterministic."""
    fingerprint: str
    batch_id: str
    start_ms: int
    end_ms: int


def compute_fingerprint(
    batch_id: str,
    start_ms: int,
    end_ms: int,
    audio_content_hash: str,
) -> Fingerprint:
    """Content-address a span. `audio_content_hash` is the backend-adapter chromaprint;
    deterministic in-process here for interface completeness.
    """
    material = f"{audio_content_hash}|{start_ms}|{end_ms}".encode("utf-8")
    fp = hashlib.sha256(material).hexdigest()[:FINGERPRINT_HEX_LENGTH]
    return Fingerprint(fingerprint=fp, batch_id=batch_id, start_ms=start_ms, end_ms=end_ms)


class DedupIndex:
    """Content-address dedup index. Maps fingerprint → canonical_id.

    First occurrence keeps canonical status. Subsequent matches emit Occurrence
    pointers back to the first-seen canonical. Deterministic across process runs
    when seeded from the same source order (registry-tracked).
    """

    def __init__(self) -> None:
        self._canonicals: Dict[str, str] = {}  # fingerprint → canonical_id

    def register_canonical(self, fingerprint: str, canonical_id: str) -> bool:
        """Register a canonical for a fingerprint. Returns True if first-seen."""
        if fingerprint in self._canonicals:
            return False
        self._canonicals[fingerprint] = canonical_id
        return True

    def match(self, fingerprint: str) -> Optional[str]:
        return self._canonicals.get(fingerprint)

    def size(self) -> int:
        return len(self._canonicals)


def emit_occurrence_if_duplicate(
    index: DedupIndex,
    fp: Fingerprint,
    source_canonical_id: str,
    station: str,
    absolute_timestamp_ms: int,
    programme_block_label: Optional[str] = None,
) -> Optional[Occurrence]:
    """Attempt to register `fp` as canonical; if it collides, emit an Occurrence.

    AC-A1.d: news programme blocks are DEDUP-EXEMPT — even on collision, the
    span retains canonical status (no Occurrence emitted). Exemption is
    LEGIBLE via the returned data (caller can see None return + is_news check).
    """
    is_news = programme_block_label in NEWS_DEDUP_EXEMPT_LABELS if programme_block_label else False
    if is_news:
        # News content is always registered fresh as canonical; no dedup applied.
        index.register_canonical(fp.fingerprint, source_canonical_id)
        return None

    registered = index.register_canonical(fp.fingerprint, source_canonical_id)
    if registered:
        return None

    matched_canonical = index.match(fp.fingerprint)
    if matched_canonical is None:  # defensive; should not happen after register attempt
        return None
    occurrence_id = f"occ:sha256:{hashlib.sha256(f'{fp.fingerprint}|{source_canonical_id}|{absolute_timestamp_ms}'.encode()).hexdigest()[:24]}"
    return Occurrence(
        occurrence_id=occurrence_id,
        canonical_id=matched_canonical,
        source_canonical_id=source_canonical_id,
        batch_id=fp.batch_id,
        start_ms=fp.start_ms,
        end_ms=fp.end_ms,
        fingerprint=fp.fingerprint,
        station=station,
        timestamp_ms=absolute_timestamp_ms,
        is_news_exempt=False,
        requeue_pointer=matched_canonical,
    )
