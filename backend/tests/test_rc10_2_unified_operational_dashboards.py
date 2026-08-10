from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from dtmo.main import app

ROOT = Path(__file__).resolve().parents[2]
OPS = ROOT / "backend/dtmo/operations_ui.py"
METRICS = ROOT / "backend/dtmo/operations_metrics.py"


def test_operations_summary_is_read_only_and_aggregated() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/operations/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["metric_source"] == "prometheus-client-registry"
    assert set(payload["alerts"]) == {"api_error", "connector", "storage_integrity", "search_health"}
    for field in ("request_count", "in_flight", "average_latency_ms", "active_alerts", "queue_backlog_ratio", "trace_context_total", "connector_runs_total"):
        assert field in payload


def test_operations_summary_does_not_expose_sensitive_dimensions() -> None:
    text = METRICS.read_text(encoding="utf-8").lower()
    for forbidden in ("request_body", "response_body", "authorization", "cookie", "query_string", "student_id", "object_key"):
        assert forbidden not in text


def test_operations_dashboard_uses_real_summary_and_no_placeholder_chart() -> None:
    text = OPS.read_text(encoding="utf-8")
    assert "fetch('/api/v1/operations/summary'" in text
    assert "Operational snapshot" in text
    assert "Momentopname uit de in-process Prometheus registry" in text
    assert "ops-placeholder-chart" not in text
    assert "geen synthetische waarden" in text


def test_dashboard_remains_read_only_and_accessible() -> None:
    text = OPS.read_text(encoding="utf-8")
    assert 'href="#main"' in text
    assert 'aria-label="Live operationele metrics"' in text
    assert "prefers-reduced-motion" in text
    assert "@media(max-width:760px)" in text
    assert "method:'POST'" not in text
    assert "method: 'POST'" not in text
