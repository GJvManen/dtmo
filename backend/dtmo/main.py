from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from dtmo.config import get_settings
from dtmo.connectors.cisa_kev import CisaKevConnector
from dtmo.logging import configure_logging, correlation_id, get_logger
from dtmo.scheduler import ScheduledJob, SchedulerService

settings = get_settings()
configure_logging(settings.log_level)
log = get_logger("api")
scheduler = SchedulerService()
REQUESTS = Counter("dtmo_http_requests_total", "HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("dtmo_http_request_seconds", "HTTP request latency", ["method", "path"])


async def run_cisa_kev() -> dict[str, object]:
    result = await CisaKevConnector(settings).run()
    log.info(
        "connector_run_finished",
        connector_id=result.connector_id,
        status=result.status,
        records=len(result.records),
        attempts=result.attempts,
    )
    return {
        "connector_id": result.connector_id,
        "status": result.status,
        "records": len(result.records),
        "attempts": result.attempts,
        "error": result.error,
    }


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.feature_live_connectors:
        scheduler.register(
            ScheduledJob(
                id="cisa-kev",
                interval_seconds=settings.connector_poll_seconds,
                handler=run_cisa_kev,
            )
        )
        scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="DTMO API",
    version="16.0.0rc4",
    description="Education-focused cyber threat intelligence platform",
    lifespan=lifespan,
)


@app.middleware("http")
async def request_context(request: Request, call_next):  # type: ignore[no-untyped-def]
    request_id = request.headers.get("x-correlation-id", str(uuid4()))
    token = correlation_id.set(request_id)
    path = request.url.path
    with LATENCY.labels(request.method, path).time():
        response = await call_next(request)
    correlation_id.reset(token)
    response.headers["x-correlation-id"] = request_id
    response.headers["x-content-type-options"] = "nosniff"
    response.headers["x-frame-options"] = "DENY"
    response.headers["referrer-policy"] = "no-referrer"
    REQUESTS.labels(request.method, path, response.status_code).inc()
    return response


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "healthy",
        "version": app.version,
        "environment": settings.environment,
        "scheduler": scheduler.status(),
        "publication_gate": "human-approval-required",
    }


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/connectors")
def connectors() -> list[dict[str, object]]:
    return [
        {
            "id": "cisa-kev",
            "enabled": settings.feature_live_connectors,
            "reliability": "authoritative",
            "schedule_seconds": settings.connector_poll_seconds,
        }
    ]


@app.post("/connectors/cisa-kev/run")
async def run_connector() -> dict[str, object]:
    if settings.production and not settings.feature_live_connectors:
        return {"status": "disabled", "reason": "feature flag is off"}
    return await run_cisa_kev()


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
