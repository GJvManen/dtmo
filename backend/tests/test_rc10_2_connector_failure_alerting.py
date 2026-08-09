from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from prometheus_client import generate_latest

from dtmo.alerts import ConnectorAlertManager
from dtmo.connectors.base import ConnectorResult
from dtmo.logging import configure_logging, correlation_id


def _result(*, connector_id: str, status: str, error: str | None = None) -> ConnectorResult:
    return ConnectorResult(
        connector_id=connector_id,
        started_at="2026-08-09T15:45:00+00:00",
        finished_at="2026-08-09T15:45:01+00:00",
        records=[],
        attempts=3 if status == "failed" else 1,
        status=status,
        error=error,
    )


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


def test_terminal_failure_raises_actionable_correlated_alert_and_metric(
    caplog: pytest.LogCaptureFixture,
) -> None:
    configure_logging("INFO")
    caplog.set_level("INFO", logger="connector.alerts")
    manager = ConnectorAlertManager()
    connector_id = "rc10-2-controlled-failure"
    token = correlation_id.set("rc10-2-correlation-001")
    try:
        signal = manager.record(
            _result(
                connector_id=connector_id,
                status="failed",
                error="token=must-not-appear-in-alert-log",
            )
        )
    finally:
        correlation_id.reset(token)

    assert signal.state == "active"
    assert signal.transitioned is True
    assert signal.correlation_id == "rc10-2-correlation-001"
    assert signal.action
    assert signal.publish_approved is False

    metrics = generate_latest().decode("utf-8")
    assert f'dtmo_connector_alert_active{{connector="{connector_id}"}} 1.0' in metrics
    assert (
        f'dtmo_connector_alert_transitions_total{{connector="{connector_id}",transition="raised"}} 1.0'
        in metrics
    )

    raised = [event for event in _json_events(caplog) if event.get("event") == "connector_alert_raised"]
    assert raised
    assert raised[-1]["connector_id"] == connector_id
    assert raised[-1]["correlation_id"] == "rc10-2-correlation-001"
    assert raised[-1]["severity"] == "warning"
    assert raised[-1]["publish_approved"] is False
    assert "credentials" in str(raised[-1]["action"])
    assert "must-not-appear-in-alert-log" not in json.dumps(raised[-1])


def test_success_after_failure_clears_alert_with_correlation_evidence(
    caplog: pytest.LogCaptureFixture,
) -> None:
    configure_logging("INFO")
    caplog.set_level("INFO", logger="connector.alerts")
    manager = ConnectorAlertManager()
    connector_id = "rc10-2-controlled-recovery"

    failed = manager.record(
        _result(connector_id=connector_id, status="failed", error="upstream unavailable"),
        correlation="rc10-2-failure-002",
    )
    cleared = manager.record(
        _result(connector_id=connector_id, status="completed"),
        correlation="rc10-2-recovery-002",
    )

    assert failed.state == "active"
    assert cleared.state == "clear"
    assert cleared.transitioned is True
    assert cleared.correlation_id == "rc10-2-recovery-002"
    assert cleared.publish_approved is False

    metrics = generate_latest().decode("utf-8")
    assert f'dtmo_connector_alert_active{{connector="{connector_id}"}} 0.0' in metrics
    assert (
        f'dtmo_connector_alert_transitions_total{{connector="{connector_id}",transition="cleared"}} 1.0'
        in metrics
    )

    cleared_events = [
        event for event in _json_events(caplog) if event.get("event") == "connector_alert_cleared"
    ]
    assert cleared_events
    assert cleared_events[-1]["correlation_id"] == "rc10-2-recovery-002"
    assert cleared_events[-1]["publish_approved"] is False


def test_repeated_terminal_failure_does_not_repeat_raise_transition() -> None:
    manager = ConnectorAlertManager()
    connector_id = "rc10-2-no-alert-storm"

    first = manager.record(_result(connector_id=connector_id, status="failed", error="first"))
    second = manager.record(_result(connector_id=connector_id, status="failed", error="second"))

    assert first.transitioned is True
    assert second.transitioned is False
    assert first.state == second.state == "active"


def test_prometheus_alert_rule_is_actionable_and_clears_from_metric() -> None:
    contract = yaml.safe_load(Path("ops/prometheus/dtmo-alerts.yml").read_text(encoding="utf-8"))
    rule = contract["groups"][0]["rules"][0]

    assert rule["alert"] == "DTMOConnectorFailure"
    assert rule["expr"] == "dtmo_connector_alert_active == 1"
    assert rule["labels"]["severity"] == "warning"
    assert "Inspect connector health" in rule["annotations"]["action"]
    assert "successful connector run" in rule["annotations"]["clear_condition"]
