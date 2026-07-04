"""RMS Intelligence System — FastAPI assembler (G0).

Minimal scaffold. G0 mounts:
  * /api/health           — liveness probe.
  * /api/system/state     — surfaces data-source mode (synthetic vs real).
  * /api/openapi.json     — re-exposed (FastAPI default) for the CI smoke.

Future phases will mount Layer-D Service-2 routers (G3), Mtafiti / Targeta
admin (G4), Operator Console (G5), and Outer-Gate file-out (G6). At G0
the surface is intentionally tiny; the load-bearing work this gate is
contract freezing, not endpoint count.

Cousin pointer: /reference/akki-legacy/backend/server.py L1-L80 (shape of
the thin assembler + router-include style).
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from core import APP_NAME, db, iso, now
from routers import contracts as contracts_router
from routers import discipline as discipline_router
from routers import handoff as handoff_router
from routers import v1 as v1_router
from routers import g1 as g1_router
from routers import northena as northena_router
from routers import objectives as objectives_router
from routers import service_1 as service_1_router
from routers import solva as solva_router
from services.data_source import get_active_data_source
from services.service_1 import async_state as async_state_service
from services.service_1 import async_worker as async_worker_service
from services.system_state import current_system_state

log = logging.getLogger("rms.server")

app = FastAPI(
    title=APP_NAME,
    version="0.0.1-g0",
    description=(
        "RMS Intelligence System. Doctrine names canonical: "
        "Akki / SyniSense / Northena / Solva / Mtafiti / Targeta. "
        "G0 ships frozen contracts + Inner-Gate substrate only."
    ),
    # Expose OpenAPI + docs under /api so the Kubernetes ingress routes them.
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = APIRouter(prefix="/api")


@api.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "app": APP_NAME,
        "gate": "G0",
        "time": iso(now()),
    }


@api.get("/system/state")
async def system_state() -> dict:
    """Surfaces the data-source mode (synthetic vs real) per G0 Deliverable 3.c.
    The G5 Engine console will read this and render "running on synthetic /
    V-gates pending" when applicable.
    """
    ds = get_active_data_source()
    return current_system_state(data_source_name=ds.name, data_source_mode=ds.mode)


app.include_router(api)
# Contract-surfacing routes — make the frozen Pydantic models discoverable
# via /api/openapi.json::components.schemas (G0 follow-up; tester TEST 4).
app.include_router(contracts_router.router, prefix="/api")
app.include_router(v1_router.router, prefix="/api")
app.include_router(g1_router.router, prefix="/api")
app.include_router(northena_router.router, prefix="/api")
app.include_router(solva_router.router, prefix="/api")
app.include_router(service_1_router.router, prefix="/api")
app.include_router(discipline_router.router, prefix="/api")
app.include_router(handoff_router.router, prefix="/api")
app.include_router(objectives_router.router, prefix="/api")
from routers import mtafiti as mtafiti_router  # noqa: E402
app.include_router(mtafiti_router.router, prefix="/api")
from routers import pricing as pricing_router  # noqa: E402
app.include_router(pricing_router.router, prefix="/api")
app.include_router(pricing_router.fleet_router, prefix="/api")


@app.on_event("startup")
async def _startup() -> None:
    log.info("rms.startup: db=%s gate=Phase_5_Stage_B", db.name)
    # Phase 5 Stage B — async delivery substrate boot sequence.
    # Ordering: (1) ensure Mongo indexes exist; (2) run recovery sweep
    # to re-enqueue non-terminal objectives left over from prior boot;
    # (3) start the worker pool. Any error here fails ASGI startup —
    # loud, not silent (Standing Disposition infra-not-refusal).
    try:
        await async_state_service.ensure_indexes()
        await async_worker_service.recovery_sweep()
        await async_worker_service.start_workers()
    except Exception:
        log.exception("rms.startup: async delivery substrate boot failed")
        raise


@app.on_event("shutdown")
async def _shutdown() -> None:
    log.info("rms.shutdown: draining async workers")
    # Graceful shutdown — cancel worker tasks; in-flight objectives
    # left in `running` state on disk; next boot's recovery sweep will
    # reset them to `accepted` and re-enqueue.
    try:
        await async_worker_service.stop_workers()
    except Exception:
        log.exception("rms.shutdown: worker stop error (state persists in Mongo)")
