from __future__ import annotations

from dtmo.dashboards import dashboards_page


def test_dashboard_exposes_real_data_visualizations() -> None:
    body = dashboards_page().body.decode("utf-8")

    assert "RC12.2 graphical dashboards" in body
    assert "/api/v1/dashboards/summary" in body
    assert "Intelligence trend — 7 dagen" in body
    assert "Severity-verdeling" in body
    assert "Reviewstatus" in body
    assert "Top intelligencebronnen" in body
    assert "Connector health" in body
    assert "<svg" in body
    assert "Staafdiagram" in body


def test_dashboard_has_accessible_table_alternatives_and_live_status() -> None:
    body = dashboards_page().body.decode("utf-8")

    assert 'role="status"' in body
    assert 'aria-live="polite"' in body
    assert "chart-table" in body
    assert 'scope="col"' in body
    assert 'role="img"' in body
    assert 'aria-label="Staafdiagram"' in body


def test_dashboard_preserves_read_only_governance_boundary() -> None:
    body = dashboards_page().body.decode("utf-8")

    assert "dashboards zijn read-only" in body
    assert "geen review- of publicatiebevoegdheid" in body
    assert "afzonderlijke menselijke goedkeuring" in body
    assert "X-DTMO-Subject" in body
    assert "X-DTMO-Roles" in body
    assert "X-DTMO-API-Key" in body
    assert "localStorage" not in body
