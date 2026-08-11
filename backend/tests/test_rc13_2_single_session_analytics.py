from __future__ import annotations

from pathlib import Path

import yaml

from dtmo.rc13_analytics import single_session_design_system

ROOT = Path(__file__).resolve().parents[2]


def test_rc13_analytics_css_hides_separately_authenticated_grafana_embed() -> None:
    response = single_session_design_system()
    css = response.body.decode("utf-8")

    assert ".grafana-shell{display:none!important}" in css
    assert response.media_type == "text/css"
    assert response.headers["cache-control"] == "no-store"


def test_rc13_analytics_css_route_precedes_legacy_frontend_css() -> None:
    main = (ROOT / "backend/dtmo/main.py").read_text(encoding="utf-8")

    assert "from dtmo.rc13_analytics import router as rc13_analytics_router" in main
    assert main.index("app.include_router(rc13_analytics_router)") < main.index(
        "app.include_router(frontend_router)"
    )


def test_native_visual_analytics_remain_the_canonical_product_surface() -> None:
    page = (ROOT / "backend/dtmo/unified_console.py").read_text(encoding="utf-8")

    assert 'data-view-panel="analytics"' in page
    assert 'id="severity-chart"' in page
    assert 'id="source-chart"' in page
    assert 'id="connector-chart"' in page
    assert 'id="review-chart"' in page
    assert "Native console summary" in page


def test_grafana_security_boundary_is_not_weakened() -> None:
    compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
    grafana = compose["services"]["grafana"]

    assert grafana["environment"]["GF_AUTH_ANONYMOUS_ENABLED"] == "false"
    assert grafana["environment"]["GF_USERS_ALLOW_SIGN_UP"] == "false"
    assert grafana["environment"]["GF_SECURITY_ALLOW_EMBEDDING"] == "true"
