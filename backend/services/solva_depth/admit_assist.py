"""Solva admit-assist — sibling to G1's Solva Depth v1.

Mandate `/app/docs/mandates/northena_v1.0.md` §4, §9, §10:
Admit invokes Solva for compilation judgement (scope resolution,
preservation depth, defensibility floor). Solva does the judgement;
Northena freezes the returned value. This module IS that Solva
interface — sibling to `services/g1_defensibility/solva_depth/`, no
contract change to G1 Solva Depth v1.

v0 stubs (deterministic-default): full inference lands post-V3. The
three methods return simple typed values — no wrapper dataclasses,
no ceremony — because v0 has nothing to wrap. When judgement plugs
in, callers see typed values, not opaque `.value` unwrapping.

Cousin substrate:
  `services/layer_b/factory.py` — Protocol + default-returning stub
    pattern (honest-availability discipline).
  G1 reshape at `services/g1_defensibility/solva_depth/refusal.py`
    (cousin: `solva_v2/engines/refusal.py`) — structured-refusal
    discipline. Absorbed at the caller (admit.py refusal shape), not
    duplicated here.
"""
from __future__ import annotations

from typing import List, Optional, Protocol


class RegistryStub:
    """v0 registry stub. Real Registry lands at G4 (Mtafiti / Targeta)."""

    def __init__(self, known: Optional[List[str]] = None) -> None:
        self._known = set(known or ["news_anchor_read", "panel_debate"])

    def exists(self, name: str) -> bool:
        return name in self._known


class SolvaAdmitAssistProtocol(Protocol):
    def resolve_scope(self, declared: List[str], registry: RegistryStub) -> List[str]: ...
    def preservation_depth(self, hint: Optional[str]) -> str: ...
    def defensibility_floor(self, hint: Optional[str]) -> str: ...


class SolvaAdmitAssistV0:
    """v0 deterministic-default assist. Full judgement lands post-V3."""

    def resolve_scope(self, declared: List[str], registry: RegistryStub) -> List[str]:
        # TODO[post-V3]: real scope resolution + ambiguity report.
        return [m for m in declared if registry.exists(m)]

    def preservation_depth(self, hint: Optional[str]) -> str:
        return hint or "default"  # TODO[post-V3]: judged per Spec §6.

    def defensibility_floor(self, hint: Optional[str]) -> str:
        return hint or "utterance"  # TODO[post-V3]: judged per Spec §6.3.


_DEFAULT: SolvaAdmitAssistProtocol = SolvaAdmitAssistV0()


def get_assist() -> SolvaAdmitAssistProtocol:
    return _DEFAULT
