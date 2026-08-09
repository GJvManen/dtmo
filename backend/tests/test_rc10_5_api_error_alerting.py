from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from fastapi import FastAPI, Response
from fastapi.testclient import TestClient
from prometheus_client import generate_latest

from dtmo.api_alerts import ApiErrorAlertManager
from dtmo.logging import configure_logging
from dtmo.main import request_context


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


def test_three_consecutive_5xx_raise_correlated_api_alert_without_request_data(
    caplog: pytest.LogCaptureFixture,
) -> None:
    configure_logging("INFO")
    caplog.set_level("INFO", logger="api.alerts")
    manager = ApiErrorAlertManager()
    route = "/api/rc10-5/{item_id}"

    first = manager.observe(route, status_code=500, correlation="rc10-5-error-001")
    second = manager.observe(route, status_code=502, correlation="rc10-5-error-002")
    third = manager.observe(route, status_code=503, correlation="rc10-5-error-003")

    assert first.state == second.state == "clear"
    assert first.transitioned is second.transitioned is False
    assert third.state == "active"
    assert third.transitioned is True
    assert third.consecutive_errors == 3
    assert third.correlation_id == "rc10-5-error-003"
    assert third.publish_approved is False

    metrics = generate_latest().decode("utf-8")
    assert f'dtmo_api_error_streak{{route="{route}"}} 3.0' in metrics
    assert f'dtmo_api_error_alert_active{{route="{route}"}} 1.0' in metrics
    assert (
        f'dtmo_api_error_alert_transitions_total{{route="{route}",transition="raised"}} 1.0'
        in metrics
    )

    raised = [event for event in _json_events(caplog) if event.get("event") == "api_error_alert_raised"]
    assert raised
    event = raised[-1]
    assert event["route"] == route
    assert event["correlation_id"] == "rc10-5-error-003"
    assert event["publish_approved"] is False
    serialized = json.dumps(event, sort_keys=True)
    assert "student-record-9981" not in serialized
    assert "token=secret" not in serialized
    assert "authorization" not in serialized.lower()


def test_active_api_alert_requires_two_non_5xx_outcomes_to_clear() -> None:
    manager = ApiErrorAlertManager()
    route = "/api/rc10-5/recovery"

    for status in (500, 500, 500):
        raised = manager.observe(route, status_code=status, correlation="rc10-5-raise-002")
    recovering = manager.observe(route, status_code=200, correlation="rc10-5-recover-002a")
    cleared = manager.observe(route, status_code=204, correlation="rc10-5-recover-002b")

    assert raised.state == "active"
    assert recovering.state == "active"
    assert recovering.transitioned is False
    assert recovering.consecutive_recoveries == 1
    assert cleared.state == "clear"
    assert cleared.transitioned is True
    assert cleared.consecutive_recoveries == 0
    assert cleared.publish_approved is False

    metrics = generate_latest().decode("utf-8")
    assert f'dtmo_api_error_alert_active{{route="{route}"}} 0.0' in metrics
    assert (
        f'dtmo_api_error_alert_transitions_total{{route="{route}",transition="cleared"}} 1.0'
        in metrics
    )


def test_repeated_5xx_while_active_does_not_repeat_raise_transition() -> None:
    manager = ApiErrorAlertManager(raise_after=1)
    route = "/api/rc10-5/no-storm"

    first = manager.observe(route, status_code=500, correlation="rc10-5-first-003")
    second = manager.observe(route, status_code=500, correlation="rc10-5-second-003")

    assert first.state == second.state == "active"
    assert first.transitioned is True
    assert second.transitioned is False


def test_api_error_alert_rejects_raw_url_or_unbounded_route_identifier() -> None:
    manager = ApiErrorAlertManager()

    with pytest.raises(ValueError, match="bounded route template"):
        manager.observe("/api/items/42?token=secret", status_code=500)
    with pytest.raises(ValueError, match="bounded route template"):
        manager.observe("/api/student records/42", status_code=500)


def test_request_middleware_feeds_bounded_route_template_and_recovery() -> None:
    controlled = FastAPI()
    controlled.middleware("http")(request_context)
    state = {"requests": 0}

    @controlled.get("/rc10-5/controlled/{item_id}")
    def controlled_outcome(item_id: str) -> Response:
        del item_id
        state["requests"] += 1
        return Response(status_code=500 if state["requests"] <= 3 else 200)

    with TestClient(controlled) as client:
        for index in range(3):
            response = client.get(
                "/rc10-5/controlled/student-record-9981?token=secret",
                headers={"x-correlation-id": f"rc10-5-http-error-{index}"},
            )
            assert response.status_code == 500
            assert response.headers["x-correlation-id"] == f"rc10-5-http-error-{index}"

        metrics = generate_latest().decode("utf-8")
        route = "/rc10-5/controlled/{item_id}"
        assert f'dtmo_api_error_alert_active{{route="{route}"}} 1.0' in metrics
        assert "student-record-9981" not in metrics
        assert "token=secret" not in metrics

        for index in range(2):
            response = client.get(
                "/rc10-5/controlled/recovered",
                headers={"x-correlation-id": f"rc10-5-http-recovery-{index}"},
            )
            assert response.status_code == 200

        metrics = generate_latest().decode("utf-8")
        assert f'dtmo_api_error_alert_active{{route="{route}"}} 0.0' in metrics


def test_api_error_prometheus_rule_is_actionable_and_hysteretic() -> None:
    contract = yaml.safe_load(Path("ops/prometheus/dtmo-alerts.yml").read_text(encoding="utf-8"))
    api_group = next(group for group in contract["groups"] if group["name"] == "dtmo.api.alerts")
    rule = api_group["rules"][0]

    assert rule["alert"] == "DTMOApiServerErrors"
    assert rule["expr"] == "dtmo_api_error_alert_active == 1"
    assert rule["labels"]["severity"] == "warning"
    assert "3 consecutive HTTP 5xx" in rule["annotations"]["threshold_policy"]
    assert "2 consecutive non-5xx" in rule["annotations"]["threshold_policy"]
    assert "correlated request trace" in rule["annotations"]["action"]
    assert "two consecutive non-5xx" in rule["annotations"]["clear_condition"]
