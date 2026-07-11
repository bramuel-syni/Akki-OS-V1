"""Brief grounding gate — OB-E1 α mechanical byte-verbatim substring check.

Owner ruling OB-E1 α (2026-07-10 · verbatim): *"Structured anchor +
byte-verbatim substring check, whole-brief reject on any failure, gate
never patches — the AF-E1 β grammar ported intact, including its
conditions (mechanical check, no semantic scoring)."*

Two sub-gates:
  (A) byte-verbatim value check — every `value` in
      `quantitative_anchors` MUST appear byte-verbatim in the text of
      the Registry read at `registry_read_ref`.
  (B) numeric-coverage check — every numeric in `brief_text` (regex
      `[0-9]+(?:[.,][0-9]+)*%?`) has a corresponding anchor entry.

Whole-brief reject (Owner-verbatim): any failure → brief NOT emitted;
regeneration tagged `grounding_reject`; gate NEVER patches the brief.

**NO semantic scoring** (AF-G6b lineage · §6.10 AST attest at
`test_ob_g6_brief_grounding_no_semantic_scoring_ast`).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional


# Same numeral regex as AF-E1 β Owner Condition 1.
_NUMERAL_RE = re.compile(r"[0-9]+(?:[.,][0-9]+)*%?")


@dataclass(frozen=True)
class BriefGroundingResult:
    passed: bool
    reject_detail: Optional[str]  # populated iff passed is False


def verify_brief_grounding(
    brief_text: str,
    quantitative_anchors: List[Dict],
    registry_read_texts: Dict[str, str],
) -> BriefGroundingResult:
    """Run OB-E1 α gates against a Shield-emitted brief payload.

    Args:
      brief_text: the composed brief prose.
      quantitative_anchors: list of `{value, registry_read_ref}` dicts
        emitted by Shield-side brief_synthesizer as structured output.
      registry_read_texts: {registry_read_ref → text} mapping supplied
        by the caller (generator built this from the Registry read
        surface before Shield synthesis).

    Returns:
      BriefGroundingResult(passed=True, reject_detail=None) on success.
      BriefGroundingResult(passed=False, reject_detail=<str>) on any
      failure. `reject_detail` names the specific sub-gate + item.

    Owner Condition 2 verbatim: *"any unanchored or failing sentence
    → grounding REJECT → whole response falls to the mechanical arm
    — the gate never patches prose."* Applied to briefs: any failure
    → brief NOT emitted; gate never edits the brief.
    """
    # (A) byte-verbatim value check
    for i, anchor in enumerate(quantitative_anchors):
        value = anchor.get("value", "")
        ref = anchor.get("registry_read_ref", "")
        if not value or not ref:
            return BriefGroundingResult(
                passed=False,
                reject_detail=(
                    f"empty_anchor:index={i}:value={value!r}:ref={ref!r}"
                ),
            )
        registry_text = registry_read_texts.get(ref)
        if registry_text is None:
            return BriefGroundingResult(
                passed=False,
                reject_detail=(
                    f"unknown_registry_read_ref:index={i}:ref={ref!r}"
                ),
            )
        if value not in registry_text:
            return BriefGroundingResult(
                passed=False,
                reject_detail=(
                    f"value_not_in_registry_read:index={i}:"
                    f"value={value!r}:ref={ref!r}"
                ),
            )

    # (B) numeric-coverage check — every numeric in brief_text has a
    # corresponding anchor `value` (byte-matching).
    anchored_values = {a["value"] for a in quantitative_anchors if a.get("value")}
    for numeral in _NUMERAL_RE.findall(brief_text):
        if numeral not in anchored_values:
            return BriefGroundingResult(
                passed=False,
                reject_detail=(
                    f"numeric_not_anchored:numeral={numeral!r}"
                ),
            )

    return BriefGroundingResult(passed=True, reject_detail=None)
