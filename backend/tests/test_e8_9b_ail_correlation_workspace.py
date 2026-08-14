from __future__ import annotations

from dtmo.ail_correlation_workspace import (
    _JS,
    _PAGE,
    _indicator_from_external_id,
    _investigation_refs,
    router,
)
from dtmo.threat_workspace import router as threat_workspace_router


def test_workspace_routes_are_read_only_and_registered_on_canonical_router() -> None:
    local = {(route.path, ",".join(sorted(route.methods or []))) for route in router.routes}
    assert ("/api/v1/intelligence/{item_id}/ail-correlations", "GET") in local
    assert ("/ui/intelligence-workspace", "GET") in local
    assert all("POST" not in methods and "PATCH" not in methods and "DELETE" not in methods for _, methods in local)

    paths = [route.path for route in threat_workspace_router.routes]
    assert paths[0] == "/api/v1/intelligence/{item_id}/ail-correlations"
    assert paths.index("/ui/intelligence-workspace") < paths.index("/api/v1/intelligence/{item_id}/workspace")


def test_enhanced_workspace_contains_visible_privacy_bounded_correlation_panel() -> None:
    assert 'id="ail-correlation-panel"' in _PAGE
    assert "Investigation correlations" in _PAGE
    assert "Raw leak-content wordt niet weergegeven" in _PAGE
    assert "/ui/ail-correlation-workspace.js" in _PAGE
    assert "/ui/ail-correlation-workspace.css" in _PAGE
    assert "/ail-correlations" in _JS
    assert "Degraded evidence" in _JS
    assert "Geen exacte correlaties gevonden" in _JS
    assert "raw_payload" not in _JS
    assert "share_approved=true" not in _JS.lower()


def test_indicator_and_investigation_projection_remain_bounded() -> None:
    assert _indicator_from_external_id("domain:None:login.example") == ("domain", "login.example")
    raw = {
        "_dtmo_ail": {
            "investigation_references": [
                {"id": "case-1", "title": "must not surface"},
                {"id": "case-2"},
            ],
            "raw_content": "must not surface",
        }
    }
    assert _investigation_refs(raw) == [{"id": "case-1"}, {"id": "case-2"}]
