"""V1 metric scorers — sketches at G0.5.

Full implementations (WER via jiwer, DER via simple-der or pyannote.metrics,
NER recall over a labelled set) land at G2 alongside the first real
Hour A run. At G0.5 we only ship type-correct stubs so the harness
contract is callable end-to-end against synthetic.
"""
from __future__ import annotations

from typing import List


def wer(reference: str, hypothesis: str) -> float:
    """Stub WER. Returns 1.0 if either side is empty, else a naive
    word-error proxy. G2 swaps in `jiwer.wer`."""
    r = (reference or "").split()
    h = (hypothesis or "").split()
    if not r:
        return 1.0 if h else 0.0
    matches = sum(1 for a, b in zip(r, h) if a == b)
    return max(0.0, 1.0 - matches / len(r))


def ner_recall(gold_entities: List[str], retrieved_entities: List[str]) -> float:
    """Recall = |gold ∩ retrieved| / |gold|."""
    if not gold_entities:
        return 1.0
    g = set(gold_entities)
    return len(g & set(retrieved_entities)) / len(g)


def der_thirty_plus(gold_turns_seconds: List[float], retrieved_turns_seconds: List[float]) -> float:
    """Stub DER. Real scoring is segment-overlap based."""
    return 0.0  # placeholder; G2 wires the real scorer
