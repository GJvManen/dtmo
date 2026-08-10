from __future__ import annotations

from collections.abc import Iterable

from fastapi import APIRouter
from prometheus_client import REGISTRY
from prometheus_client.samples import Sample

router = APIRouter(prefix="/api/v1/operations", tags=["operations"])

_ALLOWED_METRICS = {
    "dtmo_http_requests_total",
    "dtmo_http_request_seconds_count",
    "dtmo_http_request_seconds_sum",
    "dtmo_http_requests_in_flight",
    "dtmo_api_error_alert_active",
    "dtmo_connector_alert_active",
    "dtmo_queue_backlog_utilization_ratio",
    "dtmo_storage_integrity_alert_active",
    "dtmo_search_health_alert_active",
    "dtmo_trace_context_total",
    "dtmo_connector_runs_total",
}


def _samples() -> Iterable[Sample]:
    for metric in REGISTRY.collect():
        for sample in metric.samples:
            if sample.name in _ALLOWED_METRICS:
                yield sample


def _aggregate() -> dict[str, float]:
    values = {name: 0.0 for name in _ALLOWED_METRICS}
    for sample in _samples():
        values[sample.name] += float(sample.value)
    return values


@router.get("/summary")
def operations_summary() -> dict[str, object]:
    values = _aggregate()
    request_count = values["dtmo_http_request_seconds_count"]
    latency_sum = values["dtmo_http_request_seconds_sum"]
    average_latency_ms = (latency_sum / request_count * 1000.0) if request_count else 0.0
    alert_count = sum(
        1
        for name in (
            "dtmo_api_error_alert_active",
            "dtmo_connector_alert_active",
            "dtmo_storage_integrity_alert_active",
            "dtmo_search_health_alert_active",
        )
        if values[name] > 0
    )
    backlog_ratio = max(0.0, min(1.0, values["dtmo_queue_backlog_utilization_ratio"]))
    return {
        "metric_source": "prometheus-client-registry",
        "request_count": values["dtmo_http_requests_total"],
        "in_flight": values["dtmo_http_requests_in_flight"],
        "average_latency_ms": round(average_latency_ms, 3),
        "active_alerts": alert_count,
        "queue_backlog_ratio": round(backlog_ratio, 4),
        "trace_context_total": values["dtmo_trace_context_total"],
        "connector_runs_total": values["dtmo_connector_runs_total"],
        "alerts": {
            "api_error": values["dtmo_api_error_alert_active"] > 0,
            "connector": values["dtmo_connector_alert_active"] > 0,
            "storage_integrity": values["dtmo_storage_integrity_alert_active"] > 0,
            "search_health": values["dtmo_search_health_alert_active"] > 0,
        },
    }
