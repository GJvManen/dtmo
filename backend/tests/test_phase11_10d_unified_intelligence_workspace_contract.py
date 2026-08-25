from __future__ import annotations

from pathlib import Path

from dtmo.main import app

ROOT = Path(__file__).resolve().parents[2]


def test_existing_governed_intelligence_contracts_remain_mounted() -> None:
    paths = app.openapi()["paths"]
    assert "/api/v1/intelligence/search" in paths
    assert "/api/v1/intelligence/{item_id}/workspace" in paths
    assert "/api/v1/command-center" in paths


def test_unified_intelligence_workspace_uses_only_dtmo_api_boundaries() -> None:
    source = (ROOT / "frontend/src/UnifiedIntelligenceWorkspace.tsx").read_text(encoding="utf-8")
    app_source = (ROOT / "frontend/src/App.tsx").read_text(encoding="utf-8")
    styles = (ROOT / "frontend/src/unified-intelligence.css").read_text(encoding="utf-8")

    for marker in (
        "/api/v1/command-center",
        "/api/v1/intelligence/search?",
        "/api/v1/intelligence/${encodeURIComponent(result.id)}/workspace",
        "11.10q Functional recovery",
        "Read-only investigation",
        "Canonical DTMO persistence is unavailable",
        "Canonical detail unavailable",
        "Recent intelligence is read from canonical DTMO persistence",
        "Search uses the governed search projection",
        "Not approved for sharing",
        "Provenance chain",
        "Canonical recent view without fabricated content",
    ):
        assert marker in source

    assert '<Route path="/intelligence"' in app_source
    assert '<Route path="/intelligence/iocs"' in app_source
    assert "UnifiedIntelligenceWorkspace" in app_source
    assert ".intelligence-workspace-grid" in styles
    assert ".provenance-row" in styles
    assert "https://intelowl" not in source.lower()
    assert "https://opencti" not in source.lower()
    assert "https://misp" not in source.lower()


def test_search_and_detail_apis_preserve_server_side_read_authority() -> None:
    routes = (ROOT / "backend/dtmo/api/routes.py").read_text(encoding="utf-8")
    detail = (ROOT / "backend/dtmo/threat_workspace.py").read_text(encoding="utf-8")
    assert 'require_permission(Permission.READ_INTELLIGENCE)' in routes
    assert 'require_permission(Permission.READ_INTELLIGENCE)' in detail
    assert "search backend unavailable" in routes
    assert "provenance" in detail


def test_phase11_10d_package_is_professionally_discoverable() -> None:
    required = (
        "frontend/src/UnifiedIntelligenceWorkspace.tsx",
        "frontend/src/unified-intelligence.css",
        "docs/architecture/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE.md",
        "docs/user/UNIFIED_INTELLIGENCE_WORKSPACE.md",
        "docs/qa/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE_GATE.md",
        "backend/tests/test_phase11_10d_unified_intelligence_workspace_contract.py",
        "backend/tests/test_phase11_10d_unified_intelligence_workspace_browser.py",
        ".github/workflows/phase11-unified-intelligence-workspace.yml",
    )
    for path in required:
        assert (ROOT / path).is_file(), path
