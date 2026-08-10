from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_CENTER = ROOT / "backend/dtmo/source_center.py"
MAIN = ROOT / "backend/dtmo/main.py"


def test_source_center_is_wired_and_governed() -> None:
    text = SOURCE_CENTER.read_text(encoding="utf-8")
    main = MAIN.read_text(encoding="utf-8")
    assert '"/ui/source-center"' in text
    assert '"/api/v1/source-center/status"' in text
    assert "Permission.MANAGE_CONNECTORS" in text
    assert "Role.ADMIN not in principal.roles" in text
    assert "principal.is_service_account" in text
    assert "app.include_router(source_center_router)" in main


def test_source_center_exposes_bounded_health_and_schedule_context() -> None:
    text = SOURCE_CENTER.read_text(encoding="utf-8")
    for field in ("health_status", "last_success_at", "last_failure_at", "consecutive_failures", "isolated_until", "interval_seconds", "provenance"):
        assert field in text
    assert "secret_ref" not in text
    assert "raw_evidence" not in text
    assert "share_approved" not in text


def test_source_center_keeps_mutations_in_existing_control_plane() -> None:
    text = SOURCE_CENTER.read_text(encoding="utf-8")
    assert 'href="/ui/admin-sources"' in text
    assert "manage:connectors" in text
    assert "geen review- of share approval-recht" in text
    assert 'role="status"' in text
    assert 'href="#content"' in text
