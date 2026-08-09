from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = ROOT / "infrastructure/grafana/dashboards/dtmo-operations.json"
DATASOURCE = ROOT / "infrastructure/grafana/provisioning/datasources/dtmo-prometheus.yml"
PROVIDER = ROOT / "infrastructure/grafana/provisioning/dashboards/dtmo.yml"
OVERLAY = ROOT / "docker-compose.observability.yml"


def _dashboard() -> dict[str, object]:
    value = json.loads(DASHBOARD.read_text())
    assert isinstance(value, dict)
    return value


def _expressions() -> list[str]:
    expressions: list[str] = []
    for panel in _dashboard()["panels"]:
        assert isinstance(panel, dict)
        for target in panel.get("targets", []):
            assert isinstance(target, dict)
            expression = target.get("expr")
            if isinstance(expression, str):
                expressions.append(expression)
    return expressions


def test_dashboard_is_read_only_and_uses_provisioned_prometheus_only() -> None:
    dashboard = _dashboard()
    assert dashboard["uid"] == "dtmo-operations"
    assert dashboard["editable"] is False
    panels = dashboard["panels"]
    assert isinstance(panels, list) and len(panels) >= 8
    for panel in panels:
        assert isinstance(panel, dict)
        datasource = panel["datasource"]
        assert datasource == {"type": "prometheus", "uid": "dtmo-prometheus"}


def test_dashboard_covers_release_critical_operational_signals() -> None:
    joined = "\n".join(_expressions())
    for metric in (
        "dtmo_http_requests_total",
        "dtmo_http_request_seconds_bucket",
        "dtmo_http_requests_in_flight",
        "dtmo_api_error_alert_active",
        "dtmo_connector_alert_active",
        "dtmo_queue_backlog_utilization_ratio",
        "dtmo_storage_integrity_alert_active",
        "dtmo_search_health_alert_active",
        "dtmo_trace_context_total",
        "dtmo_connector_runs_total",
    ):
        assert metric in joined


def test_dashboard_queries_do_not_request_sensitive_or_unbounded_request_dimensions() -> None:
    query_text = "\n".join(_expressions()).lower()
    for forbidden in (
        "request_body",
        "response_body",
        "request_uri",
        "raw_url",
        "query_string",
        "authorization",
        "cookie",
        "email",
        "student_id",
        "object_key",
        "checksum",
    ):
        assert forbidden not in query_text


def test_provisioning_is_non_editable_and_contains_no_credentials() -> None:
    datasource = yaml.safe_load(DATASOURCE.read_text())
    provider = yaml.safe_load(PROVIDER.read_text())
    ds = datasource["datasources"][0]
    assert ds["uid"] == "dtmo-prometheus"
    assert ds["url"] == "http://prometheus:9090"
    assert ds["editable"] is False
    configured = provider["providers"][0]
    assert configured["editable"] is False
    assert configured["disableDeletion"] is True
    text = DATASOURCE.read_text().lower() + PROVIDER.read_text().lower()
    assert "password" not in text
    assert "token" not in text
    assert "api_key" not in text


def test_observability_overlay_fails_closed_and_disables_anonymous_access() -> None:
    text = OVERLAY.read_text()
    assert "${GRAFANA_IMAGE:?" in text
    assert "@sha256:<vendor-verified-digest>" in text
    assert "${GRAFANA_ADMIN_USER:?" in text
    assert "${GRAFANA_ADMIN_PASSWORD:?" in text
    assert 'GF_AUTH_ANONYMOUS_ENABLED: "false"' in text
    assert 'GF_USERS_ALLOW_SIGN_UP: "false"' in text
    assert '127.0.0.1:3000:3000' in text
    assert "no-new-privileges:true" in text
    assert "grafana/grafana:latest" not in text
