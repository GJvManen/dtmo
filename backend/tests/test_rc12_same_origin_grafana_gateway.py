from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "docker-compose.yml"
GATEWAY = ROOT / "infrastructure/gateway/nginx.conf"


def test_grafana_is_configured_for_managed_subpath() -> None:
    compose = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    grafana = compose["services"]["grafana"]
    env = grafana["environment"]
    assert env["GF_AUTH_ANONYMOUS_ENABLED"] == "false"
    assert env["GF_SECURITY_ALLOW_EMBEDDING"] == "true"
    assert env["GF_SERVER_ROOT_URL"] == "%(protocol)s://%(domain)s/grafana/"
    assert env["GF_SERVER_SERVE_FROM_SUB_PATH"] == "true"


def test_gateway_routes_dtmo_and_grafana_on_one_browser_origin() -> None:
    compose = yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))
    gateway = compose["services"]["gateway"]
    assert "8080:8080" in gateway["ports"]
    assert gateway["read_only"] is True
    assert "no-new-privileges:true" in gateway["security_opt"]

    nginx = GATEWAY.read_text(encoding="utf-8")
    assert "location /grafana/" in nginx
    assert "proxy_pass http://grafana:3000" in nginx
    assert "location /" in nginx
    assert "proxy_pass http://api:8000" in nginx
    assert "X-Forwarded-Proto" in nginx
