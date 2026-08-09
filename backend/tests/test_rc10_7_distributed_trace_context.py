from __future__ import annotations

import json

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from prometheus_client import generate_latest

from dtmo.config import Settings
from dtmo.connectors.base import Connector, ConnectorRecord
from dtmo.logging import configure_logging
from dtmo.main import request_context
from dtmo.trace_context import (
    begin_trace,
    end_trace,
    outbound_traceparent,
    parse_traceparent,
)

VALID_TRACE_ID = "0af7651916cd43dd8448eb211c80319c"
VALID_PARENT_ID = "b7ad6b7169203331"
VALID = f"00-{VALID_TRACE_ID}-{VALID_PARENT_ID}-01"


class TraceProbeConnector(Connector):
    id = "trace-probe"

    def __init__(self, settings: Settings) -> None:
        super().__init__(settings)
        self.observed_traceparent: str | None = None

    async def fetch(self, client: httpx.AsyncClient) -> object:
        self.observed_traceparent = client.headers.get("traceparent")
        return {}

    def parse(self, payload: object) -> list[ConnectorRecord]:
        del payload
        return []


def _json_events(caplog: pytest.LogCaptureFixture) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for record in caplog.records:
        try:
            payload = json.loads(record.getMessage())
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events


def test_valid_w3c_traceparent_preserves_trace_id_and_creates_child_span() -> None:
    binding = begin_trace(VALID)
    try:
        assert binding.incoming_accepted is True
        assert binding.trace_id == VALID_TRACE_ID
        assert binding.span_id != VALID_PARENT_ID
        assert len(binding.span_id) == 16
        child = parse_traceparent(outbound_traceparent())
        assert child is not None
        child_trace_id, child_span_id, flags = child
        assert child_trace_id == VALID_TRACE_ID
        assert child_span_id != binding.span_id
        assert flags == "01"
    finally:
        end_trace(binding)


@pytest.mark.parametrize(
    "value",
    [
        "00-00000000000000000000000000000000-b7ad6b7169203331-01",
        "00-0af7651916cd43dd8448eb211c80319c-0000000000000000-01",
        "00-0AF7651916CD43DD8448EB211C80319C-b7ad6b7169203331-01",
        "ff-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01",
        "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01-extra",
        "student@example.test",
    ],
)
def test_untrusted_or_malformed_traceparent_is_rejected(value: str) -> None:
    assert parse_traceparent(value) is None
    binding = begin_trace(value)
    try:
        assert binding.incoming_accepted is False
        assert binding.trace_id != value
        assert len(binding.trace_id) == 32
    finally:
        end_trace(binding)


@pytest.mark.asyncio
async def test_outbound_connector_propagates_same_trace_without_request_payload() -> None:
    binding = begin_trace(VALID)
    try:
        connector = TraceProbeConnector(Settings(environment="test", connector_max_attempts=1))
        result = await connector.run()
        assert result.status == "completed"
        assert connector.observed_traceparent is not None
        parsed = parse_traceparent(connector.observed_traceparent)
        assert parsed is not None
        propagated_trace_id, _child_span_id, flags = parsed
        assert propagated_trace_id == VALID_TRACE_ID
        assert flags == "01"
        assert "student" not in connector.observed_traceparent
    finally:
        end_trace(binding)


def test_request_logs_bind_trace_and_do_not_echo_trace_headers_or_request_values(
    caplog: pytest.LogCaptureFixture,
) -> None:
    configure_logging("INFO")
    caplog.set_level("INFO")
    test_app = FastAPI()
    test_app.middleware("http")(request_context)

    @test_app.get("/trace/{record_id}")
    def traced(record_id: str) -> dict[str, str]:
        return {"record_id": record_id}

    secret_path = "student-secret-4711"
    secret_query = "token-do-not-log"
    with TestClient(test_app) as client:
        response = client.get(
            f"/trace/{secret_path}?access={secret_query}",
            headers={"traceparent": VALID, "tracestate": "vendor=private-value"},
        )

    assert response.status_code == 200
    assert "traceparent" not in response.headers
    events = _json_events(caplog)
    completed = [event for event in events if event.get("event") == "http_request_completed"]
    assert completed
    event = completed[-1]
    assert event["route"] == "/trace/{record_id}"
    assert event["trace_id"] == VALID_TRACE_ID
    assert isinstance(event["span_id"], str) and len(event["span_id"]) == 16
    serialized = json.dumps(event, sort_keys=True)
    assert secret_path not in serialized
    assert secret_query not in serialized
    assert "private-value" not in serialized
    assert VALID not in serialized


def test_trace_context_metrics_record_only_bounded_decisions() -> None:
    binding = begin_trace(VALID)
    end_trace(binding)
    rejected = begin_trace("malicious trace header with spaces")
    end_trace(rejected)
    metrics = generate_latest().decode("utf-8")
    assert 'dtmo_trace_context_total{decision="accepted"}' in metrics
    assert 'dtmo_trace_context_total{decision="rejected"}' in metrics
    assert VALID not in metrics
    assert "malicious trace header with spaces" not in metrics
