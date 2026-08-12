from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "docker-compose.yml"
DATASOURCE_DIR = ROOT / "infrastructure/grafana/provisioning/datasources"
DATASOURCE = DATASOURCE_DIR / "dtmo-prometheus.yml"
PROVIDER = ROOT / "infrastructure/grafana/provisioning/dashboards/dtmo.yml"
DASHBOARD = ROOT / "infrastructure/grafana/dashboards/dtmo-operations.json"
ENV_EXAMPLE = ROOT / ".env.example"


def test_grafana_is_self_hosted_fail_closed_and_version_pinned() -> None:
    compose = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    grafana = compose["services"]["grafana"]
    assert grafana["image"] == "grafana/grafana:13.1.0"
    assert grafana["environment"]["GF_AUTH_ANONYMOUS_ENABLED"] == "false"
    assert "GRAFANA_ADMIN_USER:?" in grafana["environment"]["GF_SECURITY_ADMIN_USER"]
    assert "GRAFANA_ADMIN_PASSWORD:?" in grafana["environment"]["GF_SECURITY_ADMIN_PASSWORD"]
    assert grafana["security_opt"] == ["no-new-privileges:true"]


def test_prometheus_datasource_is_git_provisioned_and_not_editable() -> None:
    data = yaml.safe_load(DATASOURCE.read_text(encoding="utf-8"))
    source = data["datasources"][0]
    assert source["uid"] == "dtmo-prometheus"
    assert source["type"] == "prometheus"
    assert source["url"] == "http://prometheus:9090"
    assert source["isDefault"] is True
    assert source["editable"] is False


def test_grafana_provisioning_has_only_one_default_datasource_per_org() -> None:
    defaults: list[tuple[int, str, str]] = []
    seen_uids: set[tuple[int, str]] = set()

    for path in sorted(DATASOURCE_DIR.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for source in data.get("datasources", []):
            org_id = int(source.get("orgId", 1))
            uid = str(source["uid"])
            key = (org_id, uid)
            assert key not in seen_uids, f"duplicate datasource uid for org {org_id}: {uid}"
            seen_uids.add(key)
            if source.get("isDefault") is True:
                defaults.append((org_id, uid, path.name))

    defaults_by_org: dict[int, list[tuple[str, str]]] = {}
    for org_id, uid, filename in defaults:
        defaults_by_org.setdefault(org_id, []).append((uid, filename))

    assert defaults_by_org
    for org_id, entries in defaults_by_org.items():
        assert len(entries) == 1, f"org {org_id} has multiple default datasources: {entries}"


def test_dashboard_provider_is_file_backed_and_read_only() -> None:
    data = yaml.safe_load(PROVIDER.read_text(encoding="utf-8"))
    provider = data["providers"][0]
    assert provider["type"] == "file"
    assert provider["editable"] is False
    assert provider["disableDeletion"] is True
    assert provider["options"]["path"] == "/var/lib/grafana/dashboards"


def test_dtmo_operations_dashboard_uses_bounded_aggregate_metrics() -> None:
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    assert dashboard["uid"] == "dtmo-operations"
    assert dashboard["editable"] is False
    expressions = [target["expr"] for panel in dashboard["panels"] for target in panel.get("targets", [])]
    assert "sum(rate(dtmo_http_requests_total[5m]))" in expressions
    assert any("dtmo_http_request_seconds_bucket" in expr for expr in expressions)
    assert any("dtmo_connector_runs_total" in expr for expr in expressions)
    assert all("payload" not in expr.lower() for expr in expressions)
    assert all("object_key" not in expr.lower() for expr in expressions)


def test_grafana_credentials_are_documented_as_external_inputs() -> None:
    env = ENV_EXAMPLE.read_text(encoding="utf-8")
    assert "GRAFANA_ADMIN_USER=<external-grafana-admin-user>" in env
    assert "GRAFANA_ADMIN_PASSWORD=<external-strong-grafana-password>" in env
    assert "GRAFANA_ADMIN_PASSWORD=admin" not in env
