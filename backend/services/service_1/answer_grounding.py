"""Answer-grounding gate — Answer Fluency §3.8 (AF-E1 β + 2 conditions).

Owner ruling AF-E1 β + 2 conditions (2026-07-10) verbatim: *"β, two
conditions. Per-sentence structured anchor mapping — positive
attribution, mechanically checkable, 9.2a-E1 pattern. Conditions closing
the self-declaration gap (a fabricated sentence can cite a real
unit_id): (1) numeric grounding is verified, not declared — every
numeral in a sentence must appear verbatim in that sentence's anchored
units; mechanical check, no semantic scoring. (2) Any unanchored or
failing sentence → grounding REJECT → whole response falls to the
mechanical arm — the gate never patches prose."*

Four mechanical sub-gates:
  * (A) unit_id ∈ set        — every declared unit_id ∈ load_bearing_unit_ids
  * (B) sentence-anchor cover — every sentence in prose has ≥1 anchor entry
  * (C) numeric verification — every numeral in a sentence appears verbatim
                                in that sentence's anchored unit texts
  * (D) full-response reject  — any (A)/(B)/(C) failure → REJECT; gate
                                NEVER patches prose (per Condition 2 verbatim)

**NO semantic scoring, NO overlap/similarity/jaccard/embedding
computation.** AF-G6b (§6.10 AST/reflection gate) enforces this
grep-negatively on this module.

Sentence splitter (Tier-3 default): mechanical regex on sentence-
terminating punctuation `[.!?]` followed by whitespace/EOF. Whitespace
normalisation before comparison. NOT an LLM-based segmenter (a subtle
failure mode would be a segmenter drifting from the anchor mapping).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional


# Mechanical sentence splitter: split on '.', '!', '?' followed by
# whitespace or end-of-string. Preserves the sentence text (no
# punctuation stripping); trims leading/trailing whitespace.
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")

# Numeral regex: contiguous digits with optional decimal/thousands
# separators (comma or period) and optional trailing percent sign.
_NUMERAL_RE = re.compile(r"[0-9]+(?:[.,][0-9]+)*%?")


@dataclass(frozen=True)
class GroundingResult:
    """Outcome of the grounding gate."""
    passed: bool
    reject_detail: Optional[str]  # Populated iff passed is False.


def _split_sentences(prose: str) -> List[str]:
    """Mechanical sentence splitter — returns non-empty sentences.

    Splits on sentence-terminating punctuation followed by whitespace.
    Trims each sentence; drops empty splits.
    """
    if not prose:
        return []
    raw = _SENTENCE_SPLIT_RE.split(prose)
    return [s.strip() for s in raw if s.strip()]


def _extract_numerals(text: str) -> List[str]:
    """Extract all numeral tokens from a string (mechanical regex)."""
    return _NUMERAL_RE.findall(text)


def verify_grounding(
    prose: str,
    per_sentence: List[Dict],
    load_bearing_unit_ids: List[str],
    unit_id_to_text: Dict[str, str],
) -> GroundingResult:
    """Run all four sub-gates against a fluent-draft output.

    Args:
      prose: full fluent-draft prose text.
      per_sentence: list of dicts with `sentence_text` (str) +
        `unit_ids` (list[str]). Per AF-E1 β structured-output schema.
      load_bearing_unit_ids: caller-supplied allow-list of unit_ids.
      unit_id_to_text: mapping unit_id → unit text (Five-Rings text field).

    Returns:
      GroundingResult(passed=True, reject_detail=None) on success.
      GroundingResult(passed=False, reject_detail=<str>) on any failure.
      `reject_detail` names the specific sub-gate + offending item.

    Per AF-E1 β Condition 2 (Owner verbatim): *"any unanchored or
    failing sentence → grounding REJECT → whole response falls to the
    mechanical arm — the gate never patches prose."* This function
    RETURNS the pass/fail outcome; the caller is responsible for
    routing to the mechanical arm on fail. This function never edits
    or patches prose.
    """
    allowed = set(load_bearing_unit_ids)

    # (A) unit_id ∈ set — every declared anchor's unit_ids ⊆ allowed.
    for i, entry in enumerate(per_sentence):
        for uid in entry.get("unit_ids", []):
            if uid not in allowed:
                return GroundingResult(
                    passed=False,
                    reject_detail=(
                        f"foreign_unit_id:sentence_index={i}:unit_id={uid!r}"
                    ),
                )

    # (B) sentence-anchor cover — every sentence in prose has ≥1 anchor entry.
    sentences_in_prose = _split_sentences(prose)
    sentences_in_anchors = [
        (entry.get("sentence_text") or "").strip()
        for entry in per_sentence
    ]
    for idx, prose_sentence in enumerate(sentences_in_prose):
        if prose_sentence not in sentences_in_anchors:
            return GroundingResult(
                passed=False,
                reject_detail=(
                    f"sentence_not_anchored:prose_index={idx}:"
                    f"sentence={prose_sentence!r}"
                ),
            )

    # Also require every anchor's sentence_text be non-empty AND have
    # at least one unit_id (empty unit_ids = unanchored sentence per
    # Condition 2).
    for i, entry in enumerate(per_sentence):
        if not entry.get("sentence_text") or not entry.get("sentence_text").strip():
            return GroundingResult(
                passed=False,
                reject_detail=f"empty_sentence_text:anchor_index={i}",
            )
        if not entry.get("unit_ids"):
            return GroundingResult(
                passed=False,
                reject_detail=(
                    f"sentence_not_anchored:anchor_index={i}:"
                    f"sentence={entry.get('sentence_text')!r}"
                ),
            )

    # (C) numeric verification — every numeral in a sentence appears
    # VERBATIM in that sentence's anchored unit texts. Mechanical
    # byte-substring check; no semantic scoring.
    for i, entry in enumerate(per_sentence):
        sentence_text = entry["sentence_text"]
        anchored_unit_texts = "".join(
            unit_id_to_text.get(uid, "") for uid in entry["unit_ids"]
        )
        for numeral in _extract_numerals(sentence_text):
            if numeral not in anchored_unit_texts:
                return GroundingResult(
                    passed=False,
                    reject_detail=(
                        f"numeric_verification_failed:sentence_index={i}"
                        f":numeral={numeral!r}"
                    ),
                )

    # (D) All checks passed. Full-response ACCEPT.
    return GroundingResult(passed=True, reject_detail=None)
