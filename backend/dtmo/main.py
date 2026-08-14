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
from dtmo.analytics_experience import router as analytics_experience_router
from dtmo.api.routes import close_services, ingest_connector_record, router as intelligence_router
from dtmo.api_alerts import api_error_alerts
from dtmo.auditor_ui import router as auditor_ui_router
from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.ciso_ui import router as ciso_ui_router
from dtmo.config import get_settings
from dtmo.connectors.cisa_kev import CisaKevConnector
from dtmo.connectors.opencve import OpenCVEConnector
from dtmo.connectors.vulnerability_lookup import VulnerabilityLookupConnector
from dtmo.dashboards import router as dashboards_router
from dtmo.framework_experience import router as framework_experience_router
from dtmo.framework_governance import router as framework_governance_router
from dtmo.frontend import router as frontend_router
from dtmo.governance_crosswalk import router as governance_crosswalk_router
from dtmo.governance_crosswalk_experience import router as governance_crosswalk_experience_router
from dtmo.governance_knowledge import router as governance_knowledge_router
from dtmo.logging import bind_request_context, clear_request_context, configure_logging, correlation_id, get_logger, resolve_correlation_id
from dtmo.operations_metrics import router as operations_metrics_router
from dtmo.operations_ui import router as operations_ui_router
from dtmo.rbac_admin import router as rbac_admin_router
from dtmo.rbac_management_experience import router as rbac_management_experience_router
from dtmo.rc13_administration import router as rc13_administration_router
from dtmo.rc13_analytics import router as rc13_analytics_router
from dtmo.rc13_governance import router as rc13_governance_router
from dtmo.scheduler import ScheduledJob, SchedulerService
from dtmo.severity_experience import router as severity_experience_router
from dtmo.source_center import router as source_center_router
from dtmo.source_onboarding_experience import router as source_onboarding_experience_router
from dtmo.threat_workspace import router as threat_workspace_router
from dtmo.trace_context import begin_trace, end_trace
from dtmo.ui import router as ui_router
from dtmo.unified_console import router as unified_console_router
from dtmo.ux_preferences import router as ux_preferences_router
from dtmo.vulnerability_console import router as vulnerability_console_router
from dtmo.vulnerability_console_ui import router as vulnerability_console_ui_router

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


async def _persist_connector_result(connector: CisaKevConnector | OpenCVEConnector | VulnerabilityLookupConnector) -> dict[str, object]:
    result = await connector.run()
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


async def run_cisa_kev() -> dict[str, object]:
    return await _persist_connector_result(CisaKevConnector(settings))


async def run_opencve() -> dict[str, object]:
    return await _persist_connector_result(OpenCVEConnector(settings))


async def run_vulnerability_lookup() -> dict[str, object]:
    return await _persist_connector_result(VulnerabilityLookupConnector(settings))


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    if settings.feature_live_connectors:
        scheduler.register(ScheduledJob(id="cisa-kev", interval_seconds=settings.connector_poll_seconds, handler=run_cisa_kev))
        if settings.feature_opencve_connector:
            scheduler.register(ScheduledJob(id="opencve", interval_seconds=settings.connector_poll_seconds, handler=run_opencve))
        if settings.feature_vulnerability_lookup_connector:
            scheduler.register(ScheduledJob(id="vulnerability-lookup", interval_seconds=settings.connector_poll_seconds, handler=run_vulnerability_lookup))
        scheduler.start()
    yield
    scheduler.shutdown()
    await close_services()


app = FastAPI(title="DTMO API", version="16.0.0rc12", description="Education-focused cyber threat intelligence platform", lifespan=lifespan)
app.include_router(vulnerability_console_ui_router)
app.include_router(rbac_management_experience_router)
app.include_router(source_onboarding_experience_router)
app.include_router(governance_crosswalk_experience_router)
app.include_router(framework_experience_router)
app.include_router(analytics_experience_router)
app.include_router(severity_experience_router)
app.include_router(rc13_governance_router)
app.include_router(rc13_administration_router)
app.include_router(vulnerability_console_router)
app.include_router(unified_console_router)
app.include_router(rc13_analytics_router)
app.include_router(frontend_router)
app.include_router(operations_ui_router)
app.include_router(operations_metrics_router)
app.include_router(dashboards_router)
app.include_router(threat_workspace_router)
app.include_router(source_center_router)
app.include_router(admin_center_router)
app.include_router(ux_preferences_router)
app.include_router(intelligence_router)
app.include_router(admin_sources_router)
app.include_router(rbac_admin_router)
app.include_router(governance_knowledge_router)
app.include_router(governance_crosswalk_router)
app.include_router(framework_governance_router)
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
    return [
        {"id": "cisa-kev", "enabled": settings.feature_live_connectors, "reliability": "authoritative", "schedule_seconds": settings.connector_poll_seconds, "manual_run_available": not settings.production or settings.feature_live_connectors},
        {"id": "opencve", "enabled": settings.feature_live_connectors and settings.feature_opencve_connector, "reliability": "trusted", "schedule_seconds": settings.connector_poll_seconds, "manual_run_available": settings.feature_opencve_connector, "api_version": "v2"},
        {"id": "vulnerability-lookup", "enabled": settings.feature_live_connectors and settings.feature_vulnerability_lookup_connector, "reliability": "trusted", "schedule_seconds": settings.connector_poll_seconds, "manual_run_available": settings.feature_vulnerability_lookup_connector, "api_version": "public API"},
    ]


@app.post("/connectors/cisa-kev/run")
async def run_connector(principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))]) -> dict[str, object]:
    del principal
    if settings.production and not settings.feature_live_connectors:
        return {"status": "disabled", "reason": "feature flag is off"}
    return await run_cisa_kev()


@app.post("/connectors/opencve/run")
async def run_opencve_connector(principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))]) -> dict[str, object]:
    del principal
    if not settings.feature_opencve_connector:
        return {"status": "disabled", "reason": "OpenCVE connector feature flag is off"}
    return await run_opencve()


@app.post("/connectors/vulnerability-lookup/run")
async def run_vulnerability_lookup_connector(principal: Annotated[Principal, Depends(require_permission(Permission.MANAGE_CONNECTORS))]) -> dict[str, object]:
    del principal
    if not settings.feature_vulnerability_lookup_connector:
        return {"status": "disabled", "reason": "Vulnerability-Lookup connector feature flag is off"}
    return await run_vulnerability_lookup()


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
