from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_reporting_migration_exposes_only_safe_views() -> None:
    migration = (ROOT / "database/migrations/versions/0008_grafana_reporting_views.py").read_text()

    assert 'down_revision: str | None = "0007_source_registry"' in migration
    assert "CREATE SCHEMA dtmo_reporting" in migration
    assert "dtmo_reporting.intelligence_items_safe" in migration
    assert "dtmo_reporting.connector_health_safe" in migration
    assert "summary" not in migration
    assert "metadata_json" not in migration
    assert "raw_evidence" not in migration
    assert "provenance_records" not in migration


def test_grafana_reader_provisioning_is_least_privilege() -> None:
    script = (ROOT / "tools/provision_grafana_reader.py").read_text()

    assert 'ROLE_NAME = "dtmo_grafana_reader"' in script
    assert 'REPORTING_SCHEMA = "dtmo_reporting"' in script
    assert "NOSUPERUSER" in script
    assert "NOCREATEDB" in script
    assert "NOCREATEROLE" in script
    assert "NOINHERIT" in script
    assert "REVOKE ALL ON SCHEMA public" in script
    assert "GRANT SELECT ON" in script
    assert "GRANT SELECT ON ALL TABLES IN SCHEMA public" not in script
    assert "GRAFANA_DB_PASSWORD" in script
    assert "change-me" not in script


def test_grafana_postgres_datasource_uses_runtime_secret_and_readonly_user() -> None:
    config = yaml.safe_load(
        (ROOT / "infrastructure/grafana/provisioning/datasources/dtmo-postgres.yml").read_text()
    )
    datasource = config["datasources"][0]

    assert datasource["type"] == "postgres"
    assert datasource["uid"] == "dtmo-postgres-readonly"
    assert datasource["user"] == "dtmo_grafana_reader"
    assert datasource["editable"] is False
    assert datasource["isDefault"] is False
    assert datasource["secureJsonData"]["password"] == "$__env{GRAFANA_DB_PASSWORD}"
    assert datasource["jsonData"]["database"] == "dtmo"
    assert datasource["jsonData"]["maxOpenConns"] == 10


def test_intelligence_dashboard_queries_reporting_views_only() -> None:
    dashboard = json.loads(
        (ROOT / "infrastructure/grafana/dashboards/dtmo-intelligence.json").read_text()
    )
    queries = [
        target["rawSql"]
        for panel in dashboard["panels"]
        for target in panel.get("targets", [])
        if "rawSql" in target
    ]

    assert dashboard["uid"] == "dtmo-intelligence"
    assert dashboard["editable"] is False
    assert len(queries) >= 7
    assert all("dtmo_reporting." in query for query in queries)
    assert all("public." not in query for query in queries)
    assert all("provenance_records" not in query for query in queries)
    assert all("metadata_json" not in query for query in queries)


def test_compose_provisions_reader_before_grafana_starts() -> None:
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text())
    services = compose["services"]

    provision = services["grafana-db-provision"]
    grafana = services["grafana"]
    assert provision["command"] == ["python", "tools/provision_grafana_reader.py"]
    assert provision["read_only"] is True
    assert "GRAFANA_DB_PASSWORD" in provision["environment"]
    assert grafana["depends_on"]["grafana-db-provision"]["condition"] == "service_completed_successfully"
    assert "GRAFANA_DB_PASSWORD" in grafana["environment"]
