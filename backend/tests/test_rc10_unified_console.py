from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "backend/dtmo/main.py"
CONSOLE = ROOT / "backend/dtmo/unified_console.py"


def test_unified_console_owns_primary_root_before_legacy_frontend() -> None:
    main = MAIN.read_text(encoding="utf-8")
    assert "from dtmo.unified_console import router as unified_console_router" in main
    assert main.index("app.include_router(unified_console_router)") < main.index("app.include_router(frontend_router)")


def test_unified_console_contains_required_product_areas() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    for area in ("Overzicht", "Intelligence", "Bronnen & catalogus", "Visual analytics", "Administration", "Governance"):
        assert area in text
    assert '@router.get("/", response_class=HTMLResponse)' in text
    assert '@router.get("/ui/console", response_class=HTMLResponse)' in text


def test_catalog_is_not_hidden_and_run_flow_uses_existing_governed_endpoints() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    assert "/api/v1/admin/sources/catalog" in text
    assert "/api/v1/source-center/status" in text
    assert "/api/v1/admin/sources/catalog/bootstrap" in text
    assert "/api/v1/admin/sources/${encodeURIComponent(id)}/run" in text
    assert "/connectors/${encodeURIComponent(id)}/run" in text
    assert "/api/v1/admin/sources/${encodeURIComponent(id)}/validate" in text
    assert "interval_seconds" in text
    assert "enabled" in text


def test_visual_analytics_and_governance_boundary_are_integrated() -> None:
    text = CONSOLE.read_text(encoding="utf-8")
    assert "/api/v1/dashboards/summary" in text
    assert "severity-chart" in text
    assert "severity-table" in text
    assert "source-chart" in text
    assert "source-table" in text
    assert "connector-chart" in text
    assert "connector-table" in text
    assert "fallbackvisualisaties" in text
    assert "geen review- of share approval-recht" in text
    assert "separation of duties" in text
