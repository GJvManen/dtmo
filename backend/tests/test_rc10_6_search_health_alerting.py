from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
import yaml
from prometheus_client import generate_latest

from dtmo.logging import configure_logging
from dtmo.search_alerts import SearchHealthAlertManager, probe_opensearch_health


def _events(caplog: pytest.LogCaptureFixture) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for record in caplog.records:
        try:
            value = json.loads(record.getMessage())
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            out.append(value)
    return out


def test_two_red_checks_raise_correlated_alert_without_search_data(caplog: pytest.LogCaptureFixture) -> None:
    configure_logging("INFO")
    caplog.set_level("INFO", logger="search.alerts")
    manager = SearchHealthAlertManager()
    first = manager.observe("primary-search", health_status="red", correlation="rc10-6-001")
    second = manager.observe("primary-search", health_status="red", correlation="rc10-6-002")
    assert first.state == "clear"
    assert second.state == "active" and second.transitioned is True
    assert second.publish_approved is False
    metrics = generate_latest().decode()
    assert 'dtmo_search_health_alert_active{cluster="primary-search"} 1.0' in metrics
    raised = [event for event in _events(caplog) if event.get("event") == "search_health_alert_raised"]
    assert raised[-1]["correlation_id"] == "rc10-6-002"
    text = json.dumps(raised[-1], sort_keys=True)
    assert "query=" not in text and "_source" not in text and "student" not in text


def test_active_alert_requires_two_healthy_checks_to_clear() -> None:
    manager = SearchHealthAlertManager()
    manager.observe("primary-search", health_status="unreachable", correlation="a")
    raised = manager.observe("primary-search", health_status="unreachable", correlation="b")
    recovering = manager.observe("primary-search", health_status="yellow", correlation="c")
    cleared = manager.observe("primary-search", health_status="green", correlation="d")
    assert raised.state == "active" and raised.transitioned is True
    assert recovering.state == "active" and recovering.transitioned is False
    assert cleared.state == "clear" and cleared.transitioned is True


def test_repeat_unhealthy_does_not_repeat_raise_transition() -> None:
    manager = SearchHealthAlertManager(raise_after=1)
    first = manager.observe("primary-search", health_status="red")
    second = manager.observe("primary-search", health_status="red")
    assert first.transitioned is True
    assert second.transitioned is False


@pytest.mark.asyncio
async def test_probe_returns_only_bounded_cluster_health_status() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/_cluster/health"
        return httpx.Response(200, json={"status": "green", "cluster_name": "secret-cluster-detail"})
    status = await probe_opensearch_health("https://search.example.test", transport=httpx.MockTransport(handler))
    assert status == "green"


@pytest.mark.asyncio
async def test_probe_maps_http_failure_to_unreachable_without_body() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="sensitive backend diagnostics must not escape")
    status = await probe_opensearch_health("https://search.example.test", transport=httpx.MockTransport(handler))
    assert status == "unreachable"


def test_search_health_prometheus_rule_is_actionable_and_hysteretic() -> None:
    contract = yaml.safe_load(Path("ops/prometheus/dtmo-alerts.yml").read_text(encoding="utf-8"))
    group = next(group for group in contract["groups"] if group["name"] == "dtmo.search.alerts")
    rule = group["rules"][0]
    assert rule["alert"] == "DTMOSearchHealthFailure"
    assert rule["expr"] == "dtmo_search_health_alert_active == 1"
    assert "2 consecutive red/unreachable" in rule["annotations"]["threshold_policy"]
    assert "two consecutive green/yellow" in rule["annotations"]["clear_condition"]
