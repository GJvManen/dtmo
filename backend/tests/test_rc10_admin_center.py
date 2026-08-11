from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADMIN_CENTER = ROOT / "backend/dtmo/admin_center.py"
MAIN = ROOT / "backend/dtmo/main.py"


def test_administration_center_is_wired_as_navigation_only() -> None:
    text = ADMIN_CENTER.read_text(encoding="utf-8")
    main = MAIN.read_text(encoding="utf-8")
    assert '"/ui/administration"' in text
    assert "app.include_router(admin_center_router)" in main
    assert "@router.post" not in text
    assert "@router.patch" not in text
    assert "@router.delete" not in text


def test_administration_center_preserves_existing_authority_boundaries() -> None:
    text = ADMIN_CENTER.read_text(encoding="utf-8")
    for path in ("/ui/admin-sources", "/ui/source-center", "/ui/ciso-security", "/ui/share-approval", "/ui/auditor"):
        assert path in text
    assert "manage:connectors" in text
    assert "revoke-permissie" in text
    assert "afzonderlijke beslissingen" in text
    assert "Audit blijft read-only" in text
    assert "geen API-endpoint voor mutations" in text


def test_administration_center_has_basic_accessibility_landmarks() -> None:
    text = ADMIN_CENTER.read_text(encoding="utf-8")
    assert 'href="#content"' in text
    assert 'id="content"' in text
    assert 'aria-label="Beheergebieden"' in text
