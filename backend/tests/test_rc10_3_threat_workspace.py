from __future__ import annotations

from pathlib import Path

from dtmo.threat_workspace import _CVE_RE, _PAGE, _JS, router

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "backend/dtmo/main.py"


def test_workspace_router_exposes_read_only_detail_and_ui_routes() -> None:
    routes = {(route.path, ",".join(sorted(route.methods or []))) for route in router.routes}
    assert ("/api/v1/intelligence/{item_id}/workspace", "GET") in routes
    assert ("/ui/intelligence-workspace", "GET") in routes
    assert ("/ui/threat-workspace.css", "GET") in routes
    assert ("/ui/threat-workspace.js", "GET") in routes
    assert all("POST" not in methods and "PATCH" not in methods and "DELETE" not in methods for _, methods in routes)


def test_workspace_is_wired_into_application() -> None:
    text = MAIN.read_text()
    assert "from dtmo.threat_workspace import router as threat_workspace_router" in text
    assert "app.include_router(threat_workspace_router)" in text


def test_workspace_reuses_governed_search_and_session_scoped_test_identity() -> None:
    assert "/api/v1/intelligence/search" in _JS
    assert "/api/v1/intelligence/${encodeURIComponent(id)}/workspace" in _JS
    assert "sessionStorage.getItem('dtmo.apiKey')" in _JS
    assert "sessionStorage.setItem('dtmo.apiKey'" in _JS
    assert "X-DTMO-API-Key" in _JS
    assert "X-DTMO-Roles" in _JS
    assert "X-DTMO-Subject" in _JS


def test_workspace_preserves_human_governance_boundary() -> None:
    page = _PAGE.lower()
    assert "zoeken en onderzoeken verleent geen review- of share approval-recht" in page
    assert "/ui/share-approval" in _PAGE
    assert "review_status" in _JS
    assert "share_approved" in _JS
    for forbidden in ("/review", "/share-approval')", "method:'post'", "method:\"post\""):
        assert forbidden not in _JS.lower()


def test_cve_context_extraction_is_bounded_to_explicit_cve_identifiers() -> None:
    text = "Vendor advisory CVE-2026-12345 and cve-2025-9999; not-CVE-2026-12"
    assert sorted(match.upper() for match in _CVE_RE.findall(text)) == ["CVE-2025-9999", "CVE-2026-12345"]


def test_workspace_does_not_render_raw_sensitive_metadata_fields() -> None:
    source = (ROOT / "backend/dtmo/threat_workspace.py").read_text().lower()
    for forbidden in (
        'metadata_json["raw_object"]',
        '"authorization"',
        '"cookie"',
        '"request_body"',
        '"response_body"',
        '"student_id"',
        '"object_key"',
    ):
        assert forbidden not in source
