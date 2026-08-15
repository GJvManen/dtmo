from fastapi.testclient import TestClient

from dtmo.main import app


def test_misp_workspace_is_real_runtime_surface_with_governance_boundaries() -> None:
    response = TestClient(app).get("/ui/misp-workspace")
    assert response.status_code == 200
    body = response.text
    assert "MISP Workspace" in body
    assert "Read-only ingest" in body
    assert "published=false" in body
    assert "geen review- of share approval-recht" in body
    assert "service accounts" in body
    assert "replay" in body
    assert "geen bewijs van lokale exposure of compromise" in body
    assert response.headers["cache-control"] == "no-store"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]


def test_misp_workspace_assets_are_served_without_secrets() -> None:
    client = TestClient(app)
    css = client.get("/ui/misp-workspace.css")
    script = client.get("/ui/misp-workspace.js")
    assert css.status_code == 200
    assert script.status_code == 200
    assert "misp_api_key" not in script.text
    assert "X-DTMO-API-Key" not in script.text
    assert "/misp-export" in script.text
    assert "/api/v1/intelligence/search" in script.text
