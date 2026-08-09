from __future__ import annotations

import json
from uuid import UUID

import pytest
import structlog
from fastapi.testclient import TestClient

from dtmo import main
from dtmo.logging import bind_request_context, clear_request_context, resolve_correlation_id


def test_resolve_correlation_id_accepts_bounded_safe_value() -> None:
    assert resolve_correlation_id("phase7.request-001") == "phase7.request-001"


def test_resolve_correlation_id_replaces_unsafe_value() -> None:
    generated = resolve_correlation_id("unsafe correlation id with spaces")
    UUID(generated)


def test_structlog_request_context_contains_correlation_id_and_method() -> None:
    clear_request_context()
    bind_request_context("phase7-context-001", "GET")
    try:
        context = structlog.contextvars.get_contextvars()
        assert context["correlation_id"] == "phase7-context-001"
        assert context["method"] == "GET"
    finally:
        clear_request_context()


def test_request_observability_emits_correlated_log_and_route_metrics(
    caplog: pytest.LogCaptureFixture,
) -> None:
    request_id = "phase7-health-001"
    caplog.set_level("INFO", logger="api")
    caplog.clear()

    with TestClient(main.app) as client:
        response = client.get("/health", headers={"x-correlation-id": request_id})
        metrics = client.get("/metrics").text

    assert response.status_code == 200
    assert response.headers["x-correlation-id"] == request_id
    assert 'dtmo_http_requests_total{method="GET",route="/health",status="200"}' in metrics
    assert 'dtmo_http_request_seconds_count{method="GET",route="/health"}' in metrics

    payloads: list[dict[str, object]] = []
    for record in caplog.records:
        try:
            payload = json.loads(record.getMessage())
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            payloads.append(payload)

    health_events = [
        payload
        for payload in payloads
        if payload.get("event") == "http_request_completed" and payload.get("route") == "/health"
    ]
    assert health_events
    assert health_events[-1]["correlation_id"] == request_id
    assert health_events[-1]["method"] == "GET"
    assert health_events[-1]["status"] == 200


def test_request_observability_rejects_unsafe_inbound_correlation_id() -> None:
    with TestClient(main.app) as client:
        response = client.get(
            "/health",
            headers={"x-correlation-id": "unsafe correlation id with spaces"},
        )

    assert response.status_code == 200
    assert response.headers["x-correlation-id"] != "unsafe correlation id with spaces"
    UUID(response.headers["x-correlation-id"])
