from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from time import perf_counter
from typing import Annotated

from fastapi import Depends, FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

from dtmo.admin_center import router as admin_center_router
from dtmo.admin_sources import router as admin_sources_router
from dtmo.admin_ui import router as admin_ui_router
from dtmo.alerts import connector_alerts
from dtmo.api.routes import close_services, ingest_connector_record, router as intelligence_router
from dtmo.api_alerts import api_error_alerts
from dtmo.auditor_ui import router as auditor_ui_router
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.ciso_ui import router as ciso_ui_router
from dtmo.config import get_settings
from dtmo.connectors.cisa_kev import CisaKevConnector
from dtmo.frontend import router as frontend_router
from dtmo.logging import bind_request_context, clear_request_context, configure_logging, correlation_id, get_logger, resolve_correlation_id
from dtmo.operations_metrics import router as operations_metrics_router
from dtmo.operations_ui import router as operations_ui_router
from dtmo.scheduler import ScheduledJob, SchedulerService
from dtmo.source_center import router as source_center_router
from dtmo.threat_workspace import router as threat_workspace_router
from dtmo.trace_context import begin_trace, end_trace
from dtmo.ui import router as ui_router
from dtmo.ux_preferences import router as ux_preferences_router

settings = get_settings()
configure_logging(settings.log_level)
log = get_logger("api")
scheduler = SchedulerService()
REQUESTS = Counter("dtmo_http_requests_total", "HTTP requests", ["method", "route", "status"])
LATENCY = Histogram("dtmo_http_request_seconds", "HTTP request latency", ["method", "route"])
IN_FLIGHT = Gauge("dtmo_http_requests_in_flight", "HTTP requests in flight", ["method"])


def _route_template(request: Request) -> str:
    route = request.scope.get("route")
    route_path = getattr(route, "path", None)
    return route_path if isinstance(route_path, str) else "<unmatched>"


async def run_cisa_kev() -> dict[str, object]:
    result = await CisaKevConnector(settings).run()
    inserted = 0
    indexed = 0
    if result.status == "completed":
        for record in result.records:
            receipt = await ingest_connector_record(result.connector_id, record)
            inserted += int(receipt.inserted)
            indexed += int(receipt.indexed)
    alert = connector_alerts.record(result)
    log.info("connector_run_finished", connector_id=result.connector_id, status=result.status, records=len(result.records), inserted=inserted, indexed=indexed, attempts=result.attempts, alert_state=alert.state, correlation_id=alert.correlation_id)
    return {"connector_id": result.connector_id, "status": result.status, "records": len(result.records), "inserted": inserted, "indexed": indexed, "attempts": result.attempts, "error": result.error, "alert_state": alert.state, "correlation_id": alert.correlation_id}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if settings.feature_live_connectors:
        scheduler.register(ScheduledJob(id="cisa-kev", interval_seconds=settings.connector_poll_seconds, handler=run_cisa_kev))
        scheduler.start()
    yield
    scheduler.shutdown()
    await close_services()


app = FastAPI(title="DTMO API", version="16.0.0rc10", description="Education-focused cyber threat intelligence platform", lifespan=lifespan)
app.include_router(frontend_router)
app.include_router(operations_ui_router)
app.include_router(operations_metrics_router)
app.include_router(threat_workspace_router)
app.include_router(source_center_router)
app.include_router(admin_center_router)
app.include_router(ux_preferences_router)
app.include_router(intelligence_router)
app.include_router(admin_sources_router)
app.include_router(admin_ui_router)
app.include_router(ui_router)
app.include_router(ciso_ui_router)
app.include_router(auditor_ui_router)


@app.middleware("http")
async def request_context(request: Request, call_next):  # type: ignore[no-untyped-def]
    request_id = resolve_correlation_id(request.headers.get("x-correlation-id"))
    correlation_token = correlation_id.set(request_id)
    trace_binding = begin_trace(request.headers.get("traceparent"))
    bind_request_context(request_id, request.method, trace_id=trace_binding.trace_id, span_id=trace_binding.span_id)
    started = perf_counter()
    IN_FLIGHT.labels(request.method).inc()
    try:
        response = await call_next(request)
    except Exception:
        duration = perf_counter() - started
        route = _route_template(request)
        REQUESTS.labels(request.method, route, "500").inc()
        LATENCY.labels(request.method, route).observe(duration)
        api_error_alerts.observe(route, status_code=500, correlation=request_id)
        log.exception("http_request_failed", route=route, status=500, duration_ms=round(duration * 1000, 3))
        raise
    else:
        duration = perf_counter() - started
        route = _route_template(request)
        response.headers["x-correlation-id"] = request_id
        response.headers["x-content-type-options"] = "nosniff"
        response.headers["x-frame-options"] = "DENY"
        response.headers["referrer-policy"] = "no-referrer"
        REQUESTS.labels(request.method, route, str(response.status_code)).inc()
        LATENCY.labels(request.method, route).observe(duration)
        api_error_alerts.observe(route, status_code=response.status_code, correlation=request_id)
        log.info("http_request_completed", route=route, status=response.status_code, duration_ms=round(duration * 1000, 3))
        return response
    finally:
        IN_FLIGHT.labels(request.method).dec()
        clear_request_context()
        end_trace(trace_binding)
        correlation_id.reset(correlation_token)


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "healthy", "version": app.version, "environment": settings.environment, "scheduler": scheduler.status(), "publication_gate": "human-approval-required", "authentication": "api-key-and-rbac"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/connectors")
def connectors() -> list[dict[str, object]]:
    return [{"id": "cisa-kev", "enabled": settings.feature_live_connectors, "reliability": "authoritative", "schedule_seconds": settings.connector_poll_seconds, "manual_run_available": not settings.production or settings.feature_live_connectors}]


@app.post("/connectors/cisa-kev/run")
async def run_connector(principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))]) -> dict[str, object]:
    del principal
    if settings.production and not settings.feature_live_connectors:
        return {"status": "disabled", "reason": "feature flag is off"}
    return await run_cisa_kev()


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
