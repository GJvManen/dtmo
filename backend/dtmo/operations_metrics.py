from __future__ import annotations

from collections.abc import AsyncIterator, Iterable
from typing import Annotated

from fastapi import APIRouter, Depends
from prometheus_client import REGISTRY
from prometheus_client.samples import Sample
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.connectors.state import ConnectorHealthEvent, ConnectorRuntimeState, as_utc
from dtmo.persistence.session import Database

router = APIRouter(prefix="/api/v1/operations", tags=["operations"])
database = Database()

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


async def get_session() -> AsyncIterator[AsyncSession]:
    async for session in database.session():
        yield session


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


def _timestamp(value: object) -> str | None:
    if value is None:
        return None
    return as_utc(value).isoformat()  # type: ignore[arg-type]


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


@router.get("/runtime-evidence")
async def operations_runtime_evidence(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, object]:
    """Expose bounded persisted connector runtime evidence for canonical Operations.

    This endpoint is deliberately read-only. It reports durable DTMO connector state
    and recent run observations without returning raw quarantined evidence, connector
    credentials, or any execution/configuration authority.
    """

    states = list(
        await session.scalars(
            select(ConnectorRuntimeState).order_by(ConnectorRuntimeState.connector_id.asc())
        )
    )
    recent_runs = list(
        await session.scalars(
            select(ConnectorHealthEvent)
            .order_by(ConnectorHealthEvent.observed_at.desc())
            .limit(25)
        )
    )
    return {
        "evidence_source": "dtmo-persistent-connector-runtime-state",
        "state_table": "connector_runtime_states",
        "history_table": "connector_health_events",
        "connector_states": [
            {
                "connector_id": state.connector_id,
                "health_status": state.health_status,
                "last_run_id": str(state.last_run_id) if state.last_run_id else None,
                "last_success_at": _timestamp(state.last_success_at),
                "last_failure_at": _timestamp(state.last_failure_at),
                "consecutive_failures": state.consecutive_failures,
                "circuit_open_until": _timestamp(state.circuit_open_until),
                "updated_at": _timestamp(state.updated_at),
            }
            for state in states
        ],
        "recent_runs": [
            {
                "connector_id": run.connector_id,
                "run_id": str(run.run_id),
                "observed_at": _timestamp(run.observed_at),
                "status": run.status,
                "duration_seconds": run.duration_seconds,
                "record_count": run.record_count,
                "quarantine_count": run.quarantine_count,
                "error_code": run.error_code,
                "publish_approved": run.publish_approved,
            }
            for run in recent_runs
        ],
        "claim_boundary": (
            "Persisted DTMO runtime observations are operational evidence only; they do not prove live "
            "upstream availability, absence of incidents, production assurance, or publication authority."
        ),
    }
