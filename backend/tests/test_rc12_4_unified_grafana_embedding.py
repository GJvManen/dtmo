from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_unified_console_embeds_both_grafana_dashboards() -> None:
    page = (ROOT / "backend/dtmo/unified_console.py").read_text()

    assert 'id="grafana-operations"' in page
    assert 'id="grafana-intelligence"' in page
    assert "/d/dtmo-operations/dtmo-operations" in page
    assert "/d/dtmo-intelligence/dtmo-intelligence" in page
    assert 'data-view-panel="analytics"' in page
    assert "Native console summary" in page
    assert 'id="severity-chart"' in page
    assert 'id="source-chart"' in page
    assert 'id="connector-chart"' in page


def test_grafana_embedding_keeps_anonymous_access_disabled() -> None:
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
    grafana = compose["services"]["grafana"]

    assert grafana["environment"]["GF_AUTH_ANONYMOUS_ENABLED"] == "false"
    assert grafana["environment"]["GF_SECURITY_ALLOW_EMBEDDING"] == "true"


def test_unified_console_does_not_navigate_operators_to_grafana() -> None:
    page = (ROOT / "backend/dtmo/unified_console.py").read_text()

    assert "window.location" not in page
    assert "location.href" not in page
    assert "target=\"_blank\"" not in page
    assert "Grafana blijft afzonderlijk geauthenticeerd" in page
