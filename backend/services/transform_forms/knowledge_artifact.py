"""Knowledge Artifact assembly (TF-R1).

Assembles a `KnowledgeArtifactV0` from a claim source (Registry read or
composition output). Provenance preservation invariant enforced structurally
by the Pydantic contract: every node MUST have `defensibility.class` +
`trace_id` at construction time.

TF-E3 α condition: `class` validated through
`services.transform_forms.defensibility_loader.validate_defensibility_class`.
"""
from __future__ import annotations

from typing import Iterable, List, Tuple

from contracts.knowledge_artifact_v0 import (
    KnowledgeArtifactEdge,
    KnowledgeArtifactNode,
    KnowledgeArtifactNodeDefensibility,
    KnowledgeArtifactNodeProvenance,
    KnowledgeArtifactV0,
)
from services.transform_forms.defensibility_loader import validate_defensibility_class


def build_knowledge_artifact(
    *,
    node_specs: Iterable[dict],
    edge_specs: Iterable[dict],
) -> KnowledgeArtifactV0:
    """Assemble a `KnowledgeArtifactV0` from claim + edge specs.

    Args:
      node_specs: iterable of dicts matching the KA node shape.
      edge_specs: iterable of dicts matching the KA edge shape.

    Every node's `defensibility.class` is validated against the
    canonical registry (TF-E3 α). Missing `class` or `trace_id` on
    any node → Pydantic ValidationError (provenance preservation
    invariant enforced structurally).
    """
    nodes: List[KnowledgeArtifactNode] = []
    for spec in node_specs:
        defensibility = spec.get("defensibility") or {}
        class_ = defensibility.get("class") or defensibility.get("class_")
        if class_ is None:
            raise ValueError(
                f"KA node {spec.get('claim_id')!r} missing "
                "defensibility.class — provenance preservation "
                "invariant violated."
            )
        validate_defensibility_class(class_)
        nodes.append(
            KnowledgeArtifactNode(
                claim_id=spec["claim_id"],
                claim_text=spec["claim_text"],
                defensibility=KnowledgeArtifactNodeDefensibility(
                    **{"class": class_, "contested": bool(defensibility.get("contested", False))}
                ),
                trace_id=spec["trace_id"],
                provenance=KnowledgeArtifactNodeProvenance(
                    source_ref=spec["provenance"]["source_ref"]
                ),
            )
        )

    edges: List[KnowledgeArtifactEdge] = [
        KnowledgeArtifactEdge(
            from_claim_id=e["from_claim_id"],
            to_claim_id=e["to_claim_id"],
            relation=e["relation"],
        )
        for e in edge_specs
    ]

    return KnowledgeArtifactV0(nodes=nodes, edges=edges)
