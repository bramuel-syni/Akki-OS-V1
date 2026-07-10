"""Transform Forms router — 3 endpoints (BCR §3.7 landing).

Endpoints:
  * POST /api/transform/knowledge_artifact/produce — KA assembly.
  * POST /api/transform/callable_skill/provision — skill provisioning
    (write-once slice-freeze per TF-E4 (b) α).
  * POST /api/callable_skill/{skill_id}/query — per-call query, gated
    by `require_governed_skill_query` (TF-E4 (a) α inner gate).
"""
from __future__ import annotations

import uuid
from typing import Any, Dict

from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse

from services.transform_forms.callable_skill_gate import (
    BelowFloorError,
    below_floor_refusal_envelope,
    ensure_response_carries_class,
    require_governed_skill_query,
)
from services.transform_forms.callable_skill_persistence import provision_skill
from services.transform_forms.knowledge_artifact import build_knowledge_artifact
from core import db


router = APIRouter(tags=["transform_forms"])


@router.post("/transform/knowledge_artifact/produce")
async def produce_knowledge_artifact(body: Dict[str, Any] = Body(...)):
    """TF-R1: assemble a KA from claim + edge specs.

    Every node carries `defensibility.class` + `trace_id` inline
    (provenance preservation invariant enforced by the KA contract).
    """
    node_specs = body.get("nodes", [])
    edge_specs = body.get("edges", [])
    try:
        ka = build_knowledge_artifact(node_specs=node_specs, edge_specs=edge_specs)
    except (ValueError, KeyError) as exc:
        return JSONResponse(
            status_code=400,
            content={"outcome": "invalid_input", "detail": str(exc)},
        )
    return ka.model_dump(by_alias=True)


@router.post("/transform/callable_skill/provision")
async def provision_callable_skill(body: Dict[str, Any] = Body(...)):
    """TF-R2: provision a callable skill. Write-once slice-freeze.

    `skill_id` is minted server-side (uuid.hex). `corpus_slice_ref` +
    `key_grant_id` + `floor` + `scope` + `endpoint_path` are caller-supplied.
    """
    try:
        skill_id = uuid.uuid4().hex
        record = await provision_skill(
            db,
            skill_id=skill_id,
            corpus_slice_ref=body["corpus_slice_ref"],
            key_grant_id=body["key_grant_id"],
            floor=body["floor"],
            scope=body["scope"],
            endpoint_path=body.get(
                "endpoint_path", f"/api/callable_skill/{skill_id}/query"
            ),
        )
    except KeyError as exc:
        return JSONResponse(
            status_code=400,
            content={"outcome": "invalid_input", "detail": f"missing field: {exc}"},
        )
    return record.model_dump()


@router.post("/callable_skill/{skill_id}/query")
async def query_callable_skill(
    skill_id: str,
    request: Request,
    body: Dict[str, Any] = Body(...),
):
    """TF-R2 + Owner Tier-1 line: per-call inner gate + response class inline.

    Inner gate (TF-E4 (a) α) fires FIRST — identity + scope + floor. On
    pass, the query proceeds; response is mutated to carry
    `defensibility.class` inline (Owner-verbatim: 'every response
    carries class inline'). Below-floor → refusal envelope.
    """
    gate_result = await require_governed_skill_query(request, skill_id, db)
    if isinstance(gate_result, JSONResponse):
        return gate_result
    provisioning = gate_result

    # Skill-body path: for this baseline landing, the query is a
    # pass-through (real skill invocation lives at the LLM router; the
    # inner gate is what makes the surface governed). We attach class
    # inline; a below-floor result raises the refusal envelope.
    raw_response = {
        "skill_id": skill_id,
        "query": body.get("query", ""),
        "answer": body.get("answer_stub", "governed"),
    }
    # Class-inline mutation. The response builder (upstream skill logic)
    # is responsible for supplying its own class label; here we default
    # to the provisioning floor to preserve honesty grammar.
    class_label = body.get("class_label", provisioning.floor)

    try:
        mutated = ensure_response_carries_class(
            raw_response,
            class_label=class_label,
            floor=provisioning.floor,
        )
    except BelowFloorError:
        return JSONResponse(
            status_code=200,
            content=below_floor_refusal_envelope(
                class_label=class_label, floor=provisioning.floor
            ),
        )
    return mutated
