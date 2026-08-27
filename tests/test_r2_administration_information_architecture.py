from pathlib import Path


def test_administration_route_uses_one_canonical_console():
    main = Path("frontend/src/main.tsx").read_text(encoding="utf-8")
    assert "import { AdministrationConsole } from './AdministrationConsole';" in main
    assert 'path="/administration" element={<AdministrationConsole />}' in main
    assert "<AdministrationWorkspace /><BundledPlatformReadiness />" not in main


def test_administration_console_exposes_stable_section_navigation():
    text = Path("frontend/src/AdministrationConsole.tsx").read_text(encoding="utf-8")
    for label in (
        "Overview",
        "Integrations",
        "Sources",
        "Identity",
        "Roles & Permissions",
        "Security & Audit",
    ):
        assert label in text

    assert "#integration-admin-title" in text
    assert "#identity-admin-title" in text
    assert 'data-admin-section=\\"role-catalog\\"' in text
    assert 'data-admin-section=\\"security-audit\\"' in text
    assert "route: '/collection'" in text


def test_navigation_preserves_server_authority_boundaries():
    text = Path("frontend/src/AdministrationConsole.tsx").read_text(encoding="utf-8")
    assert "Navigation does not grant authority" in text
    assert "server-authorized" in text
    assert "AdministrationSecurityAudit" in text
    assert "AdministrationWorkspace" in text
