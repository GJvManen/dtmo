from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "backend/dtmo/main.py"
OPS = ROOT / "backend/dtmo/operations_ui.py"
PYPROJECT = ROOT / "pyproject.toml"


def test_rc10_workspace_is_wired_and_versioned() -> None:
    main = MAIN.read_text(encoding="utf-8")
    project = PYPROJECT.read_text(encoding="utf-8")
    assert "from dtmo.operations_ui import router as operations_ui_router" in main
    assert "app.include_router(operations_ui_router)" in main
    assert 'version="16.0.0rc10"' in main
    assert 'version = "16.0.0rc10"' in project


def test_operations_workspace_has_professional_navigation_contract() -> None:
    text = OPS.read_text(encoding="utf-8")
    assert "Operations Workspace" in text
    assert 'href="#main"' in text
    assert 'aria-label="Operations navigatie"' in text
    assert "Command palette" in text
    assert "Operational notifications" in text
    assert "Role workspaces" in text
    assert "/ui/admin-sources" in text
    assert "/ui/share-approval" in text
    assert "/ui/auditor" in text
    assert "/ui/ciso-security" in text


def test_operations_workspace_uses_real_runtime_endpoints_and_no_privileged_writes() -> None:
    text = OPS.read_text(encoding="utf-8")
    assert "fetch('/health'" in text
    assert "fetch('/connectors'" in text
    assert "fetch('/api/v1/admin/sources'" not in text
    assert "method:'POST'" not in text
    assert "method: 'POST'" not in text


def test_operations_workspace_preserves_accessibility_and_responsive_contracts() -> None:
    text = OPS.read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in text
    assert "@media(max-width:760px)" in text
    assert 'aria-haspopup="dialog"' in text
    assert 'aria-label="Command center views"' in text
    assert "event.metaKey||event.ctrlKey" in text
